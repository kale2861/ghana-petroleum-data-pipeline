import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

data = {
    "year": [2022, 2023, 2024],
    "total_production_barrels": [51756481, 48247037, 48240010],
    "petroleum_revenue_usd": [1428760000, 1062323419.12, 1357793869.40],
    "source_report": [
        "PIAC 2022 Annual Report",
        "PIAC 2023 Annual Report",
        "PIAC 2024 Annual Report"
    ]
}

df = pd.DataFrame(data)

df.to_csv(
    RAW_DIR / "ghana_petroleum_summary_manual.csv",
    index=False
)

print("Raw Ghana petroleum dataset created.")