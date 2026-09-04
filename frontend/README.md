# 🌱 AgriSense AI: Intelligent Agricultural Advisory Platform

AgriSense AI is a full-stack, web-based platform designed to support informed and sustainable agricultural practices. It integrates agricultural data management, monitoring, and machine learning to provide data-driven decision-making tools for farmers and agricultural stakeholders.

**Developed as a B.Tech Minor Project by Team MNP036.**

## 🚀 Features
* **Farm & Profile Management:** Secure user authentication and management of farm profiles (location, soil type).
* **Agricultural Data Tracking:** Log and monitor essential parameters (Nitrogen, Phosphorus, Potassium, pH, Temperature, Humidity, Rainfall).
* **Crop Recommendation:** Scikit-Learn Random Forest classification model to suggest optimal crops based on soil/weather data.
* **Yield Prediction:** Custom-built Random Forest regression model (benchmarked against Scikit-Learn) to estimate harvest yield (hg/ha).
* **Crop Advisory:** Curated, rule-based agronomic insights and best practices generated upon crop prediction.
* **Analytics Dashboard:** Chronological visualization of historical N-P-K soil records using interactive charts.

## 🛠️ Technology Stack
* **Frontend:** React.js, Vite, Recharts, standard CSS
* **Backend:** Python, Flask REST API, Flask-SQLAlchemy, Flask-CORS
* **Database:** MySQL (Local hosting via DBngin)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib

## ⚙️ Local Setup Instructions

### Prerequisites
1. Python 3.9+
2. Node.js & npm
3. MySQL Server (DBngin recommended for MacOS)

### 1. Database Configuration
* Start your MySQL server on port `3306`.
* Open your database client and execute: 
  ```sql
  CREATE DATABASE agrisense_db;

2. Backend Setup

Navigate to the backend directory, install dependencies, and start the Flask API:

cd backend
pip install -r requirements.txt
python app.py