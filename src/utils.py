"""
一些辅助类/方法
"""

import tiktoken
import config
import pymysql
from config import DATABASE_CONFIG

enc = tiktoken.encoding_for_model(config.MODEL)

def count_token(text):
    """计算text对应的token数"""
    tokens = enc.encode(text)
    return len(tokens)


def get_db_connection():
    """建立数据库连接"""
    conn = pymysql.connect(
        host=DATABASE_CONFIG["host"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        port=DATABASE_CONFIG["port"],
        charset=DATABASE_CONFIG["charset"],
        database=DATABASE_CONFIG["database"],
    )
    return conn


def query_database(sql):
    """执行 SQL 语句并返回结果（字符串形式）"""
    try:
        # 正常情况：执行 SQL
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)

                # 如果是查询操作，获取列名和结果
                if sql.strip().upper().startswith("SELECT"):
                    column_names = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()

                    # 检查是否有结果
                    if not results:
                        return "Success: Query executed, but no results found."

                    # 构造查询结果字符串
                    result_str = f"Columns: {', '.join(column_names)}\n"
                    for row in results:
                        result_str += f"Row: {', '.join(map(str, row))}\n"
                    return f"Success:\n{result_str}"
                else:
                    # 对于非查询操作，获取受影响行数
                    affected_rows = cursor.rowcount
                    conn.commit()
                    return f"Success: {affected_rows} row(s) affected."
    except Exception as e:
        # 出现异常：返回错误信息
        return f"Fail, error: {str(e)}"


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

    return user  


def sql_in_text(text):
    """判断text中是否有sql语句"""
    return config.SQL_START in text and config.SQL_END in text


def extract_sql(text):
    """从text中提取sql语句"""
    start = text.find(config.SQL_START) + len(config.SQL_START)
    end = text.find(config.SQL_END)
    return text[start:end].strip()


def get_cur_time():
    """获取当前时间（年月日，时间，星期几）"""
    sql = "select NOW(), DAYNAME(NOW());"
    try:
        # 正常情况：执行sql并提交事务、返回结果
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
            conn.commit()
        return str(results)
    except Exception as e:
        # 出现异常：返回报错
        return f"Fail, error: {str(e)}"


def get_user_identity(user_id):
    """获取当前用户的身份（老师/学生/DBA）"""
    sql = f"""
    SELECT 
        CASE status
            WHEN 'S' THEN '学生'
            WHEN 'T' THEN '老师'
            WHEN 'DBA' THEN '管理员'
            ELSE '未知'
        END AS 用户身份
    FROM obe.user
    WHERE user_id = {user_id};
    """
    return query_database(sql)
