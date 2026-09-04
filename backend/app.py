from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from db_schema import db, User, FarmData
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/agrisense_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

try:
    crop_model = joblib.load("custom_random_forest.pkl")
    yield_model = joblib.load("custom_yield_model.pkl")
except Exception as e:
    print(f"Warning: Models not found or failed to load. {e}")
    crop_model, yield_model = None, None

with app.app_context():
    db.create_all()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user_id": new_user.id})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/predict", methods=["POST"])
def predict():
    if not crop_model or not yield_model:
        return jsonify({"error": "ML models offline"}), 500
    
    data = request.get_json()
    user_id = data.get("user_id")
    
    features = [
        float(data["nitrogen"]), float(data["phosphorus"]), float(data["potassium"]),
        float(data["temperature"]), float(data["humidity"]), float(data["ph"]), float(data["rainfall"])
    ]
    
    crop_prediction = crop_model.predict(np.array([features]))[0]
    
    try:
        y_pred = yield_model.predict(np.array([features]))[0]
        yield_prediction = f"{round(y_pred, 2)} hg/ha"
    except Exception:
        yield_prediction = "Shape mismatch with Kaggle Data"
    
    if user_id:
        new_record = FarmData(
            user_id=user_id, nitrogen=features[0], phosphorus=features[1], potassium=features[2],
            temperature=features[3], humidity=features[4], ph=features[5], rainfall=features[6],
            recommended_crop=str(crop_prediction)
        )
        db.session.add(new_record)
        db.session.commit()

    return jsonify({
        "status": "success", 
        "recommended_crop": str(crop_prediction),
        "estimated_yield": yield_prediction
    })

@app.route("/api/history/<int:user_id>", methods=["GET"])
def get_history(user_id):
    records = FarmData.query.filter_by(user_id=user_id).order_by(FarmData.record_date.desc()).all()
    history = []
    for r in records:
        history.append({
            "id": r.id,
            "crop": r.recommended_crop,
            "n": r.nitrogen, "p": r.phosphorus, "k": r.potassium,
            "date": r.record_date.strftime("%Y-%m-%d %H:%M")
        })
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True, port=5000)