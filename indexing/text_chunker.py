# This file handles splitting research paper text into smaller chunks
# These chunks will later be converted into embeddings

from typing import List
from models.paper_models import PaperSection



def chunk_sections(
    sections: List[PaperSection],
    paper_id: str,
    chunk_size: int = 500
) -> List[dict]:
    """
    This function splits each PaperSection into smaller text chunks
    and attaches useful metadata to each chunk.

    At this stage:
    - We still use simple character-based chunking
    - Each chunk gets a unique chunk_id
    - Paper-level metadata is attached
    """

    chunks = []
    chunk_counter = 0

    # Loop through each section of the paper
    for section in sections:

        section_text = section.content

        # Split section text into fixed-size chunks
        for i in range(0, len(section_text), chunk_size):

            chunk_text = section_text[i:i + chunk_size]

            # Create a unique chunk ID
            chunk_id = f"{paper_id}_chunk_{chunk_counter}"
            chunk_counter += 1

            # Store chunk along with metadata
            chunks.append({
                "chunk_id": chunk_id,
                "paper_id": paper_id,
                "section_name": section.section_name,
                "text": chunk_text
            })

    return chunks
