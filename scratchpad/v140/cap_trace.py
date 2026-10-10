import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for f in ('zz-av140.html','app.html'):
      for th in ('light','dark'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('geste_vu_pelote','1');localStorage.setItem('geste_vu_aura-apparait','1');}catch(e){}"%th)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(5000)
        cdp = ctx.new_cdp_session(pg)
        bo = pg.evaluate("()=>{const r=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, r.left, r.top, r.width, r.height]}")
        cx,cy=bo[0],bo[1]
        def tp(x,y,r=11): return [{'x':x,'y':y,'radiusX':r,'radiusY':r,'force':1}]
        def glisse(P, r=11):
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':tp(P[0][0],P[0][1],r)})
            for (x,y) in P[1:]:
                pg.wait_for_timeout(22); cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':tp(x,y,r)})
            pg.wait_for_timeout(350); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(400)
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(400)
        import math
        # une courbe en S
        P=[(cx-60+120*i/24, cy-35+18*math.sin(i/24*2*math.pi)) for i in range(25)]
        glisse(P)
        v=pg.evaluate("()=>{const e=_aura.etat(); return [e.lac,e.tan]}")
        # un appui long ailleurs, sans faire tourner
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':tp(cx-30,cy+45,12)}); pg.wait_for_timeout(1400); cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente}", timeout=25000); pg.wait_for_timeout(900)
        pg.screenshot(path='scratchpad/v140/trace-%s-%s.png'%(f.replace('.html',''),th),clip={'x':bo[2]-10,'y':bo[3]-10,'width':bo[4]+20,'height':bo[5]+40})
        ctx.close()
    b.close()
