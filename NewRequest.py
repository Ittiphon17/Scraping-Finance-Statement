import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

BASE_FOLDER = 'Financial Statements'

# กำหนด header สำหรับ request
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

URLS = {    
    'Income': 'https://stockanalysis.com/quote/bkk/{ticker}/financials/',
    'Balance Sheet': 'https://stockanalysis.com/quote/bkk/{ticker}/financials/balance-sheet/',
    'Cash Flow': 'https://stockanalysis.com/quote/bkk/{ticker}/financials/cash-flow-statement/',
    'Ratio': 'https://stockanalysis.com/quote/bkk/{ticker}/financials/ratios/',
}

def fetch_financial_data(ticker, statement_type, url):
    print(f"Scraping {statement_type} for {ticker.upper()}...")
    response = requests.get(url.format(ticker=ticker), headers=HEADERS)
    return response

def parse_html_table(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = pd.read_html(str(soup), attrs={'data-test': 'financials'})
    return tables

def process_dataframe(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]
    df = df.iloc[:, :-1]
    if df.columns.size > 0:
        df.columns.values[0] = 'Item'
    return df

def transform_to_long_format(df):
    if 'Item' in df.columns:
        id_col = 'Item'
        df_long = df.melt(id_vars=id_col, var_name='Date', value_name='Value')
        return df_long
    return None

def clean_data(df_long):
    if df_long is not None:
        df_long['Date'] = df_long['Date'].str.extract(r'([A-Za-z]{3} \d{1,2}, \d{4})')
        df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
        df_long['Created_at'] = datetime.now()
        df_long['Item'] = df_long['Item'].str.strip()
        df_long['Value'] = (
            df_long['Value']
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.replace('%', '', regex=False)
            .str.replace('—', '', regex=False)
            .str.replace('N/A', '', regex=False)
            .str.replace('nan', '', regex=False)
            .str.strip()
        )
        df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')
        df_long = df_long.dropna(subset=['Date', 'Value'])
        df_long = df_long.drop_duplicates()
    return df_long

def save_to_csv(df, ticker, statement_type):
    if df is not None:
        folder_path = os.path.join(BASE_FOLDER, statement_type)
        os.makedirs(folder_path, exist_ok=True)
        file_name = f"{ticker.upper()}-{statement_type}.csv"
        file_path = os.path.join(folder_path, file_name)
        df.to_csv(file_path, index=False)
        print(f"✅ Saved to {file_path}")

def scrape_financials(ticker):
    for statement_type, url in URLS.items():
        response = fetch_financial_data(ticker, statement_type, url)

        if response.status_code != 200:
            print(f"❌ Invalid ticker symbol '{ticker.upper()}' for {statement_type}. Skipping.")
            continue

        tables = parse_html_table(response)
        if not tables:
            print(f"❌ No data found for {statement_type} for {ticker.upper()}. Skipping.")
            continue

        df = tables[0]
        df = process_dataframe(df)
        df_long = transform_to_long_format(df)
        df_long_cleaned = clean_data(df_long)
        save_to_csv(df_long_cleaned, ticker, statement_type)
