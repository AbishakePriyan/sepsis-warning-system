from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

try:
    model = joblib.load("sepsis_model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    print(f"Error loading model: {e}")
    model, scaler = None, None

@app.route("/")
def home():
    return "Sepsis Prediction API is running."

@app.route("/predict", methods=["POST"])
def predict():
    if not model or not scaler:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        features = np.array([[data["HeartRate"], data["RespRate"], data["Temp"], data["WBC"], data["Lactate"]]])
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]

        return jsonify({"sepsis_risk": int(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
