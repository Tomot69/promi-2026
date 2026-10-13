import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    print(pg.evaluate("()=>promises.map(p=>({t:p.title,who:p.who,avec:p.avec,from:p.from,ch:!!p.chiche,req:!!p.req,nu:p.nuee,st:p.status,T:window._parts.tenants(p)})).filter(x=>x.T.length>1||['faire les crêpes','nager le mardi','courir dimanche'].indexOf(x.t)>=0)"))
    for t in ('faire les crêpes','nager le mardi','courir dimanche'):
        pg.evaluate("(t)=>{ try{closeAll()}catch(e){} openDetail(promises.find(q=>q.title===t).id); }", t); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const b=document.querySelector('#segStatus button[data-st=tenu]'); if(b) b.click(); }"); pg.wait_for_timeout(4500)
        print(t, pg.evaluate("(t)=>{ var p=promises.find(q=>q.title===t); return [p.status, JSON.stringify(p.parts||null), document.getElementById('dptEtat')&&document.getElementById('dptEtat').textContent]; }", t))
    b.close()
