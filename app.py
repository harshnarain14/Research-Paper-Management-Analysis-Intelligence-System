# Streamlit UI for Research Paper Intelligence System

import streamlit as st
import tempfile

from ingestion.pdf_parser import build_research_paper
from indexing.text_chunker import chunk_sections
from indexing.embeddings import load_embedding_model, embed_chunks
from indexing.faiss_index import create_faiss_index, semantic_search
from rag.basic_rag import generate_answer_with_sources


def main():
    # -------------------------------
    # PAGE CONFIG
    # -------------------------------
    st.set_page_config(
        page_title="Research Paper Assistant",
        layout="wide"
    )

    st.title("📄 Research Paper Intelligence System")

    # -------------------------------
    # SIDEBAR UPLOAD
    # -------------------------------
    st.sidebar.header("Upload Research Paper")

    uploaded_file = st.sidebar.file_uploader(
        "Upload a research paper PDF",
        type=["pdf"]
    )

    # -------------------------------
    # SESSION STATE INIT
    # -------------------------------
    if "paper" not in st.session_state:
        st.session_state.paper = None
    if "index" not in st.session_state:
        st.session_state.index = None
    if "embedded_chunks" not in st.session_state:
        st.session_state.embedded_chunks = None
    if "model" not in st.session_state:
        st.session_state.model = None

    # -------------------------------
    # PROCESS PDF
    # -------------------------------
    if uploaded_file is not None:
        with st.spinner("Processing research paper..."):

            try:
                # Save PDF temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    pdf_path = tmp.name

                # -------------------------------
                # BUILD PAPER (PDF PARSING)
                # -------------------------------
                paper = build_research_paper(
                    pdf_path=pdf_path,
                    paper_id="uploaded_paper",
                    title=uploaded_file.name,
                    authors=["Unknown"]
                )

                # 🔥 DEBUG CHECK
                if not paper or not paper.sections:
                    st.error("❌ Failed to parse PDF. Try another file.")
                    st.stop()

                # -------------------------------
                # CHUNKING
                # -------------------------------
                chunks = chunk_sections(
                    sections=paper.sections,
                    paper_id=paper.paper_id,
                    chunk_size=300
                )

                if not chunks:
                    st.error("❌ No content extracted from PDF.")
                    st.stop()

                # -------------------------------
                # LOAD MODEL
                # -------------------------------
                model = load_embedding_model()

                # -------------------------------
                # EMBEDDINGS
                # -------------------------------
                embedded_chunks = embed_chunks(model, chunks)

                if not embedded_chunks:
                    st.error("❌ Embeddings failed.")
                    st.stop()

                # -------------------------------
                # FAISS INDEX
                # -------------------------------
                index, _ = create_faiss_index(embedded_chunks)

                if index is None:
                    st.error("❌ Failed to create FAISS index.")
                    st.stop()

                # -------------------------------
                # SAVE STATE
                # -------------------------------
                st.session_state.paper = paper
                st.session_state.index = index
                st.session_state.embedded_chunks = embedded_chunks
                st.session_state.model = model

                st.success("✅ Paper processed successfully!")

            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
                st.stop()

    # -------------------------------
    # DISPLAY PAPER DETAILS
    # -------------------------------
    if st.session_state.paper:
        paper = st.session_state.paper

        st.subheader("📌 Paper Details")
        st.write("**Title:**", paper.title)
        st.write("**Authors:**", ", ".join(paper.authors))

        st.subheader("Abstract")
        st.write(paper.abstract if paper.abstract else "No abstract found")

        # -------------------------------
        # CHAT SECTION
        # -------------------------------
        st.subheader("💬 Ask Questions About the Paper")

        user_query = st.text_input("Enter your question")

        if user_query:
            if (
                st.session_state.model is None
                or st.session_state.index is None
                or st.session_state.embedded_chunks is None
            ):
                st.error("Please upload and process a paper first.")
            else:
                with st.spinner("Generating answer..."):
                    try:
                        # -------------------------------
                        # RETRIEVAL
                        # -------------------------------
                        retrieved_chunks = semantic_search(
                            query=user_query,
                            model=st.session_state.model,
                            index=st.session_state.index,
                            chunks=st.session_state.embedded_chunks,
                            top_k=3
                        )

                        if not retrieved_chunks:
                            st.warning("⚠️ No relevant content found.")
                            st.stop()

                        # -------------------------------
                        # GENERATION
                        # -------------------------------
                        result = generate_answer_with_sources(
                            query=user_query,
                            retrieved_chunks=retrieved_chunks
                        )

                        # -------------------------------
                        # OUTPUT
                        # -------------------------------
                        st.markdown("### ✅ Answer")
                        st.write(result.get("answer", "No answer generated"))

                        st.markdown("### 📚 Sources")
                        for src in result.get("sources", []):
                            st.write(
                                f"- Section: {src.get('section')} | Chunk ID: {src.get('chunk_id')}"
                            )

                    except Exception as e:
                        st.error(f"❌ Error generating answer: {str(e)}")


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    main()
