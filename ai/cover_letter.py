import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class CoverLetter:

    def generate(self, job_title, company, job_description, resume_text):
        prompt = f"""
Write a strong, professional cover letter for the job role below.

JOB TITLE: {job_title}
COMPANY: {company}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Tone: enthusiastic, professional, confident (NOT braggy).
Length: 150–200 words.
"""

        resp = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )

        return resp.choices[0].message["content"]
