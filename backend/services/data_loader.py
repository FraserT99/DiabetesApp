import os
import pandas as pd
import string
import random
from faker import Faker  # Import Faker to generate random names
from models import db  # Import db from models to handle database interactions
from models.user import User  # Import User model to interact with User table
from models.patient import Patient  # Import Patient model to interact with Patient table

# Initialize Faker to generate fake data (names, etc.)
fake = Faker()

def load_data_from_csv():
    """
    Loads diabetic patient data from a CSV file, creates Patient and User records,
    and stores them in the database if new data is found.
    """
    # Get the base directory of the project (parent directory of 'services')
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Path to current file (data_loader.py)
    csv_file_path = os.path.join(base_dir, '..', 'data', 'diabetes_data.csv')  # Adjust path to 'data' folder
    csv_file_path = os.path.abspath(csv_file_path)  # Get the absolute path to the CSV file

    # Ensure the CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"[ERROR] CSV file not found at {csv_file_path}. Please check the file path.")
        return

    try:
        # Loading CSV data
        print("[INFO] Loading data from CSV...")
        df = pd.read_csv(csv_file_path)

        # Check if the CSV is empty
        if df.empty:
            print("[WARNING] The CSV file is empty.")
            return

        # Filter for only diabetic patients (Diagnosis = 1)
        print("[INFO] Filtering for diabetic patients...")
        df = df[df['Diagnosis'] == 1]

        # Check if there are any diabetic patients left to process
        if df.empty:
            print("[INFO] No diabetic patients found in the CSV. Exiting.")
            return

        # Get all Patient IDs from the database as a set
        print("[INFO] Checking existing patients in the database...")
        existing_patient_ids = {p.patient_id for p in Patient.query.all()}

        # Get all Patient IDs from the CSV as a set
        csv_patient_ids = set(df['PatientID'])

        # Check if all patients in the CSV already exist in the database
        if csv_patient_ids.issubset(existing_patient_ids):
            print("[INFO] Data already loaded. No new patients to process.")
            return  # Early exit

        print("[INFO] New data found. Proceeding to load data...")

        # --- STEP 1: Create and load Patient records ---
        loaded_patient_count = 0
        batch_size = 100  # Commit in batches to improve performance
        patient_ids = set()  # Track already loaded patient IDs to avoid duplicates

        # Iterate through each row in the CSV to process patients
        for _, row in df.iterrows():
            patient_id = row['PatientID']

            # Skip patients that already exist in the database or have been processed in this run
            if patient_id in existing_patient_ids or patient_id in patient_ids:
                continue

            # Generate random first and last names based on gender
            if row.get('Gender') == 0:  # Male
                first_name = fake.first_name_male()
            elif row.get('Gender') == 1:  # Female
                first_name = fake.first_name_female()
            else:
                first_name = fake.first_name()  # Fallback in case gender is missing or other values

            last_name = fake.last_name()  # Generate a random last name

            # Create and add the patient record
            new_patient = Patient(
                patient_id=patient_id,
                first_name=first_name,
                last_name=last_name,
                age=row.get('Age'),
                gender=row.get('Gender'),
                diagnosis=row.get('Diagnosis'),
                latest_fasting_blood_sugar=row.get('FastingBloodSugar'),
                latest_blood_pressure_systolic=row.get('SystolicBP'),
                latest_blood_pressure_diastolic=row.get('DiastolicBP'),
                latest_bmi=row.get('BMI'),
                latest_cholesterol_total=row.get('CholesterolTotal'),
                latest_hba1c=row.get('HbA1c'),
                ethnicity=row.get('Ethnicity'),
                smoking=row.get('Smoking'),
                alcohol_consumption=row.get('AlcoholConsumption'),
                physical_activity=row.get('PhysicalActivity'),
                diet_quality=row.get('DietQuality'),
                sleep_quality=row.get('SleepQuality'),
                family_history_diabetes=row.get('FamilyHistoryDiabetes'),
                gestational_diabetes=row.get('GestationalDiabetes'),
                polycystic_ovary_syndrome=row.get('PolycysticOvarySyndrome'),
                previous_pre_diabetes=row.get('PreviousPreDiabetes'),
                hypertension=row.get('Hypertension'),
                antihypertensive_medications=row.get('AntihypertensiveMedications'),
                statins=row.get('Statins'),
                antidiabetic_medications=row.get('AntidiabeticMedications'),
                medical_checkups_frequency=row.get('MedicalCheckupsFrequency'),
                medication_adherence=row.get('MedicationAdherence'),
                health_literacy=row.get('HealthLiteracy')
            )

            # Add the patient to the session
            db.session.add(new_patient)
            patient_ids.add(patient_id)  # Mark this patient as loaded
            loaded_patient_count += 1

            # Commit patients in batches
            if loaded_patient_count >= batch_size:
                db.session.commit()  # Commit the current batch of patients
                print(f"[INFO] Committed {batch_size} patients.")
                loaded_patient_count = 0  # Reset counter for the next batch

        # Commit any remaining patient records that weren't committed in batches
        if loaded_patient_count > 0:
            db.session.commit()
            print(f"[INFO] Committed remaining {loaded_patient_count} patients.")

        print(f"[INFO] Total new patients loaded: {len(patient_ids)}")

    except Exception as e:
        print(f"[ERROR] Failed to load CSV data. Exception: {e}")


# Helper functions

def generate_username(last_name, patient_id):
    """
    Generates a username using the first 3 letters of the last name and the patient ID.
    """
    return last_name[:3].lower() + str(patient_id)

def generate_random_password(length=12):
    """
    Generates a random password containing letters, digits, and symbols.
    """
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(all_characters, k=length))
    return password
