import os
import pandas as pd
import json
import re  

def convert_csv_to_json(base_dir="Financial Statements", output_base="Financial_JSON"):
    statement_map = {
        "Income": "Income Statement",
        "Cash Flow": "Cash Flow Statement",
        "Balance Sheet": "Balance Sheet",
        "Ratio": "Financial Ratios"
    }

    for category_folder in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category_folder)
        if not os.path.isdir(category_path):
            continue

        for filename in os.listdir(category_path):
            if filename.endswith(".csv"):
                symbol = filename.split("-")[0].upper()
                filepath = os.path.join(category_path, filename)
                df = pd.read_csv(filepath)

                section_name = statement_map.get(category_folder, category_folder)
                symbol_json = {section_name: {}}

                # จัดข้อมูล long format -> nested dict
                for item in df["Item"].unique():
                    sub_df = df[df["Item"] == item]
                    data = [{row["Date"]: row["Value"]} for _, row in sub_df.iterrows()]
                    symbol_json[section_name][item] = data

                # ตรวจสอบชื่อโฟลเดอร์ให้เป็น a-z, A-Z, 0-9 เท่านั้น
                if re.match(r"^[A-Z0-9]+$", symbol):
                    safe_symbol_folder = symbol
                else:
                    safe_symbol_folder = f"_{symbol}"

                output_dir = os.path.join(output_base, safe_symbol_folder)
                os.makedirs(output_dir, exist_ok=True)

                out_file = os.path.join(output_dir, category_folder.lower().replace(" ", "") + ".json")
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(symbol_json, f, indent=2, ensure_ascii=False)

                print(f"✅ Converted {category_folder} {symbol} to JSON")

    print(f"\nAll CSV files converted to JSON and stored in '{output_base}' directory.")

