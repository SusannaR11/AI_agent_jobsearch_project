from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def project_root() -> Path:
    return Path(__file__).resolve().parents[3]

def get_gemini_api_key() -> str:
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(f"Kunde inte hitta GOOGLE_API_KEY i .env")

DEFAULT_LANCEDB_DIR = project_root() /"rag_playground" / "db" / "yrkesbarometer_vectors"

def lancedb_dir() -> Path:
    return Path(os.getenv("LANCEDB_DIR", str(DEFAULT_LANCEDB_DIR))).resolve()