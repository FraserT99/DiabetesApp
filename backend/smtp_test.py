import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    print("Connected successfully to Gmail SMTP on port 587.")
    server.quit()
except Exception as e:
    print(f"Connection failed: {e}")
