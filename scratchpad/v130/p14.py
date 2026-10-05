import io
S=io.open('redteam_decisions.py',encoding='utf-8').read()
old="""CORPS_SOMBRE = {'promi': '#335382', 'chiche': '#7C3F58', 'nuee': '#5D4978'}     # v113 (Q358) ; ⚠ le Cercle : ajout de v113, pas une citation de Tom"""
new="""CORPS_SOMBRE = {'promi': '#8ACBE8', 'chiche': '#7C3F58', 'nuee': '#5D4978'}     # v113 (Q358) ; ⚠ le Cercle : ajout de v113, pas une citation de Tom
# ⚑ v130 (Tom, 5 oct. 2026) : le corps sombre d'un Promi #335382 est REMPLACÉ par le Pantone 13-4307 TPG « Tropical Breeze », #8ACBE8
#   (relevé par Tom sur son échantillon) — fiche Promi et page + d'un Promi ; le texte posé dessus passe à l'encre #201908.
SRC_TROPICAL = 'v130 (Tom, 5 oct. 2026) : Pantone 13-4307 TPG Tropical Breeze #8ACBE8, relevé sur son échantillon ; remplace #335382 (v113, Q358)'"""
assert S.count(old)==1; S=S.replace(old,new)
old="""        for nom, nat in (('Promi à tenir', 'promi'), ('Promi en cours', 'promi'), ('Chiche lancé', 'chiche'), ('Cercle', 'nuee')):
            D.append((nom, th, 'corps', CORPS_SOMBRE[nat], 'v113 (30 sept., Q358) : « option 2 »'))
        for nom in ('Promi à tenir', 'Promi en cours', 'Chiche lancé'):
            for z in ('aQui', 'echeance', 'trace'):
                D.append((nom, th, z, CREME, 'v16 (Q290) : les textes d\\'état sur fond sombre passent crème'))"""
new="""        for nom, nat in (('Promi à tenir', 'promi'), ('Promi en cours', 'promi'), ('Chiche lancé', 'chiche'), ('Cercle', 'nuee')):
            D.append((nom, th, 'corps', CORPS_SOMBRE[nat], SRC_TROPICAL if nat == 'promi' else 'v113 (30 sept., Q358) : « option 2 »'))
        for z in ('aQui', 'echeance', 'trace'):
            D.append(('Chiche lancé', th, z, CREME, 'v16 (Q290) : les textes d\\'état sur fond sombre passent crème'))
        for nom in ('Promi à tenir', 'Promi en cours'):
            for z in ('titre', 'aQui', 'echeance', 'trace'):
                D.append((nom, th, z, ENCRE, 'v130 (Tom, 5 oct. 2026) : « le texte posé sur ce corps passe à l\\'encre #201908 (titre, à-qui, échéance, mentions) »'))"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    if th == 'dark': D.append(('page +', th, 'corps', CORPS_SOMBRE['promi'], 'v113 (Q358) : « corps sombre de la fiche et de la page + »'))"""
new="""    if th == 'dark': D.append(('page +', th, 'corps', CORPS_SOMBRE['promi'], SRC_TROPICAL))"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_decisions.py','w',encoding='utf-8').write(S)
