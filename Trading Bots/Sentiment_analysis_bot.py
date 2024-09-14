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