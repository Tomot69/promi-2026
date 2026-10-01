# Décisions — mondes de la Toile (23 sept. 2026)

## Le modèle de la Toile (ce qui doit être vrai de tout monde)

Une Toile **naît vide** et **vit du semis**. Chaque promesse plantée ajoute une dalle : la matière
réagit autour d'elle, se réorganise, se stabilise. Deux personnes n'ont jamais la même Toile —
elles n'ont pas planté les mêmes promesses dans le même ordre.

Conséquences pour un monde :

1. **La matière naît des promesses réellement plantées.** Aucun décor global figé qu'on colorie,
   aucun réseau décidé une fois pour toutes et identique pour tout le monde.
2. **Ce qui doit être stable, c'est la dalle d'une promesse donnée** — son aspect ne change pas
   d'un rendu à l'autre. Ce qui bouge, c'est la composition autour, quand la Toile grandit.
   Le déterminisme porte donc sur la CELLULE (clé stable : titre + personne), jamais sur l'image entière.
3. **Une dalle qui paraît ailleurs — fiche, Index, Fil, Pelote — est engendrée seule par le moteur.**
   Ce qu'on voit alors : **une forme irrégulière, la sienne, posée sur rien**. Pas de voisines, pas
   de fond, pas de cadre, pas de carré — sa silhouette découpée, avec sa matière dedans. Comme un
   éclat de verre posé sur une table : on voit ses bords, et la table autour.
   **Un carré contenant plusieurs fragments n'est pas une dalle.** Jamais un morceau de Toile,
   jamais une capture rognée, jamais un cadre posé sur un rendu, jamais une image redimensionnée.
   Interdit absolu du produit, vérifié par contrôle automatique.
   *Test :* demander le rendu d'une seule promesse. Un carré = raté. Une forme = bon.
   *Côté monde :* le monde peint ses fragments normalement ; pour une dalle seule, seul le fragment
   de la promesse demandée est peint (le masque du moteur y suffit pour un monde contenu), sur un
   canevas laissé transparent.

## Comment une Toile se remplit

Le **semis grandit avec les promesses**. Une Toile à six promesses a **six cellules** (plus un peu
de matière), pas quarante dont trente-quatre seraient vides. Il n'y a ni fragments en attente qui se
colorieraient un à un, ni image définie qu'on dézoomerait progressivement.

- à six : six grandes formes franches qui occupent presque tout l'écran, quelques fragments de
  matière entre elles ;
- à quarante : quarante formes plus petites, la matière presque disparue — la Toile s'est densifiée
  parce qu'elle contient plus de choses ;
- entre les deux : planter une promesse **ajoute une cellule au semis** ; les voisines s'écartent,
  se reproportionnent, se stabilisent, et la nouvelle a pris sa place.

Ordre de grandeur retenu pour la matière : `nMatière ≈ 2 + 0,15 · nPromesses` — quelques fragments
à vide, une part qui s'efface quand la Toile se remplit.

## La matière (les fragments sans promesse)

Une cellule sans promesse porte **une variation de la couleur du mode** : des nuances de crème en
mode clair, des nuances sombres en mode sombre. **Jamais une couleur de la palette, jamais un gris
plaqué.** C'est ce qui rend belle une Toile peu remplie — c'est ainsi dans les huit mondes existants
(voir Encre et Mosaïque), et c'est aux nouveaux mondes de s'aligner.

Côté moteur c'est déjà le chemin 1 de `cOf` : une cellule vide rend son gris modulé sur la rampe du
monde (`TH[monde].g` en sombre, `GLIGHT` en clair). **Donc un monde n'a rien à inventer : il appelle
`cOf` pour la matière comme pour une dalle.** Il faut en revanche déclarer la rampe du monde dans
`TH` (§12 du contrat) — pour Esquille : une rampe sombre proche de celle d'Encre.

## Esquille — la plaque se casse autour des promesses

**Une dalle est UN fragment**, et la Toile n'est QUE des fragments : un par cellule du semis.
Aucune plaque préalable qu'on colorie ensuite.

Chaque cassure **sépare le semis en deux groupes** (coupe perpendiculaire à l'axe d'étalement du
groupe, déviée d'un angle tiré des clés du groupe), et on recommence jusqu'à ce que chaque fragment
ne contienne plus qu'une cellule. Les cassures sont donc **longues et partagées** — c'est ce qui
fait la plaque brisée, qu'un pavage de Voronoï ne donne pas.

**Peu de fragments, et gros.** Une plaque brisée, ce n'est pas du verre pilé : sur une Toile de
vingt promesses on voit vingt formes franches, pas trois cents échardes. Le nombre de fragments est
exactement le nombre de cellules du semis — rien ne se subdivise en plus.

Une promesse **pèse beaucoup plus lourd** que la matière dans le choix des coupes : poids
`1 + (7 − 5·sat)`, soit **8× sur une Toile vide et 2× à saturation** (`sat` = part des cellules qui
portent une promesse). Son fragment est donc franchement plus gros au début, et rejoint la taille
commune quand la Toile se remplit. C'est ce poids, et lui seul, qui rend les dalles repérables d'un
coup d'œil — aucun contour, aucun cadre n'est dessiné.

Planter une promesse **ne recasse que la branche où elle tombe** : les voisines s'écartent, se
reproportionnent, changent de forme, puis se stabilisent. Le reste de la plaque garde ses cassures.

La plaque part de la **boîte des graines**, jamais du canevas : la même dalle se casse pareil,
engendrée seule ou dans la Toile. La fêlure est un retrait à **largeur constante** (chaque arête
reculée de 0,022 u), donc les angles restent vifs.

## Madrure — exception écrite au §4.1 (révisée : trois tons sur trois)

> Révision du 23 sept. : retour au code d'origine. La dalle de Madrure est le **nœud** — le bombement qu'une promesse crée dans le champ —, pas une région colorée. L'onde n'est donc pas teintée par `cOf` : filet = palette[0], veine = palette[1], veine claire = palette[2]. La version « deux tons sur trois » ci-dessous découpait l'onde par cellules : c'est exactement ce que la matière refuse. Elle est abandonnée.

### Ancienne rédaction (abandonnée)

**Madrure prend deux de ses trois tons dans la palette**, et non dans `cOf` :

| rôle | source |
|---|---|
| le filet de contact (la lisière sombre de chaque couche) | `curPAL()[0]` |
| la veine claire | `curPAL()[2]` |
| la veine de base | `cOf(s, now)` — la couleur de la promesse |

Raison, constatée en comparant les trois rendus : forcée à `cOf` seul, sa matière meurt.
(1) La cellule redevient visible — la couleur change net à la frontière, on voit réapparaître des
plaques de couleur sous les veines, exactement la dalle-en-cadre que le produit refuse.
(2) Le filet, devenu « nuance sombre de la cellule », perd son trait : bordeaux, vert foncé, gris.
(3) La veine claire d'un rouge ou d'un vert donne du rose et du gris-vert délavés : la Toile pâlit.

Sa matière est **une onde teintée par la palette, que les promesses découpent sans la colorer**.
L'exception tombe d'elle-même le jour où `dalleTrame` publie la rampe du §10 : Madrure devient
alors conforme sans changer une ligne, et Ritournelle en profite.
