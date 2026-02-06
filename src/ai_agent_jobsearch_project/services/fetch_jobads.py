import requests
from ai_agent_jobsearch_project.frontend.constants import JOBADS_URL

def fetch_jobads(limit=200, q =None):
    params={"limit":limit}

    if q:
        params["q"] = q

    r= requests.get(JOBADS_URL, params=params, timeout=30)    
    r.raise_for_status()
    return r.json()["hits"]

if __name__ == "__main__":
    hits = fetch_jobads(limit=50)
    print("Found ads: ", len(hits))
    print("Example occupation group: ") # to verify
    print(hits[0] ["occupation_group"] ["label"])

# to run, run as package
# uv run python src/ai_agent_jobsearch_project/services/fetch_jobads.py