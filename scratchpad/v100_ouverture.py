# 1re ouverture d'une Nuée : barre en place (y 804), plus longue image, bande complète (_nueeSemis.sautees == 0).
import sys
from playwright.sync_api import sync_playwright
APP=sys.argv[1]; WK='--webkit' in sys.argv
SUIT=r"""()=>new Promise(res=>{ const t0=performance.now(); let k=null; for(const q in NUE){k=q;break;} closeAll(); openNueeDetail(k);
  let prev=t0, pire=0, barre=null, complet=null;
  (function f(){ const t=performance.now(); pire=Math.max(pire,t-prev); prev=t;
    const b=document.querySelector('#dpDetails .dpd-tog'); const y=b?Math.round(b.getBoundingClientRect().top):null;
    if(barre==null && y===804) barre=Math.round(t-t0);
    const s=window._nueeSemis; if(complet==null && s && s.cle===k && !s.sautees && s.cases && s.cases.length) complet=Math.round(t-t0);
    if(t-t0<4000) requestAnimationFrame(f); else res({barre:barre, pire:Math.round(pire), complet:complet, cases:(window._nueeSemis||{}).cases?window._nueeSemis.cases.length:0}); })(); })"""
with sync_playwright() as p:
    for k in range(1):
        b=p.webkit.launch() if WK else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(2000)
        print(APP, 'WebKit' if WK else 'Chromium', pg.evaluate(SUIT), flush=True); b.close()
