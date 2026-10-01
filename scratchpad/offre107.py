from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        pg.evaluate("t=>{setTheme(t);setPremium(false);closeAll();ouvreCercle()}",th); pg.wait_for_timeout(1800)
        pg.screenshot(path=f'scratchpad/o107_{th}.png')
        print(th, errs, pg.evaluate("()=>{const y=document.getElementById('buyYear'),s=y.querySelector('span');return [s.textContent,s.scrollWidth,y.clientWidth,getComputedStyle(s).whiteSpace]}"))
