from playwright.sync_api import sync_playwright
PHOTO=open('redteam_entier.py',encoding='utf-8').read().split('PHOTO=r"""')[1].split('"""')[0]
EMP2=r"""()=>{ const dp=document.getElementById('detailPoster'); return [...dp.querySelectorAll('*')].map((e,i)=>i+' '+e.tagName+'#'+e.id+'|'+(e.getAttribute('class')||'')+'|'+(e.getAttribute('style')||'')+'|'+(e.children.length?'':(e.textContent||'').slice(0,30))); }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for k in range(4):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}", 'dark' if k%2 else 'light'); pg.wait_for_timeout(600)
        pg.evaluate("(src)=>{ closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; p.photo=src; openDetail(p.id); }", pg.evaluate(PHOTO)); pg.wait_for_timeout(3000)
        a=pg.evaluate(EMP2); pg.touchscreen.tap(20+195,44+215); pg.wait_for_timeout(500); pg.touchscreen.tap(20+195,44+600); pg.wait_for_timeout(500); c=pg.evaluate(EMP2)
        d=[(x,y) for x,y in zip(a,c) if x!=y]; print(k, len(d))
        for x,y in d[:2]: print('   AV', x[:330]); print('   AP', y[:330])
        ctx.close()
    b.close()
