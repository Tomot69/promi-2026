from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} try{ setTheme('light'); }catch(e){} window.ouvrirIndex(); }"); pg.wait_for_timeout(2500)
    r=pg.evaluate("""()=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>{ const cv=c.querySelector('canvas'); return [c.textContent.slice(0,50), cv?[...cv.attributes].map(a=>a.name+'='+a.value.slice(0,60)).join(' '):null]; })""")
    for x in r: print(x)
    b.close()
