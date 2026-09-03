from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FarmRecord(db.Model):
    __tablename__ = 'farm_records'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_name = db.Column(db.String(100), nullable=False)
    area_acres = db.Column(db.Float, nullable=False)
    crop_grown = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farm_name": self.farm_name,
            "area_acres": self.area_acres,
            "crop_grown": self.crop_grown,
            "created_at": self.created_at.strftime("%Y-%m-%d")
        }