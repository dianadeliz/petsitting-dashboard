import pandas as pd
from pathlib import Path


# Find the project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of raw CSV files
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"


# Find every CSV file in the raw data folder
EXCLUDED_FILES = {
    "Dec2-Dec15.csv"
}

csv_files = [
    file
    for file in RAW_DATA_PATH.glob("*.csv")
    if file.name not in EXCLUDED_FILES
]

print(f"Found {len(csv_files)} CSV files after exclusions.\n")

print("Excluded files:")
for filename in EXCLUDED_FILES:
    print(f" - {filename}")

print()


# Read each CSV file
dataframes = []

for csv_file in csv_files:
    print(f"Reading: {csv_file.name}")

    df = pd.read_csv(csv_file)

    # Add the original filename so we know where each record came from
    df["Source_File"] = csv_file.name

    dataframes.append(df)


# Combine all CSV files into one DataFrame
all_data = pd.concat(dataframes, ignore_index=True)


print("\n--- COMBINED DATASET ---")
print(f"Rows: {len(all_data)}")
print(f"Columns: {len(all_data.columns)}")

print("\n--- COLUMNS ---")
print(all_data.columns.tolist())

print("\n--- FIRST 10 ROWS ---")
print(all_data.head(10).to_string(index=False))

print("\n--- ROWS BY SOURCE FILE ---")
print(all_data["Source_File"].value_counts())

print("\n--- SERVICE TYPES ---")
print(all_data["Service"].value_counts(dropna=False))

print("\n--- SPECIAL DAY VALUES ---")
print(all_data["Day"].value_counts(dropna=False))

print("\n--- MISSING VALUES ---")
print(all_data.isnull().sum())

print("\n--- TOTALS ROWS ---")
totals_rows = all_data[all_data["Day"] == "TOTALS:"]
print(totals_rows.to_string(index=False))

print("\n--- TOTAL NUMBER OF TOTALS ROWS ---")
print(len(totals_rows))