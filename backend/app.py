#Imports
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from models import db
from controllers.auth import auth_bp
from services.data_loader import load_data_from_csv
from controllers.dashboard import create_dashboard  
from dotenv import load_dotenv
from services.notifications import (
    init_mail,
    send_inactive_user_email,
    send_goal_nudge_email,
    send_challenge_reminder_email,
    send_challenge_reminder_sms,
    send_goal_nudge_sms
)
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone

from services.user_service import fetch_user_data
from services.challenge_service import fetch_challenges, fetch_patient_progress
from services.goal_utils import calculate_goal_progress
from models.user import User

#Loading enviroment variables
load_dotenv()

#Initialising flask app
app = Flask(__name__)
app.config.from_object(Config)

#Initialising mail
init_mail(app)

#Intialising db and login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

#Enabling CORS for frontend
CORS(app, origins=["http://localhost:3000"])

#Registering API routes
app.register_blueprint(auth_bp)

#Flask-Login: Load user
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

#Scheduled jobs

def check_inactive_users():
    print("[SCHEDULER] Running inactivity check...")
    with app.app_context():
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        users = User.query.all()
        emailed_count = 0

        for user in users:
            if user.last_login and user.last_login < seven_days_ago:
                patient = user.patient
                if patient and patient.email and patient.email_alerts:
                    send_inactive_user_email(patient.email, user.username, 7)
                    print(f"[INACTIVE] Emailed: {user.username}")
                    emailed_count += 1

        print(f"[SUMMARY] Total inactive users emailed: {emailed_count}")

def check_challenge_reminders():
    print("[SCHEDULER] Checking challenge progress...")
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not user.patient:
                continue
            email = user.patient.email
            phone = user.patient.phone_number
            if not (email or phone):
                continue

            challenges = fetch_challenges()
            for ch in challenges:
                progress = fetch_patient_progress(user.username, ch["id"])
                percent = round((progress / ch["goal"]) * 100) if ch["goal"] > 0 else 0

                if percent < 100 and percent >= 75:
                    if user.patient.email_alerts:
                        send_challenge_reminder_email(email, user.username, ch["name"], percent)
                    if user.patient.sms_alerts:
                        send_challenge_reminder_sms(phone, ch["name"], percent)

def check_goal_proximity():
    print("[SCHEDULER] Checking goal proximity...")
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not user.patient:
                continue
            email = user.patient.email
            phone = user.patient.phone_number
            if not (email or phone):
                continue

            user_data = fetch_user_data(user.username)
            for metric, value in user_data.items():
                if metric.startswith("latest_") and isinstance(value, (int, float)):
                    start, end, x_data, y_data, progress = calculate_goal_progress(user.username, metric, "daily")
                    if progress >= 80 and progress < 100:
                        label = metric.replace("latest_", "").replace("_", " ").title()
                        if user.patient.email_alerts:
                            send_goal_nudge_email(email, user.username, label, int(progress))
                        if user.patient.sms_alerts:
                            send_goal_nudge_sms(phone, label, int(progress))

#Inital db and data set up
def initialise_app():
    print("[INFO] Initialising database and loading data from CSV...")
    db.create_all()
    load_data_from_csv()

    #Starting background job for inactivity
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_inactive_users, 'interval', days=1)
    scheduler.add_job(check_challenge_reminders, 'interval', hours=6)
    scheduler.add_job(check_goal_proximity, 'interval', hours=6)
    scheduler.start()
    print("[INFO] Scheduler started with user reminders.")


with app.app_context():
    initialise_app()

#Attaching Dash app
create_dashboard(app)

#Running Flask server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)