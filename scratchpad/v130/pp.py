from playwright.sync_api import sync_playwright
Q="()=>[...document.querySelectorAll('#createSheet #csPhrase *')].filter(e=>e.children.length===0&&e.textContent.trim()&&e.getBoundingClientRect().width>2).map(e=>e.textContent.trim().slice(0,14)+':'+getComputedStyle(e).color+':'+(e.getAttribute('data-trop')||'-')+':'+e.style.getPropertyPriority('color')+':'+e.tagName+'.'+e.className).join(' | ')"
with sync_playwright() as p:
    b=p.webkit.launch()
    for i in range(3):
        ctx=b.new_context(viewport={'width':430,'height':932})
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600)
        print(pg.evaluate(Q)[:700]); print('  passe manuelle →', pg.evaluate("()=>window._tropical()"), '|', pg.evaluate(Q)[:300])
        ctx.close()
    b.close()
