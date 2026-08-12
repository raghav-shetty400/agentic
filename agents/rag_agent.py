from rag.retriever import search_knowledge


def rag_agent(state):

    question = state["question"]

    result = search_knowledge(question)

    return {

        "answer": result
    }