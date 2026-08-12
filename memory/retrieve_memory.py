from memory.sqlite_memory import retrieve_memories


def get_memory():

    memories = retrieve_memories()

    return "\n".join(memories)
