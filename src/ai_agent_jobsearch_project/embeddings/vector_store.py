import lancedb
from pathlib import Path



DB_PATH = Path(__file__).resolve().parents[3]/ "rag_playground" / "db" / "yrkesbarometer_vectors"



def connect_db(db_path : str | Path = DB_PATH):
    """
    Connect to LanceDB database. Create a database if not exists.
    Uses DB_PATH if no path is provided.
    """

    p = Path(db_path)
    p.mkdir(parents=True, exist_ok= True)
    return lancedb.connect(str(p))


def create_or_overwrite_table(db, table_name: str, records: list[dict]):
    """
    Create (or overwrite) a table from a list of dict-records.
    """
    return db.create_table(table_name, data=records, mode="overwrite")