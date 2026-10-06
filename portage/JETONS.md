# JETONS — couleurs, typographie, espacements de Promi

> Établi le 6 oct. 2026, lot v134. Accompagne `portage/JETONS.json`, qui fait foi pour les valeurs.
> Rien n'est inventé ici : chaque valeur porte la décision de Tom qui la fonde (date, lot) et sa source (`fichier:ligne` ou bloc de `CLAUDE.md`).
> Ce qui manque est listé en fin de document (« Trous ») et dans `JETONS.json › trous`.

## 1 · Comment lire le JSON

Unité : le point, sur un écran de référence **390 × 844**. Une couleur est un hexadécimal sRGB.

Chaque entrée a la même forme :

| Champ | Sens |
|---|---|
| `valeur` | la valeur à porter (ou `clair` / `sombre` quand elle bascule avec le thème) |
| `decision` | la citation courte, sa date, son lot. `null` = aucune décision de Tom retrouvée |
| `source` | où la valeur a été lue |
| `alerte` | deux sources se contredisent, ou la valeur est en attente |
| `morts` | les valeurs qui ont tenu ce rôle et qu'il ne faut pas reprendre |

Les sections :

| Section | Contenu |
|---|---|
| `couleurs.natures` | le CHAMP : Promi `#82AEF8`, Chiche `#FFB8D2`, Cercle `#C9A8F5` |
| `couleurs.etats` | la LIGNE : à tenir `#DD4D23`, en cours `#291547`, tenu `#00341A` ; l'amande `#8FE08F` |
| `couleurs.fonds` | pages, encre, terre et crête d'une fiche tenue, fond de la Toile |
| `couleurs.corps` | le corps d'une fiche par nature et par thème |
| `couleurs.textes` | ce qu'on pose sur un champ, un corps, la terre, le plateau |
| `couleurs.traits` | le trait posé sur un champ plein (`NATTRAIT`) et les libellés sur corps sombre (`NATCLAIR`) |
| `couleurs.maParole` | l'orange des mots « Ma Parole ! » dans les phrases des murs, et ses deux éclaircis |
| `couleurs.pelote` | sol, corps, halo, ombre, densité de la Pelote |
| `couleurs.mesuresSurCorpsSombrePromi` | les contrastes mesurés sur `#0E78F2` (v134) |
| `couleurs.decisions` | **le tableau de `redteam_decisions.py`, en entier** : 85 lignes (écran, thème, zone, valeur, décision) |
| `couleurs.exceptions[]` | chaque exception nommée |
| `couleurs.roles`, `couleurs.paletteFixe` | copie de `PROMI-TOKENS.json` (rôles clair/sombre ; jetons `--c-*`) |
| `typographie` | trois polices, cinq faces, sept niveaux, table de report, minima, tailles particulières |
| `espacements` | composants communs, cotes de l'Aura (B), paramètres du mode dessin, ondes, flous, durées |
| `rayons` | la grammaire des contours |
| `palettes` | les vingt-quatre palettes du Studio, dans l'ordre AFFICHÉ |
| `seuils` | tous les planchers mesurables |
| `trous` | ce qui n'a pas été trouvé ou se contredit |

**Deux niveaux de couleur, et lequel porter.** `couleurs.roles` bascule avec le thème : c'est ce que `Promi+Design.swift` emploie. `couleurs.paletteFixe` ne bascule jamais : c'est ce que les règles du prototype emploient, et beaucoup de ses 257 jetons sont de la dette. Pour le portage, les sections nommées (`natures`, `etats`, `fonds`, `corps`, `textes`, `traits`, `maParole`) priment sur les rôles quand ils diffèrent — trois rôles sont en retard (voir Trous).

## 2 · L'essentiel, en clair

### La règle des trois tons
Un écran de fiche porte toujours trois couleurs distinctes : **la dalle** (monde et palette du Studio), **le champ** (la nature, jamais l'état), **le trait** (l'état, jugé en ΔE sur le champ). Source : `CLAUDE.md` §3, repris le 30 sept. 2026.

### Natures et états

| | Valeur | Décision |
|---|---|---|
| Promi | `#82AEF8` | Tom, 17 sept. 2026, planche des correspondances |
| Chiche | `#FFB8D2` | idem |
| Cercle | `#C9A8F5` | idem — « le lilas est le champ, le violet est ce qu'on pose dessus » |
| à tenir | `#DD4D23` | Tom, 16 sept. ; Q262 (22 sept.) ; v132 : « ne sert à rien d'autre » |
| en cours | `#291547` | Tom, v7 (20 sept.) ; Q262 |
| tenu | `#00341A` | Tom, v7 (20 sept.) ; Q262 |
| tenu sur fond sombre, mention « TENU(E) », célébration | `#8FE08F` | Tom, 22 et 23 sept. |

En thème sombre, les **libellés** d'état (à-qui, échéance, « trace pour tenir », cartes) passent **crème** `#F7F0DE` (Q290, v16 ; Q374, v122). Les arcs et les traits gardent les trois valeurs.

### Fonds et corps

| Rôle | Clair | Sombre | Décision |
|---|---|---|---|
| page | `#F7F0DE` | `#050302` (seiche) | 16 sept. · v116, v121 |
| encre / texte | `#201908` | `#F7F0DE` | v7 (20 sept.) |
| corps d'une fiche Promi | `#F7F0DE` | **`#0E78F2`** | v122 · **v134, définitif** |
| corps d'une fiche Chiche | `#F7F0DE` | `#7C3F58` | v122 · v113 (Q358) |
| corps d'une fiche de Cercle | `#F7F0DE` | `#5D4978` | v122 · v113, validé v123 |
| corps d'une fiche tenue | `#2B1020` (terre) | `#2B1020` | v8 (21 sept.) ; crête `#0B4A2A` |
| fond de la Toile | `#DFCAA4` | `#050302` | v118 · v116 |

Pour le corps sombre d'un Promi, `#1A52F0`, `#273CEB`, `#8ACBE8` et `#335382` sont **morts**.

### Le trait sur le champ (`NATTRAIT`)
Promi `#022140` · Chiche `#3D0F23` · Cercle `#43291C` (valeur du code ; voir Trous). Seuil : ΔE (CIELAB) ≥ 15 sur le champ.

### « Ma Parole ! »
`#FB4C0D` partout ; `#FF7A55` sur les corps sombres Chiche et Cercle ; `#FED0C3` sur le corps sombre d'un Promi (3,01:1). Ces trois valeurs n'existent que dans les mots orange des phrases des murs.

### Typographie
Trois polices, cinq faces : **Gilbert 700** (sous-titres, libellés, navigation, en capitales), **Atkinson 400 · 500 · 700** (tout le texte), **PromiLate 400** (titres d'écran, mot-marque, phrases du trait). Rien sous 12 px ; aucune opacité sous 72 % sur un texte à lire. Gilbert : CC BY-SA 4.0, **crédit obligatoire dans « à propos », glyphes non modifiables**. Atkinson : SIL OFL 1.1. Depuis v96, Gilbert et Atkinson sont agrandies de 12 %.

### Contours
Trait 2 px, couleur du corps, rayon = hauteur ÷ 2 ; au-delà de 94,5 de haut, rayon 30. Plateau 342 × 60 à 24 / 40 ; Peaufiner 342 × 62 ; geste 118 ; disque 44 ; bouton photo 34 ; jour d'anneau 3 px d'arc.

### Palettes
Vingt-quatre, quatre tons chacune (poids ≈ 34 · 28 · 23 · 15 %), quatre rangées de six. Ordre affiché depuis v133 : **Primesautier, Ingénu, Candide…** Le défaut reste **Ingénu** (clé `signal`).

## 3 · Les exceptions nommées

Chacune est dans `couleurs.exceptions[]` avec sa valeur, son contraste mesuré, qui l'a décidée et quand.

| # | Exception | Où | Valeur · mesure | Décidée |
|---|---|---|---|---|
| 1 | Le texte crème sur le corps sombre d'un Promi | fiche et page + d'un Promi, sombre | `#F7F0DE` sur `#0E78F2` · 3,70:1 (petites mentions sous 4,5:1) | Tom, 6 oct. 2026, v134 |
| 2 | La phrase lilas de la page + sur ce corps | page + d'un Promi, sombre | `#F4EEFF` · 3,71:1 | **non décidée — Q403 ouverte** |
| 3 | Le trait « à tenir » sur ce corps | fiche Promi à tenir, sombre | `#DD4D23` · Δlum 1,7 · 1,03:1 · ΔE 126,2 | à savoir (Q404), rien retouché |
| 4 | Le filet crème sous le trait | la terre d'une fiche tenue, deux thèmes | `rgba(247,240,222,.55)` · crête/terre Δlum 15,7 | Tom, 30 sept., v114 — exigé là, interdit ailleurs |
| 5 | L'encre neutre de Touffe | monde Touffe, sombre | `#F4F2F0` | Tom, v115 |
| 6 | La couleur mère face au kaki | la jauge du Studio | seule couleur qui peut être kaki | Tom, 30 sept., v114 |
| 7 | Le brun de page face au kaki | encre `#201908` (h 87°) | hors périmètre : une page, pas une dalle | constat v114, v124 |
| 8 | La Pelote, seul volume | l'Aura | halo ΔE00 14 au ras, 0,12 D ; ombre | Tom, 30 sept., v114 ; constantes v123 |
| 9 | Le choix de taille du dessin | mode dessin | trois points de taille croissante | Tom, 4 oct., v127–v128 |
| 10 | Ingénu : la dalle dit la nature | palette par défaut seulement | bleu, rose, lilas, crème dalle | Tom, 21 sept., v17 |
| 11 | La bande haute teinte sa dalle | bande d'une fiche, champ de la page + | rampe de la nature (Q30) | Tom, 18 août |
| 12 | Le Studio garde ses flous | Studio | ailleurs 4,8 px | Tom, 30 sept., v104 |
| 13 | L'onboarding en Gilbert minuscules ; « Deuxio » à 3° | onboarding | `skewX(-3deg)` | Tom, 4 oct., v127, v129 |
| 14 | « Zzz » en minuscules | bouton du mode nuit | Z majuscule, zz minuscules | Tom, 2 oct., v118 (le Zzz est coupé depuis v120) |
| 15 | Le ✕ sur la surface de dessin | mode dessin | 44 pt, ✕ de 18 | Tom, 5 oct., v133 |
| 16 | Houle reste par image | monde Houle | 36 / 29 images | Tom, 27 sept., v61 |
| 17 | La pilule cède à 94,5 | tout contour | rayon 30 au-delà | Tom, 11 sept., Q203 |
| 18 | Les pertes d'air de v96 | page +, Index, Fil, Peaufiner, Réglages, Partager | −1,5 à −13 pt, voulues | Tom, 30 sept., v102 |

## 4 · Trous

Un trou est une valeur absente des sources lues, ou deux sources qui se contredisent sans décision pour trancher.

1. **⚠ TROU : le fond sombre du jeu.** `PROMI-TOKENS.json › roles.fond.sombre` vaut `#100D0B` ; les pages sombres sont peintes en seiche `#050302` (v116, v121, `redteam_decisions.py:31`). Le rôle n'a pas suivi. `Promi+Design.swift` porte donc `#100D0B`.
2. **⚠ TROU : les corps clairs du jeu.** `roles.corps-promi/chiche/nuee.clair` (`#CFE5FE`, `#FFF4FC`, `#EEE4F8`) « ne peignent pas le corps » (v122) : le corps clair est la crème. Leur emploi réel n'est pas établi.
3. **⚠ TROU : le trait et le texte sur le lilas d'un Cercle.** Le code dit `#43291C` (`app.html:14301`, v7) ; `CLAUDE.md` §3 dit `#291547` (18 sept., et la table reprise le 30 sept.) et `#43291C` (table des fonds).
4. **⚠ TROU : les « clairs » d'état.** `CLAUDE.md` §3 écrit encore « en cours, clair sur fond sombre : `#A77CF7` » ; Q262 et le jeu n'ont qu'une valeur par état.
5. **⚠ TROU : `ETAT-30-SEPTEMBRE-2026.md` est en retard** sur deux points : corps sombre d'un Promi `#1A52F0` (v134 : `#0E78F2`) et « un monde à l'unité 1 € » (v118 : 2 €).
6. **⚠ TROU : deux niveaux de texte du jeu contredisent le §6.** `titre.poids` = 600 (PromiLate n'a que 400) ; `meta.opacite` = 0,65 (plancher : 72 %).
7. **⚠ TROU : les sept niveaux ne sont pas câblés.** Les jetons `--t-*-taille` ont zéro consommateur (`CLAUDE.md` §8) : la taille réelle de chaque texte de chaque écran n'est pas dans ce document.
8. **⚠ TROU : la couleur de la barre Peaufiner** par nature et par thème (17 sept. : « corps mauve `#291547` » pour un Cercle ; C-059, v133 : « à la couleur de la nature » en clair).
9. **⚠ TROU : trois rôles sans décision** — `garde-de-cote` `#AE3929`, `corps-a-tenir`, `corps-garde` — contraires à « plus aucun aplat d'état n'existe ».
10. **⚠ TROU : `#F07A2E`** (« accent secondaire, célébration », 17 sept.) : emploi actuel non établi.
11. **⚠ TROU : le filet crème des anneaux** posés sur du sombre (v18) face à v113–v114 (« plus aucun filet crème autour des disques », sauf la fiche tenue).
12. **⚠ TROU : « Ma Parole ! » `#FB4C0D` sur un Peaufiner clair** : 2,65:1 (Promi) et 2,78:1 (Cercle) mesurés en v120 sur des corps qui n'étaient pas crème ; non remesuré, non tranché.
13. **⚠ TROU : Q403**, la phrase lilas sur `#0E78F2`.
14. **⚠ TROU : géométrie non relevée ici** — valeurs de repos de l'onde par état de fiche, rayon du coin de la Toile, cotes de l'accueil et de la barre du bas.
15. **⚠ TROU : les rampes de nature de Q30** (trois teintes par nature) : seules les valeurs d'août existent, dans une archive.
16. **⚠ TROU : deux choix attendent Tom** — le symbole du bouton photo (C-060) et la diversité des tailles de dalles (C-062).
