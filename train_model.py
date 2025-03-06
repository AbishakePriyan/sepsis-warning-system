# train_model.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os

# Load dataset
df = pd.read_csv("datasets/Paitients_Files_Train.csv")

# Drop the ID column if it exists
if 'ID' in df.columns:
    df.drop('ID', axis=1, inplace=True)

# Convert target labels to numeric (assuming "Positive" for high risk, "Negative" for low risk)
df["Sepsis"] = df["Sepsis"].map({"Positive": 1, "Negative": 0})
print("Target distribution:")
print(df["Sepsis"].value_counts())

# Define features and target
FEATURES = ["PRG", "PL", "PR", "SK", "TS", "M11", "BD2", "Age", "Insurance"]
TARGET = "Sepsis"
X = df[FEATURES]
y = df[TARGET]

# Convert categorical Insurance if needed
if X["Insurance"].dtype == "object":
    X["Insurance"] = X["Insurance"].astype("category").cat.codes

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model with balanced class weights
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("✅ Model Accuracy: {:.2f}".format(accuracy))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model and scaler into the models directory
if not os.path.exists("models"):
    os.makedirs("models")
joblib.dump(model, "models/sepsis_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("✅ Model and Scaler Saved!")
