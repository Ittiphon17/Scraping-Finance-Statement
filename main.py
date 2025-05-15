from RequestFinancial import scrape_financials
from to_json import convert_csv_to_json
import pandas as pd

def get_stock_tickers_from_csv(filename='Stocks_Name.csv'):
    try:
        df = pd.read_csv(filename, encoding="utf-8")
        return df['Stocks_Name'].dropna().astype(str).str.strip().str.upper().tolist()
    except Exception as e:
        print(f"❌ Failed to read {filename}: {e}")
        return []

def scrape_and_convert_data():
    tickers = get_stock_tickers_from_csv()
    if not tickers:
        raise ValueError("No tickers found. Exiting...")
    
    for ticker in tickers:
        print(f"\n--- Scraping Financial Data for {ticker} ---")
        scrape_financials(ticker)
    
    print("\n--- Converting CSV to JSON ---")
    convert_csv_to_json()

if __name__ == "__main__":
    scrape_and_convert_data()

# uvicorn get_api:app --host 0.0.0.0 --port 8000 --reload
