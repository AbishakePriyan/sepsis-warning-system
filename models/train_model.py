import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load your dataset (use your own file or synthetic data)
df = pd.read_csv("synthetic_sepsis_data.csv")  # Replace with your dataset file

# Example: drop unnecessary columns and fill missing values
df = df.fillna(df.mean())

# Define features and target
X = df[['HeartRate', 'RespRate', 'Temp', 'WBC', 'Lactate']]
y = df['SepsisLabel']  # Ensure your dataset has this column

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model (using RandomForest as an example)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the model and scaler
joblib.dump(model, "sepsis_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Trained model and scaler saved successfully!")
