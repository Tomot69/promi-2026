import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        for nom,js,wt in (('accueil',"()=>{closeAll();}",1800),
                       ('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}",3000),
                       ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}",3000),
                       ('cercle',"()=>{closeAll(); var ps=document.getElementById('plusScreen'); ps.classList.add('show'); if(window.buildCercleHero)buildCercleHero();}",3000)):
            pg.evaluate(js); pg.wait_for_timeout(wt)
            open('scratchpad/s26/%s-%s.png'%(nom,th),'wb').write(pg.query_selector('#device').screenshot())
    b.close()
print("ok")
