import os
import glob
import re

assets_dir = "clone/assets"
html_dir = "clone"

# Find all incorrectly named SVGs
svg_files = []
for ext in ["*.png", "*.webp"]:
    for path in glob.glob(os.path.join(assets_dir, ext)):
        with open(path, "rb") as f:
            header = f.read(10)
            if b"<svg" in header.lower():
                svg_files.append(path)

print(f"Found {len(svg_files)} SVG files incorrectly named.")

rename_map = {}

for path in svg_files:
    new_path = path.rsplit(".", 1)[0] + ".svg"
    os.rename(path, new_path)
    print(f"Renamed {path} -> {new_path}")
    
    old_filename = os.path.basename(path)
    new_filename = os.path.basename(new_path)
    rename_map[old_filename] = new_filename

# Update all HTML files
if rename_map:
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                for old_name, new_name in rename_map.items():
                    content = content.replace(old_name, new_name)
                    
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated references in {file_path}")

print("Fixed SVG extensions!")
