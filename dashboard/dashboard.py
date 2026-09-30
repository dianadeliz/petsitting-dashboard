import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# 1. Set project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "petsitting.db"
)

PUBLIC_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "public"
    / "anonymized_services.csv"
)


# --------------------------------------------------
# 2. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Pet Sitting Business Dashboard",
    layout="wide"
)


# --------------------------------------------------
# 3. Load dashboard data
# --------------------------------------------------

# Local/private mode:
# Use the SQLite database when it exists.
#
# Public mode:
# If the private database is unavailable, use the
# anonymized CSV included with the GitHub project.

if DATABASE_PATH.exists():

    connection = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql_query(
        """
        SELECT
            Transaction_ID,
            Day,
            Date,
            Client,
            Service,
            Pay,
            Service_Category
        FROM services
        """,
        connection
    )

    connection.close()

    data_mode = "Private"

else:

    if not PUBLIC_DATA_PATH.exists():
        st.error(
            "No dashboard data source was found."
        )
        st.stop()

    df = pd.read_csv(PUBLIC_DATA_PATH)

    data_mode = "Public"


# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])


# --------------------------------------------------
# 4. Dashboard title
# --------------------------------------------------

st.title("Pet Sitting Business Dashboard")

st.write(
    "Overview of transactions, revenue, services, "
    "and client activity."
)


# --------------------------------------------------
# 5. Dashboard filters
# --------------------------------------------------

st.sidebar.header("Filters")


# Year filter
available_years = sorted(
    df["Date"].dt.year.unique()
)

selected_years = st.sidebar.multiselect(
    "Year",
    options=available_years,
    default=available_years
)


# Service category filter
available_categories = sorted(
    df["Service_Category"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Service Category",
    options=available_categories,
    default=available_categories
)


# Date range filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# --------------------------------------------------
# 6. Apply filters
# --------------------------------------------------

if len(selected_dates) == 2:

    start_date = pd.Timestamp(
        selected_dates[0]
    )

    end_date = pd.Timestamp(
        selected_dates[1]
    )

    filtered_df = df[
        (df["Date"].dt.year.isin(selected_years))
        &
        (df["Service_Category"].isin(
            selected_categories
        ))
        &
        (df["Date"] >= start_date)
        &
        (df["Date"] <= end_date)
    ].copy()

else:

    filtered_df = df[
        (df["Date"].dt.year.isin(selected_years))
        &
        (df["Service_Category"].isin(
            selected_categories
        ))
    ].copy()


# --------------------------------------------------
# 7. Check for empty filter results
# --------------------------------------------------

if filtered_df.empty:

    st.warning(
        "No transactions match the selected filters. "
        "Try adjusting the year, service category, "
        "or date range."
    )

    st.stop()


# --------------------------------------------------
# 8. Calculate key metrics
# --------------------------------------------------

total_revenue = filtered_df["Pay"].sum()

total_transactions = len(filtered_df)

unique_clients = (
    filtered_df["Client"].nunique()
)

average_transaction = (
    filtered_df["Pay"].mean()
)


# --------------------------------------------------
# 9. Display KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)


col2.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)


col3.metric(
    "Unique Clients",
    f"{unique_clients:,}"
)


col4.metric(
    "Average Revenue per Transaction",
    f"${average_transaction:,.2f}"
)


# --------------------------------------------------
# 10. Revenue over time
# --------------------------------------------------

st.subheader("Revenue Over Time")

st.caption(
    "Monthly revenue based on the currently "
    "selected filters."
)


monthly_revenue = (
    filtered_df
    .assign(
        Month=filtered_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby(
        "Month",
        as_index=False
    )["Pay"]
    .sum()
    .rename(
        columns={
            "Pay": "Revenue"
        }
    )
)


st.line_chart(
    monthly_revenue,
    x="Month",
    y="Revenue"
)


# Latest month warning
if (
    filtered_df["Date"].max().to_period("M")
    == pd.Timestamp.today().to_period("M")
):

    st.caption(
        "Note: The latest month may contain "
        "partial data."
    )


# --------------------------------------------------
# 11. Revenue by service category
# --------------------------------------------------

st.subheader(
    "Revenue by Service Category"
)

st.caption(
    "Total revenue generated by each "
    "service category."
)


category_revenue = (
    filtered_df
    .groupby(
        "Service_Category",
        as_index=False
    )["Pay"]
    .sum()
    .rename(
        columns={
            "Pay": "Revenue"
        }
    )
)


st.bar_chart(
    category_revenue,
    x="Service_Category",
    y="Revenue",
    horizontal=True
)


# --------------------------------------------------
# 12. Transactions and revenue analysis
# --------------------------------------------------

col1, col2 = st.columns(2)


# --------------------------------------------------
# 12a. Transactions by service category
# --------------------------------------------------

with col1:

    st.subheader(
        "Transactions by Service Category"
    )

    st.caption(
        "Number of recorded transactions "
        "by service category."
    )


    category_transactions = (
        filtered_df
        .groupby(
            "Service_Category",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Transactions"
            }
        )
    )


    st.bar_chart(
        category_transactions,
        x="Service_Category",
        y="Transactions",
        horizontal=True
    )


# --------------------------------------------------
# 12b. Revenue by day of week
# --------------------------------------------------

with col2:

    st.subheader(
        "Revenue by Day of Week"
    )

    st.caption(
        "Total revenue generated on each "
        "day of the week."
    )


    daily_revenue = (
        filtered_df
        .groupby(
            "Day",
            as_index=False
        )["Pay"]
        .sum()
        .rename(
            columns={
                "Pay": "Revenue"
            }
        )
    )


    day_order = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]


    daily_revenue["Day"] = pd.Categorical(
        daily_revenue["Day"],
        categories=day_order,
        ordered=True
    )


    daily_revenue = (
        daily_revenue
        .sort_values("Day")
    )


    st.bar_chart(
        daily_revenue,
        x="Day",
        y="Revenue"
    )


# --------------------------------------------------
# 13. Client with most visits per month
# --------------------------------------------------

st.subheader(
    "Client with Most Visits per Month"
)

st.caption(
    "Client(s) with the highest number of "
    "recorded pet-care visits in each month. "
    "Ties are included."
)


visit_categories = [
    "Cat Visit",
    "Dog Walk",
    "Pet Sitting",
    "Puppy Visit"
]


visits_df = filtered_df[
    filtered_df["Service_Category"].isin(
        visit_categories
    )
].copy()


if not visits_df.empty:

    visits_df["Month"] = (
        visits_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_client_visits = (
        visits_df
        .groupby(
            ["Month", "Client"],
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "Visits"
            }
        )
    )


    monthly_max_visits = (
        monthly_client_visits
        .groupby("Month")["Visits"]
        .transform("max")
    )


    top_client_by_month = (
        monthly_client_visits[
            monthly_client_visits["Visits"]
            == monthly_max_visits
        ]
        .copy()
    )


    top_client_by_month = (
        top_client_by_month
        .sort_values(
            ["Month", "Client"]
        )
    )


    st.dataframe(
    top_client_by_month,
    width="stretch",
    hide_index=True,
    column_config={
        "Month": st.column_config.TextColumn(
            "Month"
        ),
        "Client": st.column_config.TextColumn(
            "Client"
        ),
        "Visits": st.column_config.NumberColumn(
            "Visits",
            format="%d"
        )
    }
)

else:

    st.info(
        "No pet-care visits are available "
        "for the selected filters."
    )


# --------------------------------------------------
# 14. Dashboard information
# --------------------------------------------------

st.divider()


st.caption(
    f"Showing {len(filtered_df):,} "
    f"of {len(df):,} transactions "
    f"from "
    f"{filtered_df['Date'].min().strftime('%b %d, %Y')} "
    f"to "
    f"{filtered_df['Date'].max().strftime('%b %d, %Y')}."
)


# Show which data source is being used
if data_mode == "Private":

    st.caption(
        "Data source: local private database."
    )

else:

    st.caption(
        "Data source: anonymized public dataset."
    )