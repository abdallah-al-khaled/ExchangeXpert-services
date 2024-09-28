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

# Configure and train Prophet model for each stock
def train_prophet(stock_data, stock_name, yearly_seasonality=True, daily_seasonality=False, holidays=None, changepoint_prior_scale=0.05):
    # Initialize Prophet with customized parameters
    m = Prophet(yearly_seasonality=yearly_seasonality,
                    daily_seasonality=daily_seasonality,
                    holidays=holidays,
                    changepoint_prior_scale=changepoint_prior_scale)

    # Fit the model to stock data
    m.fit(stock_data)

    # Forecast for the next 365 days
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    # Plot forecast
    fig = m.plot(forecast)
    plt.title(f'Forecast for {stock_name}')
    plt.show()

    # Return the forecast for further analysis
    return forecast