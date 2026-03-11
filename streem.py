import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("project.db")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "SQL Query Runner", "Top 3 crypto price"],
        icons=["house", "gear"],
        menu_icon="cast",
        default_index=0
    )

# ---------------- HOME PAGE ----------------
if selected == "Home":
    st.title("Home")
    option = st.selectbox(
    "Select the query",
    ("oil_prices", "stock_prices", "cryptocurrencies","crypto_prices"),
)

    if(option == 'oil_prices'):
        df = pd.read_sql("select * from oilPrice",conn)
        st.dataframe(df)

    elif(option =="stock_prices"):
        option = st.selectbox(
    "select the finance",
    ("^GSPC", "^IXIC", "^NSEI"),)
        if(option == "^GSPC"):
            df = pd.read_sql("SELECT * FROM gspcData", conn)
            st.dataframe(df)
        elif(option == "^IXIC"):
            df = pd.read_sql("SELECT * FROM ixicData", conn)
            st.dataframe(df)
        elif(option == "^NSEI"):
            df = pd.read_sql("SELECT * FROM nseiData", conn)
            st.dataframe(df)

    elif(option == "cryptocurrencies"):
        df = pd.read_sql("SELECT * FROM historicalData", conn)
        st.dataframe(df)

    elif(option =="crypto_prices"):
        df = pd.read_sql("SELECT * FROM cryptoData", conn)
        st.dataframe(df, use_container_width=True)
# ---------------- SQL QUERY RUNNER ----------------
elif selected == "SQL Query Runner":
    st.title("🧠 SQL Query Runner")

    question = st.selectbox(
        "Select a Question",
        (
            # CRYPTO METADATA
            "1. Top 3 cryptocurrencies by market cap",
            "2. Coins where circulating supply exceeds 90%",
            "3. Coins within 10% of ATH",
            "4. Average market cap rank where volume > 1B",
            "5. Most recently updated coin",
            # CRYPTO PRICES
            "6. Highest Bitcoin price",
            "7. Average Ethereum price",
            "8. Bitcoin prices (latest month)",
            "9. Coin with highest average price",
            "10. Bitcoin % change",
            # OIL
            "11. Highest oil price",
            "12. Average oil price per year",
            "13. Oil prices during COVID crash",
            "14. Lowest oil price",
            "15. Oil volatility per year",
            # STOCKS
            "16. All stock prices",
            "17. Highest NASDAQ closing price",
            "18. Top 5 S&P500 biggest swings",
            "19. Monthly avg closing price",
            "20. Average NSEI volume 2024",
            # JOINS / COMPARISONS
            "21. Bitcoin vs Oil average price",
            "22. Bitcoin vs S&P500 same dates",
            "23. Ethereum vs NASDAQ",
            "24. Oil spike vs Bitcoin",
            "25. Top 3 crypto vs NIFTY",
            "26. S&P500 vs Oil",
            "27. Bitcoin vs Oil correlation data",
            "28. NASDAQ vs Ethereum trend",
            "29. Crypto + Stock join",
            "30. Multi-market comparison"
        )
    )

    query = None  # default

    # ---------------- CRYPTO ----------------
    if question == "1. Top 3 cryptocurrencies by market cap":
        query = "SELECT name, current_price, market_cap FROM cryptoData ORDER BY market_cap DESC LIMIT 3"

    elif question == "2. Coins where circulating supply exceeds 90%":
        query = "SELECT name, circulating_supply, total_supply FROM cryptoData WHERE circulating_supply >= 0.9*total_supply"

    elif question == "3. Coins within 10% of ATH":
        query = "SELECT name, current_price, ath FROM cryptoData WHERE current_price >= ath*0.9"

    elif question == "4. Average market cap rank where volume > 1B":
        query = "SELECT AVG(market_cap_rank) AS avg_rank FROM cryptoData WHERE total_volume > 1000000000"

    elif question == "5. Most recently updated coin":
        query = 'SELECT * FROM cryptoData ORDER BY last_updated DESC LIMIT 1'

    elif question == "6. Highest Bitcoin price":
        query = "SELECT MAX(current_price) AS highest_price FROM cryptoData WHERE symbol='btc'"

    elif question == "7. Average Ethereum price":
        query = "SELECT AVG(current_price) AS avg_price FROM cryptoData WHERE symbol='eth'"

    elif question == "8. Bitcoin prices (latest month)":
        # get latest month for BTC
        latest_month_df = pd.read_sql("SELECT MAX(last_updated) AS latest_date FROM cryptoData WHERE symbol='btc'", conn)
        if not latest_month_df.empty:
            latest_month = pd.to_datetime(latest_month_df.iloc[0]['latest_date']).strftime('%Y-%m')
            query = f"SELECT name, current_price, last_updated FROM cryptoData WHERE symbol='btc' AND strftime('%Y-%m',last_updated)='{latest_month}'"
        else:
            query = "SELECT name, current_price, last_updated FROM cryptoData WHERE 0=1"

    elif question == "9. Coin with highest average price":
        query = "SELECT symbol, AVG(current_price) AS avg_price FROM cryptoData GROUP BY symbol ORDER BY avg_price DESC LIMIT 1"

    elif question == "10. Bitcoin % change":
        query = """
        SELECT ((last_price - first_price)*100.0/first_price) AS percent_change
        FROM (
            SELECT 
                (SELECT current_price FROM cryptoData WHERE symbol='btc' ORDER BY last_updated ASC LIMIT 1) AS first_price,
                (SELECT current_price FROM cryptoData WHERE symbol='btc' ORDER BY last_updated DESC LIMIT 1) AS last_price
        )
        """

    # ---------------- OIL ----------------
    elif question == "11. Highest oil price":
        query = "SELECT MAX(Price) AS highest_price FROM oilPrice"

    elif question == "12. Average oil price per year":
        query = "SELECT strftime('%Y',Date) AS year, AVG(Price) AS avg_price FROM oilPrice GROUP BY year"

    elif question == "13. Oil prices during COVID crash":
        query = "SELECT * FROM oilPrice WHERE Date BETWEEN '2020-03-01' AND '2020-04-30'"

    elif question == "14. Lowest oil price":
        query = "SELECT MIN(Price) AS lowest_price FROM oilPrice"

    elif question == "15. Oil volatility per year":
        query = "SELECT strftime('%Y',Date) AS year, MAX(Price)-MIN(Price) AS volatility FROM oilPrice GROUP BY year"

    # ---------------- STOCKS ----------------
    elif question == "16. All stock prices":
        query = "SELECT * FROM cryptoData"

    elif question == "17. Highest NASDAQ closing price":
        query = "SELECT MAX(close) AS highest_close FROM 'gspcData'"

    elif question == "18. Top 5 S&P500 biggest swings":
        query = "SELECT date,(high-low) AS difference FROM gspcData ORDER BY difference DESC LIMIT 5"

    elif question == "19. Monthly avg closing price":
        query = "SELECT strftime('%Y-%m',date) AS month, AVG(close) AS avg_close FROM gspcData GROUP BY month"

    elif question == "20. Average NSEI volume 2024":
        query = "SELECT AVG(volume) AS avg_volume FROM gspcData where strftime('%Y',date)='2024'"

    # ---------------- JOINS ----------------
    elif question == "21. Bitcoin vs Oil average price":
        query = "SELECT AVG(c.current_price) AS bitcoin_avg, AVG(o.Price) AS oil_avg FROM cryptoData c JOIN oilPrice o"

    elif question == "22. Bitcoin vs S&P500 same dates":
        query = "SELECT c.last_updated AS date, c.current_price AS bitcoin_price, s.close AS sp500_close FROM cryptoData c JOIN stock_prices s"

    elif question == "23. Ethereum vs NASDAQ":
        query = "SELECT c.last_updated AS date, c.current_price AS ethereum_price, s.close AS nasdaq_close FROM cryptoData c JOIN gspcData s WHERE c.symbol='eth'"

    elif question == "24. Oil spike vs Bitcoin":
        query = "SELECT o.Date AS date, o.Price AS oil_price, c.current_price AS bitcoin_price FROM oilPrice o JOIN cryptoData c ORDER BY o.Price DESC LIMIT 20"

    elif question == "25. Top 3 crypto vs NIFTY":
        query = "SELECT c.last_updated AS date, c.symbol, c.current_price, s.close AS nifty_close FROM cryptoData c JOIN nseiData s "

    elif question == "26. S&P500 vs Oil":
        query = "SELECT strftime('%Y-%m',date) AS month, AVG(close) AS avg_close FROM gspcData GROUP BY month"

    elif question == "27. Bitcoin vs Oil correlation data":
        query = "SELECT c.last_updated AS date, c.current_price AS bitcoin_price, o.Price AS oil_price FROM cryptoData c JOIN oilPrice o WHERE c.symbol='btc'"

    elif question == "28. NASDAQ vs Ethereum trend":
        query = "SELECT s.date, s.close AS nasdaq_close, c.current_price AS ethereum_price FROM ixicData s JOIN cryptoData c WHERE c.symbol='eth'"

    elif question == "29. Crypto + Stock join":
        query = "SELECT c.last_updated AS date, c.symbol, c.current_price, s.ticker, s.close FROM cryptoData c JOIN gspcData s"

    elif question == "30. Multi-market comparison":
        query = "SELECT AVG(volume) AS avg_volume FROM gspcData where strftime('%Y',date)='2024'"

    # ---------------- RUN QUERY ----------------
    if query is not None:
        try:
            df = pd.read_sql(query, conn)
            st.subheader("Query Result")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error running query: {e}")

elif(selected=="Top 3 crypto price"):
        st.title("Top 3 crypto data")
        df = pd.read_sql("SELECT * FROM historicalData", conn)
        st.dataframe(df)
