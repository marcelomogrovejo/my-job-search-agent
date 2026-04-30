import os
import smtplib
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv
from config import REQUIRED_KEYWORDS, PREFERRED_KEYWORDS, EXCLUDED_KEYWORDS

load_dotenv()


def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()

    jobs = []
    for item in data:
        if not isinstance(item, dict) or "position" not in item:
            continue

        jobs.append({
            "title": item.get("position", ""),
            "company": item.get("company", ""),
            "location": item.get("location", "Remote"),
            "url": item.get("url", ""),
            "description": item.get("description", "")
        })

    return jobs


def score_job(job):
    text = " ".join([
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", "")
    ]).lower()

    if any(excluded in text for excluded in EXCLUDED_KEYWORDS):
        return 0

    if not all(required in text for required in REQUIRED_KEYWORDS):
        return 0

    score = 50

    for keyword in PREFERRED_KEYWORDS:
        if keyword.lower() in text:
            score += 10

    return score


def build_summary(jobs):
    ranked = sorted(jobs, key=lambda job: job["score"], reverse=True)
    ranked = [job for job in ranked if job["score"] > 0][:10]

    if not ranked:
        return "No strong iOS matches found today."

    lines = ["Top iOS job matches today:\n"]

    for index, job in enumerate(ranked, start=1):
        lines.append(
            f"{index}. {job['title']} - {job['company']}\n"
            f"Location: {job['location']}\n"
            f"Score: {job['score']}\n"
            f"Link: {job['url']}\n"
        )

    return "\n".join(lines)


def send_email(subject, body):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_APP_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not email_user or not email_password or not email_to:
        raise ValueError("Missing email configuration in .env")

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = email_user
    message["To"] = email_to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_password)
        server.send_message(message)


def main():
    jobs = fetch_remoteok_jobs()

    scored_jobs = []
    for job in jobs:
        score = score_job(job)
        if score > 0:
            job["score"] = score
            scored_jobs.append(job)

    summary = build_summary(scored_jobs)
    send_email("Daily iOS Job Matches", summary)


if __name__ == "__main__":
    main()