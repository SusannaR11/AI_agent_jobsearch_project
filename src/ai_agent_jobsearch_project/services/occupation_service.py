
from ai_agent_jobsearch_project.embeddings.vector_store import get_table, search_by_vector
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.backend.schemas import OccupationMatch
from ai_agent_jobsearch_project.services.ranking import apply_ranking


def get_occupation_matches(yrkesomrade: str, query_yrke: str, lan: str = None, limit: int = 5):
    table = get_table("yrken")
    
    #Gör vektorsökning
    q_vector = encode_texts([query_yrke])[0].tolist()
    results = search_by_vector(table, q_vector, k=200)

    #Filtrerar resultatet på yrkesområde
    filtered = results[results["yrkesomrade"] == yrkesomrade].copy()
    if lan:
        filtered = filtered[filtered["lan"] == lan].copy()
        
    #Logik för exakt matchning
    exact = filtered[filtered["yb_yrke"] == query_yrke].copy()
    if not exact.empty:
        filtered = exact

    if filtered.empty:
        return []
    
    #rankinglogiken
    filtered = apply_ranking(filtered)

    # Sortering (nationell prognos eller län + Score)
    if not lan:
        filtered["is_national"] = (filtered["lan"] == "00")
    else:
        filtered["is_national"] = False

    filtered = filtered.sort_values(
        by=["is_national", "rank_score", "_distance"],
        ascending=[False, False, True]
    ).head(limit)

    #returnera Pydantic-objekt
    return [
        OccupationMatch(
            **row.to_dict(), 
            distance=float(row.get("_distance", 0.0))
        ) for _, row in filtered.iterrows()
    ]
    
    