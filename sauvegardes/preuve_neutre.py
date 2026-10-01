# -*- coding: utf-8 -*-
"""PREUVE — le contrôle « trait neutre » de releve-design mord encore après réécriture (§7).
   On passe le critère seul sur de vrais gris et sur les couleurs du jeu."""
import io
S = io.open('releve-design.py', encoding='utf-8').read()
i = S.find('ENCRES = {'); j = S.find('def comparer')
ns = {}; exec(S[i:j], ns); ctrl = ns['controler_couleurs']
CAS = [("un vrai gris moyen #888888", (136,136,136), True),
       ("le gris de sous-texte #83858C", (131,133,140), True),
       ("un gris froid #55576C", (85,87,108), True),
       ("l'encre brune du jeu #201908", (32,25,8), False),
       ("le papier du jeu #F7F0DE", (247,240,222), False),
       ("l'accent orange #DD4D23", (221,77,35), False),
       ("le mauve de Nuée #291547", (41,21,71), False)]
ok = 0
for nom, rgb, attendu in CAS:
    faux = {'clair/atenir': {'fiche · champ': {'boxShadow': 'rgb(%d, %d, %d) 0px 0px 0px 2px' % rgb}}}
    pris = bool(ctrl(faux))
    bon = (pris == attendu); ok += bon
    print(f"  {'✓' if bon else '✗'} {nom:34} rgb{rgb} → {'PRIS' if pris else 'passé'}")
print(f"{ok}/{len(CAS)}")
