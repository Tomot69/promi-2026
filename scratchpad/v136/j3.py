import io
S=io.open('redteam_couleurs_ref.py',encoding='utf-8').read()
a="""                    # E9 (v132) : le lilas éclairci de la page + d'un Promi en sombre ; le libellé « Supprimer ce Promi / ce Chiche » et sa corbeille
"""
assert S.count(a)==1
S=S.replace(a,"""                    # E11 (v136, Tom, 7 oct. 2026, C-059) : « en clair, le corps d'une fiche tenue (Promi et Chiche) devient la crème #F7F0DE ; la mention
                    #   TENU en #00341A en clair ». Sur les quatre écrans d'une fiche tenue, EN CLAIR seulement, ces trois échanges-là et rien d'autre :
                    #   la terre → la crème (fond) ; la crème → l'encre, pleine ou à 0,34 (texte et contours) ; l'amande → #00341A (texte).
                    if cle[1] == 'light' and cle[0] in ('fiche tenue', 'fiche chiche', 'Peaufiner', 'Peaufiner Chiche') and va and vr:
                        if pr_ == 'bg' and vr == 'rgb(43, 16, 32)' and va == 'rgb(247, 240, 222)': exceptions['E11'] = exceptions.get('E11', 0) + 1; continue
                        if pr_ in ('color', 'tfill', 'bT', 'bB', 'bL', 'bR') and vr == 'rgb(247, 240, 222)' and va in ('rgb(32, 25, 8)', 'rgba(32, 25, 8, 0.34)'): exceptions['E11'] = exceptions.get('E11', 0) + 1; continue
                        if pr_ in ('color', 'tfill') and vr == 'rgb(143, 224, 143)' and va == 'rgb(0, 52, 26)': exceptions['E11'] = exceptions.get('E11', 0) + 1; continue
"""+a)
a="  E7  v123 §2 : en sombre, l'ombre de la Pelote est une ellipse CRÈME"
assert S.count(a)==1
S=S.replace(a,"""  E11 v136 (Tom, 7 oct. 2026, C-059) : en clair, la fiche tenue (Promi et Chiche) et son Peaufiner : terre → crème, crème → encre, amande → #00341A.
      v136 (C-071) : le halo et l'ombre de la Pelote sont SUPPRIMÉS — E7 ne trouve plus son nœud (0), le nœud est listé « sans vis-à-vis ».
"""+a)
a="print('exceptions nommées : E1 Toile entière %d canevas"
assert S.count(a)==1
S=S.replace(a,"print('E11 fiche tenue en clair sur la crème (v136, C-059) : %d' % exceptions.get('E11', 0))\n"+a)
io.open('redteam_couleurs_ref.py','w',encoding='utf-8').write(S)
