import io
S=io.open('redteam_flash_etat.py',encoding='utf-8').read()
old="""CREME, ORANGE = 'rgb(247, 240, 222)', 'rgb(221, 77, 35)'"""
new="""CREME, ORANGE = 'rgb(247, 240, 222)', 'rgb(221, 77, 35)'
# ⚑ v130 (Tom, 5 oct. 2026) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_flash_etat-avant-v130.py).
#   La règle d'avant : « les textes d'état sur fond sombre passent crème » (v16, Q290) — le corps sombre d'un Promi ÉTAIT sombre.
#   La décision qui la remplace sur la fiche Promi : le corps sombre devient Tropical Breeze #8ACBE8 et « le texte posé sur ce corps
#   passe à l'encre #201908 (titre, à-qui, échéance, mentions) ». Le contrôle protège la même chose — la couleur FINALE dès la
#   première image, jamais l'orange — avec la valeur d'aujourd'hui.
ENCRE = 'rgb(32, 25, 8)'"""
assert S.count(old)==1; S=S.replace(old,new)
old="""        if not pr or any(c != CREME for c in pr.get('c', {}).values()): premieres_ko += 1"""
new="""        if not pr or any(c != ENCRE for c in pr.get('c', {}).values()): premieres_ko += 1"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    t('1 · [sombre] la première image où ils paraissent les montre déjà crème', premieres_ko == 0"""
new="""    t('1 · [sombre] la première image où ils paraissent les montre déjà à l\\'encre #201908 (v130, corps Tropical Breeze)', premieres_ko == 0"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('redteam_flash_etat.py','w',encoding='utf-8').write(S)
