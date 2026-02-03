import os
import requests

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def get_areas():
    r = requests.get(f"{API_BASE}/areas", timeout=10)
    r.raise_for_status()
    return r.json()["areas"]

def get_forecast(yrkesomrade: str, query_yrke: str, lan: str | None, limit: int = 5):
    params = {
        "yrkesomrade": yrkesomrade, 
        "query_yrke": query_yrke, 
        "limit": limit
    }
    if lan:
        params["lan"] = lan
    r = requests.get(f"{API_BASE}/forecast", params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def get_occupations(yrkesomrade: str, lan: str | None = None):
    params = {"yrkesomrade": yrkesomrade}
    if lan:
        params["lan"] = lan
    
    r = requests.get(f"{API_BASE}/occupations", params=params, timeout=10)
    r.raise_for_status()
    return r.json()["occupations"]

        

    
    
