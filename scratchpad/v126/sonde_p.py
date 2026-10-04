from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{window.__pp={}; document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    for k,v in pg.evaluate("()=>window.__pp").items(): print(v, k[:230])
    print(pg.evaluate("()=>JSON.stringify(Toile.fondToile())"))
    b.close()
