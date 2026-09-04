# AgriSense AI: Intelligent Agricultural Advisory Platform

AgriSense AI is a comprehensive web-based platform designed for managing agricultural information, monitoring farming parameters, and providing analytical and advisory support. Developed as a B.Tech minor project.

## Features
* **Farm & Profile Management:** Secure user authentication and management of farm profiles.
* **Agricultural Data Management:** Tracking and storing soil and environmental parameters (N-P-K, pH, temperature, humidity, rainfall).
* **Analytics Dashboard:** Statistical tracking and visual representation of historical agricultural data using Pandas, NumPy, and charting libraries.
* **Crop Recommendation:** Scikit-Learn classification model to recommend optimal crops.
* **Yield Prediction:** Scikit-Learn regression model to estimate expected harvest yield.
* **Crop Advisory & Insights:** Curated, rule-based agronomic guidance and cultivation insights.

## Technology Stack
* **Frontend:** React.js, Vite, HTML5, CSS3, JavaScript, Recharts
* **Backend:** Python Flask REST API, Flask-SQLAlchemy
* **Database:** MySQL, SQLAlchemy ORM
* **Data Processing & ML:** Pandas, NumPy, Scikit-Learn, Joblib

## Project Structure
```text
Agrisense-AI/
├── frontend/                    
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   └── package.json
├── backend/                    
│   ├── app.py
│   ├── config.py
│   ├── db_schema.py
│   ├── fetch_data.py
│   ├── train_and_benchmark.py
│   ├── train_yield_model.py
│   ├── requirements.txt
│   ├── routes/                  
│   │   ├── farm_routes.py
│   │   └── ml_routes.py
│   ├── models/
│   │   └── db_models.py
│   └── ml_core/
│       ├── custom_regressor.py
│       ├── decision_tree.py
│       ├── random_forest_classifier.py
│       └── random_forest_regressor.py
└── data/ 
    └── crop_data.csv
```



## Getting Started Prerequisites

    Python 3.x

    Node.js and npm

    MySQL Server installed and running

### 1. Database Setup

Create a MySQL database named agrisense_db:

```
CREATE DATABASE agrisense_db;
```

### 2. Backend Installation & Execution

Navigate to the backend directory, install the required dependencies, and run the server:

```
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Frontend Installation & Execution
Open a separate terminal window, navigate to the frontend directory, install the required packages, and start the development server:


```
cd frontend
npm install
npm run dev
```

Minor Project, Team: MNP036,
Authors: 
ABHINAV PANDIT,
MANASVI KUMAR,
SANJEEV KUMAR JHA
