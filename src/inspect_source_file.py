import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw"

source_file = RAW_PATH / "Dec2-Dec15(Gus adjusted849-14=835).csv"

df = pd.read_csv(source_file)

print(f"\n--- {source_file.name} ---")
print(f"Rows including TOTALS row: {len(df)}")

print("\n--- SOURCE DATA ---")
print(df.to_string(index=False))

print("\n--- PAY TOTAL ---")
print(f"${df['Pay'].sum():.2f}")