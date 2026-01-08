from fastapi import APIRouter, Depends
import pandas as pd
from sqlalchemy import create_engine
from pprint import pprint
from pathlib import Path

BASE_DIR = Path("backend/app/routes").parents[3].resolve()
print(BASE_DIR)
DB_PATH = BASE_DIR / "my_local.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

router = APIRouter()

#dependency injection 
def get_engine():
    return engine

@router.get("/prices")
def get_prices(engine = Depends(get_engine)):
    # returns a dict with key price and value of a list containing a dict of prices
    query = """
    WITH ranked AS (
    SELECT
        fp.date_id, fp.asset_id, da.symbol, dd.date,
        fp.open_price, fp.high_price, fp.low_price, fp.close_price, fp.volume,
        ROW_NUMBER() OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id DESC) as rn
    FROM fact_prices fp
    JOIN dim_asset da ON da.asset_id = fp.asset_id
    JOIN dim_date dd ON dd.date_id = fp.date_id
    )
    SELECT *
    FROM ranked
    WHERE rn <= 30
    ORDER BY asset_id, date_id;
    """
    prices_df = pd.read_sql(query, engine)
    prices = prices_df.to_dict("records")
    return {"prices": prices}

if __name__ == "__main__":
    pprint(get_prices())
