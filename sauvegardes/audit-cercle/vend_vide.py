# L'ÉCRAN QUI VEND SANS AUCUN PROMI — la vraie liste vidée dans la page (le démarrage neuf ne le fait pas : le jeu se remplit
# derrière), puis la porte de l'accueil ; deux thèmes ; capture ; et les portes qui restent visibles dans cet état.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'vend')
exec(open(os.path.join(D, 'portes_vides.py'), encoding='utf-8').read().split("PORTES = [")[0].split("import json, os")[1].replace("from playwright.sync_api import sync_playwright", ""))
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{ promises.length=0; }"); pg.evaluate(BASE); pg.wait_for_timeout(400)
        pt = pg.evaluate(POINT, '#cercleTopBtn'); pg.mouse.click(pt['x'], pt['y']); pg.wait_for_timeout(1400)
        v = pg.evaluate(VIDE); print(th, json.dumps(v, ensure_ascii=False))
        clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
        pg.screenshot(path=os.path.join(OUT, 'vide_%s.png' % th), clip=clip)
        pg.context.close()
    br.close()
