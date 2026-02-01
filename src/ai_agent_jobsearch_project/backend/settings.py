from pathlib import Path
import os

def project_root() -> Path:
    return Path(__file__).resolve().parents[3]

DEFAULT_LANCEDB_DIR = project_root() /"rag_playground" / "db" / "yrkesbarometer_vectors"

def lancedb_dir() -> Path:
    return Path(os.getenv("LANCEDB_DIR", str(DEFAULT_LANCEDB_DIR))).resolve()