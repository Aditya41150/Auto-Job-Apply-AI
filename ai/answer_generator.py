import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class AnswerGenerator:

    def generate(self, question: str, job_description: str):
        prompt = f"""
You are applying for a job. Write a strong, short answer.
QUESTION: {question}
JOB DESCRIPTION: {job_description}

Tone: confident, professional, humble.
"""

        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message["content"]
