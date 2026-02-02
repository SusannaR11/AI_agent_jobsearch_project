import requests
from backend.constants import JOBADS_URL

def fetch_jobads(limit=200, q =""):
    r= requests.get(JOBADS_URL, params={"q":q, "limit":limit}, timeout=30)
    r.raise_for_status()
    return r.json()["hits"]

if __name__ == "__main__":
    hits = fetch_jobads(limit=50)
    print("Found ads: ", len(hits))
    print("Example occupation group: ") # to verify
    print(hits[0] ["occupation_group"] ["label"])