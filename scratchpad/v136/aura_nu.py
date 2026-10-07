from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); 
    for th in ('light','dark'):
        c=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3); pg=c.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("t=>{document.getElementById('device').classList.toggle('light',t==='light'); try{setTheme&&0}catch(e){}}",th)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(3500)
        print(th, pg.evaluate("()=>({halo:!!document.getElementById('auPeloteHalo'),ombre:!!document.getElementById('auPeloteOmbre'),gl:document.querySelectorAll('#auBouleGL').length,err:window._auraErreur||null})"), errs[:3])
        pg.screenshot(path='planche-v136/aura-nue-%s.png'%th, clip={'x':20,'y':44,'width':390,'height':844})
        c.close()
    b.close()
