import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ localStorage.removeItem('promi_compte'); closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    for i in range(12):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1500)
    c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(1800)
    t=pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, document.elementFromPoint(r.left+r.width/2, r.top+r.height/2).className]; }")
    print('tard', t)
    pg.evaluate("()=>{ window.__log=[]; const o=console.error; window.addEventListener('error', e=>window.__log.push(String(e.message))); }")
    pg.touchscreen.tap(t[0],t[1])
    pg.wait_for_timeout(2600)
    t2=pg.evaluate("()=>{ const e=[...document.querySelectorAll('#accRappelCompte .tard')].pop(); const r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return [r.left+r.width/2, r.top+r.height/2, h&&(h.tagName+'#'+h.id+'.'+h.className+' < '+(h.parentNode&&(h.parentNode.id||h.parentNode.className))+' < '+(h.parentNode&&h.parentNode.parentNode&&(h.parentNode.parentNode.id||h.parentNode.parentNode.className))), document.querySelector('#accRappelCompte .lab').textContent]; }")
    print('second', t2); pg.touchscreen.tap(t2[0],t2[1])
    for k in range(5):
        pg.wait_for_timeout(300)
        print(pg.evaluate("()=>({cls:document.getElementById('accRappelCompte').className, pf:[...document.querySelectorAll('.passage-flaques')].map(c=>(c.id||'')+':'+c.getAttribute('data-mode')+':'+c.getAttribute('data-u')+':'+(c.parentNode&&c.parentNode.id)), panel:!!document.querySelector('#accRappelCompte .onbv-compte'), log:window.__log, c:localStorage.getItem('promi_compte')})"))
    b.close()
