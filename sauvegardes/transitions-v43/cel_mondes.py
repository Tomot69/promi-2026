# La célébration dans les 13 mondes : une plantation, capture à 850 ms (le vert TIENT), compte des pixels #8FE08F exacts.
import sys, io, base64
from playwright.sync_api import sync_playwright
from PIL import Image
MONDES=['encre','touffe','mosaique','braille','pixel','halin','esquille','madrure','ritournelle','bobinette','terrazzo','gravure','sillons']
TH=sys.argv[1] if len(sys.argv)>1 else 'dark'
JS=r"""async (m)=>{ Toile.setTheme(m); await new Promise(r=>setTimeout(r,2600));
  const cv=document.getElementById('toileCv'); const id=9000+Math.floor(Math.random()*999);
  promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id);
  const t0=performance.now(); await new Promise(r=>{ function f(){ if(performance.now()-t0>=850) r(); else requestAnimationFrame(f);} requestAnimationFrame(f); });
  const D=Toile.dalleAbs(id), V=Toile.vue(); const box=D?[(D.minx*V.s+V.ox)*V.dpr,(D.miny*V.s+V.oy)*V.dpr,(D.w*V.s)*V.dpr,(D.h*V.s)*V.dpr]:null; const url=cv.toDataURL('image/png'); const x=cv.getContext('2d'); const d=x.getImageData(0,0,cv.width,cv.height).data; let n=0;
  for(let i=0;i<d.length;i+=4){ if(Math.abs(d[i]-143)<=2&&Math.abs(d[i+1]-224)<=2&&Math.abs(d[i+2]-143)<=2) n++; }
  const E=window._celebrationEtat||{}; promises.pop(); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id));
  await new Promise(r=>setTimeout(r,1500)); return [url,n,E.n||0,box]; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2,color_scheme='light' if TH=='light' else 'dark')
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ims=[]; zo=[]
    for m in MONDES:
        u,n,e,bx=pg.evaluate(JS,m); print(m,'pixels #8FE08F exacts',n,'· dalles célébrées',e)
        im=Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'); ims.append(im)
        if bx:
            cx,cy=bx[0]+bx[2]/2,bx[1]+bx[3]/2; R=max(bx[2],bx[3])*0.75+20; zo.append(im.crop((int(cx-R),int(cy-R),int(cx+R),int(cy+R))).resize((300,300)))
    errs=pg.evaluate("()=>1"); b.close()
w,h=ims[0].size; k=0.28; W2,H2=int(w*k),int(h*k); s=Image.new('RGB',(W2*7+60,H2*2+10),(255,255,255))
for i,im in enumerate(ims): s.paste(im.resize((W2,H2)),((i%7)*(W2+10),(i//7)*(H2+10)))
s.save('sauvegardes/transitions-v43/cel_mondes_%s.png'%TH)
z=Image.new('RGB',(310*7,310*2),(255,255,255))
for i,im in enumerate(zo): z.paste(im,((i%7)*310,(i//7)*310))
z.save('sauvegardes/transitions-v43/cel_zoom_%s.png'%TH)
