from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1320,'height':1000},device_scale_factor=1)
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:120]))
    pg.goto('http://127.0.0.1:8752/moodboard-celebration.html?v=3'); pg.wait_for_timeout(600)
    for k,ms in enumerate([160,1600]):
        pg.evaluate('(m)=>new Promise(r=>{ const t=performance.now(); (function f(){ if((horloge%CYCLE)>=m) r(); else requestAnimationFrame(f); })(); })', ms)
        print(k, 'niveau', round(pg.evaluate('()=>niveau'),3))
        pg.screenshot(path='sauvegardes/v47/mood2_%d.png'%k, clip={'x':0,'y':330,'width':1320,'height':620})
    print('niveau', pg.evaluate("()=>niveau"), 'graines', pg.evaluate("()=>seeds.length"), 'erreurs', er)
    b.close()
