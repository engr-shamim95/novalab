import os
import glob
import re

svg_main = """<svg width="160" height="49" viewBox="0 0 160 49" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t1 { font-family: 'Arial', sans-serif; font-weight: 900; font-size: 26px; fill: #0A192F; }
    .t2 { font-family: 'Arial', sans-serif; font-weight: 300; font-size: 26px; fill: #0A192F; }
  </style>
  <text x="5" y="34" class="t1">Nova</text>
  <text x="72" y="34" class="t2">Lab</text>
</svg>"""

svg_white = """<svg width="160" height="49" viewBox="0 0 160 49" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t1 { font-family: 'Arial', sans-serif; font-weight: 900; font-size: 26px; fill: white; }
    .t2 { font-family: 'Arial', sans-serif; font-weight: 300; font-size: 26px; fill: white; }
  </style>
  <text x="5" y="34" class="t1">Nova</text>
  <text x="72" y="34" class="t2">Lab</text>
</svg>"""

assets_dir = "clone/assets"
main_files = ["LogoMain_11.svg", "img_47_1787457640423.svg"]
white_files = ["LogoWhite_12.svg", "img_53_1787457660265.svg"]

# 1. Overwrite SVG files
for f in main_files:
    path = os.path.join(assets_dir, f)
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as out:
            out.write(svg_main)
            print(f"Replaced {f}")

for f in white_files:
    path = os.path.join(assets_dir, f)
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as out:
            out.write(svg_white)
            print(f"Replaced {f}")

# 2. Update HTML files
html_dir = "clone"
for root, dirs, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Replace old PNG logos with SVG
            new_content = content.replace("AminoClubLogoMain_6.png", "LogoMain_11.svg")
            new_content = new_content.replace("LogoMain_222.png", "LogoMain_11.svg")
            
            # Replace brand name references
            new_content = new_content.replace("Amino Club", "Nova Lab")
            new_content = new_content.replace("amino club", "nova lab")
            new_content = new_content.replace("Amino club", "Nova lab")
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated brand references in {file}")

print("Successfully rebranded to Nova Lab!")
