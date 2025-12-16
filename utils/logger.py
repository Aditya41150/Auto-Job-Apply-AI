from utils.logger import log_job

def apply_to_job(job):
    # your job fields
    title = job["title"]
    company = job["company"]
    platform = job["platform"]

    try:
        # your auto apply logic here
        success = auto_apply(job)

        if success:
            log_job(title, company, platform, "applied")
        else:
            log_job(title, company, platform, "failed")

    except Exception:
        log_job(title, company, platform, "error")
