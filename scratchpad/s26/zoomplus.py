from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=3)
    pg.goto('http://127.0.0.1:8752/sauvegardes/app-avant-lot-v12.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(700)
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1800)
        el=pg.query_selector('#createBtn')
        bx=el.bounding_box()
        pg.screenshot(path='scratchpad/s26/PLUS-avant-%s.png'%th, clip={'x':bx['x']-14,'y':bx['y']-14,'width':bx['width']+28,'height':bx['height']+28})
    b.close()
