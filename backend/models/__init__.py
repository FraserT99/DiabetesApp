from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Import models after db initialization
from .user import User
from .patient import Patient
from .health_history import HealthHistory  # Import HealthHistory model