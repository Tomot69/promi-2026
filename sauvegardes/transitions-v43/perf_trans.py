# Intervalle entre images pendant une ARRIVÉE puis un DÉPART (2,2 s chacun). python3 perf_trans.py monde [--webkit] [--taux=4]
import sys
from playwright.sync_api import sync_playwright
M=[a for a in sys.argv[1:] if not a.startswith('--')][0]; WK='--webkit' in sys.argv
RATE=int(([a.split('=')[1] for a in sys.argv if a.startswith('--taux=')] or ['1'])[0])
JS=r"""async (m)=>{ Toile.setTheme(m); await new Promise(r=>setTimeout(r,2600)); const o={};
 async function mesure(nom, geste){ const d=[]; let t0=performance.now(); const fin=t0+2200; geste();
   await new Promise(res=>{ function f(t){ d.push(t-t0); t0=t; if(t<fin) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
   d.sort((x,y)=>x-y); o[nom]={images:d.length, med:+d[d.length>>1].toFixed(1), p90:+d[Math.floor(d.length*.9)].toFixed(1), max:+d[d.length-1].toFixed(1)}; }
 await mesure('arrivée', ()=>Toile.addPromi(null)); await new Promise(r=>setTimeout(r,800));
 const ids=promises.filter(p=>!p.draft).map(p=>p.id); await mesure('départ', ()=>Toile.sync(ids.slice(1)));
 return o; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if RATE>1: ctx.new_cdp_session(pg).send('Emulation.setCPUThrottlingRate',{'rate':RATE})
    for k,v in pg.evaluate(JS,M).items(): print(('webkit' if WK else 'chromium×%d'%RATE), M, k, v)
    b.close()
