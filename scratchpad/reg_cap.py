from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setPremium(false);localStorage.removeItem('promi_murs')}")
    pg.evaluate("()=>{closeAll(); document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#settingsScreen *')].filter(e=>e.scrollHeight>e.clientHeight+5&&/(auto|scroll)/.test(getComputedStyle(e).overflowY)).map(e=>e.id+'.'+e.className+' '+e.scrollHeight+'/'+e.clientHeight)"""))
    print(pg.evaluate("""()=>[...document.querySelectorAll('#settingsScreen .scard, #settingsScreen .grouplab, #settingsScreen [class*=row]')].map(e=>(e.textContent||'').trim().replace(/\\s+/g,' ').slice(0,50)+' | '+getComputedStyle(e).filter+' | '+getComputedStyle(e).opacity)"""))
