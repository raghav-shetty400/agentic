from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import CharacterTextSplitter

from langchain_core.documents import Document


def create_vector_db():

    with open("rag/docs/knowledge.txt", "r", encoding="utf-8") as f:

        text = f.read()

    splitter = CharacterTextSplitter(

        chunk_size=200,

        chunk_overlap=20
    )

    chunks = splitter.split_text(text)

    docs = [Document(page_content=chunk) for chunk in chunks]

    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)

    db.save_local("faiss_db")

    print("Vector DB Created")


if __name__ == "__main__":

    create_vector_db()