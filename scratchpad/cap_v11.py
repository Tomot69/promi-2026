from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(500)
    for nom,js in (('accueil',"()=>{closeAll();}"),
                   ('fiche',"()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"),
                   ('reglages',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}")):
        pg.evaluate(js); pg.wait_for_timeout(2600)
        open('scratchpad/v11-%s.png'%nom,'wb').write(pg.query_selector('#device').screenshot())
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5400)
    open('scratchpad/v11-aura.png','wb').write(pg.query_selector('#device').screenshot())
    b.close()
