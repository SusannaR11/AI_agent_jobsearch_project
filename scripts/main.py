from ai_agent_jobsearch_project.data.load_yrkesbarometern import load_yrkesbarometern
from ai_agent_jobsearch_project.embeddings.document_builder import build_document
from ai_agent_jobsearch_project.embeddings.sentence_transformer import encode_texts




def main():
    df = load_yrkesbarometern()  # använder default DATA_PATH

    docs = [
        build_document(df.iloc[0].to_dict()),
        build_document(df.iloc[1].to_dict())
    ]

    embeddings = encode_texts(docs)

    print("Embeddings shape:", embeddings.shape)
    print("First vector length:", len(embeddings[0]))




if __name__ == "__main__":
    main()
