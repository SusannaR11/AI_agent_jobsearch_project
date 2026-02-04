import duckdb
from pathlib import Path
import pandas as pd


other_repo = Path("/Users/susannarokka/Desktop/NBI_year_1/Python/hr_analytics_proj")

db_path = other_repo / "ads_data_warehouse.duckdb"

print("DB file exists:", db_path.exists())
print("DB path:", db_path)

con = duckdb.connect(database=str(db_path), read_only=True)

tables = con.execute("SHOW TABLES").fetchall()
print("Tables:")
for t in tables:
    print("-", t[0])

df = con.execute("SELECT * FROM src_job_ads LIMIT 5").fetchdf()

print("\nPreview of src_job_ads:")
print(df.head())

con.close()