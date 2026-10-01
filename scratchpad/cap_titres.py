from playwright.sync_api import sync_playwright
ECR=[('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}"),
     ('index',"()=>{closeAll(); document.getElementById('indexBtn').click();}"),
     ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('reglages',"()=>{closeAll(); const b=document.getElementById('settingsBtn'); b&&b.click();}"),
     ('partage',"()=>{closeAll(); const b=document.getElementById('shareBtn'); if(b)b.click(); else if(window.openShare)openShare();}")]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'light'); pg.wait_for_timeout(400)
    ims=[]
    for nom,js in ECR:
        pg.evaluate(js); pg.wait_for_timeout(2200)
        open('scratchpad/titre-%s.png'%nom,'wb').write(pg.screenshot(clip={'x':0,'y':0,'width':430,'height':130}))
    b.close()
