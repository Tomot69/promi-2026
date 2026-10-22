import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('redteam_toile_stable.py').read().split('res = []')[1].split('with sync_playwright()')[0].replace('def juge','def _j'))
W=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1] else []
with sync_playwright() as p:
    br=p.webkit.launch(); ctx=B.contexte(br, stockage={'promi_monde':'ramage'}); B.toile_pleine(ctx,25); pg=B.ouvre(ctx,'app.html',q='?nosilh=1')
    pg.evaluate("m=>{ try{setPremium(true)}catch(e){} if(Toile.getTheme()!==m) Toile.setTheme(m); }", 'ramage'); pg.wait_for_timeout(3000)
    pg.evaluate("W=>{ const id=promises.find(p=>!p.draft).id; const M=Toile.mondeCourant(); W.forEach(w=>window._rendDalle(id,64,64,{monde:{m:w,p:M.p,h:M.h}})); }", W); pg.wait_for_timeout(1500)
    a=pg.evaluate(GEO); page(pg,'studio'); b=pg.evaluate(GEO); print(W, ecart(a,b))
    br.close()
