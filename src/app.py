import openai
import markdown
from flask import Flask, render_template, request, jsonify
from db.db_utils import query_database
from config import OPENAI_API_KEY

# 创建 Flask 应用
app = Flask(__name__)

PROMPT = """
你是一款课业管理助手（名叫ChatOBE，帮助用户管理选课信息、作业、成绩等内容。
你面向的用户可能是学生，也可能是老师，用户不同时你的功能会有一定的差异。
请用专业且友好的语气回答用户的问题。
请牢记这些内容，记住你的功能和任务。
"""

# openai.api_key = OPENAI_API_KEY  # 添加api-key后，这行注释掉

# 存储对话历史
conversation_history = [
    {
        "role": "system",
        "content": PROMPT,
    }
]


# 创建函数与 OpenAI API 进行交互
def get_ai_response(user_input):
    # 将用户消息添加到历史中
    conversation_history.append({"role": "user", "content": user_input})

    # 与 OpenAI API 交互，传递整个对话历史
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", messages=conversation_history  # 使用 gpt-3.5-turbo 模型
    )

    # 获取 AI 回复并将其添加到历史中
    ai_message = response.choices[0].message.content.strip()
    ai_message = ai_message.replace("| |", "|\n|").replace("\\n", "\n")
    conversation_history.append({"role": "assistant", "content": ai_message})

    # 将 AI 回复转换为 Markdown 格式
    md_message = markdown.markdown(ai_message)  # 转换为 HTML 格式

    return md_message


# 首页
@app.route("/")
def index():
    WELCOME_MSG = "欢迎使用ChatOBE~ \n 我是结合了大语言模型的OBE系统，可以帮你进行选课、查询等等。需要我帮你做些什么？"
    return render_template("index.html", initial_message=WELCOME_MSG)


# 处理用户消息
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    ai_message = get_ai_response(user_message)
    return jsonify({"ai_message": ai_message})


if __name__ == "__main__":
    app.run(debug=True)
    # http://127.0.0.1:5000/
