import subprocess
import time
from datetime import timedelta
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
import signal
import os
from to_json import convert_csv_to_json
from main import get_stock_tickers_from_csv
from RequestFinancial import scrape_financials

# ---- Task: Stop API ----
@task
def stop_api_server():
    logger = get_run_logger()
    logger.info("Stopping existing FastAPI server (if any)")
    # This assumes the API runs on port 8000; we kill it with lsof or pkill
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=True)
        logger.info("✅ API server stopped")
    except subprocess.CalledProcessError:
        logger.warning("⚠️ No running API server found or failed to stop it.")

# ---- Task: Scrape Data ----
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=12))
def scrape_data():
    logger = get_run_logger()
    logger.info("📊 Starting financial data scraping")

    tickers = get_stock_tickers_from_csv()
    if not tickers:
        raise ValueError("❌ No tickers found in CSV")
    
    for ticker in tickers:
        try:
            scrape_financials(ticker)
        except Exception as e:
            logger.error(f"❌ Failed scraping for {ticker}: {e}")

# ---- Task: Convert CSV to JSON ----
@task
def convert_to_json():
    logger = get_run_logger()
    logger.info("🔄 Converting CSV to JSON")

    convert_csv_to_json()

# ---- Task: Start API ----
@task
def start_api_server():
    logger = get_run_logger()
    logger.info("🚀 Starting FastAPI server on port 8000")
    subprocess.Popen(["uvicorn", "get_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    time.sleep(5)  # wait a bit to ensure server starts

# ---- Main Flow ----
@flow(name="Stock Data Daily Pipeline")
def stock_data_pipeline():
    stop_api_server()
    scrape_data()
    convert_to_json()
    start_api_server()
