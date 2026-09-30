import pandas as pd
from pathlib import Path


# Find the project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of raw CSV files
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"


# File that was superseded by a corrected version
EXCLUDED_FILES = {
    "Dec2-Dec15.csv"
}


validation_results = []


# Check every active CSV file
for csv_file in sorted(RAW_DATA_PATH.glob("*.csv")):

    if csv_file.name in EXCLUDED_FILES:
        continue

    df = pd.read_csv(csv_file)

    # Separate transaction rows from the TOTALS row
    transaction_rows = df[df["Day"] != "TOTALS:"].copy()
    totals_rows = df[df["Day"] == "TOTALS:"]

    # Calculate transaction-level total
    transaction_total = transaction_rows["Pay"].sum()

    # Read the source-reported total
    if len(totals_rows) == 1:
        source_total = totals_rows["Pay"].iloc[0]
    else:
        source_total = None

    # Calculate difference
    if source_total is not None:
        difference = transaction_total - source_total
    else:
        difference = None

    # Determine validation status
    if source_total is None:
        status = "CHECK"
    elif abs(difference) < 0.01:
        status = "PASS"
    else:
        status = "FAIL"

    validation_results.append({
        "Source_File": csv_file.name,
        "Transaction_Rows": len(transaction_rows),
        "Calculated_Total": transaction_total,
        "Source_Total": source_total,
        "Difference": difference,
        "Status": status
    })


# Create validation DataFrame
validation_df = pd.DataFrame(validation_results)


print("\n--- SOURCE TOTAL VALIDATION ---")
print(
    validation_df.to_string(
        index=False,
        formatters={
            "Calculated_Total": "${:.2f}".format,
            "Source_Total": "${:.2f}".format,
            "Difference": "${:.2f}".format
        }
    )
)


print("\n--- SUMMARY ---")

print(
    f"Files checked: {len(validation_df)}"
)

print(
    f"PASS: {(validation_df['Status'] == 'PASS').sum()}"
)

print(
    f"FAIL: {(validation_df['Status'] == 'FAIL').sum()}"
)

print(
    f"CHECK: {(validation_df['Status'] == 'CHECK').sum()}"
)


# Show any files that require investigation
failed_files = validation_df[
    validation_df["Status"] != "PASS"
]

if len(failed_files) > 0:

    print("\n--- FILES REQUIRING INVESTIGATION ---")

    print(
        failed_files.to_string(
            index=False,
            formatters={
                "Calculated_Total": "${:.2f}".format,
                "Source_Total": "${:.2f}".format,
                "Difference": "${:.2f}".format
            }
        )
    )