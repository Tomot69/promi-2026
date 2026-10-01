# LE SEUIL DE LA PILULE — l'analyse, sur le relevé de seuil_pilule.py (aucun navigateur).
# La mesure est celle de tout le lot : distance du DÉBUT d'une ligne à la courbe intérieure du contour (coin haut-gauche pour
# une ligne de la moitié haute, bas-gauche pour la moitié basse, milieu-gauche si la ligne passe par le milieu ; distance au
# cercle de l'arrondi si le point y tombe, au bord droit du trait sinon). Le rayon ne touche pas la mise en page : on recalcule
# l'écart pour tout rayon, exactement. VALIDATION : au rayon en place, le calcul doit redonner l'écart lu au navigateur.
import json, math, os, sys
D = os.path.dirname(os.path.abspath(__file__))
ET = sys.argv[1] if len(sys.argv) > 1 else 'app'
REL = json.load(open(os.path.join(D, 'lignes', 'seuil_releve_%s.json' % ET)))

def ecart(ln, h, R, bw):
    R = min(R, h / 2.0); cy = h / 2.0; ri = R - bw
    hm, bm = ln['b'] < cy, ln['t'] > cy
    py = ln['t'] if hm else (ln['b'] if bm else (ln['t'] + ln['b']) / 2.0)
    ay = R if py < R else (h - R if py > h - R else py)
    return (ri - math.hypot(ln['l'] - R, py - ay)) if ln['l'] < R else (ln['l'] - bw)

def extremes(m, R):
    L = m['lignes']; return ecart(L[0], m['h'], R, m['bw']), ecart(L[-1], m['h'], R, m['bw'])

# 1 · validation + état des champs réels
print('== 1 · LES CHAMPS RÉELS (l\'écart des lignes extrêmes : au rayon en place / pilule h÷2 / rayon 30)')
vus, pire_valid = {}, 0.0
for ecran, champs in REL.items():
    for m in champs:
        if m['w'] < 300: continue                                   # le plateau (enh) et « Planter un Promi » ne sont pas des champs
        p0, d0 = extremes(m, m['rayon'])
        pire_valid = max(pire_valid, abs(p0 - m['nav_premiere']), abs(d0 - m['nav_derniere']))
        cle = (m['champ'], m['id'] or m['cls'], m['h'], len(m['lignes']))
        if cle in vus: continue
        vus[cle] = m
        pp, dp = extremes(m, m['h'] / 2.0); p3, d3 = extremes(m, 30.0)
        print('   %-16s %-18s h %6.1f · %d lignes · en place r%4.0f %5.1f/%5.1f · pilule %5.1f/%5.1f · r30 %5.1f/%5.1f   (%s)' % (
            m['champ'], (m['id'] or m['cls'])[:18], m['h'], len(m['lignes']), m['rayon'], p0, d0, pp, dp, p3, d3, ecran))
print('   validation : écart maximal calcul ↔ navigateur = %.3f px' % pire_valid)

# 2 · la courbe d'un champ qui S'OUVRE : sa première ligne garde sa place en haut, sa dernière sa place en bas, la hauteur
#     monte ; rayon h ÷ 2. On lit où l'écart passe sous chaque repère.
print('\n== 2 · UN CHAMP QUI S\'OUVRE, RAYON h ÷ 2 (la 1re ligne garde sa place en haut, la dernière en bas)')
def courbe(m, Hs):
    L = m['lignes']; h0 = m['h']; a = L[0]; z = L[-1]
    out = []
    for H in Hs:
        haut = dict(a); bas = {'l': z['l'], 't': z['t'] + (H - h0), 'b': z['b'] + (H - h0)}
        e1 = ecart(haut, H, H / 2.0, m['bw']); e2 = ecart(bas, H, H / 2.0, m['bw'])
        out.append((H, min(e1, e2)))
    return out
Hs = [60 + 0.25 * i for i in range(int((200 - 60) / 0.25) + 1)]
REPERES = [('reste au-dessus de l\'air d\'une ligne seule, 22', 21.9), ('13,5 · l\'air que tient le champ ouvert (rayon 30)', 13.5),
           ('12,9 · le champ à deux lignes, le plus serré validé', 12.86), ('0 · la courbe touche la ligne', 0.0)]
for cle, m in vus.items():
    if len(m['lignes']) < 2: continue
    c = courbe(m, Hs)
    print('   %-16s %-18s (1re ligne : gauche %.1f, haut %.1f · dernière : bas à %.1f du bord)' % (m['champ'], (m['id'] or m['cls'])[:18], m['lignes'][0]['l'], m['lignes'][0]['t'], m['h'] - m['lignes'][-1]['b']))
    for nom, g in REPERES:
        x = next((H for H, e in c if e < g - 1e-9), None)
        print('        passe sous %-50s à h = %s' % (nom, ('%.2f' % x) if x is not None else '> 200'))
json.dump({'courbes': {'%s|%s|%s' % (k[0], k[1], k[2]): courbe(m, Hs) for k, m in vus.items() if len(m['lignes']) >= 2}},
          open(os.path.join(D, 'lignes', 'seuil_courbes_%s.json' % ET), 'w'), ensure_ascii=False)
