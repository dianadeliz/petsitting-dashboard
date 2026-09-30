import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

csv_file = RAW_DATA_PATH / "Aug26-Sep06.csv"

df = pd.read_csv(csv_file)

print("\n--- CLIENTS ---")
print(df["Client"].dropna().unique())

print("\n--- SERVICES ---")
print(df["Service"].dropna().unique())

print("\n--- PAY VALUES ---")
print(df["Pay"].dropna().unique())

print("\n--- VALUES IN UNNAMED: 4 ---")
print(df["Unnamed: 4"].dropna().unique())

print("\n--- NUMBER OF RECORDS BY SERVICE ---")
print(df["Service"].value_counts(dropna=False))

print("\n--- TOTAL PAY FROM SERVICE RECORDS ---")
service_rows = df[df["Day"] != "TOTALS:"]
print(service_rows["Pay"].sum())

print("\n--- FILE TOTAL ---")
print(df["Pay"].sum())