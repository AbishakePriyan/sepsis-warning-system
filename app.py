from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
import os

app = Flask(__name__)

# ✅ Configure SQLAlchemy Database (SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sepsis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ✅ Define Feedback Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)

# ✅ Load Trained Model & Scaler
MODEL_PATH = "models/sepsis_model.pkl"
SCALER_PATH = "models/scaler.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
else:
    model, scaler = None, None
    print("⚠️ Warning: Model or scaler not found! Ensure they are trained.")

# 📌 1️⃣ Home Page
@app.route("/")
def home():
    return render_template("index.html")

# 📌 2️⃣ Prediction Page
@app.route("/predict")
def predict_page():
    return render_template("predict.html")

# 📌 3️⃣ Feedback Page
@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html")

# 📌 4️⃣ API Endpoint for Prediction
@app.route("/api/predict", methods=["POST"])
def predict():
    if not model or not scaler:
        return jsonify({"error": "Model not available. Train the model first!"}), 500

    try:
        data = request.json
        input_data = np.array([[data["heartRate"], data["respRate"], data["temperature"], data["wbc"], data["lactate"]]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]

        return jsonify({"sepsis_risk": int(prediction)})
    
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400

# 📌 5️⃣ API Endpoint for Feedback (Using Database)
@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    try:
        data = request.json
        new_feedback = Feedback(name=data.get("name", "Anonymous"), feedback_text=data["feedbackText"])
        db.session.add(new_feedback)
        db.session.commit()

        return jsonify({"message": "Feedback submitted successfully!"})

    except Exception as e:
        return jsonify({"error": f"Feedback submission failed: {str(e)}"}), 400

# ✅ Initialize Database Properly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensures database tables are created before running
    app.run(debug=True)
