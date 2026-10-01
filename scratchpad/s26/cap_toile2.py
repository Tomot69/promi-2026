from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(700)
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1500)
    for k in ('truculent','petulant','fantasque'):
        pg.evaluate("(k)=>{window.Toile.setPalette(k);}",k); pg.wait_for_timeout(3000)
        open('scratchpad/s26/T2-%s.png'%k,'wb').write(pg.query_selector('#device').screenshot())
    pg.evaluate("()=>{window.Toile.setPalette('signal');}"); pg.wait_for_timeout(800)
    b.close()
print('ok')
