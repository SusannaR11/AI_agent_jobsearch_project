from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern
from ai_agent_jobsearch_project.embeddings.document_builder import build_document
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.embeddings.vector_store import connect_db, create_or_overwrite_table, search_by_vector


def main():

    SELECTED_AREAS = [
        "Data/IT",
        "Administration, ekonomi, juridik",
        "Hälso- och sjukvård",
    ]

    df = load_yrkesbarometern()

    #df_small = df[df["yrkesomrade"].str.contains("Data/IT", na =False)].copy() #En liten df för att testa funktionalitet
    #print("Rows selected", len(df_small))  

    df_filtered = df[df["yrkesomrade"].isin(SELECTED_AREAS)].copy() 

    df_small = df_filtered.head(800).copy()  

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



    #query = "yrken inom Data/IT med goda framtidsutsikter"
    #query_vector = encode_texts([query])[0].tolist()

    #results = search_by_vector(table, query_vector, k=10)
    #print(results[["yb_yrke", "lan", "_distance"]])


    queries = [
        "Yrken inom Data/IT med goda framtidsutsikter", 
        "Yrken inom sjukvård med goda framtidsutsikter"
    ]

    for q in queries:
        q_vector = encode_texts([q])[0].tolist()
        results = search_by_vector(table, q_vector, k = 5)

        print("\nQUERY:", q)
        print(results[["yb_yrke", "lan", "_distance"]])


if __name__ == "__main__":
    main()

