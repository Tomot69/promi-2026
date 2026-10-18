# §8 : la page + avec un choix ouvert (la personne) — qu'y a-t-il à droite, vers 708 ? « garder de côté » forcé visible, capture.
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, dsf=2); pg = ouvre(ctx)
    tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2400)
    tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(1000); tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1300)
    r = pg.evaluate("""()=>{ const cs=document.getElementById('createSheet'); const g=cs.querySelector('.pp-garder'); g.style.setProperty('display','block','important'); const L=[]; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
      for(const y of [690,700,708,716,724]) for(const x of [250,300,340,360]){ const e=document.elementFromPoint(D.left+x*k, D.top+y*k); L.push([x,y,e?(e.id||e.className||e.tagName):null]); } return {ouvert:cs.classList.contains('pp-ouvert'), L:L}; }""")
    print(r['ouvert']); [print(x) for x in r['L']]
    capture(pg, 'scratchpad/v149/garder_ouvert.png'); b.close()
