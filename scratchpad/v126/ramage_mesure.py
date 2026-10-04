# C-009 — par événement de Ramage : (a) l'anneau au bord du disque, (b) le saut de toute la Toile à la fin. Variantes par drapeau.
import sys, json
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; DRAPEAU = sys.argv[2] if len(sys.argv)>2 else ''; OU = sys.argv[3] if len(sys.argv)>3 else 'studio'; MOT = sys.argv[4] if len(sys.argv)>4 else 'webkit'
JS = r"""async ([sel,duree])=>{ const cv=document.querySelector(sel); const W=cv.width, H=cv.height; const o=document.createElement('canvas'); const k=Math.min(1, 400/W); o.width=Math.round(W*k); o.height=Math.round(H*k); const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; };
  let av=lit(), EV=[], cur=null, t0=performance.now(), calme=0;
  await new Promise(res=>{ function f(t){ const d=lit(); let n=0, x0=1e9,x1=-1,y0=1e9,y1=-1, faible=0;
      for(let i=0;i<d.length;i+=4){ const e=Math.max(Math.abs(d[i]-av[i]),Math.abs(d[i+1]-av[i+1]),Math.abs(d[i+2]-av[i+2])); if(e>12){ n++; const p=i/4, x=p%o.width, y=(p/o.width)|0; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
      const part=n/(d.length/4), boite=n?((x1-x0+1)*(y1-y0+1))/(d.length/4):0;
      if(n>30){ if(!cur){ cur={t:Math.round(t-t0), im:[]}; EV.push(cur); } cur.im.push([+(part*100).toFixed(2), +(boite*100).toFixed(1), n?[x0,y0,x1,y1]:null]); calme=0; }
      else if(cur && ++calme>12) cur=null;
      av=d; if(t-t0>duree) res(); else requestAnimationFrame(f); } requestAnimationFrame(f); });
  return {EV, w:o.width, h:o.height}; }"""
with sync_playwright() as p:
    b=(p.webkit.launch() if MOT=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']))
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){};"+DRAPEAU)
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500)
    R=pg.evaluate(JS, ['#stBg', 22000])
    for e in R['EV']:
        im=e['im']; fin=im[-1]; dern=[i for i in im if i[1]>60]   # une image où la boîte des changements couvre plus de 60 % de la Toile : le saut d'ensemble
        print('événement à %5d ms · %2d images · part changée par image : %s%s' % (e['t'], len(im), ' '.join('%.1f' % i[0] for i in im[:22]), '  ⚠ SAUT D\'ENSEMBLE (boîte %.0f %% de la Toile, %.1f %% des pixels)' % (dern[-1][1], dern[-1][0]) if dern else ''))
    print('erreur film :', pg.evaluate("()=>window._ramFilmErr||null"), '· worker :', pg.evaluate("()=>(window._ramFilmW||[]).length"))
    b.close()
