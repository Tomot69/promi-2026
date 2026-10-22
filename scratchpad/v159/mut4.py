import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':'ramage'}); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,'app.html',attente=1500)
    pg.evaluate("m=>{ try{setPremium(true)}catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", 'ramage')
    G=[]
    for i in range(int(sys.argv[1]) if len(sys.argv)>1 else 12):
        pg.wait_for_timeout(1000); G.append(pg.evaluate(GEO)); print(i, pg.evaluate("()=>[window._silhouettes&&window._silhouettes().length, Toile_state().running, (Toile.semisNeuf&&Toile.semisNeuf())]"), ecart(G[0],G[-1])[0][:60])
    a=G[-1]; page(pg,'studio'); b=pg.evaluate(GEO); print('studio', ecart(a,b)); page(pg,'aura'); b=pg.evaluate(GEO); print('studio', ecart(a,b))
    br.close()
