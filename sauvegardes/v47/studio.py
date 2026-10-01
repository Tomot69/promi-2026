from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('esquille'); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2200)
    pg.locator('#device').screenshot(path='sauvegardes/v47/studio.png')
    print(pg.evaluate("""()=>[...document.querySelectorAll('#studioScreen *')].filter(e=>!e.children.length && /Esquille|Ingénu|\\ben\\b/i.test(e.textContent||'') && e.getBoundingClientRect().width>0).map(e=>{const cs=getComputedStyle(e), r=e.getBoundingClientRect(); return (e.id||'')+'.'+e.className+' «'+e.textContent.trim().slice(0,40)+'» '+cs.fontFamily.split(',')[0]+' '+cs.fontSize+' '+cs.fontWeight+' y'+Math.round(r.top)})"""))
    print(pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-nom, #studioScreen .st3-wn'); return e? e.parentElement.outerHTML.slice(0,900):null}"))
    b.close()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('esquille'); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2000)
    pg.evaluate("()=>Toile.setPalette('primesautier')"); pg.wait_for_timeout(800)
    print('après changement de palette :', pg.evaluate("()=>document.getElementById('stpNom').textContent"))
    pg.locator('#device').screenshot(path='sauvegardes/v47/studio2.png')
    b.close()
