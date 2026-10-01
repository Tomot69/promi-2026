# LE SEUIL DE LA PILULE, SUR L'ENCRE — l'analyse des captures de seuil_encre.py.
# Pour chaque champ : l'encre (pixels intérieurs qui s'écartent du fond), puis, pour tout rayon R, la distance de l'encre la plus
# proche à la courbe INTÉRIEURE du contour (distance exacte à un rectangle arrondi, trait déduit).
#   · « air au droit » = la même distance si le cadre était un rectangle (R = trait) : l'air que le texte a vers les bords droits.
#   · la courbe MANGE le texte de (air au droit − air au rayon R).
# Un champ QUI S'OUVRE garde sa première rangée à sa place en haut et sa dernière clouée en bas (c'est la loi de caleZone) :
# on rejoue sa hauteur en décalant l'encre de la moitié basse, et on lit où la pilule passe sous le repère.
import json, math, os
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); E = os.path.join(D, 'lignes', 'encre')
META = json.load(open(os.path.join(E, 'meta.json')))

def encre(m):
    im = np.asarray(Image.open(os.path.join(E, m['png'])).convert('RGB')).astype(np.int16)
    H, W = im.shape[:2]; k = m['w'] / W                      # px CSS par pixel d'image
    ys, xs = np.mgrid[0:H, 0:W]; x = (xs + 0.5) * k; y = (ys + 0.5) * k
    g = sdf(x, y, m['w'], m['h'], m['R'], m['bw'])
    dedans = g > 1.5                                           # le trait réel et son lissage sont exclus
    fond = np.median(im[dedans], axis=0)
    ecart = np.abs(im - fond).max(axis=2)
    ink = dedans & (ecart > 48)
    return x[ink], y[ink], fond

def sdf(x, y, w, h, R, bw):
    """distance (positive dedans) à la courbe intérieure d'un rectangle arrondi w×h, rayon R, trait bw"""
    R = min(R, h / 2.0, w / 2.0); ri = max(R - bw, 0.0)
    a, b = w / 2.0 - bw, h / 2.0 - bw
    dx = np.abs(x - w / 2.0) - (a - ri); dy = np.abs(y - h / 2.0) - (b - ri)
    return ri - np.hypot(np.maximum(dx, 0), np.maximum(dy, 0)) - np.minimum(np.maximum(dx, dy), 0)

def air(x, y, w, h, R, bw):
    return float(sdf(x, y, w, h, R, bw).min()) if len(x) else None

INK = {}
print('== 1 · CHAQUE CHAMP — air minimal de l\'encre au contour (px d\'écran 390)')
print('   %-44s %6s %5s  %9s %9s %9s %9s' % ('champ', 'h', 'R', 'au droit', 'en place', 'pilule', 'rayon 30'))
for cle, m in META.items():
    x, y, fond = encre(m); INK[cle] = (x, y)
    if not len(x): print('   %-44s — aucune encre' % cle); continue
    dr = air(x, y, m['w'], m['h'], m['bw'], m['bw'])
    print('   %-44s %6.1f %5.1f  %9.2f %9.2f %9.2f %9.2f' % (cle[:44], m['h'], m['R'], dr, air(x, y, m['w'], m['h'], m['R'], m['bw']),
          air(x, y, m['w'], m['h'], m['h'] / 2, m['bw']), air(x, y, m['w'], m['h'], 30, m['bw'])))

# le repère : l'air que tient un champ OUVERT, au rayon 30 (P, validé par Tom) — le plus serré de tous
ouverts = [k for k in META if META[k]['h'] > 100 and len(INK[k][0])]
C = min(air(*INK[k], META[k]['w'], META[k]['h'], 30, META[k]['bw']) for k in ouverts)
kC = min(ouverts, key=lambda k: air(*INK[k], META[k]['w'], META[k]['h'], 30, META[k]['bw']))
print('\n   repère C = l\'air le plus serré d\'un champ ouvert au rayon 30 : %.2f  (%s)' % (C, kC))

print('\n== 2 · UN CHAMP QUI S\'OUVRE, EN PILULE : à quelle hauteur l\'encre passe sous C')
COURBES = {}
for cle, m in META.items():
    x, y = INK[cle]
    if not len(x) or m['h'] < 80: continue
    haut = y < m['h'] / 2.0
    pts = []
    for i in range(0, 561):
        Hh = 60 + i * 0.25
        yy = np.where(haut, y, y + (Hh - m['h']))
        if yy.min() < 0 or (yy.max() > Hh): pts.append((Hh, None)); continue      # l'encre ne tient plus dans cette hauteur
        pts.append((Hh, air(x, yy, m['w'], Hh, Hh / 2.0, m['bw'])))
    COURBES[cle] = pts
    ok = [Hh for Hh, a in pts if a is not None]
    x_C = next((Hh for Hh, a in pts if a is not None and Hh >= m['h'] - 30 and a < C), None)
    # la dernière hauteur (en montant) où la pilule tient encore C
    tient = [Hh for Hh, a in pts if a is not None and a >= C]
    print('   %-44s h réel %6.1f · pilule à h réel %6.2f · tient C jusqu’à h = %s' % (cle[:44], m['h'], air(x, y, m['w'], m['h'], m['h'] / 2, m['bw']),
          ('%.2f' % max(tient)) if tient else 'jamais'))
json.dump({'C': C, 'C_champ': kC, 'courbes': COURBES}, open(os.path.join(E, 'analyse.json'), 'w'), ensure_ascii=False)
