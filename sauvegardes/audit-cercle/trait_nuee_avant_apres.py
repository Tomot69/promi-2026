# LE TRAIT d'une Nuée, avant / après la bascule — la carte seule, deux thèmes.
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'seuil')
with sync_playwright() as p:
    br = p.chromium.launch()
    for nom, url in (('avant', 'http://127.0.0.1:8752/sauvegardes/app-avant-seuil-pilule.html'), ('apres', 'http://127.0.0.1:8752/app.html')):
        for th in ('dark', 'light'):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(url); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
            pg.evaluate("()=>{ closeAll(); openEssaim('potager'); }"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1800)
            r = pg.evaluate("()=>{ const c=document.getElementById('npTrait'); c.scrollIntoView({block:'center'}); const q=c.getBoundingClientRect(); return {x:q.left-12,y:q.top-12,width:q.width+24,height:q.height+24, R:getComputedStyle(c).borderTopLeftRadius}; }")
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, 'trait_nuee_%s_%s.png' % (nom, th)), clip={k: r[k] for k in ('x', 'y', 'width', 'height')})
            print(nom, th, 'rayon', r['R'])
            pg.context.close()
    br.close()
