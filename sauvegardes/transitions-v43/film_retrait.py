# Film du retrait d'une dalle : 8 images de la Toile entre 0 et 900 ms, cadrées sur la dalle qui part.
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
import io, base64
M=sys.argv[1] if len(sys.argv)>1 else 'cabochon'
T=[0,150,300,400,480,560,640,900]
JS=r"""async (a)=>{ Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,3500));
 const cv=document.getElementById('toileCv');
 const ids=promises.filter(p=>!p.draft).map(p=>p.id); const vis=promises.filter(p=>!p.draft); const cible=vis.find(p=>/nager le mardi/.test(p.title))||vis[0]; Toile.sync(vis.filter(p=>p!==cible).map(p=>p.id));
 const t0=performance.now(), out=[]; let k=0;
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; if(k<a.T.length && e>=a.T[k]){ out.push([Math.round(e),cv.toDataURL('image/png')]); k++; } if(k<a.T.length) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    d=pg.evaluate(JS,{'m':M,'T':T}); b.close()
ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB') for _,u in d]
# la zone qui change le plus entre la première et la dernière
import numpy as np
a=np.asarray(ims[0]).astype(int); z=np.asarray(ims[-1]).astype(int); df=np.abs(a-z).sum(2)
ys,xs=np.nonzero(df>40); cx,cy=int(np.median(xs)),int(np.median(ys)); R=230
box=(max(0,cx-R),max(0,cy-R),max(0,cx-R)+2*R,max(0,cy-R)+2*R)
W=2*R; s=Image.new('RGB',(W*4+30,W*2+10),(255,255,255))
for i,im in enumerate(ims): s.paste(im.crop(box),((i%4)*(W+10),(i//4)*(W+10)))
s.save('film_retrait_%s.png'%M)
w,h=ims[0].size; k=0.3; t=Image.new('RGB',(int(w*k)*4+30,int(h*k)*2+10),(255,255,255))
for i,im in enumerate(ims): t.paste(im.resize((int(w*k),int(h*k))),((i%4)*(int(w*k)+10),(i//4)*(int(h*k)+10)))
t.save('film_retrait_%s_entier.png'%M); print([t for t,_ in d], box)
