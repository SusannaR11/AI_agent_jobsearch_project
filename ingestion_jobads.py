import json
from pathlib import Path
import lancedb
from backend.data_models import JobAd
from backend.constants import VECTOR_DATABASE_PATH

DATA_FILE = Path("data/jobads_2026-02-05.jsonl")

db = lancedb.connect(VECTOR_DATABASE_PATH)

def main():
    rows = []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            rows.append({
                "doc_id": row["id"],
                "occupation_group": row["occupation_group"],
                "content": row["text"],
            })

    table = db.create_table("jobads", schema=JobAd, mode="overwrite")
    table.add(rows[:10])


if __name__ == "__main__":
    main()
