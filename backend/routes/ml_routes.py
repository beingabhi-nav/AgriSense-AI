from flask import Blueprint, request, jsonify
import numpy as np
# Assuming we will load saved model weights later
# from ml_core.random_forest_classifier import CustomRandomForestClassifier
# from ml_core.random_forest_regressor import CustomRandomForestRegressor

ml_bp = Blueprint('ml', __name__)

@ml_bp.route('/recommend-crop', methods=['POST'])
def recommend_crop():
    data = request.json
    try:
        # Expected input features matching the Kaggle dataset:
        # N, P, K, temperature, humidity, pH, rainfall
        features = np.array([[
            float(data['N']), float(data['P']), float(data['K']),
            float(data['temperature']), float(data['humidity']), 
            float(data['ph']), float(data['rainfall'])
        ]])
        
        # Placeholder prediction until models are trained on the dataset
        predicted_crop = "Rice (Placeholder)" 
        
        return jsonify({"recommended_crop": predicted_crop}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ml_bp.route('/predict-yield', methods=['POST'])
def predict_yield():
    data = request.json
    try:
        # We will map these inputs to the specific Indian yield dataset later
        area = float(data.get('area', 0))
        rainfall = float(data.get('rainfall', 0))
        
        # Placeholder prediction 
        predicted_yield = 4.5 * (area / 10) 
        
        return jsonify({"estimated_yield": round(predicted_yield, 2), "unit": "tonnes"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400