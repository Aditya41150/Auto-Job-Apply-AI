import asyncio
import time

from engine.auto_apply import AutoApply
from engine.lever_apply import LeverApply
from engine.workday_apply import WorkdayApply
from scrapers.greenhouse_scraper import GreenhouseScraper
from core.tracker import Tracker
from ai.jd_extractor import JDExtractor

async def cycle():
    tracker = Tracker()
    jd_extractor = JDExtractor()

    scrapers = [
        GreenhouseScraper("stripe"),
        GreenhouseScraper("coinbase")
    ]

    answers = {
        "name": "Aditya .",
        "email": "yourmail@gmail.com",
        "phone": "+918058695424",
        "linkedin": "https://linkedin.com/in/aditya41150",
        "github": "https://github.com/Aditya41150"
    }

    lever = LeverApply()
    workday = WorkdayApply()
    general = AutoApply()

    print("\n🔍 Starting job scan...")

    for scraper in scrapers:
        jobs = await scraper.fetch_jobs()

        for job in jobs:
            job_id = job.url.split("/")[-1]

            if tracker.already_applied(job_id):
                continue

            # extract JD for intelligence
            if job.description:
                jd_data = jd_extractor.extract(job.description)
                print(jd_data)

            if "lever.co" in job.url:
                await lever.apply(job.url, answers)

            elif "workday" in job.url:
                await workday.apply(job.url, answers)

            else:
                await general.apply_to_job(job.url, answers)

            tracker.save(job_id, job.title, job.company, job.url)

async def main():
    while True:
        await cycle()
        print("⏳ Waiting 25 minutes before next scan...")
        time.sleep(1500)   # 25 minutes

asyncio.run(main())
