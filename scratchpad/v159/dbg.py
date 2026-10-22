import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); toile_pleine(ctx, 10); pg = ouvre(ctx, 'app.html'); pg.evaluate("()=>{try{setPremium(true)}catch(e){}}")
    for k in range(2):
        tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(1800)
        for _ in range(3):
            r=glisse(pg, droite([300,420],[90,420],10), pas=16); pg.wait_for_timeout(900); print(k, r, pg.evaluate("()=>Toile.getTheme()"))
        tap_sel(pg,'#studioScreen .closeb'); pg.wait_for_timeout(1500)
        print('après fermeture', pg.evaluate("()=>{var s=document.getElementById('studioScreen');return [s.classList.contains('show'), s.getBoundingClientRect().top]}"))
    b.close()
