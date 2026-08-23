import os
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

clone_dir = "clone"
base_url = "https://www.aminoclub.com"
cookies = {"amino_age_verified": "1"}
assets_dir = os.path.join(clone_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

session = requests.Session()
session.cookies.update(cookies)
session.headers.update({"User-Agent": "Mozilla/5.0"})

downloaded_map = {}

def get_best_url(srcset):
    # Parse srcset and get the url with the largest width
    best_url = None
    max_w = -1
    for part in srcset.split(","):
        parts = part.strip().split(" ")
        if not parts or not parts[0]: continue
        url = parts[0]
        if len(parts) > 1 and parts[1].endswith("w"):
            try:
                w = int(parts[1][:-1])
                if w > max_w:
                    max_w = w
                    best_url = url
            except:
                pass
        else:
            if best_url is None:
                best_url = url
    return best_url

def download_image(url):
    if url in downloaded_map:
        return downloaded_map[url]
        
    full_url = url if url.startswith("http") else base_url + url
    if "aminoclub.com" not in full_url:
        return url

    # Generate a simple filename
    import time
    filename = f"img_{len(downloaded_map)}_{int(time.time()*1000)}.webp"
    
    local_path = os.path.join(assets_dir, filename)
    relative_path = f"/assets/{filename}"
    
    print(f"Downloading {full_url} -> {relative_path}")
    try:
        res = session.get(full_url, timeout=5)
        if res.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(res.content)
            downloaded_map[url] = relative_path
            return relative_path
    except Exception as e:
        pass
        
    downloaded_map[url] = url
    return url

for root, dirs, files in os.walk(clone_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
                
            changed = False
            for img in soup.find_all("img"):
                best_url = None
                srcset = img.get("srcset")
                if srcset:
                    best_url = get_best_url(srcset)
                
                src = img.get("src")
                if not best_url and src:
                    best_url = src
                    
                if best_url:
                    local_url = download_image(best_url)
                    img["src"] = local_url
                    if img.has_attr("srcset"):
                        del img["srcset"]
                    changed = True
                    
            for source in soup.find_all("source"):
                srcset = source.get("srcset")
                if srcset:
                    best_url = get_best_url(srcset)
                    if best_url:
                        local_url = download_image(best_url)
                        source["srcset"] = local_url
                        changed = True

            if changed:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                print(f"Updated {path}")

print("Done! All images are now local.")
