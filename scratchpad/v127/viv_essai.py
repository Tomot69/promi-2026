# essai d'un monde : forcer N mouvements ; par mouvement — part max des pixels changés face à l'image d'avant, boîte, reste au retour, temps d'image
import sys, json
from playwright.sync_api import sync_playwright
M=sys.argv[1]; INIT=sys.argv[2] if len(sys.argv)>2 else ''; N=int(sys.argv[3]) if len(sys.argv)>3 else 3
JS=r"""async (N)=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=cv.width; o.height=cv.height; const g=o.getContext('2d',{willReadFrequently:true});
 const lit=()=>{ g.globalCompositeOperation='copy'; g.drawImage(cv,0,0); return g.getImageData(0,0,o.width,o.height).data; }; const out=[];
 for(let k=0;k<N;k++){ await new Promise(r=>setTimeout(r,700)); const av=lit(); const n0=Toile.vivant.journal().length; Toile.vivant.force(); let j=Toile.vivant.journal(); if(j.length===n0){ out.push({rate:1}); continue; } j=j[j.length-1];
   let mx=0, bx=0, im=0, lent=0, tp=performance.now(); const fin=performance.now()+j.d+500;
   await new Promise(res=>{ function f(t){ const dt=t-tp; tp=t; if(dt>lent) lent=dt; im++; if(im%4===0){ const d=lit(); let n=0,x0=1e9,x1=-1,y0=1e9,y1=-1; for(let i=0;i<d.length;i+=4){ if(d[i]!==av[i]||d[i+1]!==av[i+1]||d[i+2]!==av[i+2]){ n++; const p=i/4,x=p%o.width,y=(p/o.width)|0; if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y; } } const part=100*n/(d.length/4); if(part>mx){ mx=part; bx=n?100*(x1-x0+1)*(y1-y0+1)/(d.length/4):0; } } if(performance.now()<fin) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
   await new Promise(r=>setTimeout(r,300)); const d=lit(); let n=0; for(let i=0;i<d.length;i+=4) if(d[i]!==av[i]||d[i+1]!==av[i+1]||d[i+2]!==av[i+2]) n++;
   out.push({n:j.n, part:+mx.toFixed(3), boite:+bx.toFixed(1), reste:n, images:im, pire:Math.round(lent)}); }
 return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("window._vivantFixe=600000;"+INIT+";try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme(m);}", M); pg.wait_for_timeout(7000)
    for r in pg.evaluate(JS, N): print(M, json.dumps(r))
    b.close()
