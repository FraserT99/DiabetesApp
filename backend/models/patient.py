from models import db
from models.health_history import HealthHistory  # Import HealthHistory

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)  # PatientID: A unique identifier assigned to each patient (6000 to 7878).
    first_name = db.Column(db.String(100))  # First name of the patient
    last_name = db.Column(db.String(100))  # Last name of the patient
    age = db.Column(db.Integer)  # Age: The age of the patients ranges from 20 to 90 years
    gender = db.Column(db.Integer)  # Gender: 0 for Male, 1 for Female (integer representation)
    ethnicity = db.Column(db.Integer)  # Ethnicity: 0: Caucasian, 1: African American, 2: Asian, 3: Other
    diagnosis = db.Column(db.Integer)  # Diagnosis: 0 for No Diabetes, 1 for Diabetes

    # ============================
    # Lifestyle and Health Behavior Section
    # ============================
    smoking = db.Column(db.Boolean)  # Smoking: 0 for non-smoker, 1 for smoker
    alcohol_consumption = db.Column(db.Float)  # Alcohol Consumption: Weekly alcohol consumption in units, ranging from 0 to 20
    physical_activity = db.Column(db.Float)  # Physical Activity: Weekly activity in hours (0 to 10)
    diet_quality = db.Column(db.Float)  # Diet Quality: Diet quality score (0 to 10)
    sleep_quality = db.Column(db.Float)  # Sleep Quality: Sleep quality score (4 to 10)

    # ============================
    # Medical History Section
    # ============================
    family_history_diabetes = db.Column(db.Boolean)  # Family History of Diabetes: 1 if family history, 0 if not
    gestational_diabetes = db.Column(db.Boolean)  # Gestational Diabetes: 1 if yes, 0 if no
    polycystic_ovary_syndrome = db.Column(db.Boolean)  # Polycystic Ovary Syndrome: 1 if yes, 0 if no
    previous_pre_diabetes = db.Column(db.Boolean)  # Previous Pre-Diabetes: 1 if yes, 0 if no
    hypertension = db.Column(db.Boolean)  # Hypertension: 1 if yes, 0 if no

    # ============================
    # Medications Section
    # ============================
    antihypertensive_medications = db.Column(db.Boolean)  # Antihypertensive Medications: 1 if on antihypertensive, 0 if not
    statins = db.Column(db.Boolean)  # Statins: 1 if on statins, 0 if not
    antidiabetic_medications = db.Column(db.Boolean)  # Antidiabetic Medications: 1 if on antidiabetic, 0 if not

    # ============================
    # Medical Checkups and Adherence Section
    # ============================
    medical_checkups_frequency = db.Column(db.Integer)  # Medical Checkups Frequency: Frequency of check-ups (0 to 4)
    medication_adherence = db.Column(db.Float)  # Medication Adherence: Medication adherence score (0 to 10)
    health_literacy = db.Column(db.Float)  # Health Literacy: Health literacy score (0 to 10)

    # ============================
    # Latest Health Metrics Section
    # ============================
    latest_blood_pressure_systolic = db.Column(db.Integer)  # Systolic BP: Ranges from 90 to 180 mmHg
    latest_blood_pressure_diastolic = db.Column(db.Integer)  # Diastolic BP: Ranges from 60 to 120 mmHg
    latest_bmi = db.Column(db.Float)  # BMI: Body Mass Index (15 to 40)
    latest_cholesterol_total = db.Column(db.Float)  # Cholesterol Total: Ranges from 150 to 300 mg/dL
    latest_hba1c = db.Column(db.Float)  # HbA1c: Hemoglobin A1c levels (4.0 to 10.0)
    latest_fasting_blood_sugar = db.Column(db.Float)  # Fasting Blood Sugar: Levels (70 to 200 mg/dL)

    # ============================
    # Relationship with Other Models Section
    # ============================
    user = db.relationship('User', back_populates='patient', uselist=False)  # Relationship with User model
    health_history = db.relationship('HealthHistory', backref='patient', lazy='dynamic', cascade="all, delete-orphan")  # Relationship to HealthHistory model

    def __repr__(self):
        return f'<Patient(id={self.patient_id}, name={self.first_name} {self.last_name})>'

    # ============================
    # Method to Update Health Metrics Section
    # ============================
    def update_health_metric(self, metric_name, new_value):
        """Method to update any health metric and log it into health history."""
        # Record the previous value to history
        history_entry = HealthHistory(
            patient_id=self.patient_id,
            metric_name=metric_name,
            value=new_value
        )
        db.session.add(history_entry)

        # Update the latest value in the patient table based on the metric name
        if metric_name == "blood_pressure":
            self.latest_blood_pressure_systolic = new_value[0]  # Systolic BP update
            self.latest_blood_pressure_diastolic = new_value[1]  # Diastolic BP update
        elif metric_name == "bmi":
            self.latest_bmi = new_value  # BMI update
        elif metric_name == "cholesterol":
            self.latest_cholesterol_total = new_value  # Cholesterol Total update
        elif metric_name == "hba1c":
            self.latest_hba1c = new_value  # HbA1c update
        elif metric_name == "fasting_blood_sugar":
            self.latest_fasting_blood_sugar = new_value  # Fasting Blood Sugar update

        db.session.commit()  # Commit changes to the database
