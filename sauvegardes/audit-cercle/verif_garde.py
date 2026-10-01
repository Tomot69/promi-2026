# UN GARDÉ DE CÔTÉ : PEAUFINER S'OUVRE-T-IL ? — refait par la BONNE porte.
# verif_mur.py touchait `#dpDetails .dpd-tog` (la barre de la FICHE) : or un gardé de côté n'ouvre pas une fiche, il
# rouvre la PAGE + (openDetail → reprendreBrouillon, l. 9607). La barre touchée était celle d'un écran caché. Ici : on
# rouvre le gardé de côté, puis on touche #csBotBar AU POINT (souris au centre de la barre), deux thèmes.
import os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'mur')
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        g = pg.evaluate("()=>{const d=promises.find(p=>p.draft); return d?d.id:null;}")
        pg.evaluate("(id)=>{ try{closeAll();}catch(e){} openDetail(id); }", g); pg.wait_for_timeout(1800)
        e0 = pg.evaluate("()=>{const cs=document.getElementById('createSheet'); return {classes:cs.className, garde:cs.classList.contains('pp-garde')};}")
        pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_garde_page_plus.png' % th))
        bar = pg.evaluate("""()=>{const b=document.getElementById('csBotBar'); if(!b) return null; const r=b.getBoundingClientRect();
            const x=r.left+r.width/2, y=r.top+r.height/2, h=document.elementFromPoint(x,y);
            return {x, y, vis:b.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}), w:Math.round(r.width), h:Math.round(r.height),
                    recoit: h? (h===b||b.contains(h)?'soi':(h.id||h.className.toString().split(' ')[0])) : null,
                    texte:b.textContent.replace(/\\s+/g,' ').trim().slice(0,40)};}""")
        if bar and bar['vis']:
            pg.mouse.click(bar['x'], bar['y']); pg.wait_for_timeout(1600)
        e1 = pg.evaluate("""()=>{const cs=document.getElementById('createSheet'); const b=cs.querySelector('.s2-cercle');
            const l=[...cs.querySelectorAll('.s2-liste > *')].map(x=>(x.querySelector('.s2-lab')||x).textContent.replace(/\\s+/g,' ').trim().slice(0,30));
            return {peaufiner:cs.classList.contains('pp-peauf'), classes:cs.className, bloc:!!b, lignes:l};}""")
        pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_garde_apres_barre.png' % th))
        print('\n== %s · gardé de côté %s\n  rouvert : %s\n  barre : %s\n  après le toucher : %s' % (th, g, e0, bar, e1))
        ctx.close()
    br.close()
