# 🦟 Malaria Prediction Dashboard (Benin)

## 🌍 Live App

👉 https://malaria-prediction-benin-fadil-ade.streamlit.app/

## 📌 Project Overview

This project predicts malaria cases in Benin using machine learning and climate data such as rainfall and temperature.

It demonstrates how **Artificial Intelligence can be applied to public health** to better understand and anticipate disease trends.

---

## 📸 Application Preview

### 🔹 Dashboard

![Dashboard](screenshot1.png)

### 🔹 Prediction Result

![Prediction](screenshot2.png)

### 🔹 Data Visualization

![Graphs](screenshot3.png)

---

## 🚀 Features

* 📊 Predict malaria cases for any future year
* 📈 Forecast next 5 years automatically
* 🌧️ Input rainfall & temperature
* 📉 Interactive graphs and analysis
* 🧠 Feature importance explanation

---

## 🧠 Machine Learning Model

This project uses:

* **Random Forest Regressor** (main model)
* **Linear Regression** (baseline model)

### Features used:

* Rainfall
* Temperature
* Previous year malaria cases
* Year

---

## 📊 How It Works

1. Load datasets (malaria + climate)
2. Filter data for Benin
3. Merge datasets by year
4. Train machine learning model
5. Predict malaria cases
6. Display results in a Streamlit dashboard

---

## 🛠️ Technologies Used

* Python
* Pandas
* Scikit-learn
* Matplotlib
* Streamlit

---

## 📂 Dataset Sources

* Our World in Data (Malaria data)
* Climate dataset (Rainfall & Temperature)

---

## 💻 Run Locally

```bash
git clone https://github.com/available-pixel/malaria_prediction_benin.git
cd malaria_prediction_benin

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 Project Objective

* Apply AI to real-world health problems
* Build a strong portfolio project for scholarships
* Understand epidemic prediction using data

---

## ⚠️ Disclaimer

This project is for educational purposes only and does not provide medical advice.

---

## 👤 Author

**Fadil ADELABOU**
Aspiring Data Scientist | AI & Public Health Enthusiast
