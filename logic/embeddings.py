from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(text_chunks):
    """
    Converts text chunks into vector embeddings.
    """
    return model.encode(text_chunks)
