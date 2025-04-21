import os

class Config:
    """
    Central configuration for Flask app.
    Uses environment variables for sensitive or environment-specific values.
    """

    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # 🔐 Used for session management & CSRF protection
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///diabetes.db')  # 🛢 Default to local SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 🚫 Disable event system (performance boost)
    DEBUG = True  
