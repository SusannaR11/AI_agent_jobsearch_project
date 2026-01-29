from sentence_transformers import SentenceTransformer
import numpy as np


MODEL = "sentence-transformers/all-MiniLM-L6-v2"


_model = SentenceTransformer(MODEL)         #-> OBS! Kod/tips från chat-GPT - genom att använda _model laddas modellen endast en gång, 
                                            #vilket innebär att modellen återanvänds 

def encode_texts(texts: list[str]) -> np.ndarray:
    """
    Encodes a list of texts to eembedding vectors. 
    Returns a numpy-array
    """

    embeddings = _model.encode(texts)
    return embeddings

