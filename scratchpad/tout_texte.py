from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for js in ["()=>document.getElementById('souffleBtn').click()","()=>ouvreCercle()","()=>document.getElementById('settingsBtn').click()"]:
        pg.evaluate("()=>closeAll()"); pg.evaluate(js); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const o=new Set();const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.parentElement.closest('script,style'))continue;const t=n.textContent.replace(/\\s+/g,' ').trim();if(/Nu[ée]e|NU[ÉE]E|Cercle|CERCLE/.test(t))o.add(t.slice(0,160));}return [...o]}""")
    for t in r: print(t)
