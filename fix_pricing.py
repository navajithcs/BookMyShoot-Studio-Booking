import os
import glob

directory = r'c:\Users\navaj\OneDrive\Desktop\main_project\frontend\services'
html_files = glob.glob(os.path.join(directory, '*.html'))

fix_css = """
    /* PRICING ALIGNMENT FIX */
    .pricing-grid {
      display: flex;
      flex-wrap: wrap;
      align-items: stretch;
    }
    .pricing-card {
      display: flex !important;
      flex-direction: column;
      height: 100%;
      flex: 1 1 250px;
    }
    .pricing-features {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
    }
    .pricing-card .book-btn, .book-btn.margin-auto {
      margin-top: auto !important;
    }
"""

patched_count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "/* PRICING ALIGNMENT FIX */" not in content:
        # Before replacing </style>, check if </style> exists
        if "</style>" in content:
            content = content.replace("</style>", fix_css + "</style>")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            patched_count += 1

print(f"Patched {patched_count} files successfully out of {len(html_files)}.")
