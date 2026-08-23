import os
import re
import urllib.request
import ssl
from pathlib import Path

# Fix SSL context if needed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html_dir = "."
assets_css_dir = "assets/css"
os.makedirs(assets_css_dir, exist_ok=True)

downloaded_css = {}

# Find and download all CSS files
for root, dirs, files in os.walk(html_dir):
    if "assets" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            css_urls = set(re.findall(r'href="(https://www.aminoclub.com/_next/[^"]+\.css[^"]*)"', content))
            for url in css_urls:
                if url not in downloaded_css:
                    # Clean filename
                    filename = url.split('/')[-1].split('?')[0]
                    local_path = os.path.join(assets_css_dir, filename)
                    
                    try:
                        print(f"Downloading {url} to {local_path}")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, context=ctx) as response, open(local_path, 'wb') as out_file:
                            out_file.write(response.read())
                        downloaded_css[url] = filename
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")
                        
            # Now replace the URLs in the HTML content
            new_content = content
            for url, filename in downloaded_css.items():
                if url in new_content:
                    # Determine relative path depth
                    depth = path.count(os.sep)
                    if root == ".":
                        depth = 0
                    prefix = "../" * depth + "assets/css/"
                    new_content = new_content.replace(url, prefix + filename)
                    
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated CSS links in {path}")

print("CSS downloaded and localized successfully!")
