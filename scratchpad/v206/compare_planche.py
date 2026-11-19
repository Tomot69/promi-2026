"""v206 — la planche d'un lot contre la référence, écran par écran : la part des pixels qui diffèrent de plus de 24 niveaux (sur un canal).
Le bruit : une seconde passe de la référence elle-même (la matière respire). Un écran du lot est « identique » s'il ne s'écarte pas plus que le bruit (+ 0,5 point).
python3 compare_planche.py <référence> <bruit> <lot>"""
import sys, os
import numpy as np
from PIL import Image
R, Bz, L = sys.argv[1:4]
def ecart(a, b):
    A = np.asarray(Image.open(a).convert('RGB'), dtype=np.int16); B_ = np.asarray(Image.open(b).convert('RGB'), dtype=np.int16)
    if A.shape != B_.shape: return 100.0
    return 100.0 * float((np.abs(A - B_).max(axis=2) > 24).mean())
ok = 0; n = 0; pires = []
for f in sorted(os.listdir(R)):
    if not f.endswith('.png') or f.startswith('PLANCHE'): continue
    if not (os.path.exists(os.path.join(L, f)) and os.path.exists(os.path.join(Bz, f))): print('manque', f); continue
    eb = ecart(os.path.join(R, f), os.path.join(Bz, f)); el = ecart(os.path.join(R, f), os.path.join(L, f)); n += 1
    bon = el <= eb + 0.5; ok += bon
    print('%s %-40s bruit %6.2f %%   lot %6.2f %%' % ('✅' if bon else '❌', f, eb, el))
print('%d/%d écrans dans le bruit' % (ok, n))
