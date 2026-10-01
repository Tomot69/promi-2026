# Le disque « toi » de la rangée de l'Aura : que montre-t-il quand un doigt le touche ?
import sys, os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(sys.argv[1]); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(600)
    pt = pg.evaluate("""()=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()==='toi'); if(!lb) return null; const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
        for(const n of document.querySelectorAll('#auraScreen .au-nb')){ const r=n.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""")
    print('disque « toi » :', pt)
    if pt:
        pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1500)
        print(pg.evaluate("""()=>{ const sh=document.getElementById('personSheet'); return JSON.stringify({ouvre:window._auraOuvre, show:sh.classList.contains('show'),
          nom:(document.getElementById('psName')||{}).textContent, sub:(document.getElementById('psSub')||{}).textContent, liste:(document.getElementById('psList')||{}).textContent.slice(0,80)}); }"""))
        dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
        pg.screenshot(path=os.path.join(sys.argv[2], 'var-dark-toi-au-doigt.png'), clip={'x': dev[0], 'y': dev[1], 'width': dev[2], 'height': dev[3]})
    b.close()
