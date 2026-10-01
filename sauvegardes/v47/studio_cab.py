from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('cabochon'); document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    print(pg.evaluate("()=>[[...document.querySelectorAll('#studioBody .st3-dot')].map(d=>d.dataset.w).join(' '), document.getElementById('stpNom').textContent, document.getElementById('studioScreen').classList.contains('world-locked')]"))
    pg.locator('#device').screenshot(path='sauvegardes/v47/studio_cab.png')
    b.close()
