from flask import Blueprint, request, jsonify
from models.db_models import db, FarmRecord

farm_bp = Blueprint('farm', __name__)

@farm_bp.route('/add', methods=['POST'])
def add_farm():
    data = request.json
    new_farm = FarmRecord(
        farm_name=data['farm_name'],
        area_acres=data['area_acres'],
        crop_grown=data['crop_grown']
    )
    db.session.add(new_farm)
    db.session.commit()
    return jsonify({"message": "Farm record added successfully"}), 201