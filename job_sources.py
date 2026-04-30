import requests


def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    jobs = []

    for item in response.json():
        if not isinstance(item, dict) or "position" not in item:
            continue

        jobs.append({
            "title": item.get("position", ""),
            "company": item.get("company", ""),
            "location": item.get("location", "Remote"),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "source": "RemoteOK",
        })

    return jobs


def fetch_all_jobs():
    jobs = []
    jobs.extend(fetch_remoteok_jobs())
    return jobs