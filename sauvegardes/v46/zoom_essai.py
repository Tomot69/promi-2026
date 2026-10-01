import sys
from playwright.sync_api import sync_playwright
M=(sys.argv[1:] or ['touffe'])[0]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
    er=[]; pg.on('pageerror',lambda e: er.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(m);}", M); pg.wait_for_timeout(2500)
    cdp=ctx.new_cdp_session(pg)
    D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
    dev=lambda x,y:(D[0]+x*D[2],D[1]+y*D[2]); vue=lambda: pg.evaluate("()=>Toile.vue()")
    def pince(d0,d1,n=14):
        cx,cy=dev(195,440)
        def ev(tp,d):
            pts=[] if tp=='touchEnd' else [{'x':cx-d/2,'y':cy,'id':1},{'x':cx+d/2,'y':cy,'id':2}]
            cdp.send('Input.dispatchTouchEvent',{'type':tp,'touchPoints':pts})
        ev('touchStart',d0)
        for i in range(1,n+1): ev('touchMove',d0+(d1-d0)*i/n); pg.wait_for_timeout(16)
        ev('touchEnd',d1)
    voile=lambda: pg.evaluate("()=>[getComputedStyle(document.getElementById('accPlat')).opacity, getComputedStyle(document.getElementById('accBarre')).visibility]")
    print('départ', vue(), voile())
    pince(300*D[2],60*D[2]); pg.wait_for_timeout(1500); print('dézoom max relâché', {k:round(v,3) for k,v in vue().items()}, voile())
    pg.locator('#device').screenshot(path='sauvegardes/v46/zoom_min_%s.png'%M)
    pg.evaluate("()=>{ const b=document.getElementById('indexBtn')||document.querySelector('[data-v=index]'); if(b) b.click(); }"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1500); print('après une page', {k:round(v,3) for k,v in vue().items()})
    pince(60*D[2],330*D[2]); pg.wait_for_timeout(300); pince(60*D[2],330*D[2]); pg.wait_for_timeout(1500); print('zoom avant', {k:round(v,3) for k,v in vue().items()}, voile())
    pg.locator('#device').screenshot(path='sauvegardes/v46/zoom_max_%s.png'%M)
    pg.evaluate("()=>{const q=P('essai zoom','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);}"); pg.wait_for_timeout(2500)
    print('après une plantation', {k:round(v,3) for k,v in vue().items()})
    print('erreurs', er[:3]); b.close()
