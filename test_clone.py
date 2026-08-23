import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        # Set cookie for aminoclub.com so that absolute image links load correctly
        await context.add_cookies([{
            "name": "amino_age_verified",
            "value": "1",
            "domain": ".aminoclub.com",
            "path": "/"
        }])
        
        page = await context.new_page()
        
        # Test local us.html
        local_us_path = f"file:///{os.path.abspath('clone/us.html').replace(os.sep, '/')}"
        print(f"Testing {local_us_path}...")
        await page.goto(local_us_path)
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="local_us_screenshot2.png", full_page=True)
        print("Saved local_us_screenshot2.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
