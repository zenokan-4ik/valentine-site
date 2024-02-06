from flask import Flask, request, render_template, jsonify


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/change", methods=['POST', 'GET'])
def change_page():
    return render_template("valentine.html")

@app.route('/update_click_count', methods=['POST'])
def update_click_count():
    global click_count
    data = request.get_json()
    click_count = data['clickCount']
    with open("result.txt", "r+") as file:
        file.write(str(click_count))
    return jsonify({'message': 'Click count updated successfully', 'clickCount': click_count})

@app.route("/yipeee", methods=["POST", "GET"])
def yipeee():
    return render_template("yipee.html")

if __name__ == "__main__":
    app.run(debug=True)