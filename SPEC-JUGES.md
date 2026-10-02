# LES RÈGLES QUE PORTENT LES JUGES — spécification pour le portage

> Engendré par `spec_juges_generer.py` le 2026-10-02. **Les valeurs sont lues dans les juges eux-mêmes** : pour changer une valeur, on change le juge (sur une décision de Tom), puis on relance. Le portage Swift ne reprend pas Playwright : il reprend CES règles, et `banc_rendu.py` (280 images au pixel) pour la matière.

## 1 · Le rythme de chaque monde — `redteam_rythme.py`

On juge **la fin du mouvement dans le moteur** (l'image où la Toile cesse de bouger) à l'arrivée d'une parole et à son départ, à **± max(100 ms, 8 %)** sauf tolérance écrite. **Houle** (`sillons`) est l'exception : elle reste PAR IMAGE, on juge son nombre d'images (± max(3, 20 %)). La **cadence** ne tombe jamais sous 60 % de la cadence validée. Valeurs validées le 26 sept. 2026 (v60, vrai GPU), puis les décisions datées dans le juge.

| Monde | Famille | Arrivée | Départ | Tolérance écrite |
|---|---|---|---|---|
| encre | horloge | 872 ms (33 images) | 851 ms (32 images) | — |
| touffe | horloge | 812 ms (48 images) | 791 ms (48 images) | — |
| mosaique | horloge | 792 ms (47 images) | 780 ms (47 images) | — |
| braille | horloge | 865 ms (44 images) | 786 ms (40 images) | — |
| pixel | horloge | 817 ms (46 images) | 784 ms (44 images) | — |
| halin | horloge | 2270 ms (135 images) | 2995 ms (170 images) | depart ± 15 % |
| esquille | horloge | 1437 ms (82 images) | 1426 ms (73 images) | — |
| madrure | horloge | 2432 ms (132 images) | 2431 ms (133 images) | — |
| ritournelle | horloge | 1945 ms (113 images) | 2040 ms (116 images) | — |
| bobinette | horloge | 2462 ms (57 images) | 2463 ms (70 images) | — |
| terrazzo | horloge | 799 ms (45 images) | 820 ms (46 images) | — |
| gravure | horloge | 793 ms (48 images) | 797 ms (45 images) | — |
| sillons | images | 1313 ms (36 images) | 950 ms (29 images) | — |
| brouillamini | horloge | 1742 ms (70 images) | 2046 ms (92 images) | — |
| chamade | horloge | 1668 ms (44 images) | 1946 ms (44 images) | — |
| volubilis | horloge | 3178 ms (155 images) | 2472 ms (119 images) | arrivee ± 15 %, depart ± 15 % |
| guingois | horloge | 1722 ms (30 images) | 1865 ms (31 images) | depart ± 15 % |
| chantourne | horloge | 1677 ms (16 images) | 1849 ms (36 images) | depart ± 33 % |
| mascaret | horloge | 1674 ms (20 images) | 1834 ms (32 images) | — |
| ramage | horloge | 1690 ms (83 images) | 2620 ms (149 images) | arrivee ± 33 %, depart ± 33 % |

**Les constantes qui font ce rythme** (vérifiées dans le source, moteur compris) :
- Ritournelle, transition 1 900 ms
- Esquille, transition 1 400 ms
- Bobinette, transition 2 400 ms
- Madrure, transition 2 400 ms
- Halin, transition 1 800 ms
- Halin, retrait 900 ms
- ressort du moteur 0,17 / 0,22
- v61 · cinq mondes à l'horloge, 0,83 / 0,78 (= 0,17 / 0,22 à 60 i/s)
- v61 · un redémarrage de boucle fait UN pas
- v61 · mondes neufs : temps vrai en sous-pas de 1/60 s
- ressort Pochade/Touffe 0,838 / 0,79
- fondu d'arrivée 760 ms
- Brouillamini, transition 1 600 ms · retrait 900 ms
- Chamade, transition 1 600 ms · retrait 900 ms
- Volubilis, transition 1 600 ms · retrait 900 ms
- Guingois, transition 1 600 ms · retrait 900 ms
- Chantourné, transition 1 600 ms · retrait 900 ms
- Mascaret, transition 1 600 ms · retrait 900 ms
- Ramage, transition 1 600 ms · retrait 900 ms
- v72 · Ramage : le fondu du plumage d'arrivée = ARR 900 ms

## 2 · Les murs de Ma Parole ! — `redteam_murs.py`

- flou d'un réglage réservé : `blur(4.8px)` (le Studio garde les siens) ; aucun encart, aucune explication
- la phrase se pose au centre du mur touché, sans fond ni trait, en 3 lignes au plus, une seule taille ; encre {"light": "rgb(32, 25, 8)", "dark": "rgb(247, 240, 222)"}
- temps de lecture : 1,4 s + 60 ms par caractère, borné à [3000 ; 5500] ms ; elle est encore là à 2500 ms
- la toute première fois l'offre s'ouvre à la fin de la lecture ; ensuite un toucher pendant la lecture l'ouvre
- « Ma Parole ! » d'une autre couleur que la phrase, les deux à Δlum ≥ 42 du fond
- compteur global, 21 phrases dans l'ordre puis au hasard sans répéter la précédente ; remis à zéro après 14 jours

## 3 · Les notifications — `redteam_notifs.py`

- jamais de demande de permission au lancement ; « Je te le rappelle ? » à la plantation d'une parole datée, demande seulement après « oui »
- deux « pas besoin » d'affilée, puis plus rien ; rien pour une parole en l'air
- **rien quand la date est passée** ; une notification par jour au plus ; « C'est aujourd'hui » à l'heure choisie
- la page : MES PAROLES DATÉES · MES PAROLES EN L’AIR · L’HEURE · CE QU’ON ME LANCE
- les mots, au caractère près :
  - `veille_soi` — titre « Promi » · texte « Demain, c’est « lire au soleil ». »
  - `veille_autre` — titre « « rendre le livre » » · texte « Tu as promis ça à Nico. Demain. »
  - `veille_chiche` — titre « Promi » · texte « Ton Chiche à Marion arrive demain. »
  - `jour` — titre « « rendre le livre » » · texte « C’est aujourd’hui. »
  - `lair` — titre « Promi » · texte « « apprendre la guitare » flotte toujours. Un de ces jours ? »

## 4 · Les gestes, l'air, les filets, le contrat visuel

- **Partager la Pelote** (`redteam_pelote_partage.py`) : appui long **380 ms**, tolérance de déplacement **8 px** ; seule, ou dans Mon Folio, déplaçable au doigt ; jamais dans « Ma Toile ».
- **Le geste de couleur du Studio** (`redteam_studio_geste.py`) : appui **480 ms**, course horizontale **390 px** = un tour de teinte, un pas vertical de **48 px** = une palette ; on revient exactement d'où l'on vient.
- **Rien ne paraît une fraction de seconde** (`redteam_flash.py`) : aucune couche de premier plan (grille 6 × 11, 2 points au moins) ne vit moins de **800 ms**, ni au début ni à la fin ; jamais l'ancien chrome `.topbar`, `.footer`, `.statusbar` ; la page + paraît composée dès sa première image ; une plantation coupe.
- **L'air entre les textes** (`redteam_air.py`) : aucune paire de textes ne se resserre de plus de **0.6 px** à l'ENCRE contre la référence `air-reference.json` (ses paires sont la spécification : 686 paires sur 68 écrans-thèmes) ; un bloc annoncé centré entre deux voisins a des écarts égaux.
- **Les filets** (`redteam_filets.py`) : aucun trait horizontal hors de ceux que le moodboard porte : `csBotBar`, `cbb`, `dpDetails`, `dpdTog`, `dpd-tog`, `dpm-filet`, `dpMsg`, `mg-note-line`, `ix-hair`.
- **Ce qui se touche est joignable** (`redteam_joignable.py`, v118) : au centre de chaque élément interactif, `elementFromPoint` rend l'élément ou un de ses descendants ; chaque gestionnaire n'appelle que des fonctions qui existent, sur un nœud qui existe ; la dette est nommée dans `joignable-dette.json`.
- **La dalle d'origine dans la bande haute** (`redteam_origine.py`, v118) : la couleur d'origine, sauf si son écart au champ est sous **ΔE 15.0** (CIELAB) — alors la rampe de Q30 ; les cas à moins de 2.0 du seuil ne sont jugés que sur la lisibilité.
- **Le Zzz** (`redteam_nuit.py`, v118) : premier lancement en clair, Zzz activé ; nuit = coucher du soleil + 1 h → lever (NOAA, coordonnées du fuseau ; inconnu : 22 h – 7 h ; almanach de Paris à ± 3 min) ; aucune bascule sous les yeux, aucun fondu ; cran de nuit = neutres clairs à OKLCH L − 0,06 (± 0,006), tous les autres jetons au hex près, contraste ≥ 7 : 1.
- **Le contrat visuel** (`releve-design.py`, référence `design-reference.json`, figée le 30 sept.) : 25 cibles × 25 propriétés × 6 configurations ; ⚠ les couleurs n'y sont PAS comparées (accent, backgroundColor, borderColor, boxShadow, color, dalle, fill, stroke) — elles vivent dans `PROMI-TOKENS.json` et `redteam_tokens`.

## 5 · Ce que les juges ne portent PAS, et qu'il faudra porter autrement

- les deux références figées (`air-reference.json`, `design-reference.json`) photographient **l'app**, pas une décision : elles disent « rien n'a bougé », jamais « c'est juste » ; ce qui est juste est dans `ETAT-30-SEPTEMBRE-2026.md` ;
- la matière d'un monde : c'est `banc_rendu.py` qui la juge, au pixel.
