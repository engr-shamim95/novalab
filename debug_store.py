from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = f"file:///{os.path.abspath('us/store.html')}"
    page.goto(url)
    page.screenshot(path="debug_store.png", full_page=True)
    browser.close()
