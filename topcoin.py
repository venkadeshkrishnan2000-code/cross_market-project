import requests
import pandas as pd
import sqlite3

topCoins = ["bitcoin", "ethereum"]

allData = []

if topCoins:
    for hisPrice in topCoins:
        url = f"https://api.coingecko.com/api/v3/coins/{hisPrice}/market_chart?vs_currency=inr&days=365"
        histResponse = requests.get(url)

        if histResponse.status_code == 200:
            historicalPriceresponse = histResponse.json()

            prices = historicalPriceresponse["prices"]

            historicalDf = pd.DataFrame(prices, columns=["timestamp", "price_inr"])

            historicalDf["date"] = pd.to_datetime(
                historicalDf["timestamp"], unit="ms"
            ).dt.date

            historicalDf["coin_id"] = hisPrice

            historicalDf = historicalDf[["coin_id", "date", "price_inr"]]

            allData.append(historicalDf)

# combine all coins
finalDf = pd.concat(allData, ignore_index=True)

connectionSql = sqlite3.connect("project.db")

finalDf.to_sql("historicalData", if_exists="replace", con=connectionSql, index=False)

df = pd.read_sql("SELECT * FROM historicalData", connectionSql)
print(df)
