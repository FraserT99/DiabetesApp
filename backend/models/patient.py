#Imports
from models import db
from models.health_history import HealthHistory  


#Patient Model
class Patient(db.Model):
 
    __tablename__ = 'patients'

    #Unique patient identifier.
    patient_id = db.Column(db.Integer, primary_key=True)

    #Full name of the patient.
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)  #0 = Male, 1 = Female
    ethnicity = db.Column(db.Integer)  #0 = Caucasian, 1 = African American, etc.
    diagnosis = db.Column(db.Integer)  #0 = No Diabetes, 1 = Diabetes

    #Lifestyle & Health Behavior
    smoking = db.Column(db.Boolean)
    alcohol_consumption = db.Column(db.Float)
    physical_activity = db.Column(db.Float)
    diet_quality = db.Column(db.Float)
    sleep_quality = db.Column(db.Float)

    #Medical History
    family_history_diabetes = db.Column(db.Boolean)
    gestational_diabetes = db.Column(db.Boolean)
    polycystic_ovary_syndrome = db.Column(db.Boolean)
    previous_pre_diabetes = db.Column(db.Boolean)
    hypertension = db.Column(db.Boolean)

    #Medications
    antihypertensive_medications = db.Column(db.Boolean)
    statins = db.Column(db.Boolean)
    antidiabetic_medications = db.Column(db.Boolean)

    #Medical Checkups & Adherence
    medical_checkups_frequency = db.Column(db.Integer)  #Visits/year
    medication_adherence = db.Column(db.Float)  #Scale of 0–10
    health_literacy = db.Column(db.Float)  #Scale of 0–10

    #Latest Health Metrics
    latest_blood_pressure_systolic = db.Column(db.Integer)
    latest_blood_pressure_diastolic = db.Column(db.Integer)
    latest_bmi = db.Column(db.Float)
    latest_cholesterol_total = db.Column(db.Float)
    latest_hba1c = db.Column(db.Float)
    latest_fasting_blood_sugar = db.Column(db.Float)

    #Nutrition & Activity (New Metrics) 
    latest_calories_consumed = db.Column(db.Float)
    latest_protein_intake = db.Column(db.Float)
    latest_carbs_intake = db.Column(db.Float)
    latest_fats_intake = db.Column(db.Float)
    latest_fiber_intake = db.Column(db.Float)

    latest_water_intake = db.Column(db.Float)
    latest_steps_taken = db.Column(db.Integer)
    latest_active_minutes = db.Column(db.Integer)
    latest_calories_burned = db.Column(db.Float)
    latest_distance_walked = db.Column(db.Float)
    latest_distance_ran = db.Column(db.Float)
    latest_workout_sessions = db.Column(db.Integer)
    latest_heart_rate = db.Column(db.Integer)
    latest_weight = db.Column(db.Float)
    latest_height = db.Column(db.Float)

    #Gamification / Rewards 
    reward_points = db.Column(db.Integer, default=0)

    #Privacy Settings 
    show_on_leaderboard = db.Column(db.Boolean, default=True)
    email_alerts = db.Column(db.Boolean, default=True)
    sms_alerts = db.Column(db.Boolean, default=True)
    data_export_consent = db.Column(db.Boolean, default=False)

    #Contact Information 
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    #Relationships 
    user = db.relationship('User', back_populates='patient', uselist=False)
    #One-to-one link with user account.

    health_history = db.relationship(
        'HealthHistory',
        backref='patient',
        lazy='dynamic',
        cascade="all, delete-orphan"
    )
    #All historical metric entries (used in graphs & trends).

    challenges = db.relationship("PatientChallenge", back_populates="patient")
    #Active or completed challenges.

    goals = db.relationship("PatientGoal", backref="patient", lazy="dynamic", cascade="all, delete-orphan")
    #Goals set for this patient.

    def __repr__(self):
        return f'<Patient(id={self.patient_id}, name={self.first_name} {self.last_name})>'

    #Methods 
    def update_health_metric(self, metric_name, new_value):
        """
        Update a specific health metric and log it to the history.

        Args:
            metric_name (str): Name of the metric to update (must match a field).
            new_value (float|int): New metric value.

        Returns:
            bool: True if updated and logged successfully.
        """
        previous_value = getattr(self, metric_name, "N/A")

        #Create a historical log entry
        history_entry = HealthHistory(
            patient_id=self.patient_id,
            metric_name=metric_name,
            value=new_value
        )
        db.session.add(history_entry)

        #Update the "latest_" field on the patient model
        setattr(self, metric_name, new_value)
        db.session.commit()

        return True
