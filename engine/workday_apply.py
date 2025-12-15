from playwright.async_api import async_playwright
from core.field_mapper import field_match
import asyncio, random

class WorkdayApply:

    def __init__(self, resume_path="data/resumes/resume.pdf"):
        self.resume_path = resume_path

    async def pause(self):
        await asyncio.sleep(random.uniform(0.5, 1.2))

    async def apply(self, url: str, answers: dict):
        print(f"🌐 Workday → Opening {url}")

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)

            await self.pause()

            # next buttons
            async def next_step():
                possible = ["Next", "Continue", "Save and Continue"]
                for t in possible:
                    btn = page.get_by_text(t)
                    if await btn.count() > 0:
                        await btn.click()
                        return True
                return False

            # upload resume
            file_input = page.locator("input[type='file']")
            if await file_input.count() > 0:
                print("📄 Uploading resume...")
                await file_input.nth(0).set_input_files(self.resume_path)
                await self.pause()

            # try multiple steps
            for _ in range(6):
                clicked = await next_step()
                if not clicked:
                    break
                await self.pause()

            print("🚀 Workday steps complete.")
            await browser.close()
