from flask import Flask, render_template, request, jsonify

from ChatOBE import ChatOBE
import config

# 创建 Flask 应用
app = Flask(__name__)


# 创建ChatOBE实例
chatobe = ChatOBE()


# 首页
@app.route("/")
def index():
    return render_template("index.html", initial_message=config.WELCOME_MSG)


# 处理用户消息
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    ai_message = chatobe.chat(user_message)
    return jsonify({"ai_message": ai_message})


if __name__ == "__main__":
    app.run(debug=True)
    # http://127.0.0.1:5000/
