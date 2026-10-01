import sys
from playwright.sync_api import sync_playwright
URL=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000)
    S="()=>[...document.querySelectorAll('.screen.show')].map(e=>e.id+':'+Math.round(e.getBoundingClientRect().top))"
    for js in ["()=>document.getElementById('settingsBtn').click()", "()=>document.getElementById('souffleBtn').click()", "()=>document.getElementById('indexBtn').click()"]:
        pg.evaluate("()=>closeAll()"); pg.evaluate(js); pg.wait_for_timeout(700); print(js[25:40], pg.evaluate(S))
    pg.evaluate("()=>{closeAll()}"); pg.wait_for_timeout(700); print('closeAll',pg.evaluate(S))
    pg.evaluate("()=>{document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700); print('create',pg.evaluate(S))
