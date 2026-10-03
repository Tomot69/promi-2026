from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4000)
    print(pg.evaluate("()=>JSON.stringify({gl:_peloteGLEtat&&_peloteGLEtat(), n:document.getElementById('auBoule').__gl, dispo:PeloteMoteur.glDispo(), err:window._peloteGLErreur||null})"))
    b.close()
