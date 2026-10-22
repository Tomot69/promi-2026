import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
F=sys.argv[1]; M=sys.argv[2]; ATT=int(sys.argv[3]); N=int(sys.argv[4]) if len(sys.argv)>4 else 25
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':M}); B.toile_pleine(ctx,N); pg=B.ouvre(ctx,F,q='?nosilh=1')
    pg.evaluate("m=>{ try{setPremium(true)}catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", M); pg.wait_for_timeout(3000)
    a=pg.evaluate(GEO)
    B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2200)
    for s in (-1, -1, -1, 1, 1, 1):
        x0, x1 = (300, 90) if s > 0 else (90, 300)
        B.glisse(pg, B.droite([x0, 420], [x1, 420], 10), pas=16); pg.wait_for_timeout(ATT)
    pg.wait_for_timeout(1500); B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(3500)
    b=pg.evaluate(GEO); print(F, M, ATT, ecart(a,b))
    br.close()
