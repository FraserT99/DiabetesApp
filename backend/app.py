from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from models import db
from controllers.auth import auth_bp
from services.data_loader import load_data_from_csv

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Enable CORS
CORS(app, origins=["http://localhost:3000"])

# Register blueprints
app.register_blueprint(auth_bp)

# Define User loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User  # Avoid circular import
    return User.query.get(int(user_id))

# Use the before_first_request in app context
def initialize_app():
    """Perform initial setup for the app."""
    print("[INFO] Initializing database and loading data from CSV...")
    db.create_all()  # Ensure the database is initialized
    load_data_from_csv()  # Load data from CSV on startup

with app.app_context():
    initialize_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Start the app
