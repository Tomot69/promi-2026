import sys, json
from playwright.sync_api import sync_playwright
MONDES = (sys.argv[1] if len(sys.argv)>1 else 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons,brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage').split(',')
JS = r"""async ()=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=cv.width; o.height=cv.height; const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0); return g.getImageData(0,0,o.width,o.height).data; };
  const a=lit(); await new Promise(r=>setTimeout(r,400)); const a2=lit();
  const dif=(x,y)=>{ let n=0, s=0, x0=1e9,x1=-1,y0=1e9,y1=-1; for(let i=0;i<x.length;i+=4){ const e=Math.max(Math.abs(x[i]-y[i]),Math.abs(x[i+1]-y[i+1]),Math.abs(x[i+2]-y[i+2])); if(e>10){ n++; s+=e; const p=i/4, px=p%o.width, py=(p/o.width)|0; if(px<x0)x0=px; if(px>x1)x1=px; if(py<y0)y0=py; if(py>y1)y1=py; } } return [+(100*n/(x.length/4)).toFixed(3), n?Math.round(s/n):0, n?[x0,y0,x1-x0,y1-y0]:null]; };
  const bruit=dif(a,a2);
  window._vivantOff=false; Toile.vivant.force(); window._vivantOff=true; const j=Toile.vivant.journal().slice(-1)[0];
  let mx=[0,0,null], ims=0, t0=performance.now();
  while(performance.now()-t0<2300){ await new Promise(r=>requestAnimationFrame(r)); const d=dif(a,lit()); ims++; if(d[0]>mx[0]) mx=d; }
  await new Promise(r=>setTimeout(r,1500)); const fin=dif(a,lit());
  return {j, bruit:bruit[0], pendant:mx, apres:fin[0], w:o.width, h:o.height, boucle:Toile.vivant.boucle()}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}; window._vivantOff=true;")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for m in MONDES:
        pg.evaluate("m=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(6500)
        for rep_ in range(5):
          r=pg.evaluate(JS); pg.wait_for_timeout(600)
          print('   ', m, r['j']['n'], 'pendant %.3f' % r['pendant'][0], 'après %.3f' % r['apres'], flush=True)
        print('%-13s %d dalle(s) · pendant : %.3f %% des pixels (écart moyen %d, boîte %s sur %d×%d) · après %.3f %% · bruit %.3f %% · boucle arrêtée après : %s' % (m, r['j']['n'], r['pendant'][0], r['pendant'][1], r['pendant'][2], r['w'], r['h'], r['apres'], r['bruit'], not r['boucle']), flush=True)
    b.close()
