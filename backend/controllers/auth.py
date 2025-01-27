from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from models import db
from models.user import User
from models.patient import Patient  # Import Patient model for registration

auth_bp = Blueprint('auth', __name__)

from flask import redirect, url_for

@auth_bp.route('/api/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()

        # Extract required fields
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        age = data.get('age')
        gender = data.get('gender')
        ethnicity = data.get('ethnicity')
        diagnosis = data.get('diagnosis')
        smoking = data.get('smoking')
        family_history_diabetes = data.get('family_history_diabetes', False)

        # Check if required fields are provided
        if not all([first_name, last_name, password, age, gender, ethnicity, diagnosis is not None, smoking is not None]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Create Patient entry first
        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            diagnosis=diagnosis,
            ethnicity=ethnicity,
            family_history_diabetes=family_history_diabetes,
            smoking=smoking,
            alcohol_consumption=0.0,
            physical_activity=0.0,
            diet_quality=0.0,
            sleep_quality=0.0,
            gestational_diabetes=False,
            polycystic_ovary_syndrome=False,
            previous_pre_diabetes=False,
            hypertension=False,
            antihypertensive_medications=False,
            statins=False,
            antidiabetic_medications=False,
            medical_checkups_frequency="unknown",
            medication_adherence=0.0,
            health_literacy=0.0,
            latest_blood_pressure_systolic=0,
            latest_blood_pressure_diastolic=0,
            latest_bmi=0.0,
            latest_cholesterol_total=0.0,
            latest_hba1c=0.0,
            latest_fasting_blood_sugar=0.0,
        )

        # Add patient to the session and commit to get an ID
        db.session.add(new_patient)
        db.session.commit()  # Patient gets its patient_id assigned now

        # Now, generate username using the patient_id
        username = f"{last_name[:3].lower()}{new_patient.patient_id}"  # Using the actual patient_id after commit

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400

        # Now create the user
        new_user = User(username=username, password=password)  # Pass the plain password
        new_user.patient_id = new_patient.patient_id  # Link the patient ID to the user

        # Commit the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()

            # Print full details of the new user and patient in the terminal
            print(f"[INFO] New User Registered: {new_user.username}")
            print(f"[INFO] User ID: {new_user.id}, Username: {new_user.username}, Plain-text Password: {password}, Patient ID: {new_user.patient_id}")

            # Now, print the patient's details as requested
            print(f"[INFO] Patient ID: {new_patient.patient_id}, First Name: {new_patient.first_name}, Last Name: {new_patient.last_name}, "
                  f"Age: {new_patient.age}, Gender: {new_patient.gender}, Diagnosis: {new_patient.diagnosis}, "
                  f"Fasting Blood Sugar: {new_patient.latest_fasting_blood_sugar}, Blood Pressure: {new_patient.latest_blood_pressure_systolic}/{new_patient.latest_blood_pressure_diastolic}, "
                  f"BMI: {new_patient.latest_bmi}, Cholesterol: {new_patient.latest_cholesterol_total}, "
                  f"HbA1c: {new_patient.latest_hba1c}, Ethnicity: {new_patient.ethnicity}, Smoking: {new_patient.smoking}, "
                  f"Alcohol Consumption: {new_patient.alcohol_consumption}, Physical Activity: {new_patient.physical_activity}, "
                  f"Diet Quality: {new_patient.diet_quality}, Sleep Quality: {new_patient.sleep_quality}, "
                  f"Family History of Diabetes: {new_patient.family_history_diabetes}, Gestational Diabetes: {new_patient.gestational_diabetes}, "
                  f"PCOS: {new_patient.polycystic_ovary_syndrome}, Previous Pre-Diabetes: {new_patient.previous_pre_diabetes}, "
                  f"Hypertension: {new_patient.hypertension}, Antihypertensive Medications: {new_patient.antihypertensive_medications}, "
                  f"Statins: {new_patient.statins}, Antidiabetic Medications: {new_patient.antidiabetic_medications}, "
                  f"Medical Checkups Frequency: {new_patient.medical_checkups_frequency}, Medication Adherence: {new_patient.medication_adherence}, "
                  f"Health Literacy: {new_patient.health_literacy}")

            login_user(new_user)  # Log the user in after registration

            # Return the logged-in username
            return jsonify({
                "success": True,
                "message": "Registration successful. User logged in.",
                "username": new_user.username
            })

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] {str(e)}")
            return jsonify({"success": False, "message": "An error occurred during registration"}), 500

    return jsonify({"success": False, "message": "Invalid request"}), 400

# Login Route
@auth_bp.route('/api/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Plain-text password from the request

        print(f"[DEBUG] Attempting login for username: {username}, Plain-text Password: {password}")

        user = User.query.filter_by(username=username).first()

        if user:
            print(f"[DEBUG] Found user: {user.username}, Password Hash: {user.password_hash}")

        if user and check_password_hash(user.password_hash, password):
            print(f"[DEBUG] Login successful for user: {user.username}")
            login_user(user)
            return jsonify({"success": True, "message": "Login successful", "username": user.username})

        print(f"[DEBUG] Invalid credentials provided.")
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    return jsonify({"success": False, "message": "Invalid request"}), 400
