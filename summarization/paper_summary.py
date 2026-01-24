# This file is responsible for generating automatic summaries
# of a research paper using a Large Language Model (GROQ)

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
from pydantic import SecretStr


def generate_short_summary(paper) -> str:
    """
    This function generates a short bullet-point summary
    of a research paper.

    At this stage:
    - We generate only a short summary (5–6 bullets)
    - We use abstract + key sections as context
    - We keep the prompt strict to avoid hallucinations
    """

    # Load environment variables
    load_dotenv()

    # Read API key and wrap as SecretStr for type compatibility
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_api_key_secret = SecretStr(groq_api_key) if groq_api_key is not None else None

    # Initialize GROQ LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key_secret,
        temperature=0.2
    )

    # Build context using abstract and section titles
    context_parts = []

    if paper.abstract:
        context_parts.append("ABSTRACT:\n" + paper.abstract)

    # Add limited content from important sections
    for section in paper.sections:
        if section.section_name.lower() in [
            "introduction", "methodology", "methods",
            "results", "conclusion"
        ]:
            # Limit section text to avoid overload
            context_parts.append(
                f"{section.section_name.upper()}:\n{section.content[:800]}"
            )

    context = "\n\n".join(context_parts)

    # Create a controlled academic prompt
    prompt = f"""
You are an academic research assistant.
Create a short summary of the research paper in 5 to 6 bullet points.
Use ONLY the provided context.
Do NOT add assumptions or external knowledge.

Context:
{context}

Short Summary (5–6 bullet points):
"""

    # Invoke the LLM
    response = llm.invoke(prompt)

    # Normalize response.content to a string to satisfy return type
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        processed_items = []
        for item in content:
            if isinstance(item, str):
                processed_items.append(item)
            else:
                try:
                    processed_items.append(json.dumps(item, ensure_ascii=False))
                except Exception:
                    processed_items.append(str(item))
        return "\n".join(processed_items)

    # Fallback for other types
    return str(content)
def generate_structured_summary(paper) -> dict:
    """
    This function generates a structured summary of a research paper.

    Output format:
    {
        "problem": "...",
        "approach": "...",
        "key_contributions": "...",
        "results": "...",
        "limitations": "..."
    }

    At this stage:
    - We enforce strict structure
    - We avoid free-form text
    - This makes output reliable and explainable
    """

    # Load environment variables
    load_dotenv()

    # Initialize GROQ LLM
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_api_key_secret = SecretStr(groq_api_key) if groq_api_key is not None else None
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key_secret,
        temperature=0.2
    )

    # Build context using full abstract and important sections
    context_parts = []

    if paper.abstract:
        context_parts.append("ABSTRACT:\n" + paper.abstract)

    for section in paper.sections:
        if section.section_name.lower() in [
            "introduction",
            "methodology",
            "methods",
            "results",
            "discussion",
            "conclusion"
        ]:
            context_parts.append(
                f"{section.section_name.upper()}:\n{section.content[:1000]}"
            )

    context = "\n\n".join(context_parts)

    # Structured and very explicit prompt
    prompt = f"""
You are an academic research assistant.
Using ONLY the provided context, extract the following information.

Rules:
- Do NOT use external knowledge
- If information is missing, write "Not explicitly stated"
- Be concise and factual

Context:
{context}

Provide the output in the following format:

Problem:
<text>

Approach:
<text>

Key Contributions:
<text>

Results:
<text>

Limitations:
<text>
"""

    # Invoke LLM
    response = llm.invoke(prompt)

    # Return raw structured text
    # (We keep it as text for explainability)
    return {
        "structured_summary": response.content
    }
