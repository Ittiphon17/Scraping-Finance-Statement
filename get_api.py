from fastapi import FastAPI, HTTPException
import os
import json
from fastapi.responses import JSONResponse

app = FastAPI()

BASE_DIR = os.path.join(os.getcwd(), "Financial_JSON")

FILE_MAP = {
    "incomestmt": "income.json",
    "cashflow": "cashflow.json",
    "balancesheet": "balancesheet.json",
    "ratio": "ratio.json"
}

@app.get("/symbol={symbol}/{statement}/")
async def get_financial_statement(symbol: str, statement: str):
    statement = statement.lower()
    if statement not in FILE_MAP:
        raise HTTPException(status_code=404, detail="Invalid statement type.")

    # รองรับชื่อหุ้นที่ขึ้นต้นด้วย _
    safe_symbol = symbol.upper()
    if safe_symbol == "COM7":
        safe_symbol = f"_{safe_symbol}"

    symbol_path = os.path.join(BASE_DIR, safe_symbol)
    if not os.path.exists(symbol_path):
        raise HTTPException(status_code=404, detail="Symbol not found.")

    file_path = os.path.join(symbol_path, FILE_MAP[statement])
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Statement file not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return JSONResponse(content=data)

# :8000/symbol=_COM7/ratio/
# :8000/symbol=BBL/cashflow/
