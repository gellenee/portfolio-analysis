import sqlite3
import pandas as pd
import numpy as np

def compute_price_metrics():
   conn = sqlite3.connect("my_local.db")
   with open("data/db/fact_prices_return.sql") as f:
      daily_return_query = f.read()
   returns_df = pd.read_sql(daily_return_query, conn)

   #compute for volatility (standard deviation of returns)
   daily_volatility = returns_df.groupby("asset_id")["daily_return"].std()
   annual_volatility = daily_volatility*np.sqrt(252)
   print(annual_volatility)

   #cumulative values and returns
   returns_df["cumulative_value"] = returns_df.groupby("asset_id")["daily_return"].transform(lambda x: (1+x).cumprod())   
   returns_df["cumulative_return"] = returns_df["cumulative_value"] - 1
   
   # max drawdown is the difference from peak to a later trough
   returns_df["current_peak"] = returns_df.groupby("asset_id")["cumulative_value"].cummax()
   returns_df["drawdown"] = (returns_df["cumulative_value"] - returns_df["current_peak"]) / returns_df["current_peak"]
   drawdown_max = returns_df["drawdown"].min()

   print(returns_df)
   print(drawdown_max)

if __name__ == "__main__":
   compute_price_metrics()