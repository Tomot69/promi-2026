import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(600)
        print(th, pg.evaluate(r"""()=>{const b=document.getElementById('createBtn'); if(!b) return 'pas de +';
          const z=b.closest('.acc-barre')||b.parentElement;
          const out=[]; (z.querySelectorAll('svg *')||[]).forEach(e=>{
            const s=(e.getAttribute('stroke')||'').toUpperCase(), f=(e.getAttribute('fill')||'').toUpperCase();
            const r=e.getBoundingClientRect(); if(r.width<1) return;
            if(s&&s!=='NONE') out.push(['trait',s,e.getAttribute('stroke-width')]);
            if(f&&f!=='NONE') out.push(['fill',f]);});
          return out;}"""))
    b.close()
