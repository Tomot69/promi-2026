import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
OU=open('redteam_deplace.py',encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b,gestes_vus=False); pg=ouvre(ctx)
    plante(pg,'rendre le livre'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ window.__t={}; (function f(){ const n=performance.now(), dp=document.getElementById('detailPoster'), g=document.getElementById('gesteFantome'); if(dp&&dp.classList.contains('show')&&!__t.show) __t.show=n; if(dp&&dp.classList.contains('show')&&!__t.vis){ const r=dp.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); if(Math.abs(r.top-d.top)<4 && +getComputedStyle(dp).opacity>0.99) __t.vis=n; } if(g&&g.children.length&&getComputedStyle(g).display!=='none'&&!__t.main) __t.main=n; requestAnimationFrame(f); })(); document.addEventListener('touchend',()=>{ if(!__t.tap) __t.tap=performance.now(); },true); }")
    G=pg.evaluate(OU); a=list(G)[0]; tap(pg,G[a][0],G[a][1]); pg.wait_for_timeout(4500)
    t=pg.evaluate("()=>__t"); print({k:round(v-t['tap']) for k,v in t.items()}); b.close()
