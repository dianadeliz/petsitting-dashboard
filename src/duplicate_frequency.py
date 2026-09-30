import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

file_path = PROCESSED_PATH / "cleaned_services.csv"

df = pd.read_csv(file_path)

# Count repeated transactions within each source file
frequency = (
    df.groupby(
        ["Date", "Client", "Service", "Pay", "Source_File"]
    )
    .size()
    .reset_index(name="Count")
)

# Keep only repeated records
repeated = frequency[frequency["Count"] > 1].copy()

print("\n--- DUPLICATE FREQUENCY ---")

print(
    repeated["Count"]
    .value_counts()
    .sort_index()
    .rename_axis("Times Appearing")
    .reset_index(name="Number of Groups")
    .to_string(index=False)
)

print("\n--- GROUPS APPEARING 2 TIMES ---")
print(
    repeated[repeated["Count"] == 2]
    .to_string(index=False)
)

print("\n--- GROUPS APPEARING 4 TIMES ---")
print(
    repeated[repeated["Count"] == 4]
    .to_string(index=False)
)