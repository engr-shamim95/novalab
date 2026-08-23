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
            
            # Replace /_next/static/media/foo.woff2 with ../assets/media/foo.woff2
            new_content = re.sub(r'/_next/static/media/([^"\'\\]+)', lambda m: prefix + "media/" + m.group(1), content)
            
            escaped_prefix_media = (prefix + "media/").replace("/", "\\/")
            new_content = re.sub(r'\\?\/_next\\?\/static\\?\/media\\?/([^"\'\\]+)', lambda m: escaped_prefix_media + m.group(1), new_content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed internal _next media in {path}")

# Now fix the CSS files themselves
css_dir = "assets/css"
if os.path.exists(css_dir):
    for file in os.listdir(css_dir):
        if file.endswith(".css"):
            path = os.path.join(css_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            new_content = re.sub(r'/_next/static/media/([^"\'\)]+)', lambda m: "../media/" + m.group(1), content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed internal _next media in {path}")
                
print("Media paths localized!")
