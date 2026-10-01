# Promi — Spécification des mondes (saison 2)

Source de référence : `Promi - Trois matières.dc.html`, la planche validée et téléchargée. **Le code de cette planche fait foi.** Ce document explique ce que chaque fonction doit produire et pourquoi, pour que Claude Code puisse le porter à l'identique dans le moteur. Au moindre doute, rejouer la fonction citée et comparer pixel à pixel.

---

## 0. Contrat commun (tous les mondes)

**Entrées.** Chaque monde est une méthode `monde(g, S, T, only, mesure)`.
- `g` : contexte 2D, en unités logiques. La Toile iPhone fait `W × H` (≈ 300 × 650).
- `S.pr` : les promesses. Chacune a une position `x, y`, un rayon de place `R`, deux indices de couleur `ci` et `ci2`, et un hachage stable `h`.
  - `S.g` est la graine de la Toile et `S.u` l'unité de place.
- `T` : le thème.
  - `T.cols[i]` : les couleurs de la palette.
  - `T.ink` : l'encre.
  - `T.bg` : le papier.
  - `T.mat[]` : les tons du fond, seulement pour les mondes qui en ont.
- `only = p` : dessiner seulement la **dalle seule** de la promesse `p`, sur rien.
- `mesure = [x0, y0, x1, y1]` : ne rien dessiner, seulement étendre la boîte de ce que la dalle `p` peindrait. C'est avec cette boîte qu'on cadre la dalle seule.

**Règles absolues.**
1. **Rien ne se chevauche, rien ne se touche**, sauf les attaches voulues : une feuille sur sa tige, une tige greffée sur une autre. Un joint régulier sépare toujours deux formes.
2. **Chaque promesse est une dalle identifiable** : une forme à elle, qu'on distingue de ses voisines d'un coup d'œil.
3. **Dalle seule.** Elle se dessine pour elle-même, avec sa silhouette propre, sur rien. Ce n'est jamais un morceau de Toile détouré, jamais un carré, jamais une image.
4. **Déterminisme.** Tout aléa passe par `this.rng(seed)` : `S.g` pour ce qui est commun à la Toile, `p.h` pour ce qui est propre à une promesse. La dalle d'une promesse a le même aspect sur la Toile et seule.
5. **Croissance organique.** Planter une promesse ajoute une cellule au semis. Les voisines se réorganisent et la matière se recompose. On ne dézoome jamais, et on ne colorie pas des cases qui attendaient.
6. **Aplats francs.** Pas de dégradé, pas d'ombre portée, pas de transparence molle. Toute « ombre » naît du seul rapprochement des traits.
7. **Aucune ligne cassée.** Toute courbe est lissée (Chaikin, moyenne glissante ou Bézier) et échantillonnée finement : pas de coude visible.
8. **Pas d'espace vide** pour les mondes « pleins » (Volubilis). Pour les mondes « à fond », le papier ou les bandes sont la matière.

---

## I · Ramage — fonction `parure`
- **Principe.** Un plumage couvre toute la Toile, plume sur plume. Autour de chaque promesse, les plumes s'ouvrent, grandissent et se colorent : c'est l'**œil**.
- **Dalle.** L'œil, fait des plumes qui l'entourent. Son bord est leur festonnage.
- **Matière.** Le plumage, dans le ton du papier.
- **Détails validés :**
  - de fines barbes fendues de part et d'autre de la tige, sur les grandes plumes ;
  - un croissant plus clair à la pointe des plumes colorées de l'œil ;
  - le centre de l'œil est toujours plein : un fond d'encre sous la touffe centrale, qui suit la pointe des feuilles et n'est jamais un cercle.
- **Référence :** `parure()` et ses auxiliaires dans le fichier.

## II · Chantourné — fonction `chine`
- **Principe.** La soie chinée lyonnaise, parente de l'ikat. Les fils de chaîne sont teints avant le tissage, par écheveaux.
- **Dalle.** Un médaillon au bord frangé fil à fil.
- **Matière.** Les fils teints en flammes libres.
- **À ne pas faire :** trame croisée, fils alternés plus sombres. Ils avaient été essayés puis rejetés ; c'est la version 1 qui est retenue.
- **Référence :** `chine()`.

## III · Brouillamini — fonction `decoupe`
- **Principe.** La gouache découpée, à la manière du dernier atelier de Matisse. Chaque promesse est une forme taillée d'un seul geste.
- **Dalle.** La découpe entière, lobée, ou parfois un cœur. Elle a souvent une chute d'une autre couleur, taillée à part.
- **Détail validé :** les formes à cinq lobes et plus (étoiles, fleurs) ont des échancrures nettement tirées vers l'intérieur. Elles ne doivent pas ressembler aux formes rondes, en nuage.
- **Référence :** `decoupe()`.

---

## IV · Mascaret — fonction `plisse` (variantes retenues : `vr = 'DEF'`)
- **Principe.** Une affiche d'op art. Des bandes d'encre fines, d'épaisseur constante, traversent la page. Chaque promesse est une lame qui soulève la page à sa place, et toutes les bandes suivent.
- **Bandes.**
  - L'orientation est tirée par Toile : verticale une fois sur 0,4, horizontale sinon.
  - Période `per = W / (19…23)`. Chaque bande occupe `[j·per, (j + 0,5)·per]`.
- **Champ de lame `D(u, v)`.** Pour chaque promesse, `su = max(1,6·per, R·(0,8…1,3))`, `sv = max(2,2·per, R·(0,9…1,5))` et `A = ±per·(1,1…2,2)`. La forme dépend du type de lame :
  - bosse : `A · e^(−du²) · e^(−dv²)` ;
  - vague : `A · sin(2,2·du) · e^(−0,5·du²) · e^(−dv²)` ;
  - cascade : `A · ½(1 + tanh(1,8·du)) · e^(−dv²)`.
  Chaque bord de bande est déplacé de `D(u, bord)`.
- **Dalle : les traits de couleur.**
  - Chaque point de bande appartient au pli de poids `w = exp(−(du/(su·0,8))² − (dv/(sv·0,7))²)` le plus fort, et seulement si `w > 0,45`. Deux dalles ne se chevauchent jamais, et des bandes d'encre les séparent.
  - Chaque tronçon devient une capsule qui remplit **toute l'épaisseur** de la bande, avec des bouts ronds.
  - Un tronçon long (plus de `5·per`) est coupé en deux une fois sur trois.
  - Un tronçon plus court que `1,1·per` est ignoré.
- **D · Épines.** Juste après chaque bout de trait, deux fines épines de papier entament la bande d'encre, une depuis chaque bord.
  - Il y a trois tailles seulement (petite, moyenne, grande), décalage `(0,09…0,17)·per`.
  - Parfois une seule épine.
- **E · Point de ponctuation.**
  - Un point de couleur, de rayon `0,42 × épaisseur`, placé à `0,75·per` après le **dernier** trait du tronçon.
  - Il n'est dessiné que s'il tient **entier** sur l'encre, sans toucher le trait suivant ni le bord. Il fait partie de la dalle, et apparaît aussi dans la dalle seule.
- **F · Bande dédoublée.**
  - Un filet de papier au milieu de la bande, épaisseur `0,12·per`, sur **une bande sur trois** seulement.
  - Seulement là où `|D| > 0,85·per`, et jamais près d'un trait de couleur (poids > 0,2).
- **Rejetés :** épaisseur en relief, repérage décalé, second ton.

## V · Volubilis — fonctions `volBuild`, `volFeuilles`, `jardin`
- **Principe.** Un jardin découpé, tenu dans son cadre, d'après la référence en papier découpé noir fournie en cours de conception.
- **Dalle.** La fleur. **Matière :** les feuilles noires et les tiges.
- **Fleurs.**
  - Une par promesse. On les écarte d'abord (relaxation). La fleur la plus haute monte près du bord supérieur. Les coins du haut, et le centre s'il y a au moins cinq fleurs, sont toujours tenus par une fleur.
  - Chaque fleur prend sa place entre ses voisines et le cadre : cellule de puissance, joint `gut`.
  - Sa forme est l'**union de 4 à 6 disques-pétales** autour d'un petit cœur : cœur `0,34…0,40·R`, centres des pétales à `0,55…0,62·R`, rayons `0,36…0,46·R`. Un pétale pointe vers la plus grande place libre au-dessus.
  - L'union est mise à l'échelle au 25ᵉ centile du rapport place / pétales, puis aplatie contre la place par un minimum adouci (`kS = 0,08·R`).
  - Jusqu'à trois pétales en plus peuvent pousser, dans l'axe d'un pétale existant, vers le haut ou les côtés, et vers le bas aussi au-delà de 12 fleurs.
  - Le cœur est une grappe de 3 à 7 pois de tailles libres.
- **Tiges.**
  - De longues courbes en S qui descendent de chaque fleur et contournent les autres fleurs, selon leur vrai contour (`volR`).
  - Elles se greffent au point exact de rencontre : jamais de croisement en X.
  - Lissées puis ré-échantillonnées. Elles sont plus épaisses en bas, et leur épaisseur respire légèrement le long du trait.
  - Les branches sans fleur partent d'une tige, tangentes à celle-ci (`volTan`).
- **Feuilles.**
  - Chaque feuille est attachée à une tige, **jamais flottante**.
  - Elle remplit sa place, bornée par ses voisines, puis sa forme est lissée par une série de Fourier limitée à la 2ᵉ harmonique : des ovales simples.
  - Elle est centrée sur sa place, puis ramenée contre sa tige **sans sortir de sa place**.
  - Elle se termine par un col court et doux vers la tige.
  - L'espacement le long des tiges suit la densité : `0,15·W` avec peu de fleurs, jusqu'à `0,06·W` avec beaucoup.
- **Couverture.** Une passe finale comble chaque vide avec une feuille portée par une petite tige secondaire lisse. Au plus deux fleurs d'encre non-dalles, avec leur tige, peuvent remplir un dernier grand vide.

## VI · Chamade — fonction `coeurs`
- **Principe.** Une page rayée à la main, au feutre.
- **Fond.**
  - Des bandes d'encre presque horizontales, période `W / 21`, épaisseur `0,42…0,58·per`, bords tremblés (fonction `feutre`).
  - Toutes les bandes suivent une grande onde commune : trois sinus dont l'amplitude est modulée par zone, et trois remous locaux.
  - C'est la version validée : ne pas changer l'orientation ni le nombre de vagues.
- **Dalle : le cœur.**
  - Une forme de cœur paramétrique dont les réglages varient par promesse : largeur, hauteur, lobes gauche et droit, pointe, inclinaison `±0,55`, part d'ovale (« dodu »), léger tremblé.
  - Le cœur est ramené dans la page. Les cœurs s'écartent d'abord les uns des autres, rétrécissent ensuite avec un plancher de lisibilité, et **ne se touchent jamais**.
  - Il est cerné d'un trait d'encre. Il n'y a **pas de liseré** : les bandes du fond touchent le trait.
- **Remplissage du cœur, par promesse :**
  - rayures en chevrons courbes, qui épousent la pointe ;
  - rayures en biais ;
  - **coulée**, dans 45 % des cas : des anneaux versés au centre, de moins en moins cœur vers l'intérieur (mélange forme du cœur / flaque molle), bords ondulés. Les couleurs se succèdent : `[ci, ci2, encre, ci, ci2]`, et la couche extérieure n'est **jamais** à l'encre.
- **Rejeté :** les anneaux concentriques qui suivent le contour du cœur.

## VII · Guingois — fonctions `froisseBuild`, `froisse`
- **Principe.** Un quadrillage tracé à main levée sur une étoffe pliée, d'après la référence en quadrillage déformé fournie en cours de conception.
- **Grille.**
  - Pas `c = W / (20…23)`, trait `0,11·c` d'épaisseur **constante**. L'ombre naît du seul rapprochement des lignes.
  - Chaque ligne tremble légèrement, pour un tracé à main levée.
  - Échantillonnage fin (`c / 9`), pour qu'aucune ligne ne soit cassée.
- **Déformation `warp(x, y)`, la clé du rendu.** On additionne :
  1. une ondulation de fond douce ;
  2. **une ou deux zones froissées** par Toile. Le relief y est concentré ; ailleurs l'étoffe reste calme ;
  3. des bosses et des creux **en plateau**, `e = exp(−q²)`, allongés et orientés, sur trois échelles : deux grandes houles n'importe où, puis des moyennes et des petites **dans les zones**. Les lignes se serrent sur leur pourtour : c'est l'ombre au contour ;
  4. des **arêtes** : une par promesse, plus deux ou trois cassures de fond placées dans les zones.
     - Ce sont des profils gaussiens, **jamais pointus**, asymétriques.
     - L'étoffe est tirée vers l'arête et glisse un peu le long de celle-ci.
     - Le pli d'une promesse est plus fort quand il tombe dans une zone.
  5. **Garde-fou anti-repli.** En chaque point, la somme des resserrements est plafonnée à 0,86. La grille ne se croise jamais, et chaque case garde ses quatre côtés.
- **Dalle.**
  - Les cases dont le centre **déformé** est au cœur du pli d'une promesse : poids > 0,42, avec une avance d'au moins 0,15 sur le poids suivant.
  - Toute case voisine d'une autre dalle, même par un coin, reste blanche. Les cases isolées sont retirées.
  - La dalle est d'une seule couleur (`ci`).
  - Dalle seule : ses cases teintes, avec leur seul quadrillage.

---

## Noms (validés)
- **Nouveaux mondes :** Ramage, Chantourné, Brouillamini, Mascaret, Volubilis, Chamade, Guingois.
- **Mondes précédents :** Esquille, Bobinette, Madrure, Ritournelle.
- **Mondes existants renommés :** Pochade (Encre), Tesselle (Mosaïque), Touffe, Comptine (Braille), Buvard (Pixel), Houle (Sillons), Éclisse (Terrazzo), Taille-douce (Gravure).
