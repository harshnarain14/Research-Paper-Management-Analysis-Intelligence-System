# This file is responsible for generating vector embeddings from text
# Embeddings convert text into numerical vectors for semantic search

from sentence_transformers import SentenceTransformer


def load_embedding_model():
    """
    This function loads a sentence-transformer embedding model.
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def embed_text(model, text: str):
    """
    Convert a single text string into an embedding vector.
    """

    # convert_to_numpy=False ensures compatibility with FAISS + serialization
    embedding = model.encode(text, convert_to_numpy=False)
    return embedding


def embed_chunks(model, chunks: list) -> list:
    """
    Generate embeddings for all chunks and attach them to chunk metadata.
    """

    embedded_chunks = []

    for chunk in chunks:
        embedding = embed_text(model, chunk["text"])

        chunk_with_embedding = {
            **chunk,
            "embedding": embedding
        }

        embedded_chunks.append(chunk_with_embedding)

    return embedded_chunks
