# Filmstrip d'une plantation sur la Toile vivante : copie #toileCv à des instants donnés après addPromi.
# Usage : python3 film.py monde [--webkit] [--clair] [--pas=120] [--fin=2000] [--out=film_monde.png]
import sys, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image
M=[a for a in sys.argv[1:] if not a.startswith('--')][0]
WK='--webkit' in sys.argv; CLAIR='--clair' in sys.argv
opt=lambda k,d: ([a.split('=',1)[1] for a in sys.argv if a.startswith('--'+k+'=')] or [d])[0]
PAS=int(opt('pas','120')); FIN=int(opt('fin','2000')); OUT=opt('out','film_%s%s.png'%(M,'_clair' if CLAIR else ''))
JS=r"""async (a)=>{ Toile.setTheme(a.m); if(a.clair&&window.setTheme) setTheme('light'); await new Promise(r=>setTimeout(r,2600));
 const cv=document.getElementById('toileCv'); const out=[]; const tt=[]; for(let t=0;t<=a.fin;t+=a.pas) tt.push(t);
 let i=0; const t0=performance.now(); Toile.addPromi(null);
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; if(i<tt.length && e>=tt[i]){ const c=document.createElement('canvas'); c.width=cv.width/2; c.height=cv.height/2; c.getContext('2d').drawImage(cv,0,0,c.width,c.height); out.push([Math.round(e),c.toDataURL('image/png')]); while(i<tt.length&&e>=tt[i]) i++; } if(i<tt.length) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return out; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    fr=pg.evaluate(JS,{'m':M,'pas':PAS,'fin':FIN,'clair':CLAIR}); b.close()
ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB') for _,u in fr]
w,h=ims[0].size; sc=0.5; w2,h2=int(w*sc),int(h*sc); cols=6; rows=(len(ims)+cols-1)//cols
sheet=Image.new('RGB',(cols*w2,rows*(h2+18)),(255,255,255))
from PIL import ImageDraw
d=ImageDraw.Draw(sheet)
for k,(im,(t,_)) in enumerate(zip(ims,fr)):
    x=(k%cols)*w2; y=(k//cols)*(h2+18); sheet.paste(im.resize((w2,h2)),(x,y+18)); d.text((x+4,y+3),'%d ms'%t,fill=(0,0,0))
sheet.save(OUT); print(OUT, len(ims), [t for t,_ in fr])
