from playwright.sync_api import sync_playwright
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""
C = """()=>{const c=_peloteLumiere.carte(); if(!c) return null; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0,sa=0,mx=0; for(let i=3;i<d.length;i+=4){ if(d[i]){ n++; sa+=d[i]; if(d[i]>mx)mx=d[i]; } } const e=_peloteLumiere.etat(); return {W:c.width, pleins:n, alphaMoy:+(sa/Math.max(1,n)).toFixed(1), alphaMax:mx, cal:e.calibrages, cle:e.cle, cv:document.getElementById('auBoule').width}}"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800); pg.evaluate(OUVRE); pg.wait_for_timeout(5000); print('1', pg.evaluate(C))
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1500); pg.evaluate(OUVRE); pg.wait_for_timeout(3000); print('2', pg.evaluate(C))
    pg.evaluate("()=>{_peloteLumiere.recalibre()}"); pg.wait_for_timeout(2500); print('3 (recalibrée au calme)', pg.evaluate(C))
    b.close()
