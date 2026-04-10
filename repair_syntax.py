import os
import glob
import re

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

patched_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Bug 1: '; return false;">Logout</a>';
    content = content.replace("'; return false;\">Logout</a>';", "';")
    
    # Bug 2: '; return false;">👤 ' + user.first_name + '</a><a href="#" class="logout-btn" onclick="logout(); return false;">Logout</a>'; }
    # Let's fix this using regex for safety
    content = re.sub(
        r"'; return false;\">👤 ' \+ user\.first_name \+ '</a><a href=\"#\" class=\"logout-btn\" onclick=\"logout\(\); return false;\">Logout</a>';\s*}",
        "'; }",
        content
    )
    
    # Bug 3 (engagement.html): '; return false;">👤 ' + user.first_name + '</a><a href="#" class="logout-btn" onclick="logout(); return false;">Logout</a>';" without }
    content = re.sub(
        r"'; return false;\">👤 ' \+ user\.first_name \+ '</a><a href=\"#\" class=\"logout-btn\" onclick=\"logout\(\); return false;\">Logout</a>';",
        "';",
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        patched_count += 1

print(f"Repaired syntax in {patched_count} files!")
