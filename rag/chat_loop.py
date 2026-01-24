# This file implements a simple interactive chat loop
# over a single research paper using RAG

from indexing.faiss_index import semantic_search
from rag.basic_rag import generate_answer_with_sources


def rag_chat_loop(
    model,
    index,
    embedded_chunks: list
):
    """
    This function runs a simple question-answer loop
    over a single research paper.

    The user can ask multiple questions one by one.
    Type 'exit' to stop the chat.
    """

    print("Research Paper Chat Assistant")
    print("Type 'exit' to end the conversation\n")

    while True:
        # Take user input
        query = input("Ask a question: ")

        # Exit condition
        if query.lower() == "exit":
            print("Ending chat.")
            break

        # Step 1: Retrieve relevant chunks using semantic search
        retrieved_chunks = semantic_search(
            query=query,
            model=model,
            index=index,
            chunks=embedded_chunks,
            top_k=3
        )

        # Step 2: Generate answer using GROQ LLM
        result = generate_answer_with_sources(
            query=query,
            retrieved_chunks=retrieved_chunks
        )

        # Display answer
        print("\nAnswer:")
        print(result["answer"])

        # Display sources
        print("\nSources:")
        for source in result["sources"]:
            print(
                f"- Section: {source['section']} "
                f"(Chunk ID: {source['chunk_id']})"
            )

        print("\n" + "-" * 50 + "\n")
