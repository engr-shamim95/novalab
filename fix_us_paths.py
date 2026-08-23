import os

html_dir = "us"
for file in os.listdir(html_dir):
    if file.endswith(".html"):
        path = os.path.join(html_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content.replace("../../assets/css/", "../assets/css/")
        new_content = new_content.replace("../../assets/js/", "../assets/js/")
        
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed relative paths in {path}")

print("Fixed us/ HTML files!")
