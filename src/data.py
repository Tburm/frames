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
    df = pd.read_sql("""
        select 
            ts,
            market_symbol,
            volume
        from
            base_mainnet.fct_perp_market_stats_daily
        where
            ts > now() - interval '14 days'
        order by 2, 1
    """, conn)
    conn.close()
    return df

def get_oi():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT ts,
            market_symbol,
            size_usd
        FROM base_mainnet.fct_perp_market_history
        where
            ts > now() - interval '14 days'
        order by market_symbol, ts
    """, conn)

    # add latest points
    latest_ts = df['ts'].max()
    
    latest_data = df[df['ts'] == latest_ts]
    missing_symbols = set(df['market_symbol']) - set(latest_data['market_symbol'])

    new_rows = []
    for symbol in missing_symbols:
        most_recent_data = df[df['market_symbol'] == symbol].iloc[-1]
        new_row = {'ts': latest_ts, 'market_symbol': symbol, 'size_usd': most_recent_data['size_usd']}
        new_rows.append(new_row)

    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)    

    conn.close()
    return df