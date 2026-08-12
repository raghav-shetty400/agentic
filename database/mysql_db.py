import mysql.connector


def get_mysql_connection():

    return mysql.connector.connect(
        host="database-1.cghiaau8yfbh.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Raghu_9964",
        database="h2o",
        port=3306,
        autocommit=True
    )