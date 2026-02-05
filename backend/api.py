from fastapi import FastAPI
from backend.services import get_top_job_listings, get_top_searches
from backend.constants import DATA_DIR
from backend.data_models import Prompt
from backend.rag import rag_agent

app = FastAPI()

@app.get("/top-searches")
def top_searches(days: int = 7):
    return get_top_searches(days=days, top_n=10)

@app.get("/top-job-listings")
def top_job_listings(days: int = 7):
    return get_top_job_listings(top_n=10)

@app.post("/rag/query")
async def rag_query(query:Prompt):
    result = await rag_agent.run(query.prompt)
    return result.output # or data??


# to run:
# uv run uvicorn backend.api:app --reload

