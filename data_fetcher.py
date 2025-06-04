import yfinance as yf
from config import HISTORY_PERIOD

def fetch_stock_data(ticker):
    """Fetch historical stock data"""
    stock = yf.Ticker(ticker)
    data = stock.history(period=HISTORY_PERIOD)
    return data[['Open', 'High', 'Low', 'Close', 'Volume']]