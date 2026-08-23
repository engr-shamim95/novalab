import re
with open('temp.html', 'r', encoding='utf-8') as f:
    html = f.read()
matches = re.findall(r'<img[^>]+src="(/images/[^"]+)"', html)
print("Images starting with /images/:")
print(matches[:10])

matches_next = re.findall(r'<img[^>]+src="(/_next/image[^"]+)"', html)
print("\nImages starting with /_next/image:")
print(matches_next[:2])
