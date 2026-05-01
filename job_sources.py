import html
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
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_itviec_cards(soup)
        print(f"  {url}: {len(page_jobs)} iOS jobs found")
        jobs.extend(page_jobs)

    return deduplicate_jobs(jobs)


def parse_topdev_cards(soup):
    jobs = []

    title_links = soup.find_all(
        "a", href=lambda h: h and "/detail-jobs/" in h
    )

    for title_link in title_links:
        title = title_link.get_text(strip=True)
        if not title or not is_ios_relevant(title):
            continue

        href = title_link.get("href", "")
        job_url = f"https://topdev.vn{href}" if href.startswith("/") else href

        # Walk up to the card container
        card = title_link
        for _ in range(10):
            card = card.parent
            classes = " ".join(card.get("class", []))
            if "shadow" in classes:
                break

        company = "Unknown"
        company_span = card.find(
            "span",
            class_=lambda c: c and "text-text-500" in c and "font-medium" in c,
        )
        if company_span:
            company = company_span.get_text(strip=True)

        location = "Vietnam"
        grid = card.find("div", class_=lambda c: c and "grid" in c and "grid-cols-2" in c)
        if grid:
            loc_span = grid.find("span", class_="line-clamp-1")
            if loc_span:
                loc_text = loc_span.get_text(strip=True)
                location = f"{loc_text}, Vietnam" if loc_text.lower() == "remote" else loc_text

        skills = []
        skill_links = card.find_all(
            "a", href=lambda h: h and "/jobs/search?keyword=" in h
        )
        for link in skill_links:
            skills.append(link.get_text(strip=True))

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": job_url,
            "description": " ".join(skills),
            "source": "TopDev",
        })

    return jobs


def fetch_topdev_jobs():
    print("Fetching TopDev jobs...")

    urls = [
        "https://topdev.vn/jobs/search?keyword=ios",
        "https://topdev.vn/jobs/search?keyword=swift+developer",
    ]

    jobs = []

    for url in urls:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_topdev_cards(soup)
        print(f"  {url}: {len(page_jobs)} iOS jobs found")
        jobs.extend(page_jobs)

    return deduplicate_jobs(jobs)


def parse_vietnamdevs_cards(soup):
    jobs = []
    cards = soup.find_all("div", class_=lambda c: c and "card-hoverable" in c)

    for card in cards:
        h2 = card.find("h2")
        if not h2:
            continue

        link = h2.find("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        if not is_ios_relevant(title):
            continue

        job_url = link.get("href", "")

        company = "Unknown"
        img = card.find("img", alt=True)
        if img:
            alt = html.unescape(img.get("alt", ""))
            if alt.endswith("'s logo"):
                company = alt[:-7]

        location = "Vietnam"
        loc_p = card.find("p", class_=lambda c: c and "text-gray-500" in c)
        if loc_p:
            location = loc_p.get_text(strip=True)

        skills = [li.get_text(strip=True) for li in card.find_all("li", class_="gray-label")]

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": job_url,
            "description": " ".join(skills),
            "source": "VietnamDevs",
        })

    return jobs


def fetch_vietnamdevs_jobs():
    print("Fetching VietnamDevs jobs...")

    urls = [
        "https://vietnamdevs.com/jobs/swift",
        "https://vietnamdevs.com/jobs/mobile-engineer",
        "https://vietnamdevs.com/jobs/object-c",
    ]

    jobs = []

    for url in urls:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_vietnamdevs_cards(soup)
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

    try:
        jobs.extend(fetch_topdev_jobs())
    except Exception as error:
        print(f"TopDev source failed: {error}")

    try:
        jobs.extend(fetch_vietnamdevs_jobs())
    except Exception as error:
        print(f"VietnamDevs source failed: {error}")

    return deduplicate_jobs(jobs)