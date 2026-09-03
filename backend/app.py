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
        

    from routes.farm_routes import farm_bp
    from routes.ml_routes import ml_bp
    
    app.register_blueprint(farm_bp, url_prefix='/api/farm')
    app.register_blueprint(ml_bp, url_prefix='/api/ml')


    @app.route('/', methods=['GET'])
    def home():
        return {"message": "AgriSense AI API is running!"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)