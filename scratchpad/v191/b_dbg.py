import sys, io; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); cx,pg=BJ.ouvre(b,'app.html','promi')
    pg.evaluate("()=>{document.getElementById('detailPoster').scrollTop=1}"); pg.wait_for_timeout(200)
    J=pg.evaluate("()=>_v189Jonction().F"); s0=J['s0']; P=J['P']; ic=min(range(len(P)),key=lambda i:P[i]); print('s0',s0,'crest x',ic*2, 'dens', pg.evaluate("()=>window._densEcran&&_densEcran()"))
    pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}", s0+2); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
    L=pg.evaluate("""a=>{ const c=document.getElementById('v189Jonction'), g=c.getContext('2d'), E=c.width/390; const out=[]; for(const x of a){ const col=g.getImageData(Math.round(x*E),Math.round(108*E),1,Math.round(8*E)).data; const r=[]; for(let y=0;y<col.length/4;y++) r.push([+(108+y/E).toFixed(2), col[y*4],col[y*4+1],col[y*4+2],col[y*4+3]]); out.push([x,r]); } return out; }""", [ (ic+d)*2 for d in (-4,-2,0,2,4)])
    for x,r in L: print(x, [q for q in r if 111<=q[0]<=113.2])
    d=B.dev(pg); k=d[4]; im=Image.open(io.BytesIO(pg.screenshot(clip={'x':d[0],'y':d[1]+100*k,'width':390*k,'height':20*k}))).convert('RGB'); q=im.size[0]/390
    for x in [(ic+dd)*2 for dd in (-4,-2,0,2,4)]:
        print('ecran',x,[(round(100+yy/q,2),im.getpixel((int(x*q),yy))) for yy in range(int(11*q),int(13.5*q))])
    b.close()
