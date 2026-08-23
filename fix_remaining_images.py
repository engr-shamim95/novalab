import os
import glob
import re
from PIL import Image
from rembg import remove

assets_dir = "clone/assets"
html_dir = "clone"

# 1. Rename all .webp to .png
webp_files = glob.glob(os.path.join(assets_dir, "*.webp"))
for webp_path in webp_files:
    png_path = webp_path[:-5] + ".png"
    if not os.path.exists(png_path):
        os.rename(webp_path, png_path)
        print(f"Renamed {webp_path} to {png_path}")
    else:
        # If png exists, just remove the webp
        os.remove(webp_path)

# 2. Update all HTML files
for root, dirs, files in os.walk(html_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            # Find all assets/*.webp and replace with .png
            new_html = re.sub(r'(assets/[^"\']+)\.webp', r'\1.png', html)
            if new_html != html:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                print(f"Updated HTML references in {path}")

# 3. Process remaining non-transparent PNGs
png_files = glob.glob(os.path.join(assets_dir, "*.png"))
print(f"Found {len(png_files)} PNG files to check.")

for path in png_files:
    # Only process files that don't start with img_ since we already did those
    # (Though we can also just check if they have alpha channel, but rembg is safer if we just do the remaining)
    filename = os.path.basename(path)
    if not filename.startswith("img_"):
        print(f"Removing background for {filename}...")
        try:
            input_image = Image.open(path).convert("RGBA")
            # Just run rembg
            output_image = remove(input_image)
            output_image.save(path, "PNG")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

print("All remaining images processed and made transparent!")
