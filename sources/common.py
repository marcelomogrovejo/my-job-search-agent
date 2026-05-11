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
    best = {}
    for job in jobs:
        key = (
            job.get("title", "").lower().strip(),
            job.get("company", "").lower().strip(),
        )
        if key not in best:
            best[key] = job
        else:
            # Merge data from duplicates: keep the richer version but
            # combine descriptions so keywords from both sources survive
            existing = best[key]
            new_richness = len(job.get("description", "")) + len(job.get("salary", "")) + len(job.get("posted", ""))
            old_richness = len(existing.get("description", "")) + len(existing.get("salary", "")) + len(existing.get("posted", ""))

            if new_richness > old_richness:
                winner, donor = job, existing
            else:
                winner, donor = existing, job

            # Merge descriptions (combine unique keywords from both)
            winner_desc = set(winner.get("description", "").split())
            donor_desc = set(donor.get("description", "").split())
            merged = winner_desc | donor_desc
            winner["description"] = " ".join(sorted(merged))

            # Fill in missing fields from donor
            if not winner.get("salary") and donor.get("salary"):
                winner["salary"] = donor["salary"]
            if not winner.get("posted") and donor.get("posted"):
                winner["posted"] = donor["posted"]

            best[key] = winner
    return list(best.values())
