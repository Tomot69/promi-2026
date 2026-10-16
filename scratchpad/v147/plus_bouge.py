import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(650); B.tap_sel(pg,'.acc-pil[data-k=chiche]'); pg.wait_for_timeout(2500)
    B.tap_sel(pg,'#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1000); B.tap_sel(pg,'#createSheet .gn > .ph-add'); pg.wait_for_timeout(500)
    for n in ['Rachel','Marion','Nico']:
        pg.keyboard.type(n,delay=25)
        rs=pg.evaluate("""async()=>{ var out=[]; var d=document.getElementById('device').getBoundingClientRect(),k=d.width/390;
          for(var i=0;i<16;i++){ var e=document.querySelector('#createSheet .gn > .ph-add .gn-plus'); var b=e&&e.getBoundingClientRect();
            var m=document.querySelector('#createSheet [data-gn-tete]'); var mb=m&&m.getBoundingClientRect();
            out.push(b?[Math.round((b.left-d.left)/k),Math.round((b.top-d.top)/k),Math.round(b.width/k)]:null); await new Promise(r=>setTimeout(r,60)); }
          return {plus:out, moi:mb?[Math.round((mb.left-d.left)/k),Math.round((mb.top-d.top)/k),Math.round(mb.width/k),Math.round(mb.height/k)]:null}; }""")
        print(n, rs)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(800)
