import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw"

original_file = RAW_PATH / "Dec2-Dec15.csv"
adjusted_file = RAW_PATH / "Dec2-Dec15(Gus adjusted849-14=835).csv"

original = pd.read_csv(original_file)
adjusted = pd.read_csv(adjusted_file)

# Remove totals rows
original = original[original["Day"] != "TOTALS:"].copy()
adjusted = adjusted[adjusted["Day"] != "TOTALS:"].copy()

# Remove the checkmark column
original = original.drop(columns=["Unnamed: 4"])
adjusted = adjusted.drop(columns=["Unnamed: 4"])

# Add source labels
original["Source"] = "Original"
adjusted["Source"] = "Adjusted"

print("\n--- ORIGINAL FILE ---")
print(f"Rows: {len(original)}")
print(f"Pay total: ${original['Pay'].sum():.2f}")

print("\n--- ADJUSTED FILE ---")
print(f"Rows: {len(adjusted)}")
print(f"Pay total: ${adjusted['Pay'].sum():.2f}")

# Compare the unique transaction rows
columns = ["Day", "Date", "Client", "Service", "Pay"]

original_unique = original[columns].drop_duplicates()
adjusted_unique = adjusted[columns].drop_duplicates()

# Rows in original but not adjusted
only_original = original_unique.merge(
    adjusted_unique,
    on=columns,
    how="outer",
    indicator=True
)

only_original = only_original[
    only_original["_merge"] == "left_only"
].drop(columns="_merge")

# Rows in adjusted but not original
only_adjusted = original_unique.merge(
    adjusted_unique,
    on=columns,
    how="outer",
    indicator=True
)

only_adjusted = only_adjusted[
    only_adjusted["_merge"] == "right_only"
].drop(columns="_merge")

print("\n--- ROWS ONLY IN ORIGINAL ---")
print(only_original.to_string(index=False))

print("\n--- ROWS ONLY IN ADJUSTED ---")
print(only_adjusted.to_string(index=False))