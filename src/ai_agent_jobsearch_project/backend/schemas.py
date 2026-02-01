from pydantic import BaseModel

class ForecastResult(BaseModel):
    yb_yrke: str
    yrkesomrade: str
    lan: str
    prognos: str
    jobbmojligheter: str
    rekryteringssituation: str
    text_jobbmojligheter: str
    text_rekryteringssituation: str
    distance: float