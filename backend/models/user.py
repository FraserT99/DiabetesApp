from werkzeug.security import generate_password_hash
from flask_login import UserMixin  # Import UserMixin from flask_login
from models import db  # Import db from models package

class User(UserMixin, db.Model):  # Inherit from UserMixin
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=True)

    # Relationship to link user to patient
    patient = db.relationship('Patient', back_populates='user', lazy=True)

    def __init__(self, username, password, patient_id=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.patient_id = patient_id

    # Flask-Login required methods
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
