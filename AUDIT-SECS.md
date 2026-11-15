# Audit des changements secs — v200 §4, suivi v201b (C-271)

Règle de Tom (C-271) : aucun changement sec à l'écran, nulle part.
- Un texte qui change se détrace, puis le nouveau se trace.
- Un chiffre ou une valeur change en fondu croisé.
- Une boîte qui change de taille ou de place s'adapte en douceur.
- Rien n'apparaît ni ne disparaît d'une image à l'autre.

**Juge : `redteam_secs.py`.**
- Il relève l'écran à chaque image, après la peinture (WebKit, ×3, 430 × 932).
- **T** est une faute : un texte visible qui change sans transition déclarée (ni tracé, ni détracé, ni fondu, ni découpe, ni animation finie en cours).
- **B** est une faute : une rangée ou une carte repérée par sa clé qui saute de plus de 12 pt d'une image à l'autre, dans le repère de ce qui défile.
- **Résultats** : v201a 5/11 à 6/11 selon la passe, v201b 11/11.
- **Il ne juge pas les apparitions et les disparitions de texte**, ni la frappe.

## Corrigés

| | Écran · élément | Ce qui changeait d'un coup | Aujourd'hui | Lot |
|---|---|---|---|---|
| ✔ | Page + · places « qui », « avec », le verbe | « qui ? » → « moi », « moi » ↔ « Rachel », « Chiche » ↔ « chiche » | Détracé, encart en douceur, tracé | v200 |
| ✔ | Page + · le libellé du trait | « trace pour planter » → « trace ta moitié » | Détracé, puis tracé | v200 |
| ✔ | Fiche · la ligne de la phrase | « Je me promets de » → « Je promets à Rachel de » | Détracée, retracée, le titre glisse | v200 |
| ✔ | 1 · Page + · le choix des personnes | Rachel s'insère en tête : les rangées se décalent d'un coup ; sur un Cercle, tout le panneau saute de 147 pt | Chaque rangée glisse de sa place à la nouvelle, une rangée neuve se découvre, le panneau glisse (suivi à chaque image, avant la peinture) | v201b |
| ✔ | 3 · Page + Promi · la bascule du sens | L'exemple du titre change, « à qui ? » paraît | L'exemple se détrace puis se trace ; « à qui ? » se trace en arrivant | v201b |
| ✔ | 5 · Page + Chiche · « avec qui en est ? » | — | Sous `lot-V200-DOUCEUR` (la place `avec`) | v200–v201b |
| ✔ | 6 · Fiche · « Un mot… » et la liste des mots | Le nombre change d'un coup ; un mot neuf en tête fait sauter les autres de 58 pt | Le nombre en fondu croisé ; les mots glissent, le neuf se découvre | v201b |
| ✔ | 7 · Fiche · « Les Mots » | Le titre paraît d'un coup avec le premier mot | Il se trace — **non jugé** (une apparition) | v201b |
| ✔ | 8, 9 · Index, Fil · reclassement, recherche, tris | Les cartes sautent, paraissent, partent | Elles glissent, se découvrent en arrivant, se referment en partant | v201b |
| ✔ | 10 · Pastilles « pas encore vu » | Paraissent d'un coup | Grandissent de leur centre — **non jugé** | v201b |
| ✔ | 11 · Aura · les deux chiffres, la phrase | Changent d'un coup quand une parole est tenue | Les chiffres en fondu croisé, la phrase se détrace puis se trace | v201b |
| ✔ | 12 · Studio · le nom du monde, de la palette | Changent d'un coup au glissé | Se détracent puis se tracent | v201b |
| ✔ | 13 · Peaufiner · les valeurs des rangées | « en l'air » → « samedi 21 » d'un coup (la fiche est rebâtie deux fois) | Fondu croisé, qui continue sur le nœud rebâti | v201b |
| ✔ | 14 · Réglages · les valeurs | Changent d'un coup | Fondu croisé — **non jugé** (la valeur basculée par le juge ne change pas à l'écran) | v201b |
| ✔ | 15 · Les toasts | Paraissent et partent d'un coup | Se découvrent et se referment — **non jugé** | v201b |
| ✔ | 16 · La pointe d'un Promi à la jonction | La branche basse paraît double | La découpe du trait plat est calculée au ⅓ pt | v201a |

## v202a — les quatre points non faits, et les « non jugés »

**Juge : `redteam_secs2.py`** (image par image, après la peinture ; une image de plus de 80 ms dans la fenêtre : « non jugé », ni vert ni rouge). La sonde (transitions coupées) le fait rougir : 1/7.

| | Écran · élément | Aujourd'hui | Juge |
|---|---|---|---|
| ✔ | 2 · Page + · la taille de la phrase (34 → 30, et toute taille que la composition change : le titre effacé, la sortie du champ, la bascule) | La composition calcule toujours la taille finale (la même qu'en v201b, mesuré sur trois passes) ; la taille affichée y va en 320 ms. La passe se fait sur la taille finale, la taille du moment est rendue à la fin (`lot-V202A-TAILLE`). ⚠ Le retour à la ligne de l'exemple (une ligne ↔ deux) change d'un coup quand la composition coupe l'exemple. | p_choix, p_stab (scratchpad) |
| ✔ | 3 · « à qui ? » qui part | Une copie à sa place se détrace, puis part. Trouvé : en v201b, la bascule était lue APRÈS que la reconstruction avait rendu son ancien texte au sens : « à qui ? » qui arrive ne se traçait jamais non plus. | secs2 F |
| ✔ | 4 · La pastille du titre à la première lettre (et le titre effacé, C-274) | L'exemple se détrace, la pastille se remplit en flaques, ce qu'on tape paraît ; effacé, l'inverse, l'exemple se trace. | secs2 G |
| ✔ | 10 · La pastille « pas encore vu » qui part | Elle se referme sur son centre (260 ms), puis part. | secs2 C |
| ✔ | 7 · « Les Mots » | **Il paraissait d'un coup au premier mot** (un nœud neuf : l'observateur de v201b ne suivait que celui qui existait) — il se trace. | secs2 A |
| ✔ | 10 · Pastilles qui arrivent | Grandissent de leur centre (≥ 180 ms). | secs2 B |
| ✔ | 14 · Réglages · les valeurs | Fondu croisé (≥ 150 ms). | secs2 D |
| ✔ | 15 · Le toast | Se découvre et se referme. | secs2 E |
| ⚠ | Page + · une autre nature (le + → Chiche) | Une page neuve : elle arrive en entier, aucune place ne se transforme (l'exemple d'une autre nature se traçait sans composition et sortait de l'écran — régression de v202a trouvée par `redteam_app`, corrigée avant le commit). | redteam_app |
