from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# In-memory storage (ileride DB / Redis kullanılabilir)
bus_data = {}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "OK",
        "service": "Bus Density REST API"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/update/<bus_id>", methods=["POST"])
def update_bus(bus_id):
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()

    if "people_count" not in data:
        return jsonify({"error": "people_count field missing"}), 400

    try:
        people_count = int(data["people_count"])
        if people_count < 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "people_count must be a non-negative integer"}), 400

    bus_data[bus_id] = people_count

    return jsonify({
        "message": "Bus data updated",
        "bus_id": bus_id,
        "people_count": people_count
    }), 200


@app.route("/bus/<bus_id>", methods=["GET"])
def get_bus(bus_id):
    return jsonify({
        "bus_id": bus_id,
        "people_count": bus_data.get(bus_id, 0)
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
