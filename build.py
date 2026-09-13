import json
import os
import shutil
import subprocess
from jinja2 import Environment, FileSystemLoader

# 1. Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
detail_template = env.get_template('detail.html')

# 2. Ensure output directories exist
os.makedirs('docs/css', exist_ok=True)
os.makedirs('docs/img', exist_ok=True)

# 3. Copy image assets
src_images_dir = 'img'
dst_images_dir = os.path.join('docs', 'img')

if os.path.exists(src_images_dir):
    for filename in os.listdir(src_images_dir):
        src_path = os.path.join(src_images_dir, filename)
        dst_path = os.path.join(dst_images_dir, filename)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)

# 4. Load rock data
with open('data.json', 'r', encoding='utf-8') as f:
    rocks = json.load(f)

# 5. Render index.html
index_html = index_template.render(rocks=rocks)
with open(os.path.join('docs', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

# 6. Render detail pages
for rock in rocks:
    clean_id = rock['id'].replace('#', '')
    filename = f"rock_{clean_id}.html"
    output_path = os.path.join('docs', filename)
    
    html_content = detail_template.render(rock=rock)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# 7. Compile Tailwind CSS
print("Compiling Tailwind CSS...")
try:
    subprocess.run(
        'npx @tailwindcss/cli -i src/style.css -o docs/css/style.css --minify',
        shell=True,
        check=True
    )
    print("Tailwind CSS compiled successfully!")
except Exception as e:
    print(f"Failed to compile Tailwind CSS: {e}")

print("Build complete! Files generated in docs/")