from ai_agent_jobsearch_project.services.ingestion_services import load_rows, create_and_append_records
from ai_agent_jobsearch_project.embeddings.vector_store import connect_db, search_by_vector
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts
from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern



def main():

    #Hämta samtliga yrkesområden
    df_raw = load_yrkesbarometern()
    ALL_AREAS = df_raw["yrkesomrade"].unique().tolist()

    print(f"Hittade {len(ALL_AREAS)}  yrkesområden")

    TABLE_NAME = "yrken"
    LIMIT = 10000
    BATCH_SIZE = 100

    rows = load_rows(ALL_AREAS, limit=LIMIT)

    db = connect_db()
    table, inserted_total = create_and_append_records(
        db=db,
        table_name=TABLE_NAME,
        rows=rows,
        batch_size=BATCH_SIZE,
    )
    print(f"Inläsningen klar - totalt: {inserted_total} rader i tabellen '{TABLE_NAME}'.")

    # #Hämta ett urval av yrkesområden
    # SELECTED_AREAS = [
    #     "Data/IT",
    #     "Administration, ekonomi, juridik",
    #     "Hälso- och sjukvård",
    #     "Bygg och anläggning",
    #     "Industriell tillverkning",
    #     "Transport",
    #     "Försäljning, inköp, marknadsföring",
    # ]  

    # TABLE_NAME = "yrken"
    # LIMIT = 1600
    # BATCH_SIZE = 100  
   
    # rows = load_rows(SELECTED_AREAS, limit = LIMIT)

    # db = connect_db()
    # table, inserted_total = create_and_append_records(
    #     db=db,
    #     table_name=TABLE_NAME,
    #     rows=rows,
    #     batch_size=BATCH_SIZE,
    # )

    # print(f"Inserted total: {inserted_total} records")
    # print(f"Rows in table: {table.count_rows()}")

    # query_config = [
    #     ("goda framtidsutsikter", "Data/IT"),
    #     ("goda framtidsutsikter", "Hälso- och sjukvård"),
    #     ("goda framtidsutsikter", "Administration, ekonomi, juridik"),
    #     ("goda framtidsutsikter", "Bygg och anläggning"),
    #     ("goda framtidsutsikter", "Industriell tillverkning"),
    #     ("goda framtidsutsikter", "Transport"),
    #     ("goda framtidsutsikter","Försäljning, inköp, marknadsföring"),

    # ]

    # for q, area in query_config:
    #     q_vector = encode_texts([q])[0].tolist()
    #     results = search_by_vector(table, q_vector, k = 200)
    #     results = results[results["yrkesomrade"] == area].head(20)
        
    #     print("\nYrkesområde:", area, "| QUERY:", q)
    #     print(results[
    #         [
    #             "yb_yrke",
    #             "yrkesomrade",
    #             "prognos",
    #             "jobbmojligheter",
    #             "rekryteringssituation",
    #             "text_jobbmojligheter",
    #             "text_rekryteringssituation",
    #             "_distance"            ]
    #     ]) 


if __name__ == "__main__":
    main()

