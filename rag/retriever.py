from rag.embeddings import get_embedding
from rag.vector_store import search


def retrieve_documents(query, top_k=4):

    print()
    print("========== RAG RETRIEVER ==========")
    print("FILE     : rag/retriever.py")
    print("FUNCTION : retrieve_documents()")
    print("QUERY    :", query)
    print("TOP K    :", top_k)

    query_embedding = get_embedding(query)

    results = search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    documents = results.get("documents", [[]])[0]

    metadatas = results.get("metadatas", [[]])[0]

    print()
    print("RETRIEVED DOCUMENTS :", len(documents))

    for i, document in enumerate(documents):

        print()
        print(f"--- RESULT {i + 1} ---")
        print("SOURCE :", metadatas[i] if i < len(metadatas) else "")
        print("TEXT   :", document[:300])

    print("====================================")

    return documents