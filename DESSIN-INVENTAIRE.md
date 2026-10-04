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

## Ce que montrent les planches

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
