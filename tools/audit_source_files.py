import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw"

results = []

for file in sorted(RAW_PATH.glob("*.csv")):
    df = pd.read_csv(file)

    # Remove TOTALS row for transaction analysis
    transactions = df[df["Day"] != "TOTALS:"].copy()

    # Convert dates
    transactions["Date"] = pd.to_datetime(
        transactions["Date"],
        errors="coerce"
    )

    results.append({
        "Source_File": file.name,
        "Rows": len(transactions),
        "Start_Date": transactions["Date"].min(),
        "End_Date": transactions["Date"].max(),
        "Pay_Total": transactions["Pay"].sum()
    })

audit = pd.DataFrame(results)

audit = audit.sort_values(
    ["Start_Date", "End_Date", "Source_File"]
)

print("\n--- SOURCE FILE AUDIT ---")
print(audit.to_string(index=False))

print("\n--- FILE COUNT ---")
print(f"Files: {len(audit)}")