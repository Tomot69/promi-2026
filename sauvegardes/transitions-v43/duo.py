# Deux à quatre images pleines d'une plantation, côte à côte. python3 duo.py monde t1 t2 ... [--webkit] [--clair] [--out=]
import sys, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
M=sys.argv[1]; TT=[int(a) for a in sys.argv[2:] if a.isdigit()]
WK='--webkit' in sys.argv; CLAIR='--clair' in sys.argv
OUT=([a.split('=',1)[1] for a in sys.argv if a.startswith('--out=')] or ['duo_%s.png'%M])[0]
JS=r"""async (a)=>{ Toile.setTheme(a.m); if(a.clair&&window.setTheme) setTheme('light'); await new Promise(r=>setTimeout(r,2600));
 const cv=document.getElementById('toileCv'); const out=[]; const tt=a.tt; let i=0; const t0=performance.now(); promises.push(Object.assign({},promises[0],{id:9999,title:'essai',nuee:null})); Toile.addPromi(9999);
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; if(i<tt.length && e>=tt[i]){ out.push([Math.round(e),cv.toDataURL('image/png')]); i++; } if(i<tt.length) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return out; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    fr=pg.evaluate(JS,{'m':M,'tt':TT,'clair':CLAIR}); b.close()
ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB') for _,u in fr]
w,h=ims[0].size; sc=min(1,1400/(w*len(ims))); w2,h2=int(w*sc),int(h*sc)
sheet=Image.new('RGB',(len(ims)*w2,h2+20),(255,255,255)); d=ImageDraw.Draw(sheet)
for k,(im,(t,_)) in enumerate(zip(ims,fr)): sheet.paste(im.resize((w2,h2)),(k*w2,20)); d.text((k*w2+4,4),'%d ms'%t,fill=(0,0,0))
sheet.save(OUT); print(OUT, sheet.size)
