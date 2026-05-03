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


def build_html_summary(grouped_jobs):
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'></head>",
        "<body style='font-family: -apple-system, system-ui, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; color: #333;'>",
        "<h1 style='color: #1a1a1a; border-bottom: 2px solid #007AFF; padding-bottom: 10px;'>Daily iOS Job Matches</h1>",
    ]

    has_results = False

    for group in LOCATION_PRIORITY.keys():
        jobs = grouped_jobs.get(group, [])
        if not jobs:
            continue

        has_results = True
        label = LOCATION_LABELS[group]
        html_parts.append(
            f"<h2 style='color: #555; margin-top: 30px;'>{label} ({len(jobs)})</h2>"
        )
        html_parts.append("<table style='width: 100%; border-collapse: collapse;'>")

        for job in jobs:
            salary_badge = ""
            if job.get("salary"):
                salary_badge = (
                    f"<span style='background: #e8f5e9; color: #2e7d32; "
                    f"padding: 2px 8px; border-radius: 4px; font-size: 12px;'>"
                    f"{job['salary']}</span> "
                )

            posted_text = ""
            if job.get("posted"):
                posted_text = f" &middot; {job['posted']}"

            source_color = {
                "ITviec": "#e53935",
                "TopDev": "#1565c0",
                "VietnamDevs": "#6a1b9a",
                "ViecLamIT": "#ef6c00",
                "VietnamWorks": "#2e7d32",
                "RemoteOK": "#555",
            }.get(job["source"], "#888")

            html_parts.append(
                f"<tr style='border-bottom: 1px solid #eee;'>"
                f"<td style='padding: 12px 8px; vertical-align: top;'>"
                f"<a href='{job['url']}' style='color: #007AFF; text-decoration: none; font-weight: 600; font-size: 15px;'>"
                f"{job['title']}</a><br>"
                f"<span style='color: #666;'>{job['company']}</span><br>"
                f"<span style='font-size: 13px; color: #888;'>{job['location']}{posted_text}</span><br>"
                f"<span style='font-size: 12px;'>"
                f"{salary_badge}"
                f"<span style='background: {source_color}; color: white; "
                f"padding: 2px 6px; border-radius: 4px; font-size: 11px;'>{job['source']}</span>"
                f"</span>"
                f"</td></tr>"
            )

        html_parts.append("</table>")

        if group == "vietnam":
            linkedin_url = "https://www.linkedin.com/jobs/search/?keywords=ios%20developer&location=Vietnam"
            html_parts.append(
                "<div style='margin-top: 12px; padding: 16px; background: #e3f2fd; "
                "border-left: 4px solid #1565c0; border-radius: 4px;'>"
                "<strong style='color: #1565c0;'>Don't forget LinkedIn!</strong><br>"
                "<span style='font-size: 14px; color: #333;'>"
                "Many top companies post exclusively on LinkedIn. "
                f"<a href='{linkedin_url}' style='color: #1565c0;'>Check iOS jobs in Vietnam on LinkedIn</a>"
                "</span></div>"
            )

    if not has_results:
        html_parts.append("<p>No strong iOS matches found today.</p>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def main():
    print("Starting job search agent...")
    jobs = fetch_all_jobs()

    scored_jobs = []
    for job in jobs:
        scored = score_job(job)
        if scored:
            scored_jobs.append(scored)

    grouped_jobs = group_jobs(scored_jobs)
    html_body = build_html_summary(grouped_jobs)

    send_email("Daily iOS Job Matches", html_body)


if __name__ == "__main__":
    main()
