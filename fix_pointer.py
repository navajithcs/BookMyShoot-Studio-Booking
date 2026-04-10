import os
import glob
import re

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

patched_count = 0

old_style = "style=\"width: 24px; height: 24px; border-radius: 50%; object-fit: cover; margin-right: 6px; vertical-align: middle; display: inline-block;\""
new_style = "style=\"width: 24px; height: 24px; border-radius: 50%; object-fit: cover; margin-right: 6px; vertical-align: middle; display: inline-block; pointer-events: none;\""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if old_style in content:
        content = content.replace(old_style, new_style)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        patched_count += 1

print(f"Fixed {patched_count} files with pointer-events: none!")
