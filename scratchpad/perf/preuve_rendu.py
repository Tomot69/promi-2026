# Preuve dans la MÊME page, sur renderTo (Toile entière, 780×1688), horloge figée : variantes window._X comparées
# à la référence, et un témoin référence/référence. Plusieurs semis : on RESSÈME entre deux (Toile.reGray + graines
# tirées par la page). Usage : python3 preuve_rendu.py APP monde '{"ref":{...},"test":{...}}' [--webkit] [--semis=3]
import sys, json
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, __file__.rsplit('/', 1)[0]); from outil import lab, img
APP, MONDE, V = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]); WK = '--webkit' in sys.argv
NS = int(([a.split('=')[1] for a in sys.argv if a.startswith('--semis=')] or ['3'])[0])
JS = r"""async (a)=>{ var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}
  document.getElementById('device').classList.toggle('light',a.clair); Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,a.att));
  const T=performance.now()+100000; const pn=performance.now; performance.now=()=>T; window._shLabels=false;
  const r=(x)=>{ window._X=x; window._perfAncien=!!(x&&x.ancien); const c=document.createElement('canvas'); Toile.renderTo(c,2); window._X=null; window._perfAncien=undefined; return c.toDataURL('image/png'); };
  const out={ref:r(a.v.ref), ref2:r(a.v.ref), test:r(a.v.test), test2:r(a.v.test)};
  window._shLabels=undefined; performance.now=pn; return out; }"""
pire = 0
with sync_playwright() as p:
    b = (p.webkit if WK else p.chromium).launch()
    for s in range(NS):
        for clair in (True, False):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); pg = ctx.new_page()
            pg.goto('http://127.0.0.1:8752/' + APP); pg.wait_for_timeout(6800)
            if s: pg.evaluate("n=>{ for(let i=0;i<n;i++) Toile.addPromi(null); }", 6 * s)   # semis différents : on plante 0, 6, 12… dalles de plus
            o = pg.evaluate(JS, {'m': MONDE, 'clair': clair, 'v': V, 'att': 3000})
            a, a2, t, t2 = img(o['ref']), img(o['ref2']), img(o['test']), img(o['test2'])
            w = np.abs(a - a2).max(-1); w2 = np.abs(t - t2).max(-1); d = np.abs(a - t).max(-1); de = np.sqrt(((lab(a) - lab(t)) ** 2).sum(-1))
            if '--carte' in sys.argv:
                from PIL import Image as I; I.fromarray(np.concatenate([a[...,:3],np.repeat((d>0)[...,None]*255,3,-1)],1).astype(np.uint8)).save(f'scratchpad/perf/carte_{MONDE}_{s}_{int(clair)}.png')
                print('   d>10 :', int((d>10).sum()), ' d>20 :', int((d>20).sum()), ' d>40 :', int((d>40).sum())); I.fromarray(np.concatenate([a[...,:3],t[...,:3],np.repeat((d>10)[...,None]*255,3,-1)],1).astype(np.uint8)).save(f'scratchpad/perf/carte_{MONDE}_{s}_{int(clair)}.png')
            part = (d > 2).mean() * 100; pire = max(pire, part)
            print(f"{MONDE:9s} semis{s} {'clair ' if clair else 'sombre'}  témoin px≠ {(w>0).sum()} · 2e rendu≠1er {(w2>0).sum()}  |  px≠(>2 niv) {part:.4f} %  px≠ {(d>0).sum()}  max {d.max()} niv  ΔE moy {de.mean():.4f}  ΔE max {de.max():.1f}  ΔE>2 {(de>2).mean()*100:.4f} %")
            ctx.close()
    b.close()
print('PIRE', round(pire, 4), '%')
