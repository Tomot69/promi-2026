import sys
from playwright.sync_api import sync_playwright
MS=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in MS:
        pg.evaluate("async(m)=>{Toile.setTheme(m); await new Promise(r=>setTimeout(r,2500)); closeAll(); await new Promise(r=>setTimeout(r,400)); openDetail(promises.filter(p=>!p.draft)[3].id);}", m)
        pg.wait_for_timeout(2500); pg.locator('#device').screenshot(path='fiche_%s.png'%m)
        print(m, pg.evaluate("()=>{const c=document.getElementById('dpTrameCv'); if(!c) return null; const r=c.getBoundingClientRect(); return [Math.round(r.width),Math.round(r.height), c.dataset.matiere||'', Toile.natureDalle? Toile.natureDalle(promises.filter(p=>!p.draft)[3].id):'']}"))
    b.close()
