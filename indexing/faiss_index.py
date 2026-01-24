"""Create and use a FAISS index for embedding vectors."""

import faiss
import numpy as np


def create_faiss_index(embedded_chunks: list):
    """Create a FAISS index from embedded text chunks.

    - Assumes all embeddings have the same dimension
    - Uses IndexFlatL2 (exact search)
    """

    embeddings = [chunk["embedding"] for chunk in embedded_chunks]
    embedding_matrix = np.array(embeddings).astype("float32")
    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(dimension)

    # FAISS add expects the numpy array as a positional argument
    index.add(embedding_matrix)

    return index, embedding_matrix


def semantic_search(
    query: str,
    model,
    index,
    chunks: list,
    top_k: int = 5,
) -> list:
    """Perform semantic search over the FAISS index and return matching chunks."""

    query_embedding = model.encode(query)
    query_vector = query_embedding.astype("float32").reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results
