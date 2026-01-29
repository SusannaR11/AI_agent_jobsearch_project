from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern
from ai_agent_jobsearch_project.embeddings.document_builder import build_document
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.embeddings.vector_store import connect_db, create_or_overwrite_table, search_by_vector


def main():
    df = load_yrkesbarometern()

    df_small = df[df["lan"] == "00"].head(10).copy()        #En liten df för att testa funktionalitet

    docs = [build_document(row.to_dict()) for _, row in df_small.iterrows()]
    vectors = encode_texts(docs)

    records = []
    for i, (_, row) in enumerate(df_small.iterrows()):
        records.append({
            "yb_concept_id": row["yb_concept_id"],
            "yb_yrke": row["yb_yrke"],
            "lan": row["lan"],
            "document": docs[i],
            "vector": vectors[i].tolist(),
        })

    db = connect_db()
    table = create_or_overwrite_table(db, "yrken", records)

    print("Rows in table:", table.count_rows())



    query = "yrken inom administration med goda framtidsutsikter"
    query_vector = encode_texts([query])[0].tolist()

    results = search_by_vector(table, query_vector, k=5)
    print(results[["yb_yrke", "lan", "_distance"]])


if __name__ == "__main__":
    main()

