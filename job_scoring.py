from config import REQUIRED_KEYWORDS, PREFERRED_KEYWORDS, EXCLUDED_KEYWORDS, LOCATION_PRIORITY


def detect_location_group(job):
    text = " ".join([
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", ""),
    ]).lower()

    if "vietnam" in text or "ho chi minh" in text or "hanoi" in text:
        return "vietnam"

    if "japan" in text or "tokyo" in text or "osaka" in text:
        return "japan"

    if "thailand" in text or "bangkok" in text:
        return "thailand"

    if "australia" in text or "sydney" in text or "melbourne" in text or "perth" in text:
        return "australia"

    if "remote" in text or "worldwide" in text or "anywhere" in text:
        return "international"

    return "international"


def score_job(job):
    text = " ".join([
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", ""),
    ]).lower()

    if any(excluded in text for excluded in EXCLUDED_KEYWORDS):
        return None

    if not all(required in text for required in REQUIRED_KEYWORDS):
        return None

    relevance_score = 50

    for keyword in PREFERRED_KEYWORDS:
        if keyword.lower() in text:
            relevance_score += 10

    location_group = detect_location_group(job)
    location_score = LOCATION_PRIORITY.get(location_group, 0)

    job["location_group"] = location_group
    job["relevance_score"] = relevance_score
    job["location_score"] = location_score
    job["final_score"] = relevance_score + location_score

    return job