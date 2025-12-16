from fastapi import FastAPI, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys, os, time, threading
sys.path.append(os.path.dirname(__file__))

# CREATE APP FIRST
app = FastAPI()

# ADD CORS IMMEDIATELY AFTER APP CREATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- imports AFTER middleware ----
from gsheets import get_sheet
from run_bot import run_bot
from apply_single_job import apply_single

# Runtime flags
BOT_RUNNING = False
BOT_THREAD = None


@app.post("/apply-job")
def apply_single_job_route(job: dict = Body(...)):
    result = apply_single(job)
    return {"status": "applied", "message": result}



# ------------------------------
#   HELPERS
# ------------------------------

def bot_loop():
    global BOT_RUNNING
    while BOT_RUNNING:
        print("🤖 Bot Cycle Starting...")
        # In a real implementation, fetch new jobs and run the bot
        jobs = new_jobs()
        run_bot(jobs)
        print("⏳ Bot Sleeping 20 mins...")
        time.sleep(1200)   # 20 minutes


# ------------------------------
#   API ENDPOINTS
# ------------------------------
@app.post("/run-bot")
def run_bot_endpoint():
    jobs = new_jobs()
    results = run_bot(jobs)
    return {"message": "Bot finished", "processed": len(results)}

@app.get("/new-jobs")
def new_jobs():
    return [
        {
            "job_id": "job_1",
            "title": "Software Engineer Intern",
            "company": "Test Company",
            "url": "https://example.com",
        },
        {
            "job_id": "job_2",
            "title": "Backend Developer",
            "company": "Demo Corp",
            "url": "https://example.com",
        }
    ]

# removed duplicate /run-bot endpoint

@app.get("/applied-records")
def applied_records():
    sheet = get_sheet()
    rows = sheet.get_all_records()
    return [
        {
            "job_id": r.get("job_id"),
            "title": r.get("title"),
            "company": r.get("company"),
            "url": r.get("url"),
            "status": r.get("status"),
            "date": r.get("date"),
        }
        for r in rows
    ]

@app.get("/")
def root():
    return {"status": "backend ok"}


@app.get("/status")
def status():
    return {"running": BOT_RUNNING}


# removed undefined run_auto_apply endpoint


@app.post("/start-bot")
def start_bot():
    global BOT_RUNNING, BOT_THREAD
    if BOT_RUNNING:
        return {"status": "already_running"}

    BOT_RUNNING = True
    BOT_THREAD = threading.Thread(target=bot_loop, daemon=True)
    BOT_THREAD.start()
    return {"status": "bot_started"}


@app.post("/stop-bot")
def stop_bot():
    global BOT_RUNNING
    BOT_RUNNING = False
    return {"status": "bot_stopped"}


@app.get("/applied")
def applied():
    sheet = get_sheet()
    rows = sheet.get_all_values()

    header = rows[0]
    data = rows[1:]

    result = []
    for r in data:
        if len(r) >= 6:
            result.append({
                "job_id": r[0],
                "title": r[1],
                "company": r[2],
                "url": r[3],
                "status": r[4],
                "date": r[5]
            })
    return result


@app.get("/stats")
def stats():
    sheet = get_sheet()
    rows = sheet.get_all_values()[1:]  # skip header

    day_map = {}
    for row in rows:
        if len(row) >= 6:
            day = row[5]
            day_map[day] = day_map.get(day, 0) + 1

    return [{"day": day, "count": count} for day, count in day_map.items()]


# ------------------------------
#   EXTRA STUB ENDPOINTS (Frontend)
# ------------------------------

@app.get("/jobs/history")
def jobs_history():
    # Build a simple history view from the applied sheet
    try:
        sheet = get_sheet()
        rows = sheet.get_all_values()[1:]  # skip header
        history = []
        for r in rows:
            if len(r) >= 6:
                history.append(
                    {
                        "title": r[1],
                        "company": r[2],
                        "platform": "N/A",
                        "status": r[4],
                        "timestamp": r[5],
                    }
                )
        return history
    except Exception:
        return []


@app.post("/profile/update")
def profile_update(payload: dict = Body(...)):
    # Accept and acknowledge profile updates; no persistence for now
    return {"status": "ok", "saved": {k: payload.get(k) for k in ["name", "email", "phone"]}}


@app.post("/profile/upload_resume")
def profile_upload_resume(file: UploadFile = File(...)):
    # Save uploaded resume to data/resumes
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        save_dir = os.path.join(base_dir, "data", "resumes")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, file.filename)
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        return {"status": "uploaded", "filename": file.filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}


