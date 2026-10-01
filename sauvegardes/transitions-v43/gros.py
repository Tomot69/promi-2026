import io, base64, sys
from playwright.sync_api import sync_playwright
from PIL import Image
T=[0,150,300,450,600,750,900,1100,1300,1600,2000,2600]
OP=sys.argv[1]; M=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800); pg.evaluate('m=>{window.__M=m}',M)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(window.__M);}"); pg.wait_for_timeout(3500)
    R=pg.evaluate("""async (a)=>{ const cv=document.getElementById('toileCv'); let id;
      if(a.op==='plante'){ id=9004; promises.push(Object.assign({},promises[0],{id:id,title:'essai',nuee:null})); Toile.addPromi(id); }
      else { const P=promises.filter(p=>!p.draft); id=P[5].id; const D=Toile.dalleAbs(id), V=Toile.vue(); window.__c=[(D.minx+D.w/2)*V.s*V.dpr+V.ox*V.dpr,(D.miny+D.h/2)*V.s*V.dpr+V.oy*V.dpr]; Toile.sync(P.filter(p=>p.id!==id).map(p=>p.id)); }
      const t0=performance.now(), out=[]; let k=0; await new Promise(r=>{ function f(){ const e=performance.now()-t0; if(k<a.T.length&&e>=a.T[k]){ out.push(cv.toDataURL('image/png')); k++; } if(k<a.T.length) requestAnimationFrame(f); else r(); } requestAnimationFrame(f); });
      let c=window.__c; if(a.op==='plante'){ const D=Toile.dalleAbs(id), V=Toile.vue(); c=[(D.minx+D.w/2)*V.s*V.dpr+V.ox*V.dpr,(D.miny+D.h/2)*V.s*V.dpr+V.oy*V.dpr]; } return {imgs:out, c:c}; }""",{'T':T,'op':OP})
    cx,cy=R['c']; S=250
    ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB').crop((int(cx-S),int(cy-S),int(cx+S),int(cy+S))) for u in R['imgs']]
    pl=Image.new('RGB',(506*4,506*3),(255,255,255))
    for i,im in enumerate(ims): pl.paste(im,((i%4)*506,(i//4)*506))
    pl.save('gros_%s_%s.png'%(M,OP)); b.close()
