# Capture chaque image jusqu'à FIN ms et montre la paire dont l'écart est le plus grand (+ la carte des différences).
import sys, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat
M=sys.argv[1]; DEP='--depart' in sys.argv; FIN=int(([a.split('=')[1] for a in sys.argv if a.startswith('--fin=')] or ['400'])[0])
DEB=int(([a.split('=')[1] for a in sys.argv if a.startswith('--deb=')] or ['0'])[0])
JS=r"""async (a)=>{ Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,3000)); const cv=document.getElementById('toileCv'); const o=[];
 const t0=performance.now(); if(a.dep){ const ids=promises.filter(p=>!p.draft).map(p=>p.id); Toile.sync(ids.slice(1)); } else Toile.addPromi(null);
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; if(e>=a.deb) o.push([Math.round(e),cv.toDataURL()]); if(e<a.fin) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); }); return o; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    fr=pg.evaluate(JS,{'m':M,'dep':DEP,'fin':FIN,'deb':DEB}); b.close()
ims=[(t,Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')) for t,u in fr]
best=None
for i in range(1,len(ims)):
    d=ImageChops.difference(ims[i-1][1],ims[i][1]); m=sum(ImageStat.Stat(d).mean)/3
    print(ims[i][0], round(m,2))
    if not best or m>best[0]: best=(m,i)
m,i=best; a,bb=ims[i-1][1],ims[i][1]
d=ImageChops.difference(a,bb).convert('L').point(lambda v:255 if v>20 else 0)
w,h=a.size; s=Image.new('RGB',(w*3//2,h//2),'white'); s.paste(a.resize((w//2,h//2)),(0,0)); s.paste(bb.resize((w//2,h//2)),(w//2,0)); s.paste(d.convert('RGB').resize((w//2,h//2)),(w,0)); s.save('paire_%s.png'%M)
print('pire', ims[i-1][0],'→',ims[i][0], round(m,2))
