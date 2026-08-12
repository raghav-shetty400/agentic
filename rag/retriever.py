from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(

    "faiss_db",

    embeddings,

    allow_dangerous_deserialization=True
)


def search_knowledge(query):

    query = query.lower()

    # GREETING HANDLING

    if query in ["hi", "hello", "hey"]:

        return "Hello 👋 Welcome to AI Baby Camera Support"

    results = db.similarity_search(query, k=1)

    if results:

        return results[0].page_content

    return "Sorry, I could not understand."