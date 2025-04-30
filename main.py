from RequestFinData import requests_financial_data

# Call the function
# symbols = ['2s', 'bbl', 'aot', 'ptt', 'scb']
symbols = ['2s', 'kbank', 'siri']

for sym in symbols:
    requests_financial_data(sym)
    print('-'*120)



