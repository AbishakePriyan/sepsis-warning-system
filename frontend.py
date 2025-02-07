import streamlit as st
import requests

st.title("Sepsis Early Warning System")

# User input fields
heart_rate = st.number_input("Heart Rate", min_value=40, max_value=180, value=80)
resp_rate = st.number_input("Respiratory Rate", min_value=10, max_value=40, value=20)
temp = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0)
wbc = st.number_input("White Blood Cell Count (WBC)", min_value=3000, max_value=20000, value=7000)
lactate = st.number_input("Lactate Level", min_value=0.5, max_value=5.0, value=1.2)

# Predict button
if st.button("Check Sepsis Risk"):
    data = {"HeartRate": heart_rate, "RespRate": resp_rate, "Temp": temp, "WBC": wbc, "Lactate": lactate}
    response = requests.post("https://sepsis-warning-system-1.onrender.com", json=data)
    prediction = response.json()["sepsis_risk"]

    if prediction == 1:
        st.error("⚠️ High Risk of Sepsis! Seek Medical Attention.")
    else:
        st.success("✅ No Immediate Risk of Sepsis.")
