import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
import pandas as pd

# Load the FinBERT sentiment analysis model
tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

sp500_table = pd.read_html(url)[0]

sp500_table['Security'].tolist()