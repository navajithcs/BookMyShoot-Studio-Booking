import os
import glob
import re

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

patched_count = 0

# The exact logic block we injected
avatar_regex = re.compile(r"const avatarUrl = user \? .*?\s*authNav\.innerHTML = `.*?(<a[^>]*class=[\"']user-btn[\"'][^>]*>).*?Logout</a>`;", re.DOTALL)

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    if filename == 'index.html':
        # specific revert for index.html to preserve My Orders button
        def index_replacer(match):
            # match.group() is the whole string replacing
            return """authNav.innerHTML = `
          <a href="my-orders.html" class="nav-orders-btn"><i class="bi bi-receipt"></i> My Orders</a>
          <a href="#" class="user-btn" onclick="showProfile(); return false;"><i class="bi bi-person-circle"></i> ${user.first_name}</a>
          <a href="#" class="logout-btn" onclick="logout(); return false;"><i class="bi bi-box-arrow-right"></i> Logout</a>`;"""
        content = avatar_regex.sub(index_replacer, content)
    else:
        # standard revert for other files
        def general_replacer(match):
            if "profile.html" in filename:
                return "authNav.innerHTML = '<a href=\"profile.html\" class=\"user-btn\">👤 ' + (user.first_name || 'Profile') + '</a><a href=\"#\" class=\"logout-btn\" onclick=\"logout(); return false;\">Logout</a>';"
            else:
                return "authNav.innerHTML = '<a href=\"#\" class=\"user-btn\" onclick=\"showProfile(); return false;\">👤 ' + user.first_name + '</a><a href=\"#\" class=\"logout-btn\" onclick=\"logout(); return false;\">Logout</a>';"
        content = avatar_regex.sub(general_replacer, content)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        patched_count += 1

print(f"Reverted {patched_count} files!")
