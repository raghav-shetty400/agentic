from database.mysql_db import get_mysql_connection

def get_device(user_id):

    conn = get_mysql_connection()

    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM devices
    WHERE user_id=%s
    """

    cursor.execute(sql, (user_id,))

    device = cursor.fetchone()

    cursor.close()

    return device