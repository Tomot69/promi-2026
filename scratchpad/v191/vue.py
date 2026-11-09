import sys, io; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; nat=sys.argv[2] if len(sys.argv)>2 else 'promi'; out=sys.argv[3] if len(sys.argv)>3 else 'scratchpad/v191/vue.png'
with sync_playwright() as p:
    b=p.webkit.launch(); cx,pg=BJ.ouvre(b,F,nat)
    j=pg.evaluate("()=>{document.getElementById('detailPoster').scrollTop=1; return 1}"); pg.wait_for_timeout(200)
    J=pg.evaluate("()=>window._v189Jonction&&_v189Jonction()"); print('s0', J and J['F'] and J['F']['s0'], 'BAS', J and J['F'] and J['F'].get('BAS'))
    d=B.dev(pg); k=d[4]; ims=[]
    for s in (0,40,80,100,110,120,130,150,170,200,0):
        pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}",s); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
        im=Image.open(io.BytesIO(pg.screenshot(clip={'x':d[0],'y':d[1]+60*k,'width':390*k,'height':360*k}))); ims.append(im)
        print(s, pg.evaluate("()=>{const c=document.getElementById('v189Jonction'); return c? [getComputedStyle(c).display, c.getAttribute('data-jonction')]:null}"), pg.evaluate("()=>document.getElementById('tenirZone').style.pointerEvents"))
    W,H=ims[0].size; m=Image.new('RGB',(W*6, H*2),'white')
    for i,im in enumerate(ims): m.paste(im,((i%6)*W,(i//6)*H))
    m.save(out); print(pg.erreurs[:3]); b.close()
