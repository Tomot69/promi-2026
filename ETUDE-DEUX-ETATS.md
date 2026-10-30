# C-210 — Deux états au lieu de trois, un seul orange · étude (aucun code écrit)

Tom, 30 oct. 2026 : « L'état « à tenir » (date passée, parole pas tenue) est supprimé ; il ne reste que « en cours » et « tenu ». Tous les oranges de l'app reprennent EXACTEMENT #FB4C0D ; aucune variante dérivée ne reste (ni #DD4D23, ni #FF7A55, ni #FED0C3). La légende des états : ses pastilles deviennent des rectangles d'aperçu, de la hauteur d'une majuscule des mots de la légende. »

Périmètre de v173 : les états, les disques et la légende, les oranges. Rien d'autre. Toutes les mesures viennent de l'app servie (v172), en WebKit ; les lignes citées sont celles d'`app.html` à ce jour.

## 1 · Ce que Tom doit trancher

| # | Question | Ma proposition |
|---|---|---|
| D1 | « Ma Parole ! » sur le Peaufiner d'un Promi passe de 3,01:1 à **1,23:1** ; sur Chiche et Cercle, de 3,0 à 2,27. Voir `c210-oranges-lisibilite.png`. | Appliquer #FB4C0D sans exception, comme tu l'as écrit. Le mot se lit encore par sa teinte sur Chiche et Cercle, mais presque plus sur le bleu Promi. C'est toi qui juges sur la capture. |
| D2 | Un Chiche reçu dit « À RELEVER », et ce mot dépend de `status:'rate'` (l. 15529) : ce n'est pas une date passée. | Garder « À RELEVER », déduit du Chiche reçu et pas encore relevé, plus de `rate`. |
| D3 | `#F5AC9E` (saumon) colore les textes du Chiche sur la page + et son Peaufiner : c'est la teinte claire d'une NATURE, pas un état. | Ne pas y toucher : ce n'est pas un orange d'état, et C-204 interdit de changer une couleur non demandée. |
| D4 | La rampe des îles de la Pelote évite #DD4D23 (l. 33275, 37201) : non peint, mais présent dans le code. | Ne pas y toucher : elle change la couleur des îles, et la Pelote est hors périmètre. |
| D5 | « c'était le 12 oct. » reste une marque visible de retard (grille §12, questions 1 et 3). | Le poser comme tu le proposes, à l'encre, sans couleur ni mouvement. Si un testeur le lit comme un reproche, retirer la date suffit. |
| D6 | La règle écrite dit que #FB4C0D marque « le départ d'une action et rien d'autre ». Tes oranges restants (« demande », pastille du Fil, « UNE PAROLE T'ATTEND ») n'en sont pas. | Récrire la règle : #FB4C0D est le seul orange, il marque ce qui attend un geste. |

## 2 · Les données

| Point | Aujourd'hui | v173 |
|---|---|---|
| `echeancesDepassees` (l. 4306, enveloppée l. 42615) | passe `encours` → `rate` à la date passée | supprimée ; plus aucun écrivain de `rate` |
| Paroles déjà en `rate` sur les téléphones | restent `rate` | migrées en `encours` à la relecture de l'état, une fois, date gardée |
| Fil déjà enregistré (« … est à tenir », type `missed`) | pre « À TENIR », orange (l. 4581) | la branche retirée ; le texte stocké reformulé à la migration en « … : c'était le 12 oct. » |
| Sélecteur `#segStatus` (l. 3980, caché) | trois boutons | le bouton `rate` retiré |
| REPORTER, `_fpost` (l. 42624) | remet en `encours` | ne change plus l'état, seulement la date |
| `p.ech`, `dueISO`, `due` | inchangés | inchangés : la date reste une date (C-160) |
| Jeu de démonstration (l. 3097, 22021, 22058, 22067, 22091) | contient des `rate` | passés en `encours` (Chiche reçu : voir D2) |
| `keptOf`, chemins anciens (`STLAB`, `STCOL`, `SealViz`, `drawEmblem`) | comptent `rate` | `rate` retiré des tables ; aucun changement visible |

## 3 · Les écrans

| Écran | Aujourd'hui | v173 |
|---|---|---|
| Fiche, ligne d'état (l. 12767) | « À TENIR · DANS 2 JOURS » | « EN COURS · DANS 2 JOURS » ; date passée : « EN COURS · C'ÉTAIT LE 12 OCT. » (296 pt mesurés, tient dans les 342) |
| Fiche, à-qui et échéance en sombre et clair | orange « à tenir » (`f-atenir`, l. 5944, 15010) | la branche retirée : les couleurs de « en cours » |
| Fiche, trait (l. 14355) | orange | #291547, l'état « en cours » |
| Fiche, ruban de création (`ETAT_COL`, l. 42417) | `rate` jamais employé à la plantation | l'entrée retirée |
| Carte Index et Fil (`motEtat`, l. 19678) | « À TENIR · 2 JOURS » | « EN COURS · 2 JOURS » ; date passée : « C'ÉTAIT LE 12 OCT. » seul, 142,9 pt pour 141,9 aujourd'hui ; avec « EN COURS · » : 235,6 pt, ne tient pas |
| Mot du temps (`motDuTemps`, l. 6482) | `rate` ou `due<0` → « à tenir » orange | `due<0` → « c'était le 12 oct. », `vif:false`, sans couleur |
| Fil d'un Cercle (l. 6044, 6062, 16075, 16088) | orange pour `rate`, `nf-ocre` | la branche retirée |
| Index, filtre « À tenir » (l. 3748) | filtre `manquees` | retiré |
| Index, tri « À tenir en premier » (l. 3784) | tri `tenir` | retiré ; les autres tris ne bougent pas |
| Fil, filtre « À tenir » (l. 4499) | filtre `atenir` | retiré |
| Fil, rangée TRACER · REPORTER (l. 7127) | parole `rate` | parole `encours` à date passée : mêmes boutons, mêmes personnes |
| Fil, pre « UNE PAROLE T'ATTEND », « TON PROMI ARRIVE » (l. 4575) | #DD4D23 | #FB4C0D |
| Notifications | rien quand la date est passée | inchangé (R-023) |
| Aide de l'Aura, carte Noyaux (l. 34743) | « tenu, en cours, à tenir » | « tenu, en cours » |

## 4 · Les disques et la légende

| Point | Aujourd'hui | v173 |
|---|---|---|
| Noyaux de l'Aura (l. 30444, 30470) | trois arcs au plus | deux arcs : tenu, en cours ; un seul état : arc plein, jour de 3 pt conservé |
| Anneau du + (l. 37178) | trois parts | deux parts |
| Anneau des fiches (`karmaRing`, l. 15985) | trois parts | deux parts |
| Compteurs de l'Aura (l. 31020) | trois chiffres | deux chiffres, chacun sous son entrée |
| Légende de l'Aura (`.au-lg`) | pastille ronde 20 × 20 ; Gilbert 19,4 px, capitale **15,2 pt** | rectangle 24 × **15,2** pt, rayon 3 pt, écarts inchangés |
| Légende d'une personne (`.ps-lg`) | pastille 8 × 8 ; Atkinson 16 px, capitale **12,0 pt** | rectangle 19 × **12** pt, rayon 3 pt |
| Légende de l'aide (`.ah-legend`) | pastille 9 × 9 ; Atkinson 11 px, capitale **8,2 pt** | rectangle 13 × **8,2** pt, rayon 2 pt |
| Filet crème des pastilles de l'Aura | inset 1,4 pt à 55 % | gardé : sans lui, en sombre, #00341A fait 1,48:1 et #291547 1,27:1 sur la seiche |

La largeur (1,6 × la hauteur) et les rayons sont ma proposition : tu n'as fixé que la hauteur.

## 5 · Les oranges

Relevé sur 34 écrans × 2 thèmes × gratuit et Ma Parole !, couleurs réellement rendues, plus les phrases des murs. Ce qui est orange à l'écran se réduit à trois valeurs, plus #FF7A55 et #FED0C3 dans les murs. Les autres occurrences du code ne peignent rien sur ces écrans.

| Valeur | Où elle peint aujourd'hui | v173 |
|---|---|---|
| **#DD4D23** | états « à tenir » (arcs, légende, trait, texte) | disparaît avec l'état |
| **#DD4D23** | pastille `#filDot` de la barre, `.s4-att` (l. 36060), mot « demande » (l. 3751), pre du Fil | #FB4C0D |
| **#DD4D23** | héros de l'écran Ma Parole ! (`plHeroCv`, l. 7172 ; mélanges #D86457, #C96251…) | sa couleur de départ passe à #FB4C0D, les mélanges suivent |
| **#DD4D23** | onboarding d'origine et tuto (l. 6770–6776), `KC.O`, `SIG`, `SPECTRE` | #FB4C0D : chemins morts ou non vus sur ces écrans, remplacés pour qu'il n'en reste rien |
| **#FF7A55** | « Ma Parole ! » sur les corps Chiche et Cercle | #FB4C0D (D1) |
| **#FED0C3** | « Ma Parole ! » sur le corps Promi | #FB4C0D (D1) |
| **#FF8664** | commentaires seulement (l. 39346, 39351) | retirée |
| **#B8362D** | dérivée claire du héros (l. 6718), jamais vue sur ces écrans | #FB4C0D |
| Jetons | `--c-orange53`, `--c-orange53-txt`, `--c-orange-maparole-corps`, `--c-orange-maparole-cobalt`, Swift `aTenir` | retirés de `PROMI-TOKENS.json`, du bloc CSS et de `Promi+Design.swift` |
| Autres `--c-orange*` (#FE5000, #E1966E…) | teintes des palettes du Studio | intouchées (C-204) |
| `promi-moteur.js` | commentaires seulement (l. 6570–71) | intouché : le moteur est sacré |

Contrastes de #FB4C0D sur les fonds concernés : crème 3,01 · seiche 6,02 · barre brune 5,10 · Toile claire 2,14 · corps Promi 1,23 · Chiche 2,27 · Cercle 2,28.

⚠ Limite du relevé : les écrans passent par les 34 de `redteam_air`, pas par tous les états. La série de v173 cherchera chaque ancienne valeur en hexadécimal, en triplet et en `rgb()` (§8).

## 6 · Les documents et les juges

| Point | Ce qui sera fait |
|---|---|
| `CLAUDE.md` | §3 (trois états → deux), « trois arcs » → deux, R-015 → deux chiffres, règle de l'orange (D6), le §2 et les blocs datés restent pour l'histoire |
| `portage/` | occurrences à reprendre : SPEC-ECRANS 29, TEXTES.json 23, JETONS.json 36, SPEC-DONNEES 8, schema 7, REGLES 6, DETTE 5, SPEC-GESTE 5, JETONS.md 3, MANQUES 3, TESTS 2, TEXTES.md 1 |
| Juges | environ 45 portent « à tenir » ou #DD4D23 : remis au niveau un par un, originaux dans `sauvegardes/*-avant-v173.py` ; `redteam_maparole` perd ses deux variantes ; `redteam_decisions`, `redteam_couleurs_ref`, `redteam_tonsurton`, `redteam_contraste_trait`, `releve-S*` suivent |
| Juge neuf | `redteam_deux_etats.py` : aucune parole ni mot « à tenir » après une date passée (`?jour=+30`), date à l'encre, légende à la bonne hauteur lue sur l'image, plus aucun orange autre que #FB4C0D ; rouge sur v172 |

## 7 · Trouvé pendant l'étude, non touché

- Sur le Peaufiner d'un Cercle, toucher un trait payant (le mur de 60 pt de large) écrase la phrase sur une colonne d'un mot par ligne, qui déborde du rail. v172 ne touche pas aux murs, mais ce cas n'a pas été rejoué sur v171 (Q593).

## 8 · Ce que v173 ne touchera pas

Le moteur, les palettes du Studio, la Pelote, les couleurs de la grille C-204, Q584, le « À » et le « ! » de PromiLate, les invitations, Q592.
