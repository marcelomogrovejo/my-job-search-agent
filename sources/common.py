import requests
from bs4 import BeautifulSoup

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

IOS_KEYWORDS = {"ios", "swift", "swiftui", "uikit", "objective-c", "obj-c"}

NON_IOS_KEYWORDS = {
    "flutter", "react native", "android developer", "senior android",
    "fullstack", "full stack", "full-stack", "backend", "back-end",
    "front-end", "frontend", "devops", "data engineer", "data scientist",
    "qa engineer", "tester", "golang", "java developer", ".net",
    "python developer", "php developer", "ruby", "node.js", "nodejs",
    "angular", "vue.js", "react developer",
}


def is_ios_relevant(title):
    lowered = title.lower()
    if any(kw in lowered for kw in NON_IOS_KEYWORDS):
        return False
    if any(kw in lowered for kw in IOS_KEYWORDS):
        return True
    if "mobile" in lowered:
        return True
    return False


def deduplicate_jobs(jobs):
    seen = set()
    unique = []
    for job in jobs:
        key = (
            job.get("title", "").lower().strip(),
            job.get("company", "").lower().strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return unique
