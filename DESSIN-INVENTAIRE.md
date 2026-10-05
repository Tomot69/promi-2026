# C-042 · L'outil de dessin — inventaire des composants (planche v127, rien n'est construit dans l'app)

Planches : `planche-v127/dessin-*` (@3x, clair et sombre). Outils de planche : `scratchpad/v127/dessin/` (`ov.js` pose les éléments
par-dessus l'app rendue, `pen.js` rend le trait, `dessin.py` et `trait.py` montent les planches).

## Composants EXISTANTS, réutilisés tels quels

| Composant | Où il vit dans l'app | Cotes | Réutilisé pour |
|---|---|---|---|
| Le disque | rond Partager de Peaufiner, disques du Studio | 44 × 44, trait 2 px, rayon 50 % | chaque outil des compositions A et B ; les tons de la palette déployée |
| Le disque choisi (plein, à l'encre, icône inversée) | Studio, SOMBRE / CLAIR | idem, fond = encre du mode | plume choisie, gomme choisie, couleur déployée |
| Le petit disque de la bande | bouton photo d'une fiche (`.ph-photo-btn`) | 34 × 34, trait 1 px | le bouton de masquage, à gauche de la bande (le bouton photo est à droite) |
| La pilule pleine | menu photo (« IMPORTER UNE IMAGE », « LA DALLE D'ORIGINE ») | h 44, rayon 22, Gilbert 15 px capitales | « DESSINER » dans le menu photo (le vrai bouton, cloné) et sur la page + ; « POSER » |
| La pilule au trait | rail du pinceau de la page + (Plein, Coulé…) | h 44, rayon 22, trait 2 px | composition C (icône + mot), rangée qui glisse comme le rail |
| Le plateau | plateau d'une fiche | 342 × 60, trait 2 px, rayon 30 | composition B (les outils posés au bas de la bande) |
| Le sélecteur à deux moitiés | sélecteur de sujet de Partager | h 44, rayon 22, trait 2 px | onglets TRAIT / FOND |
| Le grand panneau | panneau du Studio | trait 2 px, rayon 30 (h > 94,5) | la couleur déployée (342 × 128) |
| Les tons de la palette | disques de palette du Studio | disques pleins | les teintes de la palette en cours |
| Le symbole du Studio | icône STUDIO de la barre d'accueil (`#studioBtn svg`, cloné) | 22 px | S2 |
| La flèche de retour | — (voir « nouveau ») | | |

## Éléments NOUVEAUX (signalés)

- **Quatre icônes au trait de 2 px**, dans la grammaire des icônes de fiche (appareil photo, partage) : la plume, la gomme, la flèche
  de retour (annuler), l'œil (masquage) et l'œil barré.
- **S1** : le rond troué de quatre quartiers pleins, séparés par un petit jour.
- **Les trois points de taille** (6, 10, 16 px), à l'encre du mode, dans une pilule au trait posée au-dessus de l'outil ; le point
  choisi est cerné. C'est l'exception nominative à la loi des points (CLAUDE.md §5).
- **Le trait** (`pen.js`) : peinture pleine et opaque, contour lissé (Catmull-Rom), largeur variable.
- **Le ton grisé** : la teinte du fond, à 28 % d'opacité, dans l'onglet TRAIT.

> ⚑ v128 : la planche est refaite en PARCOURS (`planche-v128/dessin-parcours-*`) ; trois principes : le dessin REMPLACE la dalle, le menu est compact (pastille `.chip`, 32,5 px, écart 4), « Dessiner » est en tête. Les planches v127 ci-dessous restent pour le trait (C) et les états.

> ⚑ v129 : **le mode dessin libère l'écran** — les disques et leurs noms disparaissent, l'encart du haut ne garde que son contour au trait fin (sans fond ni texte, jamais une transparence) ; tout revient à POSER ou à la sortie du mode. Planche `planche-v129/dessin-epure-*`.

## Ce que montrent les planches (v127)

- **A · la rangée d'outils** (`dessin-A-rangee-*`) — PLUME · GOMME · ANNULER · COULEUR · POSER, sur une fiche Promi, Chiche et Cercle :
  - **A** : sous la bande, icônes seules, cinq cibles réparties sur 342 pt (disques de 44, « POSER » en pilule pleine à droite) ;
  - **B** : posée au bas de la bande, dans un plateau, icônes seules resserrées (pas de 50), « POSER » en mot ;
  - **C** : sous la bande, icônes et mots, une rangée de pilules qui glisse (COULEUR et POSER sont hors champ au repos).
  - ⚠ Sur une fiche Promi ou Chiche, A et C prennent la place de « TRACE POUR TENIR » (masqué le temps du dessin). Sur un **Cercle**, il
    n'y a pas de place sous la bande : la colonne descend de 56 pt (A, C) ; en B le plateau recouvre la bande, haute de 50 pt seulement.
- **B · les tailles** (`dessin-BDE-*`) : au second toucher sur la plume ou la gomme.
- **C · le trait** (`dessin-C-trait-*`) : E1 (effilé sur les derniers 10 %, début +16 %) et E2 (derniers 25 %, début +38 %), aux trois
  tailles (2,5 · 4,5 · 8 pt) : un mot, un cœur, un trait rapide, un trait lent, un point et un trait très court (sans effilé), une étoile
  crème. Plus fin quand le geste est rapide (jusqu'à −28 %), jamais sous 1 pt ; la pression d'un stylet module la largeur (55 à 135 %).
  ⚠ Les gestes de la planche sont SYNTHÉTIQUES (courbes calculées, vitesses simulées) : ce n'est pas un doigt.
- **D · le symbole de couleur** : S1 et S2, avec l'état déployé (onglets TRAIT et FOND, teintes de la palette + l'encre du mode pour le
  trait, la teinte du fond grisée pour le trait).
- **E · les états** : plume choisie, gomme choisie, le bouton de masquage (dessin affiché, puis masqué), « Dessiner » dans le menu photo
  et sur la page +, une bande avec trois palettes mêlées (Ingénu, Truculent, Fantasque).
- Les états B, D et E sont montrés sur la composition A ; ils se transposent tels quels sur B et C.

## v130 (5 oct. 2026) — la mise en page du mode dessin (planche `planche-v130/dessin-*`, rien dans l'app)
- **Tom retient la rangée A (sous la bande).** **Principe absolu : aucune superposition sur l'espace de dessin** — ni rangée, ni menu
  de tailles, ni couleurs déployées. En mode dessin, la page se réorganise pour faire de la place ; tout revient à POSER ou à la sortie.
- **Fiche Promi et Chiche** (mesuré sur la fiche « à tenir ») : bas du trait à 315 ; la rangée à **339** (24 pt sous le trait — proposé) ;
  les tailles se déploient sous elle (393 → 437), les couleurs aussi (393 → 521) ; les disques, leurs noms et « TRACE POUR TENIR » sont
  masqués ; les trois lignes (« À Rachel », le titre, « À TENIR · … ») descendent de **36 pt** (503 → 539), espacements gardés ; la barre
  Peaufiner ne bouge pas.
- **Fiche Cercle** : bas du trait à 199 ; la rangée à **223** (24 pt) ; tailles 277 → 321, couleurs 277 → 405 ; tout ce qui est sous la
  bande est masqué (disques, « Avec… », le compte, le fil), **sauf le titre**, descendu de 42 pt (381 → 423), sous les déploiements.
- Preuve de non-superposition, lue sur la planche : le plus haut des outils est à 339 (Promi) / 223 (Cercle), sous le bas du trait
  (315 / 199) — 20 cadres sur 20 ; le plus bas des outils (521 / 405) reste au-dessus du premier texte (539 / 423).
- Restent au choix de Tom : **E1 ou E2** (l'effilé du trait), **S1 ou S2** (le symbole de la couleur), et l'écart de 24 pt.

## v131 (5 oct. 2026) — la mise en page corrigée par Tom (planche `planche-v131/dessin-*`, rien dans l'app)
- **La planche v130 ne suivait pas ses consignes.** **Fiche Promi et Chiche : tout reste à sa place.** Les trois lignes du bas ne
  descendent pas (mesuré sur la planche : 0,0 pt sur « À Rachel », le titre, l'échéance, Peaufiner et la bande). Seule la rangée bouge :
  à **16 pt sous le trait** (331 → 375). Les tailles se déploient sous elle (383 → 427), les couleurs aussi (383 → 497, panneau compacté
  à 114 pt) ; le premier texte est à 503.
- **Fiche Cercle : rien ne disparaît** — ni le titre, ni le fil, ni les disques. Tout descend d'un bloc (166 pt) pour laisser la place à
  la rangée (215 → 259) et à ses déploiements (267 → 381) ; ce qui dépasse passe sous le bandeau Peaufiner, comme en défilant.
- Toujours aucun outil dans la bande (20 cadres sur 20). Tout revient à POSER ou à la sortie.
- Gardé de v129 (non révoqué) : sur une fiche Promi, les disques et « TRACE POUR TENIR » s'effacent le temps du dessin ; le plateau ne
  garde que son contour.
- Restent au choix de Tom : **E1 ou E2**, **S1 ou S2**.

## v132 (5 oct. 2026) — CONSTRUIT DANS L'APP (`lot-V132-DESSIN`) ; les planches v130 et v131 sont abandonnées
- Choix de Tom : effilé **E2**, symbole **S2**. La surface prend tout l'écran jusqu'à la rangée, posée en bas ; les déploiements au-dessus
  d'elle ; le reste de la fiche se retire. Paramètres : `window._dessinParams`. Détail : bloc v132 de `CLAUDE.md`. Juge : `redteam_dessin.py`.
