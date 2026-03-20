import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np

# =====================================================
# 1. APP TITLE & CONFIG + BACKGROUND
# =====================================================
st.set_page_config(page_title="Malaria Prediction - Benin", layout="wide")

# Set background color using Markdown + CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E6F2FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

from PIL import Image
import base64
from io import BytesIO

# Load image
img = Image.open("benin_map.png")

# Convert image to base64
buffered = BytesIO()
img.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Display title + image inline using HTML
st.markdown(
    f"""
    <h3>🦟 Malaria Prediction Dashboard (Benin) 
    <img src="data:image/png;base64,{img_str}" width="30" style="vertical-align: middle;">
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown("""
Predict malaria cases using historical data, rainfall, temperature, and trends.
This dashboard is interactive: select the year, input climate data, and explore predictions visually.
""")

# =====================================================
# 2. LOAD DATA
# =====================================================
malaria = pd.read_csv("malaria.csv")
climate = pd.read_csv("climate.csv")

# Filter Benin
malaria_benin = malaria[malaria['Entity'] == 'Benin']
malaria_benin = malaria_benin[['Year', 'Incidence of malaria (per 1,000 population at risk)']]
malaria_benin = malaria_benin.rename(
    columns={'Incidence of malaria (per 1,000 population at risk)': 'Cases'}
)

climate_benin = climate[climate['Country'] == 'Benin']

# Merge
data = pd.merge(malaria_benin, climate_benin, on='Year')

# Add previous year feature
data['Cases_last_year'] = data['Cases'].shift(1)
data = data.dropna()

# =====================================================
# 3. TRAIN MODELS
# =====================================================
X = data[['Rainfall', 'Temperature', 'Cases_last_year', 'Year']]
y = data['Cases']

# Random Forest for single-year prediction
rf_model = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)
rf_model.fit(X, y)

# Linear Regression for multi-year prediction
lr_model = LinearRegression()
lr_model.fit(X, y)

# =====================================================
# 4. SIDEBAR USER INPUT
# =====================================================
st.sidebar.header("Input Climate & Year for Prediction")

rainfall = st.sidebar.number_input("Rainfall (mm)", min_value=500, max_value=2000, value=1350)
temperature = st.sidebar.number_input("Temperature (°C)", min_value=20.0, max_value=35.0, value=28.3)
future_year = st.sidebar.number_input(
    "Year to Predict", 
    min_value=int(data['Year'].max()+1), 
    max_value=2030, 
    value=int(data['Year'].max()+1)
)

last_cases = data.iloc[-1]['Cases']

# =====================================================
# 5. SINGLE YEAR PREDICTION (Random Forest)
# =====================================================
if st.sidebar.button("Predict Malaria Cases"):
    future = pd.DataFrame({
        'Rainfall': [rainfall],
        'Temperature': [temperature],
        'Cases_last_year': [last_cases],
        'Year': [future_year]
    })

    prediction = rf_model.predict(future)
    st.success(f"Predicted malaria cases for {future_year}: {prediction[0]:.2f}")

# =====================================================
# 6. MULTI-YEAR PREDICTION TABLE (Dynamic)
# =====================================================
st.subheader("Predicted Malaria Cases (Next 5 Years)")

years = range(int(data['Year'].max())+1, int(data['Year'].max())+6)
predicted_cases = []
prev_cases = last_cases

for i, yr in enumerate(years):
    # Small dynamic variation for realism
    rainfall_year = rainfall + i * 10      # +10mm per year
    temperature_year = temperature + i * 0.2  # +0.2°C per year

    row = pd.DataFrame({
        'Rainfall': [rainfall_year],
        'Temperature': [temperature_year],
        'Cases_last_year': [prev_cases],
        'Year': [yr]
    })
    pred = lr_model.predict(row)[0]
    predicted_cases.append(pred)
    prev_cases = pred  # next year uses this prediction

future_multi = pd.DataFrame({
    'Year': list(years),
    'Predicted_Cases': predicted_cases,
    'Rainfall': [rainfall + i*10 for i in range(5)],
    'Temperature': [temperature + i*0.2 for i in range(5)]
})
st.dataframe(future_multi)

# =====================================================
# 7. VISUALIZATION
# =====================================================
st.subheader("Visualizations")
col1, col2 = st.columns(2)

# Left: Historical + Predicted
with col1:
    fig, ax = plt.subplots()
    ax.plot(data['Year'], data['Cases'], marker='o', color='red', label='Historical')
    ax.plot(future_multi['Year'], future_multi['Predicted_Cases'], marker='x', color='green', linestyle='--', label='Predicted 5 years')
    ax.set_title("Malaria Cases Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cases per 1,000 population")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# Right: Real vs Predicted (training data)
with col2:
    y_pred_all = rf_model.predict(X)
    fig2, ax2 = plt.subplots()
    ax2.scatter(y, y_pred_all, color='blue')
    ax2.plot([y.min(), y.max()], [y.min(), y.max()], linestyle='--', color='black')
    ax2.set_title("Real vs Predicted Cases (Training Data)")
    ax2.set_xlabel("Real")
    ax2.set_ylabel("Predicted")
    ax2.grid(True)
    st.pyplot(fig2)

# =====================================================
# 8. FEATURE IMPORTANCE
# =====================================================
st.subheader("Feature Importance (Random Forest)")
importance = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
st.bar_chart(importance)