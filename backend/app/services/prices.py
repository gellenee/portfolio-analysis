# thin wrapper to read from db

import pandas as pd
from sqlachemy import create_engine

engine = create_engine("sqlite3://my_local.db")

def list_prices(engine):

    pd.read_sql(query, conn)
