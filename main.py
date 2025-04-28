import pandas as pd
import numpy as np
import time
import requests
import os
from bs4 import BeautifulSoup

def requests_financial_data(ticker):
    ticker = ticker.upper()
    start_time = time.time()

    # Define report types and their corresponding paths
    report_types = {
        "Income Statement": ("financials", "Income"),
        "Balance Sheet": ("financials/balance-sheet", "BalanceSheet"),
        "Cash Flow Statement": ("financials/cash-flow-statement", "CashFlow")
    }

    for folder_name, (report_path, _) in report_types.items():
        time.sleep(np.random.randint(1, 6))  # Random delay to avoid rate-limiting
        url = f'https://stockanalysis.com/quote/bkk/{ticker}/{report_path}/'
        file_name = f"{ticker}_{folder_name.replace(' ', '')}.csv"
        
        # Create folder if it doesn't exist
        folder_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Simplified folder creation
        file_path = os.path.join(folder_path, file_name)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', id='main-table')

            if table:
                df = pd.read_html(str(table))[0].iloc[:, :-1]  # Directly parse the table
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)  # Flatten MultiIndex columns
                df.to_csv(file_path, index=False, encoding='utf-8')  # Save to CSV
                print(f"Time taken for {ticker} - {folder_name}: {time.time() - start_time:.2f} sec (Saved to {file_path})")
            else:
                print(f"Warning: Data table not found for {ticker} - {folder_name}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL for {ticker} - {folder_name}: {e}")
        except ValueError as e:
            print(f"Error parsing table for {ticker} - {folder_name}: {e}")

# Call the function
requests_financial_data('bbl')