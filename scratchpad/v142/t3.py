import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); pg=ouvre(ctx)
    pg.evaluate("(m)=>{try{setPremium(true)}catch(e){} Toile.setTheme(m)}",'ritournelle'); pg.wait_for_timeout(1500)
    L="()=>{var l=Toile_lecture();return JSON.stringify({main:window._vueMain,vue:l.vue,cible:l.cible,W:l.W,H:l.H,n:l.graines.length,col:l.graines.filter(g=>g.kind!=='gray').length})}"
    print('départ',pg.evaluate(L))
    for t in ['boire un verre','appeler Mamie']:
        plante(pg,t); pg.wait_for_timeout(3000); print('planté',pg.evaluate(L))
    pg.evaluate("()=>Toile_autoView()"); pg.wait_for_timeout(2500); print('autoView',pg.evaluate(L))
    pg.evaluate("()=>Toile_recadre()"); pg.wait_for_timeout(2500); print('recadre',pg.evaluate(L))
    pg.reload(); pg.wait_for_timeout(7000); print('rechargé',pg.evaluate(L), pg.evaluate("()=>Toile.curWorld&&Toile.curWorld()"))
    capture(pg,'scratchpad/v142/t3-recharge.png')
    b.close()
