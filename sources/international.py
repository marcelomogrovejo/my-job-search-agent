import requests
from sources.common import BROWSER_HEADERS, is_ios_relevant


# --- RemoteOK ---

def fetch_remoteok_jobs():
    print("Fetching RemoteOK jobs...")
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    jobs = []

    for item in response.json():
        if not isinstance(item, dict) or "position" not in item:
            continue

        if not is_ios_relevant(item.get("position", "")):
            continue

        jobs.append({
            "title": item.get("position", ""),
            "company": item.get("company", ""),
            "location": item.get("location", "Remote"),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "source": "RemoteOK",
            "posted": "",
            "salary": "",
        })

    return jobs


# --- Region definition ---

REGION = {
    "sources": [
        {"fetch": fetch_remoteok_jobs, "name": "RemoteOK", "color": "#555"},
    ],
}
