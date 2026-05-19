import glob
import os
from pathlib import Path
import snowflake.connector
from cryptography.hazmat.primitives import serialization


# Definition for github actions
def load_private_key():
    
    #Load RSA private key from environment variable
    
    pem = os.environ["SNOWFLAKE_PRIVATE_KEY"].replace("\\n", "\n").encode()

    key = serialization.load_pem_private_key(
        pem,
        password=None,
    )

    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

# Definition for local run
"""def load_private_key():
    with open("snowflake_keys/snowflake_key.pem", "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)

    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )"""


# Helper function for multi statement sql files
def exec_sql_file(conn, path: str):
    sql = Path(path).read_text(encoding="utf-8").lstrip("\ufeff")

    statements = []
    for stmt in sql.split(";"):
        stmt = stmt.strip()

        # Skip empty lines
        if not stmt:
            continue

        # Skip comments
        if all(line.strip().startswith("--") or not line.strip()
               for line in stmt.splitlines()):
            continue

        statements.append(stmt)

    cur = conn.cursor()
    try:
        for stmt in statements:
            cur.execute(stmt)
    finally:
        cur.close()


def main():
    # --------------------------------------------------
    # Connect to Snowflake
    # --------------------------------------------------
    private_key = load_private_key()

    conn = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        private_key=private_key,
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"]
    )

    cur = conn.cursor()

    print(" Connected to Snowflake")

    exec_sql_file(conn, "sql/initDatabase.sql")
    exec_sql_file(conn, "sql/createTables.sql")
    

    # --------------------------------------------------
    # Load into table
    # --------------------------------------------------
    print(" Loading data into jugadores_futbol_db.raw")

    print("GITHUB_ENV:", os.environ.get("GITHUB_ENV"))
    print("Loaded DATASET_PATH:", os.getenv("DATASET_PATH"))

    cur.execute("USE SCHEMA JUGADORES_FUTBOL_DB.RAW;")


    path = os.getenv("DATASET_PATH")

    print(f"path = {path}")
    cur.execute(f"PUT file://{path}/players.csv @raw_data AUTO_COMPRESS=FALSE")

    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_PLAYERS LIKE JUGADORES_FUTBOL_DB.RAW.PLAYERS;")
    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_CLUBS LIKE JUGADORES_FUTBOL_DB.RAW.CLUBS;")
    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_COMPETITIONS LIKE JUGADORES_FUTBOL_DB.RAW.COMPETITIONS;")
    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_PLAYER_VALUATIONS LIKE JUGADORES_FUTBOL_DB.RAW.PLAYER_VALUATIONS;")
    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_APPEARANCES LIKE JUGADORES_FUTBOL_DB.RAW.APPEARANCES;")

    

    cur.execute("SELECT players_result")
    players_rows = cur.fetchone()[0]

    cur.execute("SELECT clubs_result")
    clubs_rows = cur.fetchone()[0]

    cur.execute("SELECT competitions_result")
    competitions_rows = cur.fetchone()[0]

    cur.execute("SELECT player_valuations_result")
    player_valuations_rows = cur.fetchone()[0]

    cur.execute("SELECT appearances_result")
    appearances_rows = cur.fetchone()[0]

    print(str(players_rows) + " rows inserted\n Load complete")

    
    # Cleanup
    cur.execute("DROP TABLE IF EXISTS TMP_PLAYERS")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()