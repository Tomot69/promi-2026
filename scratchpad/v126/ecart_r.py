from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}; window._ramDbgOn=true; window._ramFilmDbg=true;")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(9000)
    print('écart film/base :', json.dumps(pg.evaluate("()=>{try{return window._ramFilmEcart()}catch(e){return String(e)}}"))[:600])
    d=pg.evaluate("()=>(window._ramDbg||[]).slice(0,3)")
    for e in d: print(json.dumps(e)[:700])
    print('ctLog', json.dumps(pg.evaluate("()=>(window._ramCtLog||[]).slice(0,8)"))[:600])
    b.close()
