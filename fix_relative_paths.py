import os
import re

clone_dir = "clone"

for root, dirs, files in os.walk(clone_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            # Calculate how deep we are relative to clone_dir
            rel_path = os.path.relpath(root, clone_dir)
            if rel_path == ".":
                depth = 0
                prefix = ""
            else:
                depth = len(rel_path.split(os.sep))
                prefix = "../" * depth
                
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Replace src="/assets/... with src="[prefix]assets/...
            content = content.replace('src="/assets/', f'src="{prefix}assets/')
            content = content.replace('srcset="/assets/', f'srcset="{prefix}assets/')
            content = content.replace('href="/assets/', f'href="{prefix}assets/')
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
                
print("Fixed relative paths for local viewing!")
