from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(
    name="gemini-embedding-001",
)
embedding_model.max_retries = 2

EMBEDDING_DIM = 3072


class JobAd(LanceModel):
    doc_id: str
    occupation_group: str
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField() # type: ignore


class Prompt(BaseModel):
    prompt: str


class RagResponse(BaseModel):
    occupation_group: str
    answer: str

# based off school code-alongs repo