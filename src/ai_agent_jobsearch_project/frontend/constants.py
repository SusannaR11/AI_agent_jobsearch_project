from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

JOBADS_URL = "https://jobsearch.api.jobtechdev.se/search"

FILE_RE = re.compile(r"jobsearch-(\d{4}-\d{2}-\d{2})-daily-public\.json")

VECTOR_DATABASE_PATH = PROJECT_ROOT / "knowledge_base" / "jobads.lance"

IMG_PATH = PROJECT_ROOT / "src" / "ai_agent_jobsearch_project" / "assets" / "Logga_negativ.png"
