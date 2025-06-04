import pandas as pd

def moving_average_signal(df):
    """Generate signals based on moving average crossover"""
    df['Signal'] = 0
    df.loc[df['MA20'] > df['MA50'], 'Signal'] = 1  # Buy signal
    df.loc[df['MA20'] < df['MA50'], 'Signal'] = -1  # Sell signal
    return df

def rsi_signal(df):
    """Generate signals based on RSI"""
    df['RSI_Signal'] = 0
    df.loc[df['RSI'] < 30, 'RSI_Signal'] = 1  # Oversold - Buy signal
    df.loc[df['RSI'] > 70, 'RSI_Signal'] = -1  # Overbought - Sell signal
    return df

def bollinger_bands_signal(df):
    """Generate signals based on Bollinger Bands"""
    df['BB_Signal'] = 0
    df.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 1  # Oversold - Buy signal
    df.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = -1  # Overbought - Sell signal
    return df