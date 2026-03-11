import yfinance as yf
import sqlite3
import pandas as pd


def finance():
    # inputs
    tickersList = ["^GSPC", "^IXIC", "^NSEI"]
    startDate = "2021-01-01"
    endDate = "2026-02-12"

    # extract data
    stockData = yf.download(tickersList, start=startDate, end=endDate, group_by="ticker")

    gspcData = stockData['^GSPC'].reset_index()
    ixicData = stockData['^IXIC'].reset_index()
    nseiData = stockData['^NSEI'].reset_index()
    print(gspcData)
    return gspcData, ixicData, nseiData


gspcData, ixicData, nseiData = finance()


connectionSql = sqlite3.connect("project.db")

gspcData.to_sql("gspcData", if_exists="replace", con=connectionSql, index=False)
ixicData.to_sql("ixicData", if_exists="replace", con=connectionSql, index=False)
nseiData.to_sql("nseiData", if_exists="replace", con=connectionSql, index=False)

df = pd.read_sql("SELECT * FROM gspcData", connectionSql)
print(df)
