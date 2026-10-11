import sys, math
from playwright.sync_api import sync_playwright
PALS = len(sys.argv)>1 and sys.argv[1]=='pals'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now(),der:2,decouvert:1}))}catch(e){}")
    ctx.add_init_script("window.__ev=[]; ['pointerdown','pointerup','pointercancel','touchstart','touchend','touchcancel','click'].forEach(function(n){ window.addEventListener(n,function(e){ var t=e.target; window.__ev.push(n+'@'+(t&&(t.id||t.className||t.tagName))+(e.defaultPrevented?'(dp)':'')); },true); });")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(6000)
    d = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
    def tap(x,y,dx=0,dy=0,ms=60):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(ms//2)
        if dx or dy: cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x+dx, 'y': y+dy}]})
        pg.wait_for_timeout(ms//2); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    if PALS: tap(d['x']+75, d['y']+620); pg.wait_for_timeout(1500)
    for k in range(14):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': d['x'] + 320, 'y': d['y'] + 300}]})
        for i in range(1, 11): pg.wait_for_timeout(16); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': d['x'] + 320 - i * 24, 'y': d['y'] + 300}]})
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1500)
        if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
    pg.wait_for_timeout(2500)
    print('classes', pg.evaluate("()=>document.getElementById('studioScreen').className"))
    print('bandes', pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(); return ['#stpPals','#stpTons','#stpLab','#stpVue','#stpDots','#studioBody','#stpPanneau','.st3-panel'].map(s=>{const e=document.querySelector('#studioScreen '+s); if(!e) return s+':—'; const r=e.getBoundingClientRect(), c=getComputedStyle(e); return s+':'+[Math.round(r.left-D.left),Math.round(r.top-D.top),Math.round(r.width),Math.round(r.height)].join(',')+' '+c.filter+' pe:'+c.pointerEvents+' d:'+c.display;});}"))
    pts = [(65,527,0,0),(130,527,0,0)] if PALS else [(195,600,0,0),(195,655,0,0),(195,690,0,0),(195,753,0,0),(195,765,0,0),(46,753,0,0),(195,782,0,0),(195,790,0,0)]
    for (x,y,dx,dy) in pts:
        pg.evaluate("()=>{window.__ev=[]; try{_murBaisse()}catch(e){} }"); pg.wait_for_timeout(450)
        h=pg.evaluate("([x,y])=>{const D=document.getElementById('device').getBoundingClientRect(); const e=document.elementFromPoint(D.left+x,D.top+y); return e?(e.id||e.className||e.tagName):null}",[x,y])
        tap(d['x']+x, d['y']+y, dx, dy); pg.wait_for_timeout(650)
        print((x,y,dx,dy),'sous le doigt:',h, pg.evaluate("([x,y])=>{const D=document.getElementById('device').getBoundingClientRect(); return document.elementsFromPoint(D.left+x,D.top+y).slice(0,5).map(e=>e.id||e.className||e.tagName).join(' < ')}",[x,y]),'| levée', pg.evaluate("()=>document.getElementById('murPhrase')&&document.getElementById('murPhrase').classList.contains('leve')"), '|', pg.evaluate("()=>window.__ev.join(' ')")[:300], '|', pg.evaluate("()=>document.getElementById('studioScreen').className")[:80])
    b.close()
