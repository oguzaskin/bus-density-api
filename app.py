from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Bellek içi veri (ileride DB’ye taşınabilir)
bus_data = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "OK",
        "message": "Bus Density REST API is running"
    }), 200


@app.route("/update/<bus_id>", methods=["POST"])
def update_bus(bus_id):
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()

    if "people_count" not in data:
        return jsonify({"error": "people_count field missing"}), 400

    try:
        people_count = int(data["people_count"])
    except ValueError:
        return jsonify({"error": "people_count must be an integer"}), 400

    bus_data[bus_id] = people_count

    return jsonify({
        "message": "Bus data updated",
        "bus_id": bus_id,
        "people_count": people_count
    }), 200


@app.route("/bus/<bus_id>", methods=["GET"])
def get_bus(bus_id):
    if bus_id not in bus_data:
        return jsonify({
            "bus_id": bus_id,
            "people_count": 0,
            "note": "No data yet"
        }), 200

    return jsonify({
        "bus_id": bus_id,
        "people_count": bus_data[bus_id]
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
