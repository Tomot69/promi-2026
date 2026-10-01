# Q210 · les degrés d'assombrissement du sol, VUS — une capture par degré, même page, même vue figée.
import sys, os
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/app.html'
OUT=os.path.dirname(os.path.abspath(__file__))
DEGRES=[1.00, 0.65, 0.50, 0.28]
with sync_playwright() as p:
    br=p.chromium.launch()
    pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL, timeout=300000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(120):
        pg.wait_for_timeout(250)
        e=pg.evaluate("()=>window._aura?_aura.etat():null")
        if e and e['pret'] and e['frames']>20: break
    pg.wait_for_timeout(800)
    pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.32);}"); pg.wait_for_timeout(800)
    nat=pg.evaluate("()=>(window._auraComp||{}).sol")
    clip=pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
    for d in DEGRES:
        sol=None if d==1.0 else [int(round(nat[i]*d)) for i in range(3)]
        pg.evaluate("(c)=>_aura.regleSol(c)", sol); pg.wait_for_timeout(1800)
        f=os.path.join(OUT,'sol_%03d.png'%int(d*100))
        pg.screenshot(path=f, clip=clip); print('%s  sol %s' % (os.path.basename(f), sol or ('la nature %s'%nat)))
    pg.evaluate("()=>_aura.regleSol(null)")
    br.close()
