#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_registre.py — AUCUN CHANTIER NE DISPARAÎT (v126, Tom, 4 oct. 2026). Sentinelle : dans la série de CHAQUE lot.

« Un numéro n'est jamais supprimé ni réutilisé ; seul Tom valide ou abandonne un chantier ; […] redteam_registre.py vérifie qu'aucun
numéro ne disparaît d'un commit à l'autre. Il doit rougir sur une copie amputée d'une ligne. »
  1 · les numéros se suivent de C-001 au dernier, sans trou ni doublon ;
  2 · chaque numéro présent dans un commit passé (les 30 derniers qui touchent le registre) est toujours là ;
  3 · chaque ligne porte un état de la liste, et ses sept colonnes ;
  4 · la demande d'un chantier (ses mots) n'a pas été vidée.
Sans navigateur. `python3 redteam_registre.py copie.md` juge une copie (la preuve : une copie amputée d'une ligne rougit).
"""
import sys, re, subprocess, os
ICI = os.path.dirname(os.path.abspath(__file__))
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), os.path.join(ICI, 'CHANTIERS.md'))
ETATS = ['OUVERT', 'EN COURS', 'PLANCHE EN ATTENTE DU CHOIX DE TOM', 'FAIT, EN ATTENTE DE TOM', 'VALIDÉ PAR TOM', 'REPORTÉ', 'ABANDONNÉ PAR TOM']
def lignes(txt):
    R = {}
    for l in txt.split('\n'):
        m = re.match(r'^\|\s*(C-(\d{3}))\s*\|', l)
        if m: R.setdefault(m.group(1), []).append([c.strip() for c in re.split(r'(?<!\\)\|', l)[1:-1]])
    return R
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail))
R = lignes(open(FICHIER, encoding='utf-8').read())
nums = sorted(int(k[2:]) for k in R)
juge('le registre existe et porte des chantiers', len(R) >= 30, '%d chantier(s)' % len(R))
trous = [n for n in range(1, (nums[-1] if nums else 0) + 1) if n not in nums]
juge('1 · les numéros se suivent de C-001 à C-%03d, sans trou' % (nums[-1] if nums else 0), not trous, 'manquant(s) : %s' % ', '.join('C-%03d' % n for n in trous[:8]))
juge('1 · aucun numéro en double', all(len(v) == 1 for v in R.values()), ', '.join(k for k, v in R.items() if len(v) > 1))
perdus = set(); vus = 0
try:
    revs = subprocess.run(['git', 'log', '-30', '--format=%h', '--', 'CHANTIERS.md'], cwd=ICI, capture_output=True, text=True).stdout.split()
    for r in revs:
        t = subprocess.run(['git', 'show', r + ':CHANTIERS.md'], cwd=ICI, capture_output=True, text=True).stdout
        A = lignes(t); vus += 1 if A else 0
        perdus |= set(A) - set(R)
except Exception as e: perdus.add('git : %s' % e)
juge('2 · aucun numéro d\'un commit passé n\'a disparu (%d version(s) du registre relue(s))' % vus, not perdus, 'disparu(s) : %s' % ', '.join(sorted(perdus)[:8]))
mauvais = [k for k, v in R.items() if len(v[0]) != 7 or v[0][3] not in ETATS]
juge('3 · chaque ligne porte ses sept colonnes et un état de la liste', not mauvais, ', '.join(sorted(mauvais)[:8]))
vides = [k for k, v in R.items() if len(v[0]) > 2 and len(v[0][2]) < 8]
juge('4 · aucune demande vidée', not vides, ', '.join(sorted(vides)[:8]))
print('\n%d / %d' % (ok, ok + len(ko)))
non = [(k, v[0]) for k, v in sorted(R.items()) if len(v[0]) == 7 and v[0][3] != 'VALIDÉ PAR TOM' and v[0][3] != 'ABANDONNÉ PAR TOM']
print('chantiers non validés : %d' % len(non))
sys.exit(1 if ko else 0)
