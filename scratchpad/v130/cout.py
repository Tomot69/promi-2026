from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ window.__np=0; window.__tp=0; const f=window._tropical; }")
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(2500)
    print('fiche : nœuds', pg.evaluate("()=>document.querySelectorAll('#detailPoster *').length"), '· une passe :', pg.evaluate("()=>{const t=performance.now(); for(let i=0;i<10;i++) window._tropical(); return ((performance.now()-t)/10).toFixed(2)+' ms'}"))
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
    print('Peaufiner ouvert : une passe :', pg.evaluate("()=>{const t=performance.now(); for(let i=0;i<10;i++) window._tropical(); return ((performance.now()-t)/10).toFixed(2)+' ms'}"))
    b.close()
