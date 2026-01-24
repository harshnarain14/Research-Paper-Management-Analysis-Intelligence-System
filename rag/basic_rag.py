# This file implements a basic Retrieval-Augmented Generation (RAG) pipeline
# with source attribution using GROQ LLM

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import SecretStr


def generate_answer_with_sources(
    query: str,
    retrieved_chunks: list
) -> dict:
    """
    This function generates an answer using GROQ LLM
    and also returns source information.

    Output:
    {
        "answer": "...",
        "sources": [...]
    }

    At this stage:
    - We explicitly track which sections were used
    - This improves transparency and trust
    """

    # Load environment variables from .env file
    load_dotenv()

    # Initialize GROQ chat model
    groq_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=SecretStr(groq_key) if groq_key is not None else None,
        temperature=0.2
    )

    # Combine retrieved chunk texts into one context string
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

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

    # Construct a grounded prompt
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

    # Return answer along with sources
    return {
        "answer": response.content,
        "sources": sources
    }
