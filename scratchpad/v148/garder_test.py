import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ETAT = "()=>{ const g=document.querySelector('#createSheet .pp-garder'), cs=document.getElementById('createSheet'); if(!g) return null; const r=g.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {vis:getComputedStyle(g).display!=='none' && r.width>4, inactif:g.classList.contains('inactif'), y:Math.round((r.top-D.top)/k), col:getComputedStyle(g).color, deco:getComputedStyle(g).textDecorationLine, hint:[...cs.querySelectorAll('.ph-hint')].filter(h=>getComputedStyle(h).display!=='none'&&h.getBoundingClientRect().height>0).map(h=>h.textContent)}; }"
with sync_playwright() as p:
    b=p.webkit.launch()
    for k in ('promi','chiche','nuee'):
        ctx=B.contexte(b); pg=B.ouvre(ctx)
        B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=%s]'%k); pg.wait_for_timeout(2600)
        e0=pg.evaluate(ETAT)
        n0=pg.evaluate("()=>promises.filter(p=>p.draft).length")
        B.tap_sel(pg,'#createSheet .pp-garder'); pg.wait_for_timeout(900)
        e1=pg.evaluate(ETAT); ouv=pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"); n1=pg.evaluate("()=>promises.filter(p=>p.draft).length")
        print(k, 'ouverture', e0, '| toucher inactif → page ouverte', ouv, 'gardés', n0, n1)
        b.close() if False else None
        ctx.close()
    b.close()
