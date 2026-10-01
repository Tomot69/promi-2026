from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(700)
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3400)
        open('scratchpad/s26/FIL-%s.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        pg.evaluate("()=>{var l=document.getElementById('feedList'); if(l) l.scrollTop=420;}"); pg.wait_for_timeout(1500)
        open('scratchpad/s26/FIL-%s-bas.png'%th,'wb').write(pg.query_selector('#device').screenshot())
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(700)
    b.close()
