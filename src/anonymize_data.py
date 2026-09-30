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

df = pd.read_csv(PROCESSED_DATA_PATH)

print(f"Rows loaded: {len(df)}")


# --------------------------------------------------
# 3. Create anonymous client IDs
# --------------------------------------------------

unique_clients = sorted(
    df["Client"].unique()
)

client_mapping = {
    client: f"Client {i:03d}"
    for i, client in enumerate(
        unique_clients,
        start=1
    )
}


# --------------------------------------------------
# 4. Replace client names
# --------------------------------------------------

public_df = df.copy()

public_df["Client"] = (
    public_df["Client"]
    .map(client_mapping)
)


# --------------------------------------------------
# 5. Remove private/internal columns
# --------------------------------------------------

public_df = public_df.drop(
    columns=[
        "Source_File"
    ]
)


# --------------------------------------------------
# 6. Validate anonymization
# --------------------------------------------------

print("\n--- ANONYMIZATION CHECK ---")

print(
    f"Original unique clients: "
    f"{df['Client'].nunique()}"
)

print(
    f"Anonymous unique clients: "
    f"{public_df['Client'].nunique()}"
)

print(
    f"Original rows: "
    f"{len(df)}"
)

print(
    f"Public rows: "
    f"{len(public_df)}"
)


# --------------------------------------------------
# 7. Create public data directory
# --------------------------------------------------

PUBLIC_DATA_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 8. Save anonymized dataset
# --------------------------------------------------

public_df.to_csv(
    PUBLIC_DATA_PATH,
    index=False
)

print(
    f"\nAnonymized dataset saved to: "
    f"{PUBLIC_DATA_PATH}"
)