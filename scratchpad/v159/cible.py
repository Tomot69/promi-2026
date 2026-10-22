import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
M=sys.argv[1]
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':M}); B.toile_pleine(ctx,5); pg=B.ouvre(ctx,'app.html')
    pg.wait_for_timeout(2000)
    R="()=>{var l=Toile_lecture(); return [l.vue.s.toFixed(4), l.cible&&l.cible.s.toFixed(4), Toile_cellules().c.filter(s=>s.kind!=='gray').length, window._vueMain]}"
    print('charge', pg.evaluate(R))
    print('recalc', pg.evaluate("()=>{window._recadreDemande=true;Toile_autoView(); var l=Toile_lecture(); return [l.cible.s.toFixed(4), JSON.stringify(Toile_cellules().c.filter(s=>s.kind!=='gray').map(s=>[s.kind,Math.round(s.x),Math.round(s.y)]))]}"))
    br.close()
