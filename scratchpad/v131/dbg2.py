from playwright.sync_api import sync_playwright
EMP2=r"""()=>{ const dp=document.getElementById('detailPoster'); return [dp.className+'|'+(dp.getAttribute('style')||'')].concat([...dp.querySelectorAll('*')].map((e,i)=>i+' '+e.tagName+'#'+e.id+'|'+(e.getAttribute('class')||'')+'|'+(e.getAttribute('style')||''))); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}"); pg.wait_for_timeout(3000)
    a=pg.evaluate(EMP2); pg.touchscreen.tap(20+195,44+215); pg.wait_for_timeout(500); c=pg.evaluate(EMP2)
    for x,y in zip(a,c):
        if x!=y: print('AVANT', x[:300]); print('APRÈS', y[:300])
    b.close()
