from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('zz-av146.html','app.html'):
        for th in ('light','dark'):
            ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s');}catch(e){}"%th)
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
            pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500)
            r=pg.evaluate("()=>{ const s=document.getElementById('createSheet'); return [s.className.slice(0,80), getComputedStyle(s).backgroundColor, document.getElementById('device').className.slice(0,60), !!document.querySelector('#accChoix.ouvert')]; }")
            pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
            r2=pg.evaluate("()=>{ const c=document.querySelector('#indexList .s4-carte'); const et=c&&c.querySelector('.s4-et'); return [c&&c.textContent.replace(/\\s+/g,' ').slice(0,40), et&&getComputedStyle(et).color, et&&et.getAttribute('style')]; }")
            print(f, th, r, r2); ctx.close()
    b.close()
