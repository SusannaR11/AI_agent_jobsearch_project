from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    yrkesomrade: str
    lan: Optional[str] = None

class OccupationMatch(BaseModel):
    yb_yrke: str
    yrkesomrade: str
    lan: str
    prognos: str
    jobbmojligheter: str
    rekryteringssituation: str
    text_jobbmojligheter: str
    text_rekryteringssituation: str
    distance: float

class LLMAnalysis(BaseModel):
    summary: str = Field(description="En kort sammanfattning av läget")
    recommendation: str = Field(description="Råd till användaren baserat på data")

class ChatResponse(BaseModel):
    matched_yrke: Optional[str]
    analysis: Optional[LLMAnalysis]  
    raw_data: List[OccupationMatch]  