import openai
from config.settings import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

class JDExtractor:

    def extract(self, text):
        prompt = f"""
Extract the following from the job description:

1. Key required skills
2. Soft skills
3. Seniority level
4. Tech stack
5. Responsibilities
6. Red flags (if any)
7. Keywords to include in resume

JOB DESCRIPTION:
{text}

Return in clean JSON.
"""

        resp = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return resp.choices[0].message["content"]
