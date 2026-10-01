# Preuve « la matière ne change pas » : deux versions de l'app, MÊME graine aléatoire (Math.random semé
# avant tout script), horloge figée au rendu ; Toile entière renderTo(c,2), clair et sombre, plusieurs semis.
# Usage : python3 preuve.py A.html B.html monde [graines...]
import sys, io, base64, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

A, B, MONDE = sys.argv[1], sys.argv[2], sys.argv[3]
GRAINES = [int(x) for x in sys.argv[4:]] or [1, 2, 3, 4, 5]
INIT = r"""(()=>{ let s=%d>>>0; Math.random=function(){ s=(s+0x6D2B79F5)>>>0; let t=s; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; })();"""
REND = r"""async (m)=>{ var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}
  Toile.setTheme(m); await new Promise(r=>setTimeout(r,2500));
  const T=performance.now()+100000; const pn=performance.now; performance.now=()=>T;
  const out={}; for(const cl of [true,false]){ const c=document.createElement('canvas'); window._shLabels=false; Toile.renderTo(c,2,cl); window._shLabels=undefined; out[cl?'clair':'sombre']=c.toDataURL('image/png'); }
  out.n=Toile.graines?Toile.graines():null; performance.now=pn; return out; }"""

def lab(a):
    a = a[..., :3].astype(np.float64) / 255
    a = np.where(a > 0.04045, ((a + 0.055) / 1.055) ** 2.4, a / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = a @ M.T / np.array([0.95047, 1, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)

def img(d): return np.asarray(Image.open(io.BytesIO(base64.b64decode(d.split(',')[1]))).convert('RGBA')).astype(np.int16)

def rend(p, app, graine):
    ctx = p.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script(INIT % graine)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + app); pg.wait_for_timeout(6800)
    r = pg.evaluate(REND, MONDE); ctx.close(); return r

pire = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for gr in GRAINES:
        ra, rb = rend(b, A, gr), rend(b, B, gr)
        for th in ('clair', 'sombre'):
            ia, ib = img(ra[th]), img(rb[th])
            d = np.abs(ia - ib).max(-1)
            de = np.sqrt(((lab(ia) - lab(ib)) ** 2).sum(-1))
            part = (d > 2).mean() * 100
            print(f"graine {gr} {th:6s} graines={ra['n']}/{rb['n']}  px≠(>2 niv) {part:6.3f} %  écart max {d.max():3d} niv  ΔE moy {de.mean():.3f}  ΔE max {de.max():.1f}  ΔE>2 {(de>2).mean()*100:.3f} %")
            pire = max(pire, part)
    b.close()
print('PIRE part de pixels changés :', round(pire, 3), '%')
