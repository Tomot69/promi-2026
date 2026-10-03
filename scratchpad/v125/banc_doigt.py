import sys, json
from playwright.sync_api import sync_playwright
RAF = r"""()=>{ window.__T=[]; let av=performance.now(); window.__go=true; (function f(t){ __T.push(t-av); av=t; if(window.__go) requestAnimationFrame(f); })(av); }"""
FIN = r"""()=>{ window.__go=false; const T=__T.slice(2); T.sort((a,b)=>a-b); const q=p=>+T[Math.min(T.length-1,Math.floor(T.length*p))].toFixed(1); return {images:T.length, p50:q(.5), p95:q(.95), max:q(1), touches:document.getElementById('auBoule').__ntch}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(4500)
    bo=pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left+r.width*0.4, r.top+r.height*0.5]}")
    for gl in (False, True, False, True):
        pg.evaluate("(g)=>{window._peloteGL=g}", gl); pg.wait_for_timeout(600)
        pg.mouse.move(bo[0],bo[1]); pg.mouse.down(); pg.evaluate(RAF)
        for i in range(60): pg.mouse.move(bo[0]+i*1.2, bo[1]+(i%7)); pg.wait_for_timeout(40)
        r=pg.evaluate(FIN); pg.mouse.up(); print('doigt posé et glissé ·', 'carte graphique' if gl else 'peintre d\'origine', json.dumps(r)); pg.wait_for_timeout(1500)
    b.close()
