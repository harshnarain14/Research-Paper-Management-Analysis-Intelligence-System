# This file implements a basic Retrieval-Augmented Generation (RAG) pipeline
# with source attribution using GROQ LLM

import os
from langchain_groq import ChatGroq
from pydantic import SecretStr


def generate_answer_with_sources(
    query: str,
    retrieved_chunks: list
) -> dict:
    """
    Generate an answer using GROQ LLM with clear source attribution.

    Returns:
    {
        "answer": "...",
        "sources": [...]
    }
    """

    # Read GROQ API key from environment (Streamlit Secrets compatible)
    groq_key = os.getenv("GROQ_API_KEY")

    if not groq_key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Please set it in environment variables or Streamlit Secrets."
        )

    # Initialize GROQ chat model
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=SecretStr(groq_key),
        temperature=0.2
    )

    # Combine retrieved chunk texts into one context string
    context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)

    # Build list of unique sources used
    sources = []
    for chunk in retrieved_chunks:
        source_info = {
            "paper_id": chunk["paper_id"],
            "section": chunk["section_name"],
            "chunk_id": chunk["chunk_id"]
        }
        if source_info not in sources:
            sources.append(source_info)

    # Construct a grounded academic prompt
    prompt = f"""
You are an academic research assistant.
Answer the question strictly using the provided context.
If the answer is not present in the context, say "Not found in the paper".

Context:
{context}

Question:
{query}

Answer:
"""

    # Invoke the GROQ LLM
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }
