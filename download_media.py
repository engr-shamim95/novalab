import os
import re
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html_dir = "."
assets_media_dir = "assets/media"
os.makedirs(assets_media_dir, exist_ok=True)

# We need to find all media references in the CSS files!
css_dir = "assets/css"
media_urls = set()

for file in os.listdir(css_dir):
    if file.endswith(".css"):
        with open(os.path.join(css_dir, file), "r", encoding="utf-8") as f:
            css = f.read()
            # CSS contains url(/_next/static/media/...) or url(../media/...)
            media_urls.update(re.findall(r'/(_next/static/media/[^"\')]+)', css))
            media_urls.update(re.findall(r'\.\./media/([^"\')]+)', css))
            
# Also check HTML files just in case
for root, dirs, files in os.walk(html_dir):
    if "assets" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                html = f.read()
                media_urls.update(re.findall(r'/_next/static/media/([^"\'\\]+)', html))

print(f"Found {len(media_urls)} media files to download.")

for url_part in media_urls:
    # url_part might be just the filename if it was ../media/
    filename = url_part.split('/')[-1]
    url = f"https://www.aminoclub.com/_next/static/media/{filename}"
    local_path = os.path.join(assets_media_dir, filename)
    
    if not os.path.exists(local_path):
        try:
            print(f"Downloading {url} to {local_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {url}: {e}")

print("Media downloaded!")
