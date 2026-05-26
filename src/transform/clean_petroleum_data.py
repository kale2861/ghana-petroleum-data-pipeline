import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

df = pd.read_csv(
    RAW_DIR / "ghana_petroleum_summary_manual.csv"
)

df["revenue_per_barrel"] = (
    df["petroleum_revenue_usd"]
    / df["total_production_barrels"]
)

df.to_csv(
    PROCESSED_DIR / "ghana_petroleum_summary_clean.csv",
    index=False
)

print("Clean dataset created")