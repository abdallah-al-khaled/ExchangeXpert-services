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

async def authenticate_and_subscribe(ws):
    # Authenticate with Alpaca's WebSocket
    auth_msg = {"action": "auth", "key": APCA_API_KEY_ID, "secret": APCA_API_SECRET_KEY}
    await ws.send(json.dumps(auth_msg))

    # Subscribe to all news feeds
    subscribe_msg = {"action": "subscribe", "news": ["*"]}
    await ws.send(json.dumps(subscribe_msg))


async def handle_message(message):
    message_data = json.loads(message)
    try:
        news_event = message_data[0]
        print(f"Message received: {news_event['headline']} ({news_event['symbols']}) ({news_event['content']})")
        
        event_symbols = set(news_event['symbols'])
        matching_symbols = event_symbols.intersection(stock_symbols)
        
        if matching_symbols:
            print(f"Matching symbols: {matching_symbols}")
            for symbol in matching_symbols:
                sentiment = analyze_sentiment(news_event['headline'])
                
                if sentiment == 2:  
                    buy_price = get_current_price(symbol)
                    qty = 5  
                    
                    take_profit_price = buy_price * 1.20 
                    stop_loss_price = buy_price * 0.90 

                    order = submit_bracket_order(
                        symbol=symbol,
                        qty=qty,
                        side='buy',
                        take_profit_price=take_profit_price,
                        stop_loss_price=stop_loss_price
                    )
                    print(f"Buy order placed with stop-loss and take-profit for {symbol}: {order}")

                elif sentiment == 0:  
                    sell_price = get_current_price(symbol)
                    qty = 5  
                    
                    take_profit_price = sell_price * 0.80 
                    stop_loss_price = sell_price * 1.10 

                    order = submit_bracket_order(
                        symbol=symbol,
                        qty=qty,
                        side='sell',
                        take_profit_price=take_profit_price,
                        stop_loss_price=stop_loss_price
                    )
                    print(f"Sell order placed with stop-loss and take-profit for {symbol}: {order}")

    except Exception as e:
        print(f"Error processing message: {e}")
        
async def main():
    async with websockets.connect(ws_url) as ws:
        await authenticate_and_subscribe(ws)
        async for message in ws:
            await handle_message(message)

if __name__ == "__main__":
    asyncio.run(main())