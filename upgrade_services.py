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
    
    # 1. Add "View Portfolio" and "Book Now" buttons to the hero block if not present
    if 'href="../index.html#portfolio"' not in content:
        # Find the closing </p> of the hero section
        # The hero section typically looks like:
        # <section class="service-hero">
        #   <h1>...</h1>
        #   <p>...</p>
        # </section>
        
        buttons_html = f"""
  <div style="margin-top: 30px;">
    <a href="../index.html#portfolio" class="cta-btn" style="background: rgba(255,255,255,0.15); color: white; border: 2px solid white; margin-right: 15px; box-shadow: none;"><i class="bi bi-images"></i> View Portfolio</a>
    <a href="../booking.html?service={service_id}" class="cta-btn" style="box-shadow: 0 4px 15px rgba(0,0,0,0.1);"><i class="bi bi-calendar-check"></i> Book Now</a>
  </div>
"""
        # Inject before </section> of service-hero
        # regex to find service-hero end
        content = re.sub(
            r'(\s*</section>\s*<!-- SERVICE CONTENT -->)',
            lambda m: buttons_html + m.group(1),
            content,
            count=1
        )
    
    # 2. Add "Reviews" section before <!-- CTA -->
    if 'class="reviews-section"' not in content:
        reviews_html = """
  <!-- REVIEWS -->
  <div class="reviews-section" style="margin-bottom: 60px;">
    <h2 style="text-align: center; margin-bottom: 30px; font-size: 2em; color: #1a1a1a;">What Our Clients Say</h2>
    <div class="reviews-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
      <div class="review-card" style="background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); transition: transform 0.3s ease;">
        <div style="color: #f59e0b; margin-bottom: 15px; font-size: 1.2rem;"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div>
        <p style="font-style: italic; color: #666; margin-bottom: 20px; line-height: 1.6;">"Absolutely stunning photos! The team captured every beautiful moment perfectly. The attention to detail and professionalism were outstanding. Highly recommended!"</p>
        <div style="font-weight: 600; color: #1a1a1a;">- Priya & Rahul</div>
        <div style="font-size: 0.85rem; color: #999;">Verified Client</div>
      </div>
      <div class="review-card" style="background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); transition: transform 0.3s ease;">
        <div style="color: #f59e0b; margin-bottom: 15px; font-size: 1.2rem;"><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i></div>
        <p style="font-style: italic; color: #666; margin-bottom: 20px; line-height: 1.6;">"Very professional and extremely patient. The quality of the final edited images exceeded all our expectations. We will definitely book again!"</p>
        <div style="font-weight: 600; color: #1a1a1a;">- Ananya S.</div>
        <div style="font-size: 0.85rem; color: #999;">Verified Client</div>
      </div>
    </div>
  </div>
"""
        content = content.replace("<!-- CTA -->", reviews_html + "\n  <!-- CTA -->")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    patched_count += 1

print(f"Patched {patched_count} service files with Reviews and Portfolio links!")
