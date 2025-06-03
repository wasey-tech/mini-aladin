import yfinance as yf
import pandas as pd
import ta
from flask import Flask, request, render_template

app = Flask(__name__)

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        return None
    
    # Fix: squeeze to 1D array for RSI and MACD
    close_prices = data['Close'].squeeze()

    data['rsi'] = ta.momentum.RSIIndicator(close=close_prices).rsi()
    data['macd'] = ta.trend.MACD(close=close_prices).macd()
    
    return data.tail(10).to_html()

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        ticker = request.form['ticker']
        start = request.form['start']
        end = request.form['end']
        data = fetch_data(ticker, start, end)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
