import requests
import streamlit as st

API_URL = "https://sepsis-warning-system-1.onrender.com/predict"

st.title("Sepsis Early Warning System")

heart_rate = st.number_input("Heart Rate", min_value=30, max_value=200, value=90)
resp_rate = st.number_input("Respiratory Rate", min_value=5, max_value=50, value=20)
temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=42.0, value=37.0)
wbc = st.number_input("WBC Count", min_value=3000, max_value=30000, value=8000)
lactate = st.number_input("Lactate Level", min_value=0.5, max_value=10.0, value=1.2)

if st.button("Predict"):
    input_data = {"HeartRate": heart_rate, "RespRate": resp_rate, "Temp": temp, "WBC": wbc, "Lactate": lactate}
    
    try:
        response = requests.post(API_URL, json=input_data, timeout=10)
        response_data = response.json()
        
        if "sepsis_risk" in response_data:
            st.success(f"Sepsis Risk: {response_data['sepsis_risk']}")
        else:
            st.error("Invalid response from server. Check backend logs.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
