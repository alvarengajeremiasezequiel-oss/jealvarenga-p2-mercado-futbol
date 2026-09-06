import os
from pathlib import Path
import time
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv


dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path, override=True)

def load_private_key():
    # Use the private key from the environment variable (CI) or from the local file
    pem_env = os.environ.get("SNOWFLAKE_PRIVATE_KEY")
    if pem_env:
        pem = pem_env.replace("\\n", "\n").encode()
    else:
        with open("snowflake_keys/snowflake_key.pem", "rb") as f:
            pem = f.read()

    key = serialization.load_pem_private_key(pem, password=None)

    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


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
        last_output = cur.fetchone()[0]
    finally:
        cur.close()
    return last_output


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
    # Load into raw tables
    # --------------------------------------------------
    print(" Loading data into jugadores_futbol_db.raw")

    cur.execute("USE SCHEMA JUGADORES_FUTBOL_DB.RAW;")

    path = os.getenv("DATASET_PATH")

    cur.execute(f"PUT file://{path}/players.csv @raw_data AUTO_COMPRESS=FALSE")
    players_rows =           exec_sql_file(conn, "sql/raw/populatePlayers.sql")

    cur.execute(f"PUT file://{path}/clubs.csv @raw_data AUTO_COMPRESS=FALSE")
    clubs_rows =             exec_sql_file(conn, "sql/raw/populateClubs.sql")

    cur.execute(f"PUT file://{path}/competitions.csv @raw_data AUTO_COMPRESS=FALSE")
    competitions_rows =      exec_sql_file(conn, "sql/raw/populateCompetitions.sql")

    cur.execute(f"PUT file://{path}/player_valuations.csv @raw_data AUTO_COMPRESS=FALSE")
    player_valuations_rows = exec_sql_file(conn, "sql/raw/populatePlayerValuations.sql")

    cur.execute(f"PUT file://{path}/appearances.csv @raw_data AUTO_COMPRESS=FALSE")
    appearances_rows =       exec_sql_file(conn, "sql/raw/populateAppearances.sql")

    print("Raw table players:           " + str(players_rows)           + " rows inserted\n Load complete")
    print("Raw table clubs:             " + str(clubs_rows)             + " rows inserted\n Load complete")
    print("Raw table competitions:      " + str(competitions_rows)      + " rows inserted\n Load complete")
    print("Raw table player_valuations: " + str(player_valuations_rows) + " rows inserted\n Load complete")
    print("Raw table appearances:       " + str(appearances_rows)       + " rows inserted\n Load complete")

    # Raw temp tables cleanup
    cur.execute("DROP TABLE IF EXISTS TMP_PLAYERS")
    cur.execute("DROP TABLE IF EXISTS TMP_CLUBS")
    cur.execute("DROP TABLE IF EXISTS TMP_COMPETITIONS")
    cur.execute("DROP TABLE IF EXISTS TMP_PLAYER_VALUATIONS")
    cur.execute("DROP TABLE IF EXISTS TMP_APPEARANCES")

    
    # --------------------------------------------------
    # Load into silver and gold tables
    # --------------------------------------------------

    cur.execute(
    """
        SELECT COUNT(*) AS num_tables
        FROM JUGADORES_FUTBOL_DB.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'SILVER';
    """)
    silver_num_tables = cur.fetchone()[0]

    if ( players_rows | clubs_rows |competitions_rows |
        player_valuations_rows | appearances_rows |
        (silver_num_tables != 4)):
        print(time.strftime("%Y-%m-%d %H:%M:%S"), "- Updating silver and gold layer tables...")
        exec_sql_file(conn, "sql/silver/populateSilver.sql")
        exec_sql_file(conn, "sql/gold/populateGold.sql")
        
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()