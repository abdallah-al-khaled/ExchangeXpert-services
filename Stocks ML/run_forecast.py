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