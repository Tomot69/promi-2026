# LA TOILE AU REPOS EST IDENTIQUE : dans la même page, après une plantation posée, on repeint la Toile vivante avec la
# transition coupée (`_transCoupe`) puis rétablie, horloge figée — l'écart doit être 0 pixel. python3 repos.py monde [--webkit]
import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1]; WK='--webkit' in sys.argv
JS=r"""async (m)=>{ Toile.setTheme(m); await new Promise(r=>setTimeout(r,3000)); Toile.addPromi(null); await new Promise(r=>setTimeout(r,3500));
 const cv=document.getElementById('toileCv'); const g=cv.getContext('2d');
 async function peint(coupe){ window._transCoupe=coupe; Toile.setHue(Toile.getHue()); await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); await new Promise(r=>setTimeout(r,400)); return g.getImageData(0,0,cv.width,cv.height).data; }
 const a=await peint(true), b=await peint(false), c=await peint(true); window._transCoupe=false;
 function diff(x,y){ let n=0; for(let i=0;i<x.length;i+=4) if(x[i]!==y[i]||x[i+1]!==y[i+1]||x[i+2]!==y[i+2]) n++; return n; }
 return {sans_avec:diff(a,b), temoin_sans_sans:diff(a,c), px:a.length/4}; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(M, 'webkit' if WK else 'chromium', pg.evaluate(JS,M)); b.close()
