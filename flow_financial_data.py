# dagster_pipeline.py

from dagster import job, op
import requests
import json

API_URL = "https://your-api-url.com/symbol=bbl/cashflow/"
OUTPUT_PATH = "/path/to/output/bbl-cashflow.json"

@op
def fetch_data_from_api():
    response = requests.get(API_URL)
    response.raise_for_status()  # จับ error จาก API
    return response.json()

@op
def convert_to_json(data):
    return json.dumps(data, indent=2)

@op
def save_json(json_str):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(json_str)

@job
def csv_to_json_job():
    data = fetch_data_from_api()
    json_str = convert_to_json(data)
    save_json(json_str)
