from config import REQUIRED_KEYWORDS, PREFERRED_KEYWORDS, EXCLUDED_KEYWORDS, LOCATION_PRIORITY


def detect_location_group(job):
    text = " ".join([
        job.get("title", ""),
        job.get("company", ""),
        job.get("location", ""),
        job.get("description", ""),
    ]).lower()

    # Vietnam cities (English and Vietnamese spellings)
    if any(keyword in text for keyword in [
        "vietnam",
        "ho chi minh",
        "hồ chí minh",
        "hanoi",
        "ha noi",
        "hà nội",
        "da nang",
        "danang",
        "đà nẵng",
    ]):
        return "vietnam"

    # Japan
    if any(keyword in text for keyword in [
        "japan",
        "tokyo",
        "osaka"
    ]):
        return "japan"

    # Thailand
    if any(keyword in text for keyword in [
        "thailand",
        "bangkok"
    ]):
        return "thailand"

    # Australia
    if any(keyword in text for keyword in [
        "australia",
        "sydney",
        "melbourne",
        "perth"
    ]):
        return "australia"

    # Remote / fallback
    if any(keyword in text for keyword in [
        "remote",
        "worldwide",
        "anywhere"
    ]):
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