# Portage — notes à intégrer au dossier (C-021, lot v130)

- **C-031 · la vie au repos (Tom, v129)** : dans le prototype, seize mondes bougent au repos ; **Volubilis, Guingois, Ramage et Esquille
  restent immobiles** (raisons dans `CHANTIERS.md`, C-031). Leur mouvement de repos est REPORTÉ au portage Swift : à écrire dans leur
  peintre natif, une ou deux dalles, 1 à 2 s, retour exact à l'image d'avant.
- **C-045 · le trait de validation personnalisé (concept, v129)** : si Tom le retient, le chemin est une DONNÉE de la parole (une liste de
  points lissés), jamais une image — voir `TRAIT-PERSONNALISE-CONCEPT.md`.
- **C-048 · UNE DALLE SEULE EST ENGENDRÉE, JAMAIS DÉCOUPÉE (Tom, v130, 5 oct. 2026 — « interdit, définitivement, dans le prototype comme
  dans Swift »)** : partout où une dalle paraît seule (bande d'une fiche, carte de l'Index et du Fil, fil d'un Cercle, liste de l'Aura,
  partage), le peintre du monde ENGENDRE la dalle demandée — ses carreaux, ses points, ses traits, ses sillons, et eux seuls — à sa
  taille finale. On ne rend jamais la Toile (ni un morceau de Toile) pour la rogner ensuite sur la cellule : le contour devient celui
  d'une découpe au pixel, et les éléments des voisines y laissent des éclats. En Swift : une fonction `dalle(id, taille)` par monde,
  qui ne reçoit que la graine de cette dalle et ses voisines (pour la forme), et ne peint que ce qui lui appartient ; aucune
  `UIImage`/`CGImage` recadrée. Juge du prototype : `redteam_decoupe.py`, famille G2.
- **C-049 · UNE SEULE SOURCE DE VÉRITÉ (Tom, v130)** : la liste des paroles. Chaque écran (Index, Fil, Aura, fil d'un Cercle) s'y abonne
  et se remet à l'état réel à l'image suivante ; le Fil ne montre jamais une parole qui n'existe plus. En SwiftUI : un seul modèle
  observable, aucun écran ne garde sa propre copie.
- **C-050 · le corps sombre d'un Promi (v131)** : cobalt électrique `#273CEB`, texte crème `#F7F0DE` ; « Ma Parole ! » y vaut `#FF8664`.
  (Tropical Breeze, v130, est écarté.)
- **C-051 · voir une photo en entier (v131)** : toucher la bande qui porte une photo (ou un dessin), jamais une dalle ; fond plein seiche,
  image entière, un toucher ou ✕ referme ; VoiceOver « Voir la photo en entier ». En SwiftUI : `fullScreenCover` sans transparence.
- **C-052 · « Ce que tu as tenu » (v131)** : toutes les paroles tenues, dans l'ordre chronologique, l'Aura défile.
- **C-042 · le dessin (v132, construit dans le prototype)** : un dessin est une LISTE DE TRAITS (`{fond, traits:[{c, t, g, pts:[x,y,t,p…]}],
  poses, pose, masque}`), en points sur une surface de 390 × 754 — jamais une image ; chaque trait garde sa couleur ; `poses` est ce que
  POSER a posé. En Swift : `PKCanvasView` ne convient pas tel quel (couleurs figées, effilé E2, gomme qui rend le fond) — un rendu à soi
  (`Path` remplis), le même modèle de largeur (`largeurs` dans `lot-V132-DESSIN`). Mode dessin : la surface plein écran, la rangée en bas.
- **v133** : le corps sombre d'un Promi est PROVISOIRE (`#1A52F0`, C-050 — Tom choisit sur l'iPhone par `?bleu=`) : ne pas le figer en Swift
  avant son choix ; « Ma Parole ! » sur ce corps et la phrase lilas en dérivent (3:1 et 4,5:1, même teinte OKLCH). Mode dessin : surface
  390 × 742, rangée centrée entre la surface et le bord bas utile (`safeAreaInsets.bottom`), déploiements à 16 pt ; un ✕ « Quitter le dessin »
  dans le contour ; les teintes du trait et du fond sont dans Ma Parole ! (sans elle : l'encre du mode sur le champ de la nature). Les murs :
  dix-huit phrases, chacune avec sa liste de mots en orange (`TEXTES` dans `lot-V104-MURS`).
