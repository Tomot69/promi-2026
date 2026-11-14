# Red team de toute l'app — v202a (C-276)

Demande de Tom : « une app propre avant de passer à la suite ».

**Méthode**
- **`redteam_app.py`** parcourt 19 écrans dans les deux thèmes, à trois échelles : 1 (430 × 932), 0,79 (330 × 714) et la fenêtre de Tom (390 × 651, son état exporté). Les 19 écrans :
  - l'accueil ;
  - la page + des trois natures ;
  - les fiches des trois natures et Peaufiner ;
  - l'Index, le Fil, l'Aura, les Réglages, Partager ;
  - le Studio sous six mondes.
- Il relève les erreurs (de la page et de la boîte noire), les textes qui sortent de l'appareil, les textes coupés par leur boîte et les textes qui se recouvrent.
- v201b est servie à côté, avec le même hasard : un relevé présent dans les deux versions est **préexistant**, un relevé présent dans la seule v202a est une **régression**.
- Chaque relevé est ensuite **regardé** : un relevé n'est pas un défaut tant qu'on ne l'a pas vu.
- **`redteam_secs2.py`** juge image par image les transitions que v201b avait faites sans les juger.
- Les juges d'état déjà écrits complètent le tout : `index_fil` (deux onglets, rechargement, `?jour=+N`, retour au même endroit), `effacer` (Annuler, l'effacement), `plantation_durable`, `echeance`, `lexique` (les textes de Tom, les termes bannis), `joignable`.

## Corrigés dans v202a (bloquant ou visible, sans décision de Tom)

| Défaut | Écran | Gravité | Preuve | Correction |
|---|---|---|---|---|
| « Les Mots » paraît d'un coup au premier mot (v201b le disait fait, sans l'avoir jugé) | Fiche, les trois natures | visible | `redteam_secs2` A : « NNNN… » sur v201b | Le titre né à l'écran se trace (C-125) |
| « à qui ? » qui arrive à la bascule du sens ne se traçait jamais. La condition se lisait après que la reconstruction avait rendu l'ancien texte : elle était toujours fausse. | Page + Promi | visible | trace du journal `_douceur` : `_basc` toujours faux | La bascule se lit sur le texte neuf. La place qui part se détrace à sa place (`redteam_secs2` F). |
| Un titre fait d'un seul mot plus long que sa carte (« jcicjccjc… », dans l'état de Tom) sort de la carte et de l'écran | Index | visible | `redteam_app` D, vue Tom, deux thèmes | `overflow-wrap:anywhere` sur le titre des cartes |
| La pastille « pas encore vu » part d'un coup | Index, Fil | visible | AUDIT-SECS point 10 | Elle se referme sur son centre (`redteam_secs2` C) |
| La taille de la phrase de la page + saute (34 → 30, 30 → 24, 24 → 36 à la sortie du champ) | Page + | visible | relevé image par image (`scratchpad/v202`) | Elle va en 320 ms. Taille finale identique à v201b (3 passes sur 3). |
| L'exemple du titre revient d'un coup quand on efface le titre (C-274) | Page + | visible | Tom, iPhone | Détracé, flaques, tracé (`redteam_secs2` G) |
| **Régression de v202a, trouvée avant le commit** : en ouvrant la page + dans une autre nature, l'exemple neuf se traçait sans composition et sortait de l'écran (jusqu'à x 610 pour 390) | Page +, trois natures | bloquant | `redteam_app` D sur 9 vues, aucune sur v201b | Une autre nature est une page neuve : aucune transition. En fin de transition d'un titre, la composition passe avant que l'encart se pose. |
| Le même texte se détraçait puis se retraçait quand la composition coupait l'exemple en deux lignes. La comparaison ôtait le `<br>` sans mettre d'espace (« deNadine » ≠ « de Nadine »). Pendant ce tracé inutile, l'exemple sortait de l'écran : x jusqu'à 600 pour 390. | Page + d'un Cercle (et toute place d'exemple coupée) | visible (préexistant, v201b) | `redteam_app` D, vue Tom, deux thèmes ; le journal `_douceur` (« de » → « vers », le même texte) | Un `<br>` compte pour un espace |
| Un tirage qui ne change rien : « jamais le même sol deux ouvertures de suite » (v125) tombait quand le ton tiré cédait au suivant | Aura | visible (régression de C-275, trouvée par la porte) | `redteam_corps` 32/33 | Le tirage se lit sur le ton effectif (33/33) |
| La frange douce du bord de la Pelote (v141) s'amincissait : 2,5 pt au lieu de 3 à 8,5 | Aura | visible (régression de C-275, trouvée par la porte) | `redteam_bord` F | La marche d'opacité ne vaut qu'à l'intérieur (`redteam_bord --gl` 12/12) |


## Les juges d'état et de couleur (porte)
- `index_fil` (état de Tom, trois parties) : 46/46, 25/25, 11/11.
- `effacer` : 26/26. `echeance` : 11/11, après un contrat remis au niveau : la boîte noire (C-262) consigne l'adresse, `?jour` compris ; ce n'est pas mémoriser. Le rouge était identique sur v201b.
- `lexique` (termes bannis, textes de Tom) : 3/3. `joignable` : 5/5.
- `couleurs_ref` : 0 écart, en quatre parties.
- `plantation_durable` : non jugé, plafond de 10 minutes atteint deux fois. Tous les cas mesurés avant l'arrêt sont pleins : 20/20 paroles écrites et présentes, second onglet compris.
- Erreurs JavaScript et boîte noire : 0, sur les 19 écrans × 3 vues × 2 thèmes.

## Relevés regardés, qui ne sont pas des défauts
- Les titres des cartes de l'Index et du Fil « coupés » (24 à 34 relevés) : la boîte de ligne touche la boîte qui rogne, l'encre est entière (capture `rt_index.png`).
- « à moi » et le titre d'une carte qui se « recouvrent » : leurs boîtes de ligne se chevauchent de 2 à 3 pt, pas leur encre.
- « Toi » sous le Noyau de la fiche : sa boîte finit exactement au bord de `#dAura`, l'encre est entière.

## Ouverts : une question par point, pour Tom
0. **Les îles de la Pelote, en clair (Q618).** C-275 donne au poil un ton exact de la palette. Sous Ingénu, une île porte la couleur exacte de sa nature : posée sur un poil qui est lui aussi un ton de nature, elle se noie (ΔE 8 à 13 pour un plancher de 15, `releve-aura` ; 29 à 34 en v201b). La rendre lisible demanderait de dériver une couleur. Couleurs exactes et plancher retiré, ou une clarté propre au poil du clair ?
1. **La lumière de la Pelote.** Le côté de l'ombre est maintenant le ton exact de la palette ; le côté éclairé monte encore un peu (de moitié par rapport à avant), et c'est lui qui fait le volume. Faut-il le garder ou le retirer ? (Sans lui, la boule devient un disque plat de sa couleur.)
2. **Le corps de la Pelote.** La règle de v123 est gardée : un autre ton exact tiré au hasard à chaque ouverture, ΔE00 ≥ 15 face au poil, jamais kaki ; à défaut, le ton qui contraste le plus. Préfères-tu le ton qui contraste le plus, toujours ?
3. **L'exemple qui passe d'une ligne à deux** (la coupe de la composition, à la sortie du champ) change de ligne d'un coup, pendant que sa taille va en douceur. Faut-il animer aussi le retour à la ligne (un retrait puis un tracé) ?
4. **La première lettre tapée** paraît après le détracé de l'exemple et les flaques : environ 1 s, toutes les lettres tapées entre-temps comprises (rien n'est perdu). C'est ce que demandait le §2. Est-ce trop long sur l'iPhone ?
