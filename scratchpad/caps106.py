from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        pg.evaluate("t=>{setTheme(t);setPremium(false);localStorage.setItem('promi_murs',JSON.stringify({n:2,t:Date.now(),der:1,decouvert:1}))}",th)
        pg.evaluate("()=>{closeAll();ouvreCercle()}"); pg.wait_for_timeout(1800); pg.screenshot(path=f'scratchpad/c106_offre_{th}.png')
        pg.evaluate("()=>{closeAll();const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0];openDetail(p.id)}"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
        c=pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        pg.touchscreen.tap(*c); pg.wait_for_timeout(900); pg.screenshot(path=f'scratchpad/c106_mur_{th}.png')
        print(pg.evaluate("()=>{const p=document.getElementById('murPhrase');const s=getComputedStyle(p);return [p.textContent,s.fontFamily,s.fontSize]}"))
        pg.evaluate("()=>{_murBaisse();closeAll();setPremium(true);document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(1500); pg.screenshot(path=f'scratchpad/c106_reg_paye_{th}.png')
        pg.evaluate("()=>{closeAll();setPremium(false);document.getElementById('indexBtn').click()}"); pg.wait_for_timeout(2500); pg.screenshot(path=f'scratchpad/c106_index_{th}.png')
        ctx.close()
