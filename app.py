from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load("sepsis_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return "Sepsis Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([data.values()]).reshape(1, -1)
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)[0]
    return jsonify({'sepsis_risk': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
