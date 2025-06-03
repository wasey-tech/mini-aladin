from flask import Flask, request, render_template
import yfinance as yf
import pandas as pd
import ta
import os

app = Flask(__name__)

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        return None
    data['rsi'] = ta.momentum.RSIIndicator(close=data['Close']).rsi().squeeze()
    data['macd'] = ta.trend.MACD(close=data['Close']).macd().squeeze()
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
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 so external connections work on hosting platforms
    app.run(host='0.0.0.0', port=port, debug=True)
