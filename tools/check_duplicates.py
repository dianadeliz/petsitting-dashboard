import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Load the processed dataset
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_services.csv"
)

df = pd.read_csv(PROCESSED_FILE)


# --------------------------------------------------
# 2. Find duplicate groups
# --------------------------------------------------

duplicate_columns = [
    "Day",
    "Date",
    "Client",
    "Service",
    "Pay",
]

duplicate_groups = (
    df.groupby(duplicate_columns, dropna=False)
    .agg(
        Record_Count=("Source_File", "size"),
        Source_Files=("Source_File", lambda x: ", ".join(sorted(x.unique())))
    )
    .reset_index()
)

duplicate_groups = duplicate_groups[
    duplicate_groups["Record_Count"] > 1
].sort_values(
    by="Record_Count",
    ascending=False
)


# --------------------------------------------------
# 3. Display duplicate groups
# --------------------------------------------------

print("\n--- DUPLICATE GROUPS ---")

print(
    duplicate_groups[
        [
            "Date",
            "Client",
            "Service",
            "Pay",
            "Record_Count",
            "Source_Files",
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 4. Count groups by number of source files
# --------------------------------------------------

duplicate_groups["Number_of_Source_Files"] = (
    duplicate_groups["Source_Files"]
    .str.count(",") + 1
)

print("\n--- DUPLICATE GROUPS BY NUMBER OF SOURCE FILES ---")

print(
    duplicate_groups["Number_of_Source_Files"]
    .value_counts()
    .sort_index()
)