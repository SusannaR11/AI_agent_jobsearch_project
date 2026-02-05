from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
from typing import List

from ai_agent_jobsearch_project.backend.schemas import OccupationMatch, ChatRequest, ChatResponse
from ai_agent_jobsearch_project.services.occupation_service import get_occupation_matches
from ai_agent_jobsearch_project.embeddings.vector_store import get_table
from ai_agent_jobsearch_project.services.llm_agent import generate_chat_analysis

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title = "Yrkesbarometern API")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


# ----- HEALTH CHECKS -----

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


# ----- ENDPOINTS -----

@app.get("/areas")
def list_areas():
    try:
        table = get_table("yrken")
        df = table.to_pandas()
        areas = sorted(df["yrkesomrade"].dropna().unique().tolist())        
        
        return {"areas": areas} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/forecast", response_model=List[OccupationMatch])
def forecast(
    yrkesomrade: str = Query(...),
    query_yrke: str = Query(...),
    limit: int = Query(5, ge=1, le=20),
    lan: str | None = Query(None)
):
    
    try:
        results = get_occupation_matches(yrkesomrade, query_yrke, lan, limit)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fel vid sökning: {str(e)}")
    

   
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):    
    try:
        matches = get_occupation_matches(req.yrkesomrade, req.message, req.lan, limit=3)
        analysis = generate_chat_analysis(req.message, matches)
        
        return ChatResponse(
            matched_yrke=matches[0].yb_yrke if matches else None,
            analysis=analysis, # Måste vara en dict eller pydantic-modell
            raw_data=matches  
        )
    except Exception as e:
        # Detta skriver ut det RIKTIGA felet i uvicorn-terminalen
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))



#Kontroll-utskrift av hämtade yrken pga felsökning.        
@app.get("/inspect/occupations")
def inspect_occupations():
    try:
        table = get_table("yrken")        
        df = table.to_pandas()
        
        unique_occupations = sorted(df["yb_yrke"].unique().tolist())
        
        return {
            "total_rows": len(df),
            "unique_count": len(unique_occupations),
            "occupations": unique_occupations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    