import asyncio
from playwright.async_api import async_playwright
import pytesseract
import cv2
import numpy as np
import json

custom_config = r'--oem 3 --psm 4'

def prepare_image_for_ocr(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return gray

def fuzzy_find(img, word):
    gray = prepare_image_for_ocr(img)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config=custom_config)

    print(data['text'])

    for i, txt in enumerate(data['text']):
        if txt and word.lower() in txt.lower():
            x = data['left'][i] // 2
            y = data['top'][i] // 2
            w = data['width'][i] // 2
            h = data['height'][i] // 2
            return x + w // 2, y + h // 2
    return None

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


# id="playButton"
        # Step 1: Click "Zagraj teraz"
        await page.click("#playButton")
        await page.wait_for_timeout(16000)

        # Step 2: Login
        img = await take_and_read(page, "login.png")
        coords = fuzzy_find(img, "zaloguj") or fuzzy_find(img, "alogu")
        print(coords)
        if coords:
            await page.mouse.click(*coords)
            await page.wait_for_timeout(2000)
        else:
            print("Could not find 'Zaloguj'")

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

        # studio
        await page.mouse.click(1100, 600)
        await page.mouse.click(1100, 600)
        await page.wait_for_timeout(1000)

        # filmy
        await page.mouse.click(730, 130)
        await page.mouse.click(730, 130)
        await page.wait_for_timeout(5000)

        # ogladanie filmu
        await page.mouse.click(135, 300)
        await page.mouse.click(135, 300)
        await page.mouse.click(135, 300)
        await page.wait_for_timeout(11000)
        await page.mouse.click(135, 300)

        # love it
        properx = 135
        propery = 300
        await page.mouse.click(properx, propery)
        await page.mouse.click(properx, propery)

        screenshot_bytes = await page.screenshot()
        nparr = np.frombuffer(screenshot_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Draw small red dot at click coordinates
        cv2.circle(image, (properx,  propery), 3, (0, 0, 255), -1)  # -1 fills the circle
        
        # Save
        cv2.imwrite("screenshot_with_dot.png", image)
        img = await take_and_read(page, "after_click.png")

        await page.screenshot(
            path="after_click.png"
        )

asyncio.run(main())
