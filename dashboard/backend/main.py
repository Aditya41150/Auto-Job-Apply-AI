from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from gsheets import get_sheet
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_RUNNING = False

# TEST ROUTE
@app.get("/")
def root():
    return {"status": "Backend is running"}

# RETURN ALL APPLIED JOBS
@app.get("/applied")
def applied():
    sheet = get_sheet()
    rows = sheet.get_all_values()

    header = rows[0]
    data = rows[1:]

    result = []
    for r in data:
        if len(r) >= 4:
            result.append({
                "job_id": r[0],
                "title": r[1],
                "company": r[2],
                "url": r[3],
                "status": r[4] if len(r) > 4 else "Applied"
            })
    return result

# RETURN STATS FOR GRAPH
@app.get("/stats")
def stats():
    sheet = get_sheet()
    rows = sheet.get_all_values()[1:]  # skip header

    day_count = {}

    for row in rows:
        applied_at = row[5] if len(row) > 5 else ""
        if applied_at:
            day_count[applied_at] = day_count.get(applied_at, 0) + 1

    return [{"day": d, "count": c} for d, c in day_count.items()]

@app.get("/control/start")
def start_bot():
    global BOT_RUNNING
    BOT_RUNNING = True
    return {"bot": "started"}

@app.get("/control/stop")
def stop_bot():
    global BOT_RUNNING
    BOT_RUNNING = False
    return {"bot": "stopped"}

