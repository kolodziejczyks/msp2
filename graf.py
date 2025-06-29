import asyncio
from playwright.async_api import async_playwright
import pytesseract
import cv2
import numpy as np
import json

async def take_and_read(page, path):
    await page.screenshot(path=path)
    return cv2.imread(path)

async def main():
    with open('credentials.json') as f:
        creds = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto("https://moviestarplanet2.com")
        await page.wait_for_timeout(8000)

        # Step 1: Click "Zagraj teraz"
        await page.click("#playButton")
        await page.wait_for_timeout(16000)

        # login
        await page.mouse.click(1092, 669)
        await page.mouse.click(1092, 669)
        await page.wait_for_timeout(2000)

        await page.keyboard.type(creds['username'])
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        await page.keyboard.type(creds['password'])
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(7000)

        await page.wait_for_timeout(7000)

        # friends
        await page.mouse.click(375, 50)
        await page.mouse.click(375, 50)
        await page.wait_for_timeout(5000)

        # search zakładka   
        await page.mouse.click(1175, 175)
        await page.mouse.click(1175, 175)
        await page.wait_for_timeout(1000)

        # search input
        await page.mouse.click(1175, 260)
        await page.mouse.click(1175, 260)
        await page.wait_for_timeout(1000)
        await page.keyboard.type(creds['destinationLogin'])
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        
        # profile
        await page.mouse.click(995, 340)
        await page.mouse.click(995, 340)
        await page.wait_for_timeout(1000)

        # graf menu
        await page.mouse.click(830, 460)
        await page.mouse.click(830, 460)
        await page.wait_for_timeout(1000)

        #graf machen
        properx = 1080
        propery = 330
        await page.mouse.click(properx, propery)
        await page.mouse.click(properx, propery)
        await page.wait_for_timeout(1000)

        # screenshot_bytes = await page.screenshot()
        # nparr = np.frombuffer(screenshot_bytes, np.uint8)
        # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # # Draw small red dot at click coordinates
        # cv2.circle(image, (properx,  propery), 10, (0, 0, 255), -1)  # -1 fills the circle
        
        # # Save
        # cv2.imwrite("screenshot_with_dot.png", image)
        # img = await take_and_read(page, "after_click.png")

        # await page.screenshot(
        #     path="after_click.png"
        # )

asyncio.run(main())
