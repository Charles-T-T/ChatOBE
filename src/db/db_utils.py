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

def check_user_credentials(user_id, password):  
    """  
    检查用户凭据是否正确  
    """  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            sql = "SELECT * FROM obe.user WHERE user_id = %s AND password = %s"  
            cursor.execute(sql, (user_id, password))  
            user = cursor.fetchone()  
    finally:  
        connection.close()  
    
    return user  # 返回查询结果  