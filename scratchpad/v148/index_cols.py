from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932})
        ctx.add_init_script("try{localStorage.setItem('promi_theme','%s');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');}catch(e){}" % th)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
        r = pg.evaluate("""()=>[...document.querySelectorAll('#indexList .s4-carte')].slice(0,8).map(c=>{ const g=e=>e?getComputedStyle(e).color:null; return [c.querySelector('.s4-ti')&&c.querySelector('.s4-ti').textContent.slice(0,16), getComputedStyle(c).backgroundColor, g(c.querySelector('.s4-natlab')), g(c.querySelector('.s4-et')), c.querySelector('.s4-et')&&c.querySelector('.s4-et').textContent.slice(0,12)]; })""")
        print(th); [print('  ', x) for x in r]
        ctx.close()
    b.close()
