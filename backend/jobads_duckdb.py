import duckdb
import pandas as pd
from datetime import date

def jobs_to_duckdb(db_path, job_count):
    df = pd.DataFrame(job_count, columns=["occupation_group", "count"])
    today = date.today().isoformat()
    df["date"] = today
    df = df[["date", "occupation_group", "count"]]

    conn = duckdb.connect(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobads_count (
                 date TEXT,
                 occupation_group TEXT,
                 count INT
        )
                 """)
    
    # overwrite in order to avoid duplication when rerunning script
    conn.execute("DELETE FROM jobads_count WHERE date = ?", [today])

    conn.register("df", df)
    conn.execute("INSERT INTO jobads_count SELECT * FROM df")
    conn.close()