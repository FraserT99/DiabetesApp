from datetime import datetime
from models import db

class HealthHistory(db.Model):

    __tablename__ = 'health_history'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<HealthHistory(patient_id={self.patient_id}, metric_name={self.metric_name}, value={self.value}, recorded_at={self.recorded_at})>'
