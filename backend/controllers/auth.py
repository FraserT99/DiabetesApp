from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from models import db
from models.user import User
from models.patient import Patient  # Import Patient model for registration

auth_bp = Blueprint('auth', __name__)

# Route to register a new user
@auth_bp.route('/api/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()

        # Extract required fields from the incoming JSON data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        age = data.get('age')
        gender = data.get('gender')
        ethnicity = data.get('ethnicity')
        diagnosis = data.get('diagnosis')
        smoking = data.get('smoking')
        family_history_diabetes = data.get('family_history_diabetes', False)

        # Check if all required fields are present
        if not all([first_name, last_name, password, age, gender, ethnicity, diagnosis is not None, smoking is not None]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Create the Patient entry first and save it to the database
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
            medical_checkups_frequency=0.0,
            medication_adherence=0.0,
            health_literacy=0.0,
            latest_blood_pressure_systolic=0,
            latest_blood_pressure_diastolic=0,
            latest_bmi=0.0,
            latest_cholesterol_total=0.0,
            latest_hba1c=0.0,
            latest_fasting_blood_sugar=0.0,
        )

        # Add the patient record to the session and commit to get the patient_id
        db.session.add(new_patient)
        db.session.commit()  # Patient gets its patient_id assigned now

        # Generate the username using the patient's last name and patient_id
        username = f"{last_name[:3].lower()}{new_patient.patient_id}"

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "Username already exists"}), 400

        # Now, create the user and link it to the patient
        new_user = User(username=username, password=password)  # Plain-text password passed here
        new_user.patient_id = new_patient.patient_id  # Link patient_id to the user

        # Try to save the user record to the database
        try:
            db.session.add(new_user)
            db.session.commit()

            # Print the key details of the new user and patient
            print(f"[INFO] New User Registered: User ID: {new_user.id}, Username: {new_user.username}, Patient ID: {new_patient.patient_id}, "
                  f"First Name: {new_patient.first_name}, Last Name: {new_patient.last_name}, Age: {new_patient.age}, "
                  f"Gender: {new_patient.gender}, Ethnicity: {new_patient.ethnicity}, Diagnosis: {new_patient.diagnosis}, "
                  f"Smoking: {new_patient.smoking}, Family History of Diabetes: {new_patient.family_history_diabetes}")

            login_user(new_user)  # Log the user in after registration

            # Return success message with the logged-in username
            return jsonify({
                "success": True,
                "message": "Registration successful. User logged in.",
                "username": new_user.username
            })

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            print(f"[ERROR] {str(e)}")
            return jsonify({"success": False, "message": "An error occurred during registration"}), 500

    # If the request is not JSON, return an error
    return jsonify({"success": False, "message": "Invalid request"}), 400

# Route for logging in an existing user
@auth_bp.route('/api/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Plain-text password from the request

        print(f"[DEBUG] Attempting login for username: {username}")

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            print(f"[DEBUG] Found user: {user.username}")

        # Check if the user exists and if the password matches
        if user and check_password_hash(user.password_hash, password):
            print(f"[DEBUG] Login successful for user: {user.username}")
            login_user(user)  # Log the user in after successful authentication
            return jsonify({"success": True, "message": "Login successful", "username": user.username})

        # If credentials are invalid, return an error
        print(f"[DEBUG] Invalid credentials provided.")
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    # If the request is not JSON, return an error
    return jsonify({"success": False, "message": "Invalid request"}), 400
