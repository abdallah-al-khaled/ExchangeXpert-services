import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
import pandas as pd
from datetime import datetime
import json

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

sp500_dict = dict(zip(sp500_table['Symbol'], sp500_table['Security']))

import json
with open('sp500_companies.json', 'w') as f:
    json.dump(sp500_dict, f, indent=4)
    
url = 'https://www.slickcharts.com/sp500'

response = requests.get(url,headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('tbody')


if table:
    # Dictionary to store company symbol and name
    companies = {}

    # Iterate through table rows and extract company names and symbols
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        if len(columns) > 1:
            symbol = columns[2].get_text(strip=True)  # Get stock symbol
            name = columns[1].get_text(strip=True)    # Get company name
            companies[symbol] = name

    # Save the company data to a JSON file
    with open('sp500_companies.json', 'w') as json_file:
        json.dump(companies, json_file, indent=4)

    print("JSON file created successfully!")
    print(companies)
else:
    print("Error: Unable to find the table on the webpage.")
    
MAX_TOKENS = 512
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