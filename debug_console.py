from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.on("console", lambda msg: print(f"CONSOLE {msg.type}: {msg.text}"))
    page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))
    page.on("requestfailed", lambda req: print(f"FAILED: {req.url} - {req.failure}"))
    
    url = f"file:///{os.path.abspath('us/store.html')}"
    page.goto(url, wait_until="networkidle")
    
    browser.close()
