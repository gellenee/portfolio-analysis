from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from extract import extract_prices_from_api
from transform import transform_prices
from load import load_dim_asset, load_dim_date, load_fact_prices
def run_prices_etl():
    #local dev uses sqlite tables, reading schema
    conn = sqlite3.connect("my_local.db")
    with open("db/schema.sql") as f:
        conn.executescript(f.read())
    conn.close()

    #db connection used to reading and writing to sql tables
    engine = create_engine("sqlite:///my_local.db")
    
    symbols = ["AAPL", "MSFT"]
    # extract new data from api/csv
    raw_prices_df = extract_prices_from_api(symbols)
    # load new data to dimension table
    load_dim_asset(raw_prices_df, engine)
    load_dim_date(raw_prices_df, engine)
    # read data from dim table

    dim_asset_df = pd.read_sql("SELECT symbol, asset_id FROM dim_asset", engine)
    dim_date_df = pd.read_sql("SElECT date_id, date FROM dim_date", engine)

    # transform raw data to fact table schema
    fact_df = transform_prices(raw_prices_df, dim_asset_df, dim_date_df)
    # load new data to fact table
    load_fact_prices(fact_df, engine)
    fact_prices_df = pd.read_sql("SELECT * FROM fact_prices", engine)
    print(fact_prices_df)
if __name__ == "__main__":
    run_prices_etl()
