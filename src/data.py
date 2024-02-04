import os
from dotenv import load_dotenv
import sqlalchemy
import pandas as pd

load_dotenv()


## set up db
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def get_connection():
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = sqlalchemy.create_engine(connection_string)
    conn = engine.connect()
    return conn

## queries
def get_volume():
    conn = get_connection()
    query = "SELECT * FROM volume"
    df = pd.read_sql("""
        select 
            ts,
            volume
        from
            base_mainnet.fct_perp_stats_daily
        where
            ts > now() - interval '14 days'
        order by ts 
    """, conn)
    conn.close()
    return df