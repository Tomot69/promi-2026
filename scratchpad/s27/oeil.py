# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
JOBS=[('fil-clair',"()=>{document.getElementById('filBtn').click();}",3400,'light'),
      ('fil-sombre',"()=>{document.getElementById('filBtn').click();}",3400,'dark'),
      ('chiche-clair',"()=>{openDetail(133);}",3200,'light'),
      ('studio-pals',"()=>{document.getElementById('studioBtn').click();}",3000,'dark'),
      ('reglages',"()=>{document.getElementById('settingsBtn').click();}",2600,'dark')]
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,js,wt,th in JOBS:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        pg.evaluate(js); pg.wait_for_timeout(wt)
        if nom=='studio-pals':
            pg.evaluate("()=>{var s=document.getElementById('studioScreen'); s.classList.add('stp-pals'); if(window._studioRetour)window._studioRetour();}")
            pg.wait_for_timeout(1800)
        open('scratchpad/s27/O-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
        if errs: print(nom,'ERREURS',errs)
        pg.close()
    b.close()
print('ok')
