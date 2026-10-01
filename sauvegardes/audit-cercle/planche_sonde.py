# LE JUGE DE LA PLANCHE DOIT ROUGIR SUR UNE PLANCHE FAUTIVE (CLAUDE §7) — la sonde.
# Copie PLANCHE-CERCLE.html en sauvegardes/audit-cercle/planche/sonde.html et pose QUATRE défauts dans le premier cadre
# (sombre, à l'ouverture) — chacun de la forme que le contrôle prétend attraper :
#   1 · une note à 10 px                       → « <12px »
#   2 · « soit 2,42 €/mois » remonté sur « 29 € » → recouvrement
#   3 · un texte #1B1E3A sur le fond #12142A     → contraste < 4,5
#   4 · un bloc qui sort à droite (x 330 → 450)  → hors cadre
# Le juge est ensuite passé sur la sonde : il doit nommer les quatre. La planche livrée n'est pas touchée.
import os
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(D, '..', '..'))
S = open(os.path.join(R, 'PLANCHE-CERCLE.html'), encoding='utf-8').read()
cle = 'data-cadre="cercle_dk_haut"'
assert S.count(cle) == 1, 'cadre absent ou multiple'
i = S.index(cle); j = S.index('<div class="plat"', i)
defauts = ('<div class="note sonde" style="top:760px;font-size:10px;color:#F4EEE1">SONDE dix pixels</div>'
           '<div class="note sonde" style="top:300px;color:#1B1E3A">SONDE ton sur ton</div>'
           '<div class="btn sonde" style="top:420px;left:330px;width:120px;color:#F4EEE1;border-color:#F4EEE1">SONDE</div>')
S2 = S[:j] + defauts + S[j:]
old = '<div class="sous" style="top:678px">'
assert S2.count(old) >= 1
k = S2.index(old, i)                       # le premier « sous » du cadre sondé
S2 = S2[:k] + '<div class="sous" style="top:640px">' + S2[k + len(old):]
open(os.path.join(D, 'planche', 'sonde.html'), 'w', encoding='utf-8').write(S2)
print('sonde écrite : sauvegardes/audit-cercle/planche/sonde.html')
