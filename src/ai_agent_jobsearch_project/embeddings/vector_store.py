import lancedb
from pathlib import Path
from ai_agent_jobsearch_project.embeddings.lance_models import OccupationRecord
from ai_agent_jobsearch_project.backend.settings import lancedb_dir
from functools import lru_cache


DB_PATH = lancedb_dir()


def connect_db(db_path : str | Path = DB_PATH):
    """
    Connect to LanceDB database. Create a database if not exists.
    Uses DB_PATH if no path is provided.
    """

    p = Path(db_path)
    p.mkdir(parents=True, exist_ok= True)
    return lancedb.connect(str(p))


@lru_cache(maxsize=1)               #Tips från chatGPT - skapa en cache för att kunna återanvända tabellen 
def get_db():
    return connect_db()

@lru_cache(maxsize=1)
def get_table(table_name: str = "yrken"):
    db = get_db()
    return db.open_table(table_name)


def create_or_overwrite_table(db, table_name: str, records: list[dict]):
    """
    Create (or overwrite) a table from a list of dict-records.
    """
    return db.create_table(table_name, data=records, mode="overwrite", schema = OccupationRecord)


def add_records(table, records: list[dict]):
    """
    Add records to an existing table
    """
    table.add(records)

    return table


def search_by_vector(table, query_vector: list[float], k: int = 5):
    """
    ANN vector search in LanceDB database. 
    Returns a pandas dataframe with top 5 k-matches
    """

    return table.search(query_vector).limit(k).to_pandas()