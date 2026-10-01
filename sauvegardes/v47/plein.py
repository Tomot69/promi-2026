from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in ['touffe','esquille','ritournelle']:
        pg.evaluate("async(m)=>{Toile.setTheme(m); await new Promise(r=>setTimeout(r,500)); Toile_recadre(); await new Promise(r=>setTimeout(r,2500));}", m)
        v=pg.evaluate("()=>Toile.vue()"); r=pg.evaluate("()=>{const d=document.getElementById('device').getBoundingClientRect(), c=document.getElementById('toileCv').getBoundingClientRect(); return [d.left,d.top,d.width,d.height,c.left,c.top,c.width,c.height, getComputedStyle(document.getElementById('device')).borderRadius]}")
        print(m, {k:round(x,3) for k,x in v.items()}, [round(x) if isinstance(x,float) else x for x in r])
        pg.locator('#device').screenshot(path='sauvegardes/v47/plein_%s.png'%m)
    b.close()
