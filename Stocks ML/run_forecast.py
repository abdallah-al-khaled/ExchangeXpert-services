import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

stock_symbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'meta', 'JPM', 'JNJ', 'V',
    'PG', 'DIS', 'MA', 'UNH', 'HD', 'PYPL', 'BAC', 'NFLX', 'XOM', 'VZ',
    'KO', 'PEP', 'MRK', 'INTC', 'T', 'PFE', 'CSCO', 'WMT', 'BA', 'NKE',
    'GS', 'MCD', 'ADBE', 'COST', 'IBM', 'CRM', 'ORCL', 'WFC', 'MDT', 'C',
]

# Fetch historical data for a single stock from Yahoo Finance
def fetch_stock_data(symbol, start_date='2015-01-01'):
    data = yf.download(symbol, start=start_date)
    data.reset_index(inplace=True)
    # Prophet requires columns as 'ds' and 'y'
    stock_data = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    return stock_data