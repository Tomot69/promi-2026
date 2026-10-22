import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
N=int(sys.argv[1]) if len(sys.argv)>1 else 25
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,N)
    ctx.add_init_script("window.__RD=[]; (function w(){ if(window._rendDalle && !window._rendDalle.__w){ const f=window._rendDalle; const g=function(id,a,b2,o){ const t=performance.now(); const r=f.apply(this,arguments); if(a===64&&b2===64) window.__RD.push([(o&&o.monde&&o.monde.m)||'courant', Math.round(performance.now()-t)]); return r; }; g.__w=1; Object.keys(f).forEach(k=>g[k]=f[k]); window._rendDalle=g; } setTimeout(w,100); })();")
    pg=B.ouvre(ctx,'app.html'); pg.wait_for_timeout(25000)
    print(pg.evaluate("()=>window.__RD")); print(pg.evaluate("()=>window._silhouettes&&window._silhouettes().length"))
    b.close()
