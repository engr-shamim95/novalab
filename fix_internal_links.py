import re
import os

clone_dir = "clone"

def url_to_local_path(url):
    url = url.split('#')[0].split('?')[0]
    if url == "/us":
        return os.path.join(clone_dir, "us.html")
    elif url.startswith("/us/"):
        return os.path.join(clone_dir, "us", url[4:] + ".html")
    return None

def replace_href(match, file_path):
    full_href = match.group(1)
    href = full_href
    hash_part = ""
    if "#" in href:
        parts = href.split("#", 1)
        href = parts[0]
        hash_part = "#" + parts[1]
        
    target_local_path = url_to_local_path(href)
    if target_local_path and os.path.exists(target_local_path):
        rel_path = os.path.relpath(target_local_path, os.path.dirname(file_path))
        rel_path = rel_path.replace(os.sep, "/")
        return f'href="{rel_path}{hash_part}"'
    return match.group(0)

# Process all html
for root, dirs, files in os.walk(clone_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            new_content = re.sub(r'href="(/us[^"]*)"', lambda m: replace_href(m, file_path), content)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated links in {file_path}")

print("Done updating all internal navigation links!")
