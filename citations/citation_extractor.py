# This file is responsible for extracting citation entries
# from the References section of a research paper

import re


def extract_citations_from_references(paper) -> list:
    """
    This function extracts individual citation entries
    from the References section of a research paper.

    At this stage:
    - We use simple rule-based text splitting
    - We do NOT validate citation correctness
    - We do NOT build graphs yet
    """

    references_text = ""

    # Find the References section in the paper
    for section in paper.sections:
        if section.section_name.lower() == "references":
            references_text = section.content
            break

    # If no references section is found, return empty list
    if not references_text:
        return []

    # Split references based on common citation patterns
    # This handles numbered and line-separated references
    raw_citations = re.split(r"\n|\d+\.\s", references_text)

    citations = []

    for citation in raw_citations:
        cleaned = citation.strip()

        # Ignore very short or empty lines
        if len(cleaned) > 20:
            citations.append(cleaned)

    return citations
def build_citation_relationships(paper, citations: list) -> dict:
    """
    This function builds citation relationships for a research paper.

    Relationship format:
    {
        "paper_id": "...",
        "cites": [list of cited papers]
    }

    At this stage:
    - We only store outgoing citations
    - We do NOT resolve citation metadata
    - We keep everything simple and explicit
    """

    citation_graph = {
        "paper_id": paper.paper_id,
        "cites": []
    }

    # Loop through extracted citations
    for citation in citations:
        citation_graph["cites"].append({
            "raw_citation": citation
        })

    return citation_graph
