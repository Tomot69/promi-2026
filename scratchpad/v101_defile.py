import sys
from playwright.sync_api import sync_playwright
M=r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390; const Y=v=>+((v-D.top)/k).toFixed(1);
 const enc=e=>{const rg=document.createRange();rg.selectNodeContents(e);return rg.getBoundingClientRect();};
 const o=[]; const cv=document.getElementById('dpTrameCv'); if(cv) o.push(['bande bas',Y(cv.getBoundingClientRect().bottom)]);
 ['dptNat','dptTitre','dptQuand'].forEach(id=>{const e=document.getElementById(id); if(e&&getComputedStyle(e).display!=='none'){const r=enc(e); o.push([id,Y(r.top),Y(r.bottom)]);}});
 const c=[...document.querySelectorAll('#dpNueeFil .nf-item')].filter(e=>e.getBoundingClientRect().height>2)[0]; if(c){const r=c.getBoundingClientRect(); o.push(['1re carte',Y(r.top),Y(r.bottom)]);}
 const a=document.getElementById('nfAdd'); return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for app in sys.argv[1:]:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/'+app); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll();openEssaim('potager');}"); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{window._nueeDefileEtat=1; if(window._ficheNuee) window._ficheNuee();}"); pg.wait_for_timeout(1200)
        print(app, pg.evaluate(M)); pg.close()
    b.close()
