from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern
from ai_agent_jobsearch_project.embeddings.document_builder import build_document
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.embeddings.vector_store import connect_db, create_or_overwrite_table, search_by_vector, add_records


def chunk_list(items, batch_size: int):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

#Funktion som normaliserar fälten till strängar, för att programmet inte ska krascha vid NaN
def safe_str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value != value:  
        return ""
    return str(value)

def main():

    df = load_yrkesbarometern()

    SELECTED_AREAS = [
        "Data/IT",
        "Administration, ekonomi, juridik",
        "Hälso- och sjukvård",
    ]  

    BATCH_SIZE = 100  

    df_filtered = df[df["yrkesomrade"].isin(SELECTED_AREAS)].copy() 

    df_small = df_filtered.head(800).copy()  


    rows = df_small.to_dict("records")

    db = connect_db()
    table = None

    for batch_rows in chunk_list(rows, BATCH_SIZE):

        docs = [build_document(r) for r in batch_rows]
        vectors = encode_texts(docs)
        
        records = []

        for row, doc, vec in zip(batch_rows, docs, vectors ):
            records.append({
                "yb_concept_id": row["yb_concept_id"],
                "yrkesomrade": row["yrkesomrade"],
                "yb_yrke": row["yb_yrke"],
                "lan": str(row["lan"]),
                "prognos": safe_str(row.get("prognos")),
                "jobbmojligheter": safe_str(row.get("jobbmojligheter")),
                "rekryteringssituation": safe_str(row.get("rekryteringssituation")),
                "document": doc,
                "vector": vec.tolist(),
            })        
    
        if table is None:
            table = create_or_overwrite_table(db, "yrken", records)

        else:
            table = add_records(table, records)

        print(f"Inserted {len(records)} records (table now has {table.count_rows()} rows)")


    query_config = [
        ("goda framtidsutsikter", "Data/IT"),
        ("goda framtidsutsikter", "Hälso- och sjukvård"),
        ("goda framtidsutsikter", "Administration, ekonomi, juridik"),
    ]

    

    for q, area in query_config:
        q_vector = encode_texts([q])[0].tolist()
        results = search_by_vector(table, q_vector, k = 200)
        results = results[results["yrkesomrade"] == area].head(5)
        
        print("\nYrkesområde:", area, "| QUERY:", q)
        print(
            results[[
                "yb_yrke",
                "yrkesomrade",
                "prognos",
                "jobbmojligheter",
                "rekryteringssituation",
                "_distance"
            ]]
        )

if __name__ == "__main__":
    main()

