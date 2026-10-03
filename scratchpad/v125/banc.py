# le temps par image de l'Aura (intervalle entre deux images, 6 s, respiration active), peintre d'origine contre carte graphique
import sys, json
from playwright.sync_api import sync_playwright
MOT = sys.argv[1] if len(sys.argv)>1 else 'webkit'
DSF = int(sys.argv[2]) if len(sys.argv)>2 else 3
JS = r"""async (gl)=>{ window._peloteGL=gl; const cv=document.getElementById('auBoule'); const M=window.PeloteMoteur;
  await new Promise(r=>setTimeout(r,1500));
  const T=[]; let t0=performance.now(), av=t0; const n0=cv.__gl||0;
  await new Promise(res=>{ function f(t){ T.push(t-av); av=t; if(t-t0<6000) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
  T.shift(); T.sort((a,b)=>a-b); const q=p=>+T[Math.min(T.length-1,Math.floor(T.length*p))].toFixed(1);
  return {gl, images:T.length, ips:+(T.length/6).toFixed(1), p50:q(.5), p95:q(.95), max:q(1), peintesGL:(cv.__gl||0)-n0, palier:(window._aura.palier&&window._aura.palier()), err:window._peloteGLErreur||null}; }"""
with sync_playwright() as p:
    b = (p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=DSF)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t); try{ _peloteLumiere.recalibre(); }catch(e){} }", th); pg.wait_for_timeout(600)
        pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
        pg.wait_for_timeout(4500)
        for gl in (False, True):
            print(MOT, th, json.dumps(pg.evaluate(JS, gl), ensure_ascii=False))
        pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(800)
    b.close()
