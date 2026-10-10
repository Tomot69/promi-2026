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

## v139 (9 oct. 2026)
- **La Pelote** : le contour est une limite franche au rayon de la boule (rien au-delà, un pixel de lissage) — remplace « au bord la couleur est celle de l'intérieur, le corps s'efface de R à 1,012 R » (v137). L'ombre revient (ellipse 0,45 D × 0,07 D ; encre 0,10 en clair, crème 0,105 en sombre) : `REGLES.md`, la liste blanche des volumes porte cette seule exception.
- **Le toucher de la Pelote** : profondeur q(t) = 1 − 1/(1 + t/0,60)² pendant l'appui, retour exponentiel en 0,60 s, comblement par la rotation amorti (× e^(−c/0,08)) ; la forme de l'empreinte vient du contact (`UITouch.majorRadius`, à étalonner) — remplace la loi « cède à 62 % en 50 ms puis résiste ».
- **Jetons** : en clair, le corps et l'encart d'une fiche = `#EAD9B9` (le fond de l'Index) ; les cartes du fil d'un Cercle et la carte du mot = `#F7F0DE`.
- **Photo d'une fiche** : cadrage {z, dx, dy} par parole (z 0,3 à 8, points de l'écran 390), pincement 1:1 autour du milieu des doigts, glissement 1:1 ; « Enregistrer la photo » dans la vue en entier. `ECRANS.md`, `TEXTES.md`.
- **Dessin** : tailles plume 2 · 6 · 14, gomme 8 · 18 · 36 ; un élément de dessin peut être une photo {img, x, y, w, h} ; le disque « Photo » ; le dessin partagé n'emporte pas ses photos (à trancher, Q435).
- **Accueil** : le + fait 60 pt (12 pt d'air dans la barre).
- **Main fantôme** : × 1,5, trajet 1,6 s, trois passages, elle trace la seconde moitié du trait ; elle va jusqu'au bout (tenir comme planter). Réglages : deux rangées, « Revoir la présentation » et « Revoir les gestes ».
- **Toile** : sous les douze mondes faits de leurs seules paroles, semis constant tant qu'il y a moins de neuf paroles et Cercles. Un toucher se date à l'heure de l'événement (`UITouch.timestamp`), jamais à celle du traitement.

## v140 (10 oct. 2026)
- **La Pelote, la fourrure** : densité ×1 (110 000 → 90 000 → 75 000), poil ×1, reflet d'origine — remplace « densité 3 » (v123) ; le corps est plein jusqu'au rayon de la boule et, au-delà, les POINTES dessinent la silhouette (opacité resserrée 0,30 → 0,62, couleur de l'intérieur) — remplace « limite franche » (v139) ; l'ombre à 391,224. `SPEC-RENDU`, `JETONS`.
- **La Pelote, la trace** : le chemin du doigt relevé à l'écran (un point tous les 8 pt, largeur du contact), posé au lâcher en seize arcs au plus ; un appui sans glisser = une étoile de huit branches (longueur selon le contact et la profondeur). `SPEC-GESTE`.
- **Dessin et photo** : l'un REMPLACE l'autre dans la bande (pas de coexistence) ; plume 2 · 6 · 22 ; cibles de 44 pt, point = trait + 3 ; un dessin partagé emporte ses photos importées (Q435) — remplace « n'emporte pas » (v139). **Le dessin est collaboratif** : `SPEC-DONNEES` §5 bis, `SPEC-ECRANS` (écrit en v140).
- **Enregistrer** : une icône seule (SF Symbol `square.and.arrow.down`), VoiceOver « Enregistrer » — photo en entier, dessin en entier, plateau de l'accueil (l'image de la Toile). `SPEC-ECRANS`, `TEXTES` (« Enregistrer la photo » disparaît).
- **Accueil** : le + fait 72 pt (disque 45, anneau 13,5) ; la barre du bas 100 pt (710 → 810 ; le centre du + reste à y 760). `JETONS`.
- **Toile** : sous les douze mondes faits de leurs seules paroles et moins de neuf paroles — la parole neuve prend la cellule libre la plus proche des autres ; la vue cadre à 0,8 cellule de marge pour une parole, 1,25 dès deux, zoom ≤ 3,6. `SPEC-RENDU`.
- **Murs** : au Studio, le mur est le panneau entier (la réunion des zones floutées) ; le panneau des palettes ouvert sur un monde réservé est flouté. `SPEC-ECRANS`.
- **Onboarding** : REMPLACÉ par E2 — prénom → principe → vraie page + (phrase fantôme) → fiche → dernière ligne → compte ; « Plus tard » partout ; textes dans `TEXTES_ENGAGEMENT.e2` (provisoires). `SPEC-ECRANS` §2 est à réécrire depuis `ENGAGEMENT-E2.md`. « TRACE POUR TENIR » 19 px, points à tracer Ø 12.
- **E2bis** : `promi_devoile` — la barre se dévoile (Index à la première plantation, Aura au premier tenu, Studio au retour de l'Aura, Fil à la première parole adressée ou reçue) ; réglage « Tout afficher ». `SPEC-DONNEES` §9, `SPEC-ECRANS` §1.
- **Fiche** : après « tenir », la phrase complète reste (elle retombait sur « à moi ») ; sur l'instant, la ligne d'état descend sous un titre de deux lignes.

