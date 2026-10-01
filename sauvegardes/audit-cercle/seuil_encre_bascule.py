# LA BASCULE, au centième — repère C = l'air le plus serré des champs OUVERTS validés en P (NOTE, COMMENTAIRES, DESCRIPTION,
# au rayon 30, tous états). LE TRAIT de la Nuée en est EXCLU : sa rangée de pastilles est à 14,25 du bord droit (chantier 67),
# un défaut de composition — il ne peut pas servir d'étalon.
import json, os, numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seuil_encre_analyse.py')).read().split("INK = {}")[0])
INK = {k: encre(m)[:2] for k, m in META.items()}
def a(k, R, dy=0.0, H=None):
    m = META[k]; x, y = INK[k]; H = H or m['h']
    yy = np.where(y < m['h'] / 2.0, y, y + (H - m['h'])); return float(sdf(x, yy, m['w'], H, R, m['bw']).min())
def point(k, R):
    m = META[k]; x, y = INK[k]; g = sdf(x, y, m['w'], m['h'], R, m['bw']); i = int(g.argmin()); return round(float(x[i]), 1), round(float(y[i]), 1)
Z = [k for k in META if any(s in k for s in ('NOTE|', 'COMMENTAIRES|', 'DESCRIPTION|'))]
for k in Z: print('   étalon %-44s r30 %6.2f  au point %s' % (k[:44], a(k, 30), point(k, 30)))
C = min(a(k, 30) for k in Z); print('   ⇒ C = %.2f\n' % C)
print('   les champs à DEUX rangées (la frontière), en pilule, quand ils s\'ouvrent :')
bascules = []
for k in META:
    m = META[k]
    if not (80 <= m['h'] <= 100): continue
    Hs = np.arange(m['h'] - 10, m['h'] + 30, 0.01)
    tient = [H for H in Hs if a(k, H / 2.0, H=H) >= C]
    b = max(tient) if tient else None; bascules.append((b, k))
    print('     %-44s h %5.1f · pilule %6.2f au point %s · tient C jusqu’à h = %.2f' % (k[:44], m['h'], a(k, m['h'] / 2), point(k, m['h'] / 2), b))
print('\n   ⇒ la bascule : %.2f (le plus serré : %s)' % min(bascules))
print('\n   les champs à UNE ligne, en pilule :', ', '.join('%.2f' % a(k, META[k]['h'] / 2) for k in META if META[k]['h'] < 70 and '|s2-reg' in k and 'page+' not in k))
print('   LE TRAIT (Nuée), pilule %.2f · rayon 30 %.2f · au droit %.2f' % (a('Nuée · invite · LE TRAIT|npTrait', 59), a('Nuée · invite · LE TRAIT|npTrait', 30), a('Nuée · invite · LE TRAIT|npTrait', 2)))
