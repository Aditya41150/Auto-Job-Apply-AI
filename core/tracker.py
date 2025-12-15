from core.gsheets_logger.py import GoogleSheetLogger
import json, os
from config.settings import APPLIED_JOBS_JSON, G_SHEET_URL

class Tracker:

    def __init__(self):
        if not os.path.exists(APPLIED_JOBS_JSON):
            with open(APPLIED_JOBS_JSON, "w") as f:
                json.dump([], f)

        self.sheet_logger = GoogleSheetLogger(G_SHEET_URL)

    def load(self):
        with open(APPLIED_JOBS_JSON, "r") as f:
            return json.load(f)

    def already_applied(self, job_id):
        data = self.load()
        return any(item["job_id"] == job_id for item in data)

    def save(self, job_id, job_title, company, url):
        data = self.load()
        data.append({
            "job_id": job_id,
            "job_title": job_title,
            "company": company,
            "url": url
        })

        with open(APPLIED_JOBS_JSON, "w") as f:
            json.dump(data, f, indent=2)

        # Also save online
        self.sheet_logger.log(job_id, job_title, company, url, "Applied")
