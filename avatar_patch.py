import os
import glob
import re

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend'
html_files = glob.glob(os.path.join(directory, '**/*.html'), recursive=True)

patched_count = 0

for filepath in html_files:
    # Skip dashboard if it's admin/photographer specific unless we want them too,
    # but let's just patch everything seamlessly where user-btn and authNav are injected
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content

    # Standard user object has first_name and last_name.
    avatar_logic = """const avatarUrl = user.profile_pic || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.first_name)}+${encodeURIComponent(user.last_name || '')}&background=6366f1&color=fff&size=32`;"""
    avatar_img = """<img src="${avatarUrl}" alt="Profile" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover; margin-right: 6px; vertical-align: middle; display: inline-block;">"""
    
    # 1. index.html complex template
    if 'authNav.innerHTML = `' in content and '<a href="#" class="user-btn"' in content:
        # Complex multi-line template literal replacement:
        # Specifically targeting index.html:
        # <i class="bi bi-person-circle"></i> ${user.first_name} or 👤 ${user.first_name}
        if avatar_logic not in content:
            # We inject avatar_logic just before authNav.innerHTML
            content = content.replace("authNav.innerHTML = `", f"{avatar_logic}\n          authNav.innerHTML = `")
            
            # replace icon with avatar_img in template literal
            content = re.sub(
                r'<a href="[^"]*" class="user-btn"[^>]*>.*?</a>',
                lambda m: '<a href="#" class="user-btn" onclick="showProfile(); return false;">\n            ' + avatar_img + '\n            ${user.first_name}\n          </a>',
                content,
                flags=re.DOTALL
            )
            
    # 2. String concatenation (older pages like services)
    # e.g: authNav.innerHTML = '<a href="#" class="user-btn" onclick="showProfile(); return false;">👤 ' + user.first_name + '</a><a href="#" class="logout-btn" onclick="logout(); return false;">Logout</a>';
    elif "authNav.innerHTML = '<a href=" in content and "user-btn" in content:
        # replace the entire line with a template literal
        def string_concat_replacer(match):
            # This turns the old single line string concat into our new template literal
            return f"""{avatar_logic}
    authNav.innerHTML = `
      <a href="#" class="user-btn" onclick="showProfile(); return false;">
        {avatar_img}
        ${{user.first_name}}
      </a>
      <a href="#" class="logout-btn" onclick="logout(); return false;"><i class="bi bi-box-arrow-right"></i> Logout</a>`;"""

        content = re.sub(
            r"authNav\.innerHTML\s*=\s*'[^']*user-btn[^;]*;",
            string_concat_replacer,
            content
        )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        patched_count += 1

print(f"Patched {patched_count} files with profile picture navbars!")
