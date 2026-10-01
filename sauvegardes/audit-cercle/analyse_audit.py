# LE CERCLE — ANALYSE DU RELEVÉ À L'ÉCRAN (audit.json, produit par audit_ecran.py).
# Confronte chaque nœud VISIBLE aux interdits du §6 de la spec et de CLAUDE.md §3/§6 :
#   texte < 12 px · opacité < 72 % · face hors des six embarquées · fill ≠ color · texte illisible sur son fond
#   (contraste WCAG < 3 contre le fond opaque le plus proche qui le contient) · dégradé · ombre portée · ombre de
#   texte · flou ≠ 2,4 px · débordement LATÉRAL du cadre 390 (le vertical est un défilement légitime).
# Un constat est groupé par (surface, nœud, défaut) et dit dans quels thèmes/modes il se voit.
import json, os, re, sys
from collections import defaultdict

D = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(D, 'ecran', 'audit.json'), encoding='utf-8'))
FACES = {'Fraunces', 'Bricolage', 'Apfel', 'ApfelMid'}

def rgba(s):
    m = re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)', s or '')
    if not m: return None
    return tuple(float(x) for x in m.groups(default='1'))
def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
def contraste(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def fond(n, noeuds):
    """le fond opaque le plus petit qui contient la boîte du texte (dans l'ordre du relevé)"""
    best = None
    for m in noeuds:
        if m is n or not m['vis']: continue
        c = rgba(m['bg'])
        if not c or c[3] < 0.6: continue
        if m['x'] - 0.5 <= n['x'] and m['y'] - 0.5 <= n['y'] and m['x'] + m['w'] + 0.5 >= n['x'] + n['w'] and m['y'] + m['h'] + 0.5 >= n['y'] + n['h']:
            if best is None or m['w'] * m['h'] < best['w'] * best['h']: best = m
    return best

C = defaultdict(set)   # (surface, nœud, défaut) -> {combos}
NONJUGE = defaultdict(set)   # textes dont le contraste n'est pas jugeable par cet instrument
FAMILLES = defaultdict(set)
def note(surface, n, defaut, combo):
    C[(surface, n['sel'][:60] + (' « ' + n['txt'][:40] + ' »' if n['txt'] else ''), defaut)].add(combo)

def passe(surface, combo, noeuds, fonds_ecran):
    if not isinstance(noeuds, list): return
    for n in noeuds:
        if not n['vis'] or n['w'] < 1 or n['h'] < 1: continue
        if n['x'] + n['w'] < 0 or n['x'] > 390: continue            # hors champ latéral : rangé ailleurs
        if n['txt']:
            FAMILLES[n['ff']].add(surface)
            fs = float(n['fs'].replace('px', ''))
            if fs < 12: note(surface, n, 'texte à %.1f px (< 12)' % fs, combo)
            if n['op'] < 0.72: note(surface, n, 'opacité effective %.2f (< .72)' % n['op'], combo)
            if n['ff'] not in FACES: note(surface, n, 'face hors des six : %s' % n['ff'], combo)
            if n['fill'] and n['fill'] != n['col']: note(surface, n, 'fill %s ≠ color %s' % (n['fill'], n['col']), combo)
            f = fond(n, noeuds) or fonds_ecran
            tc, bc = rgba(n['fill'] or n['col']), rgba(f['bg']) if isinstance(f, dict) else None
            # deux cas où le vrai fond n'est PAS mesuré : un nœud qui le contient peint un dégradé (le contraste
            # n'a plus de sens contre sa couleur de fond) ; le texte est recouvert (le doigt tombe sur un autre nœud :
            # une étiquette floutée sous l'encart du §3.8 se lit contre l'encart, à tort). On ne juge pas, on le dit.
            sous_degrade = any('gradient' in (m['bgi'] or '') and m['x'] - .5 <= n['x'] and m['y'] - .5 <= n['y']
                               and m['x'] + m['w'] + .5 >= n['x'] + n['w'] and m['y'] + m['h'] + .5 >= n['y'] + n['h']
                               for m in noeuds if m['vis'] and m is not n) or 'gradient' in (n['bgi'] or '')
            recouvert = n['hit'] not in ('soi', None) and n['pe'] != 'none'
            # un canevas sous le texte (la Toile du Studio, le visuel de la page du Cercle) : sa peinture n'est pas
            # dans le relevé, le contraste contre la couleur de l'écran serait faux (le nom du monde sortait à 1,00)
            sur_canevas = any(m['sel'].startswith('canvas') and m['vis'] and m['x'] - 8 <= n['x'] + n['w'] / 2 <= m['x'] + m['w'] + 8
                              and m['y'] - 8 <= n['y'] + n['h'] / 2 <= m['y'] + m['h'] + 8 for m in noeuds)
            sous_degrade = sous_degrade or sur_canevas
            if (sous_degrade or recouvert or n['pe'] == 'none') and tc and bc:
                NONJUGE[surface].add(n['txt'][:30])
                tc = None
            if tc and bc and tc[3] > 0.3:
                k = contraste(tc, bc)
                if k < 3: note(surface, n, 'ILLISIBLE : contraste %.2f (%s sur %s, fond de %s)' % (k, n['fill'] or n['col'], f['bg'], f['sel'][:30]), combo)
        if 'gradient' in (n['bgi'] or ''): note(surface, n, 'dégradé : ' + n['bgi'][:50], combo)
        if n['sh'] and n['sh'] != 'none': note(surface, n, 'ombre portée : ' + n['sh'][:60], combo)
        if n['tsh'] and n['tsh'] != 'none': note(surface, n, 'ombre de texte : ' + n['tsh'][:60], combo)
        for fl in n['filt']:
            for r in re.findall(r'blur\(([\d.]+)px\)', fl):
                if abs(float(r) - 2.4) > 0.05:
                    note(surface, n, 'flou %s px (≠ 2,4)%s' % (r, (' — hérité de ' + fl.split('>')[0]) if '>' in fl else ''), combo)
        if n['x'] < -1 or n['x'] + n['w'] > 391: note(surface, n, 'déborde latéralement : x %.0f → %.0f' % (n['x'], n['x'] + n['w']), combo)

for groupe in ('scenes', 'studio_mondes'):
    for surface, combos in A[groupe].items():
        for combo, v in combos.items():
            noeuds = v.get('noeuds')
            fonds_ecran = None
            if isinstance(noeuds, list):
                # le fond de l'écran : le premier nœud opaque du relevé (la racine ou son premier fond)
                for m in noeuds:
                    c = rgba(m['bg'])
                    if c and c[3] > 0.6 and m['w'] >= 380: fonds_ecran = m; break
            passe(('studio_' if groupe == 'studio_mondes' else '') + surface, combo, noeuds, fonds_ecran)

par_surface = defaultdict(list)
for (s, n, d), cb in C.items(): par_surface[s].append((n, d, sorted(cb)))
for s in sorted(par_surface):
    print('\n── %s' % s)
    for n, d, cb in sorted(par_surface[s], key=lambda x: (x[1], x[0])):
        print('   %-62s %s   [%s]' % (n[:62], d, ' '.join(c.replace('dark', 'S').replace('light', 'C').replace('_gratuit', '·g').replace('_cercle', '·C') for c in cb)))
print('\nfamilles de polices vues sur du texte visible :', {k: len(v) for k, v in FAMILLES.items()})
print('\ncontraste NON JUGÉ (dégradé dessous, texte recouvert ou inerte) — à regarder sur la capture :')
for s in sorted(NONJUGE): print('   %-24s %s' % (s, ' | '.join(sorted(NONJUGE[s]))[:260]))

print('\n══ LES PORTES')
for sel, combos in A['portes'].items():
    for combo, v in combos.items():
        print('   %-36s %-14s doigt→%-30s → %s · premium %s→%s · héros %s' % (sel, combo, str(v['recoit'])[:30],
              v['apres']['couches'] or '(rien)', v['avant']['premium'], v['apres']['premium'], v['hero']))
print('\n══ LES ACHATS')
for b, v in A['achats'].items():
    print('   %-12s %s' % (b, json.dumps({k: (v[k] if not isinstance(v[k], dict) else {kk: v[k][kk] for kk in ('premium', 'couches', 'toast', 'owned', 'monde', 'ls') if kk in v[k]}) for k in v}, ensure_ascii=False)[:600]))
print('\n══ LES PINCEAUX')
for combo, v in A['pinceaux'].items():
    print('   %s : %s' % (combo, json.dumps(v, ensure_ascii=False)[:700]))
print('\n══ LE STUDIO, MONDE PAR MONDE')
for m, combos in A['studio_mondes'].items():
    for combo, v in combos.items():
        print('   %-9s %-14s %s · classes « %s » · monde appliqué %s' % (m, combo, v['comment'][:40], v['etat']['studio'][:80], v['etat']['monde']))
