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