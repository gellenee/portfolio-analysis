import pandas as pd
import requests
from pprint import pprint

# pull data from api, better for new changing data
def extract_prices_from_api(symbols: list[str])-> pd.DataFrame:
    
    headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
    }

    all_data = []
    base_url = "https://query2.finance.yahoo.com" # scheme + auth
    endpoint = "/v8/finance/chart/" #path
    for symbol in symbols:
        #get 22 days in timestamp
        r = requests.get(base_url + endpoint + symbol + "?interval=1d&range=1mo", headers=headers)
        #handle errors
        if r.status_code != 200:
            raise Exception(r.status_code)
        data = r.json()
        pprint(data)
        timestamps = data["chart"]["result"][0]["timestamp"]
        #price snapshots
        quotes = data["chart"]["result"][0]["indicators"]["quote"][0]
        #pair each timestamp with data
        for i, timestamp in enumerate(timestamps):
            all_data.append({
                "symbol": symbol,
                "date": pd.to_datetime(timestamp, unit='s'),
                "open_price": quotes['open'][i],
                "high_price": quotes['high'][i],
                "low_price": quotes['low'][i],
                "close_price": quotes['close'][i],
                "volume": quotes['volume'][i]
            })

    return pd.DataFrame(all_data)
        
#reads from local csv, better for static data
def extract_prices_from_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    return df


if __name__ == "__main__":
    print(extract_prices_from_api(["AAPL", "GOOGL"]))
