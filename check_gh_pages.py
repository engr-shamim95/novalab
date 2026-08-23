import urllib.request
import re

url = 'https://engr-shamim95.github.io/novalab/us/store.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    css_links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', html)
    print("CSS Links on GitHub Pages:")
    for link in css_links:
        print(link)
except Exception as e:
    print(f"Failed: {e}")
