# joignable « Nuée défilée » : au centre de chaque carte du fil, qui est dessus ? v149 contre v148, même session.
import sys
from playwright.sync_api import sync_playwright
L = """()=>[...document.querySelectorAll('#dpNueeFil .nf-item, #nfAdd, #cm5Ligne')].map(e=>{ const r=e.getBoundingClientRect(); if(r.width<4||r.height<4) return null; const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); const dm=document.getElementById('dpMain'); return [(e.id||e.className).slice(0,22), Math.round(r.top), h?(h.id||h.className).toString().slice(0,20):null, (h===e||e.contains(h)), dm?getComputedStyle(dm).zIndex+'/'+Math.round(dm.getBoundingClientRect().top)+'-'+Math.round(dm.getBoundingClientRect().bottom):null]; }).filter(Boolean)"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in ('app.html', 'zz-av148.html'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + f); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{ if(window._nueeDefile) window._nueeDefile(true); },900);}"); pg.wait_for_timeout(3500)
        print(f); [print('  ', x) for x in pg.evaluate(L)]
        ctx.close()
    b.close()
