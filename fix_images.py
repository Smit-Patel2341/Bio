import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the first base64 image (hero) with 1.jpeg
content = re.sub(r'<img src="data:image/[^"]+"', r'<img src="1.jpeg"', content, count=1)

# Replace the next base64 images in the gallery with 2.jpeg and 3.jpeg
# Wait, let's see how many gallery images there are.
# In the previous view, there was <img class="gallery-img" src="data:image/png;base64,...">
# Let's just find all base64 images and replace them sequentially.
base64_pattern = re.compile(r'src="data:image/[^"]+"')

def replacer(match):
    global img_counter
    img_counter += 1
    # We have 1.jpeg, 2.jpeg, 3.jpeg. Let's cycle or cap at 3.
    idx = img_counter if img_counter <= 3 else 3
    return f'src="{idx}.jpeg"'

img_counter = 0
content = base64_pattern.sub(replacer, content)

# Now fix the CSS
# Desktop CSS
content = content.replace(
    "width: 260px; height: 310px; flex-shrink: 0;",
    "width: 100%; max-width: 260px; height: auto; flex-shrink: 0;"
)
content = content.replace(
    ".hero-photo img { width: 100%; height: 100%; object-fit: cover; object-position: center top; }",
    ".hero-photo img { width: 100%; height: auto; display: block; }"
)

content = content.replace(
    ".gallery-img { width: 100%; height: 280px; object-fit: cover; object-position: center top; }",
    ".gallery-img { width: 100%; height: auto; display: block; border: 2px solid var(--gold); border-radius: 8px; }"
)

# Mobile CSS
content = content.replace(
    ".hero-photo { width: 180px; height: 220px; margin: 0 auto; }",
    ".hero-photo { width: 100%; max-width: 220px; height: auto; margin: 0 auto; }"
)
content = content.replace(
    ".gallery-img { height: 200px; }",
    ".gallery-img { height: auto; }"
)

content = content.replace(
    ".hero-photo { width: 150px; height: 190px; }",
    ".hero-photo { width: 100%; max-width: 190px; height: auto; margin: 0 auto; }"
)
content = content.replace(
    ".gallery-img { height: 220px; }",
    ".gallery-img { height: auto; }"
)

with open('index.html', 'w') as f:
    f.write(content)

print(f"Replaced {img_counter} base64 images.")

