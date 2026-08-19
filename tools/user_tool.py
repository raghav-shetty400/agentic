import time

from database.mysql_db import get_mysql_connection


def get_user(username):

    # =================================================
    # MYSQL CONNECTION
    # =================================================

    start = time.time()

    conn = get_mysql_connection()

    connection_time = time.time() - start

    print(
        f"MYSQL CONNECTION: {connection_time:.2f} sec"
    )

    # =================================================
    # QUERY
    # =================================================

    start = time.time()

    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM users
        WHERE name = %s
           OR email = %s
        LIMIT 1
    """

    cursor.execute(
        sql,
        (username, username)
    )

    user = cursor.fetchone()

    query_time = time.time() - start

    print(
        f"MYSQL QUERY: {query_time:.2f} sec"
    )

    # =================================================
    # CLOSE
    # =================================================

    cursor.close()
    conn.close()

    # =================================================
    # TOTAL
    # =================================================

    total_time = connection_time + query_time

    print(
        f"GET USER TOTAL: {total_time:.2f} sec"
    )

    return user