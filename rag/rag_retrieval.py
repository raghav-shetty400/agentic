from rag.retriever import retrieve_documents


def rag_retrieval(state):

    print()
    print("====================================")
    print("          RAG RETRIEVAL NODE")
    print("====================================")
    print("FILE     : rag/rag_retrieval.py")
    print("FUNCTION : rag_retrieval()")

    question = state.get("question", "")

    print("QUESTION :", question)

    documents = retrieve_documents(
        query=question,
        top_k=4
    )

    print()
    print("RETRIEVED DOCUMENTS:")
    
    for i, document in enumerate(documents):
        print(f"--- DOCUMENT {i + 1} ---")
        print(document[:500])

    context = "\n\n".join(documents)

    print()
    print("CONTEXT LENGTH :", len(context))
    print("DOCUMENT COUNT :", len(documents))

    return {
        **state,
        "context": context
    }