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
# 3. Basic database validation
# --------------------------------------------------

print("\n--- DATABASE VALIDATION ---")

cursor.execute(
    "SELECT COUNT(*) FROM services"
)

total_records = cursor.fetchone()[0]

print(f"Total records: {total_records}")


# --------------------------------------------------
# 4. Transaction ID validation
# --------------------------------------------------

print("\n--- TRANSACTION ID VALIDATION ---")

cursor.execute(
    """
    SELECT
        COUNT(*) AS Total_Records,
        COUNT(DISTINCT Transaction_ID) AS Unique_Transaction_IDs
    FROM services
    """
)

total_records, unique_transaction_ids = cursor.fetchone()

print(f"Total records: {total_records}")
print(f"Unique transaction IDs: {unique_transaction_ids}")

if total_records == unique_transaction_ids:
    print("Transaction ID check: PASS")
else:
    print("Transaction ID check: CHECK")


# --------------------------------------------------
# 5. Total revenue
# --------------------------------------------------

print("\n--- TOTAL REVENUE ---")

cursor.execute(
    """
    SELECT SUM(Pay)
    FROM services
    """
)

total_revenue = cursor.fetchone()[0]

print(f"Total revenue: ${total_revenue:,.2f}")


# --------------------------------------------------
# 6. Revenue by service category
# --------------------------------------------------

print("\n--- REVENUE BY SERVICE CATEGORY ---")

cursor.execute(
    """
    SELECT
        Service_Category,
        COUNT(*) AS Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Service_Category
    ORDER BY Revenue DESC
    """
)

for row in cursor.fetchall():
    category, transactions, revenue = row

    print(
        f"{category}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 7. Revenue by service
# --------------------------------------------------

print("\n--- REVENUE BY SERVICE ---")

cursor.execute(
    """
    SELECT
        Service,
        COUNT(*) AS Number_of_Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Service
    ORDER BY Revenue DESC
    """
)

for row in cursor.fetchall():
    service, transactions, revenue = row

    print(
        f"{service}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 8. Revenue by month
# --------------------------------------------------

print("\n--- REVENUE BY MONTH ---")

cursor.execute(
    """
    SELECT
        strftime('%Y-%m', Date) AS Month,
        COUNT(*) AS Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Month
    ORDER BY Month
    """
)

for row in cursor.fetchall():
    month, transactions, revenue = row

    print(
        f"{month}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 9. Revenue by day of week
# --------------------------------------------------

print("\n--- REVENUE BY DAY OF WEEK ---")

cursor.execute(
    """
    SELECT
        Day,
        COUNT(*) AS Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Day
    ORDER BY Revenue DESC
    """
)

for row in cursor.fetchall():
    day, transactions, revenue = row

    print(
        f"{day}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 10. Top clients by revenue
# --------------------------------------------------

print("\n--- TOP CLIENTS BY REVENUE ---")

cursor.execute(
    """
    SELECT
        Client,
        COUNT(*) AS Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Client
    ORDER BY Revenue DESC
    LIMIT 10
    """
)

for row in cursor.fetchall():
    client, transactions, revenue = row

    print(
        f"{client}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 11. Revenue by client and service category
# --------------------------------------------------

print("\n--- REVENUE BY CLIENT AND SERVICE CATEGORY ---")
cursor.execute(
    """
    SELECT
        Client,
        Service_Category,
        COUNT(*) AS Transactions,
        SUM(Pay) AS Revenue
    FROM services
    GROUP BY Client, Service_Category
    ORDER BY Revenue DESC
    LIMIT 15
    """
)

for row in cursor.fetchall():
    client, category, transactions, revenue = row

    print(
        f"{client} | "
        f"{category}: "
        f"{transactions} transactions, "
        f"${revenue:,.2f}"
    )


# --------------------------------------------------
# 12. Data quality checks
# --------------------------------------------------

print("\n--- DATA QUALITY CHECKS ---")


# Missing required values
cursor.execute(
    """
    SELECT COUNT(*)
    FROM services
    WHERE Transaction_ID IS NULL
       OR Date IS NULL
       OR Client IS NULL
       OR Service IS NULL
       OR Pay IS NULL
       OR Service_Category IS NULL
    """
)

missing_values = cursor.fetchone()[0]

print(
    f"Records with missing required values: "
    f"{missing_values}"
)


# Zero-value transactions
cursor.execute(
    """
    SELECT COUNT(*)
    FROM services
    WHERE Pay = 0
    """
)

zero_value_transactions = cursor.fetchone()[0]

print(
    f"Zero-value transactions requiring review: "
    f"{zero_value_transactions}"
)


# Negative payments
cursor.execute(
    """
    SELECT COUNT(*)
    FROM services
    WHERE Pay < 0
    """
)

negative_payments = cursor.fetchone()[0]

print(
    f"Negative payment transactions: "
    f"{negative_payments}"
)


# --------------------------------------------------
# 12a. Inspect zero-value transactions
# --------------------------------------------------

print("\n--- ZERO-VALUE TRANSACTIONS ---")

cursor.execute(
    """
    SELECT
        Transaction_ID,
        Date,
        Client,
        Service,
        Pay,
        Source_File
    FROM services
    WHERE Pay = 0
    ORDER BY Date
    """
)

for row in cursor.fetchall():
    transaction_id, date, client, service, pay, source_file = row

    print(
        f"{transaction_id} | "
        f"{date} | "
        f"{client} | "
        f"{service} | "
        f"${pay:,.2f} | "
        f"{source_file}"
    )


# --------------------------------------------------
# 13. Transactions by service category
# --------------------------------------------------

print("\n--- TRANSACTIONS BY SERVICE CATEGORY ---")

cursor.execute(
    """
    SELECT
        Service_Category,
        COUNT(*) AS Transactions
    FROM services
    GROUP BY Service_Category
    ORDER BY Transactions DESC
    """
)

for row in cursor.fetchall():
    category, transactions = row

    print(
        f"{category}: "
        f"{transactions} transactions"
    )


# --------------------------------------------------
# 14. Close connection
# --------------------------------------------------

connection.close()

print("\nDatabase analysis complete.")          