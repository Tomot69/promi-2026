import sys
from playwright.sync_api import sync_playwright
NOM=sys.argv[1] if len(sys.argv)>1 else 'avant'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)", 'light'); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(2500)
    open('scratchpad/plus-%s-choix.png'%NOM,'wb').write(pg.query_selector('#device').screenshot())
    # la tuile Promi
    pg.evaluate("()=>{const t=document.querySelector('#ppChoix .tile[data-kind=promi], .pp-choix .tile'); if(t) t.click();}")
    pg.wait_for_timeout(2500)
    open('scratchpad/plus-%s-promi.png'%NOM,'wb').write(pg.query_selector('#device').screenshot())
    pg.evaluate("()=>{closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee)[0].id);}"); pg.wait_for_timeout(2500)
    open('scratchpad/fiche-%s.png'%NOM,'wb').write(pg.query_selector('#device').screenshot())
    b.close()
print('ok')
