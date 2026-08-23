import urllib.request
import re

req = urllib.request.Request('https://www.aminoclub.com/us/store', headers={'User-Agent': 'Mozilla/5.0', 'Cookie': 'amino_age_verified=1'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    css_files = set(re.findall(r'([^"\'\\]+\.css)', html))
    print(css_files)
except Exception as e:
    print(f"Failed: {e}")
