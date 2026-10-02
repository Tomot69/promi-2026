from playwright.sync_api import sync_playwright
E = "()=>JSON.stringify({sel:window.newWhoSel||null, fWho:(document.getElementById('fWho')||{}).value, phs:[...document.querySelectorAll('#csPhrase [data-ph]')].map(e=>e.getAttribute('data-ph')+':'+e.textContent.trim().slice(0,14)), gn:[...document.querySelectorAll('#createSheet .gn .ph-o[data-v]')].filter(e=>e.getBoundingClientRect().width>0).map(e=>e.getAttribute('data-v')+(e.classList.contains('on')?'*':'')).slice(0,8), gens:(window._gens&&window._gens.pris)?window._gens.pris():null})"
def c(pg, s):
    return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const q=(getComputedStyle(e).display==='inline'&&e.getClientRects().length)?e.getClientRects()[0]:e.getBoundingClientRect(); return q.width?{x:q.left+q.width/2,y:q.top+q.height/2}:null}", s)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{setTheme('light'); closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2600)
    print('repos', pg.evaluate(E))
    for s in ('#csPhrase [data-ph=qui]', '#csPhrase [data-ph=sens]'):
        q = c(pg, s)
        if q: pg.touchscreen.tap(q['x'], q['y']); pg.wait_for_timeout(1100); print('après', s, pg.evaluate(E)); break
    q = c(pg, '#csPhrase [data-ph=qui]'); pg.touchscreen.tap(q['x'], q['y']); pg.wait_for_timeout(1100); print('après qui', pg.evaluate(E))
    q = c(pg, '#createSheet .gn .ph-o[data-v="Rachel"]')
    if q: pg.touchscreen.tap(q['x'], q['y']); pg.wait_for_timeout(1000); print('après Rachel', pg.evaluate(E))
    b.close()
