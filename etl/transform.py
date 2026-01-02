import pandas as pd

def transform_prices(raw_data_df: pd.DataFrame, dim_asset_df: pd.DataFrame, dim_date_df: pd.DataFrame)-> pd.DataFrame:
    """
    Transform raw prices to fact_prices schema
    args:
        raw_data_df: new data extracted
        dim_asset_df: contains existing assets from asset dimension table
        dim_data_df: contains existing from date dimension table
    """
    raw_data_df["symbol"] = raw_data_df["symbol"].str.upper()
    raw_data_df['date'] = pd.to_datetime(raw_data_df['date'])
    dim_date_df['date'] = pd.to_datetime(dim_date_df['date'])
    #adding an asset_id to extracted prices, left keeps data from raw_df with no symbol match
    raw_data_df = raw_data_df.merge(dim_asset_df[["symbol", "asset_id"]], on="symbol", how = "left")
    # merge with dim_date_df to get date_id for fact table
    raw_data_df = raw_data_df.merge(dim_date_df[["date_id", "date"]], on="date", how = "left")
    fact_df = raw_data_df[["date_id", "asset_id", "open_price", "high_price", "low_price", "close_price","volume"]]
    return fact_df

