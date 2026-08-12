from database.mysql_db import get_mysql_connection


def get_settings(device_id):

    conn = get_mysql_connection()

    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM device_settings
    WHERE device_id = %s
    """

    cursor.execute(sql, (device_id,))

    settings = cursor.fetchall()

    cursor.close()
    conn.close()

    return settings