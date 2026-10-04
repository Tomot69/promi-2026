# C-009 — Ramage : chaque image d'un événement (lue dans le canevas, à chaque image du navigateur), et l'écart de chacune avec la précédente
import sys, io, json, base64
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG = sys.argv[2] if len(sys.argv)>2 else 'a'; OU = sys.argv[3] if len(sys.argv)>3 else 'studio'
JS = r"""async (sel)=>{ const cv=document.querySelector(sel); const W=cv.width, H=cv.height; const o=document.createElement('canvas'); const k=Math.min(1, 520/W); o.width=Math.round(W*k); o.height=Math.round(H*k); const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; };
  let av=lit(), F=[], actif=0, t0=performance.now(), fin=null;
  await new Promise(res=>{ function f(t){ const d=lit(); let n=0; for(let i=0;i<d.length;i+=16){ if(Math.abs(d[i]-av[i])>12||Math.abs(d[i+1]-av[i+1])>12||Math.abs(d[i+2]-av[i+2])>12) n++; }
      if(n>40 || (actif && F.length<70)){ if(!actif) F.push({t:Math.round(t-t0), u:(function(){ g.putImageData(new ImageData(av,o.width,o.height),0,0); return o.toDataURL('image/png'); })(), n:0}); actif=1; g.putImageData(new ImageData(d,o.width,o.height),0,0); F.push({t:Math.round(t-t0), u:o.toDataURL('image/png'), n:n}); }
      av=d; if(F.length>=70 || t-t0>16000) res(); else requestAnimationFrame(f); } requestAnimationFrame(f); });
  return F; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(3000)
    if OU=='studio':
        pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500); sel='#stBg'
    else: sel='#toileCv'
    Fr=pg.evaluate(JS, sel); print(len(Fr),'images ·', [ (f['t'],f['n']) for f in Fr][:70])
    ims=[Image.open(io.BytesIO(base64.b64decode(f['u'].split(',')[1]))).convert('RGB') for f in Fr]
    for i,im in enumerate(ims): im.save('scratchpad/v126/ro-%s-%02d.png'%(TAG,i))
    # planche des écarts : chaque image moins la précédente, amplifié
    if len(ims)>2:
        W,H=ims[0].size; n=min(24,len(ims)-1); o=Image.new('RGB',(6*(W//2+6), ((n+5)//6)*(H//2+6)),(128,128,128)); o2=o.copy()
        for k in range(n):
            df=ImageChops.difference(ims[k],ims[k+1]).point(lambda v:min(255,v*4))
            o.paste(df.resize((W//2,H//2)), ((k%6)*(W//2+6), (k//6)*(H//2+6))); o2.paste(ims[k+1].resize((W//2,H//2)), ((k%6)*(W//2+6), (k//6)*(H//2+6)))
        o.save('scratchpad/v126/ramage-ecarts-%s.png'%TAG); o2.save('scratchpad/v126/ramage-images-%s.png'%TAG); print(o.size)
    b.close()
