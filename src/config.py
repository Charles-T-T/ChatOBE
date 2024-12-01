DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "charles@mysql0618",
    "port": 3306,
    "charset": "utf8mb4",
    "database": "sc",
}

# author: FHT
# 这里用的是我自己的openai-api-key
# github保护机制不允许上传
# 所以运行的时候要把下面这行注释取消，并换成群里的key
OPENAI_API_KEY = "your-key"
MODEL = "gpt-4o"

PROMPT = """
你是一款课业管理助手（名叫ChatOBE，帮助用户管理选课信息、作业、成绩等内容。
你面向的用户可能是学生，也可能是老师，用户不同时你的功能会有一定的差异。
请用专业且友好的语气回答用户的问题。
请牢记这些内容，记住你的功能和任务。
"""
SUMMARY_PROMPT = "下面是先前聊天记录的总结：\n\n"
