import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variable if available
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///diabetes.db')  # SQLite by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Set this flag to False for production
