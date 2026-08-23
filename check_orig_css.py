import urllib.request
import re

def check_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cookie': 'amino_age_verified=1'})
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        css_links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', html)
        print(f"--- {url} ---")
        for link in css_links:
            print(link)
    except Exception as e:
        print(f"Failed: {e}")

check_url('https://www.aminoclub.com/us/faq')
check_url('https://www.aminoclub.com/us.html')
