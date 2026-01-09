import faiss
import os
import pickle
import numpy as np

VECTOR_DB_PATH = "data/vectordb/index.faiss"
META_PATH = "data/vectordb/meta.pkl"

def save_vector_store(vectors, texts):
    """
    Saves embeddings and corresponding text chunks.
    """
    os.makedirs("data/vectordb", exist_ok=True)

    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))

    faiss.write_index(index, VECTOR_DB_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(texts, f)


def load_vector_store():
    """
    Loads embeddings and text chunks.
    """
    index = faiss.read_index(VECTOR_DB_PATH)

    with open(META_PATH, "rb") as f:
        texts = pickle.load(f)

    return index, texts
