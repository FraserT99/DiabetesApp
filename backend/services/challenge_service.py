from models.challenge import Challenge
from models.user import User
from models.patient import Patient
from models.patientChallenge import PatientChallenge
from models import db
from datetime import datetime

from models.health_history import HealthHistory
from services.user_service import update_user_points, fetch_user_points
from datetime import datetime, timedelta
from sqlalchemy import func

from pytz import timezone, UTC

UK_TZ = timezone("Europe/London")  #Define local timezone

def get_cumulative_metric(patient_id, metric_name, period='daily'):
    """
    Fetch cumulative metric (e.g., steps, calories burned, weight loss, etc.) for a given period.
    Handles UK timezone to align challenge periods correctly.
    """

    now_uk = datetime.now(UK_TZ)
    today = now_uk.replace(hour=0, minute=0, second=0, microsecond=0)

    if period == 'daily':
        start_date = today
        end_date = start_date + timedelta(days=1)
    elif period == 'weekly':
        start_date = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=7)
    elif period == 'monthly':
        start_date = today.replace(day=1)
        next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_date = next_month
    else:
        raise ValueError(f"Invalid period: {period}. Valid options: 'daily', 'weekly', 'monthly'.")

    #Convert to UTC to match DB timestamps
    start_date_utc = start_date.astimezone(UTC)
    end_date_utc = end_date.astimezone(UTC)

    if metric_name == "latest_weight":
        weight_records = (
            HealthHistory.query.filter(
                HealthHistory.patient_id == patient_id,
                HealthHistory.metric_name == metric_name,
                HealthHistory.recorded_at >= start_date_utc,
                HealthHistory.recorded_at < end_date_utc
            )
            .order_by(HealthHistory.recorded_at.asc())
            .all()
        )

        if weight_records:
            start_weight = weight_records[0].value
            latest_weight = weight_records[-1].value
            weight_loss = max(0, start_weight - latest_weight)
            return weight_loss

        return 0

    #Sum other metrics in the window
    cumulative_value = db.session.query(func.sum(HealthHistory.value)).filter(
        HealthHistory.patient_id == patient_id,
        HealthHistory.metric_name == metric_name,
        HealthHistory.recorded_at >= start_date_utc,
        HealthHistory.recorded_at < end_date_utc
    ).scalar() or 0

    return cumulative_value


def fetch_challenges():
    """Fetch all challenges from the database."""
    try:
        challenges = Challenge.query.all()
        print(f"[DEBUG] Found {len(challenges)} challenges in DB.")  #Debugging log

        return [{
            "id": ch.id,
            "name": ch.name,
            "description": ch.description,
            "goal": ch.goal,
            "challenge_type": ch.challenge_type,
            "reward_points": ch.reward_points  #Include points to be earned
        } for ch in challenges]

    except Exception as e:
        print(f"[ERROR] Failed to fetch challenges: {e}")
        return []

def fetch_patient_progress(username, challenge_id):
    """
    Fetch the patient's challenge progress and check if it's completed.
    """
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"[ERROR] User {username} not found.")
            return 0

        patient = Patient.query.filter_by(patient_id=user.patient_id).first()
        if not patient:
            print(f"[ERROR] No patient record for user {username}.")
            return 0

        patient_challenge = PatientChallenge.query.filter_by(
            patient_id=patient.patient_id,
            challenge_id=challenge_id
        ).first()

        challenge = Challenge.query.filter_by(id=challenge_id).first()
        if not challenge:
            print(f"[ERROR] Challenge ID {challenge_id} not found.")
            return 0

        #Map to health metric and calculate progress
        metric_name = challenge_to_metric(challenge.name)
        period = challenge.challenge_type
        progress = get_cumulative_metric(patient.patient_id, metric_name, period)

        if not patient_challenge and progress >= challenge.goal:
            #Mark challenge as completed (one-time creation)
            new_challenge = PatientChallenge(
                patient_id=patient.patient_id,
                challenge_id=challenge_id,
                progress=progress,
                completed=True
            )
            db.session.add(new_challenge)
            db.session.commit()

        return progress

    except Exception as e:
        print(f"[ERROR] Failed to fetch patient progress dynamically: {e}")
        return 0

def update_challenge_progress(username, challenge_id, amount=0, suppress_completion_logs=False):
    """Updates a user's challenge progress based on their logged activity and awards points if completed."""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"[ERROR] User {username} not found.")
            return False

        patient = Patient.query.filter_by(patient_id=user.patient_id).first()
        if not patient:
            print(f"[ERROR] No patient record for user {username}.")
            return False

        patient_challenge = PatientChallenge.query.filter_by(
            patient_id=patient.patient_id,
            challenge_id=challenge_id
        ).first()

        challenge = Challenge.query.filter_by(id=challenge_id).first()
        if not challenge:
            print(f"[ERROR] Challenge ID {challenge_id} not found.")
            return False

        metric_name = challenge_to_metric(challenge.name)
        if not metric_name:
            print(f"[ERROR] No metric mapping found for challenge: {challenge.name}")
            return False

        period = challenge.challenge_type
        new_progress = get_cumulative_metric(patient.patient_id, metric_name, period)

        if not patient_challenge:
            if not suppress_completion_logs:
                print(f"[INFO] Creating new challenge progress for {username} on challenge '{challenge.name}'.")
            patient_challenge = PatientChallenge(
                patient_id=patient.patient_id,
                challenge_id=challenge_id,
                progress=0,
                completed=False
            )
            db.session.add(patient_challenge)

        previous_progress = patient_challenge.progress
        patient_challenge.progress = min(new_progress, challenge.goal)

        if patient_challenge.progress >= challenge.goal and not patient_challenge.completed:
            patient_challenge.completed = True

            current_points = fetch_user_points(username)
            new_total = current_points + challenge.reward_points
            update_user_points(username, new_total)

            if not suppress_completion_logs:
                print(f"\n[🎉 CHALLENGE COMPLETED] {username} has completed '{challenge.name}'!")
                print(f"[🏆 POINTS AWARDED] {username} earned {challenge.reward_points} points!")
                print(f"[💰 TOTAL POINTS] {username} now has {new_total} points!\n")

        elif patient_challenge.completed:
            if not suppress_completion_logs:
                print(f"[✅ CHALLENGE ALREADY COMPLETED] {username} had already completed '{challenge.name}'. Skipping points reallocation.")

        if previous_progress != patient_challenge.progress:
            print(f"[UPDATE] {username}'s challenge '{challenge.name}' progress: {previous_progress} → {patient_challenge.progress}/{challenge.goal}")

        db.session.commit()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to update challenge progress: {e}")
        return False
        
def challenge_to_metric(challenge_name):
    """
    Maps a challenge name to the corresponding health history metric.
    Only includes mappings for seeded challenges.
    """
    mapping = {
        #Daily Challenges
        "Daily Steps": "latest_steps_taken",
        "Daily Calories Burned": "latest_calories_burned",
        "Daily Active Time": "latest_active_minutes",
        "Daily Hydration": "latest_water_intake",

        #Weekly Challenges
        "Weekly Steps": "latest_steps_taken",
        "Weekly Calories Burned": "latest_calories_burned",
        "Weekly Distance Walked": "latest_distance_walked",
        "Weekly Running Distance": "latest_distance_ran",

        #Monthly Challenges
        "Monthly Steps": "latest_steps_taken",
        "Monthly Calories Burned": "latest_calories_burned",
        "Monthly Weight Loss": "latest_weight",
        "Monthly Fiber Intake": "latest_fiber_intake"
    }

    return mapping.get(challenge_name, None)  #Returns None if the challenge isn't found

def refresh_all_challenge_progress(username):
    """
    Recalculates all challenge progress for the user.
    Useful for login or first-time session loads.
    """
    challenges = fetch_challenges()  #Returns list of all defined challenges
    for challenge in challenges:
        update_challenge_progress(
            username=username,
            challenge_id=challenge["id"],
            amount=0,  
            suppress_completion_logs=True  #Prevent duplicate console logs
        )

def get_nearly_completed_challenges(username, top_n=3):
    """
    Returns up to `top_n` incomplete challenges with the highest progress % for a user.
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return []

    patient_id = user.patient.patient_id

    #Join PatientChallenge with Challenge to get details
    records = (
        db.session.query(PatientChallenge, Challenge)
        .join(Challenge, PatientChallenge.challenge_id == Challenge.id)
        .filter(PatientChallenge.patient_id == patient_id)
        .filter(PatientChallenge.completed == False)
        .order_by((PatientChallenge.progress / Challenge.goal).desc())  
        .limit(top_n)
        .all()
    )

    return [
        {
            "name": challenge.name,
            "description": challenge.description,
            "progress": round(pc.progress, 2),
            "goal": challenge.goal,
            "type": challenge.challenge_type
        }
        for pc, challenge in records
    ]

