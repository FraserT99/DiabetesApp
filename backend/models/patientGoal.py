#Imports 
from models import db
from sqlalchemy import UniqueConstraint


#PatientGoal Model 
class PatientGoal(db.Model):

    __tablename__ = 'patient_goals'

    #Columns 

    id = db.Column(db.Integer, primary_key=True)
    #Unique identifier for the goal record.

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    #Foreign key reference to the patient who set this goal.

    metric_name = db.Column(db.String(100), nullable=False)
    #Name of the metric this goal applies to (e.g., "steps", "calories").

    goal_value = db.Column(db.Float, nullable=False)
    #Target value the patient aims to achieve.

    goal_type = db.Column(db.String(20), default="daily")
    #Type of goal: "daily", "weekly", "monthly", or "long_term".

    start_date = db.Column(db.Date)
    #Optional start date for the goal (if tracking over time).

    __table_args__ = (
        UniqueConstraint('patient_id', 'metric_name', 'goal_type', name='uq_patient_metric_goal_type'),
    )
    #Ensure each patient can only have one goal per metric and goal type.

    def __repr__(self):
        return f"<PatientGoal(patient_id={self.patient_id}, metric='{self.metric_name}', goal={self.goal_value})>"
