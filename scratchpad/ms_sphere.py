import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(9000)
    print(pg.evaluate("()=>{const e=_aura.etat();return {palier:e.palier, vise:e.vise, ms:+e.ms.toFixed(2), frames:e.frames};}"))
    # coût du peintre seul
    print(pg.evaluate("""()=>{const t=[];for(let i=0;i<7;i++){const t0=performance.now();_aura.verifie&&0;
      window.__f=window.__f||0; const c=document.getElementById('auBoule');
      t.push(0);} return null;}"""))
    pg.wait_for_timeout(4000)
    print(pg.evaluate("()=>{const e=_aura.etat();return {ms:+e.ms.toFixed(2), dernier:+e.dernier.toFixed(2), palier:e.palier};}"))
    b.close()
