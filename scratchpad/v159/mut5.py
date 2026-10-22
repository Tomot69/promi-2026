import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
Q=sys.argv[1] if len(sys.argv)>1 else ''
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':'ramage'}); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,'app.html',q=Q)
    pg.evaluate("m=>{ try{ setPremium(true); }catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", 'ramage'); pg.wait_for_timeout(2800)
    a=pg.evaluate(GEO); print('silh', pg.evaluate("()=>window._silhouettes&&window._silhouettes()"))
    for k in range(4):
        pg.wait_for_timeout(1500); c=pg.evaluate(GEO); print('attente', k, ecart(a,c)[0][:50])
    a=c; page(pg,'studio'); b=pg.evaluate(GEO); print('studio', ecart(a,b))
    br.close()
