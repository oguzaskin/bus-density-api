from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Tüm domainlerden gelen isteklere izin ver

# Örnek RAM tabanlı veri (yolcu sayısı)
bus_data = {
    42: 15,
    43: 8,
    44: 23
}

@app.route("/")
def home():
    return "API çalışıyor!"

@app.route("/bus/<int:bus_id>")
def get_bus(bus_id):
    count = bus_data.get(bus_id, 0)
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run()
