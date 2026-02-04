from pathlib import Path
import re

DATA_DIR = Path("data")
JOBADS_URL = "https://jobsearch.api.jobtechdev.se/search"
FILE_RE = re.compile(r"jobsearch-(\d{4}-\d{2}-\d{2})-daily-public\.json")