from models import db
from models.health_history import HealthHistory  # Import HealthHistory

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    diagnosis = db.Column(db.Integer)  # 1 for diabetic, 0 for non-diabetic

    # ============================
    # Personal Information Section
    # ============================
    ethnicity = db.Column(db.String(100))  # Patient's ethnicity

    # ============================
    # Lifestyle and Health Behavior Section
    # ============================
    smoking = db.Column(db.Integer)  # 0 for non-smoker, 1 for smoker
    alcohol_consumption = db.Column(db.Float)  # Weekly consumption in grams or frequency
    physical_activity = db.Column(db.Float)  # Weekly activity in hours or intensity measure
    diet_quality = db.Column(db.Float)  # Diet quality score (e.g., from 1 to 10)
    sleep_quality = db.Column(db.Float)  # Sleep quality score (e.g., from 1 to 10)

    # ============================
    # Medical History Section
    # ============================
    family_history_diabetes = db.Column(db.Boolean)  # 1 if family history, 0 if not
    gestational_diabetes = db.Column(db.Boolean)  # 1 if yes, 0 if no
    polycystic_ovary_syndrome = db.Column(db.Boolean)  # 1 if yes, 0 if no
    previous_pre_diabetes = db.Column(db.Boolean)  # 1 if yes, 0 if no
    hypertension = db.Column(db.Boolean)  # 1 if yes, 0 if no

    # ============================
    # Medications Section
    # ============================
    antihypertensive_medications = db.Column(db.Boolean)  # 1 if on antihypertensive, 0 if not
    statins = db.Column(db.Boolean)  # 1 if on statins, 0 if not
    antidiabetic_medications = db.Column(db.Boolean)  # 1 if on antidiabetic, 0 if not

    # ============================
    # Medical Checkups and Adherence Section
    # ============================
    medical_checkups_frequency = db.Column(db.String(50))  # e.g., 'annually', 'semi-annually'
    medication_adherence = db.Column(db.Float)  # Medication adherence percentage (0 to 100)
    health_literacy = db.Column(db.Float)  # Health literacy score (e.g., from 1 to 10)

    # ============================
    # Latest Health Metrics Section
    # ============================
    latest_blood_pressure_systolic = db.Column(db.Integer)
    latest_blood_pressure_diastolic = db.Column(db.Integer)
    latest_bmi = db.Column(db.Float)
    latest_cholesterol_total = db.Column(db.Float)
    latest_hba1c = db.Column(db.Float)
    latest_fasting_blood_sugar = db.Column(db.Float)  # Latest fasting blood sugar value

    # ============================
    # Relationship with Other Models Section
    # ============================
    # Define relationship with User model
    user = db.relationship('User', back_populates='patient', uselist=False)

    # Define relationship to HealthHistory model (tracks all historical values)
    health_history = db.relationship('HealthHistory', backref='patient', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Patient(id={self.patient_id}, name={self.first_name} {self.last_name})>'

    # ============================
    # Method to Update Health Metrics Section
    # ============================
    def update_health_metric(self, metric_name, new_value):
        """Method to update any health metric and log it into health history."""
        # First, record the previous value to history
        history_entry = HealthHistory(
            patient_id=self.patient_id,
            metric_name=metric_name,
            value=new_value
        )
        db.session.add(history_entry)

        # Then, update the latest value in the patient table
        if metric_name == "blood_pressure":
            self.latest_blood_pressure_systolic = new_value[0]
            self.latest_blood_pressure_diastolic = new_value[1]
        elif metric_name == "bmi":
            self.latest_bmi = new_value
        elif metric_name == "cholesterol":
            self.latest_cholesterol_total = new_value
        elif metric_name == "hba1c":
            self.latest_hba1c = new_value
        elif metric_name == "fasting_blood_sugar":
            self.latest_fasting_blood_sugar = new_value

        db.session.commit()
