# defines end points for api

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

    results = []
    for _, blob in blobs:
        data= blob.get("occupation-group-label")

        if not data:
            continue

        for label, count in data[:top_n]:
            results.append({"label": label, "count": int(count)})

        break

    return results


 


