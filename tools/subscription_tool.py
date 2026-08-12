from database.mysql_db import get_mysql_connection


def get_subscription(device_id):

    conn = get_mysql_connection()

    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM device_subscriptions
    WHERE device_id = %s
    """

    cursor.execute(sql, (device_id,))

    subscription = cursor.fetchone()

    cursor.close()
    conn.close()

    return subscription