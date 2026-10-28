import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
JS="""async a=>{ const [car,N]=a; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove());
  const el=document.createElement('div'); el.id='gEl'; el.style.cssText='position:fixed;left:60px;top:60px;width:300px;font:400 '+(window.__FZ||150)+'px/1.2 PromiLate;color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
  await document.fonts.load('400 40px PromiLate'); const C=TraceLettres.trace(el, null, {manuel:true, respecteReduire:false}); await C.pret; const cv=C.canevas;
  const W=cv.width,H=cv.height,n=W*H,g2=cv.getContext('2d'); const lit=()=>{ const d=g2.getImageData(0,0,W,H).data,o=new Uint8Array(n); for(let i=0;i<n;i++) o[i]=d[4*i+3]; return o; };
  C.va(0.99999); const ref=lit(); const res=[];
  for(let i=1;i<N;i++){ C.va(i/N); const cur=lit(); let nu=0,tot=0; for(let p=0;p<n;p++){ if(ref[p]>200){ tot++; if(cur[p]<=10) nu++; } }
    if(nu<=0.10*tot) continue; const lab=new Int32Array(n); let nl=0;
    for(let p0=0;p0<n;p0++){ if(lab[p0]||!(ref[p0]>200&&cur[p0]<=10)) continue; nl++; let sz=0,x0=1e9,y0=1e9,x1=-1,y1=-1; const st=[p0]; lab[p0]=nl;
      while(st.length){ const p=st.pop(); sz++; const x=p%W,y=(p-x)/W; x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);
        for(let dy=-1;dy<=1;dy++) for(let dx=-1;dx<=1;dx++){ const xx=x+dx,yy=y+dy; if(xx<0||yy<0||xx>=W||yy>=H) continue; const q=yy*W+xx; if(!lab[q]&&ref[q]>200&&cur[q]<=10){ lab[q]=nl; st.push(q);} } }
      if(sz>=12&&sz<=0.015*tot) res.push([i,sz,[x0,y0,x1,y1]]); } }
  C.stop(); el.remove(); return [res, W, H]; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html', timeout=300000); pg.wait_for_timeout(8000); pg.evaluate('f=>window.__FZ=f', float(__import__('os').environ.get('FZ','150')))
    for c in sys.argv[1]:
        r,W,H=pg.evaluate(JS,[c,36]); print(c,W,H, r[:14])
    b.close()
