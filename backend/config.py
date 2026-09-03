class Config:
    # Replace with your actual MySQL username and password
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/agrisense_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False