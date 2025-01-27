import os
import pandas as pd
import string, random
from faker import Faker  # Import Faker to generate random names
from models import db  # Import db from models to handle database interactions
from models.user import User  # Import User model to interact with User table
from models.patient import Patient  # Import Patient model to interact with Patient table

# Initialize Faker to generate fake data (names, etc.)
fake = Faker()

def load_data_from_csv():
    """
    Loads diabetic patient data from a CSV file, creates Patient and User records,
    and stores them in the database.
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

        # --- STEP 1: Create and load Patient records ---
        loaded_patient_count = 0
        batch_size = 100  # Commit in batches to improve performance
        patient_ids = set()  # Track already loaded patient IDs to avoid duplicates

        # Iterate through each row in the CSV to process patients
        for _, row in df.iterrows():
            # Only add diabetic patients (Diagnosis = 1)
            if str(row.get('Diagnosis')) != "1":
                continue  # Skip non-diabetic patients silently

            patient_id = row['PatientID']

            # Generate random first and last names based on gender
            if row.get('Gender') == 0:  # Male
                first_name = fake.first_name_male()
            elif row.get('Gender') == 1:  # Female
                first_name = fake.first_name_female()
            else:
                first_name = fake.first_name()  # Fallback in case gender is missing or other values

            last_name = fake.last_name()  # Generate a random last name

            # Create and add the patient record if not already added
            if patient_id not in patient_ids:
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
        
        print(f"[INFO] Total patients loaded: {len(patient_ids)}")

        # --- STEP 2: Create and load User records ---
        loaded_user_count = 0
        users_to_add = []  # Temporary list to hold users before committing
        total_users_created = 0  # Keep a total count of users created

        # List to store the first 2 users with their passwords for later display
        first_two_users = []

        for _, row in df.iterrows():
            if str(row.get('Diagnosis')) != "1":  # Only add diabetic patients
                continue

            patient_id = row['PatientID']

            # Fetch the related patient to ensure it exists in the database
            patient = Patient.query.filter_by(patient_id=patient_id).first()
            if not patient:
                print(f"[ERROR] No patient found for Patient ID {patient_id}. Skipping user creation.")
                continue

            # Generate a username based on the patient's last name and patient ID
            username = generate_username(patient.last_name, patient.patient_id)

            # Generate a random password
            password = generate_random_password()

            # Check if the user already exists for this patient
            existing_user = User.query.filter_by(patient_id=patient_id).first()
            if existing_user:
                continue  # Skip if a user already exists for the patient

            # Create the new user and append it to the list for batch processing
            new_user = User(username=username, password=password, patient_id=patient_id)
            users_to_add.append(new_user)

            # Store the first two users and their plain-text passwords for later display
            if len(first_two_users) < 2:
                first_two_users.append((new_user, password))  # Store the user and their plain-text password

            # Commit users in batches
            if len(users_to_add) >= batch_size:
                db.session.add_all(users_to_add)
                db.session.commit()  # Commit the current batch of users
                print(f"[INFO] Committed {len(users_to_add)} users.")
                total_users_created += len(users_to_add)
                users_to_add = []  # Reset the list for the next batch

        # Commit any remaining users in the list
        if users_to_add:
            db.session.add_all(users_to_add)
            db.session.commit()
            print(f"[INFO] Committed remaining {len(users_to_add)} users.")
            total_users_created += len(users_to_add)

        print(f"[INFO] Total users created: {total_users_created}")

        # --- STEP 3: Fetch and print the first 2 users with all their data ---
        print("\nFirst 2 Users in the Database:")
        for user, plain_password in first_two_users:
            # Print user details first
            print(f"User ID: {user.id}, Username: {user.username}, Plain-text Password: {plain_password}, Patient ID: {user.patient_id}")

            # Print patient details after the user info
            patient = user.patient  # Accessing the related patient
            if patient:
                print(f"Patient ID: {patient.patient_id}, First Name: {patient.first_name}, Last Name: {patient.last_name}, Age: {patient.age}, Gender: {patient.gender}, Diagnosis: {patient.diagnosis}, Fasting Blood Sugar: {patient.latest_fasting_blood_sugar}, Blood Pressure: {patient.latest_blood_pressure_systolic}/{patient.latest_blood_pressure_diastolic}, BMI: {patient.latest_bmi}, Cholesterol: {patient.latest_cholesterol_total}, HbA1c: {patient.latest_hba1c}, Ethnicity: {patient.ethnicity}, Smoking: {patient.smoking}, Alcohol Consumption: {patient.alcohol_consumption}, Physical Activity: {patient.physical_activity}, Diet Quality: {patient.diet_quality}, Sleep Quality: {patient.sleep_quality}, Family History of Diabetes: {patient.family_history_diabetes}, Gestational Diabetes: {patient.gestational_diabetes}, PCOS: {patient.polycystic_ovary_syndrome}, Previous Pre-Diabetes: {patient.previous_pre_diabetes}, Hypertension: {patient.hypertension}, Antihypertensive Medications: {patient.antihypertensive_medications}, Statins: {patient.statins}, Antidiabetic Medications: {patient.antidiabetic_medications}, Medical Checkups Frequency: {patient.medical_checkups_frequency}, Medication Adherence: {patient.medication_adherence}, Health Literacy: {patient.health_literacy}")
            else:
                print("No linked patient found.")

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
