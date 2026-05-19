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

    # --------------------------------------------------
    # Load into table
    # --------------------------------------------------
    print(" Loading data into jugadores_futbol_db.raw")


    cur.execute("USE SCHEMA JUGADORES_FUTBOL_DB.RAW;")

    cur.execute("CREATE OR REPLACE TEMP TABLE TMP_PLAYERS LIKE JUGADORES_FUTBOL_DB.RAW.PLAYERS;")
    cur.execute(
        """
        COPY INTO TMP_PLAYERS
        FROM @raw_data
        FILE_FORMAT = (FORMAT_NAME = ff_jugadores_csv)
        FILES = ('players.csv')
        ON_ERROR = 'ABORT_STATEMENT';
        """
    )
    cur.execute(
        """
        MERGE INTO PLAYERS t
        USING STAGING_PLAYERS s
        ON t.player_id = s.player_id
        WHEN NOT MATCHED THEN
            INSERT ALL BY NAME;
        """
    )

    cur.execute(
        """
        SELECT
            "number of rows inserted"
        FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
        """
    )
    rows_inserted = cur.fetchone()[0]

    print(str(rows_inserted) + "rows inserted\n Load complete")

    
    # Cleanup
    cur.execute("DROP TABLE IF EXISTS TMP_PLAYERS")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()