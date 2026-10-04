import sys, json
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
def doigt(cdp,t,x,y,ms): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':([] if t=='touchEnd' else [{'x':x,'y':y}]),'timestamp':ms/1000.0})
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True,is_mobile=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); cdp=ctx.new_cdp_session(pg)
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ window.__ev=[]; ['pointermove','pointercancel','pointerup','touchmove','touchcancel'].forEach(t=>document.addEventListener(t,e=>{ __ev.push(t); },true)); }")
    d=pg.evaluate("()=>{var d=document.getElementById('device').getBoundingClientRect();return [d.left,d.top,d.width,d.height];}")
    pt=[d[0]+d[2]/2, d[1]+d[3]*0.42]
    et=lambda: pg.evaluate("()=>({hue:Math.round(Toile.getHue()), pal:Toile.getPalette(), arme:_studioGesteCouleur.arme(), ev:(()=>{const c={}; __ev.forEach(t=>c[t]=(c[t]||0)+1); __ev.length=0; return c})()})")
    for nom,(ux,uy) in (('VERTICALE d\'abord',(0,1)),('HORIZONTALE d\'abord',(1,0)),('DIAGONALE (45°)',(0.7,0.7))):
        pg.evaluate("()=>{Toile.setHue(0); Toile.setPalette('signal'); __ev.length=0}"); pg.wait_for_timeout(300)
        ms=1000; doigt(cdp,'touchStart',pt[0],pt[1],ms); pg.wait_for_timeout(720)
        for i in range(1,9): ms+=40; doigt(cdp,'touchMove',pt[0]+ux*i*15,pt[1]+uy*i*15,ms); pg.wait_for_timeout(30)
        pg.wait_for_timeout(300); r=et(); doigt(cdp,'touchEnd',0,0,ms+60); pg.wait_for_timeout(500)
        print('%-22s' % nom, json.dumps(r, ensure_ascii=False))
    b.close()
