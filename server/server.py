from flask import Flask, request, jsonify, send_from_directory
import os
import util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(BASE_DIR, "..", "Client")

app = Flask(__name__, static_folder=CLIENT_DIR)

# Load model when server starts
util.load_saved_artifacts()


# Serve Frontend
@app.route("/")
def home():
    return send_from_directory(CLIENT_DIR, "index.html")


# Serve CSS, JS and other static files
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(CLIENT_DIR, path)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(host="0.0.0.0", port=5000)