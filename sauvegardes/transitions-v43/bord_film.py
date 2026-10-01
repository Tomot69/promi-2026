# Une arrivée AU BORD, filmée : on plante jusqu'à ce que la dalle neuve touche un bord, puis planche de 12 images autour d'elle.
import sys, io, base64
from playwright.sync_api import sync_playwright
from PIL import Image
MONDES=sys.argv[1:] or ['halin','esquille','bobinette','ritournelle','madrure']
T=[0,60,120,180,240,320,400,500,620,760,950,1300]
JS=r"""async (a)=>{ const cv=document.getElementById('toileCv');
 for(let essai=0;essai<8;essai++){
  const id=9500+essai+Math.floor(Math.random()*400); promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null}));
  Toile.addPromi(id); const t0=performance.now(); const imgs=[]; let k=0;
  await new Promise(r=>{ function f(){ const e=performance.now()-t0; if(k<a.T.length&&e>=a.T[k]){ imgs.push([Math.round(e),cv.toDataURL('image/png')]); k++; } if(k<a.T.length) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
  const D=Toile.dalleAbs(id), V=Toile.vue(), Wt=cv.width/V.dpr, Ht=cv.height/V.dpr; let bx=null, bord=false;
  if(D){ const x0=D.minx*V.s+V.ox, y0=D.miny*V.s+V.oy; bx=[x0*V.dpr,y0*V.dpr,D.w*V.s*V.dpr,D.h*V.s*V.dpr]; bord=(x0<4||y0<4||x0+D.w*V.s>Wt-4||y0+D.h*V.s>Ht-4); }
  promises.pop(); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id)); await new Promise(r=>setTimeout(r,2000));
  if(bord) return {bx:bx, imgs:imgs, essai:essai};
 }
 return null; }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in MONDES:
        pg.evaluate("m=>Toile.setTheme(m)",m); pg.wait_for_timeout(3000)
        R=pg.evaluate(JS,{'T':T})
        if not R: print(m,'aucune arrivée au bord'); continue
        x,y,w,h=R['bx']; cx,cy=x+w/2,y+h/2; S=max(w,h)*0.9+60
        ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB').crop((int(cx-S),int(cy-S),int(cx+S),int(cy+S))).resize((330,330)) for _,u in R['imgs']]
        pl=Image.new("RGB",(336*6,336*2),(255,255,255))
        for i,im in enumerate(ims): pl.paste(im,((i%6)*336,(i//6)*336))
        pl.save('bord_%s.png'%m); print(m,'essai',R['essai'],'temps',[t for t,_ in R['imgs']])
    b.close()
