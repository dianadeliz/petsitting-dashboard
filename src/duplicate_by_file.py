import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

file_path = PROCESSED_PATH / "cleaned_services.csv"

df = pd.read_csv(file_path)

# Count each transaction within each source file
frequency = (
    df.groupby(
        ["Date", "Client", "Service", "Pay", "Source_File"]
    )
    .size()
    .reset_index(name="Count")
)

# Keep repeated transactions
repeated = frequency[frequency["Count"] > 1].copy()

# Summarize by source file
file_summary = (
    repeated
    .groupby("Source_File")
    .agg(
        repeated_groups=("Count", "size"),
        repeated_rows=("Count", "sum")
    )
    .reset_index()
    .sort_values("repeated_rows", ascending=False)
)

print("\n--- REPEATED RECORDS BY SOURCE FILE ---")
print(file_summary.to_string(index=False))

print("\n--- FILES WITH NO REPEATED RECORDS ---")
all_files = sorted(df["Source_File"].unique())

files_with_duplicates = set(file_summary["Source_File"])

for source_file in all_files:
    if source_file not in files_with_duplicates:
        print(source_file)