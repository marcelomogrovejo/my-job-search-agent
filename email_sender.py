import os
import smtplib
from email.mime.text import MIMEText


def send_email(subject, body):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_APP_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not email_user or not email_password or not email_to:
        raise ValueError("Missing email configuration in GitHub Secrets")

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = email_user
    message["To"] = email_to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_password)
        server.send_message(message)