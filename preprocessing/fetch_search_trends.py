from pathlib import Path
import re
import zipfile
import requests

BASE_URL = "https://data.arbetsformedlingen.se/annonser/search-trends/"
INDEX_URL = BASE_URL + "index.html?C=M&O=A"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

