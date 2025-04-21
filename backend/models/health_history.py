##Imports #
from datetime import datetime
from models import db


#HealthHistory Model
class HealthHistory(db.Model):


    __tablename__ = 'health_history'

    #Unique identifier 
    id = db.Column(db.Integer, primary_key=True)
    
    #Foreign key to the associated patient
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    
    #Name of the health metric (e.g., "steps", "bmi", "hydration").
    metric_name = db.Column(db.String(100), nullable=False)

    #Recorded value for the given metric.
    value = db.Column(db.Float, nullable=False)

    #Timestamp of when the data was logged.
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<HealthHistory(patient_id={self.patient_id}, metric_name={self.metric_name}, value={self.value}, recorded_at={self.recorded_at})>'
