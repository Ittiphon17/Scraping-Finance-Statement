# from RequestFinData import requests_financial_data
# from InputSymbol import get_stock_ticker
from NewRequest import scrape_financials

import pandas as pd

def get_stock_tickers_from_csv(filename='Stocks_Name.csv'):
    try:
        df = pd.read_csv(filename)
        return df['Stocks_Name'].dropna().astype(str).str.strip().str.upper().tolist()
    except Exception as e:
        print(f"❌ Failed to read {filename}: {e}")
        return []

def main():
    tickers = get_stock_tickers_from_csv()
    if not tickers:
        print("❌ No tickers found. Exiting...")
        return

    for ticker in tickers:
        print(f"\n--- Scraping Financial Data for {ticker} ---")
        scrape_financials(ticker)

if __name__ == "__main__":
    main()



# https://stockanalysis.com/quote/bkk/siri/financials/