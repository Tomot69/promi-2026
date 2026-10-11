import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b, stockage={'promi_murs':'{"n":3,"t":%d,"der":2,"decouvert":1}'%(__import__('time').time()*1000)}); pg=ouvre(ctx,F)
    print('premium?',pg.evaluate("()=>typeof isPremium!=='undefined'?isPremium:null"))
    r=tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(6000)
    print('studio', pg.evaluate("()=>document.getElementById('studioScreen').className"))
    capture(pg,'scratchpad/v142/m1-0.png')
    for k in range(14):
        print(k, glisse(pg, droite((320,300),(80,300),10), pas=16)); pg.wait_for_timeout(1600)
        cl=pg.evaluate("()=>document.getElementById('studioScreen').className")
        if 'world-locked' in cl: break
    print(cl); pg.wait_for_timeout(2500); capture(pg,'scratchpad/v142/m1-1.png')
    print(pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; return [...document.querySelectorAll('#studioScreen *')].filter(e=>{const f=getComputedStyle(e).filter; return f&&f.indexOf('blur')>=0&&e.getBoundingClientRect().height>2}).map(e=>{const r=e.getBoundingClientRect(); return (e.id||e.className.slice(0,20))+' '+getComputedStyle(e).filter+' ['+[r.left-dv.left,r.top-dv.top,r.width,r.height].map(v=>Math.round(v/k)).join(',')+']'}).join(' | ') }"""))
    LEVE="()=>{ const m=document.getElementById('murPhrase'); const r=m&&m.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; return {leve:!!(m&&m.classList.contains('leve')), offre:!!document.querySelector('#plusScreen.show'), y:m&&r?Math.round((r.top+r.height/2-dv.top)/k):null, tx:m?m.textContent.slice(0,30):''}; }"
    for (x,y) in [(195,200),(100,350),(300,450),(195,540),(60,620),(330,620),(195,670),(100,724),(300,724),(195,782),(195,760),(30,600),(360,690),(195,160),(195,500)]:
        sous=pg.evaluate("([x,y])=>{const d=document.getElementById('device').getBoundingClientRect(),k=d.width/390; return document.elementsFromPoint(d.left+x*k,d.top+y*k).slice(0,4).map(e=>e.id||(''+e.className).slice(0,16)||e.tagName).join(' < ')}",[x,y])
        tap(pg,x,y); pg.wait_for_timeout(700); e=pg.evaluate(LEVE); capture(pg,'scratchpad/v142/m1-t%d-%d.png'%(x,y)); print((x,y), e, '|', sous)
        pg.evaluate("()=>{ try{ _murBaisse(); }catch(e){} const c=document.querySelector('#plusScreen.show .closeb'); if(c) c.click(); }"); pg.wait_for_timeout(450)
    b.close()
