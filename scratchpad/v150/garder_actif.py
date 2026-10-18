# « garder de côté » est-il actif à l'ouverture, sans rien toucher ? (WebKit, page + Chiche et Promi, 8 ouvertures chacune)
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for nat in ('chiche', 'promi'):
        act=0
        for essai in range(8):
            ctx=B.contexte(b); pg=B.ouvre(ctx, F)
            B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(4000)
            a=pg.evaluate("()=>{ const g=document.querySelector('#createSheet .pp-garder'); return g && !g.classList.contains('inactif'); }"); act+=bool(a); ctx.close()
        print(F, nat, act, 'actif(s) sur 8 sans rien toucher')
    b.close()
