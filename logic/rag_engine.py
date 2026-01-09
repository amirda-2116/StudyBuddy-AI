import numpy as np

from logic.ingestion import load_all_documents
from logic.chunking import chunk_text
from logic.embeddings import create_embeddings
from logic.vector_store import save_vector_store, load_vector_store


def build_knowledge_base():
    """
    Reads uploaded files, chunks text, creates embeddings,
    and saves them in the vector database.
    """
    text = load_all_documents()

    if not text.strip():
        raise ValueError("No text found in uploaded documents")

    chunks = chunk_text(text)
    vectors = create_embeddings(chunks)
    save_vector_store(vectors, chunks)


def retrieve_context(query, top_k=5):
    """
    Retrieves the most relevant text chunks for a user query.
    """
    index, texts = load_vector_store()
    query_vector = create_embeddings([query])

    distances, indices = index.search(
        np.array(query_vector), top_k
    )

    return "\n".join(texts[i] for i in indices[0])
