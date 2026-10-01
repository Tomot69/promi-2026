import sys
from playwright.sync_api import sync_playwright
MB="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/promi-moodboard-H.html"
i=int(sys.argv[1])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1000})
    pg.goto('file://'+MB); pg.wait_for_timeout(3000)
    h=pg.evaluate("""(i)=>{const isF=(e)=>{const s=e.getAttribute('style')||'';
      return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
      const F=[...document.querySelectorAll('div')].filter(isF);
      return F[i]?F[i].outerHTML:'ABSENT';}""", i)
    print(h)
    b.close()
