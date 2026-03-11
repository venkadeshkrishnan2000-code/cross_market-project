import requests
import pandas as pd
import yfinance as yf

cryptoCurrency = [] #store all crypto Data
topCoins = []
historicalPrice =[] #store top coins data

def crptoCurrency():
    for pageNumber in range(1, 3):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page={pageNumber}&order=market_cap_desc&page=1&sparkline=False"
        response = requests.get(url)
        if response.status_code == 200:
            responseData = response.json()
            cryptoCurrency.extend(responseData)
            cryptoDf = pd.DataFrame(cryptoCurrency)
        if(cryptoCurrency):
             filtered_df = cryptoDf[[
             "id", "symbol", "name", "current_price", "market_cap",
             "market_cap_rank", "total_volume", "circulating_supply",
             "total_supply", "ath", "atl", "last_updated"
             ]]

             # Extract only date from last_updated
             filtered_df["last_updated"] = pd.to_datetime(filtered_df["last_updated"]).dt.date
             print(filtered_df)
             ids = cryptoDf["id"]
             topCoins.extend(ids)

        else:
            print(f"{len(cryptoCurrency)} - count of crypto currency")



if(topCoins):
    for hisPrice in topCoins:
        url = f"https://api.coingecko.com/api/v3/coins/{hisPrice}/market_chart?vs_currency=inr&days=365"
        histResponse = requests.get(url)

        if histResponse.status_code == 200:
            historicalPriceresponse = histResponse.json()

            prices = historicalPriceresponse["prices"]

            historicalDf = pd.DataFrame(prices, columns=["timestamp", "price_usd"])

            historicalDf["date"] = pd.to_datetime(historicalDf["timestamp"], unit="ms").dt.date
            historicalDf["coin_id"] = hisPrice

            historicalDf = historicalDf[["coin_id", "date", "price_usd"]]

            print(historicalDf)

def oilPrice():
    oilDataDf = pd.read_csv("./oilPrice.csv")
    filtered = oilDataDf[(oilDataDf['Date'] >= '2020-01-01') & (oilDataDf['Date'] <= '2026-02-01')]
    filtered.to_csv("oilPrice.csv", index=False)



def finance():
    #inputs
    tickersList = ["^GSPC", "^IXIC", "^NSEI"]
    startDate = "2021-01-01"
    endDate = "2026-02-12"

    #extract the data
    stockData = yf.download(tickersList, start=startDate, end=endDate, group_by="ticker")
    gspcData = stockData['^GSPC'].reset_index()
    ixicData = stockData['^GSPC'].reset_index()
    nseiData = stockData['^GSPC'].reset_index()
    print(gspcData)
    print(ixicData)
    print(nseiData)
    return(gspcData,ixicData,nseiData)

finance()