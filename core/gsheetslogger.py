import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetLogger:

    def __init__(self, sheet_url: str):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            "config/gs_creds.json", scopes=scopes
        )

        client = gspread.authorize(creds)
        self.sheet = client.open_by_url(sheet_url).sheet1

    def log(self, job_id, title, company, url, status):
        row = [job_id, title, company, url, status]
        self.sheet.append_row(row)
        print(f"📊 Google Sheet updated → {title} @ {company}")
