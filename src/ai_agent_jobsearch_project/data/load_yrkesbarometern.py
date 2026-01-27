
import json
from pathlib import Path
import pandas as pd



DATA_PATH = (Path(__file__).resolve().parents[3]/"data"/"yrkesbarometer.json")

def load_yrkesbarometern(path: Path | None = None) -> pd.DataFrame:
    """
    Loading Yrkesbarometern (utf-8) as a pandas dataframe.
    Uses default DATA_PATH if another is not provided. 
    """ 
    
    if path is None:
        path = DATA_PATH 

    with path.open("r", encoding= "utf-8") as file:
        data = json.load(file)

        return pd.DataFrame(data)
    



    
