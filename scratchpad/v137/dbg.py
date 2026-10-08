from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('settingsBtn').click(); window.__ev=[]; ['pointerdown','pointerup','touchstart','touchend','click'].forEach(n=>document.addEventListener(n,e=>window.__ev.push(n+':'+(e.target.id||e.target.className)+':'+e.defaultPrevented),true)); }"); pg.wait_for_timeout(1500)
    bb=pg.evaluate("()=>{const e=document.getElementById('setMention'); e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}}")
    pg.wait_for_timeout(400); pg.touchscreen.tap(bb['x'],bb['y']); pg.wait_for_timeout(600)
    print(pg.evaluate("()=>[window.__ev, localStorage.getItem('promi_dessin_mention'), document.getElementById('setMention').textContent]"))
    b.close()
