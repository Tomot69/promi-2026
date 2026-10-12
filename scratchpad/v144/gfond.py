import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for k in range(4):
        ctx=B.contexte(b, sombre=True); pg=B.ouvre(ctx)
        r=pg.evaluate("""async ()=>{ const L=[]; const f=window._rendDalle; window._rendDalle=function(id,a,b,o,fond){ const t=performance.now(); try{ return f.apply(this,arguments); } finally{ L.push(['rendDalle',fond?'fond':'direct',Math.round(t-T0),Math.round(performance.now()-t), (new Error().stack||'').split('\\n').slice(2,5).map(s=>s.trim().slice(0,70)).join(' < ')]); } };
          const T0=performance.now(); _guide.montre('studio'); await new Promise(r=>setTimeout(r,2300)); return [L, window._evolRecente(4000), window._tEvol>0]; }""")
        print(k, r); ctx.close()
    b.close()
