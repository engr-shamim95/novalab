import os
import re
import requests
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
import time

clone_dir = "clone"
base_url = "https://www.aminoclub.com"
cookies = {"amino_age_verified": "1"}

os.makedirs(os.path.join(clone_dir, "assets"), exist_ok=True)
downloaded_assets = {}

session = requests.Session()
session.cookies.update(cookies)
session.headers.update({"User-Agent": "Mozilla/5.0"})

def download_asset(url):
    if url in downloaded_assets:
        return downloaded_assets[url]
    
    # We only care about aminoclub domains
    if not url.startswith("http") and not url.startswith("/"):
        return url
        
    full_url = url if url.startswith("http") else base_url + url
    if "aminoclub.com" not in full_url:
        return url

    # Generate a safe filename
    # E.g. /_next/image?url=%2Fimages%2Fhero%2FTB500Desktop.webp
    parsed = urlparse(full_url)
    filename = parsed.path.split("/")[-1]
    if "url=" in parsed.query:
        # Extract original filename from query
        import urllib.parse
        qs = urllib.parse.parse_qs(parsed.query)
        if "url" in qs:
            original_path = qs["url"][0]
            filename = original_path.split("/")[-1]
            
    if not filename or filename.endswith(".com"):
        filename = f"asset_{int(time.time()*1000)}.png"
        
    # Ensure uniqueness
    base_name, ext = os.path.splitext(filename)
    if not ext: ext = ".png"
    safe_name = f"{base_name}_{len(downloaded_assets)}{ext}"
    # remove invalid chars
    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', safe_name)
    
    local_path = os.path.join(clone_dir, "assets", safe_name)
    relative_path = f"/assets/{safe_name}"
    
    print(f"Downloading {full_url} to {relative_path}")
    try:
        res = session.get(full_url, timeout=10)
        if res.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(res.content)
            downloaded_assets[url] = relative_path
            return relative_path
    except Exception as e:
        print(f"Failed {full_url}: {e}")
        
    downloaded_assets[url] = url
    return url

for root, dirs, files in os.walk(clone_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                
            changed = False
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    new_src = download_asset(src)
                    if new_src != src:
                        img["src"] = new_src
                        changed = True
                
                srcset = img.get("srcset")
                if srcset:
                    # srcset can have multiple urls separated by commas
                    new_srcset = []
                    for part in srcset.split(","):
                        parts = part.strip().split(" ")
                        if len(parts) > 0:
                            url = parts[0]
                            new_url = download_asset(url)
                            parts[0] = new_url
                            new_srcset.append(" ".join(parts))
                    new_srcset_str = ", ".join(new_srcset)
                    if new_srcset_str != srcset:
                        img["srcset"] = new_srcset_str
                        changed = True
                        
            for source in soup.find_all("source"):
                srcset = source.get("srcset")
                if srcset:
                    new_srcset = []
                    for part in srcset.split(","):
                        parts = part.strip().split(" ")
                        if len(parts) > 0:
                            url = parts[0]
                            new_url = download_asset(url)
                            parts[0] = new_url
                            new_srcset.append(" ".join(parts))
                    new_srcset_str = ", ".join(new_srcset)
                    if new_srcset_str != srcset:
                        source["srcset"] = new_srcset_str
                        changed = True

            if changed:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                print(f"Updated images in {path}")

print("Done downloading images.")
