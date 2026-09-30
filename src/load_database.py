import pandas as pd
import sqlite3
from pathlib import Path


# --------------------------------------------------
# 1. Set project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_services.csv"
)

DATABASE_PATH = (
    PROJECT_ROOT / "database" / "petsitting.db"
)


# --------------------------------------------------
# 2. Load the cleaned dataset
# --------------------------------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(PROCESSED_DATA_PATH)

print(f"Rows loaded: {len(df)}")


# --------------------------------------------------
# 3. Connect to SQLite database
# --------------------------------------------------

print("\nConnecting to SQLite database...")

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


# --------------------------------------------------
# 4. Create database table
# --------------------------------------------------

print("\nCreating services table...")

cursor.execute(
    """
    DROP TABLE IF EXISTS services
    """
)

cursor.execute(
    """
    CREATE TABLE services (
        Transaction_ID TEXT PRIMARY KEY,
        Day TEXT,
        Date TEXT,
        Client TEXT,
        Service TEXT,
        Pay REAL,
        Source_File TEXT,
        Service_Category TEXT
    )
    """
)


# --------------------------------------------------
# 5. Insert cleaned data
# --------------------------------------------------

print("Inserting cleaned data...")

df.to_sql(
    "services",
    connection,
    if_exists="append",
    index=False
)


# --------------------------------------------------
# 6. Check the database
# --------------------------------------------------

cursor.execute(
    "SELECT COUNT(*) FROM services"
)

row_count = cursor.fetchone()[0]

print(f"Rows in database: {row_count}")


# --------------------------------------------------
# 7. Check table schema
# --------------------------------------------------

print("\n--- DATABASE SCHEMA ---")

cursor.execute(
    "PRAGMA table_info(services)"
)

for row in cursor.fetchall():
    column_id, column_name, data_type, not_null, default_value, primary_key = row

    print(
        f"{column_name}: "
        f"{data_type}"
        f"{' PRIMARY KEY' if primary_key else ''}"
    )


# --------------------------------------------------
# 8. Close the connection
# --------------------------------------------------

connection.close()

print(f"\nDatabase created at: {DATABASE_PATH}")