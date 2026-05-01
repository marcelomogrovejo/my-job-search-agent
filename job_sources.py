import requests
from bs4 import BeautifulSoup

ITVIEC_HEADERS = {
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
    if "mobile" in lowered and not any(kw in lowered for kw in NON_IOS_KEYWORDS):
        return True
    return False


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


def parse_itviec_cards(soup):
    jobs = []
    cards = soup.find_all("div", class_=lambda c: c and "job-card" in c)

    for card in cards:
        title_tag = card.find("h3")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        if not is_ios_relevant(title):
            continue

        slug = card.get("data-search--job-selection-job-slug-value", "")
        job_url = f"https://itviec.com/it-jobs/{slug}" if slug else ""

        company = "Unknown"
        company_links = card.find_all("a", href=lambda h: h and "/companies/" in h)
        for link in company_links:
            text = link.get_text(strip=True)
            if text:
                company = text
                break

        skills = []
        skill_links = card.find_all("a", href=lambda h: h and "click_source=Skill" in str(h))
        for link in skill_links:
            skills.append(link.get_text(strip=True))

        jobs.append({
            "title": title,
            "company": company,
            "location": "Vietnam",
            "url": job_url,
            "description": " ".join(skills),
            "source": "ITviec",
        })

    return jobs


def fetch_itviec_jobs():
    print("Fetching ITviec jobs...")

    urls = [
        "https://itviec.com/it-jobs/ios-developer",
        "https://itviec.com/it-jobs/ios",
        "https://itviec.com/it-jobs/swift",
    ]

    jobs = []

    for url in urls:
        response = requests.get(url, headers=ITVIEC_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_itviec_cards(soup)
        print(f"  {url}: {len(page_jobs)} iOS jobs found")
        jobs.extend(page_jobs)

    return deduplicate_jobs(jobs)


def deduplicate_jobs(jobs):
    seen = set()
    unique = []

    for job in jobs:
        key = (
            job.get("title", "").lower().strip(),
            job.get("company", "").lower().strip(),
            job.get("url", "").lower().strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(job)

    return unique


def fetch_all_jobs():
    jobs = []

    try:
        print("Fetching RemoteOK jobs...")
        jobs.extend(fetch_remoteok_jobs())
    except Exception as error:
        print(f"RemoteOK source failed: {error}")

    try:
        print("Fetching ITviec jobs...")
        jobs.extend(fetch_itviec_jobs())
    except Exception as error:
        print(f"ITviec source failed: {error}")

    return deduplicate_jobs(jobs)