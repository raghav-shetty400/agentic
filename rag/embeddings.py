import requests


OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text"


def get_embedding(text):
    print()
    print("========== EMBEDDING ==========")
    print("FILE     : rag/embeddings.py")
    print("FUNCTION : get_embedding()")
    print("MODEL    :", EMBEDDING_MODEL)
    print("TEXT LEN :", len(text))

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        },
        timeout=120
    )

    response.raise_for_status()

    embedding = response.json()["embedding"]

    print("EMBEDDING SIZE :", len(embedding))
    print("==============================")

    return embedding