import sys, json
from playwright.sync_api import sync_playwright
MOT = sys.argv[1] if len(sys.argv)>1 else 'webkit'
RAF = r"""async (ms)=>{ const T=[]; let t0=performance.now(), av=t0;
  await new Promise(res=>{ function f(t){ T.push(t-av); av=t; if(t-t0<ms) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
  T.shift(); T.sort((a,b)=>a-b); const q=p=>+T[Math.min(T.length-1,Math.floor(T.length*p))].toFixed(1); return {n:T.length, p50:q(.5), p95:q(.95), max:q(1)}; }"""
with sync_playwright() as p:
    b = (p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('accueil', pg.evaluate(RAF, 4000))
    pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
    pg.wait_for_timeout(4500)
    print('aura', pg.evaluate(RAF, 4000))
    pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(500)
    print('aura figée', pg.evaluate(RAF, 4000))
    pg.evaluate("()=>{_aura.fige(false); const M=PeloteMoteur, f=M.peintGL; window.__t=[]; M.peintGL=function(c,o){ const a=performance.now(); const r=f(c,o); __t.push(performance.now()-a); return r; }; const h=window._haloPelote; }")
    print('aura', pg.evaluate(RAF, 4000), pg.evaluate("()=>{const a=__t.sort((x,y)=>x-y); return {n:a.length, p50:a[a.length>>1], p95:a[Math.floor(a.length*.95)]}}"))
    print('copies', pg.evaluate("()=>document.getElementById('auBoule').__copies"))
    pg.evaluate("()=>{ window.__pile=[]; const cv=document.getElementById('auBoule'), g=cv.getContext; cv.getContext=function(t){ if(__pile.length<3) __pile.push(new Error().stack.split('\\n').slice(1,5).join(' | ')); return g.apply(cv,arguments); }; }")
    pg.wait_for_timeout(600); print(pg.evaluate("()=>__pile"))
    pg.evaluate("()=>{ document.getElementById('auBouleGL').style.visibility='hidden'; window._peloteGL=true; }")
    print('GL caché', pg.evaluate(RAF, 4000))
    # sans la copie vers le canevas 2D : on montre le canevas GL à la place
    b.close()
