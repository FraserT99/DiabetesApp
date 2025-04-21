import os
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker  #Import Faker to generate random names
from models import db  #Import db from models to handle database interactions
from models.user import User  #Import User model to interact with User table
from models.patient import Patient  #Import Patient model to interact with Patient table
from models.health_history import HealthHistory  #Import HealthHistory for logging patient records
from models import db
from models.challenge import Challenge
from models.patientChallenge import PatientChallenge


#Initialise Faker to generate fake data (names, etc.)
fake = Faker()

#Define realistic ranges for the new health-related metrics
health_metrics_ranges = {
    #Nutrition & Hydration
    "latest_calories_consumed": (1200, 3000),
    "latest_protein_intake": (50, 150),
    "latest_carbs_intake": (150, 350),
    "latest_fats_intake": (40, 100),
    "latest_fiber_intake": (10, 40),
    "latest_water_intake": (1.5, 4.0),

    #Fitness & Activity
    "latest_steps_taken": (2000, 15000),
    "latest_active_minutes": (10, 180),
    "latest_calories_burned": (200, 800),
    "latest_distance_walked": (0.5, 10),
    "latest_workout_sessions": (0, 5),
    "latest_heart_rate": (60, 120),
    "latest_distance_ran": (0, 10),

    #Body Metrics
    "latest_weight": (50, 120),
    "latest_height": (150, 200)
}

def load_data_from_csv():
    """
    Loads diabetic patient data from a CSV file, creates Patient and User records,
    and stores them in the database if new data is found.
    """
    #Get the base directory of the project (parent directory of 'services')
    base_dir = os.path.dirname(os.path.abspath(__file__))  #Path to current file (data_loader.py)
    csv_file_path = os.path.join(base_dir, '..', 'data', 'diabetes_data.csv')  #Adjust path to 'data' folder
    csv_file_path = os.path.abspath(csv_file_path)  #Get the absolute path to the CSV file

    #Ensure the CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"[ERROR] CSV file not found at {csv_file_path}. Please check the file path.")
        return

    try:
        #Loading CSV data
        print("[INFO] Loading data from CSV...")
        df = pd.read_csv(csv_file_path)

        #Check if the CSV is empty
        if df.empty:
            print("[WARNING] The CSV file is empty.")
            return

        #Filter for only diabetic patients (Diagnosis = 1)
        print("[INFO] Filtering for diabetic patients...")
        df = df[df['Diagnosis'] == 1]

        #Check if there are any diabetic patients left to process
        if df.empty:
            print("[INFO] No diabetic patients found in the CSV. Exiting.")
            return

        #Get all Patient IDs from the database as a set
        print("[INFO] Checking existing patients in the database...")
        existing_patient_ids = {p.patient_id for p in Patient.query.all()}

        #Prevent reseeding if 10 or more patients already exist
        if Patient.query.count() >= 10:
            print("[INFO] 10 or more patients already exist. Skipping CSV seeding.")
            print_first_user()
            return

        #Get all Patient IDs from the CSV as a set
        csv_patient_ids = set(df['PatientID'])

        #Check if all patients in the CSV already exist in the database
        if csv_patient_ids.issubset(existing_patient_ids):
            print("[INFO] Data already loaded. No new patients to process.")#
            print_first_user()  #Print the first user's username every time
            return  #Early exit

        print("[INFO] New data found. Proceeding to load data...")

        #Create and load Patient records
        patient_ids = set()  #Track already loaded patient IDs to avoid duplicates

        #Limiting to 10 patients
        for _, row in df.iterrows():
            if len(patient_ids) >= 10:
                break  #Limit to only 10 users

            patient_id = row['PatientID']
            if patient_id in existing_patient_ids or patient_id in patient_ids:
                continue

            #Generate random first and last names based on gender
            if row.get('Gender') == 0:  #Male
                first_name = fake.first_name_male()
            elif row.get('Gender') == 1:  #Female
                first_name = fake.first_name_female()
            else:
                first_name = fake.first_name()  #Fallback in case gender is missing or other values

            last_name = fake.last_name()  #Generate a random last name
            
            #Generate fake but unique email and phone number
            email = fake.unique.email()
            phone_number = fake.unique.phone_number()

            #Generate a realistic points balance (100-1000)
            reward_points = random.randint(100, 1000)

            #Create and add the patient record
            new_patient = Patient(
                patient_id=patient_id,
                first_name=first_name,
                last_name=last_name,
                age=row.get('Age'),
                gender=row.get('Gender'),
                diagnosis=row.get('Diagnosis'),
                latest_fasting_blood_sugar=round(row.get('FastingBloodSugar'), 2) if pd.notnull(row.get('FastingBloodSugar')) else None,
                latest_blood_pressure_systolic=int(row.get('SystolicBP')) if pd.notnull(row.get('SystolicBP')) else None,
                latest_blood_pressure_diastolic=int(row.get('DiastolicBP')) if pd.notnull(row.get('DiastolicBP')) else None,
                latest_bmi=round(row.get('BMI'), 2) if pd.notnull(row.get('BMI')) else None,
                latest_cholesterol_total=round(row.get('CholesterolTotal'), 2) if pd.notnull(row.get('CholesterolTotal')) else None,
                latest_hba1c=round(row.get('HbA1c'), 2) if pd.notnull(row.get('HbA1c')) else None,
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
                health_literacy=row.get('HealthLiteracy'),
                #Privacy settings
                show_on_leaderboard=True,
                email_alerts=True,
                sms_alerts=True,
                data_export_consent=False,
                email=email,
                phone_number=phone_number,

                reward_points=reward_points,

                #New Metrics
                #New Metrics with rounding applied
                latest_calories_consumed=round(random.uniform(1200, 3000), 2),
                latest_protein_intake=round(random.uniform(50, 150), 2),
                latest_carbs_intake=round(random.uniform(150, 350), 2),
                latest_fats_intake=round(random.uniform(40, 100), 2),
                latest_fiber_intake=round(random.uniform(10, 40), 2),
                latest_water_intake=round(random.uniform(1.5, 4.0), 2),
                latest_steps_taken=random.randint(2000, 15000),  #integers don’t need rounding
                latest_active_minutes=random.randint(10, 180),
                latest_calories_burned=round(random.uniform(200, 800), 2),
                latest_distance_walked=round(random.uniform(0.5, 10), 2),
                latest_workout_sessions=random.randint(0, 5),
                latest_heart_rate=random.randint(60, 120),
                latest_distance_ran=round(random.uniform(0, 10), 2),
                latest_weight=round(random.uniform(50, 120), 2),
                latest_height=round(random.uniform(150, 200), 2),
            )

            #Add the patient to the session
            db.session.add(new_patient)
            patient_ids.add(patient_id)  #Mark this patient as loaded

            #Create User records
            username = generate_username(last_name, patient_id)

            #Default password here
            default_password = "DefaultPassword123"  

            if User.query.filter_by(username=username).first():
                print(f"[WARNING] Username {username} already exists. Skipping this user.")
                continue

            new_user = User(username=username, password=default_password, patient_id=new_patient.patient_id)

            db.session.add(new_user)

        #Commit remaining records
        db.session.commit()
        print(f"[INFO] Committed 10 patients and users.")

        print(f"[INFO] Total new patients and users loaded: {len(patient_ids)}")
        
        seed_challenges()
        
        #Seed challenge progress
        seed_patient_challenge_progress()

        #Seed historical health data for all patients
        seed_health_history()

        print("[INFO] Historical health data successfully seeded for all users.")
        
        print_first_user()  #Print the first user's username every time

    except Exception as e:
        print(f"[ERROR] Failed to load CSV data. Exception: {e}")

def seed_patient_challenge_progress():
 
    print("[INFO] Seeding challenge progress for patients...")
    patients = Patient.query.all()
    challenges = Challenge.query.all()

    if not challenges:
        print("[WARNING] No challenges found. Skipping challenge progress seeding.")
        return

    total_entries = 0

    for patient in patients:
        for challenge in challenges:
            #Skip if patient already has this challenge
            existing_entry = PatientChallenge.query.filter_by(patient_id=patient.patient_id, challenge_id=challenge.id).first()
            if existing_entry:
                continue

            #Start progress at 0 (it will be updated dynamically based on health history)
            new_entry = PatientChallenge(
                patient_id=patient.patient_id,
                challenge_id=challenge.id,
                progress=0,
                completed=False
            )

            db.session.add(new_entry)
            total_entries += 1

    db.session.commit()
    print(f"[INFO] Assigned {total_entries} challenge progress records successfully.")
    
from pytz import UTC, timezone
UK_TZ = timezone("Europe/London")

def seed_health_history():

    print("[INFO] Seeding historical health data for the first five users...")

    users = User.query.limit(10).all()
    if not users:
        print("[WARNING] No users found. Skipping seeding.")
        return

    total_entries = 0
    today_uk = datetime.now(UK_TZ).date()

    for user in users:
        if not user.patient:
            print(f"[WARNING] User {user.username} has no associated patient record. Skipping.")
            continue

        patient = user.patient

        #Start seeding from 29 days ago
        start_date = datetime.combine(today_uk - timedelta(days=29), datetime.min.time()).astimezone(UTC)

        #Automatically detect all "latest_" metrics
        latest_metrics = {
            attr: getattr(patient, attr)
            for attr in dir(patient)
            if attr.startswith("latest_") and not callable(getattr(patient, attr)) and not attr.startswith("__")
        }

        for metric, latest_value in latest_metrics.items():
            if latest_value is None or latest_value == "N/A":
                min_val, max_val = health_metrics_ranges.get(metric, (50, 100))
                latest_value = round(random.uniform(min_val, max_val), 2)
            else:
                latest_value = round(latest_value, 2)

            #Seed 29 historical days
            for day in range(29):
                record_date = start_date + timedelta(days=day)

                existing_record = HealthHistory.query.filter_by(
                    patient_id=patient.patient_id,
                    metric_name=metric,
                    recorded_at=record_date
                ).first()

                if not existing_record:
                    variation = round(random.uniform(latest_value * 0.8, latest_value * 1.2), 2)
                    db.session.add(HealthHistory(
                        patient_id=patient.patient_id,
                        metric_name=metric,
                        value=variation,
                        recorded_at=record_date
                    ))
                    total_entries += 1

            #Ensure a clean log is created for today at 00:00 UK time (UTC converted)
            today_utc = datetime.combine(today_uk, datetime.min.time()).astimezone(UTC)

            existing_today = HealthHistory.query.filter_by(
                patient_id=patient.patient_id,
                metric_name=metric,
                recorded_at=today_utc
            ).first()

            if not existing_today:
                db.session.add(HealthHistory(
                    patient_id=patient.patient_id,
                    metric_name=metric,
                    value=latest_value,
                    recorded_at=today_utc
                ))
                total_entries += 1

    db.session.commit()
    print(f"[INFO] Seeded {total_entries} historical health records for the first five users.")


def generate_username(last_name, patient_id):
    """
    Generates a username using the first 3 letters of the last name and the patient ID.
    """
    return last_name[:3].lower() + str(patient_id)

from models import db
from models.challenge import Challenge

def seed_challenges():
    challenges = [
        #Daily Challenges
        {"name": "Daily Steps", "description": "Walk 5,000 steps today.", "goal": 5000, "challenge_type": "daily", "reward_points": 10},
        {"name": "Daily Calories Burned", "description": "Burn 300 calories today.", "goal": 300, "challenge_type": "daily", "reward_points": 10},
        {"name": "Daily Active Time", "description": "Log at least 30 active minutes today.", "goal": 30, "challenge_type": "daily", "reward_points": 10},
        {"name": "Daily Hydration", "description": "Drink at least 2.5L of water today.", "goal": 2.5, "challenge_type": "daily", "reward_points": 10},


        #Weekly Challenges
        {"name": "Weekly Steps", "description": "Walk 35,000 steps this week.", "goal": 35000, "challenge_type": "weekly", "reward_points": 50},
        {"name": "Weekly Calories Burned", "description": "Burn 2,000 calories this week.", "goal": 2000, "challenge_type": "weekly", "reward_points": 50},
        {"name": "Weekly Distance Walked", "description": "Walk 15 kilometers this week.", "goal": 15, "challenge_type": "weekly", "reward_points": 50},
        {"name": "Weekly Running Distance", "description": "Run at least 10 km this week.", "goal": 10, "challenge_type": "weekly", "reward_points": 50},


        #Monthly Challenges
        {"name": "Monthly Steps", "description": "Walk 150,000 steps this month.", "goal": 150000, "challenge_type": "monthly", "reward_points": 100},
        {"name": "Monthly Calories Burned", "description": "Burn 8,000 calories this month.", "goal": 8000, "challenge_type": "monthly", "reward_points": 100},
        {"name": "Monthly Weight Loss", "description": "Lose 2 kg this month.", "goal": 2, "challenge_type": "monthly", "reward_points": 100},
        {"name": "Monthly Fiber Intake", "description": "Consume at least 500g of fiber this month.", "goal": 500, "challenge_type": "monthly", "reward_points": 10},
    ]   

    #Insert the challenges into the database
    for challenge in challenges:
        existing_challenge = Challenge.query.filter_by(name=challenge["name"]).first()
        if not existing_challenge:
            new_challenge = Challenge(
                name=challenge["name"],
                description=challenge["description"],
                goal=challenge["goal"],
                challenge_type=challenge["challenge_type"],
                reward_points=challenge["reward_points"]
            )
            db.session.add(new_challenge)

    db.session.commit()
    print("[INFO] Successfully seeded challenges!")

def print_first_user():
    """
    Fetches and prints the first patient's full details, including patient fields,
    all latest health metrics, historical data, and associated user information.
    """
    first_user = User.query.first()

    if not first_user or not first_user.patient:
        print("[WARNING] No users or patients found in the database.")
        return

    patient = first_user.patient

    history_records = HealthHistory.query.filter_by(
        patient_id=patient.patient_id
    ).order_by(HealthHistory.recorded_at.desc()).limit(5).all()

    print("\n======================")
    print(f"[INFO] First Patient's Full Details")
    print("======================")
    print(f"Username: {first_user.username}")
    print(f"Patient ID: {patient.patient_id}")
    print(f"Name: {patient.first_name} {patient.last_name}")
    print(f"Age: {patient.age} | Gender: {'Male' if patient.gender == 0 else 'Female'} | Ethnicity: {patient.ethnicity}")
    print(f"Diagnosis: {'Diabetes' if patient.diagnosis == 1 else 'No Diabetes'}")
    print(f"Reward Points: {patient.reward_points}")
    
  
