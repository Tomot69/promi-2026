import io, base64, sys
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
M=sys.argv[1] if len(sys.argv)>1 else 'esquille'
T=[0,80,160,240,320,400,500,650,800,1000,1300,1600]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=1)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(m);}",M); pg.wait_for_timeout(3500)
    R=pg.evaluate("""async (T)=>{ const cv=document.getElementById('toileCv'); const id=9010; promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null}));
      const pre=cv.toDataURL(); const s=Toile.addPromi(id); const t0=performance.now(), out=[pre]; let k=0; await new Promise(r=>{ function f(){ const e=performance.now()-t0; if(k<T.length&&e>=T[k]){ out.push(cv.toDataURL()); k++; } if(k<T.length) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
      const V=Toile.vue(); return {out:out, c:[s.x*V.s+V.ox, s.y*V.s+V.oy]}; }""",T)
    ims=[np.asarray(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')).astype(int) for u in R['out']]
    h,w,_=ims[0].shape; pl=Image.new('RGB',((w//2+6)*6,(h//2+6)*2),(255,255,255))
    yy,xx=np.mgrid[0:h,0:w]; dist=np.hypot(xx-R['c'][0], yy-R['c'][1])
    for i in range(1,len(ims)):
        dm=np.abs(ims[i]-ims[i-1]).sum(2); d=dm>40
        base=(ims[i]*0.35+255*0.65).astype(np.uint8); base[d]=[220,30,30]
        pl.paste(Image.fromarray(base).resize((w//2,h//2)),(((i-1)%6)*(w//2+6),((i-1)//6)*(h//2+6)))
    tot=(np.abs(ims[-1]-ims[0]).sum(2)>40)
    print(M,'pixels changés au total', int(tot.sum()), '| dont à plus de 150 px de la dalle', int((tot&(dist>150)).sum()))
    pl.save('diff_%s.png'%M); b.close()
