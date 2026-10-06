import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    Q="()=>{const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('stpPals'); return [...P.children].map(e=>{const r=e.getBoundingClientRect(); return (e.id||e.className.split(' ')[0])+'@'+Math.round(r.top-dv.top)+'→'+Math.round(r.bottom-dv.top)}).join('  ')+' | st3pn dans le document : '+document.querySelectorAll('#st3pn').length+' | monde '+Toile.getTheme()}"
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500); print('ouverture 1 :', pg.evaluate(Q))
    # le VRAI geste : glisser à l'horizontale sur la Toile du Studio pour changer de monde
    for k in range(2):
        pg.mouse.move(20+300,44+300); pg.mouse.down()
        for i in range(1,13): pg.mouse.move(20+300-i*18,44+300); pg.wait_for_timeout(16)
        pg.mouse.up(); pg.wait_for_timeout(2600); print('après un glissement de monde :', pg.evaluate(Q))
    pg.evaluate("()=>{const x=document.querySelector('#studioScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500); print('ouverture 2 :', pg.evaluate(Q))
    b.close()
