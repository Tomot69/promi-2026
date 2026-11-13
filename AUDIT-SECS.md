# Audit des changements secs — v200 §4 (C-271)

Règle de Tom (C-271) : aucun changement sec à l'écran, nulle part. Un texte qui change se détrace puis le nouveau se trace ; une boîte qui change de taille s'adapte en douceur ; rien n'apparaît ni ne disparaît d'une image à l'autre.

Ce relevé forme le **lot suivant**. Dans v200, seul ce qui touche le lot a été corrigé (marqué ✔).

**Comment les entrées ont été trouvées**
- **Mesuré** : `scratchpad/v200/audit.py`. Banc WebKit, 430 × 932, ×3. Un relevé est pris dans la page, à chaque image ; il note tout texte visible qui change à sa place sans tracé en cours. Le parcours : la page + des trois natures (ouverture, bascule du sens, saisie, validation, choix des personnes, Rachel ajoutée, choix fermé), puis l'Index, le Fil, l'Aura, les Réglages, le Studio (quatre mondes) et une fiche.
- **Lu** : relevé dans le code ou vu en jugeant, sans mesure image par image dans ce lot. C'est écrit comme tel.

## Corrigés dans v200 (ils touchaient le lot)

| | Écran · élément | Ce qui changeait d'un coup | Aujourd'hui |
|---|---|---|---|
| ✔ | Page + · la place « qui » (Promi, Chiche), « avec » (Cercle) | « qui ? », « qui ose ? », « tout le monde » → « moi » à la validation ; « moi » ↔ « Rachel » ; l'encart sautait de largeur | Détracé, encart en douceur, tracé ; les pointillés partent ou reviennent en flaques (`lot-V200-DOUCEUR`) |
| ✔ | Page + Chiche · le verbe | « Chiche » ↔ « chiche » à l'ajout ou au retrait d'une personne | Détracé, puis tracé |
| ✔ | Page + · le libellé du trait | « trace pour planter » → « trace ta moitié » à l'ajout d'une personne | Détracé, puis tracé |
| ✔ | Fiche · la ligne de la phrase (`#dptQui`), les trois natures | « T'es pas chiche de » → « Rachel, t'es pas chiche de » ; « Je me promets de » → « Je promets à Rachel de » | Détracée, retracée ; le titre glisse |

## À faire (le lot suivant)

| # | Écran · élément | Ce qui change d'un coup | Trouvé |
|---|---|---|---|
| 1 | Page + · le choix des personnes | Un nom ajouté s'insère en tête de la liste : les rangées suivantes se décalent d'un coup (leur initiale et leur nom changent sous l'œil) | Mesuré |
| 2 | Page + · la phrase entière | Elle se recompose d'un coup à l'ouverture et à la fermeture d'un choix : taille 34 → 30 → 34 px (Promi 36 ↔ 30), place 342 → 230 pt. Aussi dans v196 | Mesuré |
| 3 | Page + Promi · la bascule « Je me promets » ↔ « Je promets … à qui ? » | Le verbe change ; la ligne « à qui ? » paraît ou part, d'une image à l'autre | Mesuré |
| 4 | Page + · la pastille du titre (ou du nom d'un Cercle) | À la première lettre tapée : de vide (pointillés, mot d'exemple) à pleine, d'un coup | Mesuré (la frappe elle-même n'est pas un défaut) |
| 5 | Page + Chiche · la place « avec qui en est ? » | Mêmes règles que « qui » ; elle n'est pas encore branchée sur `lot-V200-DOUCEUR` | Lu |
| 6 | Fiche · « Un mot… » | Le nombre de mots (« 1 », « +1 ») change d'un coup | Lu |
| 7 | Fiche · « Les Mots » | Le titre paraît d'un coup avec le premier mot | Lu |
| 8 | Index, Fil · « Récents » | Une action reclasse les cartes d'un coup (C-245) | Lu |
| 9 | Index · la recherche, les tris | Les cartes filtrées paraissent ou partent d'un coup | Lu |
| 10 | Index, Fil, Index d'une personne · pastilles « pas encore vu » (`.s4-att`) | Paraissent et partent d'un coup | Lu |
| 11 | Aura · les deux chiffres (tenues, en cours) | Changent d'un coup | Lu |
| 12 | Studio · le nom du monde, le nom de la palette | Changent d'un coup au glissé | Lu |
| 13 | Peaufiner · les pastilles d'échéance, les valeurs des rangées | Leur état change d'un coup | Lu |
| 14 | Réglages · les valeurs des rangées (Affichée · Masquée, etc.) | Changent d'un coup | Lu |
| 15 | Toasts (« Design débloqué ✓ », « … dissous ») | À vérifier : comment ils paraissent et partent | Lu |
| 16 | La rencontre des pointes d'un Promi (jonction, C-267) | Le trait est incliné dans la vague et droit dans le trait plat : la branche basse paraît double sur ≈ 10 pt de défilement. Aussi dans v199 | Mesuré (`redteam_un_trait`) |

L'audit mesuré ne couvre que les **textes**. Les boîtes qui changent de taille (hors la phrase de la page +) et les éléments qui paraissent ou partent n'ont pas été relevés image par image dans ce lot : c'est écrit tel quel.
