import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
OU = open('redteam_deplace.py', encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
SUIT = """(sel)=>{ const e=document.querySelector(sel), t0=performance.now(), L=window.__S=[]; (function f(){ const c=getComputedStyle(e), r=e.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); L.push([Math.round(performance.now()-t0), e.classList.contains('show')?1:0, c.opacity, Math.round((r.top-d.top)/(d.width/390)), c.visibility, c.transitionDuration]); if(performance.now()-t0<1400) requestAnimationFrame(f); })(); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
    G = pg.evaluate(OU); pid = list(G)[0]
    pg.evaluate(SUIT, '#detailPoster'); B.tap(pg, G[pid][0], G[pid][1]); pg.wait_for_timeout(1500); L = pg.evaluate('()=>window.__S')
    print('FICHE, ouverture (ms, show, opacité, haut, visibilité, transition) :'); i0=next((i for i,l in enumerate(L) if l[1]),0); print(L[max(0,i0-2):i0+16]); print('   …', L[-1])
    pg.wait_for_timeout(1500)
    pg.evaluate(SUIT, '#detailPoster')
    r = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#detailPoster .closeb, #detailPoster [data-close]')].find(x=>x.getBoundingClientRect().width>4); const q=e.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }")
    pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(1500); L = pg.evaluate('()=>window.__S')
    print('FICHE, fermeture :'); i0=next((i for i,l in enumerate(L) if not l[1]),0); print(L[max(0,i0-2):i0+16]); print('   …', L[-1])
    pg.wait_for_timeout(800)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); pg.evaluate(SUIT, '#createSheet'); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(1500); L = pg.evaluate('()=>window.__S')
    print('PAGE + :'); i0=next((i for i,l in enumerate(L) if l[1]),0); print(L[max(0,i0-2):i0+22]); print('   …', L[-1])
    b.close()
