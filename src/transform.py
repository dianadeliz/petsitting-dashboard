import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Set project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"


# --------------------------------------------------
# 2. Define source-file exclusions
# --------------------------------------------------

# This file was superseded by the adjusted version.
# The original raw file remains untouched.
EXCLUDED_FILES = {
    "Dec2-Dec15.csv"
}


# --------------------------------------------------
# 3. Extract data from active CSV files
# --------------------------------------------------

csv_files = [
    file
    for file in RAW_DATA_PATH.glob("*.csv")
    if file.name not in EXCLUDED_FILES
]

print(f"Files processed: {len(csv_files)}")
print(f"Files excluded: {len(EXCLUDED_FILES)}")

print("\nExcluded files:")
for filename in EXCLUDED_FILES:
    print(f" - {filename}")


dataframes = []

for csv_file in sorted(csv_files):

    df = pd.read_csv(csv_file)

    # Keep the original filename for data lineage
    df["Source_File"] = csv_file.name

    dataframes.append(df)


# Combine all active source files
all_data = pd.concat(dataframes, ignore_index=True)


print(f"\nRows before cleaning: {len(all_data)}")


# --------------------------------------------------
# 4. Remove TOTALS rows
# --------------------------------------------------

totals_rows = all_data[all_data["Day"] == "TOTALS:"].copy()

clean_data = all_data[all_data["Day"] != "TOTALS:"].copy()

print(f"TOTALS rows removed: {len(totals_rows)}")
print(f"Transaction rows remaining: {len(clean_data)}")


# --------------------------------------------------
# 5. Remove unnecessary column
# --------------------------------------------------

clean_data = clean_data.drop(columns=["Unnamed: 4"])


# --------------------------------------------------
# 6. Convert Date to datetime
# --------------------------------------------------

clean_data["Date"] = pd.to_datetime(
    clean_data["Date"],
    format="%m/%d/%Y"
)


# --------------------------------------------------
# 7. Make sure Pay is numeric
# --------------------------------------------------

clean_data["Pay"] = pd.to_numeric(clean_data["Pay"])


# --------------------------------------------------
# 8. Standardize text fields
# --------------------------------------------------

text_columns = [
    "Day",
    "Client",
    "Service",
    "Source_File"
]

for column in text_columns:
    clean_data[column] = clean_data[column].str.strip()


# --------------------------------------------------
# 9. Create service categories
# --------------------------------------------------

def categorize_service(service):

    service_lower = service.lower()

    if service_lower.startswith("surcharge"):
        return "Surcharge"

    elif "cat visit" in service_lower:
        return "Cat Visit"

    elif "walk" in service_lower:
        return "Dog Walk"

    elif "sitting" in service_lower:
        return "Pet Sitting"

    elif "puppy visit" in service_lower:
        return "Puppy Visit"

    elif "key pickup" in service_lower or "key drop off" in service_lower:
        return "Administrative"

    elif "meet & greet" in service_lower:
        return "Administrative"

    elif "credit for adjustment" in service_lower:
        return "Adjustment"

    else:
        return "Other"


clean_data["Service_Category"] = clean_data["Service"].apply(
    categorize_service
)


# --------------------------------------------------
# 10. Create transaction ID
# --------------------------------------------------

clean_data.insert(
    0,
    "Transaction_ID",
    [f"TRX{i:06d}" for i in range(1, len(clean_data) + 1)]
)


# --------------------------------------------------
# 11. Check for missing values
# --------------------------------------------------

print("\n--- MISSING VALUES ---")

missing_values = clean_data.isnull().sum()

print(missing_values)


# --------------------------------------------------
# 12. Display cleaned data
# --------------------------------------------------

print("\n--- CLEANED DATA ---")

print(
    clean_data.head(10).to_string(index=False)
)


print("\n--- DATA TYPES ---")

print(clean_data.dtypes)


print("\n--- CLEANED DATASET SHAPE ---")

print(clean_data.shape)


# --------------------------------------------------
# 13. Service category check
# --------------------------------------------------

print("\n--- SERVICE CATEGORIES ---")

print(
    clean_data["Service_Category"].value_counts()
)


# --------------------------------------------------
# 14. Overall revenue check
# --------------------------------------------------

total_revenue = clean_data["Pay"].sum()

print("\n--- OVERALL REVENUE ---")

print(f"Total transaction revenue: ${total_revenue:,.2f}")


# --------------------------------------------------
# 15. Save cleaned dataset
# --------------------------------------------------

PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

output_file = PROCESSED_DATA_PATH / "cleaned_services.csv"

clean_data.to_csv(
    output_file,
    index=False
)


print(f"\nCleaned data saved to: {output_file}")
