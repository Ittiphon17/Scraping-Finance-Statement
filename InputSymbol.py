def get_stock_ticker():
    while True:
        ticker = input("Enter the stock ticker symbol (e.g., BBL, kbank) or type 'exit' to quit: ").strip().lower()
        return ticker