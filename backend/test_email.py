from flask import Flask
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER"),
)

mail = Mail(app)

with app.app_context():
    try:
        msg = Message(subject="Test Email",
                      recipients=["frasertxyz@hotmail.co.uk"],
                      body="This is a test email from Flask!")
        mail.send(msg)
        print("Test email sent successfully.")
    except Exception as e:
        print(f"Failed to send: {e}")
