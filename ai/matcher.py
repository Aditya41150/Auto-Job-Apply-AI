import openai
from config.settings import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

class Matcher:

    def score(self, job_title: str, job_description: str, resume_text: str):
        prompt = f"""
You are a hiring manager. Rate how well this resume fits the job.

JOB TITLE:
{job_title}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return a single integer (0-100).
"""

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return int(response.choices[0].message["content"].strip())
