# Banc CONTRAT-MONDE §12 ter (Q5 bis) : 10 canevas DISTINCTS, renderTo(c,2) + relecture d'un pixel chacun (dessin forcé),
# et l'image à l'écran (Toile vivante repeinte à chaque image, sans relecture), moyenne par image.
# Usage : python3 banc.py [--webkit] [--ancien] [--taux=1,4] [--app=app.html] monde...
import sys, json
from playwright.sync_api import sync_playwright
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = {a.split('=')[0]: (a.split('=')[1] if '=' in a else True) for a in sys.argv[1:] if a.startswith('--')}
MONDES = args or ['touffe', 'gravure', 'madrure']
TAUX = [int(x) for x in str(opt.get('--taux', '1,4')).split(',')]
APP = opt.get('--app', 'app.html')
WK = '--webkit' in opt
JS = r"""async (a)=>{ const o={}; const K=10; window._perfAncien=a.ancien;
 for (const w of a.mondes){ Toile.setTheme(w); await new Promise(r=>setTimeout(r,600));
  if(w==='madrure'){ const c=document.createElement('canvas'); Toile.renderTo(c,2); c.getContext('2d').getImageData(0,0,1,1); }
  window._shLabels=false; const M=[], S=[];
  for(let r=0;r<5;r++){
    const cs=[]; for(let k=0;k<K;k++){ const c=document.createElement('canvas'); c.width=780; c.height=1688; c.getContext('2d').getImageData(0,0,1,1); cs.push(c); }
    let t0=performance.now(); for(const c of cs) Toile.renderTo(c,2); const t1=performance.now(); for(const c of cs) c.getContext('2d').getImageData(0,0,1,1);
    M.push((performance.now()-t0)/K); S.push((t1-t0)/K); }
  window._shLabels=undefined; [M,S].forEach(t=>t.sort((x,y)=>x-y));
  const d=[]; let n=0, t0=performance.now();
  await new Promise(res=>{ function f(t){ d.push(t-t0); t0=t; Toile.refigeCouleurs(); if(++n<70) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
  d.splice(0,8); const moy=d.reduce((x,y)=>x+y,0)/d.length;
  o[w]={calcul:+S[2].toFixed(1), dessin:+M[2].toFixed(1), ecran:+moy.toFixed(1)}; }
 if(a.mondes.includes('madrure')){ const B=[]; Toile.setTheme('madrure'); await new Promise(r=>setTimeout(r,600));
   for(let r=0;r<5;r++){ Toile._madrure(true); const c=document.createElement('canvas'); const t=performance.now(); Toile.renderTo(c,2); c.getContext('2d').getImageData(0,0,1,1); B.push(performance.now()-t); }
   B.sort((x,y)=>x-y); o.madrure_construction={med:+B[2].toFixed(1),max:+B[4].toFixed(1)}; }
 window._perfAncien=undefined; Toile.setTheme('encre'); return o;}"""
with sync_playwright() as p:
    b = (p.webkit if WK else p.chromium).launch()
    for rate in ([1] if WK else TAUX):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); pg = ctx.new_page()
        pg.goto('http://127.0.0.1:8752/' + APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if not WK: ctx.new_cdp_session(pg).send('Emulation.setCPUThrottlingRate', {'rate': rate})
        r = pg.evaluate(JS, {'mondes': MONDES, 'ancien': bool(opt.get('--ancien'))})
        print(('webkit' if WK else 'chromium ×%d' % rate), json.dumps(r, ensure_ascii=False)); ctx.close()
    b.close()
