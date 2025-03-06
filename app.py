# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
import os

app = Flask(__name__)

# Configure SQLite database for feedback storage
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sepsis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define a model to store user feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)

# Load the trained model and scaler from the models folder
MODEL_PATH = "models/sepsis_model.pkl"
SCALER_PATH = "models/scaler.pkl"
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model and scaler loaded successfully.")
else:
    model, scaler = None, None
    print("⚠️ Warning: Model or scaler not found. Please run train_model.py first.")

# Route for Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route for Prediction Page
@app.route("/predict")
def predict_page():
    return render_template("predict.html")

# Route for Feedback Page
@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html")

# API Endpoint for Sepsis Prediction
@app.route("/api/predict", methods=["POST"])
def api_predict():
    if not model or not scaler:
        return jsonify({"error": "Model not available. Train the model first."}), 500

    try:
        data = request.json
        # Ensure the order matches your training FEATURES list
        input_data = np.array([[data["PRG"], data["PL"], data["PR"], data["SK"], data["TS"], data["M11"], data["BD2"], data["Age"], data["Insurance"]]])
        print("Raw Input Data:", input_data)

        input_scaled = scaler.transform(input_data)
        print("Scaled Input Data:", input_scaled)

        probabilities = model.predict_proba(input_scaled)[0]
        print("Prediction Probabilities:", probabilities)

        # Experiment with threshold - adjust from 0.5 to a lower value if needed
        threshold = 0.4
        prediction = 1 if probabilities[1] > threshold else 0
        print("Final Prediction (with threshold = {}):".format(threshold), prediction)

        return jsonify({"sepsis_risk": int(prediction), "probabilities": probabilities.tolist()})
    except Exception as e:
        print("Prediction Error:", str(e))
        return jsonify({"error": "Prediction failed: " + str(e)}), 400


# API Endpoint for Feedback Submission
@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    try:
        data = request.json
        new_feedback = Feedback(name=data.get("name", "Anonymous"), feedback_text=data["feedbackText"])
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({"message": "Feedback submitted successfully!"})
    except Exception as e:
        return jsonify({"error": "Feedback submission failed: " + str(e)}), 400

# Initialize the database and run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they do not exist
    app.run(debug=True)
