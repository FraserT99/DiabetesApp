#Imports 
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from twilio.rest import Client

#Environment Setup 
load_dotenv()


#Flask-Mail Configuration


mail = Mail()

def init_mail(app):
    """
    Initializes Flask-Mail using environment variables from .env.
    """
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True") == "True",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER"),
    )
    mail.init_app(app)
    mail.debug = 0

#Email Notifications 

def send_username_email(email, username):
    try:
        msg = Message(
            subject="🎉 Welcome to GlucoTrack!",
            recipients=[email],
            body=(
                f"Hi {username},\n\n"
                f"Thank you for registering with GlucoTrack!\n\n"
                f"Your username is: {username}\n\n"
                f"Take charge of your health today.\n\n"
                f"Best,\nThe GlucoTrack Team"
            )
        )
        mail.send(msg)
        print(f"[EMAIL SENT] to {email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

def send_inactive_user_email(email, username, days_inactive):
    try:
        msg = Message(
            subject="👋 We Miss You at GlucoTrack!",
            recipients=[email],
            body=(
                f"Hi {username},\n\n"
                f"We haven't seen you in {days_inactive} days. Come back and log your progress!\n\n"
                f"Stay consistent for your health goals.\n\n"
                f"- GlucoTrack Team"
            )
        )
        mail.send(msg)
        print(f"[REMINDER EMAIL SENT] to {email}")
    except Exception as e:
        print(f"[REMINDER EMAIL ERROR] {e}")

def send_goal_nudge_email(email, username, metric, progress):
    try:
        msg = Message(
            subject="🌟 Almost There!",
            recipients=[email],
            body=(
                f"Hey {username},\n\n"
                f"You're {progress}% of the way to your {metric} goal.\n\n"
                f"Don't stop now — you're so close!\n\n"
                f"You've got this,\nThe GlucoTrack Team"
            )
        )
        mail.send(msg)
        print(f"[GOAL NUDGE EMAIL SENT] to {email}")
    except Exception as e:
        print(f"[GOAL EMAIL ERROR] {e}")

def send_challenge_reminder_email(email, username, challenge_name, progress):
    try:
        msg = Message(
            subject="⏳ Challenge Ending Soon!",
            recipients=[email],
            body=(
                f"Hi {username},\n\n"
                f"Your challenge \"{challenge_name}\" is ending soon and you're at {progress}% progress.\n\n"
                f"You can still complete it — give it one last push!\n\n"
                f"- GlucoTrack Team"
            )
        )
        mail.send(msg)
        print(f"[CHALLENGE EMAIL SENT] to {email}")
    except Exception as e:
        print(f"[CHALLENGE EMAIL ERROR] {e}")



#Twilio SMS Configuration


twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

def send_username_sms(phone, username):
    try:
        message = twilio_client.messages.create(
            body=f"👋 Welcome to GlucoTrack! Your username is: {username}",
            from_=twilio_number,
            to=phone
        )
        print(f"[SMS SENT] SID: {message.sid}")
    except Exception as e:
        print(f"[SMS ERROR] {e}")

def send_goal_nudge_sms(phone, metric, progress):
    try:
        message = twilio_client.messages.create(
            body=f"🔥 You're {progress}% toward your {metric} goal. Keep going!",
            from_=twilio_number,
            to=phone
        )
        print(f"[GOAL SMS SENT] SID: {message.sid}")
    except Exception as e:
        print(f"[GOAL SMS ERROR] {e}")

def send_challenge_reminder_sms(phone, challenge_name, progress):
    try:
        message = twilio_client.messages.create(
            body=f"⏳ Your challenge \"{challenge_name}\" is almost over! You're at {progress}%. Push to finish strong!",
            from_=twilio_number,
            to=phone
        )
        print(f"[CHALLENGE SMS SENT] SID: {message.sid}")
    except Exception as e:
        print(f"[CHALLENGE SMS ERROR] {e}")
