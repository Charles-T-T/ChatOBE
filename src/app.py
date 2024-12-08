from flask import Flask, render_template, request, jsonify, redirect, url_for, session  
from db.db_utils import query_database, check_user_credentials 
from ChatOBE import ChatOBE

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = '97992c973fff1906706a1cb0512f2cf3'

# 创建ChatOBE实例
chatobe = ChatOBE()

# 登录页面  
@app.route("/login", methods=["GET", "POST"])  
def login():  
    if request.method == "POST":  
        data = request.get_json()  
        user_id = data.get("user_id")  
        password = data.get("password")  

        # 从数据库检查用户凭据  
        user = check_user_credentials(user_id, password)  

        if user:  # 如果用户存在，则登录成功  
            session['logged_in'] = True  
            session['user_id'] = user_id  # 可以将用户ID存储在会话中  
            print(f"User {user_id} logged in.")  # 调试信息  
            return jsonify({"success": True})  
        else:  
            return jsonify({"success": False, "message": "学号或密码错误。"})  

    return render_template("login.html")  # 显示登录页面  

# 首页（未登录时重定向）
@app.route("/")  
def index():  
    if not session.get('logged_in'):  # 如果用户未登录，重定向到登录页面  
        return redirect(url_for('login'))  

    WELCOME_MSG = "欢迎使用ChatOBE~ \n 我是结合了大语言模型的OBE系统，可以帮你进行选课、查询等等。需要我帮你做些什么？"  
    return render_template("index.html", initial_message=WELCOME_MSG)  


# 处理用户消息
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    ai_message = chatobe.chat(user_message)
    return jsonify({"ai_message": ai_message})


if __name__ == "__main__":
    app.run(debug=True)
    # http://127.0.0.1:5000/
