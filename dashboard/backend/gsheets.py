import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import gspread
from google.oauth2.service_account import Credentials
from config.settings import G_SHEET_URL

def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(
        "../../config/gs_creds.json",
        scopes=scopes
    )
    client = gspread.authorize(creds)
    return client.open_by_url(G_SHEET_URL).sheet1
