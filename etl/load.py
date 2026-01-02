import pandas as pd
def load_dim_asset(raw_df: pd.DataFrame, engine ):
    # get entries from table
    existing_df = pd.read_sql("SELECT symbol FROM dim_asset ", engine)
    # convert new entires, no asset_id since surrogate key
    assets_df = (
        raw_df[["symbol"]]
        .drop_duplicates()
        .assign(
            asset_name = None,
            asset_type = "stock",
            currency = "USD"
        )
    )
    #only add assets that dont belong in the table already
    new_assets_df = assets_df[~assets_df["symbol"].isin(existing_df["symbol"])]
    if not new_assets_df.empty:
        new_assets_df.to_sql(
            "dim_asset",
            engine,
            if_exists = "append", 
            index= False)

def load_dim_date(raw_df: pd.DataFrame, engine ):
    # ensure date column is datetime
    raw_df['date'] = pd.to_datetime(raw_df['date'])
    # get entries from table
    existing_df = pd.read_sql("SELECT date FROM dim_date ", engine)
    # convert new entires to dim_date schema
    dates_df = (
        raw_df[["date"]]
        .drop_duplicates()
        .assign(
            date_id = lambda x: x['date'].dt.strftime('%Y%m%d').astype(int),
            year = lambda x: x['date'].dt.year,
            quarter = lambda x: (x["date"].dt.month-1)//3+1,
            month = lambda x: x['date'].dt.month,
            day = lambda x: x['date'].dt.day,
            day_of_week=lambda x: x['date'].dt.weekday,
        )
    )
    #only add assets that dont belong in the table already
    new_dates_df = dates_df[~dates_df["date"].isin(existing_df["date"])]
    if not new_dates_df.empty:
        new_dates_df.to_sql(
            "dim_date",
            engine,
            if_exists = "append", 
            index= False)
        
def load_fact_prices(fact_df, engine):
    existing = pd.read_sql("SELECT asset_id, date_id FROM fact_prices", engine)
    # check for duplicates based on date_id and asset_id
    new_fact_prices_df = (
    fact_df
    .merge(
        existing[['date_id', 'asset_id']],
        on=['date_id', 'asset_id'],
        how='left',
        indicator=True
    )
    .query('_merge == "left_only"') # chooses rows that don't exist in both
    .drop(columns=['_merge'])       
    )

    if not new_fact_prices_df.empty:
        new_fact_prices_df.to_sql(
            "fact_prices",
            engine,
            if_exists ="append",
            index = False)

    