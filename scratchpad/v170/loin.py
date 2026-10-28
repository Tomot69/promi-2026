import sys, os, base64, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
import numpy as np
cars=sys.argv[1]
JS="""async a=>{ const [car,N]=a; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
  const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:60px;top:60px;width:300px;font:400 150px/180px PromiLate;color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
  await document.fonts.load('400 150px PromiLate'); const C=TraceLettres.trace(el, null, {manuel:true, respecteReduire:false}); await C.pret; const cv=C.canevas;
  const W=cv.width,H=cv.height,n=W*H,g2=cv.getContext('2d'); const lit=()=>{ const d=g2.getImageData(0,0,W,H).data,o=new Uint8Array(n); for(let i=0;i<n;i++) o[i]=d[4*i+3]; return o; };
  C.va(0.99999); const ref=lit(); const res=[];
  for(let i=1;i<N;i++){ C.va(i/N); const cur=lit(); const unr=new Uint8Array(n); for(let p=0;p<n;p++){ if(ref[p]>127&&cur[p]<=10) unr[p]=1; }
    const L=[]; for(let y=0;y<H;y++) for(let x=0;x<W;x++){ const p=y*W+x; if(!(ref[p]>0&&cur[p]>10&&cur[p]<ref[p]-10)) continue; let v=false; const rp=cur[p]/ref[p];
      for(let dy=-2;dy<=2&&!v;dy++) for(let dx=-2;dx<=2&&!v;dx++){ const xx=x+dx,yy=y+dy; if(xx<0||yy<0||xx>=W||yy>=H) continue; const q=yy*W+xx; if(unr[q]||(ref[q]>127&&cur[q]/ref[q]<rp-0.05)) v=true; } if(!v) L.push([x,y,cur[p],ref[p]]); }
    if(L.length) res.push([i,L.length,L.slice(0,6)]); }
  C.stop(); el.remove(); return res; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html', timeout=300000); pg.wait_for_timeout(8000)
    for c in cars:
        r=pg.evaluate(JS,[c,36]); print(c, r[:8])
    b.close()
