# la trace sous le doigt : S, appui court, appui long — pendant le geste (doigt posé) et au repos
import sys, math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; out=sys.argv[2] if len(sys.argv)>2 else 'scratchpad/v141/trace.png'
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for cas in ('S','court','long'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','light');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500); cdp=ctx.new_cdp_session(pg)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(7000)
        r=pg.evaluate("()=>{var c=document.getElementById('auBoule').getBoundingClientRect(); return [c.left,c.top,c.width,c.height]}")
        cx,cy=r[0]+r[2]/2,r[1]+r[3]/2
        def T(t,pts,rx=11): cdp.send('Input.dispatchTouchEvent',{'type':t,'touchPoints':[{'x':x,'y':y,'radiusX':rx,'radiusY':rx*1.25,'id':0} for (x,y) in pts]})
        def cap(lab):
            pg.screenshot(path='/tmp/t.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append((cas+' — '+lab, Image.open('/tmp/t.png').convert('RGB')))
        n0=pg.evaluate("()=>_aura.tracesGeo().length")
        if cas=='S':
            P=[(cx-55+110*u, cy-40+80*u+28*math.sin(u*2*math.pi)) for u in [i/40 for i in range(41)]]
            T('touchStart',[P[0]]); pg.wait_for_timeout(120)
            for q in P[1:21]: T('touchMove',[q]); pg.wait_for_timeout(24)
            cap('à mi-chemin, doigt posé (%d trace(s))'%pg.evaluate("()=>_aura.tracesGeo().length"))
            for q in P[21:]: T('touchMove',[q]); pg.wait_for_timeout(24)
            pg.wait_for_timeout(250); cap('au bout, doigt posé (%d)'%pg.evaluate("()=>_aura.tracesGeo().length"))
            T('touchEnd',[]); pg.wait_for_timeout(3500); cap('au repos (%d)'%pg.evaluate("()=>_aura.tracesGeo().length"))
        elif cas=='court':
            T('touchStart',[(cx-20,cy+10)]); pg.wait_for_timeout(90); cap('doigt posé, 0,09 s'); T('touchEnd',[]); pg.wait_for_timeout(3500); cap('au repos (%d trace)'%pg.evaluate("()=>_aura.tracesGeo().length"))
        else:
            T('touchStart',[(cx-20,cy+10)],16); pg.wait_for_timeout(1400); cap('doigt posé, 1,4 s'); T('touchEnd',[]); pg.wait_for_timeout(3500); cap('au repos (%d trace)'%pg.evaluate("()=>_aura.tracesGeo().length"))
        print(cas, n0, pg.evaluate("()=>_aura.tracesGeo().map(t=>({L:+t.L.toFixed(2),w:+t.w.toFixed(2),et:t.et}))")); ctx.close()
    b.close()
W=ims[0][1].width
P=Image.new('RGB',(len(ims)*(W+16),ims[0][1].height+40),'white'); d=ImageDraw.Draw(P)
for i,(lab,im) in enumerate(ims): P.paste(im,(i*(W+16),40)); d.text((i*(W+16)+10,12),lab,fill=(0,0,0))
P.save(out); P.resize((P.width//3,P.height//3)).save(out.replace('.png','-p.png'))
