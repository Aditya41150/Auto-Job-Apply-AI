from datetime import datetime
from gsheets import add_applied_job

def run_bot(jobs: list[dict]):
    """Minimal bot stub that marks jobs as applied in Google Sheets.
    Replace with Playwright automation later.
    """
    results = []
    for job in jobs:
        record = {
            "job_id": job.get("job_id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "url": job.get("url"),
            "status": "applied",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        add_applied_job(record)
        results.append(record)
    return results
