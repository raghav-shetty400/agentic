import sqlite3

DB_NAME = "chatbot.db"


def save_memory(memory):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memory (user_memory) VALUES (?)",
        (memory,)
    )

    conn.commit()
    conn.close()


def retrieve_memories():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT user_memory FROM memory")

    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]
