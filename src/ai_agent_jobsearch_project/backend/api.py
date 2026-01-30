from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(title = "Yrkesbarometern API")

@app.get("/health")
def health_check():
    return {"status:", "OK"}

@app.get("/")
def root():
    return RedirectResponse(url="/docs")