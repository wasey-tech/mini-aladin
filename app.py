from flask import Flask, render_template, request
from datetime import datetime
from stock_data_fetcher import fetch_stock_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    result_table = None

    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')

        try:
            if not ticker or not start_date or not end_date:
                raise ValueError("All fields are required.")

            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")

            if start_dt >= end_dt:
                raise ValueError("Start date must be before end date.")

            df = fetch_stock_data(ticker, start_date, end_date)
            result_table = df.to_html(classes='table table-bordered table-striped table-sm', justify='center')

        except Exception as e:
            error = str(e)

    return render_template('index.html', error=error, table=result_table, max_date=datetime.today().strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(debug=True)
