import os
import glob

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

patched_count = 0

old_logic = "const avatarUrl = user.profile_pic || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.first_name)}+${encodeURIComponent(user.last_name || '')}&background=6366f1&color=fff&size=32`;"
new_logic = "const avatarUrl = user ? (user.profile_pic || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.first_name || 'User')}+${encodeURIComponent(user.last_name || '')}&background=6366f1&color=fff&size=32`) : '';"

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        patched_count += 1

print(f"Fixed {patched_count} files!")
