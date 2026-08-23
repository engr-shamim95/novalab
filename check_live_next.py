import urllib.request

url = 'https://engr-shamim95.github.io/novalab/us/store.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    import re
    next_refs = re.findall(r'/_next/static/[^"\'\s]+', html)
    print("Next Refs on GitHub Pages:")
    for ref in set(next_refs):
        print(ref)
except Exception as e:
    print(f"Failed: {e}")
