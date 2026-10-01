import sys
from playwright.sync_api import sync_playwright
MS=sys.argv[1:] or ['touffe']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:120]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in MS:
        r=pg.evaluate("""async(m)=>{ Toile.setTheme(m); await new Promise(r=>setTimeout(r,2500));
          const set=(s)=>{ const v=Toile.vue(); /* on passe par la même voie que le doigt : on pose la vue et on relance */ window.__zoomTest && 0; };
          return 1; }""", m)
        # pincement réel
        cdp=pg.context.new_cdp_session(pg)
        D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
        cx,cy=D[0]+195*D[2],D[1]+440*D[2]
        for d0,d1 in [(80,240)]:
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':cx-d0/2,'y':cy,'id':1},{'x':cx+d0/2,'y':cy,'id':2}]})
            for i in range(1,15):
                d=d0+(d1-d0)*i/14; cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':cx-d/2,'y':cy,'id':1},{'x':cx+d/2,'y':cy,'id':2}]}); pg.wait_for_timeout(16)
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(400)
        pg.wait_for_timeout(1200)
        print(m, {k:round(v,2) for k,v in pg.evaluate("()=>Toile.vue()").items()}, pg.evaluate("()=>Toile_state()"))
        pg.locator('#toileCv').screenshot(path='sauvegardes/v46/zs_%s.png'%m)
    print('erreurs', er[:4]); b.close()
