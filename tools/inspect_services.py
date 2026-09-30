import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_services.csv"

df = pd.read_csv(PROCESSED_DATA_PATH)

print("\n--- SERVICE DESCRIPTIONS ---")

for service in sorted(df["Service"].unique()):
    print(repr(service))

print("\n--- SERVICE DESCRIPTION LENGTHS ---")

for service in sorted(df["Service"].unique()):
    print(f"{len(service):3} | {repr(service)}")