import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=contexte(b, stockage={'promi_murs':'{"n":3,"t":%d,"der":2,"decouvert":1}'%(__import__('time').time()*1000)}); pg=ouvre(ctx)
    tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(6000)
    for k in range(14):
        glisse(pg, droite((320,300),(80,300),10), pas=16); pg.wait_for_timeout(1600)
        if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
    pg.wait_for_timeout(2000); tap(pg,195,640); pg.wait_for_timeout(800)
    print(pg.evaluate("()=>[...document.querySelectorAll('.mur-lu')].map(e=>e.id).join(',')+' | '+['stpTons','stpLab','stpVue','stpDots'].map(i=>{const e=document.getElementById(i); return i+':'+getComputedStyle(e).visibility+':'+(e.parentElement.id||e.parentElement.className)+':'+!!e.closest('#stpBas')}).join(' ')+' | n stpBas '+document.querySelectorAll('#stpBas').length"))
    b.close()
