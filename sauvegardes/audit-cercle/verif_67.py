# CHANTIER 67 — vérifié à l'écran, deux thèmes : l'encre de la carte LE TRAIT à la courbe, le contenu symétrique, le rail qui répond.
import io, os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'trait67' if len(sys.argv) <= 1 else 'trait67_preuve'); os.makedirs(OUT, exist_ok=True)
C = 15.19
def sdf(x, y, w, h, R, bw):
    R = min(R, h / 2.0, w / 2.0); ri = max(R - bw, 0.0); a, b = w / 2.0 - bw, h / 2.0 - bw
    dx = np.abs(x - w / 2.0) - (a - ri); dy = np.abs(y - h / 2.0) - (b - ri)
    return ri - np.hypot(np.maximum(dx, 0), np.maximum(dy, 0)) - np.minimum(np.maximum(dx, dy), 0)
def air(png, m):
    im = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16); H, W = im.shape[:2]; k = m['w'] / W
    ys, xs = np.mgrid[0:H, 0:W]; x = (xs + .5) * k; y = (ys + .5) * k; g = sdf(x, y, m['w'], m['h'], m['R'], m['bw'])
    dedans = g > 1.5; fond = np.median(im[dedans], axis=0); ink = dedans & (np.abs(im - fond).max(axis=2) > 48)
    return float(g[ink].min()) if ink.any() else None
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
J = r"""()=>{ const c=document.getElementById('npTrait'); c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(), k=getComputedStyle(c), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const R=(q)=>{ const e=c.querySelector(q); if(!e) return null; const b=e.getBoundingClientRect(); return [+((b.left-r.left)/s).toFixed(1), +((b.top-r.top)/s).toFixed(1), +(b.width/s).toFixed(1), +(b.height/s).toFixed(1)]; };
  return {x:r.left, y:r.top, w:r.width, h:r.height, bw:parseFloat(k.borderTopWidth), R:Math.min(parseFloat(k.borderTopLeftRadius)||0, r.height/2), lab:R('.np-lab'), val:R('.np-val'), rail:R('.pc-glisse'),
          valeur:(c.querySelector('.np-val')||{}).textContent}; }"""
KO = []
def ok(nom, cnd, d):
    print('   %s %s  %s' % ('✓' if cnd else '✗', nom, d))
    if not cnd: KO.append(nom)
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1800)
        m = pg.evaluate(J); pg.wait_for_timeout(300); m = pg.evaluate(J)
        png = pg.screenshot(clip={'x': m['x'], 'y': m['y'], 'width': m['w'], 'height': m['h']})
        a = air(png, m); bas = m['h'] - (m['rail'][1] + m['rail'][3])
        ok('%s · l’encre de la carte LE TRAIT tient l’air d’un champ ouvert (≥ %.2f)' % (th, C - .5), a is not None and a >= C - .5, 'encre à %.2f · rayon %.0f' % (a, m['R']))
        # les cotes CSS (22) se comptent DANS le trait de 2 : vus du bord extérieur, on compare les deux airs entre eux
        ok('%s · le contenu est symétrique : air du libellé en haut = air du rail en bas' % th, abs(m['lab'][1] - bas) <= 1, ('libellé en haut', m['lab'][1], 'rail en bas', round(bas, 1)))
        ok('%s · le rail reste dans la carte, sous le libellé (air ≥ 10)' % th, m['rail'][1] - (m['lab'][1] + m['lab'][3]) >= 10 and m['rail'][1] + m['rail'][3] <= m['h'], m['rail'])
        # le rail RÉPOND : toucher la 2e pastille change le trait de la Nuée (au doigt : le point doit tomber sur elle)
        t = pg.evaluate("""()=>{ const b=[...document.querySelectorAll('#npTrait .pc-t')][1]; if(!b) return null; const r=b.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
            return {x:r.left+r.width/2, y:r.top+r.height/2, nom:(b.querySelector('.pc-n')||b).textContent.trim(), doigt:!!(h&&(h===b||b.contains(h)))}; }""")
        if t: pg.mouse.click(t['x'], t['y']); pg.wait_for_timeout(700)
        v2 = pg.evaluate("()=>(document.querySelector('#npTrait .np-val')||{}).textContent")
        ok('%s · toucher une pastille change le trait (au doigt)' % th, bool(t) and t['doigt'] and v2 == t['nom'], (m['valeur'], '→', v2, t))
        pg.screenshot(path=os.path.join(OUT, '%s_trait.png' % th), clip={'x': m['x'] - 12, 'y': m['y'] - 12, 'width': m['w'] + 24, 'height': m['h'] + 24})
        pg.context.close()
    br.close()
print('══ %d raté(s)' % len(KO)); [print('   ✗ ' + k) for k in KO]
