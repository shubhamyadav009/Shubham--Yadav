# All_in_One_Forcaster_App.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model and scaler
model = joblib.load('Sustainable Energy and Efficiency/All_in_One_Forcaster_Model.pkl')
scaler = joblib.load('Sustainable Energy and Efficiency/scaler.pkl')

# Target column names (used in prediction)
target_columns = [
    "wastage_mw_if_pjme_is_load",
    "generation_required_mw_if_pjme_is_load",
    "gen_after_renewables_mw",
    "net_load_after_renewables_mw",
    "co2e_tons_after_renewables",
    "co2e_tons_avoided_by_renewables"
]

# Streamlit UI
st.title('🔋 All-in-One Renewable Energy Forecasting App')
st.markdown("Enter energy and environmental parameters below to get forecast predictions.")

# Input fields
solar_mw = st.number_input("☀️ Solar Power (MW)", value=0.0)
wind_mw = st.number_input("🌬️ Wind Power (MW)", value=0.0)
temp_c = st.number_input("🌡️ Temperature (°C)", value=25.0)
humidity_pct = st.number_input("💧 Humidity (%)", value=50.0)
ghi_wm2 = st.number_input("🔆 Global Horizontal Irradiance (W/m²)", value=400.0)
wind_ms = st.number_input("🌪️ Wind Speed (m/s)", value=5.0)
pjme_mw = st.number_input("⚡ Total PJME Load (MW)", value=1000.0)
co2e_tons_gross_gen = st.number_input("💨 Gross CO2e Emissions (tons)", value=500.0)

# Predict button
if st.button("Predict Outputs"):
    # Create input dataframe
    input_data = pd.DataFrame([{
        "solar_mw": solar_mw,
        "wind_mw": wind_mw,
        "temp_c": temp_c,
        "humidity_pct": humidity_pct,
        "ghi_wm2": ghi_wm2,
        "wind_ms": wind_ms,
        "PJME_MW": pjme_mw,
        "co2e_tons_gross_gen": co2e_tons_gross_gen
    }])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)[0]

    # Show output
    st.subheader("🔍 Predicted Outputs")
    for name, value in zip(target_columns, prediction):
        st.write(f"**{name}**: `{value:.2f}`")
    st.success("Prediction completed!")



    #  C:\Users\yadav\AppData\Local\Microsoft\WindowsApps\python3.13.exe -m streamlit run "C:\Users\yadav\OneDrive\Desktop\Hey09\Sustainable Energy and Efficiency\All_in_One_Forcaster_App.py"