import re

def check_css_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'[^"\'\s]+?\.css[^"\'\s]*', content)
    print(f"--- {filepath} ---")
    for link in set(links):
        print(link)

check_css_all('us/store.html')
check_css_all('us/bulk.html')
