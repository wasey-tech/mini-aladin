import yfinance as yf
import pandas as pd
import ta

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        print("❌ No data found.")
        return None
    return data

def add_indicators(data):
    data = data.copy()
    data['rsi'] = ta.momentum.RSIIndicator(close=data['Close']).rsi()
    data['macd'] = ta.trend.MACD(close=data['Close']).macd()
    return data

def main():
    ticker = input("Enter the stock ticker symbol (e.g., TSLA, AMZN, RELIANCE.NS, ^NSEI): ")
    start = input("Enter the start date (YYYY-MM-DD): ")
    end = input("Enter the end date (YYYY-MM-DD): ")

    data = fetch_data(ticker, start, end)
    if data is not None:
        data = add_indicators(data)
        print(data.tail())

if __name__ == "__main__":
    main()
