import subprocess
import json

def apply_single(job):
    """
    job = {
        "job_id": "...",
        "title": "...",
        "company": "...",
        "url": "..."
    }
    """

    print("\n=== Running Single Apply Bot ===")
    print(job)

    # Save job to a temp json
    with open("temp_job.json", "w") as f:
        json.dump(job, f, indent=4)

    # TEMP: Only simulate the bot
    # Later we link this to Playwright script
    return f"Applied to {job['title']} at {job['company']}!"
