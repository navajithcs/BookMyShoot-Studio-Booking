import os
import glob

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

string_to_remove = "const avatarUrl = user ? (user.profile_pic || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.first_name || 'User')}+${encodeURIComponent(user.last_name || '')}&background=6366f1&color=fff&size=32`) : '';\n"
string_to_remove_fallback = "const avatarUrl = user ? (user.profile_pic || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.first_name || 'User')}+${encodeURIComponent(user.last_name || '')}&background=6366f1&color=fff&size=32`) : '';"

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if string_to_remove in content or string_to_remove_fallback in content:
        content = content.replace(string_to_remove, '')
        content = content.replace(string_to_remove_fallback, '')
        
        # also clean up empty lines that might have been left
        lines = content.split('\n')
        lines = [line for line in lines if "const avatarUrl = user" not in line]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
