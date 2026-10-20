import sys, time; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
sombre = '--sombre' in sys.argv
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, sombre=sombre); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    for i in range(12):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1500)
    D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    clip={'x':D[0],'y':D[1],'width':D[2],'height':D[3]}
    c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    shots=[]; pg.screenshot(path='scratchpad/v155/b_pre.png', clip=clip, scale='css')
    t=time.time(); pg.touchscreen.tap(c[0],c[1])
    for k in range(14):
        f='scratchpad/v155/b%02d.png'%k; pg.screenshot(path=f, clip=clip, scale='css', animations='allow'); shots.append((round((time.time()-t)*1000),f))
    print(shots)
    ims=[Image.open('scratchpad/v155/b_pre.png')]+[Image.open(f) for _,f in shots[:9]]
    w,h=ims[0].size; out=Image.new('RGB',(w*5,h*2))
    for i,im in enumerate(ims): out.paste(im.convert('RGB'),((i%5)*w,(i//5)*h))
    out.resize((w*5//2,h)).save('scratchpad/v155/planche_b%s.png'%('s' if sombre else ''))
    b.close()
