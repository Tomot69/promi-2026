# -*- coding: utf-8 -*-
"""⚑ v192 (Tom, C-259 suite : « au défilement rapide, ça saute ») — LE TRAIT TIENT À LA JONCTION PENDANT L'ÉLAN.
Banc WebKit (banc_tom), horloge et hasard figés ; échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) et la fenêtre de Tom
(PYTHONPATH=scratchpad/v190/fenetretom PROMI_ECHELLE=tom). Cercle, Promi, Chiche. Un défilement LANCÉ à 1 500, 3 000 et 5 000 pt/s, avec l'élan (la décroissance d'iOS,
× 0,998 par ms), vers le bas depuis le repos, puis vers le haut depuis le bas ; une image toutes les 16,7 ms. Deux modes :
  vivant — le JavaScript tourne (une image d'application entre deux pas) ;
  gelé   — `requestAnimationFrame` est COUPÉ pendant tout l'élan : c'est le JavaScript en retard de Safari pendant l'élan, poussé au pire. La position du trait doit tenir
           sans lui ; seul l'aplatissement peut être en retard (Tom : « un retard d'une image dans l'aplatissement est acceptable ; un trait qui décroche, non »).
À chaque image, sur l'écran, autour du sommet de l'onde : le haut du trait est à la jonction (112 pt) à 0,5 pt près une fois accroché, ou à sa place de repos (le haut de
son empreinte − le défilement) à 0,5 pt près avant (plus un pixel de lecture) ; le trait se reconnaît à sa couleur — ni le champ ni le corps ; et il est là (aucune image sans trait). La forme vient du peintre de la fiche (`__ligne`) ou du tracé du
Cercle (`_onde.chemin`), rendue hors de l'écran — jamais de la couche jugée. Rouge sur v191 (la couche fixe, en mode gelé)."""
import sys, io, os, re; sys.path.insert(0, '.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['cercle', 'promi', 'chiche'])
MODES = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--modes=')), ['vivant', 'gele'])
VIT = [1500, 3000, 5000]
ECH = os.environ.get('PROMI_ECHELLE', '1'); J = 112
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-110s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True); return ok
# le haut de la vraie ligne, colonne par colonne (2 pt), rendue par son peintre hors de l'écran, en cotes de la fiche (défilement 0)
FORME = """()=>{ const c=document.getElementById('dpTrameCv'), dp=document.getElementById('detailPoster'), t=(c.getAttribute('data-trait')||'').split(','), base=+t[0], amp=+t[1], lw=10*(window._TRAIT_K||1.3);
  const cercle=dp.classList.contains('dp-mode-nuee')||dp.classList.contains('dp-nuee'), y=_onde.onde(base, amp), P=[]; for(let x=0;x<=390;x+=2) P.push(y(x));
  const E=3, o=document.createElement('canvas'); o.width=390*E; o.height=Math.ceil(Math.max(...P)+80)*E; const g=o.getContext('2d'); g.setTransform(E,0,0,E,0,0);
  if(cercle){ g.lineWidth=lw; g.lineCap='round'; g.lineJoin='round'; g.strokeStyle='#000'; g.beginPath(); _onde.chemin(g, y, 0, 390); g.stroke(); } else if(c.__ligne) c.__ligne(g, base, amp);
  const D=g.getImageData(0,0,o.width,o.height).data, EN=[]; for(let i=0;i<=195;i++){ const x=Math.min(o.width-1, i*2*E); let top=null; for(let yy=0;yy<o.height;yy++){ if(D[(yy*o.width+x)*4+3]>8){ top=yy/E; break; } } EN.push(top); }
  const mn=Math.min(...P); return {P, EN, mn, lw, s0:mn-lw/2-112, cercle, smax:dp.scrollHeight-dp.clientHeight, champ:c.getAttribute('data-champ')}; }"""
def ouvre(b, nat):
    ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); ctx.add_init_script(BJ.AMORCE); pg = B.ouvre(ctx, F, 6000)
    M = [['Marion', 'On commence quand ?'], ['Rachel', 'Je prends la farine.'], ['Nico', 'Samedi ?'], ['Lou', 'Je viens aussi.'], ['Adrien', 'Partant.']]
    if nat == 'cercle': pg.evaluate("m=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; m.forEach((x,i)=>o.comments.push({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); openEssaim('potager'); }", M)
    else: pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); p.status='encours'; delete p.parts; if(a[1]){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; p.who='Adrien'; } p.comments=a[2].map((x,i)=>({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); openDetail(p.id); }",
                      [{'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}[nat], nat == 'chiche', M])
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(50)
    pg.wait_for_timeout(500); return ctx, pg
def trajet(v0, s_dep, sens, smax):
    """l'élan d'iOS : v(t) = v0 · 0,998^t (t en ms), une image toutes les 16,7 ms, borné au défilement possible"""
    out = []; s = s_dep; v = v0 / 1000.0; t = 0
    while v > 0.02 and len(out) < 90:
        s = s + sens * v * 16.7; v *= 0.998 ** 16.7; s = max(0, min(smax, s)); out.append(round(s, 2))
        if s in (0, smax): break
    return out
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in NATS:
        ctx, pg = ouvre(b, nat); G = pg.evaluate(FORME); P, EN, mn, s0 = G['P'], G['EN'], G['mn'], G['s0']
        smax = G['smax']; d = B.dev(pg); k = d[4]; dpr = pg.evaluate("()=>devicePixelRatio")
        ic = min(range(len(P)), key=lambda i: P[i]); cols = [i for i in range(max(0, ic - 5), min(len(P), ic + 6))]
        rep = min(EN[i] for i in cols if EN[i] is not None)   # le haut de la ligne au repos, autour du sommet
        if smax < s0 + 45: juge('[%s · %s] la fiche défile au-delà de l\'accrochage (s0 + 45 = %.0f ; possible %.0f)' % (ECH, nat, s0 + 45, smax), False); ctx.close(); continue
        champ = None; corps = tuple(int(x) for x in re.findall(r'\d+', pg.evaluate("()=>getComputedStyle(document.getElementById('detailPoster')).backgroundColor"))[:3])
        for mode in MODES:
            mauvais = []; n = 0
            for v0 in VIT:
                for sens, dep in ((1, 0), (-1, smax)):
                    pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", dep); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
                    if mode == 'gele': pg.evaluate("()=>{ window.__rafVrai=window.requestAnimationFrame; window.requestAnimationFrame=function(){ return 0; }; }")
                    for s in trajet(v0, dep, sens, smax):
                        pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s)
                        if mode == 'vivant': pg.evaluate("()=>new Promise(r=>(window.__rafVrai||requestAnimationFrame)(()=>r()))")
                        im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px = im.load()
                        Y = lambda yy: int(round((d[1] + yy * k) * dpr)); XX = lambda xx: int(round((d[0] + xx * k) * dpr)); PT = lambda Yp: (Yp / dpr - d[1]) / k
                        if champ is None: champ = px[XX(4), Y(106)]
                        sr = pg.evaluate("()=>document.getElementById('detailPoster').scrollTop")
                        att = J if sr >= s0 else rep - sr
                        h = None
                        for i in cols:
                            X = XX(i * 2)
                            for yy in range(Y(max(104, att - (1.0 if sr >= s0 else 8))), Y(att + 10)):   # accroché : au-dessus de la jonction, c'est l'en-tête (sa bande, v187, posée par le JavaScript : absente en mode gelé) ; un trait décroché vers le haut garde des pixels sous 111 pt et reste pris
                                c = px[X, yy]
                                if sum(abs(c[j] - champ[j]) for j in range(3)) > 60 and sum(abs(c[j] - corps[j]) for j in range(3)) > 60:   # le TRAIT : ni le champ, ni le corps
                                    v = PT(yy); h = v if h is None or v < h else h; break
                        n += 1
                        if h is None or abs(h - att) > 0.5 + 1.0 / (dpr * k): mauvais.append((v0, sens, round(sr, 1), round(att, 2), h and round(h, 2)))
                    if mode == 'gele': pg.evaluate("()=>{ window.requestAnimationFrame=window.__rafVrai; }"); pg.wait_for_timeout(300)
            juge('[%s · %s · %s] à chaque image d\'un élan (1 500, 3 000, 5 000 pt/s, bas puis haut ; %d images) : le trait à la jonction (± 0,5 pt) ou à sa place de repos, jamais absent'
                 % (ECH, nat, mode, n), not mauvais, (len(mauvais), mauvais[:4]))
        juge('[%s · %s] aucune erreur de page' % (ECH, nat), not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
