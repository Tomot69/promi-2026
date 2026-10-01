from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setPremium(false)}")
    for sy in (0,500,900):
      for y in range(120,900,40):
        pg.evaluate("()=>{localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now(),der:2,decouvert:1}));closeAll();window._murBaisse&&_murBaisse();document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(500)
        pg.evaluate("y=>document.getElementById('stScroll').scrollTop=y",sy); pg.wait_for_timeout(150)
        h=pg.evaluate("y=>{const e=document.elementFromPoint(215,y);return e?(e.id+'.'+(e.className||'')+' '+(e.textContent||'').trim().slice(0,25)):''}",y)
        pg.touchscreen.tap(215,y); pg.wait_for_timeout(500)
        st=pg.evaluate("()=>({leve:!!document.querySelector('#murPhrase.leve'),offre:document.getElementById('plusScreen').classList.contains('show'),scr:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')})")
        if st['offre'] or st['leve']: print(sy,y,h,st)
