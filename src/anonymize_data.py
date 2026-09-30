import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Set project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_services.csv"
)

PUBLIC_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "public"
    / "anonymized_services.csv"
)


# --------------------------------------------------
# 2. Load cleaned private dataset
# --------------------------------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(
    PROCESSED_DATA_PATH
)

print(
    f"Rows loaded: {len(df)}"
)


# --------------------------------------------------
# 3. Create anonymous client IDs
# --------------------------------------------------

unique_clients = sorted(
    df["Client"]
    .dropna()
    .unique()
)


client_mapping = {
    client: f"Client {i:03d}"
    for i, client in enumerate(
        unique_clients,
        start=1
    )
}


# --------------------------------------------------
# 4. Create public copy
# --------------------------------------------------

public_df = df.copy()


public_df["Client"] = (
    public_df["Client"]
    .map(client_mapping)
)


# --------------------------------------------------
# 5. Remove private/internal columns
# --------------------------------------------------

columns_to_remove = [
    "Source_File"
]


public_df = public_df.drop(
    columns=[
        column
        for column in columns_to_remove
        if column in public_df.columns
    ]
)


# --------------------------------------------------
# 6. Validate anonymization
# --------------------------------------------------

print(
    "\n--- ANONYMIZATION CHECK ---"
)


original_clients = (
    df["Client"].nunique()
)

anonymous_clients = (
    public_df["Client"].nunique()
)


print(
    f"Original unique clients: "
    f"{original_clients}"
)

print(
    f"Anonymous unique clients: "
    f"{anonymous_clients}"
)

print(
    f"Original rows: "
    f"{len(df)}"
)

print(
    f"Public rows: "
    f"{len(public_df)}"
)


# Check that row count was preserved
if len(df) != len(public_df):

    raise ValueError(
        "Anonymization changed the "
        "number of records."
    )


# Check that client count was preserved
if original_clients != anonymous_clients:

    raise ValueError(
        "Anonymization changed the "
        "number of unique clients."
    )


# Check client naming convention
invalid_clients = public_df[
    ~public_df["Client"].str.match(
        r"^Client \d{3}$",
        na=False
    )
]


if not invalid_clients.empty:

    raise ValueError(
        "Public dataset contains "
        "non-anonymized client values."
    )


print(
    "PASS: All client names are anonymized."
)


# --------------------------------------------------
# 7. Create public directory
# --------------------------------------------------

PUBLIC_DATA_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 8. Save public dataset
# --------------------------------------------------

public_df.to_csv(
    PUBLIC_DATA_PATH,
    index=False
)


print(
    f"\nAnonymized dataset saved to: "
    f"{PUBLIC_DATA_PATH}"
)