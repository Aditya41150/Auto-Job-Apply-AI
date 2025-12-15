from playwright.async_api import async_playwright
from core.field_mapper import field_match
import asyncio
import random

class LeverApply:

    def __init__(self, resume_path="data/resumes/resume.pdf"):
        self.resume_path = resume_path

    async def wait(self):
        await asyncio.sleep(random.uniform(0.3, 0.7))

    async def apply(self, url: str, answers: dict):
        print(f"🌐 Lever → Opening {url}")

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)

            inputs = page.locator("input, textarea").all()

            for inp in inputs:
                name = await inp.get_attribute("name")
                matched = field_match(name, answers)
                if matched:
                    print(f"→ Filling {matched}")
                    await inp.fill(answers[matched])
                    await self.wait()

            # Resume upload
            file_inputs = page.locator("input[type='file']")
            if await file_inputs.count() > 0:
                print("📄 Uploading resume...")
                await file_inputs.nth(0).set_input_files(self.resume_path)

            # Submit
            btn = page.get_by_text("Submit application")
            if await btn.count() > 0:
                await btn.click()

            await self.wait()
            await browser.close()

            print("🚀 Lever application submitted.")
