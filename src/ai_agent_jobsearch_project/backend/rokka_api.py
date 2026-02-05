from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from ai_agent_jobsearch_project.services.occupation_services import get_top_job_listings, get_top_searches
from ai_agent_jobsearch_project.frontend.constants import DATA_DIR
from ai_agent_jobsearch_project.backend.data_models import Prompt
from ai_agent_jobsearch_project.services.rag import rag_agent


app = FastAPI(title = "Arbetsmarknadsinsikter API")
 

#------Susanna's API -------

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
# uv run uvicorn ai_agent_jobsearch_project.backend.rokka_api:app --reload --port 8000

