import os
import json
import asyncio
import websockets
import pandas as pd
import requests
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

df = pd.read_csv('nasdaq.csv')
stock_symbols = set(df['Symbol'].tolist())  # Use a set for fast lookup
print(stock_symbols)

APCA_API_KEY_ID = os.getenv('APCA_API_KEY_ID')
APCA_API_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = "https://paper-api.alpaca.markets"

ws_url = "wss://stream.data.alpaca.markets/v1beta1/news"

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

def analyze_sentiment(text):
    results = nlp(text)
    print(results)
    if results[0]['label'] == 'Positive' and results[0]['score'] > 0.85:
        return 2  # Positive sentiment
    elif results[0]['label'] == 'Negative' and results[0]['score'] > 0.85:
        return 0 
    else:
        return 1
    
def get_current_price(symbol):
    url = f"https://data.alpaca.markets/v2/stocks/bars/latest?symbols={symbol}&feed=iex"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": APCA_API_KEY_ID,
        "APCA-API-SECRET-KEY": APCA_API_SECRET_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['bars'][symbol]['c']

def submit_bracket_order(symbol, qty, side, take_profit_price, stop_loss_price):
    url = f"{BASE_URL}/v2/orders"
    headers = {
        "APCA-API-KEY-ID": APCA_API_KEY_ID,
        "APCA-API-SECRET-KEY": APCA_API_SECRET_KEY,
        "Content-Type": "application/json"
    }
    
    # Define bracket order payload
    order_data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,  # "buy" or "sell"
        "type": "market",  
        "time_in_force": "gtc",  
        "order_class": "bracket",
        "take_profit": {
            "limit_price": take_profit_price 
        },
        "stop_loss": {
            "stop_price": stop_loss_price 
        }
    }

    # Send the POST request to Alpaca API
    response = requests.post(url, headers=headers, json=order_data)
    return response.json()