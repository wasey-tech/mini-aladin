import numpy as np
import tensorflow as tf
import pandas as pd
from config import MODEL_PATH
from data_fetcher import fetch_stock_data
from data_processor import clean_data
from technical_indicators import add_technical_indicators
from trading_strategies import moving_average_signal, rsi_signal, bollinger_bands_signal
from model_trainer import train_model, prepare_lstm_data

def predict_stock(ticker):
    """Main prediction pipeline"""
    # Fetch and process data
    df = fetch_stock_data(ticker)
    df = clean_data(df)
    df = add_technical_indicators(df)
    
    # Train model (in real app, you'd load pre-trained)
    model, scaler, _ = train_model(df)
    
    # Prepare prediction data
    seq_length = 60
    scaled_data = scaler.transform(df['Close'].values.reshape(-1, 1))
    X_pred = scaled_data[-seq_length:]
    X_pred = np.reshape(X_pred, (1, seq_length, 1))
    
    # Make prediction
    predicted_price = scaler.inverse_transform(model.predict(X_pred))[0][0]
    last_price = df['Close'].iloc[-1]
    
    # Calculate entry and stop loss
    entry_point = last_price * 0.99  # 1% below current
    stop_loss = last_price * 0.95   # 5% stop loss
    
    # Apply trading strategies
    df = moving_average_signal(df)
    df = rsi_signal(df)
    df = bollinger_bands_signal(df)
    
    # Combine signals
    df['Final_Signal'] = df['Signal'] + df['RSI_Signal'] + df['BB_Signal']
    
    # Current signal
    current_signal = df['Final_Signal'].iloc[-1]
    
    # Create chart data
    chart_data = df[['Close', 'MA20', 'MA50']].tail(100).reset_index(drop=True)
    
    return {
        'ticker': ticker,
        'current_price': round(last_price, 2),
        'predicted_price': round(predicted_price, 2),
        'entry_point': round(entry_point, 2),
        'stop_loss': round(stop_loss, 2),
        'signal': "BUY" if current_signal > 0 else "SELL" if current_signal < 0 else "HOLD",
        'chart_data': {
            'Close': chart_data['Close'].tolist(),
            'MA20': chart_data['MA20'].tolist(),
            'MA50': chart_data['MA50'].tolist()
        }
    }