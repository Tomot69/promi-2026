# couleur calculée et propriétaire du mot du trait sur les trois pages + (et la fiche, pour comparaison), deux thèmes
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for s in (False, True):
        ctx=B.contexte(b, sombre=s); pg=B.ouvre(ctx, F)
        for k in ('promi','chiche','nuee'):
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(400)
            B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=%s]'%k); pg.wait_for_timeout(2800)
            print('sombre' if s else 'clair ', k, pg.evaluate("""()=>{ const t=document.querySelector('#createSheet .pp-trace'); if(!t) return null; const c=getComputedStyle(t);
              return [t.textContent.trim(), c.color, c.webkitTextFillColor, t.getAttribute('style')||'', t.className]; }"""))
        ctx.close()
    b.close()
