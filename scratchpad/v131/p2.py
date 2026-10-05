import io,re
def patch(f, reps):
    S=io.open(f,encoding='utf-8').read()
    for a,b in reps:
        assert S.count(a)==1,(f,S.count(a),a[:70]); S=S.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(S)
# ── décisions
patch('redteam_decisions.py',[
("""CORPS_SOMBRE = {'promi': '#8ACBE8',""","""CORPS_SOMBRE = {'promi': '#273CEB',"""),
("""SRC_TROPICAL = 'v130 (Tom, 5 oct. 2026) : Pantone 13-4307 TPG Tropical Breeze #8ACBE8, relevé sur son échantillon ; remplace #335382 (v113, Q358)'""",
 """# ⚑ v131 (Tom, 5 oct. 2026) : « Tropical Breeze est écarté (trop proche du bleu du champ) » — le corps sombre d'un Promi devient le
#   COBALT ÉLECTRIQUE #273CEB (fiche Promi et page + d'un Promi) ; « le texte posé sur ce corps redevient crème #F7F0DE, comme avant ».
SRC_TROPICAL = 'v131 (Tom, 5 oct. 2026) : cobalt électrique #273CEB ; remplace Tropical Breeze #8ACBE8 (v130, écarté) et #335382 (v113, Q358)'"""),
("""                D.append((nom, th, z, ENCRE, 'v130 (Tom, 5 oct. 2026) : « le texte posé sur ce corps passe à l\\'encre #201908 (titre, à-qui, échéance, mentions) »'))""",
 """                D.append((nom, th, z, CREME, 'v131 (Tom, 5 oct. 2026) : « le texte posé sur ce corps redevient crème #F7F0DE, comme avant Tropical : titre, à-qui, échéance, mentions »'))"""),
])
# ── flash d'état : la crème de nouveau
patch('redteam_flash_etat.py',[
("""ENCRE = 'rgb(32, 25, 8)'""","""ENCRE = 'rgb(32, 25, 8)'
# ⚑ v131 (Tom, 5 oct. 2026) — Tropical Breeze est écarté, le corps sombre d'un Promi est le cobalt #273CEB : « le texte posé sur ce corps
#   redevient crème #F7F0DE, comme avant ». Le contrat revient à la crème (v16, Q290), avec cette source."""),
("""any(c != ENCRE for c in pr.get('c', {}).values())""","""any(c != CREME for c in pr.get('c', {}).values())"""),
("""les montre déjà à l\\'encre #201908 (v130, corps Tropical Breeze)'""","""les montre déjà crème (v131, corps cobalt)'"""),
])
# ── murs : contrôle 7, l'orange du cobalt
patch('redteam_murs.py',[
("""        MUR_ORANGE = 'rgb(255, 122, 85)' if th != 'light' else 'rgb(251, 76, 13)'     # la décision, en dur (la phrase est mesurée sur le Peaufiner d'une fiche)""",
 """        # ⚑ v131 (Tom, 5 oct. 2026) : sur le corps cobalt #273CEB d'un Promi, « même teinte OKLCH que #FB4C0D, éclaircie jusqu'à 3:1 » → #FF8664
        #   (3,02:1 ; #FF7A55 n'y fait que 2,79:1). La phrase est mesurée sur le Peaufiner d'une fiche PROMI : c'est cette valeur, en dur.
        MUR_ORANGE = 'rgb(255, 134, 100)' if th != 'light' else 'rgb(251, 76, 13)'"""),
])
# ── Ma Parole ! : trois valeurs
patch('redteam_maparole.py',[
("""ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)')""","""ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)', 'rgb(255, 134, 100)')
# ⚑ v131 (Tom, 5 oct. 2026) — CONTRAT ÉTENDU (original : sauvegardes/redteam_maparole-avant-v131.py) : une TROISIÈME valeur, #FF8664, « même
#   teinte OKLCH que #FB4C0D, éclaircie jusqu'à 3:1 » sur le corps cobalt #273CEB d'un Promi (jeton --c-orange-maparole-cobalt). Elle non plus
#   n'existe nulle part ailleurs. Le Peaufiner mesuré en C est celui d'un Promi : en sombre, c'est elle qu'on attend."""),
("""HEX = re.compile(r'#(?:FB4C0D|FF7A55)\\b|\\b251\\s*,\\s*76\\s*,\\s*13\\b|\\b255\\s*,\\s*122\\s*,\\s*85\\b', re.I)""","""HEX = re.compile(r'#(?:FB4C0D|FF7A55|FF8664)\\b|\\b251\\s*,\\s*76\\s*,\\s*13\\b|\\b255\\s*,\\s*122\\s*,\\s*85\\b|\\b255\\s*,\\s*134\\s*,\\s*100\\b', re.I)"""),
("""--c-orange-maparole(-corps)?\\s*:\\s*#(FB4C0D|FF7A55)'""","""--c-orange-maparole(-corps|-cobalt)?\\s*:\\s*#(FB4C0D|FF7A55|FF8664)'"""),
("""re.search(r'#murPhrase(\\.sur-corps)?\\s*$', s.strip())""","""re.search(r'#murPhrase(\\.sur-corps(\\.sur-cobalt)?)?\\s*$', s.strip())"""),
("""        attendu = ORANGE[1] if th == 'dark' else ORANGE[0]""","""        attendu = ORANGE[2] if th == 'dark' else ORANGE[0]"""),
("""'#FF7A55' if th == 'dark' else '#FB4C0D'), bool(e.get('leve'))""","""'#FF8664 (corps cobalt d\\'un Promi)' if th == 'dark' else '#FB4C0D'), bool(e.get('leve'))"""),
])
# ── couleurs de référence : E8 = le cobalt, et lui seul
patch('redteam_couleurs_ref.py',[
("""MUR_ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)')""","""MUR_ORANGE = ('rgb(251, 76, 13)', 'rgb(255, 122, 85)', 'rgb(255, 134, 100)')"""),
("""                        if '51, 83, 130' in vr and va == vr.replace('51, 83, 130', '138, 203, 232'): exceptions['E8'] += 1; continue          # ① le corps
                        if pr_ in ('color', 'tfill', 'bT', 'bR', 'bB', 'bL', 'fill', 'stroke', 'outline') and va == 'rgb(32, 25, 8)': exceptions['E8'] += 1; continue   # ② l'encre""",
 """                        if '51, 83, 130' in vr and va == vr.replace('51, 83, 130', '39, 60, 235'): exceptions['E8'] += 1; continue          # le corps, et lui seul (v131 : le cobalt ; l'encre de Tropical est retirée)"""),
("""  E8  v130 (Tom, 5 oct. 2026) : le corps sombre d'un Promi #335382 devient Tropical Breeze #8ACBE8 (fiche Promi, page + d'un Promi),
      et ce qui est posé dessus passe à l'encre #201908.""","""  E8  v131 (Tom, 5 oct. 2026) : le corps sombre d'un Promi #335382 devient le COBALT #273CEB (fiche Promi, page + d'un Promi) ; le texte
      posé dessus reste crème, comme en v118 (Tropical Breeze, v130, est écarté — son exception d'encre ② est RETIRÉE).
      E3 s'étend à #FF8664, l'orange de « Ma Parole ! » sur ce corps."""),
])
print('ok')
