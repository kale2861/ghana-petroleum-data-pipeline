import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Read Brent data sheet
df = pd.read_excel(
    RAW_DIR / "RBRTEa.xls",
    sheet_name="Data 1"
)

# Rename columns
df.columns = ["date", "brent_price_usd"]

# Remove metadata rows
df = df.iloc[2:]

# Convert types
df["date"] = pd.to_datetime(df["date"])
df["brent_price_usd"] = pd.to_numeric(
    df["brent_price_usd"],
    errors="coerce"
)

# Extract year
df["year"] = df["date"].dt.year

# Keep only needed years
df = df[df["year"].isin([2022, 2023, 2024])]

# Keep final columns
df = df[["year", "brent_price_usd"]]

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
df.to_csv(
    PROCESSED_DIR / "brent_yearly_prices_clean.csv",
    index=False
)

print(df)

print("Clean Brent dataset saved.")