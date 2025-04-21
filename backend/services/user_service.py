from datetime import datetime
import pandas as pd
from models import db
from models.user import User
from models.patient import Patient
from models.health_history import HealthHistory

#Centralized Metric Dictionary
METRIC_LABELS = {
    "latest_fasting_blood_sugar": "Fasting Blood Sugar (mg/dL)",
    "latest_hba1c": "HbA1c Level (%)",
    "latest_bmi": "Body Mass Index (BMI)",
    "latest_blood_pressure_systolic": "Systolic Blood Pressure (mmHg)",
    "latest_calories_consumed": "Calories Consumed (kcal)",
    "latest_protein_intake": "Protein Intake (g)",
    "latest_carbs_intake": "Carbohydrates (g)",
    "latest_fats_intake": "Fats (g)",
    "latest_fiber_intake": "Fiber Intake (g)",
    "latest_water_intake": "Water Intake (L)",
    "latest_steps_taken": "Steps Taken",
    "latest_active_minutes": "Active Minutes",
    "latest_calories_burned": "Calories Burned",
    "latest_distance_walked": "Distance Walked (km)",
    "latest_workout_sessions": "Workout Sessions",
    "latest_heart_rate": "Heart Rate (bpm)",
    "latest_distance_ran": "Running Distance (km)",
    "latest_weight": "Weight (kg)",
    "latest_height": "Height (cm)",
}

#Centralized Metric Units
METRIC_UNITS = {
    "latest_fasting_blood_sugar": "mg/dL",      #Fasting Blood Sugar
    "latest_hba1c": "%",                        #HbA1c Level
    "latest_bmi": "BMI",                        #Body Mass Index
    "latest_blood_pressure_systolic": "mmHg",   #Systolic Blood Pressure
    "latest_calories_consumed": "kcal",         #Calories Consumed
    "latest_protein_intake": "g",               #Protein Intake
    "latest_carbs_intake": "g",                 #Carbohydrates Intake
    "latest_fats_intake": "g",                  #Fats Intake
    "latest_fiber_intake": "g",                 #Fiber Intake
    "latest_water_intake": "L",                 #Water Intake
    "latest_steps_taken": "steps",              #Steps Taken
    "latest_active_minutes": "minutes",         #Active Minutes
    "latest_calories_burned": "kcal",           #Calories Burned
    "latest_distance_walked": "km",             #Distance Walked
    "latest_workout_sessions": "sessions",      #Workout Sessions
    "latest_heart_rate": "bpm",                 #Heart Rate
    "latest_distance_ran": "km",                #Running Distance
    "latest_weight": "kg",                      #Weight
    "latest_height": "cm",                      #Height
}

#Centralized Thresholds
THRESHOLDS = {
    "latest_fasting_blood_sugar": {"normal": (70, 99), "warning": (100, 125), "critical": (126, 400)},
    "latest_hba1c": {"normal": (4.0, 5.6), "warning": (5.7, 6.4), "critical": (6.5, 15)},
    "latest_bmi": {"normal": (18.5, 24.9), "warning": (25, 29.9), "critical": (30, 60)},
    "latest_blood_pressure_systolic": {"normal": (90, 119), "warning": (120, 139), "critical": (140, 250)},
    
    "latest_calories_consumed": {"normal": (1500, 2500), "warning": (2501, 3000), "critical": (3001, 5000)},
    "latest_protein_intake": {"normal": (50, 100), "warning": (101, 130), "critical": (131, 200)},
    "latest_carbs_intake": {"normal": (130, 300), "warning": (301, 350), "critical": (351, 500)},
    "latest_fats_intake": {"normal": (40, 80), "warning": (81, 100), "critical": (101, 150)},
    "latest_fiber_intake": {"normal": (25, 40), "warning": (10, 24), "critical": (0, 9)},
    "latest_water_intake": {"normal": (2, 3.5), "warning": (1.5, 1.9), "critical": (0, 1.4)},
    
    "latest_steps_taken": {"normal": (7000, 12000), "warning": (3000, 6999), "critical": (0, 2999)},
    "latest_active_minutes": {"normal": (30, 120), "warning": (10, 29), "critical": (0, 9)},
    "latest_calories_burned": {"normal": (300, 600), "warning": (150, 299), "critical": (0, 149)},
    "latest_distance_walked": {"normal": (2, 8), "warning": (1, 1.9), "critical": (0, 0.9)},
    "latest_workout_sessions": {"normal": (3, 5), "warning": (1, 2), "critical": (0, 0)},
    
    "latest_heart_rate": {"normal": (60, 90), "warning": (91, 110), "critical": (111, 200)},
    "latest_distance_ran": {"normal": (3, 10), "warning": (1, 2.9), "critical": (0, 0.9)},
    
    "latest_weight": {"normal": (50, 80), "warning": (81, 100), "critical": (101, 200)},
    "latest_height": {"normal": (150, 190), "warning": (191, 200), "critical": (201, 250)},
}

GOAL_TYPE_OPTIONS_BY_METRIC = {
    "latest_fasting_blood_sugar": ["daily"],
    "latest_hba1c": ["monthly"],  #Usually measured monthly or quarterly
    "latest_bmi": ["monthly"],
    "latest_blood_pressure_systolic": ["daily"],
    "latest_blood_pressure_diastolic": ["daily"],
    "latest_cholesterol_total": ["monthly"],  #Often checked every few months

    "latest_calories_consumed": ["daily", "weekly", "monthly"],
    "latest_protein_intake": ["daily", "weekly"],
    "latest_carbs_intake": ["daily", "weekly"],
    "latest_fats_intake": ["daily", "weekly"],
    "latest_fiber_intake": ["daily", "weekly"],
    "latest_water_intake": ["daily"],
    
    "latest_steps_taken": ["daily", "weekly", "monthly"],
    "latest_active_minutes": ["daily", "weekly", "monthly"],
    "latest_calories_burned": ["daily", "weekly", "monthly"],
    "latest_distance_walked": ["daily", "weekly", "monthly"],
    "latest_workout_sessions": ["weekly", "monthly"],
    "latest_heart_rate": ["daily"],
    "latest_distance_ran": ["daily", "weekly", "monthly"],
    
    "latest_weight": ["monthly"],
    "latest_height": []  #Typically static
}

#Metric behavior for goal tracking
METRIC_GOAL_BEHAVIOR = {
    "latest_steps_taken": "cumulative",
    "latest_calories_burned": "cumulative",
    "latest_distance_walked": "cumulative",
    "latest_calories_consumed": "cumulative",
    "latest_protein_intake": "cumulative",
    "latest_carbs_intake": "cumulative",
    "latest_fats_intake": "cumulative",
    "latest_fiber_intake": "cumulative",
    "latest_water_intake": "cumulative",
    "latest_active_minutes": "cumulative",
    "latest_workout_sessions": "cumulative",
    "latest_distance_ran": "cumulative",

    "latest_heart_rate": "average",
    "latest_hba1c": "average",
    "latest_blood_pressure_systolic": "average",
    "latest_fasting_blood_sugar": "average",

    "latest_bmi": "change",
    "latest_weight": "change",
}

METRIC_CATEGORIES = {
    "medical": [
        "latest_fasting_blood_sugar", "latest_hba1c", "latest_bmi",
        "latest_blood_pressure_systolic", "latest_blood_pressure_diastolic",
        "latest_heart_rate"
    ],
    "nutrition": [
        "latest_calories_consumed", "latest_protein_intake", "latest_carbs_intake",
        "latest_fats_intake", "latest_fiber_intake", "latest_water_intake"
    ],
    "activity": [
        "latest_steps_taken", "latest_active_minutes", "latest_calories_burned",
        "latest_distance_walked", "latest_workout_sessions", "latest_distance_ran"
    ],
    "body": [
        "latest_weight", "latest_height"
    ]
}

#Mappings for coded fields
GENDER_MAP = {0: "Male", 1: "Female"}
ETHNICITY_MAP = {0: "Caucasian", 1: "African American", 2: "Asian", 3: "Other"}
YES_NO_MAP = {0: "No", 1: "Yes"}
DIAGNOSIS_MAP = {0: "None", 1: "Diabetes"}
WATER_QUALITY_MAP = {0: "Good", 1: "Poor"}


#Fetch User Data
def fetch_user_data(username):
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return {}

    patient = user.patient

    #Start with basic user info
    user_data = {
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "age": patient.age,
        "gender": GENDER_MAP.get(patient.gender, 'Unknown'),
        "ethnicity": ETHNICITY_MAP.get(patient.ethnicity, 'Unknown'),
        "smoking": YES_NO_MAP.get(patient.smoking, 'Unknown'),
        "alcohol_consumption": round(patient.alcohol_consumption, 2),
        "physical_activity": round(patient.physical_activity, 2),
        "diet_quality": round(patient.diet_quality, 2),
        "sleep_quality": round(patient.sleep_quality, 2),
        "diagnosis": DIAGNOSIS_MAP.get(patient.diagnosis, 'Unknown'),

        "hypertension": YES_NO_MAP.get(patient.hypertension, 'Unknown'),
        "previous_pre_diabetes": YES_NO_MAP.get(patient.previous_pre_diabetes, 'Unknown'),
        "polycystic_ovary_syndrome": YES_NO_MAP.get(patient.polycystic_ovary_syndrome, 'Unknown'),
        "gestational_diabetes": YES_NO_MAP.get(patient.gestational_diabetes, 'Unknown'),
        "family_history_diabetes": YES_NO_MAP.get(patient.family_history_diabetes, 'Unknown'),

        "antihypertensive_medications": YES_NO_MAP.get(patient.antihypertensive_medications, 'Unknown'),
        "statins": YES_NO_MAP.get(patient.statins, 'Unknown'),
        "antidiabetic_medications": YES_NO_MAP.get(patient.antidiabetic_medications, 'Unknown'),

        "medical_checkups_frequency": round(patient.medical_checkups_frequency, 2),
        "medication_adherence": round(patient.medication_adherence, 2),
        "health_literacy": round(patient.health_literacy, 2),
        
        "show_on_leaderboard": patient.show_on_leaderboard,
        "email_alerts": patient.email_alerts,
        "sms_alerts": patient.sms_alerts,
        "data_export_consent": patient.data_export_consent,
    }

    #Dynamically add all metric fields defined in METRIC_LABELS
    for field in METRIC_LABELS.keys():
        if field not in user_data:  #Avoid overwriting existing values
            value = getattr(patient, field, None)
            user_data[field] = round(value, 2) if isinstance(value, (int, float)) and value is not None else "N/A"

    #Add reward points at the end
    user_data["reward_points"] = patient.reward_points if patient.reward_points is not None else 0

    return user_data

#Fetch Health History
def fetch_health_history(username, metric_name):
    """Fetch historical health data for a specific metric."""
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.patient:
        return pd.DataFrame()

    patient = user.patient
    patient_id = patient.patient_id

    #Fetch only explicitly logged history
    history_records = (
        HealthHistory.query
        .filter_by(patient_id=patient_id, metric_name=metric_name)
        .order_by(HealthHistory.recorded_at.asc())
        .all()
    )

    #Safely construct data list
    data = []
    for record in history_records:
        if record.recorded_at:
            data.append({
                "Date": record.recorded_at,
                "Value": round(record.value, 2)
            })

    #If nothing was added, return empty df
    if not data:
        return pd.DataFrame()

    #Now build and sort the DataFrame
    df = pd.DataFrame(data)
    if "Date" not in df.columns:
        return pd.DataFrame()  #just in case

    return df.sort_values("Date", ascending=True)


def fetch_user_points(username):
    """Fetch the user's total reward points."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"[ERROR] User {username} not found.")
            return 0

        patient = Patient.query.filter_by(patient_id=user.patient_id).first()
        if not patient:
            print(f"[ERROR] No patient record found for {username}.")
            return 0

        print(f"[DEBUG] {username} has {patient.reward_points} points.")
        return patient.reward_points

    except Exception as e:
        print(f"[ERROR] Failed to fetch user points: {e}")
        return 0
    
def update_user_points(username, new_points):
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        print(f"[ERROR] No patient found for user: {username}")
        return False

    user.patient.reward_points = new_points
    db.session.commit()
    print(f"[UPDATE] {username}'s points set to {new_points}.")
    return True

def fetch_recent_activity(username, limit=3):
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return []

    entries = (HealthHistory.query
        .filter_by(patient_id=user.patient.patient_id)
        .order_by(HealthHistory.recorded_at.desc())
        .limit(limit)
        .all()
    )

    return [
        f"{entry.metric_name.replace('_', ' ').title()} → {round(entry.value, 2)} on {entry.recorded_at.strftime('%b %d, %Y')}"
        for entry in entries
    ]
    
def update_user_data(username, updated_data):
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return False

    patient = user.patient

    try:
        if "first_name" in updated_data:
            patient.first_name = updated_data["first_name"]
        if "last_name" in updated_data:
            patient.last_name = updated_data["last_name"]
        if "age" in updated_data:
            patient.age = updated_data["age"]
        if "gender" in updated_data:
            patient.gender = 0 if updated_data["gender"] == "Male" else 1
        if "smoking" in updated_data:
            patient.smoking = updated_data["smoking"]

        #Privacy Settings
        if "show_on_leaderboard" in updated_data:
            patient.show_on_leaderboard = updated_data["show_on_leaderboard"]
        if "email_alerts" in updated_data:
            patient.email_alerts = updated_data["email_alerts"]
        if "sms_alerts" in updated_data:
            patient.sms_alerts = updated_data["sms_alerts"]
        if "data_export_consent" in updated_data:
            patient.data_export_consent = updated_data["data_export_consent"]

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user data: {e}")
        return False
