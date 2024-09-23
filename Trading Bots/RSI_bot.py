import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
import datetime as dt
import time

import os

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')


def get_historical_data(symbol, start_date, end_date, interval='1d'):
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    data.dropna(inplace=True)
    return data

def apply_rsi_strategy(data, window=14):
    rsi = RSIIndicator(data['Close'], window=window)
    data['RSI'] = rsi.rsi()
    data['Signal'] = 0
    data['Signal'][rsi.rsi() < 30] = 1  # Buy signal
    data['Signal'][rsi.rsi() > 70] = -1  # Sell signal
    data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
    return data

def apply_ma_crossover_strategy(data, slow_window=50, fast_window=20):
    slow_ma = SMAIndicator(data['Close'], window=slow_window)
    fast_ma = SMAIndicator(data['Close'], window=fast_window)
    data['Slow_MA'] = slow_ma.sma_indicator()
    data['Fast_MA'] = fast_ma.sma_indicator()
    data['Signal'] = 0
    data['Signal'][fast_ma.sma_indicator() > slow_ma.sma_indicator()] = 1  # Buy signal
    data['Signal'][fast_ma.sma_indicator() < slow_ma.sma_indicator()] = -1  # Sell signal
    data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
    return data

def apply_ma_crossover_strategy(data, slow_window=50, fast_window=20):
    slow_ma = SMAIndicator(data['Close'], window=slow_window)
    fast_ma = SMAIndicator(data['Close'], window=fast_window)
    data['Slow_MA'] = slow_ma.sma_indicator()
    data['Fast_MA'] = fast_ma.sma_indicator()
    data['Signal'] = 0
    data['Signal'][fast_ma.sma_indicator() > slow_ma.sma_indicator()] = 1  # Buy signal
    data['Signal'][fast_ma.sma_indicator() < slow_ma.sma_indicator()] = -1  # Sell signal
    data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
    return data

def backtest_strategy(data):
    data['Market_Returns'] = data['Close'].pct_change()
    data['Strategy_Returns'] = data['Market_Returns'] * data['Position'].shift(1)
    cumulative_returns = (1 + data['Strategy_Returns']).cumprod() - 1
    return cumulative_returns

def place_order(symbol, qty, side, order_type='market', time_in_force='gtc'):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=order_type,
        time_in_force=time_in_force
    )

def place_bracket_order(symbol, qty, side, limit_price, take_profit, stop_loss):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            time_in_force='gtc',
            limit_price=limit_price,
            order_class='bracket',
            take_profit={'limit_price': take_profit},
            stop_loss={'stop_price': stop_loss}
        )
        print(f"Bracket order placed for {symbol}: {side} {qty} shares at ${limit_price}")
    except Exception as e:
        print(f"An error occurred while placing order for {symbol}: {e}")

def get_current_position(symbol):
    try:
        position = api.get_position(symbol)
        qty = float(position.qty)
        return qty
    except tradeapi.rest.APIError as e:
        # If no position exists, an exception is thrown
        if 'position does not exist' in str(e):
            return 0
        else:
            print(f"An error occurred while fetching position for {symbol}: {e}")
            return 0
        
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
import datetime as dt
import time
import threading
import os

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

# Function to get historical data
def get_historical_data(symbol, period='5d', interval='1m'):
    data = yf.download(symbol, period=period, interval=interval)
    data.dropna(inplace=True)
    return data

# RSI Strategy
def apply_rsi_strategy(data, window=14):
    rsi = RSIIndicator(data['Close'], window=window)
    data['RSI'] = rsi.rsi()
    data['Signal'] = 0
    data.loc[rsi.rsi() < 30, 'Signal'] = 1  # Buy signal
    data.loc[rsi.rsi() > 70, 'Signal'] = -1  # Sell signal
    data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
    print(data['RSI'])
    return data

# Function to place bracket orders
def place_bracket_order(symbol, qty, side, limit_price, take_profit, stop_loss):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            time_in_force='gtc',
            limit_price=limit_price,
            order_class='bracket',
            take_profit={'limit_price': take_profit},
            stop_loss={'stop_price': stop_loss}
        )
        print(f"Bracket order placed for {symbol}: {side} {qty} shares at ${limit_price}")
    except Exception as e:
        print(f"An error occurred while placing order for {symbol}: {e}")

# Function to get current position of a stock
def get_current_position(symbol):
    try:
        position = api.get_position(symbol)
        qty = float(position.qty)
        return qty
    except tradeapi.rest.APIError as e:
        # If no position exists, an exception is thrown
        if 'position does not exist' in str(e):
            return 0
        else:
            print(f"An error occurred while fetching position for {symbol}: {e}")
            return 0

# Main trading logic
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
import datetime as dt
import time
import threading

import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets' 

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')

# Function to get historical data
def get_historical_data(symbol, period='5d', interval='1m'):
    data = yf.download(symbol, period=period, interval=interval)
    data.dropna(inplace=True)
    return data

# RSI Strategy
def apply_rsi_strategy(data, window=14):
    rsi = RSIIndicator(data['Close'], window=window)
    data['RSI'] = rsi.rsi()
    data['Signal'] = 0
    data.loc[rsi.rsi() < 35, 'Signal'] = 1  # Buy signal
    data.loc[rsi.rsi() > 65, 'Signal'] = -1  # Sell signal
    data['Position'] = data['Signal'].replace(to_replace=0, method='ffill')
    print(data['RSI'])
    return data

# Function to place bracket orders
def place_bracket_order(symbol, qty, side, limit_price, take_profit, stop_loss):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='limit',
            time_in_force='gtc',
            limit_price=limit_price,
            order_class='bracket',
            take_profit={'limit_price': take_profit},
            stop_loss={'stop_price': stop_loss}
        )
        print(f"Bracket order placed for {symbol}: {side} {qty} shares at ${limit_price}")
    except Exception as e:
        print(f"An error occurred while placing order for {symbol}: {e}")

# Function to get current position of a stock
def get_current_position(symbol):
    try:
        position = api.get_position(symbol)
        qty = float(position.qty)
        return qty
    except tradeapi.rest.APIError as e:
        # If no position exists, an exception is thrown
        if 'position does not exist' in str(e):
            return 0
        else:
            print(f"An error occurred while fetching position for {symbol}: {e}")
            return 0

# Main trading logic
def run_trading_bot():
    stock_list = ['AAPL', 'MSFT', 'GOOGL', 'NVDA','AMZN', 'META']
    
    time_interval = 60  
    
    print("Starting trading bot...")
    try:
        while True:
            print(f"\nRunning trading cycle at {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for stock in stock_list:
                print(f"\nProcessing {stock}...")
                
                data = get_historical_data(stock, period='5d', interval='1m')
                data = apply_rsi_strategy(data)
            
                latest_signal = data['Signal'].iloc[-1]
                current_price = data['Close'].iloc[-1]
                qty_owned = get_current_position(stock)
                
                if latest_signal == 1:
                    if qty_owned == 0:
                        print(f"Buy signal detected for {stock}.")
                        investment_amount = 10000  
                        qty = int(investment_amount / current_price)
                        if qty > 0:
                            limit_price = round(current_price * 1.001, 2)  
                            take_profit = round(current_price * 1.02, 2)   
                            stop_loss = round(current_price * 0.98, 2)     
                            place_bracket_order(stock, qty=qty, side='buy', limit_price=limit_price,
                                                take_profit=take_profit, stop_loss=stop_loss)
                        else:
                            print(f"Insufficient funds to buy {stock}.")
                    else:
                        print(f"Already holding {qty_owned} shares of {stock}. No additional buy executed.")
                elif latest_signal == -1:
                    if qty_owned > 0:
                        print(f"Sell signal detected for {stock}.")
                        # Sell all owned shares
                        limit_price = round(current_price * 0.999, 2)  
                        take_profit = round(current_price * 0.98, 2)   
                        stop_loss = round(current_price * 1.02, 2)    
                        place_bracket_order(stock, qty=qty_owned, side='sell', limit_price=limit_price,
                                            take_profit=take_profit, stop_loss=stop_loss)
                    else:
                        print(f"Sell signal detected for {stock}, but no shares owned. No action taken.")
                else:
                    print(f"No action for {stock}. Latest signal: Hold.")
                
                time.sleep(1)
            
            print(f"Sleeping for {time_interval} seconds...")
            time.sleep(time_interval)
    except KeyboardInterrupt:
        print("\nTrading bot stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the trading bot
if __name__ == "__main__":
    run_trading_bot()

