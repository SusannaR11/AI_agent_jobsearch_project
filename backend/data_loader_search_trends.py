from pathlib import Path
import json
import re
from backend.constants import DATA_DIR

FILE_RE = re.compile(r"jobsearch-(\d{4}-\d{2}-\d{2})-daily-public\.json")

# loads and matches files by date from json jobsearch files in "data" folder
# matches search words for later analysis


def list_files():
    items = []
    for path in DATA_DIR.glob("jobsearch-*-daily-public.json"):
        matchfile = FILE_RE.match(path.name)
        if matchfile:
            date_str = matchfile.group(1)
            items.append((date_str, path))

    items.sort(key=lambda x: x[0])
    return [p for _, p in items]

# validation if missing data
def latest_file():
    files = list_files()
    if not files:
        raise FileNotFoundError("No JSON files found in ./data/ folder")
    return files[-1]

def last_n_files(n=7):
    files = list_files()
    return files[-n:]

# load json file into pyhton dict
def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_latest():
    p = latest_file()
    return p, load_json(p)


def load_last_n(n=7):
    result = []
    for p in last_n_files(n):
        result.append((p, load_json(p)))
    return result

