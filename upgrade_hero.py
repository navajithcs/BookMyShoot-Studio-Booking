import os
import glob
import re

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend\services'
html_files = glob.glob(os.path.join(directory, '*.html'))

patched_count = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    service_id = filename.replace('.html', '')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'href="../index.html#portfolio"' not in content:
        buttons_html = f"""
  <div style="margin-top: 30px;">
    <a href="../index.html#portfolio" class="cta-btn" style="background: rgba(255,255,255,0.15); color: white; border: 2px solid white; margin-right: 15px; box-shadow: none;"><i class="bi bi-images"></i> View Portfolio</a>
    <a href="../booking.html?service={service_id}" class="cta-btn" style="box-shadow: 0 4px 15px rgba(0,0,0,0.1);"><i class="bi bi-calendar-check"></i> Book Now</a>
  </div>
"""
        
        target_str = '</section>\n\n<!-- SERVICE CONTENT -->'
        target_str_2 = '</section>\r\n\r\n<!-- SERVICE CONTENT -->'
        
        if target_str in content:
            content = content.replace(target_str, buttons_html + target_str)
        elif target_str_2 in content:
            content = content.replace(target_str_2, buttons_html + target_str_2)
        else:
            content = re.sub(
                r'(\n</section>\n\n<!-- SERVICE CONTENT -->)',
                lambda m: buttons_html + m.group(1),
                content,
                count=1
            )
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        patched_count += 1

print(f"Patched {patched_count} service files with Hero buttons!")
