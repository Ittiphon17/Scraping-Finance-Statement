## 📦 Installation Instructions

This project includes **web scraping** functionality that extracts financial statement data of **Thai stocks** from [stockanalysis.com](https://stockanalysis.com), including:

- 📄 Income Statement  
- 📊 Balance Sheet  
- 💸 Cash Flow Statement  
- 📈 Financial Ratios  

---

## 🗂️ Project Structure
```
Agent Stock Suggestion/
├── pycache/                   # Compiled Python files 
├── Financial Statements/      # Folder for raw financial statement data (CSV/Excel) ⭐
├── FinancialJSON/             # Folder for financial data in JSON format ⭐
├── myenv/                     # Virtual environment (should be in .gitignore)
├── .gitignore                 # Git ignore rules
├── flow_financial_data.py     # Orchestrates data scraping and processing flow ⭐
├── get_api.py                 # FastAPI server exposing API endpoints ⭐
├── main.py                    # Entry point or controller logic for the app ⭐
├── NewRequest.py              # Script to send scraping requests ⭐
├── README.md                  # Project documentation
├── requirements.txt           # List of Python dependencies
├── Stocks_Name.csv            # List of Thai stock symbols (input file) There are only examples!
├── to_json.py                 # Converts scraped data to JSON format ⭐
```

To get started, please install all the required dependencies by running the following command in your terminal:

---

## 📦 Installation & Running

1. **Install dependencies**

```bash
pip install -r requirements.txt
```
2. **Run the FastAPI server**

```bash
uvicorn get_api:app --host 0.0.0.0 --port 8000 --reload
```
- Access the API at: [http://localhost:8000](http://localhost:8000)
- Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Network Access: http://{your-ip}:8000

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/symbol={symbol}/incomestmt/`       | Get Income Statement |
| `/symbol={symbol}/balancesheet/` | Get Balance Sheet Statement |
| `/symbol={symbol}/cashflow/`     | Get Cash Flow Statement |
| `/symbol={symbol}/ratio/`        | Get Financial Ratios |

### 📍 Example Request

```
GET http://localhost:8000/symbol=CPALL/incomestmt/
OR
GET http://<your-ip>:8000/symbol=CPALL/incomestmt/
```

## 📤 Sample Response (JSON)

```json
{
  "Income Statement": {
    "Operating Revenue": [
      {
        "2025-03-31": 970481
      },
      {
        "2024-12-31": 958998
      },
      {
        "2023-12-31": 895281
      },
      {
        "2022-12-31": 829099
      },
      {
        "2021-12-31": 565060
      },
      {
        "2020-12-31": 525884
      }
    ],
    ...
  ]
}
```
