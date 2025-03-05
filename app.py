import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import joblib
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sepsis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model for storing prediction records
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Float, nullable=False)
    resp_rate = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    wbc = db.Column(db.Float, nullable=False)
    lactate = db.Column(db.Float, nullable=False)
    sepsis_risk = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Prediction {self.id} - Risk: {self.sepsis_risk}>"

# Attempt to load the trained model and scaler from disk
try:
    model = joblib.load("sepsis_model.pkl")
    scaler = joblib.load("scaler.pkl")
    print("Model and scaler loaded successfully.")
except Exception as e:
    print("Error loading model or scaler:", e)
    model = None
    scaler = None

# Home route to serve the front-end
@app.route("/")
def index():
    return render_template("index.html")

# Prediction endpoint that receives JSON data, makes a prediction, and saves the record
@app.route("/predict", methods=["POST"])
def predict():
    if not model or not scaler:
        return jsonify({"error": "Model or scaler not loaded."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided."}), 400

    try:
        # Extract features from the input data
        heart_rate = float(data.get("HeartRate"))
        resp_rate = float(data.get("RespRate"))
        temperature = float(data.get("Temp"))
        wbc = float(data.get("WBC"))
        lactate = float(data.get("Lactate"))
        features = np.array([[heart_rate, resp_rate, temperature, wbc, lactate]])

        # Preprocess the features using the saved scaler
        scaled_features = scaler.transform(features)

        # Predict sepsis risk using the saved model
        prediction = model.predict(scaled_features)[0]

        # Save the prediction to the database
        new_prediction = Prediction(
            heart_rate=heart_rate,
            resp_rate=resp_rate,
            temperature=temperature,
            wbc=wbc,
            lactate=lactate,
            sepsis_risk=int(prediction)
        )
        db.session.add(new_prediction)
        db.session.commit()

        # Return the prediction as JSON
        return jsonify({"sepsis_risk": int(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Get port from environment (for deployment) or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
