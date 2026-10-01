from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(700)
        pg.evaluate("()=>{closeAll(); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2800)
        pg.evaluate("()=>{var s=document.getElementById('studioScreen'); s.classList.add('stp-pals'); if(window._studioRetour)window._studioRetour();}")
        pg.wait_for_timeout(1600)
        open('scratchpad/s26/PALS24-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        pg.evaluate("()=>{closeAll(); document.getElementById('studioScreen').classList.remove('stp-pals');}"); pg.wait_for_timeout(600)
    # la Toile sous chacune des trois neuves
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(600)
    for k in ('truculent','petulant','fantasque'):
        pg.evaluate("(k)=>{closeAll(); window.Toile.setPalette(k);}",k); pg.wait_for_timeout(2600)
        open('scratchpad/s26/TOILE-%s.png'%k,'wb').write(pg.query_selector('#device').screenshot())
    pg.evaluate("()=>{window.Toile.setPalette('signal');}"); pg.wait_for_timeout(600)
    b.close()
print('ok')
