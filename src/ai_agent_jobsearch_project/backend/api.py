from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
from typing import List

from ai_agent_jobsearch_project.embeddings.vector_store import get_table, search_by_vector
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.backend.schemas import ForecastResult
from ai_agent_jobsearch_project.services.ranking import apply_ranking


from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title = "Yrkesbarometern API")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")             #Visar att appen körs och kan ta emot requests
def health_check():
    return {"status": "OK"}

@app.get("/ready")              #Tips från ChatGPT inför Docker & Azure - visar att databas finns och att tabellen 'yrken' går att öppna. 
def ready_check():
    try:
        _ =get_table("yrken")
        return {"status": "READY"}
    except Exception:
        raise HTTPException(
            status_code= 503,
            detail = "Not ready: table 'yrken' not found. Run ingestion"
        )
    

@app.get("/areas")
def list_areas():   

    try:
        table = get_table("yrken")      
    except Exception:
        raise HTTPException(status_code=500, detail="Table 'yrken' not found. Run ingestion first.")

    df = table.to_pandas()
    areas = sorted(df["yrkesomrade"].dropna().unique().tolist())

    return {"areas": areas}   

@app.get("/forecast", response_model=List[ForecastResult])
def forecast(
    yrkesomrade: str = Query(...),
    query_yrke: str = Query(...),
    limit: int = Query(5, ge=1, le=20),
    ):
    
    try:
        table = get_table("yrken")
    except Exception:
        raise HTTPException(status_code=500, detail="Table 'yrken' not found. Run ingestion first.")
    

    q_vector = encode_texts([query_yrke])[0].tolist()
    results = search_by_vector(table, q_vector, k=200)

    filtered = results[results["yrkesomrade"] == yrkesomrade].head(limit)

    if filtered.empty:
        return []
    
    filtered = apply_ranking(filtered)

    filtered = filtered.sort_values(
        by=["rank_score", "_distance"],
        ascending=[False, True]
    ).head(limit)

    payload = []
    for _, row in filtered.iterrows():
        payload.append({
            "yb_yrke": row.get("yb_yrke", ""),
            "yrkesomrade": row.get("yrkesomrade", ""),
            "lan": row.get("lan", ""),
            "prognos": row.get("prognos", ""),
            "jobbmojligheter": row.get("jobbmojligheter", ""),
            "rekryteringssituation": row.get("rekryteringssituation", ""),
            "distance": float(row.get("_distance")),
        })

    return payload
