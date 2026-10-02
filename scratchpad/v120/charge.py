import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for moteur in ('webkit','chromium'):
        b=p.webkit.launch() if moteur=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
        for F,Q in (('zz-v119.html','?nuit=1'),('zz-v119.html','?nuit=0'),('app.html','')):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
            ctx.add_init_script("""try{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');
              window.__mut=0; var _MO=window.MutationObserver; window.MutationObserver=function(cb){ return new _MO(function(a,b){ window.__mut+=a.length; return cb(a,b); }); }; window.MutationObserver.prototype=_MO.prototype;
              var _sp=CSSStyleDeclaration.prototype.setProperty; window.__sp=0; CSSStyleDeclaration.prototype.setProperty=function(){ window.__sp++; return _sp.apply(this,arguments); };}catch(e){}""")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F+Q); pg.wait_for_timeout(7000)
            if moteur=='chromium':
                c=ctx.new_cdp_session(pg); c.send('Emulation.setCPUThrottlingRate',{'rate':4})
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*STUDIO\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}")
            pg.wait_for_timeout(3000)
            r=pg.evaluate("""()=>new Promise(res=>{ const m0=window.__mut, s0=window.__sp; let n=0, pire=0, t0=performance.now(), av=t0; function f(t){ n++; pire=Math.max(pire,t-av); av=t; if(t-t0<4000) requestAnimationFrame(f); else res({images_s:+(n/4).toFixed(1), pire_ms:Math.round(pire), mutations_s:Math.round((window.__mut-m0)/4), setProperty_s:Math.round((window.__sp-s0)/4)}); } requestAnimationFrame(f); })""")
            print(moteur, F+Q, r); ctx.close()
        b.close()
