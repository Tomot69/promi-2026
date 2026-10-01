# Qui prend le fil en WebKit après une plantation ? Chaque rappel > 15 ms est journalisé avec son origine.
import sys
from playwright.sync_api import sync_playwright
M=(sys.argv[1:] or ['ritournelle'])[0]
INIT=r"""(()=>{ const L=window.__longs=[]; const T0={v:0}; window.__t0=T0;
 function wrap(fn,kind,src){ if(typeof fn!=='function') return fn; return function(){ const a=performance.now(); try{ return fn.apply(this,arguments); } finally { const d=performance.now()-a; if(d>15&&T0.v) L.push([Math.round(a-T0.v),Math.round(d),kind,src]); } }; }
 function where(){ const s=(new Error().stack||'').split('\n').slice(2,4).join(' | '); return s.slice(0,220); }
 const st=window.setTimeout; window.setTimeout=function(f,ms){ return st.call(this,wrap(f,'timeout '+ms,where()),ms); };
 const raf=window.requestAnimationFrame; window.requestAnimationFrame=function(f){ if(f&&f.name==='pas'&&T0.v&&!window.__pasPile){ window.__pasPile=(new Error().stack||'').split('\n').slice(1,9).join(' | '); } return raf.call(this,wrap(f,'raf',(f&&f.name)||where())); };
 const MO=window.MutationObserver; window.MutationObserver=function(cb){ return new MO(wrap(cb,'mutation',where())); }; window.MutationObserver.prototype=MO.prototype;
 const ael=EventTarget.prototype.addEventListener; EventTarget.prototype.addEventListener=function(t,f,o){ return ael.call(this,t,(typeof f==='function')?wrap(f,'event '+t,where()):f,o); };
})();"""
JS=r"""async (m)=>{ window.__pl=[]; ['repaint','repaintWorld','preview'].forEach(function(k){ const o=Toile[k]; Toile[k]=function(){ window.__pl.push([k, Math.round(performance.now()-(window.__t0.v||performance.now())), (new Error().stack||'').split('\n').slice(2,7).join(' | ')]); return o.apply(this,arguments); }; }); Toile.setTheme(m); await new Promise(r=>setTimeout(r,2600)); const d=[];
 window.__t0.v=performance.now(); Toile.addPromi(null);
 let t0=performance.now(); await new Promise(res=>{ let n=0; function f(t){ d.push(Math.round(t-t0)); t0=t; if(++n<40) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return {images:d, longs:window.__longs, pile:window.__pl.filter(x=>x[0]!=='repaint'||x[2].indexOf('pas')<0).slice(-6)}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page(); pg.add_init_script(INIT)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ctx.new_cdp_session(pg).send('Emulation.setCPUThrottlingRate',{'rate':4}); r=pg.evaluate(JS,M); print('images',r['images'])
    [print(x) for x in r.get('pile')]
    b.close()
