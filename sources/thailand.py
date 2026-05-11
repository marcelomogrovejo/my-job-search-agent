import requests
from sources.common import BROWSER_HEADERS, is_ios_relevant, deduplicate_jobs


# --- JobsDB Thailand (REST API) ---

def fetch_jobsdb_jobs():
    print("Fetching JobsDB Thailand jobs...")

    api_url = "https://th.jobsdb.com/api/jobsearch/v5/search"

    queries = ["ios developer", "swift developer", "mobile developer"]
    all_jobs = []

    for query in queries:
        params = {
            "siteKey": "TH-Main",
            "keywords": query,
            "pageSize": 50,
            "page": 1,
            "sortMode": "ListedDate",
        }

        response = requests.get(
            api_url, params=params,
            headers={"User-Agent": BROWSER_HEADERS["User-Agent"]},
            timeout=20,
        )
        response.raise_for_status()

        data = response.json().get("data", [])
        print(f"  query='{query}': {len(data)} results")

        for item in data:
            title = item.get("title", "")
            if not is_ios_relevant(title):
                continue

            company = item.get("companyName", "Unknown")
            job_id = item.get("id", "")
            job_url = f"https://th.jobsdb.com/job/{job_id}" if job_id else ""

            locations = item.get("locations", [])
            location = locations[0].get("label", "Thailand") if locations else "Thailand"

            salary = item.get("salaryLabel", "")

            posted = ""
            listing_date = item.get("listingDate", "")
            if listing_date:
                posted = listing_date[:10]

            teaser = item.get("teaser", "")
            work_types = " ".join(item.get("workTypes", []))
            work_arrangement = ""
            arrangements = item.get("workArrangements", {})
            if arrangements:
                work_arrangement = arrangements.get("displayText", "")

            role_id = item.get("roleId", "")
            classifications = item.get("classifications", [])
            subcategory = ""
            if classifications:
                subcategory = classifications[0].get("subclassification", {}).get("description", "")

            description_parts = [teaser, work_types, work_arrangement, role_id, subcategory]
            description = " ".join(p for p in description_parts if p)

            all_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "url": job_url,
                "description": description,
                "source": "JobsDB",
                "posted": posted,
                "salary": salary,
            })

    return deduplicate_jobs(all_jobs)


# --- Region definition ---

REGION = {
    "sources": [
        {"fetch": fetch_jobsdb_jobs, "name": "JobsDB", "color": "#0d47a1"},
    ],
    "manual_reminders": [
        {
            "group": "thailand",
            "title": "Don't forget LinkedIn!",
            "text": "Many top companies post exclusively on LinkedIn.",
            "links": [
                {"label": "Check iOS jobs in Thailand on LinkedIn", "url": "https://www.linkedin.com/jobs/search/?keywords=ios%20developer&location=Thailand"},
            ],
        },
        {
            "group": "thailand",
            "title": "Check Blognone Jobs manually",
            "text": "Thailand's top tech job board blocks scrapers.",
            "links": [
                {"label": "iOS jobs on Blognone", "url": "https://jobs.blognone.com/search?q=iOS"},
                {"label": "Mobile jobs on Blognone", "url": "https://jobs.blognone.com/search?q=mobile"},
            ],
        },
    ],
}
