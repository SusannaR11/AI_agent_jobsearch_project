from pathlib import Path
import re
import zipfile
import io
import requests
from backend.constants import DATA_DIR

# pick up search trend json files from url
BASE_URL = "https://data.arbetsformedlingen.se/annonser/search-trends/"
INDEX_URL = BASE_URL + "index.html?C=M&O=A"

DATA_DIR.mkdir(exist_ok=True)

# only keep 7 days on file in 'data' folder
KEEP_DAYS = 7

ZIP_RE = re.compile(r"jobsearch-daily-(\d{4}-\d{2}-\d{2})\.zip")

def latest_zip_file():
    response = requests.get(INDEX_URL)
    html = response.text

    dates = ZIP_RE.findall(html)
    if not dates:
        raise RuntimeError("Unable to find latest zip file on index page.")
    latest_date = max(dates) # sorts YYYY-MM-DD to max/highest date
    zip_name = f"jobsearch-daily-{latest_date}.zip"
    return BASE_URL + zip_name


# download zip, open it, and save json to directory
def download_save_json(zip_url: str) -> Path:
    r = requests.get(zip_url, timeout=60)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        json_name = next(n for n in z.namelist() if n.endswith(".json"))
        out_path = DATA_DIR / Path(json_name).name

        if out_path.exists():
            return out_path
        
        out_path.write_bytes(z.read(json_name))
        return out_path
    

def keep_last_7_days():
    files = sorted(DATA_DIR.glob("jobsearch-*-daily-public.json"))
    for f in files[:-KEEP_DAYS]:
        f.unlink()

def main():
    url = latest_zip_file()
    saved = download_save_json(url)
    keep_last_7_days()
    print("Latest saved JSON file: ", saved.name)


if __name__ == "__main__":
    main()

