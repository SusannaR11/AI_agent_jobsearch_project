from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

JOBADS_URL = "https://jobsearch.api.jobtechdev.se/search"

FILE_RE = re.compile(r"jobsearch-(\d{4}-\d{2}-\d{2})-daily-public\.json")

VECTOR_DATABASE_PATH = PROJECT_ROOT / "knowledge_base" / "jobads.lance"

IMG_PATH = PROJECT_ROOT / "src" / "ai_agent_jobsearch_project" / "assets" / "Logga_negativ.png"


LAN_OPTIONS = [
    ("", "Nationellt (ingen filtrering)"),
    ("01", "Stockholms län"),
    ("03", "Uppsala län"),
    ("04", "Södermanlands län"),
    ("05", "Östergötlands län"),
    ("06", "Jönköpings län"),
    ("07", "Kronobergs län"),
    ("08", "Kalmar län"),
    ("09", "Gotlands län"),
    ("10", "Blekinge län"),
    ("12", "Skåne län"),
    ("13", "Hallands län"),
    ("14", "Västra Götalands län"),
    ("17", "Värmlands län"),
    ("18", "Örebro län"),
    ("19", "Västmanlands län"),
    ("20", "Dalarnas län"),
    ("21", "Gävleborgs län"),
    ("22", "Västernorrlands län"),
    ("23", "Jämtlands län"),
    ("24", "Västerbottens län"),
    ("25", "Norrbottens län"),
]
