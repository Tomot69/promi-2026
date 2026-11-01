#!/usr/bin/env python3
"""redteam_fiches_orange.py — ⚑ v174 (Tom, 31 oct. 2026, C-214, C-215).

C-214 : « Sur les fiches (Promi, Chiche, Cercle), le libellé TRACE POUR … passe en orange #FB4C0D, comme sur la page +. »
C-215 : « Sur les fiches de Promi et de Chiche à moitié tracées, la partie orange ne couvre qu'un bout (43 pt, Q563). Elle couvre maintenant TOUTE la partie tracée, du départ
à gauche jusqu'au point du milieu, en #FB4C0D. La seconde moitié (à tenir) ne change pas. »

Banc comme Tom (WebKit), deux thèmes, échelles 1 et 0,79. La couleur en dur : (251, 76, 13).
  A · C-214 : le libellé « trace pour … » au style calculé et à l'image ; un autre mot du créneau (« à Rachel de tracer sa part ») garde l'encre de l'état
  B · C-215 : sur le canevas de la fiche, l'axe du trait est orange de x = 8 à x = 190 ; pas un pixel d'orange à droite du milieu au-delà de la pointe ; les points restent
Rouge sur v173 (`--fichier=zz-v173.html`). Le trait se lit sur l'axe de l'onde déclarée (`#dpTrameCv[data-trait]`, un pointeur, §7) ; le verdict vient des pixels.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ORANGE = (251, 76, 13)
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:200]), flush=True)
def proche(p, c=ORANGE, t=36): return abs(p[0] - c[0]) + abs(p[1] - c[1]) + abs(p[2] - c[2]) <= t
AXE = """()=>{ const c=document.getElementById('dpTrameCv'), v=(c.getAttribute('data-trait')||'').split(',').map(parseFloat); const y=window._onde.onde(v[0],v[1]);
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=[]; for(let x=8;x<=380;x+=2) r.push([x,y(x)]); return {pts:r,k:k,dx:D.left,dy:D.top}; }"""
def axe(pg):
    a = pg.evaluate(AXE); im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); K = im.width / 390.0
    return [(x, im.getpixel((min(im.width - 1, int(x * K)), min(im.height - 1, int(y * K))))) for x, y in a['pts']]
LIB = """()=>{ const t=document.getElementById('dptTrace'); if(!t||getComputedStyle(t).display==='none') return null; const c=getComputedStyle(t); return {mot:t.textContent, col:c.color, fill:c.webkitTextFillColor}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    print('fichier :', F, '· charge %.1f' % B.charge())
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            T = '[%s · %s]' % ('sombre' if sombre else 'clair', nom)
            ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
            B.plante_doigt(pg, 'écrire à Lou', 'moi', 0); pid = pg.evaluate("()=>promises.slice(-1)[0].id")
            B.plante_doigt(pg, 'marcher loin', 'moi', 1); pc = pg.evaluate("()=>promises.slice(-1)[0].id")
            B.plante_doigt(pg, 'lire un livre', 'Rachel', 1); pr = pg.evaluate("()=>promises.slice(-1)[0].id")
            pg.wait_for_timeout(500); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2800)
            l = pg.evaluate(LIB); juge(T + ' A · fiche Promi : « trace pour … » en #FB4C0D (style calculé, encre pleine)', l and l['mot'].lower().startswith('trace') and l['col'] == 'rgb(251, 76, 13)' and l['fill'] == 'rgb(251, 76, 13)', l)
            ax = axe(pg); g = [q for q in ax if q[0] <= 186]; dr = [q for q in ax if q[0] >= 215]; o_g = sum(1 for _, c in g if proche(c)); o_d = sum(1 for _, c in dr if proche(c))
            juge(T + ' B · fiche Promi : la partie tracée est orange du bord au milieu (≥ 96 %), rien à droite', o_g >= 0.96 * len(g) and o_d == 0, '%d/%d à gauche · %d à droite' % (o_g, len(g), o_d))
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800); pg.evaluate("id=>openDetail(id)", pc); pg.wait_for_timeout(2800)
            l = pg.evaluate(LIB); juge(T + ' A · fiche Chiche à soi : « trace pour lancer » en #FB4C0D', l and l['col'] == 'rgb(251, 76, 13)', l)
            ax = axe(pg); g = [q for q in ax if q[0] <= 186]; o_g = sum(1 for _, c in g if proche(c)); juge(T + ' B · fiche Chiche : même chose', o_g >= 0.96 * len(g), '%d/%d' % (o_g, len(g)))
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(800); pg.evaluate("id=>openDetail(id)", pr); pg.wait_for_timeout(2800)
            l = pg.evaluate(LIB); juge(T + ' A · un mot qui n\'est pas « trace … » garde l\'encre de l\'état', l and not l['mot'].lower().startswith('trace') and l['col'] != 'rgb(251, 76, 13)', l)
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
