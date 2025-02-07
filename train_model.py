import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("synthetic_sepsis_data.csv")  # Make sure this file is in the same directory

# Drop unnecessary columns if any (e.g., PatientID, Timestamp)
df = df.drop(columns=['PatientID', 'Timestamp'], errors='ignore')

# Fill missing values with column mean
df = df.fillna(df.mean())

# Define features (X) and target (y)
X = df.drop(columns=['SepsisLabel'])  # Feature columns
y = df['SepsisLabel']  # Target column

# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (important for ML models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model (Random Forest Classifier)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model accuracy
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model and scaler for future use
joblib.dump(model, "sepsis_model.pkl", compress=3)
joblib.dump(scaler, "scaler.pkl", compress=3)

print("✅ Model and scaler saved successfully!")
