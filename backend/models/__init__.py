from flask_sqlalchemy import SQLAlchemy

#Initialise the database instance
db = SQLAlchemy()

#Import models after db initialisation
from .user import User
from .patientChallenge import PatientChallenge
from .challenge import Challenge
from .patient import Patient
from .health_history import HealthHistory  
