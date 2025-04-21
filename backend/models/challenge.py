#Imports 
from models import db
from models.patientChallenge import PatientChallenge


#Challenge Model 
class Challenge(db.Model):

    __tablename__ = "challenges"

    #Columns 

    id = db.Column(db.Integer, primary_key=True)
    #Unique identifier for each challenge.

    name = db.Column(db.String(100), nullable=False)
    #Name of the challenge (e.g., "Step Up", "Hydration Boost").

    description = db.Column(db.String(255), nullable=False)
    #Description of the challenge shown to users.

    challenge_type = db.Column(db.String(10), nullable=False)
    #Type of challenge: 'daily', 'weekly', or 'monthly'.

    goal = db.Column(db.Integer, nullable=False)
    #Goal value the user needs to reach (e.g., 10000 steps).

    reward_points = db.Column(db.Integer, nullable=False)
    #Number of points the user earns for completing the challenge.

    #Relationships 

    participants = db.relationship("PatientChallenge", back_populates="challenge")
    #Relationship to track which users are participating in this challenge.
