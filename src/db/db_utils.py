import pymysql
from config import DATABASE_CONFIG


def get_db_connection():
    """建立数据库连接"""
    conn = pymysql.connect(
        host=DATABASE_CONFIG["host"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        port=DATABASE_CONFIG["port"],
        charset=DATABASE_CONFIG["charset"],
        database=DATABASE_CONFIG["database"]
    )
    return conn


def query_database(conn, sql):
    """执行查询语句并返回结果"""
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return results
