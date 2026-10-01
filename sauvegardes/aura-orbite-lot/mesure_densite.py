# LE PREMIER CONTRÔLE — la densité, mesurée dans l'app, sphère en rotation lente.
# ⚠ Aucun téléphone physique n'est joignable depuis cette machine. Ce qui suit est une
#   mesure de SUBSTITUTION, et elle se dit comme telle : Chromium sur le Mac Intel
#   i5-8279U du banc, puis le même processeur RALENTI ×4 (le profil « mobile moyen » de
#   Lighthouse) et ×6. On relève, par palier, le temps de `peint` par image (médiane, 9e
#   décile), et ce que fait le gouverneur quand on part du plus haut palier.
import sys, os, io, json, statistics
from playwright.sync_api import sync_playwright
ICI = os.path.dirname(os.path.abspath(__file__))
INJECTE = '--injecte' in sys.argv
CSS = io.open(os.path.join(ICI, 'aura.css'), encoding='utf-8').read()
MOT = io.open(os.path.join(ICI, 'moteur.js'), encoding='utf-8').read()
JS = io.open(os.path.join(ICI, 'aura.js'), encoding='utf-8').read()
ENREG = r"""async (n)=>{ const out=[]; let f0=_aura.etat().frames;
  await new Promise(r=>{ const t0=performance.now(); function f(){ const e=_aura.etat();
      if(e.frames!==f0){ f0=e.frames; out.push([e.palier, e.dernier]); }
      if(out.length<n && performance.now()-t0<40000) requestAnimationFrame(f); else r(); }
    requestAnimationFrame(f); });
  return out; }"""

def q(L, p):
    s = sorted(L); return s[min(len(s)-1, int(p*len(s)))]

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for rate in (1, 4, 6):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if INJECTE:
            pg.add_style_tag(content=CSS); pg.add_script_tag(content=MOT); pg.add_script_tag(content=JS)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(120):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>_aura.etat().pret&&_aura.etat().frames>10"): break
        cdp = pg.context.new_cdp_session(pg)
        cdp.send('Emulation.setCPUThrottlingRate', {'rate': rate})
        par = {}
        for i in (0, 1, 2):
            pg.evaluate("(i)=>_aura.palier(i)", i); pg.wait_for_timeout(600)
            for pal, ms in pg.evaluate(ENREG, 60):
                par.setdefault(pal, []).append(ms)
        # le gouverneur, livré à lui-même depuis le plus haut palier
        pg.evaluate("()=>{_aura.palier(0);}"); c0 = pg.evaluate("()=>_aura.etat().cede")
        pg.evaluate(ENREG, 150)
        e = pg.evaluate("()=>_aura.etat()")
        res[rate] = {'par': {k: (round(statistics.median(v), 1), round(q(v, 0.9), 1), len(v)) for k, v in par.items()},
                     'gouverneur': (e['palier'], e['cede'] - c0)}
        cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
        pg.close()
    b.close()

print('\nprocesseur   palier     médiane   9e décile   images   au-dessus de 16,7 ms ?')
for rate, r in res.items():
    for pal in sorted(r['par'], reverse=True):
        m, d9, n = r['par'][pal]
        print('   ×%d       %6d    %6.1f ms   %6.1f ms    %3d      %s' % (rate, pal, m, d9, n, 'OUI' if m > 16.7 else 'non'))
    print('   ×%d       le gouverneur, parti de 110 000 : se pose à %d (%d cession%s)\n'
          % (rate, r['gouverneur'][0], r['gouverneur'][1], 's' if r['gouverneur'][1] > 1 else ''))
json.dump(res, open(os.path.join(ICI, 'densite.json'), 'w'))
