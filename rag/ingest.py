import os
import uuid

from rag.embeddings import get_embedding
from rag.vector_store import add_documents


DOCUMENT_FOLDER = "rag/docs"


def split_text(text, chunk_size=800, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def ingest_documents():

    print()
    print("====================================")
    print("        RAG DOCUMENT INGESTION")
    print("====================================")
    print("FILE     : rag/ingest.py")
    print("FUNCTION : ingest_documents()")
    print("FOLDER   :", DOCUMENT_FOLDER)

    documents = []
    embeddings = []
    ids = []
    metadatas = []

    for filename in os.listdir(DOCUMENT_FOLDER):

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        if not os.path.isfile(file_path):
            continue

        if not filename.endswith(".txt"):
            continue

        print()
        print("READING FILE :", filename)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        print("TEXT LENGTH :", len(text))

        chunks = split_text(text)

        print("CHUNKS CREATED :", len(chunks))

        for index, chunk in enumerate(chunks):

            print(
                f"Embedding chunk {index + 1}/{len(chunks)}"
            )

            embedding = get_embedding(chunk)

            documents.append(chunk)
            embeddings.append(embedding)

            ids.append(
                str(uuid.uuid4())
            )

            metadatas.append({
                "source": filename,
                "chunk": index
            })

    if not documents:

        print()
        print("NO DOCUMENTS FOUND")
        return

    add_documents(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print()
    print("====================================")
    print("INGESTION COMPLETED")
    print("TOTAL CHUNKS :", len(documents))
    print("====================================")


if __name__ == "__main__":
    ingest_documents()