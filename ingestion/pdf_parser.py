import pdfplumber
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None


def open_pdf(pdf_path: str):
    """Open a PDF file using pdfplumber and return the PDF object."""
    pdf = pdfplumber.open(pdf_path)
    return pdf


def extract_first_page_text(pdf):
    """Extract text from the first page of a pdfplumber PDF object."""
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    return text
def extract_full_text(pdf):
    """
    This function extracts text from ALL pages of the PDF
    and combines it into a single string.

    At this stage:
    - We are NOT cleaning the text
    - We are NOT detecting sections
    - We are ONLY collecting raw text page by page
    """

    # Initialize an empty string to store text from all pages
    full_text = ""

    # Loop through each page in the PDF
    for page in pdf.pages:

        # Extract text from the current page
        page_text = page.extract_text()

        # Some pages may not contain readable text
        # So we check before adding
        if page_text:
            # Append page text to the full text string
            # Newline helps separate content from different pages
            full_text += page_text + "\n"

    # Return the combined text from all pages
    return full_text


def extract_text_with_pymupdf(pdf_path: str) -> str:
    """Fallback text extraction using PyMuPDF (works for many PDFs and scanned+OCRed files)."""
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed")

    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        try:
            page_text = page.get_text("text")
        except Exception:
            page_text = ""
        if page_text:
            texts.append(page_text)
    doc.close()
    return "\n".join(texts)
def basic_text_cleaning(text: str) -> str:
    """
    This function performs very basic cleaning on raw extracted text.

    At this stage, cleaning includes:
    - Removing extra spaces
    - Removing empty lines
    - Normalizing line breaks

    We are intentionally NOT doing advanced cleaning yet.
    """

    # Split the text into individual lines
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        # Strip leading and trailing spaces from each line
        cleaned_line = line.strip()

        # Ignore completely empty lines
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    # Join cleaned lines back into a single string
    # Using newline to keep logical separation
    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text
def split_text_into_sections(text: str) -> dict:
    """
    This function splits cleaned research paper text into sections
    based on common academic section headings.

    At this stage:
    - We use simple rule-based detection
    - We do NOT use AI or NLP models
    - This is intentionally kept simple and explainable
    """

    # Common section headings found in research papers
    # We keep them in lowercase for easy comparison
    section_headings = [
        "abstract",
        "introduction",
        "related work",
        "methodology",
        "methods",
        "experiments",
        "results",
        "discussion",
        "conclusion",
        "references"
    ]

    sections = {}
    current_section = "unknown"
    sections[current_section] = ""

    # Loop through each line of the cleaned text
    for line in text.splitlines():

        # Normalize the line for comparison
        normalized_line = line.strip().lower()

        # Check if the line exactly matches a known section heading
        if normalized_line in section_headings:
            current_section = normalized_line
            sections[current_section] = ""
        else:
            # Append line content to the current section
            sections[current_section] += line + " "

    return sections
# Import the PaperSection data model
# Import directly from models.paper_models to avoid package import issues
from models.paper_models import PaperSection


def convert_sections_to_models(sections: dict) -> list:
    """
    This function converts section text stored in a dictionary
    into a list of PaperSection objects.

    Input:
    sections (dict): Dictionary where
        - key = section name (e.g., "abstract", "introduction")
        - value = text content of that section

    Output:
    List[PaperSection]: Structured section objects
    """

    section_models = []

    # Loop through each detected section
    for section_name, content in sections.items():

        # Create a PaperSection object for each section
        section = PaperSection(
            section_name=section_name.title(),  # Convert to readable format
            content=content.strip()              # Remove extra spaces
        )

        # Add the section object to the list
        section_models.append(section)

    return section_models
# Import the ResearchPaper data model
# Import directly from models.paper_models to avoid package import issues
from models.paper_models import ResearchPaper


def build_research_paper(
    pdf_path: str,
    paper_id: str,
    title: str,
    authors: list
) -> ResearchPaper:
    """
    This function creates a complete ResearchPaper object
    from a research paper PDF.

    At this stage:
    - Metadata (title, authors) is passed manually
    - Year, venue, keywords are NOT extracted yet
    - This keeps the pipeline simple and explainable
    """

    # Step 1: Try to open the PDF file and extract using pdfplumber
    raw_text = ""
    try:
        pdf = open_pdf(pdf_path)
        try:
            # Step 2: Extract raw text from all pages
            raw_text = extract_full_text(pdf)
        finally:
            try:
                pdf.close()
            except Exception:
                pass
    except Exception:
        # Fallback: try PyMuPDF to extract text directly from file
        try:
            raw_text = extract_text_with_pymupdf(pdf_path)
        except Exception:
            raw_text = ""

    # Step 3: Apply basic text cleaning
    cleaned_text = basic_text_cleaning(raw_text)

    # Step 4: Split cleaned text into logical sections
    sections_dict = split_text_into_sections(cleaned_text)

    # Step 5: Convert section text into PaperSection objects
    section_models = convert_sections_to_models(sections_dict)

    # Step 6: Extract abstract text separately if available
    abstract_text = ""
    for section in section_models:
        if section.section_name.lower() == "abstract":
            abstract_text = section.content
            break

    # Step 7: Create the ResearchPaper object
    paper = ResearchPaper(
        paper_id=paper_id,
        title=title,
        authors=authors,
        abstract=abstract_text,
        sections=section_models
    )

    # Return the structured ResearchPaper object
    return paper
