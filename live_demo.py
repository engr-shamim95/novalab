import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    print("Launching visible Chrome browser for a live demo...")
    async with async_playwright() as p:
        # Launch non-headless browser to show the user
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Path to the fully offline clone
        local_us_path = f"file:///{os.path.abspath('clone/us.html').replace(os.sep, '/')}"
        print(f"Navigating to {local_us_path}...")
        
        await page.goto(local_us_path)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        
        # Show off the home page by scrolling down slowly
        print("Scrolling down the homepage...")
        for _ in range(5):
            await page.mouse.wheel(0, 700)
            await asyncio.sleep(1.5)
            
        # Scroll back up a bit
        print("Scrolling back up...")
        for _ in range(3):
            await page.mouse.wheel(0, -700)
            await asyncio.sleep(1)
            
        # Click on the "Products" link in the header
        print("Clicking 'Products' link...")
        await page.click("text=Products")
        
        # Now we're on the store page! (Actually local navigation won't work perfectly unless the hrefs are exactly local paths)
        # Let's manually navigate to the local store page since relative links in static HTML might point to /us/store which doesn't resolve in file://
        local_store_path = f"file:///{os.path.abspath('clone/us/store.html').replace(os.sep, '/')}"
        await page.goto(local_store_path)
        await asyncio.sleep(2)
        
        # Scroll down the store page to see all the downloaded images
        print("Scrolling through the store catalog...")
        for _ in range(6):
            await page.mouse.wheel(0, 600)
            await asyncio.sleep(1)
            
        print("Finished browsing! Closing browser in 3 seconds...")
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
