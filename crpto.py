import requests
import pandas as pd
import sqlite3

cryptoCurrency = []  # store all crypto data

def crptoCurrency():
    for pageNumber in range(1, 3):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=100&order=market_cap_desc&page={pageNumber}&sparkline=false"

        response = requests.get(url)

        if response.status_code == 200:
            responseData = response.json()
            cryptoCurrency.extend(responseData)
        else:
            print("API Error")

crptoCurrency()


cryptoDf = pd.DataFrame(cryptoCurrency)

if not cryptoDf.empty:

    filtered_df = cryptoDf[[
        "id", "symbol", "name", "current_price", "market_cap",
        "market_cap_rank", "total_volume", "circulating_supply",
        "total_supply", "ath", "atl", "last_updated"
    ]]

    # convert datetime to date
    filtered_df["last_updated"] = pd.to_datetime(filtered_df["last_updated"]).dt.date


# SQLITE
connectionSql = sqlite3.connect("project.db")

filtered_df.to_sql("cryptoData", if_exists="replace", con=connectionSql, index=False)

df = pd.read_sql("SELECT * FROM cryptoData", connectionSql)

print(df)
