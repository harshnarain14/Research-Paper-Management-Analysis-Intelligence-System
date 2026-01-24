# Streamlit UI for Research Paper Intelligence System
# This app allows:
# 1. Uploading a research paper PDF
# 2. Parsing the paper
# 3. Chatting with the paper using RAG

import streamlit as st
import tempfile
from ingestion.pdf_parser import build_research_paper
from indexing.text_chunker import chunk_sections
from indexing.embeddings import load_embedding_model, embed_chunks
from indexing.faiss_index import create_faiss_index, semantic_search
from rag.basic_rag import generate_answer_with_sources


def main():
    # Page configuration
    st.set_page_config(
        page_title="Research Paper Assistant",
        layout="wide"
    )

    st.title("📄 Research Paper Intelligence System")

    # -------------------------------
    # PDF UPLOAD SECTION
    # -------------------------------
    st.sidebar.header("Upload Research Paper")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a research paper PDF",
        type=["pdf"]
    )

    # Initialize session state
    if "paper" not in st.session_state:
        st.session_state.paper = None
    if "index" not in st.session_state:
        st.session_state.index = None
    if "embedded_chunks" not in st.session_state:
        st.session_state.embedded_chunks = None
    if "model" not in st.session_state:
        st.session_state.model = None

    # If a PDF is uploaded
    if uploaded_file is not None:
        with st.spinner("Processing research paper..."):

            # Save uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            # Build ResearchPaper object
            paper = build_research_paper(
                pdf_path=pdf_path,
                paper_id="uploaded_paper",
                title=uploaded_file.name,
                authors=["Unknown"]
            )

            # Chunk sections
            chunks = chunk_sections(
                sections=paper.sections,
                paper_id=paper.paper_id,
                chunk_size=300
            )

            # Load embedding model once
            model = load_embedding_model()

            # Generate embeddings
            embedded_chunks = embed_chunks(model, chunks)

            # Create FAISS index
            index, _ = create_faiss_index(embedded_chunks)

            # Store in session state
            st.session_state.paper = paper
            st.session_state.index = index
            st.session_state.embedded_chunks = embedded_chunks
            st.session_state.model = model

        st.success("Paper uploaded and processed successfully!")

    # -------------------------------
    # PAPER DETAILS SECTION
    # -------------------------------
    if st.session_state.paper:
        paper = st.session_state.paper

        st.subheader("📌 Paper Details")
        st.write("**Title:**", paper.title)
        st.write("**Authors:**", ", ".join(paper.authors))

        st.subheader("Abstract")
        st.write(paper.abstract)

        # -------------------------------
        # CHAT SECTION
        # -------------------------------
        st.subheader("💬 Ask Questions About the Paper")

        user_query = st.text_input("Enter your question")

        if user_query:
            if st.session_state.model is None or st.session_state.index is None or st.session_state.embedded_chunks is None:
                st.error("Please upload and process a paper first.")
            else:
                with st.spinner("Generating answer..."):

                    retrieved_chunks = semantic_search(
                        query=user_query,
                        model=st.session_state.model,
                        index=st.session_state.index,
                        chunks=st.session_state.embedded_chunks,
                        top_k=3
                    )

                    result = generate_answer_with_sources(
                        query=user_query,
                        retrieved_chunks=retrieved_chunks
                    )

                st.markdown("### ✅ Answer")
                st.write(result["answer"])

                st.markdown("### 📚 Sources")
                for src in result["sources"]:
                    st.write(
                        f"- Section: {src['section']} | Chunk ID: {src['chunk_id']}"
                    )


# Run Streamlit app
if __name__ == "__main__":
    main()
