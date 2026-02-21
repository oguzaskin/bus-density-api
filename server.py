from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

current_count = 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/count", methods=["POST"])
def count():
    global current_count
    data = request.get_json()
    current_count = data.get("count", 0)
    return jsonify({"status": "ok"})

@app.route("/data", methods=["GET"])
def data():
    return jsonify({"count": current_count})

if __name__ == "__main__":
    app.run()
