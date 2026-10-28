import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import numpy as np, colorsys
car=sys.argv[1]
JS="""async car=>{ TraceLettres._debug=true; TraceLettres._cache={}; TraceLettres._cacheN=0; const el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:60px;width:300px;font:400 '+(window.__FZ||150)+'px/1.2 PromiLate;color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
 await document.fonts.load('400 40px PromiLate'); const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret; C.va(0.5); const d=TraceLettres._derniere; C.stop(); el.remove();
 return {w:d.w,h:d.h,T:Array.from(d.T),own:Array.from(d.own),dep:d.dep,bouts:d.bouts}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000); pg.evaluate('f=>window.__FZ=f', float(__import__('os').environ.get('FZ','150')))
    r=pg.evaluate(JS,car); b.close()
w,h=r['w'],r['h']; T=np.array(r['T']).reshape(h,w); own=np.array(r['own']).reshape(h,w)
im=np.full((h,w,3),255,np.uint8); tm=T.max() or 1
cols=[(230,60,60),(60,160,60),(60,90,230),(220,160,0),(160,60,200),(0,170,190)]
for y in range(h):
    for x in range(w):
        o=own[y,x]
        if o==-1 and T[y,x]==0: continue
        c=cols[o%6] if o>=0 else (90,90,90); f=0.35+0.65*T[y,x]/tm
        im[y,x]=[int(255-(255-v)*f) for v in c]
# time bands
o2=Image.fromarray(im).resize((w*2,h*2),Image.NEAREST); o2.save('scratchpad/v170/own.png'); print(w,h,r['dep'],[ [round(v,1) for v in b[4:]] for b in r['bouts']])
