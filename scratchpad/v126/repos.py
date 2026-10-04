# §3 — un mouvement au repos existe-t-il déjà ? monde par monde : la Toile de l'accueil, sans rien toucher, 24 s, une lecture toutes les 300 ms
import sys, json
from playwright.sync_api import sync_playwright
MONDES = (sys.argv[1] if len(sys.argv)>1 else 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons,brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage').split(',')
DUREE = int(sys.argv[2]) if len(sys.argv)>2 else 24
JS = r"""async (duree)=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=195; o.height=Math.round(195*cv.height/cv.width); const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; };
  let av=lit(); const S=[]; const t0=performance.now(); let rafs=0, go=true; (function f(){ rafs++; if(go) requestAnimationFrame(f); })();
  while(performance.now()-t0<duree*1000){ await new Promise(r=>setTimeout(r,300)); const d=lit(); let n=0, sx=0, sy=0, x0=1e9,x1=-1,y0=1e9,y1=-1;
    for(let i=0;i<d.length;i+=4){ if(Math.abs(d[i]-av[i])>10||Math.abs(d[i+1]-av[i+1])>10||Math.abs(d[i+2]-av[i+2])>10){ n++; const p=i/4, x=p%o.width, y=(p/o.width)|0; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
    S.push([Math.round(performance.now()-t0), +(100*n/(d.length/4)).toFixed(2), n?[x0,y0,x1,y1]:null]); av=d; }
  go=false; return S; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    R={}
    for m in MONDES:
        pg.evaluate("m=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(7000)
        S=pg.evaluate(JS, DUREE); bouge=[s for s in S if s[1]>0.05]
        R[m]=S
        print('%-13s lectures %d · qui bougent %d (%.0f %%) · part de pixels changés : max %.2f %%, médiane des mouvements %.2f %% · instants (s) : %s' % (m, len(S), len(bouge), 100*len(bouge)/len(S), max(s[1] for s in S), (sorted(s[1] for s in bouge)[len(bouge)//2] if bouge else 0), ' '.join('%.1f' % (s[0]/1000) for s in bouge[:14])), flush=True)
    json.dump(R, open('scratchpad/v126/repos.json','w'))
    b.close()
