#Imports 
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models import db


#User Model 
class User(UserMixin, db.Model):
 
    __tablename__ = 'users'

    #Columns 

    id = db.Column(db.Integer, primary_key=True)
    #Unique identifier for the user.

    username = db.Column(db.String(80), unique=True, nullable=False)
    #Login username (must be unique).

    password_hash = db.Column(db.String(200), nullable=False)
    #Hashed version of the user’s password.

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=True)
    #Foreign key to the associated patient profile (if applicable).

    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    #Timestamp of the user's last login.

    #Relationships 

    patient = db.relationship('Patient', back_populates='user', lazy=True)
    #One-to-one link to patient profile (if user is a patient).

    def __init__(self, username, password, patient_id=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.patient_id = patient_id

    #Flask-Login Properties 

    @property
    def is_active(self):
        """True if the user account is active."""
        return True

    @property
    def is_authenticated(self):
        """True if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """False, as anonymous users are not represented by this model."""
        return False

    def get_id(self):
        """Return the user's unique ID as a string."""
        return str(self.id)
