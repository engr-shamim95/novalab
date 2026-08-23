import re
with open(r'clone/us/store.html', 'r', encoding='utf-8') as f: html = f.read()

matches = re.findall(r'<header[^>]*>.*?</header>', html, flags=re.DOTALL)
if matches:
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', matches[0])
    print('Header images:', imgs)
else:
    print("No header tag found.")
