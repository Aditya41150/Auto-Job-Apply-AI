import asyncio
import random

class Humanizer:

    @staticmethod
    async def delay(min_ms=80, max_ms=300):
        await asyncio.sleep(random.uniform(min_ms/1000, max_ms/1000))

    @staticmethod
    async def human_type(element, text):
        for char in text:
            await element.type(char)
            await Humanizer.delay(20, 90)

    @staticmethod
    async def random_scroll(page):
        for _ in range(random.randint(2, 5)):
            await page.mouse.wheel(0, random.randint(100, 400))
            await Humanizer.delay(200, 600)

    @staticmethod
    async def random_mouse_move(page):
        for _ in range(random.randint(5, 12)):
            x = random.randint(0, 800)
            y = random.randint(0, 800)
            await page.mouse.move(x, y)
            await Humanizer.delay(10, 40)
    