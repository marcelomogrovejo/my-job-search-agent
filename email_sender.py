import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


def send_email(subject, body):
    load_dotenv()
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_APP_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not email_user or not email_password or not email_to:
        print("Email credentials not set — printing summary instead.\n")
        print(f"Subject: {subject}\n")
        print(body)
        return

    message = MIMEText(body, "html")
    message["Subject"] = subject
    message["From"] = email_user
    message["To"] = email_to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_password)
        server.send_message(message)

    print("Email sent successfully.")
