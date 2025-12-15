import openai
from config.settings import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


class ResumeCustomizer:

    def __init__(self, base_resume_path="data/resumes/resume.txt"):
        self.resume_path = base_resume_path

    def load_resume(self):
        with open(self.resume_path, "r", encoding="utf-8") as f:
            return f.read()

    def customize(self, job_description: str):
        base_resume = self.load_resume()

        prompt = f"""
You are a professional resume writer.
Customize the following resume for the job description below.
Keep the structure similar but optimize keywords and skills.

RESUME:
{base_resume}

JOB DESCRIPTION:
{job_description}

Return ONLY the improved resume text.
"""

        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message["content"]
