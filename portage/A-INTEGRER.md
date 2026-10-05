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
- **C-050 · le corps sombre d'un Promi** : Tropical Breeze `#8ACBE8` (Pantone 13-4307 TPG), texte à l'encre `#201908`.
