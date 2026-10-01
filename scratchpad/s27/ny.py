from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('avant ouverture', pg.evaluate("()=>[].map.call(document.querySelectorAll('#shMode button'),function(b){return b.getAttribute('data-mode')+':'+b.textContent.trim();})"))
    pg.evaluate("()=>{document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(4200)
    print('apres  ouverture', pg.evaluate("()=>[].map.call(document.querySelectorAll('#shMode button'),function(b){return b.getAttribute('data-mode')+':'+b.textContent.trim();})"))
    print('v13 present', pg.evaluate("()=>typeof window._v13Partage"))
    pg.evaluate("()=>{window._v13Partage();}"); pg.wait_for_timeout(300)
    print('apres  appel   ', pg.evaluate("()=>[].map.call(document.querySelectorAll('#shMode button'),function(b){return b.getAttribute('data-mode')+':'+b.textContent.trim();})"))
    print('err',errs)
    b.close()
