import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=False); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, 'app.html', q='?veille=5', attente=3000)
    print('à 3 s', pg.evaluate("()=>_veille().active"))
    pg.wait_for_timeout(5000); v = pg.evaluate("()=>_veille()"); print('à 8 s', {k: v[k] for k in ('active','depuis','couleurs','logo','bornes','tons')})
    B.capture(pg, 'scratchpad/v161/veille-1.png')
    pg.wait_for_timeout(15000); v = pg.evaluate("()=>_veille()"); print('à 23 s', v['rebonds'], 'rebonds', v['couleurs'], v['logo'])
    B.tap(pg, 195, 760); pg.wait_for_timeout(1500)
    print('après le toucher', pg.evaluate("()=>[_veille().active, document.getElementById('createSheet')&&document.getElementById('createSheet').classList.contains('show'), _veille().derniere]"))
    print('erreurs', pg.erreurs[:3]); b.close()
