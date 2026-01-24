# Import BaseModel from pydantic
# BaseModel helps us create structured and validated data models
from pydantic import BaseModel, Field
from typing import List, Optional


class PaperSection(BaseModel):
    """
    This class represents a single logical section of a research paper.
    Examples of sections:
    - Abstract
    - Introduction
    - Methodology
    - Results
    - Conclusion
    """

    # Name of the section (e.g., "Abstract", "Introduction")
    # This helps us identify which part of the paper this text belongs to
    section_name: str

    # Actual text content of the section
    # This will store the cleaned text extracted from the PDF
    content: str


class Citation(BaseModel):
    """
    Represents one citation/reference used by the paper
    """
    cited_title: str
    cited_year: Optional[int] = None


class ResearchPaper(BaseModel):
    """
    This class represents a complete research paper
    in a structured and machine-readable format.
    """

    # Unique internal identifier for the paper
    # Example: "paper_001" or "arxiv_2301_12345"
    paper_id: str

    # Title of the research paper
    title: str

    # List of author names
    # Example: ["John Doe", "Jane Smith"]
    authors: List[str]

    # Abstract of the paper
    # Stored separately because it is very important for search and summaries
    abstract: str

    # List of all logical sections of the paper
    # Each section is represented using the PaperSection model
    sections: List[PaperSection]

    # Publication year of the paper (optional)
    year: Optional[int] = None

    # Venue where the paper was published (optional)
    # Example: NeurIPS, ICML, ACL
    venue: Optional[str] = None

    # List of keywords or topics related to the paper (optional)

    # List of references cited by this paper (optional)
    # Each reference is represented using the Citation model
    from pydantic import Field

    keywords: Optional[List[str]] = Field(default_factory=list)
    references: Optional[List[Citation]] = Field(default_factory=list)


    # Number of times this paper has been cited (optional)
    citations: Optional[int] = None
