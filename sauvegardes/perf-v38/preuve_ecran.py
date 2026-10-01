# Preuve dans la MÊME page : la Toile vivante (#toileCv) peinte par l'ancien chemin (_perfAncien) puis le nouveau,
# horloge figée, même état ; clair et sombre ; plusieurs vues. Usage : python3 preuve_ecran.py [--webkit] monde...
import sys
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from outil import lab, img
WK = '--webkit' in sys.argv
MONDES = [a for a in sys.argv[1:] if not a.startswith('--')] or ['touffe']
JS = r"""async (a)=>{ var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}
  document.getElementById('device').classList.toggle('light',a.clair); Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,a.att||2500));
  const raf=()=>new Promise(r=>setTimeout(r,120));
  const cv=document.getElementById('toileCv'); const out=[];
  for(const vue of a.vues){
    if(vue) Toile.vue(vue.s,vue.ox,vue.oy); await new Promise(r=>setTimeout(r,1500));
    const T=performance.now()+100000; const pn=performance.now; performance.now=()=>T; const rq=window.requestAnimationFrame; window.requestAnimationFrame=cb=>rq.call(window,()=>cb(T));
    const paire=[];
    for(const anc of [true,true,false]){ window._perfAncien=anc; Toile.refigeCouleurs(); await raf(); await raf(); paire.push(cv.toDataURL('image/png')); }
    window._perfAncien=undefined; performance.now=pn; window.requestAnimationFrame=rq; out.push(paire); }
  return out; }"""
VUES = [None]
pire = 0
with sync_playwright() as p:
    b = (p.webkit if WK else p.chromium).launch()
    for m in MONDES:
        for clair in (True, False):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
            pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
            for k, (ra, ra2, rb) in enumerate(pg.evaluate(JS, {'m': m, 'clair': clair, 'vues': VUES, 'att': 12000})):
                ia, ia2, ib = img(ra), img(ra2), img(rb)
                t = np.abs(ia - ia2).max(-1); from PIL import Image as _I; _I.fromarray(np.concatenate([ia[...,:3],ia2[...,:3],np.repeat((t>2)[...,None]*255,3,-1)],1).astype(np.uint8)).save('scratchpad/perf/temoin.png'); print(f"   témoin ancien/ancien : px≠(>2) {(t>2).mean()*100:.4f} %  px≠ {(t>0).sum()}")
                d = np.abs(ia - ib).max(-1); de = np.sqrt(((lab(ia) - lab(ib)) ** 2).sum(-1))
                part = (d > 2).mean() * 100; pire = max(pire, part)
                print(f"{m:9s} {'clair ' if clair else 'sombre'} vue{k}  {ia.shape[1]}×{ia.shape[0]}  px≠(>2 niv) {part:.4f} %  max {d.max()} niv  ΔE moy {de.mean():.4f}  ΔE max {de.max():.1f}  px≠ {(d>0).sum()}")
            ctx.close()
    b.close()
print('PIRE', round(pire, 4), '%')
