# 

import pandas as pd
from backend.data_loader_search_trends import load_last_n
from preprocessing.fetch_jobads import fetch_jobads
#from constants import DATA_DIR, JOBADS_URL, FILE_RE

TZ = "Europe/Stockholm"

def get_top_job_listings(top_n: int = 10):
    hits = fetch_jobads(limit=50)
    df = pd.json_normalize(hits)

    titles = df["occupation_group.label"]

    top = titles.value_counts().head(top_n)

    return [{"label": k, "count": int(v)} for k, v in top.items()]


def get_top_searches(days: int=7, top_n: int = 10):
    blobs = load_last_n(days)

    labels = []
    for _, blob in blobs:
        items= blob.get("items", blob)
        print("TYPE blob:", type(blob))
        print("TYPE items:", type(items))
        print("FIRST items:", items[:3] if isinstance(items, list) else str(items)[:200])

        for it in items:
            label = it.get("label") or it.get("occupation_group") or it.get("occupation_group.label")
            if label:
                labels.append(label)

    if not labels:
        return[]

    top = pd.Series(labels).value_counts().head(top_n)
    return [{"label": k, "count": int(v)} for k, v in top.items()]


 


