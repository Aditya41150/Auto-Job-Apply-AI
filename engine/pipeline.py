import json
from typing import List
from ai.matcher import Matcher
from ai.resume_customizer import ResumeCustomizer
from core.job_model import Job

class Pipeline:

    def __init__(self, scrapers: List):
        self.scrapers = scrapers
        self.matcher = Matcher()
        self.resume_customizer = ResumeCustomizer()

    async def run(self):
        base_resume = self.resume_customizer.load_resume()
        all_jobs = []

        # SCRAPE JOBS
        for scraper in self.scrapers:
            jobs = await scraper.fetch_jobs()
            all_jobs.extend(jobs)

        results = []

        # SCORE JOBS USING AI
        for job in all_jobs:
            score = self.matcher.score(
                job.title,
                job.description or "",
                base_resume
            )
            results.append((score, job))

        results.sort(reverse=True, key=lambda x: x[0])
        return results

    def get_best_resume(self, job_description: str):
        return self.resume_customizer.customize(job_description)
    