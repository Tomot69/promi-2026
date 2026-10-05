from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(2000)
    pg.evaluate("()=>openDetail(136)"); pg.wait_for_timeout(2200)
    pg.evaluate("()=>{ window.__n=0; const r=window._aura.rafraichit; window._aura.rafraichit=function(){ window.__n++; window.__r=r.apply(this,arguments); return window.__r; }; document.querySelector('#segStatus button[data-st=tenu]').click(); }")
    for t in (100,1100,2500,5000):
        pg.wait_for_timeout(t if t==100 else 1200)
        print(t, pg.evaluate("()=>[window._tenirAnime, window.__n, window.__r, window._instant, document.getElementById('auraScreen').className, [...document.querySelectorAll('#auraScreen .au-mo .au-c span')].map(e=>e.textContent), window._auraErreur]"))
    b.close()
