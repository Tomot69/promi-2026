import sys, json
from playwright.sync_api import sync_playwright
RAF = r"""async (ms)=>{ const T=[]; let t0=performance.now(), av=t0;
  await new Promise(res=>{ function f(t){ T.push(t-av); av=t; if(t-t0<ms) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
  T.shift(); T.sort((a,b)=>a-b); const q=p=>+T[Math.min(T.length-1,Math.floor(T.length*p))].toFixed(1); return 'n %d p50 %s p95 %s max %s'.replace('%d',T.length).replace('%s',q(.5)).replace('%s',q(.95)).replace('%s',q(1)); }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}"+(";window.__bbz=1" if len(sys.argv)>1 else ""))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4500)
    pg.evaluate("()=>{ const M=PeloteMoteur; window.__gl=M.peintGL; window.__cpu=M.peint; window.__halo=window._haloPelote; }")
    for tour in range(3):
        pg.evaluate("()=>{ PeloteMoteur.peintGL=__gl; }"); pg.wait_for_timeout(400)
        print('carte graphique      ', pg.evaluate(RAF, 4000))
        pg.evaluate("()=>{ PeloteMoteur.peintGL=function(){return true}; }"); pg.wait_for_timeout(400)
        print('rien                 ', pg.evaluate(RAF, 4000))
    pg.evaluate("()=>{ PeloteMoteur.peintGL=__gl; }"); pg.wait_for_timeout(400)
    print(pg.evaluate('()=>JSON.stringify(_peloteGLEtat())'))
    b.close()
