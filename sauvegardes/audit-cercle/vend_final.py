# L'ÉCRAN QUI VEND, version finale (a543d1e1) — haut et bas, deux thèmes, sous un nom à part (la preuve avait écrasé seuil/).
import os
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vend')
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('light', 'dark'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate("()=>{ closeAll(); document.getElementById('cercleTopBtn').click(); }"); pg.wait_for_timeout(1500)
        clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
        print(th, pg.evaluate("()=>['#buyMonth','#buyYear'].map(q=>getComputedStyle(document.querySelector(q)).borderTopColor)"))
        pg.screenshot(path=os.path.join(OUT, 'final_%s_haut.png' % th), clip=clip)
        pg.evaluate("()=>{const s=document.getElementById('plusScreen'); s.scrollTop=s.scrollHeight;}"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, 'final_%s_bas.png' % th), clip=clip)
        pg.context.close()
    br.close()
