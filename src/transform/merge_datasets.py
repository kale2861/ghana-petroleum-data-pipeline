import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

# Load petroleum dataset
petroleum_df = pd.read_csv(
    PROCESSED_DIR / "ghana_petroleum_summary_clean.csv"
)

# Load Brent dataset
brent_df = pd.read_csv(
    PROCESSED_DIR / "brent_yearly_prices_clean.csv"
)

# Merge on year
merged_df = pd.merge(
    petroleum_df,
    brent_df,
    on="year",
    how="left"
)

# Save merged dataset
merged_df.to_csv(
    PROCESSED_DIR / "ghana_petroleum_analytics.csv",
    index=False
)

print(merged_df)

print("Merged analytics dataset created.")