from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

JOBADS_URL = "https://jobsearch.api.jobtechdev.se/search"
FILE_RE = re.compile(r"jobsearch-(\d{4}-\d{2}-\d{2})-daily-public\.json")

VECTOR_DATABASE_PATH = Path(__file__).parents[1] / "knowledge_base"