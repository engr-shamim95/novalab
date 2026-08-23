import re

def check_missing(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    css = re.findall(r'href="(/_next/[^"]+\.css[^"]*)"', html)
    js = re.findall(r'src="(/_next/[^"]+\.js[^"]*)"', html)
    if css or js:
        print(f"--- {filepath} ---")
        if css: print("CSS:", css)
        if js: print("JS:", js)

check_missing('us/store.html')
