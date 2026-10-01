# Intégration — Esquille · Bobinette · Ritournelle · Madrure

Fichier à intégrer : **`promi-mondes.js`**. Tout le reste (`mondes-origine*.js`, `mondes-avant.js`, `mondes-pdf.js`, les pages `.dc.html`) sert au banc et ne s'intègre pas.

## Les trois points bloquants — vérifiés sur le fichier

| Point | État | Vérification |
|---|---|---|
| Aucune image | ✓ | zéro occurrence de getImageData, putImageData, drawImage, createPattern, toDataURL, createImageData, OffscreenCanvas, createElement dans le code (hors commentaires) |
| Aucune couleur en dur | ✓ | zéro littéral de couleur (#…, rgb(…)). Toute couleur vient de `cOf`, `curPAL` ou `rampe` ; les seules constantes sont des **nuances** d'une couleur reçue (mélange vers le clair ou le sombre) |
| Longueurs en fraction de u | ✓ | la dernière longueur en px (recouvrement de raccord de Bobinette, 0,5 px) est passée à 0,05 × l'épaisseur du fil. Restent des **nombres sans unité** : angles, pondérations, nombre d'anneaux, et un plafond de 260 000 nœuds de grille pour Madrure (garde-fou, pas une longueur) |

## Coût — méthode demandée

Toile 390×844, DPR 2, champ d'origine (91 graines), **dix canevas distincts, une relecture chacun**, médiane. Canevas accéléré. Témoin : canevas neuf + un aplat + relecture = **2,2 ms**.

| Monde | Total, relecture comprise | Dont appels de dessin | Tient 16,7 ms ? |
|---|---|---|---|
| Esquille | 15,8 ms | 2,5 ms | oui, de justesse |
| Bobinette | 35,5 ms | 9,3 ms | non |
| Ritournelle | 25,1 ms | 6,6 ms | non |
| Madrure — image en cache | 40,4 ms | 0,1 ms | non |
| Madrure — construction (plantation) | 136,9 ms (max 291,7) | — | une fois par plantation |

Les quatre sont en dessous de Gravure (55 ms) et de Touffe (90 ms).

**Ce que ces chiffres ne disent pas.** Sur des canevas distincts, le processeur graphique découpe chaque chemin pour la première fois : c'est ce qui pèse, pas le calcul (colonne « appels »). Sur **le même** canevas redessiné, comme la Toile à chaque image, les mêmes mondes mesuraient : Esquille 1,0 · Bobinette 5,5 · Ritournelle 6,4 · Madrure en cache 1,4 ms. La vérité de l'app est entre les deux ; seul son banc la donne.

## Ce que chaque monde attend du moteur

**Commun aux quatre**
- `seeds[]` : `x`, `y`, `w` (poids additif), `px`/`py` facultatifs (position frémissante) ; `pid` ou `nuee` pour une promesse, rien pour la matière.
- `cOf(s, now)` → `[r, g, b]` ; `_dalleDeCle(pid)` → entier stable ; le rectangle visible `(x0, y0, x1, y1)`.

**Esquille** — LIBRE. La cassure partage le semis ; un fragment = une cellule, mais sa forme n'est pas la cellule du moteur. Ne demande rien d'autre que `cOf`.

**Bobinette** — LIBRE, trame ancrée dans le monde. Les arcs traversent les frontières ; chaque arc prend la couleur de la cellule sous son milieu. Deuxième ton près d'une frontière : `rampe(s)[1..3]`, sinon la palette.

**Ritournelle** — CONTENUE. Une coulée par cellule, rognée par sa cellule. Quatre tons : `rampe(s)` du §10, sinon `curPAL()` tourné pour que l'anneau extérieur porte la couleur de la cellule.

**Madrure** — LIBRE. Exception écrite au §4.1 : ses trois tons viennent de `curPAL()` (0 filet, 1 veine, 2 veine claire). Angle de l'onde : `cleToile`. **Cache** : la géométrie est gardée d'une image à l'autre et tombe à tout changement de semis (position de repos, poids, clé), de `cleToile`, ou quand la vue sort de la zone calculée (vue + 12 %). Les couleurs ne sont jamais gardées : palette et thème s'appliquent à l'image suivante sans reconstruction. `Rmad.invalider()` force la reconstruction.

## Madrure sur un appareil quatre fois plus lent

La construction mesure 91 ms de calcul sur le même canevas et 137 ms (max 292) sur canevas neuf. Sur un appareil ×4 : **environ 360 à 550 ms**, jusqu'à ~1,2 s dans le pire cas. C'est un gel visible au moment où l'utilisateur vient de planter. Deux remèdes, non faits :
1. **Construire par tranches sur plusieurs images**, en continuant d'afficher l'ancienne onde : la nouvelle apparaît après un temps équivalent, sans gel.
2. **Construire la géométrie hors du fil principal** : le calcul est purement numérique (grille, lignes de niveau, lissage) et rend des tableaux de nombres ; seul le passage en chemins reste sur le fil principal (~20 % du coût).

Le 1 est le plus simple ; le 2 enlève le gel entièrement.

## Dalle seule et toucher — mondes LIBRES (Esquille, Bobinette, Madrure)

Trois fonctions exposées par la fabrique :

| Fonction | Rôle |
|---|---|
| `seule(nom, s, now, cx, cy, taille)` | peint la dalle de la graine `s` seule, sur rien, centrée en (cx, cy), `taille` = son plus grand côté |
| `contour(nom, s)` | le contour réellement peint, `[[x, y], …]` en coordonnées Toile |
| `nature(nom, s)` | Madrure : `'oeil'`, `'fermee'` (strate fermée) ou `null` (pas de dalle seule) |
| `toucher(nom, x, y)` | la graine dont la dalle PEINTE contient le point, ou `null` — le moteur retombe alors sur `cAt` |

**Principe.** La matière d'un monde libre naît de toute la Toile : on la calcule sur toute la Toile dans un contexte muet (rien n'est peint), on note ce qui appartient à chaque promesse, puis on ne peint que cela, en vecteurs, à la taille demandée. La dalle seule est donc géométriquement celle de la Toile : même grain, mêmes tons, déterministe. Aucun rognage d'image, aucun cadre.

- **Esquille** — le fragment de la promesse, tel quel.
- **Bobinette** — ses arcs épaissis (la bobine) et ses boucles de fil. Toucher : les disques de la bobine et des boucles.
- **Madrure** — l'**œil** du nœud, tel qu'il paraît sur la Toile : la plus grande ligne de niveau fermée qui n'entoure que ce nœud et qui est le bord extérieur d'un de ses filets. Dedans, la matière exacte de la Toile (mêmes lignes, mêmes tons), découpée par la même courbe que le filet : la dalle finit sur son liseré, sans trait parasite. Calculée sur la zone du nœud seule (1,6 u ; grille ancrée, donc mêmes lignes que la Toile). La bande de fond de l'œil demande au moteur sa couleur : `fondToile()` (sinon elle reste transparente). **Un nœud dont les lignes ne se referment pas sur lui n'a pas d'œil : `seule()` rend `false`** — environ 30 promesses sur 55 ont un œil, sur trois semis.

**Carnet** (calculé une fois par semis, palette, thème et couleurs des cellules) : Esquille ~1 ms · Bobinette 12 ms · Madrure : 12–15 ms par dalle, la première fois (zone du nœud), puis gardée. Ensuite, par appel : `seule` à 40 px — Esquille 0,14 ms · Bobinette 0,23 ms ; `toucher` < 0,04 ms. Vingt dalles de Madrure dans l'Index : ~280 ms au premier affichage, puis rien.

**Toile de Madrure.** Les yeux des nœuds sont maintenant échantillonnés à 64 points au moins, et chaque point est reposé sur la ligne de niveau exacte après lissage : plus de bosse sur les petites boucles. Construction à la plantation : 174 ms à la méthode (dix canevas, une relecture).

**Corrigé au passage.** La cassure d'Esquille ne portait que sur les graines visibles : déplacer la vue recassait la plaque. Elle porte maintenant sur tout le semis. Deux restes du banc (`kind === 'gray'`) remplacés par la règle promesse/matière.

## En suspens

1. **Les cellules du moteur ondulent-elles ?** Le prototype ondulait ; Ritournelle y doit une partie de ses espaces entre les flaques.
2. **`curPAL()`** existe-t-il, et sous quel format ? Le fichier accepte des chaînes « #rrggbb » ou des `[r, g, b]`.
3. **La rampe du §10.** Sans elle, Ritournelle et Bobinette tournent la palette à partir de la couleur de la cellule — c'est l'aspect validé, mais c'est une hypothèse sur l'ordre.
4. **`cleToile`.** Sans elle, l'angle de Madrure est fixe (0,6 rad) : toutes les Toiles ont la même direction d'onde.
5. **Promesse ou matière** : le fichier suppose `pid` ou `nuee` ⇒ promesse. À confirmer.
6. **Dalle seule et toucher** : faits (voir plus haut). Reste au moteur de brancher `dalleTrame` sur `seule()` et son test de toucher sur `toucher()`.
7. **Madrure, trois natures de dalle seule** — `nature('madrure', s)` rend `'oeil'`, `'fermee'` ou `'cercle'` ; **aucune promesse n'est sans dalle** (trois semis de 55 : œil 27–36 · strate fermée 16–19 · cercle 3–9 · vide 0).
   - **œil** : la plus grande ligne fermée qui n'entoure que ce nœud, bord extérieur d'un filet ; matière exacte de la Toile.
   - **strate fermée** : la strate la plus lointaine qui enveloppe le nœud sur au moins `SEUIL_STRATE` = 70 % de son tour, fermée par une courbe douce (Hermite sur le rayon) ; le **liseré est prolongé** le long de la fermeture, à l'épaisseur du filet mesurée aux deux bords. Peut enjamber un nœud sans œil, jamais un œil.
   - **cercle** (dernier recours, jamais pour un nœud qui a un œil) : le bombement du nœud dans la **courbure réelle du champ** — ψ = φ moins la seule pente des autres nœuds (leur gradient au nœud). Les anneaux de ψ se déforment comme le bois (rapport rayon max/min 1,1 à 1,85 sur trois semis), mêmes tons et filets, arrêtés sur le filet le plus lointain qui se ferme sous 0,5 u. Ce ne sont pas des lignes de la Toile, mais on ne les distingue plus d'un œil à l'œil nu.
8. **`fondToile()`** à exposer : la couleur du fond de la Toile, pour la bande blanche des yeux.
8. **Madrure ne frémit pas** pendant la seconde de plantation (le cache suit la position de repos). L'animer coûterait une reconstruction par image pendant cette seconde.
9. `SP_U = 1,2` : le rapport entre l'écart moyen des prototypes et u. Si le moteur définit u autrement, ce seul nombre suffit à recaler les quatre mondes.
