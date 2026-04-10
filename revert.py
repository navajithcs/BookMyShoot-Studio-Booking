import os

css_path = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()
if '/* PORTFOLIO FILTERS & LIGHTBOX */' in css:
    css = css.split('/* PORTFOLIO FILTERS & LIGHTBOX */')[0]
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)

js_path = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend\js\main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()
if '// PORTFOLIO LOGIC: Category Filtering' in js:
    js = js.split('// PORTFOLIO LOGIC: Category Filtering')[0]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)

print("Reverted CSS and JS files successfully.")
