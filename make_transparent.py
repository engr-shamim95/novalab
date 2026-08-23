import os
import glob
from rembg import remove
from PIL import Image

assets_dir = "clone/assets"
images = glob.glob(os.path.join(assets_dir, "img_*.png"))

print(f"Found {len(images)} images to process.")

for path in images:
    try:
        print(f"Removing background for {path}...")
        input_image = Image.open(path)
        output_image = remove(input_image)
        output_image.save(path, "PNG")
    except Exception as e:
        print(f"Failed to process {path}: {e}")

print("Done making all images transparent!")
