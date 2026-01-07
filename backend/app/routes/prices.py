from fastapi import APIRouter
from create_engine import sqlalchemy
router = APIRouter()

engine = create_engine("sqlite3://my_local.db")
@router.get("/prices")
def get_prices():
    fact_prices_df = pd.read_sql("SELECT * FROM fact_prices ", engine)
