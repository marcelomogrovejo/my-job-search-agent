from sources.common import deduplicate_jobs
from sources.vietnam import REGION as VIETNAM
from sources.japan import REGION as JAPAN
from sources.international import REGION as INTERNATIONAL

# ──────────────────────────────────────────────
# Comment out a line to disable an entire region
# ──────────────────────────────────────────────
ACTIVE_REGIONS = [
    VIETNAM,
    JAPAN,
    INTERNATIONAL,
]

# Derived from active regions — no manual updates needed
ACTIVE_SOURCES = [s for r in ACTIVE_REGIONS for s in r["sources"]]
SOURCE_COLORS = {s["name"]: s["color"] for s in ACTIVE_SOURCES}
LINKEDIN_REMINDERS = {}
for _region in ACTIVE_REGIONS:
    reminder = _region.get("linkedin_reminder")
    if reminder:
        LINKEDIN_REMINDERS[reminder["group"]] = reminder


def fetch_all_jobs():
    jobs = []

    for source in ACTIVE_SOURCES:
        try:
            jobs.extend(source["fetch"]())
        except Exception as error:
            print(f"Source {source['name']} failed: {error}")

    return deduplicate_jobs(jobs)
