import sys
from playwright.sync_api import sync_playwright
NOM=sys.argv[1] if len(sys.argv)>1 else 'v10'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
        pg.wait_for_timeout(2600)
        open('scratchpad/fiche-%s-%s.png'%(NOM,th),'wb').write(pg.query_selector('#device').screenshot())
    b.close()
