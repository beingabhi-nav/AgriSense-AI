from flask import Flask
from flask_cors import CORS
from models.db_models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Allow React frontend to make requests
    CORS(app) 
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Creates tables if they don't exist yet
        db.create_all()

    @app.route('/', methods=['GET'])
    def home():
        return {"message": "AgriSense AI API is running!"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)