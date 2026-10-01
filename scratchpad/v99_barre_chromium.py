# La barre Peaufiner d'une Nuée : sa position image par image après openNueeDetail (1re et 2e ouverture), WebKit.
import sys
from playwright.sync_api import sync_playwright
APP=sys.argv[1] if len(sys.argv)>1 else 'app.html'
SUIT=r"""()=>new Promise(res=>{ const L=[]; const t0=performance.now(); let k=null; for(const q in NUE){k=q;break;} closeAll(); openNueeDetail(k);
  (function f(){ const t=performance.now()-t0; const b=document.querySelector('#dpDetails .dpd-tog'); const y=b?Math.round(b.getBoundingClientRect().top):null;
    if(!L.length||L[L.length-1][1]!==y) L.push([Math.round(t),y]); if(t<3000) requestAnimationFrame(f); else res(L); })(); })"""
with sync_playwright() as p:
    for k in range(2):
        b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist']); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        print('page',k+1,'1re :',pg.evaluate(SUIT)); pg.wait_for_timeout(500)
        print('page',k+1,'2e  :',pg.evaluate(SUIT), flush=True)
        b.close()
