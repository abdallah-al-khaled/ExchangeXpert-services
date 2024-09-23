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

sp500_table = sp500_table[['Symbol', 'Security']]

import pandas as pd

# Load the S&P 500 table from the URL
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(url)[0]

# Create a dictionary with symbols as keys and company names as values
sp500_dict = dict(zip(sp500_table['Symbol'], sp500_table['Security']))

# Convert the dictionary to JSON and save it to a file
import json
with open('sp500_companies.json', 'w') as f:
    json.dump(sp500_dict, f, indent=4)
    
sp500_table = sp500_table['Symbol'].tolist()

MAX_TOKENS = 512
from datetime import datetime
api_url = "http://127.0.0.1:8000/api/sentiment-analysis"
for stock in sp500_table:
    url = f"https://finance.yahoo.com/quote/{stock}/news?p={stock}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('li', class_='stream-item')
        
        sentiment_scores = []
        print(f"\nScraped Headlines and Sentiment Scores for {stock}:")
        
        for i, item in enumerate(news_items):    
            headline_tag = item.find('h3')
            headline = headline_tag.get_text().strip() if headline_tag else ''
            
            description_tag = item.find('p')
            description = description_tag.get_text().strip() if description_tag else ''
            
            text = f"{headline} {description}"
            
            if len(text) > MAX_TOKENS:
                # If text is too long, use only the description
                text = description if len(description) <= MAX_TOKENS else description[:MAX_TOKENS]
            
            if description and headline:
                finbert_result = finbert(text)[0]
                
                sentiment_score = finbert_result['score']
                sentiment_label = finbert_result['label']
                
                if sentiment_label == 'positive' or sentiment_label == 'negative':
                    if sentiment_label == 'negative':
                        sentiment_score = -sentiment_score 
                    sentiment_scores.append(sentiment_score)
                
                print(f"{i+1}. Headline: {headline}")
                print(f"   Description: {description}")
                print(f"   Sentiment: {sentiment_label}, Score: {sentiment_score:.4f}")
                print('-' * 80)
                
        if sentiment_scores:
            average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            print(f"Average Sentiment Score for {stock}: {average_sentiment:.4f}")
            data = {
                "stock_symbol": stock,
                "sentiment_score": average_sentiment,  # Example sentiment score
                "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
            }
            response = requests.post(api_url, json=data)
            if response.status_code == 201:
                print("Data successfully sent to the API!")
                print(response.json())  # Print the response from the API
            else:
                try:
                    print(f"Failed to send data. Status code: {response.status_code}")
                    print(response.json())  # Print the error message
                except(e) :
                    print("error ",e)
        else:
            print("No sentiment scores to average.")

    else:
        print(f"Failed to fetch data for {stock}. Status code: {response.status_code}")