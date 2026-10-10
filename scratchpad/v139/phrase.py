import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','bande'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1'));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for t in ('faire les crêpes','planter un arbre','courir dimanche','planter un arbre','faire les crêpes'):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("(t)=>{ openDetail(promises.find(p=>p.title===t).id); }",t); L=[]
        for ms in (300,700,1500,3000,6000):
            pg.wait_for_timeout(ms-(L[-1][0] if L else 0)); L.append((ms,pg.evaluate("()=>document.getElementById('dptQui').textContent.trim()")))
        print(t,'|',L)
    b.close()
