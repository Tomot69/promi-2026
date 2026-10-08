> **⚑ v134 (6 oct. 2026) — INTÉGRÉ** dans `SPEC-DONNEES`, `SPEC-ECRANS`, `SPEC-GESTE`, `SPEC-RENDU` et `JETONS`. Ce fichier reste comme journal ; le corps sombre d'un Promi y est encore « provisoire » : il est `#0E78F2`, définitif.

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

## v135 (6 oct. 2026) — ce qui a changé APRÈS l'écriture du dossier, à reporter dans les dix documents

- **Plus aucun filet** (disques, Noyaux, trait, crête ; clair et sombre) : l'exception « terre d'une fiche tenue » de JETONS et de REGLES tombe.
- **Le bouton photo** porte le cadre traversé d'un trait (SPEC-ECRANS : fiche, page +, Cercle) ; VoiceOver inchangé.
- **Sur `#0E78F2`** : les libellés lilas du Peaufiner d'une fiche Promi sont `#F4EEFF` (JETONS).
- **Contradictions du README, tranchées** : Pelote = un tour en 100 s ; fond sombre = seiche `#050302` dans le rôle `fond` ; un design = 2 €
  (« 4 pour 3 € » retiré) ; aide de l'Aura = « la plus récente en premier » ; À propos = Gilbert pour sous-titres et libellés, PromiLate pour les titres.
- **Studio** : la pagination des mondes est une rangée de barrettes (10 × 4, la courante 18 × 4), plus des points.
- **Moteur** : `_AMP_MI` — ampleur à mi-force sous TROIS mondes (Esquille 0,3 · Ritournelle 0,3 · Ramage 0,6 ; SPEC-RENDU §a) ; le banc de rendu est refigé pour eux. Guingois (et Chantourné seul) diffèrent de la référence du banc depuis avant v135 (C-066).
- **La grille anti-coercition** est au §12 de `CLAUDE.md` (les trente-deux règles de REGLES §A) ; les six critères et les six risques de Tom manquent (Q406).
- **Juge neuf** : `redteam_lexique.py` (TESTS : termes bannis et loi des points ; se porte en test sur les chaînes et en revue des composants).

## v136 (7 oct. 2026) — à reporter dans les dix documents

- **Fiche tenue** : en clair le corps est la crème, la mention TENU en `#00341A` ; la terre et l'amande ne valent plus qu'en sombre (JETONS, SPEC-ECRANS).
- **La phrase de la fiche** (`_phraseFiche`) : huit formes, le titre seul dans son nœud, « + x personnes » dépliable (SPEC-ECRANS, TEXTES).
- **Plein écran** : aussi sur la page + (SPEC-ECRANS, SPEC-GESTE). **Le +** : 84 pt (JETONS).
- **La grille anti-coercition** : le texte de Tom, `CLAUDE.md` §12 — il coiffe REGLES §A.
- **Ampleur** : Esquille, Ritournelle, Halin 0,3 · Brouillamini 1,5 · Bobinette 0,3 ; lue sur le monde choisi ; ressemis d'un monde neuf à l'autre si elle est en jeu (SPEC-RENDU).
- **Partage du dessin** (C-068) : décidé par Tom, PAS construit — mention de la nature et logo en bas à gauche par défaut, réglage qui masque la mention, une photo ne se partage jamais (MANQUES).
- **La Pelote n'a plus ni halo ni ombre** (Tom, 7 oct., C-071 : « ne masque pas, supprime ») : dans `portage/RENDU.md` et `ECRANS.md`, retirer le halo (niveau 3), l'ombre crème du sombre et l'ellipse du clair ; la colonne de l'Aura garde les cotes B, la place de l'ombre reste vide.

## v137 (8 oct. 2026)
- **Phrases des Chiche** (Q412) : « T’es pas chiche de » · « {qui}, t’es pas chiche de » · « {liste}, vous êtes pas chiches de » · « {de} me dit : t’es pas chiche de » — remplacent « Chiche de », « À … · avec … · chiche de », « … me lance : chiche de » dans `TEXTES.md` et `ECRANS.md`.
- **La Pelote** : plus aucun effet autour (ni halo, ni ombre, ni liseré) ; au bord (> 0,92 R) la couleur est celle de l'intérieur (vis-à-vis replié autour de 0,92 R), le corps est plein jusqu'à R et s'efface de R à 1,012 R. `REGLES.md` : la liste blanche des volumes est vide ; seule exception restante, le flou des murs de Ma Parole !.
- **Partage du dessin** (C-068) : construit — remplace la ligne « PAS construit » ci-dessus. Sujet d'une fiche avec dessin posé et non masqué → image = le dessin entier sur son fond, logo « Promi » (PromiLate) en bas à gauche, mention de la nature (Gilbert, capitales) au-dessus ; réglage `promi_dessin_mention` ('0' = masquée) ; jamais de photo ; dessin masqué → Folio réduit, dalle.

