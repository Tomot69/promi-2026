from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
    for r in pg.evaluate("()=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>[...c.querySelectorAll('.s4-et,.s4-eb')].map(e=>e.className+'|'+e.textContent.trim().slice(0,30)+'|'+getComputedStyle(e).color).join(' ;; '))"): print(r)
