import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
def bleu(c): return abs(c[0]-130)<30 and abs(c[1]-174)<30 and abs(c[2]-248)<30
def mes(pg):
    im=image(pg); px=im.load(); xs=[];ys=[]
    for y in range(0,844,2):
        for x in range(0,390,2):
            if bleu(px[x,y]): xs.append(x); ys.append(y)
    return [min(xs),max(xs),min(ys),max(ys)] if xs else None
L="()=>{var l=Toile_lecture();return JSON.stringify({vue:l.vue,g:l.graines.filter(g=>g.kind!=='gray').map(g=>({x:Math.round(g.x),y:Math.round(g.y),w:g.w,b:g.boite}))})}"
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); pg=ouvre(ctx)
    pg.evaluate("(m)=>{try{setPremium(true)}catch(e){} Toile.setTheme(m)}",'ritournelle'); pg.wait_for_timeout(1500)
    plante(pg,'boire un verre'); pg.wait_for_timeout(3000); print('planté',pg.evaluate(L),'matière écran',mes(pg))
    pg.reload(); pg.wait_for_timeout(7000); print('rechargé',pg.evaluate(L),'matière écran',mes(pg))
    pg.wait_for_timeout(5000); print('rechargé+5s',pg.evaluate(L),'matière écran',mes(pg))
    b.close()
