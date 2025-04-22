from models import db
from models.patientChallenge import PatientChallenge

class Challenge(db.Model):

    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    challenge_type = db.Column(db.String(10), nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    reward_points = db.Column(db.Integer, nullable=False)

    #Relationship to track which users are participating in this challenge.
    participants = db.relationship("PatientChallenge", back_populates="challenge")

