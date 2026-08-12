from database.mysql_db import get_mysql_connection

def get_user(username):

    conn = get_mysql_connection()

    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM users
    WHERE name=%s
       OR email=%s
    """

    cursor.execute(sql, (username, username))

    user = cursor.fetchone()

    cursor.close()

    return user