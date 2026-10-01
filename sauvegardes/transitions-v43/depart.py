# Départ d'une dalle : on retire le premier Promi planté et on filme. python3 depart.py [--webkit]
import sys, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
WK='--webkit' in sys.argv; TT=[10,150,300,450,620,900,1400,2100]
JS=r"""async (a)=>{ Toile.setTheme('ritournelle'); await new Promise(r=>setTimeout(r,2600));
 const cv=document.getElementById('toileCv'); const out=[]; let i=0; const n0=Toile.count();
 const ids=promises.filter(p=>!p.draft).map(p=>p.id); const t0=performance.now(); Toile.sync(ids.slice(1));
 await new Promise(res=>{ function f(){ const e=performance.now()-t0; if(i<a.tt.length && e>=a.tt[i]){ out.push([Math.round(e),cv.toDataURL('image/png'),Toile.count()]); i++; } if(i<a.tt.length) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
 return {n0:n0, out:out}; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    r=pg.evaluate(JS,{'tt':TT}); b.close()
fr=r['out']; print('avant',r['n0'],'compte',[c for _,_,c in fr])
ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB') for _,u,_ in fr]
w,h=ims[0].size; sc=1400/(w*4); w2,h2=int(w*sc),int(h*sc)
sheet=Image.new('RGB',(4*w2,2*(h2+20)),(255,255,255)); d=ImageDraw.Draw(sheet)
for k,(im,(t,_,_)) in enumerate(zip(ims,fr)): x=(k%4)*w2; y=(k//4)*(h2+20); sheet.paste(im.resize((w2,h2)),(x,y+20)); d.text((x+4,y+4),'%d ms'%t,fill=(0,0,0))
sheet.save('depart.png')
