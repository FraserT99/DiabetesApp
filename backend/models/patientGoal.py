from models import db
from sqlalchemy import UniqueConstraint

class PatientGoal(db.Model):

    __tablename__ = 'patient_goals'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    goal_value = db.Column(db.Float, nullable=False)
    goal_type = db.Column(db.String(20), default="daily")
    start_date = db.Column(db.Date)

    __table_args__ = (
        UniqueConstraint('patient_id', 'metric_name', 'goal_type', name='uq_patient_metric_goal_type'),
    )

    def __repr__(self):
        return f"<PatientGoal(patient_id={self.patient_id}, metric='{self.metric_name}', goal={self.goal_value})>"
