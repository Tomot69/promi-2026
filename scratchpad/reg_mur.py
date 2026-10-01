from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setPremium(false);localStorage.removeItem('promi_murs')}")
    pg.evaluate("()=>{closeAll(); document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(1500)
    L=pg.evaluate("""()=>{const o=[];document.querySelectorAll('#settingsScreen *').forEach(e=>{const f=getComputedStyle(e).filter;if(f&&f.includes('blur')&&e.getClientRects().length){const r=e.getBoundingClientRect();o.push([e.tagName,e.id,e.className,f,Math.round(r.top),Math.round(r.height),getComputedStyle(e).pointerEvents,(e.textContent||'').trim().slice(0,60)])}});return o}""")
    for x in L: print(x)
    locks=pg.evaluate("""()=>[...document.querySelectorAll('#settingsScreen .adv-lock, #settingsScreen [onclick]')].map(e=>[e.className,e.getAttribute('onclick'),e.getClientRects().length?getComputedStyle(e).display:'-'])""")
    print(locks)
