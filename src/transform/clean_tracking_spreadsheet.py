import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

input_file = RAW_DIR / "ghana_petroleum_tracking.xlsx"
output_file = PROCESSED_DIR / "ghana_petroleum_analytics.csv"

df = pd.read_excel(input_file)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove rows without year
df = df.dropna(subset=["year"])

# Convert year
df["year"] = df["year"].astype(int)

# Automatically generate source column
df["source"] = (
    "PIAC " + df["year"].astype(str) + " Annual Report"
)

# Numeric columns
numeric_cols = [
    "total_production_barrels",
    "petroleum_revenue_usd",
    "brent_price_usd"
]

# Clean numeric values
for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")

# Create revenue efficiency metric
df["revenue_per_barrel"] = (
    df["petroleum_revenue_usd"]
    / df["total_production_barrels"]
)

# Sort by year
df = df.sort_values("year")

# Save clean dataset
df.to_csv(output_file, index=False)

print(df.head())
print(df.tail())

print("Expanded analytics dataset created.")