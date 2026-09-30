import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load cleaned dataset
file_path = PROJECT_ROOT / "data" / "processed" / "cleaned_services.csv"

df = pd.read_csv(file_path)

# Columns that define an exact duplicate transaction
duplicate_columns = [
    "Date",
    "Client",
    "Service",
    "Pay"
]

# Find duplicate records
duplicates = df[
    df.duplicated(
        subset=duplicate_columns,
        keep=False
    )
].copy()

# --------------------------------------------------
# 1. DUPLICATES WITHIN THE SAME SOURCE FILE
# --------------------------------------------------

same_file = (
    duplicates
    .groupby(duplicate_columns + ["Source_File"])
    .size()
    .reset_index(name="Count")
)

same_file = same_file[same_file["Count"] > 1]

print("\n--- DUPLICATES WITHIN THE SAME SOURCE FILE ---")
print(same_file.to_string(index=False))

# --------------------------------------------------
# 2. DUPLICATES ACROSS DIFFERENT SOURCE FILES
# --------------------------------------------------

cross_file = (
    duplicates
    .groupby(duplicate_columns)
    .agg(
        Record_Count=("Date", "size"),
        Number_of_Source_Files=("Source_File", "nunique"),
        Source_Files=("Source_File", lambda x: ", ".join(sorted(x.unique())))
    )
    .reset_index()
)

cross_file = cross_file[
    cross_file["Number_of_Source_Files"] > 1
]

print("\n--- DUPLICATES ACROSS DIFFERENT SOURCE FILES ---")
print(cross_file.to_string(index=False))

# --------------------------------------------------
# 3. SUMMARY
# --------------------------------------------------

print("\n--- SUMMARY ---")

print(
    f"Duplicate records within same file: "
    f"{same_file['Count'].sum() if not same_file.empty else 0}"
)

print(
    f"Duplicate groups across different files: "
    f"{len(cross_file)}"
)