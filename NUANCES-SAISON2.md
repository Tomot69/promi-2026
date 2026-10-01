# Nuances de dessin — saison 2

Ce fichier recense ce qui ne se devine pas en lisant le code : pourquoi chaque réglage est là, ce qui a été refusé, et ce qui rendrait le monde faux si on le changeait.
À lire avec `MONDES-SPEC.md` (le mécanisme) et `PORTAGE-SAISON2.md` (les décisions). La planche `Promi - Trois matières.dc.html` fait foi pour l'aspect.

> **Limite honnête.** Les premières itérations de Ramage, Chantourné et Brouillamini ne sont plus dans ma mémoire de travail. Pour ces trois mondes, je n'écris que ce dont je suis sûr, et les lacunes sont signalées. Leur rendu validé est celui de la planche : il faut le comparer pixel à pixel, ne pas le réinterpréter.

---

## Règles transverses (valables pour les sept mondes)

- **Aucune ligne cassée.** Toute courbe est lissée et finement échantillonnée. L'œil repère un coude de quelques degrés, et c'est aussitôt « informatique », refusé.
- **Rien ne se touche**, sauf les attaches voulues. Le joint est régulier, fin, et le même partout.
- **Pas de motif répété à l'identique.** Une échelle de formes identiques, une rangée régulière ou un espacement constant ont chaque fois été refusés comme « cheap ». Il faut toujours faire varier taille, pas et angle.
- **Pas d'effet psychédélique ni de déformation gratuite.** Une forme déformée par un champ sans raison a toujours été refusée. La forme doit se lire comme un objet réel : un pli, une coulée, une fleur, une feuille.
- **L'ombre naît du dessin, jamais d'un aplat.** Serrer des lignes, oui. Épaissir un trait pour faire une tache, non.
- **La dalle se reconnaît d'un coup d'œil**, par sa couleur et sa forme. Elle n'est jamais noyée dans la matière.
- **La matière reste belle quand la Toile est vide.** C'est le premier écran vu.

---

## I · Ramage (plumage)

- **La matière.** Des plumes superposées couvrent toute la Toile, dans les tons du papier. Autour de chaque promesse, les plumes s'ouvrent et prennent la couleur de la promesse : c'est l'œil, la dalle.
- **Validé :** l'utilisateur l'a jugé « 99,99 % parfait ». Il faut le reprendre à l'identique, sans rien améliorer.
- **Détails fins, gardés :**
  - de fines barbes fendues de part et d'autre de la tige, seulement sur les grandes plumes ;
  - un croissant plus clair à la pointe des plumes colorées de l'œil.
- **Défaut corrigé, à ne pas réintroduire :** un point blanc apparaissait au centre de l'œil, entre les pointes des petites feuilles de la touffe centrale. On le comble par un fond d'encre qui suit la pointe des premières feuilles. Ce fond n'est jamais un cercle.
- **Lacune :** je n'ai plus les proportions exactes (taille des plumes, rayon de l'œil). Elles sont dans `parure()`.

## II · Chantourné (soie chinée)

- **La matière.** La soie chinée lyonnaise, parente de l'ikat : des fils de chaîne teints par écheveaux avant le tissage, en flammes libres. La dalle est un médaillon au bord frangé fil à fil.
- **Refusé :** une trame qui croise les fils, et des fils alternés plus sombres. Ces deux « détails fins » rendaient l'étoffe trop chargée et floue. L'utilisateur a exigé le retour à la **première version**.
- **Défaut corrigé :** un recadrage trop serré des dalles seules rendait les fils gros et flous. La dalle seule garde le cadrage d'origine.
- **Lacune :** les proportions (largeur des fils, forme des flammes) sont dans `chine()`.

## III · Brouillamini (gouache découpée)

- **La matière.** Des formes taillées d'un seul geste, à la manière du dernier atelier de Matisse. La dalle est la découpe entière : lobée, ou parfois un cœur. Elle a souvent une « chute » d'une autre couleur, taillée à part.
- **Nuance validée :** les formes à cinq lobes et plus (étoiles, fleurs) ont des échancrures nettement tirées vers l'intérieur et des branches marquées. Elles ne doivent pas ressembler aux formes à trois ou quatre lobes, plus rondes, en nuage.
- **Nom :** ce monde s'appelait Chantourné jusqu'à un renommage.
- **À corriger au portage :** à 0 promesse, la Toile est à 97 % de papier. Il faut une matière dense et belle : des découpes non-dalles dans les tons de la rampe.
- **Lacune :** les proportions de base sont dans `decoupe()`.

---

## IV · Mascaret (op art, bandes)

- **Référence :** des affiches d'op art et du Bauhaus, avec des bandes pleines déformées par une onde.
- **La matière.** Des bandes d'encre fines, d'**épaisseur constante**, traversent la page, horizontales ou verticales. Chaque promesse soulève les bandes à sa place, en bosse, en vague ou en cascade, et toutes les bandes suivent **sans jamais se croiser**.
- **La dalle.** Des traits de couleur posés dans les bandes :
  - un trait remplit **toute l'épaisseur** de sa bande, bouts parfaitement ronds ;
  - il est long au cœur de la lame et court sur ses bords ;
  - un trait long est parfois coupé en deux.
- **Ce qui fait tout le charme :** juste après chaque bout de trait, deux fines **épines de papier** entament la bande d'encre depuis ses deux bords. Elles sont nées d'un défaut de tracé, puis ont été gardées exprès. Trois tailles seulement : petite, moyenne, grande. Parfois une seule épine. Une variation plus forte a été refusée.
- **Points de ponctuation :** un point de couleur après le dernier trait d'un tronçon. Il fait partie de la dalle, **entier ou absent**, jamais coupé par une bande ou par le trait suivant.
- **Bande dédoublée :** un filet de papier au milieu d'une bande.
  - Il est **rare** : une bande sur trois, seulement là où la lame est haute.
  - Il ne s'approche jamais d'un trait ni d'une épine, sinon il forme des croix disgracieuses.
- **Refusés, avec leur raison :**
  - l'épaisseur en relief : « moche » ;
  - le repérage décalé : trop chargé ;
  - le second ton : on ne le voyait pas ;
  - un liseré d'encre autour du trait de couleur : il retirait le caractère ;
  - des traits de couleur qui se chevauchent : le patchwork était illisible.
- **Ce qui le rendrait faux :**
  - des bandes d'épaisseur variable ;
  - des traits qui ne remplissent pas la bande ;
  - des épines absentes ou trop variées ;
  - un filet partout.

## V · Volubilis (papier découpé noir)

- **Référence :** un papier découpé noir sur fond crème. Grandes fleurs molles, feuilles charnues, tiges fines en S, tout imbriqué avec un joint régulier.
- **Les fleurs, la partie la plus travaillée.** Une fleur est une **grappe de pétales ronds** de tailles inégales autour d'un petit cœur. Les creux du contour sont là où deux pétales se rejoignent.
  - Refusé : une corolle radiale échancrée, qui fait marguerite de clip-art.
  - Refusé : une rosace régulière.
  - Refusé : une forme en carré arrondi, quand la fleur épouse trop sa place.
  - Refusé : une fleur contenue dans un cercle.
  - La fleur s'aplatit **un peu** contre ses voisines et le cadre, sans perdre ses lobes.
  - Les pincements doivent rester visibles : un cœur petit, des pétales assez écartés.
- **Le cœur des fleurs.** Une grappe de 3 à 7 pois, de tailles libres, placés à la main. Une couronne régulière de six pois a été refusée comme « artificielle ».
- **Les feuilles.**
  - Des ovales et des gouttes charnues, qui remplissent leur place et sont aplaties par leurs voisines.
  - Elles se terminent par un **col court et doux** vers la tige.
  - Refusé : feuilles triangulaires ou en éclats, en éventail, en fléchette (long col sur petit corps), en têtard, ou tarabiscotées.
- **Les tiges.**
  - De longues courbes en S, plus épaisses en bas, avec une épaisseur qui respire.
  - Jamais de croisement en X, jamais collées l'une à l'autre, jamais un bout nu.
  - Chaque tige finit sur une feuille, une fleur ou une autre tige.
  - Les branches partent tangentes à leur tige, sans V.
- **Toujours :**
  - aucune feuille flottante, sans tige ;
  - **aucun espace vide**, même quand la référence en a un ;
  - quelques rares fleurs d'encre non-dalles, avec leur tige, pour combler les derniers grands vides.
- **Densité :** avec beaucoup de fleurs, les feuilles se font plus petites et plus serrées pour ne jamais laisser de vide.

## VI · Chamade (page rayée au feutre, cœurs)

- **Référence :** un grand cœur rayé en noir et blanc, fait de bandes, sur un fond de bandes droites.
- **Le fond.**
  - Des bandes d'encre au feutre, **presque** droites et **presque** parallèles : bords tremblés, épaisseur variable.
  - Toutes suivent une grande onde commune, en relief sur toute la page, avec des zones plus calmes et d'autres plus agitées.
  - C'est la version validée. Une tentative avec des vagues d'orientation variée a été refusée, et on est revenu exactement à la précédente.
- **Les cœurs.**
  - Chacun a sa forme : dodu, élancé, trapu, penché, aux lobes inégaux, à la pointe ronde ou longue. Refusé : des cœurs tous pareils, « kitsch ».
  - Les extrêmes (très haut et bancal, en citron) ont été resserrés.
  - Un trait d'encre les cerne. **Pas de liseré de papier** : les bandes du fond touchent le trait.
- **Le remplissage des cœurs :**
  - des rayures courbes en chevrons qui épousent la pointe ;
  - des rayures en biais ;
  - une **coulée**, reprise de l'ancien Chamade en « pouring art » : des anneaux versés au centre, de moins en moins cœur vers l'intérieur, aux bords mous.
    - Refusé : des anneaux qui reproduisent le contour du cœur en réduction, « artificiel ».
    - La couche extérieure n'est jamais à l'encre, sinon le cœur disparaît dans le fond.
- **Toujours :** jamais deux cœurs qui se touchent, jamais un cœur minuscule, jamais un cœur coupé par le bord.

## VII · Guingois (quadrillage d'étoffe)

- **Référence :** une photographie d'un quadrillage noir sur une étoffe froissée.
- **La matière.** Un quadrillage tracé à main levée, avec un trait **d'épaisseur constante** et un tremblement léger et lent.
- **Le secret du relief : le contraste.**
  - Une grande partie de l'étoffe reste **calme**, avec des cases presque régulières.
  - Une ou deux **zones froissées** concentrent le relief : des bosses et des creux en plateau, et de longues arêtes où les lignes se serrent et s'inclinent.
  - L'ombre naît **uniquement du rapprochement des lignes**, sur le pourtour des reliefs.
- **Refusés, avec leur raison :**
  - le relief partout : surchargé ;
  - des bosses et des arêtes pointues, qui faisaient des angles cassés ;
  - un trait qui s'épaissit pour faire l'ombre : des taches ;
  - une grille qui se replie sur elle-même, avec des croisements et des nœuds noirs ;
  - des reliefs trop petits et hachés : il faut des mouvements amples ;
  - des reliefs tout ronds sans caractère : il faut quelques plis plus serrés.
- **La dalle.**
  - Les cases teintes au cœur du pli d'une promesse, d'une seule couleur.
  - Toujours séparée des autres dalles par des cases blanches.
  - Toujours d'un seul tenant.
- **À régler au portage :** 14 promesses sur 120 n'ont pas de dalle. Chaque promesse doit teinter au moins quelques cases.

---

## Ce qu'un nouveau venu ne « sentira » pas

- **L'utilisateur juge à l'œil, en plein écran et en détail ×3.** Un chiffre bon ne suffit pas. Montre toujours la Toile, la dalle seule et un détail agrandi.
- **Une Toile validée est figée.** Au portage, on ne l'« améliore » pas. La planche fait foi pixel à pixel, aux tirages près, qui changent avec le passage au LCG. Si le passage au LCG déplace les formes, c'est normal. Si le **caractère** change (densité, proportions, rythme), c'est faux.
- **« Pas cheap, pas artificiel »** veut dire, concrètement :
  - des tailles variées ;
  - aucune régularité mécanique ;
  - des courbes lisses ;
  - pas d'effet de démonstration technique ;
  - pas de déformation sans objet réel derrière.
- **Les petits accidents sont souvent la beauté.** Les épines de Mascaret en sont l'exemple : nées d'un défaut, gardées exprès. Avant de « corriger » un détail qui a l'air d'un défaut dans la planche, demande.
- **Quand l'utilisateur dit « un poil », c'est un poil.** Il faut changer un seul paramètre, de 10 à 20 %, et rien d'autre.
- **Les noms sont validés un par un.** Ramage, Chantourné, Brouillamini, Mascaret, Volubilis, Chamade, Guingois. Braille garde son nom, et Halin existe.

---

## Questions à poser à l'utilisateur avant de porter ces trois mondes

**Ramage**
1. Sur la Toile, les plumes de matière peuvent-elles recouvrir en partie les plumes de l'œil ? Ou l'œil doit-il toujours passer au-dessus, comme dans sa dalle seule ?
2. Quelle doit être la taille de l'œil par rapport à la place de la promesse ? Est-ce que la planche est juste, ou est-ce qu'il était trop grand ou trop petit à 40 promesses ?
3. Le croissant clair à la pointe des plumes colorées doit-il rester, sachant qu'il est obtenu en mélangeant 30 % de blanc ? Ou faut-il le prendre dans la rampe de la palette, par un ton plus clair de la même couleur ?

**Chantourné**
1. La « première version » que tu as fait rétablir est-elle bien celle de la planche actuelle, sans trame croisée ni fils alternés ?
2. Faut-il garder la largeur des fils et la forme des flammes telles qu'elles sont à 40 promesses, ou étaient-elles trop fines à cette densité ?
3. Le bord frangé du médaillon doit-il effilocher fil à fil sur toute la périphérie, ou seulement en haut et en bas, dans le sens des fils de chaîne ?

**Brouillamini**
1. À 0 promesse, quelle matière veux-tu : des découpes non-dalles dans les tons de la rampe, des chutes éparses, ou une autre idée ?
2. Dans quelle proportion faut-il des cœurs parmi les découpes, et des chutes d'une autre couleur ?
3. La différence entre les formes rondes (3 à 4 lobes, en nuage) et les formes étoilées (5 lobes et plus, échancrures profondes) doit-elle rester aussi marquée que dans la planche ?
