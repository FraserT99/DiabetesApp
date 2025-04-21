#Imports 
from models import db


#PatientReward Model 
class PatientReward(db.Model):

    __tablename__ = "patient_rewards"

    #Columns 

    id = db.Column(db.Integer, primary_key=True)
    #Unique ID for the claimed reward entry.

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    #Foreign key linking to the claiming patient.

    reward_id = db.Column(db.String(50), nullable=False)
    #Identifier for the reward (e.g., used by claim-button component).

    reward_name = db.Column(db.String(100), nullable=False)
    #Human-readable name of the reward (e.g., "Golden Stepper Badge").

    claimed_at = db.Column(db.DateTime, server_default=db.func.now())
    #Timestamp when the reward was claimed.

    __table_args__ = (
        db.UniqueConstraint("patient_id", "reward_id", name="uq_patient_reward_once"),
    )
    #Each patient can only claim each reward once.

    def __repr__(self):
        return f"<PatientReward(patient_id={self.patient_id}, reward_id='{self.reward_id}', reward_name='{self.reward_name}')>"
