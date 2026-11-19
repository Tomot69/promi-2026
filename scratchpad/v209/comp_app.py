"""v209 §1 — l'app (le style de la coquille) contre b9f98bd : hors de la bande de l'encart du haut (36 → 107 pt), chaque écran dans le bruit de la référence
(la seconde passe de Safari) ; dans la bande, l'encart décalé de 3 pt : la référence décalée de 3 pt (9 px) vers le bas recouvre le lot."""
import os, sys, numpy as np
from PIL import Image
R, L, Bz = 'app-ref', 'app-lotzz', 'pl-bruit1'; ok = n = 0
def im(p): return np.asarray(Image.open(p).convert('RGB'), dtype=np.int16)
for f in sorted(os.listdir(R)):
    if not f.endswith('.png') or f.startswith('PLANCHE') or 'studio_' in f: continue
    a, b = im(os.path.join(R, f)), im(os.path.join(L, f)); n += 1
    m = np.abs(a - b).max(axis=2) > 24; y0, y1 = 36 * 3, 107 * 3
    hors = 100.0 * (m[:y0].sum() + m[y1:].sum()) / (m.size - (y1 - y0) * m.shape[1])
    s = np.zeros_like(a); s[9:] = a[:-9]; md = np.abs(s[y0:y1] - b[y0:y1]).max(axis=2) > 24
    dans_dec = 100.0 * md.mean(); dans = 100.0 * m[y0:y1].mean()
    bz = os.path.join(Bz, f); eb = 100.0 * (np.abs(im(bz) - im(os.path.join('pl-ref1', f))).max(axis=2) > 24).mean() if os.path.exists(bz) else 0
    bon = hors <= eb + 0.5; ok += bon
    print('%s %-30s hors bande %5.2f %% (bruit %5.2f)   bande : %5.2f %% tel quel · %5.2f %% décalée de 3 pt' % ('✅' if bon else '❌', f, hors, eb, dans, dans_dec))
print('%d/%d écrans : rien ne bouge hors de la bande de l\'encart' % (ok, n))
