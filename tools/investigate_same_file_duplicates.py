import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

file_path = PROCESSED_PATH / "cleaned_services.csv"

df = pd.read_csv(file_path)

# Find exact duplicate transaction rows
duplicate_mask = df.duplicated(
    subset=["Date", "Client", "Service", "Pay"],
    keep=False
)

duplicates = df[duplicate_mask].copy()

# Count how many times each transaction appears
summary = (
    duplicates
    .groupby(["Date", "Client", "Service", "Pay", "Source_File"])
    .size()
    .reset_index(name="Count")
    .sort_values(["Source_File", "Date", "Client"])
)

print("\n--- SAME-FILE DUPLICATES ---")
print(summary.to_string(index=False))

print("\n--- SUMMARY ---")
print(f"Rows involved in repeated transactions: {len(duplicates)}")
print(f"Repeated transaction groups: {len(summary)}")