# §10 C-088 — Ritournelle de 1 à N paroles, par le vrai chemin : part visible de chaque coulée, part de la zone visible couverte, échelle
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
NMAX = int(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--n=')), '15'))
Z = (0, 100, 390, 710)
TITRES = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche', 'appeler mamie', 'finir la maquette', 'ranger le garage', 'faire les crêpes', 'réparer le vélo',
          'trier les photos', 'semer les radis', 'nager le mardi', 'lire Proust', 'planter un arbre', 'écrire à Paul', 'peindre la porte']
def aire(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2
def coupe(P, x0, y0, x1, y1):
    def clip(P, dedans, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if dedans(b):
                if not dedans(a): out.append(inter(a, b))
                out.append(b)
            elif dedans(a): out.append(inter(a, b))
        return out
    def ix(xv):
        return lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / ((b[0] - a[0]) or 1e-9))
    def iy(yv):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yv - a[1]) / ((b[1] - a[1]) or 1e-9), yv)
    for d, it in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        P = clip(P, d, it)
        if not P: return []
    return P
def mesure(e):
    s, ox, oy = e['vue']; K = 2; im = Image.new('L', ((Z[2] - Z[0]) * K, (Z[3] - Z[1]) * K), 0); d = ImageDraw.Draw(im); vis = []
    for f in e['formes']:
        p = f['pts']; P = [(ox + s * p[i], oy + s * p[i + 1]) for i in range(0, len(p), 2)]
        a = aire(P); c = coupe(P, *Z); vis.append(aire(c) / a if a > 1 and c else 0.0)
        d.polygon([((x - Z[0]) * K, (y - Z[1]) * K) for x, y in P], fill=255)
    cov = sum(1 for v in im.getdata() if v) / float(im.size[0] * im.size[1])
    return vis, cov
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500); L = []
    for i in range(NMAX):
        B.plante(pg, TITRES[i]); pg.wait_for_timeout(5200)
        e = pg.evaluate("()=>{ var v=Toile.vue(); return {vue:[v.s,v.ox,v.oy], formes:(window._ritFormes||[]).slice(), n:promises.filter(p=>!p.draft).length, g:Toile_graines().length}; }")
        if len(e['formes']) != e['n']: pg.wait_for_timeout(1500); e = pg.evaluate("()=>{ var v=Toile.vue(); return {vue:[v.s,v.ox,v.oy], formes:(window._ritFormes||[]).slice(), n:promises.filter(p=>!p.draft).length, g:Toile_graines().length}; }")
        vis, cov = mesure(e) if e['formes'] else ([], 0)
        print('%2d paroles · %2d coulées · échelle %.3f · visible min %3.0f %% (méd. %3.0f %%) · couverture %3.0f %%' % (e['n'], len(e['formes']), e['vue'][0], 100 * min(vis or [0]), 100 * sorted(vis or [0])[len(vis or [0]) // 2], 100 * cov), flush=True)
        if '--cap' in sys.argv: B.capture(pg, 'scratchpad/v146/rit-%02d.png' % e['n'])
        L.append({'n': e['n'], 's': e['vue'][0], 'vis': vis, 'cov': cov})
    json.dump(L, open('scratchpad/v146/rit-mesure-%s.json' % ('avant' if 'avant' in F else 'app'), 'w'))
    b.close()
