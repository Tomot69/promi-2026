## ⚑ L'ORBITE EN THÈME CLAIR — la peau s'éclaircit, le poil garde sa nature · 10 septembre 2026

> **`app.html` modifié** — md5 avant `8e579374b07507b90015e0f6d18bb437`, **après `a57f16aedee5ca615d82bd03438a9e25`**. Même bloc
> `lot-AURA-ORBITE`, refabriqué ; une cinquième retouche du peintre, dite (`PEINT_PEAU` dans `fabrique.py`).
> Aucune règle existante touchée, aucune ligne du moteur de la Toile. **Le thème sombre est intact** : la
> retouche ne joue que si `peauVers` est donné, et il ne l'est qu'en clair.

### 1 · LE DÉFAUT — l'Orbite n'avait jamais été peinte que sur fond sombre (Q182)
La planche peint sur `#16171B` (`_v_planche.js` l. 427). Dans l'app le canevas est transparent. La PEAU sous
le poil est la couleur du lieu × 0,64, et son alpha suit la part peinte : dans les cellules du sol, au poil
court, elle est semi-transparente — en sombre la page ne se voit pas, en clair le crème passe. Résultat en
clair : des plages bleu nuit à bords polygonaux, une tache presque carrée sur la sphère vide, et une boule
qui « crève l'écran » (boule ↔ page 130, contre 76 en sombre — métrique du §3).

### 2 · L'ARBITRAGE — mesuré, trois voies, puis trois essais (Tom : « ta version d'abord »)
```
                                          boule↔page   contour   dalles (médiane)
sombre (référence)                           ≈ 76         60          ≈ 57
A · poil de nature, peau → teinte claire      93          96           54     ← contour et dalles tiennent
B · poil inversé (corps sombre §1.3)          138         151          105    (des taches)
C · la « 2 » (poil clair, peau assombrie)     66          39 ✗         25 ✗   (plages revenues)
```
Tom : *« Fixe A. Ma règle était mal posée — les dalles sont le point dur. Un objet trop présent se corrige ; un
objet qui se dissout, non. »* Puis trois essais pour rattraper l'écart sans toucher aux dalles (même page) :
peau à 30 % vers le crème (90,6), **à 60 % (85,1 — retenu)**, poil 15 % plus clair (88,3). **Retenu : A2** —
la peau part ENTIÈREMENT vers la teinte claire de la nature (§1.2), elle-même tirée à 60 % vers le crème du
corps (§1.3). **Les 9 points au-dessus de 76 sont ASSUMÉS** : un excès de présence, pas une dissolution.

### 3 · LE CONTRÔLE — la famille 10 du juge, « la matière »
`releve-aura.py` (original `sauvegardes/releve-aura-avant-clair.py`) — valeurs EN DUR : boule ↔ page 76 en
sombre, 85 en clair, ± 8 ; contour ≥ 42 ; les dalles du clair pas moins lisibles qu'en sombre, **dans la même
page** (médiane et plus faible, à 5 près). ⚠ **Pas de seuil absolu sur les dalles** : leurs couleurs sont
tirées au hasard à chaque chargement — la médiane du sombre a varié de 57 à 41 d'une page à l'autre. Les îles
se découpent par le masque « sans îles » (une trame VIDE : `trame:null` fait lever le peintre — mesuré), en
composantes de 300 cellules au moins (en dessous, c'est du bruit du poil). **Prouvée contre de vrais défauts** (`preuve_matiere.py`, le code du juge
importé) : A2 tel quel — rien ; la « 2 » posée en clair — PRISE (écart 68,4 au lieu de 85, contour 39,2) ; la
boule sombre posée en clair — PRISE (écart 129,3). Et sur l'app d'avant (`8e579374…`) le juge prend 3 écarts
(clair à 129, et l'app ne sait pas masquer ses îles). **⚠ Réserve, dite telle quelle : la partie « dalles » n'a
pas encore été vue mordre SEULE** — sur la « 2 », ce sont l'écart et le contour qui ont pris ; dans cette page le
sombre de référence était lui-même faible (médiane 31,6, les dalles étant tirées au hasard), et les dalles de la
« 2 » ne passaient pas sous la barre. Q191.

### 4 · CE QUE L'INSTRUMENT M'A FAIT DIRE DE FAUX — deux fois
- La première passe de mesure a rendu des ZÉROS et une ligne « îles » qui recopiait « boule ↔ page », sans
  rien dire : le masque `trame:null` arrêtait le peintre. L'instrument vérifie désormais chaque image (pas
  d'erreur, boule peinte) et s'arrête s'il mesure du vide.
- La mesure des îles a changé de 57 à 41 d'une page à l'autre : dalles tirées au hasard, et du bruit dans le
  masque. D'où le filtre à 300 cellules et la comparaison dans la même page.

### 5 · CONTRÔLES
**Série complète, EN SÉRIE, sur l'app insérée `a57f16ae…`** — `bat_apres11.log`, 17 batteries, aucune
sortie en erreur : redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande
19/19 · redteam_toile 17/17 · redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite ·
redteam_vide 61/61 · redteam_air ✅ 442 paires · redteam_champ 32/32 · releve-design ✅ aucun écart ·
redteam_fonctions 22/22 · redteam_polices 0 couple absent · redteam_superpo 0 recouvrement · **releve-aura ✅ au
vert, dix familles** — la matière : sombre 76,8 (décidé 76), clair 81,8 (décidé 85), contour 94,7, dalles du clair
39,3 / 56,1 contre 31,2 / 55,3 en sombre. Preuve des 18 contrats sur la même app : ils mordent.
**Captures sur disque, regardées, non envoyées** (`sauvegardes/aura-orbite-lot/clair/captures/`, deux thèmes,
cinq phrases et l'état vide) : en clair la sphère est un pervenche homogène — plus aucune plage polygonale, le
poil se lit en sombre sur la peau claire, le contour est net ; **la sphère vide en clair n'a plus sa tache
presque carrée** (le pire cas, celui de la première impression), et son bouton est entier ; les îles se lisent,
l'orange franchement, les lilas plus doucement ; le sombre n'a pas bougé. L'air de la colonne, remesuré, est
intact (phrase → disques 27,1 / 27,7 ; libellés → bouton 28,5).

### 6 · LA SUITE (ordre de Tom)
La fiche de la personne, **audit d'abord** (Q184) · la densité et le capteur sur un vrai téléphone (Q178) ·
le Cercle. Le chantier 58 reste hors de tout ça, prioritaire au retour à la performance.
