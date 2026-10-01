from playwright.sync_api import sync_playwright
MB="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/promi-moodboard-H.html"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1000})
    pg.goto('file://'+MB); pg.wait_for_timeout(3500)
    out=pg.evaluate("""()=>{const isF=(e)=>{const s=e.getAttribute('style')||'';
      return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
      const F=[...document.querySelectorAll('div')].filter(isF);
      return F.map((f,i)=>{
        const t=(f.innerText||'').replace(/\\s+/g,' ').trim().slice(0,72);
        return i+' | '+t;});}""")
    for l in out: print(l)
    b.close()
