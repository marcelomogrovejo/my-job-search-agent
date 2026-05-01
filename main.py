from config import LOCATION_PRIORITY, LOCATION_LABELS
from job_sources import fetch_all_jobs
from job_scoring import score_job
from email_sender import send_email


def group_jobs(scored_jobs):
    grouped = {key: [] for key in LOCATION_PRIORITY.keys()}

    for job in scored_jobs:
        group = job.get("location_group", "international")
        grouped.setdefault(group, []).append(job)

    for group in grouped:
        grouped[group] = sorted(
            grouped[group],
            key=lambda job: job["final_score"],
            reverse=True,
        )

    return grouped


def build_summary(grouped_jobs):
    lines = ["Daily iOS Job Matches\n"]

    has_results = False

    for group in LOCATION_PRIORITY.keys():
        jobs = grouped_jobs.get(group, [])
        if not jobs:
            continue

        has_results = True
        lines.append(f"\n{LOCATION_LABELS[group]}\n")

        for index, job in enumerate(jobs, start=1):
            lines.append(
                f"{index}. {job['title']} - {job['company']}\n"
                f"Location: {job['location']}\n"
                f"Source: {job['source']}\n"
                f"Score: {job['final_score']} "
                f"(Relevance: {job['relevance_score']}, Location: {job['location_score']})\n"
                f"Link: {job['url']}\n"
            )

    if not has_results:
        return "No strong iOS matches found today."

    return "\n".join(lines)


def main():
    print("Starting job search agent...")
    jobs = fetch_all_jobs()

    scored_jobs = []
    for job in jobs:
        scored = score_job(job)
        if scored:
            scored_jobs.append(scored)

    grouped_jobs = group_jobs(scored_jobs)
    summary = build_summary(grouped_jobs)

    send_email("Daily iOS Job Matches", summary)


if __name__ == "__main__":
    main()