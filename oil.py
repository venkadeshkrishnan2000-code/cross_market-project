import pandas as pd
import sqlite3


def oilPrice():
    oilDataDf = pd.read_csv("./oilPrice.csv")
    filtered = oilDataDf[(oilDataDf['Date'] >= '2020-01-01') & (oilDataDf['Date'] <= '2026-02-01')]
    filtered.to_csv("oilPrice.csv", index=False)

    connectionSql = sqlite3.connect("project.db")
    cursor = connectionSql.cursor()
    filtered.to_sql("oilPrice",if_exists="replace",con=connectionSql)
    df = pd.read_sql("select * from oilPrice",connectionSql)
    print(df)

oilPrice()
