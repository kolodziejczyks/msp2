import asyncio
from playwright.async_api import async_playwright
import cv2
import json
import argparse
import numpy

async def take_and_read(page, path):
    await page.screenshot(path=path)
    return cv2.imread(path)

async def main():
    parser = argparse.ArgumentParser(description='Script for giving grafs like a boss')
    parser.add_argument('username', help='Account username')
    parser.add_argument('password', help='Account password')
    parser.add_argument('destinationLogin', help='Destination account username')

    creds = parser.parse_args()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-extensions'
        ])

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            extra_http_headers={
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
            }
        )

        page = await context.new_page()

        await page.add_init_script("""
                Object.defineProperty(document, 'hidden', {
                    get: () => false,
                });
                
                Object.defineProperty(document, 'visibilityState', {
                    get: () => 'visible',
                });
                
                Object.defineProperty(document, 'hasFocus', {
                    value: () => true,
                });
                
                // Override Page Visibility API
                document.addEventListener = new Proxy(document.addEventListener, {
                    apply(target, thisArg, args) {
                        if (args[0] === 'visibilitychange') {
                            return; // Don't add visibility change listeners
                        }
                        return target.apply(thisArg, args);
                    }
                });
            """)

        # page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto("https://wwww.moviestarplanet2.pl")

        await page.wait_for_timeout(1000)

        print(creds.username)

        await page.screenshot(
            path="before_play_button.png"
        )

        # Step 1: Click "Zagraj teraz"
        await page.click("#playButton")
        await page.wait_for_timeout(13000)
        await page.screenshot(
            path="play_button.png"
        )

        try:
            # Extract window.nebula object
            nebula_data = await page.evaluate('() => window.nebula')
            
            # Write to log file with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'nebula_log_{timestamp}.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(nebula_data, f, indent=2, ensure_ascii=False)
            
            print(f"window.nebula successfully copied to {filename}")
            
        except Exception as e:
            print(f"Error extracting window.nebula: {e}")
            
            # Fallback: check if window.nebula exists and log its type
            try:
                nebula_exists = await page.evaluate('() => typeof window.nebula')
                print(f"window.nebula type: {nebula_exists}")
                
                if nebula_exists != 'undefined':
                    # Try to get it as string
                    nebula_str = await page.evaluate('() => JSON.stringify(window.nebula)')
                    with open(f'nebula_log_{timestamp}.txt', 'w', encoding='utf-8') as f:
                        f.write(nebula_str)
                    print(f"window.nebula copied as string to nebula_log_{timestamp}.txt")
            except Exception as e2:
                print(f"Failed to extract window.nebula: {e2}")

        # login
        await page.mouse.click(1092, 669)
        await page.mouse.click(1092, 669)
        await page.wait_for_timeout(2000)

        await page.keyboard.type(creds.username)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1000)
        await page.keyboard.type(creds.password)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(7000)

        await page.wait_for_timeout(7000)

        await page.screenshot(
            path="after_login.png"
        )

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
        await page.keyboard.type(creds.destinationLogin)
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
        properx = 1130
        propery = 330
        await page.mouse.click(1130, 330)
        await page.mouse.click(1130, 330)
        await page.wait_for_timeout(1000)

        counter = 0

        while counter < 10:
            await page.mouse.click(1130, 330)
            await page.mouse.click(1130, 330)
            counter += 1
            await page.wait_for_timeout(60000)

            screenshot_bytes = await page.screenshot()
            nparr = numpy.frombuffer(screenshot_bytes, numpy.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Draw small red dot at click coordinates
            cv2.circle(image, (properx,  propery), 10, (0, 0, 255), -1)  # -1 fills the circle
            
            # Save
            cv2.imwrite(creds.username + ".png", image)

asyncio.run(main())
