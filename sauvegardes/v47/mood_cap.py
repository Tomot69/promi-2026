from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':1000},device_scale_factor=1)
    pg.goto('http://127.0.0.1:8752/moodboard-celebration.html'); pg.wait_for_timeout(14000)
    pg.evaluate("()=>document.getElementById('pause').click()")
    for m in ['ritournelle','esquille']:
        pg.evaluate("(m)=>{ [...document.querySelectorAll('#mondes button')].find(b=>b.textContent.toLowerCase()===(m==='ritournelle'?'ritournelle':'esquille')).click(); }", m); pg.wait_for_timeout(3000)
        pg.evaluate("()=>document.getElementById('un').click()"); pg.wait_for_timeout(150)
        pg.screenshot(path='sauvegardes/v47/mood_%s.png'%m, clip={'x':0,'y':230,'width':1300,'height':660})
    b.close()
