import os

folders = [
    "config", "data", "data/logs", "data/resumes",
    "core", "scrapers", "engine", "ai"
]

files = [
    "README.md", "requirements.txt",
    "config/settings.py", "data/applied_jobs.json",
    "core/__init__.py", "core/job_model.py",
    "core/scraper_base.py", "core/utils.py",
    "scrapers/__init__.py", "scrapers/greenhouse_scraper.py",
    "engine/__init__.py", "engine/pipeline.py",
    "ai/__init__.py", "ai/matcher.py",
    "main.py"
]

for f in folders:
    os.makedirs(f, exist_ok=True)

for f in files:
    open(f, "a").close()

print("Project folder structure created successfully!")
