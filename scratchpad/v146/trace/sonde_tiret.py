# sonde : le tiret de trois rangées au départ d'un fût (étape 27 du juge) — les valeurs de pixel, rangée par rangée
import sys, io, numpy as np; sys.path.insert(0, '../../..')
from playwright.sync_api import sync_playwright
from PIL import Image
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.evaluate("""()=>{ document.getElementById('page').style.display='none'; document.getElementById('barre').style.display='none';
      const s=document.createElement('div'); s.style.cssText='position:fixed;left:0;top:0;width:390px;height:520px;z-index:50;background:#F7F0DE;color:#291547';
      s.innerHTML='<div style="position:absolute;left:24px;top:24px;width:342px"><div id="jT" style="font:700 35px/44px Gilbert;letter-spacing:-1.05px;min-height:44px">Promi planté\\u00a0!</div></div>'; document.body.appendChild(s); }""")
    info = pg.evaluate("""async()=>{ TraceLettres._debug=true; window.c=TraceLettres.trace(document.getElementById('jT'), null, {manuel:true, respecteReduire:false}); await c.pret; return c.glyphes.map(g=>[g.car,g.variante,+g.x.toFixed(2),+g.y.toFixed(2)]); }""")
    print(info)
    for f in (27 / 40.0,):
        pg.evaluate("f=>c.va(f)", f); pg.wait_for_timeout(60)
        im = np.asarray(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 0, 'width': 390, 'height': 100}))).convert('L')).astype(int)
        print(pg.evaluate("()=>JSON.stringify(c.etat())"))
        for y in range(119, 130): print(y, im[y, 480:504].tolist())
        print(pg.evaluate("""()=>{ const cv=c.canevas, r=cv.getBoundingClientRect(), g=cv.getContext('2d'); const x=Math.round((163-r.left)*3), y0=Math.round((40-r.top)*3); const d=g.getImageData(x, y0, 1, 12).data; const a=[]; for(let i=0;i<12;i++) a.push(d[i*4+3]);
           return JSON.stringify({rect:[r.left,r.top,r.width,r.height], w:cv.width, h:cv.height, style:cv.getAttribute('style').slice(-160), alpha:a, y0:y0, dpr:devicePixelRatio}); }"""))
        d = pg.evaluate("()=>{ const d=TraceLettres._derniere; const out=[]; for(let y=0;y<8;y++){ const r=[]; for(let x=4;x<16;x++) r.push(+d.T[y*d.w+x].toFixed(2)); out.push(r); } return {w:d.w,h:d.h,T:out,dep:d.dep,mins:d.mins}; }")
        print(d['w'], d['h'], d['dep'], d['mins']); [print(r) for r in d['T']]
    b.close()
