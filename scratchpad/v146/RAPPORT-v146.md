# Rapport du lot v146 — retours iPhone de Tom sur v145

## À savoir d'abord

- **Rien n'est encore validé par toi dans ce lot** : tout est « fait, en attente de Tom ». Trois choses à regarder AVANT tout le reste :
  1. **C-125, le tracé des lettres** : `promi-trace-lettres.html`. Le module n'est PAS branché par défaut (règle du brief : te le montrer d'abord) ;
     `?trace=1` le montre en place dans le guide et l'onboarding.
  2. **C-094, le guide en flaques** (2e récidive) : `app.html?guide=1` ; au quart : `promi-guide-variantes.html?flaques=1`.
  3. **C-118, tenir en marée** : `app.html?mareeLent=4` pour la voir au quart.
- **Ce Mac est partagé** : une autre session y fait tourner un émulateur Android, un simulateur iOS et des compilations Rust. La charge a atteint
  70 à 300 pendant la fin du lot. Je n'ai rien arrêté chez elle (consigne). Les juges de CADENCE (images au-delà de 16,7 / 20 ms) n'ont donc
  PAS pu être jugés au calme : je le dis juge par juge plus bas, avec la charge relevée.
- **Quatre défauts trouvés par la série de fin de lot, corrigés, chacun avec son juge** (détail plus bas) : la ligne « Un mot… » d'un Cercle partait
  avec le fil ; toucher le bandeau de Peaufiner pouvait faire monter une phrase de mur (et, la toute première fois, ouvrir l'offre seule) ; en clair,
  les cartes de l'Index, du Fil et d'une personne avaient perdu leurs couleurs d'état ; le « + » qui valide un nom faisait perdre le focus au champ.
- **Un défaut ancien trouvé, non corrigé (hors du lot)** : C-136 — une Toile sans parole sort entièrement colorée au chargement, environ 1 fois sur 6,
  déjà en v145.

## §1 · C-122 — Ajouter une personne (page + et fiche)
- **Cause** : toucher « + ajouter quelqu'un » remplaçait la zone par un second encart plein (`.gn-barre`), et rien dans l'app ne lisait la hauteur
  du clavier : sur l'iPhone la ligne restait dessous, et il n'y avait pas de validation joignable.
- **Fait** : la zone en pointillés EST le champ (un champ caché `#gnSaisie` garde le clavier) ; le texte s'écrit là ; un « + » orange `#FB4C0D`,
  gras, haut comme une capitale du nom, paraît dès le premier caractère, sur la même ligne, sans encart ; Retour valide aussi ; le nom se pose et
  une nouvelle ligne en pointillés s'offre ; la fiche défile (le clavier est lu par `visualViewport`) pour garder la ligne visible.
- **Trouvé en fin de lot, corrigé** : toucher le « + » faisait perdre le focus au champ (le « + » était focalisable) pendant ~30 ms : clavier qui
  peut clignoter sur l'iPhone, lettres perdues si on tape vite. Le « + » ne prend plus le focus.
- **Juges** : `redteam_ajout_personne` (1, 2 et 4 personnes, + et Retour, ligne au-dessus du clavier, aucun second encart ; + « le champ ne perd
  jamais le focus ») · `redteam_part` rejoué par ce vrai chemin (plus avec `?parts=1`) : **55/55**.
- **À valider sur iPhone** : le vrai clavier, le « + » au doigt, la ligne qui remonte.

## §2 · C-131 — La même Toile en clair et en sombre
- **Cause trouvée (un vrai défaut, petit)** : au changement de thème, `reGray` / `reGrayStudio` retiraient AU HASARD le gris de chaque cellule vide.
  Les graines, les poids et les formes ne bougeaient pas, mais les cellules vides changeaient de gris : v145, aller-retour clair → sombre → clair :
  32–34 % des pixels changés sous Pochade, 33–39 % Tesselle, 8 % Touffe, 9,6 % Braille. **v146 : 0 %** (le rang du gris est gardé).
- **Le moodboard** : statique, 43 paires clair/sombre, tracés identiques. La dalle différente que tu as vue venait de MA page des variantes de tenir
  (v145) : deux captures faites dans deux sessions, deux paroles plantées au hasard. Corrigé dans la page (une seule session).
- **Tableau monde par monde** (1, 5, 25 et 50 paroles ; écart de graine en points, carte du toucher, gris, silhouette d'une dalle seule, image
  après un aller-retour) — **identique dans les 20 mondes** : écart 0,0 pt, carte 0, gris 0, silhouette 1,0000, image 0,0 % (tableau complet :
  `planche-v146/clair-sombre.md`).

| Monde | 1 · 5 · 25 · 50 paroles | Dalle seule | Image après aller-retour | Verdict |
|---|---|---|---|---|
| Pochade | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Touffe | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Brouillamini | 0,0 pt partout | 1,0000 | — | identique |
| Halin | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Esquille | 0,0 pt partout | 1,0000 | — | identique |
| Tesselle | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Braille | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Buvard | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Ramage | 0,0 pt partout | 1,0000 | — | identique |
| Guingois | 0,0 pt partout | 1,0000 | — | identique |
| Chantourné | 0,0 pt partout | 1,0000 | — | identique |
| Volubilis | 0,0 pt partout | 1,0000 | — | identique |
| Madrure | 0,0 pt partout | 1,0000 | — | identique |
| Chamade | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Ritournelle | 0,0 pt partout | 1,0000 | — | identique |
| Bobinette | 0,0 pt partout | 1,0000 | — | identique |
| Mascaret | 0,0 pt partout | 1,0000 | — | identique |
| Éclisse | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Taille-douce | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |
| Houle | 0,0 pt partout | 1,0000 | 0,0 % · 0,0 % | identique |

  (« — » : monde qui bouge au repos, l'image ne se compare pas au pixel ; la géométrie, elle, est comparée.)
- **Juge** : `redteam_clair_sombre`.

## §3 · C-135 — La Pelote paraît dans l'image où l'Aura s'ouvre
- **Cause** : tout était préparé À l'ouverture (atlas des poils, semis, ton, dalles des îles, îles, carte graphique).
- **Fait** : tout est préparé au repos après le démarrage (jamais pendant que la Toile bouge, ni sous un doigt), le contexte graphique est gardé.
- **Mesure avant / après** (banc WebKit, du toucher à la première image de Pelote) :

| | v145 | v146 |
|---|---|---|
| 1re ouverture | 1 436 ms | 108 ms (dans l'image où l'écran paraît) |
| 2e et 5e ouverture | 324 à 564 ms | 39 ms |
| après une tenue | — | 33 ms |

- **Juge** : `redteam_aura_latence`. ⚠ En fin de lot, machine chargée par l'autre session (8 à 10), la 1re ouverture sort à 153–214 ms (la Pelote
  toujours dans la même image que l'écran ; même chiffre sur la copie d'avant les corrections du jour) ; les suivantes 36–44 ms. **À mesurer sur l'iPhone**
  avec `?mesure=1`.
- **Trouvé en fin de lot, corrigé** : cette préparation repartait ~3,2 s après « tenir », par étapes de 240 à 306 ms (un toucher y attendait 0,3 s).
  Elle suit maintenant la règle des tâches de fond : jamais dans les 6 s qui suivent « tenir » (`redteam_fluide` 5 : 306–491 ms → 30 ms).

## §4 · C-094 (2e récidive) — Le guide en flaques
- **Cause de la récidive, écrite** : la demande portait sur une matière vivante, aléatoire et ciblée ; la livraison a été une découpe géométrique trop
  large qui se déplace (un disque qui glissait du Studio au +).
- **Fait** : l'accueil est flouté À L'AVANCE (4,8) ; un masque est dessiné à chaque image : un relief tiré au hasard, un niveau d'eau qui monte —
  des flaques naissent dans les creux, grossissent, se touchent, couvrent l'écran (1,4 s) ; la phrase paraît sans aucun contour (34 px, mots-clés en
  PromiLate et en bleu Promi : « monde », « Studio » ; « commence » pour le +) ; l'entourage du Studio naît du même effet, légèrement imparfait, serré
  sur l'icône et son mot (0,7 s), puis se referme SUR LUI-MÊME (jamais de translation) ; même chose pour le + ; la fin : les flaques se vident.
  Les variantes A, B, C sont retirées de `promi-guide-variantes.html` ; `?flaques=1` la montre au quart.
- **Le tracé des lettres (4.2)** : pas branché par défaut (§13 : tu vois la page d'abord) ; `?trace=1` le montre en place.
- **Juge** : `redteam_guide` réécrit — couverture, phrase, zone Studio / +, empreinte, aucune translation, vidage, chemins. Au calme (début de lot) :
  60/60 et la cadence 6 passes sur 6 (pire image 12,8 ms).
- **Vidéo ralentie** : `planche-v146/videos/C-094-guide-flaques-quart.webm`.

## §5 · C-121 — L'orange, le + de l'accueil
- Le signe + passe en `#FB4C0D`, clair et sombre, le signe seul (son disque et son anneau ne bougent pas). **Règle inscrite** (CLAUDE.md) : l'orange
  marque les points de départ d'une action, et rien d'autre — le + de l'accueil, le + qui valide un nom, le départ de la flèche du trait. Jeton
  `--c-orange-depart` (JSON, CSS, Swift).

## §6 · C-119 — « Enregistrer la Toile » retiré de l'accueil
- Le bouton, son icône et ce qui va avec sont retirés du plateau. On enregistre par Partager : le bouton de la page remet un fichier PNG
  2160 × 3840 à la feuille de partage du téléphone (photo ou fichier) ; sans feuille, il se télécharge. Juge : `redteam_partage_toile`.

## §7 · C-120 — Les noms des icônes en bleu
- En clair : `#022140`, la valeur pleine du I de PROMI (il clignote par l'opacité, 1 → 0,6 : sa valeur la plus foncée est la pleine), 14,3:1.
- En sombre : NON appliqué — `#022140` sur la barre ferait 1,27:1, illisible ; les noms gardent la crème. Capture des deux : `planche-v146/PLANCHE-5-accueil.png`.
  Proposition : `#82AEF8` en sombre (9,2:1), si tu veux du bleu aussi la nuit (Q500).

## §8 · C-132, C-133 — Les fiches en version sombre partout, la flèche en orange
- **Fait** : en clair, chaque fiche est EXACTEMENT sa version sombre (Promi `#0E78F2`, Chiche `#7C3F58`, Cercle `#5D4978` sous le trait), pour planter,
  tenir, tenue, reçue, à plusieurs ; la page + et Peaufiner aussi. La règle « fiches en `#F7F0DE` » est retirée de CLAUDE.md. Le départ de la flèche
  (le chevron) est en `#FB4C0D` sur toutes les fiches, deux thèmes, tous les pinceaux (page + et onboarding aussi).
- **Trouvé en fin de lot, corrigé** : les cartes de l'Index, du Fil et de la fiche d'une personne demandent leurs couleurs au même résolveur que la
  fiche ; il répondait « sombre » pour elles aussi : en clair, leurs libellés d'état étaient passés à l'encre au lieu de l'orange « à tenir » et du
  violet « en cours ». Rendu (pris par `redteam_couleurs_ref`).
- **Juges** : `redteam_fiches_theme` (81/81 : chaque fiche est la même image en clair et en sombre, le fond du bas des trois natures, le chevron orange) ;
  `redteam_couleurs_ref` remis au niveau (exceptions nommées E13 à E16 : la fiche claire comparée à la référence sombre, l'orange du départ, les noms
  de la barre, le champ qui garde sa nature à « referme ») ; `redteam_decisions`, `redteam_maparole`, `redteam_murs`, `redteam_tonsurton` remis au niveau.

## §9 · C-134 — Peaufiner reste ouvert
- **Fait** : un choix s'applique sur place ; on sort par un glissement du haut vers le bas (le panneau suit le doigt, la fiche se découvre au-dessus) ;
  plus jamais la Toile depuis Peaufiner (toute fermeture générale née d'un geste dans Peaufiner est refusée, sauf supprimer / dissoudre ; l'offre
  Ma Parole ! s'ouvre par-dessus et, refermée, rend Peaufiner).
- **⚠ Le chemin de ton iPhone n'a PAS été reproduit au banc** (aucun choix ne refermait Peaufiner). Chaque refus est gardé avec sa pile et part au Mac
  avec `?mesure=1` : si la fiche se referme encore, ouvre l'app avec `?mesure=1` (Q501).
- **Trouvé en fin de lot, corrigé** : toucher le bandeau Peaufiner pour le refermer, quand une rangée réservée passait sous lui, faisait monter une phrase
  de mur (« Eh non. Mais avec Ma Parole !, oui. ») et — la toute première fois — ouvrait l'offre toute seule. Le bandeau n'est plus un mur.
- **Juge** : `redteam_peaufiner` 21/21 (+ « le bandeau n'est pas un mur », rouge sur la version d'avant la correction).

## §10 · C-088 rouvert — Ritournelle, la règle des 75 %
- **Le bug à une dalle** (« un texte qui flotte ») : une parole seule n'était pas peinte. Corrigé.
- **Fait** : chaque coulée bute contre la zone plateau → barre (6 pt autour) et s'y arrondit au lieu d'être coupée par l'écran ; la part d'une coulée se
  resserre jusqu'à neuf paroles puis revient progressivement (aucun saut entre 9 et 10) ; vue à l'échelle 1 ; aucune graine sous la barre ; deux graines
  ne se confondent plus.
- **Mesuré, de 1 à 9 paroles** : 92 à 100 % de chaque coulée visible (3 à 40 % avant), 83 à 90 % de l'écran couvert. Planche 1 à 15 :
  `planche-v146/PLANCHE-10-ritournelle-1-15.png` (et la même sur la version d'avant).
- **Q496 tranchée (§17)** : sous Ritournelle, l'appui long ne déplace plus une dalle, sans message (une coulée se centre sur sa cellule : la poser sous le
  doigt changerait le cadrage que tu as gardé).
- **Juges** : `redteam_ritournelle` réécrit (63/63, 1 à 15 paroles, écart d'échelle borné entre deux nombres consécutifs) ; `redteam_deplace` remis au
  niveau pour Ritournelle ; `banc_rendu` refigé pour Ritournelle seul (les 266 autres images au pixel).

## §11 · C-123, C-124 — L'onboarding : dalles et textes
- **C-123** : à « Promi planté ! », la Toile d'avant se retire EN FLAQUES (720 ms) — la dalle en vol part avec elle — et les voisines naissent une à une
  (140 ms d'écart ; elles poussent, les cellules autour s'écartent), puis partent une à une. Ni flou, ni dégradé, ni fondu. `app.html?onbLent=4` : au quart.
  **Vidéo ralentie** : `planche-v146/videos/C-123-onboarding-voisines-quart.webm`.
- **C-124** : tes mots ne changent pas (sauf 11.4) ; « "Prénom", donc. » et « Petite ou grande promesse, elle compte » à 28 px (80 % de la phrase de
  promesse), en `#291547` en clair ; la page suivante de même ; le message de fin coupé en lignes courtes, mots-clés en PromiLate, hiérarchie de tailles ;
  « Promi planté ! » (exception nommée au « ! », inscrite à côté de « Ma Parole ! »), « Promi » en gros en `#0E78F2` en clair ; dessous la phrase qui donne
  le ton ; le reste au toucher ; le bloc remonté au-dessus des dalles, avec de l'air. En sombre, les couleurs d'avant restent.
- **11.6** : la phrase sous « La suite t'appartient. » n'existe plus en dessous ; je comprends que c'est « Le reste se découvre en traçant. » (juste avant) :
  elle reste mot pour mot, texte à écrire par toi (Q498).
- **Juges** : `redteam_onboarding_texte` (42/42), `redteam_onb_sorties` et `redteam_onboarding` remis au niveau (le texte de 11.4, les mots-clés en
  PromiLate, deux touchers : le premier montre le reste, le second mène au compte).

## §12 · C-126 — La page du premier Promi (clair)
- Cette page a SON fond clair (la Toile de l'onboarding), ce n'est pas la fiche : ta demande s'applique telle quelle — « trace pour planter » en
  `#00341A`, le départ de la flèche en orange, le trait non tracé à l'encre de l'app.

## §13 · C-125 — Le tracé des lettres (À REGARDER AVANT TOUT BRANCHEMENT)
- **Livré** : `promi-trace-lettres.html` (tout l'alphabet, accents, chiffres, ponctuation ; ×1, ×0,25, ×0,05 ; le mode qui montre le chemin de chaque glyphe ;
  les textes de l'onboarding et du guide tracés) ; module `variantes/trace-lettres.js` ; 270 chemins tracés sur les glyphes de Gilbert.
- **Pas branché** dans l'onboarding ni le guide (règle du brief) : `?trace=1` l'y montre.
- **Défauts restants, vus au ralenti extrême** : des dents sur le « g », une fente au départ bas du « é », les barres du « t » et du « f » pas tracées de
  gauche à droite, une bosse au flanc du fût (h, n, b, d). PromiLate n'est pas livré (chemins trop grossiers).
- **Juge** : `redteam_trace_lettres` (dernière image identique au texte statique, aucune opacité intermédiaire au front, chaque glyphe finit à droite,
  R3 avec ses exceptions, repassage minimal).
- **Vidéo ralentie** : `planche-v146/videos/C-125-trace-lettres-quart.webm`.

## §14 · C-118 — Tenir : la variante A, corrigée, dans l'app
- **Fait** : plus de liseré, de filet ni de jour sous le trait ; le trait vert s'épaissit (12 → 46 pt) et devient le haut d'une nappe du même vert — une
  seule matière — qui descend EN FLAQUES jusqu'à la barre (descente 0,65 s), porte « Parole tenue. » / « Défi relevé. » à l'encre, puis remonte en flaques
  à 2 s ; l'instant dure 2,5 s ; le champ garde sa nature, la dalle sa taille (rien ne saute à 2 s). Promi et Chiche (un Cercle n'a pas de geste tenir :
  on tient une parole dans sa propre fiche). B et C retirées de la page des variantes. `app.html?mareeLent=4` : au quart.
- **Juge** : `redteam_tenir` (28/28 à charge 9). **Vidéo ralentie** : `planche-v146/videos/C-118-tenir-maree-quart.webm`.
- **Registre corrigé** : C-105, C-106, C-107 et la trace de la Pelote (C-083) validés ; C-109 remplacé par C-110 ; C-108 remplacé par C-115.

## §15 · C-116, C-128 — Commentaires, noms, visages, dates
- **C-116** : le texte d'un mot à la taille des noms (16), le visage petit et rond à gauche, sans cerclage ; « Un mot… » aussi sur la fiche d'un Cercle,
  juste au-dessus de « + Planter dans le Cercle ».
- **Trouvé en fin de lot, corrigé** : sur un Cercle, la ligne « Un mot… » partait avec le fil quand on le faisait défiler (elle recouvrait ses cartes) :
  elle vit maintenant dans le bloc collant de « + Planter ». Un Cercle SANS parole n'a pas la ligne (16 pt seulement entre « encore aucune parole » et
  « + Planter » : elle recouvrait l'état et poussait l'entrée sous le bandeau) — Q511. Le nom d'un Cercle n'est jamais abrégé (« l'atelier du samedi »
  sortait « l'atel. »).
- **C-128** : `window._noms` — entier s'il tient, sinon 6 lettres et « . », prolongé jusqu'à la lettre qui distingue (Christo. / Christi.) ; un nom se
  touche → la fiche de la personne. Posé sur les mots, la liste des parts, les Noyaux, **la phrase de la fiche, l'Index, le Fil** ; le sélecteur reste
  tel quel. Les noms des cartes ne se touchent pas (la carte entière est déjà une porte) : à trancher (Q512).
- **La date** : « à l'instant », « il y a 5 min », « il y a 3 h », « hier », « 12 oct. », l'année au-delà d'un an.
- **Juges** : `redteam_noms` (21), `redteam_commentaires` (28), `redteam_part` (55), `redteam_cercle_tom` (20 : + la ligne du Cercle au repos et fil défilé).

## §16 · C-129 — Aucun emoji
- Filtrés à l'entrée, au collage et à l'enregistrement (paroles, noms, mots, prénom, mots du Cercle), sans message ; la même liste est écrite pour Swift
  et Firebase (`portage/SPEC-DONNEES` §1.10). Juge : `redteam_emoji` (11/11).

## §17 · Les décisions du chef de chantier
- Q485 (une seule parole à plusieurs), Q486 (Chiche : chaque destinataire a sa part ; Cercle : chaque membre engagé ; Promi à plusieurs : seul l'auteur),
  Q487 (initiales sous les parts tracées seulement ; la liste montre tout le monde, une date pour ceux qui ont tracé), Q488 (« Un mot… » reste
  provisoire), Q496 (déplacement désactivé sous Ritournelle), « Un mot… » au-dessus de « + Planter » sur un Cercle : posés.

## §18 · Restes
- **C-112** : ta mesure avec `?mesure=1` sur ta Toile n'est pas encore arrivée : il reste ouvert, la page envoie ses images au Mac dès que tu l'ouvres.
- **C-102** : rejoué avec la marée, au calme relatif (charge 2,8 à 3,9) : 17 animations sur 20 sans aucune image au-delà de 20 ms ; p95 6,7 à 7,8 ms ;
  la durée tenue (1 982 à 2 026 ms pour 2 000) ; après l'animation, plus de tâche au-delà de 30 ms (voir §3). Les images longues qui restent (38 ms à la
  première image de l'instant, et des pics de 100 à 575 ms quand l'autre session charge la machine) ne sont pas jugées au calme. En WebKit, la marée
  elle-même : intervalle d'images p50 17 ms, p95 20 ms.
- **C-136 (nouveau, trouvé par la série)** : une Toile sans parole sort entièrement colorée au chargement, environ une fois sur six, déjà en v145. Mesuré,
  pas corrigé (hors du lot) : à prendre dans un lot à venir.

## Les juges, honnêtement
**Verts dans la série finale** (charge 4 à 10, l'émulateur de l'autre session tourne en continu) : `redteam_part` 55/55 · `redteam_ajout_personne` 128/128 ·
`redteam_tenir` 28/28 · `redteam_trace_lettres` 14/14 · `redteam_decisions` 98/98 · `redteam_tonsurton` 26/26 · `redteam_reperage` 16/16 ·
`redteam_cercle_tom` 20/20 · `redteam_noms` 21/21 · `redteam_commentaires` 28/28 · `redteam_peaufiner` 21/21 · `redteam_murs` 28/28 · `redteam_maparole` 14/14 ·
`redteam_joignable` 5/5 · `redteam_ecrans` 152/152 · `redteam_volume` · `redteam_tokens` 46/46 · `redteam_registre` · `redteam_onboarding` 46/46 ·
`redteam_engagement` 11/11 · `redteam_gestes` 27/27 · `redteam_partage_toile` (Guingois) 6/6 · `redteam_fiches_theme` 81/81 · `redteam_couleurs_ref`
0 écart (sur les écrans repris après correction) · `redteam_onboarding_texte` 42/42 · `redteam_onb_sorties` · `redteam_ritournelle` 63/63 · `redteam_emoji` 11/11 ·
`redteam_phrase_fiche` 74/74 · `redteam_vide` 61/61 · `redteam_air` intact (758 paires) · `redteam_pleine` 27/27 (12 durées non jugées : machine chargée) ·
`banc_rendu` 280/280 au pixel.

**Rouges ou non jugés, avec leur raison** :
- `redteam_guide` : 57 à 60/60 selon la charge ; la cadence, 5 passes sur 6 sans image au-delà de 16,7 ms (pire 6,7 à 10,4 ms), la sixième avec une image de
  69 ms pendant un pic de charge (27). Au calme (pendant le lot) : 60/60 et 6/6.
- `redteam_aura_latence` : la 1re ouverture à 153–214 ms au lieu de ≤ 120 (machine chargée ; 108 ms au calme pendant le lot).
- `redteam_fluide` (C-102) : 5/6 au calme relatif — seul le contrôle 1 (aucune image au-delà de 20 ms pendant l'animation) reste rouge ; détail en §18.
- `redteam_evol` et `redteam_rythme` : rouges dans la série (cadence 51 à 76 %, pics de charge) ; repassés seuls, les cas en cause sont verts et égaux ou meilleurs
  que la version d'avant le lot (Pochade en plantant : moteur p95 3 ms, 7 avant ; Brouillamini départ 2 166 ms contre 2 195 ; Touffe 824 contre 817).
- `redteam_clair_sombre` : une passe sur trois, sous Pochade à 25 ou 50 paroles, deux « boîtes » de dalle lues dans le moteur diffèrent entre clair et sombre
  (graines, vue, carte du toucher, gris, silhouettes identiques) — non nommé, inscrit au registre (C-131).
- `redteam_onboarding` O8 : une passe sur trois — C-136 (défaut ancien).

**Contrats de test remis au niveau des décisions** (originaux : `sauvegardes/*-avant-v146.py`) : `redteam_onboarding`, `redteam_onb_sorties`, `redteam_maparole`,
`redteam_murs`, `redteam_tonsurton`, `redteam_couleurs_ref` (exceptions E13 à E16), `redteam_volume`, `redteam_decisions`, `redteam_guide`, `redteam_ritournelle`,
`redteam_deplace`, `redteam_cercle_tom`, `redteam_gens`. Trois juges ferment maintenant Peaufiner en le déclarant (`_peaufSortie`) avant de tout fermer, sinon le
garde de C-134 refuse : `redteam_fiches_theme`, `redteam_gens`, `redteam_ajout_personne`. `redteam_air` refigé (dates relatives, ligne du Cercle).

## À valider sur ton iPhone
1. **Le tracé des lettres** — `promi-trace-lettres.html` (à regarder avant tout branchement) ; dans l'app : `app.html?trace=1`.
2. **Le guide en flaques** — `app.html?guide=1` ; au quart : `promi-guide-variantes.html?flaques=1`.
3. **Tenir en marée** — une fiche à tenir ; au quart : `app.html?mareeLent=4`.
4. **L'onboarding** (dalles qui naissent une à une, textes) — Réglages → « Revoir la présentation » ; au quart : `app.html?onbLent=4`.
5. **Les fiches sombres en clair**, le chevron orange, le + orange de l'accueil, les noms bleus de la barre.
6. **Ajouter une personne** (page + et fiche) avec le vrai clavier, puis planter à plusieurs et tracer les parts.
7. **Peaufiner** : plusieurs choix d'affilée, sortie en glissant vers le bas — avec `?mesure=1` si la fiche se referme encore.
8. **Ritournelle** de 1 à 15 paroles.
9. **L'Aura** : la Pelote dès l'ouverture (avec `?mesure=1`, la mesure part au Mac).
10. **Les noms** (mots, Noyaux, phrase de la fiche, Index, Fil) et un emoji tapé ou collé.
11. **C-112** : ta Toile avec `?mesure=1`, plante et retire quelques paroles.

## Questions ouvertes du lot
Q497 (C-127 sans demande) · Q498 (la phrase sous « La suite t'appartient. ») · Q499 (mots-clés du guide) · Q500 (noms de la barre en sombre) · Q501 (le chemin
de Peaufiner) · Q503 (Ritournelle) · Q504 (le reste au toucher) · Q506 (la marée) · Q510 (contour retiré des murs du Studio) · Q511 (pas de ligne « Un mot… »
sur un Cercle vide) · Q512 (les noms des cartes ne se touchent pas).

## Les chantiers non validés (126)

| N° | État | La demande |
|---|---|---|
| C-001 | FAIT, EN ATTENTE DE TOM | « BLOQUANT : la Pelote sur iPhone […] la rotation et la lumière se font par … |
| C-002 | FAIT, EN ATTENTE DE TOM | « La double zone derrière la Pelote, en sombre. » |
| C-003 | FAIT, EN ATTENTE DE TOM | « Tom ne voit pas la teinte du corps changer d'une ouverture à l'autre […] L… |
| C-004 | FAIT, EN ATTENTE DE TOM | « Les textes en couleur de la palette : jamais noirs. » |
| C-005 | FAIT, EN ATTENTE DE TOM | « L'Aura : composition B, figée. » |
| C-006 | FAIT, EN ATTENTE DE TOM | « Les deux phrases du concept […] passent sur la dernière [diapositive]. Le … |
| C-007 | FAIT, EN ATTENTE DE TOM | « Le travail remis après "tenir" part en tâche de fond, découpée. » |
| C-008 | FAIT, EN ATTENTE DE TOM | « Le relevé ?mesure=1 ne décale plus rien […] la Pelote reste visible. » |
| C-009 | FAIT, EN ATTENTE DE TOM | « Ramage : Tom voit une onde ronde, par intermittence, au Studio et sur la T… |
| C-010 | FAIT, EN ATTENTE DE TOM | « Studio : le geste perdu (appui long, déplacer le doigt fait varier la pale… |
| C-011 | EN COURS | « Palettes vides vues par Tom au Studio. » |
| C-012 | OUVERT | « Zzz à réintroduire. » |
| C-013 | OUVERT | « Îles ternies par le corps. » |
| C-014 | OUVERT | « Tests iPhone en attente. » |
| C-015 | OUVERT | « Usages de #DD4D23 hors état, décision de Tom. » |
| C-016 | FAIT, EN ATTENTE DE TOM | « Fond de la Toile en clair #DFCAA4, à valider. » |
| C-017 | OUVERT | « redteam_kaki. » |
| C-018 | OUVERT | « redteam_air et les dates. » |
| C-019 | OUVERT | « releve-S5. » |
| C-020 | OUVERT | « Code mort et faux positifs de redteam_volume. » |
| C-021 | FAIT, EN ATTENTE DE TOM | « Dossier de portage » (dossier portage/, dix documents, lecture seule). |
| C-022 | REPORTÉ | « Vibrations et notifications (conversation dédiée). » |
| C-023 | OUVERT | « Page du trait partagé. » |
| C-024 | OUVERT | « Héritage : Fil en ligne de temps, visages, dalle floue de la page +, Ramag… |
| C-025 | OUVERT | « Avant publication : PromiLate, Gilbert, pages légales, version. » |
| C-026 | OUVERT | « Avant Swift : archive, VoiceOver de la Toile, StoreKit, Firebase. » |
| C-027 | REPORTÉ | « Après le portage : le relevé. » (« délier » a son chantier propre : C-082,… |
| C-028 | FAIT, EN ATTENTE DE TOM | « La Toile vit au repos : de temps en temps, la matière d'une ou deux dalles… |
| C-029 | FAIT, EN ATTENTE DE TOM | « Le creux sous le doigt passe lui aussi à la carte graphique. Cible au banc… |
| C-030 | FAIT, EN ATTENTE DE TOM | « La série de juges, allégée : les juges des chantiers touchés, plus six sen… |
| C-031 | REPORTÉ | La vie au repos des huit mondes qui n'ont pas encore leur manière : Volubili… |
| C-032 | OUVERT | « Les quatre mondes neufs sont-ils gratuits ou [de Ma Parole !] ? » — à vali… |
| C-033 | OUVERT | « Le gel de Madrure à la plantation » ; Madrure à surveiller sur un vrai iPh… |
| C-034 | OUVERT | « L'écran qui vend et les six mondes payants » — à trancher. |
| C-035 | OUVERT | « Mots de l'achat sans compte » — à valider (payer sans compte, l'achat sera… |
| C-036 | OUVERT | « Les compteurs — à faire après les cinq mondes. » |
| C-037 | OUVERT | « À faire : la palette noir et blanc au Studio. » |
| C-038 | OUVERT | « Les textes de l'aide de l'Aura — mots à valider. » |
| C-039 | OUVERT | « La phrase du mur : "trop rapide" contre "1,3 s validé" » — choix fait, à c… |
| C-040 | OUVERT | « L'inventaire de joignabilité : la dette. » |
| C-041 | OUVERT | Questions anciennes dont l'état est à relire avec Tom : Q284 (les trois libe… |
| C-042 | FAIT, EN ATTENTE DE TOM | « PLANCHE SEULE pour l'outil de dessin. Ne construis rien dans l'app. Tom ch… |
| C-043 | FAIT, EN ATTENTE DE TOM | « onboarding mets tout le texte en gilbert ce sera plus beau, et espace les … |
| C-044 | FAIT, EN ATTENTE DE TOM | « La loi des points, à inscrire dans CLAUDE.md §5, avant son exception : “Le… |
| C-045 | FAIT, EN ATTENTE DE TOM | « Le trait de validation personnalisé, à concevoir, sans rien construire. Un… |
| C-046 | FAIT, EN ATTENTE DE TOM | « En haut de la fiche d'un Cercle, le mot “CERCLE” est trop haut dans son en… |
| C-047 | FAIT, EN ATTENTE DE TOM | « redteam_couleurs_ref : explique les 2 écarts du premier passage (le caneva… |
| C-048 | FAIT, EN ATTENTE DE TOM | « Des captures de Toile à la place des dalles (BLOQUANT). Dans les fiches, l… |
| C-049 | FAIT, EN ATTENTE DE TOM | « Les écrans ne réagissent plus aux changements (BLOQUANT). Quand on plante … |
| C-050 | FAIT, EN ATTENTE DE TOM | « Le corps sombre des fiches Promi devient Tropical Breeze » : Pantone 13-43… |
| C-051 | FAIT, EN ATTENTE DE TOM | « Voir un dessin ou une photo en entier. Dans toute fiche, toucher la bande … |
| C-052 | FAIT, EN ATTENTE DE TOM | « La liste « Ce que tu as tenu » de l'Aura montre toutes les paroles tenues,… |
| C-053 | FAIT, EN ATTENTE DE TOM | « « SUPPRIMER CE PROMI » passe en crème #F7F0DE : le #DD4D23 est une couleur… |
| C-054 | FAIT, EN ATTENTE DE TOM | « La phrase lilas de la page + garde sa teinte, éclaircie jusqu'à 4,5:1 : do… |
| C-055 | FAIT, EN ATTENTE DE TOM | « Extrais toutes les phrases des murs de Ma Parole ! (chaque mur, chaque var… |
| C-056 | FAIT, EN ATTENTE DE TOM | « Sortir du mode dessin sans poser : un ✕ dans le contour de l'encart du hau… |
| C-057 | FAIT, EN ATTENTE DE TOM | « Le Studio cassé : le menu des palettes du Studio bugue. Nomme la cause et … |
| C-058 | FAIT, EN ATTENTE DE TOM | « Sous certains mondes, la Toile ne répond plus au doigt. Sous Ramage notamm… |
| C-059 | FAIT, EN ATTENTE DE TOM | « En clair, le corps d'une fiche Promi prend le même traitement que celui de… |
| C-060 | FAIT, EN ATTENTE DE TOM | « Le symbole d'appareil photo ne dit plus ce que fait le bouton. Propose tro… |
| C-061 | FAIT, EN ATTENTE DE TOM | « Les couleurs du dessin passent dans Ma Parole ! : sans Ma Parole !, on des… |
| C-062 | FAIT, EN ATTENTE DE TOM | « La Toile garde sa diversité de tailles : au-delà de 7 à 9 dalles, les tail… |
| C-063 | FAIT, EN ATTENTE DE TOM | « Les phrases des murs de Ma Parole !, réécrites par Tom » : dix-huit phrase… |
| C-064 | FAIT, EN ATTENTE DE TOM | « Contradictions du dossier, tranchées : la vérité est ce que Tom voit à l'é… |
| C-065 | FAIT, EN ATTENTE DE TOM | « La grille anti-coercition n'est écrite nulle part : inscris-la dans CLAUDE… |
| C-066 | FAIT, EN ATTENTE DE TOM | banc_rendu : Guingois diffère de la référence depuis AVANT v135 (constaté av… |
| C-067 | FAIT, EN ATTENTE DE TOM | « Le plein écran, dès la page + » : toucher le dessin ou la photo sur la pag… |
| C-068 | FAIT, EN ATTENTE DE TOM | « Le partage du dessin » : seul un dessin se partage, jamais une photo impor… |
| C-069 | FAIT, EN ATTENTE DE TOM | « La phrase complète dans les fiches Promi et Chiche » (jamais dans le Fil n… |
| C-070 | FAIT, EN ATTENTE DE TOM | « Le + de l'accueil, plus visible » : agrandi d'environ 25 % (cible tactile … |
| C-071 | FAIT, EN ATTENTE DE TOM | « La Pelote, ça ne va pas : les contours font flou, pas net ; le halo c'est … |
| C-072 | FAIT, EN ATTENTE DE TOM | releve-aura, acquis 6 (« le lancer ne comble pas » : le creux lancé doit viv… |
| C-073 | FAIT, EN ATTENTE DE TOM | ENGAGEMENT — E0, « Garde-fous, avant tout autre lot » : ① le verrou de l'onb… |
| C-074 | FAIT, EN ATTENTE DE TOM | ENGAGEMENT — E1, « Gestes appris en situation » : ① un seul composant GesteF… |
| C-075 | FAIT, EN ATTENTE DE TOM | ENGAGEMENT — E2, « Le premier Promi, tenu en une minute » : ① état des lieux… |
| C-077 | OUVERT | ENGAGEMENT — E3, « Le moment "tenir" » : A1 PRIME — ni onde sur les dalles v… |
| C-078 | OUVERT | ENGAGEMENT — E4, « Écrans vides qui invitent, et phrases d'exemple à la page… |
| C-079 | OUVERT | ENGAGEMENT — E5, « Phrases d'accueil » : ① un tableau unique PHRASES_ACCUEIL… |
| C-080 | OUVERT | ENGAGEMENT — E6A, « La Pelote qui s'enrichit : maquette d'abord » (aucune in… |
| C-081 | OUVERT | ENGAGEMENT — E6B, « Intégration (après validation de Tom seulement) ». |
| C-082 | OUVERT | « Délier » (étude 2 : issue pour un Promi jamais tenu). *Ce chantier-ci augm… |
| C-084 | FAIT, EN ATTENTE DE TOM | « Le crème des fiches en clair » : le corps des fiches (sous le trait) et le… |
| C-085 | FAIT, EN ATTENTE DE TOM | « La photo d'une fiche » : recadrer au pincement, comme dans Photos sur iPho… |
| C-086 | FAIT, EN ATTENTE DE TOM | « Le dessin » : importer une ou plusieurs photos dans le dessin, chacune dép… |
| C-087 | FAIT, EN ATTENTE DE TOM | « Le + de l'accueil » : l'anneau touche les encarts du haut. Réduire le diam… |
| C-088 | FAIT, EN ATTENTE DE TOM | « Ritournelle » : au départ la Toile est trop zoomée — on doit voir plusieur… |
| C-089 | REPORTÉ | « La façade animée (GIF ou vidéo de quelques secondes en couverture de fiche… |
| C-090 | OUVERT | « Le prix de Ma Parole ! (des testeurs le trouvent trop bas) » : décision de… |
| C-091 | FAIT, EN ATTENTE DE TOM | « Un seul bouton Enregistrer, partout » : une icône seule, sans texte, discr… |
| C-092 | FAIT, EN ATTENTE DE TOM | « Le Studio : la phrase du mur au mauvais endroit » : quand on touche une zo… |
| C-093 | REPORTÉ | « Le dessin est collaboratif entre les personnes d'un Promi, d'un Chiche ou … |
| C-094 | FAIT, EN ATTENTE DE TOM | « L'arrivée sur l'accueil : le flou qui guide (remplace E2bis) » : la barre … |
| C-095 | FAIT, EN ATTENTE DE TOM | « Le trait, dans les fiches et la page + » : « TRACE TA MOITIÉ » quand la pa… |
| C-096 | FAIT, EN ATTENTE DE TOM | « La fiche d'un Cercle » : le bandeau Peaufiner revient tout en bas ; l'enca… |
| C-097 | FAIT, EN ATTENTE DE TOM | « Partager une seule parole » : la dalle au centre de l'image, un peu au-des… |
| C-098 | FAIT, EN ATTENTE DE TOM | « Les photos se tournent » : une photo dans la bande d'une fiche, comme une … |
| C-099 | FAIT, EN ATTENTE DE TOM | « Le bouton recadrer de l'accueil » : ses trois pois enfreignent la loi des … |
| C-100 | FAIT, EN ATTENTE DE TOM | « La réactivité des murs » : au Studio, toucher une zone floutée ne réagit q… |
| C-101 | FAIT, EN ATTENTE DE TOM | « Déplacer une dalle sur sa Toile », à inscrire sans rien construire : un to… |
| C-102 | FAIT, EN ATTENTE DE TOM | « redteam_fluide flotte » : après « tenir », trois passes du juge sur quatre… |
| C-103 | FAIT, EN ATTENTE DE TOM | « redteam_decisions flotte sur le champ du Cercle » : deux passes sur cinq l… |
| C-104 | FAIT, EN ATTENTE DE TOM | « Supprimer mon compte » devient la dernière ligne des Réglages. |
| C-111 | FAIT, EN ATTENTE DE TOM | « Le moment tenir : plus lent » : pour un Promi comme pour un Chiche l'étape… |
| C-112 | FAIT, EN ATTENTE DE TOM | « La Toile saccade quand une dalle apparaît ou disparaît » : quand on plante… |
| C-114 | FAIT, EN ATTENTE DE TOM | « banc_rendu flotte sous Chamade » : 3 à 8 images de Chamade diffèrent de la… |
| C-115 | FAIT, EN ATTENTE DE TOM | « À plusieurs : la règle de la part. » Tom : il faut décider de la règle ; l… |
| C-116 | FAIT, EN ATTENTE DE TOM | « Les commentaires apparaissent-ils correctement ? Quand on reçoit un Promi … |
| C-118 | FAIT, EN ATTENTE DE TOM | « Tenir : une continuité, pas trois écrans. » Tom : la durée est bonne, mais… |
| C-119 | FAIT, EN ATTENTE DE TOM | « Supprimer “Enregistrer la Toile” de l'accueil » : Tom ne l'avait pas deman… |
| C-120 | FAIT, EN ATTENTE DE TOM | « Noms des icônes de l'accueil en bleu » : Studio, Aura, Index et Fil prenne… |
| C-121 | FAIT, EN ATTENTE DE TOM | « L'orange : le + de l'accueil, et une règle » : Tom — le + de l'accueil est… |
| C-122 | FAIT, EN ATTENTE DE TOM | « Ajouter une personne, page + et fiche (bug bloquant) » : Tom — toucher « a… |
| C-123 | FAIT, EN ATTENTE DE TOM | « L'onboarding : les dalles » : les dalles colorées ne doivent pas arriver t… |
| C-124 | FAIT, EN ATTENTE DE TOM | « L'onboarding : les textes » : les mots de Tom restent les siens (seule mod… |
| C-125 | FAIT, EN ATTENTE DE TOM | « Le tracé des lettres » (module réutilisable) : au toucher, le passage suiv… |
| C-126 | FAIT, EN ATTENTE DE TOM | « La page du premier Promi dans l'onboarding » (mode clair) : « Tracer pour … |
| C-127 | REPORTÉ | Numéro sauté par le brief du lot v146 (il passe de C-126 à C-128) : aucune d… |
| C-128 | FAIT, EN ATTENTE DE TOM | « Noms et visages » : partout où un nom paraît (sauf le sélecteur) — le pseu… |
| C-129 | FAIT, EN ATTENTE DE TOM | « Pas d'emoji dans Promi » : bloqués partout où l'on écrit (paroles, noms, c… |
| C-130 | FAIT, EN ATTENTE DE TOM | « RIEN DE CHEAP, RIEN DE BORING, TOUT ARTY » : à inscrire en tête des règles… |
| C-131 | FAIT, EN ATTENTE DE TOM | « Même Toile en clair et en sombre, dans tous les mondes » : c'est EXACTEMEN… |
| C-132 | FAIT, EN ATTENTE DE TOM | « Les fiches : la version sombre partout » : toutes les fiches (Promi, Chich… |
| C-133 | FAIT, EN ATTENTE DE TOM | « La flèche en orange » : le départ de la flèche du trait (le chevron où l'o… |
| C-134 | FAIT, EN ATTENTE DE TOM | « Peaufiner reste ouvert » : un choix dans Peaufiner (fiche ou page +) s'app… |
| C-135 | FAIT, EN ATTENTE DE TOM | « L'Aura : la sphère tarde 1 à 2 secondes » : à l'ouverture de l'Aura la pla… |
| C-136 | OUVERT | Une Toile SANS parole sort entièrement colorée au chargement (les 69 cellule… |
