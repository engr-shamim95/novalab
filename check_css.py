import re

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'<link[^>]*rel="stylesheet"[^>]*>', content)
    print(f"--- {filepath} ---")
    for link in links:
        print(link)

check_file('us/store.html')
check_file('us/bulk.html')
check_file('us/faq.html')
