from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits long text into smaller overlapping chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)
