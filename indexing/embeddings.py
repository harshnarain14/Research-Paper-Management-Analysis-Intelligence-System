# This file is responsible for generating vector embeddings from text
# Embeddings convert text into numerical vectors for semantic search

from sentence_transformers import SentenceTransformer


def load_embedding_model():
    """
    This function loads a sentence-transformer embedding model.

    At this stage:
    - We only load the model
    - We do NOT store embeddings
    - We do NOT use FAISS yet
    """

    # Load a lightweight and popular embedding model
    # This model is fast, open-source, and works well for semantic search
    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def embed_text(model, text: str):
    """
    This function converts a piece of text into a vector embedding.

    Parameters:
    model: Loaded SentenceTransformer model
    text (str): Input text

    Returns:
    list: Numerical embedding vector
    """

    # Generate embedding for the input text
    embedding = model.encode(text)

    return embedding
def embed_chunks(model, chunks: list) -> list:
    """
    This function generates embeddings for all text chunks.

    At this stage:
    - We loop through each chunk
    - Generate embedding for chunk text
    - Attach embedding to the chunk dictionary
    - We do NOT store embeddings in a database yet
    """

    embedded_chunks = []

    for chunk in chunks:
        # Generate embedding for the chunk text
        embedding = model.encode(chunk["text"])

        # Create a new dictionary including embedding
        chunk_with_embedding = {
            **chunk,
            "embedding": embedding
        }

        embedded_chunks.append(chunk_with_embedding)

    return embedded_chunks
