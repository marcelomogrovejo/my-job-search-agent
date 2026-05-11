from sources.common import deduplicate_jobs
from sources.vietnam import REGION as VIETNAM
from sources.japan import REGION as JAPAN
from sources.thailand import REGION as THAILAND
from sources.international import REGION as INTERNATIONAL

# ──────────────────────────────────────────────
# Comment out a line to disable an entire region
# ──────────────────────────────────────────────
ACTIVE_REGIONS = [
    VIETNAM,
    JAPAN,
    THAILAND,
    INTERNATIONAL,
]

# Derived from active regions — no manual updates needed
ACTIVE_SOURCES = [s for r in ACTIVE_REGIONS for s in r["sources"]]
SOURCE_COLORS = {s["name"]: s["color"] for s in ACTIVE_SOURCES}
MANUAL_REMINDERS = {}
for _region in ACTIVE_REGIONS:
    for reminder in _region.get("manual_reminders", []):
        group = reminder["group"]
        MANUAL_REMINDERS.setdefault(group, []).append(reminder)


def fetch_all_jobs():
    jobs = []

    for source in ACTIVE_SOURCES:
        try:
            jobs.extend(source["fetch"]())
        except Exception as error:
            print(f"Source {source['name']} failed: {error}")

    return deduplicate_jobs(jobs)
