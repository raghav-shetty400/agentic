from memory.save_memory import create_memory
from memory.retrieve_memory import get_memory


def memory_agent(state):

    question = state["question"]

    if "remember" in question:

        create_memory(question)

        return {
            "answer": "Memory saved"
        }

    memories = get_memory()

    return {
        "answer": memories
    }
