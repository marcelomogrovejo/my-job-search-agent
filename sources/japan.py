import re
import requests
from bs4 import BeautifulSoup
from sources.common import BROWSER_HEADERS, is_ios_relevant, deduplicate_jobs


# --- TokyoDev ---

def parse_tokyodev_jobs(soup):
    jobs = []

    job_headings = soup.find_all("h4", class_=lambda c: c and "font-bold" in c)

    for h4 in job_headings:
        link = h4.find("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        if not is_ios_relevant(title):
            continue

        href = link.get("href", "")
        job_url = f"https://www.tokyodev.com{href}" if href.startswith("/") else href

        # Walk up to the company <li> container to find the company name
        container = h4
        for _ in range(10):
            container = container.parent
            if container is None or container.name == "li":
                break

        company = "Unknown"
        if container and container.name == "li":
            h3 = container.find("h3")
            if h3:
                comp_link = h3.find("a")
                if comp_link:
                    company = comp_link.get_text(strip=True)

        # Parse tags from the sibling div (salary, skills, remote policy)
        tags_div = h4.find_next_sibling("div")
        salary = ""
        skills = []
        location = "Japan"

        if tags_div:
            for tag in tags_div.find_all("a", class_=lambda c: c and "tag" in c):
                tag_text = tag.get_text(strip=True)
                tag_href = tag.get("href", "")
                tag_classes = " ".join(tag.get("class", []))

                if "tag-primary" in tag_classes:
                    salary = tag_text
                elif "tag-emerald" in tag_classes:
                    if "fully-remote" in tag_href:
                        location = "Remote, Japan"
                elif "tag-muted" in tag_classes:
                    if "japanese" not in tag_href:
                        skills.append(tag_text)

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": job_url,
            "description": " ".join(skills),
            "source": "TokyoDev",
            "posted": "",
            "salary": salary,
        })

    return jobs


def fetch_tokyodev_jobs():
    print("Fetching TokyoDev jobs...")

    urls = [
        "https://www.tokyodev.com/jobs?category%5B%5D=ios",
        "https://www.tokyodev.com/jobs?query%5B%5D=swift",
        "https://www.tokyodev.com/jobs?query%5B%5D=mobile",
    ]

    jobs = []

    for url in urls:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_tokyodev_jobs(soup)
        print(f"  {url}: {len(page_jobs)} iOS jobs found")
        jobs.extend(page_jobs)

    return deduplicate_jobs(jobs)


# --- Forkwell ---

def parse_forkwell_jobs(soup):
    jobs = []

    # Find job links matching /company-slug/jobs/numeric-id
    job_links = soup.find_all(
        "a", href=lambda h: h and re.match(r"/[^/]+/jobs/\d+", h)
    )

    seen_urls = set()

    for link in job_links:
        href = link.get("href", "")
        full_url = f"https://jobs.forkwell.com{href}"
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        # Title is in h2 or h3 inside the link, or the link text itself
        title_el = link.find(["h2", "h3"])
        if title_el:
            title = title_el.get_text(strip=True)
        else:
            title = link.get_text(strip=True)

        if not title or not is_ios_relevant(title):
            continue

        # Walk up to the card container (li)
        card = link
        for _ in range(10):
            card = card.parent
            if card is None or card.name == "li":
                break

        if card is None:
            continue

        # Company name from links to /company-slug (without /jobs/)
        company = "Unknown"
        company_links = card.find_all(
            "a", href=lambda h: h and re.match(r"^/[^/]+$", h)
        )
        for cl in company_links:
            text = cl.get_text(strip=True)
            if text and text != title:
                company = text
                break

        # Skills from links to /t/tag
        skills = []
        skill_links = card.find_all("a", href=lambda h: h and h.startswith("/t/"))
        for sl in skill_links:
            skills.append(sl.get_text(strip=True))

        # Salary in Japanese yen format
        salary = ""
        card_text = card.get_text()
        salary_match = re.search(r"\u5e74\u53ce\s*[\d,]+\u4e07\u5186\s*[~\u301c]\s*[\d,]+\u4e07\u5186", card_text)
        if salary_match:
            salary = salary_match.group(0)

        # Updated date from <time> element
        posted = ""
        time_el = card.find("time")
        if time_el:
            posted = time_el.get_text(strip=True)

        jobs.append({
            "title": title,
            "company": company,
            "location": "Japan",
            "url": full_url,
            "description": " ".join(skills),
            "source": "Forkwell",
            "posted": posted,
            "salary": salary,
        })

    return jobs


def fetch_forkwell_jobs():
    print("Fetching Forkwell jobs...")

    urls = [
        "https://jobs.forkwell.com/jobs/search?q[title]=ios&q[sort]=published_at+desc",
        "https://jobs.forkwell.com/jobs/search?q[title]=swift&q[sort]=published_at+desc",
        "https://jobs.forkwell.com/t/swift",
    ]

    jobs = []

    for url in urls:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_jobs = parse_forkwell_jobs(soup)
        print(f"  {url}: {len(page_jobs)} iOS jobs found")
        jobs.extend(page_jobs)

    return deduplicate_jobs(jobs)


# --- Region definition ---

REGION = {
    "sources": [
        {"fetch": fetch_tokyodev_jobs, "name": "TokyoDev", "color": "#dc2626"},
        {"fetch": fetch_forkwell_jobs, "name": "Forkwell", "color": "#7c3aed"},
    ],
    "linkedin_reminder": {
        "group": "japan",
        "url": "https://www.linkedin.com/jobs/search/?keywords=ios%20developer&location=Japan",
        "label": "Japan",
    },
}
