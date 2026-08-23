import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html_dir = "."
assets_js_dir = "assets/js"
os.makedirs(assets_js_dir, exist_ok=True)

downloaded_js = {}

for root, dirs, files in os.walk(html_dir):
    if "assets" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            js_urls = set(re.findall(r'href="(https://www.aminoclub.com/_next/[^"]+\.js[^"]*)"', content) + \
                          re.findall(r'src="(https://www.aminoclub.com/_next/[^"]+\.js[^"]*)"', content))
            
            for url in js_urls:
                if url not in downloaded_js:
                    # Deal with subdirectories inside _next/static like /chunks/, /pages/
                    clean_url = url.split('?')[0]
                    # Keep the path structure flat for simplicity, just use the last two parts to avoid collisions
                    parts = clean_url.split('/')
                    if len(parts) >= 2:
                        filename = f"{parts[-2]}_{parts[-1]}"
                    else:
                        filename = parts[-1]
                        
                    local_path = os.path.join(assets_js_dir, filename)
                    
                    try:
                        print(f"Downloading {url} to {local_path}")
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, context=ctx) as response, open(local_path, 'wb') as out_file:
                            out_file.write(response.read())
                        downloaded_js[url] = filename
                    except Exception as e:
                        print(f"Failed to download {url}: {e}")
                        
            new_content = content
            for url, filename in downloaded_js.items():
                if url in new_content:
                    depth = path.count(os.sep)
                    if root == ".":
                        depth = 0
                    prefix = "../" * depth + "assets/js/"
                    new_content = new_content.replace(url, prefix + filename)
                    
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated JS links in {path}")

print("JS downloaded and localized successfully!")
