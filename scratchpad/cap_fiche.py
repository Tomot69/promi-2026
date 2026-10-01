from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee)||promises[0]; openDetail(p.id);}")
    pg.wait_for_timeout(2600)
    open('scratchpad/fiche-apres.png','wb').write(pg.query_selector('#device').screenshot())
    b.close()
