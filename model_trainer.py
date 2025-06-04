import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from config import MODEL_PATH
import os

def create_sequences(data, seq_length):
    """Create input sequences for LSTM model"""
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

def prepare_lstm_data(df, seq_length=60):
    """Prepare data for LSTM model"""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    
    X, y = create_sequences(scaled_data, seq_length)
    
    # Reshape for LSTM [samples, time steps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    return X, y, scaler

def build_lstm_model(input_shape):
    """Build advanced LSTM model"""
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(units=100, return_sequences=True, input_shape=input_shape))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.LSTM(units=100, return_sequences=True))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.LSTM(units=50))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(units=1))
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

def train_model(df):
    """Train LSTM model and save it"""
    X, y, scaler = prepare_lstm_data(df)
    
    # Split data (80% train, 20% validation)
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]
    
    model = build_lstm_model((X_train.shape[1], 1))
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    # Save model
    model.save(MODEL_PATH)
    
    return model, scaler, history