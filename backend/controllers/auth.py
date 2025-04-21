from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from models import db
from models.user import User
from models.patient import Patient
from services.notifications import send_username_email, send_username_sms
import re
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    data = request.get_json()

    #Extract fields 
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()
    phone_number = data.get("phone_number", "").strip()
    age = data.get("age")
    gender = data.get("gender")
    ethnicity = data.get("ethnicity")
    diagnosis = data.get("diagnosis")
    smoking = data.get("smoking", False)
    family_history_diabetes = data.get("family_history_diabetes", False)

    #Validate presence of required fields 
    required_fields = [first_name, last_name, password, email, phone_number, age, gender, ethnicity, diagnosis]
    if any(field in [None, ""] for field in required_fields):
        return jsonify({"success": False, "message": "All fields are required."}), 400

    #Field validations 
    name_regex = re.compile(r"^[A-Za-z]{2,50}$")
    if not name_regex.match(first_name):
        return jsonify({"success": False, "message": "First name must contain only letters (2–50 characters)."}), 400

    if not name_regex.match(last_name):
        return jsonify({"success": False, "message": "Last name must contain only letters (2–50 characters)."}), 400

    password_regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$")
    if not password_regex.match(password):
        return jsonify({"success": False, "message": "Password must be 8–20 characters with at least one letter and one number."}), 400

    email_regex = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
    if not email_regex.match(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400

    phone_regex = re.compile(r'^\+?\d{10,15}$')
    if not phone_regex.match(phone_number):
        return jsonify({"success": False, "message": "Invalid phone number format. Must be 10–15 digits."}), 400

    try:
        age = int(age)
        if age < 18 or age > 120:
            return jsonify({"success": False, "message": "Age must be between 18 and 120."}), 400
    except ValueError:
        return jsonify({"success": False, "message": "Age must be a valid number."}), 400

    #Check for duplicate email 
    if Patient.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already registered."}), 400

    #Hash password 
    hashed_password = generate_password_hash(password)

    #Create Patient record 
    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        diagnosis=diagnosis,
        ethnicity=ethnicity,
        smoking=smoking,
        family_history_diabetes=family_history_diabetes,
        email=email,
        phone_number=phone_number,
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

    db.session.add(new_patient)
    db.session.commit()

    #Generate username 
    username = f"{last_name[:3].lower()}{new_patient.patient_id}"
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already exists."}), 400

    new_user = User(username=username, password=hashed_password)
    new_user.patient_id = new_patient.patient_id

    try:
        db.session.add(new_user)
        db.session.commit()

        print(f"[INFO] New User Registered: Username: {username}, Email: {email}, Phone: {phone_number}")
        login_user(new_user)

        #Notify 
        if email:
            send_username_email(email, username)
        if phone_number:
            send_username_sms(phone_number, username)

        return jsonify({
            "success": True,
            "message": "Registration successful. User logged in.",
            "username": username
        })

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Registration failed: {str(e)}")
        return jsonify({"success": False, "message": f"An error occurred during registration: {str(e)}"}), 500

#Route for logging in an existing user
@auth_bp.route('/api/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  #Plain-text password from the request

        print(f"[DEBUG] Attempting login for username: {username}")

        #Check if the user exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            print(f"[DEBUG] Found user: {user.username}")

        #Validate the user credentials
        if user and check_password_hash(user.password_hash, password):
            print(f"[DEBUG] Login successful for user: {user.username}")
            login_user(user)  #Log the user in after successful authentication

            #Update last_login timestamp
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            #Refresh challenge progress after login
            from services.challenge_service import refresh_all_challenge_progress
            refresh_all_challenge_progress(user.username)
            print(f"[CHALLENGES] Refreshed challenge progress for: {user.username}")

            return jsonify({
                "success": True,
                "message": "Login successful",
                "username": user.username
            })

        #If credentials are invalid, return an error
        print(f"[DEBUG] Invalid credentials provided.")
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    #If the request is not JSON, return an error
    return jsonify({"success": False, "message": "Invalid request"}), 400
