from playwright.sync_api import sync_playwright
PHOTO=open('redteam_entier.py',encoding='utf-8').read().split('PHOTO=r"""')[1].split('"""')[0]
EMP2=r"""()=>{ const dp=document.getElementById('detailPoster'); return [...dp.querySelectorAll('*')].map((e,i)=>i+' '+e.tagName+'#'+e.id+'|'+(e.getAttribute('class')||'')+'|'+(e.getAttribute('style')||'')); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:160])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(src)=>{ closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; p.photo=src; openDetail(p.id); }", pg.evaluate(PHOTO)); pg.wait_for_timeout(3000)
    print(pg.evaluate("()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const x=dv.left+195, y=dv.top+215; const h=document.elementFromPoint(x,y); const cv=document.getElementById('dpTrameCv'); const r=cv.getBoundingClientRect(); let px=null; try{ px=[...cv.getContext('2d').getImageData(Math.round((x-r.left)*cv.width/r.width), Math.round((y-r.top)*cv.height/r.height),1,1).data]; }catch(e){ px=String(e); } return {h:h&&(h.tagName+'#'+h.id+'.'+h.className), par:h&&h.parentElement&&(h.parentElement.id+'.'+h.parentElement.className), px:px, src:typeof cur!=='undefined'&&!!(cur&&cur.photo), cv:[r.top,r.height,cv.width,cv.height]}; }"))
    a=pg.evaluate(EMP2); pg.wait_for_timeout(1200); c=pg.evaluate(EMP2)
    print('sans rien toucher, en 1,2 s :', [ (x,y) for x,y in zip(a,c) if x!=y][:3])
    b.close()
