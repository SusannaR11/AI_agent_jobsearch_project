import duckdb
import pandas as pd
from datetime import date
from collections import Counter

from preprocessing.fetch_jobads import fetch_jobads

def count_occ_group(hits):
    c = Counter()
    for h in hits:
        occgr = h.get("occupation_group") or {}
        label = occgr.get("label")
        if label:
            c[label] += 1
        return c.most_common()

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


if __name__ == "__main__":
    hits = fetch_jobads(limit=50, q="*")
    job_count = count_occ_group(hits)

    jobs_to_duckdb("data/jobads.duckdb", job_count)

    print("Saved to DuckDB") # verify
    print("Top 5:", job_count[:10])

# to run script in command line:
# uv run python -m preprocessing.process_jobads


