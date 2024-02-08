from flask import Flask, request, render_template, jsonify
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
    return jsonify(data)


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

if __name__ == "__main__":
    app.run(debug=True)