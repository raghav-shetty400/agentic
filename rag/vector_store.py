import chromadb


CHROMA_PATH = "./rag/vectorstore"

COLLECTION_NAME = "iot_knowledge"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_documents(documents, embeddings, ids, metadatas=None):

    print()
    print("========== VECTOR STORE ==========")
    print("FILE     : rag/vector_store.py")
    print("FUNCTION : add_documents()")
    print("DOCUMENTS:", len(documents))

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print("VECTOR STORE : Documents added")
    print("==================================")


def search(query_embedding, top_k=4):

    print()
    print("========== VECTOR SEARCH ==========")
    print("FILE     : rag/vector_store.py")
    print("FUNCTION : search()")
    print("TOP K    :", top_k)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print(
        "RESULTS :",
        len(results["documents"][0])
        if results["documents"]
        else 0
    )

    print("===================================")

    return results