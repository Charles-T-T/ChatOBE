from flask import Flask, render_template, request, jsonify
from db.db_utils import query_database
from ChatOBE import ChatOBE

# 创建 Flask 应用
app = Flask(__name__)


# 创建ChatOBE实例
chatobe = ChatOBE()


# 首页
@app.route("/")
def index():
    WELCOME_MSG = "欢迎使用ChatOBE~ \n 我是结合了大语言模型的OBE系统，可以帮你进行选课、查询等等。需要我帮你做些什么？"
    return render_template("index.html", initial_message=WELCOME_MSG)


# 处理用户消息
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]

    # 测试：根据用户输入查询数据库
    if "查询课程" in user_message:
        sql = "SELECT * FROM course WHERE cname LIKE %s"
        params = (f"%{user_message.split()[-1]}%",)
        db_results = query_database(sql, params)
    else:
        db_results = None

    ai_message = chatobe.chat(user_message, db_results=db_results)
    return jsonify({"ai_message": ai_message})


if __name__ == "__main__":
    app.run(debug=True)
    # http://127.0.0.1:5000/
