import os
import re

html_dir = "."
for root, dirs, files in os.walk(html_dir):
    if "assets" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            depth = path.count(os.sep)
            if root == ".":
                depth = 0
            prefix = "../" * depth + "assets/"
            
            # Replace /_next/static/chunks/foo.css with ../assets/css/foo.css
            new_content = re.sub(r'/_next/static/chunks/([^"\'\\]+\.css)[^"\'\\]*', lambda m: prefix + "css/" + m.group(1), content)
            
            # Replace /_next/static/chunks/foo.js with ../assets/js/foo.js
            new_content = re.sub(r'/_next/static/chunks/([^"\'\\]+\.js)[^"\'\\]*', lambda m: prefix + "js/" + m.group(1), new_content)
            
            # Also handle escaped versions like \/_next\/static\/chunks\/
            escaped_prefix_css = (prefix + "css/").replace("/", "\\/")
            escaped_prefix_js = (prefix + "js/").replace("/", "\\/")
            
            new_content = re.sub(r'\\?\/_next\\?\/static\\?\/chunks\\?/([^"\'\\]+\.css)[^"\'\\]*', lambda m: escaped_prefix_css + m.group(1), new_content)
            new_content = re.sub(r'\\?\/_next\\?\/static\\?\/chunks\\?/([^"\'\\]+\.js)[^"\'\\]*', lambda m: escaped_prefix_js + m.group(1), new_content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed internal _next chunks in {path}")

print("Internal Next.js chunk references localized!")
