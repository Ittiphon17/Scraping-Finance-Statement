import pandas as pd
import json

# โหลดข้อมูล (ถ้าเป็นจาก CSV)
df = pd.read_csv("BBL-Balance Sheet.csv")

# สร้างโครงสร้าง JSON
output = {}
for item in df["Item"].unique():
    records = df[df["Item"] == item][["Date", "Value"]]
    data = [{row["Date"]: row["Value"]} for _, row in records.iterrows()]
    output[item] = data

# ใส่ key 'Income Statement'
final_output = {"Income Statement": output}

# บันทึกเป็น JSON
with open("incomestmt.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)
