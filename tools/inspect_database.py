import sqlite3
from pathlib import Path


# --------------------------------------------------
# 1. Set database path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT / "database" / "petsitting.db"
)


# --------------------------------------------------
# 2. Connect to database
# --------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


# --------------------------------------------------
# 3. List tables
# --------------------------------------------------

print("\n--- DATABASE TABLES ---")

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    """
)

tables = cursor.fetchall()

for table in tables:
    print(table[0])


# --------------------------------------------------
# 4. Inspect services table
# --------------------------------------------------

print("\n--- SERVICES TABLE STRUCTURE ---")

cursor.execute(
    "PRAGMA table_info(services)"
)

columns = cursor.fetchall()

for column in columns:
    print(column)


# --------------------------------------------------
# 5. Count unique service descriptions
# --------------------------------------------------

print("\n--- UNIQUE SERVICES ---")

cursor.execute(
    """
    SELECT COUNT(DISTINCT Service)
    FROM services
    """
)

unique_services = cursor.fetchone()[0]

print(f"Unique service descriptions: {unique_services}")


# --------------------------------------------------
# 6. Count unique clients
# --------------------------------------------------

print("\n--- UNIQUE CLIENTS ---")

cursor.execute(
    """
    SELECT COUNT(DISTINCT Client)
    FROM services
    """
)

unique_clients = cursor.fetchone()[0]

print(f"Unique clients: {unique_clients}")


# --------------------------------------------------
# 7. List service descriptions
# --------------------------------------------------

print("\n--- SERVICE DESCRIPTIONS ---")

cursor.execute(
    """
    SELECT DISTINCT Service
    FROM services
    ORDER BY Service
    """
)

for row in cursor.fetchall():
    print(row[0])


# --------------------------------------------------
# 8. Close connection
# --------------------------------------------------

connection.close()