import yfinance as yf
import ta
import pandas as pd

def fetch_stock_data(ticker, start_date, end_date):
    ticker = ticker.strip().upper()
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        raise ValueError("No data found for your query. Please check the ticker symbol and date range.")

    close_series = df['Close'].astype(float)

    df['RSI'] = ta.momentum.RSIIndicator(close=close_series).rsi()
    macd = ta.trend.MACD(close=close_series)
    df['MACD'] = macd.macd()
    df['Signal Line'] = macd.macd_signal()

    return df[['Close', 'RSI', 'MACD', 'Signal Line']].dropna()
