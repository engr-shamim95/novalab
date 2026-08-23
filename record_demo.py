import asyncio
import threading
import http.server
import socketserver
import os
from playwright.async_api import async_playwright

# Start local server
PORT = 8000
DIRECTORY = "clone"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def log_message(self, format, *args):
        pass # Suppress logging

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Record video
        context = await browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )
        
        # Intercept network to add the bypass cookie to all aminoclub.com requests
        async def handle_route(route, request):
            if "aminoclub.com" in request.url:
                headers = request.headers
                headers["Cookie"] = "amino_age_verified=1"
                await route.continue_(headers=headers)
            else:
                await route.continue_()
                
        await context.route("**/*", handle_route)
        
        page = await context.new_page()
        page.set_default_timeout(15000)
        
        try:
            print("Navigating to home...")
            await page.goto(f"http://localhost:{PORT}/us.html")
            await page.wait_for_load_state("networkidle")
            
            # Simulate browsing: scroll down
            print("Scrolling...")
            for i in range(5):
                await page.mouse.wheel(0, 800)
                await asyncio.sleep(1)
            
            # Scroll back up
            for i in range(5):
                await page.mouse.wheel(0, -800)
                await asyncio.sleep(0.5)
                
            # Click on store
            print("Navigating to store...")
            await page.click("text=Products")
            await asyncio.sleep(1)
            await page.goto(f"http://localhost:{PORT}/us/store.html")
            await page.wait_for_load_state("networkidle")
            
            # Scroll store
            print("Scrolling store...")
            for i in range(4):
                await page.mouse.wheel(0, 600)
                await asyncio.sleep(1)
                
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error during browsing: {e}")
            
        print("Closing browser...")
        await context.close()
        await browser.close()
        
        # Find the video file
        videos = os.listdir("videos")
        if videos:
            print(f"Video saved as videos/{videos[0]}")
            # move to workspace root
            os.rename(f"videos/{videos[0]}", "demo_recording.webm")
            print("Moved to demo_recording.webm")

if __name__ == "__main__":
    asyncio.run(main())
