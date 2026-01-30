from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
from typing import List

from ai_agent_jobsearch_project.embeddings.vector_store import connect_db, search_by_vector
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.backend.schemas import ForecastResult


app = FastAPI(title = "Yrkesbarometern API")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    return {"status:", "OK"}



@app.get("/areas")
def list_areas():
    db = connect_db()

    try:
        table = db.open_table("yrken")
    except Exception:
        raise HTTPException(status_code=500, detail="Table 'yrken' not found. Run ingestion first.")

    df = table.to_pandas()
    areas = sorted(df["yrkesomrade"].dropna().unique().tolist())

    return {"areas": areas}
    



@app.get("/forecast", response_model=List[ForecastResult])
def forecast(
    yrkesomrade: str = Query(...),
    query: str = Query(...),
    limit: int = Query(5, ge=1, le=20),
    ):
    db = connect_db()

    try:
        table = db.open_table("yrken")
    except Exception:
        raise HTTPException(status_code=500, detail="Table 'yrken' not found. Run ingestion first.")
    

    q_vector = encode_texts([query])[0].tolist()
    results = search_by_vector(table, q_vector, k=200)

    filtered = results[results["yrkesomrade"] == yrkesomrade].head(limit)

    if filtered.empty:
        return []

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
