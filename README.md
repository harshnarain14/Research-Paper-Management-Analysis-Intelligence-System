# 📄 Research Paper Management & Analysis Intelligence System

An end-to-end **GenAI-powered Research Paper Intelligence System** that allows users to upload a research paper PDF and interact with it through a conversational chat interface using **Retrieval-Augmented Generation (RAG)**.

This project is designed to mirror **real-world academic search engines and research assistants**, combining document intelligence, semantic search, and LLM-based reasoning.

---

## 🚀 Project Overview

Researchers today face challenges such as:

- Reading long research papers end-to-end
- Finding relevant sections quickly
- Asking precise questions about a paper
- Understanding contributions, results, and limitations efficiently

This system solves these problems by enabling:

- Automatic paper ingestion and parsing
- Semantic search across paper content
- Context-aware question answering
- Transparent answers with source attribution
- A clean and interactive Streamlit-based chat UI

---

## 🎯 Objectives

The system is designed to:

1. Ingest and parse research paper PDFs
2. Extract and structure academic sections (Abstract, Methods, Results, etc.)
3. Chunk content intelligently for semantic retrieval
4. Index content using FAISS vector search
5. Answer user questions using Retrieval-Augmented Generation (RAG)
6. Provide grounded answers with section-level citations
7. Offer an intuitive researcher-facing UI using Streamlit

---

## 🧠 System Architecture (High Level)

PDF Upload
↓
Text Extraction & Section Parsing
↓
Section-based Chunking
↓
Embedding Generation
↓
FAISS Vector Index
↓
Semantic Retrieval
↓
RAG with GROQ LLM
↓
Streamlit Chat UI


---

## 🧱 Project Structure

genai_research_assistant/
│
├── app.py # Streamlit application (UI entry point)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── ingestion/
│ ├── init.py
│ └── pdf_parser.py # PDF parsing and section extraction
│
├── indexing/
│ ├── init.py
│ ├── text_chunker.py # Section-aware chunking logic
│ ├── embeddings.py # Embedding model loading
│ └── faiss_index.py # FAISS indexing and semantic search
│
├── rag/
│ ├── init.py
│ ├── basic_rag.py # RAG answer generation with sources
│ └── chat_loop.py # Interactive RAG chat logic
│
├── mcp/
│ ├── init.py
│ ├── tools.py # MCP-style external research tools
│ ├── tool_router.py # Tool routing logic
│ └── response_builder.py # Unified response generation
│
└── citations/
├── init.py
└── citation_extractor.py # Citation extraction and enrichment


---

## 📄 Document Ingestion & Representation

### PDF Parsing
- Research papers are loaded using Python-based PDF parsing
- Text is cleaned and normalized
- Academic sections are detected using rule-based heuristics

### Section-Level Representation
Each paper is internally represented using:
- Paper metadata (title, authors, year)
- Structured sections (Abstract, Introduction, Methods, Results, Conclusion)
- References section for citation tracking

---

## 🔎 Chunking & Semantic Indexing

### Intelligent Chunking
- Section-based chunking strategy
- Preserves metadata such as:
  - Paper ID
  - Section name
  - Chunk ID

### Vector Indexing
- Sentence-transformer embeddings are generated for each chunk
- FAISS is used for efficient vector similarity search
- Enables fast semantic retrieval across the paper

---

## 🤖 Retrieval-Augmented Generation (RAG)

The RAG pipeline works as follows:

1. User submits a question
2. Question embedding is generated
3. Relevant chunks are retrieved from FAISS
4. Retrieved context is passed to the LLM
5. GROQ LLM generates a grounded answer
6. Sources (sections + chunks) are returned with the answer

This ensures:
- Minimal hallucination
- High factual grounding
- Transparent source attribution

---

## 📚 Source Attribution

Every generated answer includes:
- Paper ID
- Section name
- Chunk ID

This improves:
- Trustworthiness
- Explainability
- Academic usability

---

## 💬 Streamlit Chat Interface

The system includes a real-time chat interface built using **Streamlit**:

### Key UI Features
- PDF upload from sidebar
- One-time document processing
- Chat-style interaction (`st.chat_input`)
- Persistent chat history using session state
- Real-time answers with citations

---

## 🔌 MCP-Style Tool Integration

To simulate real-world research systems, the project includes **MCP-style tools**:

### Tools Implemented
- Paper metadata lookup
- Related work discovery
- Trend analytics (simulated)

A rule-based router decides whether:
- A tool should be called
- Or the RAG pipeline should handle the query

This design keeps the system:
- Transparent
- Debuggable
- Easily extensible

---

## 🧪 Evaluation Scenarios

The system was tested on scenarios such as:

1. Quickly understanding a new paper
2. Asking section-specific questions
3. Identifying limitations of a method
4. Exploring related work
5. Validating grounded answers

---

## ⚠️ Limitations

- Supports single-paper analysis (current version)
- Section detection is rule-based
- External research tools are simulated
- Large PDFs may increase processing time

---

## 🚀 Future Improvements

- Multi-document paper library
- Real citation APIs (Semantic Scholar, arXiv)
- Research trend visualization
- Improved section detection using ML
- Hybrid RAG with real-time web search

---

## 🛠️ Tech Stack

- **Language:** Python
- **LLM:** GROQ (LLaMA 3)
- **Vector Store:** FAISS
- **Embeddings:** Sentence Transformers
- **UI:** Streamlit
- **Orchestration:** LangChain concepts

---

## ▶️ How to Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py