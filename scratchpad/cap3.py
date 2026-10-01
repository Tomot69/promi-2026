from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for k in ('promi','chiche','nuee'):
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1600)
        pg.evaluate("(k)=>{const t=[...document.querySelectorAll('.tile')].find(x=>x.getAttribute('data-kind')===k)||document.querySelector('.tile'); if(t) t.click();}", k)
        pg.wait_for_timeout(2200)
        open('scratchpad/plus-%s.png'%k,'wb').write(pg.query_selector('#device').screenshot())
    b.close()
