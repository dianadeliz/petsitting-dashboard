import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

EXCLUDED_FILES = {
    "Dec2-Dec15.csv"
}


# Read all active CSV files
dataframes = []

for csv_file in RAW_DATA_PATH.glob("*.csv"):

    if csv_file.name in EXCLUDED_FILES:
        continue

    df = pd.read_csv(csv_file)

    # Remove TOTALS rows
    df = df[df["Day"] != "TOTALS:"].copy()

    # Keep only the fields that identify a transaction
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Source_File"] = csv_file.name

    dataframes.append(df)


all_data = pd.concat(dataframes, ignore_index=True)


# Find transactions that appear in more than one source file
transaction_columns = [
    "Date",
    "Client",
    "Service",
    "Pay"
]

duplicate_groups = (
    all_data
    .groupby(transaction_columns, dropna=False)["Source_File"]
    .agg(lambda files: sorted(set(files)))
    .reset_index()
)

duplicate_groups["Number_of_Files"] = (
    duplicate_groups["Source_File"].apply(len)
)


cross_file_duplicates = duplicate_groups[
    duplicate_groups["Number_of_Files"] > 1
]


print("\n--- CROSS-FILE DUPLICATE CANDIDATES ---")
print(
    cross_file_duplicates.to_string(index=False)
)


print("\n--- SUMMARY ---")
print(
    f"Transaction groups appearing in multiple files: "
    f"{len(cross_file_duplicates)}"
)