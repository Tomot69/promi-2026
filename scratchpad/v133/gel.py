import re, sys
from playwright.sync_api import sync_playwright
POINTS=re.search(r'POINTS=r"""(.*?)"""', open('redteam_toucher.py',encoding='utf-8').read(), re.S).group(1)
M=['encre','touffe','brouillamini','halin','esquille','mosaique','braille','pixel','ramage','guingois','chantourne','volubilis','madrure','chamade','ritournelle','bobinette','mascaret','terrazzo','gravure','sillons']
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("""()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){}
      window.__g={max:0,n:0,t:0}; let der=performance.now(); (function f(){ const t=performance.now(); const d=t-der; der=t; if(window.__g.on){ window.__g.n++; if(d>window.__g.max) window.__g.max=d; } requestAnimationFrame(f); })();
      document.addEventListener('pointerdown',()=>{ window.__g={max:0,n:0,on:1}; },true); }""")
    for m in M:
        pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m);}", m); pg.wait_for_timeout(5000)
        P=pg.evaluate(POINTS); q=P['pts'][0]
        pg.mouse.move(q['x'],q['y']); pg.mouse.down(); pg.wait_for_timeout(600)       # doigt POSÉ, sans lever : ce que le toucher déclenche
        g=pg.evaluate("()=>window.__g"); pg.mouse.up(); pg.wait_for_timeout(900); pg.evaluate("()=>{try{closeAll()}catch(e){}}")
        print('%-13s doigt posé 600 ms : %3d images, la plus longue %4d ms'%(m, g['n'], g['max']), flush=True)
    b.close()
