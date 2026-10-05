import io
S=io.open('CHANTIERS.md',encoding='utf-8').read().split('\n')
i=[k for k,l in enumerate(S) if l.startswith('| C-047 |')][0]
S[i+1:i+1]=[
"""| C-048 | 4 oct. · v130 §1 · RÉCIDIVE (règle du 23 sept., v29) | « Des captures de Toile à la place des dalles (BLOQUANT). Dans les fiches, l'Index, le Fil et le fil d'un Cercle, on voit de nouveau des morceaux de Toile capturés dans un cadre, au lieu de vraies dalles engendrées, avec leur forme et leur contour réels. C'est interdit, définitivement, dans le prototype comme dans Swift. » | EN COURS | — | redteam_decoupe | v130 |""",
"""| C-049 | 4 oct. · v130 §3 · RÉGRESSION | « Les écrans ne réagissent plus aux changements (BLOQUANT). Quand on plante ou qu'on retire une parole, l'Index, le Fil et la liste des dalles en bas de l'Aura ne se mettent pas à jour tout de suite, et la liste de l'Aura est incomplète. […] une seule source de vérité, et chaque écran qui s'y abonne. » | EN COURS | — | redteam_reactif | v130 |""",
"""| C-050 | 4 oct. · v130 §4 | « Le corps sombre des fiches Promi devient Tropical Breeze » : Pantone 13-4307 TPG, #8ACBE8, à la place de #335382 — fiche Promi et page + d'un Promi, en sombre ; le texte posé dessus passe à l'encre #201908. | EN COURS | — | redteam_decisions | v130 |"""]
for k,l in enumerate(S):
    if l.startswith('| C-002 |'):
        c=l.split(' | '); c[3]='EN COURS'; c[4]+=" ⚠ v130 — RÉCIDIVE signalée par Tom : en sombre, le contour dédoublé revient derrière la Pelote après la deuxième ouverture du Studio."; c[6]='v130 |'; S[k]=' | '.join(c)
    if l.startswith('| C-021 |'):
        c=l.split(' | '); c[6]='v131 |'; S[k]=' | '.join(c)
    if l.startswith('| C-006 |'):
        c=l.split(' | '); c[4]+=" v130 (Tom) : « La suite t'appartient. » sans point d'exclamation — le texte posé est le bon."; S[k]=' | '.join(c)
io.open('CHANTIERS.md','w',encoding='utf-8').write('\n'.join(S))
