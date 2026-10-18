# le mot du trait de la page + d'un Chiche reste-t-il à la cote d'un autre nombre de lignes ? (WebKit, 8 ouvertures)
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'; DY = float(sys.argv[2]) if len(sys.argv) > 2 else 7.5
with sync_playwright() as p:
    b=p.webkit.launch(); faux=0
    for essai in range(8):
        ctx=B.contexte(b); pg=B.ouvre(ctx, F)
        B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=chiche]'); pg.wait_for_timeout(3500)
        r=pg.evaluate("()=>{ const e=_ppEcran(), tr=document.querySelector('#createSheet .pp-trace'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=tr.getBoundingClientRect(); return [e.nl, e.base, +((r.top-D.top)/k).toFixed(1)]; }")
        ok = abs(r[2] - (r[1] + 31 + DY)) < 0.6; faux += (not ok); print(essai, r, 'juste' if ok else 'FAUX (attendu %.1f)' % (r[1] + 31 + DY)); ctx.close()
    print(F, faux, 'faux sur 8'); b.close()
