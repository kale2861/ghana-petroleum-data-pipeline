import duckdb
import pandas as pd

# Load analytics dataset
df = pd.read_csv(
    "data/processed/ghana_petroleum_analytics.csv"
)

# Connect to DuckDB
conn = duckdb.connect("ghana_petroleum.duckdb")

# Create table
conn.execute("""
CREATE OR REPLACE TABLE petroleum_analytics AS
SELECT * FROM df
""")

# Preview query
result = conn.execute("""
SELECT *
FROM petroleum_analytics
""").fetchdf()

print(result)

conn.close()

print("Dataset loaded into DuckDB.")