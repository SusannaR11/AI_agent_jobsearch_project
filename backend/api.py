from fastapi import FastAPI
from backend.services import get_top_job_listings, get_top_searches

app = FastAPI()

@app.get("/top-searches")
def top_searches(days: int = 7):
    return get_top_searches(days=days, top_n=10)

@app.get("/top-listings")
def top_job_listings():
    return get_top_job_listings(top_n=10)

