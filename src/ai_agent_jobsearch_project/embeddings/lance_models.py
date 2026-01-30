from lancedb.pydantic import LanceModel, Vector

class OccupationRecord(LanceModel):
    yb_concept_id: str
    yrkesomrade: str
    yb_yrke: str
    lan: str

    prognos: str = ""
    jobbmojligheter: str = ""
    rekryteringssituation: str = ""

    document: str
    vector: Vector(384)
