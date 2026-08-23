from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = f"file:///{os.path.abspath('us/store.html')}"
    page.goto(url)
    
    # Let's get the classes of the first product wrapper
    classes = page.evaluate("""
        () => {
            const el = document.querySelector('[data-testid="product-wrapper"] > div');
            if (!el) return 'NOT FOUND';
            const style = window.getComputedStyle(el);
            return {
                className: el.className,
                backgroundColor: style.backgroundColor,
                borderRadius: style.borderRadius,
                display: style.display,
                width: style.width
            };
        }
    """)
    print("PRODUCT CARD STYLES:")
    print(classes)
    
    # Check if CSS files are loaded
    stylesheets = page.evaluate("""
        () => {
            return Array.from(document.styleSheets).map(s => s.href);
        }
    """)
    print("LOADED STYLESHEETS:")
    for s in stylesheets:
        print(s)
        
    browser.close()
