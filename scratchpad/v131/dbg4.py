from playwright.sync_api import sync_playwright
E=r"""()=>{ const dp=document.getElementById('detailPoster'); return [dp].concat([...dp.querySelectorAll('*')]).map((e,i)=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e);
    return i+' '+e.tagName+'#'+e.id+'.'+(e.getAttribute('class')||'')+'|'+[r.left,r.top,r.width,r.height].map(v=>Math.round(v*2)/2).join(',')+'|'+c.color+'|'+c.backgroundColor+'|'+c.fontFamily.split(',')[0]+'|'+c.fontSize+'|'+c.display+'|'+c.visibility+'|'+c.opacity+'|'+(e.children.length?'':(e.textContent||'').slice(0,30)); }); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}"); pg.wait_for_timeout(3900)
    a=pg.evaluate(E); pg.wait_for_timeout(2500); a2=pg.evaluate(E); print('sans toucher, 2,5 s plus tard :', sum(1 for x,y in zip(a,a2) if x!=y))
    pg.touchscreen.tap(20+195,44+215); pg.wait_for_timeout(1400); c=pg.evaluate(E)
    d=[(x,y) for x,y in zip(a2,c) if x!=y]; print('après le toucher :', len(d))
    for x,y in d[:4]: print('   AV', x[:260]); print('   AP', y[:260])
    b.close()
