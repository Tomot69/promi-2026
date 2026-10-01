# Accueil dézoomé (pincement au vrai doigt), ancien chemin puis nouveau, trois mondes × deux thèmes : on REGARDE le coin arrondi.
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch()
    for clair in (False, True):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("c=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('device').classList.toggle('light',c);}", clair)
        cdp=ctx.new_cdp_session(pg)
        r=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
        cx,cy=r[0]+195*r[2], r[1]+440*r[2]
        def ev(tp,d):
            pts=[] if tp=='touchEnd' else [{'x':cx-d/2,'y':cy,'id':1},{'x':cx+d/2,'y':cy,'id':2}]
            cdp.send('Input.dispatchTouchEvent',{'type':tp,'touchPoints':pts})
        ev('touchStart',300*r[2])
        for i in range(1,15): ev('touchMove',300*r[2]+(60-300)*r[2]*i/14)
        ev('touchEnd',60); pg.wait_for_timeout(1500)
        ims=[]
        for m in ('touffe','gravure','madrure'):
            for anc in (True, False):
                pg.evaluate("a=>{window._perfAncien=a.anc; Toile.setTheme(a.m);}", {'m':m,'anc':anc}); pg.wait_for_timeout(2200)
                pg.screenshot(path='scratchpad/perf/_t.png', clip={'x':r[0],'y':r[1],'width':390*r[2],'height':844*r[2]}); ims.append(Image.open('scratchpad/perf/_t.png').convert('RGB'))
        W,H=ims[0].size; out=Image.new('RGB',(W*6,H))
        for i,im in enumerate(ims): out.paste(im,(i*W,0))
        out.resize((W*6//2,H//2)).save('scratchpad/perf/dezoom_%s.png'%('clair' if clair else 'sombre')); ctx.close()
    b.close()
