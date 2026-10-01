from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{var ps=document.getElementById('plusScreen'); ps.classList.add('show'); if(window.buildCercleHero)buildCercleHero(); if(window.drawCercleHero)drawCercleHero();}")
        pg.wait_for_timeout(2600)
        open('scratchpad/s26/cercle-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(900)
        # studio + panneau palettes
        pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{var s=document.getElementById('studioScreen'); s.classList.add('stp-pals'); if(window._studioRetour)window._studioRetour();}")
        pg.wait_for_timeout(1400)
        open('scratchpad/s26/studiopals-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        print(th, json.dumps(pg.evaluate(r"""()=>{
          var b=document.querySelector('.stp-retour'), pl=document.getElementById('stpPals');
          var cs=b?getComputedStyle(b):null, cp=pl?getComputedStyle(pl):null;
          return {btn:cs?{color:cs.color,fill:cs.webkitTextFillColor,border:cs.borderTopColor}:null,
                  panel:cp?{bg:cp.backgroundColor,border:cp.borderTopColor}:null,
                  classes:document.getElementById('studioScreen').className,
                  nPals:document.querySelectorAll('#stpPals .st3-p').length};
        }"""),ensure_ascii=False))
        pg.evaluate("()=>{closeAll(); var s=document.getElementById('studioScreen'); s.classList.remove('stp-pals');}"); pg.wait_for_timeout(600)
    b.close()
