# Halin : 1) au repos, 2 s — ce qui bouge ; 2) une arrivée, images toutes les ~50 ms, planche des zones qui clignotent.
import io, base64, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
M=sys.argv[1] if len(sys.argv)>1 else 'halin'
JS=r"""async (a)=>{ const cv=document.getElementById('toileCv'); const out=[]; const t0=performance.now();
  if(a.plante){ const id=9000+Math.floor(Math.random()*999); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id); }
  await new Promise(r=>{ function f(){ const e=performance.now()-t0; out.push([Math.round(e),cv.toDataURL('image/png')]); if(e<a.dur) setTimeout(()=>requestAnimationFrame(f),30); else r(); } requestAnimationFrame(f); });
  return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(m);}", M)
    pg.wait_for_timeout(4000)
    for nom,pl,dur in [('repos',False,2000),('arrivee',True,2200)]:
        d=pg.evaluate(JS,{'plante':pl,'dur':dur})
        ims=[np.asarray(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')).astype(int) for _,u in d]
        diffs=[np.abs(ims[i]-ims[i-1]).sum(2) for i in range(1,len(ims))]
        print(nom, 'images',len(ims), 'pixels changés par image', [int((x>30).sum()) for x in diffs][:40])
        np.save('film_%s_%s.npy'%(M,nom), np.array([im.astype(np.uint8) for im in ims]))
    b.close()
