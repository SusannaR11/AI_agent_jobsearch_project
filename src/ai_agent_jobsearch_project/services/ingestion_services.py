from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern
from ai_agent_jobsearch_project.embeddings.document_builder import build_document
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.embeddings.vector_store import (create_or_overwrite_table, add_records)



def chunk_list(items, batch_size: int):
    """
    Yield successive chunks from a list.
        Items: List of items to split into chunks.
        Batch_size: Number of items per chunk.
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def safe_str(value) -> str:
    """
    Normalize values to string.
    If None or NaN, converts to empty string.
    """
    if value is None:
        return ""
    if isinstance(value, float) and value != value:  
        return ""
    return str(value)

def load_rows(selected_areas: list[str], limit: int) -> list[dict]:
    """
    Load and filter Yrkesbarometern data.
    Filters rows by selected occupation areas (yrkesområden) and limits the number of rows.
    Returns the result as a list of dictionaries.
    """    
    df = load_yrkesbarometern()
    df = df[df["yrkesomrade"].isin(selected_areas)].copy()
    df = df.head(limit).copy()
    return df.to_dict("records")


def build_records(batch_rows: list[dict]) -> list[dict]:
    """
    Build vectorized records for LanceDB.
    Returns aist of records containing metadata, document text, and embedding vectors.
    """
    docs = [build_document(r) for r in batch_rows]
    vectors = encode_texts(docs)

    records = []
    for row, doc, vec in zip(batch_rows, docs, vectors):
        records.append({
            "yb_concept_id": row["yb_concept_id"],
            "yrkesomrade": row["yrkesomrade"],
            "yb_yrke": row["yb_yrke"],
            "lan": str(row["lan"]),
            "prognos": safe_str(row.get("prognos")),
            "jobbmojligheter": safe_str(row.get("jobbmojligheter")),
            "rekryteringssituation": safe_str(row.get("rekryteringssituation")),
            "document": doc,
            "vector": vec.tolist()
        })
    return records

def create_and_append_records(db, table_name: str, rows: list[dict], batch_size: int):
    """
     Write records to a LanceDB table in batches. 
    Creates or overwrites the table on the first batch.
    Appends batches to table. 
    Returns av tuple (table, inserted_total)
    """
    table = None
    inserted_total = 0

    for batch_rows in chunk_list(rows, batch_size):
        records = build_records(batch_rows)

        if table is None:
            table = create_or_overwrite_table(db, table_name, records)
        
        else:
            table = add_records(table, records)
    
        inserted_total += len(records)
    
    return table, inserted_total

