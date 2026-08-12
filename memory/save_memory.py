from memory.sqlite_memory import save_memory


def create_memory(user_text):

    save_memory(user_text)

    return "Memory stored"
