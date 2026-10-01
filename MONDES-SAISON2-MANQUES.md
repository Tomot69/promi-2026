# Mondes saison 2 — ce qui manque avant intégration (27 sept. 2026)

Relu : `VRAIS-MONDES-SPEC.md`, le dossier « Promi — vrais nouveaux mondes graphiques (1) », CONTRAT-MONDE.md.
Le code des sept mondes n'existe QUE dans `Promi - Trois matières.dc.html` (classe `Component`). Les `.js` du dossier
sont les quatre mondes de v32 (identiques à `promi-mondes.js` à la racine) ; `DECISIONS-MONDES.md` et
`INTEGRATION-MONDES.md` datent du 23 sept.

## Les trois éliminatoires

1. **Aucune image** — TENU. Ni drawImage, ni get/putImageData, ni createPattern, ni toDataURL dans les sept fonctions.
   (Ramage efface par `destination-out` dans sa dalle seule : c'est un tracé, pas une image.)
2. **Aucune couleur en dur** — NON TENU. Dans les fonctions : deux mélanges vers `'#FFFFFF'` (croissant de Ramage 30 %,
   cœur de fleur de Volubilis seule 72 %) et un `'#000'` de masque. Surtout, TOUTES les couleurs viennent de l'objet `T`
   de la planche : 9 hexadécimaux en dur par mode (`bg`, 4 `mat`, `ink` sombre `#E6DDCB`) et 3 palettes qui ne sont pas
   celles du produit (leur « Chafouin » et leur « Primesautier » ≠ ceux de l'app ; « Rogue » n'existe pas).
3. **Longueurs en fraction de u** — NON TENU. Tout est en fraction de W (W/40, W/86, W/22, W/19–23, W/21, W/20–23,
   W·0,055…), Chamade et Guingois renormalisent sur la largeur de la planche (`k = W/300`), et des littéraux absolus :
   Chantourné `y += 1`, `±2`, `+0,35` · Mascaret `du = 3`, `±6`, `/1,2`, `0,6`, `rd > 0,3`, `U − 2` ·
   Volubilis grille `cs = 1,5` · Chamade `x += 5`, `−4`, `lw ≥ 1,2`, boîte `±2`.

## Point par point contre le contrat

| point | état | ce qui manque |
|---|---|---|
| signature | ✗ | `monde(g, S, T, only, mesure)` au lieu de `R(now, x0, y0, x1, y1)` / fabrique. `S.pr` porte `R` (rayon de place) et `ci2` : aucun équivalent dans le moteur. |
| unité u | ✗ | `S.u = √(W·H/(n+m))` avec `m = max(3, 3+0,3n)` points de matière — le semis `_NEUFS` n'en a pas. Quel u ? (`uMat` ? `avg()` ? la formule de la planche ?) |
| LCG sur clé stable | ~ | générateur mulberry32 (`rng`), pas le LCG. Le garder = fidèle à la planche ; passer au LCG = tous les tirages changent. Deux tirages viennent de la POSITION, pas de la clé : l'asymétrie d'arête de Guingois (`x·7,13 + y·3,71`), les épines et la coupe des traits de Mascaret (`Math.round(s0)`, `bm`). |
| cOf | ✗ | jamais appelé : `T.cols[p.ci]` en direct. |
| curPAL() | ✗ | jamais appelé : `T.cols` = les 3 tons les plus clairs triés par luminance, `T.ink` = le plus sombre. Ingénu (défaut) n'a aucun ton sombre. |
| rampe TH | ✗ | aucune déclarée ; la planche a 4 tons de matière en dur par mode (TH en veut 5, et en clair GLIGHT est commun). La matière n'a pas de graine sur laquelle appeler `cOf`. |
| fondToile() | ✗ | `T.bg` en dur. Quatre mondes peignent eux-mêmes le fond (Mascaret, Chamade, Volubilis, Guingois) et quatre « découpent » en peignant la couleur du papier (Ramage, Mascaret, Chamade, Volubilis) — sur le dégradé de l'accueil, ça fait des aplats. |
| Toile.cle() | ✓ | `S.g` s'y branche directement ; `p.h` sur `_dalleDeCle`. |
| déterminisme | ~ | pur au repos ; `now` jamais lu (aucun frémissement). |
| budget | ✗ | tableau ci-dessous. |
| seule() | ~ | le mode `only` existe. Mais Volubilis seule ≠ sur la Toile (cœur à 72 % de blanc au lieu du papier) ; Ramage : les plumes de matière recouvrent en partie celles de l'œil sur la Toile, pas seule — à vérifier. |
| contour() | ✗ | absent (seulement la boîte `mesure`). |
| toucher() | ✗ | absent — et indispensable : Volubilis déplace ses fleurs (couronne du haut, coins), Chamade écarte et recale ses cœurs ; le contour peint n'est pas à la place de la promesse. |
| nature() | ✗ | absent. |
| arrivée / départ | ✗ | rien : ni `now`, ni `env.trans`, ni `transDur`. Les constructions sont globales (tout le jardin, la relaxation de tous les cœurs, tous les plis) : une plantation recompose tout d'un coup. |

## Dalles vides — mesuré (3 Toiles × 2 thèmes)

Mascaret : 2 promesses sur 120 sans dalle à 40 · Guingois : 14 sur 120 à 40. Promesse invisible, rien à toucher, pas de
dalle seule. Les cinq autres : 0.

## Coût — mesuré dans la planche (300 × 650 × 3, 10 canevas, dessin forcé) — contrat : ≤ 16,7 ms

```
peint seul, Chromium · WebKit (ms)   3 promesses    20            40
Ramage                              203 · 149     327 · 268     470 · 409
Chantourné                           28 ·  25     114 ·  98     201 · 191
Brouillamini                          9 ·   7      19 ·  30      38 ·  61
Mascaret                             25 ·  20     153 · 111     489 · 349
Volubilis                            12 ·   7      15 ·   9      16 ·  11   + construction 500–900 par plantation
Chamade                              18 ·  21      36 ·  41      54 ·  75   (un clip() par cœur — piège WebKit §8)
Guingois                             86 ·  37     119 ·  60     178 ·  86   + construction ≈ 90–180
```

## Questions de produit, non couvertes

- Les Nuées (`kind:'nuee'`) : la planche n'en a pas. Par défaut, précédent v32 : une Nuée = une promesse.
- Toile sans promesse et aperçus du Studio (cellules colorées sans parole) : que montrer ? Brouillamini à 0 promesse = 2,9 % de pixels hors papier.
- Gratuit ou Cercle, pour chacun.
- Descriptions du Studio : reprendre les textes de la planche ?
- La spec renomme Braille en « Comptine » (v33 : Braille gardait son nom) et ne cite pas Halin (ex-Cabochon).
- La classe définit `coeurs` deux fois (l. 1054 et 2398) : la seconde gagne — c'est bien celle de la spec ?
