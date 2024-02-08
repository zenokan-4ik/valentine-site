from flask import Flask, request, render_template, jsonify, redirect, make_response
from flask_login import LoginManager
import database as db

click_count = []

app = Flask(__name__)

#init users database
db.init_db()

@app.route("/")
def home():
    return render_template("linktree.html")

@app.route("/main", methods=["POST", "GET"])
def valentine():
    return render_template("main.html")

@app.route("/valentine", methods=['POST', 'GET'])
def change_page():
    return render_template("valentine.html")

@app.route("/register-page", methods=["POST",  "GET"])
def register_page():
    return render_template("registration.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    name = request.args.get('name')
    login = request.args.get('login')
    password = request.args.get('password')
    email = request.args.get('email')
    data = db.register_user(name, login, password, email)
    if data[0]:
        resp = make_response(jsonify(data))
        resp.set_cookie('user', login)
        print(request.cookies.get('user'))
        return resp
    return jsonify(data)

@app.route("/login-page", methods=['POST', 'GET'])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    login = request.args.get("login")
    password = request.args.get("password")
    db_response = db.login_user(login, password)
    if db_response[0]:
        resp = make_response(jsonify(db_response[1]))
        resp.set_cookie('user', login)
        return resp
    return jsonify(db_response[1])

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    resp = make_response('Вы вышли из своего аккаунта!')
    resp.set_cookie('user', '')
    return resp

@app.route('/update_click_count', methods=['POST'])
def update_click_count():
    global click_count
    data = request.get_json()
    click_count.append(data['clickCount'])
    return jsonify({'message': 'Click count updated successfully', 'clickCount': click_count})

@app.route("/admin", methods=["POST", "GET"])
def admin():
    list = ['/clicks', '/rofl/<>']
    return render_template('admin.html', admin_text=f'доступные админ страницы:', list=list)

@app.route("/admin/clicks", methods=["POST", "GET"])
def get_clicks():
    return render_template("admin.html", admin_text=click_count)

@app.route("/admin/rofl/<text>", methods=["POST", "GET"])
def rofl(text):
    return render_template("admin.html", admin_text=text)

@app.route("/yipeee", methods=["POST", "GET"])
def yipeee():
    return render_template("yipee.html")

@app.route("/see_cookies")
def see_cookie():
    return str(request.cookies.get('user'))

if __name__ == "__main__":
    app.run(debug=True)