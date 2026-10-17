import re, io
p = 'CHANTIERS.md'; L = io.open(p, encoding='utf-8').read().split('\n')
VAL = {'C-088': 'Ritournelle', 'C-094': 'le guide en flaques (« flou ok »)', 'C-116': 'les commentaires', 'C-129': 'pas d\'emoji', 'C-135': 'la Pelote paraît tout de suite', 'C-142': 'le menu du + (« parfait » : on fige)'}
NOTE = {
 'C-118': '**v148 : le rideau descend à vitesse CONSTANTE (cause : l\'épaississement du trait puis un ease-in-out caché sous lui, et l\'horloge partie à l\'allocation du canevas) ; le reste validé par Tom.** ',
 'C-124': '**v148 : l\'Atkinson −7 % (25 / 22,3 pt) ; « Promi planté ! » pas à pas — le titre seul, puis un paragraphe par toucher, le texte remonte et les dalles descendent du même mouvement, 22 pt d\'air ; les dalles finissent à 722 pt (−16) ; « La suite t\'appartient » 9 pt plus bas ; les voisines choisies autour de la parole remontée (6 au lieu de 2).** ',
 'C-139': '**v148 : la page des variantes ne montre plus que l\'invitation (A les points s\'allument, B la flèche avance) ; aucune invitation animée dans l\'app (redteam_ronds E).** ',
 'C-140': '**v148 : les cartes ont la construction de la fiche (C-147) : les mêmes contrastes, Q513/Q514 valent pour elles.** ',
 'C-141': '**v148 : toutes les transitions de l\'onboarding en flaques (`_passageFlaques`), plus de balayage ni de fondu ; l\'arrivée douce des encarts validée par Tom, inchangée. redteam_transitions_onb réécrit (23/23 par thème).** ',
 'C-138': '**v148 : l\'échelle reprise dans CLAUDE.md (texte 25, liste 22,3, mot-clé 25, guide 29 en gras) — redteam_echelle_onboarding 10/10.** ',
}
NEUF = {
 'C-143': ('FAIT, EN ATTENTE DE TOM', 'v148 : cause — dans WebKit l\'animation `tenirPouls` battait l\'opacité nulle `!important` ; les peintres du geste ne peignent plus les ronds ; le chevron reste.', 'redteam_ronds 40/40'),
 'C-144': ('FAIT, EN ATTENTE DE TOM', 'v148 : « Parole tenue ! », « Défi relevé ! », centrés ; exception nommée au « ! » dans CLAUDE.md (avec « Ma Parole ! » et « Promi planté ! »).', 'redteam_tenir, redteam_engagement'),
 'C-145': ('FAIT, EN ATTENTE DE TOM', 'v148 : les deux phrases en Atkinson 700, 29 pt, interligne 1,45, mots-clés PromiLate 29 ; « monde » #8363AA / #C9A8F5 ; tracées (vu à l\'image, deux thèmes).', 'redteam_guide, redteam_echelle_onboarding'),
 'C-146': ('FAIT, EN ATTENTE DE TOM', 'v148 : toucher ailleurs à l\'étape du Studio = le rappel (la phrase du Studio réécrite) ; jamais le + avant le Studio ; reprise au lancement tant que le Studio n\'a pas été ouvert (`promi_guide` = « studio »).', 'redteam_ordre_guide 24/24 (rouge sur v147)'),
 'C-147': ('FAIT, EN ATTENTE DE TOM', 'v148 : cartes de l\'Index, du Fil et du fil d\'un Cercle construites comme la fiche, deux thèmes ; contraste du trait : Chiche et Cercle IMPOSSIBLES à 3:1 (Q513), l\'orange à tenir (Q514), la crête sur la terre (Q528) — rouge par décision.', 'redteam_contraste_trait (rouge par décision), redteam_decisions, redteam_couleurs_ref E19'),
 'C-148': ('FAIT, EN ATTENTE DE TOM', 'v148 : un ruban amande PLEIN qui suit l\'onde, 94 pt (80 %), bords légèrement irréguliers, plus de rectangle ; capture envoyée à Tom.', 'redteam_ruban 36/36'),
 'C-149': ('FAIT, EN ATTENTE DE TOM', 'v148 : les aides « se retourne » retirées ; « garder de côté » actif seulement si la page a changé (`_garderEtat`).', 'redteam_garder 40/40'),
}
out = []
for l in L:
    m = re.match(r'^\| (C-\d+) \|', l)
    if m:
        c = l.split(' | '); n = m.group(1)
        if n in VAL and c[3] != 'VALIDÉ PAR TOM':
            c[3] = 'VALIDÉ PAR TOM'; c[4] = '**v148 (Tom, 16 oct.) : VALIDÉ — %s.** ' % VAL[n] + c[4]
        elif n in NOTE:
            c[4] = NOTE[n] + c[4]
        elif n in NEUF:
            c[3], c[4] = NEUF[n][0], NEUF[n][1]; c[5] = NEUF[n][2]
        l = ' | '.join(c)
    out.append(l)
io.open(p, 'w', encoding='utf-8').write('\n'.join(out)); print('ok')
# les chantiers trouvés pendant la série (aucun travail fait dessus)
s = io.open(p, encoding='utf-8').read().rstrip('\n')
s += "\n| C-150 | 16 oct. · v148 (trouvé par la série) | `redteam_cercle_couleur` 6 : « rouvrir la page + efface le choix de couleur en attente » est ROUGE dans les deux thèmes — déjà sur v147 (rejoué sur `zz-av147.html` : 32/34). Une sonde qui suit le même chemin hors du juge voit la remise à zéro se faire : cause non nommée (le juge ou le produit). | OUVERT | v148 : constaté, rien n'est changé. | redteam_cercle_couleur | à fixer |"
s += "\n| C-151 | 16 oct. · v148 (trouvé en composant la capture des cartes) | Sur les cartes de l'Index (deux par ligne), un titre de deux lignes est ROGNÉ par la ligne d'état : « planter un / arbre », « le potager », « le grand plongeoir » (hauteur du texte 52 px pour 33 visibles). Identique sur v147, au pixel. | OUVERT | v148 : constaté (`scratchpad/v148/index_cmp.py`), rien n'est changé. | — | à fixer |\n"
io.open(p, 'w', encoding='utf-8').write(s); print('ajoutés')
