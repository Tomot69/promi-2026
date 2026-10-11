import sys, time; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=contexte(b, sombre=True, stockage={'promi_murs':'{"n":3,"t":%d,"der":2,"decouvert":1}'%(time.time()*1000)}); pg=ouvre(ctx)
    tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(6000); tap(pg,75,620); pg.wait_for_timeout(1500)
    for k in range(14):
        glisse(pg, droite((320,300),(80,300),10), pas=16); pg.wait_for_timeout(1600)
        if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
    pg.wait_for_timeout(2500); capture(pg,'scratchpad/v142/m5.png')
    for i in range(6):
        print(pg.evaluate("([x,y])=>{const d=document.getElementById('device').getBoundingClientRect(),k=d.width/390; return document.elementsFromPoint(d.left+x*k,d.top+y*k).slice(0,5).map(e=>e.id||(''+e.className).slice(0,16)||e.tagName).join(' < ')}",[69,711]))
        tap(pg,69,711); pg.wait_for_timeout(650)
        print(pg.evaluate("()=>({l:document.getElementById('murPhrase')&&document.getElementById('murPhrase').className, o:!!document.querySelector('#plusScreen.show'), et:JSON.stringify(window._murEtat||null), st:localStorage.getItem('promi_murs')})"))
        pg.evaluate("()=>{ try{ _murBaisse(); }catch(e){} const c=document.querySelector('#plusScreen.show .closeb'); if(c) c.click(); }"); pg.wait_for_timeout(420)
    b.close()
