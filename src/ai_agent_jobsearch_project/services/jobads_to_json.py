# Load from jobads API to jsonl - text-based fileformat efficient for ML

import json
from pathlib import Path
import pandas as pd
from datetime import datetime
from ai_agent_jobsearch_project.services.fetch_jobads import fetch_jobads

# path - to go in constants.py
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def main():
    hits = fetch_jobads(limit=50)  # limit 50
    df = pd.json_normalize(hits)

    today = datetime.now().date().isoformat()
    out_path = DATA_DIR / f"jobads_{today}.jsonl"

    with out_path.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            if not row.get("description.text"):
                continue

            doc = {
                "id": row.get("id"),
                "occupation_group": row.get("occupation_group.label"),
                "headline": row.get("headline"),
                "employer": row.get("employer.name"),
                "published": row.get("publication_date"),
                "text": row.get("description.text"),
            }

            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print("Saved file:", out_path)

if __name__ == "__main__":
    main()
