import pandas as pd

def clean_data(df):
    """Clean and prepare stock data"""
    df = df.dropna()
    df = df[~df.index.duplicated(keep='first')]
    return df