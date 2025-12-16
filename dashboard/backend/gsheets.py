import os
import gspread
from google.oauth2.service_account import Credentials
from config.settings import G_SHEET_URL


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def _creds_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "config", "gs_creds.json")

def get_sheet():
    creds = Credentials.from_service_account_file(
        _creds_path(),
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    return client.open_by_url(G_SHEET_URL).sheet1


def add_applied_job(job: dict):
    sheet = get_sheet()
    sheet.append_row([
        job.get("job_id"),
        job.get("title"),
        job.get("company"),
        job.get("url"),
        job.get("status"),
        job.get("date"),
    ])
