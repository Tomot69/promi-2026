# Q536 : ce que la classe .tracant change à l'écran d'une fiche (filtre, opacité, transition), élément par élément.
import sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + PAGE); pg.wait_for_timeout(6500)
        r = pg.evaluate("""async ()=>{ const L=promises.filter(x=>!x.draft&&!x.chiche&&!x.nuee&&x.status!=='tenu'); openDetail(L[0].id); await new Promise(r=>setTimeout(r,1500));
          const dp=document.getElementById('detailPoster'); const els=[...dp.querySelectorAll('*')];
          const lit=()=>els.map(e=>{ const c=getComputedStyle(e); return [c.filter, c.opacity]; });
          const a=lit(); dp.classList.add('tracant'); await new Promise(r=>setTimeout(r,700)); const b=lit(); dp.classList.remove('tracant');
          const out=[]; els.forEach((e,i)=>{ if(a[i][0]!==b[i][0]||a[i][1]!==b[i][1]){ const r=e.getBoundingClientRect(); if(r.width>0&&r.height>0) out.push([e.id||e.className.toString().slice(0,30), a[i], b[i]]); } }); return out; }""")
        print(th, len(r)); [print('  ', x) for x in r[:20]]
        ctx.close()
    b.close()
