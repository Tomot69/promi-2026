# ÉTAT DES LIEUX

## ⚑ JOURNAL DES LOTS — une ligne par lot (à partir du 13 sept. 2026)

| Date | Lot | app.html | Ce qui est fixé |
|---|---|---|---|
| 27 sept. | **Clôture de session (v60–v61)** | — | Tom garde la nouvelle durée de Halin (temps réel). Fichiers de preuve rangés dans `sauvegardes/rythme-v61/` (version validée v60, sa page, les deux dérives). Série complète sur v61 : verte sauf deux rouges intermittents, pris une fois en série, verts deux fois seuls — **`redteam_geste` · « Mes Promi : le % est peint »** (l. 126 : compte les pixels orangés de `#shCanvas`, seuil 60 ; le contrôle n'imprime PAS son compte, on ne sait pas de combien il a manqué — instrument au pixel sur un canevas, famille du §7) et **`redteam_nuee_dalle` · « [sombre] 10 · au doigt, sa dalle ouvre SA fiche »** (`None · False` : `TROUVE_PID` n'a trouvé AUCUN point de la dalle neuve où le canevas soit au premier plan ; il cherche AVANT `closeAll`, la fiche du potager encore ouverte — cause probable lue dans le code, non prouvée : dépend de l'endroit où la dalle tombe). `releve-aura` : « [clair] les dalles se noient », ouvert depuis v42. |
| 27 sept. | **Lot v61 — les mouvements à l'horloge, sauf Houle ; le banc sur le vrai GPU** (sauvegarde `app-avant-v61.html`) | — | Tesselle, Braille, Buvard, Éclisse, Taille-douce : ressort au temps (= 0,17/0,22 à 60 i/s) ; mondes neufs : temps vrai en sous-pas de 1/60 s ; l'œil de Madrure (GPU) compte les images lentes jusqu'à 250 ms ; un redémarrage de boucle fait UN pas. Houle reste par image (exception écrite). **Madrure mesurée jusqu'ici sur son chemin de SECOURS** (le banc n'avait pas de GPU) : outils passés au vrai GPU. A/B v60 ↔ v61 (pages fraîches, GPU) : identiques sauf Halin −105/−147 ms (ses accrocs ne lui volent plus de temps). Sous processeur bridé ×3 : v61 38/38, v60 26/38 (Taille-douce départ 660 ms au lieu de 357). WebKit 13 mondes : page validée = app. `redteam_rythme` réécrit : fin du mouvement dans le moteur (horloge), images (Houle), cadence ; `--bride=3` ; mesure du changement ramenée à 16,67 ms. Premier jet gardé `sauvegardes/redteam_rythme-v60-images.py`. |
| 26 sept. | **Lot v60 — le rythme des treize mondes : l'app contre celebration-mondes.html ; `redteam_rythme.py`** (sauvegarde `app-avant-v60.html`) | — | Outil `sauvegardes/rythme-v60/rythme.py` : arrivée et départ de chaque monde, sur la page validée, dans l'app par le même appel moteur, et par le VRAI chemin (page +, tracé ; fiche, Supprimer, Oui). Grandeur : la dernière image où un bloc de 32 px bouge encore (l'écart moyen sur toute la Toile ratait les départs d'une seule dalle). Deux tirages semés (place d'arrivée, semis d'un monde neuf). **Page = app** monde par monde, dans le bruit. **Vrai chemin, corrigé** : le frémissement (`liven`) se superposait à l'arrivée et au départ → il cède pendant un mouvement de dalle ; la page + se repeignait en glissant ; l'Index fermé se reconstruisait (`offsetParent` ≠ visible, §8) ; les passes d'interface attendent la fin du mouvement (`_apresMouvement`) ; **supprimer une parole laissait sa dalle sur la Toile** → `rafraichit` resynchronise. **Reste, porté à Tom** : six mondes (Tesselle, Braille, Buvard, Éclisse, Taille-douce, Houle) ont un ressort compté en IMAGES — sur le vrai chemin, les images perdues à la fermeture de la page + / de la fiche les étirent (Taille-douce départ 345 → 530 ms, mêmes 17 images ; Houle 482 → 1 173 une fois) ; Madrure varie en vrai de 1 983 à 2 764 ms (cache par tranches). `redteam_rythme.py` : valeurs en dur, durée (mondes à l'horloge) ou images (mondes comptés en images) + cadence ≥ 60 % ; prouvé contre `app-derive-latence.html` (20 rouges / 26, aucune constante touchée) et `app-derive-ressort.html` (constante + 4). |
| 26 sept. | **Lot v59 — les latences ; la bande de Nuée sous Madrure ; un juge mort** (sauvegarde `app-avant-v59.html`) | — | Outil `sauvegardes/latences-v59/latences.py` (vrai clic, Chromium + profileur CDP, WebKit ; `--deux` = 1re et 2e ouverture). **Causes mesurées** : 1 · la passe des polices relisait le style calculé de TOUT le document après chaque clic et chaque rendu (jusqu'à 1,3 s pendant une plantation) → synchrone sur ce qui est À L'ÉCRAN seulement (+60, +420, +900 ms), le reste en tâche découpée à +1,5 s ; 2 · la taille de la phrase de la page + se recalculait (mesures forcées) à chaque mouvement du doigt → mémorisée tant que rien ne change ; 3 · `repasse` (couleurs sur fond sombre) après chaque `_ficheCotes`/`_fichePose`/`_s4Index` → une fois par image ; 4 · `ajusteTitres` réécrivait tous les titres huit fois par ouverture → mémorisé par titre, appels fusionnés ; la passe « plateau » (clic + changement d'écran, doublée) → fusionnée ; 5 · une plantation invalide toutes les dalles en cache → rappel des 40 dernières dalles demandées, re-rendues en tâche de fond quand l'app est au repos depuis 1,5 s. Chromium, bloqué avant → après (1re ouverture) : page + 900→483 · plantation 900→583 · fiche 1283→700 · Index 717→233 · Partager 700→133 · Réglages 583→133 · Studio 250→33 · Cercle 250→33. Restent : l'impression de la plantation (≈ 680 ms, animation conçue `printTirage`) et la Pelote de l'Aura (peinture par image). **Nuée sous Madrure** : l'œil remplissait sa case de bande (×1,35) → 0,58 de la case. **`redteam_polices` était mort** (il ne regardait que Fraunces/Bricolage/Apfel, retirées le 22 sept.) → réécrit sur les trois polices, prouvé (sonde : 54 éléments pris). **`redteam_nuee_dalle` 37/38** : non reproduit en 24 passages (série, charge, v55) ; `sauvegardes/serie.py` garde désormais le journal complet de chaque passage (`sauvegardes/journaux/`). |
| 25 sept. | **Lot v58 — Bobinette : la goutte d'eau supprimée, la couleur parcourt les fils** (sauvegarde `app-avant-v58.html`) | — | La déformation radiale autour de la dalle (le « champ ») ÉTAIT l'effet goutte d'eau : supprimée — aucun fil ne se déforme, seules les tuiles tournent sur leur axe (900 ms, inchangé). Les arcs qui changent sont reliés en FILS (bout à bout) ; un train de trois segments d'autres tons de la palette parcourt chaque fil d'un bout à l'autre, puis la nouvelle couleur le gagne par ses deux bouts et se referme au milieu. Chaque fil a son moment et son sens (tirés de sa clé), sa durée selon sa longueur (0,9 à 2 s). |
| 25 sept. | **Lot v57 — plus aucune onde : Esquille et Bobinette** (sauvegarde `app-avant-v57.html`) | — | **Cause de l'onde d'Esquille, mesurée** : à chaque plantation 57 éclats changeaient en une image, partout — l'état final se calculait depuis la place COURANTE des graines (à peu près au point fixe), toutes bougeaient d'un rien, et chaque promesse qui franchissait une cassure changeait d'éclat. → relâchement local aussi pour Esquille, les graines éloignées partent de leur place finale d'avant (`_finPrev`, Esquille seul), et chaque morceau garde sa décision de refente sauf près de la dalle : 13 éclats à l'arrivée, 4 au retrait. Rendu : plus de bascule à mi-course — la couleur se fond (620 ms, lissée), les voisins de la dalle sont poussés doucement vers l'extérieur puis reviennent, chacun à SON moment (0–320 ms, tiré de sa clé). **Bobinette** : plus de tour compté de proche en proche (l'effet goutte d'eau) — chaque arc part à son moment (0–420 ms) et dans son sens (tirés de sa clé) ; la couleur VOYAGE dans le fil : deux segments d'autres tons de la palette le parcourent d'un bout à l'autre, la nouvelle couleur le gagne par les deux bouts et se referme au milieu. Tuiles qui tournent et anneau qui naît : inchangés. |
| 25 sept. | **Lot v56 — Bobinette repris élément par élément ; Pochade/Touffe à peine plus lents** (sauvegarde `app-avant-v56.html`) | — | **Pochade, Touffe** : 0,17 → 0,162 et 0,22 → 0,21 par image, montée 300 → 360 ms (Tom : « très très peu »). **Bobinette** : chaque arc est un élément — (1) il se DÉFORME dans le champ du mouvement (traction autour de la dalle qui arrive, fermeture autour de celle qui part, un léger tour ; champ continu, les fils restent attachés ; hors champ l'arc exact) ; (2) une tuile qui se retourne TOURNE d'un quart de tour, la couleur coulant dessus ; (3) la couleur coule le long des fils, de proche en proche, le tour compté en ARCS depuis l'anneau ; (4) l'anneau neuf grandit depuis son centre. Plus d'éclats. Anneaux placés par ordre de plantation et à place FIDÈLE (57 tuiles retournées → 12 à 39), relâchement local 2 → 1,5 pas (arcs changés au-delà de 3 pas : 63 → 11). **Couleurs** : sous Ingénu, les fils prennent la couleur de palette figée de leur cellule (multicolore, comme le PDF) ; l'anneau d'une parole garde sa nature (Q329). |
| 25 sept. | **Lot v55 — sept corrections de mouvement et de rendu** (sauvegarde `app-avant-v55.html`) | — | **Halin** : bulles jusqu'à 4,7 jour² pendant les mouvements (1,3 au repos) → bornées à un disque de 1,2 jour et à l'aire de repos ; 0 saut. **Pochade, Touffe** : pas calculés sur le TEMPS (une fraction par image variait avec la durée des images) ; au retrait, `sync` remettait toutes les dalles en gris et replantait au hasard → les dalles qui restent gardent place et allure, celle qui part redevient grise sur place et éteint sa couleur en 760 ms (`tOut`) ; départ 22,97/49,19 → 0,94/4,25. **Esquille** : plus d'onde — chaque éclat a son retard et sa direction tirés de sa clé ; la dalle neuve prend sa couleur tout de suite (plus de blanc). **Bobinette** : relâchement local à 2 pas, retissage 700 ms, retard selon la distance (≤ 1,5 s), la couleur coule sur le fil, et un éclat vif de la palette à la tête de chaque fil qui se tire ; 240–290 arcs à l'arrivée, 1 plusieurs fois. **Studio** : aperçus Halin et Ritournelle semés comme une vraie Toile (≈ 21 cellules, poids variés). **Cercle** : la Toile de démonstration montre les treize mondes (décision v34 « six payants » renversée par Tom), une part égale par monde, une parole de chaque nature. **Madrure** : `couvre` grossissait l'œil jusqu'à couvrir le champ → posé dans sa boîte ; couleurs exactes (pas de rampe Q30 : elle fondait les strates, un Chiche sortait en disque uni) ; trait sombre tout autour. |
| 25 sept. | **Lot v54 — mouvements : Halin synchrone, Pochade/Touffe adoucis, Bobinette local ; liseré de la page + ; vérification du trait** (sauvegarde `app-avant-v54.html`) | — | **Halin** : la dalle naissait par une mise à l'échelle à elle (800 ms) pendant que ses jours suivaient les graines → elle naît PAR LA MÊME FRONTIÈRE que ses jours (`_halArr` dans `_halFront`), bornée côté bord par un disque qui grandit ; au départ ses voisines visent leur place finale tout de suite (relax : une dalle qui part ne pousse plus, `RD.douce`) ; rebond d'impact retiré. **Pochade, Touffe** : premier écart mesuré 6,7 et 28,2 (puis ~1 et ~4) — la dalle neuve PREND LA PLACE de la cellule grise (même rang, lieu, poids, allure) et le pas monte en 300 ms (`_amo`) ; premier écart 0,04 et 0,24. **Bobinette** : 790 arcs retissés par plantation (116 plusieurs fois), 556 différents au repos dont 358 à plus de 3 pas — chaque graine se redistribuait. → relâchement LOCAL (voisines à 1,25 pas) pendant la transition et 4 s après, état final calculé une fois par transition, les graines y vont, la trame s'y lit ; retissage retardé selon la distance à la dalle, du bout tourné vers elle ; couleur fondue sur place pour un même arc, sans instant vide. Mesuré : 197 arcs à l'arrivée (1,5 pas médian, 3,1 max), 144 au départ, 10 plusieurs fois. Sondes `bob_repos.py`, `bob_mesure.py`. **Page +** : filet crème 0,8 px sous le début du trait, en sombre, trois natures, le long du bord du ruban effilé. **Vérifié** : un Promi et un Chiche envoyés — l'émetteur trace sa moitié (0 → 195), le destinataire la sienne (l'instant : « X vient de tracer sa moitié. Le dessin existe. ») ; une Nuée se lance d'un trait entier. |
| 25 sept. | **Lot v53 — le vert de célébration retiré ; point 1 : les bugs d'affichage** (sauvegarde `app-avant-v53.html`) | — | **Célébration abandonnée** (Tom : « la célébration, c'est le mouvement lui-même ») : `_celLit`, `_celebre`, `s.cel`, `Rhal.cellule` retirés ; la page `celebration-mondes.html` montre l'arrivée et le retrait. **Bulles de Halin** : mesuré 18 bulles qui SAUTAIENT (apparition/disparition à pleine taille, seuils francs, clé qui change) → mémoire de la taille affichée par bulle, rejointe en ~0,3 s, taille propre lissée aussi, seuil de place adouci ; la boucle tourne tant qu'une bulle n'a pas rejoint sa taille (`window._mondeEncore`, remis à zéro avant chaque monde). Juge `sauvegardes/transitions-v43/hal_pops.py` : 24 sauts sans lissage, 0 avec. **Arrivée au bord** : Halin et Ritournelle faisaient grandir la dalle depuis le centre de sa cellule, HORS de l'écran pour une dalle au bord (la cellule va jusqu'à la borne) → elle grandit depuis le centre de sa partie VISIBLE ; au repos rien ne change. Esquille, Bobinette, Madrure : aucun défaut propre au bord dans les films (`bord_film.py`) ; Esquille passe par un blanc sur ses grands éclats à l'arrivée, gardé pour le point 3. |
| 24 sept. | **Lot v52 — la célébration épouse la dalle ; le rappel du compte ; l'achat sans compte** (sauvegarde `app-avant-v52.html`) | — | **Célébration** (rejet de la v51, cadre approximatif) : avant d'effacer, la Toile relit son image précédente autour de la dalle neuve ; sa matière dans sa cellule, REFERMÉE sur ses propres vides dans les mondes à trame (Braille, Tesselle, Taille-douce, Houle, Buvard, Touffe, Bobinette), donne sa silhouette exacte ; un liseré #8FE08F de 2,6 px la cerne, posé en calque SOUS la matière (§4), pulse (380 → 700 → tient → 1 050 → 1 750 ms). Demi-résolution : WebKit 17 ms/image pendant la célébration (Halin, Braille), Houle p90 26 contre 20. Rien au mouvement. Buvard : aucun fond visible, aucun liseré. **Rappel du compte** : 142 au lieu de 156 (14 px sous le plateau, l'écart des pilules des Réglages) ; revient après chaque « Plus tard », 5/10/20 paroles ou 3/7/14 jours. **Achat sans compte** (`lot-ACHAT-SANS-COMPTE`, posé tôt) : sur #buyYear, #buyMonth, #stLockBuy, sans compte → panneau « Avant d’acheter » (perte explicite, « Acheter sans compte »), puis après l'achat « Garder ton achat ». Mots à valider, Q326. |
| 24 sept. | **Lot v51 — la célébration dans l'app, les treize mondes ; les bulles de Halin épousent l'espace** (sauvegarde `app-avant-v51.html`) | — | **Célébration** (`_celebre`, boucle de la Toile ; le voile v47 est retiré) : à la plantation (`s.cel`, posé par addP/addPromi/addMember — jamais au chargement), l'amande #8FE08F en APLAT sous la matière, qui grandit avec la dalle ; monte 380→700 ms, TIENT le vert exact à opacité 1 jusqu'à 1 050 ms, s'efface à 1 750. Halin déclare sa cellule (`RD.cellule`) ; les autres mondes : une bande le long du bord de la cellule pondérée (la cellule entière faisait de gros aplats à travers les mondes clairsemés). Mesuré : pixels #8FE08F exacts dans 12 mondes sur 13 — **Buvard (pixel) : 0, il n'a pas de jours**. Page `celebration-mondes.html` : la vraie app, plantation et retrait en boucle, monde par monde. **Bulles de Halin** : triangle dont chaque côté est parallèle au coin arrondi qui lui fait face, à un jeu fixe — une dalle convexe est tout entière de l'autre côté, la bulle ne peut pas la toucher ; seulement là où la jonction a de la place (rayon inscrit > 0,22 jour), une sur trois ; pilules très rares dans les jours larges. Moodboard aligné (même courbe, mêmes bulles). |
| 24 sept. | **Lot v50 — Halin (nom et clé), la vie et la douceur ; la célébration en aplat** (sauvegardes `app-avant-v50.html`, `moodboard-celebration-avant-v50.html`, `redteam_decoupe-avant-v50.py`) | — | Clé et code renommés `halin` (`promi_monde` n'est jamais relu : rien à migrer). Dalles de tailles différentes (écart de poids tiré de la clé, ±0,16 u) ; jours inégaux (0,72–1,28, tirés des clés du couple). Mouvement : pas de poussée à l'arrivée, ressort 6,2/5,2 rad/s, retrait 900 ms qui va au bout, impact ramené à 0,6 % (`RD.halin` : douce, omx, omw, partDur — le moteur ne change que pour Halin). Bulles : petits triangles arrondis dans une jonction sur trois, rétrécis jusqu'à tenir dans l'espace libre (sous 55 % : aucune) ; rares bulles dans les jours. Moodboard : le code de Rhal recopié, l'amande en APLAT sur les jours qui bordent la dalle neuve, qui grandit avec elle (380 → 1 700 ms). Mesuré : aucun saut (Chromium, WebKit), 16,7 ms. **Juge réécrit** : `redteam_decoupe` H repérait l'Aura au nom de l'écran ; l'Aura se bâtit aussi pendant l'export du Folio (la Pelote, « Ce que tu as tenu ») → d'où le rouge intermittent. Il la repère maintenant au peintre ; prouvé sur une sonde (Index en plantation : pris, 62 appels). La célébration n'est toujours pas dans l'app. |
| 24 sept. | **Lot v49 — Halin (ex-Cabochon) repris ; la célébration redessinée au moodboard** (sauvegardes `app-avant-v49.html`, `moodboard-celebration-avant-v49.html`) | — | **Retrait** : la frontière avec la dalle qui part cède jusqu'au bout (avant : bornée à 6 %, puis saut à 620 ms) ; **impact** : rebond de 2 % en 220 ms à la rencontre. **Bulles** taillées dans l'espace libre mesuré par rayons contre les contours arrondis — jamais tronquées, elles épousent l'angle ; jonctions 1/2, jours 1/6 ; elles se retirent quand leurs dalles bougent. **Moodboard** : le code de l'app recopié tel quel ; l'amande #8FE08F part du contour de la dalle neuve (pur à la source, 20 % au loin, 900 ms), 40 marches composées exactement (plus de cibles). Mesuré : aucun saut au départ (Chromium et WebKit), 16,7 ms les deux moteurs. La célébration n'est PAS encore dans l'app : elle attend Tom sur la nouvelle forme. |
| 24 sept. | **Lot v48 — Cabochon, treizième monde (gratuit) ; la célébration à 25 %** (sauvegarde `sauvegardes/app-avant-v48.html`) | — | **Cabochon** (`Rcab`, bloc lot-V32-MONDES) : le dessin du moodboard figé — cellules pondérées arrondies (rayon 0,17 u), jour 0,09 u où se voit le fond, une couleur par dalle ; monde contenu, famille des neufs (une cellule par parole) ; naît de rien / se retire ; avant-dernier des gratuits (avant Esquille). Nom proposé, à valider (Q325). Mesuré : 60 i/s Chromium et WebKit, aucun saut, repos identique · moodboard : B 10 · C 16 · **D 25 %** · repère D ×3. **+ Les bulles (Tom, en route)** : une jonction sur trois porte une goutte en triangle très arrondi, tournée vers ses trois jours ; un jour sur huit porte une bulle en œuf, couchée dans son sens ; tirage par les clés des dalles voisines (jamais leur position), couleur d'une voisine, jamais dans une dalle seule. Mesuré : 16,7 ms Chromium et WebKit, aucun saut, découpe 0 (sauvegarde `app-avant-v48-bulles.html`). |
| 24 sept. | **Lot v47 — le clignotement, la Toile plein écran, Esquille frémit, le nom du Studio, la célébration en essai** (sauvegarde `sauvegardes/app-avant-v47.html`) | — | **Clignotement** : le S de RÉGLAGES et le R de PARTAGER ne clignotaient PAS (4 règles `opacity:1!important` écrasaient `promiBlink`) — mesuré au rendu : i 165↔112 · S 162↔108 · R 162↔108 (sombre) · **défaut = plein écran** (`_zDef` ≥ 1) · **Esquille** : sans poussée (la dalle naît à sa taille), plaque découpée sur l'ÉQUILIBRE de la Toile (point fixe de relax) — une seule recomposition, cassure 160 ms, 0,96 / 0,02 rad ; plus de saut · **Studio** : « Esquille / en / Ingénu » (Atkinson 400, 22) · **célébration** : voile amande sous la matière selon le mouvement, derrière `window._celebration` (ÉTEINTE), `moodboard-celebration.html` (4 téléphones : sans · 6 · 10 · 16 %) — à trancher par Tom avant intégration. |
| 24 sept. | **Lot v46 — le É de NUÉE, les titres longs, l'élision à la frappe, Esquille adouci, le zoom** (sauvegardes `app-avant-v46.html`, `app-avant-v46-zoom-mondes.html`, juge `sauvegardes/redteam_zoom-avant-v46.py`) | — | **É** : deux propriétaires réécrivaient « Nuée » (`cotes` et `accorde`, qui lisait « NuE’e » comme faux) ; sonde 12 écrans : 0 É fautif · **titres longs** : la phrase de la page + garde sa taille, seuls « de / d’ » + la pastille rapetissent (2 lignes, 3, puis points de suite ; place réservée au pinceau) ; fiche : 2 → 3 lignes puis points de suite (le titre entier reste dans la promesse) · **élision** à chaque touche (`_promiElide`) · **Esquille** : cassure 250 ms, 0,9 / 0,05 rad / 0,07 u · **zoom** : pincement en coordonnées de la Toile, élastique, élan, ressort sur le temps ; ZMIN 0,72 (Toile entière, encarts effacés), ZMAX 5 ; persiste ; défaut à la création / suppression / fermeture ; défaut(n) ; double toucher partout (fiche après 260 ms) · **quatre anciens mondes n'avaient jamais zoomé** : Touffe, Éclisse (vue ignorée), Buvard, Tesselle (grille à l'échelle de l'écran) — corrigés, identiques à l'échelle 1 · juges : `redteam_zoom` réécrit (16/16 ; 6/16 sur v45), `redteam_titres_longs` neuf (14/14). |
| 24 sept. | **Lot v45 — les quatre mondes selon le PDF** (sauvegarde `sauvegardes/app-avant-v45.html`) | — | Esquille : arbre de cassures, promesse ≫ matière · ampleur des paroles (quatre neufs) · Bobinette : fils retissés · Madrure : un œil par nœud, dalle = l'œil, onde GPU (WebGL2, repli CPU) · comptes vérifiés · CONTRAT-MONDE §15.11. |
| 24 sept. | **Lot v44 — le saut WebKit, redteam_toile, le mouvement jusqu'au bout, Esquille** (sauvegarde `sauvegardes/app-avant-v44.html`, juge `sauvegardes/redteam_toile-avant-v44.py`) | — | Saut WebKit : `lot-CERCLE-TOILE` sans `requestIdleCallback` sous Safari — tranche seulement Toile au repos · `redteam_toile` au niveau de la composition (`window._renduComp`), 3/3 stable, prouvé sur deux défauts · ressort critique sur le temps réel (quatre neufs) · Ritournelle : plus de saut (départ, première image) · Esquille : la plaque se casse · au repos identique au pixel · CONTRAT-MONDE §15.10. |
| 24 sept. | **Lot v43 — transitions : l'infrastructure et Ritournelle** (sauvegarde `sauvegardes/app-avant-v43.html`) | — | Moteur : `_trans` (arrivée, départ), `env.trans` sur la Toile vivante seule, `transDur`, graine `part` au départ (seulement si le monde déclare `transDur`) — CONTRAT-MONDE §1 amendé, §15.9 · Ritournelle : doigts hors écran, langues tirées, strates en retard, ressort · coût nul mesuré (Chromium ×1 16,7 · WebKit 17 · ×4 = v42) · Batteries : decoupe 0 ×2 · toile 17 · Nuée-dalle 38 · dalle figée 4 · zoom 16 · aperçus 10. Ouvert : saut WebKit à la 1re plantation (antérieur). |
| 24 sept. | **Clôture de session** | `07822524…` | Esquille : gratuit, net — rien à corriger (Tom). Ordre des chantiers décidé : performance (Touffe, Gravure, Madrure, Bobinette) puis transitions des mondes neufs. Point de reprise : mémoire `point-de-reprise-24-sept.md`. |
| 24 sept. | **Lot v37 — l'ordre du Studio, l'aperçu de Madrure** | `07822524…` | Rail : gratuits puis Esquille, puis Madrure, Ritournelle, Bobinette, Éclisse, Taille-douce, Houle · aperçu de Madrure : cinq nœuds (lignes, presque vide) · Toile du Studio : déjà régénérée à chaque ouverture (mesuré, 3 compositions sur 3) · Esquille au Studio en gratuit : net, les trois autres floutés (capture) — question posée à Tom · **releve-design refigé** (titres en capitales validés) · aperçus 10 · Studio 13 · design ✅. |
| 24 sept. | **Lots v35–v36 — le semis des anciens rétabli, les titres en capitales, les filets adoucis** (sauvegardes `app-avant-v35.html`, `app-avant-v36.html`) | `0a29349e…` | **Semis** : les huit anciens retrouvent le semis constant et le `sync` d'origine, les quatre neufs gardent le semis qui grandit — incohérence assumée (CLAUDE.md), ressemis au changement de famille · verrous vérifiés (Esquille net, 6 floutés) · **geste de couleur circulaire** (24 palettes atteignables) · Madrure sous Ingénu : onde en palette, dalles en nature · Ritournelle au Studio : strates variées · **titres en capitales PromiLate** sauf Le studio ; **É = E + apostrophe PromiLate** (lot-V35-E-ACCENT, sûr : une passe par image, plafond par nœud — la 1re écriture bouclait, redteam_ecrans bloqué 2 h 46) · **titres rétrécis à l'échelle ≠ 1** (ajusteTitres mélangeait deux unités : 23 px au lieu de 35 à 0,72) · **filets** des disques, de l'Aura et sous le trait : crème à 55 % (`_FILET_DOUX`), liseré 0,8 px peint AVANT le trait, seulement sous le tracé, sous la flèche · liseré à droite du trait des cartes du fil d'une Nuée (sombre seulement) · Batteries : decoupe 0 ×2 · toile 17 · zoom 16 · dalle figée 4 · aperçus 10 · Studio 13 · écrans 150 · vide 61 · accueil 22 · Nuée-dalle 38 · Nuée 0 écart · repérage 16 · verbe 6 · gens 38 · tuiles 64 · tokens 46 · air ✅ 512 · aura ✅ · design : 10 écarts, tous le mot de nature de la fiche en capitales (demandé, NON refigé). |
| 23 sept. | **Lot v34 — le semis grandit avec les promesses, tout suit le Studio sauf l'Aura** (sauvegarde `sauvegardes/app-avant-v34.html`) | `ee9b9791…` | **Semis** : 68 graines fixes → une par promesse et par Nuée (8 · 22 · 42 pour 6 · 20 · 40), vue entière, Toile vide = semis du §10.6 · **unité de matière fixe** (`env.uMat`) pour Esquille ×0,5, Bobinette ×1,07, Madrure ×1,38, calée côte à côte sur le PDF ; Esquille casse un semis de matière et se recolore (cassure gardée) ; Madrure bosses bornées, **sous Ingénu** onde crème + dalles en nature (Q315) · **tout suit le Studio sauf l'Aura** (défaut du moteur, cartes, fiche personne, petite Toile de Nuée, `_ingenuRampe`) · dalles : bord de la Toile net, Ritournelle bute sur les bords, rampe Q30 d'une dalle uniforme, page + préfère une cellule intérieure · écran qui vend : « Six mondes de plus », prix 36 px sur une ligne ; Toile du Cercle = six payants · bandeau « Garder ta Toile » à 156 · `hit()` vide hors Toile (Q212) · Pelote : rampe sombre 0,85 → 1,4 · juges réécrits : decoupe H, dalle_figee D (prouvé : 10 prises sur la version fautive) · Batteries : decoupe 0 ×5 · toile 17 · zoom 16 · dalle figée 4 · aperçus 10 · Studio 13 · écrans 150 · vide 61 · accueil 22 · Nuée-dalle 38 · repérage 16 · verbe 6 · gens 38 · tuiles 64 · tokens 46 · design ✅ · air ✅ · aura ✅ (2ᵉ passage : parité clair, Q297 connu). |
| 23 sept. | **Lot v33 — les décisions de Tom sur les mondes neufs** (sauvegarde `sauvegardes/app-avant-v33.html`) | `ad369e08…` | Esquille gratuit, Bobinette/Ritournelle/Madrure au Cercle (six payants) · **renommage des libellés** (clés inchangées) : Pochade, Tesselle, Buvard, Houle, Taille-douce, Éclisse — Studio, onboarding, écran qui vend · descriptions des quatre neufs · **Madrure par tranches** (générateur `_madGen`) : pire image à la plantation ×1 100 ms · ×4 450 ms (Gravure 67 · 300 ; avant 240 · 1 360–1 760 d'un bloc) · **encre des libellés sur ce qui est peint dessous** (`RD.madrure.sous`) · CLAUDE.md §8 (signature de cache sur un état qui bouge) · Q315 proposition, Q317 (six noms = 466 px sur 291) · Batteries : decoupe 0 ×5 · toile 17 · zoom 16 · Studio 13 · aperçus 10 · dalle figée 4 · écrans 150 · vide 61 · tokens 46 · design ✅ · air ✅ 510 paires · aura 1 écart : parité clair (Δlum médiane 48,0 / 42,9 contre 76,7 / 54,3), défaut connu Q297 pris à ce passage. |
| 23 sept. | **Lot v32 — Esquille, Bobinette, Ritournelle, Madrure intégrés** (sauvegarde `sauvegardes/app-avant-v32.html`) | `cd70c8a5…` | Bloc `lot-V32-MONDES` = `promi-mondes.js` + cinq retouches (repos, signature ½ px, cache de Madrure sans reconstruction pendant que le semis bouge — 25 → 1 construction par plantation, `boite()`, `env.cible`) ; environnement à accesseurs, `TH`, `RD`, dalle seule `_dalleNeuve`, toucher sur la dalle peinte, `Toile.natureDalle/contourDalle` ; Studio : rail, noms (gratuits, Q314) · **défaut antérieur corrigé** : l'Aura et la fiche d'une personne étiraient une dalle rendue sous sa boîte (`width:auto!important`, jusqu'à 4,9 % sur Encre) — cotes en ligne `important` · CONTRAT-MONDE §15, CHANTIERS, Q314–Q316 · Batteries : decoupe 0 ×5 configurations (option `--monde=`) · toile 17 · zoom 16 · dalle figée 4 · aperçus 10 · Studio 13 · repérage 16 · Nuée-dalle 38 · écrans 150 · vide 61 · tokens 46 · design ✅ · aura ✅. |
| 23 sept. | **Lot v31 — les réponses au banc des mondes neufs, `Toile.cle()`, le banc au dessin forcé** (sauvegarde `sauvegardes/app-avant-v31.html`) | `8f252549…` | **`Toile.cle()` / `cleUnite()`** (bloc `lot-V31-CLE`, hors moteur) : tirée de `promi_graine`, stable au rechargement et après plantation + sync · **CONTRAT-MONDE §12 ter** : bords droits/hyperboliques jamais ondulés (flèche max 0,94 / 4,27 px, mesuré), `curPAL()`, rampe v29 (dalles seulement), exception Madrure, clé ; **le banc ne comptait que le calcul** — au dessin forcé Touffe 62 ms, Gravure 39 (50 par image), Sillons 26, Pixel 21, Encre 15 ; trois mondes tiennent 16,7 ms à l'écran · renommage : clés gardées (Q313) · fond de Toile : dette à part (CHANTIERS). |
| 23 sept. | **Lot v30 — les voisines dans cinq mondes, le monde de plantation partout, le terrain des mondes neufs** (sauvegarde `sauvegardes/app-avant-v30.html`) | `fc42a961…` | **Index spatial exact** `_grilleProp` (0 écart sur 300 000 points) dans Pixel, Braille, Mosaïque, Gravure, Sillons — Toile ×1 : Gravure 440 → 26 ms, Pixel 72 → 14 ; ×4 : Gravure 1 944 → 120, Pixel 292 → 77 (encore > 50) · **monde de plantation dans le moteur** (défaut de `dalleTrame`), `courant` déclaré par la page + et le Studio · **`redteam_decoupe` famille H · monde** : 0 prise ; prouvée sur la règle retirée (434 dalles, 6 lignes) · **CONTRAT-MONDE** : rampes de matière des huit + `TH` obligatoire (§4 bis), fond de la Toile (§4 ter, quatre chemins divergents), renommage (§12 bis : 175 clés / 60 lignes, 33 libellés / 12 lignes, sauvegardes à migrer) · **releve-aura réécrit** (6 bis : la référence « monde courant » passe le monde exprès ; original `sauvegardes/releve-aura-avant-v30.py`) · Batteries : design ✅ · écrans 150 · Toile 17 · zoom 16 · aperçus 10 · Studio 13 · dalle figée 4 · repérage 16 · Nuée-dalle 38 · Nuée 0 · champ 32 · tonsurton 26 · vide 61 · accueil 22 · verbe 6 · gens 38 ×3 (36/38 une fois en série, non reproduit) · partage 42 · S1 S3 S4 S5 0 · air ✅ · aura : parité clair/sombre (aléatoire connu, Q297) · Q312. |
| 23 sept. | **Lot v29 — la dette de la découpe soldée, les deux ajouts au moteur, Q310 appliqué** (sauvegarde `sauvegardes/app-avant-v29.html`, CLAUDE.md `sauvegardes/CLAUDE-avant-v29.md`) | `f5ae7f6e…` | **Feu vert de Tom** : `UK` (pas des cinq mondes à trame en unité relative ; Toile inchangée à UK = 1) et `dalleTrame(…, opts)` (`rampe` Q30/Q297, `decale` ch. 59, `donnees` Pelote), le moteur DÉCLARE ce qu'il a peint (`__dalleInfo`) · un seul poseur `_poseDalle` / `_rendDalle` / `_poseUn` (bloc `lot-V29-DALLE`) : rendue à la taille finale, posée 1:1 · **les 24 lignes de la dette + 9 appelants non vus + famille G (affichage CSS, 2 prises) → `decoupe-dette.json` vide**, 9 familles à 0 · **les 8 photos `PROMI_DALLES` retirées (411 Ko)** · Touffe : cœur = sa couleur vers l'encre (plus `#DD4D23`) · **perf** : masque de `dalleTrame` limité aux voisines qui peuvent gagner, trié (exact) — dalle de 200 px 20–48 ms à ×1 (Pixel 201 → 48) ; Gravure 440 ms / 1,9 s par Toile, intenable, à revoir (Q311) · **pris en route et corrigé** : `renderTo` peignait à la densité de la Toile (export Ma Toile petit, aperçu zoomé ×1,23) ; cache du poseur à clé complète (gens 30/32 → 38/38) ; boucle d'ajustement ≤ 2 passes (verbe 3/6 → 6/6 ×4) ; la passe `lot-V10-SOMBRE` ne défait plus qu'elle-même (S1 : l'à-qui du Chiche à relever) · **Q310 appliqué** : LANCÉ = en cours, textes tenu de l'instant en clair `#00341A`, Gilbert 700, crème unique · **S1 224 → 0, S5 67 → 0** · voir Q311. |
| 23 sept. | **Lot v28 — le contrat d'un monde, la découpe interdite, S1 et S5 repris** (aucune modification d'`app.html`) | `9f68a09e…` inchangé | **`CONTRAT-MONDE.md`** écrit pour les quatre mondes à venir (signature, cellule implicite, `cOf` et la préséance, échelle `k` et l'unité `u`, monde figé, déterminisme par clé stable, budget MESURÉ ×1/×4, Gravure commenté, dérives des huit : Touffe peint `#DD4D23`, cinq mondes à pas en px, Gravure 499 ms par Toile) · **`redteam_decoupe.py`** : six familles piégées à l'exécution, 19 écrans × 2 thèmes, prouvé sur une copie à cinq défauts (5/5 pris à leur ligne) ; **dette figée à sa naissance : 24 lignes, ~2 100 appels** — toutes les dalles hors Toile sont redimensionnées, Q30/Q297 retouchent les pixels, `promiTrame` pose des photos webp ; échoue sur toute ligne nouvelle · **`releve-S1` 224 → 7, `releve-S5` 67 → 4**, prouvés contre une sonde ; restes = Q310 (sans décision) · Q308 bis (export `#120E05`, pois de Braille : tranché) · Q309 (feu vert moteur + budget à valider). |
| 22 sept. | **Lot v27 — un choix explicite prime sur la nature · le piège `.show` nommé** (sauvegarde `sauvegardes/app-avant-v27.html`) | `9f68a09e…` | **Q307 tranché par Tom** : sous Ingénu, un TON DE PALETTE choisi à la main passe devant la nature, comme le code libre. Ce qui manquait n'était pas une règle mais une TRACE — `p.dalle={ci,lit}` s'écrit pareil à la plantation et au réglage. Les **quatre** écritures d'un choix portent `choisi:1`, `_dalleFigee` le descend à la graine, `cOf` le lit. Ordre de préséance complet : code libre → ton choisi → nature (Ingénu) → palette · **`redteam_cercle_couleur` 26/34 → 28/34**, la cible ; les 6 restants sont les contrats « Réglages », la dette d'avant v17 · **CLAUDE.md §8 : le piège `.show` est nommé** — `#studioScreen` et `#auraScreen` ne perdent jamais la classe, troisième fois qu'elle casse quelque chose (Pelote, Noyaux, semis du Studio) · **« glisse pour changer de monde » gardée telle quelle** (Tom : elle meurt après le premier geste, c'est bien) · Q307 bis. |
| 22 sept. | **Lot v26 — Braille : le fond, pas les pois** (sauvegarde `sauvegardes/app-avant-v26.html`) | `9c52d552…` | **Mesuré d'abord** : pas 18 px, pois 12 px, **34,9 % de couverture — identiques** entre l'aperçu et la vraie Toile, et inchangés depuis le lot v14 (22,8 % de pixels froids aujourd'hui, 22,4 avant v17, 21,7 avant v14). **Aucune régression sur le dessin** · **La seule différence : le FOND** — `#120E05` (encre profonde) dans l'aperçu contre `#201908` (le fond du mode) sur la vraie Toile. Invisible sur Encre/Pixel/Mosaïque qui couvrent tout ; sur Braille et Touffe, **les deux tiers de l'écran sont ce fond** · ⚠ **TROIS fonctions le peignaient** (`preview`, `repaintWorld`, `repaint`) — corriger les deux premières ne changeait RIEN à la mesure, `repaint` repasse à chaque frémissement ; §7, un seul propriétaire : **`Toile.fondToile(clair)`** · Après : fond `[32,25,8]` contre `[34,25,8]` sur la vraie Toile, contraste pois ↔ fond **Δlum 161,2** · Contrat neuf **`redteam_apercus` E**, rouge sur la version d'avant, **10/10** · **Non fait, dit** : le fond de l'image exportée (`renderSeal`) garde `#120E05` ; et grossir les pois serait le MOTEUR (`Rbra`), donc Braille partout · Q308. |
| 22 sept. | **Lot v25 — le Studio avait perdu sa Toile depuis le lot v17** (sauvegarde `sauvegardes/app-avant-v25.html`) | `6e9d1380…` | **Ce n'était PAS v24** : bissection sur huit sauvegardes — 47,9 % de pixels colorés avant le lot v17, **11,4 % après**, et 13,6 % encore en v24 · **Cause : l'exception Ingénu.** `cOf` rend le crème dalle quand une cellule n'a pas de nature — juste pour la vraie Toile, faux pour un APERÇU, qui n'a aucune parole : ses 72 cellules tombaient toutes sur le crème. Le canevas était PEINT (13 167 px), d'où l'invisibilité aux juges · **Deux correctifs** : ① l'aperçu se déclare (`s.apercu`) et `cOf` lui rend la palette — ⚠ le drapeau se perdait dans la copie à champs énumérés de `pcv.__c` ; ② `buildStudio` peint `#stBg` sans `_shAllColored` (~13 cellules, le défaut de Q132) et le semis juste était accroché à l'observateur de `.show`, **que `#studioScreen` ne perd jamais** — donc toutes les ouvertures après la première étaient cassées ; `poseToile` a désormais le dernier mot · **Juge neuf `redteam_apercus.py`** (8 contrats × 2 thèmes, plancher par monde relevé sur la référence) : **0/8 sur la version cassée, 8/8 sur celle-ci** ; ⚠ sa première écriture passait au vert sur l'écran mort — « max−min > 40 » compte les crèmes ; avec la teinte, la version cassée tombe à 3,6 % · **« glisse pour changer de monde » : pas un défaut** — mesurée visible à y 776, c'est « l'invite qui meurt », remplacée à sa place par les huit points · Batteries : design ✅ · toile 17 · studio_geste 13 · apercus 8 · Q307. |
| 22 sept. | **Lot v24 — trois polices, et trois seulement** (sauvegarde `sauvegardes/app-avant-v24.html`, CLAUDE.md `sauvegardes/CLAUDE-avant-v24.md`) | `fe3715e0…` | **Bricolage et Apfel retirées** sur décision de Tom (« en Swift elles n'existeront pas ») — 131,8 Ko, **161,9 Ko avec Fraunces** ; piles, `NOTRE`, table de report, `PILE`, jeu, Swift et crédits suivis ; il ne reste que **Gilbert, Atkinson, PromiLate** · **Les trois caractères qu'elles peignaient, regardés et mesurés** (captures avant/après) : « CHOISIR → » +51 % de chasse, ‹ › +84 %, › +81 % — mais la HAUTEUR ne gagne que **9 %**, et le glyphe passe de 82-84 % à **89-92 %** de la capitale voisine. **Aucune cote reprise** : les chevrons étaient sous-dimensionnés. Seule boîte qui bouge : « CHOISIR → » 124,1 → 129,6 à x 42 · **CLAUDE.md §6 corrigé** — la note qui gardait ces faces « pour ✕ ✦ ● » était fausse : ✕ ✦ ● viennent déjà du système (Zapf Dingbats, 40 glyphes) ; dix faces → **cinq** · `releve-design` 136 écarts, **136/136 des `fontFamily`** (la queue de la pile, première famille identique partout) — voulus, référence **refigée** · Batteries : air ✅ 510 paires · écrans 150 · S3 0 · S4 0 · vide 61 · champ 32 · tokens 46 · polices 0 absent · Q306. |
| 22 sept. | **Lot v23 — la bande retirée, Fraunces sortie, trois portes vers le compte, `releve-S4` remis à neuf** (sauvegarde `sauvegardes/app-avant-v23.html`) | `f67684ec…` | **La bande de lisibilité de l'onboarding est RETIRÉE** (Tom : « ça fait cheap, et c'était une erreur de ma part ») — A et B sont morts ; ce qui reste de v22 : l'encre sur les pastilles pastel, le contraste franc, et **la Toile qui se tait au rejeu** · **Les polices, MESURÉES au CDP** (polices de plateforme + nombre de glyphes, 11 écrans × 2 thèmes) : **Fraunces 0 glyphe** → retirée (2 faces, 30,1 Ko ; `--f-titre` → PromiLate ; table de report, canevas de signature, préchargement, crédits) ; ⚠ **Bricolage (60 glyphes : ‹ ›) et Apfel (6 : →) PEIGNENT ENCORE** — Gilbert et Atkinson n'ont pas ces caractères ; gardées, crédit OFL gardé, un mot suffit à les sortir (‹ › +80 %, → +50 % de chasse) · **Le panneau du compte a trois portes** : fin de l'onboarding, bandeau de rappel, et **« Garder ta Toile » aux Réglages** tant qu'aucun compte n'existe ; le rejeu ne le saute plus ; le bandeau PARAÎT (mesuré : 3 Promi, deux jours, après l'Aura) — juges **O21/O22**, prouvés rouges sur la version d'avant · **`releve-S4` : 106 → 0**, trié — 105 de juge en retard (palette et polices du 16-17 sept., PromiLate, Q281, recherche 278) et **1 vraie régression** : la passe « crème sur le sombre » ne défait jamais ce qu'elle pose, l'inline `!important` survit au changement de thème — le compte du Fil restait crème sur un plateau crème, **Δlum 0,0 → 201,1** ; le juge ouvrait aussi le Fil par `setView('fil')`, il passe par `#filBtn` · **Le panneau du compte appelé des Réglages prend le voile de l'app** (`.scrim`, noir 50 %) : il flottait au-dessus de la liste · Batteries : design ✅ · écrans 150 · tonsurton 26 · vide 61 · champ 32 · nuee 0 · air ✅ · accueil 22 · geste 13 · reperage 16 · S3 0 · **S4 0 (106 avant)** · onboarding 44 · tokens 46 · polices 0 absent · **dette antérieure, mesurée identique avant et après : `releve-S1` 224, `releve-S5` 67** (juges de la palette d'avant le 16 sept., comme S4 l'était) · Q305. |
| 22 sept. | **Lot v22 — B « la Toile se tait », l'encre sur le pastel, le rejeu sur Toile vide, deux transitions** (sauvegarde `sauvegardes/app-avant-lot-v22.html`) | `23b3ab96…` | **B par défaut** (bande du fond sous le texte, message de fin compris ; A retiré) · **contraste franc** : plus d'opacité réduite sur un texte ; la pastille-verbe à l'encre sur le pastel (onboarding ET page +) · **rejeu** : c'était lui (20 dalles) ; la Toile existante se tait, Nuées comprises, et revient au trait ou à la fermeture — O19 l'exige, prouvé contre v21 · **Studio et Partager** entraient en fondu (0,34 s) : pleine opacité à l'entrée ; le plateau de Partager glisse avec l'écran (recale image par image) · **défaut trouvé par releve-S3, venu de ma coupe v20** : la coupe ajoutait une ligne après le calcul des cotes — phrase et trait 32 px trop bas par intermittence ; cotes recalculées (3/3 à 0) · `releve-S4` : 106 écarts, **dette antérieure** (108 sur v20 et v21) — chantier proposé à part · Q304. |
| 22 sept. | **Lot v21 — transitions, latence, Fil, Pelote, lisibilité de l'onboarding** (sauvegarde `sauvegardes/app-avant-lot-v21.html`) | `2d1e5727…` | **Latence du + → nature : 550–1 040 ms → 107–135 ms** (causes : écran des tuiles intermédiaire, boucle de 150 ms, `arme()` et `natureCourante()` lisaient une géométrie et le texte de la phrase, le lot 5 remettait le choix 130 ms après chaque +) · **Transitions** (détecteur image par image au doigt + screencast) : ancien sélecteur Toile/Index RETIRÉ du HTML ; page + sans tuiles à l'ouverture ni ancien en-tête à la fermeture ; plateaux posés dès l'entrée (plus de titre nu ni de saut de 46 px aux Réglages) ; `s4` à l'ouverture (recherche du Fil) ; ancien titre de Partager ; fond du Studio vide ; aperçu de Partager à trois propriétaires (366/234/316) · **Fil** : l'entrée du journal dont le pid ne résout plus est reliée par son titre (la ligne sans dalle, 3e fois — prouvé : l'ancienne version reproduit le défaut) ; guillemets insécables ; cartes à 204 comme l'Index · **Index** : air titre → compte 22 à l'encre · **Onboarding** : le message reste (≥ 4 s + toucher) et dit « Le reste se découvre à ton rythme. » ; deux propositions de lisibilité (`planche-onboarding/lisibilite.html`, à choisir) · **Pelote** : le poil se couche là où on la touche et reste couché ; lisse à chaque ouverture ; 9 → 48 caresses · **Régression v20 trouvée et corrigée** : le Fil sortait vide au premier lancement (il était bâti pendant le vidage de l'onboarding) · Juges repris au niveau de la décision : onboarding (O20), S3 et air (exemples déterministes), ecrans (sélecteur retiré), aura (poil couché) · air refigé (Fil −11, Index −3 demandés ; page + : référence prise sur un tirage) · Batteries : onboarding 40 · accueil 22 · tuiles 64 · verbe 6 · phrase 6 · gens 38 · S3 0 · nuee 0 · nuee_entree 24 · vide 61 · écrans 150 · geste 13 · champ 32 · tokens 46 · studio_geste 13 · air ✅ · design ✅ · aura 0 · Q303. |
| 22 sept. | **Lot v20 — l'onboarding intégré, les exemples qui tournent, l'élision, le fil de Nuée** (sauvegarde `sauvegardes/app-avant-lot-v20.html`, `1079910d…` ; lot `sauvegardes/v20/lot-onb.html`) | `b6a1b161…` | **Onboarding** (`lot-ONB-V20`) : prénom → premier trait → la Toile, écran plein sur la vraie Toile vide ; phrase de la page + ; le trait d'une fiche par défaut (`_onde`) ; la dalle naît sous le doigt et vole à sa cellule ; « Ça y est. » ; le compte après ; pas de tutoriel ; thème du téléphone ; rappel du compte en bandeau (3 Promi ou 2 jours) — `redteam_onboarding` **38/38** (7/38 sur la version d'avant) · **Exemples** (`lot-EXEMPLES-V20`) : listes de Tom, premier à la première ouverture, tirage ensuite, Nuée par catégorie ; la pastille d'un exemple long se COUPE en morceaux équilibrés au plancher de 28 (80/80 ≥ 28 px, 0 débordement) · **Élision** : règle de Tom, 32/32, un seul propriétaire `_promiElide` · **Le fil d'une Nuée** : `light()` sur un booléen levait une TypeError avalée — tout le poseur sautait dès qu'une carte était tenue (depuis v10) ; `recote` lisait la méta en plein vol — `redteam_nuee` **68 → 0** · **Studio** : curseur = dalle du monde en silhouette, grille centrée sans fondu · **Aura** : pastilles de légende 20 px, filet crème 1,4 · **Titres** : Partager 30 · Réglages 32 · Index 35 · L'aura 33 (bornés par ✕ FERMER) · Index centré à l'encre 15,5/16,5 · Batteries : onboarding 38 · nuee 0 · nuee_entree 24 · vide 61 · accueil 22 · S3 0 · verbe 6 · phrase 6 · tuiles 64 · gens 38 · tokens 46 · polices ✅ · champ 32 · écrans 150 · studio_geste 13 · design ✅ · aura 1 (Q297, aléatoire, antérieur) · **air 18 paires (page + : exemple long ; Index recentré) — NON refigé** · Q302. |
| 21 sept. | **Onboarding — juges en retard, juge neuf, planche** (aucune modification d'`app.html`) | `1079910d…` inchangé | **`releve-S3-page-plus`** repris au niveau des décisions (palette v7, PromiLate 29/15, Gilbert, NATTRAIT, Q221, verbe et barre de Nuée #291547) : **212 → 0**, prouvé contre une sonde (50 prises) · **`redteam_nuee`** repris pour les cartes qui grandissent à deux lignes (v16) et le trait brun encre (v7) : **94 → 68**, prouvé (12 prises) ; les **68 restants sont un vrai défaut** — le fil d'une Nuée ne suit plus la méta (502 attendu, 551/588 mesuré ; juste en v7, cassé depuis v10) : chantier proposé, pas corrigé · **`redteam_onboarding.py`** écrit, 19 contrats × 2 thèmes au vrai doigt : **7/38 sur la version d'aujourd'hui** (accueil touchable dessous, compte avant le trait, ni prénom ni trait) · **planche** `planche-onboarding/planche.html` : 8 cadres × 2 thèmes + un cadre vivant par thème, Toile/dalle/accueil rendus par l'app (`capture.py`), mesurée 0 défaut sur 112 textes · Q301. Originaux : `sauvegardes/*-avant-onboarding.py`. |
| 21 sept. | **Lot v19 — la rampe du Chiche, et les références figées** (sauvegarde `sauvegardes/app-avant-lot-v19.html`) | `1079910d…` | **Rampe du Chiche bornée** (Tom : « jamais près du terracotta, ΔE 25 minimum de #DD4D23, à toutes les tailles ») : elle passait par un rose poudré à ΔE 26,4 ; elle passe maintenant par un rose FROID — prune `#3A0F33` → `#A8457E` → rose `#FFB8D2` → clarté (teinte 345°). Minimum **ΔE 2000 = 28,9** sur la rampe et sur tout mélange de deux de ses points ; mesuré au rendu : Index **29,1** (pixel par pixel, bords compris, deux thèmes), et **28,5** sur les trois Chiche du jeu aux sept hauteurs de rampe de la Pelote · **`releve-design` et `redteam_air` FIGÉS** (Tom) — 142 éléments / 6 configurations, 497 paires / 38 écrans ; repassés après : ✅ aucun écart, ✅ air intact. Anciennes références : `sauvegardes/*-reference-avant-v19.json` · écrans 150 · `releve-aura` 1 (la parité clair/sombre, défaut aléatoire nommé, aucune île sous le plancher). |
| 21 sept. | **Lot v18 — la mention TENU, l'air de la ligne d'état, le filet des disques, Q297** (sauvegarde `sauvegardes/app-avant-lot-v18.html`) | `b3b68529…` | **Mention TENU en amande** (« TENUE », « TENU À DEUX · 3 AOÛT ») posée par le peintre de la fiche (une règle de feuille perdait contre la passe du sombre) · **Ligne d'état** : l'air à l'encre allait de 21 à 37,5 selon le JAMBAGE de la dernière ligne et les accents de l'état, pas le nombre de lignes → la cote compte les deux (`_jambageDernier`, `_accentHaut`) : **36,5 à 39** sur 18 fiches, deux thèmes · **Filet des disques** : 1 px, sur le seul bord extérieur de chaque segment, interrompu dans les écarts — `drawKRing`, `_filetsDisques` (éteint), SVG Aura/personne/aide, et l'anneau du + repeint en segments nets (plus de fondu, plus de contour continu) · **Q297** : recalage de la clarté sur une rampe de SA nature (trait → couleur → clarté ; pas `DALPAL`, qui faisait un Promi lilas) sur les cartes d'Index et du Fil (ΔE dalle/champ **15,3 à 24,2**, 11–12 avant) et les îles de la Pelote, où il REMPLACE la cession du chantier 59 (un Promi sortait kaki) ; hauteur de rampe choisie contre le sol tiré en sombre, fixe (1,8) en clair · **Q294** : « À bientôt », « Promi · 0.16 ». **Juges réécrits** : `redteam_ecrans` (le filet n'est pas un arc), `releve-aura` (arc à sa largeur + filet 1 px au bord extérieur, prouvé en v17 sur une sonde) — originaux `*-avant-v18.py`. **Batteries** : tokens 46 · écrans 150 · vide 61 · toile 17 · geste 13 · repérage 16 · tonsurton 26 · champ 32 · filets 0 · accueil 22 · dalle figée 4 · Nuée-dalle 38 · **releve-aura : 0 · 0 · 1 sur trois tirages** (le rouge restant est la PARITÉ clair/sombre, 60,8 contre 68,6 à 5 près — aucune île sous le plancher, ΔE ≥ 18 partout) · nuée 94 · air 29 (aucune paire neuve) · design 80 (mêmes causes qu'en v16). NON figés. |
| 21 sept. | **Lot v17 — Ingénu, l'icône, Marseille** (sauvegarde `sauvegardes/app-avant-lot-v17.html`, patch `sauvegardes/v16/patch_ingenu.py`) | `0f478cfd…` | **Ingénu** (ex-Avenant, clé `signal`) : dans cette palette seulement, la couleur d'une dalle dit sa nature — `cOf()` lit `s.nat` posé par `_dalleFigee` (Promi bleu, Chiche rose, Nuée lilas) ; les ~53 cellules colorées sans parole (73 colorées pour 18 paroles + 2 Nuées) passent au crème dalle ; un code libre du Cercle passe devant ; la couleur figée n'est pas effacée, elle revient hors d'Ingénu ; le sol de la Toile ne bouge pas. Exception au §4 écrite dans CLAUDE.md · **Icône des Réglages** : A, les deux curseurs (accueil + table des icônes) · **À propos** : « un week-end à Marseille ». **Coût mesuré, à trancher (Q297)** : sur les cartes d'Index/Fil, dalle et champ de la même nature → ΔE 11,0–12,0 (Promi, Chiche), sous le plancher de 15 ; sur la Pelote, une île de Promi à ΔE 9,2–14,9 selon le tirage du sol (`releve-aura` : 1 écart, 0 sur la version d'avant Ingénu). **Juge réécrit** : `releve-aura` — l'arc cerné du lot v16 (arc − 2,8 + filet crème à la largeur de l'arc), prouvé sur une sonde (12 prises), original `sauvegardes/releve-aura-avant-v16.py`. **Batteries** : toile 17 · dalle figée 4 · Nuée-dalle 38 · repérage 16 · accueil 22 · écrans 150 · tonsurton 26 · vide 61 · releve-aura 1 (ci-dessus). releve-design / redteam_air NON figés. |
| 21 sept. | **Lot v16 — les décisions de Tom sur l'audit, et les corrections** (sauvegarde `sauvegardes/app-avant-lot-v16.html`, patchs sous `assert` et bloc `lot-V16` dans `sauvegardes/v16/`) | `60a747c0…` | **Trait** : phrases en PromiLate CAPITALES 15 px, quatre reformulées faute de capitales accentuées (Q291) · **États en sombre** : trois valeurs exactes, filet crème 1,4 px dans chaque pastille, chaque arc (SVG de l'Aura et de la personne, canevas `drawKRing`) et les icônes de l'aide ; textes d'état crème ; **l'amande ne peint plus que la célébration** (trois propriétaires + une règle CSS passés à la crème) · **Réglages** : les cinq réglages du Cercle en sortent, la Langue sort (cinq langues sur six ne changeaient rien), « Se déconnecter », interrupteur des Notifications, « Vie privée », Compte, Légal = Conditions · Politique · À propos ; pages « Légal » (bientôt disponible) et « À propos » (texte de Tom, crédits Gilbert CC BY-SA 4.0 et Atkinson + OFL 1.1 intégrale dépliable, polices de secours, version) · **Suppressions** : « Supprimer ce Promi » ne faisait rien (un clic qui n'armait que `#actDel`) → confirmation + rangée distincte (terracotta, corbeille, sans pilule) ; « Annuler » 5 s après toute suppression (Promi, Nuée dissoute, photo) ; compte / données / tout effacer DIFFÉRÉS de 5 s · **Mots** : la Pelote, Le Studio, « navigateur » sorti, tutoiement (y compris le « vous » pluriel), « Revoir la présentation », « 2 JOURS »/« DEMAIN », « AVANT » dit une date, le nom « Ton » (champ taillé avant Gilbert), « première » · **Accents** : ils étaient ROGNÉS (boîte = hauteur du texte), l'encre déborde désormais ; « TENU À DEUX » identique · **Textes coupés** : fil d'une Nuée (la carte grandit, 2 lignes, points de suite), « Ce que tu as tenu » (2 lignes) · **Contrastes** : Chiche « Chiche »/« Plein »/tuile à l'encre, « ou le mois » en bouton trait · **Cercle** : « 39 € / an », ✕ dans son plateau (titre PromiLate, Toile descendue de 18), « LE CERCLE » identique (CERCLE lilas) · **Finitions** : Vie privée/Langue à 24 px, sans filets, titres PromiLate ; « L'aura » ; aide alignée ; zones de toucher 44 (✕ FERMER : 116 × 60 au bord du plateau, photo, i) ; état pressé `scale:.97` partout (jamais d'opacité ni de filtre sur une dalle) ; « garder de côté » sort d'un gardé de côté (il créait un doublon) · **Densité 1×** : trois appelants taillaient la Toile à ×2 en dur, ils prennent `Toile.vue().dpr` (code de la Toile intact). **Proposé, non posé** : palette par défaut (Q292, `planche-v16/PALETTE-DEFAUT.png`), icône des Réglages (Q293, `planche-v16/PICTOS-REGLAGES.png`). **Batteries** (série) : tokens 46 · polices 0 · écrans 150 · vide 61 · verbe 6 · champ 32 · tonsurton 26 · repérage 16 · accueil 22 · gens 38 · tuiles 64 · toile 17 · geste 13 · filets 0 · **air 29** (30 avant le lot, aucune paire neuve) · **nuée 94** (88 avant : +6 = les cartes du fil qui grandissent pour leurs deux lignes) · **releve-design 80** (62 avant : +18 = trait 15 px, ligne de fil 83, `-webkit-box`). **NON figés.** Juges réécrits au niveau de la décision : `releve-S3-page-plus`, `releve-S5-instant` (mots du trait). |
| 24 sept. | **Le partage de la Pelote : seule, ou dans Mon Folio** (sauvegarde `sauvegardes/app-avant-lot-v15.html`, `2530a1ba…`) | `51c0f543…` | **1 · LA PELOTE NE SE PARTAGE PLUS AVEC LA TOILE** (Tom : « on ne choisit pas entre A et B ») — `lot-V14-TOILE` vidé (Q289 caduque) ; sur Ma Toile la rangée DANS L'IMAGE sort (elle ne porte plus que La Pelote). ⚠ Ce bloc causait un défaut hors de son sujet : il retirait le `display:none` de l'invite du doigt dans TOUS les sujets — la bande « pince pour zoomer » barrait la dernière rangée du Folio (y 641, 317 × 33) · **2 · DANS MON FOLIO, LA PELOTE SE DÉPLACE AU DOIGT** : appui long **380 ms** doigt immobile (tolérance **8 px** : un doigt qui bouge avant ne prend rien), elle suit le doigt ×1,06, sa place vide suit la case visée, les dalles se rangent autour ; bornée à la dernière rangée utile (`ceil((n+4)/cols)−2`), plus de rangée vide. Cache des dalles le temps du geste (une recomposition coûtait ~130 ms). Géométrie publiée (`_plancheComp.bloc/grille`) · **3 · L'IMAGE PARTAGÉE EST L'APERÇU** — `shareExport` n'avait que `toile` et SINON `paintPreview` (une Toile) : partager le Folio ou la Pelote envoyait une Toile (écart à l'aperçu **172 et 194 niveaux** sur l'ancienne version, **4,5 et 0,6** maintenant). L'export compose à la taille de l'aperçu et peint à 3840 (sinon l'arrondi de la taille des titres réordonnait les cases) ; le mot-marque est relevé sur l'aperçu ; le canevas ne se multiplie plus par la densité (33 à 74 Mpx → **8,3**, sous le plafond iPhone de 16,7) ; le bouton Partager est rebranché (il tenait la fonction d'origine, aucune enveloppe ne l'atteignait). **Juge neuf** `redteam_pelote_partage.py` **42/42** au doigt (CDP), deux fonds ; sur la version d'avant **2/10** avant d'arrêter. **Batteries** (en série) : écrans **150** · toile **17** · geste **13** · vide **61**. **Vu, non pris :** à l'export un titre peut couper autrement qu'à l'aperçu (« récupérer les plants de tomat… ») ; les dalles de l'export sont agrandies ×6,8 depuis leur rendu natif (flou en 4K). `releve-design` et `redteam_air` **non figés**. |
| 13 sept. | **Cinq défauts vus à l'œil** (sauvegarde `sauvegardes/app-avant-lot-cinq-defauts.html`, `009de5e5…`) | `664d9ea1…` | Studio : « SOMBRE · AVEC TEXTE » à 649,5, 13 px (le plancher le posait après coup), air 18,5 / 17,5 à l'encre · pinceaux rangés hors `.pp` (écran des choix) · rond photo masqué sur `pp-choix` · aide de la page + cotée en `offsetHeight` (sous `.frame` mise à l'échelle elle remontait sur « avec qui ? ») · rangée des pinceaux = max(651, bas de l'aide + 13,5) — **chantier 62 clos** · `#nueePhrase` prend les creux de `#csPhrase` (pastilles 52 / 49) · ✕ de l'écran des choix rendu à la feuille (encre en ligne héritée) · `enteteLisible` ne juge pas un canevas non affiché · fiche : FERMER composite dès le HTML (double ✕ sur une Nuée ouverte à froid) · Nuée ouverte après une fiche : classe de nature, `#dpCorps` et rond photo retirés, `_fichePose` rappelée (depuis le disque « le potager » : titre du Promi, pas de fil) · « Peaufiner » d'une Nuée à 21 · pas de halo sur « Nuée » dans le plateau. Batteries en série : toutes vertes (design 0 · écrans 150 · 15 · 10 · 18 · 19 · toile 17 · geste 13 · verbe 6 · filets 0 · vide 61 · air 436 · champ 32 · nuée 24/0 · polices 0 · tonsurton 26). **Vu, non pris :** l'état d'une Nuée à 13 px à froid, 13,5 après une fiche ; « Plein » pris d'une Nuée pâle sur mauve. |
| 13 sept. | **Pinceaux au milieu, rangés pendant la saisie** (sauvegarde `sauvegardes/app-avant-lot-pinceaux-milieu.html`, `664d9ea1…`) | `29ee8530…` | Page + : la rangée se centre à l'encre entre le bas du texte au-dessus (aide −7, « GARDÉ DE CÔTÉ » −3, pastilles sur leur boîte) et « garder de côté » (+0,5) ou la barre (760) — mesuré : Promi 42,5 / 43 · Chiche 16,5 / 17 · Nuée 76 / 75 · gardé 46 / 46,5 · rangée masquée tant qu'un créneau est ouvert (`pp-ouvert`, ou `#nueeChoix` plein) · pour qu'elle revienne : Entrée referme le mot, toucher hors panneau et hors phrase referme une liste, et `closeAll` vide un panneau resté ouvert (il faisait ouvrir la Nuée suivante « en saisie ») · grille des personnes et « DÉJÀ PROMIS » dérivées du bas réel de la phrase (+32 / +30) — la grille recouvrait « avec qui ? » sur un Chiche · mot d'une pastille prise en crème (les trois natures, comme le verbe), trait gardé en teinte claire · état d'une Nuée posé à 13,5 par son propre peintre. `redteam_air` refigé (18 paires, exactement les deux écarts demandés ; ancienne référence : `sauvegardes/air-reference-avant-pinceaux-milieu.json`). |
| 13 sept. | **La saisie et les personnes** (sauvegarde `sauvegardes/app-avant-lot-saisie-personnes.html`, `29ee8530…`) | `e4c2d41a…` | `lot-GENS` : un seul choix des personnes (page + à qui · qui tu défies · avec qui · la Nuée ; Peaufiner de la page + et de la fiche : À QUI · À QUI JE LANCE · AVEC · MEMBRES) — toucher ajoute, croix retire, « + ajouter quelqu'un » collé en bas de la liste qui défile au-dessus de Peaufiner (rangées entières) · la Nuée ouverte compte comme un choix ouvert (trait au plancher, liste à 486) · plusieurs personnes = un disque chacune · « je me promets » sans « à qui » · `lot-CURSEUR` : barre qui clignote + « … » dans la pastille, « … » comme exemple de tout champ · exemples des créneaux (Q211, tournent d'une page + à l'autre) · rond photo reposé à l'ouverture d'une liste (Chiche 166 → 126) · ✕ FERMER du Peaufiner d'une Nuée = celui d'une fiche · Encre du Cercle posée sur son sol dans sa silhouette (la variation du moteur est le sol sous les ellipses à 90 %). Batteries en série : toutes vertes (+ pastilles 12 · photo 27 · superpo 0 · S2 0 · S3 0). |
| 13 sept. | **Accueil — audit et planches, sans intégration** | `e4c2d41a…` (inchangé) | `AUDIT-ACCUEIL.md` · `PLANCHE-ACCUEIL.html` (A · B · C, deux thèmes, vraie Toile capturée) · **défaut pris au doigt : la tuile « Un Chiche » ouvre un Promi** (carrousel d'origine l. 8805-8811, `acc_chiche_piege.py`) · atteinte des dalles 0 inatteignable sur 15/30/60, zooms 0,4 → 5, et 0/180 sous le chrome de A et C · `redteam_gens.py` écrit : 38/38, 4 sondes sur 4 prises, version d'avant le lot rouge (0/10, par absence du choix) · `planche-accueil/NUEE-ALIGNEMENT.png`. **Vu, non pris :** « Moi » absent du choix d'une Nuée (§5) ; 9 personnes coupent la pastille de la phrase sur « Ilyes, » sans points de suite. |
| 13 sept. | **Le Chiche au doigt + planche 2 de l'accueil** (sauvegarde `sauvegardes/app-avant-lot-chiche-doigt.html`, `e4c2d41a…`) | `c852e14f…` | Carrousel d'origine : ne s'arme plus sur `pp-choix`, un toucher sous le seuil ne change plus de tuile · `redteam_tuiles.py` au doigt CDP 64/64 (version d'avant : 30 KO) · CLAUDE §8 : une ligne · décisions de Tom en Q212 · `PLANCHE-ACCUEIL-2.html` (direction B, deux thèmes, 0 inatteignable sur 180 à dix zooms, air ≥ 8 partout) · la barre d'état est peinte par l'app : défaut, à retirer à l'intégration · la porte du Cercle dans les Réglages vérifiée au doigt. Batteries en série : design 0 · écrans 150 · 15 · 10 · 18 · 19 · toile 17 · geste 13 · verbe 6 · filets 0 · vide 61 · air 436 · champ 32 · pastilles 12 · phrase 6 · gens 38 · tuiles 64. |
| 13 sept. | **La dalle garde sa couleur** (sauvegarde `sauvegardes/app-avant-lot-dalle-figee.html`, `c852e14f…`) | `05150bcd…` | Couleur figée à la plantation (`p.dalle = {ci, lit}`, `_dalleFigee`, `_dalleDeCle` sur titre et personne — l'id change à chaque chargement sur le jeu) · monde de plantation passé aux peintres de l'Index et du Fil · la réserve de l'onboarding n'éclaircit plus une dalle reliée à un Promi (elle doublait la part de lilas : 50 % → 27 %, 10 chargements en sombre) · `redteam_dalle_figee.py` 4/4, version d'avant 0/4 · §4 et §8 · planches repérage, accueil (tuiles −24) et fiche de Nuée dans la copie `scratchpad/app-planche-reperage.html`. Batteries en série : design 0 · écrans 150 · 15 · 10 · 18 · 19 · toile 17 · geste 13 · verbe 6 · filets 0 · vide 61 · air 436 · champ 32 · pastilles 12 · phrase 6 · gens 38 · tuiles 64 · dalle 4. **Vu, non pris :** la position de défilement d'une fiche de Nuée survit à `closeAll` · le fil d'une Nuée ne montre que 8 cartes (`slice(0, 8)`) — le 9ᵉ Promi du potager n'y est pas. |
| 13 sept. | **Index · Fil — lire la nature** (sauvegarde `app-avant-lot-index-fil.html`) | — | Libellé Promi · Chiche · Nuée (Bricolage 700/12, pastille crème) sur chaque carte et à gauche de chaque ligne ; la dalle se décale à droite du libellé (sous lui sur une carte étroite — elle n'était plus peinte en « 3 par ligne », pris par releve-S4) ; largeur du libellé en COTE (la police n'est pas là au moment de peindre) ; boîte déclarée = boîte peinte · Nuée = petite Toile (`_petiteToile`, déterministe) · Nuée vide = Nuée, « AUCUNE PAROLE » · Index « N paroles · N Nuées » sous le titre, plateau 88 (`recale` porte l'exception), barre 144, liste 232 · `redteam_reperage` 16 (0/14 avant) · `releve-S4` réécrit (24 écarts avant). |
| 13 sept. | **Fiche de Nuée — « Planter dans la Nuée »** (sauvegarde `app-avant-lot-nuee-entree.html`) | — | Dernière ligne du fil au repos, pleine (12 sous la dernière carte) comme vide (16 sous « ENCORE AUCUNE PAROLE ») · n du trait compte l'entrée (vide 460 → 374), écarts de la fiche identiques · invitation du §5 retirée (déjà sous la barre) · `redteam_nuee_entree` 24 (8/24 avant) · `redteam_nuee` et `redteam_vide` réécrits au niveau de Q213, prouvés sur la version d'avant · `releve-design` figé (30 écarts, tous sur le bouton). |
| 13 sept. | **Accueil — direction B** (sauvegarde `app-avant-lot-accueil.html`) | — | Plateau 88 « Promi » Fraunces 27 + « 15 paroles · 2 Nuées », Partager et Réglages · barre 342 × 88 Studio · Aura | + 68 | Index · Fil (entrées centrées 70·124·266·320, + sur leur ligne) · le + (vrai toucher) ouvre les trois natures sur place, puis la page + sur la nature ; un appel par script ouvre la page + comme avant · anneau menthe/periwinkle/terracotta, rotation lente conservée · retirés : barre d'état, sélecteur Toile/Index, rond du Cercle (porte dans les Réglages), libellé vertical, voiles et flous, appui long → Studio, mode signature et son amorce · commandes DÉPLACÉES, jamais recréées · `redteam_accueil` 22 (2/22 avant) · `redteam_ecrans` : un renommage de nœud (`#accBarre`). |
| 13 sept. | **Le zoom tient** (sauvegarde `app-avant-lot-zoom.html`) | — | Borne de repos = borne de pincement (0,40) · une vue déplacée par la main n'est plus reprise par une plantation · rond « recadrer » (dalles-fantômes pleines) au besoin, et double toucher sur une case vide · `redteam_zoom` 16 (6/16 avant). **Non fait :** la couleur au Cercle (en attente d'un feu vert moteur). |
| 13 sept. | **La couleur au Cercle** (sauvegarde `app-avant-lot-cercle-couleur.html`, `539f6445…`) | `be5d4517…` | Cinquième réglage « LA COULEUR » (fiche Promi/Chiche, page +, Réglages) · bloc 384, encart 147 · ouverte : 4 tons de la palette du monde de la dalle + champ « code couleur » · moteur (feu vert) : `cOf` lit `s.rgb`, `_dalleFigee` le pose, `Toile.refigeCouleurs`, `Toile.tonsDe` · page + : le choix attend `Toile.addPromi`, effacé à la réouverture · `redteam_cercle_couleur` 34 (2/34 avant) · `releve-S2` réécrit (4→5, 304→384, 108→147, original gardé) · série : tout vert sauf `aveugle` (rouge d'avant) et `reperage` 15/16 une fois (« le potager », Index clair), 16/16 trois fois seul. **Non fait :** la Nuée (pas de dalle à elle) ; rien ne survit au rechargement sur le jeu de démonstration, couleur comprise. |
| 13 sept. | **Une Nuée a sa dalle — et son bloc du Cercle** (sauvegarde `app-avant-lot-nuee-dalle.html`, `be5d4517…`) | `b0980482…` | Constat : aucune Nuée n'avait de dalle (0 toucher `nuee` sur 9 165) — `Toile.sync()` l'effaçait à chaque plantation · moteur : une dalle par Nuée dans `sync` (taille de Nuée du moteur, wFin 14), couleur figée par Nuée (`NUEDALLE`, sauvegardée), `Toile.colorOfNuee` en lecture, la réserve de l'onboarding épargne la dalle de Nuée (elle sortait lilas puis bleue) · Peaufiner de Nuée : bloc du Cercle en page 2 sous « Planter », DISSOUDRE 124 → 618 ; page + d'une Nuée : le code va à la Nuée créée, jamais à un Promi · repérage : la petite Toile ne monte plus dans la zone du libellé (9/12 chargements avant, 0/12 après) · `redteam_nuee_dalle` 28 (6/28 avant) · `redteam_nuee` réécrit (DISSOUDRE +494, prouvé : 2 écarts sur la version d'avant) · série complète (moteur touché) : tout vert sauf `aveugle` (rouge d'avant) · `redteam_reperage` 10/10 passes à 16/16 · chantier 78 (la démo écrase la sauvegarde). |
| 14 sept. | **Un Promi planté dans une Nuée a sa dalle reliée** (sauvegarde `app-avant-lot-membre-lie.html`, `b0980482…`) | `b5156c0e…` | Pris au vrai chemin (« Planter dans la Nuée » → page + → `#addPromi`) : une dalle de plus sur la Toile, mais sans `pid` — pas de boîte pour sa fiche, pas de couleur, pas de couleur figée, 0 point au doigt · moteur : `addMember(clé, id)` relie la dalle et fige sa couleur, `addNuee` ne double pas une Nuée qui a déjà sa dalle · les trois appelants (`#addPromi`, `#addNuee`, `regenRecur`) passent l'id · `redteam_nuee_dalle` 38 (contrats 10 : 3 KO par thème sur la version d'avant ; le 11, Nuée neuve, y passe aussi — ce chemin recale la Toile juste après) · série complète (moteur) : tout vert sauf `aveugle` (rouge d'avant). |
| 14 sept. | **Huit défauts vus à l'œil + chantier 78** (sauvegarde `app-avant-lot-huit-defauts.html`) | `c096d7f1…` | Réglages : titre centré sur ✕ FERMER · « 3 Nuées offertes » retiré (Réglages, note du partage) · Index : titre + ligne resserrés et centrés, 32 du bord · Fil : plateau et barre de l'accueil masqués (`vue-fil`) · page + : les tuiles ne se voient plus au passage d'une pilule (6 à 10 images → 0) · fiche d'information de l'Aura réécrite sur l'écran actuel · + plus gras, anneau ×2 par l'intérieur, 100 s · jeu de démonstration seulement sans sauvegarde · `redteam_aveugle` réécrit au doigt (la carte passait sous la barre opaque) · 318 scripts jetables non cités mis à la Corbeille · batteries ciblées : accueil 22, tuiles 64, zoom 16, écrans 150, design 0, air 486 paires, S4 vert, repérage 16, aveugle 26, pastilles 12, fonctions 22. |
| 14 sept. | **Page + : les notices sur Peaufiner retirées** (sauvegarde `app-avant-lot-notices.html`) | `63c63167…` | Promi : l'aide garde seulement « touche ⇄ pour changer d'intention » · Chiche : plus d'aide · Nuée : n'en avait pas · la rangée des pinceaux se recentre d'elle-même (Promi 669 → 645, Chiche 697 → 630) · batteries : releve-S3 0, air intact, verbe 6, phrase 6. |
| 14 sept. | **File : 59 · 71 · 60 + chantier 79 noté** (sauvegarde `app-avant-lot-file-59.html`) | `68a4b605…` | 59 (résidu du sombre) : la teinte cède sous 31 sur le masque (15 ÷ 0,48), vise 32 — releve-aura vert, ΔE sombre 35 à 55 · 71 : le jeu ne passe plus deux fois (garde sur DOMContentLoaded) — « faire les crêpes » = 126 sur 4 chargements · 60 : « au groupe » (`_aQui`, trois endroits) · 79 PRIORITAIRE : le Cercle n'ajoute rien à l'Aura · 62 déjà fait · 76, 74, 61 : décisions de Tom · batteries : aura, S4, air, dalle_figee. |
| 14 sept. | **76 remesuré + audit et planche du 79** (sauvegarde `app-avant-lot-76.html`) | `e4900b3c…` | Aide de l'Aura : la sphère ne dit que le geste · 76 : le moteur ne peint PAS de crème — les creux sont transparents (gravure 76,1 %, braille 76,7 %, sillons 79,8 %) ; piste ② posée dans une COPIE (`scratchpad/app-planche-76.html`), `planche-76/PLANCHE-76.html`, rien intégré · 79 : `AUDIT-RECIPROCITE.md` + `planche-79/PLANCHE-79.html` (second anneau du §2.9 sur les données du jeu, et « Ce qu'on t'a tenu »). |
| 14 sept. | **76 fermé sur l'écran qui vend** (sauvegarde `app-avant-lot-76-vendre.html`) | `a438af18…` | Gravure, Braille, Sillons posés sur leur silhouette dilatée (5), teinte de la dalle mêlée à 55 % vers le blanc (clair) ou l'encre (sombre) · plus de crème entre les traits · moteur intact · batterie : verif_cercle 89/89 (le premier passage a pris une lecture de pixels interdite sur cet écran : couleur prise au moteur). |
| 14 sept. | **79 : C retenu, planche B refaite** | — (app inchangée) | Spécification §2.9 corrigée : les deux moitiés remplacent le second anneau · `planche-79/PLANCHE-79-DISTINGUER.html` (A 0,58 · B 0,51 · C 0,01) · `planche-79/PLANCHE-79-B.html` avec C, jour de 6 px, deux thèmes, jeu + trois promesses reçues. |
| 14 sept. | **La réciprocité sur l'Aura — intégrée** (sauvegarde `app-avant-lot-reciprocite.html`) | `0990b44d…` | Données : `envers()` (à toi · sa moitié d'un Chiche relevé · à ta Nuée), rangée alphabétique qui accueille qui te promet sans retour · Noyaux en DEUX MOITIÉS (gauche ce que tu tiens, droite ce qu'on te tient, jour 6 px, pas de piste) · « Ce qu'on t'a tenu » sous « Ce que tu as tenu », 28 d'air, ses propres classes · gratuit : moitiés droites et rangée floutées 2,4 px, encart « ✦ Le Cercle » net (62) → écran qui vend · jeu : trois promesses reçues (Rachel, Nico, Marion), cartes « de Rachel » · rangée de 5 Noyaux : 442 dans 366, défile · batteries : aura vert, S4 vert, repérage 16, écrans 150, accueil 22, dalle figée 4, toile 17, air intact (513 paires) · juges réécrits au niveau de C/B : `releve-aura` (arcs en chemins, pas de piste, bouton sous la 2ᵉ rangée), `redteam_ecrans` (arcs, pas de piste). |
| 14 sept. | **Six contradictions + passe des carnets** (sauvegarde `app-avant-lot-contradictions.html`) | — | Prix du Cercle alignés — **corrigé le même jour (Tom) : l'annuel en avant, « 39 € · soit 3,25 €/mois », le mois « ou le mois — 5,99 € » en option ; l'ancien écran dit la même chose** (`6627c0f2…`, `verif_cercle` 89/89, option mise à jour au niveau de la décision) · fil d'une Nuée sans coupe à 8 (9/9 au potager) · « Moi » après « tout le monde » dans le choix d'une Nuée, la phrase dit « avec Moi » · variable `urgent` → `bientot` · « Réinitialiser (test) » hors de la vue et sans Cercle · sous-titre de l'accueil : déjà masqué depuis l'accueil B · carnets : CHANTIERS § « État au 14 septembre », 23 lignes ✅, 6 ⊘ ; listes périmées de l'état des lieux signalées ; CLAUDE.md et QUESTIONS remis à jour. |
| 18 sept. | **Les titres sont une police — PromiLate** (sauvegarde `app-avant-lot-police-titres.html`) | 75f78a3d… | `lot-TITRES-DESSINS` remplacé par `lot-TITRES-POLICE` : PromiLate embarquée (woff2), jeton `--f-marque` (JSON · CSS · Swift), titres à 27 px (cap 18,9 = les dessins ; 29 sur la page +), « Le Studio », « L’aura », « i » de Promi en accent · phrases du trait (`.tenir-lab`, `.pp-trace`, `#dptTrace`) · `ajusteTitres` part de 27 pour PromiLate · Q234. Batteries : tokens 35/35, polices 0 absent, air 506 intactes, écrans 150/150, verbe 6/6, design 54 (42 avant, +12 demandés). |
| 23 sept. | **Le partage : Mon Folio, la Pelote dans l'image, les titres sur deux lignes** (sauvegarde `sauvegardes/app-avant-lot-v14.html`) | `138ed3f1…` | **1 · « Mes dalles » devient « MON FOLIO »** — c'est le SUJET du partage qui change de nom ; « mes dalles » reste le nom de la Toile. Vocabulaire du §2 · **2 · LES TITRES DU FOLIO SE CHEVAUCHAIENT.** Ils étaient tracés sur UNE ligne, centrés, sans mesure et sans coupe — quatre libellés l'un sur l'autre : « le grand plongeoimonter la serre avant lesprendre l'arrosage autécupérer les plants de t… ». Un titre se **mesure** et se coupe **aux mots**, deux lignes au plus, points de suite au-delà — **jamais de réduction de taille**. Une rangée prend la hauteur de son titre le plus haut, et **les titres longs se regroupent** : rangées **[1,1,1,2,2,2]** au lieu de quatre rangées hautes mélangées · **3 · LA PELOTE PREND QUATRE CASES.** Le mécanisme était déjà écrit pour le Noyau (« deux cases sur deux ») : on le reprend tel quel. Les quatre cases sont ENJAMBÉES, les dalles se rangent autour — **18 dalles + 4 = 22, en 6 rangées de 4, aucune case partagée** · ⚠ **ET LA PLANCHE TIENT DANS SON CADRE** : à six rangées la dernière écrivait SUR le mot-marque. Sa bande est réservée, et si ça dépasse encore **la CASE rétrécit** — jamais le texte seul ; on itère, ça converge au deuxième tour · **4 · « PROMITTEURS » NE PEIGNAIT RIEN** — vérifié dans le code : `_sealParts.prometteurs` n'est lu que par `renderSeal`, le peintre de l'ancien mode Noyau, retiré du partage. Il sort, et sa place revient à **« La Pelote »** dans DANS L'IMAGE · **5 · « LE MOT-MARQUE · Bricolage / Signature » SORT** (la rangée du panneau et celle de la feuille) — masqué, pas détruit · **6 · LA PELOTE DANS « MA TOILE » — DEUX COMPOSITIONS À CHOISIR** : **A · le coin** (la Toile partout SAUF un disque en bas à gauche, laissé au fond uni) et **B · le socle** (la Toile aux deux tiers hauts, coupés net, la Pelote sur un socle uni). On ne touche pas à `shareToile` : on RECOMPOSE après — copie, fond, découpe, Pelote. La Toile est CLIPÉE, le disque n'en reçoit pas un pixel. ⚠ La bande du mot-marque est réservée dans les deux, et l'invite du doigt s'efface quand la Pelote prend ce coin. **Posé par défaut : A.** Q287, Q288, Q289. **Juges repris au niveau de la décision** (originaux `sauvegardes/redteam_toile-avant-v14.py`, `redteam_geste-avant-v14.py`) : cinq contrats du Noyau dans la planche deviennent des contrats de la Pelote, et « les intitulés restent » devient **« aucun intitulé ne disparaît »** — on compare les IDS, parce qu'un titre peut désormais prendre ses points de suite quand la case rétrécit. Le glissement animé du bloc sort avec le Noyau (il n'y a plus de déplacement à animer) : à sa place, **« rien ne disparaît, rien ne se superpose »**, mesuré sur la composition publiée. **Batteries** (en série) : écrans **150** · vide **61** · toile **17** · geste **13** · cercle **34** · `redteam_air` **30** et `releve-design` **62** — **listes identiques à v13, ce lot n'en ajoute aucun. NI L'UN NI L'AUTRE N'EST FIGÉ.** ⚠ **Un rouge de passe parallèle réfuté** : « les dalles sont aux bonnes positions » (5/10) pendant que `air` et `design` tournaient — **17/17 en série**, c'est le piège du §7. |
| 23 sept. | **Le Fil, le Chiche, la Pelote, les titres, la colonne de l'Aura, le partage** (sauvegarde `sauvegardes/app-avant-lot-v13.html`) | `da351d5f…` | **1 · LE FIL.** La dalle était peinte et ne se voyait pas : `champCede` ne poussait le champ que DANS UN SENS — sur le Chiche (`#FFB8D2`, saturation 100 %) la clarté plafonne et l'écart s'arrêtait à **15,2** là où le §3 demande 42 ; vers le bas il passe sans peine, en restant le rose du Chiche. Les deux sens sont essayés : écarts mesurés sur les cinq bandeaux **132 · 98 · 220 · 108 · 185**. Et **le titre garde sa taille** (24 px, plus aucune réduction) : il REMONTE — la boîte grandit vers le haut depuis 92, l'événement suit jusqu'à 8 du bord, deux lignes tiennent pile dans 50 — et **au-delà il coupe avec des points de suite**. Une carte à une ligne ne bouge pas d'un pixel. Q280, Q281 · **2 · LE CHICHE.** Le filet crème n'était posé que sous LA CRÊTE d'une parole tenue ; il se décide maintenant PAR MESURE — dès que le trait est à moins de 42 du corps (Chiche **Δlum 4,1**, Promi **0,0**, en sombre ; en clair, jamais). Et ce qui est écrit sur un corps sombre se lit : le violet « en cours » y tombait à **Δlum 6,8** — amande si la parole est tenue, crème sinon, **et seulement ce qui passe sous 42** (le terracotta « à tenir » tient déjà à 82,5). Prouvé contre la page sans le bloc : **6,8 sans, ≥ 209,9 avec**. Les contours aussi (le cadre d'« écris un mot »). Q282 · **3 · LA PELOTE** — la sphère change de nom, et **« Orbite » disparaît** : 115 `ORB`, 4 `PeloteMoteur`, 9 clés de stockage (**migrées**, sinon les caresses étaient perdues), 8 ids de lot, 32 occurrences du mot dans l'app, **221 dans 14 documents** — 0 restant. Son sol **tire au hasard parmi les quatre tons** à chaque ouverture (six ouvertures : `2·3·3·0·1·2`) ; un tirage invalide les DEUX caches. Q283 · **4 · LES TITRES.** Mesuré avant de toucher : **ils étaient tous à 27 px**, au dixième de pixel. Ce qui diffère, c'est l'air avant ✕ FERMER (Fil **129,2** · Index 76,9 · Le Studio **20,3**). Le départ d'`ajusteTitres` passe à **31** et sa boucle borne chacun à son plateau : **Index 31 · Réglages 31 · L'aura 31 · Fil 31 · Partager 29 · Le Studio 27** (les deux derniers sont les plus longs). ⚠ Le mot de nature d'une FICHE suit (27 → 31) : même composant, même propriétaire. L'encart de l'Index se recalcule — **le compte ne descend pas** (`redteam_air` l'a pris à −4,5), c'est le titre qui remonte. Q285 · **5 · LA COLONNE DE L'AURA.** Le bouton tombait à **y 1045**, 201 px sous le pli ; il est **à 636**, sous la légende, air de 28 de part et d'autre. ⚠ `lgINK` passe de −0,5 à **−6** : le voisin du bas n'est plus un titre mais un BOUTON, dont le contour commence plus haut dans sa boîte — mesuré 36,5/31,0, corrigé à **31,5/31,0 à l'encre**. Q186 sort avec le bouton. Q283 · **6 · LE PARTAGE.** Le Noyau sort (« le partager, c'est partager son score ») ; le sujet devient **Ma Pelote**, la Pelote se compose SEULE sur le fond choisi — plus de superposition. Des six commandes il ne reste que **Promitteurs** ; la catégorie devient **« DANS L'IMAGE »** et remonte : **LE SUJET · DANS L'IMAGE · QUELS PROMI**, puis les cinq réglages techniques. ⚠ **On masque, on ne détruit pas** : retiré du DOM, « Le Noyau » **revenait 2,5 s plus tard** (`pose()` rappelle son créateur, dont le garde est « s'il existe, ne rien faire »). ⚠ Et le peintre exige la trame : sans îles, la Pelote sortait NOIRE. **Trois libellés à choisir** pour l'ex-« CE QU'IL MONTRE » : **DANS L'IMAGE** · CE QU'ON VOIT · CE QUE L'IMAGE PORTE. Q284 · **7 · « Signal » devient « Avenant »** (la clé `signal` ne bouge pas). Q286. **Juges repris au niveau de la décision** (originaux `sauvegardes/redteam_ecrans-avant-v13.py`, `releve-aura-avant-v13.py`, `redteam_air-avant-v13.py`) : trois contrats de `redteam_ecrans` (le bouton, l'ordre de la colonne, le voisin de la légende), sept de `releve-aura` (l'ordre, le libellé, l'air, le sol qui doit être **l'un des quatre tons**), un de `redteam_air` (un bloc annoncé centré l'est **à l'encre** : l'écart de boîte est désormais DÉCLARÉ, troisième champ de `data-centre-entre`). **Batteries** (en série) : écrans **150** · vide **61** · repérage **16** · accueil **22** · tonsurton **26** · champ **32** · toile **17** · geste **13** · studio-geste **13** · tokens **46** · nuée-dalle **38** · cercle **34** · `releve-S4` **110** (124 avant) dont **présence peinte 14 → 0** · `releve-aura` **1** (30 avant : le seul restant est la dalle tirée au hasard du chantier 59, ΔE 8,0) · `redteam_air` **30 paires** contre 42 : **11 disparues** (toute la légende de l'Aura), **1 neuve à −1 px** — et elle s'explique : le texte était ton sur ton (Δ23), donc INVISIBLE, et la sonde d'encre ne le trouvait pas ; rendu lisible, son encre se mesure enfin. Géométrie des bandeaux **identique au pixel** avant/après. `releve-design` **62**, exactement les mêmes nœuds qu'avant, seules les valeurs du mot de nature bougent. **NI L'UN NI L'AUTRE N'EST FIGÉ.** **Vu, non pris :** la carte d'Index garde sa réduction de dernière extrémité (aucune carte du jeu n'y est réduite) ; le chantier 59 se tire plus souvent maintenant que le sol prend l'un des quatre tons. |
| 23 sept. | **Le filet collé, Le Cercle, le Fil, le retour du Studio, trois palettes** (sauvegarde `sauvegardes/app-avant-lot-v12.html`, `42bdacc5…`) | `c31321a0…` | **1 · LE FILET, CINQUIÈME ÉCRITURE.** Tom : « il y a un écart, il cerne le bord sans jeu ». Deux fois la même faute — **une cote calculée sur une géométrie qui n'est pas celle de l'objet** : l'`outline-offset:3px` du **+** venait de `.dhero::before{inset:-3px}`, la règle GÉNÉRALE, alors que l'accueil impose `inset:0` (offset → **0**) ; et `drawKRing` posait le sien au bord du CANEVAS (`W/2`) quand l'anneau s'arrête à **0,4069·W** — mesuré **8,2 px de jeu** sur un Noyau de 104, ramenés à **0,5**. ⚠ `_filetsDisques` était un **second propriétaire** (§7) : elle lit maintenant `data-filet`. Les Noyaux SVG (−1,4, le filet DANS l'anneau) et le Noyau au canevas d'une fiche (0,08) ne bougent pas. Q276 · **2 · « PROMI » OUVRE LE CERCLE** (sur le `click`, par `ouvreCercle()` — rien ne bouge à l'œil) · **3 · LE TITRE DEVIENT « LE CERCLE »** en PromiLate ; **taille gardée à 32** (décidé seul, Q279) : mesuré **216,42 px dans une boîte de 291**, une seule ligne · **4 · LE FIL : UNE CARTE MANQUAIT, ET LE TITRE LONG ÉTAIT TRONQUÉ.** `_filComp` déclarait **5** entrées, le Fil en peignait **4** — `etatEvenement` appelle `etatTrait` pour un événement `tenue`, une fonction de l'IIFE de l'onde absente du bloc S4 : `ReferenceError` avalé (le piège du §8, la console ne disait rien). Et le titre : boîte 42, peint à 24, deux lignes = 49,9 → coupées. Il **remonte** (la boîte grandit vers le haut depuis 92, l'événement suit, plancher 8 du bord ; airs 6 et 6 inchangés) **puis rétrécit** (1 px, plancher 11, `important`). Mesuré sur les deux versions : avant **4 cartes, `tronque:true`, 76 dans 42** ; après **5 cartes, 50 dans 50, 18 et 22 px** — et une carte à une ligne ne bouge pas d'un pixel. Q277 · **5 · LE RETOUR DU STUDIO** était `rgb(0,0,0)` **dans les deux thèmes** (mesuré) : il prend la bascule de `#st3pn`, crème sur le panneau sombre, encre sur le clair · **6 · TROIS PALETTES** — **Truculent** `#FF3E00 #00E5FF #5600D6 #F6FF00`, **Pétulant** `#FF8A00 #6800E0 #00C85A #FFAAC8`, **Fantasque** `#00FF8C #E60073 #0040FF #FFF7DE`, posées avec les claires : 24 pastilles = **quatre rangées de six**. ΔE 2000 — écart interne **48,3 · 38,0 · 28,5** (le jeu : 13,0 à 37,8), distance à la plus proche **17,1 · 17,8 · 16,6** (le jeu : 9,2 à 20,7, médiane 16,9), entre elles **20,5 à 23,5** ; garde-fou du sol repassé sur 24 : **0 sous 42 sur 48 mesures**. Q278. **Batteries** (en série) : écrans **150** · accueil **22** · repérage **16** (le Fil y compte **5 lignes**, pas 4) · vide **61** · toile **17** · studio-geste **13** · tokens **46** · `releve-S4` **124** contre **119** avant — **les 5 écarts de plus sont la cinquième carte, qui n'existait pas** (4 écarts de style de la même famille que les quatre autres, + 1 ton sur ton déjà connu du Fil sombre). **Vu, non pris :** le ton sur ton du Fil en sombre passe de 3 à 4 cartes — c'est le défaut antérieur (20 sept., « vu non pris ») qui s'applique à une carte de plus, pas un défaut neuf. **`releve-design` 62 et `redteam_air` 42 — passés sur les DEUX versions, listes **identiques au caractère** : ce lot n'en ajoute aucun, tout est antérieur (les titres PromiLate, les lots de palette). **NON FIGÉS — Tom ne les a pas ouverts.** |
| 23 sept. | **Les filets entiers, les titres, la dernière lettre** (sauvegarde `app-avant-lot-v11.html`) | — | **1 · LE FILET, QUATRIÈME ÉCRITURE.** Tom : « tu as des filets crème tronqués ». Ce n'est pas un élément posé dessus — **c'est la boîte qui rogne** : un `box-shadow` DÉBORDE, et les rangées qui glissent (`.au-nx`, `.aura-track`, `overflow:auto hidden`) le coupent. Mesuré en repeignant l'ombre **en rouge pur**, 360 points : **96,4 % du tour, trou de 264 à 277°**. Rembourrer les rangées ne suffit pas (90,0 → 94,7) et déplace. **Ce qui tient : le peintre le trace lui-même, en DERNIER, DANS la boîte** (l'anneau finit à `R+lw/2 = W/2`). ⚠ Une passe extérieure qui peint dans un canevas est effacée au rendu suivant (0 % sur une Nuée). **Mesuré après : 100 % du tour partout** — Aura, fiche tenue, fiche à tenir, Nuée (Q274) · **2 · LE FILET DU +** sur l'accueil : `outline` 1 px à `outline-offset:3`, pile sur le bord du `::before` — **100 % du tour** · **3 · LES TITRES** : ils étaient tous à 27 px et **ça ne suffit pas** — à 27, PromiLate fait cap 19,9 / large 163,8, Gilbert cap 18,9 / large **101,7**. « Ton Aura » était le dernier en Gilbert, et à **33**. Tous PromiLate 27, onze écrans relevés ⚠ trois ids nécessaires (`:not(.ah-head)` l'exclut) · **4 · LA DERNIÈRE LETTRE** : le Fil et l'Index la perdent ; le « i » de l'accueil prend le clignotement de Réglages — **même couleur, même 1,15 s**, mesuré. ⚠ **Je m'étais trompé au tour précédent** : j'avais ÉTEINT le clignotement au lieu de l'étendre, et **l'extinction n'avait même pas pris** — j'ai annoncé le contraire de ce qui était à l'écran, faute d'avoir remesuré (Q275). **Juge repris** : `redteam_ecrans` comptait le filet (1,4 px) parmi « les arcs font 6 px et plus » — il vise les ARCS, qui se déclarent (original `sauvegardes/redteam_ecrans-avant-v11.py`). Batteries : écrans **150** · accueil 22 · vide 61 · tonsurton 26 · repérage 16 · champ 32 · geste 13 · toile 17 · verbe 6 · tuiles 64 · gens 38 · nuée-dalle 38 · tokens 46 · cercle 34 · **aura 0** (+1 antérieur) · nuée 124 (son chiffre d'avant). |
| 23 sept. | **Le pourpre, les filets, les cartes, les titres** (sauvegarde `app-avant-lot-v10.html`) | — | **1 · SUR UN FOND SOMBRE LE TENU EST L'AMANDE** (Tom, corrige le 22 sept.) : `#00341A` sur la terre `#2B1020` donne **Δlum 11,3** ; l'amande **190,6**. Passe qui lit la couleur CALCULÉE et remonte au premier fond OPAQUE — on trie les surfaces, pas les règles. ⚠ Elle NE FIGE PAS : `_ficheCotes` réécrit `color` en ligne avec `important` à chaque passage (piégé au peintre, §7) — la passe se relit et le peintre est enveloppé. « TENUE » marquée en amande ; ⚠ « un peu gras » ne peut pas être une graisse, Gilbert n'en a qu'une (§6) : chasse +0,06 em et +6 % de taille (Q269) · **2 · LE FILET CRÈME — POURQUOI IL N'ÉTAIT PAS FAIT** : peint DANS le canevas avant l'anneau (l'anneau extérieur du Cercle repasse dessus) ET conditionné à une CLASSE, alors que `drawKRing` est appelé **8 à 12 fois** par ouverture et que les premiers appels précèdent la pose de la classe. Il vit maintenant **sur le NŒUD** (`box-shadow` 1,4 px : le bord extérieur d'un anneau EST le bord de sa boîte, mesuré 116 sur 117) et paraît **dès que le fond sous lui est sombre** (Q270) · **3 · UNE SEULE ÉPAISSEUR** : le même objet portait **trois cotes** (Aura 12/9, poseur de fiche 8/6, `KR_LW` 0,21) — une seule, celle de l'Aura · **filet crème SOUS LE TRAIT** d'une parole tenue (crête sur terre : Δlum 15,7, sous le seuil), il suit la courbe (Q271) · **4 · LES CARTES** : la boucle qui rétrécit un titre trop long posait `fontSize` **sans `important`** et `#device .s4-ti{24px!important}` la battait — le titre restait coupé (« planter un arbre » : 33 px de haut pour 48 de texte) · **5 · LE FIL D'UNE NUÉE PLEINE** rendait à **y 0** et recouvrait l'entête : c'est l'ORDRE (bâti après le poseur). ⚠ Deux parades fausses avant la bonne — rappeler `_ficheCotes()` renvoie toute la fiche hors écran, et « top non posé » ne marche pas (le poseur écrit 30, posé ET faux) : **le critère est le RECOUVREMENT** · **6 · LE STUDIO** : 14 px d'air en haut, 38 en bas → **26 / 26** ⚠ `margin-top` n'a pas de prise et `#studioScreen` ne vit pas sous `#device` · **7 · LES TITRES** tous à 27 (« Ton Aura » sortait à 33, « La langue » et « La confidentialité » à 29) · **le « s » de Réglages ne clignote plus** · **8 · UNE PASTILLE** de 9 px cernée du filet crème sur ce qui attend un geste, Fil et Index (Q272) · **9 · L'IMAGE PARTAGÉE** : plus de pourcentage ni de mot d'harmonie sur le Noyau, le pied ne porte que le mot-marque à l'« i » coloré, et un liseré FLOU (2 px / flou 6 sur 1080) détache le Noyau sans halo net (Q273). Batteries : écrans **150** · vide 61 · repérage 16 · tonsurton 26 · champ 32 · geste 13 · accueil 22 · toile 17 · verbe 6 · tuiles 64 · gens 38 · nuée-dalle 38 · cercle 34 · dalle 4 · tokens 46 · **aura 0** (+1 antérieur). **Vu, non pris :** `redteam_nuee` **124 écarts, exactement son chiffre d'avant le lot** (mot-marque 52/55,2, « aucune ligne peinte sur l'onde ») — antérieurs · la dalle « rapporter le livre » sous ΔE 15 en sombre (chantier 59). **NON FAIT SUR LE PARTAGE, ET DIT :** la Pelote ne s'ajoute pas (le bouton bascule pourtant bien le drapeau) · le Noyau prend la place de dalles en « Mes dalles » et rien ne se recompose autour · on ne peut pas ajouter le Noyau ET la sphère · les choix d'affichage ne sont pas remontés au-dessus des réglages techniques — **un lot de dessin, pas un correctif** (Q273). **`releve-design` et `redteam_air` toujours pas passés : Tom ne les a pas ouverts.** |
| 23 sept. | **La sphère, les disques, la légende, les flèches, la page +** (sauvegarde `app-avant-lot-v9.html`) | — | **1 · LA SPHÈRE** — deux causes mesurées et indépendantes : le brin faisait **2 à 3 px** sur un canevas de 592 (agrandi **×1,6**), et en clair la peau ne gardait RIEN de la couleur du lieu (`PEAU_T` 1 → **0,78**) — des fibres sombres sur un fond crème, c'est la page qu'on croyait voir. Le « piquant » (écart-type local 3×3, la grandeur qui a la forme du défaut) tombe de **11,93 à 6,93** en clair, **7,19 à 5,48** en sombre, et le limbe cesse d'être un cercle net. ⚠ **Le plafond est le budget d'image : 13,8 → 17,0 ms** — ce sont les PIXELS qui dominent (à pixels égaux, 60 000 poils longs coûtent comme 110 000 courts). ×2,2 donnait un pelage franchement plus beau et **35 ms** : refusé (Q264) · **2 · LES DISQUES** — le jour valait 0,8 % DU TOUR, donc un ANGLE : 1,00 px sur « Toi », 0,76 sur une personne. Il est en **PIXELS D'ARC (3)**, converti par anneau, **n arcs et n jours identiques**, centré sur midi ; l'ouverture double du haut (reliquat des deux moitiés) sort, et l'anneau d'une FICHE perd son fondu de 3 % pour le même jour. ⚠ **Un seul état ne peut pas faire 360° pile** — Nico est sorti sans anneau au premier jet (Q265) · **3 · LA LÉGENDE** 30 → **19,4**, la taille du commentaire, qui monte de 18,9 à 19,4 — **plafond MESURÉ : à 20 la phrase passe à la ligne** (349 > 342). Le commentaire est **à équidistance de la BOULE et du disque de soi** : son bas visible est 353,4, pas 385,4 (la boule n'occupe que 232 de sa boîte de 296) ; l'air valait **50,3 / 26,7**, il vaut **38,18 des deux côtés**. À l'encre : phrase 37,0 / 36,0 · légende 32,5 / 33,0 (Q266) · **4 · LES FLÈCHES** — un bout ROND dépasse de la moitié de sa largeur : le trait finissait À LA POINTE du chevron, la flèche d'invite 2,25 px au-delà de sa propre tête. Les deux s'arrêtent en deçà (Q267) · **5 · LA PAGE +** — l'estimation du §2.8 porte **0,53**, la largeur moyenne d'un caractère de la police de la PLANCHE ; Gilbert donne **0,44** (mesuré). Elle sur-contraignait de 20 %. **La mesure fait foi désormais**, bornée en haut par la taille de départ du §2.8 ; l'estimation reste en repli. Promi **25 → 35** · Nuée 33 → 36 · Chiche 18 → 25 ; l'aide de guideline 17,5 → 20 (Q268). **Juges repris au niveau de la décision** : `redteam_ecrans` (LG_INK −1,25 → −0,5, **150/150**) et `releve-aura` (cote du mot, de la légende, AIR_MOT, LIGNE_MOT — **prouvé : 10 écarts sur la version d'avant, 0 après** ; original `sauvegardes/releve-aura-avant-v9.py`). Batteries : écrans 150 · verbe 6 · phrase 6 · tuiles 64 · geste 13 · vide 61 · tonsurton 26 · champ 32 · repérage 16 · toile 17 · accueil 22 · aura 0 (+1 antérieur). **Vu, non pris :** `redteam_nuee` sort **124 écarts — IDENTIQUES sur la version d'avant** (mot-marque 52 / 55,2 et hauteur 36 / 29,6, et « aucune ligne peinte sur l'onde ») : antérieurs à ce lot, non ouverts · la dalle « rapporter le livre » à ΔE 14,8 en sombre (chantier 59) · **`releve-design` et `redteam_air` toujours pas passés : Tom ne les a pas ouverts.** |
| 22 sept. | **Les sept corrections** (sauvegardes `app-avant-lot-v8d.html` `03e01c25…`, `app-avant-lot-v8e.html`) | — | **1 · LES TROIS VALEURS, ET ELLES SEULES** — les deux clairs posés la veille (`#33BA6C`, `#A77CF7`) et la bascule `-txt` qui les portait sortent ; balayé sur le RENDU, **14 écrans × 2 thèmes : 558 surfaces sur les trois valeurs, 0 ailleurs** (`scratchpad/etats_reste.py`). **27 familles de nœuds corrigées** (`etats_diff.py`), et **l'anneau du + pris aux PIXELS** — il n'est pas dans le DOM (`conic-gradient`) : `#33BA6C`+`#A77CF7` → **`#00341A`+`#291547`+`#DD4D23`** ; ⚠ la règle qui le nomme (l. 95, lilas et bleu) est MORTE. Dernière amande : l'illustration « Ce que tu as tenu » de l'aide, hors de l'appareil quand l'écran est fermé — invisible pour les balayages d'avant (Q262) · **2 · le filet des disques passe À L'EXTÉRIEUR** — crème `#F7F0DE`, 1,4 px, cernant l'anneau (v8) · **3 · les disques épaissis** — trait 8 → **12** (toi) et 6 → **9** (une personne), 0,21 × le diamètre ; jours entre segments 2 % → **0,8 %** du tour · **4 · la légende doublée** — 15 → **30 px**, boîte 18 → 36, et centrée **À L'ENCRE** dans son espace (cote déclarée `K.lgINK = −1,25`, Gilbert se pose bas dans sa ligne) : **29,5 / 29,0** aux cinq phrases × deux thèmes · **5 · « toi » → « Toi »** (10 endroits) · **6 · `atlasAlpha` comprise** — le seuil portait sur l'alpha APRÈS multiplication : il effaçait le bord des poils sombres. Il porte sur LA SOURCE, et un poil retenu garde au moins 1 d'alpha : **peau nue 27,91 % → 26,74 %** sans un ms de plus (13,8 ms) · et le sol **suit bien la palette**, sans nature ni état (`sol_suit.py`) · **7 · l'animation de célébration notée comme À ÉCRIRE** (Q258) · « Mes dalles » validé. **Juges repris au niveau de la décision** : `redteam_ecrans` (150/150), `redteam_tokens` (46/46), **`releve-aura` — six familles de contrats périmés + la sonde d'encre qui rendait 0** sur la seule phrase à descendante (le « g » de « légère » passe sous sa boîte de ligne) + le contrat « palette de plantation » qui forçait **`ocean`**, palette disparue avec les vingt du 17 sept. (Q263). **94 écarts → 0**, et **prouvé contre la version fautive : 41 écarts**. Batteries : écrans 150 · tokens 46 · aura 0 (+ 1 antérieur). **Vu, non pris :** la dalle « rapporter le livre » sous le plancher ΔE 15 en sombre (12,2 à ce passage) — défaut du chantier 59 · l'illustration « Ce que tu as tenu » mêle un état et une nature · l'image du mode « Le Noyau » (Q260) · **`releve-design` et `redteam_air` toujours pas passés : Tom ne les a pas ouverts.** |
| 22 sept. | **Un anneau, trois arcs · l'amande · le sol ressaturé** (sauvegarde `app-avant-lot-v8c.html`, `c0d54b67…`) | `03e01c25…` | **UN ANNEAU NE PORTE QUE TROIS ARCS** : les deux moitiés de la réciprocité (Q215) donnaient jusqu'à SIX segments (« toi » 6 · Marion 5 · Rachel 4) — et pour Adrien et Nico, seule la moitié DROITE existait, leur anneau ne montrant que ce qu'ON leur tient. L'anneau porte désormais les trois états **des deux sens, une fois**, pondérés par le NOMBRE de paroles (on concatène les LISTES) ; la réciprocité garde sa rangée. Le `opacity:.5` du gratuit **quitte les arcs** — c'est lui qui délavait les trois couleurs. Rendu mesuré : #DD4D23 · #291547 · #00341A, opacité 1 (`scratchpad/anneaux.py`) · **L'AMANDE NE PEINT PLUS QUE L'ANIMATION** : balayé sur 8 écrans × 2 thèmes, **0 surface hors animation** (`scratchpad/amande.py`) — restaient le verbe de la phrase (repli) et l'icône des Noyaux de l'aide · **LE SOL GARDE LA COULEUR DE LA PALETTE** : il prenait bien le ton dominant, mais Q210 écrasait sa chroma (41,6 → 18,8 → **6,4**) ; on garde la clarté et **on ressature à 0,72 × C1** — et ⚠ **dans `solEffectif`, pas dans `fondSphere`** (c'est le POIL qui fait la couleur). Mesuré en clair : Signal 7,3 → **13,6** · Irascible **30,7** · Allègre **21,4** · Taciturne **18,9** ; « la matière » de `releve-aura` passe de 1 à **0** · **« PARTAGER MON NOYAU »** : la page s'ouvrait bien, mais `#auraScreen` ne perd jamais `.show` — l'Aura restait par-dessus (le même défaut que le régulateur le 20 sept.). Corrigé · **« Mes Promi » → « Mes dalles »** (provisoire, trois noms en Q261). Batteries : écrans 150 · tonsurton 26 · tokens 46 · vide 61 · champ 32 · toile 17 · accueil 22 · verbe 6 · geste 13 · phrase 6 · repérage 16 · `releve-aura` **52 écarts** (contre 64 — les arcs ont fait tomber 12 écarts de style). **NON FAIT, ET DIT :** l'animation de célébration (la seconde dalle décalée) **n'existe pas** — l'« instant » du moodboard est autre chose (Q258) · l'image du mode « Le Noyau » montre l'ANCIEN Noyau, sans la sphère, et on ne peut pas la tourner au doigt (Q260) · la normalisation d'`atlasAlpha` n'est pas comprise, la sphère garde ses écarts entre poils (Q255). |
| 21 sept. | **Les états basculent · le paysage v8 · le Fil** (sauvegarde `app-avant-lot-v8b.html`, `50902883…`) | `c0d54b67…` | **L'amande n'est PLUS la valeur claire de « tenu »** (réservée à l'animation de célébration) : le tenu prend **#33BA6C**, par le MÊME transport que le couple validé (ΔL +49, ΔC +34, teinte gardée) et, comme lui, à ΔE 60 de son plein · **les états basculent avec LEUR FOND** — la colonne de l'Aura est sur la page (clair → profondes, sombre → claires), l'anneau du + est sur la barre sombre (claires toujours) ; `eta()` se REPEINT au changement de thème · **le balayage a trouvé 3 autres états aux anciennes valeurs** (l'aide de l'Aura en couleurs de NATURE, le bandeau du Fil, le fil d'une Nuée) — **0 sur 2 thèmes × 6 écrans** après (`scratchpad/etats.py`) · **LE PAYSAGE v8** : terre **#2B1020**, crête **#0B4A2A**, anneau #00341A 5 px **cerné d'un filet crème de 1,4 px** — le filet est la condition de lisibilité (le vert n'est qu'à ΔE 44,6 de la terre, le crème à Δlum 217,3) ; l'ocre est abandonné, #6B4630 sort · **LE FIL, deux défauts, une cause** : `feedAdd` ne passait pas le `pid` — pas de titre, pas d'état, **pas de dalle** ; 7 appels corrigés · et le retrait du titre se cassait sur une **apostrophe** — on retire du « au » (`scratchpad/fil_tenu.py` 5/5) · **⚑ LE JUGE NE METTAIT JAMAIS L'APP EN SOMBRE** : `redteam_ecrans` ajoutait `.light` pour la passe claire et ne faisait rien pour l'autre, or le défaut de l'app est `theme='light'` — la passe [sombre] tournait EN CLAIR depuis toujours. Corrigé, **150/150**, et la moitié des contrôles mesure enfin ce qu'elle annonce. · Juges repris : `redteam_tokens` (46/46), `redteam_ecrans`, `redteam_tonsurton` (26/26, la crête). Batteries : écrans 150 · tonsurton 26 · vide 61 · champ 32 · repérage 16 · toile 17 · accueil 22 · nuée 38 · tokens 46 · aura 64 écarts (tous antérieurs). · **MESURÉ, RIEN POSÉ — la sphère** : 27,9 % de la surface est à la couleur de la peau, et **les trois leviers évidents l'aggravent** (épaisseur → 30,8 et 32,3 % · nombre → 29,3 % · opacité → 53,2 %). Le peintre normalise ; les trois essais sont défaits, la sphère est exactement comme avant. Le levier est dans `atlasAlpha` — Q255. |
| 21 sept. | **Le jaune sort · le visage se fige · le garde-fou du sol** (sauvegarde `app-avant-lot-v8.html`, `9e09e522…`) | `50902883…` | **Le jaune #FFD447 est retiré SOUS SES TROIS FORMES** — 36 occurrences, dont 10 triplets `[255,212,71]` ; le jeton `--c-bleu68` n'existe plus. Le clair d'« en cours » devient **#A77CF7, le violet que le jeu portait déjà** (`--c-mauve63`) : ΔE 30 du lilas, 41 du bleu, 58 du rose. **Ma règle de Q238 était fausse** — « le clair d'un état est la valeur qu'il remplace » ramenait ici une couleur retirée ; elle devient « de la FAMILLE de son état, à ΔE 25 minimum des trois natures ». **La direction bleu-violet est fermée, mesuré** : 31° seulement entre le bleu Promi et le lilas, et le seul bleu-violet qui passe ΔE 25 est à ΔE 3-11 du périwinkle retiré. · **`_BPAL` = l'identité seule** (le vermillon sort aussi : un visage ne porte pas un état) · **`USER.seed` figé** (`_grainePropre` : sauvegardée, sinon dérivée du nom — même parade que les dalles le 13 sept. ; ⚠ une DÉCLARATION de fonction, `USER` est construit 960 lignes plus haut) — 3 chargements, une seule graine · **`--ghost-ink` #8FA0FF → #C8BAA4** (teinte claire neutre) et un `CREME` périmé (#F4EEE1) corrigé dans le module de l'Aura · **LE GARDE-FOU DU SOL** : il se décale en gardant sa teinte jusqu'à ≥ 42 (§3) de la page ; on vise 44, la marge de 0,7 est mesurée. Balayé sur **21 palettes × 2 thèmes : 0 sous le seuil sur 42 mesures**, la plus faible Taciturne sombre **43,0** contre **10,4** sans garde-fou (`scratchpad/balaye20.py`). · **Juges repris au niveau de la décision** : `redteam_tokens` (46/46, **41/46 sur la version d'avant**, + deux contrats neufs « #FFD447 et #8FA0FF ne reviennent nulle part, sous leurs trois formes »), `redteam_ecrans` (150/150), `releve-aura` — la cote boule ↔ page (76/116 ± 8, calibrée sur le bleu) devient **un plancher de 42**, elle n'avait plus de sens depuis que le sol suit la palette. Batteries : écrans 150 · tonsurton 26 · champ 32 · vide 61 · toile 17 · accueil 22 · repérage 16 · cercle 34 · nuée 38 · dalle 4 · studio-geste 13 · tokens 46 · aura 64 écarts (base 65). · **PROPOSÉ, NON POSÉ** : `PLANCHE-PROPOSITIONS.html` — six clairs d'« en cours » (3 rouge-violet, 3 violets profonds) et **cinq ocres** (#6D3908 · #5D3703 · #74300B · #583613 · #694714) rendus sous les trois champs, dans les **deux partis** (corps plein / corps clair avec l'ocre dans le texte). **`#6B4630` reste en place jusqu'au choix de Tom.** **Vu, non pris :** la dalle « rapporter le livre » à ΔE 11,8 en sombre (défaut aléatoire du chantier 59, pris à ce passage). |
| 20 sept. | **L'Aura : la légende et le sol** (sauvegarde `app-avant-lot-AURA-2.html`, `17e7f0ea…`) | `9e09e522…` | **La légende** 13 → 15 px (niveau « libellé » du §6), pastille 8 → 9, `K.lgH` 16 → 18 — `K.lgY` se DÉDUIT de `lgH`, donc l'air reste égal par construction : **27,00 / 27,00**, cinq phrases × deux thèmes. À l'encre il reste **2 px** (36 / 34, contre 36 / 35 avant) — Gilbert se pose bas dans sa boîte, et `lgH` ne peut pas le rattraper (essayé 19 et 20 : la boîte monte de 0,5, l'encre redescend de 0,5). Q244. · **Le sol de la sphère prend la palette du Studio** — le ton dominant C1, décalage de teinte compris ; `natureMaj` ne colore plus rien mais reste publiée · la fourrure se repeint au changement de palette (`onPaletteChange` ENVELOPPÉ, la couleur du sol n'est pas dans la clé de cache du peintre). · **LA FRONTIÈRE, MESURÉE et non lue** (`scratchpad/frontiere.py`, `sol_suit.py`, trois palettes éloignées) : le sol BOUGE (ΔE 42,2 et 33,2) ; les îles, les dalles de « Ce que tu as tenu », les pastilles de la légende, les arcs des Noyaux et les libellés d'état rendent **une seule valeur distincte sur trois palettes**. **Aucun élément d'état ne prend une couleur du Studio.** Seul `#kLegend` (ancien Karma) peint encore des états en couleurs de NATURE — il est masqué, résidu mort. Q245. · **Juge repris au niveau de la décision** (`sauvegardes/releve-aura-avant-AURA2.py`) : la cote de la légende 589/16 → 588/18 + sa taille décidée en dur (15 px) ; le contrat « le sol porte la nature majoritaire » devient « le sol porte le ton dominant de la palette » ET, par l'autre bord, « changer la nature ne change PLUS le sol ». Prouvé : sur la version d'avant, 4 écarts de position et 3 de données contre 2 et 1 après. `releve-aura` revenu à sa base (2 · 58 · 1 · 2 · 2, tous antérieurs). Batteries : écrans 150 · vide 61 · toile 17 · accueil 22 · cercle 34 · studio-geste 13. **Vu, non pris :** l'écart boule ↔ page cesse d'être une constante — balayé sur 8 palettes, de **10,4** (Taciturne) à **156,2** (Primesautier) en sombre : sous les deux palettes les plus sombres **la boule se fond dans la page**, et la calibration de Q210 ne garantit plus rien hors du bleu · `USER.seed` est tiré au hasard à chaque chargement (`Math.random`, jamais sauvegardé) : **ton propre avatar change de couleurs à chaque ouverture de l'app** — même famille que la dalle tirée au hasard, corrigée le 13 sept. |
| 20 sept. | **La palette v7 + six défauts + la sphère** (sauvegardes `app-avant-lot-v7.html` `46f7b1e0…`, `app-avant-lot-C.html`, `app-avant-lot-B.html`, `app-avant-lot-D.html`) | `17e7f0ea…` | **Couleurs (v7)** : encre du clair arrêtée à `#201908`, fond sombre `#100D0B` (l'échange de la v4 abandonné) · trois bruns étagés `#201908` / `#43291C` / `#6B4630` (marches 10,3 et 13,9 de L*) · le violet quitte l'encre, le vert quitte la surface · « en cours » `#291547` et « tenu » `#00341A`, chacun avec SA valeur claire pour le fond sombre — le jaune `#FFD447` et l'amande `#8FE08F`, c'est-à-dire la valeur que l'état remplace (un transport du violet donnait ΔE 8 du lilas Nuée : même teinte) · le corps d'une fiche tenue prend le brun surface, encre inversée en crème, marques en amande (clôt Q217) · audit des TROIS formes : l'ancien orange peignait encore 14 accents par `--c-orange42`, et 6 triplets `[240,122,46]` vivaient en JS · **Palette d'identité par défaut** : « Signal » (bleu · rose · lilas · crème dalle), 21ᵉ et première du rail ; `_BPAL` perd ses deux reliquats · **Six défauts** : recherche 270 → 278 (écart au tri 20 → 12, Index et Fil) · le flou des Noyaux de l'Aura remplacé par une opacité (2,4 px sur un trait de 6 px auréolait) · le mot-marque de la page + suit `data-kind` par observateur · les trois mots de nature passent en PromiLate sur les cartes (cotes remesurées 73 · 81 · 57 ; sur les FICHES ils y étaient déjà, mesuré) · **le geste de couleur du Studio écrit** (appui 480 ms, horizontale = teinte, verticale = palette — clôt Q125/Q135) · Q234 répondu au glyphe : `→`, `ô`, `è`, six phrases du trait, aucun titre · **Sphère** : le régulateur n'appliquait JAMAIS sa vise (`#auraScreen` ne perd jamais `.show`) — appliqué au retrait, et seul l'appliqué est persisté ; 110 000 → 75 000 → 90 000 → 110 000 sous ×8 puis relâché · le velours ne revient pas avec la palette (même image au pixel) et ma cause d'avant était fausse — Q243. Jeu régénéré (246 fixes, 31 rôles) + Swift. **Juges repris au niveau de la décision** : `redteam_tokens` (44/44, 31/44 sur la version d'avant), `redteam_reperage` (16/16, 12/16 avant), `redteam_tonsurton` (26/26, deux valeurs ajoutées), `juge_studio_geste` neuf (13/13). Batteries : écrans 150 · vide 61 · toile 17 · geste 13 · verbe 6 · phrase 6 · filets 0 · champ 32 · tonsurton 26 · tokens 44 · repérage 16 · dalle 4 · nuée 38 · accueil 22 · tuiles 64 · gens 38 · cercle 34 · polices 0 · redteam 14/15 et redteam3 17/18 (rouges d'avant, PromiLate). **Vu, non pris :** 4 textes ton sur ton sur le Fil en sombre (Δ6 et Δ7, antérieurs) · `--ghost-ink` peint encore en `#8FA0FF`, un périwinkle qui n'existe plus · `PKEYS` nomme 5 palettes absentes de `PALS`. **releve-design et redteam_air non passés : Tom ne les a pas ouverts.** |
| 18 sept. | **La loi de contact de la sphère** (sauvegarde `app-avant-lot-matiere-contact.html`) | 75f78a3d… | Cède puis résiste (62 % en τ 0,05 s, le reste en τ 0,50 s), profondeur 0,46 × pulpe (0,58), retour τ 0,15 s (1,35), empreinte retirée à p 0,0004 · creux vivant après lâcher 3,8 s → 0,6 s · `releve-aura` : contrat 4 réécrit (original `sauvegardes/releve-aura-avant-contact.py`, 3 rouges sur la loi d'avant), acquis 8/8, dernier pas 0,32 niveau · Q235. Couleurs et densité : mesurées, rien touché — Q236, Q237. |

## ⚑ POINT DE REPRISE · fin de session, 21 sept. 2026 (lots v16 à v19)

> `app.html` `1079910d…`. Lignes au journal ci-dessus ; décisions **Q290 à Q300**.
> **Figés le 21 sept. (Tom)** : `releve-design` et `redteam_air` — ils protègent de nouveau. Toute nouvelle
> différence est une régression jusqu'à preuve du contraire.

### La suite — dans une session neuve
**L'onboarding, refait entièrement, avec l'idée du premier trait.** Point de départ prêt :
**`onboarding-depart/ONBOARDING-POINT-DE-DEPART.md`** (ce qui existe, ce que Tom a décidé, les quatre questions à lui
poser une par une, les règles, le juge à écrire d'abord). Puis, dans l'ordre de CHANTIERS : le Fil en ligne de temps,
les visages, la dalle floue de la page +, erreurs et chargement avec Firebase, la main de l'autre, VoiceOver.

### Ce qui reste ouvert
| | quoi | où |
|---|---|---|
| **aléatoire** | la parité clair/sombre des îles de la Pelote (`releve-aura`, « les dalles se noient ») rate sur certains tirages du sol — aucune île sous le plancher (ΔE ≥ 18) ; en clair le masque ne prédit pas l'écran | Q297, Q182 |
| **juriste** | chiffrement App Store × CC BY-SA ; notre WOFF2 de Gilbert ; la licence de PromiLate, inconnue | Q295 |
| **à fixer** | le numéro de version (« Promi · 0.16 ») | Q294 |
| **à brancher** | « Se déconnecter » appelle `window.promiDeconnexion` — avec Firebase | Q294 |
| **dette de juge** | `redteam_nuee` 94 (88 avant v16 : +6 = les cartes du fil qui grandissent pour deux lignes) ; `releve-S3-page-plus` porte encore « Bricolage 700/18.5 » pour le mot de trace (PromiLate depuis le 18 sept.) | — |
| **vu** | un prénom accentué tombe en Gilbert dans une phrase du trait en capitales | Q291 |
| **caduc** | les propositions de palette et d'icône (tranchées : Ingénu, curseurs) | Q292, Q293 |

---

## ⚑ POINT DE REPRISE · lot v16 (21 sept. 2026)

> Lot des décisions de Tom sur l'audit : ligne du journal ci-dessus, décisions **Q290 à Q296**.
> **À trancher par Tom :** la palette par défaut (Q292), l'icône des Réglages (Q293), les mots neufs (Q294),
> le numéro de version. **Pour un juriste avant publication :** Q295 (chiffrement App Store × CC BY-SA, notre
> WOFF2 de Gilbert, licence de PromiLate inconnue).
> **La suite** est dans CHANTIERS, en tête : onboarding (le premier trait), Fil en ligne de temps, visages, dalle floue
> de la page +, erreurs/chargement avec Firebase, la main de l'autre, VoiceOver.
> `releve-design` (80) et `redteam_air` (29) : **NE PAS FIGER** sans le feu vert de Tom.

---

## ⚑ POINT DE REPRISE · 23 septembre 2026, fin de session

> **`app.html` `138ed3f1…`.** Trois lots ce jour — **v12** (le filet collé, Le Cercle, le Fil,
> trois palettes), **v13** (le Fil, le Chiche, la Pelote, les titres, la colonne de l'Aura, le
> partage), **v14** (Mon Folio, la Pelote dans l'image). Sauvegardes : `app-avant-lot-v12.html`,
> `app-avant-lot-v13.html`, `app-avant-lot-v14.html`. Lignes au journal ci-dessus.
> Décisions : **QUESTIONS Q276 à Q289**.

### La suite, dans l'ordre donné par Tom

**l'onboarding · le tutoriel · les mondes · les notifications · puis Swift et Firebase.**

### La règle permanente, rappelée le 23 septembre

> *« Vérifie les espacements et la mise en page de chaque élément que tu touches. Rien de mal
> placé dans son cadre, rien de tronqué, rien qui colle à son voisin. C'est la règle, pas une
> consigne de ce lot. »*

### Ce qui reste ouvert

| | quoi | où |
|---|---|---|
| **à trancher** | **la composition de la Pelote sur la Toile** : **A · le coin** (posée) ou **B · le socle** | Q289 |
| **à trancher** | le libellé de l'ex-« CE QU'IL MONTRE » : **DANS L'IMAGE** (posé, et **validé par Tom**) · CE QU'ON VOIT · CE QUE L'IMAGE PORTE | Q284 |
| **feu vert** | **`releve-design` (62) et `redteam_air` (30) — NE PAS FIGER.** Listes inchangées depuis le lot des titres PromiLate | — |
| **ouvert** | la carte d'**Index** garde sa réduction de taille de dernière extrémité ; Tom a dit « jamais de réduction » à propos du Fil. Aucune carte du jeu n'y est réduite | Q281 |
| **ouvert** | **chantier 59** — la dalle tirée au hasard sous le plancher ΔE 15 ; elle se tire plus souvent depuis que le sol de la Pelote prend l'un des QUATRE tons | CHANTIERS |
| **ouvert** | **Q273** — les points du partage antérieurs : la recomposition sans superposition est faite (Q287) ; l'ajout simultané de deux objets n'est pas demandé | Q273 |
| **caduc** | « l'Orbite qui ne s'ajoute pas » : l'objet n'existe plus, la Pelote le remplace | Q283 |

### Vocabulaire arrêté ce jour

**La Pelote** (la boule de l'Aura) · **Mon Folio** (la planche des dalles, au partage) ·
**Ingénu** (la palette par défaut, ex-Avenant — 21 sept.). **« Orbite » et « la sphère » sont bannis** ; « mes dalles »
reste le nom de la Toile.

---

## ⚑ POINT DE REPRISE · 13 septembre 2026, fin de session

> **app.html `e4c2d41a…`.** Trois lots ce jour, lignes au journal ci-dessus. Batteries toutes vertes en série au dernier lot.
> Tom garde tels quels : « Moi » dans « qui tu défies », et les personnes qui persistent d'une page + à la suivante.
> Méthode : journal d'une ligne par lot, QUESTIONS.md = décisions seulement (Q211 la dernière).

### Ce qui reste ouvert

**Remplacé le 14 sept. 2026 par `CHANTIERS.md` § « État au 14 septembre » — le seul relevé à jour.** Depuis cette liste : 59, 76, 71, 60, 62, 78, 79 fermés ; `redteam_gens` est dans la liste des batteries du §7.

---

## ⚑ POINT DE REPRISE · 12 septembre 2026, fin de session

> **app.html — `dcd533b76a42…` → `009de5e5c1f9d759e5b169de46eec40c`.** Sauvegardes de la session, dans l'ordre où elles ont été prises :
> `app-avant-src-valide.html` · `app-avant-ch59.html` · `app-avant-ch58.html` · `app-avant-ch73.html` ·
> `app-avant-q210.html`. Juges d'origine : `sauvegardes/releve-aura-avant-q210.py`,
> `sauvegardes/verif_seuil-avant-cercle-toile.py`.

### Ce qui a été fait, dans l'ordre de la file de Tom

1. **Les trois preuves obsolètes, réécrites** — `preuve_vend.py` (16/16 + 2/2 statiques), `preuve_vide.py`
   (8/8 + 2 contrats pris sur la vraie version fautive), `verif_seuil.py` (familles D et G retirées, 11 747
   caractères ; A·B·C·E·F à 0 raté). **Un défaut réel trouvé au passage** : la collection de dalles de
   l'écran qui vend **survivait à la disparition des Promi qui l'avaient bâtie** → `srcValide()`.
2. **Chantier 76 noté** — le crème que le moteur peint entre les motifs (gravure 76,4 % … pixel 0 %),
   masqué par le recouvrement, cause dans le moteur (§9).
3. **59 · la dalle illisible** — ◐ **sombre fait** (0 sur 10 chargements contre 7 sur 8 avant) ;
   le clair est réglé par **Q210** ci-dessous. Trois critères essayés, deux jetés sur la mesure.
4. **75 · redteam_verbe en sombre** — ✕ **le chantier n'existait pas** : c'étaient mes Playwright concurrents.
5. **64 · 67 · 70** — ✔ tenaient déjà (0 raté chacun), rien à refaire.
6. **58 · `frame()` sur douze écrans** — ✔ **65,87 % → 0,00 %** du fil principal sur l'accueil ; écritures
   sur les écrans fermés **7 227 → 0** ; l'écran ouvert inchangé. `.show` seul aurait éteint l'ombre du Fil
   (il s'ouvre avec `.in`) — vérifié avant d'écrire la parade.
7. **Le téléphone** — ▸ **PAS FAIT, je n'ai pas d'iPhone.** Tout est mesuré au bridage CPU du CDP, déclaré.
8. **73 · l'élan sur appareil lent** — ✔ **tranché et corrigé** : ce n'est pas la charge, c'est **l'écart
   entre deux mouvements** (0,00 rad/s dès 120 ms → 7,40 / 4,44 / 2,78 après). → **chantier 77**, portage Swift.
9. **Q210 · le sol du clair** — ✔ **A, fait et mesuré** : le poil du clair s'assombrit (la nature ×0,38,
   teinte gardée), la peau va au crème. **0 île sous le plancher sur 8 chargements** (4 sur 10 avant).
   **La cote du juge est recentrée de 85 à 116** (§7, au niveau de la décision) — c'est le seul point à
   revoir avec Tom ; s'il ne veut pas de ce 116, on revient à `app-avant-q210.html` (voie C).

### L'état des batteries, toutes passées EN SÉRIE après le dernier lot

`releve-design` 0 écart · `redteam_ecrans` 150/150 · `redteam` 15/15 · `redteam2` 10/10 · `redteam3` 18/18 ·
`redteam_demande` 19/19 · `redteam_toile` 17/17 · `redteam_geste` 13/13 · `redteam_verbe` 6/6 ·
`redteam_filets` 0 parasite · `redteam_vide` 61/61 · `redteam_air` 436 paires intactes · `redteam_champ` 32/32 ·
`verif_cercle` 89/89 · `verif_64`/`verif_67`/`verif_70` 0 raté · `releve-aura` **AU VERT, deux thèmes**.

### Ce qui reste OUVERT — la liste, par ordre de ce qui bloque

| | Quoi | Où |
|---|---|---|
| **77** | **⚑ PORTAGE SWIFT, PRIORITAIRE** — le geste se perd quand les événements s'espacent, et Chromium le cache (Safari n'a pas `getCoalescedEvents`). En UIKit : `UITouch.timestamp` + `coalescedTouches(for:)`, et jamais de fenêtre de vitesse calibrée à 60 images/s. | CHANTIERS n° 77 |
| **—** | **LE TÉLÉPHONE (iPhone 12, A13)** — non fait. À vérifier en premier : à quelle cadence iOS livre les `touchmove` quand le fil est bloqué (ça dit où l'on tombe dans le tableau du 77) ; puis la densité de la Pelote. | CHANTIERS n° 73, n° 77 |
| **59** | Le résidu du **sombre** : la cession de teinte décide sur le masque, dont le rapport à l'écran descend à ×0,48 — **1 dalle sur les 8 derniers chargements** est encore passée sous le plancher (13,7). Ce n'est pas une garantie. | CHANTIERS n° 59 |
| **76** | Le **crème que le moteur peint** entre les motifs (jusqu'à 76,4 %) — masqué par le recouvrement de l'écran qui vend, pas supprimé. Ressortira dès que la densité baissera. **Cause dans le moteur (§9)**. | CHANTIERS n° 76 |
| **74** | Quatre portes mènent au Cercle depuis un état vide — **à trancher par Tom** : lesquelles doivent exister avant le premier Promi. | CHANTIERS n° 74 |
| **71** | Les numéros du jeu de démonstration changent d'un chargement à l'autre (le jeu passe deux fois sur trois chargements sur quatre). | CHANTIERS n° 71 |
| **62 · 60 · 61** | L'aide de la page + sous les pinceaux · « à le groupe » · les libellés de cartes contre le §6. | CHANTIERS § 4 |
| **Q210** | **La cote boule ↔ page du clair est passée de 85 à 116.** Recentrée sur ta décision A — à confirmer ou à annuler (voie C). | QUESTIONS · Q210 |
| **Q182** | Reste ouverte pour le reste de la Pelote en clair, mais son point dur (les îles) est réglé par Q210. | QUESTIONS · Q182 |

---

## ⚑ LA FILE DES CHANTIERS · 12 septembre 2026 — 59 · 75 · 64 · 67 · 70 · 58, puis le téléphone et 73

> **app.html `f6bced35e9b7…` → `dcd533b76a4291203684d40c517e5080`.**
> Sauvegardes, dans l'ordre : `app-avant-src-valide.html`, `app-avant-ch59.html`, `app-avant-ch58.html`,
> `app-avant-ch73.html`. Batteries toutes au vert, **en série** : `releve-design` 0 écart · `redteam_ecrans`
> 150/150 · 15/15 · 10/10 · 18/18 · `demande` 19/19 · `toile` 17/17 · `geste` 13/13 · `verbe` 6/6 ·
> `filets` 0 parasite · `vide` 61/61 · `air` 436 paires intactes · `champ` 32/32 · `verif_cercle` 89/89.
> `releve-aura` : **1 écart, et c'est le résidu déclaré du chantier 59 en thème clair** (une dalle sous le
> plancher ΔE 15 quand le tirage tombe mal, 4 chargements sur 10).

### Les trois preuves obsolètes — réécrites, pas laissées au vert sur du vide

- **`preuve_vend.py`** : 16 sondes, une page par sonde, chacune visant un contrat — plus `statique_fautive()`,
  qui écrit un `app-preuve-decoupe.html` avec un `drawImage` à 9 arguments et un `getImageData` injectés.
  **2/2 contrats statiques PRIS · 16/16 contrats visés PRIS.**
- **`preuve_vide.py`** : réécrite pour l'état `pc-sans`. 8 sondes dans les deux thèmes, **8/8 PRISES**, plus
  **2 contrats pris sur la VRAIE version fautive** (`app-avant-src-valide.html`).
  ⚑ **Elle a trouvé un défaut réel au passage** : `cleCollection()` ne portait que palette·teinte·thème, donc
  la collection de dalles **survivait à la disparition des Promi qui l'avaient bâtie** — on vidait `promises`,
  `TODO` restait, l'écran posait encore des dalles d'ids SUPPRIMÉS et `pc-sans` n'était jamais posée. Le
  commentaire de `prepare()` annonçait « la classe suit les DONNÉES » : elle suivait un cache. Corrigé par
  `srcValide()` — la collection se rebâtit dès qu'un de ses ids source disparaît, et **planter ne l'invalide
  pas** (sinon la première ouverture retomberait aux 3 dalles du minimum vital, le défaut déjà mesuré).
- **`verif_seuil.py`** : familles **D et G RETIRÉES** (11 747 caractères), elles mesuraient `#plCadre`,
  `.plv-dal`, « 29 € », `plv-sans` — des nœuds qui n'existent plus. A, B, C, E, F gardées, **0 raté**.
  L'en-tête pointe vers `verif_cercle.py`. Original : `sauvegardes/verif_seuil-avant-cercle-toile.py`.
  ⚠ La famille E héritait du `setPremium(false)` que D posait : elle le pose elle-même maintenant.

### Ce que la file a donné, chantier par chantier

| | État | Le chiffre qui compte |
|---|---|---|
| **59** la dalle illisible | ◐ **fait en sombre, pas en clair** | sombre **0 dalle sous le plancher sur 10 chargements** (7 sur 8 avant) · clair **4 sur 10, inchangé** → **Q210** |
| **75** redteam_verbe en sombre | ✕ **le chantier n'existe pas** | 6/6 sur **quatre** versions au repos, 8/8 sous bridage ×1 à ×10 |
| **64** bandeau + rond photo | ✔ tenait déjà | `verif_64` **0 raté** |
| **67** pastilles de LE TRAIT | ✔ tenait déjà | `verif_67` **0 raté** |
| **70** la cause des rebâtissages | ✔ tenait déjà | `verif_70` **0 raté** |
| **58** `frame()` sur douze écrans | ✔ **fait** | **65,87 % → 0,00 %** du fil principal sur l'accueil ; écritures sur les écrans fermés **7 227 → 0** |
| **73** l'élan sur appareil lent | ✔ **tranché et corrigé** | **0,00 → 7,40 / 4,44 / 2,78 rad/s** dès 120 / 200 / 320 ms entre deux mouvements |
| le téléphone | ▸ **pas fait — je n'ai pas d'iPhone** | tout ce qui précède est mesuré au bridage CPU du CDP, déclaré comme substitut |

### Chantier 76, noté : le crème que le moteur peint entre les motifs

Part de pixels à la couleur du fond crème **à l'intérieur** d'une dalle, en clair : gravure **76,4 %** ·
braille 71,7 % · sillons 70,1 % · terrazzo 64,8 % · touffe 46,7 % · mosaïque 34,1 % · encre 24,9 % ·
**pixel 0 %**. Ce n'est pas une transparence — le moteur PEINT le crème, donc rien posé dessous ne remonte.
Sur l'écran qui vend, le vide ne tombe à 1–6 % que parce que **140 poses se recouvrent** : le crème est
masqué, pas supprimé. **La cause est dans le moteur (§9) : rien sans autorisation.**

### Les deux leçons d'instrument, inscrites au §8 de CLAUDE.md

1. **Un instrument qui ralentit avec la machine fabrique de faux chantiers** — deux le même jour (75, et la
   prémisse de 73). Un geste s'injecte par le CDP, avec un horodatage par événement.
2. **Chromium cache le défaut de la cible** : il regroupe les `pointermove` (`getCoalescedEvents`) ; **Safari
   n'a pas cette API**. Toute mesure de geste destinée à l'iPhone se fait regroupement éteint.


## ⚑ L'ÉCRAN QUI VEND, REFAIT AUTOUR D'UNE TOILE DE DÉMONSTRATION · 12 septembre 2026

> **app.html `3ac4975ccaed…` → `83771993d9a30c67dd8424be03431093`** · sauvegarde `sauvegardes/app-avant-cercle-toile.html`.
> **`lot-CERCLE-VEND` est RETIRÉ, pas neutralisé** — vérifié à zéro occurrence de `lot-CERCLE-VEND`, `plCadre`, `plv-dal`,
> `plv-prix`, `_vendDalles`, `_vendSans`. Le lot neuf : `lot-CERCLE-TOILE-css` + `lot-CERCLE-TOILE`, en fin de fichier.
> **Le juge porte la décision** : `releve-aura.py` passe à `AUTO_DECIDE = 2π/100` (original `sauvegardes/releve-aura-avant-100s.py`).

**La composition**, cotes mesurées, écran 390 × 844, **aucun défilement** : le ✕ FERMER **du produit** (`.enh > .closeb`, 265,5 / 62,5)
· la Toile 22 / 98, 346 × 206, rayon 28, filet de 2 px en halo · « Rejoins le **Cercle** ! » à 336, Fraunces 600 · 32, « Cercle » en
mauve `#8A5CF0` (écart de luminosité 126 en clair, 91 en sombre), le « ! » en encre · le sous-titre à 382, ApfelMid 500, sans couleur
· trois arguments à 434 / 488 / 542, libellés **Bricolage 600**, détails Apfel 400 · « 39 € » à 612 en Fraunces 600 · 40 · le CTA
framboise à 680, 346 × 58, **seconde couche en mauve**, chevron du produit · l'option à 756, fond mauve avec la seconde couche de
l'encart signature, texte mauve · le légal à 816. Le point le plus bas : 830.

**LA TOILE — des dalles qui se superposent, et rien d'autre.** Trois architectures ont été essayées et deux rejetées, chaque fois sur
mesure, jamais à l'œil :
1. **des dalles posées sur un panneau** → clairsemé ; ce n'était pas une Toile.
2. **un pavage dense** (jusqu'à 448 cellules, chacune un rendu du moteur découpé sur son polygone exact) → à 12,6 px de cellule les
   motifs du moteur, **ancrés en coordonnées absolues** (braille 9, mosaïque 11, sillons 6, pixel 5), n'y tiennent qu'en fragment et
   **le fond paraît davantage** : 70 % des pixels couleur de la page en clair. Densifier aggravait le défaut.
3. **RETENU — une collection de vraies dalles, posées en se recouvrant.** `dalleTrame(cv, id, k, monde)` rend chaque dalle **à sa
   taille finale** (3 Promi × 8 mondes = 24 dalles, de ~68 × 56 à ~100 × 92), et on la **pose** 140 fois : position, rotation et ordre
   tirés à chaque ouverture. **Aucune dalle n'est redimensionnée à la pose** — on la dessine à la taille que le moteur lui a donnée.

**L'ORDRE EST UNE DÉCOUVERTE DU LOT, et c'est lui qui rend le pavage lisible.** La superposition crée une hiérarchie : les dernières
posées cachent les autres. Donc les mondes qui **remplissent** vont dessous (Encre, Terrazzo, Pixel, Mosaïque — ils tuent le fond), les
mondes à **lignes** ensuite (Braille, Sillons, Gravure), et la **Touffe au-dessus** — elle est ajourée, elle ne se lit que **posée sur de
la couleur**. « Plus de Touffe » veut donc dire : plus de poses dans la couche du haut. Elle est à **28,6 %** (34 % était un cran de trop).

**Mesuré** : fond visible **3 à 6 %** · **66 à 108 teintes** (quantification grossière) · les **huit mondes** présents à chaque ouverture
(forcé : sans garde-fou le tirage pondéré en oubliait un — Gravure tombée à 1 puis à 0) · trois ouvertures et trois sessions **toutes
distinctes** · les poses coûtent **1 à 6 ms**.

**LE PRIX, ET OÙ IL A ÉTÉ DÉPLACÉ.** La collection ne dépend ni de l'ouverture ni des poses — seulement du thème et de la palette — donc
elle se bâtit **une fois, au démarrage, en fond**, par tranches, **sous `requestIdleCallback`** : elle n'entre jamais en concurrence avec
le fil principal. Mesuré, processeur ralenti ×1 / ×4 / ×6 (substitut de Lighthouse, **pas un appareil**) :

```
                                      sans le lot    tout de suite    collection prête
démarrage jusqu'à Toile vivante  ×1      1 593 ms         1 487 ms
                                 ×4     13 020 ms        13 409 ms
ouverture du Cercle              ×1        622 ms           788 ms          510 ms
                                 ×4      1 764 ms         2 167 ms        1 346 ms
                                 ×6            —                —        1 984 ms
```

**Le démarrage n'est pas retardé, et une fois la collection bâtie l'écran s'ouvre plus vite qu'avant.** Le prix d'une dalle selon sa
taille (×4) : 74,6 ms à 50 de côté · 219 ms à 90 · **450,8 ms à 130** · 614,9 ms à 150 — c'est ce tableau qui a imposé 24 dalles de 100
et non 48 de 130 (qui faisaient **21,6 s** de calcul et une ouverture à 17–27 s).

**QUATRE DÉFAUTS TROUVÉS ET CORRIGÉS DANS LE LOT, tous de moi :**
- **`Toile.sync(ids)` appelé par mon lot** réattribuait les dalles quand il passait avant la liaison de l'app. Pris par `redteam_toile` :
  « les dalles sont aux bonnes positions » **7/10 avant → 5/10 avec**, écarts de 500 px. Mon lot ne touche plus à la liaison ; il attend.
- **le bâti de fond volait le fil principal** (~100 ms toutes les 260 ms, 38 %) : `redteam_verbe` tombait de 3/6 à **0/6**, la page +
  rendant des hauteurs NULLES. Passé sous `requestIdleCallback`.
- **rien ne reposait le pavage entier à la fin de la cascade** : le canevas gardait la dernière image du balayage, voile encore fermé —
  pavage composé à 100 %, écran à **1 %**. L'état final ne dépend plus de l'instant où la boucle s'arrête.
- **le choix des Promi était déterministe** (`ids[(i*7)%n]`) : si leurs dalles portaient la même couleur, **toute Toile sortait
  monochrome**, à chaque session. Ils sont maintenant répartis, départ tiré par session.

**LA SÉRIE, en série, sur `83771993`** : redteam_ecrans **150/150** · redteam 15/15 · redteam2 10/10 · redteam3 18/18 ·
redteam_demande 19/19 · redteam_toile **17/17** · redteam_geste 13/13 · redteam_filets **0 filet parasite** · redteam_vide 61/61 ·
redteam_air **intact** (436 paires) · redteam_champ 32/32 · redteam_polices **0 couple absent** · **releve-design : AUCUN ÉCART**.
**Deux rouges, prouvés PRÉEXISTANTS en repassant la batterie sur la sauvegarde :** `redteam_verbe` **3/6** (le sombre était déjà rouge
— chantier 75) et `redteam_tonsurton` 24/26 + `releve-aura` 2 écarts, qui **nomment la dalle** « planter un arbre » à ΔE 12,1 —
**défaut du chantier 59, pris à ce passage** (§7 : un rouge qui nomme un défaut tiré au hasard fait son travail).

**LE POINT QUE TOM A DEMANDÉ QUATRE FOIS — LES VRAIES DALLES. Vérifié, et voici la vérification.** Le lot ne contient plus que **deux**
`drawImage` : `drawImage(d.cv, -d.w/2, -d.h/2, d.w, d.h)` — **cinq** arguments, donc aucun rectangle source, et les cotes de destination
sont celles du canevas lui-même (`d.w = cv.width/dpr`) : **aucune découpe, aucun redimensionnement** ; et `drawImage(OFF, 0, 0)` — trois
arguments, la copie 1:1 du pavage composé vers le canevas visible. **Plus aucun `getImageData` ni `putImageData`** : plus aucun choix de
pixels. Les deux seuls appels à `dalleTrame` portent une **échelle `k`** — le moteur peint à la taille finale, y compris pour les trois
pastilles (16 px, canevas 25 × 21 par exemple, affichage au pixel). **Où j'en avais encore, et c'est dit :** dans la version d'avant, la
Toile était composée en **choisissant les pixels** parmi huit rendus du moteur, et les pastilles étaient des **fragments d'image
redimensionnés**. Les deux sont partis. Ce que je déclare quand même : la **rotation** avant la pose rééchantillonne (elle place la dalle,
elle ne change pas son échelle), et la copie `OFF → visible` est un tampon.

**Ce qui reste ouvert :** le crème que le moteur peint lui-même entre les motifs en thème clair (gravure 76,4 % · braille 71,7 % ·
sillons 70,1 % · terrazzo 64,8 % · touffe 46,7 % · mosaïque 34,1 % · encre 24,9 % · **pixel 0 %**) — le recouvrement le masque, il ne le
supprime pas ; et les preuves de l'ancien lot (`preuve_vend.py`, `verif_seuil.py`, `preuve_vide.py`) sont **obsolètes**, le lot qu'elles
gardaient n'existe plus.


## ⚑ LE CERCLE FINI, PUIS LES CHANTIERS 64 · 67 · 70 · 69 · 72 · 11–12 septembre 2026 (nuit), sans arrêt (Tom : « va jusqu'au bout »)

> **app.html `8b3c8cb1…` → `3ac4975ccaed06419950963a8804a212`**, un lot à la fois, chaque lot sous `assert`, sauvegarde avant chacun :
> `app-avant-vend-vide.html` (8b3c8cb1) → `app-avant-64.html` (b7a5bef1) → `app-avant-67.html` (34c2c455) → `app-avant-70.html`
> (aedf74fe) → `app-avant-69.html` (3cbc06b9). Patchs : `sauvegardes/audit-cercle/patch_vend_vide.py`, `patch_64.py`, `patch_67.py`,
> `patch_70.py`, `patch_69.py`. **`releve-design` non figé** (Tom).

**Le Cercle, sans aucun Promi** (Tom : « cache la rangée et remonte le prix ») — la classe `plv-sans` suit les DONNÉES : dalles et
noms cachés, le bloc remonte de 144 (prix 132, année 242, essai 320). Vérifié (deux thèmes) et prouvé (`preuve_vide.py` : la rangée
vide montrée → pris ; l'essai caché → pris ; témoin vert). **Les portes depuis un état vide** (`portes_vides.py`) : l'accueil, les
Réglages, le verrou du Studio, l'aide de l'Aura mènent au Cercle sans passer par un Promi — **chantier 74, à trancher par Tom**. Et
le démarrage neuf n'atteint jamais zéro Promi : le jeu se remplit derrière (chantier 71).

**64 — le bandeau et le rond photo** : Peaufiner de la page + ouvert, le plateau de la page + et le rond photo retirés NOMMÉMENT
(relevé nœud par nœud contre le Peaufiner d'une fiche) ; au repos, rien ne change. `verif_64.py` **16 / 16**, prouvé sur l'app d'avant.
**67 — les pastilles de LE TRAIT** : la rangée à 22 du bas (calculée : ≥ 20 pour tenir 15,19 au coin), symétrique du libellé ;
encre **16,68** (11,14). `verif_67.py` **8 / 8**, prouvé.
**70 — le toucher perdu** : `peaufBati` vidait et rebâtissait la liste à chaque repeinte ; il compare désormais la signature de ce
qu'il bâtit. **0 rebâtissage** (6 + 6 avant), l'encart **20 / 20**, une vraie modification rebâtit toujours. `verif_70.py`, prouvé.
**69 — le pinceau jamais gardé** : `lot-PINCEAU` lit `promises` (le `let`), plus `window.promises` (undefined). De bout en bout : le
Promi né garde « Coulé » / « Peigné », sa fiche l'affiche. `verif_69.py`, prouvé (trait `None` avant).
**72 — les juges qui visent un numéro** : un seul dans les batteries, `releve-fiche-personne` (porte 8, `openDetail(126)`) — réécrit
sur la fiche de Rachel prise par ce qu'elle est, attente sur condition (ouverture mesurée 315–1 413 ms) ; original gardé ; prouvé
par `SONDE_PORTE8`.

**⚠ Une erreur de ma part, corrigée :** j'avais écrit que la fiche 126 était « passée ratée dans la soirée ». FAUX — « faire les
crêpes » est ratée dès le jeu ; ce qui change, c'est son NUMÉRO (126 une fois sur quatre, 142 sinon : le jeu passe deux fois dans
trois chargements sur quatre, `probe_ids.py`). Et « deux tableaux » (chantier 71) était faux aussi : un seul tableau, renuméroté.
Corrigé dans CHANTIERS 71 / 72, ce fichier, et le commentaire de `verif_integration`.
**Mes instruments, encore :** des attentes à DURÉE fixe (un toucher sur la tuile pendant l'animation, perdu — tout attend désormais un
ÉTAT) ; un contrat qui supposait ce que fait « ✕ FERMER » (il referme la feuille, comme avant) ; la barre du bas prise pour un
recouvrement (la liste défile dessous, voulu) ; un repère de symétrie compté hors du trait ; un `scrollIntoView` qui déplaçait la page.

**Série finale sur `3ac4975c…`** (`journaux/bat_final.log`, 23:34 → 00:2x, 24 batteries, une à la fois) : redteam_ecrans **150/150** ·
redteam 15/15 · redteam2 10/10 · redteam3 18/18 · demande 19/19 · toile 17/17 · geste 13/13 · verbe 6/6 · filets 0 · vide 61/61 ·
champ 32/32 · **releve-design ✅ aucun écart** · fonctions 22/22 · polices 0 · superpo 0 recouvrement · **releve-fiche-personne ✅ 258
(porte 8 : 14/14)** · nuee ✅ 24 · S1 ✅ · S2 ✅ 0/0 · S3 ✅ 0 · S4 ✅ · S5 ✅. **Et les vérifications d'écran : `verif_integration`
64/64 · `verif_64` 16/16 · `verif_67` 8/8 · `verif_70` 8/8 · `verif_69` 6/6.**
**Trois rouges, tranchés :**
- **`redteam_air` — 4 paires, toutes sur la carte LE TRAIT d'une Nuée, dans les deux thèmes : le resserrement DEMANDÉ par le
  chantier 67.** `LE TRAIT → Plein` 19 → 11, `Plein → Sec` 15 → 7 : la rangée de pastilles est remontée de 8. La carte gagne son air
  au contour (11,14 → **16,68**) et perd 8 px d'air intérieur — c'est le troc du chantier 67, décidé par Tom. **Référence refigée**
  (avant : `sauvegardes/air-reference-avant-ch67.json`).
- **`releve-aura` — 4 écarts, tous « la matière » : défaut du chantier 59, pris à ce passage** (« rapporter le livre » ΔE 5,9 / 7,0 ·
  « le grand plongeoir » 13,1, plancher 15). Toutes les autres familles à 0 — l'élan est revenu (la machine avait soufflé).
- **`verif_seuil` — 2 contrats : le MIEN, périmé par le chantier 70.** Il exigeait de VOIR au moins un rebâtissage de la zone pour la
  juger (`T and not mauvais`) ; depuis le 70 il n'y en a plus, et « 0 rebâtissage » est le bon résultat. Réécrit au niveau de la
  décision : aucun rebâtissage ne doit laisser la zone mal calée (ce qui est protégé n'a pas changé). **Puis un second faux rouge,
  de ma mesure encore :** « jamais étirée » comparait l'encre peinte à la TAILLE DU CANEVAS source — or une dalle peut laisser une
  marge transparente (Sillons : canevas 1,247, encre peinte 1,315, pour 4 % de tolérance). Le juge REDEMANDE désormais la dalle au
  moteur et mesure LUI-MÊME les deux encres (tolérance 6 % : la matière respire). **Repassé : `verif_seuil` 66 / 66, 0 raté**, et
  `preuve_vend` rejoué — la dalle étirée est toujours prise, le témoin reste vert : la mesure a été corrigée, pas desserrée.

**Tout est vert sur `3ac4975ccaed06419950963a8804a212`**, hors les deux défauts connus et déclarés : le chantier 59 (dalles de
l'Aura tirées au hasard) et le chantier 73 (l'élan à 0 quand les images approchent 100 ms). **`releve-design` n'est pas figé.**
- **La preuve du juge réécrit (chantier 72)** : `SONDE_PORTE8=1` (le disque rendu intouchable) → porte 8 rouge dans les deux thèmes.

## ⚑ L'ÉCRAN QUI VEND PREND LE BAS DE LA PLANCHE · 11 septembre 2026 (nuit) · `lot-CERCLE-VEND-css` réécrit + `lot-CERCLE-VEND`

> **app.html `a543d1e1…` → `8b3c8cb167bbb379defb460f5c02bc39`** (sauvegarde d'avant : `sauvegardes/app-avant-vend-planche.html`).
> Patchs sous `assert` : `sauvegardes/audit-cercle/patch_vend_planche.py` (le libellé de « Prendre l'année », le bloc CSS de ce soir
> réécrit, le script neuf), puis une ligne (l'ombre de dalle du fond). Décision : **Q205** (Tom). **`releve-design` NON figé** (Tom).

**Ce qui est posé.** Le bas de la planche, ses cotes au pixel, remonté sous le plateau à 132 (la cote du premier bloc de la
planche) : **trois VRAIES dalles** (`Toile.dalleTrame(src, id, 1, monde)`, le monde courant avec seul `m` changé — Sillons,
Gravure, Terrazzo ; les trois derniers Promi plantés de l'utilisateur ; une dalle se rend une fois, posée sans être étirée ;
l'app publie `window._vendDalles`), leurs noms, **« 29 € » en Bricolage 700 / 56**, « soit 2,42 €/mois · −39 % », **« Prendre
l'année » plein à 386, « Essayer 14 jours, puis 3,99 €/mois » en contour juste dessous à 464** (les mêmes boutons, déplacés : achats
et chemin « par-dessus » intacts), les deux notes (la seconde perd son opacité .70, sous le plancher du §6). Masqués nommément : le
visuel, le titre, la phrase, les cinq lignes, et **l'ombre de dalle du fond** — vue derrière les dalles À LA CAPTURE (§4, règle 6 :
jamais de dalle en fond animé sur un écran qui montre des dalles de référence ; cet écran seulement). Rien ne défile.
**Lisibilité des dalles, mesurée** (`vend_dalles_de.py`, 8 chargements — les couleurs sont tirées au hasard) : ΔE au fond 66 à 84
en sombre, 48 à 112 en clair (plancher 15).

**Vérifié à l'écran** (`verif_seuil.py`, **62 contrats, 0 raté**, `journaux/verif_vend_planche.log`) — les contrats de l'écran qui
vend **réécrits au niveau de Q205** (original `verif_seuil-avant-vend-planche.py`) : les trois vraies dalles dans l'ordre · chacune
peinte, à sa cote, **jamais étirée — la boîte PEINTE mesurée par le juge sur l'alpha**, pas la déclaration de l'app (§7) · « 29 € » en
grand · « Prendre l'année » en premier, l'essai visible dessous, sans défiler, au doigt · chaque texte lisible (min 4,95) · les deux
boutons se voient (215 / 217) · plus de visuel ni d'ombre · les cotes de la planche, jamais « offert ».
**Prouvés, un par un** (`preuve_vend.py`, deux thèmes, une page neuve par sonde) : une dalle étirée, une dalle vide, « 29 € » à 40,
l'essai poussé hors de l'écran, une note à la teinte du fond → **chacun pris par SON contrat** ; le témoin sans sonde, vert. Et sur
l'ancien écran (`app-avant-vend-planche.html`) : « ABSENT », deux thèmes.
**Captures regardées** (`seuil/*_vend_haut.png`, `vend/planche_*`) : la première passe a montré l'ombre derrière les dalles — retirée,
recapturée propre dans les deux thèmes. **À voir par toi :** le bloc tient le haut de l'écran ; ~250 px restent libres sous les notes.
**Mes instruments :** la mesure plantait sur une version fautive (elle DIT « absent » désormais) et sur une page + qui ne s'ouvre pas
(rouge nommé) ; trois espaces insécables tapées telles quelles dans le juge ; deux navigateurs à la fois font dépasser 30 s au
chargement ce soir — tout s'enchaîne désormais un navigateur à la fois.

**Batteries en série sur `8b3c8cb1…`** (`journaux/bat_vend_planche.log`, 21:06 → 21:56) : redteam_ecrans 150/150 · redteam 15/15 ·
redteam2 10/10 · redteam3 18/18 · demande 19/19 · toile 17/17 · geste 13/13 · verbe 6/6 · filets 0 · vide 61/61 · **air ✅ 436 paires**
· champ 32/32 · **releve-design ✅ aucun écart** (il ne relève pas l'écran du Cercle — rien à figer de ce côté) · fonctions 22/22 ·
polices 0 · superpo 0 · nuee ✅ 24 · S1 ✅ · S2 ✅ 0/0 · S3 ✅ 0 · S4 ✅ · S5 ✅. **Trois rouges, tranchés un par un :**
- **`verif_integration` (62 ✓ / 2 ✗, clair) — l'achat depuis le mur de la page + n'a pas eu lieu : défaut du chantier 70, pris à ce
  passage.** Rejoué seul (`repro_achat_pp.py`, 10 essais par thème) : **écran refait 19 / 19**, app d'avant le lot 18 / 19 — le raté,
  encart DÉTACHÉ sous le doigt, l'écran qui vend jamais ouvert. Les boutons déplacés répondent ; le toucher perdu est antérieur.
- **`releve-fiche-personne` (256 / 258) — porte 8 « le disque de Rachel sur une fiche », deux thèmes : le JUGE, pas le produit.**
  Il ouvre la fiche 126 en dur — et 126 n'existe qu'une fois sur quatre : les numéros du jeu changent d'un chargement à l'autre
  (chantier 71 ; ⚠ j'avais d'abord écrit « passée ratée dans la soirée » : faux, « faire les crêpes » est ratée dès le jeu) ; **mêmes deux écarts sur l'app d'avant le lot**
  (`journaux/fiche_personne_avant.log`). Chantier 72. Batterie non touchée dans ce lot.
- **`releve-aura` (4 écarts) — la MACHINE, pas le lot : tranché par quatre passes alternées, seules** (avant · actuelle · avant ·
  actuelle, `journaux/aura_alt*.log`). La médiane par image monte à chaque passe, quelle que soit la version : **20,7 → 24,4 → 26,2 →
  28 ms** (palier 75 000 partout, contre 110 000 plus tôt dans la soirée), et **l'app d'AVANT le lot, à la 3ᵉ passe, prend les mêmes
  rouges** (élan à 0, lancer qui ne comble pas, sphère pas pleine en clair, boule à 76,7, dalles illisibles). Aucun chemin de l'écran
  qui vend vers l'Aura : `releve-aura` n'ouvre jamais le Cercle, et ses dalles ne se peignent qu'à l'ouverture de son écran. Les
  dalles illisibles restent le **chantier 59**. **Constat, hors lot : l'élan tombe à 0 dès que les images approchent 100 ms** (peintre
  20 à 36 ms) — sur les deux versions ; c'est l'ordre d'un téléphone lent (chantier 73, à mesurer contre l'iPhone 12, A13).

## ⚑ LA BASCULE DU RAYON, LE CHANTIER 68 SUR LA PAGE +, L'ÉCRAN QUI VEND · 11 septembre 2026 (soir) · `lot-CERCLE-MUR` + `lot-CERCLE-VEND-css`

> **app.html `53aae647…` → `a543d1e196b42378d16a462cdcabd769`** (sauvegarde d'avant : `sauvegardes/app-avant-seuil-pilule.html`).
> Trois patchs sous `assert` : `sauvegardes/audit-cercle/patch_seuil_pilule.py` (4 remplacements), `patch_cercle_vend.py` (une phrase +
> un bloc CSS en fin de fichier), puis deux retouches du bloc (le montant du bouton, le contour des boutons — vus par la vérification
> et par la capture). Décisions : **Q203** (la bascule, mesurée), **Q204** (l'écran qui vend : ma lecture, à confirmer), B12, CLAUDE §5.

**1 · La bascule du rayon — rayon = hauteur ÷ 2 jusqu'à 94,5, 30 au-delà.** Tom : *« mesure le seuil exact — à quelle hauteur la
pilule commence à manger le texte — et pose la bascule là, pas à un nombre de lignes arbitraire »*.
- **Mesurée sur l'ENCRE** (`seuil_encre.py`, `_analyse`, `_bascule`) : chaque champ capturé, la distance de l'encre la plus proche à
  la courbe intérieure recalculée pour tout rayon. « Manger » = serrer l'encre plus qu'un champ ouvert au rayon 30 (P, validé) :
  **C = 15,19**. Un champ à deux rangées qui s'ouvre tient C en pilule jusqu'à **94,53** (PIÈCES JOINTES de la page +), 96,21
  (Nuée), 105,95 (fiche) ⇒ **94,5**. Les champs réels tombent nettement de part et d'autre (en pilule : 64 → 19 à 23 · 92 → 15,7 à
  18 · 104 → 10,7 · 118 → 6,3 · 163 → −3,0 ; au rayon 30, tous les champs ouverts entre 15,2 et 16,8).
- **Ce n'est pas une affaire de lignes** : la place de la première rangée décide (une NOTE en pilule mangerait dès 85,75). La
  bascule vaut pour les compositions du produit ; tout champ qui la contredirait est pris par les contrats.
- **Un seul propriétaire** : `rayon()` dans `lot-CERCLE-MUR` (`window._seuilPilule`) — il pose le rayon des zones (sur leur hauteur
  CALCULÉE) et des autres rangées de Peaufiner ; la Nuée (`pose` de `lot-NUEE-PEAUFINER`) l'appelle. La règle CSS « trois lignes →
  30 » (une classe) est retirée — deux écrivains se défont (§7).
- **Ce qui a bougé à l'écran : LE TRAIT d'une Nuée, 59 → 30** — son libellé n'est plus contre la courbe (encre à 1,6 en pilule).
  Tout le reste garde son rayon. Reste du chantier 67 : ses pastilles à 14,25 du bord droit (encre à 11,1 du contour).
- **Mon premier instrument mentait** : il mesurait des boîtes de ligne et fusionnait le libellé de gauche avec la valeur de droite
  (« 0 fichier », à 23, donnait son haut à « PIÈCES JOINTES », à 26,4). Remplacé par l'encre.

**2 · Chantier 68, sur la page +** — Tom : *« c'est la même géométrie »*. Sur la fiche, la note grandissait déjà ; sur la PAGE +, la
zone de la note est **rebâtie sans cesse** (six zones en 2,5 s, au défilement aussi — chantier 70, pas cherché qui) et, entre un
rebâtissage et l'image suivante, la zone neuve restait à 118 avec trois lignes (dernière ligne à 0,5 de la courbe). Elle est
recalée **dans la foulée de la mutation** (micro-tâche), avant toute image. À 4 et 5 rangées, fiche et page + : libellé → texte
15 / 17, texte → « visible par … » **14,6**, toutes les lignes montrées ; sonde d'observateur : **16 rebâtissages, tous à 163**.

**3 · L'écran qui vend — `#plusScreen`, une seule version, corrigé sans redessin** (Q204, ma lecture : `cercleScreen` n'existe nulle
part ; la page du Cercle est celle qui porte le prix et les boutons, et tous les murs y mènent). Mesuré avant (`vend_avant.py`) :
en clair, « Prendre l'année — 29 € » **1,09**, « Essayer 14 jours » **1,16**, les montants de la phrase **1,09** ; en sombre, le
montant du bouton bleu sur encre 3,36 ; les textes à x 6 pour une marge de 24 ; « soit près de cinq mois offerts ». Après :
**rapport ≥ 14,4 partout**, remplissage = couleur, **« 29 € · soit 2,42 €/mois · −39 % »**, marge **24** (titre, phrase, liste,
boutons), **contour des deux boutons à l'encre en clair** (il était crème sur crème : le texte se lisait, le bouton ne se voyait
plus — **vu à la capture, pas par ma première vérification**, qui ne mesurait que le texte ; contrat ajouté, prouvé sur la version
d'avant : écart de luminosité 0 → pris). **Non fait : le bas de la planche** (trois mondes, « 29 € » en grand) — c'est la question.

**Vérifié à l'écran, deux thèmes** (`verif_seuil.py`, **54 contrats, 0 raté**, journal `journaux/verif_seuil_final.log`) : l'app
déclare 94,5 · le rayon de CHAQUE champ = la règle (fiche, page +, Nuée, notes à 4 et 5 rangées) · l'air de l'encre ≥ 14,69 partout
· chantier 68 et la sonde de rebâtissage · l'écran qui vend (lisibilité, forme du prix, marge, contours) · les encarts du gardé de
côté (par-dessus) et des Réglages y mènent. **Défauts connus, déclarés, non comptés** : le rond photo posé sur AVANT de la page +
(chantier 64) ; les pastilles de LE TRAIT d'une Nuée (chantier 67). **Non confirmés au doigt** (sous la barre ou hors cadre, en bas
de liste) : C'EST IMPORTANT ? et LA MÉMOIRE de la page + — des pilules de 64, mesurées hors écran à 21,6 / 22,1.
**Captures regardées une par une** (`sauvegardes/audit-cercle/seuil/`, `vend/final_*`) : la pilule et le champ ouvert côte à côte
(deux thèmes — même trait, même libellé, même air ; seuls les coins changent, du demi-cercle au rayon 30 du grand panneau) ; les
huit notes ouvertes ; LE TRAIT avant / après ; l'écran qui vend haut et bas.
**Mes instruments, dits :** la première passe plantait sur une page + pas encore ouverte, et comptait comme « recouvert » un champ
dont le doigt tombait sur SA liste (un ancêtre n'est pas un recouvrement) — corrigés ; la preuve lancée sur la version fautive a
**écrasé** les captures de la passe finale (même dossier) — elle écrit désormais dans `seuil_preuve/`, et la capture finale a été
reprise (`vend/final_*`).

**J'ai réécrit un contrat de test : `releve-S2`** — le rayon attendu suivait une CLASSE (Q202) ; il suit la hauteur, **94,5 écrit en
dur**, et le juge vérifie que l'app le déclare. Original : `sauvegardes/releve-S2-peaufiner-avant-seuil.py`. **Prouvé sur deux
versions fautives, une de chaque côté de la bascule** : l'app d'avant le mur (zones en pilule) → style 13 (12 rayons + seuil non
déclaré) ; la même app avec un seuil à 60 → style 37 (tous les 64 et le 92 à 30, et la déclaration).

**Batteries en série, sur `a543d1e1…`** (`sauvegardes/audit-cercle/journaux/bat_seuil_a543.log`, 19:07 → 19:56, 24 batteries) :
redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 · redteam_toile 17/17 · redteam_geste 13/13 ·
redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 · **redteam_air ✅ 436 paires, intact** (la marge de
l'écran qui vend ne resserre rien) · redteam_champ 32/32 · **releve-design ✅ aucun écart** · redteam_fonctions 22/22 ·
redteam_polices 0 couple absent · redteam_superpo 0 recouvrement · releve-fiche-personne ✅ 258 · redteam_nuee ✅ 24 écrans ·
releve-S1 ✅ · **releve-S2 ✅ position 0 · style 0** (contrat réécrit) · releve-S3 ✅ 0 · releve-S4 ✅ · releve-S5 ✅.
- **`releve-aura` — 4 écarts, famille « la matière » : défaut du chantier 59, pris à ce passage.** « arroser tous les soirs » à
  ΔE 6,0 (sombre) / 5,8 (clair), « monter la serre avant les gelées » à 14,6 / 14,8, plancher 15. La couleur d'une dalle est
  tirée au hasard à chaque chargement (`cc()`) ; ce lot ne touche pas l'Aura. Tout le reste du juge est à 0. Pas relancé pour
  un vert (CLAUDE §7) : le défaut reste ouvert.
- **`redteam_ecrans` — n'a rien mesuré dans la série** : `Page.goto` a dépassé 30 s (la page ne s'est pas chargée), pendant que
  trois navigateurs tournaient à la fois (la série, une capture et `verif_integration`, qui a échoué de même). **Repassé SEUL :
  ✅ 150/150.**
- **Les séries précédentes de ce lot** (`bat_seuil.log` sur 93286104, `bat_seuil_final.log` sur 91a73c6c) ont été ARRÊTÉES à 6 et
  7 batteries, toutes vertes : chaque retouche de l'écran qui vend (montant, puis contour) changeait l'app — la série ne vaut que
  sur la version livrée.

**Les 34 contrats du lot du mur, repassés** (`verif_integration.py`, `journaux/verif_integration_a543.log`) : **63 ✓, 1 raté** —
« page + · l'encart ouvre le Cercle PAR-DESSUS », en clair : **défaut du chantier 70, pris à ce passage**. La page + rebâtit sa
liste sous le doigt ; l'encart touché est détaché entre l'appui et le relâcher, le clic se perd. Reproduit sur l'app d'AVANT ce
lot (38 / 40 touchers, les deux ratés avec l'encart détaché) ; sur l'app du lot, 40 / 40. Antérieur, tiré au hasard, ouvert.
**Mes instruments, encore :** (1) la fiche 126 que visaient `verif_integration` et `verif_seuil` est passée à l'état « raté »
dans la soirée (son échéance est tombée) — plus d'id en dur, on prend le premier Promi en cours adressé à quelqu'un, comme
`releve-S2` ; (2) en l'écrivant, j'ai collé un commentaire AU MILIEU d'une ligne de `verif_integration` : le toucher sur la barre
Peaufiner était passé en commentaire, et le mur « manquait » — trois contrats rouges qui ne mesuraient que moi ; (3) une sonde
lisait `window.promises`, un autre tableau (16 Promi, 141 à 156), et m'a fait croire que le jeu avait changé de numéros ; (4) un
espion d'événements posé sur la fenêtre empêchait la page + d'ouvrir son Peaufiner (3 contextes sur 4) — retiré.

## ⚑ LE CERCLE, INTÉGRÉ — LE MUR POSÉ, LES CHAMPS À TROIS LIGNES, LE CHEMIN · 11 septembre 2026 · `lot-CERCLE-MUR`

> **app.html `48b1a56b…` → `53aae6471a35bab225ea0b974b98c644`** (sauvegarde d'avant : `sauvegardes/app-avant-cercle-mur.html`).
> Patch : `sauvegardes/audit-cercle/patch_cercle_mur.py` (7 remplacements sous `assert`) + bloc neuf `lot-CERCLE-MUR` (source :
> `sauvegardes/audit-cercle/bloc_cercle_mur.html`). Décisions : Q200, Q201, **Q202** (Tom, 11 sept.).

**Ce qui est posé**
- **L'ordre des réglages payants** — RÉCURRENCE · RAPPEL · C'EST IMPORTANT ? · LA MÉMOIRE — à la source : la brique `cercle()`
  (fiche, page +) et `cercleReglages()` (Réglages).
- **L'encart du mur porte « ✦ Le Cercle », seul** (Q201) — `cercle()` ne pose plus le sous-titre ; l'encart des Réglages le masque
  et reste « ✦ Le Cercle » après tout `setPremium` (il devenait « Membre du Cercle ✓ » et le restait en gratuit : défaut P4
  de l'audit, réglé au passage parce que c'est le même libellé).
- **Le mur sur la page +** — la brique même de l'app, en fin de liste, remise par un observateur quand `peaufBati` rebâtit la
  liste (un bloc posé une fois disparaît en moins d'une seconde). Le **gardé de côté** le reçoit du même coup (il rouvre la
  page +). Masqué / net selon `_cerclePaye`, comme sur la fiche.
- **P** (Q202) — les champs de trois lignes et plus au **rayon 30** : `.s2-zone` (NOTE, COMMENTAIRES — fiche et page +) par une
  règle CSS postérieure à la grammaire des contours ; DESCRIPTION et COMMENTAIRES d'une Nuée À LA SOURCE (le constructeur de
  `lot-NUEE-PEAUFINER`, `b.ph ? 30 : b.h/2` — un seul propriétaire).
- **Le texte du milieu centré** — son haut à `bord + (base − 2·bord − 22) / 2` (48 dans 118, 41 dans 104), la marge se
  calcule sur le bas du LIBELLÉ, lu en fraction (les `offset*` arrondissaient : 45,5 / 46,5 sur la page +, corrigé).
- **Chantier 68** — le champ grandit d'une ligne (22,5) par ligne de texte ; le `textarea` montre toutes ses lignes (il était
  peint sur 56 px pour une max-height de 44, sa 3ᵉ ligne passait sous « visible par Rachel »).
- **Chantier 66** — PIÈCES JOINTES d'une Nuée aux places de celle d'une fiche (libellé 23, bas 50,8), à la source.
- **Le chemin** — l'encart du mur (fiche, page +) ouvre la page du Cercle PAR-DESSUS (`.cercle-dessus`, z 95) sans rien
  fermer ; ✕ et l'achat y ramènent au même Peaufiner, la phrase de la page + intacte, les réglages nets — plus d'Aura après
  l'achat. Les autres portes gardent leur chemin. Rangé par `closeAll` (`_rangeurs`).

**Vérifié à l'écran, deux thèmes** (`verif_integration.py`, 34 contrats × 2 — **0 raté**) : ordre et encart (fiche, page +,
gardé, Réglages) · floutés 2,4 et intouchables · rayon 30 · écarts du texte du milieu **46 / 46** (fiche, page +, NOTE à 2 et
3 lignes), **39 / 39** (Nuée) · début des lignes extrêmes 14,1 / 13,5 (15,9 / 14,1 sur la Nuée) · NOTE à 2 et 3 lignes de
texte : 140,5 et 163 de haut, **15 d'air sous le libellé, 14,6 au-dessus de la visibilité** (1,3 avant) · le mur tient après
les rebâtisseurs · le chemin depuis la page + (✕ puis achat) et depuis la fiche **au vrai doigt** (la page reste ouverte) ·
PIÈCES JOINTES de la Nuée à 23 / 50,8 · la porte de l'accueil inchangée. **24 captures regardées une par une**
(`sauvegardes/audit-cercle/integration/`).
**Mes instruments, dits :** un contrat d'air comptait l'interligne du paragraphe (0,5 = 22 de dessin dans 22,5) comme un
défaut — réécrit avant toute série sur le défaut vu par Tom (texte ↔ libellé, texte ↔ visibilité) ; la vérification faisait
défiler la barre de la page + avant de la toucher (`scrollIntoView` déplaçait la page) — la barre, touchée à la souris et au
doigt, au centre et à 80 %, ouvre son Peaufiner dans les 8 cas, avant et après le lot ; la première série de batteries n'a
PAS tourné (la liste passée comme un seul nom de fichier, code de retour 0 quand même) — relancée.

**Ce qui reste visible, et ne relève pas de ce lot :** le bandeau du Peaufiner de la page + (chantier 64, Tom : « tu ne les
corriges pas ici ») ; **l'ancienne page du Cercle**, ouverte par-dessus, qui n'affiche toujours pas ses prix en clair — elle
attend A ou B (`PLANCHE-CERCLE-AB.html`), et le mur y mène désormais ; le halo sur « ✦ Le Cercle » des Réglages (§6, audit E10).

**Batteries en série, sur `53aae647…`** (`sauvegardes/audit-cercle/journaux/bat_cercle_mur.log`, 16:48 → 17:22, 24 batteries) :
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 · redteam_toile 17/17 ·
redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 · redteam_champ 32/32 ·
releve-design ✅ aucun écart · redteam_fonctions 22/22 · redteam_polices 0 couple absent · redteam_superpo 0 recouvrement ·
releve-aura ✅ au vert · releve-fiche-personne ✅ 258 · redteam_nuee ✅ 24 écrans · releve-S1 ✅ · releve-S3 ✅ 0 · releve-S4 ✅ ·
releve-S5 ✅. **Deux rouges, tous deux sur ce que Q202 a décidé, et rien d'autre :**
- **`releve-S2`** — position 4 (l'ancien ordre du bloc, C'EST IMPORTANT ? en tête) · style 12 (rayon = hauteur ÷ 2 sur NOTE,
  COMMENTAIRES, DESCRIPTION). **Contrat réécrit au niveau de la décision** (ordre de Tom ; rayon 30 pour un champ de trois
  lignes, hauteur ÷ 2 pour les autres, tolérance inchangée), original `sauvegardes/releve-S2-peaufiner-avant-cercle-mur.py`.
  **Prouvé :** passé sur l'app d'avant le lot, il rougit sur exactement les 16 points (position 4 · style 12) ; sur l'app
  intégrée, **position 0 · style 0 · collisions 0 · hors cadre 0 · peinture 0**.
- **`redteam_air`** — 8 paires resserrées, toutes sur le Peaufiner d'une Nuée : DESCRIPTION et COMMENTAIRES, libellé → texte
  9 → 7 (le recentrage décidé, 39 / 39) ; PIÈCES JOINTES, 23,5 → 9,3 et 27 → 12,8 (l'alignement sur la fiche, chantier 66,
  montré sur la planche 3). **Référence refigée** (avant : `sauvegardes/air-reference-avant-cercle-mur.json`) ; relancé :
  ✅ **436 paires**, 38 écrans, deux thèmes — 442 avant : les 6 paires du sous-titre de l'encart, retiré par Q201 (fiche d'un
  Promi, d'un Chiche, Réglages × 2 thèmes).

## ⚑ LE CERCLE, PLANCHE 3 — LES TROIS CORRECTIONS DE TOM · 11 septembre 2026

> **`app.html` n'est PAS touché** (`48b1a56b…`). Planche : **`PLANCHE-CERCLE-3.html`**. Outils :
> `sauvegardes/audit-cercle/probe_bandeau.py`, `mesure_lignes.py`, `cale_lignes.py`, `planche3_captures.py`, `planche3_build.py`.

1. **L'ordre des réglages payants** (Tom : la récurrence se comprend tout de suite, l'importance est la plus abstraite) :
   **RÉCURRENCE · RAPPEL · LA MÉMOIRE · C'EST IMPORTANT ?** — mur, état abonné, écran qui vend. Mesuré dans l'ordre sur
   les 14 captures du mur et de l'abonné.
2. **Le bandeau du Peaufiner de la page +** — vérifié par un chemin utilisateur PUR (touchers seuls) : les deux défauts sont
   AU PRODUIT, aucun ne vient de la maquette. La pastille de la page + (`.enh`) reste peinte sous l'en-tête du Peaufiner, son
   « FERMER » (`span.cb-mot`) tombe sur le titre (`.s2-titre`), confirmé au doigt, deux thèmes ; le rond photo
   (`.ph-photo-btn`, 34 × 34 à 332/230) reste sur AVANT. Le Peaufiner d'une fiche n'a ni l'un ni l'autre. **Masqués et
   déclarés sur la planche ; chantier 64.**
3. **Les champs à trois lignes et plus.** Mesure : distance du début de la 1re / dernière ligne à la courbe intérieure.
   Norme = le champ à deux lignes de la fiche (PIÈCES JOINTES) : **12,9 / 13,7**, air 5,8. Aujourd'hui : NOTE et
   COMMENTAIRES (118, rayon 59) **3,0 / 2,5** ; Nuée DESCRIPTION / COMMENTAIRES (104) **7,4 / 5,8** ; Nuée PIÈCES JOINTES
   **6,35** (même champ que la fiche). **Tenir la norme par l'interligne seul est impossible** (`cale_lignes.py`) : à trois
   lignes dans 118, zéro air entre les lignes ; dans 104, elles se chevauchent ; à quatre, impossible — cause : rayon =
   hauteur ÷ 2 (le §3.4 d'origine dessinait ces champs au rayon 22). Deux versions mesurées (deux thèmes, mêmes chiffres) :
   **T** (la consigne : l'interligne resserré, jamais sous 5,8, texte recentré ; sans effet quand la boîte est pleine) —
   **9,4 / 9,4** à trois lignes, **inchangé** à quatre, 7,9 sur la Nuée ; **P** (rayon 30, le grand panneau de la
   grammaire, interligne intact) — **14,1 / 13,5** à trois ET à quatre lignes, 15,9 / 14,1 sur la Nuée. PIÈCES JOINTES de
   la Nuée alignée sur la fiche dans les deux : 12,9 / 13,7. **T appliqué sur les captures du mur ; question posée : T ou P.**
   Chantiers 65 (la décision), 66 (PJ de la Nuée), 67 (LE TRAIT de la Nuée à 5,3), **68 (une note de trois lignes déborde
   sur sa ligne de visibilité — textarea peint sur 56 pour une max-height de 44)**.
**Mes instruments, dits :** le premier calage réduisait l'interligne à tort (il comptait deux lignes d'après la hauteur
du textarea) ; T aggravait d'abord le cas à quatre lignes (−1,1) ; la variante « boîte allongée » cassait les lignes sans
que le juge le voie (il ne mesurait que les lignes extrêmes — l'air entre lignes est désormais mesuré) ; le texte « long »
de la première passe faisait trois lignes, et le filtre sur la max-height cachait celle qui déborde. Tout est refait.

## ⚑ LE CERCLE, PLANCHE 2 — POSER LE MUR LÀ OÙ IL MANQUE · 11 septembre 2026

> **`app.html` n'est PAS touché** (`48b1a56b…`). Planche : **`PLANCHE-CERCLE-2.html`** (autonome). Outils :
> `sauvegardes/audit-cercle/verif_mur.py`, `verif_garde.py`, `planche2_captures.py`, `planche2_build.py`.

**Le sujet, dans les mots de Tom :** *« il ne s'agit pas de corriger un mur, il s'agit d'en poser un là où il n'y en a
pas. Les quatre réglages doivent exister, visibles et verrouillés, dans le Peaufiner d'une fiche et de la page +. »*
Décisions du jour : **Q201** (l'encart porte « ✦ Le Cercle », seul) · **Q200** (le Studio garde ses libellés).

**Mesuré avant de dessiner (deux thèmes) — la phrase de Tom corrigée sur deux points :**
- **Fiche : le mur EXISTE**, y compris sur un Promi planté à neuf (141) — 342 × 304, quatre réglages floutés à 2,4 et
  intouchables, encart net. Ce qui n'existe nulle part, c'est la FONCTION (inertes, même payés).
- **Page + : le mur MANQUE** — confirmé (`peaufBati` n'appelle pas `cercle()`).
- **Gardé de côté : son Peaufiner S'OUVRE** — il rouvre la page + (`openDetail` → `reprendreBrouillon`) et `#csBotBar`
  pose `pp-peauf` ; il porte À QUI · AVANT · DANS UNE NUÉE · NOTE · PIÈCES JOINTES, **sans le mur**. (Un premier test
  touchait la barre de la fiche, cachée derrière la page + : faux, refait par la bonne porte.)
- **Préexistant, sur l'écran où le mur va entrer :** le Peaufiner de la page + montre un second « ✕ FERMER » sous le
  titre et le rond de la photo sur la rangée AVANT (vu sur la capture de l'audit, chemin normal) ; en sombre, défilé, le
  plateau et son « ✕ FERMER » chevauchent la rangée NOTE.

**La planche :** 1 · le mur (fiche Promi, fiche Chiche, page +, gardé de côté — captures de l'app, la brique `cercle()`
accrochée à la page + par un observateur qui la remet quand la liste est rebâtie, en comparant avant d'agir : la première
accroche, posée une fois, était défaite par `peaufBati` en moins d'une seconde) · 2 · le chemin (fiche → mur, doigt sur
l'encart → l'écran qui vend → **retour au même Peaufiner, réglages nets**) · 3 · l'écran qui vend, **deux variantes** :
A (réglages nets en aperçu) / B (le mur repris) · 4 · l'état abonné (fiche, page +, gardé de côté). Juge sur les 8 cadres
composés : 0 hors cadre, 0 < 12 px, 0 recouvrement ; contraste faible seulement sur l'encart de B en sombre (2,42, spec).
**Question posée à Tom : A ou B.**

## ⚑ LE CERCLE — AUDIT À L'ÉCRAN, NŒUD PAR NŒUD · 11 septembre 2026

> **`app.html` n'est PAS touché** (`48b1a56b6b4b58f425dbd7a84e0b9f1f`). Audit complet : **`AUDIT-CERCLE.md`**. Outils,
> journaux, 83 + 40 captures : `sauvegardes/audit-cercle/` (`audit_ecran.py`, `audit_complement.py`, `repro_etats.py`,
> `analyse_audit.py`, `constats-ecran.md`). Deux thèmes × gratuit / Cercle payé, 430 × 932 (#device à 390 × 844).
> `batteries.sh` adapté : `sauvegardes/audit-cercle/batteries.sh` écrit dans `sauvegardes/audit-cercle/journaux/`.

**Le Cercle tel qu'il est ne peut pas être vendu.** Six constats, tous vus et reproduits sur page neuve :
1. **En clair, la page du Cercle n'affiche ni ses prix ni ses boutons** — « 29 € », « 3,99 €/mois », « Prendre l'année »
   à **1,09** de contraste, « Essayer 14 jours… » blanc sur crème à **1,16**.
2. **Rien n'est débité, rien n'est gardé** : année, mois, monde à 1 € — perdus au rechargement (aucune clé en localStorage).
3. **Fin du Cercle** (`setPremium(false)`) : **le monde payant reste** sur la Toile et s'ouvre sans verrou au Studio (P3) ;
   un monde **gratuit** (Mosaïque, Pixel) est ramené à Encre (P5 — logique inversée, l. 3119) ; **« ✦ Membre du Cercle ✓ »
   s'affiche en gratuit** (P4 — le texte réécrit par `setPremium(true)` n'est jamais rendu).
4. **Ce qu'on paie ne fait rien** : les quatre réglages défloutés sont inertes, valeurs figées ; **l'Aura (la Pelote) ne
   connaît pas le Cercle** (0 occurrence dans ses trois blocs) ; l'achat mène à l'Aura. Seuls Sillons / Gravure / Terrazzo
   s'ouvrent vraiment.
5. **L'abonné est traité en prospect** : `#cercleTopBtn` lui revend l'essai ; après l'achat, le Studio lui sert
   **« Adopte ce design — 1 € » sur Encre** (P1 — `world-locked` / `stp-verrou` survivent).
6. **La page du Cercle est l'ancienne** : « près de cinq mois offerts », mois en primaire, halo, glyphes, titre à x ≈ 6,
   visuel VIDE si ouverte par l'accueil. Aucun mot de Q165.

**Ce qui tient :** le bloc du §3.8 sur le Peaufiner d'un Promi et d'un Chiche (2,4 px, encart net, couleurs de la spec) ·
le partage ne porte aucun signe du Cercle (Q113) · Éclats n'a aucune porte (Q102) · aucun compteur nulle part.
**Revenu hors de la carte, à ne pas perdre :** huit pinceaux à 0,50 € (choisir un payant ne coûte rien) · « 4 pour 3 € »
(aucun achat ne l'implémente, et il n'y a que trois mondes payants) · codes couleur au Cercle (PLANCHE-STUDIO, non intégré).
**Trouvé en passant, hors Cercle :** aucun Promi ne garde son pinceau — `window.promises` indéfini (`let promises`,
l. 2856) dans `lot-PINCEAU` (l. 24234). Signalé comme tâche à part.
**Mes instruments, dits :** la première scène du Peaufiner de la page + cliquait la mauvaise porte (`.dpd-tog` au lieu de
`#csBotBar`) — refaite par le complément ; le premier complément a planté (`__file__`) avant toute mesure ; le juge de
contraste jugeait des textes posés sur un dégradé ou un canevas — corrigé, ces textes sont désormais « non jugés » et
listés ; P2 (Encre verrouillé en gratuit) venait de l'enchaînement de l'audit, **non reproduit sur page neuve**, retiré.
Les portes ont été touchées à la souris au point, pas au vrai doigt.

### La planche — `PLANCHE-CERCLE.html` (autonome : six faces et images embarquées), avant toute intégration
- **La page du Cercle**, quatre cadres (sombre / clair × à l'ouverture / défilée) : le bloc du §3.8 aux cotes relevées
  dans l'app (quatre réglages floutés 2,4, encart net à +108) → les trois mondes en VRAIES dalles du moteur
  (`dalleTrame(cv, id, 1, monde)`, trois Promi différents), nettes → « 29 € · soit 2,42 €/mois · −39 % » → « Prendre
  l'année » en premier → « Essayer 14 jours, puis 3,99 €/mois » et les deux notes sous le pli. **Zéro mot neuf** : tout
  vient de la spec, de l'app ou de Tom. Retirés sans remplacement : « Essaie tout, sans t'engager. », la phrase de prix
  interdite, les cinq arguments et leurs glyphes. « 4 pour 3 € » gardé (revenu), signalé (Q196.4).
- **Le Studio** (monde du Cercle, au repos / au doigt) et **les Réglages** : captures de l'app, avec Q106, Q117 et le
  sous-titre du §3.8 posés dans la page le temps de la prise (le rotateur de `#stBuyTx` rendu sourd pour la capture).
- **Juge** `planche_verif.py` : 4 cadres — 0 hors cadre, 0 texte < 12 px ni opacité < 0,72, 0 face étrangère,
  0 recouvrement hors l'encart du §3.8 ; contraste ≥ 4,5 partout **sauf l'encart en sombre (2,42, valeur de la spec —
  Q196.1)**. **Prouvé sur une sonde** (`planche_sonde.py`) : les quatre défauts posés sont nommés.
- **Non dessiné, et dit sur la planche :** les blocs d'Aura que le Cercle ouvre (ils n'existent pas sur la Pelote —
  Q196.2), le chiffre d'harmonie, l'écran d'un abonné, le bloc à la page +, pinceaux et codes couleur.

## ⚑ UNE DALLE TENUE MÈNE À SA FICHE — `lot-DALLE-PORTE` · 11 septembre 2026

Tom : *« Trois défauts à vérifier sur l'Aura […] Mesure, ne suppose pas. »* Deux des trois n'en étaient pas — mesuré ;
le troisième était réel, il est corrigé — et en le prouvant au vrai doigt, un défaut plus large est apparu (le clic
fantôme, § 3 bis). Le chantier 63 suit dans le même passage (§ 3 ter). **app.html `faff6e93…` → `48b1a56b6b4b58f425dbd7a84e0b9f1f`**,
trois blocs neufs à la fin : `lot-DALLE-PORTE`, `lot-CHEMINS-PERSONNE`, `lot-CLIC-FANTOME` (sauvegarde
`sauvegardes/app-avant-dalle-porte.html`). Journaux entiers : `sauvegardes/aura-trois/`.

### 1 · « Ce que tu as tenu » porte-t-il les trois natures ? — OUI, déjà
Le peintre (`donnees()` → `mesPromi()` → `ordreTenus()`) ne filtre que « tenu » et « planté par moi » — aucune nature.
Au jeu de démonstration : **5 paroles tenues à moi — 2 Promi (125, 139), 1 Chiche (129), 2 Promi de Nuée (130, 134) — la
rangée porte les 5.** (132, tenue, est d'Adrien : ce n'est pas ma parole, elle n'y est pas — voulu.)
**Contrôle neuf** (`releve-aura`, données) : la règle écrite en dur (`TENUES_MIENNES`, sans filtre de nature) ; quand
toutes tiennent dans la rangée, toutes y sont. **Sonde `sans-chiche` PRISE** : « perd [129] — natures ['chiche'] », deux thèmes.

### 2 · Chaque dalle garde-t-elle son monde de plantation ? — OUI, pour l'Aura et « Tenu ensemble »
Mesuré par la SORTIE, pas par le code : Studio passé en terrazzo puis en pixel (l'appel du Studio, `Toile.setTheme`), les
dalles du jeu figées en encre. Chaque dalle peinte comparée dans la même page à deux rendus du moteur — sa plantation (A),
le monde courant (B) : **distance à la plantation 0,000 à 0,002, au monde courant 0,02 à 0,62**, sur les 6 dalles (5 de
l'Aura, 1 de la fiche de Rachel). Un piège sur `dalleTrame` : chaque appel de l'Aura et de la fiche reçoit bien « encre ».
⚠ Mon premier verdict automatique disait « monde courant » pour 7 dalles : l'histogramme des couleurs ne départage pas
(encre et terrazzo peignent ici la même teinte) ; c'est le taux de remplissage qui tranche. Corrigé dans le juge : une
distance composée, et une dalle dont les deux mondes ne se distinguent pas n'est pas jugée.
**Contrôle neuf 6 bis** (page neuve — le cache de l'Aura garderait un rendu d'avant le changement ; Studio en `pixel`) :
5 dalles jugées, distance plantation / courant 0,000–0,001 / 0,14–0,62. **Sonde `monde-courant` PRISE** (les dalles de l'Aura peintes sans leur 4ᵉ argument) : les 5 nommées, à 0,097–0,723 de
leur plantation et 0,000–0,007 du monde courant.
**Ce qui ne garde PAS son monde :** seuls l'Aura (l. 28081) et la fiche d'une personne (l. 28877) passent le 4ᵉ argument ;
les 24 autres appels de `dalleTrame` en passent trois — cartes d'Index, bandeaux du Fil, fiches, et donc les cartes « Ce
que vous partagez ». C'est le lot « brancher les peintres » (§4), toujours ouvert.
**Au jeu de démonstration la rangée est uniforme** : tous les Promi ont été figés dans le monde du jour au chargement
(le rattrapage du 4 septembre — « rien n'est tiré de leur date »). La diversité viendra des plantations nouvelles.

### 3 · Toucher une dalle ouvre-t-il sa fiche ? — NON, c'était le vrai manque. CORRIGÉ.
Relevé : `cellule(p)` (Aura) et les cellules de « Tenu ensemble » n'avaient **aucun gestionnaire**. Bloc neuf
**`lot-DALLE-PORTE`** : un écouteur délégué (les cellules sont rebâties à chaque ouverture) ; la porte est
**`openDetail(id)` — la même que la carte d'Index (l. 18932) et le bandeau du Fil (l. 19049)** ; l'Aura reste dessous et
**✕ y ramène** (mesuré). **Un glissement n'ouvre rien** : le toucher se juge comme celui des Noyaux — déplacement du doigt
PLUS défilement de la colonne, sous `G.TAP` (6 pt) ; au vrai doigt, le navigateur annule en plus le toucher dès que la
colonne défile.
**Preuves :** `releve-aura` sur l'app d'avant — **8 bis PRIS** (« toucher la dalle « rapporter le livre » n'ouvre pas SA
fiche ») ; sur l'app corrigée — vert (Promi 139 ouvert, attendu 139 ; ✕ → l'Aura). `releve-fiche-personne` sur l'app
d'avant — **2 écarts, la porte de « Tenu ensemble »** ; après — **258 / 258**. **Au vrai doigt** : § 3 bis — c'est là que la
première écriture est tombée.

### 3 bis · LE CLIC FANTÔME — trouvé au vrai doigt, et il cassait AUSSI la porte des Noyaux
La première écriture de la porte ouvrait au lever du doigt (`pointerup`). Les juges, joués à la souris, étaient verts.
**Au vrai doigt (événements tactiles CDP), la fiche s'ouvrait et se refermait aussitôt** : journal des événements —
`openDetail(139)` → `closeAll` ← `openDetail` → `touchend` → **`click` sur `#scrim`** → tout se referme. Après un toucher,
le navigateur synthétise un clic AU POINT DU DOIGT, après `touchend` : ouvrir avant lui, c'est lui donner la feuille neuve à
cliquer. **La porte des Noyaux de l'Aura (lot-AURA-PELOTE, d'origine) avait exactement le même défaut** : `openPerson(Marion)`
→ clic sur `#scrim` → l'Aura, rien d'ouvert. **Sur un téléphone, toucher un Noyau n'ouvrait donc rien de visible** — aucun
juge à la souris ne pouvait le voir. Deux parades :
- **la porte des dalles (et celle du 63) s'ouvre sur le CLIC** : le lever du doigt l'arme (même cellule, sous le seuil), le
  clic qui suit l'ouvre. `app.html` restauré à `faff6e93…` et le bloc réinséré réécrit (la version d'abord insérée,
  `7ca1cc98…`, est gardée : `sauvegardes/aura-trois/app-dalle-porte-pointerup-7ca1cc98.html`) ;
- **`lot-CLIC-FANTOME`** pour la porte des Noyaux, qu'on ne touche pas : un clic ISSU D'UN TOUCHER qui tombe sur une
  COUCHE OUVERTE PENDANT LE GESTE (sa couche `.show` n'existait pas quand le doigt s'est posé) est la queue du geste
  précédent — avalé. Jamais un clic de souris, jamais un clic de script, jamais un clic sur une couche déjà ouverte :
  ✕ FERMER et une carte d'Index, touchés au vrai doigt, marchent (contrôlé). ⚠ Une première écriture comparait l'élément
  touché à l'élément cliqué — elle aurait avalé un vrai toucher sur un bouton que l'app redessine sous le doigt, sans
  qu'aucune série à la souris ne le voie ; resserrée sur la forme exacte du défaut AVANT toute série (la chaîne arrêtée).
**Le défaut dort-il ailleurs ? (Tom : « confirme-le en balayant les autres ».)** Dans le CODE : **53 écouteurs de pose ou de
lever du doigt** (`pointerdown/up`, `touchstart/end`, `mousedown/up`, en `addEventListener` ou en attribut) ; **un seul
ouvre quelque chose — la porte des Noyaux de l'Aura** (l. 28578, `openPerson`). Le curseur de teinte du Studio écoute
`pointerup` mais n'ouvre rien. AU DOIGT (`balayage_fantome.py` : chaque élément touchable de douze écrans, touché au doigt
puis cliqué à la souris, écran rouvert à neuf ; une porte fantôme est une porte où le doigt et la souris ne finissent pas au
même endroit) : **79 éléments touchables sur douze écrans** (accueil, Index, Fil, Aura, fiches d'un Promi, d'un Chiche, d'une Nuée, leurs
Peaufiner, fiche de Rachel, Studio, Réglages), chacun au doigt ET à la souris. **Sur une copie SANS garde** (`1cf70b18…`) :
**2 écarts, et seulement eux — les Noyaux de Marion et de Rachel sur l'Aura** (le clic issu du toucher tombe sur `#scrim`).
**Sur l'app finale : 0 écart** — les deux mêmes clics fantômes sont consignés, et avalés : le doigt finit où finit la
souris. Le code et le doigt disent la même chose : le défaut ne dort nulle part ailleurs. ⚠ Limite dite : le balayage ne
voit que ce qui se DÉCLARE touchable (bouton, `onclick`, `role`, curseur main) ; les portes déléguées — les dalles, les
noms écrits — ont leur propre preuve au doigt (`doigt_defile.py`, `chemins63.py`). Journaux :
`sauvegardes/aura-trois/balayage_sans_garde.log`, `balayage_finale.log`.
**Preuves au vrai doigt (`doigt_defile.py`, événements tactiles CDP)** — sur la version d'abord insérée, sans garde :
**4 ratés sur 11** (les deux touchers de dalle de l'Aura, le Noyau de Marion, le nom « Rachel » d'une Nuée : ouverts puis
refermés). Sur l'app finale (`48b1a56b…`) : **13 / 13** —
- **un glissement vertical n'ouvre JAMAIS une fiche** : sur l'Aura, la colonne défile de 145 pt (course 150), aucune fiche ;
  sur « Tenu ensemble », 84 pt (toute la course), aucune fiche ;
- un toucher net, et un toucher qui tremble de 4 pt (sous le seuil de 6), ouvrent la fiche de la dalle (Promi 139), sur les
  deux écrans ;
- le Noyau de Marion, au doigt : SA fiche s'ouvre et **reste** ; le nom « Rachel » dans « Avec Rachel, Adrien, +3 » :
  SA fiche s'ouvre et reste ;
- les vrais touchers marchent toujours : ✕ FERMER referme la fiche, une carte d'Index ouvre son Promi ;
- un seul chemin : l'appel nu `openPerson` EST `window.openPerson`, la fiche refaite.
**La sonde « porte naïve »** (une porte qui ouvre à chaque doigt levé, même après un défilement) est **PRISE** au
glissement sur les deux écrans — sur l'app finale aussi (la sonde passe sous le garde : c'est bien le glissement que le contrôle juge).

### 3 ter · LE CHANTIER 63 — les noms écrits mènent à la personne (`lot-CHEMINS-PERSONNE`)
Bloc neuf `lot-CHEMINS-PERSONNE` (la porte commune, ouverte sur le clic). Le nom touché dans une ligne mène à SA fiche —
`openPerson`, le même chemin que les Noyaux et les disques ; le toucher lit le MOT sous le doigt et ne l'accepte que s'il est
une personne connue (`peopleList`). Aucune forme neuve, aucun nœud ajouté. **Preuve au doigt (`chemins63.py`)** — sur l'app
d'avant : **7 ratés sur 12** (tous les noms) ; sur l'app finale : **12 / 12** —
- fiche de Nuée « Avec Rachel, Adrien, +3 » : Rachel → la fiche de Rachel, Adrien → celle d'Adrien, **« +3 » → personne** ;
- Peaufiner de la Nuée « Rachel · Adrien · +3 » : de même ;
- fiche du Chiche « À Marion · avec Rachel » : Marion, Rachel ; fiche du Promi « À Rachel » : Rachel ;
- **la rangée « À QUI » du Peaufiner d'un Promi n'ouvre personne** — elle règle le destinataire (validé par Tom) ;
- un glissement de 30 pt sur un nom n'ouvre rien ; au vrai doigt, « Rachel » d'une Nuée ouvre SA fiche et elle reste.
**✔ Le 63 est FERMÉ (Tom, 11 sept.).** Ses deux restes vivent ailleurs : « toi » relève du mode « moi » (le mode « moi » n'a pas
de fiche — décision de produit) ; les noms et visages DANS une carte du Fil ou de l'Index restent la question Q195.

### 4 · Un seul chemin de code
Une dalle mène à la fiche de SON Promi : `openDetail`, partout (carte d'Index, bandeau du Fil, dalle de l'Aura, « Tenu
ensemble »). Un Noyau, un disque, un nom mènent à la fiche de la personne : `openPerson` — et l'appel nu est
`window.openPerson`, la fiche refaite (mesuré : l'appel nu `openPerson` EST `window.openPerson`, et au doigt le Noyau de Marion, « Rachel » d'une Nuée, les noms du Peaufiner d'une Nuée et ceux de la ligne d'une fiche ouvrent tous `#psCadre[data-fiche=nom]` — la même fiche, jamais l'ancienne). Les seuls appels morts sont dans l'ancienne Aura masquée (l. 6320,
6322, 6510 — déjà relevés). ⚠ Mise au point : je n'ai trouvé **aucun** `openPerson` orphelin dans le Fil ni dans la fiche
d'un Promi.

### 5 · Contrôles
**Série complète, EN SÉRIE, sur `48b1a56b…`** (`sauvegardes/aura-trois/bat_apres14.log`, 03:27 → 03:55) — 18 batteries :
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 · redteam_toile 17/17 ·
redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 · redteam_air ✅ 442 paires ·
redteam_champ 32/32 · releve-design ✅ aucun écart · redteam_fonctions 22/22 · redteam_polices 0 couple absent ·
redteam_superpo 0 recouvrement · releve-fiche-personne ✅ 258 · **releve-aura : 4 écarts, tous dans la matière** —
« monter la serre » ΔE 7,8 / 9,0 et « arroser tous les soirs » 5,8 / 6,9 (sombre / clair) ; toutes ses autres familles à 0,
dont les trois contrôles neufs (natures, 6 bis, 8 bis). Les juges étendus ont d'abord été passés sur l'app d'avant (pris) et
sous deux sondes (prises), avant la série.
**`releve-aura` rougit sur la matière à chaque passage de ce lot** — « planter un arbre », « monter la serre », « arroser
tous les soirs », de ΔE 6,2 à 12,9 selon le tirage. **Règle de Tom (CLAUDE.md §7, 11 sept.) : c'est le défaut du chantier
59, PRIS à ces passages ; un relancer vert ne l'annulerait pas.** Ce lot ne touche pas la matière.

## ⚑ LA FICHE D'UNE PERSONNE, REFAITE — `lot-FICHE-PERSONNE` · 11 septembre 2026

> **`app.html` modifié** — md5 avant `6f2f028d149a9b1bc5ffa0771250b76e` (sauvegarde `sauvegardes/app-avant-fiche-personne.html`),
> **après `faff6e93a90857bc3b7895e4495aae63`**. Un bloc neuf en fin de fichier (`lot-FICHE-PERSONNE-CSS` + `lot-FICHE-PERSONNE`) ;
> aucune règle existante touchée, rien du moteur de la Toile. Audit : `AUDIT-FICHE-PERSONNE.md` ; planche validée :
> `PLANCHE-FICHE-PERSONNE-4.html` ; Tom : *« Go, intègre. L'écran, les deux gestes, la série complète, le chapitre. »*

### 1 · Ce qui reste, ce qui sort
**Reste (Tom, Q193) :** le nom (plateau, Bricolage 700) · le visage dans l'anneau · **le Noyau du §2.9** (58, arc 6, image 36,
piste neutre) qui compte **toute la liste** · **« Tenu ensemble »** — les paroles tenues, en dalles, **dans le monde de leur
plantation** (`dalleTrame(cv, id, 1, monde)`) · **« Ce que vous partagez »** — Promi, Chiche (le compagnon `avec` compris) et
Promi de Nuée, en **VRAIES cartes d'Index** : la dalle sur le champ de sa nature, **le trait qui dit l'état**, la ligne du bas
réduite au temps quand l'app le sait et à la Nuée (« 5 J · LE POTAGER ») — **l'état n'est plus écrit** · **« + Planter un
Promi » et « + Lancer un Chiche »**.
**Sort, sans remplacement — les infractions de l'audit (§ C) :** le mot d'harmonie (« votre harmonie : rayonnante · ta
parole : … »), les agrégats (« N Promi échangés · N reçus · N donnés »), « comment ça évolue » (la ligne grise et sa rampe
inventée), le second anneau et sa légende, l'équilibre « toi NN % ⟷ eux NN % » et sa phrase, l'ombre de dalle animée, les
trois opacités sous 72 %, « votre », la colonne à 8 au lieu de 24, le nom en Bricolage 800, les vignettes jamais peintes,
« aucun Promi pour l'instant » (excluait les Chiche).

### 2 · Comment c'est posé
- **`openPerson` redéfinie** (le correctif `avec` compris). Elle ne remplit plus rien de l'ancienne fiche.
- **L'ancienne fiche est masquée NŒUD PAR NŒUD** (`.ps-head`, `#psMirror`, `.grouplab`, `#psList`, `.grip`) et reste dans le DOM,
  vide. Son code reste dans le fichier (§9 : on ne nettoie pas) mais **plus rien ne l'atteint** : tous les appelants passent par
  `window.openPerson` (vérifié : l. 4900, la rangée de l'Aura, le disque d'une fiche).
- **Un cadre de 390 × 844 posé sur `#device`** (la fiche fait 422 et commence 16 px avant : le piège du §8), mesuré à chaque
  ouverture, transformation d'ouverture retirée ; la colonne défile **sous le plateau** (`clip-path` à 100), comme l'Aura.
- **Les vraies cartes d'Index : le moteur du lot S4 est PRÊTÉ.** `_s4Index` bâtit dans `#indexList` ; on prête ce nom à la
  boîte de la fiche le temps d'un appel, puis on rend tout à l'identique (l'id, les entrées, le cache). **Aucune variante
  locale de la carte (§5).** ⚠ Son CSS est rattaché à `#device .s4-carte` (lot-S4, l. 18502-18522) et la fiche vit sous
  `.frame` : **les mêmes valeurs sont re-rattachées à `#psCadre`** — si la carte change dans le lot S4, elle doit changer ici.
  ⚠ Les cartes gardent l'appel de l'Index (`dalleTrame` à 3 arguments, le monde courant) : brancher le monde de plantation sur
  les cartes est le lot « brancher les peintres » (§4). Au jeu de démonstration les deux coïncident (vérifié, Promi par Promi).
- **Les deux gestes** ouvrent la page + comme `openCreateForNuee` : la personne est posée là où la plantation la lit
  (`newWhoSel`, `#fWho`) et dans la phrase (`_phrase.qui`), la nature dans `_csSens` / `_phrase.sens`.
- **Un rangeur pour `closeAll`** (`window._rangeurs`) retire le cadre à la fermeture (§8, « rien ne survit à closeAll »).
- `harmonyWord` a encore des appelants **hors de cette fiche** (l. 6338, 6370 : le mot du TON Noyau dans l'image de partage) —
  hors lot. Et `frame()` écrit toujours ses variables d'ombre sur `#personSheet` à chaque image (chantier 58).

### 3 · Le juge — `releve-fiche-personne.py`, 254 contrôles, 9 familles
Il lit **l'écran**, jamais le DOM seul (le faux vert de `redteam_ecrans`) : la présence en **pixels** sur la capture de
l'appareil — le champ de chaque carte dans la couleur que son peintre déclare (`data-champ`), la dalle posée dessus, les arcs
du Noyau, la dalle tenue, le visage ; un texte ne compte que s'il est **touché au doigt**. La composition se compare aux
**données qu'il recalcule** (qui · de qui · avec). Les cotes décidées sont **en dur** (§2.9, plateau, cartes, gestes, pli).
Familles : présence · composition · cotes · polices (dont « les cartes de la fiche ont les polices de l'Index », mesuré dans
la même page) · les infractions (18 mots, les anciens nœuds invisibles, l'ombre, la ligne grise) · lisibilité · libellés et
état vide · portes (la rangée de l'Aura et le disque d'une fiche, au doigt) · **les deux gestes au doigt**.
**Prouvé contre de vrais défauts :**
```
l'app d'avant (sauvegarde)          16 écarts sur 22 — pas de nouvelle fiche, pas de gestes, l'état vide faux     PRIS
sonde « cartes vidées »             8 écarts — chaque carte nommée, « part du champ 0,00 »                        PRIS
sonde « ligne d'harmonie remise »   22 écarts — « harmonie », « rayonnante », « votre », #psSub visible au doigt  PRIS
l'app intégrée                      254 / 254                                                                    VERT
```
Deux premières écritures du juge étaient fausses et ont été corrigées AVANT de servir, dites : la présence d'une carte se
mesurait sur la carte entière (son corps est proche du fond par dessin — une carte parfaite sortait à 0,38), puis sur « le
haut, 40 % » (le trait d'un Chiche lancé monte plus haut — 0,80) ; elle se mesure sur ce que le peintre DÉCLARE avoir versé.
Et le juge **plantait** sur l'app d'avant au lieu de la juger (une colonne absente) : il nomme désormais ce qui manque.

### 4 · Les deux gestes, AU DOIGT, jusqu'au Promi planté
La rangée de l'Aura touchée → la fiche de Rachel → « + Planter un Promi » touché → la page + s'ouvre, **la phrase porte déjà
« Rachel »** → le titre tapé dans la phrase → **le trait tracé au doigt** (événements tactiles réels, du point gauche au-delà
des deux tiers) → **un Promi planté pour Rachel, sans la ressaisir**. Même chose pour « + Lancer un Chiche » → **un Chiche
lancé à Rachel** (`chiche`, `chicheEtat: 'lance'`).

### 5 · Contrôles
**Série complète, EN SÉRIE, sur `faff6e93…`** (`sauvegardes/audit-fiche-personne/apres/bat_apres13.log`, 01:41 → 02:08) —
18 batteries : redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 ·
redteam_toile 17/17 · redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 ·
redteam_air ✅ 442 paires · redteam_champ 32/32 · releve-design ✅ aucun écart · redteam_fonctions 22/22 · redteam_polices
0 couple absent · redteam_superpo 0 recouvrement · **releve-fiche-personne ✅ 254 contrôles** · **releve-aura : 2 écarts —
« la dalle « planter un arbre » est illisible : ΔE 12,2 (plancher 15) », sombre et clair**, toutes ses autres familles à 0.
C'est le tirage de couleur du chantier 59 (bleu sur bleu), que le juge prend quand il tombe. Relancé seul, sur un
nouveau tirage, il est sorti vert (la plus faible à ΔE 22 / 20 ; `aura_reconfirme.log`) — **⚠ requalifié le 11 sept.
(règle de Tom, CLAUDE.md §7) : ce vert n'annule rien. Le rouge est le résultat : défaut du chantier 59, PRIS à ce
passage, toujours ouvert.** Ce lot ne touche rien de l'Aura.
**Captures, regardées une par une** (`sauvegardes/audit-fiche-personne/apres/final-*.png`) : Rachel en sombre et en clair, à
l'ouverture (le Noyau et son visage, la légende, « Tenu ensemble », les quatre cartes, les gestes franchement sous le pli) et
défilée jusqu'au bout (la colonne passe sous le plateau, les gestes entiers en bas) ; Nico, vide, dans les deux thèmes (le
Noyau et sa seule piste, les deux gestes — très nu, c'est ce qui a été décidé) ; la page + ouverte par « + Lancer un Chiche »,
« à Rachel, chiche … » déjà écrit. Défauts vus : « à le groupe » (chantier 60) ; et dans la page +, voir ci-dessous.
**⚠ Un recouvrement dans la PAGE + (autre écran — noté, pas corrigé ici, CHANTIERS n° 62).** L'aide sous la phrase
(`.ph-hint`) suit la hauteur de la phrase ; la rangée des pinceaux (`#csPinceau`) est fixe à y 651. Dès que la phrase prend
une ligne, elles se recouvrent. **Mesuré : le Chiche par le chemin NORMAL** (bouton de création → tuile Chiche) : l'aide
« le compagnon et l'échéance sont dans Peaufiner » 636 → 685 sous les pinceaux 651 → 695 — **défaut préexistant** ; **le
Promi par le geste de la fiche** : « à Rachel » ajoute une ligne, l'aide descend de 26 pt (590 → 664) sur les pinceaux. Par
le chemin normal, au repos, la phrase d'un Promi ne porte pas de personne : pas de recouvrement — je n'ai pas trouvé au doigt
le chemin qui y pose une personne, donc je ne peux pas dire si le chemin normal le montre aussi. Les deux gestes, eux,
fonctionnent jusqu'au bout.

### 5 bis · Une seule fiche par personne — les chemins, touchés au doigt (après la clôture, 11 sept.)
Tom : « quel que soit le chemin, on arrive sur la même fiche ». Chaque nom et chaque visage visibles, touchés un par un sur
douze écrans (journaux : `sauvegardes/audit-fiche-personne/chemins/`, détail QUESTIONS.md Q195). **Aucun chemin n'ouvre autre
chose que cette fiche** — ni l'ancienne, ni une variante ; le seul autre écran d'une personne, `#profileScreen` (le tien),
n'a aucun appel. **Cinq chemins manquants → CHANTIERS n° 63**, dont un vrai trou : **depuis une Nuée, rien ne mène à ses
membres** (« Avec Rachel, Adrien, +3 » inerte, aucun disque de membre). Dans une carte du Fil ou de l'Index, le nom ouvre la
parole, pas la personne — c'est le toucher de la carte : question ouverte (Q195). app.html inchangé (`faff6e93…`).

### 6 · Ce qui reste ouvert
**chantier 63 (les chemins manquants vers la fiche, § 5 bis ci-dessus)** · « Tenu ensemble » à valider · chantier 60 (« à le groupe ») · chantier 61 (les libellés de carte en Bricolage 600 et le §6) ·
chantier 62 (page + : l'aide sous la phrase passe sous les pinceaux — préexistant sur le Chiche, visible sur le Promi ouvert
depuis la fiche d'une personne) ·
la densité et le capteur sur un vrai téléphone (Q178) · **chantier 59** — la voie retenue par Tom (« seule la teinte cède,
la mémoire du monde est préservée ») : il l'appelle « C60 » et « piste 4 », c'est le n° 59 · **le Cercle, pas commencé**
(et avec lui « comment ça évolue », Q183) · le monde de plantation sur les cartes (lot « brancher les peintres », §4).

## ⚑ UN CHICHE FIGURE SUR LA FICHE DE SON COMPAGNON — `lot-PERSONNE-AVEC` · 11 septembre 2026

> **`app.html` modifié** — md5 avant `a57f16aedee5ca615d82bd03438a9e25` (sauvegarde `sauvegardes/app-avant-personne-avec.html`),
> **après `6f2f028d149a9b1bc5ffa0771250b76e`**. Un bloc neuf en fin de fichier ; aucune règle existante touchée, rien du
> moteur de la Toile. Tom : *« avec non lu par openPerson : corrige. C'est un vrai bug, pas une décision. »*

**Le défaut.** Un Chiche engage trois personnes : qui le lance (`from`), le défié (`who`) et le **compagnon** (`avec`). La
fiche d'une personne (`openPerson`, l. 6312) ne lisait que `who` et `from` : un Chiche dont elle est la compagne n'y figurait
pas, alors que la rangée de disques d'une fiche compte déjà le compagnon (l. 3640). Au jeu de démonstration : **deux
rangées absentes** — « courir dimanche » chez Rachel, « vider le composteur à deux » chez Adrien.

**Le correctif.** `openPerson` redéfinie dans le bloc `lot-PERSONNE-AVEC`, **à l'identique à un seul changement près** : le
filtre des paroles lit aussi `avec`. Personne n'enveloppe `openPerson` (vérifié : aucune affectation ni enveloppe) — la
redéfinir ne défait aucun autre lot. L'original reste en place l. 6312. Rien d'autre ne bouge : la fiche refaite est un
autre lot, sur planche (`PLANCHE-FICHE-PERSONNE-3.html`, en attente du choix de Tom).

**La preuve, dans les deux sens** (`sauvegardes/audit-fiche-personne/outils/preuve_avec.py`) : sur chaque fiche, les
rangées doivent être exactement les paroles où la personne est `who`, `from` ou `avec`.
```
avant (sauvegarde)   Rachel 3/4 (manque « courir dimanche ») · Marion 3/3 · Adrien 2/3 (manque « vider le composteur »)  → PRIS
après (app.html)     Rachel 4/4 · Marion 3/3 · Adrien 3/3, aucune erreur de page                                          → COMPLET
```
**Série complète, EN SÉRIE, sur `6f2f028d…`** (`bat_apres12.log`, 00:14 → 00:39) — 17 batteries, aucune en erreur :
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande 19/19 · redteam_toile 17/17 ·
redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite · redteam_vide 61/61 · redteam_air ✅ 442 paires
· redteam_champ 32/32 · releve-design ✅ aucun écart · redteam_fonctions 22/22 · redteam_polices 0 couple absent ·
redteam_superpo 0 recouvrement · releve-aura ✅ au vert (ce chargement ne tirait aucune dalle sous le plancher).

## ⚑ LE PLANCHER DES DALLES — le juge de la Pelote mesure chaque dalle là où elle est · 10 septembre 2026

> **`app.html` inchangé** (`a57f16aedee5ca615d82bd03438a9e25`). Seul le juge change : `releve-aura.py`, famille 10
> « la matière » (original `sauvegardes/releve-aura-avant-plancher.py`). Une ligne au §8 de CLAUDE.md (original
> `sauvegardes/CLAUDE-avant-plancher-dalles.md`). Q192 ouverte, Q191 mise à jour.

### 1 · Les deux questions de Tom
*« "Pas plus faibles qu'en sombre à 5 près" est une borne relative… Ajoute un plancher absolu. »* — *« Ton filtre à 300
cellules : dis-moi ce qu'il écarte. Vérifie qu'aucune dalle réelle du jeu de démonstration ne tombe sous ce seuil. »*

### 2 · Ce que le filtre écartait — la dalle qu'il devait voir
Inventaire des îles RÉELLES (centres du moteur exporté, recoupés avec `_auraComp.derniere` : écart 0), même page, deux
thèmes, cinq chargements. Le masque « avec − sans » (seuil 12) **fragmente une île pâle** : sous son centre, 1 à 96
cellules ; son plus gros morceau faisait 442/438 dans un chargement (gardé), **212/176 et 187/274 dans deux autres —
jetés**. **Oui, une dalle réelle tombait sous 300 : la plus illisible, dans deux chargements sur cinq** ; le juge
rapportait alors la suivante comme « la plus faible ». Aucune île lisible n'y tombait ; le bruit du poil plafonne à 60.
**Le filtre est retiré** : chaque île se mesure à son cœur (disque de ½ rayon projeté), là où le moteur la pose, de face
seulement (z > 0,35), et le juge vérifie qu'il retrouve les îles de l'app avant de mesurer.

### 3 · Le plancher est en COULEUR — la luminance ne lit pas une dalle
L'île orange se lit franchement à Δlum 18–21 ; l'île bleue sur bleu ne se lit pas à 13–14. En ΔE (CIELAB, couleurs
moyennes au cœur, avec et sans l'île) : **84–94 contre 9–11**. Le 42 du §3 est un écart de luminosité entre deux
aplats ; sur une dalle texturée sous le poil, une dalle blanche bien lisible n'y fait que 25 à 39.

### 4 · La valeur : 15 — calibrée à l'œil, à valider sur un téléphone (Q192)
```
vu ILLISIBLE   9,4 · 10,4 · 10,8 · 11,1 · 14,0          (sonde orange sur orange : 7 à 13)
vu LISIBLE     16,3 · 17,1 · 18,3 (sphères de sonde) · 21,2 (moucheté pâle, clair) · 24,1 · le reste ≥ 25
```
Un premier plancher à **20** nommait des dalles lisibles (16 à 18) : **baissé à 15**. Marge mince (14,0 / 16,3).

### 5 · La preuve — `preuve_plancher.py`, le code du juge importé
Les couleurs étant tirées au hasard, le défaut se FABRIQUE : le sol prend la couleur BRUTE de la dalle la plus lisible
(la dominante de sa vraie dalle — stable dans une page, vérifié : trois rendus identiques). **Nommée** en sombre (9,5)
et en clair (7,0), avec les deux autres dalles de la même couleur ; les deux lilas, bien lisibles, **non nommés** —
conforme à l'œil sur les images. Sol loin de toutes → **rien**. Sonde défaite → la page remesurée au centième.
Un premier essai de sonde (la couleur vue au cœur, « corrigée de l'ombrage ») **ne noyait pas la cible** (90 → 30) :
retiré, dit. `preuve_matiere.py` reste verte (3/3) ; le critère relatif, pris désormais sur les îles réelles, a mordu
sur la « 2 » — avec l'écart et le contour, pas seul (Q191).

### 5 bis · LA PREUVE SUR LE CAS RÉEL — rien de posé (Tom : « l'île bleu-sur-bleu doit être prise »)
`preuve_cas_reel.py` (copié dans `sauvegardes/aura-pelote-lot/clair/`, journal et images dans `…/clair/cas-reel/`) : on
recharge, et sur les MÊMES pixels on passe l'ANCIEN juge (`releve-aura-avant-plancher.py`) et le NOUVEAU.
```
chargement 2 · sombre   « monter la serre »    ΔE  8,0   76 morceaux, le plus gros 39 cell. → jetée    ancien : rien   nouveau : NOMMÉE
chargement 3 · sombre   « le grand plongeoir » ΔE 12,9  138 morceaux, le plus gros 41 cell. → jetée    ancien : rien   nouveau : NOMMÉE
                clair   les mêmes, ΔE 8,3 et 14,0 — gardées par le filtre (313, 481)             ancien : rien   nouveau : NOMMÉES
chargement 1            aucune dalle sous 15 (la plus faible 29,9 / 25,7)                        ancien : rien   nouveau : rien
```
En clair, l'ancien juge se taisait alors que le filtre gardait l'île : **la borne relative laissait passer**, le sombre de
référence étant aussi mauvais — la faille que Tom avait nommée. À l'œil, les trois dalles nommées ne se lisent pas.
**Le plancher (15) — pourquoi :** au-dessus de l'amas illisible (max 14,0), bas devant ce qui passe (lisible naturel dès
21,2 ; dalles pâles des sondes, lisibles, 16,3–18,3). Critère relatif de luminance **gardé** en plus (Tom).
Leçon au §7 de CLAUDE.md : « une dalle se lit par sa teinte — un seuil de luminance seul ment dans les deux sens ».

### 6 · CE QUE LE PLANCHER RÉVÈLE — le bleu sur bleu, environ un chargement sur deux
Sur six chargements mesurés en ΔE, **trois** portent une dalle sous 15 en sombre, **deux** en clair. C'est le tirage
de couleur du moteur (`cc()`, `Math.random`, code de la Toile) contre un sol qui EST la couleur de nature. **Le défaut
existait avant le thème clair, et le sombre est autant touché.** `releve-aura` rougira donc environ une fois sur deux,
en nommant la dalle : il dit vrai. **Non corrigé — et tranché par Tom : c'est un CHANTIER, pas une question** (CHANTIERS.md n° 59) : *quand une dalle est
trop proche du sol, sa couleur doit être écartée à la plantation.* Non urgent ; d'ici là le juge rougit quand le tirage
tombe mal, et c'est ce qu'on lui demande. Compté sur tout ce qui a été relevé : 6 chargements sur 10, 12 dalles sur 99,
la pire à ΔE 8,0.

### 7 · Contrôles
**`releve-aura`, joué seul avec le plancher : ❌ 2 ÉCARTS — les deux le MÊME défaut** : « la dalle « rapporter le livre »
est illisible : ΔE 8,1 » en sombre, 9,8 en clair (`juge_plancher_2.log`). Toutes les autres familles à 0 ; matière :
sombre 75,1 (décidé 76) · clair 83,1 (85) · contour 94,7 · ΔE des dalles 50 51 37 39 **8** / 44 41 32 32 **10**. Le
chargement d'avant (plancher alors à 20) était vert : aucune dalle n'y était tirée près du sol (ΔE ≥ 36). **C'est le
comportement attendu tant que Q192 n'est pas tranchée** — le juge n'a pas été desserré pour rester vert.
Série des 17 batteries **non repassée : l'app n'a pas bougé** (même md5 que `bat_apres11.log`, 17/17).
Images sur disque, regardées, non envoyées : `sauvegardes/aura-pelote-lot/clair/iles/` (vignettes, marques),
`…/iles/de/` (les trois chargements en ΔE), `…/plancher/` (tel quel, mord, passe, deux thèmes). Instruments copiés dans
`sauvegardes/aura-pelote-lot/clair/` : `inventaire_iles.py` (⚠ son appariement « la plus proche » s'est trompé d'île :
remplacé par `iles_meme_page.py`), `vignettes_iles.py`, `couleur_dalle.py`, `preuve_plancher.py`.

## ⚑ L'PELOTE EN THÈME CLAIR — la peau s'éclaircit, le poil garde sa nature · 10 septembre 2026

> **`app.html` modifié** — md5 avant `8e579374b07507b90015e0f6d18bb437`, **après `a57f16aedee5ca615d82bd03438a9e25`**. Même bloc
> `lot-AURA-PELOTE`, refabriqué ; une cinquième retouche du peintre, dite (`PEINT_PEAU` dans `fabrique.py`).
> Aucune règle existante touchée, aucune ligne du moteur de la Toile. **Le thème sombre est intact** : la
> retouche ne joue que si `peauVers` est donné, et il ne l'est qu'en clair.

### 1 · LE DÉFAUT — la Pelote n'avait jamais été peinte que sur fond sombre (Q182)
La planche peint sur `#16171B` (`_v_planche.js` l. 427). Dans l'app le canevas est transparent. La PEAU sous
le poil est la couleur du lieu × 0,64, et son alpha suit la part peinte : dans les cellules du sol, au poil
court, elle est semi-transparente — en sombre la page ne se voit pas, en clair le crème passe. Résultat en
clair : des plages bleu nuit à bords polygonaux, une tache presque carrée sur la sphère vide, et une boule
qui « crève l'écran » (boule ↔ page 130, contre 76 en sombre — métrique du §3).

### 2 · L'ARBITRAGE — mesuré, trois voies, puis trois essais (Tom : « ta version d'abord »)
```
                                          boule↔page   contour   dalles (médiane)
sombre (référence)                           ≈ 76         60          ≈ 57
A · poil de nature, peau → teinte claire      93          96           54     ← contour et dalles tiennent
B · poil inversé (corps sombre §1.3)          138         151          105    (des taches)
C · la « 2 » (poil clair, peau assombrie)     66          39 ✗         25 ✗   (plages revenues)
```
Tom : *« Fixe A. Ma règle était mal posée — les dalles sont le point dur. Un objet trop présent se corrige ; un
objet qui se dissout, non. »* Puis trois essais pour rattraper l'écart sans toucher aux dalles (même page) :
peau à 30 % vers le crème (90,6), **à 60 % (85,1 — retenu)**, poil 15 % plus clair (88,3). **Retenu : A2** —
la peau part ENTIÈREMENT vers la teinte claire de la nature (§1.2), elle-même tirée à 60 % vers le crème du
corps (§1.3). **Les 9 points au-dessus de 76 sont ASSUMÉS** : un excès de présence, pas une dissolution.

### 3 · LE CONTRÔLE — la famille 10 du juge, « la matière »
> **⚠ Repris le même jour — voir « LE PLANCHER DES DALLES », plus haut.** Le filtre à 300 cellules décrit ci-dessous est
> RETIRÉ (il perdait la dalle la plus illisible), chaque île se mesure là où le moteur la pose, et un plancher absolu en
> couleur s'ajoute (ΔE 15, Q192). « Pas de seuil absolu sur les dalles » n'est plus vrai.

`releve-aura.py` (original `sauvegardes/releve-aura-avant-clair.py`) — valeurs EN DUR : boule ↔ page 76 en
sombre, 85 en clair, ± 8 ; contour ≥ 42 ; les dalles du clair pas moins lisibles qu'en sombre, **dans la même
page** (médiane et plus faible, à 5 près). ⚠ **Pas de seuil absolu sur les dalles** : leurs couleurs sont
tirées au hasard à chaque chargement — la médiane du sombre a varié de 57 à 41 d'une page à l'autre. Les îles
se découpent par le masque « sans îles » (une trame VIDE : `trame:null` fait lever le peintre — mesuré), en
composantes de 300 cellules au moins (en dessous, c'est du bruit du poil). **Prouvée contre de vrais défauts** (`preuve_matiere.py`, le code du juge
importé) : A2 tel quel — rien ; la « 2 » posée en clair — PRISE (écart 68,4 au lieu de 85, contour 39,2) ; la
boule sombre posée en clair — PRISE (écart 129,3). Et sur l'app d'avant (`8e579374…`) le juge prend 3 écarts
(clair à 129, et l'app ne sait pas masquer ses îles). **⚠ Réserve, dite telle quelle : la partie « dalles » n'a
pas encore été vue mordre SEULE** — sur la « 2 », ce sont l'écart et le contour qui ont pris ; dans cette page le
sombre de référence était lui-même faible (médiane 31,6, les dalles étant tirées au hasard), et les dalles de la
« 2 » ne passaient pas sous la barre. Q191.

### 4 · CE QUE L'INSTRUMENT M'A FAIT DIRE DE FAUX — deux fois
- La première passe de mesure a rendu des ZÉROS et une ligne « îles » qui recopiait « boule ↔ page », sans
  rien dire : le masque `trame:null` arrêtait le peintre. L'instrument vérifie désormais chaque image (pas
  d'erreur, boule peinte) et s'arrête s'il mesure du vide.
- La mesure des îles a changé de 57 à 41 d'une page à l'autre : dalles tirées au hasard, et du bruit dans le
  masque. D'où le filtre à 300 cellules et la comparaison dans la même page.

### 5 · CONTRÔLES
**Série complète, EN SÉRIE, sur l'app insérée `a57f16ae…`** — `bat_apres11.log`, 17 batteries, aucune
sortie en erreur : redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · redteam_demande
19/19 · redteam_toile 17/17 · redteam_geste 13/13 · redteam_verbe 6/6 · redteam_filets 0 filet parasite ·
redteam_vide 61/61 · redteam_air ✅ 442 paires · redteam_champ 32/32 · releve-design ✅ aucun écart ·
redteam_fonctions 22/22 · redteam_polices 0 couple absent · redteam_superpo 0 recouvrement · **releve-aura ✅ au
vert, dix familles** — la matière : sombre 76,8 (décidé 76), clair 81,8 (décidé 85), contour 94,7, dalles du clair
39,3 / 56,1 contre 31,2 / 55,3 en sombre. Preuve des 18 contrats sur la même app : ils mordent.
**Captures sur disque, regardées, non envoyées** (`sauvegardes/aura-pelote-lot/clair/captures/`, deux thèmes,
cinq phrases et l'état vide) : en clair la sphère est un pervenche homogène — plus aucune plage polygonale, le
poil se lit en sombre sur la peau claire, le contour est net ; **la sphère vide en clair n'a plus sa tache
presque carrée** (le pire cas, celui de la première impression), et son bouton est entier ; les îles se lisent,
l'orange franchement, les lilas plus doucement ; le sombre n'a pas bougé. L'air de la colonne, remesuré, est
intact (phrase → disques 27,1 / 27,7 ; libellés → bouton 28,5).

### 6 · LA SUITE (ordre de Tom)
La fiche de la personne, **audit d'abord** (Q184) · la densité et le capteur sur un vrai téléphone (Q178) ·
le Cercle. Le chantier 58 reste hors de tout ça, prioritaire au retour à la performance.

---

## ⚑ L'AIR DE LA COLONNE DE L'AURA — la cote se dérive, la colonne défile · 10 septembre 2026

> **`app.html` modifié** — md5 avant `e10da6dc1bfb81aef2081b34e0c39b6b`, **après `8e579374b07507b90015e0f6d18bb437`**.
> Même bloc `lot-AURA-PELOTE`, refabriqué (`sauvegardes/aura-pelote-lot/fabrique.py`) : aucune règle
> existante touchée, aucune ligne du moteur de la Toile. Tom : *« sous le commentaire de la sphère, les
> disques sont trop près : ça ne respire pas. Baisse tout ce qui est en dessous. Mesure, ne rapproche
> pas à l'œil, et vérifie sur l'image rendue. C'est la quatrième fois qu'un espacement revient, ça ne
> doit plus arriver. »*

### 1 · MESURÉ AVANT DE TOUCHER — aux boîtes ET à l'encre, les cinq phrases, deux thèmes
`sauvegardes/aura-pelote-lot/mesure_air_aura.py`, relevé `air_avant.log` :
```
                                   phrase d'une ligne   phrase de deux lignes
sphère → phrase                         50,3                  50,3
PHRASE → DISQUES                        27,3                   3,7   (5,5 à l'encre)
prénoms → légende                       28,0                  28,0
légende → « ce que tu as tenu »         28,0                  28,0
LIBELLÉS DES DALLES → BOUTON             2,7                   2,7
```
**La cause — le piège du §8, « une cote dérivée n'est pas un espace » :** la planche posait les Noyaux à
**454** (396 dans son gabarit), calcul fait pour une phrase d'UNE ligne. Deux des cinq phrases de Tom en
font DEUX (« Rien de ce qui est ici n'a été dit à la légère. », « On ne dirait pas comme ça, mais c'est
du solide. ») : la seconde ligne mangeait l'air. **Mon port avait recopié le défaut de la planche à
l'identique** — et aucun relevé fait sur une seule phrase ne pouvait le voir. Et les libellés des
dalles touchaient le bouton (2,7 pt ; 1 px dans la planche), dans tous les états.

### 2 · LA CORRECTION — la colonne se dérive, et elle défile
- **`place()`** (aura.js) : les Noyaux = bas RÉEL de la phrase + **26,675** (l'air que la planche laissait
  sous UNE ligne : 454 − 403,7 − 18,9 × 1,25) ; la légende et « Ce que tu as tenu » suivent du même écart
  (28 de chaque côté, inchangé) ; le bouton = bas des libellés + **28** (le rythme de la colonne). La
  fonction compare avant d'écrire, et se relance quand la phrase change de hauteur (polices arrivées).
- **La colonne DÉFILE sous le plateau** : le cadre garde ses cotes 390 × 844, défile, et ROGNE au bas du
  plateau (`clip-path: inset(100px 0 0 0)`) — la parade de l'Index (§8). Il se DÉCLARE (`data-defile`).
  La sphère garde `touch-action:none` : un doigt posé sur elle la tourne, il ne fait pas défiler.
- **Le bouton n'est JAMAIS coupé par le pli** (Tom — Q186 : *« un vrai défaut, pas un choix »*) : à
  l'ouverture il est ENTIER avec sa marge (bas ≤ 822) ou FRANCHEMENT sous le pli (haut ≥ 844). Avec l'air
  de 28, il ne peut plus être entier dès qu'il y a des Noyaux : il tombe sous le pli, on le découvre en
  défilant. (Une première version le laissait coupé : de 3,4 pt avec une phrase d'une ligne, à mi-hauteur
  de son libellé avec deux — 34 pt visibles sur 60.)
- **Rien au-dessus de la phrase ne bouge.** L'état vide ne bouge pas (le bouton y reste à 762, entier).

**Après** (relevé `air_apres.log`, deux thèmes identiques) :
```
                                   phrase d'une ligne   phrase de deux lignes
PHRASE → DISQUES                        27,7                  27,1   (28,0 / 29,0 à l'encre)
prénoms → légende → titre              28 · 28               28 · 28
LIBELLÉS DES DALLES → BOUTON            27,8                  27,8
la colonne défile de                    ≈ 26 pt               ≈ 49 pt
```
**Le pli, mesuré sur la version insérée** (`air_pli.log`, deux thèmes identiques) : dans les états
non vides, le bouton est FRANCHEMENT sous le pli — son haut à 844 exactement, rien de lui ne se voit à
l'ouverture ; libellés → bouton 84,4 pt (phrase d'une ligne) et 61,4 pt (deux lignes), la colonne défile de
≈ 82 pt. **Dans l'état vide, le bouton est ENTIER à l'ouverture, 22 pt du bord** (bas 822) — c'est le seul
écran qu'un nouveau verra (Tom). **⚠ Mais rien n'annonce le bouton sous le pli** : sous les derniers
libellés, 84,4 / 61,4 pt de fond nu jusqu'au bas de l'écran, rien ne passe le pli.
**Q187, tranché par Tom — c'est le fond nu qui trahit, pas le bouton ; on supprime le vide, on n'ajoute pas
de signe** (ni flèche, ni ombre, ni fondu : trois choses interdites). « Ce que tu as tenu » porte jusqu'à
**SIX** dalles, deux rangées : une rangée de plus, que le bord de l'écran coupe, dit qu'il y a la suite —
le principe de la rangée des six qui défile. **Mesuré** (`mesure_rangees.py`, le DESSIN des dalles, simulé à 3 · 4 · 5 · 6 · 9 tenues) :
```
paroles tenues   phrase d'une ligne (3 phrases sur 5)             phrase de deux lignes (2 sur 5)
3 ou 4           une rangée · bouton sous le pli, fond nu           idem
5 (3 + 2)        2e rangée : trou à droite · dessins entiers,       trou à droite · dessins cachés à 26 %
                 à 8 pt du bord · libellés sous le pli
6 et plus        2e rangée pleine · dessins entiers, POSÉE contre   2e rangée pleine · cachée à 26 %
                 le bord · libellés sous le pli
```
**RÈGLE (Tom — Q189) : la seconde rangée paraît à partir de CINQ dalles tenues ; en dessous, la
première seule** — une rangée au tiers (3 + 1) dirait « il en manque deux ». À cinq, le trou d'une case est
accepté. Portée dans le code (`K.RANG2`, `nbMoisson()`) et EN DUR dans le juge (`RANG2`). **Prouvée** : sur l'app d'avant (`31a0ed37…`) le juge
prend « 3 dalles tenues au lieu de 5 » ; sur la version corrigée il passe ; mesurée à 3 · 4 · 5 · 6 · 9 tenues —
à quatre, une rangée (3 dalles) ; à cinq, 3 + 2 ; à six et au-delà, deux rangées pleines.
**Restent ouverts :** avec une phrase d'une ligne, la seconde rangée est posée contre le bord plutôt que
franchement coupée ; et à quatre tenues ou moins, le fond nu revient (Q188) — le bouton ne peut pas y rester
entier avec l'air de 28 (son bas tomberait à 848 ou 871).
**Q188 — quand il n'y en a pas assez :** dès qu'on a tenu trois paroles ou moins, il n'y a qu'une rangée et
rien à couper ; le fond nu revient. C'est une question de COMPOSITION de la colonne, posée à Tom.

### 3 · LE CONTRÔLE — pour que ça n'arrive plus (CLAUDE.md §8, « un espacement qui revient pour la cinquième fois »)
**J'ai réécrit un contrat de test et j'en ai ajouté un** (`releve-aura.py` ; original
`sauvegardes/releve-aura-avant-colonne.py`) :
- **positions** : la rangée, la légende, le titre et le bouton ne sont plus attendus à des cotes figées
  (454 · 589 · 633 · 762) — ils se DÉRIVENT du bas réel de la phrase et des deux airs décidés, **écrits en
  dur dans le juge** (26,675 et 28).
- **9ᵉ famille, « air de la colonne »** : pour CHACUNE des cinq phrases, deux thèmes, CHAQUE paire de
  blocs, texte ou non — phrase → disques ≥ 26 et indépendant du nombre de lignes, légende centrée,
  libellés → bouton ≥ 26, **le bouton jamais coupé par le pli à l'ouverture** (Q186), bouton atteignable
  en défilant, rien du cadre au-dessus du plateau une fois
  défilé ; **et à l'encre, sur l'image rendue**, phrase → disques ≥ 26. `redteam_air.py` ne mesure que des
  paires de TEXTES : il ne pouvait pas voir une phrase contre une rangée de disques.
- **débordements** : un bloc qui dépasse VERS LE BAS dans une colonne DÉCLARÉE, qui tient dans l'appareil
  et qui rogne, n'est pas un débordement (la règle de la rangée glissante, tournée d'un quart).
**Prouvés dans les deux sens :** sur l'app d'avant (`e10da6dc…`) le juge est PRIS — 8 écarts de position,
20 d'air (3,7 pt sous la phrase, 2,8 sous les libellés, 6,0 à l'encre) ; sur la version corrigée il
passe. La preuve des 18 contrats de l'Aura, sur l'app insérée finale (`8e579374…`), avec l'instrument corrigé : **deux passes, les 18 passent tels quels et PRENNENT le défaut posé exprès** (`preuve_finale_1.log`, `preuve_finale_2.log`, journaux entiers). La règle du pli, prouvée elle aussi : sur la version d'avant (`3ec7bd34…`) le juge prend le bouton COUPÉ à l'ouverture (33,6 pt visibles sur 60 avec deux lignes, 56,6 avec une), sur la version corrigée il passe. Les contrôles réécrits contre des sondes (`preuve_defile.py`) : la version telle quelle passe ; les quatre défauts
sont PRIS — le cadre qui ne se déclare plus, le cadre qui ne rogne plus, un bloc qui sort par le côté
(pris par `DEBORD`), le cadre qui défile sans rogner sous le plateau (pris par `PROTEGE`). Le code testé
est celui du juge, importé. **⚠ Une sonde a d'abord été AVALÉE** (§7) : posée dans `<head>` avec la même
spécificité que le bloc, qui vient après elle, elle ne s'appliquait pas — la colonne défilait encore de
48 pt. Renforcée, et chaque sonde affiche désormais l'état réellement obtenu avant d'être jugée.

### ⚠ LA PREUVE A ROUGI UNE FOIS APRÈS INSERTION — ARRÊT, RESTAURATION, ET CE QUE C'ÉTAIT
Règle de Tom : *batterie verte qui rougit → arrêt immédiat et restauration*. Insérée, la version à la règle
des cinq (`8e579374…`) a donné **2 contrats « légende centrée » NON PRIS** (redteam_ecrans et redteam_air).
La série a été arrêtée, **`app.html` remis à `e10da6dc…`** (la dernière série complète verte), la version
rouge gardée à côté, tout le diagnostic fait sur une COPIE.
- **Le contrat n'était pas éteint** : isolée, la sonde (+9 px sur la légende) s'applique et se voit
  (28/28 → 37/19), sur la version rouge comme sur la verte ; rejouée, la preuve la PREND.
- **C'était l'instrument** : la sonde et la mesure étaient posées en DEUX appels ; une image pouvait passer
  entre eux, la colonne se recalculer (`place()`) et réécrire la cote de la légende — la sonde était
  avalée (§7, « une sonde qui n'est pas prise peut être avalée »). **Sonde et mesure sont désormais dans la
  MÊME tâche** — le contrat ne change pas ; original `preuve_contrats-avant-meme-tache.py`.
- **L'audit des sondes (demandé par Tom) a trouvé deux contaminations DANS une passe** (pas d'une passe à
  l'autre : chaque passe ouvre une page neuve) : les sondes de la légende se « défaisaient » par
  `removeProperty('top')`, ce qui effaçait AUSSI la cote écrite par `place()` — la légende retombait sur
  l'ancienne cote figée du CSS jusqu'à la réouverture ; et la sonde de la phrase remettait le texte sans que
  la colonne se recalcule tout de suite. **Corrigé** : chaque sonde remet la valeur d'avant et sa priorité,
  la phrase remise force le recalcul, et **le verdict nomme les contrats qui ratent** (original
  `preuve_contrats-avant-retraits-exacts.py`). Piège inscrit au §8 de CLAUDE.md.
- Sur six passes, une autre a donné « 1 contrat à reprendre » **sans que je sache lequel** — mon filtre
  n'imprimait que la légende et le verdict, le journal entier n'était pas gardé : l'instrument était
  aveugle (Q190, « vu une fois, non reproduit ») ; **non reproduit** : sept passes de suite à 18/18 sur la version rouge,
avec l'instrument corrigé (`preuve_rouge_1…7.log`). Je le dis tel quel : non reproduit, non identifié. Puis
réinsertion (`8e579374…`, identique à la copie jugée) et série complète.

### 4 · CONTRÔLES
**Série complète, EN SÉRIE, sur l'app insérée finale `8e579374…`** — journal
`sauvegardes/aura-pelote-lot/bat_apres10.log`, 17 batteries, aucune sortie en erreur :
```
redteam_ecrans      150/150        redteam_vide        61/61
redteam             15/15          redteam_air         ✅ 442 paires, 38 écrans, deux thèmes
redteam2            10/10          redteam_champ       32/32
redteam3            18/18          releve-design       ✅ aucun écart
redteam_demande     19/19          redteam_fonctions   22/22
redteam_toile       17/17          redteam_polices     0 couple absent
redteam_geste       13/13          redteam_superpo     0 recouvrement de texte
redteam_verbe       6/6            releve-aura         ✅ au vert — 9 familles (air de la colonne compris)
redteam_filets      0 filet parasite
```
(`redteam_air` compte 442 paires au lieu de 448 : les libellés de la seconde rangée sont sous le pli,
il y a moins de textes visibles à apparier ; aucun air ne s'est resserré.) Syntaxe : `node --check` — OK.

### 5 · DÉCISIONS ET CONSTATS DE CE TOUR (QUESTIONS.md)
- **Q181 VALIDÉ** — le régulateur n'applique son palier qu'à l'ouverture suivante ; l'alternative en fondu attend.
- **La sphère ne s'explique pas** (décision Tom) — pas de légende, pas de phrase qui dit ce qu'elle est.
- **Q184** — la fiche de la personne : hors DA, trois interdits (la courbe « COMMENT ÇA ÉVOLUE » → Cercle,
  Q183 ; un mot d'harmonie pointé vers quelqu'un → règle 1 ; « 3 Promi échangés · 1 reçu · 2 donnés » →
  règle 4). **Rien de corrigé** : c'est le lot suivant, avec un audit.
- **Q185** — l'aide « i » décrit l'ancienne Aura (grand chiffre, harmonie, jauge, meilleure Nuée).
- **Q187 TRANCHÉ (Tom)** — supprimer le vide, pas ajouter un signe : une seconde rangée de dalles, coupée par le bord.
- **Q188** — trois paroles tenues ou moins : une seule rangée, rien à couper — question de composition, pour Tom.
- **Le bouton en thème clair n'est pas bleu nuit** : il est à l'encre `#16171B` (trait et texte), la même que le trait
  du plateau — la grammaire des contours. Le seul bleu nuit de l'écran est le fond du plateau en SOMBRE, `#12142A`, la
  teinte de corps du §1.3, posée sur le sol `#16171B` de la planche ; et en clair, la plage de la sphère (Q182).
- **Q186 TRANCHÉ (Tom)** — la colonne qui défile est la bonne réponse (*« mieux vaut assumer le défilement
  que serrer »*) ; le bouton coupé est un vrai défaut : entier ou franchement sous le pli, jamais coupé.
- **Q185 — VÉRIFIÉ : l'aide « i » n'explique pas la sphère** (HTML statique, aucun script n'y écrit ; ni
  « sphère », ni « enroulée » ; « pelote » y désigne l'ancien double Noyau du Cercle). Elle décrit l'ancienne
  Aura : un lot de textes à part, non corrigé.
- Captures sur disque, non envoyées (`sauvegardes/aura-pelote-lot/colonne/`).

### 6 · LA SUITE — l'ordre fixé par Tom
1. **la Pelote en thème clair** — Q182 : la planche n'a été peinte que sur fond sombre ; trois options.
2. **la fiche de la personne** — Q184, **l'audit d'abord** (comme pour le partage), puis la DA.
3. **la densité et le capteur sur un vrai téléphone** — Q178.
4. **le Cercle.**
**Le chantier 58 reste hors de tout ça** — prioritaire quand on reviendra à la performance.

---

## ⚑ L'PELOTE EST DANS L'APP — `lot-AURA-PELOTE` · 10 septembre 2026

> **`app.html` modifié** — md5 avant `61280542751d0d0df5bce546f9a091b1`, **après `e10da6dc1bfb81aef2081b34e0c39b6b`**
> (rotation lente à 2 min — § 7 et Q173 ; retour de l'empreinte fini — § 4 quater ; régulateur de densité
> qui ne change plus rien sous les yeux — § 4 quinquies et Q181).
> Trois insertions intermédiaires ont été ANNULÉES : `8fa52b38…` (rotation plus lente), `a5a69b39…`
> (retour de l'empreinte qui sautait), `17e2e1ca…` (série verte, mais le régulateur changeait la
> matière sous les yeux).
> Sauvegarde : `sauvegardes/app-avant-aura-pelote.html`. Bloc neuf AVANT `</body>` : un `<style>`
> et deux `<script>` (`lot-AURA-PELOTE`, `lot-AURA-PELOTE-MOTEUR`). **Aucune règle existante touchée,
> aucune ligne du moteur de la Toile.** Point de reprise du chantier : `sauvegardes/pelote-velours/`.
> Matériel du lot : `sauvegardes/aura-pelote-lot/` (fabrique, css, js, preuves, mesures, captures, journaux).

### 1 · LE PREMIER CONTRÔLE — LA DENSITÉ. ⚠ PAS SUR UN TÉLÉPHONE.
Aucun appareil physique n'est joignable depuis cette machine. Ce qui suit est une mesure de
**substitution**, et je la dis comme telle : Chromium sur le Mac Intel i5-8279U (celui des bancs),
puis le même processeur **ralenti ×4** (profil « mobile moyen » de Lighthouse) et **×6**.
```
processeur  110 000    90 000    75 000     le gouverneur, parti de 110 000
   ×1      13,7 ms   12,2 ms   10,6 ms     reste à 110 000
   ×4      58,4 ms   51,9 ms   45,7 ms     descend à 75 000 (2 paliers) — 22 images/s
   ×6      88,6 ms   78,9 ms   69,7 ms     descend à 75 000 (2 paliers) — 14 images/s
```
**⚠ Et je le dis franchement : sur un processeur ×4, même le plancher ne tient pas 60 images par
seconde.** Le coût n'est pas proportionnel aux poils — 75 000 coûtent encore 78 % de 110 000. Une part
FIXE (~19 ms à ×4 : vider et verser le tampon 592 × 592, la peau, le comblement) dépasse à elle seule le
budget. **Le levier sur un appareil lent est la résolution du tampon, pas le nombre de poils.** → Q178.
**Ce qui répond au « si ça ne tient pas » : un régulateur, dans l'écran.** Il mesure chaque image ;
si la médiane dépasse une image à 60 Hz (16,7 ms), il VISE le palier le plus dense qui tiendrait
(110 000 → 90 000 → 75 000) ; si le palier du dessus tiendrait sous 15 ms au prorata des poils, il vise
de remonter. **La vise ne s'applique qu'à l'ouverture suivante, jamais sous les yeux** (§ 4 quinquies,
Q181 — un palier change 71 à 78 % des pixels). **La densité cède, jamais le comportement** — prouvé
sous ×6 : la rotation continue, le doigt tourne toujours, et la matière ne bouge pas d'une image.
**Ce qui reste à faire, par Tom : la mesure sur un vrai téléphone.** Servir le dossier sur le réseau
local par un SECOND serveur (le 8752 des outils ne bouge pas), ouvrir l'Aura dans Safari sur l'iPhone,
puis sur le Mac Safari → Développement → l'iPhone → console : `_aura.etat()` rend le palier tenu
(`palier`), la médiane par image (`ms`), le nombre de cessions (`cede`) et le palier visé (`vise`) —
**ouvrir l'Aura deux fois** : la vise ne s'applique qu'à l'ouverture suivante (Q181). **Dans le même geste, lever
la réserve du capteur** (le juge pilote une souris, pas un doigt : la taille du contact lue au capteur
n'est jamais testée) : pendant un appui, `_aura.etat().emp.a` rend le demi-axe réellement lu — 0,40 =
le pouce par défaut (le capteur n'a rien dit) ; entre 0,26 et 0,40 = le capteur a parlé. → Q178.

### 2 · LES CINQ FICHIERS — ET QUATRE RETOUCHES, DITES
Les cinq fichiers de `sauvegardes/pelote-velours/` sont portés **tels quels**, enfermés dans une
fonction (ils définissent `D`, `TAU`, `mix`, `hh`, `peint`… : posés à la racine, ils auraient écrasé
des globales de l'app). Rien ne sort sauf `window.PeloteMoteur`. Quatre retouches, chacune par motif
`assert count == 1` dans `fabrique.py`, et aucune autre :
- **`batIles` — la source de la dalle.** `Toile.dalleGeneree` n'existe QUE dans la copie du moteur ;
  l'ajouter à `app.html` = toucher la Toile. Dans l'app une île est un Promi réel : sa vraie dalle,
  `Toile.dalleTrame(cv, id, 1, p.monde)`. → QUESTIONS Q168.
- **Le peigne tourne avec l'objet** — voir § 4.
- **Une caresse se retouche en place** (`retoucheTraces`), au lieu de refaire tout le cache — § 4 ter.
- **L'empreinte s'éteint avec sa profondeur** (`PEINT_FE`) — § 4 quater.

### 3 · #auraScreen, RÉÉCRIT EN ENTIER, DEUX THÈMES
Cotes de `ecranAura()` ÷ 0,872 ; Noyaux au §2.9 à la lettre. Le plateau (`Aura`, le i, ✕ FERMER)
reste. L'ancienne Aura est masquée **nœud par nœud** (25 enfants nommés) : ses nœuds restent dans le
DOM, parce que `buildAura()` les adresse par id et que le gestionnaire de `#souffleBtn` n'est pas
protégé. L'ombre de dalle de `.tuto-fond::before` se peignait derrière la sphère : masquée ici seulement.
**Captures finales, à 2×, sur l'app insérée `e10da6dc…`**, regardées une à une avant envoi
(`sauvegardes/aura-pelote-lot/finales/`) :
- `aura_{dark,light}.png` — l'écran au repos : plateau, sphère et ses îles, la phrase, les trois Noyaux,
  la légende, « ce que tu as tenu », le bouton.
- `aura_{dark,light}_caresse.png` + `_caresse_carte.png` — la trace, face à nous (vue d'avant la caresse
  remise, puis figée) ; la carte montre avant | après | l'écart ×8, dite comme telle. **La première
  capture de la caresse ne montrait rien** — le glissement tourne la sphère, les îles partaient derrière
  et la trace ne se voyait pas : refaite (`capture_caresse.py`).
- `aura_{dark,light}_personne.png` — un toucher sur un Noyau ouvre la fiche de la personne : c'est
  l'écran EXISTANT de l'app, pas refait dans ce lot (il porte « COMMENT ÇA ÉVOLUE » — Q183).
- `aura_{dark,light}_vide.png` — l'état vide : sphère sans île, « La première parole laissera sa trace ici. »
- `aura_rotation_20s.webm` — **20 s de rotation lente, en temps réel, à 1×** (les ~11 premières secondes
  du fichier sont le chargement de l'app). Mesuré pendant le film : **1,0489 rad en 20 s = 0,0524 rad/s**,
  la vitesse décidée. Une vitesse ne se juge pas sur une image fixe.
- `retour_film.png` — le retour de l'empreinte, avant/après la correction (§ 4 quater).
- `regulateur/paliers_{dark,light}.png` — les trois paliers de densité à vue égale (§ 4 quinquies).
**⚠ En clair, le pavage de la sphère se lit** — grandes plages bleu nuit à bords polygonaux, et une
tache presque carrée sur la sphère vide. La planche n'a été peinte que sur fond sombre ; en clair, le
crème passe entre les poils courts du sol. Pas un défaut prouvé, mais jamais validé : **Q182, à
trancher** — rien n'est changé en attendant.

### 4 · ⚠ LE PEIGNE ÉTAIT LIÉ À LA VUE — DEUX ACQUIS SE CONTREDISAIENT
Le peigne de la planche est l'horizontale de L'ÉCRAN au moment où le cache se remplit. L'Pelote
tourne toujours : ~41 s plus tard un zéro du peigne — **un épi** — arrive au centre de la face ; et
chaque caresse recuisait le peigne : **une caresse changeait 77 % des pixels**, un relissage laissait
7,8 %. Peigne azimutal (`u = y × p`) : égal au B de la planche au centre de la face, indépendant de la
vue. **Une caresse : 9,2 %. Relissé : 0,0000.** `scratchpad/aura/peigne_comparaison.png`. → Q172.

### 4 bis · TROIS COMPORTEMENTS QUI AURAIENT CÉDÉ SUR UN APPAREIL LENT — corrigés
- **L'élan était perdu quand les images ralentissent.** Les mouvements du doigt étaient horodatés
  à leur TRAITEMENT : livrés groupés après une image lente, ils tombaient « au même instant », la
  vitesse sortait nulle. On lit l'heure de l'ÉVÉNEMENT (`timeStamp`) et chacun des événements
  regroupés (`getCoalescedEvents`).
- **La rotation lente ralentissait avec les images.** La planche bornait le pas de temps à 50 ms :
  à 130 ms par image, la rotation tombait au tiers. Borne portée à 100 ms (le temps réel ; la
  borne ne sert qu'après une pause).
- **Une caresse faisait une saccade au lâcher** (le cache refait pendant l'élan). Elle s'inscrit
  maintenant au repos. → Q171.
- **La densité ne pouvait que descendre, et c'était gardé.** Un passage lent l'aurait abaissée pour
  toujours : elle remonte si le palier du dessus, au prorata des poils, tiendrait sous 15 ms — à
  l'ouverture suivante, comme la descente (§ 4 quinquies).

### 4 ter · ⚠ L'IMAGE DE 267 ms PENDANT L'ÉLAN — TROUVÉE AU PROFILEUR, CORRIGÉE, PROUVÉE
Relevé du juge : la plus longue image de l'élan faisait **267 ms, dont 16 ms pour le peintre**. Tom :
*« c'est le moment précis où l'objet doit être fluide »* — priorité avant tout le reste. Profileur du
navigateur (échantillon 0,5 ms), trois lancers, chaque tâche longue attribuée à ses fonctions
(`scratchpad/aura/profil_elan.py`, `profil_taches.py`).
**Les deux suspects de Tom, écartés ou confirmés :**
- **Le glaneur de mémoire : écarté.** 158 ms sur 20 s (0,8 %). Le peintre n'alloue pas par image.
- **Un recalcul qui n'a rien à faire là : CONFIRMÉ, deux fois.**
  1. **L'ombre de dalle (`frame`, l. 8917) — 27 % du fil.** Elle écrit trois variables héritées sur les
     douze écrans `.tuto-fond`, fermés compris, à chaque image ; la lecture d'`offsetParent` force
     ensuite le recalcul de style de milliers de nœuds cachés. Deux hypothèses fausses d'abord, et je
     les dis : ce n'était pas l'écriture sur l'Aura seule (bloquée : 27 % restait), ni la réassignation
     de taille du canevas du peintre (remplacée par un effacement : 27 % restait). **Prouvé par une
     sonde : 27 % → 1,6 %.** Corrigé en n'ignorant que ces écritures-là, sur l'Aura et sur les écrans
     cachés dessous tant qu'elle est ouverte. Le coût demeure ailleurs dans l'app → Q180, hors lot.
  2. **La reconstruction complète du cache à chaque caresse — 240 à 340 ms.** Pour UNE caresse on
     refaisait les 110 000 poils, relief `phi` compris, qui ne dépend pas des caresses. **La caresse se
     retouche maintenant** (`retoucheTraces`, la seule addition au moteur) : seuls les points proches
     des arcs qui changent. **Prouvé égal à une reconstruction complète** sur trois caresses et un
     relissage : lustre et main identiques point par point, sens du poil à 2·10⁻⁶ près (arrondi 32 bits).
     **10 à 14 ms au lieu de 210 à 320.**
- Et `couvert()` ne consulte plus le navigateur qu'une image sur six (il forçait la mise en page).
**Après :** `frame` 1,7 % ; plus aucune tâche au-delà de 120 ms pendant trois lancers.

### 4 quater · ⚠ LE RETOUR DE L'EMPREINTE SAUTAIT À LA FIN — vu par Tom, corrigé, mesuré

Tom : *« la dernière étape avant que la sphère ne redevienne lisse… ça passe de trop loin encore
déformé à net d'un coup »*. **Deux causes, lues dans le peintre :**
1. **L'empreinte était retirée à p = 0,02**, quand elle était encore profonde de 7 % de son
   maximum (≈ 1,4 pt) et large de 27 % de sa taille — on l'enlevait visible.
2. **Trois de ses effets ne dépendaient pas de la profondeur** : le poil peigné en rosette sous
   le doigt (100 %), l'ombre au fond du creux (jusqu'à −80 % de lumière) et le poil raccourci
   d'un cran sur toute la calotte touchée. Ils restaient ENTIERS jusqu'à la dernière image,
   puis tombaient ensemble.

**Le correctif — une 4ᵉ retouche du peintre, dite (`PEINT_FE` dans `fabrique.py`) :** une part
d'effet `FE = min(1, (d/dmax)/0,3)`, pleine tant que le creux garde 30 % de sa profondeur
(donc **rien ne change pendant l'appui ni au début du retour**), puis proportionnelle à la
profondeur jusqu'à zéro. La rosette, l'ombre, la normale et la position du fond plat la
suivent ; le poil raccourci est **tramé** point par point (une part FE des points). Et
l'empreinte n'est retirée qu'à **p = 0,002** (0,4 pt, effets à 5 %) — quand elle est
invisible. La durée du retour, en usage, ne change pas : c'est le comblement (lié à la
rotation) qui la termine.

**Le contrôle, prouvé dans les deux sens :** `releve-aura.py` enregistre dans la page **chaque
image peinte du retour** et mesure le DERNIER PAS (dernière image déformée → première image
lisse) **en amplitude** — l'écart moyen en niveaux sur la zone du doigt : il ne doit pas
dépasser 3 fois la médiane des 10 pas qui le précèdent (plancher 0,5 niveau).
**⚠ Sa première écriture était MORTE, et c'est la preuve qui l'a dit.** Elle comptait la PART
des pixels qui changent. Un retour lisse en change déjà beaucoup, d'un rien, à chaque image
(médiane 17 %) ; le saut de l'ancienne version (43,9 %) passait dessous — **vert sur la version
fautive**. Réécrite en amplitude avant de juger la version corrigée, et bornée d'un plafond
absolu d'**1 niveau** : la règle relative seule ne prenait l'ancienne version qu'à 3,5 fois la
médiane pour un seuil à 3 — un contrat à marge mince oscille.

```
                     écart au repos, niveaux (zone du doigt)          DERNIER PAS   médiane   images
avant (p 0,02)       40,0 → 36,0 → 31,2 → 25,0 → 17,8 → 8,4 → lisse     8,45        2,48      119   ❌ pris
après (FE, p 0,002)  40,5 → 36,4 → 30,9 → 20,7 →  9,4 → 0,5 → lisse     0,46        0,83      131   ✅
```

Les 14 dernières images d'avant le retrait, corrigée : 4,9 · 4,4 · 4,0 · 3,7 · 3,3 · 2,9 · 2,6 ·
2,4 · 2,0 · 1,7 · 1,5 · 1,0 · 0,67 · 0,46 → lisse. Rien d'autre n'a bougé (rotation 0,0528,
élan à 0 écart de la loi, prise au millième) ; le creux vit 3,52 s au lieu de 3,29 — les
0,2 s de la fin qui manquait. Relevés : `sauvegardes/aura-pelote-lot/retour_{ancien,fe}.txt` ;
planche avant/après des dernières images : `retour_film.png`.

**Tom a validé le diagnostic et la correction, et demandé deux vérifications** (`preuve_retour_trace.py`,
ancienne version contre l'app insérée, trois fois chacune, vue figée, thème sombre) :
1. **Le retour reste-t-il rapide ?** On n'échange pas un saut contre une traîne.
2. **La trace survit-elle au creux ?** Ce qui disparaît, c'est la DÉFORMATION ; le poil couché, le
   lustré et la chroma restent — c'est le cœur du concept.

**Dans le code, d'abord :** `FE` n'est lu qu'à cinq endroits, tous dans le peintre — trois DANS le bloc
du contact (`if(E){`, qui ne tourne que tant qu'un doigt ou un creux existe), deux derrière `mo`
(les points que le contact touche). La trace, elle, vit dans le CACHE du peintre : le poil couché
(`champPoil(…, o.traces)`), le lustré (`m_poli`), la chroma (la boucle sur `o.traces`), et
`retoucheTraces` — **aucun ne lit `FE`**. Creux refermé, seul le cache peint. Et pendant le retour,
la rosette des points touchés se fond vers le sens du poil DU CACHE — celui qui porte déjà la
trace : la trace réapparaît en continu sous le creux qui s'efface, là où le saut la découvrait
d'un coup.

**1 · La durée — mesurée, trois fois chacune** (appui 950 ms, écart moyen au repos sur la zone du
doigt, en niveaux ; le temps compte depuis le lâcher) :
```
             moitié partie   reste 10 %   plus rien à l'œil (< 1 niv)   retirée    ce qui restait au retrait
avant          2,49 s          3,21 s       3,21 s — PAR UN SAUT          3,21 s      8,51 niveaux
après          2,33 s          3,21 s       3,40 s                         3,44 s      0,53 niveau
```
**Pas de traîne.** Le corps du retour est aussi rapide, plus rapide même à mi-course (−0,16 s : les
effets suivent la profondeur au lieu de rester entiers) ; les 10 % derniers tombent au même instant.
Ce qui s'ajoute, ce sont **0,19 s** — le temps que ces 10 % derniers se dissolvent au lieu d'être
coupés. En usage, c'est le comblement lié à la rotation qui termine le retour : il n'a pas changé.

**2 · La trace — elle reste.** Une caresse ; creux refermé et caresse inscrite, on mesure la part de la
boule qui la porte et son amplitude ; puis 5 s plus tard, même vue, contre un relissage pris JUSTE
APRÈS au même palier de densité :
```
                     juste après le creux          5 s plus tard            l'image a bougé de
avant  (110 000)     9,6 % des pixels · 1,48 niv    9,6 % · 1,48 niv         0,000 niv (×3)
après  (110 000)     9,6 % des pixels · 1,50 niv    10,3 % · 1,67 niv ¹      —
après  ( 90 000)     10,3 % des pixels · 1,67 niv   10,3 % · 1,67 niv        0,000 niv (×2)
```
**À densité égale, la trace est la même avant et après la correction** (9,6 % · 1,48 contre 9,6 % ·
1,50), **et elle ne bouge pas d'un niveau en 5 s.** ¹ Une seule image a bougé en entier (10 niveaux) :
le gouverneur venait de descendre de 110 000 à 90 000 poils — la série de batteries tournait à côté et
chargeait la machine. Tous les poils changent alors d'un coup ; la trace, mesurée contre un relissage
au même palier, est toujours là. **⚠ Ma première mesure ne l'avait pas vu** : elle comparait l'image de
5 s à une référence prise AVANT la caresse, donc avant le changement de palier — 3 passes sur 6
annonçaient « 76 % des pixels ont bougé ». C'était l'instrument, pas la trace.
Relevés : `sauvegardes/aura-pelote-lot/preuve_retour_trace.log`, `preuve_trace2.log`.

### 4 quinquies · ⚠ LE RÉGULATEUR DE DENSITÉ CHANGEAIT LA MATIÈRE SOUS LES YEUX — mesuré, tranché (Q181)
Vu en mesurant la trace : sous charge, toute l'image changeait d'un coup. Tom : *« si le régulateur
est nécessaire, il l'est — mais il doit être imperceptible »*. **Mesuré** (`mesure_regulateur.py`,
planches `regulateur/paliers_{dark,light}.png`, même vue figée) :
```
                          pixels qui changent   amplitude   luminance de la boule
sombre  110 000 → 90 000        71,4 %          10,7 niv     93,0 → 90,2   (−2,8)
sombre  110 000 → 75 000        76,1 %          14,1 niv     93,0 → 86,4   (−6,6)
clair   110 000 → 90 000        73,2 %          10,3 niv    106,7 → 111,5  (+4,8)
clair   110 000 → 75 000        77,6 %          14,9 niv    106,7 → 117,9  (+11,2)
premier passage à 90 000, sphère qui tourne : UNE IMAGE DE 783 ms (peintre 526 ms) — contre 50 au plus
sous ×4 : 110 000 → 90 000 à 7,2 s, → 75 000 à 13,9 s ; charge levée : → 90 000 en ≈ 3 s, → 110 000 en ≈ 13 s
```
- **Ça se voit.** Un palier n'est pas un sous-ensemble du précédent : c'est un AUTRE semis (la spirale
  dépend du nombre de poils) — chaque poil change de place. **Et la matière s'éclaircit en clair** : le
  fond crème passe entre les poils, les îles sombres deviennent un semis pâle ; en sombre elles se
  trouent de noir.
- **Ça remonte** — mais chaque remontée est un nouveau changement de toute la texture : un épisode de
  charge en fait QUATRE.
- **Quand** : jugé sur les 45 dernières images, suspendu seulement tant qu'un creux existe. Rien ne
  l'empêchait en plein élan (l'élan dure jusqu'à 5,2 s, le creux se referme en 0,4 s). Possible par le
  code ; **pas observé** dans ma mesure (l'élan s'y était éteint avant le premier palier).

**Tranché, option la plus sobre (Q181, à confirmer) : le régulateur mesure et VISE pendant qu'on
regarde ; la vise ne s'applique qu'à l'OUVERTURE suivante**, pendant que l'écran se bâtit (`prepare`).
Aucun changement de matière, aucune image figée sous les yeux — jamais. Coût, dit franchement : une
session sur un appareil lent reste entière au palier où elle a commencé ; il pèse peu (×4 : 17 images/s
à 110 000, 22 à 75 000 — le vrai levier est la résolution du tampon, Q178). **L'alternative**, si Tom
veut une densité qui s'adapte pendant la vue : des paliers EMBOÎTÉS et un éclaircissement en fondu sur
une ou deux secondes — une retouche du moteur, lot à part.
**Contrat réécrit** (`releve-aura.py`, famille 8 — original `sauvegardes/releve-aura-avant-regulateur.py`) :
sous ×6, le régulateur doit DÉCIDER de céder (vise plus basse gardée), le palier peint ne doit pas
bouger d'une image tant que l'Aura est ouverte, la vise doit prendre effet à la réouverture, et les
gestes doivent tenir. **Prouvé dans les deux sens :** sur la version d'avant (`17e2e1ca…`) il est
PRIS — « le palier a changé sous les yeux : 110 000 / 90 000 » et « aucune vise gardée » ; sur la
version corrigée il passe — palier peint 110 000 d'un bout à l'autre sous ×6, vise 75 000 (une
décision, au prorata du budget), 75 000 à la réouverture, gestes intacts, les huit acquis inchangés.

### 5 · LES VRAIES DONNÉES — et c'était là que tout pouvait mentir
Le jeu de l'app (celui du moodboard) donne **5 paroles tenues**, toutes des Promi → **sol bleu** ;
**2 personnes** (Marion, Rachel, par ordre alphabétique) ; 5 îles peintes pour 5 tenues. Vérifié en
FAISANT MENTIR les données, dans l'app, puis en restaurant :
```
toutes mes tenues passées en Chiche        nature « chiche », sol peint à ~345° (framboise)
toutes passées dans une Nuée               nature « nuee »,   sol peint à ~262° (mauve)
zéro parole tenue                          n = 0, nature « promi » (bleu, la base)
la plus récente plantée en braille/océan   son île porte ['braille','ocean'] et sa dalle tenue
                                           sort dans la palette OCÉAN, pas celle du Studio
le Studio passe en océan                   le monde des dalles déjà plantées ne bouge pas
USER.photo posée                           « toi » prend la vraie photo (data-photo)
tout gardé de côté                         l'état vide : sa phrase, pas de Noyaux, sphère pleine
```
⚠ **Ce que les données disent, et qui n'est pas un défaut :** les cinq Promi du jeu ont tous été figés
en `encre` par le rattrapage `_figeMondesManquants` (« rien n'est tiré de leur date ») : les îles sont
toutes du même monde, là où la planche les mélangeait à la main. La diversité viendra des plantations
futures. Et la COULEUR d'une dalle est tirée au hasard à chaque chargement (moteur, connu) : deux
captures successives n'ont pas les mêmes teintes d'îles.

### 6 · releve-aura.py — LE JUGE
Huit familles, deux thèmes : positions (> 3 px), styles, collisions, débordements (la rangée des
Noyaux exemptée SOUS CONDITION), **présence peinte** (la sphère lue dans ses pixels — disque plein,
transparent autour, teinte du sol ; les îles comptées dans la composition publiée ; arcs, visages et
dalles tenues lus), données, les huit acquis, densité. **La matière respire** : aucune égalité de
pixels n'est exigée ; les égalités se lisent dans `window._auraComp`, les pixels ne disent que « peint /
pas peint » et « a changé / est revenu », à vue figée (`_aura.fige`).
**Trois erreurs du juge lui-même, trouvées en route et dites :** il lisait une composition périmée
(avant de rouvrir) ; il photographiait avant que l'image recalculée soit peinte (il attend désormais
deux images RÉELLEMENT peintes, jamais un délai) ; il prenait une image de 100 ms pour une saccade.
**Le critère de saccade est réécrit au niveau de la règle** — la continuité : chaque vitesse suit
`v·exp(−Δt/0,55)` sur le temps réellement écoulé. Prouvé sur séquences : élan régulier et image de
100 ms passent ; remise à zéro en plein élan PRISE (2,23 rad/s d'écart), vitesse coupée de moitié PRISE.
**Et Playwright ne sait pas lancer** : face à un fil principal occupé, ses mouvements arrivent à
~130 ms les uns des autres et le relâcher 129 ms après le dernier — un doigt qui s'arrête. Les
lancers du juge se jouent donc DANS la page, cadencés à 16 ms.

### 7 · LES HUIT ACQUIS, DANS L'APP — la valeur mesurée de chacun
`releve-aura.py`, Chromium, deux thèmes, sphère en rotation. ⚠ **Une souris, pas un doigt** : le pointeur
est la souris de Playwright ; les lancers sont des événements pointeur joués dans la page, cadencés à
16 ms. **Le chemin qui lit la taille réelle du contact au capteur n'est jamais testé** — c'est la valeur
par défaut du pouce qui joue. À mesurer sur appareil, avec la densité (Q178).
Les deux colonnes sont relevées sur l'app INSÉRÉE finale (`17e2e1ca…`), recopiées telles quelles
depuis les journaux du juge (`table_valeurs.py`) — aucune valeur retapée à la main.
**Un chiffre par acquis, dans les deux thèmes** — extrait des journaux par `table_valeurs` (motifs sur les
lignes du juge, aucun chiffre retapé) :
```
                       SOMBRE                                               CLAIR
1 · rotation lente     0.0528 rad/s (décidé 0,0524)                         0.0528 rad/s (décidé 0,0524)
2 · prise, droite      Δlac +0.809 (att. +0.808)                            Δlac +0.809 (att. +0.808)
2 · prise, bas         Δtan -0.538 (att. -0.538)                            Δtan -0.538 (att. -0.538)
2 · prise, diagonale   Δlac -0.604 · Δtan +0.404                            Δlac -0.604 · Δtan +0.404
3 · élan               9.36 rad/s → éteint 5.2 s → 0.0528 rad/s · écart loi 0.0000 9.66 rad/s → éteint 5.2 s → 0.0518 rad/s · écart loi 0.0000
4 · retour             dernier pas 0.43 niv (médiane 0.88)                  dernier pas 0.56 niv (médiane 0.83)
4 · toucher            p 1.000 / 1.000 · 98.3 % sous le doigt               p 1.000 / 1.000 · 98.0 % sous le doigt
5 · trace              gardée · 9.8 % des pixels                            gardée · 10.7 % des pixels
6 · comblement         creux 3.58 s lâché · 0.39 s lancé                    creux 3.58 s lâché · 0.39 s lancé
7 · relisse            0 caresse · écart 0.000 %                            0 caresse · écart 0.000 %
8 · personne           toucher → « Marion » · glisser 1.14 rad, rien d'ouvert toucher → « Marion » · glisser 1.11 rad, rien d'ouvert
croissance             tour 5 · z = 0.942                                   tour 5 · z = 0.939
palier                 densité 110000 · 13.6 ms/image · ×6 : vise 75000, rouverte à 75000 densité 110000 · 13.4 ms/image · ×6 : vise 75000, rouverte à 75000
```

**Les deux relevés complets, tels que le juge les imprime :**
```
LES VALEURS MESURÉES — acquis joués en thème sombre
   1 · rotation lente   0.0528 rad/s sur 2 s (décidé 0.0524, un tour en 2 min)
   2 · prise, droite    Δlac +0.809 (attendu +0.808) · Δtan +0.000 (attendu +0.000)
   2 · prise, bas       Δlac +0.003 (attendu +0.000) · Δtan -0.538 (attendu -0.538)
   2 · prise, diagonale Δlac -0.604 (attendu -0.606) · Δtan +0.404 (attendu +0.404)
   3 · élan             au lâcher 9.36 rad/s · éteint à 5.2 s · puis 0.0528 rad/s · écart max à la loi 0.0000 rad/s · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s)
   4 · retour           écart au repos (niveaux) : 40.5 → 36.4 → 31.0 → 23.2 → 11.3 → 0.4 → lisse · DERNIER PAS 0.43 niveau (médiane des 10 d'avant 0.88) · 130 images · empreinte retirée à 3.27 s
   4 · toucher          p 1.000 à 250 ms, 1.000 à 950 ms · sous le doigt 98.3 % des pixels changent, hors de portée 1.78 %, bruit 0.00 % · revenu ≈ 3.3 s après le lâcher, écart au repos 0.00 %
   5 · trace            en attente au lâcher : 1 · 0 → 1 caresse(s), gardée(s) : 1 · au repos, 9.8 % des pixels portent la caresse
   7 · relisse          deux touchers à 120 ms : 0 caresse restante · écart à l'objet neuf 0.000 % des pixels
   6 · comblement       le creux vit 3.58 s lâché sur place, 0.39 s lancé (11 %)
   8 · personne         toucher sur « Marion » → ouvre « Marion », fiche affichée · glissement de 30 pt sur la rangée → n'ouvre rien · glissement de 80 pt sur la sphère → Δlac 1.14 rad, personne d'ouvert
   croissance           une parole de plus → tour 5 · la dernière dalle finit face à toi, z = 0.942

palier 110000 · médiane 13.6 ms · 1886 images · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s) · sous ×6 : palier peint 110000 pendant qu'on regarde, vise 75000, 1 décision(s) · à la réouverture : palier 75000
✅  L'AURA AU VERT
```
```
LES VALEURS MESURÉES — acquis joués en thème clair
   1 · rotation lente   0.0528 rad/s sur 2 s (décidé 0.0524, un tour en 2 min)
   2 · prise, droite    Δlac +0.809 (attendu +0.808) · Δtan +0.000 (attendu +0.000)
   2 · prise, bas       Δlac +0.003 (attendu +0.000) · Δtan -0.538 (attendu -0.538)
   2 · prise, diagonale Δlac -0.604 (attendu -0.606) · Δtan +0.404 (attendu +0.404)
   3 · élan             au lâcher 9.66 rad/s · éteint à 5.2 s · puis 0.0518 rad/s · écart max à la loi 0.0000 rad/s · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s)
   4 · retour           écart au repos (niveaux) : 40.4 → 36.7 → 30.1 → 21.3 → 9.9 → 0.6 → lisse · DERNIER PAS 0.56 niveau (médiane des 10 d'avant 0.83) · 132 images · empreinte retirée à 3.27 s
   4 · toucher          p 1.000 à 250 ms, 1.000 à 950 ms · sous le doigt 98.0 % des pixels changent, hors de portée 1.84 %, bruit 0.00 % · revenu ≈ 3.3 s après le lâcher, écart au repos 0.00 %
   5 · trace            en attente au lâcher : 1 · 0 → 1 caresse(s), gardée(s) : 1 · au repos, 10.7 % des pixels portent la caresse
   7 · relisse          deux touchers à 120 ms : 0 caresse restante · écart à l'objet neuf 0.000 % des pixels
   6 · comblement       le creux vit 3.58 s lâché sur place, 0.39 s lancé (11 %)
   8 · personne         toucher sur « Marion » → ouvre « Marion », fiche affichée · glissement de 30 pt sur la rangée → n'ouvre rien · glissement de 80 pt sur la sphère → Δlac 1.11 rad, personne d'ouvert
   croissance           une parole de plus → tour 5 · la dernière dalle finit face à toi, z = 0.939

palier 110000 · médiane 13.4 ms · 1898 images · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s) · sous ×6 : palier peint 110000 pendant qu'on regarde, vise 75000, 1 décision(s) · à la réouverture : palier 75000
✅  L'AURA AU VERT
```

### 8 · TROIS CONTRATS DE BATTERIE RÉÉCRITS — ET PROUVÉS
**J'ai réécrit des contrats de test** (CLAUDE.md §7) — l'Aura est réécrite, et ses nœuds anciens restent
dans le DOM, masqués : un contrôle qui les viserait passerait VERT sur une interface morte.
- `redteam_ecrans.py` — onze contrôles de l'ancienne Aura, chacun ramené à la décision qui l'a remplacé
  (l'Aura sans chiffre, la porte « Partager mon Noyau » rétablie, la dalle figée à sa plantation, la
  piste neutre du §2.9) ; deux fusionnés et dits (le % en signature et son décalage protégeaient la même
  chose). `DEBORDE` exempte une rangée `data-glisse` SOUS CONDITION (elle tient dans l'appareil et rogne).
  Original : `sauvegardes/redteam_ecrans-avant-aura-pelote.py`.
- `redteam_air.py` — l'Aura entre dans sa liste : c'est ce qui fait MORDRE le contrôle du bloc centré.
  Original : `sauvegardes/redteam_air-avant-aura-pelote.py`.
- **Prouvés contre un vrai défaut, DANS LES DEUX SENS, sur l'app insérée finale** (`e10da6dc…`, sans
  aucune injection — `sauvegardes/aura-pelote-lot/preuve_contrats.py`, relevé `preuve_finale.log`) :
  **les 18 passent tels quels, et les 18 PRENNENT le défaut posé exprès.** Une sonde était fausse au
  premier passage — `overflow-x:visible` à côté d'un `overflow-y:hidden` se recalcule en `auto` : la
  rangée rognait toujours ; la vraie sonde ouvre les deux axes.
- **`releve-aura.py` — un contrat NEUF, pas réécrit** : le retour de l'empreinte (§ 4 quater). Sa
  première écriture était morte ; la seconde prend l'ancienne version (8,45 niveaux) et passe la
  corrigée (0,46).

### ⚠ LA PREMIÈRE SÉRIE APRÈS INSERTION A ROUGI DEUX FOIS — ARRÊT, RESTAURATION, ET CE QUE C'ÉTAIT
Règle de Tom : *batterie verte qui rougit → arrêt immédiat et restauration*. `app.html` a été remis à
`61280542…` aussitôt ; la version insérée gardée à côté (`scratchpad/aura/app-insere-efbe.html`), et
tout le diagnostic fait sur une COPIE (`--copie`), jamais sur le fichier.
- **`redteam_ecrans` 149/150** — « la piste est neutre » en passe **[sombre]**. Ce n'était pas le CSS :
  cette batterie ne pose jamais le thème sombre (sa passe « sombre » n'ajoute simplement pas `.light`),
  et l'app démarre en CLAIR (relevé : `#device.light`, fond crème, `promi_theme = light`). **Mon contrat
  réécrit lisait l'étiquette de la passe au lieu du thème affiché** ; il lit `#device.light`, comme le
  faisait déjà sa preuve. Règle intacte : la piste est neutre pour le thème qu'on voit.
- **`releve-aura` — « une saccade »**. Deux choses mêlées : **mon échantillonneur** avait lu deux images
  de 130 ms comme une seule de 260 et appliqué UNE décroissance au lieu de deux — il lit désormais le
  pas de temps de LA BOUCLE, publié (`tick`, `dtReel`) ; et **de vraies images longues** existent
  pendant l'élan — voir « ce qui n'est pas fait ».
Sur la copie : `redteam_ecrans` 150/150, `releve-aura` au vert. Réinséré (md5 `4cfa48fe…`, identique
à la copie jugée), puis série complète.

### CONTRÔLES
**Série complète, EN SÉRIE (une batterie à la fois), sur l'app insérée finale `e10da6dc…`** — journal
`sauvegardes/aura-pelote-lot/bat_apres6.log`, 17 batteries, aucune sortie en erreur. (La même série était
déjà verte, 17/17, sur `17e2e1ca…` — `bat_apres5.log` — avant la correction du régulateur.)
```
redteam_ecrans      150/150        redteam_vide        61/61
redteam             15/15          redteam_air         ✅ 448 paires, 38 écrans, deux thèmes
redteam2            10/10          redteam_champ       32/32
redteam3            18/18          releve-design       ✅ aucun écart
redteam_demande     19/19          redteam_fonctions   22/22
redteam_toile       17/17          redteam_polices     0 couple absent
redteam_geste       13/13          redteam_superpo     0 recouvrement de texte
redteam_verbe       6/6            releve-aura         ✅ au vert — 8 familles ; sous ×6 le palier
                                                        peint reste 110 000, vise 75 000 à la réouverture
redteam_filets      0 filet parasite
```
Syntaxe : `node --check` sur tous les `<script>` d'`app.html` — OK. Preuve des contrats réécrits sur
cette même app : 18/18 dans les deux sens (§ 8).

### ⚠ CE QUI RESTE OUVERT — trois choses, et aucune n'est dans ce lot
**1 · La densité et le capteur, sur un vrai téléphone.** 110 000 poils est un plafond mesuré sur le Mac
Intel du banc ; sur un processeur ralenti ×4, même le plancher de 75 000 ne tient pas 60 images/s (la
part fixe du tampon domine — Q178). Et **la taille réelle du contact n'a jamais été testée** : le juge
pilote une souris, c'est la valeur par défaut du pouce qui joue. **Ce qu'il faut pour lever la réserve :**
- un iPhone (et si possible un Android de milieu de gamme) sur le même Wi-Fi que le Mac ;
- servir le dossier sur le réseau par un SECOND serveur, sur un autre port que 8752 (qui reste réservé
  aux outils, lié à 127.0.0.1) — c'est Tom qui l'ouvre ;
- ouvrir l'Aura dans Safari sur le téléphone ; sur le Mac, Safari → Développement → l'iPhone → console ;
- **densité** : `_aura.etat()` rend `palier` (le palier tenu), `ms` (médiane par image), `cede`, `vise`
  (le palier visé) — l'ouvrir, la laisser tourner ~10 s, la fermer, la ROUVRIR : la vise ne s'applique
  qu'à l'ouverture suivante (Q181), c'est le palier de la seconde ouverture qui dit ce que l'appareil tient ;
- **capteur** : appuyer du pouce puis de l'index, lire `_aura.etat().emp.a` pendant l'appui —
  **0,40 = la valeur par défaut** (le capteur n'a rien dit), **entre 0,26 et 0,40 = le capteur a
  parlé**. On ne sait pas si Safari iOS remplit `PointerEvent.width/height` pour un doigt : c'est
  précisément ce que la mesure dira ; s'il ne le fait pas, il faudra lire `Touch.radiusX` ou décider
  de s'en passer.
Si la densité ne tient pas sur l'appareil : le levier est la résolution du tampon (`D`), lot à part.

**2 · Le chantier 58 — entier hors de l'Aura.** Le lot n'a neutralisé l'ombre de dalle que sur l'Aura et
sous elle. Partout ailleurs, `frame()` écrit toujours sur les douze écrans à chaque image : **27 % du fil
principal**. C'est une règle d'un autre lot, pas touchée. Inscrit en tête de CHANTIERS.md.

**3 · Le Cercle — pas commencé.** Rien de ce qu'il ajoute à l'Aura n'est dessiné ni codé : les deux
moitiés du trait (*ta moitié · la leur*), la réciprocité, *nuée par nuée*, les graphes d'évolution, et le
chiffre s'il revient. L'entrée d'auteur `#karmaCercle` est sortie avec l'ancienne Aura (Q176). **Rien du
Cercle n'apparaît en gratuit.** Les mots existent en partie (Q165) ; la planche, non.

---

## ⚠ TROIS FOIS LA MÊME DEMANDE — ON MESURE, ON N'AJUSTE PAS · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · sauvegarde du juge :
> `sauvegardes/redteam_air-avant-centre.py`

### CE QUE JE FAISAIS DE TRAVERS
Tom a demandé **trois fois** que la légende de l'Aura soit centrée entre les prénoms et
« CE QUE TU AS TENU ». Les trois fois je l'ai **rapprochée à l'œil** au lieu de relever les
trois boîtes une seule fois. Relevé du défaut, enfin fait :
```
bas des prenoms          490          ecart au-dessus de la legende      8 px
haut de la legende       498
bas de la legende        512
haut de « CE QUE... »    552          ecart en dessous de la legende    40 px
```
**8 contre 40.** La cote se calcule : `(552 − 490 − 14) / 2 = 24` de chaque côté, donc
`top = 514`.

### VÉRIFIÉ SUR L'IMAGE RENDUE, PAS SEULEMENT DANS LE DOM
```
DOM, deux themes                au-dessus 24,00   en dessous 24,00   difference 0,00
image rendue a 2x, sombre       prenoms (954,972)  legende (1032,1050)  titre (1110,1129)
                                au-dessus 59 px    en dessous 59 px     DIFFERENCE 0
image rendue a 2x, clair        idem, DIFFERENCE 0
```

### ⚑ LE CONTRÔLE, POUR QUE ÇA NE REVIENNE PAS
**« Un bloc annoncé centré entre deux voisins a des écarts égaux. »** Posé dans
`redteam_air.py`, tolérance **1 px** (la moitié d'un pixel d'appareil).
**Le bloc se DÉCLARE** — `data-centre-entre="selHaut|selBas"`. Un contrôle qui devinerait
les voisins se tromperait de nœud : c'est l'écran qui sait ce qu'il centre entre quoi. Et
il est **silencieux** tant qu'aucun nœud ne se déclare : il ne coûte rien aux autres écrans.

**⚠ ET IL EST PROUVÉ CONTRE UN VRAI DÉFAUT** — `scratchpad/preuve_centre.py`. Un contrôle
neuf qui ne trouve rien peut être juste **ou éteint**, et les deux se ressemblent dans un
rapport vert :
```
tel quel                             2 blocs declares   PRIS : 0   (24,00 / 24,00)
avec un defaut de 9 px pose expres   2 blocs declares   PRIS : 2   (33,00 / 15,00)
```
*L'écran Aura n'étant pas encore dans `app.html`, le contrôle y trouve zéro nœud déclaré et
se tait — il mordra à la seconde où le portage y posera l'attribut.*

```
redteam_air   OK — l'air est intact, et zero bloc centre en defaut
md5 app.html  61280542751d0d0df5bce546f9a091b1  inchange
```

---

## ⚠ LE BUDGET, CORRIGÉ — IL N'Y A PAS D'ÉTAT IMMOBILE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`)

### ⚠ CE QUE J'AVAIS CONCLU, ET QUI ÉTAIT FAUX
Mon premier relevé donnait **deux régimes** : 360 000 poils au repos (image gardée,
0,00 ms) et 110 000 en mouvement. **Ça supposait un état IMMOBILE — et il n'existe pas.**
La rotation lente est acquise depuis le début du chantier : **la Pelote tourne toujours**.
Un chiffre mesuré sur un état qui n'existe pas ne vaut rien. **Conclusion retirée.**

### LE VRAI CHIFFRE — ROTATION LENTE PERMANENTE
`scratchpad/banc_lent.py`, au rythme du produit (un tour en ~50 s, **0,0021 rad par
image**), 80 images par palier, dans le vrai `#auraScreen` avec tout l'écran autour :
```
160 000 x1,00   mediane 21,30 ms   9e dec 29,30   80 images sur 80 au-dessus de 20 ms
130 000 x1,00   mediane 18,30 ms   9e dec 18,70    4 sur 80
110 000 x1,00   mediane 16,20 ms   9e dec 16,80    2 sur 80   <- LE PLAFOND
110 000 x1,70   mediane 21,30 ms   9e dec 22,00   80 sur 80
 90 000 x1,70   mediane 18,30 ms   9e dec 18,60    0 sur 80
 75 000 x1,90   mediane 17,30 ms   9e dec 17,60    0 sur 80, mais 0,23 % d'encre
```
**110 000, tout le temps.** Pas de double régime, pas de bitmap gardé.

### ⚑ ET GROSSIR LE BRIN NE RACHÈTE PAS LA DENSITÉ
La couverture vaut `N × surface du brin` : en théorie, moins de poils plus gros devraient
rendre la même matière. **Mesuré : le coût suit exactement la même loi.** À `110 000 × 1,70`
on retrouve la matière de 160 000 — et on en paie le prix au centième près (**21,30 ms les
deux fois**). Il n'y a pas de repas gratuit de ce côté-là.

### LA SPHÈRE À 110 000, REGARDÉE
`0,05 %` du disque encore à l'encre — négligeable. Au zoom 2 elle est **un peu plus grenue**
qu'à 160 000, les brins se lisent un peu plus individuellement ; **à la taille réelle
(342 px) la différence n'est pas perceptible**. La planche est passée à cette densité :
elle montre désormais ce que l'app peut réellement payer.

### ⚠ ET LA MISE EN GARDE TIENT
Mesure sur un **Mac**, dans la vraie page et la vraie géométrie, **pas sur un téléphone**.
**110 000 est un plafond haut, pas une garantie** — à reconfirmer sur appareil dès que
possible, et c'est le premier contrôle du portage.

### ⚑ CE QUE LA SPHÈRE SAIT DÉJÀ FAIRE — ET QUI DOIT SE RETROUVER DANS L'APP
Tout ceci est **acquis et validé**. Le portage n'a pas le droit d'en perdre une ligne :
```
· la rotation lente au repos — elle ne s'arrete jamais
· on la prend au doigt et on la tourne dans tous les sens
· l'elan qui continue, puis se rend a la rotation lente SANS SACCADE
· le toucher qui creuse, resiste, et revient
· la trace qui reste
· le comblement du creux quand on lance
· le geste qui relisse tout
· un toucher ouvre la personne, un glissement tourne
```

### LA SEPTIÈME SILHOUETTE — **AFFORDANCE, PAS DÉBORDEMENT**
Validé par Tom. `24 + 78 + 30 + 6×58 + 5×26 + 24 = 634 px` pour un écran de 390 : trois
personnes tiennent, la quatrième est coupée. Le §2.9 fixe six personnes et des écarts
constants ; **il n'a jamais prévu qu'elles tiennent toutes à l'écran**. Le disque coupé
**dit qu'il y en a d'autres** — la rangée se déclare glissante (`data-glisse`, Q128 §3).

### CE QUI SUIT
```
2 · le portage : les cinq fichiers dans app.html, sans toucher au moteur de la Toile.
    #auraScreen reecrit en entier, deux themes, BLOC NEUF EN FIN DE FICHIER.
3 · les vraies donnees : natures, etats, personnes, mondes de plantation.
4 · releve-aura.py, avec le controle de PRESENCE PEINTE comme les autres juges.
5 · batteries en serie, captures a 2x une par une, ETAT-DES-LIEUX a jour.
```

---

## ⚑ LE BUDGET D'IMAGE, MESURÉ DANS L'APP — AVANT DE PORTER QUOI QUE CE SOIT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) — la mesure **n'a pas touché
> le fichier** : `scratchpad/banc_aura.py` injecte le peintre à l'exécution
> (`addScriptTag`), ouvre le vrai `#auraScreen`, et fait tourner la sphère dans un
> `#device` de 390 × 844 **avec tout l'écran autour**. C'est ce « autour » qui manquait à
> la planche.

### LE RELEVÉ — 70 images par palier, la sphère en rotation
```
360 000 poils   mediane 42,20 ms   9e decile 43,40   70 images sur 70 au-dessus de 20 ms
240 000         mediane 30,00 ms   9e decile 30,80   70 sur 70
160 000         mediane 21,70 ms   9e decile 22,40   70 sur 70
110 000         mediane 16,60 ms   9e decile 17,10   ZERO sur 70      <- le plafond
 75 000         mediane 12,90 ms   9e decile 13,40   zero sur 70
```
**La planche tournait à 3,3 fois ce qu'un téléphone peut payer.** C'était bien la question
à poser avant de porter cinq fichiers.

### ET LA SPHÈRE ALLÉGÉE — REGARDÉE, PAS SUPPOSÉE
`scratchpad/banc_vue.py` rend la même sphère aux quatre densités
(`scratchpad/pav/vel/_densites.png`) :
```
360 000   le velours est une MATIERE continue
160 000   encore juste, un peu plus grenu
110 000   on commence a lire les BRINS au lieu de la matiere
 75 000   ca casse : l'encre du fond repasse entre les poils, la boule se troue
```
**Donc : au plafond des 60 images, la sphère est visiblement dégradée. À 75 000, elle est
perdue.** Si on s'en tenait à un seul chiffre, il faudrait choisir entre la fluidité et
l'objet.

### ⚑ MAIS LA VRAIE QUESTION N'ÉTAIT PAS « COMBIEN DE POILS » — C'ÉTAIT « QUAND »
**Au repos, la Pelote ne bouge pas.** La repeindre soixante fois par seconde ne sert à rien.
Mesuré, dans les mêmes conditions :
```
une passe pleine densite (360 000)   41,2 ms   UNE FOIS
l'image gardee, reblittee             0,00 ms  par image (sous la resolution du timer)
```
**Le régime est donc double, et il n'y a rien à sacrifier :**
```
AU REPOS            360 000 poils, peint UNE FOIS, garde en bitmap    0 ms / image
EN MOUVEMENT        110 000 poils                                    16,6 ms / image
A LA FIN DU GESTE   une passe pleine densite                         41,2 ms, une fois
                    (une seule image sautee, a l'instant ou le doigt se leve)
```
L'objet qu'on regarde, qu'on partage et qu'on vend est **celui du repos** : il garde sa
pleine matière. Ce qui s'allège, c'est la demi-seconde où la boule tourne — et pendant
qu'elle tourne, personne ne compte les brins.

### ⚠ CE QUE CETTE MESURE NE DIT PAS
Elle tourne sur un **Mac, en Chromium headless**, dans la vraie page et la vraie géométrie
— mais **pas sur un téléphone**. Un appareil réel remplit moins vite : **110 000 est un
plafond haut, pas une garantie.** Le chiffre se reconfirme sur un appareil au moment du
portage, et c'est le premier contrôle du lot suivant.

### ⚑ LA SEPTIÈME SILHOUETTE : LA RANGÉE DÉFILE, IL N'Y EN A PAS UN DE TROP
La cote se calcule, elle ne se devine pas — §2.9, en unités du document :
```
24 + 78 + 30 + 6 x 58 + 5 x 26 + 24 = 634 px   pour un ecran de 390
trois personnes tiennent, la quatrieme est coupee au bord
```
Le §2.9 fixe **six** personnes et des écarts constants ; **il n'a jamais prévu qu'elles
tiennent toutes à l'écran**. Le disque coupé n'est pas un débordement, c'est **l'affordance
du défilement** — c'est lui qui dit qu'il y en a d'autres. La rangée se déclare glissante
(`data-glisse`, Q128 §3) pour que les juges de débordement l'exemptent **sous condition**.

### TRANCHÉ AU PASSAGE
**Le sol à zéro Promi reste bleu** — le bleu est la nature de base, et à zéro rien ne
domine. Choix confirmé par Tom.

### CE QUI SUIT, DANS CET ORDRE
```
2 · le portage : les cinq fichiers dans app.html, #auraScreen reecrit en entier,
    deux themes, BLOC NEUF EN FIN DE FICHIER, jamais une regle existante,
    et rien du code de la Toile (§9)
3 · les vraies donnees : natures, etats, personnes, mondes de plantation.
    C'est la que tout peut mentir — la planche a un jeu de demonstration.
4 · releve-aura.py, avec le controle de presence peinte comme les autres juges
5 · batteries en serie, captures a 2x une par une, ETAT-DES-LIEUX a jour
```

---

## ⚑ L'PELOTE — CLÔTURE DU CHANTIER · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · point de reprise :
> `sauvegardes/pelote-velours/` (les cinq `_v_*.js`, `_m_base.js`, `PLANCHE-VELOURS.html`)
> · `sauvegardes/PROMI-SPECIFICATIONS-avant-piste-neutre.md`

### 1 · ⚠ J'AVAIS RETIRÉ SANS REMPLACER
En enlevant la couleur de nature des visages — elle était **arbitraire**, je l'avais écrite
à la main sans règle derrière — il ne restait que **six silhouettes grises identiques**. En
thème sombre elles disparaissaient, et on ne distinguait plus personne : c'est pourtant à
ça que sert cette rangée. **Retirer un défaut n'est pas une correction tant que rien ne
prend sa place.**

**La réponse existait déjà dans l'app** : `avatarHTML` / `_blobBg`. Une **vraie photo** si
la personne en a une, sinon **l'image abstraite générée**, déterministe à partir du nom,
avec sa palette `_BPAL` (six teintes) et sa **texture de bruit en soft-light**. Reprise à
l'identique, hachage FNV compris : deux personnes n'ont jamais la même image, et la même
personne a toujours la sienne. **C'est ça qui identifie quelqu'un — pas une couleur de
nature.**

### 2 · ⚑ LE §2.9 EST CORRIGÉ, PAS CONTOURNÉ
Le document disait *« piste de l'anneau : teinte de la nature »*. **Une personne n'a pas de
nature** : la règle était inapplicable à la moitié des Noyaux qu'elle décrit, et c'est ce
vide qui avait produit une couleur arbitraire. **La piste est neutre** — `#2A2C34` en
sombre, `#DED7C6` en clair — **et seuls les arcs portent la couleur**, celle de l'ÉTAT.
Ton Noyau à toi suit la même règle : c'est le même composant.
*L'écart n'est pas laissé en suspens : `PROMI-SPECIFICATIONS.md §2.9` est réécrit, avec la
raison et la version d'origine en sauvegarde.*

### 3 · ⚠ LE SOL N'ÉTAIT PAS CALCULÉ DU TOUT
Il sortait **mauve** sur les deux captures. **Pas parce que la Nuée dominait — parce
qu'aucun calcul n'était branché** : le sol prenait simplement la couleur de la palette du
Studio. La rangée des trois natures démontrait la règle ; l'écran ne l'appliquait pas.
**Vérifié dans le moteur** : `Toile.sync()` ne plante que des **Promi** ; une Nuée ne naît
que de `addNuee()`, que la planche n'appelle jamais. **La nature la plus présente est donc
Promi, et le sol doit être BLEU.** Il l'est.
*À zéro Promi aucune nature ne domine : le sol prend le bleu, la nature de base. Choix
noté, pas mesuré.*

### 4 · DEUX RÉGLAGES D'AIR
La légende **remonte de 14 px** vers les anneaux dont elle nomme les arcs ; le titre
« CE QUE TU AS TENU » **gagne 7 px** au-dessus de ses dalles.

### CONTRÔLES — LOT COMPLET
```
node --check sur le JS de app.html            OK
redteam_ecrans   150/150      redteam         15/15
redteam2          10/10       redteam3        18/18
redteam_demande   19/19       redteam_toile   17/17
redteam_geste     13/13       redteam_verbe    6/6
releve-design                 AUCUN ECART, le design est intact
trente-cinq cadres compares   deux couples identiques, et les deux sont des TEMOINS
                              voulus (c-cinq/pg-cinq, pg-trente/q-repos)
circularite  g-vide           rayon 275,9  ecart-type 1,24  soit 0,45 %
             v-30             rayon 565,3  ecart-type 3,17  soit 0,56 %
md5 app.html                  61280542751d0d0df5bce546f9a091b1  INCHANGE
```

### ⚑ CE QUE L'PELOTE EST DEVENUE — RÉCAPITULATIF DU CHANTIER
```
LA SPHERE         le velours, ses dalles dans le monde de leur plantation,
                  et la memoire de la main. RIEN D'AUTRE.
                  Elle n'encode ni les gens ni les etats : une matiere ne sait
                  pas dire un nom, et vingt series ont echoue a le lui demander.
                  Aucun nom dessus => l'image se partage.
LE SOL            la NATURE la plus presente (bleu / framboise / mauve).
                  Menthe et terracotta ne servent qu'aux etats, nulle part ailleurs.
LA CROISSANCE     la dalle plantee se pose du cote qu'on regarde, puis la Pelote
                  fait UN TOUR pour l'amener au centre. Les anciennes ne bougent
                  pas d'un pouce.
LA MAIN           des caresses au diametre du doigt (0,27 rad), qui couchent le
                  poil dans leur sens : 19,66 % des pixels. Visible sans toucher.
LES SIX           SOUS la sphere, en Noyaux du §2.9 : avatar du produit, piste
                  neutre, trois arcs d'etat, prenom sur la meme ligne de base.
LE MOT            il qualifie L'OBJET dans le registre du rejeu, jamais la
                  personne. Ni note, ni verdict, ni valeur qui descend.
L'ANNEAU          un seul, celui de ton Noyau. Celui de la sphere faisait doublon.
```

### ⚠ CE QUI N'EST PAS FAIT — ET C'EST LE PLUS IMPORTANT DE CE CHAPITRE
**LE PORTAGE DANS `app.html` N'EST PAS FAIT.** Le md5 est inchangé, et ce n'est pas un
oubli : c'est un lot à part entière, pas la fin de celui-ci. Ce qu'il demande —
```
1 · faire entrer cinq fichiers (_v_moteur, _v_iles, _v_semis, _v_peint, _m_base)
    dans app.html, sans toucher au code de la Toile (§9)
2 · reecrire #auraScreen : la sphere, la rangee des Noyaux, la legende, le mot,
    la rangee des dalles tenues, le bouton — deux themes
3 · brancher les VRAIES donnees : natures, etats, personnes, mondes de plantation
4 · le budget d'image sur un vrai telephone (la planche tourne a 180 000 poils
    pour 340 px, ce n'est PAS une densite d'app)
5 · un juge dedie, `releve-aura.py`, avant de figer quoi que ce soit
```
- **Le Cercle** : graphes d'évolution, commentaires sur la hausse, réciprocité, et le
  chiffre s'il revient. **Rien n'en apparaît en gratuit** — c'est de la mesure fine.
- **Le filtre « pas de Nuée dans la rangée »** est une règle d'app : une Nuée est un
  contenant, ce sont les Promi qu'elle porte qui sont tenus.

---

## ⚑ DEUX SYSTÈMES DE COULEUR, ET ILS SE TÉLESCOPAIENT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

### 1 · LE SOL DISAIT « À QUI » AVEC DES COULEURS D'ÉTAT
Menthe, terracotta et mauve pour dire *soi / quelqu'un / un groupe* : sur **le même écran**,
le menthe disait « tenu » dans un anneau et « à toi » sur la sphère. **Une couleur signal
qui dit deux choses** — ce que le §3 interdit.
**Le sol prend les couleurs de NATURE** : bleu `#3A54FF` surtout des Promi, framboise
`#FA2258` surtout des Chiche, mauve `#8A5CF0` surtout en Nuée. **Il dit ce qu'on promet,
pas à qui.** Menthe et terracotta ne servent plus qu'aux états, nulle part ailleurs.

### 2 · ⚠ LA COULEUR DES VISAGES ÉTAIT ARBITRAIRE — RÉPONSE FRANCHE
Je l'avais écrite **à la main** dans le tableau `GENS`, sans règle derrière : ce n'était la
Nuée de personne. **Une personne n'est ni un Promi ni un Chiche : elle n'a pas de nature,
donc pas de couleur de nature.** Le visage passe au **neutre** (l'encre ou la crème du
thème) ; il ne reste de coloré que ce qui porte du sens, les arcs d'état.
**⚠ Et le même défaut touche LA PISTE de l'anneau** : le §2.9 la veut « teinte de la
nature », ce qui n'existe pas pour une personne. Elle passe au neutre aussi — **point à
trancher**.

### 3 · L'ANNEAU DE LA SPHÈRE SORT, LA LÉGENDE DESCEND
Il faisait **doublon** avec le Noyau « toi » juste en dessous : deux anneaux à trois arcs
disant la même chose. Le mien porte mon visage et vit dans la rangée des six ; celui de la
sphère cerclait un objet qui n'est pas moi.
**La légende descend sous la rangée des six** — c'est là qu'elle nomme quelque chose de
précis : **les arcs des Noyaux**, qui sont juste au-dessus d'elle. Elle a son air au-dessus
(22 px) et en dessous (44 px).
**Et les Noyaux portent maintenant TROIS arcs**, pas un seul : une légende à trois entrées
ne pouvait pas nommer un unique arc menthe.

### 4 · ⚠ LE LEXIQUE DU TITRE ÉTAIT FAUX, ET JE NE L'AVAIS PAS VU
« Tes paroles tenues » **ne couvre ni les Chiche ni les Nuées**, alors qu'ils sont là.
**« Ce que tu as tenu »** englobe les trois natures sans en nommer aucune.

**Ce que contient vraiment la rangée, vérifié dans le moteur :** `Toile.sync()` ne plante
que des **Promi** — une Nuée ne naît que de `addNuee()`, que la planche n'appelle jamais.
Les six ids de la rangée (3, 7, 11, 14, 17, 19) résolvent tous en dalles réelles via
`dalleAbs` (qui exclut déjà les cellules vides). **Il n'y a donc aucune dalle de Nuée dans
la rangée de la planche** — mais **la règle reste à écrire côté app** : une Nuée est un
contenant, ce sont les Promi qu'elle porte qui sont tenus.

### 5 · ⚑ LE MONDE DE LA PLANTATION, ENFIN CÂBLÉ
Un Promi porte `{m,p,h}`, figé par sa fabrique au moment où il est planté (lot du
4 septembre). **`dalleTrame` prend ce 4ᵉ argument depuis ce jour-là — il n'avait jamais été
câblé**, et les six dalles sortaient toutes dans le monde courant. C'est une règle du
produit, pas un détail : la diversité des dalles est ce qui rend la Toile vivante. Les
trois dalles visibles sont maintenant en **touffe, sillons, braille**.

### 6 · ⚑ L'PELOTE TOURNE UNE FOIS QUAND UNE PAROLE EST TENUE
Le levier était le **geste**, pas le rendu. La vue qui centre une direction se **calcule** :
```
lac = atan2(-c0, c2)        tan = atan2(c1, hypot(c0, c2))
```
Vérifié en repassant la direction par la transformation directe : **elle rend (0, 0, 1)
exactement**, et les six îles ont toutes `z > 0` — donc **toutes sur la face visible, rien
n'a reculé**.
```
5 -> 6 (la dalle se pose du bon cote)      4,75 % des pixels
6 -> apres le tour                        52,21 %
```

### 7 · LES PHRASES — LE REGISTRE EST CELUI DU REJEU
Mes cinq phrases décrivaient l'objet : **c'était un inventaire, pas une voix**. Le registre
est le clin d'œil complice — *« Tu l'avais dit »*, *« Tiens donc »*. Les cinq de Tom sont en
place, et l'état vide n'en garde que deux :
```
La premiere parole laissera sa trace ici.
   Tout commence par une parole donnee.
```

### CONTRÔLES
```
trente-cinq cadres compares deux a deux   deux couples identiques, et les deux sont VOULUS
                                          (c-cinq/pg-cinq et pg-trente/q-repos : memes
                                          etats, ce sont les temoins de deux rangees)
la derniere dalle, apres le tour          (0, 0, 1) a 1e-6 pres
les six iles apres le tour                z = 0,92 · 0,71 · 0,71 · 0,88 · 0,90 · 1,00
md5 app.html                              61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI RESTE
- **La piste des Noyaux** : neutre par défaut de règle, à trancher.
- **Le Cercle n'est pas dessiné** — graphes, commentaires sur la hausse, réciprocité,
  et le chiffre s'il revient. **Rien n'en apparaît en gratuit.**
- **Le filtre « pas de Nuée dans la rangée »** est une règle d'app, pas de planche.

---

## ⚑ L'AURA SANS CHIFFRE — LE MOT QUALIFIE L'OBJET · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

### 1 · CE QUI SORT, ET POURQUOI
**Le chiffre d'harmonie et le mot qui qualifie la personne.** Les deux font *score*, même
sans le mot : l'un est une note, l'autre un verdict sur quelqu'un. Et **le chiffre baisse
quand on ne tient pas** — une valeur qui décroît par inaction.

### 2 · CE QUI RESTE, ET IL A CHANGÉ DE SUJET
**Un mot revient : il qualifie L'OBJET, jamais la personne.** Pas *« ta parole est
solide »* — mais ce que la sphère est devenue. Cinq phrases proposées, aucune ne compare,
ne mesure ni ne juge :
```
Le velours s'est epaissi.
Plusieurs mondes se cotoient ici.
La main a laisse son passage.
Les premieres dalles sont toujours la.
Les dalles se touchent, maintenant.
```

### 3 · L'ANNEAU ET SA LÉGENDE
**L'anneau est la seule mesure de l'écran, et elle ne se lit pas en chiffres** : trois arcs
autour de la sphère, avec 2,4 % de vide entre eux. La légende — *tenues · en cours · à
tenir* — **nomme** les trois arcs, elle ne quantifie rien. Air au-dessus (34 px), air en
dessous (34 px).
**⚠ Et l'anneau ne doit pas toucher la sphère.** À `R = 0,438` le velours arrivait au ras
des arcs : ça se lisait comme un **cerclage de l'objet**, et le moindre poil qui déborde
salissait l'arc. `R = 0,392` — l'air entre les deux fait que l'anneau se lit comme une
mesure **posée autour**.

### 4 · « LA MOISSON » SORT
Mot d'agriculture, pas du produit : on plante et on tient parole, on ne récolte pas.
Trois propositions, la première est en place : **« Tes paroles tenues »** · *« Ce que tu as
tenu »* · *« Les dalles tenues »*. Le titre dit **ce que c'est**, jamais combien.

### 5 · « PARTAGER MON NOYAU »
La porte manquait sur l'Aura alors que l'aide l'annonce en gratuit et que le mode existe
côté partage. Bouton en bas, à la **grammaire des contours** : 298 × 52, trait 2, rayon 26
(le 342 × 62 du document, ramené au gabarit).

### 6 · L'ÉTAT VIDE EXISTE
```
Le velours est neuf.
La premiere parole y laissera sa dalle.
   Tout part d'une parole donnee — a toi, a quelqu'un, a plusieurs.
```
Deux autres proposées : *« Ici, tout part d'une parole donnée. »* · *« Rien n'est encore
planté. La matière est prête. »* Aucune injonction, aucun point d'exclamation.
**Et la sphère y est déjà belle** : c'est le test décisif, un objet qui n'est beau qu'à
trente est refusé. À zéro, **pas d'anneau** — il n'y a rien à mesurer.

### 7 · LES DEUX CORRECTIONS DE LA CAPTURE
- **Les prénoms sont sur la même ligne de base.** Chaque Noyau est une colonne de hauteur
  fixe (94 px) alignée par le bas, et le libellé a une hauteur de ligne fixe : « toi » ne
  peut plus décrocher de Rachel.
- **Les diamètres sont vérifiés au §2.9** : 78 et 58 dans le document, soit **68 et 51** au
  gabarit (× 0,872). Rapport 1,333 contre 1,345 — l'écart est l'arrondi au pixel, pas un
  accident.

### ⚑ 8 · LA MAIN SE VOIT ENFIN AU REPOS
```
sans traces -> avec traces :  19,66 % des pixels bougent de plus de 3/255
```
**⚠ Une caresse est LARGE, et les arcs ne l'étaient pas.** `m_gestes` donne des arcs de
0,055 à 0,13 rad — **trois à sept degrés, c'est un ongle, pas une pulpe**. La pulpe d'un
pouce couvre 0,27 rad (mesure du lot de l'empreinte). À cette largeur-là une caresse ne
pouvait pas se voir, et c'était pourtant la seule chose que personne d'autre n'a. Les arcs
passent au diamètre du doigt (`0,115 + w × 1,35`) et ce qu'ils ont poli monte.

### CONTRÔLES
```
trente-sept cadres compares deux a deux   zero doublon
5 -> 6 Promi                              4,75 % des pixels
sans traces -> avec traces                19,66 %
circularite v-30                          rayon 565,3  ecart-type 3,17  soit 0,56 %
md5 app.html                              61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI RESTE
- **Le Cercle n'est pas dessiné** : graphes d'évolution, commentaires sur la hausse,
  réciprocité « envers les autres », et le chiffre si on le garde un jour. **Rien de tout
  ça n'apparaît en gratuit** — c'est de la mesure fine, pas de l'information.
- **Les dalles de « Tes paroles tenues » sont toutes dans le monde courant.** Un Promi doit
  garder le monde de SA plantation (4ᵉ argument de `dalleTrame`, écrit, jamais câblé).
- **5 → 6 vaut 4,75 %** : la nouvelle dalle se voit, mais c'est un ajout discret, pas un
  événement. Si Tom veut que ça se voie franchement, le levier est le geste de plantation,
  pas le rendu.

---

## ⚑ UNE MATIÈRE NE SAIT PAS DIRE UN NOM · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

### LA DÉCISION, ET C'EST ELLE QUI COMPTE
On a demandé à la matière d'encoder **qui est qui** : par la position, par la saturation,
par la densité, puis par un **épi** — un tourbillon de poil par personne. Verdict de Tom :
*« ça fait des signes BMW, ni beau ni compréhensible »*. Et la vraie raison n'est pas
l'exécution :

> **UNE MATIÈRE NE SAIT PAS DIRE UN NOM.** Un épi ne peut pas être « Rachel ». Une
> saturation non plus, une densité non plus. **C'est structurel** — et c'est pour ça que
> vingt séries ont échoué au même endroit.

**On arrête de le lui demander.** La sphère ne porte plus que trois choses : **le velours,
ses dalles dans le monde de leur plantation, et la mémoire de la main.** Elle dit *« voilà
ce que j'ai tenu, et j'y ai passé du temps »*.
**Les six et le Noyau vivent sous elle**, en anneaux du §2.9 — piste à la teinte de la
nature, arc menthe, visage, prénom. C'est là qu'on lit la relation, sans deviner.
**Et l'image devient partageable** : aucun nom dessus, indéchiffrable pour un inconnu.

### CE QUE ÇA CHANGE DANS LE CODE
- `champPoil` n'a plus que deux termes : **le peigne** (une direction unique, ses deux zéros
  au limbe) et **les caresses**. Plus d'épis, plus de couronne. Comme tout le reste est
  uniforme, **la main est la seule structure de la surface** — donc la plus visible, ce qui
  est exactement le but.
- Le lustre de la main double le contraste du brin (on **suit** le sens du geste) et monte
  le ton (`_po × 2,6`) et la chroma.
- `disques` et `noyau` restent dans le fichier, **non appelés**.

### ⚑ UN PROMI DE PLUS SE VOIT — ET CE N'ÉTAIT PAS UN PROBLÈME DE RENDU
```
avant ce lot        5 -> 6 Promi :  0,09 % des pixels bougent de plus de 3/255
apres               5 -> 6 Promi :  4,80 %
```
**Aucune variable globale continue ne peut rendre un +1 visible** — un trente-quatrième de
quoi que ce soit est invisible, c'est de l'arithmétique. Ce qui rend un +1 visible, c'est
**la dalle elle-même**, et il y avait une chance sur deux qu'elle tombe **sur la face
cachée** : la grappe pousse par accrétion vers l'extérieur.

**⚠ Et on ne fait pas tourner la boule pour autant.** Essayé, mesuré, regardé : en tournant
l'objet pour présenter la dernière dalle, les cinq précédentes partaient sur le dos — **à
six Promi on en voyait MOINS qu'à cinq** (17,22 % de pixels changés, et une régression de
sens). *« Rien ne recule jamais »* interdit ça.
**La loi de croissance ne bouge pas** (l'accrétion fait la forme) : parmi les positions
valides, on garde **celle qui regarde le plus vers nous**. Les anciennes ne bougent pas d'un
pouce, la nouvelle est devant.

### L'ÉCRAN AURA, EN ENTIER, DEUX THÈMES
`ecranAura()` dans la planche : le titre, la sphère (312 px), **la rangée des Noyaux**
(§2.9 — tien 78→68, personnes 58→51, visages du §2.10, arc menthe, prénom dessous, la
rangée déborde à droite : elle défile), puis **la moisson** en **vraies dalles du moteur**.

**⚠ Deux pièges payés sur la moisson :**
- **`dalleTrame` lit LE PARENT du canvas** : appelée avant que la grille soit disposée, elle
  rend du vide **en silence**. On repasse à 0, 120 et 420 ms (§4, règle 5).
- **Un id hors de la Toile synchronisée rend un canevas vide, en silence.** La planche fait
  `Toile.sync([1..20])` : les ids 37, 58, 73, 91, 104 ne rendaient rien — **cinq dalles sur
  six manquaient**, et rien ne le signalait.

### CONTRÔLES
```
trente-trois cadres compares      deux couples identiques, et les deux sont VOULUS :
                                  c-cinq / pg-cinq  (le meme etat a cinq Promi)
                                  pg-trente / q-repos (le temoin de la rangee du doigt)
circularite  g-vide               rayon 275,9  ecart-type 1,24  soit 0,45 %
             n-marque             rayon 276,8  ecart-type 1,42  soit 0,51 %
md5 app.html                      61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI N'EST PAS FAIT, ET QUI SE VOIT SUR LA PLANCHE
- **Les dalles de la moisson sont toutes dans le monde courant.** Un Promi doit garder le
  monde de SA plantation (4ᵉ argument de `dalleTrame`, déjà écrit, jamais câblé).
- **La rangée des Noyaux déborde** — c'est le §2.9 (elle défile), mais le geste n'est pas
  démontré.
- **Le prénom au toucher sur la sphère n'a plus lieu d'être** : il n'y a plus rien à
  effleurer. `o.effleure` devient mort.
- **La moisson n'est qu'une grille de six** ; ce qu'elle devient à trente n'est pas dessiné.

---

## ⚑ LES ÉPIS — LE NOYAU ET LES SIX SONT DEVENUS DE LA MATIÈRE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

**Trois choses écrivent maintenant le sens du poil, et aucune n'ajoute quoi que ce soit à la
matière : elles SONT la matière.** Tout passe par une seule fonction, `champPoil`.

### 1 · LA COURONNE — le Noyau
Tout pelage a un point d'où il part. Le sien est **au centre de la face qu'on regarde** :
c'est « toi », et ça ne coûte pas un pixel d'interface. Le champ est le gradient de l'angle
à ce point ; ses deux seuls zéros sont **la couronne** (le dessin qu'on veut) et son
antipode, sur le dos, qu'on ne peint pas.
*Avant :* un disque crème de 8 % du rayon, qui se lisait comme **un trou clair percé dans le
velours**.

### 2 · LES ÉPIS — les six
Une personne à qui on a donné sa parole est **un épi** : le poil tourne autour d'elle en
spirale. **Le rayon et le serrage montent avec le cumul** — plus on a tenu parole avec
quelqu'un, plus l'épi est large et serré. `k` ne descend jamais : **un épi ne se défait pas**.
*Avant :* six pastilles sombres à anneau, à intervalle égal, qui **n'encodaient plus rien**
depuis qu'on avait libéré la géométrie. Six trous percés dans le velours, et le §3 les
condamnait.

**⚠ Deux réglages qui décident de tout, et les deux ont été payés :**
- **UN ÉPI EST PETIT.** À `0,15 + 0,33 k` il couvrait **vingt-sept degrés** : sur le disque
  visible, une **cuvette** — et comme toutes les fibres y convergent, elles s'éteignent
  ensemble. Six grands creux sombres, **une balle de golf**. Ramené à trois-huit degrés.
- **UN ÉPI TOURNE PLUS QU'IL NE CONVERGE.** À dominante radiale, tous les brins pointent au
  même endroit et s'éteignent ensemble : petit **cratère** sombre. À dominante tangentielle
  (`0,42 · radial + 0,91 · tour`), la moitié du tour regarde la lumière et l'autre s'en
  détourne : **un croissant clair et un croissant sombre**. C'est à ça qu'on reconnaît un épi
  sur un vrai pelage, et ça ne salit rien.

### 3 · LES CARESSES — et elles reviennent au repos
**⚠ Elles avaient été retirées le matin même, et à raison** : c'étaient des **gravures**
posées au hasard sur un objet neuf. Ce n'est plus la même chose : une caresse ne creuse plus
rien, elle **couche le poil dans son sens**. On lit le parallélisme de quelques milliers de
brins — et **c'est ça, un lustre**. L'objet au repos porte donc ses traces : on voit, sans
toucher, que quelqu'un s'en est occupé. Une Pelote neuve n'en a aucune.

**⚠ Et sans le terme de lustre, une bande peignée sortait SOMBRE** — une salissure, pas une
caresse : les brins alignés s'éteignent tous ensemble. Le poli monte donc **le ton (+1,7
marche) et la chroma** (l'étage saturé de la table). `_PO` ne porte plus que ça : **la
mémoire de la main**. Les six en sont sortis — ils écrivent le SENS, pas le ton, et
mélanger la main et les gens dans une même variable était une faute.

### 4 · LE PRÉNOM NE S'ÉCRIT QU'AU TOUCHER
Rien n'est lisible sur la Pelote pour un inconnu. `o.effleure` pose le prénom au-dessus de
l'épi effleuré, puis il disparaît. Aucun texte au repos.

### ⚠ LA CROISSANCE — CE QUI EST TENU, ET CE QUI NE L'EST PAS
`pousse` (0 → 1, jamais en arrière) relève le plancher de longueur du poil et monte le ton
d'une marche et demie. **Mesuré, à la vraie question :**

```
pousse  0 -> 34 Promi    59,05 % des pixels bougent de plus de 3/255
pousse  5 -> 34 Promi    57,64 %
pousse  5 ->  6 Promi     2,74 %      (0,09 % avant ce lot)
```

**Sur la longue course, la croissance se voit — franchement.** Sur **un** Promi de plus,
elle reste au ras du seuil, et je ne prétendrai pas l'inverse : **aucune variable globale
continue ne peut rendre un +1 visible** — un trente-quatrième de quoi que ce soit est
invisible, c'est de l'arithmétique.

**Ce qui rendra le +1 visible, c'est LA DALLE ELLE-MÊME** — et aujourd'hui **une chance sur
deux qu'elle tombe sur la face cachée**. La réponse est une règle de PLACEMENT, pas de
rendu : *la dalle qu'on vient de planter se pose face à toi.* **Ce n'est pas fait** — c'est
le lot suivant, et c'est le vrai.


### ⚠ ET ON NE LES VOYAIT PAS — CORRIGÉ LE MÊME JOUR
Tom : *« pas compris ni vu le principe des épis »*. Il avait raison, et deux choses le
rendaient illisible :

- **ILS ÉTAIENT TROP PETITS.** À trois-huit degrés, un épi fait **quatre à dix brins de
  large** : à cette taille on ne lit pas une spirale, on lit une petite salissure. Ils
  passent à **six-dix-huit degrés** (`0,105 + 0,205 k`), soit une trentaine de brins. Le
  creux sombre ne revient pas pour autant : ce qui l'évitait, ce n'était pas la petite
  taille, c'était **la dominante tangentielle**.
- **LE BRIN SE FONDAIT DANS SA PEAU.** Un épi ne se lit que si on **suit les brins qui
  tournent**. Au contraste de la surface plate, ils disparaissaient et il ne restait qu'une
  ombre vague. **L'amplitude du lustre double à l'intérieur de l'épi** (`11,5 → 26,5`) et le
  poil y gagne un cran de longueur — un poil que le peigne redresse est plus long à l'écran.
  Le brin se détache, et c'est **le tour** qu'on lit, pas une tache.

Le poids d'épi est publié par point (`_EW`, porté jusqu'au versement comme `_PO`), donc il
ne coûte pas une seconde boucle sur les six.

**Et une rangée de la planche montre le principe** : trois gros plans, un seul épi, à trois
cumuls — `ep-faible`, `ep-moyen`, `ep-fort`. Sur la page entière un épi fait quelques
dizaines de pixels ; c'est de près qu'on comprend.

### CONTRÔLES
```
vingt-huit cadres compares deux a deux   un seul couple identique, et il est VOULU
                                         (pg-trente / q-repos : meme etat, le temoin
                                         de la rangee du doigt)
circularite  g-vide                      rayon 278,4  ecart-type 0,97  soit 0,35 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **La dalle neuve face à toi** — le vrai correctif du critère 4.
- **Le terracotta contre sa propre grammaire** (§3 : il veut dire « à tenir »).
- **Une dalle orange sur un sol terracotta disparaît** (seuil 42 non tenu).
- **La composition de la page** : la boule occupe le tiers haut.
- `disques` et `noyau` restent dans le fichier, **non appelés** (`o.pastilles` les rallume),
  le temps que Tom confirme qu'on ne revient pas en arrière.

---

## ⚑ LA COULEUR DIT À QUI TU AS TENU PAROLE — JAMAIS CE QUI MANQUE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

### ⚠ LA VARIABLE N'EST PAS L'ÉTAT, ET C'EST TOM QUI A POSÉ LA BORNE
Piloter le sol par l'état majoritaire donnait une sphère terracotta qui dit
**« la plupart de tes paroles sont en retard »** : un état de manquement rendu visible, et
— pire — **une couleur qui change toute seule quand le temps passe**. C'est une valeur qui
décroît par inaction. **Écarté.**

**La variable prise : À QUI LA PAROLE TENUE S'ADRESSAIT.**
L'Pelote ne contient que des paroles **tenues**. On les répartit selon la personne
concernée, et le sol prend la couleur du groupe le plus fourni :

```
menthe      #2BE88C   celles que tu as tenues POUR TOI
terracotta  #F07A2E   celles que tu as tenues POUR QUELQU'UN
mauve       #8A5CF0   celles que tu as tenues AVEC UN GROUPE (une Nuee)
```

Les trois comptes **ne font que monter**. Aucun ne peut baisser, aucun ne bouge quand on ne
fait rien, aucun ne nomme un manquement : les trois disent une parole tenue, seulement pas
à la même personne. La teinte change **en faisant plus**, jamais en laissant filer.

**⚠ ET LE PRIX EST RÉEL, IL FAUT LE DIRE.** Au §3 de `CLAUDE.md`, **terracotta veut dire
« à tenir »**. Lui faire dire ici « tenue pour quelqu'un », c'est **une couleur signal qui
dit deux choses** — exactement ce que la grammaire du produit interdit. Le jeu sans
ambiguïté serait **bleu #3A54FF · framboise #FA2258 · mauve #8A5CF0** (les trois natures,
trois signaux existants, zéro collision) — mais il perd le terracotta et la menthe.
**Arbitrage à Tom, non tranché.**

**Le sol n'est pas une dalle** : la règle du §4 (« la dalle porte le monde ») tient entière
— chaque dalle garde le monde et la couleur de sa plantation.

### ⚑ LA DÉLICATESSE DU POIL VENAIT DE SON ÉPAISSEUR, ET ELLE ÉTAIT TROP FINE
À **0,50 px** d'épaisseur et à pleine opacité, une mèche tombe entre deux pixels : elle sort
**en marches**, et la matière se lit en **grains durs**. La finesse d'un velours ne vient pas
de brins plus maigres — elle vient de brins **qui se fondent**. On élargit d'un tiers de
pixel (`0,82`) et on baisse l'opacité du tampon (`1,00 → 0,78`) : même densité, même sens,
un **fondu** au lieu d'un crénelage. Et la mèche s'allonge d'un tiers (`TAI0` de 1,9-5,5 à
2,5-7,3) : sous quatre pixels de long, l'œil ne lit plus un **brin**, il lit un **grain**.

### ⚠ ET DEUX TACHES RESTAIENT, DE MÊME FAMILLE
- **Les six sortaient en disques saturés.** Le seuil de bascule vers l'étage ressaturé
  était **franc** : un seuil franc sur une calotte donne un disque à bord net — la version
  chroma de « des pois ronds qui ne correspondent à rien ». **Le seuil se tire au poil** :
  la bascule devient un fondu granuleux, à l'échelle de la fibre. Et la ressaturation
  descend de `× 1,34` à `× 1,11`.
- **Le lustre éteignait une région entière.** Là où le peigne pointe vers la lumière, tous
  les poils du coin s'éteignent **en même temps** : ça ne fait pas du grain, ça fait une
  **salissure**, au même endroit sur les trois teintes. Le lustre est donc **borné par le
  bas** : il éclaire librement, il n'assombrit que d'une marche.

### L'ÉCLAIRAGE MONTE D'UN CRAN
Le pied de la rampe passe de **2,2 à 5,4** et la course se resserre (20,0 → 16,4) pour ne
pas écrêter le clair. Mesuré sur la terracotta, diagonale haut-gauche → bas-droit :
**170 · 155 · 119 · 116** de luminance.

### CONTRÔLES
```
vingt-huit cadres compares deux a deux   un seul couple identique, et il est VOULU :
                                         pg-trente et q-repos sont le meme etat (30 Promi,
                                         sans empreinte) — q-repos est le temoin de la
                                         rangee du doigt.
circularite  e-terra-0                   rayon 153,3  ecart-type 0,81  soit 0,53 %
             e-vert-0                    rayon 153,3  ecart-type 0,81  soit 0,53 %
             g-vide                      rayon 276,0  ecart-type 0,99  soit 0,36 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **Le terracotta contre sa propre grammaire** (ci-dessus) — décision produit.
- **Une dalle orange sur un sol terracotta disparaît** : le seuil 42 du §3 n'est pas tenu
  entre le sol et les dalles de même famille. Visible sur `e-terra-30`.
- **L'état à zéro n'a pas de majorité** : quelle teinte porte une Pelote neuve ?
- **La composition de la page** : la boule occupe le tiers haut.

---

## ⚑ LE GRAVIER N'ÉTAIT PAS DU GRAIN — C'ÉTAIT LE FOND QUI PASSAIT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

Deux reproches : **« ton dégradé, on n'y croit pas »** et **« ça fait des croisillons »**.
Ils avaient la même cause, et ce n'était ni la lumière ni le relief.

### 1 · LE POIL SE COMPOSAIT SUR DU NOIR
Le bord d'un tampon de poil est **doux** : son alpha tombe à 60 ou 100 sur le pourtour.
Comme le versement ne garde que **le plus opaque** et rien d'autre, une foule de pixels
restaient à mi-alpha — et se composaient avec **l'encre du fond**. Mesure : **6,9 % du
disque sous 40 de luminance**, en tirets noirs, partout.
Ce bruit est **à haute fréquence et uniformément réparti** : il écrase mécaniquement une
variation lente. **Tant qu'il était là, aucun dégradé ne pouvait se voir** — on aurait pu
le monter à n'importe quelle amplitude.

**⚠ Et on ne corrige pas ça en opacifiant la fourrure.** Essai fait, regardé, revenu :
toute la forme d'un poil vit dans son **alpha** — sa couleur n'est qu'un aplat de marche.
Forcer alpha à 255 remplace le pelage par des aplats ; la boule est sortie **en bandes
lisses, sans un poil**.

**La parade — une peau.** Un pelage a une peau : entre deux poils on ne voit pas le vide,
on voit la bête. On la fabrique **à partir du dépôt lui-même** — le tampon réduit par
blocs, chaque bloc prenant la moyenne pondérée de ce qui s'y trouve, puis redilaté en
lissage bilinéaire. C'est donc, par construction, **la couleur du lieu, dalles comprises**,
sans un calcul de plus.

**⚠ Trois pièges, tous payés :**
- **Le bloc doit être GRAND devant le poil.** À 7 px — la taille d'un poil — la peau *est*
  la fourrure : elle annule son propre contraste. Bloc **26**, soit trois à quatre poils.
- **La peau s'arrête un bloc AVANT le limbe.** Un bloc à cheval sur le bord est à moitié
  peint ; lui donner un alpha proportionnel faisait sortir **des carrés de couleur** autour
  de la boule. On **érode** : un bloc n'est opaque que si lui *et ses quatre voisins* sont
  pleins. C'est la fourrure, antialiasée, qui dessine seule la silhouette.
- **⚠ ET LE COMBLEMENT SE LIT SUR UNE COPIE, JAMAIS SUR LUI-MÊME.** Écrit en place, un
  balayage en lignes prend pour voisin **ce qu'il vient de combler** : le remplissage se
  propage vers le bas et vers la droite, et la boule sortait avec **un escalier de
  rectangles** hors du limbe — **en bas à droite seulement**. *C'est l'asymétrie qui trahit
  ce bug : un défaut de géométrie serait symétrique.*

### 2 · LE GRAIN VIENT MAINTENANT DE L'ANGLE DE LA FIBRE
Une fois la peau posée, il fallait redonner un dessin au pelage — sans les trous. Sur un
vrai velours, un poil **en travers** de la lumière s'allume, un poil **dans son axe**
s'éteint : c'est le terme de Kajiya-Kay, appliqué ici **à la marche d'un poil entier**, pas
en tache spéculaire. Aucun reflet n'apparaît, seulement des poils un peu plus clairs et un
peu plus sombres que leur voisinage.

**⚠ Et deux réglages le rendaient invisible :**
- **la dispersion d'angle se pose sur LA FIBRE, pas sur le tampon.** Posée juste avant
  `secteur`, elle ne tournait que le **dessin** ; le lustre continuait de lire le peigne
  moyen, donc tous les poils sortaient à la même marche.
- **la rampe ne doit pas saturer.** À `lum × 19,4`, le côté éclairé tombait déjà sur la
  dernière marche : la variation de fibre y était **écrêtée**, et la fourrure sortait lisse
  en haut à gauche et grenue en bas à droite, sans qu'on comprenne pourquoi.

### ⚑ ET LE « CROISILLON » ÉTAIT UNE MOIRE
Depuis que le peigne porte un biais, tous les poils d'une zone tombaient dans **le même
secteur sur vingt-quatre** : le même tampon, au même angle, sur un semis quasi-régulier —
**ça tisse**. Sur un vrai pelage les poils suivent le peigne **à peu près**, et c'est ce
« à peu près » qui fait le soyeux. La dispersion d'angle (0,74 rad) le rend.

### ⚠ ET LA MARGE DE REJET APLATISSAIT LA SILHOUETTE
Un poil dont le tampon sortirait du tampon de pixels écrirait sur la ligne suivante : on le
rejette, à 26 px du bord. Mais à **R = 0,472** la boule laissait **moins de marge que ça** —
le rejet lui coupait donc **quatre méplats**, en haut, en bas, à gauche et à droite. On
lisait un polygone là où la géométrie était un cercle exact. **R = 0,438**, soit un
diamètre de 342 pt dans un écran de 390 : les gouttières du produit.

### ⚠ ET LE BAS DE LA RAMPE NE DOIT PAS REJOINDRE L'ENCRE
À 0,62 vers le fond, le côté sombre **descendait sous le seuil de lecture de sa propre
silhouette** : les 360 rayons s'arrêtaient vingt pixels trop tôt en bas à droite. Une boule
dont le bord se dissout dans le fond n'a plus de contour — et le contour est ce qui la fait
exister. On garde le glissement vers l'encre (c'est lui qui évite le bleu électrique), on
s'arrête avant de la toucher : **0,44**.

### ⚑ LA TAILLE DE L'EMPREINTE SE CALCULE, ELLE NE SE CHOISIT PAS
`a` est le demi-grand axe du contact, **en fraction du rayon de la boule**. Il était à
**0,42** : l'empreinte faisait **84 % du diamètre de la Pelote** — un doigt aussi large que
l'objet. Ce n'est pas un goût, c'est une cote :

```
ecran            390 pt pour 71,5 mm          =>  5,455 pt / mm
la boule         R = 0,438 x 390              =>  170,8 pt de rayon
pulpe de pouce   17 x 12 mm  => 8,5 et 6,0 mm =>  46,4 et 32,7 pt
pulpe d'index    11 x  8 mm  => 5,5 et 4,0 mm =>  30,0 et 21,8 pt

POUCE  a = 0,272  el = 0,70   soit 27 % du diametre
INDEX  a = 0,176  el = 0,73   soit 18 % du diametre
```

**Et c'est le capteur qui tranche, pas une constante.** Un `Touch` porte `radiusX`,
`radiusY` et `rotationAngle` : l'app lit la pulpe **réelle** et pose `a = radiusX / R`,
`el = radiusY / radiusX`, l'axe à l'angle donné. Les deux jeux ci-dessus sont **les bornes**
entre lesquelles ça tombe — c'est à ça qu'ils servent.
Une rangée de la planche le montre dans la page Aura, avec la pulpe tracée par-dessus à
l'échelle (calque de mesure, pas un élément du produit).

### CONTRÔLES
```
dix-neuf cadres compares deux a deux     zero doublon
circularite  g-vide                      rayon 275,0  ecart-type 0,91  soit 0,33 %
             n-neuf                      rayon 275,3  ecart-type 0,93  soit 0,34 %
             v-30 (grand format)         rayon 561,9  ecart-type 2,07  soit 0,37 %
degrade, diagonale haut-gauche -> bas-droite
  -0,85 (173,136,253) 161   -0,50 (147,100,253) 132   -0,20 (127, 71,250) 108
  +0,20 ( 97, 37,228)  76   +0,50 ( 70, 19,184)  53   +0,85 ( 75, 21,194)  57
cout des deux passes ajoutees, tampon 680 x 680
  comble 1,1 ms   peau 1,6 ms            (median sur onze passages)
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI N'EST PAS TENU
**Le budget de 60 images par seconde ne l'est pas sur cette planche** : un cadre de la page
Aura coûte **40 ms**, et **34 ms restent même en coupant tout le versement** — c'est la
boucle sur les points et le blit, pas les deux passes ajoutées. La planche tourne à
**180 000 poils** pour un écran de 340 px, là où le banc donnait 36 450 poils à 16,4 ms.
**C'est une densité de planche, pas une densité d'app** : le chiffre à tenir se mesurera
sur la vraie page, avec la densité qu'elle portera.

---

## ⚑ UNE SEULE VARIATION LARGE SUR LA BOULE : LA LUMIÈRE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/pelote-velours/`

Deux demandes : **retirer les traces de doigt au repos**, et **un vrai dégradé** — clair
en haut à gauche, violet profond vers le bas-droite. La seconde a ouvert quatre défauts
qui se cachaient les uns derrière les autres.

### 1 · LES TRACES SORTENT DU REPOS
Neuf caresses gravées en permanence **n'ont pas de sens** : au repos l'objet est **neuf**,
et c'est cette uniformité qui donne envie d'y toucher. La trace n'appartient qu'à **la
séquence du doigt** (`d-apres`, `n-marque`), jamais à l'état de repos.

### 2 · UN SEUL DÉGRADÉ, ET LA CLÉ RETROUVE SON AMPLITUDE
J'avais aplati la lumière à **0,16** pour tuer les halos — et j'ai tué le volume avec.
Ce n'était pas la clé qui posait des halos, c'étaient les termes qui posent un **motif**
(lustre de fibre en bandes, contre-jour en anneau, liseré au limbe). Ceux-là restent
coupés ; la clé repasse à **0,30 + 0,70**, et elle est **seule** — donc aucun motif n'est
possible. Mesuré sur la diagonale de `g-vide`, du coin haut-gauche au coin bas-droit :

```
-0,85   (130, 104, 188)   luminance 122
-0,50   (107,  78, 172)              97
-0,20   (100,  74, 161)              91
+0,20   ( 73,  36, 155)              60
+0,50   ( 66,  28, 150)              53
+0,85   ( 68,  27, 160)              54
```

### ⚑ MAIS TROIS AUTRES CHOSES VARIAIENT À LA MÊME ÉCHELLE, ET PASSAIENT DEVANT

**Un dégradé ne se voit que si RIEN D'AUTRE ne varie à sa taille.** Le dégradé était posé
et juste — et illisible, parce que trois mécanismes fabriquaient des taches de la taille
d'un cinquième de boule. Il a fallu les retirer un par un.

**a · LES ÉPIS DU PEIGNE.** Le sens du poil venait d'un seul bruit. Un champ de directions
tiré d'un bruit a des **points critiques** — des épis, comme sur un crâne — et chacun
sortait en large tache grise à centre radial. Un champ tangent sur une sphère **ne peut
pas** être partout non nul (boule chevelue) : il a forcément deux zéros. On choisit donc
**où ils tombent** au lieu de les subir — un biais constant, dans la direction qui sort
**horizontale à l'écran**, met les deux zéros **au limbe gauche et au limbe droit**, là où
la matière est vue de profil. Le bruit reste, à un tiers : il donne l'ondulation, plus la
structure.

**b · LE BAS DU SPECTRE DU RELIEF.** `A × K` est l'inclinaison qu'une onde donne à la
fibre, et les six valaient **0,12 chacune** : la plus basse fréquence inclinait donc autant
que la plus haute, mais sur cinq fois plus de surface. ⚠ **Essai fait et mesuré : faire
monter `A × K` avec `K` sort un QUADRILLAGE de pois pâles.** Dès qu'une fréquence domine,
on lit sa période ; six ondes de même inclinaison se somment en bruit. On ne touche donc
pas à la **répartition** — on divise **l'ensemble** par deux.

**c · L'ENVELOPPE.** Sa fréquence est de l'ordre de la boule : tout ce qu'elle peut
produire est une **tache**. Elle était là pour « faire respirer la matière » — mais la
respiration se lit dans le grain. **Amplitude nulle.**

### ⚑ ET LA PROXIMITÉ DES SIX ÉTAIT CÂBLÉE SUR LE MAUVAIS AXE
« Une personne proche est une matière **plus saturée, plus travaillée**. » Je l'avais
branchée sur **la marche de clarté** : +1,9 marche dans une calotte de 0,19 rad. Résultat,
**six pois ronds pâles** — exactement ce qui avait été refusé. Une marche de clarté **est
de la lumière**, et la lumière de cette boule vient du titre, d'un seul côté : on ne peut
pas s'en servir pour dire autre chose.
La table de couleurs a donc **un second étage** — les mêmes teintes, les mêmes vingt
marches, **ressaturées** (`s × 1,34 + 0,06`). Le poli ne déplace plus la marche, il change
d'étage : la matière devient plus dense **en couleur**, jamais plus claire. Coût par
image : nul, la table se bâtit une fois.

### ⚠ ET LA CLAIRIÈRE DU NOYAU N'AVAIT PLUS DE RAISON D'ÊTRE
Même adoucie à 0,80, elle sortait en **grand disque sombre** autour du Noyau — le « halo
bizarre » refusé, sous un autre nom. Le Noyau est crème sur un velours violet : il se
détache seul. `pres = 1` partout.

### ⚠ ET LE HAUT DE LA RAMPE VIRAIT AU GRIS, COMME LE BAS VIRAIT AU BLEU
Le mur de colorimétrie a **deux bouts**, et `rampeCouleur` ne joue que sur la clarté HSL.
En bas, baisser la clarté d'un violet saturé donne un **bleu électrique** — on mélange donc
vers l'encre du fond. En haut, la monter donne un **gris-lilas délavé** — on monte donc la
clarté de moitié moins (`+0,225` au lieu de `+0,30`) et **on ressature** (`× 1,34`). Le
haut reste violet, il est seulement plus lumineux.

### ⚠ ET LE SIGNE DE LA LUMIÈRE SE VÉRIFIE AU CHIFFRE, PAS AU RAISONNEMENT
J'ai déduit **deux fois de suite** la mauvaise convention pour la normale de vue, et deux
fois le clair est sorti du mauvais côté. Le contrôle tient en trois relevés de couleur
moyenne sur la diagonale (tableau ci-dessus). **On mesure, on ne déduit pas.**

### CONTRÔLES AVANT LIVRAISON
```
seize cadres compares deux a deux        zero doublon
circularite de la silhouette (g-vide)    rayon 295,7  ecart-type 0,87  soit 0,30 %
circularite (v-30, grand format)         rayon 601,3  ecart-type 5,26  soit 0,87 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **La composition de la page Aura** : la boule n'occupe que le tiers haut de l'écran.
- **Le concept alternatif** reste à construire — la fourrure est le candidat, pas la réponse.

---

## ⚑ LA LUMIÈRE VIENT DU TITRE, ET ELLE EST PRESQUE INVISIBLE · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### CE QUE TOM A DEMANDÉ
La sphère vit dans **l'écran Aura**, le mot-marque **Aura** en haut à gauche. La lumière vient
**de lui**, mais **suggérée** : un dégradé uniforme presque invisible, **et pas de halo** —
« ça complexifie trop ».

### CE QU'ON A COUPÉ, ET POURQUOI
```
la cle              0,42 -> 0,13     un tiers de la boule etait dans l'ombre
le lustre de fibre  0,22 -> 0        il pose UNE BANDE perpendiculaire au peignage ;
                                     sur un velours en volutes, les bandes se croisent
le contre-jour      0,40 -> 0        c'est un ANNEAU : un halo, donc un interdit
le lisere au limbe  +0,22 -> -0,10   un bord plus clair que le centre EST une aureole
le duvet du limbe   coupe
```
**Amplitude totale de la lumière : 0,16 sur 1.** Le volume vient du **grain**, pas de l'ombre.
La direction pointe franchement vers le haut-gauche — vers le titre.

### ⚠ J'AI ACCUSÉ LE CULLING À TORT, ET LA MESURE M'A REPRIS
Je lisais des **facettes** sur le bord et j'ai élargi le seuil des plaques pour « rendre la
frontière aux points ». Mesure ensuite (`scratchpad/mesure_rond.py`, 360 rayons tirés du
centre) : **rayon 296,3, écart-type 1,65 — soit 0,56 %.** **La silhouette était déjà un
cercle.** Ce que je prenais pour des facettes, ce sont les **grands plateaux clairs de la
matière** : l'enveloppe faisait varier l'amplitude du relief de **un à cinq**, d'où des zones
à bord franc qu'une lumière uniforme révèle. Ramenée de un à deux. Seuil de culling remis à
sa valeur, et son surcoût avec.
> **La condition « on doit pouvoir tracer un cercle parfait autour » est donc tenue, et
> mesurée : 0,59 % d'écart après correctif.**

### ET LA TRACE SE CALME
À +4,2 marches elle était lisible sous une lumière sculptée ; sous une lumière uniforme elle
devenait **une grande traînée pâle** qui mange la boule. **Une caresse laisse un lustre, pas
un coup de pinceau.** Ramenée à +1,9.

### CONTRÔLE AVANT LIVRAISON
**Treize cadres comparés deux à deux : zéro doublon.** C'est désormais systématique.

---

## ⚑ LA MÊME FAUTE, DEUX FOIS — et cette fois on supprime la classe · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### LE BUG, ET IL EST GRAVE PARCE QU'IL EST SILENCIEUX
`cadre()` recopiait **à la main** les options qu'elle connaît. La première fois,
`velours`/`contre`/`duvet`/`grade`/`dresse` tombaient dans le trou : huit cadres identiques au
pixel près. **Je l'ai « corrigé » en ajoutant ces cinq noms à la liste.** La faute était
**la liste elle-même** : au lot suivant, `traces` et `six` sont tombés dans le même trou.
```
« marque » et « relisse »   identiques a 0,00 %
les six par la matiere      JAMAIS APPLIQUES, sans une seule erreur
```
> **⚑ LA PARADE, ET C'EST LA BONNE :** `cadre()` recopie désormais **tout** ce que l'appelant a
> posé et que l'objet ne porte pas encore. Une option nouvelle arrive au peintre sans qu'on y
> pense. **Corriger l'occurrence d'un bug de recopie manuelle ne sert à rien — il faut
> supprimer la recopie manuelle.**
> Contrôle systématique ajouté : **treize cadres comparés deux à deux, zéro doublon.**

### ⚑ « LES HALOS AU PIXEL » — c'était une ombre portée déguisée
Les six se dessinaient **dans le tampon de pixels**, cercle par cercle, avec un test
`d² > r²` : **aucun antialiasing possible**, donc un bord en escalier. Et ils portaient un
**halo d'encre** de treize millièmes du rayon — c'est-à-dire **une ombre portée**, l'un des
trois interdits qui font le « cheap ». Le Noyau en avait un de trente-quatre millièmes.
Les deux sont redessinés **au contexte 2D, après le versement** : les arcs y sont antialiasés,
et le halo saute. Il ne reste qu'un **filet** de la couleur du fond pour que le crème ne bave
pas dans le velours — **un filet n'est pas un halo**.
Et leur **position n'encode plus rien** : ils sont posés à intervalle égal, puisque la
proximité se lit maintenant dans la matière.

---

## ⚑ « L'ÉCLAIRAGE EN CROISILLON » — c'était le RELIEF, pas la lumière · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### LA CAUSE
Le relief valait `Σ amp · sin(fx·x) · sin(fy·y) · cos(fz·z)`. **Un produit de sinus est
SÉPARABLE : ses zéros sont des plans x = cte, y = cte, z = cte.** La surface portait donc
une **grille**, et dès qu'on l'éclairait on voyait un croisillon en travers de la boule.
Ce n'était ni la lumière ni le grain — **c'était la forme même du relief.**

### LA PARADE — UNE SOMME D'ONDES PLANES OBLIQUES
```
avant   3 bandes, produit de sinus sur les axes x, y, z   -> un reseau
apres   6 ondes planes, directions prises sur une spirale de Fibonacci,
        normes 9,7 a 37,7 irrationnelles entre elles      -> isotrope
```
Aucune onde n'est alignée sur un axe, aucune période n'est commune : le relief ne se répète
plus. ⚠ **Et la règle de l'audit tient toujours** — « toutes les fréquences ≥ 8 sur les trois
axes », qui évitait une enveloppe basse fréquence sur un seul axe (une courge) : chaque onde a
un vecteur d'onde de norme ≥ 9 **dans une direction oblique**.
**L'enveloppe aussi** était un produit de sinus : elle reposait son propre réseau, plus
grossier, par-dessus le premier. Passée en somme de deux ondes obliques.
Amplitude totale **divisée par deux** : le relief n'a pas à se voir, il est là pour accrocher
la lumière rasante.

### ET UN ÉCLAIRAGE SIMPLE
Le lustre de fibre (Kajiya-Kay) pose une **bande claire perpendiculaire au peignage** : sur un
velours peigné en volutes, ces bandes **se croisent** et ajoutent leur propre motif. Joli en
mouvement, du bruit sur une image fixe. Ramené de 0,80 à **0,22** — il ne doit plus que tiédir
la matière, pas la dessiner. Contre-jour 0,70 → 0,40, grading 0,9 → 0,55.

### CE QUI RESTE DISCUTABLE
- Le contact sort encore en **tache très saturée** plutôt qu'en compression.
- La boule est maintenant **très uniforme** — subtile, comme demandé, peut-être trop calme.

---

## ⚑ LE VELOURS, ET LA MÉMOIRE DE LA MAIN · 9 septembre 2026

> **`app.html` inchangé** · **`PLANCHE-VELOURS.html`** + `scratchpad/_v_*.js`
> La fourrure est **ressortie** de `sauvegardes/PELOTE-FOURRURE-DEPOSEE/`.
> Les trois concepts du lot précédent (mémoire minérale, fil, fond perdu) sont **refusés en
> bloc** par Tom — concept et design. Ils restent dans `sauvegardes/pelote-memoire/`.

### LES QUATRE CHANGEMENTS
**1 · UN VELOURS, PAS UNE FOURRURE.** Le pelage montait à 13 px sur un cadre de 620 : ça fait
une bête, pas une matière. `[1,9 · 3,3 · 4,3 · 5,5]` — deux fois et demie plus court. **Et le
ras durcit la silhouette**, parce qu'un poil court déborde moins du contour. Semis remonté à
360 000 pour garder la matière pleine.

**2 · LES DALLES SONT TAILLÉES DANS LE MÊME VELOURS.** Le rapport entre la coupe d'une dalle
et celle du sol tombe de **3,8 à 2,3** : une dalle cesse d'être une **inclusion posée dessus**,
elle devient **un endroit où le velours a une autre teinte et une autre coupe** — dans la
couleur et le monde de sa plantation.

**3 · LA MÉMOIRE DU GESTE.** La déformation est réelle sur le moment, puis **la forme revient** :
la silhouette n'est jamais abîmée. Ce qui reste n'est **pas un creux** — c'est le poil couché :
la chroma monte de quatre marches, le grain s'oriente dans le sens du geste, la coupe se tasse.

**4 · TOUT RELISSER.** Un état « neuf » où toutes les traces sont effacées. C'est ce qui rend
le peignage **sans conséquence** : on peut jouer sans rien salir.

### ⚑ LES SIX PAR LA MATIÈRE, PAS PAR LA POSITION
Encoder la proximité par une **distance** force la structure radiale, donc le centre, donc
l'objet centré, donc le contour — **la case qui a tué quinze versions**. Ici une personne
proche est une **matière plus travaillée** : plus saturée, au grain plus fin, **où qu'elle soit
sur la sphère**. Leurs positions sont à intervalle égal et n'encodent rien. La géométrie est
libérée, et *« rien ne recule jamais »* tient toujours — **une matière ne se désature pas.**

### ⚠ UN PIÈGE ÉVITÉ CETTE FOIS
La clé du cache des statiques **ne portait ni les traces ni les six**. Deux cadres qui ne
diffèrent que par la mémoire des gestes se seraient partagé le même cache et seraient sortis
**identiques au pixel près** — exactement la livraison où huit cadres étaient les mêmes.
Ajouté à la clé avant de rendre.

### MESURÉ — les états diffèrent vraiment
```
sous le doigt        40,6 % des pixels different du repos
deux secondes apres  11,2 %
relisse              20,5 %
```

### CE QUI RESTE À JUGER
- Le contact sort en **tache très saturée** plutôt qu'en compression : lisible, mais peut-être
  trop marqué.
- L'état « deux secondes après » garde encore beaucoup — le retour pourrait être plus net.

---

## ⚑ TROIS CONCEPTS EN CANVAS 2D RÉEL — la mémoire de la main · 9 septembre 2026

> **`app.html` inchangé** · **`PLANCHE-MEMOIRE.html`** + `scratchpad/_m_*.js`
> **L'pelote-fourrure est DÉPOSÉE**, pas abandonnée : `sauvegardes/PELOTE-FOURRURE-DEPOSEE/`
> avec son mode d'emploi de retour et les six acquis qui valent pour toute suite.

### LE PARTI, ISSU DE DEUX ÉTUDES INDÉPENDANTES
**Un objet numérique qui se souvient des gestes de son propriétaire.** La patine est
**l'organe**, pas l'ornement. Avec trois conditions posées par Tom :
1. **La forme reste belle** — on doit pouvoir tracer un cercle parfait autour, quelle que soit
   l'histoire des gestes. Une empreinte ne rend jamais l'objet difforme.
2. **La matière résiste** — ni mou, ni slime, ni caoutchouc : entre la céramique crue, la cire
   minérale et la pierre tendre. Une matière qui n'existe pas.
3. **Ça revient** — la déformation est réelle sur le moment, puis la forme sphérique revient.
   **Ce qui reste n'est pas un creux : c'est un lustré, un grain, une chroma qui a monté.**

### COMMENT ON PEINT SANS DÉGRADÉ, SANS OMBRE ET SANS TACHE SPÉCULAIRE
Ce sont **ces trois-là** qui font le « méga cheap ». Donc : **chaque marque est un aplat franc**
pris dans une rampe de vingt marches. Le volume ne vient pas d'un fondu — il vient **du nombre**
de marques et de la marche que chacune prend. C'est la règle du moteur de la Toile, à la lettre.
Le contour se dessine par le **raccourci au limbe** (la matière s'y voit de biais, elle rend
moins), jamais par un liseré lumineux.

### LES TROIS PLANCHES
```
A · LA MEMOIRE DE LA MAIN   une matiere minerale (facettes, pas des poils), et le
                            POLI des gestes : le grain s'affine, se couche dans le
                            sens du geste, la chroma monte d'un ton
B · LE FIL                  le cumul des trajets d'un fil autour du Noyau ; ce qu'on
                            voit est le MOIRE qu'ils forment ensemble
C · A, A FOND PERDU         la meme matiere, sans contour, plein cadre
```

### DEUX BUGS PAYÉS
- **Les fils convergeaient tous en un point.** Je construisais un point puis je le
  **normalisais** — or normaliser rend toujours le même **grand** cercle, quels que soient le
  rayon et l'aplatissement. Tous les fils passaient donc par les deux mêmes pôles. On construit
  maintenant un **petit cercle** directement sur la sphère (axe, hauteur, `c² + r² = 1`).
- **La trace sortait SOMBRE.** Le grain poli était si fin qu'il couvrait *moins* que la matière
  brute : le fond passait entre les marques. Or ce qui reste d'un geste **n'est pas un creux,
  c'est un lustre**. Allongé sans être aminci, il couvre plus — et la chroma monte.

### CE QUE JE VOIS, HONNÊTEMENT
- **A tient son état vide** : une sphère minérale, contour parfaitement circulaire, grain fin,
  et les caresses lisibles comme des bandes lustrées. À 30, les dalles se lisent chacune dans
  son monde. **C'est le seul des trois qui passe le test décisif.**
- **B est superbe à 30** — un échevau de fils avec un vrai moiré — **et rate le test à vide** :
  sept fils ne font pas un objet, ils font des courbes lâchées dans le noir.
- **C répond à la question posée, et la réponse est non** : sans contour, on n'a plus un objet,
  on a un champ de grain. Supprimer le bord **supprime l'objet** au lieu de régler son bord.

### CE QUI N'EST PAS FAIT
- La proximité des six **par la matière** (et non par la position) n'est pas encore câblée.
- La déformation au doigt et son retour lent : c'est du mouvement, invisible sur une planche fixe.

---

## ⚑ « LE DERNIER POSÉ GAGNE » — la ligne qui bloquait tout depuis le début · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### CE QUE TOM A DIT
> *« la sphère n'est pas uniformément poilue ni éclairée, du coup on ne se rend pas compte des
> ajouts de dalles, ça complexifie tout »*

### ⚑ LA CAUSE, ET ELLE TIENT EN UNE LIGNE
`verse()` écrivait **sans relire** — *« le dernier posé gagne »*, une optimisation mesurée
(−18 % par poil) dont le commentaire disait *« acceptable pour une fourrure, un poil en
recouvre un autre »*. **Ce n'était pas acceptable, et voici pourquoi.**

L'alpha d'un brin est **fort à la racine, faible à la pointe**. Le peignage a une direction
dominante : du côté où les poils pointent, ce sont donc **les pointes qui écrasent les racines**
de leurs voisins ; du côté opposé, ce sont les racines. **Une moitié de boule à 49, l'autre à
83** — à couverture égale et à éclairage égal.

**La parade tient en un test : on garde LE PLUS OPAQUE.** L'alpha étant dans l'octet de poids
fort, comparer les entiers compare les alphas — c'est un « max » à une comparaison, pas un
mélange.

### ⚠ TROIS HYPOTHÈSES FAUSSES AVANT DE TROUVER — et c'est la mesure qui a tranché
```
aplatir la cle (0,52 -> 0,12)          aucun effet       59,2 % -> 58,3 %
supprimer les variations de densite    aucun effet
densifier x2,3                         CA EMPIRE         43,9 % -> 52,4 %
```
> **⚑ ET UN INSTRUMENT QUI MESURAIT LE MAUVAIS CHIFFRE.** Mon premier écart-type était pris
> **pixel par pixel** : sur une fourrure il mesure **les poils**, pas l'inégalité d'éclairage —
> 47 sur 80 de moyenne, et il ne bougeait pas d'un point quand je coupais tout l'éclairage.
> On réduit l'image à 40×40 (chaque case moyenne des milliers de poils) et c'est **cette**
> dispersion qui dit si la boule est uniforme.

> **⚑ ET C'EST LA SONDE QUI A DONNÉ LA RÉPONSE.** J'ai instrumenté le peintre pour relever ce
> qu'il **dépose**, quart d'écran par quart d'écran : `lum` 0,95 à 1,00, `mar` 14,5 à 15,0,
> 21 400 points chacun — **identiques**. Et le quart le plus clair en `lum` était **le plus
> sombre à l'écran**. C'est cette contradiction qui a désigné le versement.

### CE QUE ÇA DONNE
```
                        AVANT          APRES
luminance moyenne        81,9          147,7      (cible : 90 a 110)
dispersion basse freq.   43,9 %         15,2 %
moitie sombre / claire   48,9 / 83,2   156,6 / 134,6
```
**Et un dividende : l'éclairage avait été aplati pour compenser ce défaut.** Le défaut corrigé,
un éclairage plat n'avait plus de raison d'être — il donnait un aplat lilas sans relief. La
clé est rendue (0,46 + 0,42), et le volume avec.

### CE QUI N'EST PAS FAIT
- La boule est **au-dessus** de la cible de luminance et un peu **lavée** : à cette clarté le
  lilas se désature (le mur de colorimétrie du lot précédent, dans l'autre sens).
- Le peigné-mémoire, l'inertie, la naissance d'un Promi : toujours pas construits.

---

## ⚑ POIL DE CHAT, DALLES RASÉES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`
> Sauvegarde : `sauvegardes/pelote-fourrure/`

### CE QUE TOM A DEMANDÉ
> *« plus soyeux, plus comme poils de chats ou lapin, plus nets, un peu plus long — et les
> dalles c'est en rasé plus court ? »*

### QUATRE CORRECTIFS

**1 · QUATRE LONGUEURS, ET LA PREMIÈRE EST LA TONTE.** `[3,4 · 7,6 · 10,2 · 13,0]`.
Index 0 = **les dalles**, index 1 à 3 = le pelage par profondeur. **Une zone tondue dans un
pelage se lit d'un coup d'œil** — c'est du relief, pas un aplat de couleur — et le rasé
**montre sa couleur bien mieux**, puisqu'il y a moins de brins qui se recouvrent pour la
moyenner. Le réglage `dresse` (les dalles en relief) sort : elles sont **tondues**, pas dressées.

**2 · PLUS NET.** À 0,86 d'extinction, la pointe disparaissait avant d'arriver et le pelage
sortait **brumeux** — on lisait un voile, pas des poils. Un poil de chat ou de lapin garde sa
matière presque jusqu'au bout : **il s'affine beaucoup, il ne s'efface pas.** On inverse le
partage — extinction `0,86 → 0,42`, affinement `0,78 → 0,88`.

**3 · PLUS SOYEUX : LES BRINS SE SERRENT.** Une fourrure de chat ou de lapin est fine, dense
et **parallèle** — c'est l'alignement qui fait le soyeux. À ±0,44 d'écart les brins partaient
en étoile : ça fait une **brosse**, pas un pelage. Resserré à **±0,20**, allongé, affiné
(`e×0,115 → e×0,095`).

**4 · ON OUVRE L'OMBRE.** À 0,34 d'ambiant contre 0,52 de clé, **la moitié de la boule tombait
dans le noir** : on ne pouvait ni lire ses dalles ni avoir envie d'y toucher. Ambiant `0,50`,
clé `0,40` — ce que fait n'importe quel éclairage de studio : **un remplissage qui ouvre
l'ombre au lieu de la boucher**, sans effacer le volume, puisque c'est le contraste qui
sculpte et pas le noir.

### MESURÉ
```
             luminance   saturation
avant           52,5        0,31
apres           60,5        0,29     cout 10 a 25 ms
```

### CE QUI N'EST PAS FAIT
- **La cible de 90-110 reste hors d'atteinte sur un sol bleu-violet** — c'est le mur de
  colorimétrie du lot précédent, pas un réglage. Le fork (sol chaud contre sol violet) est
  toujours ouvert et il appartient à Tom.
- Les dalles gagnent en lisibilité mais restent peu contrastées sur les mondes creux.
- Le peigné-mémoire, l'inertie, la naissance d'un Promi : toujours pas construits, et c'est là
  qu'est le « donne envie de toucher » qu'une planche fixe ne peut pas montrer.

---

## ⚑ LA LUMINANCE PERÇUE, ET LE MUR DE COLORIMÉTRIE · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### ⚑ CE QUI BLOQUAIT LA CLARTÉ DEPUIS LE DÉBUT — MESURÉ
Le sol sortait à **[77, 9, 225]** : clarté HSL **0,46**, luminance **perçue 54**.
**Le bleu ne pèse que 11 % dans la luminance** (0,299 R + 0,587 V + 0,114 B) : régler une
*clarté HSL* sur une teinte bleu-violet **ne veut rien dire à l'œil**. Je croyais avoir monté
l'objet ; je n'avais monté qu'un nombre.
On résout désormais **en luminance perçue**, par dichotomie ; si la teinte ne peut pas y
arriver à saturation pleine, on désature juste ce qu'il faut — jamais l'inverse. Le sol tombe
alors **exactement sur sa cible**, vérifié : 96.

### ⚑ LES DALLES S'ÉCHELONNENT EN LUMINANCE
*« on reconnaît peu les dalles, faut les préciser ou contraster »* — deux couleurs peuvent
avoir des **teintes très différentes et la même luminance** : l'œil les sépare alors mal,
surtout sous une fourrure qui moyenne tout. On impose donc des luminances **étagées**, toutes
écartées d'au moins **34** du sol. **La teinte dit laquelle ; la luminance garantit qu'on la voit.**

### ⚠ ET LÀ ON TOUCHE UN MUR QUI N'EST PAS UN RÉGLAGE
```
decalage de rampe    luminance de la boule    saturation
+1,9                       46,7                  0,38
+3,6  (retenu)             52,5                  0,31
+5,6                       58,8                  0,23
```
**Monter la clarté d'une teinte la rapproche du blanc.** Une teinte **bleu-violet ne peut pas
être à la fois claire et saturée** — c'est de la colorimétrie, pas un défaut de réglage.
On s'arrête donc où la couleur tient encore, et **le contraste se fait ailleurs** : entre le
sol et les dalles.

**Le vrai fork, et il est de direction artistique :**
- **un sol bleu-violet** — saturé, mais plafonné vers 55 de luminance ;
- **un sol chaud** (l'orange de Signal) — qui peut monter à 100 **et** rester saturé, avec les
  dalles en bleu et violet dessus.
La cible « 90 à 110 » n'est atteignable qu'avec le second.

### CE QUI N'EST PAS FAIT
- La cible de luminance n'est pas atteinte, et **on sait maintenant pourquoi** — ce n'est ni la
  densité (mesuré : +47 % de touffes = rien) ni la rampe seule, c'est **la teinte du sol**.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits — c'est là
  qu'est le « donne envie de toucher », et ça ne se voit pas sur une planche fixe.

---

## ⚑ LE SOL UNIFORME, LES ÎLES SONT DE VRAIES DALLES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### CE QUE TOM A DIT
> *« ça doit être uniforme de base, et des dalles de Promi dans leur design et couleur de
> lorsqu'ils ont été créés (ça s'ancre et ne rechange pas, donc diversité de design de dalles
> sur la surface de la sphère). Là ce sont des pois ronds qui correspondent à rien. »*

### DEUX CORRECTIFS, ET LE SECOND EST STRUCTUREL

**1 · LE SOL EST UNIFORME.** J'avais mis trois tons répartis par un champ basse fréquence,
pour éviter l'aplat. **C'était une erreur de lecture :** ce qui doit donner la variété, ce sont
**les dalles**, pas le fond. Un fond à zones fait un camouflage, et les dalles s'y perdent.
Une seule teinte — c'est le relief de la fourrure qui la fait vivre.

**2 · UNE ÎLE EST UNE VRAIE DALLE, DANS LE MONDE DE SA PLANTATION.**
Une île n'est pas une tache de couleur : c'est **le Promi**, avec le design et la couleur qu'il
avait le jour où on l'a planté. **Ça s'ancre et ça ne rechange plus** — c'est la règle du §4 de
CLAUDE.md, « une dalle est figée à sa plantation ». D'où une **diversité de designs à la
surface de la même sphère** : une encre à côté d'une braille à côté d'une gravure.
Le moteur les peint lui-même, une par une, via `Toile.dalleGeneree`, **dans une vraie cellule
de Voronoï** — un rond « ne correspond à rien », une dalle a le contour de sa cellule.

```
la cellule    on rabote un grand carre par les bissectrices de voisines jitterees,
              une graine par ile : chaque dalle a sa propre forme
le monde      tire par ile parmi les huit — c'est ca, la diversite
la pose       la dalle est posee A PLAT dans le plan tangent de son ile, comme
              un ecusson. Au-dela de ~0,3 rad la projection s'etirerait ;
              une ile fait 0,215, on reste dedans.
le pas        la trame se lit AGRANDIE (mag 2,2) : un poil fait 6 a 10 px, un
              carreau de mosaique 11. A l'echelle naturelle le poil l'ecrase —
              c'est la collision d'echelles payee tout au long du chantier.
l'epi         chaque ile garde son peignage propre : sur un vrai pelage, deux
              plages se distinguent par LE SENS DU POIL autant que par la couleur.
```

### MESURÉ
```
zero ile     luminance 38 a 40      cout 10 a 25 ms selon le cadre
trente iles  luminance 40 a 43
```

### CE QUI N'EST PAS FAIT
- **La luminance reste très sous la cible** (38-43 contre 90-110), et on sait où c'est bloqué :
  **dans la rampe de couleur, pas dans la densité** — densifier de 47 % n'avait rien donné.
- **La première île se lit mal** : elle tombe près du Noyau et sa dalle est sombre.
- Plusieurs dalles restent peu contrastées sur le sol violet — les mondes creux (gravure,
  sillons) surtout.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚑ AFFINER LES TOUFFES, DISTINGUER LES ÎLES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`
> Sauvegarde : `sauvegardes/pelote-fourrure/`

### CE QUE TOM A DIT
> *« on ne distingue pas les dalles, et ça ne paraît pas assez doux, faut affiner les touffes »*

### TROIS CORRECTIFS
**1 · SIX BRINS, DEUX FOIS PLUS FINS.** La douceur d'une fourrure ne vient pas de sa longueur,
elle vient de la **finesse** et du **nombre** : c'est le recouvrement de brins qu'on ne
distingue plus qui fait le soyeux. À quatre brins épais on lisait encore chaque trait.
Épaisseur `e×0,19 → e×0,115`. Le coût est faible : deux brins de plus sur la **même racine**
ne paient que leurs pixels, et ils en paient moins puisqu'ils sont plus fins.

**2 · CHAQUE ÎLE A SON ÉPI.** C'est le séparateur le plus fort qu'on ait, et il ne coûte rien.
Sur un vrai pelage, deux plages ne se distinguent pas que par la couleur : elles se
distinguent par **le sens du poil**. Une spirale centrée sur l'île sépare deux îles voisines
même de teintes proches, et elle accroche la lumière rasante autrement que le sol.

**3 · DES CLARTÉS ÉCHELONNÉES POUR LES ÎLES.** Le lilas (208·176·255) et le periwinkle
sortaient presque **blancs** : leur clarté d'origine est trop haute pour servir d'île sur un
sol déjà clair, et deux îles voisines devenaient indistinctes. On garde la **teinte** de la
palette — c'est elle qui lie la Pelote au Studio — et on impose des **clartés échelonnées**,
toutes écartées du sol. La teinte dit laquelle ; la clarté garantit qu'on les sépare.

### ⚑ CE QUI NE PAIE RIEN — MESURÉ, NE PAS Y REVENIR
Affiner a coûté **cinq points de luminance** (44,4 → 39,5) : des brins plus minces couvrent
moins. J'ai cru compenser en densifiant — **190 000 → 280 000 touffes, +47 % de calcul** — et
la luminance est sortie à **38,6, c'est-à-dire RIEN**. La couverture était déjà saturée :
**ce qui plafonne la clarté n'est pas le nombre de poils, c'est LA RAMPE** (le sol part de
0,46 de clarté et les deux dernières marches sont réservées aux reflets). Retour à 190 000.
**La clarté se traitera dans la couleur, jamais dans la densité.**

### MESURÉ
```
                luminance   saturation
zero ile           38,6        0,46
cinq iles          42,6        0,42
trente iles        40,4        0,42
cout              10 a 24 ms selon le cadre
```

### CE QUI N'EST PAS FAIT
- **La luminance reste très sous la cible** (39 à 43 contre 90 à 110) et **on sait maintenant
  où elle est bloquée** : dans la rampe, pas dans la matière. C'est le prochain chantier.
- Une des quatre couleurs d'île sort **kaki** (l'orange à clarté haute perd sa saturation).
- La clairière du Noyau se lit encore comme un anneau sombre.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚑ CHANGEMENT DE PARTI · LA FOURRURE D'ABORD, LES ÎLES DEDANS · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> **`AUDIT-PELOTE.md` corrigé sur quatre points** (ancienne version :
> `sauvegardes/AUDIT-PELOTE-avant-fourrure.md`).
> Nouveau document : **`PLANCHE-FOURRURE.html`** + `scratchpad/_o_*.js`.
> `PLANCHE-PAVAGE.html` et `PELOTE-REFERENCE` restent intacts.

### CE QUI SORT DE L'AUDIT
1. **« C'est vraiment la Toile de l'utilisateur, vérifié au pixel »** — retiré des acquis.
   Un pavage **partitionne** : sa beauté est fonction de sa densité. À une dalle c'est une
   sphère unie ; il ne devient beau que vers vingt ou trente. Une Pelote neuve doit être belle
   **dès le premier jour**. La bonne géométrie est l'inverse.
2. **« Le rayon dit la date de la dernière parole tenue »** — retiré. C'était **un compte à
   rebours dessiné en rond et pointé vers une personne**. Le rayon encode désormais le
   **cumul** ; rien ne recule jamais.
3. **Le peigné devient une mécanique**, pas un effet : l'objet garde la trace de la main.
4. **Monter en chroma, pas en luminance** ; la palette vient du Studio.

### LES TROIS BUGS DE CE LOT, TOUS MESURÉS
- **Les poils étaient restés courts.** Ils avaient été ramenés à 3,1 px pour ne pas étaler la
  trame d'une dalle — **et il n'y a plus de trame**. Une île fait 0,2 rad, cent fois un poil.
  Retour à 6 / 8 / 10,4, et le semis divisé par deux puisque chaque poil couvre trois fois plus.
- **Le centre de la grappe donné en coordonnées d'OBJET — troisième fois.** La vue est tournée
  de 2,9 rad : la grappe tombait **derrière** la boule, et les états à une et cinq îles étaient
  identiques au vide. On l'écrit dans le repère de la vue puis on le ramène — comme le foyer
  du semis, comme l'empreinte. **L'audit §4 le prescrivait déjà.**
- **Zéro île en donnait une.** La première était posée avant la boucle : l'état « vide » et
  l'état « une » avaient la même luminance à la décimale près.

### ⚑ ET UN PELAGE N'A PAS UNE COULEUR, IL EN A TROIS
Un sol d'une seule teinte sort en aplat violet : on lit du bruit coloré, pas de la fourrure.
Trois tons de la **même famille**, répartis par un champ basse fréquence, suffisent — c'est
la lumière rasante qui fait le reste.

### MESURÉ
```
                 luminance   saturation      (cible : 90-110 de luminance)
zero ile            44,4        0,50
cinq iles           51,9        0,43
trente iles         62,6        0,32
avant ce lot        28,8        --
cout               10 a 22 ms selon le cadre
```

### CE QUI N'EST PAS FAIT — et je ne le maquille pas
- **La luminance reste sous la cible** (44 à 63 contre 90 à 110). L'objet a doublé de clarté,
  il n'a pas atteint le but.
- **Deux couleurs de la palette Signal lisent presque blanc** (le lilas 208·176·255 et le
  periwinkle) : leur clarté d'origine est trop haute pour servir d'île sur un sol clair.
  Il faudra les **rabattre en clarté** pour les îles, ou choisir les couleurs d'île autrement.
- **La clairière du Noyau se lit encore comme un anneau sombre**, pas comme une matière qui
  s'écarte.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚠ J'AI LIVRÉ HUIT FOIS LA MÊME IMAGE — le bug, et la règle qui en sort · 9 septembre 2026

> **`app.html` inchangé** · **la référence `PELOTE-REFERENCE` n'est pas touchée**
> Variations : `PLANCHE-SEXY.html` + `scratchpad/_s_*.js` · `sauvegardes/pelote-variations/`

### CE QUE TOM A VU AVANT MOI
> *« tu m'as mis plusieurs fois les mêmes images, je vois pas les différences. »*

**Mesuré : les huit cadres étaient identiques AU PIXEL PRÈS.** `cadre()` recopie à la main
les options qu'elle connaît — et rien d'autre. Mes réglages de variation (`velours`, `contre`,
`duvet`, `grade`, `dresse`) n'arrivaient donc **jamais** au peintre. J'ai livré huit fois le
témoin en le présentant comme six propositions.

> ### ⚑ LA RÈGLE QUI EN SORT
> **Quand on ajoute une option à un peintre, on vérifie que deux réglages différents donnent
> deux IMAGES différentes — en comptant les pixels, avant de livrer.**
> Un cadre qui ne bouge pas est un cadre qui ne prouve rien. Le contrôle tient en trois lignes
> (`ImageChops.difference`) et il aurait économisé une livraison entière.

### APRÈS CORRECTIF — l'écart au témoin, mesuré
```
B lustre de fibre   10,7 %      E + grading          15,7 %
C + contre-jour     13,0 %      F tout, pousse       19,7 %
D + limbe duveteux  13,4 %      G les Promi dresses  18,6 %   H pousse  21,1 %
```

### PLUS FOURNI — et ce que ça coûte
Reproche de Tom : *« faut densifier un peu les poils, dans mosaïque ou braille ça fait un peu
peu fourni. »* Juste : sur une trame creuse, la matière ne couvre que la moitié d'une cellule
et le fond se voit entre les marques. **330 000 → 520 000 touffes.**
```
330 000 touffes   22 ms      520 000 touffes   31 a 35 ms
```
**La densité se paie plein pot** — c'est un arbitrage, pas un progrès gratuit. La référence
reste à 330 000 ; seules les variations sont à 520 000.

---

## ⚑ LA RÉFÉRENCE EST FIGÉE — et les variations vivent à part · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> **RÉFÉRENCE : `sauvegardes/PELOTE-REFERENCE/`** — code, images, et un `LISEZ-MOI.md`
> qui dit pourquoi elle fait foi. *« enfin c'est correct merci. on garde ceci comme
> référence désormais. »* — Tom, 9 septembre 2026.
> **`PLANCHE-PAVAGE.html` reste la référence et n'est plus touchée.**
> Les variations vivent dans **`PLANCHE-SEXY.html`** + modules `scratchpad/_s_*.js`
> (copies indépendantes). Sauvegarde : `sauvegardes/pelote-variations/`.

### CE QUI EST CONSTRUIT ET RENDU — huit cadres, une chose à la fois
```
A  la reference                    le temoin
B  + le lustre de fibre            Kajiya-Kay : la clarte suit le SENS DU POIL
C  + le contre-jour                le lisere de pointes translucides au limbe
D  + le limbe duveteux             au bord le poil est vu de profil, donc plus long
E  + le grading                    cle chaude / ombre froide, cuit dans la rampe
F  tout, pousse a 150 %            pour voir ou est le trop
G  LES PROMI TENUS SE DRESSENT     le pelage d'une dalle plantee est plus long
H  le relief, pousse
```

### ⚑ LES DEUX IDÉES QUI COMPTENT, ET POURQUOI
**1 · LE LUSTRE DE FIBRE.** Un velours ne se lit pas à sa couleur, il se lit à son
**anisotropie**. Un poil est un cylindre : il ne renvoie pas dans une direction mais sur un
**cône** — le reflet n'est donc pas une tache, c'est une **bande perpendiculaire au peignage**,
et elle **glisse quand la boule tourne**. C'est la propriété qui rend un velours hypnotique,
et on avait la direction du poil sous la main : elle servait à orienter le tampon dix lignes
plus bas. ⚠ Aucune tache spéculaire n'apparaît — le terme ne dépend que du **sens** du poil,
donc la règle du §6 de l'audit tient.

**2 · LES PROMI TENUS SE DRESSENT.** C'est la proposition que je défends, et elle n'est pas
technique : elle est **éditoriale**. Sur la Toile, 58 % des cellules sont grises. Enroulées
telles quelles, ça donne *un globe gris avec des confettis* — le sujet disparaît. Ici le
pelage d'une dalle plantée est **plus long** : elle se tient plus haut que le fond, la lumière
rasante l'accroche, sa silhouette déborde sur le gris. Ni sa couleur ni son dessin ne changent
— on lui donne du **relief**. **Ce qu'on a tenu est littéralement ce qu'on touche.**
⚠ Et aucune information de cellule n'est nécessaire : sur la Toile un fond est **gris**
(saturation quasi nulle) et une dalle porte une couleur de palette. La **saturation** suffit
à les distinguer, teinte par teinte, une fois pour toutes. Coût : un cran de taille de tampon.

### CE QUI EST PROPOSÉ MAIS PAS CONSTRUIT
- **la mémoire du toucher** — l'empreinte se relève en ~1,2 s avec un léger dépassement, et le
  pelage peigné reste peigné puis se redresse. C'est ce qui transforme un toucher en jeu ;
- **l'inertie et le retard du pelage** — la boule file après une chiquenaude, la fourrure
  traîne de quelques degrés et rattrape. Rien ne dit « vivant » comme un mouvement secondaire ;
- **la naissance d'un Promi** — la boule tourne pour amener la cellule devant, le pelage
  **pousse** depuis son centre en 700 ms avec un bref éclat. C'est le moment de récompense ;
- **le souffle** — au repos, ±0,5 % de rayon sur quatre secondes ;
- **le Noyau dans le pelage** — la fourrure s'écarte autour de lui et il jette une ombre douce
  dedans, au lieu d'être posé dessus.

---

## ⚑ LOT 11 · ON N'ASSEMBLE PLUS RIEN — LA TOILE EST ENROULÉE · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Ajout dans la **copie** du moteur : `Toile.toilePleine`. Planche : `PLANCHE-PAVAGE.html`
> Sauvegarde : `sauvegardes/pelote-lot11/`

### CE QUE TOM A DIT, ET CE QUE JE FAISAIS DE TRAVERS DEPUIS LE DÉBUT
> *« on veut la vraie Toile enveloppée en sphère, mise fluffy. Là je vois bien que c'est des
> images de dalles découpées mises fluffy. »*

**Il a raison, et c'était structurel : je FABRIQUAIS des dalles et je les ASSEMBLAIS.** Même
peintes par le moteur, même dans leur vraie cellule, même avec la bonne phase — ça reste un
montage, et un montage se voit. Dix lots à améliorer un assemblage, alors que le problème
était l'assemblage lui-même.

### ⚑ LE RENVERSEMENT : UNE TOILE, PEINTE EN UNE FOIS, PUIS ENROULÉE
```
1 · `Toile.toilePleine` peint UNE Toile complete, a la densite de l'app
    (cellules de 72 px), assez grande pour couvrir la sphere : 1054 x 1054.
    C'est le moteur, son semis, son pavage, sa grille, ses contours, ses espaces.
2 · chaque poil va lire SA COULEUR DEDANS, a l'endroit ou il se trouve.
```
Plus de dalle à fabriquer, à choisir, à mettre à l'échelle, à raccorder. **Il n'y a plus
qu'un seul dessin**, et c'est celui du moteur.

**Pourquoi `toilePleine` et pas `preview` :** `preview` impose sa densité (`base = pw/5,5`,
soit toujours cinq ou six cellules de large). Pour couvrir une sphère il faut une **grande**
Toile **avec des cellules de la taille de celles de l'app**. Même mécanique, densité demandée.

**La projection : Lambert azimutale équivalente**, `k = √(2/(1+z))`, `u = kx`, `v = ky`.
Elle envoie la sphère (aire 4π) sur un disque de rayon 2 (aire 4π) : **elle conserve les
aires** — une dalle occupe sur la boule la place qu'elle occupe sur la Toile. ⚠ Aucune
projection ne conserve *aussi* les formes (Gauss) : vers le limbe les cellules s'étirent.
C'est ce que fait une image collée sur une balle.

### TROIS BUGS PAYÉS
- **Le point de fuite tombait sur la face visible.** Lambert n'a pas de défaut à son centre,
  elle en a un à **l'antipode**, où toute la Toile se rassemble en un point. Centrée sur
  `(0,0,1)` alors que la vue regarde ailleurs : un tourbillon en plein milieu. On la centre
  sur la direction de la vue — le défaut passe derrière, où rien n'est peint.
- **Le semis était encore dimensionné pour des dalles trouées.** On semait à l'inverse du
  remplissage (400 000 à 800 000 candidats) parce que la plupart tombaient dans le vide. Or
  la Toile enroulée couvre **tout** : chaque candidat peint. **531 000 touffes, 67,6 ms.**
- **La boule sortait plus sombre que la Toile qu'elle enroule** — le gros des poils
  atterrissait dans la moitié basse de la rampe. Recentré.

### CE QUE ÇA COÛTE — et c'est enfin dans le budget
```
                   avant ce lot   apres, 155k touffes   apres, 330k (livre)
hero     cadre 620     28,4 ms          11,7 ms              22,0 ms
m-gravure cadre 470    67,6 ms          10,6 ms              20,1 ms
```
On a repris la moitié du budget gagné **en définition** : à 155 000 touffes de 3,7 px la
couverture n'était que de 3,8 fois et le poil étalait sa couleur sur un carreau de 11 px.
À 330 000 touffes de 3,1 px, la couverture est de onze fois et un poil vaut un quart de carreau.

### CE QUI N'EST PAS FAIT, ET JE NE LE MAQUILLE PAS
- **La boule reste plus sombre et moins saturée que la Toile source.** La moyenne d'un pelage
  éteint toujours un peu ce qu'il recouvre. C'est le chapitre « lumière », pas encore ouvert.
- **La fourrure est devenue un velours ras** (3,1 px). C'est le prix du dessin exact : un poil
  plus long étale la couleur de sa racine et brouille un carreau de 11 px. Le compromis est
  réglable d'un chiffre, et c'est un arbitrage produit.
- 22 ms au grand cadre : au-dessus des 16,5 ms du plafond, à re-mesurer à la taille de l'app.
- `toilePleine` sème avec `Math.random` : **la Toile enroulée n'est pas déterministe** entre
  deux ouvertures. Dans l'app ce sera la Toile de l'utilisateur, donc la question ne se pose
  pas de la même façon — mais sur la planche, si.

---

## ⚑ LOT 10 · UNE SEULE GRILLE POUR TOUTE LA BOULE — la Toile, enfin · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/pelote-lot10/`

### CE QUE TOM A MONTRÉ
Une sphère `mosaique`, et : *« tu vois bien que tu ne prends pas des vrais designs de dalles
avec l'espace de la Toile. Tant que tu ne fais pas le reflet d'une Toile en fluffy, c'est mort. »*
**Deux fautes, toutes deux structurelles.**

### ⚑ 1 · CHAQUE CELLULE REDÉMARRAIT SA GRILLE À ZÉRO
Les trames du moteur sont ancrées sur des coordonnées **absolues** — pois tous les 9,
tesselles tous les 11, carrés tous les 5, sillons tous les 6. Sur la Toile il n'y a donc
**qu'une seule grille pour tout le canevas**, et une frontière de dalle n'est qu'un
**changement de couleur dessus**.
En peignant chaque cellule dans son propre canevas, la grille repartait de l'origine de ce
canevas : les carreaux ne tombaient plus en face d'une cellule à l'autre, et **le raccord se
voyait partout**. `dalleGeneree` prend maintenant une **phase**, et décale son origine d'un
multiple de la période — l'idiome que `dalleTrame` portait déjà.
**La phase globale** se prend dans une paramétrisation dont le gradient suit le repère tangent
commun (est / nord) : `longitude × cos(latitude)` vers l'est, `latitude` vers le nord.
⚠ Aucune paramétrisation ne peut être exacte partout — **c'est Gauss, la sphère n'est pas
développable.** Elle l'est **au premier ordre entre deux cellules voisines**, et c'est tout ce
qu'il faut pour que le raccord ne se voie pas.

### ⚑ 2 · LE FILET NOIR N'EXISTE PAS SUR LA TOILE
On posait **0,017 rad** de joint, « comme entre deux dalles de la Toile ». Or **il n'y en a
aucun** : les cellules y sont jointives, et l'espace qu'on voit est **la gouttière de la trame
elle-même** (2 px sur 11 en mosaïque, le vide entre deux pois en braille). Ce joint ajoutait
**4,5 px de noir à l'écran autour de chaque dalle** — c'est lui qui faisait lire des plaques
séparées au lieu d'une Toile. Ramené à 0,0035 rad, un cheveu.

### CE QU'ON VOIT MAINTENANT
```
braille   une seule grille de pois sur toute la boule, la couleur change par dalle
pixel     des aplats jointifs a bord d'escalier, aucun vide entre eux
mosaique  une seule grille de carreaux, la gouttiere du motif pour seul espace
sillons   des ondes continues d'un bout a l'autre
gravure   l'angle propre de chaque dalle — c'est le moteur qui le veut (`s.ang`)
```

### CE QUE ÇA COÛTE
```
hero      cadre 620   15,9 ms      m-encre   cadre 470   13,0 ms
m-pixel   cadre 470   28,4 ms      m-gravure cadre 470   28,0 ms
```
`pixel` et `gravure` sont les plus chers : leurs cellules sont désormais **pleines de matière
sur toute la boule**, il n'y a plus de vide à ne pas peindre. C'est le prix du dessin complet,
et il n'est pas encore rentré dans le budget des 60 im/s à la taille de l'app.

### CE QUI N'EST PAS FAIT
- **Le coût de `pixel` et `gravure` (28 ms) est au-dessus du budget.** À traiter.
- `encre` et `touffe` restent les mondes les plus clairsemés — leur nature sur la Toile aussi.
- La lumière et les couleurs d'ensemble : toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 9 · UNE DALLE PAR CELLULE — le dernier « à peu près » saute · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/pelote-lot9/`

### LE DÉFAUT QUI RESTAIT, ET IL ÉTAIT SIMPLE À NOMMER
**Vingt dalles pour soixante-dix-sept cellules.** Chaque forme revenait quatre fois, et
**aucune n'était la cellule qu'elle occupait** : on posait une dalle étrangère, mise à
l'échelle, dans un contour qui n'était pas le sien. Désormais le moteur peint, **pour chaque
cellule, une dalle dans le contour exact de cette cellule-là**. Plus de répétition, plus de
mise à l'échelle par cellule, plus de contour d'emprunt.

### ⚠ LA CELLULE NE SE DEVINE PAS, ELLE SE MESURE
L'attribution du semis est `acos(p·s) − w` : **ce n'est pas un Voronoï ordinaire**, et un
polygone reconstruit sans les poids rate le bord de **12 % du rayon**. On lance donc 24 rayons
depuis la graine et on cherche par dichotomie l'angle où l'attribution **bascule**. C'est la
vraie frontière, celle que la fourrure utilise. (`_p_semis.js` publie ses poids pour ça.)

### TROIS BUGS PAYÉS, TOUS MESURÉS AU COMPTEUR DE TOUFFES PEINTES
- **Pixels CSS contre pixels réels.** `dalleGeneree` rend un canevas de `dw × DPR` : un radian
  y vaut `PXR × DPR` pixels. Sans ce facteur l'échantillon tombait deux fois trop loin, hors
  de la dalle — **100 000 touffes peintes → 9 500**.
- **L'espacement pris sur la Toile de l'app, pas sur la cellule.** Les trois mondes libres
  dimensionnent leur marque sur `sp` ; en lui laissant 59 px alors qu'une cellule de sphère en
  fait 45, les lobes débordaient si loin que les voisines les recouvraient — **146 000 → 8 800**.
- **La graine cible peinte EN PREMIER.** `Renc`, `Rterr` et `Rtouf` peignent graine par graine
  et la dernière recouvre : toutes les voisines passaient donc par-dessus la cible. Sur la
  Toile, une graine est **au milieu** de la liste. Remise à sa place : encre **46 000 → 68 900**,
  touffe **31 700 → 59 100**, terrazzo **61 500 → 91 500**.

### CE QUE ÇA COÛTE — encore un gain
```
                    lot 6      lot 8      ce lot
hero      cadre 620  22,8 ms   19,4 ms    15,4 ms
m-encre   cadre 470  18,7 ms   15,7 ms    12,5 ms
```
(`m-pixel` et `m-gravure` remontent à ~25 ms : leurs cellules sont désormais pleines de
matière sur toute la boule, donc il y a plus à peindre. C'est le prix du dessin complet.)
Le coût de **construction** monte, lui : 77 dalles générées par monde, deux rendus chacune.

### CE QUI N'EST PAS FAIT
- **`encre` et `touffe` restent les mondes les plus clairsemés** — c'est leur nature sur la
  Toile aussi, mais sur une sphère ça se voit plus.
- La lumière et les couleurs d'ensemble : toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 8 · LA TOILE, EN SPHÈRE — le vrai dessin, à 100 % · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié avant et après).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/pelote-lot8/`

### CE QUE TOM A DIT
> *« mets des vrais designs de dalles. Là c'est des formes à peu près ressemblantes si on les
> connaît, mais c'est 10 % du vrai design, on veut 100 %. Ne livre pas si ce n'est pas ça. »*

Le générateur du lot 7 était fidèle (±4,5 points, mesuré). **La perte était dans le peintre**,
et il y en avait quatre.

### LES QUATRE PERTES, ET CE QU'ON A MESURÉ À CHAQUE FOIS

**1 · Le peintre JETAIT les vraies couleurs.** Il ne gardait qu'un écart de clarté reporté sur
la couleur de la *cellule*. Tout ce que le dessin a de propre disparaissait : le liseré crème
et le cœur orange d'une fleur de `touffe`, les recouvrements de lobes d'une `encre`, les
éclats d'un `terrazzo`, le liant d'une `mosaique`. `bat_trames` relevait pourtant déjà les
**96 teintes réellement peintes** du monde. On bâtit la rampe sur celles-là : **chaque poil
porte exactement la couleur que le moteur a posée sous sa racine.**

**2 · Toutes les cellules d'un monde à trame prenaient LA MÊME dalle-source** (celle au plus
grand rectangle inscrit) — c'était possible tant que la couleur venait de la cellule. Avec la
vraie couleur, ça rendait la sphère monochrome. Chaque cellule retire sa propre dalle.

**3 · Le contour venait du PAVAGE, pas de la dalle.** Les cinq trames lisaient leur *rectangle
inscrit* en rabattant l'échantillon sur son bord : la silhouette était un polygone sphérique
et le motif un bout d'intérieur recadré. **C'était ça, « à peu près ressemblant ».**
⚠ Ce correctif avait déjà été tenté au lot 5 et **retiré**, parce qu'il vidait la sphère.
Il est tenable **maintenant, et seulement maintenant**, parce que les cellules non plantées
portent le gris de la Toile : la boule reste pleine pendant que chaque dalle retrouve son bord.

**4 · L'échelle venait de la BOÎTE DU DESSIN, pas de la cellule.** Une dalle de `touffe` a des
tiges qui descendent d'une demi-cellule : sa boîte vaut le double de sa cellule, et caler
cette boîte-là divisait ses fleurs par deux — elles sortaient en mouchetis. On transporte donc
**le polygone et la graine** avec la dalle, et c'est d'eux que vient l'échelle.

**5 · Une cellule vide perdait le dessin.** Peinte en gris uni, elle n'avait plus ni liseré ni
cœur, et les trois quarts de la boule étaient nus. Sur la Toile, une cellule sans Promi porte
**exactement la même trame, seulement sombre**. Elle la porte maintenant.

### ⚠ UNE ERREUR QUE J'AI FAITE, ET CORRIGÉE PAR LA MESURE
J'ai d'abord accusé le **grossissement** de la trame (`mag` 2,7) d'être la cause du « 10 % ».
Je l'ai ramené à 1 — et **la grille de mosaïque a disparu** : à pas réel, une cellule montre
une vingtaine de carreaux là où la Toile en montre 5 à 7, et le motif devient du bruit. **Le
grossissement était juste ; c'est le contour qui ne l'était pas.** Remis à 2,7.

### CE QUE ÇA COÛTE — et c'est un GAIN
```
                    AVANT (lot 6)   APRES (ce lot)
hero      cadre 620     22,8 ms        19,4 ms
m-encre   cadre 470     18,7 ms        15,7 ms
m-pixel   cadre 470     25,7 ms        20,9 ms
m-gravure cadre 470     17,5 ms        18,9 ms
```
Les poils ont raccourci (le tiers du pas lu) et couvrent moins de pixels chacun.

### CE QUI N'EST PAS FAIT
- **`touffe` reste le monde le plus maigre.** Ce n'est pas un défaut du portage : sa dalle
  couvre 11 % de sa cellule sur la Toile aussi. Mais sur une sphère ça se voit plus.
- La lumière et les couleurs d'ensemble ne sont toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 7 · LE MOTEUR GÉNÈRE LA DALLE — plus aucun prélèvement · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié avant et après).
> Ajout dans **`scratchpad/toile-extrait.js`** (la COPIE du moteur, jamais l'app) :
> `Toile.dalleGeneree`. Rien n'y est réécrit — c'est un ajout.
> Sauvegarde : `sauvegardes/pelote-lot7/`

### CE QUE TOM A DEMANDÉ
> *« mets les VRAIES dalles aux vrais designs, contours, variations de teintes, pas
> superposées, pas des photos de la Toile détourées encadrées ça jamais — tu as le code de la
> Toile qui génère des dalles donc fais les vraies »*

Il a raison sur le fond : **tout ce qu'on avait PRÉLEVAIT dans une Toile déjà peinte.**
`dalleTrame` coupe les marques en deux ; l'extraction par la couleur rendait des marques
entières mais restait un tri dans une image.

### ⚑ LA CLÉ — ON FABRIQUE LA CELLULE AVEC DES GRAINES, PAS AVEC UN DÉCOUPAGE
La cellule d'une graine est l'intersection des demi-plans de ses bissectrices. Donc, **pour
qu'une graine ait exactement le polygone voulu, il suffit de poser une voisine EN MIROIR de
chaque côté** : la bissectrice entre les deux *est* ce côté. Le moteur décide alors lui-même,
avec sa propre règle, quelle marque appartient à qui — et **une marque reste entière**.
Vérifié numériquement (`scratchpad/probe_poly.py`) : les cellules sont **convexes**, et
**100 %** des points du polygone ont bien la graine cible pour plus proche, sur huit cellules.

### ⚑ ET LA DALLE SE SÉPARE DE SON FOND PAR DIFFÉRENCE DE DEUX RENDUS
Dernier prélèvement supprimé. On peint **deux fois le même jeu de graines, au même instant**,
et on ne change **qu'une** chose : la graine cible redevient grise. Tout ce qui diffère
appartient à cette dalle — **son liseré d'encre et son cœur orange compris**. C'est ce qui
règle `touffe`, dont une fleur porte trois couleurs et que tout tri par teinte mutilait.
⚠ Il faut le **même** jeu de graines (`mk()` tire au sort gray/tone/shade/ang/ph) et le
**même** instant (`cOf` dépend de `now`), sinon la différence est du bruit.

### ⚑ ET L'ESPACEMENT DE LA TOILE, POUR LES TROIS MONDES LIBRES
`Renc`, `Rterr`, `Rtouf` dimensionnent leur marque sur `sp = √(W·H / nb de graines)`. Dans un
canevas de dalle, ni `W·H` ni le nombre de graines n'ont à voir avec ceux de la Toile : les
marques sortaient **beaucoup** trop petites. On truque `W` et `H` pour que `sp` retrouve sa
valeur — l'idiome que `dalleTrame` porte déjà. ⚠ **Uniquement pour eux** : `Rpix` et `Rmos`
*bouclent* sur `W` et `H`.

### LA PREUVE, MESURÉE (`scratchpad/probe_gen2.py`)
Part de matière **dans la même cellule**, sur la Toile / générée, **critère identique des deux
côtés** (une première mesure comparait « la couleur exacte de la dalle » d'un côté et « tout ce
qui est coloré » de l'autre : elle mentait de 20 points sur `touffe`).
```
encre    -4,5      mosaique +0,7     touffe   -3,8     braille  -2,6
pixel    -2,1      terrazzo +3,7     gravure  +1,4     sillons  -0,2
```
**Les huit mondes à ±4,5 points.** Et chaque dalle sort **seule, sur fond transparent** :
rien ne se superpose.

### LES BATTERIES — toutes vertes, `app.html` non modifié
```
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18
redteam_demande 19/19 · redteam_toile 17/17 · redteam_geste 13/13 · redteam_verbe 6/6
redteam_filets 0 parasite · redteam_vide 61/61 · redteam_air 428 paires intactes
redteam_champ 32/32 · redteam_polices 0 couple absent
releve-design : AUCUN ECART
```

### CE QUI N'EST PAS FAIT
- La sphère reste **sombre**. La lumière et les couleurs ne sont pas traitées.
- Le coût par image n'a pas été re-mesuré après ce lot (la génération est un coût de
  CONSTRUCTION, pas de rendu — mais ce n'est pas vérifié).
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 6 · UNE BOULE QU'ON A ENVIE D'ÉCRASER · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · modules `_p_{peint,moteur,planche}.js`
> Sauvegardes : `sauvegardes/pelote-lot6/` (avant) · `pelote-lot6-livre/` (après)

### QUATRE CHOSES BRIDAIENT LE FLUFFY, ET DEUX ÉTAIENT ÉCRITES DANS LE CODE

**1 · Le poil RACCOURCISSAIT au bord de sa cellule** — deux crans, avec le commentaire
*« et le contour reste net : à pleine taille il déborde et rend la dalle floue »*. Mais un
bord net, c'est exactement ce qui fait une découpe. **Une fourrure se lit surtout au bord**,
quand les mèches passent par-dessus le vide. On garde la pleine longueur jusqu'au filet et on
ne raccourcit plus qu'au tout dernier rang — juste assez pour que le vide reste lisible.

**2 · Des brins, pas des mèches.** `TAI0` passe de `[4,2 · 5,6 · 7,2]` à `[5,6 · 7,5 · 9,7]`,
et le brin lui-même de `1,75·e` à `2,05·e` avec **un quart de courbure en plus** : les pointes
se rabattent et se croisent, et c'est ce croisement qui fait « mou » à l'œil.

**3 · Les grands vides noirs n'étaient PAS le joint.** Le joint vaut 0,017 rad, soit ~4,5 px à
l'écran ; les vides faisaient 20 à 40 px. C'étaient **les cellules non plantées, qui ne
peignaient rien**. Or l'audit §2 rejette déjà *« une majorité de cellules vides : la silhouette
se creuse, ce n'est plus une boule »* — et la vraie Toile ne fait pas ça : ses cellules sans
Promi sont **sombres mais pleines de matière**. On ajoute donc une teinte à la rampe — le gris
de la Toile — et les cellules vides la portent, **avec leur trame**. La boule redevient
continue et ronde ; le joint reste le seul vide.

**4 · Moins de touffes, puisqu'elles couvrent plus.** 155 000 → 118 000. C'est **la longueur
qui fait la masse, pas le nombre.**

### CE QUE ÇA COÛTE — MESURÉ, PAS ESTIMÉ (`scratchpad/cap_ms.py`, sphère en rotation)
```
                        AVANT      APRES brut   APRES avec le sol allege
hero      cadre 620      22,8 ms     36,7 ms      28,9 ms
m-encre   cadre 470      18,7 ms     28,5 ms      22,4 ms
m-pixel   cadre 470      25,7 ms     38,0 ms      30,8 ms
m-gravure cadre 470      17,5 ms     35,0 ms      28,4 ms
```
Le sol gris se paie : il a fait passer l'image de 22,8 à 36,7 ms. Comme il est **sombre et
sans motif à lire**, il n'a besoin ni de la densité d'une dalle ni de sa longueur : **une
racine sur deux, et un cran plus court**. On récupère les deux tiers du surcoût.

> ### ⚠ ET LE COÛT NE DÉPEND PRESQUE PAS DE LA TAILLE DU CADRE
> Un cadre de 470 px coûte parfois **plus** qu'un de 620 (`m-pixel` 30,8 contre `hero` 28,9).
> Ce n'est pas une anomalie : **c'est le nombre de touffes qui domine, pas les pixels** — le
> banc le disait déjà (*« un poil coûte 0,108 µs dont seulement 0,042 de pixels »*). Corollaire
> qui invalide un raccourci tentant : **on ne peut PAS extrapoler le coût à 390 px en divisant
> par le rapport des surfaces.** Il faudra le mesurer à 390.

### CE QUE JE NE MAQUILLE PAS
- **Le lot coûte +27 % par image** (22,8 → 28,9 sur le grand cadre). C'est le prix du fluffy
  demandé ; ce n'est pas gratuit et je ne le présente pas comme tel.
- **Les 60 images par seconde ne sont PAS vérifiées à la taille de l'app.** Les plafonds de
  l'audit §5 ont été mesurés à 390 px avec un autre grain : ils ne couvrent plus cet état.
- La sphère reste **sombre**. « Belle lumière générale, belles couleurs » n'est toujours pas
  traité — c'est le prochain sujet.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit) ne sont revus.

---

## ⚑ LOT 5 · LES VRAIES DALLES DANS LA FOURRURE — et un correctif que j'ai dû retirer · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** (celle de la fourrure, revenue en service)
> Modules touchés : `scratchpad/_f_dalle.js`, `_p_trame.js` · `_p_peint.js` **rétabli à l'identique**
> Sauvegardes : `sauvegardes/pelote-lot5/` (avant) · `sauvegardes/pelote-lot5-livre/` (après)

### ⚠ CE QUE J'AI CASSÉ, ET POURQUOI JE LE NOTE EN PREMIER
Tom a envoyé **deux** images : un gros plan d'une dalle `pixel` au bord sale, et une sphère
`touffe` — en disant *« t'es hyper loin de là où on en était en terme de fluffy, c'est une
grosse régression »*.
**J'ai cru que la première visait la silhouette de la sphère.** Elle visait le **bord de la
dalle plate**. J'ai donc changé `_p_peint.js` pour que la silhouette d'une cellule vienne de
la dalle et non du pavage. Résultat mesuré, avant/après au même cadre : la sphère `touffe`
est passée d'une boule fournie à **des lambeaux** — une trame est vide à 60-80 %, donc la
fourrure ne poussait plus que sur un quart de la surface.
**`_p_peint.js` est rétabli à l'identique depuis la sauvegarde.** Rien de ce correctif ne
subsiste. *(Une tentative de compensation par « silhouette fermée + trou de trame plus
sombre » est également retirée : elle rendait la masse mais éteignait la boule.)*
> **Leçon, et elle est générale :** quand une capture montre un défaut, **identifier l'écran
> d'où elle vient avant de corriger**. J'ai corrigé la sphère pour un défaut de la planche plate.

### CE QUI EST LIVRÉ, ET QUI EST PROUVÉ
**1 · La source des dalles ne passe plus par `dalleTrame`.** Elle coupe les marques en deux
(mesuré, `scratchpad/verite.html`) : demi-points de braille, demi-carreaux de mosaïque, et
l'escalier de `pixel` remplacé par un polygone lisse. `_p_trame.js` prend maintenant
**`DallesDeMonde()`** : marques entières, bord net.

**2 · Sans attendre, et sans toucher à l'app.** `Toile.preview(cv,monde,w,h)` peint
**synchroniquement** (elle appelle `RD[theme]` en ligne) et publie ses graines dans `cv.__c`.
Prélever sur la Toile vivante aurait imposé d'attendre la frame suivante — or `bat_trames`
est synchrone : on aurait lu **l'ancien monde**, sans la moindre erreur. C'est le piège du §8,
en pire. `agrandit()` n'est plus appelée : on ne redimensionne plus la Toile de l'app.

**3 · Le bord se lit par PROJECTION, plus par une bande de tolérance.** La bande gardait, à
alpha partiel, les pixels d'antialiasing **du voisin** — d'où le liseré mauve sale le long de
l'escalier, exactement ce que Tom a montré. Un pixel de bord est un **mélange** entre la
couleur de la dalle et le fond : on projette sur le segment `[fond → dalle]`, la part donne
l'alpha, et **le reste dit avec quoi le mélange se faisait**. Mélangé à une autre dalle, le
reste est élevé : rejeté, net. Vérifié à la loupe ×8 sur pixel, mosaïque et braille.

**4 · Les mondes LIBRE gardent tout ce qui n'est pas le fond.** Une fleur de `touffe` porte
**trois** couleurs (pétale, liseré d'encre, cœur orange) : triée par teinte, elle perd son
contour et son cœur — mesuré, la sphère `touffe` maigrissait. Pour encre, terrazzo et touffe
on garde donc tout ce qui n'est pas le fond, et **la graine la plus proche** dit à qui la
marque appartient — la règle du moteur.

### CE QUE JE NE MAQUILLE PAS
- **Le fluffy est REVENU à son niveau, il n'a pas augmenté.** Avant/après au même cadre :
  équivalent sur les huit mondes. Ce lot corrige la matière source, il n'ajoute pas de fourrure.
- La sphère reste sombre. « Belle lumière générale, belles couleurs » n'est pas traité ici.
- Ni limbe, ni doigt, ni les six ne sont revus.

---

## ⚑ LOT 4 · LE POLYGONE COUPAIT LES MARQUES EN DEUX — les vraies dalles, mesurées · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · sonde : **`scratchpad/verite.html`**
> Modules : `scratchpad/_f_dalle.js` (neuf) · `_f_planche.js` (réécrit)
> Sauvegarde : `sauvegardes/dalles-lot4/`

### CE QUE TOM A DIT
> *« le velours ça marche pas, et c'est encore des screenshots de dalles dans un cadre.
> Tu en mets dans encre et touffe je crois (pas sûr) mais tous les autres c'est archi faux. »*

**Il avait raison, et sur les huit mondes exactement.** Je ne l'ai pas pris à l'estime : j'ai
construit une sonde (`scratchpad/verite.html`) qui confronte, monde par monde, la dalle que je
sortais à **la même dalle prélevée sur la Toile peinte**.

### LE MÉCANISME, MESURÉ
```
encre · touffe · terrazzo    elles coincident.     (les mondes LIBRE du moteur)
mosaique · braille · pixel   elles ne coincident PAS,
gravure · sillons            et toujours de la meme facon.
```
`dalleTrame` refait l'attribution **pixel par pixel** et efface l'alpha des pixels hors
cellule. Il **coupe donc les marques en deux** : demi-points de braille, demi-carreaux de
mosaïque, hachures tranchées net. Et sur `pixel`, **l'escalier de 5 px — la signature du
monde — disparaît** au profit d'un polygone lisse.
Sur la vraie Toile c'est l'inverse : chaque marque appartient à **une** graine et se peint
**entière**. Le bord d'une dalle y est **quantifié par la trame**, jamais lisse.
**C'était ça, « la capture dans un cadre » : le cadre, c'était ce polygone.**

### LA CORRECTION — ON N'EXTRAIT PLUS PAR LA FORME, MAIS PAR L'APPARTENANCE
Le moteur peint la Toile entière, correctement. On y prélève la dalle par **sa couleur** :
le moteur garantit qu'une dalle colorée n'a jamais la couleur d'une voisine (`cc()` écarte
les couleurs des voisines, `tones()` leurs marches de clarté), donc sa teinte est **unique
dans son voisinage**. On garde ses pixels dans la cellule élargie d'une demi-période de
trame — et **les marques restent entières, coupées exactement où le moteur les a coupées**.
```
aucun redimensionnement · aucun deplacement · aucun redessin · echelle 1, pixel pour pixel
```
⚠ Ce n'est **pas** le rejet capital de l'audit §2 : celui-là vise le fait de prendre l'**image**
d'une dalle pour **découper une autre forme**. Ici on ne découpe rien — on garde ce que le
moteur a peint, tel qu'il l'a peint.

### POURQUOI DEUX CHEMINS, ET PAS UN SEUL
L'extraction par la couleur ne sait garder qu'**une** couleur. Or une marque de `touffe` en
porte **trois** : le pétale à la couleur de la dalle, le liseré à l'encre, le cœur orange.
Prélevée par la couleur, la fleur perd son contour et son cœur — **mesuré** : pétales nus,
ou cœurs orange sans pétales. Ce sont exactement les mondes que le moteur appelle **LIBRE**
(encre, terrazzo, touffe) : ceux dont la marque **déborde** de sa cellule et a donc une forme
propre. Pour eux `dalleTrame` est déjà juste, c'est mesuré. La règle reprend donc **la
distinction que le moteur fait déjà** :
```
LIBRE  encre · terrazzo · touffe                 ->  Toile.dalleTrame  (deja juste)
TRAME  mosaique · braille · pixel · gravure ·    ->  extraction par appartenance
       sillons
```

### LE VELOURS EST RETIRÉ
> *« le velours ça marche pas »*

Supprimé de la planche. `_f_velours.js` est conservé mais **seul `Velours.jour()` reste
utilisé** — la lumière générale, montrée sur sa propre colonne pour qu'elle se refuse d'un
coup d'œil. Les quatre lots de traitement de surface (effilochage, ombre portée, relief,
halo grignoté) sont archivés dans `sauvegardes/fibre-lot{1,2,3}/`.

### CE QUI N'EST PAS FAIT
- **La sphère n'existe toujours pas.** Ni limbe, ni doigt, ni les six.
- Sur la Toile les cellules sont **jointives** : le vide entre dalles (exigence 4) viendra du
  recul des plans bissecteurs sur la sphère, pas d'ici.
- **La matière reste à trouver.** Trois pistes ont été essayées et rejetées par Tom : le brin
  dessiné (cheap), le traitement de surface (détourage), le halo (néon). Ce qui est acquis,
  c'est **ce qu'on ne peut pas faire** : déplacer un pixel de la dalle, l'éclaircir vers le
  blanc, ou lui poser quoi que ce soit d'uniforme.
- L'extraction lit les pixels de la Toile : elle exige que le monde soit **peint** avant
  (setTheme + ~1,5 s). Pour la sphère il faudra un chemin qui ne dépende pas de ce délai.

---

## ⚑ LOT 3 · ON NE DÉPLACE JAMAIS UN PIXEL DE LA DALLE · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · module `scratchpad/_f_velours.js`
> Sauvegarde : `sauvegardes/fibre-lot3/`

### CE QUE TOM A REJETÉ
> *« pas des photos détourées dégueulasses, abandonne et plus jamais ça »*

**Trois gestes du lot 2 fabriquaient ce détourage**, et ils sont supprimés :
1. **L'effilochage.** Il prélevait la couleur à une position **déplacée**. Le contour du
   moteur — net, calculé, exact — en sortait **rongé** : bords mordus, irréguliers, sales.
   C'est littéralement l'aspect d'un mauvais détourage.
2. **L'ombre portée.** Une copie sombre décalée sous la matière fait un **autocollant** posé
   sur le fond, jamais une matière.
3. **Le relief à forte amplitude.** Une pente à 0,78 pose un liseré clair d'un côté, sombre
   de l'autre : encore un contour sale.

### ⚑ LA RÈGLE QUI EN SORT, ET ELLE NE SE NÉGOCIE PLUS
**ON NE DÉPLACE JAMAIS UN PIXEL DE LA DALLE.** Le moteur a calculé ce contour : il est la
vérité. Tout ce qu'on ajoute se met **AUTOUR**, ou module la **CLARTÉ** — jamais la forme.

### LE MONTAGE
```
1 · LE DUVET, AUTOUR       deux halos flous de la dalle, poses DESSOUS. Ils
                           debordent du contour : c'est ce debord qui fait le
                           coton. Le dessin, dessus, reste intact — « fluffy,
                           mais que ca reste lisible ».
2 · LE HALO SE GRIGNOTE    un flou gaussien est UNIFORME : sur fond sombre il
                           ne peut faire qu'une aureole — l'outer glow, la
                           signature du toc. On troue son alpha par un bruit
                           etire dans le sens du poil : chaque meche atteint
                           une distance differente, et il reste du VIDE entre.
3 · LE GALBE               une rondeur douce par marque, lue sur un alpha
                           floute. Sur l'alpha brut la pente vaut 255 sur deux
                           pixels : ca fait un lisere blanc, pas une rondeur.
4 · LA LUMIERE EST A LA SCENE, PAS A LA DALLE
                           posee par dalle, elle se repete a l'identique sur
                           chacune et rien ne se tient. Une seule lumiere
                           traverse toute la composition : `Velours.jour()`,
                           appliquee APRES montage. Plus une montee de
                           saturation qui ne touche pas la teinte.
```
Deux réglages ramenés à zéro parce qu'ils faisaient un néon : le duvet ne s'éclaircit
**plus du tout** (`lift = 0`) — c'est sa **découpe** qui dit la fibre, jamais sa clarté.

### UN MORCEAU DE TOILE — c'est là que la lumière se juge
La planche compose un vrai morceau : les vraies dalles du moteur, à leur place, **le vide
entre elles** (exigence 4), une seule lumière par-dessus. C'est le montage qu'aura la Pelote.
⚠ **Ce qui est approché là, et rien d'autre : la POSITION.** `dalleTrame` recadre au plus
juste et n'expose pas son décalage ; on centre donc chaque dalle sur le centre de sa cellule
(`dalleAbs`). La dalle elle-même — forme, trame, couleurs — est celle du moteur, au pixel.
Une **loupe** est toujours au plus proche, jamais un raster agrandi et lissé.

### CE QUI N'EST PAS FAIT
- **La sphère n'existe toujours pas.** La « belle lumière générale » ne se jugera vraiment
  que sur elle : ici elle est plate.
- Le coût par image n'est pas mesuré. La passe est **par pixel** (deux flous + deux boucles),
  donc les plafonds de l'audit §5, comptés en touffes, **ne s'appliquent pas** — banc à refaire.
- Les mondes creux (gravure, sillons, braille, terrazzo) laissent beaucoup de vide : la
  silhouette de la sphère devra se garantir **au limbe**, ce n'est pas éprouvé.

---

## ⚑ LOT 2 · LA VRAIE DALLE, EN VELOURS — le brin est abandonné · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · module `scratchpad/_f_velours.js`
> Sauvegardes : `sauvegardes/fibre-lot2/` (état livré) · `sauvegardes/fibre-lot1/` (les brins)

### CE QUE TOM A DIT, ET POURQUOI SES DEUX REPROCHES N'EN FONT QU'UN
> *« les poils donnent pas envie de caresser, ça fait cheap visuellement »*
> *« ça doit être les VRAIES dalles »*

En redessinant chaque monde en fibres, le lot 1 produisait **huit approximations** — braille
en étoiles au lieu de points, mosaïque en briques décalées au lieu d'une grille, gravure en
fougères au lieu de hachures, pixel sans son escalier. Et pour que le motif survive, il
fallait des brins **assez gros pour se voir un par un** : c'est précisément ce qui fait cheap.
**À cette échelle, une vraie soie ne montre aucun poil.** Les deux reproches ont la même cause.

### LE RENVERSEMENT
```
1 · LE MOTEUR PEINT LA VRAIE DALLE   Toile.dalleTrame(cv,pid,1,{m,p,h})
    vraie trame, vrai pas, vraie couleur, vraies strates, vraie cellule ponderee.
    Aucune approximation n'est POSSIBLE : c'est lui. On ne redessine plus rien.
2 · LA MATIERE EST UN TRAITEMENT DE SURFACE, jamais un poil trace
    · l'effilochage du bord, anisotrope, a la plus fine periode representable
    · le grain couche dans le sens du peignage
    · les plages claires et sombres du velours froisse
    · le RELIEF de chaque marque, lu sur un alpha floute
    · l'ombre portee, pour que la matiere ne soit pas collee au fond
```
**Aucun brin n'est jamais tracé — on ne peut donc plus en distinguer un.**

⚠ **Ce n'est pas le rejet capital de l'audit §2.** Ce qui est abandonné à tout jamais, c'est
de prendre l'**image** d'une dalle pour **découper une autre forme** — des fausses dalles
détourées. Ici la dalle n'est ni redimensionnée, ni détourée, ni déplacée : le moteur la peint
dans **sa** cellule, et on ne touche qu'à la surface. Le contour reste celui qu'il a calculé.

### LA PREUVE QUE CE SONT LES VRAIES DALLES (`scratchpad/probe_dalle.py`)
Le taux de remplissage rendu par `dalleTrame`, comparé au relevé de référence `pav/_trames.png` :
```
                rendu        reference
encre    65 %          67-73 %
pixel    63 %          50-73 %
terrazzo 60 %          37-54 %
touffe   43 %          35-51 %
mosaique 42 %          34-49 %
braille  27 %          21-32 %
sillons  27 %          21-30 %
gravure  25 %          21-29 %
```

### LES CINQ DÉFAUTS PAYÉS DANS CE LOT, ET LEUR CAUSE RÉELLE
- **Le treillis gaufré** (encre, pixel). Ce n'était pas la grille du bruit de valeur : c'était
  un **repliement de spectre**. J'avais ajouté deux octaves *plus hautes* pour casser le
  réseau ; à ×4,41 en travers leur période tombait à 0,26 px de cellule, sous
  l'échantillonnage — et une fréquence qu'on ne peut pas représenter **se replie**, en moiré
  large. **La règle : la plus fine octave est celle du pixel, on casse le réseau PAR LE BAS.**
- **Toute la dalle assombrie de 17 %.** Le lustre venait du produit fibre·lumière. Le cône du
  peignage étant centré sur 0,33 rad et la lumière sur −2,15, ce produit valait −0,79
  **partout** : un assombrissement global sans la moindre variation. Les plages viennent
  maintenant d'un champ scalaire à part, centré sur 1.
- **Un filtre posé sur une forme plate.** Le grain était là, mais rien ne se soulevait. Il
  manquait **le relief** — la pente de la matière, éclairée d'un côté.
- **Le liseré blanc.** La pente lue sur l'alpha **brut** vaut 255 sur deux pixels : le bord
  sortait en liseré blanc et la couleur se lavait. On la lit sur un alpha **flouté** : la
  marque devient un bourrelet et la lumière la parcourt en entier.
- **Le terrazzo lavé.** Un plafond de clarté **en facteur** traite le lilas comme l'encre.
  Le plafond est maintenant **en niveau de canal** (242 sur le canal le plus haut) : aucun
  écrêtage, donc teinte et saturation exactes quelle que soit la couleur de la palette.
- **L'effilochage en paquets.** Un bruit isotrope de 1,8 px donne des touffes de 1,8 px de
  large : on lit des paquets, pas des fibres. Il est maintenant pris **dans le repère du
  peignage** — 1,1 px de cellule en travers (2,2 px réels, la plus fine période
  représentable), 3,5 px dans le sens.

### CE QUI N'EST PAS FAIT, ET CE QUE JE NE MAQUILLE PAS
- **Ça rend un feutre / un velours brodé, pas une fourrure longue.** C'est la conséquence
  directe du renversement : la fourrure longue exigeait des brins visibles, et les brins
  visibles sont ce que Tom a appelé cheap. **C'est un arbitrage à trancher, pas un réglage.**
- **La sphère n'existe toujours pas.** Planche plate. Ni limbe, ni doigt, ni les six.
- Le coût par image n'est pas mesuré sur une sphère animée : la passe est **par pixel**, pas
  par poil, donc les plafonds de l'audit §5 (comptés en touffes) **ne s'appliquent plus** —
  il faudra un nouveau banc.
- L'approche « un brin dessiné » est archivée dans `sauvegardes/fibre-lot1/` avec son module
  `_f_fibre.js`. Elle garde une chose juste : chaque monde SAIT donner une loi d'implantation.

---

## ⚑ LOT 1 · LA FIBRE EST LE TRAIT DU MONDE — le parti pris change · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · modules `scratchpad/_f_{fibre,planche}.js`
> Sauvegarde : `sauvegardes/fibre-lot1/`

### LE PARTI PRIS, EN UNE PHRASE
**On ne pose pas de fourrure SUR un dessin : on DESSINE AVEC la fourrure.** Chaque monde du
Studio ne donne plus une image à recouvrir, il donne une **loi d'implantation** — où une
touffe pousse, dans quel sens elle est peignée, quelle marche de clarté elle porte.

### CE QUE ÇA DÉBLOQUE
Le mur des dix derniers tours était une **collision d'échelles** : un poil fait 6 px, un motif
du moteur a un pas de 5 à 11 px. Poil plus petit, il ne se voit pas ; poil plus grand, il
écrase le motif. **Ici il n'y a plus deux grains** : le poil EST la marque du monde. Une
hachure de gravure n'est plus une ligne qu'on duvette — c'est une rangée de fibres couchées,
du **velours côtelé**. Le produit le pensait déjà : un des huit mondes s'appelle **touffe**,
et ses fleurs sont déjà des rosettes de fibres.

```
encre     peluche froissee     mosaique  tapisserie a carreaux
touffe    fleurs en faisceaux  braille   tapis a points (chenille)
pixel     peluche rase         terrazzo  velours froisse en plaques
gravure   velours cotele       sillons   soie moiree
```

Les pas viennent des peintres du moteur **à la lettre** (`Rpix` STEP 5, `Rbra` DOT 9, `Rsil`
SP 6 / AMP 4,5 / WL 0,018, `Rgra` HS 8, `Rmos` T 11, `Renc` 9 ellipses rayon 0,6·sp, `Rterr`
7 tessons, `Rtouf` 3-5 fleurs). Les strates sont `LITS=[0,0.10,0.04,0.14,0.07]`, la loi de
`PALL()`. **Rien n'est inventé : seule la marque change.**

### LES QUATRE DÉFAUTS PAYÉS DANS CE LOT, ET LEUR CAUSE RÉELLE

- **La bogue de châtaigne.** Pas 2,4 · longueur 6,5 · trois brins : un poil couvrait trois
  pas et **se lisait tout seul**. Une fourrure ne se lit jamais brin par brin. Pas 1,05,
  longueur 3,0, **cinq** brins serrés à 0,20 : le recouvrement fait le soyeux, pas la longueur.
- **La dalle plate et pâle** (encre, pixel, deux fois). La longueur d'onde du champ de
  peignage était réglée **à l'échelle de l'écran** : le champ ne tournait pas dans une cellule
  de 67 px, le lustre devenait constant, la dalle sortait en aplat lavé. **La longueur d'onde
  se compte en CELLULES** — ~2,5 tourbillons en travers d'une cellule.
- **Les araignées noires.** Ni un poil noir ni une ombre : **le FOND qui se voit**. Un champ
  de gradient a des points critiques ; la direction y fait un tour complet, les touffes
  s'éventent en rosette et laissent un trou. On ne les rattrape pas une par une : un **biais
  constant plus long que le gradient** (1,35 > 1) enferme la direction dans un cône de ±47°
  et le champ n'a plus de point critique.
- **La feuille d'érable** (touffe) et **le pâté** (terrazzo). Les pétales fondaient faute du
  liseré d'encre : le `_tfStroke(ink)` du moteur est rendu en **fibres crème posées en
  dernier**. Les sept tessons fondaient faute de gouttière : on les **rétrécit de 14 %** vers
  leur centre.

### CE QUI EST MESURÉ (`scratchpad/compte_fibre.py`, pas supposé)

```
touffes par cellule de 67 px     encre 2963 · pixel 3304 · touffe 2547 · mosaique 1978
                                 terrazzo 1269 · braille 924 · sillons 717 · gravure 508
                                 moyenne 1776
sur la sphere, 30 cellules de face (audit §5)
   monde moyen                    53 000 touffes   266 000 poils
   pire monde (pixel)             99 000 touffes   496 000 poils
   plafond mesure (audit §5)     125 000 touffes   500 000 poils a 16,5 ms
```
**Le pire monde tient, à la limite.** Rien n'a été remesuré : ce sont les plafonds de l'audit.

### CE QUI N'EST PAS FAIT — et je ne le maquille pas
- **La sphère n'existe pas dans ce lot.** C'est une planche PLATE : elle prouve la loi
  d'implantation, elle ne prouve ni la boule, ni le limbe, ni le doigt, ni les six.
- Le mariage avec `_q_cellule.js` (le vrai polygone sphérique) n'est pas fait.
- **Terrazzo, gravure, sillons et braille sont clairsemés** par la loi du moteur elle-même.
  Sur une sphère, la silhouette risque de se trouer. La parade acquise est **au limbe**
  (§6 de l'audit) — elle n'est pas encore éprouvée sur un monde creux.
- La question du §7 de l'audit (les six disques DEDANS ou DESSUS) reste **ouverte**.

---

## ⚑ L'AUDIT EST RÉÉCRIT — passation vers un chat neuf · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> **`AUDIT-PELOTE.md` est réécrit en entier** et fait foi. L'ancien est dans
> `sauvegardes/AUDIT-PELOTE-avant-8sept.md`.

**Ce que le nouvel audit ajoute par rapport à celui du 6 septembre :**

- **Un rejet capital et définitif** — on ne découpe plus jamais un raster de dalle pour en
  faire une forme. Avec **le signe qui permet de le reconnaître** : si un défaut résiste à
  trois corrections et qu'en le réparant un autre apparaît ailleurs, ce n'est pas un réglage,
  c'est l'architecture.
- **Ce que Tom demande, dans ses mots**, rassemblé des dix derniers échanges — y compris ce
  qu'il n'avait jamais eu à préciser (§3).
- **Seize bugs payés** au lieu de huit, dont quatre neufs et coûteux : `Toile_resize` lit le
  parent, le bouchon `cc()` doit rendre un index, le cache HTTP, la boucle de rejet du semis.
- **Dix règles de dessin** payées cher, écrites une par une (§6).
- **Les mesures**, avec **ce qui paie et ce qui ne paie rien** — pour qu'on ne refasse pas
  quatre optimisations sans effet (§5).
- **Ce que j'ai mal fait** (§9), pour que le prochain ne le refasse pas.
- **Le prompt de reprise** (§10), qui autorise explicitement à **repenser** l'approche.

**L'état livré :** la version avec les poils (`PLANCHE-PAVAGE.html`, modules `_p_*`) est en
service. La branche « le moteur peint lui-même » est écartée mais gardée entière dans
`sauvegardes/pelote-dalles-8sept/` — **son calcul du vrai polygone d'une cellule
(`_q_cellule.js`) est bon et doit être réutilisé.**

---

## ⚑ RETOUR À LA VERSION AVEC LES POILS · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> **La version en service est de nouveau `PLANCHE-PAVAGE.html`** (moteur `scratchpad/_p_*.js`).

**Décision Tom : on revient à la version avec les poils, avec ses erreurs.** Les cinq modules
`_p_*` n'avaient pas été touchés depuis la sauvegarde du 6 septembre — vérifié par `diff`,
**identiques octet pour octet** à `sauvegardes/pelote-6sept/`. Rien à reconstruire : la planche
est simplement re-horodatée et re-rendue.

```
77 cellules · 76 000 a 162 000 touffes selon le monde · les six et le Noyau en place
```

**La branche « le moteur peint lui-même »** (cellules en vrai polygone, dalle dessinée par
`Toile.dalleTrame`, fourrure par-dessus) est mise de côté **entière** dans
`sauvegardes/pelote-dalles-8sept/` — `PLANCHE-PELOTE-DALLES.html` + `_q_*.js`. Elle reste
servie et consultable ; elle n'est plus la version de travail.

**Ce qu'on garde de cette branche, même écartée** — et c'est écrit dans les mémoires du projet :
le contour d'une dalle **est** sa cellule de Voronoï ; le bouchon `cc()` doit rendre un **index**
de palette (c'est lui qui privait la Pelote de ses couleurs) ; une tache spéculaire fait un
plastique, un velours est **rétro-réflectif**.

---

## ⚑ ARTY ET FLUFFY — la dalle ne se voit plus, elle colore les poils · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PELOTE-DALLES.html`** · `scratchpad/_q_{cellule,peint,planche}.js`

### ⚑ LE MONTAGE QUI TIENT LES DEUX

```
1 · LE MOTEUR PEINT LES DALLES sur un calque SOURCE — jamais a l'ecran
    dans le VRAI polygone de chaque cellule (Voronoi spherique, coins arrondis)
2 · LA FOURRURE EST TOUT CE QU'ON VOIT : chaque touffe prend la couleur du pixel
    qu'elle recouvre. Donc la vraie forme de la dalle, la vraie teinte du Studio,
    et le clair-obscur de sa trame — SANS QU'UN SEUL APLAT PLAT N'APPARAISSE.
3 · LE JOINT reste vide : c'est le recul des plans bissecteurs (0,020 rad).
4 · TOUTES les cellules portent leur dalle — c'est ce qui fait la BOULE.
```

**C'est le point 2 qui fait le fluffy** : il n'y a plus de surface lisse nulle part.

### ⚠ TROIS RÉGLAGES QUI DÉCIDENT DE TOUT

- **L'éclaircissement de la pointe.** À 0,30 + 0,42·z, la pointe montait à 72 % vers le blanc
  et **toute la palette se lavait en beige**. Ramené à 0,05 + 0,19·z : c'est le **liseré du
  limbe** qui donne la lumière, jamais le blanchiment de chaque fibre.
- **La racine doit être dans la matière.** Aller chercher une couleur vers l'intérieur quand la
  racine tombe dans le vide **remplit les joints** et rend tout boueux. Le débord vient des
  touffes enracinées **dans** la dalle — et c'est lui qui fait le halo duveteux du contour.
- **Aucune tache spéculaire.** C'est la signature d'une bille de verre. Le velours est
  **rétro-réflectif** : plus clair au bord, sans point chaud.

### ⚠ CE QUI N'EST PAS FAIT

- **30 à 48 ms par image**, soit 20 à 30 im/s. L'essentiel part dans le `getImageData` /
  `putImageData` sur 3,5 Mo (planche à 470 px ; l'app rendra à 390). **Optimisation à faire.**
- Les **mondes creux** (braille, gravure, sillons) sortent plus maigres : la fourrure ne pousse
  que sur la matière de leur trame, et leur trame est clairsemée.
- L'**empreinte du doigt**, la **dérive** et le **partage** ne sont pas reportés sur ce peintre.

---

## ⚑ LE COTON REVIENT — mais PAR-DESSUS la dalle · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PELOTE-DALLES.html`** · modules `scratchpad/_q_{cellule,peint,planche}.js`

Reproche de Tom sur la version « vraies dalles » : *« c'est mega cheap, on veut nos poils ou
coton doux ».* Il avait raison : en réparant le dessin j'avais jeté la matière, et le résultat
était du **plastique** — une bille de verre à tache spéculaire.

### ⚑ LE BON MONTAGE : LA FIBRE NE PORTE PAS LE DESSIN, ELLE LE RECOUVRE

C'est ce qui débloque la contradiction des dix derniers tours. **Tant que chaque poil devait
dire « ici il y a de la matière du motif », il fallait qu'il soit aussi petit que le motif — et
il l'écrasait.** Maintenant :

```
1 · LE MOTEUR PEINT LA DALLE   dans le vrai polygone de la cellule, a l'echelle 1
2 · LA FOURRURE SE POSE DESSUS et PREND LA COULEUR DU PIXEL DE SA RACINE,
    eclaircie vers sa pointe
```

La fibre n'a plus rien à dire du motif : elle le duvette. Elle peut donc être **fine, courte,
dense**, et **déborder** — et c'est ce débord qui fait le coton.

### ⚑ UN VELOURS, PAS UN PLASTIQUE

Le dégradé radial avec **tache spéculaire blanche** est la signature d'une bille de verre.
Le velours et le coton font l'inverse : leur réflexion est **rétro-réflective** — plus clairs
**au bord**, là où les fibres se voient de profil, et la lumière y tombe sans point chaud.
Ambiant large, clé très molle, **liseré de duvet** au limbe.

### ⚠ DEUX BUGS DANS LA PASSE DE FOURRURE

1. **Je comparais l'alpha sur une image OPAQUE.** `if(al > alpha du fond)` — le fond vaut 255
   partout, le test échouait toujours, **la passe tournait vingt millisecondes en n'écrivant
   rien**. Corrigé en peignant la fourrure sur **sa propre couche transparente**, où la
   comparaison d'alpha redevient valide, et en fondant **une seule fois** au `drawImage`.
2. **La fourrure poussait DANS les joints.** Quand la racine tombait sur le vide, j'allais
   rechercher une couleur vers l'intérieur : le joint se remplissait et tout devenait boueux.
   **Une touffe ne pousse que si sa racine est dans la matière** ; c'est en s'étendant qu'elle
   passe par-dessus le joint et par-dessus la silhouette.

### ⚠ CE QUI N'EST PAS FAIT, ET JE NE LE MAQUILLE PAS

- **33 à 55 ms par image** — soit 20 à 30 images par seconde, pas 60. L'essentiel part dans le
  `getImageData` / `putImageData` sur 3,5 Mo (la planche rend à 470 px ; l'app rendra à 390).
  **Une passe d'optimisation est nécessaire** et elle n'est pas faite.
- **Les joints restent durs.** Le débord adoucit le bord extérieur des dalles, pas le fond du
  joint.
- L'**empreinte du doigt**, la **dérive** et le **partage** ne sont pas encore reportés sur ce
  peintre.

---

## ⚑ LE PEINTRE EST REFAIT — LE MOTEUR DESSINE LUI-MÊME · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Nouvelle planche : **`PLANCHE-PELOTE-DALLES.html`**
> Modules : `scratchpad/_q_{cellule,peint,planche}.js` · l'ancien état est dans
> `sauvegardes/pelote-6sept/`

### ⚠ POURQUOI ON A REPRIS DE ZÉRO — et j'aurais dû le voir dix tours plus tôt

L'ancienne chaîne était : **raster d'une dalle → nuage de points → tampon de poil**. Trois
approximations empilées, et une **contradiction insoluble** :

```
un poil fait 6 px · un motif du moteur a un pas de 5 a 11 px
   poil plus petit que le motif   -> il l'ecrase (pixel illisible, encre en pates)
   motif agrandi pour le sauver   -> une cellule n'en montre plus qu'un ou deux,
                                     et LE MOTIF CESSE D'ETRE UN MOTIF
```

À l'échelle d'une dalle de 67 px, **il n'y a pas de place pour un grain de fourrure entre les
deux**. Aucun réglage n'en sort. Je répondais par des réglages depuis cinq tours.

### ⚑ CE QUE FAIT LE NOUVEAU PEINTRE

1. **Le vrai polygone de chaque cellule**, en sommets : on part d'une calotte large et on la
   rabote par chaque bissectrice (Sutherland-Hodgman sur la sphère). C'est le contour **exact**,
   pas une frontière devinée point par point. `inset` recule chaque plan — c'est le filet.
2. **On projette, on découpe dessus** (coins arrondis, comme le moteur arrondit ses dalles).
3. **`Toile.dalleTrame` peint dedans, à l'échelle 1.** Vrai pas de motif, vraies couleurs,
   vraies strates — parce que c'est le moteur qui peint.
4. **L'ombrage par-dessus, en un seul geste** : un dégradé continu (clé haut-gauche,
   remplissage bas-droite, liseré au limbe). Pas de quantification, donc pas de bandes.

```
COUT : 51 cellules, 2 a 3,5 ms par image — contre 15 ms pour 150 000 tampons.
Le budget n'est plus le sujet.
```

### ⚠ ET UN BUG QUI DATAIT DU PREMIER JOUR

Le bouchon de planche `function cc(){return [200,180,255];}`. Le moteur fait
`s.ci=cc(s); s.c=PAL[s.ci]` : **`cc` rend un INDEX de palette, pas une couleur.** Mon bouchon
rendait un tableau, `PAL[tableau]` valait `undefined`, et **toutes les dalles retombaient sur le
même mauve**. C'est ce bouchon — pas le moteur — qui privait la Pelote de la palette du Studio
depuis le début. Il rend maintenant un index tiré de la position de la graine, donc stable.

### Où en est chaque monde

Les huit sont lisibles et reconnaissables : encre en aplats francs, mosaïque en tesselles,
**touffe en vraies marguerites avec tiges et cœurs orange**, braille en grille de pois, pixel en
blocs, terrazzo en éclats, gravure en stries par dalle, sillons en ondes.

### Ce qui n'est PAS fait

- **La fourrure n'est plus là.** Elle redevient un traitement de surface à poser par-dessus des
  dalles justes, au lieu d'être ce qui portait le dessin. C'est le prochain lot.
- L'**empreinte du doigt**, la **dérive**, le **partage** : à reporter sur le nouveau peintre.
- L'ancien état complet est dans `sauvegardes/pelote-6sept/` — rien n'est perdu.

---

## ⚑ LE POIL ÉTAIT AUSSI GROS QUE LE MOTIF · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`**

Reproche de Tom : *« pixel illisible et mal fait, terrazzo encre illisibles aussi ça fait des
pâtés »*, et *« ça ne suit pas les contours des designs de dalles »*. Trois causes distinctes,
et je les avais confondues en une seule.

### ⚑ 1 · LE POIL DÉTRUISAIT LE MOTIF QU'IL DEVAIT DESSINER

Les trames du moteur ont des pas de **5 à 11 pixels** — carrés tous les 5, pois tous les 9,
tesselles tous les 11, sillons tous les 6. Un poil en fait **5 à 8**. À l'échelle naturelle,
**le grain est aussi gros que le détail qu'il doit peindre** : il l'écrase. D'où « pixel
illisible » et « des pâtés ».

**On lit donc la trame AGRANDIE** (×2,7) : ses détails passent à 15-30 px, franchement plus gros
que le grain, et une cellule montre trois à cinq périodes — comme une dalle de Toile qu'on
regarde de près. C'est un écart assumé au 1:1, et c'est la légibilité qui le commande.

### ⚑ 2 · UNE DALLE A UNE COULEUR, ET DES STRATES DEDANS

Le moteur ne peint pas une dalle d'un seul aplat : `PALL()` donne **une** couleur de palette
déclinée en cinq éclats, et c'est ce qui fait les strates d'une encre ou d'un terrazzo.
Je ne gardais que « matière ou vide » : les dalles sortaient en pâtés.

La trame livre maintenant **deux choses** : la matière, et de combien chaque pixel est plus
clair ou plus sombre que la médiane de son monde. Ce clair-obscur se reporte **en marches** sur
la couleur de la cellule. Les strates reviennent, et la palette du Studio ne se disperse pas.

⚠ **Et il doit rester DISCRET.** À vingt-six marches par unité de clarté, une strate claire
sautait de sept marches d'un coup — droit dans la partie qui déteint vers la crème — et **toute
la sphère se lavait de blanc**. Trois marches au plus : une strate nuance une dalle, elle ne la
repeint pas.

### ⚑ 3 · LE DESSIN DE « PIXEL » EST DANS SON CONTOUR, PAS DANS SON INTÉRIEUR

Une dalle *pixel* est **pleine** (73 % de remplissage) : ce qui la rend reconnaissable, c'est
que **son bord est calé sur une grille de cinq pixels**. Je cherchais son motif à l'intérieur —
il n'y en a pas — et elle sortait en polygone lisse, illisible. On quantifie donc la **position
qui sert à décider de la cellule** : le bord devient escalier.

### ⚑ 4 · ET LE CONTOUR RESTE NET

Un poil poussé à pleine taille **déborde du bord de sa cellule** et rend la dalle floue. On garde
donc la distance au bord (l'écart au deuxième site) et **le poil raccourcit en s'en approchant** :
deux crans sur les quarante derniers pour-cent. Une dalle a un contour franc.

### Où en est chaque monde

```
ENCRE      des blobs organiques, strates internes visibles
MOSAIQUE   une grille de tesselles, joints nets
TOUFFE     des fleurs entieres, reconnaissables
BRAILLE    de gros pois
PIXEL      un contour en escalier — son dessin
TERRAZZO   des eclats irreguliers
GRAVURE    des stries epaisses, un angle PAR DALLE
SILLONS    des ondes
```

### Ce qui reste ouvert

- **« Les six DEDANS »** attend toujours ton arbitrage (cinquième fois).
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.
- Le **×2,7 sur la trame** est un écart au 1:1 de la Toile, assumé pour la lisibilité : c'est un
  seul nombre si tu veux le rapprocher.

---

## ⚑ DE VRAIES DALLES, AVEC LEURS VRAIS CONTOURS · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`**

Reproche de Tom : *« c'est pas des vraies dalles avec leurs vrais contours, du coup y'a plein
d'erreurs »*. Il avait raison, et c'était une **erreur de conception**, pas un réglage.

### ⚠ CE QUE JE FAISAIS, ET POURQUOI C'ÉTAIT FAUX

Je découpais chaque cellule avec **la silhouette d'une IMAGE de dalle mise à l'échelle**. D'où :
des contours étirés, qui ne se raccordent pas d'une cellule à l'autre, des morceaux flottants,
un pavage qui n'en est pas un.

**Or j'avais déjà la vraie chose sous la main.** Une dalle de Toile, c'est **sa cellule de
Voronoï pondéré** — et j'en ai une, vraie, sur la sphère. Il suffisait de m'en servir comme
contour au lieu d'y plaquer une image.

### ⚑ LE CONTOUR SE LIT DANS LE DIAGRAMME, ET LES COINS S'ARRONDISSENT TOUT SEULS

Le bord d'une cellule, c'est l'écart au deuxième site : `d2 − d1`. En dessous du joint, on ne
peint plus. **Et les coins s'arrondissent gratuitement** : près d'un coin on est proche de
**deux** voisins à la fois, donc la somme `exp(−(d2−d1)/r) + exp(−(d3−d1)/r)` franchit le seuil
plus tôt et le coin se trouve rogné. Une intersection **molle** de demi-espaces — c'est la
définition même d'un arrondi, et c'est exactement ce que le moteur fait avec `round`.

### ⚑ ET LA DISTINCTION EST CELLE DU MOTEUR, PAS LA MIENNE

`dalleTrame` la pose noir sur blanc : `LIBRE = (encre || terrazzo || touffe)`.

```
MOSAIQUE · BRAILLE · PIXEL · GRAVURE · SILLONS   leur trame est DECOUPEE sur la cellule
   -> le contour vient du pavage (arrondi aux coins), l'image ne donne que LA MATIERE,
      prise dans son interieur au pas naturel, sans redimensionnement ni repli
ENCRE · TERRAZZO · TOUFFE                        leur dalle DEBORDE de sa cellule
   -> leur vrai contour est celui de LEUR FORME : on garde la silhouette de l'image,
      mise a l'echelle UNIFORMEMENT (la forme n'est jamais deformee)
```

### ⚑ ET SUR UNE TRAME, LA COULEUR VIENT DE LA DALLE, PAS DU MOTIF

Le moteur peint la trame d'une dalle **dans la couleur de cette dalle** : le motif ne dit que
« matière ou vide ». En prenant la couleur dans l'image du motif, j'étais obligé de choisir la
dalle-source **pour sa taille** — donc de tomber toujours sur les deux ou trois mêmes, et la
sphère sortait presque monochrome. Séparer les deux rend la variété de la palette **et** libère
le choix du motif : on prend celui au plus grand intérieur, celui qui ne rabattra jamais.

⚠ **Le rabattement, justement** : quand une cellule dépassait l'intérieur de sa dalle-source, je
rabattais l'échantillon sur son bord — d'où des **traînées radiales** au bord des cellules.

### L'état

```
77 cellules (la taille de dalle mesuree sur la Toile) · jusqu'a 153 700 touffes = 615 000 poils
banc : 161 156 touffes = 644 624 poils a 15,30 ms sur un ecran de 390 px, sphere en rotation
```

### Ce qui reste ouvert

- **« Les six DEDANS »** attend toujours ton arbitrage (quatrième fois) : le dos n'étant plus
  peint, les disques sont posés après la matière.
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ L'ENTRE-DALLES REDEVIENT VIDE, ET LA LUMIÈRE EST REFAITE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`

### ⚑ 1 · LES « BANDES DIAGONALES » ÉTAIENT MES MARCHES

Reproche de Tom : *« mets pas ces bandes diagonales »*. Ce n'était pas la lampe, c'était **la
quantification**. Je faisais tomber l'éclairement sur **sept marches** — et la sphère se
terrassait en bandes.

**J'appliquais à l'OMBRAGE D'UN VOLUME une règle qui vaut pour LA COULEUR D'UNE DALLE.**
« Un aplat franc, jamais un dégradé » décrit une dalle de Toile, pas la lumière qui glisse
dessus. Une dalle garde sa teinte ; son éclairement doit être **continu**. Vingt marches, l'œil
ne les sépare plus.

### ⚑ 2 · UN VRAI ÉCLAIRAGE, À TROIS TERMES

Une seule directionnelle laissait la moitié de la boule dans le noir. On pose ce que pose
n'importe quel éclairage de studio, et pour les mêmes raisons :

```
LA CLE          en haut a gauche, devant — elle sculpte le volume
LE REMPLISSAGE  en bas a droite, plus faible et plus large — il OUVRE l'ombre
                au lieu de la boucher, sans effacer la forme
LE LISERE       au limbe (Fresnel) — il detache la silhouette et affirme le cercle
+ un ambiant franc : la matiere doit se lire PARTOUT
```

⚠ **Et la moyenne doit tomber dans la partie COLORÉE de la rampe.** À `lum × 19` le gros des
poils atterrissait sur les trois dernières marches — celles qui déteignent vers la crème — et
**la palette du Studio disparaissait sous son propre éclairage**. Les hautes marches sont
réservées aux vrais reflets.

### ⚑ 3 · L'ENTRE-DALLES REDEVIENT VIDE — et c'est ce qui a payé la densité

J'avais rempli toute la sphère pour supprimer les trous noirs. Mais avec **les six disques et le
Noyau** par-dessus, ça surcharge. On ne peint donc que la matière des dalles plantées ; le reste
est du vide, et **ce vide est la place du Noyau et des six**.

Effet de bord décisif : **on peut alors SUPPRIMER du semis les points qui ne peignent rien.**
La compaction se fait une fois, avant le tri par plaques — la boucle ne visite plus que de la
matière, et le semis de départ peut être très dense sans que l'image le paie.

```
MESURE, ecran 390 px, sphere EN ROTATION :
   135 122 touffes = 540 488 poils   mediane 12,90 ms   ZERO image > 20 ms sur 144
   161 156 touffes = 644 624 poils   mediane 15,30 ms   25 images > 20 ms
La planche est reglee a ~134 000 touffes = 535 000 poils sur le monde le plus dense.
```

Le semis se dimensionne **par monde**, à l'inverse du remplissage de sa trame : encre en donnait
180 000 tampons quand gravure en donnait 58 000 pour le même semis.

### Ce que je ne fais pas passer pour fait

- **La règle « les six DEDANS »** reste enfreinte, et elle attend toujours ton arbitrage. Le vide
  entre les dalles leur redonne de la place, mais ils sont posés après la matière.
- L'**animation** n'est jugée qu'au chronomètre. Le **partage** n'est pas maquetté. La
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ 440 000 POILS, ET LA SPHÈRE N'EST PLUS NOIRE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`

Reproche de Tom : *« ça paraît noir et vide encore »*. Deux causes distinctes, et je les avais
confondues — la densité, et **les valeurs**.

### ⚑ 1 · CE QUI FAISAIT LE NOIR : LE VIDE DE LA TRAME

Le vide de la trame — l'entre-deux des pois du braille, des stries de la gravure — était peint
à **0,15 de clarté**, et les cellules vides à 0,17. Or sur un monde creux ce vide occupe **les
trois quarts d'une dalle PLANTÉE** : les trois quarts de la sphère étaient donc noirs, même là
où il y avait un Promi. Remontés à **0,26** et **0,30**, et le côté à l'ombre ne s'efface plus
(présence 0,48 au lieu de 0,26).

**Sur la Toile on accepte ce noir parce que c'est un écran plat.** Sur un volume, la matière
doit se voir partout — sinon on ne lit ni le relief ni le pelage.

### ⚑ 2 · LES POILS POUSSENT EN TOUFFES — c'est ça qui a débloqué la densité

La décomposition du banc donnait : un poil coûte **0,108 µs**, dont seulement **0,042 de pixels
écrits**. **Les deux tiers sont le passage dans la boucle** — lectures, rotation, éclairage,
rangement. Donc tant qu'un tampon ne porte qu'un poil, on paie ce passage pour chacun.

**Quatre poils partant de la même racine ne paient qu'UN passage.** Chaque poil supplémentaire
revient à 0,042 µs au lieu de 0,108 — **deux fois et demie moins cher**. Et une fourrure pousse
en touffes, pas en brins isolés : ce n'est pas un artifice, c'est plus juste.

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
    94 987 touffes = 379 948 poils   mediane 14,50 ms   19 images > 20 ms sur 144
   110 010 touffes = 440 040 poils   mediane 16,60 ms   ZERO image > 20 ms      ← retenu
   124 990 touffes = 499 960 poils   mediane 18,70 ms   ZERO image > 20 ms  (53 im/s)
```

**440 040 poils, c'est 3,5 fois les 125 000 du lot précédent.** Trois variantes de touffe pour
qu'on ne reconnaisse pas deux fois le même bouquet.

### Deux gains de plus, mesurés

- **`Math.atan2` par poil.** Il y en avait un, pour orienter le brin — cinquante à cent
  nanosecondes, plus que tout le reste de la boucle. On n'a besoin que d'un secteur sur
  vingt-quatre : le rapport du petit côté sur le grand, une table de 256 entrées, et l'octant
  se rattrape par des comparaisons de signe.
- **La clairière du Noyau se mesure au carré** : une racine de moins par poil.
  Les deux ensemble : **17,10 → 15,30 ms** à 125 000 poils.

### Ce que je ne fais pas passer pour fait

- **La règle « les six DEDANS »** reste enfreinte : le dos n'étant plus peint, les disques
  sont posés après la matière, dans une clairière d'encre. **À confirmer ou à corriger.**
- La sphère est maintenant **assez pâle** dans ses zones vides. C'est le contraire du défaut
  d'avant ; si c'est trop, c'est un seul nombre.
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, et la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ LA FOURRURE VISIBLE DOUBLE, ET 77 DALLES MESURÉES · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`
> Compte des dalles : `scratchpad/compte_dalles.html`

### ⚑ 1 · LE DOS N'EST PLUS NI PEINT NI MÊME VISITÉ

Le banc disait que le coût est **par point visité**, pas par pixel. Or la moitié du semis vit
derrière la sphère, où la fourrure ne se lit pas. Le tester point par point coûtait quatre
produits sur cette moitié.

**Parade : le culling par PLAQUES.** La sphère est découpée en **96 plaques**, les points sont
triés dedans (par une table hauteur × azimut, pas une recherche exhaustive : celle-ci coûtait
96 produits par point, soit quarante millions à la construction), et chaque image ne teste que
**96 directions**. Les plaques tournées vers l'arrière ne sont jamais parcourues.

Et dans la foulée, **tout ce qu'un point porte tient dans une seule bande de mémoire** : la
boucle lisait huit tableaux séparés, elle en lit un seul, de dix flottants par point, contigu.

```
RESULTAT, mesure au banc, ecran 390 px, sphere en rotation :
   125 000 poils TOUS DE FACE   mediane 17,10 ms
   c'etait 125 000 peints dont 62 500 de face — la fourrure QU'ON VOIT a donc DOUBLE
   165 000 de face -> 21,80 ms (46 im/s) · 210 000 -> 27,30 ms
```

⚠ **Ce que je n'ai PAS fait :** doubler le nombre *peint* (250 000). Ça coûte 27 ms, soit
37 images par seconde. Ce qui a doublé, c'est la densité **visible**, à budget égal.

### ⚑ 2 · LE NOMBRE DE DALLES EST MESURÉ, PLUS ESTIMÉ

`scratchpad/compte_dalles.html` plante jusqu'à saturation et compte les cellules.

```
LA TOILE, a 390 x 620 (l'ecran de l'app)   54 cellules -> une dalle de 66,9 x 66,9 px
LA SPHERE, meme ecran                       surface 345 237 px2
   a taille de dalle EGALE il en faut 77   (j'en avais 61)
   dont une trentaine visibles de face — comme un ecran de Toile
```

### ⚑ 3 · LE CONTRASTE — pixel et mosaïque ne se lisaient pas

Leurs aplats tombaient tous dans deux marches voisines. La rampe est élargie
(`DL` de −0,34 à +0,28 au lieu de −0,40/+0,22), la marche s'étale sur toute la rampe
(`lum×5,4−0,55` au lieu de `×4,6−0,30`), et la cellule vide descend (clarté 0,17).

⚠ **Et un vrai bug de couleur :** je dérivais le fond d'une cellule vide de **la première
teinte de la trame**. Sur touffe, la teinte la plus fréquente est le **vert des tiges** — et
toute la sphère virait à l'olive. Sur la Toile, les cellules vides prennent une table de gris
bleutés très sombres, jamais la couleur d'une dalle. On part maintenant de l'encre de l'écran.

### ⚠ CE QUI CHANGE UNE RÈGLE ACQUISE, ET QUI DEMANDE UN ARBITRAGE

**« Les six DEDANS et pas dessus »** ne peut plus tenir telle quelle. Les disques étaient
tramés entre la passe de dos et celle de devant ; le dos n'étant plus peint, ils se sont
retrouvés **sous toute la fourrure et ont disparu**. Je les pose donc **après** la matière,
dans une clairière d'encre qui les fait quand même lire comme posés *dans* le pelage.
**C'est un écart à une règle validée : à confirmer ou à corriger.**

### Ce qui reste ouvert

L'**animation** n'est toujours jugée qu'au chronomètre. Le **partage** n'est pas maquetté.
La **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon. Et il reste une **marge** entre
la dalle et le bord de sa cellule, comblée par le ton sombre : ma cellule sphérique n'a pas la
forme de la dalle qu'elle porte.

---

## ⚑ 125 000 POILS, ET LE PAVAGE ENTIER · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html` + `cap_banc.py`

### ⚑ 1 · SUR LA TOILE IL N'Y A AUCUN TROU

C'est le point que je manquais depuis trois lots. **Le canevas est ENTIÈREMENT pavé.** Ce que
je prenais pour des « écarts noirs entre les dalles », ce sont des **cellules sombres** qui
portent la même trame. Je sautais ces points : la sphère se trouait de noir, ce qui ne
ressemble à rien de la Toile.

**Maintenant tout point peint quelque chose** — la couleur de la dalle là où il y a matière,
le ton sombre de la cellule partout ailleurs. Le joint vaut **zéro**. Effet de bord heureux :
plus aucun point n'est gaspillé.

### ⚑ 2 · UNE CELLULE MONTRE UNE DALLE ENTIÈRE

En n'échantillonnant que le **rectangle inscrit** et en repliant au miroir, je découpais les
motifs : les fleurs de touffe devenaient du moucheté, la gravure des losanges. On pose
maintenant **la dalle complète** dans la cellule — sa silhouette, sa matière, ses couleurs.

⚠ Et le calage se fait sur **l'étendue réellement peinte**, pas sur le canevas : `dalleTrame`
ajoute une marge `pad` qui vaut 0,85 fois l'espacement pour encre, terrazzo et **touffe** (ces
trois-là débordent de leur cellule sur la Toile). En calant le canevas, la dalle se retrouvait
deux fois trop petite et noyée dans du fond — **c'est pour ça que touffe ne se voyait pas.**

Et les cellules sont passées de 213 à **59** : la vraie Toile montre une vingtaine de dalles par
écran, pas cent cinquante. C'est ce qui rend le design lisible.

### ⚑ 3 · 56 400 → 125 000 POILS, ET J'AI CHERCHÉ AU MAUVAIS ENDROIT TROIS FOIS

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
   110 000 poils   mediane 14,80 ms    22 images > 20 ms sur 144
   125 000 poils   mediane 16,50 ms   ZERO image > 20 ms sur 144      ← retenu
   140 000 poils   mediane 18,40 ms     3
   160 000 poils   mediane 20,50 ms   123
```

**Trois hypothèses fausses, mesurées et abandonnées :**
1. **Des poils plus petits.** De 13,9 à 9,7 pixels par poil : 19,7 → 19,2 ms. **2,5 %.** Ce ne
   sont donc pas les pixels écrits.
2. **L'atlas en tableau d'objets.** Mis à plat en deux grands tableaux typés (un départ et un
   compte par tampon) : **aucun gain**. Ce n'étaient pas les déréférencements.
3. **Les `push` sur tableaux ordinaires**, remplacés par des tableaux typés préalloués :
   **aucun gain** non plus.

**La mesure qui a tout dit** — décomposer en trois passes (complet / sans versement / sans
rien) : sur **27,4 ms** à 90 000 poils, le **versement n'en coûtait que 3,3** et la projection
**0,7**. Les **23,4 autres** étaient dans la boucle de déformation.

**Et deux causes, toutes deux évitables :**
- **`Math.pow` et `Math.hypot` par point.** `Math.hypot` fait une mise à l'échelle pour éviter
  les débordements — inutile sur des coordonnées entre −1 et 1 ; `Math.sqrt` va cinq à dix fois
  plus vite. `Math.pow(x, 0,6)` se tabule. **27,4 → 16,0 ms.**
- **La boucle de déformation repassait sur TOUS les points à chaque image**, alors qu'elle est
  **statique** : positions, normales et champ de flux vivent dans le repère de l'objet. Elle ne
  dépendait de la vue que par **l'amorti au limbe** — et celui-là se calcule à la **projection**,
  où la profondeur est déjà connue. Il ne reste par image que **la calotte du contact** : un
  produit scalaire par point pour la trouver, la vraie géométrie pour les quelques milliers qui
  y tombent, et on rend ce qu'on a touché à l'image suivante. **16,0 → 12,7 ms.**

### Ce que je ne fais pas passer pour fait

- Le **calage de la dalle sur la cellule** reste un compromis : ma cellule sphérique n'a pas la
  forme de la dalle qu'elle porte. Il reste une marge, comblée par le ton sombre de la cellule.
- L'**animation** n'est toujours pas jugée à l'œil, seulement chronométrée.
- Le **partage** n'est pas maquetté, et la **profondeur du doigt** n'est prouvée qu'à 10,5 % du
  rayon.

---

## ⚑ LA VRAIE TOILE COMME RÉFÉRENCE — et 56 400 poils · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · référence : `scratchpad/vraie_toile.html` + `cap_toile.py`
> Banc : `scratchpad/banc_poils.html` + `cap_banc.py`

**J'ai enfin capturé la vraie Toile dans les huit mondes, et elle a tranché trois débats d'un
coup.** Je réglais mes écarts et mes motifs à l'estime ; la référence existait, il suffisait de
la rendre.

### ⚑ CE QUE LA VRAIE TOILE DIT, ET QUE JE FAISAIS FAUX

```
1 · LES DALLES SE TOUCHENT.       Il n'y a pas de « joint » : un filet, au plus.
    Ce que je prenais pour des ecarts, ce sont LES CELLULES VIDES.
2 · LA PLUPART DES CELLULES SONT VIDES,   presque noires, et elles portent la MEME
    trame. Les dalles colorees sont une GRAPPE au milieu. Je peignais toutes les
    cellules en couleur : ca faisait un vitrail, pas une Toile.
3 · L'ANCRAGE DU MOTIF DEPEND DU MONDE.   braille (pas 9), mosaique (11), pixel (5)
    et sillons (6) sont ancres sur des coordonnees ABSOLUES : leur motif est CONTINU
    d'une dalle a la suivante. Encre, touffe, terrazzo et gravure portent l'angle
    propre de leur graine (`s.ang`) : chaque dalle a SA direction.
```

Je tournais **toutes** les cellules au hasard : la grille du braille partait dans tous les sens.
Puis **aucune** : la gravure devenait un peigne uniforme. **Les deux étaient faux — c'est par
monde**, et c'est le moteur qui le dit, pas moi.

### ⚑ LES MOTIFS — on n'étire plus, on agrandit la Toile

Les trames sont ancrées sur des **pas absolus**. En étirant chaque dalle pour la faire tenir
dans sa cellule, ce pas devenait quelconque : **c'est pour ça que les motifs ne ressemblaient pas
au design.** Maintenant un radian vaut toujours le même nombre de pixels de trame.

Pour que ça marche il faut de **grandes dalles**. `seedGray()` ne repeuple que si la Toile est
vide : on l'amorce petite (46 cellules), puis on **agrandit le canevas** et `relax()` étale ces
mêmes 46 cellules sur toute la surface. Les dalles passent de **72 à 200-380 px**, au pas absolu
inchangé.
⚠ **J'avais écrit `agrandit()` et je ne l'appelais pas.** Les dalles restaient petites, il
fallait donc replier au miroir pour couvrir une cellule — d'où des **chevrons** très visibles sur
la gravure.

⚠ **Et une préférence bien intentionnée écrasait tout :** j'avais ajouté « prendre la dalle au
plus grand rectangle inscrit » pour éviter les replis. Elle **écrasait le tirage au hachage** :
presque toutes les cellules tombaient sur la même dalle et **la sphère sortait monochrome**.
Supprimée — depuis que les dalles sont grandes, il n'y a plus rien à éviter.

### ⚑ LES POILS — 36 450 → 56 400, et deux optimisations mesurées

Le banc décompose le coût : **1,9 ms de fixe** puis **0,28 µs par poil** (13,9 pixels écrits,
24 ns le pixel — c'est l'**accès dispersé** dans un tampon de 2,4 Mo, pas le calcul).

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
   45 775 poils   mediane 14,40 ms   1 image > 20 ms sur 144
   56 388 poils   mediane 17,00 ms   ZERO image > 20 ms sur 144      ← retenu, 59 im/s
   66 911 poils   mediane 20,10 ms   85 images > 20 ms
```

**Ce qui a payé :**
1. **Une seule passe de tampon au lieu de deux.** Le coût fixe partait dans deux vidages de
   608 000 mots, deux `putImageData` de 2,4 Mo et deux `drawImage`. Les six restent **dedans**
   (règle acquise) : on les trame **dans le tampon**, entre le dos et le devant.
   **4,3 → 1,9 ms.**
2. **Le versement écrit sans relire.** La comparaison `a > (B[oo]>>>24)` ajoutait une **lecture**
   par pixel — donc un défaut de cache de plus et une dépendance. Le dernier posé gagne : c'est
   acceptable pour une fourrure (un poil en recouvre un autre), ça ne l'était pas pour des grains
   isolés. **−18 % par poil.**

**Ce qui n'a rien donné, et qui est noté pour ne pas y revenir :**
- **Des poils plus fins** : 16,40 contre 16,60 ms. Ce n'est pas le nombre de pixels.
- **Les `push` sur tableaux ordinaires** remplacés par des tableaux typés : **aucun gain**.
- **Ranger les poils par bande d'écran** pour grouper les écritures : **aucun gain** (17,7 contre
  17,3). Le comptage coûte ce que le cache économise.
- **Éclaircir le dos** : perte nette, déjà noté au lot précédent.

### Ce que je ne fais pas passer pour fait

- **Il reste du repli au miroir** sur les cellules plus grandes que le rectangle inscrit de leur
  dalle : on voit encore quelques losanges, surtout en gravure. La vraie parade serait de
  détecter le pas du motif et de replier par translation.
- **17,00 ms, c'est 59 images par seconde**, pas 60. Zéro image au-dessus de 20 ms sur 144 — mais
  je ne prétends pas 60.
- L'**animation** n'est toujours pas jugée, et le **partage** n'est pas maquetté.

---

## ⚑ LES ÉCARTS, LA DENSITÉ, ET LE BANC QUI TRANCHE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html` + `cap_banc.py`
> Anti-cache : `scratchpad/bust.py`

### ⚠ 0 · CE N'ÉTAIT PAS LA PLANCHE, C'ÉTAIT LE CACHE — deuxième fois

`python3 -m http.server` n'envoie **aucun** `Cache-Control`. Le navigateur applique sa
fraîcheur heuristique et **ne redemande même pas** le fichier : le serveur ne peut rien, il
n'est jamais interrogé. Ça mord surtout depuis que la planche charge cinq modules externes —
le HTML se recharge, les `.js` non. **Vérifié en `curl` avant de conclure** : les cinq modules
répondaient `200` avec les marqueurs neufs.
**`scratchpad/bust.py`** horodate chaque `<script src>` avec le `mtime` du fichier
(`?v=1788870952`) et pose un `no-store` sur le document. **À relancer après toute édition de
module.**

### ⚑ 1 · LES ÉCARTS ENTRE DALLES — la silhouette ne doit pas découper la cellule

Je découpais chaque cellule avec **la silhouette** de sa dalle. Une dalle dont les proportions
ne collaient pas y laissait une marge énorme, sa voisine presque aucune : des joints **du simple
au triple**, ce qui ne ressemble à aucune Toile.

**Parade : on ne prend que L'INTÉRIEUR de la dalle.** Chaque dalle rendue reçoit son **plus grand
rectangle inscrit** (`inscrit()` : la silhouette est fermée par balayage en lignes *et* en
colonnes, sinon les mondes creux — gravure, 22 % de pixels — n'ont pas d'intérieur du tout). La
cellule se cale sur ce rectangle, et **le joint devient une valeur angulaire constante**,
0,016 rad ≈ 4 % du diamètre d'une dalle — le même filet partout.
⚠ Les trous de la **trame** restent : les pois du braille, les stries de la gravure sont de la
matière absente, pas un bord de dalle.

### ⚑ 2 · CHAQUE MONDE VISE LA MÊME DENSITÉ

Un monde creux peignait deux fois moins de poils qu'un monde plein : la Pelote en gravure
sortait terne, alors que ce qu'on veut voir c'est **sa trame**, pas sa pénurie. On sème
maintenant en proportion inverse du remplissage du rectangle inscrit (plafonné à ×3,2).

```
MESURÉ, huit mondes, même cadre :  encre 36 616 · mosaique 36 485 · touffe 35 837
   braille 37 076 · pixel 36 575 · terrazzo 35 098 · gravure 35 942 · sillons 38 403
   (avant compensation : de 13 175 pour gravure a 36 460 pour encre)
```

### ⚑ 3 · LE BANC — et il a corrigé DEUX de mes intuitions

Le plafond de l'audit (39 500) avait été mesuré sur des **dalles**, pas sur des poils. J'ai donc
mesuré, sur **l'intervalle réel entre deux images**, sphère **en rotation**, écran de 390 px :

```
36 453 poils   mediane 16,40 ms   9e decile 17,00   1 image > 20 ms sur 144   ← le plafond
42 004         18,10              18,90             3   (≈ 55 im/s)
46 929         20,50              21,20            126   (≈ 46 im/s)
56 658         24,30              25,20            144
```

**Ce qui m'a détrompé :**
1. **Des poils plus FINS ne rendent presque rien.** 36 450 poils fins → 16,40 ms contre 16,60
   pour des gras. Ce n'est donc **pas** le nombre de pixels peints qui domine, c'est **le coût
   par tampon**. La monnaie est le tampon, pas le pixel.
2. **Éclaircir le dos est une PERTE NETTE.** Un point du dos garde son coût de boucle ; on
   n'économise que son tampon. **35 956 poils à 18,40 ms** avec un dos au tiers, contre
   **36 453 à 16,40** avec le dos plein et moins de candidats. Contre-intuitif, et mesuré.

**Ce qui a vraiment payé :** les tableaux par point en **Float32Array** au lieu de Float64 —
17,60 → 16,50 ms à nombre égal, **7 %**. La boucle est liée à la mémoire, pas au calcul.
Et le **cache du travail statique** : relief (six évaluations de `phi` par point), champ de flux
et lecture de trame vivent dans le repère de l'objet — la rotation n'y change rien. L'image ne
paie plus que la projection, la lumière et le versement.

### La réponse honnête à « plus fourni en poils »

**36 450 poils, c'est le plafond des 60 images par seconde** pour ce grain, sur un écran de
390 px. Au-delà on descend : 42 000 → 55 im/s, 47 000 → 46 im/s. Ce qui a réellement rendu la
fourrure plus fournie, ce n'est pas le nombre — c'est que **les dalles sont pleines** depuis
qu'on échantillonne leur intérieur au lieu de les découper à la silhouette, et que **les mondes
creux sont compensés**.

### Ce qui reste ouvert

L'**animation** n'est toujours pas jugée (le banc tourne, mais personne n'a regardé). Le
**partage** n'est pas maquetté. Et la **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ LA SPHÈRE EST LA TOILE — synchro Toile · Pelote · Studio · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · moteur : `scratchpad/_p_{moteur,trame,semis,peint,planche}.js`
> Sonde des huit mondes : `scratchpad/sonde_trame.html` · captures : `scratchpad/pav/`

**Décision Tom : la surface de la Pelote n'imite plus la Toile, elle EST la Toile.**
Chaque cellule du Voronoï sphérique porte **une vraie dalle du moteur** —
`Toile.dalleTrame`, échelle 1 — avec sa forme, sa matière et ses couleurs. Changer de monde ou
de palette au Studio change la Toile **et** la Pelote, du même geste. C'est la règle 1 du §4
appliquée à la lettre : jamais un polygone, jamais une approximation.

Et le grain devient un **poil** : la matière est duveteuse et **peignée**, comme immergée dans
un liquide transparent.

### ⚠ 1 · `Toile_resize()` LIT LE PARENT DU CANEVAS, PAS LE CANEVAS

```js
var st=host.parentNode; var w=st.clientWidth, h=st.clientHeight;
if(!w||!h) return;                 // ← et il ne se passe plus rien, en silence
```

Mon hôte était dans un `<div style="height:0;overflow:hidden">`. La Toile restait à **0 × 0**,
`seedGray()` ne posait aucune cellule, `plantOne()` rendait `null`, `Toile.count()` valait
**zéro** — et `dalleTrame` sortait des canevas **vides sans une seule erreur**, parce qu'elle
avale la sienne dans un `try/catch`. Une demi-heure perdue à chercher dans la mauvaise fonction.
**Le parent de l'hôte doit avoir une vraie taille** ; on lui donne 390 × 620, la géométrie de
l'app. Vérifier `Toile.count()` avant de croire une dalle.

### ⚠ 2 · TROIS ERREURS D'ÉCHELLE DE SUITE, SUR LE MÊME CALAGE

Poser une dalle du moteur dans une cellule sphérique demande un facteur pixels-par-radian. Je me
suis trompé trois fois, et **chaque erreur avait sa signature à l'écran** :

```
uu = (v·e1) × 480 × ech      ech ETAIT DEJA le facteur : tout tombait hors tableau
                             → LA SPHERE SORTAIT A UNE DALLE PEINTE (1 sur 74 000)
ech = diag/(2·rayon·1,30)    calage sur le CERCLE maximal de la cellule
                             → les cellules allongees restaient aux trois quarts vides
ech = max(w/du, h/dv)        la cellule debordait de l'IMAGE de la dalle
                             → 18 % de couverture, une sphere trouee
ech = min(w/du, h/dv)×0,98   ✓ toute la cellule tombe dans l'image ; le VIDE de la dalle
                             fait le joint d'encre, et c'est la vraie forme qui le decoupe
```

La cellule se cale sur **sa boîte** dans son propre plan tangent (u₀,u₁,v₀,v₁), pas sur son
cercle. Et on choisit pour chaque cellule la dalle dont la boîte lui ressemble le plus — même
allongement, même taille — pour que le grain de la trame garde à peu près sa taille naturelle
d'une cellule à l'autre, comme sur une vraie Toile.

### ⚑ 3 · LE DOIGT PEIGNE LA FOURRURE — sans ça l'empreinte ne se voit plus

Sur une sphère nue, un creux se lit à son ombre. **Sous un pelage, l'ombre est noyée par la
variation des poils eux-mêmes** : le pouce appuyé à fond ne se voyait pas du tout. Un vrai
pelage pressé se couche — les poils se rabattent **radialement**, en rosette, et ils
raccourcissent. C'est ce geste-là qu'on lit, pas l'ombre. Le peigne est plein au bord du
contact et s'éteint à 2,4 fois le rayon.

### Les poils, et pourquoi ils sont peignés

Le poil part de **la racine** (le centre du tampon) : il est donc orienté sur **2π**, pas sur π
comme un fil symétrique — **24 secteurs**. Il s'affine et s'éteint vers la pointe (c'est ce qui
fait doux plutôt que hérissé) et il s'incurve un peu.
**Un hachage par point donne un hérisson ; un champ lisse donne une fourrure.** L'orientation
vient du gradient tangent d'un scalaire basse fréquence : les poils tournent en volutes lentes,
jamais en bandes.

### La couleur ne se reconstruit plus : on la lit dans la dalle

Ce ne sont plus « les quatre couleurs de la palette » rebâties de mon côté, mais **les teintes
réellement peintes par le moteur**, quantifiées sur 5 bits par canal, les 96 plus fréquentes
gardées (encre en sort 6 ; touffe, 119). Le rapprochement se fait **à la demande** — un balayage
complet du cube 32³ coûtait deux millions de distances par monde.
Chaque teinte porte ses sept marches, et **la lumière fait monter la dalle d'une marche dans sa
propre rampe** : un aplat franc, jamais un fondu.

⚠ **La rampe montait trop haut** : la moitié des poils atteignait la marche du reflet et toute
la sphère virait à la crème — la palette du Studio disparaissait sous son propre éclairage.

### Ce qui est mesuré

```
LES HUIT MONDES rendent bien, et differemment (sonde_trame.html, dalles de 48 a 153 px) :
   encre 58-72 % de remplissage · mosaique 41-52 · touffe 37-49 · braille 26-35
   pixel 60-78 · terrazzo 42-52 · gravure 22-27 · sillons 24-34
LES POILS PAR IMAGE   34 366 sur les mondes pleins (encre, pixel) — sous le plafond de 39 500
   les mondes creux en peignent moins (12 900 pour gravure) : ils SONT creux, c'est la trame.
```

### Ce que je ne fais pas passer pour fait

- **L'animation n'est pas jugée.** Les poils sont peignés par un champ qui accepte un paramètre
  de temps (`tflux`), mais rien n'a été rendu en mouvement.
- **La profondeur du doigt n'est pas remesurée** depuis le lot précédent : la preuve en pixels
  vaut pour 10,5 % du rayon, la planche enfonce à 24,5 %.
- **Le grain de la trame varie encore un peu d'une cellule à l'autre** — le calage exact sur la
  boîte l'emporte sur la taille naturelle quand les proportions ne collent pas.
- **Le partage** n'est toujours pas maquetté.

---

## ⚑ LE PAVAGE HABILLÉ — QUATRE BUGS DE FOND · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · moteur : `scratchpad/_p_{moteur,semis,peint,planche}.js`
> Preuve : `scratchpad/preuve_pavage.py` + `scratchpad/mesure_pav.html`
> Diagnostics : `scratchpad/diag_pav.html` (les étages du semis), `scratchpad/diag_emp.html` (la carte des zones de contact)

**Le parti pris est tranché : C, le pavage.** La Toile fermée sur elle-même — des dalles
pleines séparées par des joints d'encre, un Voronoï pondéré sphérique. Reproche de Tom sur la
livraison précédente, et il était juste : *« tu as tout éteint pour isoler. Isoler une variable
ne veut pas dire éteindre tout le reste. On ne choisit pas un parti pris sur une maquette
morte. »*

### ⚠ 1 · LE TIRAGE DES SEMENCES NE SORTAIT JAMAIS DE LA CALOTTE NORD

La boucle de rejet s'arrêtait dès qu'elle avait ses M semences :
`while(i<CAND && garde<M)`. Or l'indice d'un réseau de Fibonacci parcourt la sphère **du pôle
nord au pôle sud**. En s'arrêtant à la 240ᵉ acceptée, on ne sortait jamais du **premier quart**
du réseau : les 240 semences étaient toutes au nord. Partout ailleurs les deux plus proches
sites étaient loin **et à égale distance**, donc `d2−d1` tombait sous le joint sur des régions
entières, et le pavage **effaçait des quartiers complets de la boule**.

**Le diagnostic l'a montré en un rendu**, et c'est la leçon de méthode : j'ai peint le semis à
trois étages (brut / joint appliqué / **densité uniforme**). Avec une densité uniforme, **les
mêmes coins noirs** — donc ce n'était pas la densité, comme je le croyais depuis deux passes.
**Parade :** balayer tout le réseau, et régler le taux d'acceptation pour tomber sur M en
moyenne (deux passes, l'une pour la somme).

### ⚠ 2 · CE QUI TUE L'EFFET REPTILE, C'EST LA DENSITÉ DU SEMIS — PAS LE POIDS DES SITES

Je faisais varier le **poids** des sites (diagramme de puissance). Ça ne marche pas : au-delà
d'un écart de l'ordre de l'espacement, un site à poids faible n'est pas une *petite* cellule —
il est **avalé**, il disparaît. Les survivantes se retrouvent donc toutes de la même taille.
C'était exactement ça, la peau de reptile.

**La bonne variable est la DENSITÉ.** Une cellule occupe 1/densité : là où les semences se
serrent, les dalles sont petites ; là où elles s'espacent, elles sont grandes — et **aucune ne
disparaît**. C'est aussi ce que fait une vraie Toile : des grappes serrées et des clairières.
Le poids reste, faible : il casse la régularité locale, il n'avale plus.
Les fréquences du champ de densité valent **4 à 7** — une grappe fait cinq ou six dalles. Plus
bas, la densité varie à l'échelle de la boule et on retombe sur des bandes.

### ⚠ 3 · LA PERTURBATION DU DOIGT PORTAIT À SOIXANTE DEGRÉS

`(u/ub)·exp(1−u/ub)` vaut encore **18 % de son pic à u = 1,4**. Avec un rayon de contact de
0,36 rad, la queue du bourrelet portait jusqu'à 60° du doigt : **la boule entière se soulevait
de 3 % et glissait de 7 %**. L'image sous le pouce ne ressemblait plus à l'image au repos, et ce
n'était pas l'empreinte — c'était un effet global.

**La carte des zones de contact** (bleu = plateau, rouge = paroi, vert = bourrelet) l'a chiffré
d'un coup : **731 points de plateau contre 3 913 de queue de bourrelet.** Le creux était
minuscule et la perturbation immense — l'inverse d'une empreinte.

Et **`U` est un glissement EN RADIANS, pas un coefficient libre** : à 1,85 avec `dmax` 0,215, la
matière glissait de **0,40 rad**. Les dalles ne se tassaient pas, elles **se mélangeaient**, et
le contact sortait en pluie de traits de toutes les couleurs. Le refoulement d'une pulpe vaut le
volume chassé sur la circonférence, soit `d·a/2` = 0,039 rad.

### ⚑ 4 · LE MUR N'EST PAS UN COUTEAU, C'EST UNE CUVETTE LARGE

Je faisais remonter la surface en `exp(−u/0,085)` : le creux revenait à zéro en un cinquantième
de radian et l'empreinte se réduisait à un petit disque terne. **La solution exacte d'un poinçon
plat sur un solide mou est connue** : hors du contact, l'enfoncement vaut **(2/π)·asin(a/r)**.
Elle vaut 1 au bord (la continuité est assurée), **0,46 à une fois et demie le rayon, 0,33 à
deux fois**. C'est une cuvette — et c'est elle qui fait « la matière cède ». Le bord garde sa
cassure de pente (la dérivée y est infinie) ; **le fond reste plat**.

### Deux erreurs d'éclairage, et elles se ressemblent

- **Le fond d'un creux est occulté par son propre bord.** Sans ce facteur, le plateau sortait
  **plus clair que le reste de la boule** — sa normale regarde le doigt, donc la lumière, et
  Lambert le récompensait jusqu'à la marche du reflet : l'empreinte sortait en **cicatrice
  blanche**. Un trou est sombre, même quand sa surface est bien orientée.
- **Seule la part TANGENTE de la lumière creuse une ombre portée, et il faut la normaliser.** Au
  point touché, la lumière était radiale à 88 % : sa part tangente valait 0,47, l'ombre ne
  séparait le fond qu'entre 0,46 et 0,81, et le creux ne se lisait pas comme un creux.

### L'ombre se porte aussi par l'OPACITÉ

L'audit du 5 septembre l'avait annoncé : *« la palette d'un monde n'a pas l'écart de luminosité
de la crème sur l'encre — c'est cet écart qui faisait le volume ; avec des dalles colorées, la
sphère s'aplatit »*. Et elle s'aplatissait : un disque à liseré, pas une boule. On rend cet écart
en laissant le côté à l'ombre **s'éteindre vers l'encre** : la palette reste exacte, c'est sa
**présence** qui baisse. Plus un **liseré de Fresnel** au limbe — c'est lui qui affirme le cercle.

⚠ **Mais la matière ne disparaît pas SOUS le doigt : elle s'assombrit.** En laissant la présence
suivre la lumière dans le creux, les dalles du contact devenaient si pâles qu'on ne voyait plus
la mosaïque — un trou noir, pas un enfoncement. Dans le creux, la présence reste pleine ; c'est
la marche de couleur qui descend.

### La couleur : celle du Studio, et la rampe de la Toile

Une dalle d'Aura **est** une dalle de Toile : une couleur de `Toile.cols()` et une marche de ton
parmi les cinq du moteur (`TON = 1 · 0,76 · 1,24 · 0,88 · 1,12`). **La lumière ne fait pas un
dégradé : elle fait monter la dalle d'une marche dans sa propre rampe** — un aplat franc, jamais
un fondu. C'est la règle de la Toile, et c'est aussi ce qui évite les rayures parallèles pour
lesquelles l'iridescence a été refusée deux fois. Le **reflet d'essence** ne tourne pas la
teinte pixel par pixel : au ras du bord, **une dalle entière bascule** sur la couleur suivante
de la palette, d'un coup — il n'y a pas de dégradé à rayer.

### La technique

```
LE TAMPON NE PORTE PLUS QUE L'ALPHA ; la couleur se compose au versement par un OR.
   Sans ça : 4 couleurs x 7 marches x 3 tailles x 8 orientations x 6 niveaux = 4 032 tampons.
   Avec :    144.
LE GRAIN SE MESURE SUR LE CADRE, pas en pixels absolus — un atlas par taille de cadre.
   Sinon, sur un cadre de 200 px le même grain est trois fois plus gros par rapport à la boule.
LES COTES DU DECOR AUSSI (le Noyau, les six) : en dur, ils mangeaient la moitié des petits cadres.
38 829 DALLES par image — SOUS le plafond mesuré de 39 500 pour 60 im/s. A 90 000 candidats
   on montait a 49 800 : plus joli d'un cheveu, et hors budget.
```

### La preuve, et ce qu'elle ne couvre pas

**Re-mesurée sur le moteur du pavage, à la profondeur de la preuve d'origine** (0,105 et
a = 0,34), pour isoler **le changement de loi de paroi** — une variable à la fois :

```
1 · UN FOND PLAT              rayon ou le profil ne bouge plus (< 15 % de l'amplitude)
      plateau   8,0 -> 2,0 -> 24,0 px        cloche  0 · 0 · 1 px — elle creuse des le centre
2 · LE FOND EST-IL PLAT ?     dans LA MEME fenetre : ecart-type / moyenne, en % de l'amplitude
      plateau   6,8 / +1,9 %   8,5 / +10,2 %   5,5 / −1,2 %     ← le coeur est intact
      cloche   25,6 / −56,6 % 18,3 / −69,9 %  47,4 / −40,7 %    ← elle vide le coeur
3 · LE BOURRELET SE DEPLACE   plateau  34 -> 60 -> 67 px  (x1,97)
      cloche    21 -> 22 -> 22 px  (x1,05)  — sa tache ne grandit pas avec la pression
```

⚠ **CE QUE JE NE FAIS PAS PASSER POUR PROUVÉ.** La planche enfonce à **24,5 %** du rayon, pas à
10,5 %. À cette profondeur la perturbation couvre la moitié de la sphère et **la sonde décroche**
— elle lit alors le limbe autant que le creux, et les profils sortent bruités et asymétriques.
Le plateau et sa cassure de pente sont vrais **par construction** (le code est le même), mais
**la profondeur de la planche n'est pas mesurée**. Et le marqueur « bord franc » ne sépare
toujours pas les deux lois sur cet observable (6/12/8 px contre 4/7/5) : c'est le **fond plat**
qui porte la preuve du bord.

### Ce qui reste ouvert

L'**animation** n'a jamais été jugée sur cette matière. Le **partage** (image seule / intégrée)
n'est pas maquetté. Et le pavage est **statique** : il ne dit rien encore de la vie d'une Toile
qui pousse.

---

## ⚑ LE FORK DE L'PELOTE — ET DEUX BUGS QUI EXPLIQUENT LES CINQ SILHOUETTES RATÉES · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-TROIS-MATIERES.html`** · moteur partagé : `scratchpad/_m_{moteur,semis,peint,neuf}.js`
> Preuve : `scratchpad/preuve_empreinte.py` + `scratchpad/mesure_emp.html` · images : `scratchpad/emp/`, `scratchpad/mat/`

### ⚠ 1 · LA SILHOUETTE — « haute fréquence » n'était appliquée QUE SUR UN AXE

Le relief de la dernière série valait `0,060 · sin(16,2x) · sin(0,7y) · cos(0,6z)`. La règle
« haute fréquence, faible amplitude » était **écrite** dans le fichier — et respectée en x
seulement. **0,7 et 0,6 en y et en z, c'est une enveloppe à l'échelle de la boule entière** :
des lobes verticaux, donc une courge. Aucune valeur d'amplitude n'aurait pu rattraper ça.

**Deux règles posées, et la seconde est plus forte que la première :**
1. toutes les fréquences ≥ 8 **sur les trois axes**, amplitude totale ≤ 3,6 % ;
2. **le déplacement radial est amorti au limbe** (facteur `face^0,6`, nul là où la normale est
   perpendiculaire au regard). La silhouette redevient alors un **cercle exact**, quelle que
   soit l'amplitude — le relief vit dans le disque, jamais sur son bord.

### ⚠ 2 · L'AXE DU DOIGT N'ÉTAIT PAS TANGENT — l'empreinte ressortait de l'autre côté

Même famille que le bug n° 1 de l'audit, et il coûtait une seconde empreinte détachée, hors
silhouette. `E.ax` gardait une part **radiale** : `du` mélangeait du tangentiel et du radial, et
la zone `s<1` n'était plus une tache sur la surface mais **un cylindre qui traverse la boule**.
Correctif : on orthogonalise l'axe à la normale, et **on mesure la tache dans le plan tangent**.

Et un troisième, dans la foulée : **le plan du plateau est perpendiculaire à la NORMALE, jamais
à l'axe du doigt.** Perpendiculaire à l'axe (qui est tangent), le « plateau » était un plan qui
**tranche** la boule : on voyait une morsure, pas une pulpe.

### L'EMPREINTE EST REFAITE — et prouvée sur l'image, pas dans le code

Le modèle n'est plus une cloche. **Une pulpe adhère et s'aplatit** : dans le contact la surface
devient **plane** (donc une seule normale, donc un méreau uniformément éclairé), **rien n'y
glisse**, et tout se passe **au bord** — paroi raide puis bourrelet. Et le rayon de contact suit
Hertz : `a = amax·p^(1/3)`, `d = dmax·p^(2/3)`.

```
LA MÊME SCÈNE, LES DEUX LOIS, ÉCLAIRAGE PLAT (l'image = la densité projetée du semis,
donc la géométrie et rien d'autre). Coupe en travers du doigt, lissée sur 13 px.

1 · UN CŒUR INTACT, ET IL GRANDIT     rayon où rien ne bouge (< 15 % de l'amplitude)
      plateau    5,0 px -> 11,0 px -> 14,0 px      ×2,80
      cloche     0,0 px ->  0,0 px ->  0,0 px      aucun : elle creuse dès le centre
2 · LE FOND EST-IL PLAT ?             DANS LA MÊME FENÊTRE, moyenne / amplitude
      plateau    +2,1 % -> +2,6 % -> +3,6 %        (écart-type 7,7 à 8,2 %)
      cloche    −80,1 % -> −76,4 % -> −78,9 %      (écart-type 20 %)
3 · LE BOURRELET                      lobe de signe opposé, au-delà du bord
      plateau    +29 % à 38 px -> +28 % à 53 px -> +32 % à 79 px
      cloche     +55 % à 16 px -> +69 % à 20 px -> +62 % à 24 px
```

**Ce que je ne fais pas passer pour prouvé :** la *raideur du bord* mesurée seule ne sépare pas
les deux lois (5 à 18 px des deux côtés, bruité). C'est le **cœur intact** qui porte la preuve du
bord : un rayon existe en deçà duquel rien ne bouge, et il n'existe pas pour la cloche.

### ⚠ TROIS PIÈGES D'INSTRUMENT PAYÉS SUR CETTE SEULE PREUVE

1. **Je cherchais de l'encre PERDUE au cœur du contact.** Il n'y en a pas : le plateau, étant
   plan et face à la lumière, en **gagne**. La sonde annonçait « fond plat : 0 px » sur un
   plateau parfaitement plat. **On mesure l'écart SIGNÉ, sans préjuger de son signe.**
2. **L'écart brut entre deux images est dominé par LE GRAIN** — un fil déplacé d'un pixel donne
   un couple +200/−200, quand la forme de l'empreinte vaut 20 à 50. On lisse sur 13 px avant de
   profiler. C'est le grain qu'on retire, jamais la forme.
3. **LA LUMINANCE NE DIT PAS LA GÉOMÉTRIE.** Sur une surface courbe vue de biais, une lumière
   directionnelle fabrique un **dipôle clair/sombre** qui noie le profil : ma coupe lisait ce
   dipôle et concluait « le fond n'est pas plat ». Il a fallu un **mode de mesure à éclairage
   plat** — tout grain vaut pareil, l'image devient la densité projetée du semis.
   *Et une quatrième, qui n'est pas un piège mais une erreur de métrique :* je normalisais par
   la valeur **au centre**, qui vaut zéro sur un plateau — c'est exactement ce qu'on cherche à
   prouver, et ça envoyait toutes les mesures à 300 %. **Le bon repère est l'amplitude.**

### LE FORK — trois partis pris, pas trois rendus

Ils ne peuvent pas coexister : un point ne peut pas être à la fois un grain libre, un maillon de
fil et une dalle d'un pavage. Chacun porte **sa** loi de contact.

```
A · LA POUSSIÈRE  des grains indépendants — on lit une DENSITÉ
                  contact : chacun pour soi, chassé vers l'extérieur
B · LE FIL        200 brins CONTINUS enroulés, colatitude ondulée (l'onde)
                  contact : un brin tendu N'ENTRE PAS dans le creux, IL L'ENJAMBE
C · LE PAVAGE     des dalles pleines séparées par des joints d'encre — un Voronoï
                  PONDÉRÉ sphérique, la Toile fermée sur elle-même
                  contact : rien ne se disperse, les dalles fusionnent en un SCEAU
```

⚠ **Ma première version de C ne gardait que les COUTURES** : ça donnait un **globe filaire**, vu
et revu, et vide. Sur la Toile c'est l'inverse — chaque dalle est **pleine**, ce sont les joints
qui sont en encre, et **chaque cellule porte son ton sur cinq marches**. C'est cette mosaïque qui
reste lisible en petit, là où une poussière n'est plus qu'un gris (contrainte du partage : les
silhouettes à relief fin disparaissent à 200 px).

**Le joint doit être plus large que le grain**, sinon le grain le comble et la partition
disparaît : joint 0,038 rad contre un grain de 3 à 5 px. C'est ce qui a fait passer C d'une
boule moussue à une mosaïque.

### CE QUE JE NE FAIS PAS PASSER POUR FINI

**Aucun des trois n'est encore un chef-d'œuvre**, et je le dis avant qu'on me le demande.
A est le déjà-vu assumé (témoin). B est fascinant **sous le doigt** et brouillon au repos.
C a une identité — c'est le seul qui soit Promi — mais il tire encore vers la peau de reptile :
ses dalles restent trop proches en taille, là où une Toile mêle des grandes et des petites.
**Le fork se tranche sur le parti pris, pas sur ce niveau de finition.**

---

## ⚑ LA DÉRIVE, ET UN EXTRAIT DU MOTEUR PÉRIMÉ · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`** · sauvegardes : `avant-derive.html`,
> `toile-extrait-avant-moteur.js`.

**Tom : « je ne vois aucun changement ».** Le serveur servait bien le fichier à jour (vérifié :
`MAS_TEINTE='encre'` présent dans la réponse HTTP) — c'était son cache. Mais deux choses
n'arrivaient réellement pas à l'écran, et les voici.

### ⚠ 1 · L'EXTRAIT DU MOTEUR DATAIT D'AVANT LE LOT DU MONDE FIGÉ

`scratchpad/toile-extrait.js` — la copie de la Toile que les planches utilisent — avait été
extraite **avant** le lot du 4 septembre. Son `dalleTrame` **ignorait silencieusement son
quatrième argument** : je passais le monde, le moteur n'en faisait rien, et les quatre sphères
« quatre mondes » sortaient **identiques**. Aucune erreur, aucun signal.

**Re-extrait depuis `app.html`** (même intervalle de texte, 60 186 octets, `mondeCourant` présent).
Les quatre mondes donnent maintenant quatre grains distincts.

**Leçon générale :** *une planche qui embarque une COPIE du moteur vieillit en silence.* Toute
planche doit vérifier ce qu'elle a — ici `Toile.mondeCourant` — au lieu de le supposer.

### ⚡ 2 · LA DÉRIVE — ce qui manquait au repos

Sans doigt, la sphère tournait **d'un bloc** : belle, et morte. Une masse vivante se **cisaille**.
Chaque bande de latitude glisse à sa propre allure, en permanence.

⚠ **Elle OSCILLE, elle ne s'accumule pas.** Une dérive cumulative décorrélerait les bandes en
quelques minutes : les fils se perdraient et la sphère finirait en bruit uniforme. Chaque bande va
et revient, sur des périodes premières entre elles (37 à 97 s). Et le **tangage respire**
(±0,028 rad sur 83 s).

```
MESURÉ SUR LES IMAGES, rotation d'ensemble NEUTRALISÉE — ce qui change tout seul
   après 1 s   24,68 % des pixels ont changé   ·  écart moyen 26,5
   après 2 s   27,84 %                            30,0
   après 4 s   30,47 %                            33,7
   après 8 s   33,36 %                            37,5
```

Coût : **six sinus par image**. `scratchpad/preuve_repos.py`.

### Les relevés

```
L'IMAGE          16,72 ms · écart-type 0,96 · 1 image > 33 ms sur 300 · coût 8,5 ms
LES DALLES       46 041 par image · teinte ENCRE (forme de la dalle, encre de l'écran)
LA VIE AU REPOS  24,7 % des pixels changent en 1 s, 33,4 % en 8 s
LE CRATÈRE       66,09 → 35,37 → 65,41 d'encre (posé, puis +3,5 s) — 99 % du retour
LA TRAÎNÉE       runH/runV 1,040 au repos → 1,564 en rotation
LE COMBLEMENT    +19 % sans lancer, +45 % avec, en 0,35 s
LES CONTRÔLES    0 recouvrement · 0 hors cadre · langue §6 tout à zéro
```

---

## ⚑ LA PREUVE EN PIXELS — mes chiffres décrivaient une intention · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`** · images : `scratchpad/preuve/`
> outils : `scratchpad/preuve_geste.py` (filme) + `scratchpad/mesure_png.html` (mesure l'image).

**Reproche de Tom, et il était fondé :** *« Rien de ce que tu annonces n'arrive à l'écran. Tes
mesures décrivent une intention, pas ce qui est peint. »* On filme trois séquences et on mesure
**les images rendues**, jamais le code.

### ⚠ DEUX PIÈGES D'INSTRUMENT, ET L'UN M'A FAIT CONCLURE FAUX

1. **Une capture prend 100 à 300 ms.** Photographier « pendant » une rotation lancée, c'est
   photographier **après** : l'élan s'est amorti, le déplacement est nul, et l'image ne montre
   aucune traînée **alors que le code en dessine 67 000**. J'ai d'abord conclu « la traînée
   n'existe pas » sur cette image. Il faut **entretenir la vitesse** pendant toute la capture.
2. **La fenêtre de mesure est fixe à l'écran.** Si la sphère tourne, on compare deux scènes
   différentes — et à pleine vitesse la densité peinte est divisée par trois. Pour le creux on
   **arrête la rotation** ; pour le comblement on **remet la vue exactement où elle était** avant
   de photographier. Sans ça, la première mesure disait « l'encre baisse après un lancer ».

### A · LE CRATÈRE EXISTE

```
rotation ARRÊTÉE · carré de 140 px au point touché · encre = luminance moyenne de l'IMAGE
   avant        66,09   33,33 % de pixels allumés
   posé         35,37    9,53 %     ← −46 % d'encre, −71 % de pixels
   tenu 0,5 s   35,37    9,53 %     ← il TIENT sous le doigt
   +0,5 s       51,31   21,93 %
   +1,5 s       61,42   29,77 %
   +3,5 s       65,41   32,80 %     ← revenu à 99 % de l'état d'avant
```

### B · LA TRAÎNÉE N'EXISTAIT PAS — les deux suspects de Tom étaient les bons

```
vitesse ENTRETENUE à 5,8 rad/s · 10 175 grains peints, 67 576 tampons de traînée
                  encre     part     runH     runV    runH/runV
   au repos       60,85   32,81 %     5,16     4,96     1,040
   en rotation    65,08   42,53 %     6,07     3,88     1,564   ← +50 %
```

Mesure : **la longueur moyenne des suites de pixels allumés**, dans le sens du mouvement et en
travers. Un grain qui traîne allonge l'une **et raccourcit l'autre** — c'est ce qu'on lit.

**Les deux causes, corrigées :**
- **Le pas était calculé, le nombre plafonné.** À pleine vitesse un grain parcourt 57 px par
  image ; quatre tampons dessus, ce sont quatre points isolés tous les 14 px. Maintenant le
  **pas est fixe (2,5 px)** et c'est la **longueur dessinée** qui est bornée (34 px).
- **Le tampon garde le plus opaque, et je peignais la traînée deux niveaux plus sourde** : dans
  une sphère dense elle passait sous n'importe quel grain et ne se voyait jamais. Sa tête est
  maintenant **au même niveau que son grain** ; c'est la queue qui s'éteint.

Le troisième soupçon (un grain sur deux au-delà d'une rotation/seconde) n'était **pas** la cause :
il réduit la densité, il n'efface pas les traînées. Il reste une approximation déclarée.

### C · LE COMBLEMENT PAR LA VITESSE

```
même creux, MÊME point de vue restauré avant la photo, 0,35 s après le lâcher
   SANS lancer    56,15 → 66,80   (+19 %)
   AVEC lancer    50,82 → 73,74   (+45 %)   ← plus de deux fois plus vite
```

### La teinte : basculée (décision Tom)

`MAS_TEINTE = 'encre'` — on garde la **forme** de la dalle du moteur, peinte dans l'encre de
l'écran. Le terracotta d'un monde est exactement « à tenir » ; la matière ne doit pas parler le
langage des états.

### ⚠ CE QUI RESTE, ET QUE JE NE FAIS PAS PASSER POUR FAIT

**Au repos, la sphère ne surprend pas.** Tout ce qui est fascinant naît du **geste** — le creux,
le flux, le comblement. Sans doigt, c'est une belle poussière qui tourne lentement, pas encore
« du jamais vu ». Je n'ai pas d'idée qui ne soit pas un effet gratuit, et je le dis plutôt que
d'en ajouter une.

**Contrôles :** 0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre
32 · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432.

---

## ⚑ LE GRAIN EST UNE DALLE — et je dis ce que ça coûte · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**. Sauvegarde : `sauvegardes/avant-dalles-grain.html`.

### Les cinq mesures demandées

```
L'IMAGE AU REPOS   17,3 ms · écart-type 3,0 · 10 images > 33 ms sur 291 · coût 8,6 ms
L'IMAGE AU DOIGT   18,7 ms · MÉDIANE 16,70 · 63 > 20 ms sur 531 · coût 9,4 ms
                   ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
LES DALLES         46 041 par image · 168 tampons dans l'atlas · tailles 3 · 4 · 6 px
LE CRATÈRE         écartement 34 px au cœur, rayon d'action 66 px
                   monte en 0,09 s · à moitié refermé 0,93 s · DURÉE DE VIE 3,52 s
LE COMBLEMENT      lancé à 0 rad/s → 3,50 s · 3 → 0,93 s · 8 → 0,42 s · 11 → 0,27 s
```

### ⚠ CE QUE JE DOIS DIRE EN PREMIER : le grain-dalle EN COULEUR abîme la sphère

Deux raisons mesurées, aucune n'est une question de goût.

1. **La palette d'un monde n'a pas l'écart de luminosité de la crème sur l'encre.** C'est cet
   écart qui faisait le volume : le limbe brillait, le fond s'éteignait. Avec des dalles
   colorées, **la sphère s'aplatit**. J'ai récupéré une partie du relief en faisant varier la
   TAILLE de la dalle avec la profondeur (devant +1 cran, au fond −1), mais pas tout.
2. **Le terracotta d'un monde est EXACTEMENT « à tenir ».** La matière se met à parler le langage
   des états, juste derrière six anneaux dont c'est le métier. **Conflit de sens.**

**Les deux versions sont livrées côte à côte sur la planche**, même phase, même vue.
**Mon avis : garder la FORME de la dalle et la peindre dans l'encre de l'écran.** C'est toujours
la vraie dalle du moteur ; l'Aura change toujours quand on change de monde — elle change de
**forme** au lieu de changer de **couleur** ; la sphère retrouve son volume ; les six redeviennent
le sujet. **Une ligne bascule tout** (`MAS_TEINTE`). Le cadre vivant est en teinte du monde parce
que c'est ce que Tom a demandé.

### ⚠ Une dalle coûte plus cher qu'un grain rond — mon banc parlait de carrés de 2 à 4 px

```
sur l'écran complet, dalles de 3 · 4 · 6 pixels d'appareil :
   39 500 → 16,72 ms · 1 image > 33 ms sur 300     ← le seuil PROPRE
   46 000 → 17,3 ms  · 10 à 13 sur 290             ← réglé ici
   63 100 → 19,1 ms  · 39 sur 262
   84 100 → 21,6 ms  · 68 sur 232
le coût FIXE (vider les quatre tampons + les verser) = 1,25 ms seulement.
Ce n'est pas la structure qui coûte, c'est le nombre de dalles.
```

Une dalle de 3 à 6 px couvre 9 à 36 pixels ; un grain rond en couvrait 4 à 9. **« 64 000 tiennent
à 16,67 ms » était vrai pour des carrés, pas pour des dalles.**

### Ce qui a été fait

- **Le grain est une vraie dalle du moteur** — `Toile.dalleTrame`, échelle 1, huit dalles ×
  trois tailles × sept niveaux de profondeur, pré-rendues dans l'atlas de tampons. Aucun
  `drawImage` (hors budget d'un facteur trois, mesuré au lot précédent).
- **Le creux est franc et il dure** : 34 px d'écartement sur 66 de rayon, poussée **radiale**,
  durée de vie **3,52 s** (c'était 1,13 s). ⚠ **Elle s'éteint en approchant du limbe** au lieu de
  rabattre les points dessus : la version qui rabattait les empilait et laissait une **baie
  vide** — un objet mordu, pas un objet qui encaisse.
- **Le creux se comble quand on lance**, proportionnellement à la vitesse (on retranche, on ne
  remplace pas) : 3,50 s au repos → **0,27 s à pleine vitesse**.
- **La traînée suit le VRAI chemin** : on garde la position de l'image précédente et on tamponne
  la dalle le long du segment réellement parcouru (jusqu'à 4 tampons tous les 2,2 px, plus petite
  taille, deux niveaux plus sourde). ⚠ **Avant, j'orientais un grain pré-étiré sur la dérivée de
  la rotation SEULE** : le doigt poussait dans un sens, la traînée pointait dans un autre.
  C'était ça, l'effet plaqué.
- **La rotation de repos passe de 84 s à 2 min 45.** C'est le geste qui accélère, pas elle.
- **Le lointain est plus rare** : une dalle sur trois aux deux niveaux les plus lointains, une
  sur deux aux deux suivants, toutes devant. Le fond DOIT être plus clairsemé.

### Ce qui reste vrai

0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre 32, 0 recouvert
sur 9 points × 72 positions × 4 vues · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432 ·
encre sous un mot 0,06 à 0,41 % (seuil 1 %) · une fiche atteignable en 0,11 s au pire.

---

## ⚑ LA SPHÈRE VIVANTE — LE GRAIN, LE CRATÈRE, L'ÉTIREMENT · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**. Sauvegarde : `sauvegardes/avant-grain-organique.html`.

### Les quatre mesures demandées

```
L'IMAGE AU REPOS   16,72 ms · écart-type 0,97 · 1 image > 33 ms sur 300 · coût 7,0 ms
L'IMAGE AU DOIGT   17,64 ms · MÉDIANE 16,70 · 27 images > 20 ms sur 533 · coût 8,6 ms
                   ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
LES GRAINS         42 045 par image · 777 tampons dans l'atlas
LE CRATÈRE         monte en 0,10 s · à moitié refermé en 0,21 s · REFERMÉ en 1,13 s
                   écartement 20 px · l'encre au cœur tombe de 80 à 3 (−96 %)
UNE FICHE          0,11 s au pire (40° de rotation, 63 px de course de doigt)
                   4 personnes sur 6 sont atteignables 100 % du tour ; les autres 89 % et 90 %
```

### ⚑ LE GRAIN N'EST PLUS UN PIXEL — c'est un TAMPON

Le carré aligné faisait « pixel Windows 98 », **et c'était la technique qui l'imposait** :
`putImageData` n'écrit que des entiers. On dessine le grain **une fois** dans un petit canevas
(rond, anticrénelé, bouts ronds), on lit ses pixels, et on les **tamponne**.

```
quatre toiles — L'INTERVALLE RÉEL ENTRE DEUX IMAGES
   carré au pixel   20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,67   64 000 → 16,67
   TAMPON DE GRAIN  20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,79   64 000 → 16,79
   drawImage        20 000 → 48,55 ms   34 000 → 80,35   48 000 → 112,49  64 000 → 151,11
```

**`drawImage` par grain est hors budget d'un facteur trois — c'est l'APPEL qui coûte, pas les
pixels.** Le tampon ne coûte rien de plus que le carré.

Le grain varie sur **trois axes** : trois épaisseurs (tirées d'une quatrième onde plus serrée que
celles qui creusent les vides) × quatre longueurs d'étirement × douze orientations. Le tampon
garde **le plus opaque**, jamais « le dernier ».

⚠ **Et l'anneau a suivi.** Il était en carrés alignés comme la sphère ; quand la matière est
passée au grain rond, il est resté en pixels — le défaut des « trois langages » revenait par
l'autre bout. **Le grain se décide à un seul endroit et tout le produit le suit.**

### La matière réagit

- **Les grains s'étirent dans le sens du mouvement**, proportionnellement à la vitesse. La
  direction vient de la **dérivée exacte de la rotation** (`Zs`, `sin(tangage)·X`), pas d'une
  différence de positions. Au repos, le plus rapide parcourt 0,2 px par image : aucun étirement,
  et on ne rentre même pas dans la branche.
- **Le cratère se referme** en exp(−t/0,28), et **les contacts s'empilent** (six au plus) : on
  peut toucher ailleurs tout de suite, rien ne se fige jamais.
- **Les traînées ne naissent que de l'accélération** — au repos, aucune. Effilochées : chaque pas
  dispersé d'un cran par un hachage stable, opacité qui saute.
- **Les prénoms s'effacent quand ça tourne vite et reviennent quand ça se pose.** En pleine
  rotation ils sont illisibles et le placement les envoyait loin de leur anneau : on voyait six
  mots errer autour de la sphère.
- **Les visages sortent de la matière** : le dégagement suit la profondeur (0,92 au fond, 0,12
  devant), bord tramé.

### ⚠ Trois pièges payés dans ce lot

1. **Un impact naissant était jeté avant d'avoir grandi.** Le filtre supprimait tout impact dont
   l'enveloppe valait moins de 2 % — or elle vaut zéro à sa première image. Le doigt ne creusait
   rien et le chronomètre rendait « refermé en 0 s » sur les trois seuils. On ne jette que ce qui
   est **lâché ET éteint**.
2. **Le creux était trop grand** (72 px de rayon, 30 d'écartement) : il mangeait un quart de la
   sphère et **cassait sa silhouette**. 56 et 20.
3. **Ma première sonde mesurait le mauvais point.** Elle plaçait l'impact en coordonnées de
   CADRE alors que le code travaille en coordonnées de la BOÎTE de matière (décalée de 23 · 100) :
   « aucun effet », alors que l'effet était de −96 %. Toujours vérifier le repère avant de
   conclure qu'un correctif ne mord pas.

### Trois optimisations, et ce qu'elles coûtent au dessin

1. **On ne stocke que les pixels qui existent, pas la boîte.** Un grain étiré en diagonale occupe
   12 × 12 pixels de boîte pour 30 peints ; chaque tampon est une **liste de décalages**.
   Le calcul d'une image en rotation : **11,1 → 8,6 ms**.
2. **Au-delà d'une rotation par seconde, un grain sur deux n'est pas dessiné.** 14,0 → 11,1 ms.
   C'est invisible en mouvement — mais c'est une vraie approximation, et elle est déclarée.
3. **Le seau d'orientation se calcule sans `atan2`** (six comparaisons de pente).

### Ce qui reste vrai

0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre 32, 0 recouvert
sur 9 points × 72 positions × 4 vues · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432 ·
encre sous un mot 0,04 à 0,27 % (seuil 1 %), clairière coupée : 6 sur 6 sont pris.
**Pas de zoom** (décision Tom). **`openPerson` n'existe pas sur la planche.**

---

## ⚑ LA SPHÈRE SE PREND AU DOIGT · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**, premier cadre vivant ET manipulable.
> Sauvegardes : `sauvegardes/avant-prise-au-doigt.html`, `sauvegardes/avant-imagedata.html`.

### Ce qui change tout : le TEMPS et le POINT DE VUE sont séparés

Un seul nombre faisait tout — les six avançaient sur leur pelote ET la matière tournait, au même
rythme. **Impossible d'y poser un doigt : tourner l'objet aurait fait avancer le temps.**

```
LE TEMPS         les six voyagent sur leur pelote — un tour en 4 min. C'est la donnée.
LE POINT DE VUE  l'objet tourne sur lui-même — 84 s au repos, et le doigt le prend.
                 Deux angles (lacet, tangage) appliqués à TOUT — matière et personnes —
                 avant la projection. Il ne touche à AUCUNE donnée.
```

**Deux gestes, un seul capteur.** Une surface transparente sur la sphère, et on tranche **à la
levée** : au-delà de 6 px c'était une rotation, en deçà un toucher — et on cherche alors qui est
sous le doigt, le plus proche du regard d'abord. On ne peut pas écouter chaque anneau : le doigt
part souvent d'un anneau et le glissement serait mangé.

**L'élan s'ADDITIONNE à la rotation lente** au lieu de lui rendre la main : il n'y a pas d'instant
de reprise, donc **pas de saccade à la reprise**.

**La matière est entraînée** — six classes de retard prises sur la latitude dans le repère du
flux : l'équateur traîne, les pôles suivent. Cisaillement d'un fluide, pas d'un maillage. Coût :
six cosinus par image.

### ⚠ MON BANC PARLAIT D'UNE PAGE VIDE — et Tom a construit sa demande dessus

J'avais écrit « 26 000 points coûtent à peine plus que 13 000 ». **Vrai sur une page nue. Faux
sur l'écran complet** — mesuré : 14 700 → 17,5 ms · 18 400 → 17,6 · **22 300 → 21,9**.
Le plafond réel du `fillRect` était **13 000**, pas 26 000. J'ai cherché la cause au mauvais
endroit pendant six mesures (nombre de tranches, résolution de la toile, arrondi du cadre,
« une seule toile » — ce dernier test était **faux** : il ne dessinait qu'un quart des points).

**La vraie réponse était de changer de technique.** On n'appelle plus `fillRect` : on écrit les
pixels dans un `Uint32Array` par tranche, et on verse d'un seul `putImageData`. **Un appel de
dessin coûte plus cher que les quatre pixels qu'il pose.**

```
quatre toiles, points carrés sur la grille — L'INTERVALLE RÉEL ENTRE DEUX IMAGES
   fillRect   15 000 → 16,66 ms   24 000 → 16,67   34 000 → 16,79   48 000 → 24,36
   tampon     15 000 → 16,67 ms   24 000 → 16,67   34 000 → 16,67   48 000 → 16,67
```

⚠ **Ce que le tampon change au dessin, et c'est voulu :** il ÉCRASE au lieu de mélanger. Deux
points superposés ne s'additionnent plus — la matière ne se sature plus dans les zones denses.

### Une seule matière sur l'écran

**Un anneau est fait des mêmes points carrés que la sphère**, au même pas (`MAS_GRAIN`), sur la
même grille. Ce n'est plus un trait plaqué sur un fond : c'est la sphère qui se resserre en
cercle. Deux conséquences que la matière a IMPOSÉES :
- **l'arc d'une personne passe de 4 à 7** — à 4 px le grain n'a la place que de deux rangs et
  l'anneau disparaît ;
- **le visage RENTRE dans l'anneau** — §2.9 donne 0,62 du diamètre, on était à **0,94** : l'anneau
  n'était qu'un liseré autour d'un disque plein. C'était ça, les « trois langages ».

### ⚠ Un contrat de test réécrit — « rien ne passe devant ton Noyau »

**La règle n'a pas changé ; sa garantie a changé de nature.** Avant : la géométrie, et ça tenait
*parce que le point de vue était fixe*. Le doigt tournant l'objet dans tous les sens, n'importe
qui peut être amené sur l'axe du regard et **aucune inclinaison ne peut l'empêcher** — Tom l'a
écrit : *« quelqu'un de proche est près du centre, donc partiellement masqué par ton Noyau, et
c'est juste »*. Après : **l'ordre de tracé**, et le contrôle est plus dur :

1. aucun anneau n'atteint jamais le rang de ton Noyau — **72 positions × 4 points de vue**, rang
   le plus haut atteint **32**, ton Noyau à **40** ;
2. **au doigt**, sur neuf points de son disque : **0 recouvert**.

Version d'origine dans `sauvegardes/coll_sphere-avant-vue-libre.py` et
`sauvegardes/ctrl_sphere-avant-vue-libre.py`. Le seuil `derriere` du contrôle de collisions passe
de 20 à 40 pour la même raison. **Et le capteur du doigt sort du test de boîtes** — surface
transparente qui ne peint rien, 91 faux positifs ; sa vraie question est mesurée au geste.

### Les relevés

```
LA MASSE            36 fils · 42 045 points · 4 tranches · 7 niveaux francs
L'IMAGE AU REPOS    16,67 → 16,72 ms · écart-type 0,06 → 0,96 · 0 à 1 image > 33 ms sur 300
                    coût 6,5 ms par image
L'IMAGE AU DOIGT    16,85 ms · médiane 16,70 · 95e centile 16,80 · 2 images > 20 ms sur 457
                    ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
                    coût 6,7 ms par image
L'ÉLAN               2 rad/s → sous la lente en 1,81 s, éteint en 4,31 s, 0,22 tour
                     5 rad/s → 2,31 s · 4,81 s · 0,49 tour
                    11 rad/s → 2,74 s · 5,24 s · 1,01 tour
LES DEUX GESTES     immobile → Marion · 4 px → Marion · 41 px → rien. Seuil 6 px.
TON NOYAU           rang 40 contre 32 · 0 recouvert sur 9 points
LES SIX DEDANS      silhouette 167,0 · enveloppe 166,0 · 0 sortie sur 432
LA PROFONDEUR       25,4 → 61,8 px · rapport 2,44
LES CONTRÔLES       0 recouvrement · 0 hors cadre · langue §6 tout à zéro
L'ENCRE SOUS UN MOT 0,26 à 0,75 % (seuil 1 %) — clairière coupée : 6 sur 6 sont pris
```

### Deux choses que je n'ai pas faites, et une que je pose

**Pas de zoom** (décision Tom, reprise telle quelle). **Le tangage ne revient pas tout seul** à
sa valeur de repos : une sphère qu'on penche reste penchée, c'est la manipulation de l'utilisateur,
pas un réglage — seulement bornée à ±1,15 rad pour ne pas basculer par-dessus le pôle. Si Tom
préfère qu'elle se redresse doucement, c'est une ligne. **`openPerson` n'existe pas sur la
planche** : le toucher affiche un bandeau qui dit quelle fiche s'ouvrirait ; le geste est réel et
mesuré, le branchement est un lot d'intégration.

---

## ⚑ LA SPHÈRE — LA MASSE D'ABORD, LES SIX ENSUITE · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, le même que depuis le lot
> du moteur). Planche : **`PLANCHE-AURA-SPHERE.html`**, premier cadre vivant.
> `PLANCHE-AURA-RETENU.html` reste comme trace de la Pelote à six anneaux.

### Le principe, en une phrase

**La sphère est un tissu de trajectoires ; six d'entre elles portent un visage.**

Six anneaux ne feront jamais une sphère, quelle que soit la finition — c'est pour ça que dix
versions ont échoué. **Le volume vient de la DENSITÉ** : vingt-trois fils enroulés d'un pôle à
l'autre, pointillés, ~11 000 points. Chaque fil est un chemin, du même genre que celui que
parcourent les six. La masse ne dit rien d'autre : c'est vivant.

### ⚠ MON PREMIER BANC MESURAIT LE MAUVAIS CHIFFRE — et c'est la leçon du lot

**Le canevas 2D EMPILE les ordres, il ne les exécute pas.** Le temps d'appel de `stroke()` n'est
pas le temps de peinture. Mon premier banc annonçait **0,25 ms pour 4 000 traits** ; l'écran
tournait à **douze images par seconde**. Un banc qui chronomètre les appels ne mesure rien.

**Le bon banc mesure l'intervalle réel entre deux images** (`scratchpad/banc3.py`) :

```
traits    2 400 → 16,9 ms    6 500 → 25,2 ms    13 000 → 50,4 ms
points   13 000 → 17,4 ms   26 000 → 18,4 ms
à couverture CONSTANTE (60 000 px de trait), le coût est dans le NOMBRE :
   15 000 morceaux de 4 px → 59 ms        940 morceaux de 64 px → 20 ms
```

**Le plafond des traits est 2 400. Un point ne coûte presque rien.** La sphère est donc
POINTILLÉE — et un point posé sur un chemin dit encore le chemin. Deux instruments indépendants
concordent : Chromium sans fenêtre, et le navigateur de l'app (mesuré par `javascript_tool`).

### ⚠ ET LA TRAÎNÉE COÛTAIT PLUS CHER QUE LA SPHÈRE

Douze images perdues sur 289. J'ai d'abord accusé la masse et retiré des points — sans effet.
**Profilé, fonction par fonction** (`scratchpad/profil.py`) :

```
la masse    1,94 ms en moyenne · 2,10 au pire   sur 12 900 points
la traînée  0,27 ms en moyenne · 20,30 AU PIRE  sur 200 segments
```

Deux causes, deux correctifs : **sa toile faisait 390 × 844** (1,3 million de pixels effacés par
image) alors que tout ce qu'elle dessine tient dans la sphère → **344 × 344** ; et elle appelait
`stroke()` **une fois par segment**, 200 fois par image — le banc l'avait pourtant dit. Les
segments sont maintenant **groupés par niveau d'opacité** : 6 strokes par personne au lieu de 20.
Et **plus aucune allocation par image** (le ramasse-miettes rendait une image à 20 ms une fois
sur cent cinquante).

```
la traînée au pire   20,3 ms → 0,40 ms
une image au pire    22,6 ms → 3,30 ms
```

### Ce que la sphère a imposé, et que je n'avais pas prévu

**UN SEUL FOYER POUR TOUTE LA SCÈNE — 270.** À deux foyers (180 pour les six, 620 pour la
matière), un anneau au premier plan **sortait de la silhouette de 25 px**. Ce n'était pas un
défaut de dessin : c'était l'incohérence de deux projections. Avec un seul foyer, un corps qui
est DANS la sphère se projette DANS la silhouette, toujours.

**QUATRE TRANCHES DE PROFONDEUR, et c'est ce qui met les six DEDANS.** Une seule toile sous tout
le monde et les anneaux flotteraient dessus. La sphère est tranchée en quatre dalles ; chaque
tranche prend **le z-index que la formule des anneaux lui donnerait** (`20 + z/10`). Un anneau
qui s'enfonce passe derrière la matière ; celui qui vient vers toi passe devant. La tranche la
plus proche reste sous ton Noyau : **rien ne passe jamais devant toi.**

**LA MATIÈRE SE RETIRE SOUS UN PRÉNOM — sans plaque, sans ombre, sans voile.** Un mot posé sur
onze mille points n'est plus lisible. On **efface les points sous le mot** (`destination-out`),
dans les quatre tranches, **à 0,88** : il reste un huitième des points, et le bord de la clairière
ne se lit plus. La forme est une **pilule, rayon = hauteur ÷ 2** — la grammaire du §5, appliquée
à un vide. **Et elle s'allège devant un anneau** (0,76, et seulement dans les tranches vraiment
devant lui) : « toujours nets » est la règle, mais tout effacer enlèverait ce qui les met dedans.

**UN PRÉNOM SANS SON ANNEAU EST UN BUG.** Quand quelqu'un passe derrière ton Noyau, il la masque.
Son prénom, posé vers l'extérieur, resterait seul à flotter : il s'efface avec elle.

### Ce que ce lot COÛTE — je le dis avant qu'il le voie

**Le rapport de profondeur tombe de 3,43 à 2,20.** C'est le prix du foyer unique. En échange, la
profondeur n'est plus portée par la taille toute seule : elle est portée par **l'occultation**,
un indice bien plus fort.

**Les rayons s'ouvrent de 116 à 118 — deux pixels, et c'est tout ce que j'ai pu prendre.**
**La borne a changé de nature** : ce n'est plus le cadre, c'est la sphère. À 122, l'enveloppe des
six passe au-dessus de la silhouette et quelqu'un sort — ce qui contredirait la règle « ils sont
dedans ».

### ⚠ Le contrôle de collisions est AVEUGLE à la masse — et il faut le dire

Le canevas de la masse couvre 344 × 344 : au test boîte-contre-boîte il recouvre tout, et il est
en `pointer-events:none`, donc **la confirmation au doigt ne le rend jamais**. Je l'exempte de ce
test — qui ne mesure rien pour lui — et je mets à la place une **mesure de pixels**, plus dure :
combien d'encre la masse pose-t-elle sous un prénom, et devant un anneau (`scratchpad/ctrl_sphere.py`).

**⚠ Et cette mesure s'est trompée deux fois avant de tenir.** (1) Elle comptait des *pixels
allumés* : un point à 0,94 d'opacité en garde 0,11 après la clairière — au-dessus de tout seuil de
comptage, alors qu'il ne se voit plus. Elle mesure maintenant **l'encre déposée**, la somme des
alphas. (2) Son critère était **relatif** (« l'encre doit tripler ») : ça ne veut rien dire là où
la sphère est déjà creuse. Il est **absolu** : sous le mot, l'encre doit rester **≤ 1 %**.
(3) Et `_nomsALaCible` posait les prénoms à leur cible **sans repeindre la matière** : le trou
restait à l'ancienne place et le contrôle relevait de l'encre qui n'est pas à l'écran.

### Les relevés

```
L'IMAGE (5 passes)   16,72 → 16,83 ms · écart-type 0,97 → 1,66
                     coût d'une image 2,45 ms en moyenne, 3,70 ms au pire
                     images au-delà de 33 ms : 1 à 3 sur 300 (0,3 à 1 %)
                     ⚠ une passe sur six sort à 487 ms : machine saturée, pas le produit
                       — on relance, c'est le piège documenté du §7
LA SPHÈRE            23 fils · 10 928 points · 4 tranches · 7 niveaux francs
                     silhouette 167,0 px · rayon 142 · foyer 270
LES SIX SONT DEDANS  enveloppe 163,4 px · 0 sortie sur 432 (6 × 72 positions)
TON NOYAU            0 anneau devant lui sur 72 positions
LA PROFONDEUR        23,3 → 51,1 px · rapport 2,20
LA BOÎTE             55 · 149 → 321 · 414
LES CONTRÔLES        0 recouvrement · 0 hors cadre · langue §6 tout à zéro
L'ENCRE SOUS UN MOT  0,16 à 0,57 % (seuil de lisibilité 1 %)
                     clairière coupée : 5 prénoms sur 6 passent au-dessus → la mesure mord
L'ENCRE DEVANT       0,3 à 2,7 % de la boîte d'un anneau
```

### Ce qui n'a PAS changé

Le Noyau au centre avec ton visage, le mot en gros dessous, le chiffre en Fraunces 34 px avec sa
couleur d'état, la légende, la moisson avec chaque dalle dans son monde d'alors, le rejeu au doigt
et ses douze phrases, le bouton « Partager mon Noyau ». **Seule la Pelote a bougé.**

---

## ⚑ LE SACCADE — LA CAUSE ÉTAIT AILLEURS, ET JE L'AVAIS MANQUÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, premier cadre vivant.

### Les trois mesures demandées

```
1 · INTERVALLE ENTRE DEUX IMAGES   16,67 ms · écart-type 0,06 ms
                                   médiane 16,70 · 95e centile 16,70 · pire 16,80
                                   0 image au-delà de 20 ms sur 301 · 0 au-delà de 33
2 · COÛT D'UNE IMAGE               0,39 ms en moyenne · 1,90 ms au pire
3 · RAPPORT PETIT / GROS ANNEAU    20,6 px → 68,8 px  ·  3,34
```

**La boucle était déjà parfaite** — rAF, temps continu, position dérivée de l'horloge, aucun
compteur d'images, aucun `setInterval`. **Et une image coûte 0,4 ms.** Ni l'un ni l'autre
n'était le problème.

### ⚠ LA VRAIE CAUSE : les prénoms se téléportaient

```
un anneau avançait de 0,024 px par image        → invisible
CHAQUE PRÉNOM SAUTAIT 46 FOIS EN 10 SECONDES    → jusqu'à 112,6 px d'un coup
```

**Le placement au moindre coût BASCULAIT d'un créneau à l'autre au moindre frémissement** — et
comme la scène, elle, ne bougeait pas visiblement, **le seul mouvement de l'écran était un nom
qui se téléporte**. J'avais accusé la fréquence de ce calcul ; c'était son **instabilité**.

**Trois correctifs, chacun mesuré :**

```
1 · on ne garde un créneau QUE tant qu'il est PARFAIT (il ne recouvre rien), et on
    prend le meilleur dès qu'il cesse de l'être — les bascules entre créneaux
    ÉGALEMENT bons disparaissent
2 · le prénom GLISSE vers sa cible au lieu d'y sauter (le calcul reste à 4 Hz, le
    mouvement se fait à chaque image)
3 · AUCUN PAS NE DÉPASSE 1,2 px — sous ce seuil un déplacement ne se voit pas.
    Un glissement proportionnel seul faisait un premier pas de 4,3 px.
```

```
avant : 46 sauts/nom, le plus gros 112,6 px
après :  0 saut · le plus grand pas est 1,2 px, et c'est le plafond
```

**Et la vitesse : 132 s → 84 s.** À 132 s un anneau avançait de 0,024 px par image : la scène
paraissait **figée**, ce qui rendait le moindre frémissement de prénom d'autant plus visible.

### Le contrôle juge désormais l'état POSÉ

Un prénom qui glisse peut croiser un anneau pendant une demi-seconde — **c'est un déplacement,
pas un recouvrement au repos.** Le contrôle pose les prénoms à leur cible avant de mesurer, et
le dit.

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
boîte de la Pelote sur un tour : 20 · 138 → 353 · 444
langue §6 : tout à zéro
```

⚠ **Les rayons restent 80 → 116.** J'ai réessayé de les ouvrir à 122 comme tu le demandais :
la boîte sortait par la gauche (x = 3) et passait sous « solide » (y = 454). **116 à 268 est
la borne**, mesurée.

---

## ⚑ LA GRAVITATION LENTE — ÉTAT COURANT · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-RETENU.html`**, premier cadre vivant.
> Le rejeu et sa jauge sont **sortis** (décision Tom : un écran qui a besoin d'une légende
> est raté). `PLANCHE-AURA-DEUX-SORTIES.html` reste comme trace.

### Ce qui a changé

```
LA VITESSE     un tour en 48 s → 2 min 12. Assez lent pour qu'aucun mouvement ne se
               remarque, assez pour que la scène ait changé si on la laisse.
LES PLANS      COMPOSÉS À LA MAIN, plus tirés de l'alphabet. Trois plans presque
               couchés se croisent près du centre, deux redressés balaient large,
               un coupe en travers ; les phases sont décalées pour qu'aucun alignement
               régulier ne se produise. LE RAYON RESTE LA DATE — la seule chose
               qu'on ne compose pas.
LA TRAÎNÉE     0,12 → 0,085 du tour · opacité 0,34 → 0,30 · 28 pas.
               Elle est, et elle était déjà, la PROJECTION DU VRAI CHEMIN 3D :
               on échantillonne les positions passées dans l'espace, on projette
               chacune, on relie. Elle s'incline avec la Pelote, s'écrase de profil,
               passe sous ton Noyau quand le chemin y passe.
LE RETOUR      UNE FOIS, À L'OUVERTURE. La personne avec qui tu viens de tenir rentre
               vers le centre en 1,5 s (lissage d'ordre 5), puis l'écran se repose.
               C'est la seule chose que le rejeu laisse derrière lui.
LA FLUIDITÉ    les prénoms se replaçaient 60 fois par seconde (6 noms × 32 essais) :
               4 fois par seconde. C'était ça, le saccade.
```

### ⚠ Ce qui n'a PAS pu être récupéré de l'image fixe

**Les rayons ouverts à 77-149 ne survivent pas à la rotation.** Mesuré : à 128 la boîte sort
de **4 px à gauche** et de **56 px en bas** (elle mordait « solide »). Avec les plans composés
— qui portent les points plus loin que les plans tirés de l'alphabet — **la borne est 116**.
Les rayons sont donc **80 → 116**, pas 77 → 149. J'ai dû aussi **redresser trois inclinaisons**
(74° → 60°) : c'est Nico, le plus lointain, qui sortait par le bas.

```
profondeur : le plus petit 20,6 px · le plus gros 68,8 px · rapport 3,34
la boîte sur un tour : 20 · 142 → 353 · 448
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ LE REJEU — LA JAUGE, ET UNE RÉSERVE QUE JE POSE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-DEUX-SORTIES.html`** — les deux cadres
> sombres sont vivants. Captures : `scratchpad/sorties/`.

### La période est MESURÉE, pas supposée

Critère de Tom : jamais plus de 2-3 s sans événement.

```
période       jours  évén.  écart moyen  trou max   durée pour ≤ 3 s
7 jours           7      2       3,5 j      4 j          5,2 s   illisible
4 semaines       28      6       4,7 j     11 j          7,6 s   illisible
8 semaines       56     15       3,7 j     11 j         15,3 s   ← la seule qui tient
```

**Le trou qui commande tout : jour 33 → jour 44, onze jours sans une seule parole tenue.**
**Retenu : huit semaines en 15 s** — silence max **2,95 s**, écart moyen **1,00 s**.

⚠ **C'est plus RAPIDE que les 28 s d'avant, pas plus lent.** L'impression de vitesse venait
du **saccade**, pas de la durée. Si après le lissage ça paraît encore rapide, 18 s coûte
0,6 s de silence en plus (3,54 s).

### La jauge — trois différences d'un coup avec l'arc d'harmonie

```
elle est DEHORS            rayon 54 contre 36
elle est TROIS FOIS PLUS FINE   5 contre 18
elle n'a AUCUNE PISTE      un arc ouvert qui pousse, pas un anneau fermé
sa teinte est L'ENCRE      aucune des trois couleurs d'état : aucune valeur lisible
```

### La fluidité — deux causes, mesurées

```
les prénoms se replaçaient 60 fois par seconde   (6 noms × 32 essais) → 4 fois par seconde
les QUATRE cadres se repeignaient à chaque image → seuls les deux SOMBRES sont vivants
le retour vers le centre : 2,2 j → 3,5 j, lissage d'ordre 5 (aucun à-coup)
```

### ⚠ EST-CE COMPRÉHENSIBLE ? — non, pas entièrement, et je le dis

**Ce qui se lit :** le **retour vers le centre** est net — on voit qu'il se passe quelque chose,
et la jauge dit qu'on rejoue une période.

**Ce qui NE se lit pas : la dérive.** Entre deux paroles, une personne ne s'écarte que de
quelques pixels en trois secondes. **« ça s'écarte » ne se lit pas comme « le temps passe »** —
il faut le savoir. J'ai ajouté la ligne **« ces huit dernières semaines, rejouées »**, sans
laquelle rien n'est compréhensible ; elle dit qu'on rejoue, elle ne dit pas pourquoi ça s'écarte.

**Ma réserve, entière :** le rejeu demande une explication pour la moitié de ce qu'il montre.
**Le moment où le retour vers le centre se lit sans un mot, c'est celui que tu avais déjà
nommé** — une fois, à l'ouverture, quand tu reviens après avoir tenu : là on vient de tenir,
on voit la personne rentrer, et la cause est évidente parce qu'on l'a provoquée.

```
4 cadres · 0 recouvrement · 0 hors cadre · langue §6 : tout à zéro
```

---

## ⚑ L'AURA — LE REJEU OU L'IMAGE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-DEUX-SORTIES.html`**, les deux premiers
> cadres sont vivants. Captures : `scratchpad/sorties/`.

### Le diagnostic de Tom, repris à mon compte

*« Six anneaux qui tournent en boucle, à vitesse constante, sans qu'aucun événement ne se
produise : ça bouge sans rien raconter. »* **Neuf lots à affiner la finition d'un mouvement qui
n'avait pas de sujet.** C'était le mauvais problème.

### 1 · LE REJEU — le mouvement dit le temps

L'pelote **ne boucle pas** : elle rejoue les huit dernières semaines en 28 s. Chaque personne
**s'éloigne parce que les jours passent**, et **revient d'un coup vers le centre quand une
parole est tenue avec elle**. Les angles ne bougent jamais ; seule la distance respire. La lune
apparaît selon ce qui était en chemin **ce jour-là**.

### 2 · L'IMAGE — une constellation fixe

Elle ne bouge plus. **Tous les anneaux à la même taille** — la seule façon d'être sûr qu'aucune
dimension ne dise une valeur ; ce sont les **places** qui font l'image.
**Les angles sont composés à la main** (autorisé par Tom : le rayon reste la date).
**Les rayons s'ouvrent : 77 → 149** au lieu de 80 → 122 — une image fixe n'a pas de tour à
dégager. **Seule bouge la lune.**

```
la grappe   Maman 77 · Adrien 89 · Marion 108, en haut à gauche — trois distances, deux Nuées
le vide     de 78° à 205° : tout le quart bas-gauche, VOULU
le lointain Nico 149, seul, au bord — cent cinquante jours
```

### Le verdict : la 2 — mais pas pour la raison donnée

**Le rejeu ne tourne pas dans le vide** : il raconte quelque chose de vrai. **Ce qui le
disqualifie, c'est le rythme.** Quinze paroles tenues en huit semaines = quinze événements en
28 s ; entre deux, la scène ne fait que **s'écarter lentement, toutes ensemble, dans la même
direction**. Ce n'est pas une histoire, c'est une dérive. Et si rien n'a été tenu depuis un
mois, l'écran ne fait que reculer, en boucle.

**La 2 tient pour une raison plus simple : l'Aura est un ÉTAT, pas un film.** On l'ouvre pour
savoir où on en est. Une image se lit en une seconde ; un rejeu demande d'attendre.

**Ce que le rejeu mérite quand même :** le mouvement qu'il invente — **le retour vers le centre
quand une parole est tenue** — est exactement ce qui devrait se passer **à l'instant où tu
tiens**. Pas en boucle : **une fois**, quand tu reviens sur l'Aura après avoir tenu. À trancher.

### ⚠ Une règle re-cassée, et reprise

J'avais glissé **une dalle sous le visage** dans chaque anneau. Fausse deux fois : invisible, et
contraire à ce que Tom avait déjà tranché — *« une dalle est la matière d'une PROMESSE »*, pas
d'une personne, et le Noyau agrège toutes tes promesses. **Retirée partout.**

```
4 cadres · 0 recouvrement · 0 hors cadre · langue §6 : tout à zéro
```

---

## ⚑ L'PELOTE AFFINÉE — LA MATIÈRE SERT LA LECTURE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-RETENU.html`**, premier cadre **vivant**.
> Les trois directions de matière (`PLANCHE-AURA-TROIS-DIRECTIONS.html`) sont **abandonnées** —
> gardées comme trace, pas comme candidat.

### La décision de Tom, et pourquoi elle est juste

*« Le diagnostic était juste : la Pelote manquait de matière. La réponse ne l'était pas — mettre
de la trame partout a tué la lisibilité. La matière doit servir la lecture, pas la remplacer. »*

**Les trois directions étaient illisibles.** L'erreur : avoir traité « il manque de la matière »
comme « il faut remplacer les formes par de la matière ». Retour aux **anneaux nets**, et on
affine la composition au lieu d'empiler de la texture.

### Ce qui a changé

```
TON NOYAU     l'arc s'amincit PAR L'INTÉRIEUR : 26 → 18. Le bord extérieur ne bouge
              pas (anneau() trace à R = (d − lw)/2), donc les 8 px rendus vont TOUS
              au creux — et le visage retrouve sa place : 27 → 40.
LA TRAÎNÉE    discrète. Longueur 0,24 → 0,12 du tour · opacité 0,92 → 0,34 ·
              largeur × 0,52 · bouts FRANCS (les bouts ronds qui se chevauchaient
              composaient des perles : la traînée redevenait un motif qu'on regarde).
L'ANNEAU      inchangé — net et simple. C'est ce qui le rendait lisible.
LA COMPOSITION  l'écart des rayons s'ouvre : 118 → 122 (mesuré : 136 sortait du cadre
              par la gauche et mordait le plateau). Profondeur : rapport 3,48.
```

### L'idée ajoutée — et c'est une SOUSTRACTION

**La traînée s'éteint derrière.** Chaque pas est éclairé par sa **profondeur** : vif quand il
vient vers toi, presque nul quand il s'enfonce. Comme une comète.
**Ça divise le bruit par deux ET ça renforce le volume** — la moitié arrière du chemin ne se
dessine plus, elle se devine. Elle ne coûte qu'une ligne : si elle nuit à la lecture, elle sort.

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ L'AURA — TROIS DIRECTIONS DE MATIÈRE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-TROIS-DIRECTIONS.html`** — les trois
> cadres du haut sont **vivants**. Captures : `scratchpad/directions/`.

### Pourquoi le canevas de `/design` ne pouvait pas porter ce lot

**Un canevas `/design` est publié dans un artefact SANS RÉSEAU SORTANT** : il ne peut charger
ni `toile-extrait.js`, ni le moteur, ni rien du produit. Y dessiner la matière aurait voulu dire
**la refaire à la main** — exactement le défaut que Tom venait de nommer (« tu dessines la Pelote
avec les outils d'un diagramme »). Le travail est donc revenu ici, **où le vrai moteur tourne**.

### La règle du moteur que ça impose

**CLAUDE.md §4 : une dalle se rend UNE FOIS, pas une fois par case.** Chaque dalle est peinte
une seule fois dans un canevas caché, puis **tamponnée** — même pixel à toutes les tailles,
sans jamais rappeler le moteur. C'est ce qui rend une traînée de 46 pas tenable.

### Les trois directions

```
A · LES DALLES GRAVITENT   une personne n'est plus un anneau : c'est SA DALLE, du monde
                           de sa dernière parole tenue. L'arc du §2.9 devient un mince
                           CERCEAU autour d'elle. La traînée est la même dalle tamponnée
                           vingt fois — une traînée d'encre, pas un arc dégradé.
B · LA TOILE EST LE CIEL   le fond n'est pas noir : c'est une vraie Toile (Toile.preview),
                           sourde, qui respire. Les gens sont des dalles vives dedans.
                           AUCUNE traînée — le ciel EST la texture.
                           Son risque : deux matières se disputent l'oeil.
C · L'ANNEAU DE MATIÈRE    vu presque de profil, inclinaison commune à 78°. Les traînées,
                           denses (46 pas), se fondent en RUBANS de trame qui s'enroulent
                           autour du Noyau — un ruban de mosaïque, un d'encre, un de
                           terrazzo. Le plus décalé des trois.
                           Ce qu'il perd : chacun n'a plus son plan propre.
```

**Ce qui ne bouge dans aucune des trois :** le rayon dit la date · la vitesse est commune ·
la lune est binaire · la couleur est catégorielle · aucune dalle ne passe devant ton Noyau
(inclinaison cherchée, moitié avant seulement) · les prénoms restent des nœuds droits, à taille
fixe, placés par essais.

**Le Noyau revient à l'arc 20** — le pâté de 26 est corrigé — et il porte **ta dalle**.

```
6 cadres · 0 recouvrement · 0 hors cadre
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'PELOTE — LA TRAÎNÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, **premier cadre vivant**.

### L'idée : la traînée

**On ne voyait pas le VOLUME parce qu'on ne voyait pas les CHEMINS** — six objets bougeaient,
le cerveau n'avait rien à reconstruire. Chaque personne traîne maintenant **un arc de sa propre
pelote** : une trace, pas un filet.

```
elle s'affine et s'efface en s'éloignant de l'anneau
sa LARGEUR suit la perspective — fine au loin, large au premier plan
elle est peinte SOUS ton Noyau : elle disparaît derrière lui et reprend de l'autre côté
   → c'est ÇA qui dit la profondeur, mieux que la taille
elle porte la couleur de la NUÉE, comme la piste de l'anneau
```

**La lune en a une aussi**, minuscule, et tourne à **sa** vitesse — six tours quand la Pelote en
fait un. **Un point qui traîne dit qu'il tourne ; un point posé ne dit rien.**

### La profondeur, poussée et mesurée

```
foyer 420 → rapport 1,3     on voyait un cercle
foyer 230 → rapport 2,59    encore timide
foyer 180 → rapport 3,43    le plus petit 20,0 px · le plus gros 68,8 px
inclinaisons 38° à 78° · échelle bornée [0,44 · 2,15] · anneaux 36 → 32
ton Noyau reste à 90 : rien ne l'atteint jamais
```

### Le Noyau : l'arc double sans grossir

`anneau()` trace à **R = (d − lw)/2** : le bord extérieur reste à **45**, donc **tout l'ajout
mange le centre**. Arc **13 → 26**, creux **64 → 38**, visage **48 → 27**.

⚠ **À signaler : il en devient épais au point de tirer vers le disque.** C'est la conséquence
directe de l'épaisseur demandée. **L'arc à 20 garderait le geste sans le pâté** — à trancher.

### Les douze phrases sont closes

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Évidemment. · Parole tenue. · C'est bien toi. · Comme d'habitude.
Tu ne t'es pas fait prier. · On n'en attendait pas moins. · Tiens donc.
```

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ L'PELOTE — LA PROFONDEUR, MESURÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, **premier cadre vivant**.

### La cause du « cercle » n'était pas seulement le foyer

**Deux causes, et la seconde était la mienne.** Le foyer à 420 aplatissait, oui — mais surtout
**j'interdisais tout recouvrement du centre**. Les pelotes le **contournaient** : personne ne
passait jamais derrière, tout le monde restait à côté. **C'est ça qui faisait un cercle.**

**La règle corrigée : ce qui est interdit, c'est de passer DEVANT.** La recherche d'inclinaison
ne teste plus que la **moitié avant** ; derrière, ton Noyau masque, franchement.

```
foyer            420 → 230        inclinaisons 20-64° → 34-66°
anneaux          44 → 36          échelle bornée à [0,52 · 1,92]
LA PROFONDEUR    le plus petit 24,9 px · le plus gros 64,7 px · RAPPORT 2,59
                 (à 420 il valait 1,3 — on voyait un cercle)
ton Noyau        90 · rien ne l'atteint jamais
la boîte         45 · 139 → 350 · 407 — dégagée du plateau et du mot
```

⚠ **Un premier essai à foyer 170 a donné un rapport de 4,89** — et un anneau au premier plan à
**129 px**, presque ton Noyau : la hiérarchie s'effondrait et la boîte sortait du cadre.
**Bornée**, la profondeur reste franche sans rien casser.

### Les cinq réglages de mise en page

```
la Pelote descend        centre 262 → 288, et se resserre (rayons 92-140 → 80-118)
le mot et le chiffre    440 → 448 · 526 → 534
la légende              26 px d'air au-dessus, 33 en dessous
« tout ce que tu as tenu »   27 px avant les dalles, au lieu de 11
```

### ⚠ Le placement des prénoms, troisième version

Huit essais avec **repli aveugle** laissaient treize noms l'un sur l'autre. Maintenant :
**trente-deux candidats, chacun évalué par la SURFACE qu'il recouvre**, et on garde le
minimum — ton Noyau pesant quatre fois, un autre nom trois fois. La position parfaite quand
elle existe, la moins mauvaise sinon. **0 recouvrement.**

### Les douze phrases

Cinq sortent sur décision de Tom (plates ou gênantes). Cinq neuves, au calibre du clin d'œil :

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Évidemment. · Parole tenue.
C'est bien toi. · Comme d'habitude. · Tu ne t'es pas fait prier.
On n'en attendait pas moins. · Tiens donc.
```

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro · les 4 sondes du contrôle passent toujours
```

---

## ⚑ L'PELOTE EN 3D — UN SYSTÈME PLANÉTAIRE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`,
> **le premier cadre est vivant** — un tour en 48 s. Captures : `scratchpad/retenu/`.

### La mécanique

```
CHACUN SUR SON PELOTE PROPRE   un cercle 3D, à SON rayon (la date), dans SON plan.
                               Inclinaison et nœud viennent du NOM : stables.
LA PERSPECTIVE                 foyer 420. Loin = petit. Ce n'est pas une valeur :
                               la taille apparente change en permanence.
LA MÊME VITESSE POUR TOUS      un tour en 48 s.
TA HIÉRARCHIE                  toi 90 / arc 13 · une personne 44 / arc 4
                               (écart volontaire au §2.9 — c'est le soleil)
L'PELOTE RESSERRÉE             rayons 92 → 140, contre 102 → 146 avant
LA MOISSON GAGNE               3 rangées dès le premier écran (la place de « avec qui »)
```

**L'pelote remplace la grille « avec qui »** — les mêmes personnes ne peuvent pas figurer deux
fois. **On touche un anneau, ça ouvre la personne** (`openPerson`).

### ⚠ Aucun anneau devant ton Noyau — ce n'est pas une question de z-index

Une pelote trop inclinée **traverse le centre à l'écran**, quel que soit l'ordre de dessin.
Donc, pour chaque personne, **l'inclinaison est cherchée par dichotomie** : on part de celle que
son nom donne, on échantillonne **96 positions**, et on réduit jusqu'à ce que son anneau **et sa
lune** dégagent le tien. **L'inclinaison retenue est celle qui tient, pas celle qu'on voulait.**
Vérifié par le contrôle sur **72 positions** : **0 écart**.

### ⚠ Trois erreurs de ma part, toutes prises par le contrôle

1. **La lune n'était pas dans le dégagement** — un point terracotta passait devant ton Noyau.
2. **J'ai exempté trop large.** J'avais exempté « personnes entre elles », prénoms compris :
   la moitié gauche est sortie **illisible**, des noms sur des visages, sans que rien ne le
   signale. **Deux anneaux qui se croisent, c'est le sujet ; deux noms qui se croisent, c'est
   une faute.** L'exemption ne couvre plus que les anneaux.
3. **Élargir le rayon d'évitement pour la lune a fait pire** — 30 recouvrements au lieu de 3,
   parce que plus aucune position ne convenait et que le repli s'appliquait partout. La lune
   passe **derrière** le nom (z 45) : elle ne cache rien.

### Deux décisions non prévues

**Le mot « toi » est retiré.** Il occupait la bande sous ton Noyau — là où passe une personne
qui arrive par le bas. Le garder obligeait à pousser la Pelote minimale de 78 à **106 px**,
c'est-à-dire à **grossir** ce qu'il fallait resserrer. Et il ne dit rien qu'on ne voie.

**Les prénoms sont placés par essais.** Huit directions autour de l'anneau, les plus proches du
regard d'abord, première position libre retenue. **Droits, 13,5 px, aucune perspective.**

### Les douze phrases, tirées au hasard

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Tu vois. · Ça y est. · Évidemment. · Parole tenue. · Le trait s'est refermé ici.
Elle a pris sa place. · Tu es venu.
```

Et **la phrase respire** : 20 → **38 px** sous « tenue. ».

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
langue §6 : tout à zéro · les 4 sondes du contrôle passent toujours
```

---

## ⚑ L'PELOTE — LE RAYON DIT LA DATE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`
> — **vivante**, la Pelote y tourne, un tour en 72 s. Captures : `scratchpad/retenu/`.

### ⚠ J'avais appliqué la règle anti-notation trop large — correction de Tom

J'avais posé **« tout au même rayon »**. **C'était faux**, et c'était moche : un cercle de
disques équidistants est un diagramme d'atome. **Les huit règles interdisent un classement de
VALEUR, pas toute variation.** Une distance qui dit une **date** ne dit aucun mérite.

Ce qui reste vrai de mon raisonnement : **tout ce qui est continu se classe** — donc la vitesse
reste identique pour tous, et ce qui est en chemin reste **binaire** (la lune), jamais un compte.

### La loi — cinq canaux, aucun ne dit un mérite

```
LE RAYON     quand remonte la dernière parole tenue. 102 px pour hier, 146 pour six mois,
             échelle logarithmique. C'est une DATE : loin = « ça fait longtemps »,
             jamais « tu comptes moins ».
L'ANGLE      le nom. LE TOUR EST L'ALPHABET — A en haut, Z après un tour entier.
             Les grappes et les vides viennent des initiales, de rien d'autre.
LA LUNE      ce qui est en chemin. Binaire, UNE SEULE, jamais deux.
LA COULEUR   la Nuée. Catégorielle.
L'ARC        l'harmonie — §2.9, là où le produit l'a déjà mise.
LA VITESSE   la même pour tous : la constellation tourne d'un seul bloc.
AUCUN FILET  ni cercle d'pelote, ni rayon, ni trait vers le centre.
```

Rayons mesurés : **Maman 108 · Adrien 114 · Marion 124 · Rachel 131 · Léa 137 · Nico 144**.

### ⚠ Ce qui a été dur, et que je n'avais pas vu

**La constellation tourne, les prénoms restent droits.** Une mise en place sans recouvrement à
u = 0 ne l'est plus à u = 1/3. **Trois versions ont échoué** (58 recouvrements, puis 19, puis
16) avant de comprendre qu'il fallait une condition **indépendante de la rotation**. Elle est
simple : **la distance entre deux centres.** Le point le plus lointain d'un prénom est à
√(31² + 57²) ≈ 65 de son centre, un anneau peint s'étend à 29 : au-delà de **106**, plus rien
ne se touche, à n'importe quel angle. **Le contrôle balaie désormais douze positions du tour**,
plus un seul instant.

⚠ **Et le rayon ne se corrige jamais.** Une version intermédiaire le remontait pour dégager le
centre : la personne la plus récente se retrouvait **à la même distance qu'une autre** — la
donnée détruite pour arranger le dessin. Le dégagement est tenu par le rayon minimal.

### Le contrôle de collisions gagne une mesure juste (pas un assouplissement)

**Une boîte carrée n'est pas la forme peinte quand la forme peinte est un anneau.** Les canevas
d'anneau déclarent `data-forme="anneau"` et leur rayon ; le contrôle mesure alors la distance du
rectangle **au cercle**. Prouvé : les quatre sondes passent toujours (deux textes ✅, un texte
débordant ✅, une marque sur sa surface exemptée ✅, une boîte bordée ✅).

### Les phrases — les neuf, tirées au hasard, une par rejeu

```
Tu l'avais dit.  ·  Et tu l'as fait.  ·  Personne n'en doutait.  ·  Voilà.
Comme prévu.  ·  Tu vois.  ·  Ça y est.  ·  Évidemment.  ·  Parole tenue.
```

« Tu l'avais dit. » ouvre la série. Sur « Parole tenue. » : gardée sur décision de Tom ; je
maintiens qu'elle est la seule qui **constate au lieu de complicer** — un tirage sur neuf la
rend tenable.

```
6 cadres · 0 recouvrement · 0 hors cadre · 0 écart à la loi · LE TOUR ENTIER : aucun recouvrement
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'AURA — L'PELOTE REMPLACE LA FRISE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`
> — **elle est VIVANTE** : la Pelote y tourne pour de vrai, un tour en 72 s.
> Captures : `scratchpad/retenu/` (10 cadres). Décision Tom : la frise sort, la Pelote revient.

### Ce que j'ai dû dire au lieu de le maquiller

Tom demandait que **le mouvement dise la proximité et l'harmonie du lien**. **Ce n'est pas
tenable sans refabriquer le classement qu'on venait de retirer**, et je l'ai posé plutôt que de
le contourner :

**Tout ce qui est CONTINU se classe.** Le rayon (le défaut de l'audit), mais aussi la vitesse,
l'amplitude, la taille, l'opacité, l'épaisseur. Dès qu'une propriété prend des valeurs graduées,
deux personnes peuvent être rangées — **même sans chiffre à l'écran**.

**Ce qui ne se classe pas est BINAIRE ou CATÉGORIEL.** Le mouvement ne peut donc pas dire un
*degré* d'harmonie. Il dit un **état** : **qui a une parole en chemin, et qui n'en a pas.**
Deux personnes qui ont quelque chose en chemin bougent **exactement pareil**.

### La loi de la Pelote — six règles, et le contrôle les mesure

```
1 · TOUS AU MÊME RAYON          132 px · mesuré : 131,99 → 132,01 sur les cinq
2 · TOUS À LA MÊME VITESSE      un tour en 72 s, la constellation tourne D'UN BLOC
3 · CE QUI VARIE EST BINAIRE    une LUNE terracotta tourne autour de qui a une parole
                                en chemin. UNE SEULE, jamais deux — ce serait un compte.
4 · LA COULEUR EST CATÉGORIELLE la piste porte la Nuée, jamais une valeur
5 · L'HARMONIE RESTE DANS L'ANNEAU   l'arc menthe du §2.9, là où le produit l'a déjà mise
6 · AUCUN FILET                 ni cercle d'pelote, ni rayon, ni trait vers le centre
```

Anneaux au **§2.9 à la lettre** : toi 78 / arc 8 / photo 48 · une personne 58 / arc 6 /
photo 36 · prénom Bricolage 600 / 13,5. Ordre alphabétique — **un cercle n'a pas de début :
placer alphabétiquement répartit, ça n'ordonne pas.**

### ⚠ Le premier dessin de la Pelote était faux, et le contrôle l'a pris

Première version : ceux qui avaient une parole en chemin **avançaient**, les autres restaient.
**Ils se percutaient** — mesuré, deux anneaux à **31 × 31 px** de recouvrement et un prénom
sous un visage. Et un recouvrement entre deux personnes, c'est **l'une devant l'autre** :
encore un rang.

**Correctif : les places sont FIXES, la constellation tourne d'un seul bloc**, et le binaire
passe dans **la lune**. Les écarts angulaires ne changent jamais.

### ⚠ Une troisième exemption au contrôle de collisions — et elle est prouvée

La lune passe au-dessus du **carré** du canevas de son propre anneau (elle dégage le cercle de
4,5 px ; c'est la boîte qui la croise dans son coin). **Deux parties du même objet ne se
percutent pas, elles se composent** : on exempte les nœuds qui partagent le même
`[data-role]`, **et eux seulement**.

```
scratchpad/preuve_collisions.py — quatre sondes, après l'exemption
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une marque sur sa surface          exemptée ✅
  4 · une boîte BORDÉE sur une dalle     PRIS ✅
```

### Les phrases du rejeu

« Tu l'avais dit. » retenue. Sur les quatre de Tom : **« Parole tenue. » est la seule faible** —
ce n'est pas un clin d'œil, c'est une **étiquette**, et c'est déjà le libellé d'état écrit
partout ailleurs. Les trois autres tiennent.
Quatre de plus, même calibre : **« Comme prévu. »** · **« Tu vois. »** · **« Ça y est. »** ·
**« Évidemment. »**

```
10 cadres · 0 recouvrement · 0 hors cadre · 0 écart à la loi de la Pelote
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'AURA — LA FRISE, SES ALTERNATIVES, ET LA PRÉSENCE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (13 cadres, regardés un par un à 2×).
> **Le 4ᵉ argument de `dalleTrame` sert ici pour la première fois** : chaque dalle de la
> frise et de la moisson est peinte dans son monde d'alors.

### 1 · La frise — reprise, et trois alternatives dessinées

**Les deux causes étaient justes.** Les dalles étaient génériques : elles sont maintenant
chacune la sienne, à sa **vraie date**, dans son **monde d'alors** — la frise traverse
**deux changements de monde en huit semaines** et ça se voit.

**Ce qui rend le temps lisible, sans graduation ni chiffre :** la réponse était dans l'objet.
**L'onde fait huit ondulations — une par semaine.** C'est la ligne du produit qui respire au
rythme du calendrier. Plus l'espacement **irrégulier** : le rythme est l'information, un creux
de treize jours se voit sans qu'on l'écrive.

```
0 · LA FRISE REPRISE   une ondulation = une semaine        118 px
A · LE RUBAN PLIÉ      trois lignes, 3 × le rythme          194 px
B · LA SPIRALE         un tour = un mois                    214 px
C · LE FIL DES JOURS   un point par jour, 57 points          96 px
```

⚠ **J'avais recommandé « 0 ou A » AVANT de les regarder à 2×. Après les avoir vues, je change
d'avis : c'est C.** Il est le plus informatif d'un coup d'œil — longueur, grappes, silence,
jours ouverts — **et le seul qui ne coûte rien** : à 96 px, « avec qui » reste sur le premier
écran. **A coûte « avec qui »**, et son cadre le montre. **B est la plus belle et la moins
lisible** : le sens de lecture ne se devine pas, le centre s'encombre (deux effleurements
mesurés), et « il y a 8 semaines / aujourd'hui » n'a plus de sens sur une spirale.

**La frise garde sa place**, pour deux raisons que la moisson ne peut pas porter : **le rythme**
(la moisson dit *quoi*, la frise dit *quand*, donc les creux) et **ce qui n'est pas encore
tenu** — les points terracotta sous la ligne. La moisson ne contient que du tenu, par définition.

### 2 · Le chiffre — il ÉTAIT en Fraunces, et c'est pour ça qu'on ne le voyait pas

Vérifié **aux pixels**, pas au style calculé : on compare la largeur d'encre du nœud réel au
même texte rendu dans chacune des six faces embarquées.

```
« 82 » à 24 px / 600      largeur réelle 27,66 px
  écart à Fraunces    0,48   ← la face rendue
  écart à ApfelMid    2,07 · Apfel 2,60 · Bricolage 2,68 · serif 3,66
```

**Le problème n'était pas la face : à 24 px son dessin ne se voit pas, et en crème il se fond.**
**34 px et sa couleur d'état** — menthe ≥ 65, periwinkle 40-64, terracotta en dessous, **mêmes
seuils que le mot** : la couleur et le mot ne peuvent pas diverger.

### 3 · La présence — structure inchangée, trois leviers

```
ce qui est gros l'est plus   le mot 52 → 64 · le Noyau 118 → 134 (trait 38) · le chiffre 24 → 34
ce qui est petit disparaît   « TA PAROLE DANS LE TEMPS » retiré — le plateau dit déjà « Aura »
                             et ce sous-titre ne portait aucune information. Réversible.
l'espace se creuse           sous le plateau 22 → 50 · autour du mot 12 → 22
                             avant la frise 26 → 31 · avant « avec qui » 21 → 39
```

### 4 · Les phrases du rejeu

« Tu l'avais dit. » retenue. Trois autres du même calibre — deuxième personne, passé, nues,
aucune mesure, aucune félicitation : **« Tu es venu. »** · **« C'était une promesse. »** ·
**« C'est toi qui l'as tracée. »**

### Ce que le contrôle a trouvé, et que l'œil n'aurait pas vu

⚠ **Trois paroles tenues dans la même semaine se couvraient l'une l'autre** — 43 dalles prises.
Une grappe doit se voir **comme une grappe**, pas comme une dalle unique : `ecarte()` garde
l'ordre et la date et écarte au minimum (D+2).

⚠ **Le message du contrôle confondait deux défauts très différents** : l'ONDE qui passerait
devant (interdit) et une DALLE VOISINE qui déborde (un défaut d'écartement). **Il nomme
désormais le coupable.** Aucune occurrence de « L'ONDE ❌ INTERDIT » : l'onde ne passe jamais
devant une dalle.

⚠ **`ecarte()` recompressait ce qu'il venait d'écarter** — six effleurements de 2 px. On décale
le **peigne entier**, et on le clampe dans la boîte du trait : sinon la première dalle sortait
de sa frise par la gauche — invisible à l'œil, mais le contrôle avait raison de la voir.

```
13 cadres · 0 hors cadre · 0 onde devant une dalle
recouvrements : 2, tous deux sur LA SPIRALE (8×2 et 6×5 px) — sa faiblesse, mesurée
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ LE MONDE D'ALORS — LE MOTEUR EST TOUCHÉ · 4 septembre 2026

> **Feu vert explicite de Tom.** Première modification du moteur de la Toile depuis
> l'interdit du §9. Sauvegarde d'avant : **`sauvegardes/avant-monde-fige.html`**.
> Planche : `PLANCHE-AURA-RETENU.html` · captures `scratchpad/retenu/` (8 cadres).

### Ce qui a changé — trois endroits, et pas un de plus

```
1 · dalleTrame prend un 4e argument FACULTATIF        {m:design, p:palette, h:teinte}
    sauvegarde/restauration de theme, palKey, hueShift ET _palLit,
    sur l'idiome que la fonction porte déjà pour g/W/H/seeds/view.
2 · Toile.mondeCourant()                              accesseur en LECTURE SEULE
3 · la fabrique P() fige mondeDuJour() sur chaque Promi
    + window._figeMondesManquants(), passe de rattrapage IDEMPOTENTE,
      appelée au chargement ET dans loadState()
```

⚠ **`_palLit` était le piège.** C'est un **mémo** de la palette calculée, invalidé par
`setPalette`/`setHue`. Sans l'invalider à l'aller, la palette de l'appelant fuit **dans** la
dalle ; sans le restaurer au retour, celle de la dalle fuit **dans la Toile**. Il est dans la
liste de sauvegarde au même titre que `theme`.

**Huit sites plantent un Promi ; tous passent par la fabrique `P()`.** On l'a patchée elle,
jamais les huit — c'est le seul point où un Promi naît.

**Les Promi déjà plantés** (jeu de démonstration comme `promi_state` sauvegardé avant ce lot)
prennent **le monde courant, figé maintenant** — décision Tom. **Rien n'est tiré de leur date :
on n'invente pas un passé qu'on n'a pas.** La moisson sera uniforme jusqu'à aujourd'hui puis se
diversifiera, c'est ce que verrait quelqu'un qui commence.

### La preuve — quatre contrats, `scratchpad/preuve_monde.py`

```
1 · SANS le 4e argument, rien ne change            deux relevés identiques ✅
2 · AVEC, la dalle sort dans le monde demandé      3/3 dalles diffèrent, sur 3 mondes ✅
3 · AUCUNE FUITE : la Toile est intacte après      encre|signal|0 → encre|signal|0 ✅
    et la dalle sans argument redonne la même      ✅
4 · chaque Promi porte un monde, rattrapage idempotent   0 sans monde, 0 touché au 2e passage ✅
0 erreur de page
```

### Les batteries, EN SÉRIE

```
releve-design    ✅ AUCUN ÉCART        ← le contrat visuel, intact
redteam_ecrans   150/150               redteam_toile  17/17     redteam_formes 38/38
redteam_vide      61/61                redteam_champ  32/32     redteam_nuee   24 écrans / 0
redteam_air      ✅ 428 paires
releve-S1 ✅ · S2 ✅ 0·0·0·0·0 · S3 ✅ · S4 ✅ · S5 ✅
```

⚠ **`redteam_tonsurton` a donné 22/26 puis 26/26.** Le premier passage suivait
`redteam_formes` dans la même boucle : la machine n'avait pas rendu la main. **Reconfirmé
seul : 26/26.** C'est le flottement documenté au §7, pas une régression — mais je le dis.

**`releve-design.py --figer` n'a PAS été lancé.** La référence est intacte et sans écart,
ce qui est attendu : **rien de ce lot n'est encore branché sur un rendu.** Le moteur gagne
une capacité, la donnée gagne un champ, aucun pixel ne bouge. Câbler les peintres de dalles
(Aura, Index, Fil) est le lot suivant, et il aura son propre avant/après.

### Les cinq corrections de dessin, sur la planche

```
1 · l'anneau : trait 13 → 33 (× 2,5)   à 13 il faisait diagramme
    ⚠ les anneaux des PERSONNES n'ont pas bougé — le §2.9 leur donne 6 sur 58 (10 %).
      Les épaissir imposerait de descendre le visage de 36 à 32. En attente.
2 · sous le plateau       14 → 22 px
3 · autour du Noyau       13 → 21 au-dessus · 12 → 18 en dessous
4 · autour du mot          8 → 12 sous « solide » · 20 avant la légende
5 · la phrase du rejeu — trois propositions, en attente de ta décision :
      « Tu l'avais dit. »              c'était une parole avant d'être une dalle
      « Le trait s'est refermé ici. »  les mots du cadre 97, le souvenir situé sans date
      « Elle a pris sa place. »        parle de la dalle, pas de toi
```

⚠ **La dalle du rejeu sortait minuscule** : je forçais une hauteur de 190 sur un canevas
carré, et `dalleTrame` **recadre au plus juste sur l'alpha** — la forme était écrasée.
Carré, jamais étiré.

```
8 cadres · 0 recouvrement · 0 hors cadre · 0 onde devant une dalle
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
air : 0 paire sous 10 px
```

---

## ⚑ L'AURA — LA MOISSON, LE REJEU, L'ONDE DERRIÈRE · 4 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (6 cadres, regardés un par un à 2×).

### ⚠ LE POINT BLOQUANT — le moteur ne sait pas repeindre une dalle dans son monde d'alors

**Vérifié avant de toucher, comme demandé. La réponse est NON, et je n'ai touché à rien.**

```
un Promi ne porte AUCUN champ de monde          Object.keys(p) n'en a pas
theme · palKey · hueShift                        trois variables de MODULE, globales
la même dalle 125, repeinte :
   encre     remplissage 4289   boîte 176 × 138
   mosaïque  remplissage 3963   boîte 178 × 200
   terrazzo  remplissage 1912   boîte 122 × 124
```

Ce n'est pas une nuance : **la forme, la densité et les tons changent.** Changer de monde au
Studio repeint **toute** la Toile, les anciennes dalles comprises. La règle « la dalle est
figée à la plantation » **n'existe pas encore dans le code**. Mesure : `scratchpad/monde_fige.py`.

**Ce que ça demande, en deux morceaux — le premier touche le moteur (§9) :**

1. **`dalleTrame` prend un 4ᵉ argument facultatif**, sur l'idiome de sauvegarde/restauration
   que la fonction porte **déjà** pour `g, W, H, seeds, view` : on y ajoute
   `theme, palKey, hueShift`. **Quatre lignes.** Aucun des six appels existants ne bouge —
   `dalleTrame(cv,id,1)` se comporte exactement comme aujourd'hui.
2. **Un champ `{m,p,h}` posé sur le Promi à la plantation**, dans `addP()` — hors moteur,
   c'est du produit. **Question ouverte que je ne peux pas trancher :** les Promi déjà plantés
   n'en ont pas. Que voient-ils ?

**En attendant, la planche montre la moisson pour de vrai** en basculant le monde et la palette
**autour de chaque peinture** — emploi en **lecture seule** de l'API publique
(`setTheme` / `setPalette`), aucun code du moteur modifié. **Non viable dans l'app** (chaque
bascule repeint toute la Toile), mais ça prouve que le rendu sait faire.

### Ce qui est décidé et dessiné

```
la frise    SORTIE B — l'onde derrière, les dalles à hauteur constante.
            Le trait plat est écarté : sur cet écran il ressemble à un filet.
            ⚠ L'ONDE NE PASSE JAMAIS DEVANT UNE DALLE — vérifié AU DOIGT, dalle
            par dalle, deux thèmes : 0 écart. Chaque dalle est au premier plan,
            opacité 1, filtre none, fusion normal.
la moisson  bloc permanent, chaque dalle dans le monde ET la palette de son jour.
            Taille égale (44, pas de 50) · chronologique, la PLUS RÉCENTE EN
            PREMIER · aucun chiffre, aucun compte, aucun libellé de quantité.
le rejeu    un doigt sur n'importe quelle dalle rejoue sa seconde — cadre 98,
            « tenue. » puis « Le dessin existe. ». Zéro pixel au repos.
P1          SORTI — doublon avec la moisson, qui contient déjà la dernière.
le chiffre  dérivé de l'anneau. Une seule source pour l'anneau, le chiffre, le mot.
```

**Le rognage des dalles n'en est pas un.** Les bords droits qu'on voit sur les dalles d'encre
sont **les frontières de la cellule de Voronoï**, pas une coupe : mesuré, la part du bord opaque
est **identique à 44, 88 et 176 px** (encre 7 % · terrazzo 2 % · mosaïque 13 % · braille 5 % ·
pixel 7 %). `scratchpad/rognage.py`. J'allais signaler un défaut qui n'existe pas.

### ⚠ MON OUTIL DE COLLISIONS — deux angles morts, tous deux prouvés

**1 · `elementsFromPoint` travaille en coordonnées de FENÊTRE.** Les cadres hors de la fenêtre
rendaient une liste vide : l'outil annonçait « 0 » sur des cadres qu'il n'avait pas regardés.
**Tous les « 0 recouvrement » antérieurs de ce projet sont partiels.** Inscrit dans
`CLAUDE.md §8`. Parade : chaque cadre entre dans la fenêtre avant d'être interrogé.

**2 · Il ne regardait que les FEUILLES.** Le bouton « Partager mon Noyau » chevauchait la
dernière rangée de la moisson et l'outil n'a rien dit : un bouton bordé porte un `<span>`, ce
n'est donc pas une feuille. **Une boîte peinte compte, même si elle a des enfants.**

```
scratchpad/preuve_collisions.py — quatre sondes, quatre verdicts
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une dalle DANS la frise            exemptée ✅   (marque sur sa surface)
  4 · une boîte BORDÉE sur une dalle     PRIS ✅       ← l'angle mort n° 2
```

### Ce qui est mesuré sur la planche

```
6 cadres 390 × 844, échelle 1, regardés un par un à 2×
recouvrements confirmés AU DOIGT, cadre par cadre    0
hors cadre                                           0
l'onde devant une dalle                              0
langue (§6)  0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre
             0 graisse hors des six faces · 0 ton sur ton
```

---

## ⚑ L'AURA — LA FRISE, LE CHIFFRE, LA CÉLÉBRATION · 3 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (9 cadres, regardés un par un à 2×).

### 1 · La frise ondulait — le reproche était juste, et mesuré

**Mon propre commentaire disait « la ligne ne code aucune valeur » et mon code dessinait
`per: 1.5` avec une enveloppe.** Mesuré : **une dalle sur une crête est posée 30 px plus haut
qu'une dalle dans un creux**. Sur un écran qui annonce huit semaines, l'œil lit une hauteur.

Deux sorties dessinées et mesurées côte à côte — `window._friseY` publie la position verticale
des dalles, mode par mode :

```
aujourd'hui · per 1.5, la dalle suit la courbe    écart 30,0 px   ← le défaut
sortie A · le trait plat                          écart  0,0 px   bloc 118 → 96
sortie B · l'onde derrière, dalles constantes     écart  0,0 px   l'onde reste
```

⚠ **`0 || 16` vaut 16.** Le premier jet du « trait plat » ondulait encore : `amp=o.amp||16`
avalait l'amplitude nulle, et **les sorties A et B sortaient identiques**. Une amplitude nulle
est une valeur, pas une absence.

**Sortie A implique un écart au §5** (« courbes quadratiques, jamais de segments droits ») :
le §5 gouverne **le geste**, celui qu'on trace au doigt ; la frise n'est pas le geste. Le tracé
reste quadratique dans le code, ses points sont colinéaires. **Signalé, pas caché.**

### 2 · Le chiffre est dérivé de l'anneau

C'était une incohérence de **données**, pas de dessin : l'anneau posé à 62 / 24 / 14, le
chiffre écrit **67** à la main — **15 points d'écart**. Désormais une seule source :

```
PARTS = {tenu:62, encours:24, rate:14}
  → les trois arcs de l'anneau
  → harmonie = 62 / (62+14) = 82
  → harmonyWord(82) = « solide »   (la fonction de l'app, recopiée mot pour mot)
```

### 3 · Célébrer sans mesurer — trois propositions, à trancher

**Le produit avait déjà les mots.** Le **cadre 98** de l'instant écrit **« tenue. »**
(Bricolage 700/64) puis **« Le dessin existe. »** (Bricolage 600/20). Rien n'a été inventé.

```
P1 · LE DESSIN EXISTE   un bloc permanent : ta dernière parole tenue, sa vraie dalle,
                        son jour, la phrase du cadre 98. Coût mesuré : 142 px, et
                        « avec qui » tient ENCORE — seul le bouton passe sous le pli.
P2 · LE REJEU           rien au repos ; un doigt sur une dalle rejoue l'instant.
                        Coût : ZÉRO pixel. Ajout validé hors inventaire (§5).
                        Son défaut : rien ne l'annonce.
P3 · LA MOISSON         toutes les dalles tenues, ensemble, à taille égale.
                        DÉCONSEILLÉE par moi : une matière qui s'épaissit est un
                        compteur déguisé — le piège qu'on vient de retirer du trait.
```

**Recommandé : P2 + P1.** P1 résout le seul défaut de P2 — il annonce que les dalles sont
vivantes.

### ⚠ MON OUTIL DE COLLISIONS ÉTAIT À MOITIÉ AVEUGLE — et je l'ai prouvé

**`document.elementsFromPoint` travaille en coordonnées de FENÊTRE.** Une planche fait
plusieurs milliers de pixels de haut : **les cadres du bas sont hors de la fenêtre, et la
confirmation au doigt y rend une liste VIDE — donc aucun recouvrement, jamais.** L'outil
annonçait « 0 » sur des cadres qu'il n'avait pas regardés. **Tous les « 0 recouvrement » des
livraisons précédentes sont donc partiels.**

Trouvé en essayant de prouver une AUTRE correction : deux textes superposés à dessein dans un
cadre du bas **n'étaient pas pris**. C'est exactement le §8 — *avant d'accuser le dessin, on
vérifie l'instrument*.

**Deux correctifs, et une preuve :**
1. **On amène chaque cadre dans la fenêtre** (`scroll_into_view_if_needed`) avant de
   l'interroger, cadre par cadre.
2. **Une marque posée sur sa surface n'est pas un recouvrement** — une dalle peinte sur la
   frise, un visage tracé dans son anneau. On n'exempte QUE la containment géométrique, et
   seulement sur un canevas ou un SVG : un texte qui **déborde** d'un canevas reste pris,
   deux textes restent comparés intégralement.

```
scratchpad/preuve_collisions.py
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une dalle DANS la frise            exemptée ✅
```

**Et il a trouvé un vrai défaut au passage :** les deux repères de la frise étaient deux boîtes
empilées — « aujourd'hui » faisait **342 de large** et passait sous « il y a 8 semaines ». Les
glyphes ne se touchaient pas ; les boîtes, si. Chacun fait désormais **165**.

### Ce qui est mesuré sur la planche

```
9 cadres 390 × 844, échelle 1, regardés un par un à 2×
recouvrements confirmés AU DOIGT, cadre par cadre    0
hors cadre                                           0
langue (§6)  0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre
             0 graisse hors des six faces · 0 ton sur ton
air          1 paire sous 10 px — « solide » → « 82 », le couple mot/qualificatif, voulu
```

---

## ⚑ L'AURA — LE PARTI A EST RETENU ET CORRIGÉ · 3 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (7 images, regardées une par une à 2×).
> **`releve-S2` est réparé et de nouveau au vert** — voir plus bas, c'est le point important.

**Décision Tom : A · le trait déroulé, avec le mot de B greffé.** Trois corrections demandées,
une quatrième proposée, une simplification :

1. **Le centre de l'anneau est nu** — plus de dalle, et plus de visage non plus (« c'est l'arc
   qui parle » ; un visage y parlait autant qu'une dalle). Les anneaux des **personnes**
   gardent leur visage : là il désigne quelqu'un.
2. **Le chiffre en Fraunces 600** — face embarquée, `document.fonts.check` la confirme chargée
   et ses métriques diffèrent du repli (26,47 px contre 24,00 sur « 67 ») : elle n'est pas
   substituée en silence. Le mot « harmonie » reste en ApfelMid 500.
3. **Le mot passe à Bricolage 700 / 52** (au lieu de 34).
4. **PROPOSÉ — les anneaux des personnes ne se doublent PAS avec le Cercle.** Un second anneau
   par personne est **un agrégat par personne, doublé** : la règle 4 enfreinte au moment même
   où on prétend la servir. **Sur l'Aura la réciprocité est GLOBALE — elle vit dans les deux
   moitiés du trait, et nulle part ailleurs.**
5. **Simplification :** « TES HUIT DERNIÈRES SEMAINES » disait ce que les repères sous le trait
   disent déjà. Retiré. Les **30 px** rendus sont ce qui permet au mot de passer à 52.

**`#kEvolve` est ressuscité** — l'évolution Nuée par Nuée, que l'app composait en entier et
jetait faute de nœud. Elle revient **en frises, jamais en rangées** : pas un taux, pas une
barre, pas un ordre de valeur. Elle vit sous le pli, avec le Cercle (3ᵉ cadre de la planche).

**Le mot du Noyau : vérifié, aucun n'est un reproche.** L'échelle est monotone et le cas le
plus bas (« naissante ») est le plus généreux. Une réserve mince, écrite dans `QUESTIONS.md ·
Q165 bis` : « à tisser » est une consigne, pas une description.

### `releve-S2` — l'oscillation est éteinte, et ce qu'elle cachait est corrigé

Le juge posait un **délai fixe** (1100 + 700 ms) puis mesurait. Le Peaufiner d'une **Nuée**
sortait alors à **0 × 0** une fois sur deux — et **le thème fautif changeait d'un passage à
l'autre**. Un délai ne gagne pas une course.

**Correctif : le juge attend une CONDITION, plus une durée** (`POSE` — la liste a sa largeur,
ses blocs ont une hauteur), **puis exige deux relevés identiques**.

⚠ **Et la première version de ce correctif m'a eu.** L'empreinte de stabilité ne prenait que
**la géométrie** : le juge repartait « posé » alors que le **plancher typographique** n'était
pas encore passé, et annonçait **30 à 39 écarts de style — pas les mêmes d'un passage à
l'autre**. L'oscillation avait simplement changé de colonne. **Une empreinte doit couvrir tout
ce que le juge compare** : elle prend désormais la géométrie ET le style.

```
trois passages consécutifs   ✅ position 0 · style 0 · collisions 0 · hors cadre 0 · peinture 0
preuve qu'il MORD encore     scratchpad/preuve_S2.py → ❌ style 6 sur un défaut fabriqué
```

La preuve est **empaquetée et auto-nettoyante** : elle copie l'app, y pose une sonde (un
libellé à 9 px, décalé de 40), relance le juge dessus, et efface tout.
Original : `sauvegardes/releve-S2-peaufiner-avant-attente-posee.py`.

### Ce qui est mesuré sur la planche retenue

```
7 cadres 390 × 844, échelle 1, deux thèmes, regardés un par un à 2×
recouvrements confirmés AU DOIGT   4 — les DEUX du §3.8 (l'encart sur sa scène), × 2 thèmes
hors cadre                          0
langue (§6)                         0 sous 12 px · 0 opacité sous 72 % · 0 dégradé
                                    0 ombre · 0 graisse hors des six faces · 0 ton sur ton
dalles                              VRAI moteur (Toile.dalleTrame, échelle 1)
```

**Les dix-neuf lignes de texte des trois écrans sont listées dans `QUESTIONS.md · Q165`**,
neuves et existantes séparées — douze sont neuves.

---

## ⚑ L'AURA ET LE CERCLE — AUDIT FAIT, TROIS PARTIS POSÉS · 3 septembre 2026

> **`app.html` n'est PAS touché.** Ce lot est un audit et trois planches, à juger avant tout code.
> Planche : `PLANCHE-AURA-TROIS-PARTIS.html` (servie en 8752) · Audit : `AUDIT-AURA-CERCLE.md`
> Outils : `scratchpad/aura_audit.py` · `scratchpad/cap_partis.py` · `scratchpad/juge_partis.py`
> · `scratchpad/air_partis.py` · captures : `scratchpad/partis/` (11 images, regardées une par une)

### Ce que l'audit a trouvé — six blocs morts et une porte manquante

**Mort dans les DEUX modes** (passer premium ne les rend pas) : `#kEvolve` et `#plusCta`
**absents du DOM** alors que le JS les alimente encore (l'évolution par Nuée est composée en
entier et jetée ; le gestionnaire d'achat est inatteignable) · `#kStats` (en cours · résolues ·
**série**) · `#kLegend` — **le graphe n'a donc aucune légende** · `#kPct`/`.kbig` (le grand
chiffre, doublon de celui du Noyau) · `.klabel`.
**La porte manquante :** la fiche d'aide annonce en gratuit « Partager mon Noyau » ; le mode
existe côté partage, **l'Aura ne porte aucun bouton** (`#auraScreen [class*=share]` → 0 nœud).

**Six des huit règles anti-notation sont enfreintes, et cinq le sont en GRATUIT** — dont
`#ksocial` qui écrit un taux **par personne** en 8 px, et dont le **rayon de la Pelote encode la
valeur** : un classement dessiné sans être écrit. Le détail, règle par règle, est dans l'audit.

### Trois partis, un par SUJET — le fork n'est pas la forme

L'exercice a **échoué au premier tour**, et c'est écrit sur la planche : opposer « la
constellation » et « la page de mots » au trait déroulé donnait des concepts qui **coexistent**
(un trait en tête, une constellation dessous — c'est l'Aura d'aujourd'hui). Le fork est **la
seule question à laquelle l'écran répond** :

```
A · LE TRAIT DÉROULÉ   « d'où je viens »   une DURÉE      le trait porte le temps, les dalles
                                                          se plantent dessus, les points dessous
B · LA PIERRE          « où j'en suis »    un INSTANT     un seul objet, un mot, une phrase
C · LA TABLÉE          « avec qui »        une COMPAGNIE  toi puis les tiens, anneaux égaux
```

**Recommandé : A, avec le haut de B greffé** (le mot, gros, sous le Noyau).
**Passent au Cercle :** les graphes (évolution · répartition · composition), les commentaires
sur la hausse, et la réciprocité. **Reste gratuit :** le Noyau, le mot, la frise, la grille
d'anneaux sans chiffre, le partage du Noyau.

### La page du Cercle — une seule, pour les trois partis

Elle **montre** au lieu de dire : la scène voilée à **2,4 px** avec l'encart **net** posé
dessus (§3.8, la seule superposition autorisée), puis trois vignettes voilées légendées.
Le prix s'écrit **29 € · soit 2,42 €/mois · −39 %**, l'année en primaire. Aucun ✦ ne sort de
l'appareil : l'audit a vérifié que le partage n'en porte aucun, et rien n'en ajoute.

### Ce qui est mesuré sur la planche

```
11 cadres 390 × 844, échelle 1, deux thèmes, regardés un par un à 2×
recouvrements confirmés AU DOIGT   4 — les DEUX du §3.8 (l'encart sur sa scène), × 2 thèmes
hors cadre                          0
langue (§6)                         0 texte sous 12 px · 0 opacité sous 72 % · 0 dégradé
                                    0 ombre · 0 graisse hors des cinq faces · 0 ton sur ton
air entre deux textes               4 paires sous 10 px — toutes VOULUES (l'encart 3 px, le prix 6 px)
dalles                              peintes par le VRAI moteur (Toile.dalleTrame, échelle 1)
```

⚠ **`releve-S2` n'est pas au vert sur cette machine.** Deux passages **en série** donnent
`position 29 · style 0 · hors cadre 2`, et **le thème fautif change d'un passage à l'autre** :
le Peaufiner de la Nuée sort mesuré **0 × 0**, il ne s'est pas ouvert à temps. C'est une course
de construction dans le juge, pas une régression de l'app. **`style 0` dans les deux passages :
la correction des sept libellés à 13 est bien en place.** Signalé, pas réglé.

⚠ **Les mots des planches sont NEUFS pour la plupart** — dix-sept, listés un par un dans
`QUESTIONS.md · Q165`, tous **à valider**. Une seule vraie question ouverte : le mot du Noyau
(« solide ») est-il le mot juste, ou un jugement déguisé ?

---


## ⚑ DEUX CORRECTIONS AVANT LE CHANTIER AURA / CERCLE — 3 septembre 2026

> Point de reprise : **`sauvegardes/lot-entete-index-fil.html`**
> Sauvegardes d'étape : `sauvegardes/avant-libelles-13.html` · `sauvegardes/avant-entete-index-fil.html`

⚠ **Le point de reprise annoncé `sauvegardes/lot-passe-finie.html` était en retard d'un lot.**
`app.html` était identique à `sauvegardes/lot-rythme-fiche.html` (le lot du rythme sous le
trait, Q163). Je suis parti de l'app telle qu'elle était, pas de `lot-passe-finie` : repartir
de là aurait perdu ce lot.

### 1 · `releve-S2 · style 12` est levé — les sept libellés à 13

Le dernier rouge du projet. **La cause n'était pas la feuille de style, c'était un repli du
plancher typographique** : sa loi `max(13, taille)` posait bien 13 sur les sept libellés, et
un repli le reprenait aussitôt sur cinq. Ce repli protège un texte qui, en grossissant,
recouvrirait le bloc placé **sous** lui ; son test comparait le bas du texte au haut du frère
suivant **sans vérifier que ce frère est dessous**. Dans une **rangée flex** le frère est **à
côté** — les boîtes se chevauchent verticalement par construction, la condition est vraie
d'emblée, et le libellé redescendait à sa butée de 12 sans qu'aucun recouvrement n'existe.
Dans une **zone** (pile verticale), le repli ne se déclenchait pas : NOTE, COMMENTAIRES et
DESCRIPTION gardaient 13. D'où **deux tailles pour sept libellés de même nature**.

La garde est **géométrique, pas une classe** : le frère ne compte comme « dessous » que s'il
commence dans la moitié basse de la boîte, ou plus bas. Relevé : **24 nœuds du produit**
étaient retenus à 12 sans avoir de voisin dessous.

**Le §6 tranche contre le cadre** — décision Tom : *« ils doivent être identiques, et le §6
interdit 11,5. Ce n'est pas le cadre qui gagne, c'est la loi. »* Erreur de dessin recensée
dans `ECARTS-MOODBOARD.md § 0 bis.4`. Contrat `releve-S2` mis à jour (13 au lieu de 11,5,
tolérance inchangée), **prouvé contre la version fautive : 36 écarts avant, 0 après**.
⚠ Une première sonde a été **avalée** — une règle CSS ne peut rien contre l'inline
`!important` que le plancher écrit ; la preuve s'est faite en rejouant le juge sur la
sauvegarde d'avant.

### 2 · L'air sous l'entête de l'Index et du Fil : 24 → 16

Signalé par Tom sur capture. Le 24 venait du cadre 72 (titre finissant à 84, barre à 108) et
avait été reporté tel quel quand le plateau de 60 a remplacé le titre de 44. **Ce 24 était
l'air d'un titre NU** ; le plateau est une **boîte bordée**. Deux boîtes bordées de la même
grammaire prennent l'**écart de bloc du §3.3 — 16 px**.

```
la barre  .ix-bar     124 → 116        la liste  #indexList/#feedList   212 → 204
le menu de tri        186 → 178        tout ce qui suit remonte de 8
```

Recensé dans `ECARTS-MOODBOARD.md § 0 bis.5`, inscrit dans `PROMI-SPECIFICATIONS §5`.
`releve-S4` mis à jour (116 / 204), **prouvé : 18 écarts sur la version d'avant, 0 après**.

### L'état des batteries après les deux lots

```
releve-S2  ✅ 0 · 0 · 0 · 0 · 0     ← LE DERNIER ROUGE DU PROJET EST LEVÉ
releve-S1  ✅   releve-S3  ✅   releve-S4  ✅   releve-S5  ✅   redteam_nuee  ✅ 24/0
releve-design  ✅ AUCUN ÉCART       redteam_ecrans 150/150     redteam_vide 61/61
redteam_superpo 0 recouvrement      redteam_polices 0 absent
redteam_air ✅ 428 paires           ← refigée DEUX fois, et chaque fois pour la même raison
```

⚠ **`redteam_air` a été refigée deux fois, et je le dis en propres termes.** Les deux fois,
le resserrement est la conséquence arithmétique du changement demandé, jamais un
desserrement : **10 paires à −1 px** entre deux libellés consécutifs (un libellé grandi d'un
pixel vers le bas, le bloc suivant à cote fixe — c'est le §8, « une cote dérivée n'est pas un
espace »), puis **5 paires à −8 px**, toutes « ✕ Fermer → ⇅ », c'est-à-dire la rangée
déplacée et rien d'autre. Aucune autre paire n'a bougé dans l'un ou l'autre cas.

⚠ **`releve-design.py --figer` n'a PAS été lancé** — la référence est intacte et sans écart.

---

## ⚑ LE STUDIO EST REPENSÉ — 1er septembre 2026

**Le pinceau a quitté le Studio.** Un choix de Studio s'appliquait à toutes les fiches d'un
coup : il interdisait de donner son trait à un Promi, à une Nuée, à un gardé de côté. Il part
**à la page +**, à la création, et se reprend **depuis Peaufiner, haut de liste**. La règle
générale est inscrite dans `CLAUDE.md` §5 — *un réglage vit là où vit ce qu'il règle* — avec
son test : **est-ce que ce réglage a un sens différent d'un Promi à l'autre ?**

**Conséquence de dessin :** le trait n'avait plus rien à montrer au Studio. L'onde disparaît,
le corps disparaît, **la Toile prend tout l'écran**, et deux plateaux flottent dessus.

### Où en est le lot

```
FAIT   la planche du Studio sans trait, six pas, sombre et clair   PLANCHE-STUDIO-SANS-TRAIT
FAIT   les cinq fonctions de l'app replacées (voir plus bas)
FAIT   les planches passées au VRAI MOTEUR (Toile.preview)         Q130
FAIT   l'audit complet de la page Partager, 17 commandes, 5 défauts
FAIT   l'intégration dans app.html — lot-STUDIO-PLATEAUX                Q133
FAIT   le frémissement du moteur, mesuré (0,38 px amorti sur 1,1 s)     Q134
FAIT   trois bugs du Studio : verrou collant, monde faux, dégradés      Q135
FAIT   l'air de la consigne de la page + : 29 → 44 px
FAIT   l'onde à 36 partout — la borne basse du §2.4 bis              Q136
FAIT   les deux paires du Studio : écart 20/56 + leurs libellés      Q137
À FAIRE  LE GESTE DE COULEUR AU DOIGT — dessiné, pas codé (Q135)
FAIT   l'encart en haut — ONZE écrans                               Q138
À FAIRE  l'encart sur les QUATRE derniers — un lot chacun, ils ont
         chacun leur grammaire : Personne, l'aperçu, la page +, la fiche
FAIT   Partager sans trait — et les 4 défauts de l'audit corrigés     Q139
FAIT   le saut à l'ouverture du Studio — mesure supprimée          Q140
FAIT   les pages alignées sur la grammaire de l'encart            Q141
FAIT   les coins : les écrans épousent l'arrondi de l'appareil    Q142
À FAIRE  le bouton actif du sujet sort sombre au lieu de crème (Q139)
À FAIRE  l'encart de Partager est #shcTitre, pas .enh — à aligner
FAIT   la passe de collisions — 5 recouvrements trouvés et corrigés  Q143
FAIT   l'Index recalé en conditions RÉELLES (plus de forçage)       Q144
À FAIRE  METTRE À JOUR releve-S4-index-fil.py — 62 écarts voulus,
         il reste rouge tant qu'il n'encode pas la décision (Q144)
FAIT   le FIL (#feedView, pas #feedScreen) — calé comme l'Index     Q145
FAIT   les filets gris retirés — redteam_tonsurton 23/26 → 26/26   Q146
FAIT   LA RÉFÉRENCE = le plateau du Studio, PLEIN + bordé, déployé   Q147
       → même crème #F4EEE1 sur l'encart, la recherche, le tri, les cartes
À FAIRE  violations du §6 PRÉEXISTANTES : textes à 10-11,5 px et
         opacités à 0,42-0,70 sur Réglages, Aura, Index, Nuée, Cercle
         + #plHeroCv qui déborde (x −16, largeur 430) — à vérifier
         contre l'inventaire de chaque cadre avant de toucher (Q143)
À FAIRE  la planche de la page + pour le trait
À FAIRE  la refonte du partage sur la base de l'audit
```

### Les cinq fonctions du Studio, et où elles sont passées

```
.st3-dots    huit points de navigation  → rangée fine sous les disques, cliquables
.st3-hint    « glisse pour changer… »   → invite qui meurt après le premier geste
.st3-pals    Toile.palettes()           → reste le moteur ; la maquette montre 4 tons
#stLockBuy   « Adopte ce design — 1 € » → sur la Toile, au-dessus du plateau
#stLockCta   l'offre du Cercle          → encart §3.8 sur les réglages floutés
```

**Sur un monde verrouillé** (décision Tom) : la matière reste **visible**, floutée à 2,4 px ;
le nom du monde s'affiche **net, 46 px, centré** — il s'affirme même quand on ne l'a pas ;
l'encart couvre une partie des réglages et en laisse voir : **on voit ce qu'on n'a pas**.
On voit **quoi**, jamais **combien**.

### Ce que l'audit du partage a trouvé

**Deux défauts rendent une fonction entière inatteignable** — le mode « Noyau seul » n'a
aucun bouton (`#sealShare` cherche un `data-mode=noyau` qui n'existe pas), et les six
commandes de `#shNoyauParts` sont masquées en dur et jamais démasquées. **La refonte
restaure, elle ne déplace pas.** Trois autres se corrigent au passage : la borne du
sur-mesure (le clamp dit 3840, les boutons s'arrêtent à 2160), deux gestionnaires sans nœud
(`#shOptVis`, `.sh-opts`), et le libellé « Format » en double.

### Points de restauration

```
sauvegardes/avant-studio-sans-trait.html    app.html avant le lot du Studio
sauvegardes/lot-studio-plateaux.html        app.html après le lot, vérifié
sauvegardes/redteam_ecrans-avant-studio-plateaux.py   deux contrats réécrits
scratchpad/c5/painter.js                    la maquette, DÉBRANCHÉE (Q130)
```

---

# État des lieux — Promi, la superposition écran par écran

> **Ce fichier suffit à reprendre le projet.** Il dit ce qui est porté, ce qui ne l'est pas,
> ce qui a été corrigé dans les documents, quels contrats de test ont changé et pourquoi,
> et ce qui reste ouvert. Écrit sans complaisance : ce qui n'est pas beau à dire est dit.
>
> Dernière mise à jour : **30 août 2026 — LE STUDIO ET LE PARTAGE SONT CONÇUS ET POSÉS.**
> Point de reprise : `sauvegardes/lot-studio-partage.html`
> Captures : `scratchpad/studio/` · `scratchpad/partage/` · `scratchpad/final/` (32 images)

---

# ⚑ LE STUDIO ET LE PARTAGE SONT CONÇUS ET POSÉS — 30 août 2026

> **Ce chapitre passe devant.** Le portage était clos ; ce chantier-ci n'en était pas un.
> Le Studio et le partage n'ont **ni cadre ni inventaire** : c'était une CONCEPTION, sortie
> de la grammaire déjà posée. Aucun duo, rien à superposer.
>
> Point de reprise : **`sauvegardes/lot-studio-partage.html`**
> Sauvegarde d'avant le chantier : `sauvegardes/avant-studio-partage.html`
> Captures : `scratchpad/studio/` (6) et `scratchpad/partage/` (4), regardées une par une.

## Ce qui a été livré

| écran | variante retenue | ce qu'elle fait |
|---|---|---|
| **Le Studio** | **B · le champ** | le champ porte la Toile du monde, bornée par l'onde ; **le trait sert deux fois** — il borne le champ ET il montre le pinceau. On **pousse le champ** pour changer de monde ; sous le trait, un **rail de huit points** (les points du §2.2). |
| **Le partage** | **2 · la feuille** | **l'onde est la poignée** : on la tire, les réglages montent, l'image se réduit. Sous l'onde, **le même rail de points** — il ne dit pas où l'on est, il dit **qu'il y a la suite**. |

Deux blocs, posés à la fin du fichier comme tous les lots : **`lot-STUDIO-CHAMP`** et
**`lot-PARTAGE-FEUILLE`** (style + script). **Rien n'a été réécrit** : les commandes
existantes sont **DÉPLACÉES** dans la nouvelle grammaire, jamais refaites.

## LE PINCEAU — la seule fonction neuve, et elle était validée

Concept donné par Tom, jamais implémenté : *« on choisit aussi son pinceau au Studio — la
matière avec laquelle on trace ses moitiés de trait. Le monde est ce qu'on récolte, le
pinceau est ce avec quoi on signe. »* Trois matières : **Plein · Encre · Trame**.
Le choix est **enregistré** (`localStorage.promi_pinceau`, lu par `window.promiPinceau()`)
et le Studio le montre sur son propre trait. **Il ne change pas encore le trait qu'on trace
au doigt** — ce trait est peint par le moteur du geste, et le brancher est un lot à part
(QUESTIONS.md · Q118). Sans branchement, le geste garde le trait plein d'aujourd'hui, qui
est exactement le pinceau « Plein ».

## Aucune fonction perdue — l'inventaire, au complet

**Studio** — déplacés, pas supprimés : `#stBg` (le monde) → le champ · `.st3-dots` → le rail
· `.st3-wn` → sous « LE MONDE » · `.st3-pals` (palettes), `.st3-spec` (teinte), `#thToggle`
(thème), `#txToggle` (texte des dalles) → **derrière la barre Peaufiner** · `#stLockBuy`
(adoption 1 €) et `#stLockCta` (l'offre) → au doigt seulement, sur le champ voilé.

**Partage** — les **quatorze** réglages sont dans la feuille : sujet · cinq formats + sur
mesure · fond de l'image · mot-marque · QR · texte des dalles · Noyau + sa taille · ce qu'il
montre · quels Promi (la portée) · les deux actions · la note des 3 Nuées offertes.
**Disparaissent : le `⋯` et le `↗`** — le tiroir EST la feuille, et `#shGo` ne faisait que
cliquer `#shShareBtn`. Aucune fonction perdue (Q109).

**Tout est gratuit (Q113)** : aucun `✦`, aucun `blur(2.4px)`, aucun encart du §3.8, aucun
réglage grisé sur l'écran de partage ni dans sa feuille. C'est le **seul écran du produit où
le §3.8 est interdit**. La borne d'export monte à **4K** (Q119).

## Un contrat de test réécrit — au niveau de la décision (§7)

| contrat | il exigeait | la décision qui l'a remplacé | original |
|---|---|---|---|
| `redteam_ecrans` · « Studio : groupe centré » | les deux bascules forment un groupe centré **en haut** du Studio | la variante B : le champ occupe le haut, les réglages passent derrière la barre Peaufiner (Q109) ; le §9 interdisant de perdre une fonction, elles sont **déplacées** | `sauvegardes/redteam_ecrans-avant-studio-champ.py` |

**Même intention, nouveau nœud** : on vérifie que les deux bascules **existent encore**,
qu'elles sont **dans le tiroir**, et que la pile est **centrée**. Le contrôle protège
exactement la même chose. Il compte désormais **trois** points au lieu de deux — d'où
**148/148** là où il y avait 146.

## Ce que l'œil a trouvé, et qui est corrigé

| | ce qui ne ressemblait pas | ce que c'était |
|---|---|---|
| **1** | la dalle du Studio sortait en **rectangle noir** posé sur le champ | `Toile.preview` **peint son propre fond**. La boîte du §2.7 ne convient pas : c'est la construction du §10.7 — l'aplat, puis la Toile découpée par le **même chemin**, puis le trait. |
| **2** | le champ et la barre **rognés de 16 px à droite** | **un `.screen` ne coïncide pas avec `#device`** : `#studioScreen` fait **422 px** et commence **16 px à gauche et au-dessus**. D'où `#stcCadre` / `#shcCadre`, un cadre de 390 × 844 **mesuré** sur l'appareil. |
| **3** | l'encart et le bouton du Cercle en **dégradé rose-orangé**, texte illisible | `.enc-fx`, `.eg`, `.eb*` peignent un dégradé animé **par-dessus** le fond plat. §6 : aucun dégradé. Éteints, comme Q23 l'a fait aux Réglages. |
| **4** | en thème **clair**, « Studio » **crème sur crème** et le trait invisible | la Toile recouvre le champ et elle est crème : **ce qui est peint dessous décide** (Q59 étendu au trait — Q116). |
| **5** | le tiroir du Studio **sombre en thème clair** | `.device.light #studioScreen` **ne matche jamais** : l'écran vit sous `.frame`, pas sous `.device` (§8). On **pose** la classe, la CSS la lit. |
| **6** | les dix palettes **débordaient** sur la teinte ; le curseur de teinte **s'échappait à gauche** | des cotes fixes au lieu d'une pile à écart 16 ; et `.st3-spec` passée en `position:static` **perdait son bloc englobant**. |
| **7** | le tiroir sortait dans le **désordre** (thème, texte, palette, teinte) | l'ordre était celui où chaque commande **existe** : `#thToggle` est dans le HTML, `.st3-pals` naît avec `buildStudio`. Les quatre boîtes se créent **d'emblée**. |
| **8** | les deux actions du partage à **~30 px**, débordant du cadre | `.sh-share` porte ses propres taille, interlettre et capitales. §3.6 imposé au `!important`. |
| **9** | la feuille du partage **inatteignable** sous la barre | `#shcCadre` est en `overflow:hidden` : la pile doit porter sa **hauteur bornée** et défiler. |
| **10** | `redteam_geste` tombé de **13/13 à 12/13** — « l'aimant de la ligne du QR attire » | **`shareRender()` dimensionne l'aperçu lui-même.** Ma mise en page ne se rejouait qu'aux événements du doigt : après un `shareRender()` extérieur, le canevas repassait de **218 × 388 à 341 × 607** et le geste tombait à côté. On **repose derrière lui**, comme le lot du Studio derrière `buildStudio`. |
| **11** | le bouton d'adoption disait **« Débloque-le — 1 € »** | un **rotateur** tire le libellé **au hasard** entre trois formulations. On réécrit derrière lui, avec la garde du §8. |

## Tout est vert

```
23 batteries      ecrans 148/148 · 15 · 10 · 18 · demande 19 · toile 17 · geste 13/13
                  verbe 6 · phrase 6 · filets 0 parasite · aveugle 26 · fonctions 22
                  tonsurton 26 · formes 38 · nuee 24 écrans/0 · champs 22 · enchaine 24
                  pastilles 12 · photo 27 · polices 0 absent · vide 61 · air 391 paires
                  champ 32
5 juges           S1 ✅ · S2 ✅ · S3 ✅ · S4 ✅ · S5 ✅
contrat visuel    releve-design.py  ✅ AUCUN ÉCART
l'œil             collisions.py  19 écrans × 2 thèmes → 0 collision
                  10 captures regardées une par une (Studio 6, partage 4)
```

**`releve-design.py --figer` n'a PAS été lancé** : la référence attend ta validation.

## Ce qui reste ouvert

- **Q115 · la transition effilochée** entre deux mondes n'est pas implémentée :
  `Toile.preview` sème avec `Math.random()`, deux mondes ne peuvent pas partager un semis, et
  rendre deux mondes en une passe demanderait **d'ouvrir le moteur de la Toile** (§9). Le
  glissement repeint net, comme avant.
- **Q118 · le pinceau ne trace pas encore** le geste réel — lot à part, il touche au geste.
- **Q117 · trois libellés** de l'app remplacés par la forme du document : à relire.

---

# ⚑ LE PORTAGE EST CLOS — 29 août 2026

> **Décision Tom :** *« C'est bon, le portage est fini. »*
> Ce chapitre suffit à reprendre. Tout ce qui suit, plus bas dans le fichier, est
> l'historique — utile pour comprendre POURQUOI une chose est ainsi, jamais nécessaire
> pour continuer.

## A · Ce qui est porté, et jusqu'où va la spécification

**Le périmètre de la spécification s'arrête à sept écrans**, et ils sont tous portés :

| Écran | Cadres | Juge |
|---|---|---|
| **Les fiches** — Promi tenue · à tenir · en cours · Chiche lancé · relevé · tenu à deux | 42 à 57 | `releve-S1-fiches.py` |
| **Peaufiner** (fiche et Nuée) | 78 à 87 | `releve-S2-peaufiner.py` |
| **La page +** — phrase vide, remplie, choix ouverts, geste, reprise d'un gardé de côté | 2 à 33 | `releve-S3-page-plus.py` |
| **L'Index** (2 et 3 par ligne) **et le Fil** | 72 à 77 | `releve-S4-index-fil.py` |
| **L'instant** — il arrive · le trait se referme · juste après | 96 à 101 | `releve-S5-instant.py` |
| **La Nuée** — avec Promi, vide, son Peaufiner | `promi-nuee-toile.html` 0 à 11 | `redteam_nuee.py` |
| **Les réglages** | — | `releve-design.py` |

**Ce qui n'a NI CADRE NI INVENTAIRE, et n'est donc pas du portage : le Studio, l'Aura, le
partage.** Le prochain chantier est une CONCEPTION, pas une superposition. Ne pas y appliquer
la méthode du duo : il n'y a rien à superposer.

## B · Comment on vérifie — la méthode, en trois temps

1. **`python3 -m http.server 8752 --bind 127.0.0.1`**, puis les trois adresses (voir CLAUDE.md).
   Le port 8752 est **en dur** dans tous les outils.
2. **Les batteries, EN SÉRIE — deux ou trois à la fois au maximum.** Douze Playwright lancés
   d'un coup font ramer la machine et **les rouges qu'on lit alors sont faux** (mesuré et
   revécu quatre fois : `enchaine` 21/24 puis 24/24, `tonsurton` 22/26 puis 26/26, sans
   toucher une ligne). Un rouge apparu dans une passe parallèle **se reconfirme seul**.
3. **L'œil, au duo.** `python3 scratchpad/duo_vue.py scratchpad/final` — le cadre à gauche,
   l'app à droite, échelle 1, 16 écrans × 2 thèmes. **On les regarde toutes, une par une.**
   Trois défauts livrés à tort sont passés par des captures produites et non regardées.

## C · Les 23 batteries et les 5 juges — tous au vert

**Attention au compte :** un `ls redteam_*.py` en donne 20 et **oublie `redteam.py`,
`redteam2.py`, `redteam3.py`**. Il y en a **23**. (J'ai écrit « 22 » dans une livraison :
c'était ce glob, pas la réalité.)

```
redteam_ecrans      146/146   la principale — 146 contrôles d'écran
redteam                15/15   ·  redteam2   10/10  ·  redteam3   18/18
redteam_demande        19/19   redteam_toile      17/17   redteam_geste      13/13
redteam_verbe            6/6   la phrase montre TOUJOURS son verbe + la bascule
redteam_filets     0 parasite  aucun trait horizontal hors moodboard
redteam_aveugle        26/26   redteam_fonctions  22/22   redteam_tonsurton  26/26
redteam_formes         38/38   la courbe peinte contre la loi extraite du cadre
redteam_nuee     24 écrans/0   redteam_champs     22/22   redteam_enchaine   24/24
redteam_pastilles      12/12   redteam_photo      27/27   redteam_phrase       6/6
redteam_polices    0 absent    aucune graisse hors des six faces embarquées
redteam_vide           61/61   UN ÉCRAN N'EST JAMAIS VIDE — il ENCHAÎNE les écrans
redteam_air        391 paires  L'AIR ENTRE LES TEXTES ne se resserre jamais
redteam_champ          32/32   UN CHAMP BLANC N'EXISTE JAMAIS
```

```
releve-S1-fiches · releve-S2-peaufiner · releve-S3-page-plus
releve-S4-index-fil · releve-S5-instant          → les cinq AU VERT
releve-design.py                                  → AUCUN ÉCART (référence figée)
```

**Les trois dernières batteries sont nées de trois défauts livrés à tort.** Chacune a été
**prouvée contre la version fautive**, jamais seulement écrite :

| Batterie | Ce qu'elle protège | Preuve |
|---|---|---|
| `redteam_vide` | un écran ne perd pas ses éléments, et n'en porte pas d'un autre | **28/61** sur la version fautive, 61/61 après |
| `redteam_air` | deux textes ne se rapprochent jamais de leur écart d'origine | **18 rouges** sur « le cran sans les écarts » |
| `redteam_champ` | le champ porte toujours sa nature, jamais la couleur du corps | **2 rouges** sur la version au champ éteint |

**Ces trois-là ENCHAÎNENT ou COMPARENT ; les autres ouvrent chaque écran sur une page
fraîche.** C'est exactement pour ça qu'elles voyaient ce que les autres ne pouvaient pas voir.

## D · Les contrats de test réécrits — et pourquoi

**Règle (CLAUDE.md §7) :** un contrôle qui encode une règle abandonnée **se met à jour au
niveau de la décision**, jamais en changeant le comportement pour le faire passer. On nomme
la règle, on nomme la décision, on garde l'original dans `sauvegardes/`, et **on le dit dans
la livraison**. Six l'ont été en fin de portage :

| Contrat | Il exigeait | La décision qui l'a remplacé | Original |
|---|---|---|---|
| `releve-S1-fiches` | des cotes recopiées une à une, titre à 38 | les cotes **se déduisent** de la règle du 29 août ; le titre a une RÈGLE (42, sauf si la ligne casse — plancher 38), pas une taille | `-avant-29aout.py` |
| `releve-S3-page-plus` | « trace pour planter » sur les huit écrans | le moodboard ne dit ce mot que **deux fois** : « trace ta moitié » au cadre 2, « trace pour planter » au cadre 10 (choix ouvert) et 26 (reprise) | `-avant-29aout.py` |
| `releve-S3-page-plus` | « pas d'aplat sur un gardé de côté » | **un champ blanc n'existe jamais** — l'aplat doit être là, c'est la matière qui manque | `-avant-champ.py` |
| `releve-S4-index-fil` | le titre d'une carte à 20 exactement | il rentre dans sa boîte : **≤ la taille du cadre, ≥ 11** — un titre ne sort pas de sa boîte | `-avant-29aout.py` |
| `releve-S5-instant` | l'état à 12,5 | le cran du 29 août : 13,5, toutes fiches, toutes natures | `-avant-29aout.py` |
| `redteam_vide` (le mien) | un texte sans nœud texte est « vide » ; un titre sur « le trait se referme » | un `<input>` porte des glyphes par son `placeholder` ; **le cadre 98 n'a pas de titre** | — |

**Un renommage de nœud ne relève PAS de cette procédure** — c'est un renommage, l'intention
est intacte : on le note, on ne délibère pas.

## E · Les erreurs de dessin recensées — la planche a tort, et on l'écrit

Recensées dans `ECARTS-MOODBOARD.md § 0 bis`. **Une erreur de dessin n'est pas une règle :**
quand elle contredit une loi du document ou une décision, la loi gagne, et on note pourquoi.

1. **Cadre 58** — une base de champ de Nuée que `base = max(176, 460 − 86 n)` ne produit pour
   aucun `n`. Six points sur six suivent la loi ; ce cadre est un dessin isolé. (Q84)
2. **Cadre 74** — il donne une **dalle** à un gardé de côté. Lui en donner une l'occuperait
   une case de la Toile, donc le planterait. (Q83)
3. **Le bouton ⇅** — dessiné en `content-box` là où sa voisine est en `border-box` : il fait
   **56**, le document et l'app s'accordent contre le cadre. (Q87)
4. **Les cadres CLAIRS qui peignent le trait en couleur pleine** — le trait y prend
   exactement la couleur de l'aplat et **disparaît**. C'est le cas que le §2.1 bis interdit.
   (CLAUDE.md §3)
5. **Les cadres 26/27 et 74 qui dessinent un gardé de côté sur le corps nu** — même famille.
   **Un champ blanc n'existe jamais** (décision du 29 août). C'est la MATIÈRE qui manque à un
   gardé de côté, jamais la couleur.
6. **Le titre qui touche l'état dans une carte d'Index** — le cadre le fait aussi ; un texte
   ne sort pas de sa boîte, l'app le fait rentrer.

**Et deux exceptions déclarées, qui ne sont PAS des erreurs** : la **matière** (une Toile est
engendrée par le moteur, la planche l'a tracée à la main — elles ne peuvent pas coïncider,
Q74) et le **dessin des glyphes** (la planche est en Hanken Grotesk, l'app en Apfel embarqué,
et le §6 l'impose — Q80). **La boîte du texte, elle, se mesure à zéro.**

## F · Ce qui reste ouvert

**Rien ne bloque le prochain chantier.** Trois points de fond, à trancher quand ils gêneront :

- **Q71 · les titres de nature.** Tom les dit manquants dans l'Index et le Fil ; je ne les
  trouve dans aucun cadre, texte par texte, cotes et couleurs à l'appui. **Il faut un cadre
  ou un mot**, sinon ce serait inventer (§9).
- **Q68 · « Apfel 500 » n'existe pas.** Le document l'écrit à plusieurs endroits ; la face
  embarquée est `ApfelMid 500`. Le report est appliqué à l'exécution (`lot-POLICES`), pas
  corrigé à la source du document.
- **Le désaccord de comptes entre les deux planches.** `promi-nuee-toile` écrit « 7 PROMI »
  au potager, `moodboard-H` « Index 12 » ; le jeu réuni donne **9** et **16**, et l'encart
  dit **le contenu réel** (décision Tom : « garde les neuf, ne retire rien »).

**Ce qui est CLOS et ne doit pas être rouvert sans décision :** la teinture est bornée à la
bande haute (Q30 bis) · la bande d'une Nuée montre **les neuf mondes non teintés**, sa
planche le dit en titre (Q94) · l'anneau garde ses **trois** arcs (Q88) · la dalle est
centrée dans une carte d'Index (Q86) · le nombre de l'entête du Fil est « Fil 4 ».

## G · Les cinq lois qu'on reperd toujours

1. **La Toile ne se touche pas.** Son code est validé et fragile (§9). La couleur d'une dalle
   y est **tirée au hasard** (`cc()`) : le même id sort tantôt lavande, tantôt exactement la
   couleur du champ. C'est pour ça que le champ **cède** dans les listes, et que la bande
   haute **teinte** (Q30). Ne jamais juger une couleur de dalle sur un seul chargement.
2. **On ne nettoie pas la CSS.** Cinq tentatives, cinq échecs. L'ordre des 769 règles du
   dernier bloc est significatif.
3. **Rien ne survit à `closeAll`** — ni ce qu'un écran masque (`data-masque`), ni ce qu'il
   pose en ligne (`data-pose`), ni ce qu'il bâtit (`window._rangeurs`).
4. **Une cote dérivée n'est pas un espace, c'est « hauteur du bloc + air ».** Grossir un texte
   ne déplace aucun `top` : l'air se mange en silence. Écrire la cote dans la bonne unité.
5. **On compare la COMPOSITION, pas la peinture.** `dalleTrame` anime la matière avec
   `performance.now()` : un contrôle bâti sur ses pixels flotte. L'app publie ce qu'elle vient
   de composer — `_plancheComp`, `_noyauSig`, `_nueeSemis`, `data-champ`, `data-cede` — et le
   contrôle lit ça.

## H · Les fichiers, dans l'ordre où on les lit

```
CLAUDE.md                 fait autorité sur tout le reste
MOODBOARD-VALEURS.md      l'arbre des neuf écrans, extrait du moodboard
promi-moodboard-H.html    la référence visuelle du parcours (102 cadres, base 390)
promi-nuee-toile.html     fait foi pour la NUÉE
PROMI-SPECIFICATIONS.md   les valeurs (§1.2 palettes, §1.3 corps, §2.x géométrie)
ECARTS-MOODBOARD.md       les erreurs de dessin recensées
QUESTIONS.md              Q1 à Q101 — le raisonnement, décision par décision
ETAT-DES-LIEUX.md         ce fichier
```

**Point de reprise : `sauvegardes/lot-champ-de-nature.html`.**

---

## ⚑ LA MÉTHODE A CHANGÉ — ON NE MESURE PLUS AU PIXEL

> **Décision Tom, 29 août.** « On arrête la mesure au pixel. Le reste est le plancher de
> deux moteurs de rendu, pas un défaut : glisser la capture de −2 à +2 px donne le minimum
> à (0,0). **Tu regardes, tu corriges, tu termines.** »

L'outil est `scratchpad/duo_vue.py` : le cadre à gauche, l'app à droite, à l'échelle 1,
quinze écrans, deux thèmes. Pas de pourcentage — une image.
`scratchpad/collisions.py` complète : il demande au navigateur si deux textes se touchent,
sur dix-neuf écrans, dans les deux thèmes.

## ⚑ CE QUE L'ŒIL A TROUVÉ, ET QUI EST CORRIGÉ

| | ce qui ne ressemblait pas | ce que c'était |
|---|---|---|
| **1** | **Le Peaufiner d'une Nuée survivait à la fiche suivante** | Ses cartes (`np-tete`, `np-carte`) restaient dans `#dpdCorps`, et ses `display:none` en ligne restaient sur `dptQui`, `dptTitre`, `dptQuand`. La fiche passait de **10 à 24 nœuds de texte** et perdait son titre sous « DESCRIPTION · MEMBRES · PIÈCES JOINTES » |
| **2** | **Le bouton photo était écrasé à 2 px de large** | `max-width:100%` résolu sur son porte-à-faux de largeur nulle. À l'écran : un filet vertical au milieu du champ |
| **3** | **Le chevron ▾ de Peaufiner disparaissait** | `opacity:.5` et 13,3 px là où le cadre 48 l'écrit plein, à 15 px |
| **4** | **L'icône de partage était trop maigre** | `svg 19 × 19, trait 1,8` contre `22 × 22, trait 2,6` au cadre |
| **5** | **La pastille du mot de la page + flottait** | Même creux que la pastille du verbe (`2px 17px 6px`) et un interligne cloué à 42 px : **57,8 de haut au lieu de 44**. Le cadre donne `0 15px 3px`, rayon 16, interligne normal |
| **6** | **Le Fil ne montrait qu'une pastille de visage sur trois** | Elle se lisait sur `p.from` — qui a promis — au lieu du `from` de l'ÉVÉNEMENT |
| **7** | **Le fil d'une Nuée disait « TENUE » et coupait ses titres** | Le cadre écrit **TENU** (le sujet est un Promi, pas une parole) et laisse le titre passer sur **deux lignes** |
| **8** | **Un chiche relevé s'affichait « CHICHE LANCÉ »** | La ligne se lisait sur l'état de la PAROLE ; c'est `chicheEtat` qui dit s'il est relevé |
| **9** | **Le Noyau d'une Nuée vide était GRIS** | §3 : « jamais de trait neutre ou gris ». Le cadre 0 de `promi-nuee-toile` l'écrit dans la teinte claire de la nature |
| **10** | **« +N » comptait mal les membres** | Le Peaufiner d'une Nuée sortait « +2 » là où le cadre 86 écrit « +3 » : il oubliait de me compter, contrairement à la ligne « à qui » de la fiche |
| **11** | **Un TROISIÈME bouton « Planter un Promi dans la Nuée »** | La liste de Peaufiner de la section 2 en bâtit un (`.s2-bouton`) que le garde des jumeaux ne voyait pas : **deux textes identiques superposés à 100 %** |
| **12** | **« écris un mot… » sur une fiche** | Le cadre 46 écrit « écris un mot » ; les points appartiennent au champ COMMENTAIRES |

## ⚑ ZÉRO COLLISION, ET TOUT EST VERT

```
scratchpad/collisions.py   19 écrans × 2 thèmes   →   0 collision
```

C'était la dernière ligne de `CASSE.md` — « les textes qui se touchent dans l'Index », « les
commentaires qui sortent de leur ligne ». **Aucun des deux n'est reproductible** ; le seul
recouvrement réel du produit était le troisième bouton « Planter » (ligne 11 ci-dessus).

⚠ **Le premier balayage annonçait 269 collisions : toutes fausses.** La sonde ratissait tout
`#device`, y compris le dock, la barre d'état et les écrans FERMÉS — qui gardent leurs nœuds
en `display:block`, simplement recouverts. Et les écarter un à un ne marche pas non plus :
dans une vraie collision, c'est le texte du DESSOUS qu'on écarterait. On prend donc **la
feuille la plus haute qui couvre l'écran** et on compare ses textes entre eux.

```
redteam_ecrans     146/146   redteam_champs      22/22   releve-S1-fiches      ✅
redteam_fonctions   22/22    redteam_pastilles   12/12   releve-S2-peaufiner   ✅
redteam_aveugle     26/26    redteam_enchaine    24/24   releve-S3-page-plus   ✅
redteam_toile       17/17    redteam_photo       27/27   releve-S4-index-fil   ✅
redteam_formes      38/38    redteam_tonsurton   26/26   releve-S5-instant     ✅
redteam_nuee        24/24    redteam_polices      0/0    redteam_filets    0 filet
redteam 15 · redteam2 10 · redteam3 18 · demande 19 · geste 13/13 · verbe 6 · phrase 6

releve-design.py   ✅  AUCUN ÉCART — référence refigée le 29 août.
```

## ⚑ CE QUI NE PEUT PAS RESSEMBLER, ET POURQUOI — quatre lignes

1. **Les glyphes.** La planche est en Hanken Grotesk et Bricolage Grotesque ; l'app porte ses
   six faces embarquées, que le §6 impose. Un titre passe à deux lignes d'un côté et une de
   l'autre — c'est le cas de « le grand plongeoir », dont la ligne d'état descend alors de
   39 px sur le cadre 56. **Ce n'est pas un écart de dessin** (Q80, tranché).
2. **Le bouton photo** (`ph-photo-btn`) n'existe sur aucun cadre : c'est l'affordance de la
   **photo de champ**, décidée en Q53, et le seul chemin vers elle — les PIÈCES JOINTES de
   Peaufiner sont autre chose (« ce n'est pas une pièce jointe », dit le lot). Il reste,
   discret, comme son propre lot l'exige.
3. **« trace pour planter »** là où les cadres 2 à 10 écrivent « trace ta moitié » : **Q35**,
   tranchée par Tom — un seul mot, qui ne change pas d'un cadre à l'autre.
4. **Le jour d'une échéance** dépend du jour où l'on regarde : le cadre 36 écrit
   « À TENIR · DIMANCHE », le cadre 44 « À TENIR · DANS 2 JOURS », pour la même fiche à deux
   jours. L'app écrit le vrai jour.

---

## 1 · En une minute

Le **portage au moodboard est terminé**. Les cinq sections prévues par
`AUTONOMIE-CLAUDE-CODE.md` sont livrées ; les cinq lignes du critère d'arrêt sont vraies sur
chacune, et les neuf batteries sont vertes.

```
app.html                    point de reprise : sauvegardes/lot-polices-usage.html
sections portées            5 / 5
juges de section            S1 ✅ · S2 ✅ · S3 ✅ · S4 ✅ · S5 ✅   (tous à zéro écart)
batteries de comportement   144/144 · 15/15 · 10/10 · 18/18 · 19/19 · 16/16 · 13/13 · 6/6 · 0 filet
contrat visuel              releve-design.py  ✅ AUCUN ÉCART
```

### Ce que le lot du 19 août a livré

| | quoi | où c'est écrit |
|---|---|---|
| **1** | **LE VIDE EST UN DÉFAUT DU PLANCHER** — et de lui seul. Fiches et page + gardent la boîte du §2.7 ; la matière ne descend jusqu'à la vague **qu'au plancher** | `CLAUDE.md §4` · `ECARTS-MOODBOARD.md` · Q57 à Q60 |
| **1 bis** | **LA TOILE D'UNE NUÉE** — trois emplacements figés remplacés par la densité de semis du §10.6 (douze graines / 390 × 435) | Q62 · Q63 |
| **2** | **UNE NUÉE SE LANCE AU TRAIT ENTIER** — 0 → 390, mode complet du §2.6, ni chevron ni points | `CLAUDE.md §4` |
| **3** | **LE TUTORIEL NE SURVIT PLUS À `closeAll`** — trois rouges de `redteam_aveugle` pour une seule cause | §5 ci-dessous |
| **4** | **LA HAUTEUR DU TRAIT D'UNE FICHE DE NUÉE** — `base = max(176, 460 − 86 n)`, amplitude 40, Noyaux à `boîte − 29` | `PROMI-SPECIFICATIONS.md` partie II §9 et §12 |

> **⚠ LA PREMIÈRE FORMULATION ÉTAIT TROP LARGE, ET JE L'AI APPLIQUÉE TROP LARGE.**
> « La matière remplit tout le champ, partout » a fait gonfler la dalle d'une fiche sur tout
> son champ — cinq fois sa taille native. Tom a corrigé : **le moodboard des fiches et de la
> page + est juste**, le défaut n'existe **qu'au plancher du trait**. Tout a été restauré,
> puis re-corrigé au bon endroit. **La leçon : quand une consigne dit « ça ne doit pas
> exister », mesurer OÙ ça existe avant de l'appliquer partout.** L'outil qui manquait —
> `scratchpad/mesure_vide.py` — existe maintenant.

**Le relevé qui tranche** (`scratchpad/mesure_vide.py`, deux thèmes, hauteur de couleur nue
entre le bas de la matière et le trait) :

```
                        avant           après
Nuée · 1 Promi     125 abscisses/125 nues     0 nue · médiane 0 · pire 0
Nuée · 3 Promi      28 bandeaux > 24 px       0 bandeau · médiane 0
Nuée · 7 Promi  ←   17 bandeaux > 24 px       0 bandeau · médiane 0     AU PLANCHER
page + · choix ouvert ←  au plancher : rempli · médiane 0               AU PLANCHER
fiche · les 4 états      boîte du §2.7, inchangée — aucune n'est au plancher
```

**Trois sondes réécrites au niveau de la décision** (`CLAUDE.md §7`), aucune desserrée —
`redteam_tonsurton`, `releve-S3-page-plus`, `releve-S5-instant`, plus le contrôle de couleur
du mot-marque de `releve-S1-fiches`. Versions d'origine dans `sauvegardes/*-avant-matiere.py`.
Détail au §6.5.

### Les six contrôles d'USAGE — la mesure qui compte

Les juges disent que le dessin est juste. **Ceux-ci disent que l'app FONCTIONNE.** Ils ont
été écrits après avoir découvert qu'aucune batterie ne remplissait un champ ni ne touchait
une pastille — un champ de 0 × 0 passait tous les contrôles de cote.

```
redteam_champs      22/22   remplir chaque champ, et vérifier que la valeur ARRIVE
redteam_pastilles   12/12   toucher chaque pastille, et vérifier qu'elle CHANGE quelque chose
redteam_enchaine    24/24   enchaîner deux écrans, et comparer le second à lui-même ouvert seul
redteam_fonctions   19/19   l'inventaire des fonctions qu'aucune refonte ne doit faire disparaître
redteam_photo       27/27   la photo de fiche : elle remplace la matière, partout
redteam_tonsurton   26/26   un trait n'est JAMAIS à moins de 42 de son champ
redteam_aveugle     26/26   les trois zones que personne ne regardait
redteam_nuee        24/24   LA FICHE DE NUÉE — les 20 écrans du §12 + les 4 du Peaufiner
redteam_polices      0/0    AUCUNE GRAISSE HORS DES SIX FACES EMBARQUÉES
redteam_toile       17/17   stable sur trois passages — le dernier flake est mort
```

**Aucune batterie n'est rouge.** Le seul écart ouvert est celui du **contrat visuel** — voir
juste dessous, et il est *demandé par le lot*.

**`redteam_aveugle` — 26/26.** Le dernier rouge est tombé avec le portage du Peaufiner
d'une Nuée : « Planter un Promi » y a sa place, et la fiche au repos n'en porte plus.
Il y avait **deux** boutons — `#nqAddPromi` (balisage d'origine, celui qui se posait à y = 0
par-dessus « ✕ FERMER ») et `#nfAdd` — désormais ramenés à un seul. **Rien n'a été retiré du
produit.** Voir `QUESTIONS.md` · Q61.

> ⚠ **`releve-design.py` sort ~35 écarts, et ils SONT le lot des polices.** Tous portent sur
> `fontFamily` / `fontWeight` : `Apfel 700/800 → ApfelMid 500`, `Bricolage 800 → 700`. La
> référence a été refigée après le lot Nuée (validé par Tom) mais date d'avant les polices.
> **Je ne l'ai pas refigée** — `--figer` attend la validation, comme le §8 bis l'exige.
> Ancienne référence : `sauvegardes/design-reference-avant-nuee.json`.

**Ce qui n'est PAS fait, et pourquoi :** trois éléments du moodboard sont des **fonctions,
pas du dessin** — ils demandent une décision de produit, pas une cote. Voir §5.

---

## 2 · Ce qui a été porté, section par section

La méthode, identique partout : **écrire chaque écran depuis son inventaire de la partie 5
de `PROMI-SPECIFICATIONS.md`**, au lieu de réparer l'existant. Un bloc neuf en fin de
`app.html`, jamais une règle existante modifiée. Puis un juge par section, puis des duos
côte à côte moodboard / app, **dans les deux thèmes**.

| | Section | Ce qui est porté | Écrans | Juge |
|---|---|---|---|---|
| **1** | **Les fiches** | Promi, Chiche, Nuée, gardé de côté, états de fiche. Le moteur géométrique (§2) posé une fois pour toutes et **exposé** (`window._onde`, `_ficheEcran`, `_ficheTrait`, `_ficheCotes`, `_visageSvg`) | **8 / 8** | `releve-S1-fiches.py` |
| **2** | **Peaufiner** | La barre, les réglages, les réglages généraux, le bloc du Cercle | **7 / 9** | `releve-S2-peaufiner.py` |
| **3** | **La page +** | La phrase, les trois natures, les choix ouverts, le geste, le Peaufiner de la page + | **16 / 16** | `releve-S3-page-plus.py` |
| **4** | **Index et Fil** | L'écran plein, l'entête, la recherche, la grille, la carte d'Index (deux densités), le bandeau du Fil | **6 / 6** + 8 cartes isolées | `releve-S4-index-fil.py` |
| **5** | **L'instant** | « L'autre moitié arrive », « le trait se referme », « juste après », et la séquence d'une seconde | **6 / 6** | `releve-S5-instant.py` |

### Le critère d'arrêt, section par section

Cinq lignes, toutes à zéro sur les sections 3, 4 et 5 :

```
écarts de position > 3 px · écarts de style · collisions · débordements · présence peinte
```

**La cinquième ligne est la plus importante.** Un bloc à la bonne coordonnée mais invisible
est un faux vert : les juges lisent donc **les pixels réellement peints** — l'aplat de
nature, la dalle, la ligne — et vérifient l'encre de chaque texte contre le fond peint
dessous, seuil de luminosité 42.

### Sections 4 et 5 en détail

**L'Index et le Fil deviennent des écrans pleins** (décision Tom) : entête « Index N » +
✕ FERMER, champ de recherche, grille. Plus de topbar, plus de mot-marque, plus de
`#viewSwitch`, plus de dock. **Les deux seuls éléments de chrome persistants du produit sont
le ✕ FERMER et la barre Peaufiner.**

**L'instant** est le seul endroit du produit où la couleur d'état prend toute la place :
le champ entier passe au menthe **une seconde**, la dalle se recompose plus grande
(604 → 1013 pixels peints, mesuré sur 18 relevés), le mot tombe, puis le champ revient à sa
nature. Le déclencheur réel est le bouton « Tenue » du sélecteur d'état, par lequel passe
le geste qui se referme.

---

## 3 · Les deux trouvailles à ne pas reperdre

### 3.1 · L'Index est une FEUILLE, pas une vue

`window.ouvrirIndex()` appelle `buildIndex()` puis `openSheet(#indexSheet)` : la feuille se
pose **par-dessus** `#stage`, qui garde la Toile. Le code le dit en toutes lettres
(l. 3039) : *« le sélecteur revient sur Toile : l'Index est une feuille, pas une vue »*.

**Conséquence :** mesurer `#stage`, ou le `.on` de `#viewSwitch`, ne peut RIEN montrer — par
construction. Une session entière a été perdue sur ce constat pris pour un blocage.
`#indexSheet` passe bien de `opacity 0 / y 816` à `13,28 · 364 × 787`. Le Fil, lui, **est**
une vue : `setView('fil')` → `#feedView.in`, `#stage` en `display:none`.

> **La leçon, générale :** avant de conclure qu'un écran « ne s'ouvre pas », instrumenter
> **l'élément que le code désigne**, pas celui qu'on suppose. `scratchpad/probe_ix.py`.

### 3.2 · La loi de la carte était dans les chemins SVG du moodboard

Le document donnait les cotes carte par carte, jamais la règle qui les produit. Elle a été
retrouvée en lisant les chemins SVG des cadres 72, 74 et des cartes isolées, et **elle est
désormais inscrite au §3.9 bis de `PROMI-SPECIFICATIONS.md`** :

```
échelle = h/600 · base = hauteur de trait figée × échelle · amplitude = 13 × l/173
boîte   = ⌊ base + amplitude + 20 ⌋ · épaisseur = 5,5 × l/173 · période = 1
```

Elle retrouve les **huit cartes isolées** du document, boîte et dalle, **8 sur 8** — et
`releve-S4-index-fil.py` refait ce contrôle à chaque passage.

> **La leçon, générale :** quand le document donne des cotes sans règle, la règle est
> souvent dans le moodboard lui-même. `python3 scratchpad/dump_cadre.py <n>` sort le HTML
> d'un cadre ; `scratchpad/liste_cadres.py` donne l'ordre réel des 102 cadres — **qui n'est
> pas celui du document.**

---

## 4 · Ce qui a été corrigé DANS LES DOCUMENTS

Trois corrections, toutes validées, toutes inscrites à leur place — pas dans un compte rendu.

| Où | Quoi | Pourquoi |
|---|---|---|
| `PROMI-SPECIFICATIONS.md` **§3.9 bis** | **La loi de la carte**, ajoutée | Elle n'était nulle part ; elle a dû être redéduite deux fois |
| `PROMI-SPECIFICATIONS.md` **§2.5** | **Les bornes `[196, 344]` valent pour la carte sans exception** | Deux fiches du document portent 376 et 372, hors échelle. Reportées sur une carte de 133 px, elles laissaient **10 px au titre** : coupé en plein mot, l'état par-dessus. Un titre coupé n'est pas un dessin, c'est un bug |
| `CLAUDE.md` **§7** | **Un contrôle qui encode une règle abandonnée se met à jour au niveau de la décision** | Voir §6 ci-dessous |

**Un piège à connaître sur la borne :** la **loi** (§3.9 bis) et la **borne** (§2.5) sont
**deux règles distinctes**. La loi ne borne rien ; la borne est un garde-fou sur la valeur
qu'on lui donne. Les appliquer d'un seul geste fait sortir « le potager » à 152 au lieu de
153 — sa base est 346, deux pixels au-dessus du plafond. Chacune se contrôle à son niveau :
`juge_composants` teste la loi **sans** la borne, `juge_borne` vérifie que la borne mord sur
376 et 372, jamais sur une base légitime, et coûte moins de 3 px sur les cas limites.

---

## 4 bis · LA CONFORMITÉ DE FORME — le chantier ouvert

### Le jeu de démonstration de la planche — FAIT

`lot-JEU-PLANCHE`, à la fin de `app.html`. Mêmes promesses, mêmes titres, mêmes personnes,
mêmes états que les deux planches. **Tous les mots viennent des cadres**, lus au texte
(`scratchpad/extrait_jeu.py` → `scratchpad/jeu_planche.json`), aucun inventé.

```
6 hors Nuée   planter un arbre TENUE · faire les crêpes À TENIR · courir dimanche (Chiche,
              relevé, avec Rachel) · nager le mardi EN COURS · le grand plongeoir (Chiche,
              TENU À DEUX) · aller voir la mer À TENIR
6 au potager  arroser tous les soirs TENUE · semer les radis · reprendre l'arrosage
              automatique · réparer le grillage du fond · rapporter la clé du cabanon ·
              chiche de venir désherber samedi        → « 6 PROMI · 1 TENU », le compte du cadre
2 Nuées       le potager (Rachel, Adrien, +3) · l'atelier du samedi (Avec toi seulement)
1 gardé       appeler Mamie
le Fil        les CINQ entrées du cadre 76, dans son ordre, avec ses tournures
```

**Mesuré : l'Index affiche « 12 », comme le cadre 72**, et le Fil montre « Marion te lance
un chiche · à moi · Adrien a planté · à Rachel · Marion a relevé » — les eyebrows de la
planche, obtenus sans les écrire : la carte retire le titre entre guillemets du texte de
l'événement, il suffit d'écrire la tournure du cadre.

> **⚠ « m'appeler » et « venir dimanche » (cadres 8 et 10) n'y sont PAS** : ce sont des
> exemples de PHRASE sur la page +, pas des Promi plantés. Les compter donnait « Index 14 »
> là où le cadre écrit **12**.

**Corrigé au passage :** le nom d'une Nuée était capitalisé d'office (« Le potager ») —
la planche écrit « le potager », en minuscule, dans les trois cadres qui le portent.

### ⚠ CE QUE LA MESURE A APPRIS, ET QUI CHANGE LA CIBLE

Le comparateur descend là où les données convergent — `fiche-tenue` de **30,4 % à 13,8 %**,
`fil` de **48,4 % à 38,4 %**. **Mais il ne descendra pas à zéro, et pas à cause du dessin :**

> **LA MATIÈRE D'UNE TOILE EST ENGENDRÉE, PAS DESSINÉE.** Les dalles de l'app sortent du
> moteur — graines, poids, monde tiré au Studio — et respirent avec `performance.now()`.
> Celles de la planche sont **des courbes dessinées à la main**, cadre par cadre. Sur une
> fiche de Nuée, le champ occupe les deux tiers de l'écran : la mesure y donne **87 à 100 %
> de pixels différents**, et **aucune correction de forme n'y changera rien**.
> **Ce qui peut atteindre zéro, et qui se vérifie : la GÉOMÉTRIE** — chemins, cotes,
> épaisseurs, mots, couleurs. C'est ce que mesure `redteam_formes.py`.
> **Question posée à Tom** (`QUESTIONS.md` · Q74) : le « zéro au pixel » doit-il s'entendre
> comme « zéro sur la géométrie et les mots, la matière exceptée » ?

### Le contrôle de forme — ÉCRIT : `redteam_formes.py`

Celui qui manquait. Il ne lit pas le code : **il lit les pixels peints**, cherche le centre
du trait à chaque ordonnée, et le compare à la loi extraite du cadre. Tolérance 1,5 px.

```
LE BANDEAU DU FIL   x(u) = 121,0 − 4,3·u − 8,425·sin(2πu) · épaisseur 7 · sans chevron
                    4 points r 3,4 aux y 77 · 90 · 103 · 116
LA CARTE D'INDEX    épaisseur 5,5 × l/173 · tenu = entier · à tenir = moitié + chevron + 6 points
```

**Mesuré : la courbe du Fil colle à 1,02 px** après correction des trois coefficients.
**Il oscille encore entre 46 et 50 sur 50** : la dernière carte n'est pas toujours peinte
quand la sonde passe. L'attente sur « liste bâtie ET peinte » l'a amélioré (38→50 puis
46-50), **elle ne l'a pas stabilisé**. À finir.

### L'outil existe : `scratchpad/duo_pixel.py`

Il superpose le cadre de la planche et la capture de l'app, **et mesure**. Il ne dit pas ce
qui ne va pas : il dit **où**, et **combien**. Premier relevé, deux thèmes :

```
fil            dark  48,4 %      fiche-tenue    light 38,5 %
nuee-3         light 40,7 %      index-2        light 31,0 %
index-3        dark  40,6 %      fiche-encours  light 18,0 %
index-2        dark  39,8 %      page-plus      dark  14,7 %
```

> **⚠ CE CHIFFRE NE PEUT PAS TOMBER À ZÉRO, ET IL FAUT LE SAVOIR AVANT DE COURIR APRÈS.**
> La planche montre **ses** données — quatre entrées dans le Fil, « le grand plongeoir »,
> « faire les crêpes », des dalles tirées de ses mondes. L'app montre **les siennes** —
> douze entrées, d'autres titres, d'autres mondes, et une rangée « TENIR · REPORTER » sous
> chaque bandeau que la planche n'a pas. Corriger la forme **ne fera pas** converger le
> pourcentage. Ce qui converge, et qui se mesure, c'est **la géométrie** : chemins, cotes,
> épaisseurs, mots. Le pourcentage sert à **classer les écrans** et à voir **quelles bandes**
> diffèrent, pas à valider.
> **Ce qu'il faudrait pour un vrai zéro : mettre l'app dans les données de la planche** —
> un jeu de démonstration qui reprend les Promi du moodboard. Ce n'est pas fait, et c'est
> la première chose à faire au prochain tour.

### Ce qui est EXTRAIT, et qui fait désormais loi

Relevé au chemin, pas estimé (`/tmp/paths*.py`, à reprendre dans `scratchpad/`) :

**Le bandeau du Fil (cadre 76)** — SVG **143 × 128**, sans viewBox, posé à `left:0;top:0` :
```
champ  M121.0 0 → 24 segments de 5,333 → L116.8 128.0 L0 128 L0 0 Z     fill = nature
       x(u) = 121,0 − 4,3·u − 8,425·sin(2πu)          (base · montée · sinus · période 1)
trait  le MÊME chemin, u de 0 à 0,5 si une moitié manque, 0 → 1 si la parole est entière
       stroke = COULEUR D'ÉTAT · épaisseur 7 · bouts ronds · AUCUN CHEVRON
points 4 cercles r 3,4 aux y 77 · 90 · 103 · 116, sur le chemin, couleur d'état
```
**Corrigé :** l'app portait `0,34 × 358 = 121,72` et `amp 13,5` (montée 4,59, sinus 8,37).
Elle porte maintenant les trois coefficients de la planche. Et ils **ne suivent pas**
`mont = 0,34·amp / a = 0,62·amp` — le bandeau du Fil a ses propres coefficients.

**La carte d'Index (cadre 72)** — SVG **165 × h**, viewBox `0 0 165 h` :
```
champ  M0 base C… (Béziers) … L165 0 L0 0 Z                 fill = nature
trait  le même chemin · stroke = couleur d'état · épaisseur 5,2457 (= 5,5 × 165/173, §3.9 bis)
       tenu → chemin ENTIER, ni chevron ni points
       à tenir → chemin jusqu'à x = 82,5 (la moitié) + CHEVRON `M-3.7 -5.2 L3.1 0 L-3.7 5.2`
                 épaisseur 3,1, puis 6 points r 3,052 aux x 93 · 103,5 · 114 · 124,5 · 135 · 145,4
       Nuée en cours → chemin ENTIER en #D0B0FF, sans points
```
**Pas encore comparé à ce que l'app dessine.** C'est le prochain pas.

### Ce qui est corrigé

| | quoi | preuve |
|---|---|---|
| **le bandeau du Fil** | les trois coefficients de la planche, au lieu de valeurs déduites | chemin extrait du cadre 76 |
| **un Chiche dans une Nuée** | sa ligne disait « en cours », le mot d'un Promi. Elle dit **CHICHE LANCÉ / CHICHE RELEVÉ** — les mots du cadre défilé de `promi-nuee-toile.html` | mesuré : la ligne passe de « en cours » à « CHICHE LANCÉ » |

### Ce qui est VÉRIFIÉ ET N'EST PAS UN DÉFAUT

**Le compte inclut déjà les Chiche.** Mesuré : on met un vrai Chiche dans la Nuée, le compte
passe de **3 à 4**, sur la fiche comme sur la carte d'Index. `promisDeNuee` et le bâtisseur
de cartes filtrent sur `!draft && nuee===k`, sans exclure les Chiche.
**Ce qui manquait n'était pas le compte, c'était le MOT de la ligne** — corrigé ci-dessus.
⚠ Reste à vérifier : l'Aura, le Noyau et les légendes, non mesurés.

### Ce qui est OUVERT, et pourquoi je m'arrête là

1. **Les titres de nature.** Cherchés dans les cadres 72 (Index) et 76 (Fil), texte par texte,
   avec leurs cotes et leurs couleurs : **aucun n'y figure**. Les eyebrows de la planche sont
   « à moi », « à Rachel », « avec +4 », « à Marion », « Marion te lance un chiche »,
   « Adrien a planté » — la nature s'y lit à la COULEUR du champ et de l'accent, pas à un mot.
   **Je ne sais donc pas où Tom les voit**, et je n'invente pas un libellé. **Question posée.**
2. **Les textes qui se touchent dans l'Index**, et **les commentaires qui sortent de leur
   ligne** : signalés, pas encore reproduits ni mesurés.
3. **Le contrôle de forme dans les juges** : pas écrit. C'est le vrai manque de méthode —
   les cinq lignes du critère ne comparent aucune courbe.
4. **Les fiches, la page +, le Peaufiner, l'instant** : le comparateur les classe, aucun n'a
   été corrigé.

## 4 ter · LES DIX DÉFAUTS QUE LE DUO A SORTIS, ET QU'AUCUNE BATTERIE NE VOYAIT

Aucun n'était visible d'une batterie : elles mesurent des cotes, des couleurs et des
présences, écran par écran, sur une page fraîche. Le duo compare **l'image**, écran après
écran, dans l'ordre où un doigt les ouvrirait.

### 1 · La classe héritée `dp-nuee` cassait l'écran porté d'une Nuée
`dp-nuee` réveille tout le CSS d'avant le portage. Mesuré, deux thèmes :
`#detailPoster` passe de `flex/absolute/844` à `block/relative/0`, et la barre Peaufiner,
collante, **tombe à y = 0, par-dessus « ✕ FERMER »**. Elle n'arrivait pas toujours :
`renderNueeDetail` la pose, `renderDetail` la retire — **selon qu'une fiche a été ouverte
avant ou non, l'écran était juste ou cassé.** C'est ce que `redteam_aveugle` criait, et que
Q75 avait mis à tort sur le compte du nouveau jeu. Blocs `lot-NUEE-LEGACY` et `lot-NUEE-CLASSE`.

### 2 · La hauteur d'une Nuée survivait à la fiche suivante — et lui volait sa barre
Le fil d'une Nuée défile : `#dpMain` porte sa hauteur en `min-height !important`, et rien ne
la retirait. Après « le potager », `#dpMain` restait à **1092 au lieu de 760** ; la barre
Peaufiner tombait à y = 1092, **hors de l'écran**. La fiche perdait sa barre, en silence.
Le duo le montrait ainsi : `fiche-tenue` **clair à 15,9 %** contre 4,8 % en sombre, sur le
même dessin. Corrigé au garde de `_ficheNuee` — **4,5 % / 4,6 % après.**

### 3 · La carte d'Index dessinait l'onde d'une FICHE
`peintCarte` appelait `O.onde(base, amp)` — qui cloue **période 1,5** (§2.1, une fiche) et
**normalise par 390**, la largeur d'une fiche. Sur une carte de 165, l'abscisse n'atteignait
que t = 0,42 : on voyait deux cinquièmes de la courbe, étirés sur toute la carte. Le §3.9 dit
**période 1**, sur la largeur de la carte. Mesuré contre le chemin du cadre 72 :

```
x        2    38    74   110   146   158
loi   102,3  94,4  98,6 106,8 104,3 100,9     creux à x=41, crête à x=124
avant 102,0  96,0  94,0  98,0 104,0 105,5     creux à x=68, crête à x=165
après 102,0  94,0  98,0 106,0 103,0  99,5     écart médian 0,65 px, maximal 1,65
```

`onde` prend maintenant deux paramètres facultatifs (`per`, `larg`) ; **la fiche ne bouge pas
d'un pixel.**

### 4 · La hauteur du trait était une cote de l'ÉTAT, pas du PROMI
Le §2.5 dit « la hauteur de trait **figée à la plantation** ». L'app la déduisait de la fiche.
Les six cartes du cadre 72 sortaient à `145 · 118 · 108 · 118 · 118 · 145` là où la planche
donne `135 · 107 · 147 · 99 · 123 · 131`. **La preuve que c'est une cote du Promi :** les deux
cadres de l'Index — 2 par ligne (198/600) et 3 par ligne (133/600) — redonnent la même hauteur
à 1,5 px près sur les huit entrées. Portée en `p.ht` / `NUEHT[k]` (Q78).

### 5 · La boîte de la dalle de la page + se tirait de la crête de l'onde
Relevé sur neuf cadres, deux bases : `base 312 → dalle 244 × 200 @ 73` et
`base 280 → 204 × 168 @ 93`, soit **`dh = base − 112`, `dw = 1,2 dh`, centrée**. L'app
calculait `(base − amp) − 100` et sortait **199 × 166 au lieu de 244 × 200** — la matière
d'un cinquième trop petite, et tout son pourtour compté comme un écart. **10,2 % → 1,8 %.**

### 6 · La bande de fond d'une Nuée suivait la boîte, pas la vague
`--nuee-bande` est le fond DERRIÈRE le canevas. Mais le canevas n'est opaque que jusqu'à
l'onde : au-delà de son point le plus haut, la bande se voyait là où le corps commence.
Mesuré sur le potager : boîte 256, vague à 140 → **116 px de mauve à bord franc**, et 100 %
de différence sur les ordonnées 180 à 240. Bornée au minimum de l'onde. **21,5 % → 9,9 %.**

### 7 · Une Nuée gardée de côté gardait son champ plein
« Rien n'est promis, donc il n'y a pas de champ » est déjà la règle d'un Promi gardé de côté
(section 1, page + cadre 27). Le cadre 74 la montre appliquée à une Nuée : « l'atelier du
samedi » y est un corps nu pointillé. L'app y peignait un aplat mauve.

### 8 · L'anneau du Noyau peignait « tenu » en MAUVE
Trois choses le contredisaient, toutes dans le produit : **`CLAUDE.md` §3** (« #2BE88C
menthe tenue »), **sa propre légende** `.klegend` (« #2BE88C tenues · #8FA0FF en cours »),
et **le cadre 48** (anneau terracotta recouvert d'un arc menthe sur 72 % du tour). Le mauve
est la couleur d'une Nuée : sur un anneau qui dit un état, il racontait autre chose.

### 9 · Le comparateur ré-échantillonnait toute la capture
`.frame` se met à l'échelle pour tenir dans la fenêtre : à un viewport de 390 × 844,
`#device` sort à **363,87 × 787,45**, soit 0,933. Les juges le savent ; le comparateur PIXEL,
lui, remontait la capture à 1 — chaque glyphe entre deux pixels, et **aucun écran ne pouvait
tomber à zéro, quoi qu'on corrige.** Mesuré : **430 × 932 donne `#device` exactement
390 × 844.**

### 10 · Et le comparateur capturait avant que l'écran soit composé
À 2 000 ms, `fiche-tenue` sortait **sans sa dalle et sans sa barre Peaufiner**. Le compte de
nœuds visibles se stabilise AVANT que tout soit peint : il faut un plancher de temps ET deux
relevés identiques.

> **La leçon, et elle vaut pour la suite : un comparateur qui redimensionne mesure son
> propre redimensionnement, et un comparateur qui capture trop tôt mesure une transition.**
> Avant d'accuser le dessin, on vérifie l'instrument.

### Et une non-cause, vérifiée : l'app est stable
`scratchpad/stabilite.py` — deux captures du même écran sans rien changer, puis une troisième
après réouverture, hors matière : **0,0 % sur les cinq écrans**. Le grain décoratif
(`.tuto-fond::before`, tiré au `Math.random` et animé) **ne sort pas de la zone de matière**.

---

## 4 quater · CE QUI RESTE — et pourquoi ce n'est pas corrigible

Les décisions de Tom du 29 août ont retiré trois causes sur cinq. Voici les cinq, avec ce
qu'elles coûtent.

### 1 · L'anti-crénelage de deux moteurs — le plancher, ~1,5 à 2 %
Un liseré d'un pixel longe chaque courbe : l'onde d'une fiche, l'anneau d'un Noyau, les
pastilles, les coins arrondis. La planche les dessine en **SVG**, l'app les peint en
**canvas**. Même chemin, même épaisseur, même couleur — deux moteurs de rasterisation.
**Vérifié que ce n'est pas un décalage :** le désaccord minimal est à (0,0), pas à ±1 px.

### 2 · Le modèle de l'anneau du Noyau — ~1,8 % sur une Nuée
La géométrie est **exacte** : 78 px, axe r 35, épaisseur 8 pour « toi » ; 58, r 26, 6 pour
une entité. Mesuré au pixel sur le canevas. **C'est le MODÈLE qui diffère :**

```
la planche   deux arcs   un cercle plein « reste » + un arc « tenu » en dasharray
             cadre 48    reste #F07A2E · tenu #2BE88C sur 72 % du tour
             cadre 10    reste #D0B0FF (la Nuée) · tenu #2BE88C
l'app        trois arcs  tenu #2BE88C · en cours #8FA0FF · à tenir #F07A2E,
                         joints dégradés sur 3 % du tour, proportions réelles
```

L'app dit **trois** états, la planche **deux**. Passer à deux perdrait « en cours » — une
décision de produit, pas une correction. Et les proportions elles-mêmes dépendent des
données. **Les couleurs, elles, sont corrigées** : elles suivent le §3 depuis aujourd'hui.

### 3 · La place de la dalle dans une carte d'Index — ~1 % (Q86, ouvert)
```
carte              planter  crêpes  potager  courir  nager  plongeoir
centre de la dalle    82,5   126,0    62,0    82,5   116,0    82,5    (centre carte 82,5)
```
Trois centrées, trois non — et le cadre 74 place les mêmes dalles à des fractions
**différentes** de la largeur (0,750 contre 0,764 pour « faire les crêpes »). Il n'y a pas de
règle à en tirer : la planche les a posées à la main. **L'app centre.**

### 4 · Le bouton ⇅ — ~0,2 %
Le cadre le rend en `content-box` (**62 × 62**) quand sa voisine, la barre de recherche, est
en `border-box` (270 × 56). Le tableau du §5 écrit **56 × 56** pour les deux, l'app pose
56 × 56, `releve-S4` le valide. **Le document et l'app s'accordent contre un oubli de rendu.**
Voir `ECARTS-MOODBOARD § 0 bis.3`.

### 5 · Les données du potager — sur la Nuée seulement
Les deux planches ne donnent pas les mêmes Promi au potager (voir `ECARTS-MOODBOARD § 0 bis.1`).
Le jeu suit **moodboard-H** pour le contenu — l'Index et le Fil en dépendent — et
**`promi-nuee-toile`** pour la loi du champ, qui fait foi. Les titres diffèrent donc, et
quand l'un tient sur une ligne et l'autre sur deux, la seconde ligne tombe **hors de la boîte
de texte** et se compte. C'est le prix du désaccord entre les deux planches, pas un défaut.

---

## 4 quinquies · CE QUE LES DÉCISIONS DU 29 AOÛT ONT CHANGÉ

| décision | ce qu'elle a retiré | mesuré |
|---|---|---|
| **Q80** · les glyphes sont la seconde exception | la substitution Hanken Grotesk → Apfel comptait comme un écart de dessin sur tous les écrans | écrite en règle au § 8 bis ; `_zonesTexte` couvre désormais aussi les **`<input>` à placeholder** — « ⌕ Rechercher » n'était pas déclaré, faute de nœud texte : la bande 120 de l'Index et du Fil est passée de **10 % à 5 %** |
| **Q84** · `promi-nuee-toile` fait foi | le cadre 58 donne base 232 pour 6 Promi, que la loi ne produit pas ; le cadre 60 donne 282 pour zéro là où la loi donne 460 | `nuee` **17,3 % → 5,2 %** · `nuee-vide` **11,8 % → 5,2 %** |
| **Q83** · un gardé de côté n'a pas de dalle | la boîte de matière était déclarée sur une carte qui ne peint rien — un masque sans matière dessous | `peintCarte` n'annonce sa boîte **qu'après avoir dessiné** |
| **index-3** · la répétition est un artifice | le cadre porte douze cartes dont quatre répètent les premières | mesuré sur les rangées 1 et 2, **fenêtre déclarée et imprimée** : `21,3 % → 2,7 %` |
| **Fil 4** | l'entête comptait `FEED.length` | il compte les gestes qui viennent d'ailleurs — **4**, comme le cadre |

---

## 5 · Ce qui reste à faire — et c'est court

### `redteam_aveugle` — 24/26 · UN seul point, et sa cause est écrite

**Trois rouges sont tombés d'un coup, et ils n'avaient qu'une cause — LE TUTORIEL.**
« tenir au geste » (deux thèmes) et « planter » au second passage échouaient dans le parcours
complet et passaient seuls. Instrumenté à `elementsFromPoint`, sous le doigt :

```
DIV#tutoOv.tuto-ov2 in  [0,0 390x844]  z=120  pe=auto
```

`addPromi` lance le tutoriel du premier Promi **450 ms après la plantation** (`_tutoSeen`).
Il couvre tout l'écran, il prend les événements — et **`closeAll()` ne le connaît pas**. Tout
geste postérieur va donc au tutoriel : le geste de la fiche ne tient rien, et au parcours
suivant le geste de la page + ne plante rien. C'était bien « la même famille que ceux que
`closeAll` a absorbés » : **un calque de chrome qu'aucune fermeture n'atteint.** On le lui a
ajouté, avec **sa propre sortie** (`out`, puis retrait à 340 ms) : rien de réécrit.
L'ordre est sans risque — `addPromi` appelle `closeAll()` **avant** de programmer le
tutoriel ; on ne le tue pas à la naissance, on l'empêche de survivre à l'écran suivant, ce
que dit déjà son bouton final « Explorer mon Promi ». Bloc `lot-TUTO-CLOSEALL`.

> **La leçon, générale :** un rouge qui n'apparaît qu'**en parcours** ne se cherche pas dans
> l'écran qui échoue. **On demande au navigateur ce qu'il y a SOUS LE DOIGT** —
> `elementsFromPoint`, pas `elementFromPoint` : la pile entière, avec `z-index` et
> `pointer-events`. Trois mesures ont suffi, après cinq sessions de suppositions.

**Le rouge restant, le même dans les deux thèmes :** « Nuée · rien ne se superpose ». Le
bouton `#nfAdd` « + Planter un Promi » est peint à y = 776, la barre Peaufiner à y = 760.
**Il n'a pas de place parce qu'il n'en a pas :** aucune ligne « Planter » dans les vingt
écrans du §12, zéro occurrence dans `promi-nuee-toile.html` ; il n'existe qu'au **cadre 86**
— *« Planter un Promi dans la Nuée · DISSOUDRE LA NUÉE → Peaufiner ▴ »*, un contrôle du
**Peaufiner ouvert**. Le déplacer est le prochain lot (le Peaufiner d'une Nuée, cadres 84 à
87) ; le retirer sans l'avoir reposé supprimerait une fonction. `QUESTIONS.md` · Q61.

### La fiche de Nuée — PORTÉE, les 24 écrans à zéro

`redteam_nuee.py` — **22 écrans mesurés, 0 écart**, cinq lignes de critère comme les autres
juges. Sa référence n'est pas dans le fichier : **elle est extraite de
`PROMI-SPECIFICATIONS.md` à chaque passage** pour les vingt écrans du §12, et lue **dans le
moodboard** (cadres 84/86) pour le Peaufiner. Si le document bouge, le juge bouge avec lui.

| | ce qui est porté | où c'est écrit |
|---|---|---|
| **la hauteur du trait** | `base = max(176, 460 − 86 n)`, amplitude 40, Noyaux à `boîte − 29`, méta à titre + 65, fil à méta + 30 | §9 et §12 |
| **la Toile** | densité de semis du §10.6 (douze graines / 390 × 435), dalles du moteur, décalage tiré de l'id | §10.6, §11 · Q62 |
| **l'état vide** | douze graines crème `GLIGHT` dans les deux thèmes, entête à l'encre | §10.6 · Q59 |
| **l'état défilé** | base **58**, amplitude **16**, bande de 114 px, entête 23 / titre 26, fil dès 182 ; la Toile est **la même, remontée** | §9 et §12 · Q64 |
| **le défilement** | le doigt fait défiler **le fil**, pas les réglages ; Peaufiner ne s'ouvre **qu'en touchant sa barre** | §13 |
| **le Peaufiner** | DESCRIPTION · MEMBRES · PIÈCES JOINTES · COMMENTAIRES · Planter · DISSOUDRE | cadres 84 à 87 · Q65 |

**Ce qui reste ouvert, et c'est peu :** Q65 (les cadres 84 et 86 sont deux pages, l'app les
montre d'un seul tenant — s'il faut un geste entre les deux, il manque) ; Q64 (l'entête du
§12 écrit « amplitude = 40 » sur l'écran défilé, contre 16 au §9 et 114 dans son propre
tableau — corrigé dans le sens du §9).

### Le chantier des polices — 0 couple hors face

**En navigateur, une graisse absente se substitue en silence. En Swift, elle casse.** Audit
refait sur l'app d'aujourd'hui (`redteam_polices.py`, qui lit les `@font-face` du fichier —
la liste ne vit que là) : **7 couples absents, 359 éléments**, tous les écrans.

```
                    avant           après
Apfel 500            159 él.   →  ApfelMid 500
Bricolage 800         87 él.   →  Bricolage 700
Apfel 600             32 él.   →  ApfelMid 500
Apfel 400 italique    31 él.   →  Apfel 400        (l'oblique était synthétique)
ApfelMid 400          26 él.   →  Apfel 400
Apfel 700             20 él.   →  ApfelMid 500
Bricolage 400          4 él.   →  Bricolage 600
                     ─────
                     0 couple absent · 0 élément
```

**En JavaScript, et pas en CSS — la raison est écrite dans le bloc `lot-POLICES` :** le
couple dépend de DEUX déclarations, la famille et la graisse, qui vivent rarement dans la
même règle ; réécrire « 800 → 700 » à l'aveugle enverrait un `Apfel 800` sur `Apfel 700`,
tout aussi absent. Et le §9 interdit de nettoyer le CSS. **C'est une couche d'exécution, pas
une correction de source** (Q70) — la table de report fait foi pour le portage Swift.

> **⚠ DEUX PIÈGES PAYÉS SUR CE LOT, tous deux mesurés :**
> **1 · Une graisse lue trop tôt et figée change la hiérarchie.** La première passe posait
> son inline `!important` et n'y revenait plus : « Peaufiner » était lu à 400 avant que la
> feuille pose son 700, reporté sur 600, et gelé là. **La passe se RELIT** — sur un élément
> déjà touché, elle retire d'abord son propre inline, relit la cascade, puis décide.
> **2 · Ne toucher que ce qui porte du texte.** Réécrire la graisse d'un conteneur ne change
> rien à l'écran et pollue le contrat visuel — mesuré : `.dpd-tog` 400 → 600, alors que son
> libellé porte sa propre graisse. 86 écarts sont tombés à 35 avec ce seul filtre.

### Le dernier flake du projet — trois contrôles, une seule cause

`redteam_toile` flottait depuis le début. La cause n'était ni le hasard ni les polices :
**`Toile.dalleTrame` anime la matière avec `performance.now()` et recadre au plus juste sur
l'alpha.** Ni les pixels ni le format d'une dalle ne se répètent d'un rendu à l'autre — un
contrôle bâti dessus ne peut pas être stable.

| contrôle | ce qu'il comptait | ce qu'il compare |
|---|---|---|
| « les intitulés restent » | les pixels clairs de la planche (seuil 200) | `window._plancheComp` — quels intitulés, à quelles cases |
| « le % s'affiche » | les pixels clairs dans le trou de l'anneau | `window._noyauSig` — le chiffre composé, publié par `_sigBloc` |
| « la double encre » | les pixels terracotta et bleus du même trou | `window._sigEncres` — les trois passes décalées, publiées par `_sigText` |

**17/17 sur trois passages consécutifs.** Le principe est inscrit dans `CLAUDE.md §7`, et
c'est le même que celui de `scratchpad/semis_determin.py` : **on compare la composition, pas
la peinture.**

### Le passage d'usage à l'œil — ce que les chiffres ne disaient pas

`scratchpad/usage_oeil.py` : on plante, on remplit, on touche, on enchaîne, dans les deux
thèmes, et **on regarde**. Le parcours passe (planté 25 → 26, tenu au geste, zéro erreur JS).

**Une trouvaille, et aucun juge ne pouvait la voir :** sur un Promi **à moi**, un seul Noyau
à l'écran, la ligne d'état annonçait **« TENUE À DEUX · À L'INSTANT »**. Les mots viennent du
cadre 101, qui montre une parole tenue **avec quelqu'un** — c'est son cas, pas une formule.
Corrigé sans rien inventer : à soi, on écrit le mot que l'app emploie déjà (`STLAB.tenu`),
et rien de plus. **Les cinq lignes du critère mesurent la cote, le style et la peinture —
pas le sens du mot.** Q69.

### Ce que le portage a fait tomber en chemin

| trouvé | ce que c'était |
|---|---|
| **deux boutons « Planter »** | `#nqAddPromi` (balisage d'origine) **et** `#nfAdd`. Le premier se posait à y = 0, par-dessus « ✕ FERMER » — le défaut signalé. Un seul reste, dans le Peaufiner |
| **une bande figée à 232,67 px** | `.dp-nuee::before`, d'un lot antérieur au moteur géométrique. Invisible tant que la boîte était plus haute ; **elle dépasse dès que le champ se réduit**. Elle suit désormais la boîte (Q67) |
| **le crible de la section 2 mord sur la Nuée** | `s2-ouv` passe en `visibility:hidden` ce que SON inventaire ne liste pas. Les cartes d'une Nuée sortaient en `display:block` **et** invisibles (Q66) |
| **un garde pris sur un drapeau** | `bati()` se gardait avec un attribut sur `#dpdCorps` : `openEssaim` rebâtit le poster, les cartes disparaissent, le drapeau reste. **Le garde se prend sur le DOM** |
| **le juge mettait l'app en arrière-plan** | lire la planche dans un second onglet bride `requestAnimationFrame` sur le premier : `_fichePose` repeint sur deux rAF et ne repeignait plus. **On lit la référence d'abord, on ferme, on mesure ensuite** |

### La fiche de Nuée — l'ancien relevé, pour mémoire

`base = max(176, 460 − 86 n)` · amplitude **40** · Noyaux à **`boîte − 29`** · méta à
**titre + 65** · première ligne du fil à **méta + 30**. Mesuré sur une Nuée de trois Promi :
boîte **282**, Noyaux **253**, titre **407**, méta **472**, fil **502 · 588 · 674** —
**l'inventaire au pixel**, et la dernière ligne s'arrête bien à 12 px de la barre.
L'app portait `232 / 282` et `36 / 44`, **deux valeurs qui ne viennent d'aucune règle** : la
fiche de Nuée n'avait jamais été portée.

**Sa Toile aussi est portée** : les trois emplacements figés du cadre 58 ont été remplacés
par la **densité de semis du §10.6** (douze graines pour 390 × 435, soit un pas de 119 px),
jamais moins d'une graine par Promi, les dalles de la Nuée tournant sur les emplacements.
Zéro abscisse nue, à tout n, dans les deux thèmes. Voir Q62.

**Ce qui reste :** les **vingt écrans** du §12 un par un (styles, couleurs, l'état *défilé*
à base 58 / amplitude 16, le §13 « le doigt fait défiler le fil, pas les réglages »), le
**semis de la Nuée vide** (§10.6 : douze graines crème `GLIGHT`, mot-marque à l'encre — à
n = 0 le champ reste mauve nu), les **duos côte à côte** contre `promi-nuee-toile.html`, et le
juge **`redteam_nuee.py`** que le §15 décrit et qui n'existe pas encore.

### L'ancien relevé, pour mémoire — 21/26 · cinq points, deux causes

**Réparés** (en JavaScript, dans `lot-RESIDUS` — le CSS ne pouvait pas : `_ficheCotes` pose
ses `display` en ligne avec `!important`) : **le Cercle payé** ne montre plus ni verre
dépoli ni réclame, et **une Nuée ne se tient pas** (ni trait, ni geste, ni mot de trace).

**Reste :**

| | ce qui ne va pas | ce qu'il faut |
|---|---|---|
| **Nuée · superposition** | `#nqAddPromi` peint à **y = 0**, par-dessus « ✕ FERMER » | une cote. Le §5 le donne à 24 / 46, mais ce y est celui d'un autre cadre. **La fiche de Nuée n'a jamais été portée** — c'est un écran de plus à porter, pas un correctif |
| **parcours · tenir au geste** (×2) | échoue dans le parcours complet, passe seul | trancher : mise en scène du contrôle ou résidu |
| **parcours · planter, 2ᵉ passage** | la page + garde un état du premier | idem |

**Les trois derniers sont probablement UN SEUL défaut** — un état de la page + qui survit à
un parcours entier. C'est le prochain fil à tirer, et le seul qui reste sur l'usage.

⚠ **Un piège payé une fois :** retirer un `display` sans distinction emporte celui que
`_ficheCotes` pose légitimement (les sections 1 et 5 sont tombées à 4 écarts chacune).
**On marque ce qu'on masque et on ne rend que ça.**

### Trois éléments du moodboard restent des FONCTIONS, pas du dessin

Aucun ne manque d'une cote : il leur manque une **décision de produit**. Tous trois sont
dessinés et mesurés là où c'est possible, **aucun n'est branché à un geste**.

| | ce qui manque | état |
|---|---|---|
| **L'Index à trois par ligne** | aucun déclencheur : ni bouton, ni seuil, ni réglage | les deux densités sont portées et mesurées ; la bascule vit dans `window._s4Trois`, qu'aucun doigt n'atteint |
| **« L'autre moitié arrive »** | l'app ne modélise pas l'événement « quelqu'un trace, maintenant » | l'écran est porté et mesuré, avec la position du cadre (`window._instantX = 268`) |
| **« À TENIR · 2 J »** | l'app ne sait pas produire le compte de jours | la carte écrit « À TENIR » seul ; le bandeau du Fil ajoute le temps que l'app affiche déjà |

### Deux écrans de Peaufiner restent à 7 sur 9

Cause identifiée et documentée : `#tenirCv` sort du cadre dès qu'un conteneur positionné
devient son ancêtre (`CLAUDE.md §8`). La parade est de ne jamais faire entrer `#tenirZone`
dans un conteneur de réglages ; les deux écrans restants demandent une réorganisation du DOM
de Peaufiner qui n'a pas été tentée.

---

## 6 · Les contrats de test modifiés — ce qui a changé et pourquoi

**Trois outils ont été touchés. Aucun n'a été desserré.** Le principe, désormais inscrit
dans `CLAUDE.md §7` : *un contrôle qui encode une règle abandonnée se met à jour au niveau de
la décision, jamais en modifiant le comportement pour le faire passer.*

### 6.1 · `redteam_ecrans.py` — de 134/144 à 144/144

Cinq contrôles nommaient l'ancien marquage de l'Index et du Fil (`.ix-bloc`, `.ix-bd canvas`,
`.ix-bj`, `.fd-item`), que la section 4 remplace par `.s4-carte`.

- **Quatre sont de simples renommages** : même intention, nouveau nœud. On le note, on ne
  délibère pas.
- **Un a changé sur le fond** : « **seuls les urgents ont un aplat** » supposait que l'état
  vivait dans le **fond** du bloc (classe `.vif`). **Il vit dans la ligne** — le champ dit
  la nature, la ligne dit l'état, c'est la loi du produit (`CLAUDE.md §3`). Le test était
  **périmé**, comme « sens » et « quand » l'ont été. Il vérifie désormais qu'**aucune carte
  n'est peinte d'une couleur d'état** : il protège la même chose, au niveau de la règle
  actuelle. **Validé par Tom.**

Version d'origine conservée : `sauvegardes/redteam_ecrans-avant-S4.py`.

### 6.2 · `releve-design.py` — le sélecteur, puis le refigement

L'outil ouvrait ses fiches en cliquant `.ix-bloc.vif / .menthe / .nuee` dans l'Index. La
carte porte désormais la même information en attributs (`data-nat`, `data-etat`) et l'outil
les emploie — **rien de neuf, le même renseignement**.

**La référence a été refigée le 18 août 2026**, après validation des cinq sections.
Elle datait d'avant la section 1 et ne mesurait plus rien : **556 écarts identiques avant et
après le portage** (comparaison ligne à ligne des deux relevés — aucune ligne nouvelle).
Elle compte maintenant **6 configurations et 142 éléments**, et rend `✅ AUCUN ÉCART`,
stable sur deux passages consécutifs.
Ancienne référence conservée : `sauvegardes/design-reference-avant-portage.json`.

> ⚠ `CLAUDE.md §8 bis` annonce « 148 propriétés sur 26 éléments ». Le compte a changé avec la
> réécriture des fiches ; l'outil imprime le sien à chaque refigement, c'est lui qui fait foi.

### 6.3 · Trois sondes de juge corrigées — des faux rouges, pas des régressions

Ces trois-là ne mesuraient pas ce qu'elles croyaient. **Aucune n'a été desserrée : elles ont
été rendues justes.**

| Sonde | Ce qu'elle faisait | Ce qui a été corrigé |
|---|---|---|
| Le trait du Fil | Comptait les **colonnes** traversées | **Le trait du Fil est VERTICAL** (§3.10) : on compte les **lignes**. Il devenait invisible dès qu'une dalle était petite |
| La boîte du trait (S5) | Lisait `style.height` | **Mélangeait deux échelles** — `#device` est mis à l'échelle par une transformation. Sortait **412** sur un canevas de **384**. Elle se mesure dans le repère du cadre, comme tout le reste |
| La couleur de la ligne (S5) | Cherchait le premier pixel voisin à ±9 px | **Elle lit LE CENTRE du trait.** Sur « le trait se referme », tout le champ au-dessus de l'onde est menthe : la ligne d'encre passait pour menthe |

### 6.5 · Le lot du 19 août — quatre sondes réécrites, aucune desserrée

**La décision « la matière remplit le champ » a déplacé le nœud que quatre sondes visaient.**
Toutes lisaient **le champ en haut du cadre**, « loin de la dalle et du trait ». Ce point est
désormais **de la matière**. Aucune règle n'a changé, aucun seuil n'a bougé : c'est le point
de lecture qui est faux. `CLAUDE.md §7`, cas « la sonde vise le mauvais nœud ».

| sonde | ce qu'elle lisait | ce qu'elle lit |
|---|---|---|
| `redteam_tonsurton` · le trait | « le pixel le plus ÉLOIGNÉ du champ le long de l'onde » — donc une **dalle** dès qu'il y a de la matière | **la ligne par SA COULEUR**, du jeu du §2.1 bis, en écartant toute couleur trop proche du champ (sinon, sur « le trait se referme », le champ menthe passait pour la ligne) |
| `redteam_tonsurton` · le champ | le pixel en (23, base × 0,06) | **la couleur que l'écran DÉCLARE** (`_ficheEcran().natCol`, `_ppEcran()`) — la valeur de l'app, lue à l'exécution |
| `releve-S3-page-plus` | « la dalle ≠ l'aplat lu en (195,40) », et « un point à plus de 60 de cet aplat » | l'aplat = **`_onde.NATCOL[nat]`** ; les points **par leur couleur** |
| `releve-S5-instant` | le champ en (20,20) | le champ = **la couleur dominante du POURTOUR** du cadre — le seul endroit qu'une matière centrée mise en couverture ne recouvre pas. Toujours au pixel |
| `releve-S1-fiches` | « le mot-marque est `#F4EEE1` » | « le mot-marque est **l'une des DEUX encres** du produit » — c'est le §10.6, généralisé (Q59) |

**Bénéfice inattendu :** la première réécriture a **corrigé un flottement antérieur**.
« bandeau du Fil · le pire » sortait 26/26 **puis** 24/26 sur l'app **inchangée**, deux
passages consécutifs — sa recherche de ligne attrapait la dalle quand celle-ci mordait sur la
colonne du trait. `redteam_tonsurton` rend maintenant **26/26 sur trois passages de suite**.

Versions d'origine : `sauvegardes/redteam_tonsurton-avant-matiere.py`,
`sauvegardes/releve-S1-fiches-avant-matiere.py`, `sauvegardes/releve-S3-page-plus-avant-matiere.py`,
`sauvegardes/releve-S5-instant-avant-matiere.py`.

### 6.4 · Les flakes connus, reconfirmés

- **`redteam_toile`** — « Mes Promi : les intitulés restent », sonde à seuil sur un canevas
  animé. Vu à 15/16 puis 14/16, puis **16/16 et 16/16** sur deux passages consécutifs.
  **Un échec isolé ne prouve rien : il faut relancer.**
- **`redteam_geste`** — « l'anneau est peint à sa nouvelle place », oscille 12↔13/13.
  Même règle. À réécrire un jour : comparer l'anneau à sa propre référence.

---

## 7 · Les questions restées ouvertes

Onze questions, **Q41 à Q51 dans `QUESTIONS.md`**. Trois demandent une décision de produit
(marquées ★) ; les autres sont des choix conservateurs déjà appliqués, à confirmer.

| | Sujet | Ce qui a été fait en attendant |
|---|---|---|
| **Q41** | Le moodboard ne centre pas toujours la dalle d'une carte ; le §2.7 dit « toujours centrée » | Le document est appliqué : **centrée** |
| **Q42** | Les bases 376 et 372 sortent de l'échelle du §2.5 | **Bornées.** Corrigé dans le document — voir §4 |
| **Q43** | « avec +4 » n'a pas de version sans membre | Le mot que `buildIndex` écrit déjà : **« perso »** |
| ★ **Q44** | « À TENIR · 2 J » — l'app ne sait pas produire le compte de jours | **« À TENIR »** seul sur la carte ; le Fil ajoute le temps que l'app affiche déjà |
| ★ **Q45** | L'Index à trois par ligne n'a aucun déclencheur | Les deux densités portées, la bascule non branchée |
| **Q46** | Cinq contrôles de `redteam_ecrans` nommaient l'ancien marquage | Réécrits au niveau de la décision — **validé** |
| ★ **Q47** | « L'autre moitié arrive » n'a aucun déclencheur observable | Écran porté, position du cadre, sans déclencheur |
| **Q48** | La ligne de « le trait se referme » est à l'encre dans les deux thèmes — le §2.1 bis ne prévoit pas ce cas | Porté tel quel ; le §2.1 bis devrait le dire |
| **Q49** | « Rachel vient de tracer sa moitié » — sans autre personne, il manque un mot | La seconde phrase seule : **« Le dessin existe. »** |
| **Q50** | La dalle de l'instant ne suit pas la formule du §2.7 (180 × 150 contre 187 × 156) | **Les valeurs des cadres**, qui font foi |
| **Q51** | Combien de temps dure « juste après » ? | Tant que la fiche est ouverte |

**Questions plus anciennes toujours ouvertes :** Q37 (« planter au bouton » contre « garder
de côté » — deux mots pour un même créneau), Q38 (la taille de la phrase sur un choix
ouvert, écart assumé de 2 px), Q40 (la coupure de la question du cadre 17, obtenue par la
largeur et non par le moyen du document). Et le **point ouvert du §3 de `CLAUDE.md`** : le
décalage de teinte de 150° des traits, que Tom juge parfois hors palette — **non tranché,
ne pas trancher seul.**

---

## 8 · Les pièges qui ont coûté du temps — la liste courte

Ceux de `CLAUDE.md §8` restent tous valables. Ces cinq-là sont ceux que le portage a ajoutés
ou reconfirmés, et qui reviendront :

1. **Un `display` posé EN LIGNE bat un `!important` de feuille.** Le geste restait à l'écran
   sur les trois cadres de l'instant : la section 1 lui pose `display:block!important` en
   ligne. **On le sort en JavaScript, pas en CSS.**
2. **L'encre du CORPS n'est pas celle du CHAMP.** Le corps est **crème en thème clair** : un
   titre posé en crème y disparaît. Vu au duo — le titre « faire les crêpes » purement absent
   du cadre 101 clair. Le juge de présence peinte le rattrape (Δ luminosité < 42).
3. **Peindre après insertion (§4.5).** Une seule passe laissait la dalle vide par
   intermittence. On rejoue à **0, 60, 200 et 600 ms**, comme `peintMinis`.
4. **Un rendu qui remplace son propre marquage doit mémoriser ses entrées.** `_s4Index`
   remplace le contenu de `#indexList` : au second appel les `.ix-bloc` de l'app n'existent
   plus, et l'écran restait figé sur la densité du premier rendu.
5. **Le crible se pose nœud par nœud, jamais sur un conteneur ni une famille.** Deux fois
   déjà, un balayage en bloc a emporté un panneau qu'un doigt ouvre.

---

## 9 · Les outils

| Outil | Ce qu'il fait |
|---|---|
| `releve-S1-fiches.py` … `releve-S5-instant.py` | **Les cinq juges de section.** Cotes, styles, collisions, débordements, présence peinte, dans les deux thèmes |
| `releve-design.py` | Le contrat visuel — 6 configurations, 142 éléments. `--figer` pour recaler après validation |
| `redteam*.py` (8 batteries historiques) | Le comportement. **Aucune livraison si une régresse** |
| **`redteam_champs.py`** | **remplit** chaque champ : atteignable · accepte · la donnée reçoit · l'écran montre |
| **`redteam_pastilles.py`** | **touche** chaque pastille et vérifie qu'elle change quelque chose |
| **`redteam_enchaine.py`** | **enchaîne** deux écrans et compare le second à lui-même ouvert seul |
| **`redteam_fonctions.py`** | l'**inventaire des fonctions** qu'aucune refonte ne doit faire disparaître |
| **`redteam_photo.py`** | la photo de fiche, et sa présence partout où la matière s'affiche |
| **`redteam_tonsurton.py`** | un trait n'est jamais à moins de **42** de son champ (§2.1 bis) |
| **`redteam_aveugle.py`** | le Cercle payé · la Nuée en profondeur · un parcours entier |
| **`redteam_nuee.py`** | **la fiche de Nuée** : les 20 écrans du §12 + les 4 du Peaufiner, cinq lignes de critère. Référence extraite du document et du moodboard, jamais recopiée |
| **`scratchpad/semis_determin.py`** | **le semis d'une Nuée ne change jamais** — 3 ouvertures × 2 thèmes × 2 densités de pixels. Compare LA CASE, pas les pixels |
| **`scratchpad/mesure_vide.py`** | le bandeau de couleur nue entre la matière et le trait, et quelle base est **au plancher** |
| **`redteam_polices.py`** | **aucune graisse hors des six faces embarquées.** Il lit les `@font-face` du fichier : embarquer une face suffit à la lui faire connaître |
| **`scratchpad/duo_pixel.py`** | **superpose le cadre de la planche et la capture de l'app**, rend la part de pixels qui diffèrent, les bandes où ça diffère, et trois images (planche · app · différence). **Il classe, il ne valide pas** — voir §4 bis |
| **`scratchpad/usage_oeil.py`** | **le passage d'usage à l'œil** — planter, remplir, toucher, enchaîner, deux thèmes, et les captures qui vont avec |
| `scratchpad/duo.py <nom> <thème> <dossier>` | Colle le cadre du moodboard et la capture d'app **côte à côte**, avec une règle de cotes. **Un juge à zéro ne fait pas un écran** |
| `scratchpad/cap_s1b/s2/s3/s4/s5.py` | Les captures, cadrées sur le device, onboarding passé |
| `scratchpad/liste_cadres.py` | L'ordre **réel** des 102 cadres du moodboard — il n'est pas celui du document |
| `scratchpad/dump_cadre.py <n>` | Le HTML complet d'un cadre : **c'est là que sont les règles que le document ne donne pas** |
| `scratchpad/probe_ix.py` | Instrumente l'ouverture de l'Index et du Fil |
| **`scratchpad/mesure_vide.py`** | **Le bandeau de couleur nue entre la matière et le trait**, écran par écran, deux thèmes. Dit aussi quelle base est **au plancher**. C'est lui qui tranche « vide » contre « boîte du §2.7 » |

**Le serveur :** `python3 -m http.server 8752`, puis `http://127.0.0.1:8752/app.html`.
**Utiliser `127.0.0.1`, jamais `localhost`** — il bascule en https et échoue.

---

## 10 · Les sauvegardes

```
sauvegardes/avant-matiere-champ.html    l'état d'entrée du lot du 19 août
sauvegardes/lot-matiere-champ.html      la matière remplit le champ + la Nuée au trait entier
sauvegardes/lot-tuto-closeall.html      + le tutoriel que closeAll ne fermait pas
sauvegardes/lot-nuee-hauteur.html       + la hauteur du trait d'une fiche de Nuée
sauvegardes/lot-matiere-tuto-nuee.html  la première formulation, trop large (conservée)
sauvegardes/avant-plancher.html         l'état d'entrée de la correction
sauvegardes/lot-plancher.html           le vide corrigé au plancher
sauvegardes/avant-defile.html           avant l'état défilé
sauvegardes/lot-nuee-vingt-ecrans.html  les 20 écrans du §12 à zéro
sauvegardes/avant-peaufiner-nuee.html   avant le Peaufiner d'une Nuée
sauvegardes/lot-nuee-complete.html      la fiche de Nuée portée
sauvegardes/avant-flake-toile.html      avant la réécriture des contrôles au pixel
sauvegardes/lot-peauf-nuee-defile.html  le Peaufiner d'une Nuée, en deux pages qui défilent
sauvegardes/avant-polices.html          l'état d'entrée du chantier des polices
sauvegardes/lot-polices-usage.html      LE POINT DE REPRISE — polices + passage d'usage
sauvegardes/design-reference-avant-nuee.json   la référence visuelle d'avant le lot Nuée
sauvegardes/s3-complete.html            fin de la section 3
sauvegardes/avant-S4-index-fil.html     état d'entrée de la section 4
sauvegardes/s4-index-fil.html           fin de la section 4
sauvegardes/s5-instant.html             fin du portage (sections 1 à 5)
sauvegardes/reparations-livrees.html    les sept correctifs de CASSE.md
sauvegardes/lot-photo-livre.html        la photo de fiche
sauvegardes/lot-tonsurton.html          l'audit du ton sur ton
sauvegardes/lot-six-verts.html          les six chiffres d'usage au vert
sauvegardes/lot-aveugle-21.html         + le Cercle payé et la Nuée  ← LE POINT DE REPRISE
sauvegardes/redteam_ecrans-avant-S4.py  la batterie avant réécriture des cinq contrôles
sauvegardes/design-reference-avant-portage.json   la référence visuelle d'avant le portage
sauvegardes/ETAT-DES-LIEUX-v592.md      l'état des lieux d'avant le portage
```

---

## 11 · La dette technique — le point le plus grave

### Les chiffres

```
fichier              1 535 Ko
règles CSS           2 400
dont mortes          54 %
!important           2 415
blocs <style>        24
blocs <script>       33
```

### Le problème

Le dernier bloc `<style>` fait **116 Ko et contient environ 70 sections**
ajoutées au fil des tours, dont beaucoup se contredisent. Certaines propriétés
sont déclarées **jusqu'à dix fois** sur le même sélecteur.

Conséquence directe : **une modification peut ne rien changer visuellement** si
une règle postérieure l'écrase. C'est arrivé de nombreuses fois et c'est la
première cause de perte de temps.

### Cinq tentatives de nettoyage, cinq échecs

| Méthode | Gain | Écarts mesurés |
|---|---|---|
| Déduplication des propriétés (dernier bloc) | 127 → 116 Ko | **0** ✅ appliquée |
| Compactage de tous les blocs | 582 → 454 Ko | 67 ❌ |
| Suppression des règles mortes (relevé DOM) | 42 % | 554 ❌ |
| Suppression par analyse statique | 16 % | 4 351 ❌ |
| Fusion des sélecteurs identiques | 116 → 113 Ko | 814 ❌ |
| Retrait des règles prouvées sans effet | 116 → 94 Ko | 6 384 ❌ |

**La conclusion, vérifiée :** retirer une règle, même prouvée sans effet visuel,
change les index des suivantes et donc leur ordre dans la cascade. Deux règles
de même spécificité échangent leur priorité.

### La recommandation

**Ne pas nettoyer.** Le coût du risque dépasse le gain.

À la place : **écrire les nouvelles règles dans un bloc neuf, discipliné** — une
déclaration par propriété, pas d'`!important` sauf nécessité prouvée. La dette
existante reste, mais elle cesse de croître.

Pour le portage Swift, ce CSS ne sera de toute façon pas repris.

---


---

## 12 · Les performances

```
ouverture Index    465 ms
ouverture Fil      268 ms
ouverture Aura     185 ms
requestAnimationFrame   38 / seconde  (était 186 avant correction v591)
```

**Corrigé en v591 :** un `MutationObserver` qui s'auto-déclenchait faisait
tourner une boucle en permanence — 3 rAF par image. C'est ce qui faisait ramer
l'app sur iPhone et empêchait même les captures d'écran d'aboutir.

**Corrigé en v561 :** `syncAll()` reconstruisait les cinq surfaces à chaque
changement, même celles hors écran. Il ne reconstruit plus que ce qui est visible.

---

---

## 13 · Ce qui bloque quoi, aujourd'hui

```
Les quatre défauts de redteam_aveugle
   └─ bloquent : rien d'autre — mais ce sont les seuls défauts d'usage qui restent
   └─ deux d'entre eux demandent du JAVASCRIPT, pas du CSS (l'inline de _ficheCotes)

Les trois décisions de produit (l'Index à trois par ligne · « l'autre moitié arrive » ·
le compte de jours)
   └─ bloquent : ces trois écrans, dessinés et mesurés, mais branchés à aucun geste

Les deux écrans de Peaufiner (7/9)
   └─ bloqués par : #tenirCv, qui sort du cadre dans un conteneur positionné

Le décalage de teinte de 150° des traits (CLAUDE.md §3, point ouvert)
   └─ bloque : la validation visuelle définitive de toutes les fiches
```

---

## 14 · Si tu reprends demain

0. **RELANCE LE SERVEUR ET DONNE LES TROIS ADRESSES, EN TÊTE DU PREMIER MESSAGE.**
   `python3 -m http.server 8752 --bind 127.0.0.1`, puis `127.0.0.1:8752/app.html`,
   `/promi-moodboard-H.html`, `/promi-nuee-toile.html`. **Le port est 8752** — tous les outils
   le portent en dur. Vérifie qu'il ne tourne pas déjà : `lsof -nP -iTCP:8752 -sTCP:LISTEN`
   (le processus s'appelle **`Python`**, majuscule — un `grep python` ne le voit pas).
   C'est la première règle de `CLAUDE.md`.

1. **Lis `CLAUDE.md`** — il fait autorité sur tout le reste, et il a deux règles neuves
   (le contrôle périmé, §7 ; les pièges du §8).
2. **`PROMI-SPECIFICATIONS.md` est ta spécification** — cotes absolues et style de chaque
   élément. **Le §3.9 bis contient désormais la loi de la carte : ne la redéduis pas.**
3. **`promi-moodboard-H.html` est l'image de contrôle**, et parfois la source de la règle.
4. **Ouvre le navigateur.** Playwright lit des données, il ne voit pas qu'un écran est cassé.
   **Un juge à zéro ne fait pas un écran** — regarde les duos, dans les deux thèmes.
5. **`QUESTIONS.md` est le journal des décisions prises sans Tom.** Devant une ambiguïté :
   écris la question, prends l'option la plus conservatrice, **et continue**. Et si c'est un
   **mot** qui manque et qu'il n'existe nulle part : écris le plus sobre, note-le « à
   valider », avance (`CLAUDE.md §2`).
6. **Lance les sept contrôles d'usage AVANT de réparer quoi que ce soit.** Un juge de cote
   ne voit pas qu'un champ ne se remplit pas. C'est la leçon la plus chère du projet.
7. **Un contrôle rouge est soit un vrai défaut, soit un contrôle qui vise le mauvais nœud.**
   Sur ce lot, **cinq** rouges sur huit étaient des contrôles qui visaient à côté : les
   pastilles de Peaufiner (elles se déplient), le menu de tri (le voile, pas le panneau),
   `#addPromi` (au repos on trace, le bouton vient après la bascule), le créneau « quand »
   (retiré par Q28), le verbe d'un Chiche (il n'a pas d'alternative).
   **Vérifie toujours au doigt avant de corriger le produit.**
8. **Un rouge qui n'apparaît qu'EN PARCOURS ne se cherche pas dans l'écran qui échoue.**
   Demande au navigateur ce qu'il y a **sous le doigt** : `elementsFromPoint` — la pile
   entière, avec `z-index` et `pointer-events`. C'est ainsi que le tutoriel a été trouvé en
   trois mesures, après cinq sessions de suppositions.
9. **`redteam_polices.py` avant tout lot de dessin.** Une graisse ajoutée sans face part
   en substitution silencieuse ici, et casse en Swift. Le contrôle lit les `@font-face` du
   fichier : si tu en embarques une, il la connaît au passage suivant.
10. **Un rouge qui n'apparaît qu'après un rendu coûteux n'est pas un flottement.**
   `releve-S5-instant` a sorti « 4 écarts » puis « AU VERT », sans rien changer — profil de
   flake. **Ce n'en était pas un :** le rouge est tombé entre le patch de densité et le
   cache par id, quand `dalleTrame` était appelé une fois par case. L'app ramait, le canevas
   n'était pas fini quand le juge l'a lu. Quatre passages consécutifs au vert depuis.
   **Avant de classer flake : cherche ce qui a ralenti le rendu.** Et `redteam_toile` a
   tourné **dix minutes sans rendre la main**, deux fois, pour la même cause (Q63).
11. **LE PORTAGE EST FINI.** Cinq sections + la fiche de Nuée, toutes les batteries vertes,
   `redteam_aveugle` à 26/26. Ce qui reste est une **validation** : `releve-design.py`
   attend un `--figer` de Tom sur les 10 écarts du bouton déplacé, et Q65 attend son avis
   sur les deux pages du Peaufiner. **Le prochain chantier n'est plus du portage** — voir
   les trois décisions de produit du §5 (l'Index à trois par ligne, « l'autre moitié
   arrive », le compte de jours) et la dette CSS du §11. (cadres 84 à 87) : c'est lui qui donne sa
   place à « + Planter un Promi » et à « DISSOUDRE LA NUÉE », et c'est le dernier rouge de
   `redteam_aveugle`. Ensuite, les vingt écrans du §12 et le juge `redteam_nuee.py` (§15).

## 29 août 2026 — lot « rien ne survit » + Q30 levée de sa borne

**Point de reprise : `sauvegardes/lot-rien-ne-survit.html`.**

**Ce qui est fait et vérifié**
- **La cause générale des écrans vides**, en trois couches (Q91) : ce qu'un écran masque
  (`data-masque`), ce qu'il pose en ligne (`data-pose`), ce qu'il bâtit (registre
  `window._rangeurs`). `closeAll` défait exactement ça, et rien de plus.
- **`redteam_vide.py`**, le contrôle qui manquait : il **enchaîne** 15 écrans sans
  recharger, 2 tours × 2 thèmes. **61/61.** Prouvé contre la version fautive : **28/61**.
- **Q92 — la teinture de Q30 n'était appliquée nulle part sur une fiche** (bornée à
  `auPlancher`, faux partout). Levée. La dalle de fiche est stable et lisible : écart de
  luminosité **97** sur le champ bleu, quatre chargements neufs.
- **Les 32 captures ont été regardées une par une.** Aucun écran vide, aucun élément
  d'entête, trait, titre ou état manquant.

**Au vert :** redteam_ecrans 146 · redteam 15 · redteam2 10 · redteam3 18 · demande 19 ·
toile 17 · geste 13 · verbe 6 · filets 0 parasite · aveugle 26 · fonctions 22 ·
tonsurton 26 · formes 38 · nuee 24 écrans 0 écart · polices 0 couple absent · champs 22 ·
enchaine 24 · pastilles 12 · photo 27 · phrase 6 · **vide 61** · S1 · S2 · S3 · S4 · S5 ·
`releve-design` AUCUN ÉCART.

**Ce qui reste ouvert — voir QUESTIONS.md · Q93** (huit écarts vus à l'œil, un lot chacun).
Le premier est un **fork réel** : une dalle peut sortir invisible dans l'Index et le Fil,
et les deux règles qui s'appliquent se contredisent (§3 interdit absolu du ton sur ton
contre §4 / Q30 bis qui borne la teinture à la bande haute).

## 29 août 2026 (soir) — trois corrections de dessin, le champ qui cède, l'écran encombré

**Point de reprise : `sauvegardes/lot-trois-corrections.html`.**

**Ce qui est fait et vérifié**
- **Le tiroir ne se peint plus par-dessus un écran.** Trois couches déjà traitées le matin
  (masque · style en ligne · nœuds bâtis) ; s'y ajoute **l'invariant**, désormais dans
  `redteam_vide.py` : *le corps du tiroir ne se voit QUE s'il est déplié*, et une fiche ne
  porte jamais un nœud du tiroir de Nuée (`.s2-titre`, `.s2-bouton`, `.s2-fermer`).
  On vérifie l'état, plus l'itinéraire. Le contrôle **attend l'écran posé** au lieu d'un
  délai fixe — il sortait un faux rouge une passe sur deux.
- **Q93 pt 1 — le champ cède.** Quand la dalle et le champ se rencontrent, c'est LE CHAMP
  qui bouge : luminosité seule, dans l'espace HSL, la teinte de nature intacte. Le §4 reste
  entier — **aucune teinture hors bande haute**. Mesuré, décision publiée par le peintre
  (`data-cede`) : **minimum 42** sur toutes les cartes d'Index et tous les bandeaux du Fil,
  deux thèmes, deux chargements.
- **Les trois corrections de dessin, toutes fiches, toutes natures** : le mot du geste
  remonte entre le trait et les disques ; les textes centraux montent d'un cran (21→23,
  38→42, 12,5→13,5), le titre redescendant d'un point à la fois si la ligne casse
  (plancher 38) ; sans mot du geste, le bloc remonte de 24.
- **Q30 étendue là où elle manquait** : la teinture s'applique aussi à **l'instant**, qui
  peignait sa dalle non teintée — `releve-S5` le relevait, « le centre a exactement la
  couleur du champ ».
- **Le gardé de côté** : `window._ppGarde` était lu et jamais posé. Posé à `reprendreBrouillon`.
  L'aplat disparaît, « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS » apparaît, le rond photo s'efface.
- **Le titre d'une carte d'Index ne touche plus l'état** (CASSE.md) : 0 débordement,
  0 chevauchement, deux densités, deux thèmes.
- **Le mot du geste de la page +** suit l'état (Q97) ; **« DANS 2 JOURS »** vient du cadre 44
  et ne se calcule plus sur l'horloge.
- **La teinture mauve de la bande d'une Nuée, posée puis RETIRÉE** — Q94, j'avais mal lu la
  planche.

**Au vert :** les 20 batteries · les 5 juges · `releve-design` (refigé : 28 écarts, tous sur
`à qui` / `titre` / `état` d'une fiche, c'est-à-dire le lot, rien d'autre).
**Contrats réécrits au niveau de la décision (§7)**, originaux dans `sauvegardes/` :
`releve-S1-fiches` (les cotes se déduisent de la règle au lieu d'être recopiées ; le titre a
une RÈGLE, pas une taille), `releve-S3-page-plus` (le mot du geste), `releve-S4-index-fil`
(le titre d'une carte), `releve-S5-instant` (l'état à 13,5).

**Les 32 captures ont été regardées une par une.** Aucun écran vide, aucun écran encombré.

**Ce qui reste, et pourquoi je ne l'ai pas fait :** Q95 (le potager à 7 Promi) et Q96
(l'anneau d'une personne) demandent tous deux **d'inventer des Promi de démonstration** —
la planche annonce des nombres qu'elle ne nomme pas. Le §9 l'interdit. Il manque des mots.

## 29 août 2026 (nuit) — l'air, les Réglages, le jeu de démonstration

**Point de reprise : `sauvegardes/lot-air-et-demo.html`.**

- **L'air rendu.** Le cran du soir avait mangé l'espace partout où une cote dérivée était
  calculée pour l'ancienne taille : `à qui → titre` 6,9 → 4,7 sur les cinq états, l'état
  −1,1 sous chaque fiche et chaque Nuée. Les cotes sont réécrites dans la bonne unité
  (« hauteur du bloc + air ») : à l'ancienne taille elles redonnent le moodboard au dixième.
  Et le mot d'un gardé de côté a retrouvé les **23 px** du cadre 26 (il en avait 9).
- **`redteam_air.py`**, la 21ᵉ batterie : l'espace réel entre deux blocs de texte, 36 écrans,
  **391 paires**, référence `air-reference.json`, `--figer` comme `releve-design`.
  Prouvé à **18 rouges** sur la version « cran sans les écarts ».
- **Les Réglages** : l'encart du profil retiré, photo et nom sur le fond (Q99).
- **Le jeu de démonstration** complété avec les mots de Tom (Q100) — potager 9 Promi,
  Index 16, anneau de Rachel à deux arcs. Q95 et Q96 sont closes.

**Au vert :** 21 batteries · 5 juges · `releve-design`. Les 32 captures regardées une à une,
deux thèmes : aucun écran vide, aucun encombré, aucun texte qui touche son voisin, aucun ton
sur ton.

**Prochain : le Studio, l'Aura, le partage.**

## 29 août 2026 — le champ porte toujours sa nature

**Point de reprise : `sauvegardes/lot-champ-de-nature.html`.**

- **Le défaut signalé.** Sur la page + en thème clair, le champ sortait **crème** — la
  couleur du corps : la dalle flottait sur du vide et « trace pour planter » était posé sur
  du crème. Cause : ma lecture fautive de Q83. « Un gardé de côté n'a pas de **dalle** » ne
  dit rien du **champ**, et la même décision précisait « sa carte d'Index garde le champ de
  nature, **sans matière** ». J'avais éteint l'aplat à **trois** endroits — la fiche, la
  page +, la carte d'une Nuée vide. Les trois sont corrigés : l'aplat reste, `sansMatiere`
  prend le relais.
- **`redteam_champ.py`**, la 22ᵉ batterie, 16 écrans × 2 thèmes → **32/32**. Au-dessus du
  trait : aucun pixel de couleur de corps, aucun champ transparent, et **chaque peintre
  déclare ce qu'il a versé** (`data-champ`). Prouvé à **2 rouges** sur la version au champ
  éteint (« le champ est TRANSPARENT à 96 % — le corps se voit dessous »).
- **`releve-S3` réécrit au niveau de la décision** (§7) : il exigeait « pas d'aplat sur un
  gardé de côté », il exige maintenant l'inverse. Original en
  `sauvegardes/releve-S3-page-plus-avant-champ.py`.
- **Le potager garde ses neuf Promi** — l'encart dit le contenu réel (décision Tom).

**Au vert :** 22 batteries · 5 juges · `releve-design`. Les 32 captures regardées une à une,
deux thèmes : aucun écran vide, aucun encombré, aucun texte qui touche son voisin, aucun ton
sur ton, **aucun champ blanc**.

**Prochain : le Studio, l'Aura, le partage.**

---

## Lot du 2 septembre 2026 — LE PLATEAU DU STUDIO, POSÉ PARTOUT À SA PLACE

**Demande de Tom** (1er septembre) : *« on repart de celui de studio qui fait référence,
déploie-le en changeant les titres et les spécificités liées à chaque page ; la mise en
page d'avant était logique, fallait juste du fine tuning. »* Puis : *« go full
verifications et focus. »*

### Ce que la vérification a trouvé, et que le lot précédent avait manqué

Le lot précédent posait l'encart **dans le flux**, à la place de l'ancien titre : il
héritait donc du `padding-top` de chaque écran. Mesuré, chaque écran ouvert **par sa vraie
porte** (jamais en forçant `.show`) :

```
Réglages 0 · La langue 38 · La confidentialité 38 · Aura 54 · Arranger 54
Comprendre ton Aura 76 · Le Cercle 203 · Partager 0 × 0 hors cadre
```

La référence est à **40**. Deux écrans seulement y étaient — l'Index et le Fil, les deux où
je l'avais posé **en absolu**. C'est donc l'absolu qui est la règle.

### `lot-PLATEAU-PARTOUT`

1. **La géométrie se pose EN LIGNE**, pas en feuille — 24 / 40 / 342 × 60, rayon 30,
   padding 26, fond du corps, contour 2 px d'encre, titre Bricolage 700 / 27.
2. **L'écart d'origine est rendu** : `padding-top` = 100 + l'écart mesuré avant le lot
   (28 aux Réglages, 4 à l'Aura, 8 à Arranger / la langue / la confidentialité, 16 à
   Comprendre ton Aura). On préserve l'ÉCART, pas la position.
3. **Le plateau ne défile pas** : aux Réglages il vivait dans `#stScroll`, il est remonté
   en enfant direct de l'écran, comme au Studio.
4. **Partager** : son plateau est `#shcTitre` (contenu `.t` / `.f`, pas `.enh-t` /
   `.closeb`) — conformé nommément ; l'encart en doublon, mesuré 0 × 0 hors cadre, ne se
   peint plus.
5. **Le Cercle** : `.pl-eb` **est** le titre du plateau (déplacé, pas dupliqué) — je
   l'avais masqué, ce qui vidait le plateau. Rétabli.

### Quatre pièges du §8 rencontrés, tous documentés

- **Un `.screen` ne coïncide pas avec `#device`** — `#langScreen`, `#privScreen` et
  `#plusScreen` sont enfants de `.frame`, 422 × 876, l'appareil à 16, 16 dedans. Lu dans
  l'**arbre** (`contains`), jamais dans la disposition : `offsetParent` vaut `null` tant
  qu'un écran est masqué, et le décalage n'arrivait qu'au deuxième passage.
- **Une cote mesurée sur elle-même oscille** — ma première correction comparait deux
  `getBoundingClientRect` **pendant la transition d'ouverture** et a écrit des cotes
  fausses sur trois écrans qui étaient justes (Réglages large de 242,7 · Fil x −20,7 ·
  Index y −65). Repayé le piège de `cale()` au Studio.
- **Piège de spécificité** — `#settingsScreen > :not(#stTrameCv){width:auto!important}`
  pèse **deux ids** (le `:not(#id)` compte l'id qu'il contient) et bat `#device .enh`.
  Le plateau retombait en largeur automatique dans un parent `flex`, donc à la largeur de
  son contenu, et le titre suivait : **342 → 242,7 → 209,4**, titre **27 → 19**, d'une
  passe à l'autre.
- **Une course, pas une cote** — le plateau est BÂTI par `lot-ENCART-HAUT` ; à la
  toute première ouverture, `recale` passait avant que le nœud existe. On chaîne :
  bâtisseur → remonte → polices → recale → `_harmonie` (qui dimensionne les titres, donc
  parle en dernier).

### Deux défauts trouvés au balayage, sur la page Partager

- **`#shNyPctRow` « % d'harmonie »** flottait à **y 58 → 87, sur le plateau du titre**, à
  opacité 0,34. Orphelin de l'ancien Noyau : il vit dans `#shTray`, qui est en
  `display:contents` — donc **rien ne le masque**. Sa fonction est déjà dans le tiroir
  neuf, sous « CE QU'IL MONTRE → Harmonie chiffrée ».
- **Un tap ailleurs ne referme plus le tiroir** — la fonction existait sur l'ancien écran
  et s'était perdue à la refonte.

### `#plHeroCv` recadré

Le héros du Cercle débordait du téléphone de **16 px à gauche et 24 à droite** (il est
dessiné pour le cadre, pas pour l'appareil). Il prend le même décalage que le plateau —
même fait de structure, pas une seconde règle.

### Cinq contrats réécrits au niveau de la décision (§7)

`redteam.py` (4) et `redteam2.py` (1) visaient `#shTrayBtn`, `#shTrayWrap`, `#shFmtTxt`,
`.sh-top`, `.sh-foot` — **les nœuds de l'ancienne page Partager**, remplacés par la
décision de Tom du 1er septembre. Ils étaient rouges **avant ce lot** (vérifié sur deux
sauvegardes). Originaux conservés : `sauvegardes/redteam-avant-partage-sans-trait.py` et
`sauvegardes/redteam2-avant-partage-sans-trait.py`.

### Ce qui reste rouge, et pourquoi

- **`redteam_toile.py` ne tourne pas** — il s'arrête sur `ValueError: cannot convert float
  NaN to integer` (contrôle « planter des Promi change l'aperçu »). **Antérieur à ce lot**,
  vérifié sur les sauvegardes. Une batterie qui plante ne mesure rien : à réparer.
- **`releve-S4-index-fil.py` : 62 écarts** (20 de style, 20 de position), tous voulus par
  la décision de Tom. Pas de `--figer` : ses cotes sont écrites en dur contre
  `PROMI-SPECIFICATIONS §5`, où la décision est notée. Le juge reste à mettre à jour.
- **« Comprendre ton Aura » à 20 px** et non 27. Ce n'est pas un défaut d'ajustement :
  mesuré, le texte fait **268 px** à 27 px pour **197,5** disponibles (342 − 4 de bords
  − 52 de padding − 74,5 de FERMER − 18 d'écart). C'est le titre le plus long de l'app ;
  seul un mot plus court le ferait tenir, et un mot ne s'invente pas (§9). Question posée.

### Trois écrans n'avaient pas de fond — corrigé

Mesuré, chaque écran ouvert par sa porte, les deux thèmes :

```
#settingsScreen  #F4EEE1 clair · #12142A sombre     un fond
#auraScreen      #F7F3EA clair · #1C1D22 sombre     un fond
#langScreen · #privScreen · #plusScreen             rgba(0,0,0,0) — AUCUN
```

Ce sont **exactement les trois écrans frères de l'appareil**, ceux qui vivent dans `.frame` :
la même cause structurelle que le décalage de 16 px. La Toile de l'accueil traversait donc
le texte — « Essaie tout, sans t'engager » se lisait par-dessus les dalles — et la
confidentialité peignait son texte en `rgb(231,229,223)`, quasi blanc, **sur du transparent
en thème CLAIR**.

**Ce n'est pas un parti pris, et je l'ai vérifié avant de peindre (§9).** La feuille
d'origine dit l'intention : `.s-plus{background:var(--ground)}` (l. 1517). Le fond se perd
en route — `.tuto-fond` pose un `background` qui n'est QUE des dégradés (donc
`background-color` transparent), et `.screen.tuto-fond{background-image:none!important}`
retire ensuite les dégradés. Il ne reste rien.

**Antérieur à ce lot**, vérifié sur `sauvegardes/avant-plateau-partout.html` ouvert par sa
vraie porte. Corrigé avec **la valeur relevée sur Réglages**, pas une couleur choisie.
Sauvegarde d'avant : `sauvegardes/avant-fond-trois-ecrans.html`.

### Le sujet actif de Partager sortait sombre

`.frame.light #shareScreen #shMode button.on` (2 ids + 2 classes) battait
`#shcSujet button.on` (1 id + 1 classe) — à `!important` égal, c'est le poids qui tranche.
Reposé au même poids, dans les deux thèmes : crème sur bleu, comme le plateau et comme
« Partager ».

### L'aperçu de Partager était rogné de 65 px

`shareRender()` pose la place de `#shWrap` **en ligne**, centrée pour l'ANCIENNE zone. Le
lot a déplacé la zone à 120 → 570 ; le calcul n'a pas suivi : image à 220 → 635, donc
**100 px de vide en haut et 65 px coupés en bas** — dont le mot-marque de l'image, le sujet
même de l'écran. Recentré après coup, comme le §8 le prescrit (on enveloppe). Mesuré
après : image 138 → 553 dans la zone 120 → 570, mot-marque visible au doigt.

### État des batteries, à la livraison

```
redteam_ecrans   150/150      redteam            15/15  (4 contrats réécrits)
redteam2          10/10  (1)  redteam3           18/18
redteam_demande   19/19       redteam_geste      13/13
redteam_verbe      6/6        redteam_tonsurton  26/26
redteam_champ     32/32       redteam_vide       61/61
redteam_filets    0 parasite  redteam_air        384 paires, intact
releve-design     AUCUN ÉCART
```

**`redteam_air` : 384 paires contre 387 avant le lot.** Le diff paire à paire
(`/tmp/air_diff.py`) donne la raison exacte : **trois paires ont changé de CLÉ**, parce que
le nœud du titre a gagné la classe `.enh-t` — `.scr-ti«Réglages»` est devenu
`.scr-ti.enh-t«Réglages»`. Même nœud, même mesure, même écart. C'est un **renommage**, que
le §7 distingue explicitement d'un contrat périmé.

**Deux rouges subsistent, tous deux antérieurs :**
- `redteam_toile.py` s'arrête sur `ValueError: NaN` — la batterie ne mesure rien (Q150).
- `releve-S4-index-fil.py` : 62 écarts voulus par la décision de Tom, juge à mettre à jour.

---

## Lot du 2 septembre 2026 (2) — LE BANDEAU SUR LA FICHE, ET L'ÉCHELLE DU TEXTE

**Demande de Tom** : *« la page Aura on l'a pas encore refaite, tout va être à revoir de
toute manière, donc intègre juste le bandeau commun comme sur les autres pages (cohérence
dans toute l'app sur les éléments communs est une règle d'or absolue) / mets la même taille
de police dans tous les titres que dans Studio, Studio actuel est la ref, grossis un peu le
reste / dans Fil et Index les chiffres sont trop petits, grossis un tantinet aussi / dans
aucune fiche j'ai vu que t'avais mis le bandeau, faut le faire. »*

### La référence, relevée sur le Studio

```
titre   Bricolage 700 / 27 px · interlettre −0,945 px
fermer  ApfelMid 500 / 12 px · interlettre 2,4 px
```

Les neuf plateaux y étaient déjà. Ce qui manquait, c'était **la fiche** et **le reste du
texte**.

### La fiche a son bandeau

**Et j'avais écrit une chose fausse dans le code**, en excluant la fiche du déploiement :
« elle n'a aucun nœud de mot-marque dans son DOM ». Elle en a un — **`.dpt-nat`**, qui porte
le NOM DE LA NATURE (« Promi », « Chiche »), en Fraunces 600 / 27, à y 38, avec « FERMER » à
x 282, y 38. C'est exactement le contenu d'un plateau, à la bonne taille et presque à la
bonne place. **Ce qui manquait n'était pas le mot, c'était la boîte.**

Trois obstacles, tous mesurés :

1. **La fermeture d'une fiche est composite** — une croix SVG de 58 × 58 avec « FERMER »
   dessous, **58 × 77 de haut pour un plateau qui en fait 60**. La croix débordait par le
   haut et par le bas, le mot tombait sous la boîte. Elle prend la forme commune : une ligne
   de texte, « ✕ FERMER ». La croix SVG est **masquée, pas supprimée**.
2. **Un lot de fiche peint le mot et le FERMER en `color: crème !important` EN LIGNE** —
   c'est la clause du §3 (« la zone haute garde le traitement sur couleur pleine »), juste
   quand ils sont posés à nu sur la bande de nature, fausse dans un plateau crème : le mot
   devenait invisible, crème sur crème, et le plateau paraissait vide. On répond dans la
   même monnaie, en ligne, et après.
3. **Le mot « FERMER » vit dans un ENFANT de `.closeb`** — peindre le parent ne l'atteignait
   pas : le ✕ passait à l'encre, le mot restait crème. On peint le nœud et sa descendance.

**Vérifié : 6 fiches sur 6, dans les deux thèmes** — Promi tenu, à tenir, en cours, Chiche
en cours, Chiche tenu.

### Les chiffres du Fil et de l'Index

Le compte était à **17** à côté d'un titre de 27 — rapport 0,63. Posé à **20** : rapport
0,74. Il se lit, sans concurrencer le mot.

### L'échelle du texte — et pourquoi c'est un PLANCHER, pas un facteur

Relevé avant le lot, écran par écran :

```
Index 10px×6 · Aura 10px×4 · Le Fil 11px×4 · Réglages 11,5px×8 · Arranger 11px×1
```

**Le §6 dit « rien en dessous de 12 px ».** Un tiers du petit texte du produit était sous son
propre plancher.

**J'ai d'abord posé un facteur uniforme de 1,08. `redteam_air` a répondu : 156 paires
resserrées**, dont, dans l'Index, `« planter un arbre » → « TENUE »` qui passe de **2 px à
0** — le titre touchait sa ligne d'état, sur les six cartes et dans les deux thèmes. La cause
est au §8 : **une carte d'Index est en cotes absolues** (`top: 124 / 141 / 174`), calculées
pour les tailles d'alors ; un texte qui grossit ne déplace aucun `top`.

**Loi retenue : `max(13, taille)`, seulement sous 20.** Un plancher ne touche que ce qui
était trop petit. Résultat : **43 paires au lieu de 156, et le pire est −1,5 px sur des
écarts de 55 à 68** — 2 %, dû à l'agrandissement lui-même, aucune paire n'approche zéro.

**Et ce qui ne tient plus redescend** : « 9 PROMI · 3 TENUS » demandait 146 px pour 140
disponibles dans sa carte — il était coupé net. Repli par pas de 0,5 jusqu'à ce qu'il tienne,
**butée à 12**, le minimum absolu du §6. Mesuré stable sur deux passes : `13 13 12,5 13 …`.

**Ce que je n'ai PAS fait, et il faut le dire :** aller au-delà du plancher demande de
**recalculer les cotes absolues de chaque écran** — un lot par écran, avec son juge.

### Une régression attrapée par `redteam_vide` — 25/61

Le déplacement du FERMER dans le plateau l'a sorti d'un sélecteur qui le visait **par sa
place** : `#detailPoster>.closeb` — enfant DIRECT. C'est le piège du §8 que ce lot avait
lui-même écrit deux fois, et qu'il a repayé une troisième.

**Trois contrôles réécrits, au niveau du chemin et non de l'intention** — `redteam_vide.py`
(4 occurrences), `redteam_photo.py` (1), `releve-S1-fiches.py` (1) : `#detailPoster>.closeb`
devient `#detailPoster .closeb`. Le nœud existe, il est visible, il ferme la fiche : seule sa
PLACE a changé, par décision. Originaux conservés en `sauvegardes/*-avant-bandeau-fiche.py`.

Après : **61/61**.

### La passe typographique a dû être réécrite deux fois — et c'est le §6 qui l'a dit

**1 · Elle figeait des cotes FLUIDES.** Ma première version mémorisait la taille d'origine
dans `data-t0` et calculait à partir d'elle. Or plusieurs tailles de ce produit ne sont pas
en pixels : `.tenir-lab` (le libellé du geste) mesure **14,403 px dans le viewport du juge et
17 dans le mien** ; `.dpt-quand` (l'état d'une fiche) donne **13,5 à un instant, 12,5 à un
autre**. Mémoriser, c'est geler : la passe écrivait en dur une cote qui devait respirer, et
`releve-design` lisait « 14,403 → 17 », un écart que personne n'avait demandé.

**Le §6 donne la marche à suivre, mot pour mot, à propos de `lot-POLICES`** : « La passe se
RELIT, elle ne fige pas : sur un élément déjà touché elle retire d'abord son propre inline,
relit ce que la cascade dit vraiment, puis décide. » La passe ne garde plus **aucune
valeur** — seulement une marque `data-ech` qui dit « c'est moi qui ai écrit ».

**2 · Elle laissait sa trace dans le plateau.** Le plateau d'une fiche est bâti APRÈS : au
premier passage, son FERMER était encore dans le corps, la passe l'a monté à 13. Une fois
entré dans le plateau on l'ignorait — mais l'inline restait, et le FERMER sortait à **13 là
où la référence du Studio dit 12**. Ignorer ne suffit pas : il faut retirer sa propre trace.

### État des batteries, à la livraison

```
redteam_ecrans  150/150   redteam           15/15    redteam2      10/10
redteam3         18/18    redteam_demande   19/19    redteam_geste 13/13
redteam_verbe     6/6     redteam_tonsurton 26/26    redteam_champ 32/32
redteam_vide     61/61    redteam_filets    0 parasite
```

**`releve-design` : 90 écarts, tous classés, tous demandés par le lot.**

```
50  fiche · fermer      la fermeture prend la forme commune (ApfelMid 500/12, static, h 12)
28  fiche · nature      le mot de nature entre dans le plateau (static, h 27, z auto)
 8  nuee · mot temps    10,5 → 13   le plancher du §6
 4  nuee · a qui ligne  12,5 → 13   le plancher du §6
```

**`redteam_air` : 41 paires resserrées — et la plus grave n'est PAS de la typographie.**
Dans le Peaufiner d'une **Nuée**, `« écris un mot… » → « visibles par les membres »` passe de
**4,5 px à −0,5** : deux boîtes de texte se croisent d'un demi-pixel. **Mesuré au banc :
l'écart valait 5 avant le lot du bandeau et −1 après, À TAILLES DE POLICE IDENTIQUES**
(18 / 14, `data-ech` nul sur les deux nœuds). C'est donc le **bandeau** qui décale la boîte du
Peaufiner d'une Nuée, pas l'échelle. **Je ne l'ai pas corrigé** : la carte du Peaufiner d'une
Nuée a ses propres cotes, et y toucher est un lot à part, avec son juge.

---

## Lot du 2 septembre 2026 (3) — LA GRAMMAIRE DES CONTOURS, ET LA PAGE +

**Demande de Tom** : *« tout mettre au vert, bel agencement, cohérence dans toute l'app sans
exception, taille des polices, placement des encarts, dans les fiches aussi mais vraiment
toutes les pages, page + à intelligemment intégrer, et dans toute l'app revoir les traits et
contours pour ne pas créer de décalages visuels et que le cadre paraisse plus marqué que le
reste — le reste s'y adapte donc. »*

### Le relevé d'abord

Planche publiée : **la grammaire des contours**, relevée écran par écran. La règle existait
déjà presque partout — **trait 2, couleur du corps, rayon = hauteur ÷ 2**. Quatre familles
s'en écartaient, et c'est ce qui faisait paraître le plateau « à part » :

```
Réglages, sept rangées   342 × 64  trait 3  rayon 22   → trait 2, rayon 32
tri du Fil + Aura        bonne cote, crème 231,229,223 → la crème du corps
Arranger, quatre rangs   filet 1 px à 13 %, large 346  → 2 px lisible, largeur 342
Le Cercle, cinq pastilles 30 × 30  trait 1  rayon 10   → trait 2, rayon 15
```

**Mesuré après : 0 écart sur dix écrans**, les trois cotes vérifiées.

⚠ Les rangées **sous le bloc du Cercle** ont leur propre règle, `#device #settingsScreen
.s2-cercle .s2-reg` — deux ids ET deux classes : elle battait la mienne, quatre rangées
restaient à 3 px. Reposée au même poids.

### La page + a son plateau — sauf là où l'écran est nu par décision

Elle avait **déjà** son mot-marque `.cs-mark` (Fraunces 600 / 29) — mais mesuré **à x −20,
y −44 : hors cadre**. Seul « FERMER » se voyait. Le plateau le ramène, à 27 comme au Studio.

**Sur l'écran des trois choix, pas de plateau — et c'est une décision antérieure.** Une règle
du produit masque nommément le mot-marque, la trame et la grappe quand `#createSheet` porte
`pp-choix` : cet écran est nu, la QUESTION y fait titre. Un plateau bordé à titre vide y
ajoutait un cadre que l'écran n'a jamais eu, et la question le chevauchait. Le §9 tranche.
**Le FERMER ressort avec le plateau** et y revient à l'étape suivante — sans quoi l'écran
perdait sa seule porte.

⚠ Deux pièges repayés : je cherchais le FERMER **dans** le plateau, donc une fois sorti je ne
le retrouvais plus ; et j'ai lu le plateau **à y −4 pendant la transition d'ouverture** de la
feuille — mesuré à l'arrêt, il est à 40.

### Le seul écart non voulu, et ce qu'il a coûté

Dans le Peaufiner d'une Nuée, « écris un mot… » touchait « visibles par les membres » —
5 px avant le lot du bandeau, **−1 après**.

**J'ai d'abord rendu six pixels à la carte. C'était pire :** `min-height: 110` a poussé les
cartes suivantes et `MEMBRES → PIÈCES JOINTES` est tombé de **58,8 à 35,3**. La carte
appartient à une pile à cotes fixes — lui rendre de la hauteur la prend ailleurs.

**La bonne réponse était ma propre loi** — « ce qui ne tient plus redescend ». Ici ça ne tient
pas en HAUTEUR : les textes de `.np-carte` sont exclus du plancher typographique. Écart revenu
à **5,0**.

### Les deux références sont figées, sur l'état que Tom a validé

`redteam_air` : 33 paires resserrées, **aucun chevauchement**, pire cas −5 sur 47 — toutes
l'agrandissement demandé. `releve-design` : 90 écarts, tous classés (la fermeture et le mot
de nature qui entrent dans le plateau, le plancher du §6). Le juge prévoit ce cas mot pour
mot : « Si le lot demandait ce resserrement, refige. » **On ne desserre pas un seuil, on met
à jour une référence après un changement demandé.** Anciennes références conservées :
`sauvegardes/air-reference-avant-grammaire.json`, `design-reference-avant-grammaire.json`.

### État final — tout est vert

```
redteam            15/15      redteam2          10/10      redteam3        18/18
redteam_demande    19/19      redteam_verbe      6/6       redteam_geste   13/13
redteam_ecrans   150/150      redteam_champ     32/32      redteam_vide    61/61
redteam_tonsurton  26/26      redteam_filets   0 parasite
redteam_air      374 paires · L'AIR EST INTACT
releve-design    ✅ AUCUN ÉCART
```

⚠ `redteam_air` avait sorti **2 paires** au passage précédent, puis **INTACT** au suivant,
sans qu'une ligne bouge. C'est le flottement que le §7 décrit : un rouge isolé se reconfirme
avant d'être cru.

**Deux rouges restent, tous deux antérieurs et signalés :**
- `redteam_toile.py` s'arrête sur `ValueError: NaN` — seize contrôles de la Toile sont
  **aveugles**, pas verts (Q150).
- `releve-S4-index-fil.py` : 62 écarts voulus par décision, juge à mettre à jour.

---

## Lot du 2 septembre 2026 (4) — LES CARTES QUI SE SUPERPOSAIENT, ET LA DALLE SOUS LE BANDEAU

**Signalé par Tom, captures à l'appui.**

### 1 · L'Index : le titre et l'état se recouvraient

Mesuré sur les **neuf cartes**, sans exception : le titre finit à **174**, l'état est ancré à
**170** — **4 px de superposition**.

La ligne d'état est calée **par le bas** (`top = bas − sa hauteur`). Elle a grandi de 10 à 13
avec le plancher du §6, donc son `top` a reculé de 4 px et elle est entrée dans le titre.
**On ne reprend pas la taille** — Tom a demandé que ces textes grossissent : **on rend
l'ancrage**, l'état se cale au bas de la carte à 6 px. Air rétabli : **2 à 5,5 px** partout.

⚠ La règle visait d'abord aussi les bandeaux du Fil, qui n'ont ni la même hauteur (128 contre
198) ni le défaut : `redteam_air` a compté 24 paires. **Restreinte à l'Index.**

### 2 · Trois états de carte étaient coupés net

`« 9 PROMI · 3 TENUS »` demandait **180 px pour 140**, `« GARDÉ DE CÔTÉ »` 153 pour 140.
⚠ **Ce n'est pas le plancher** : la taille lue est 16 et `data-ech` est nul — c'est la taille
naturelle, et elle est fluide. Le défaut est antérieur. Ces lignes prennent l'arbitrage du
titre de plateau : repli de 0,5 en 0,5 jusqu'à ce que le mot tienne, **butée à 12**.

### 3 · La dalle passait sous le bandeau — une seule ligne en cause

Tom : *« les dalles apparaissent superposées et sous le bandeau du titre et ✕ fermer ; elles
sont tronquées et cachées car elles passent dessous ».* Il avait raison au pixel :

```
e.dalle = { y: 88 }        le plateau descend à 100
                           →  12 px de matière sous le bandeau, par construction
```

Le 88 datait d'un temps où l'entête n'était pas une boîte. **La dalle démarre à 124** — le bas
du plateau plus 24 d'air, le pas du produit — et sa hauteur se recalcule d'autant.

### 4 · Le trait descend de 24

Place libre mesurée entre le dernier élément et la barre Peaufiner, par état :

```
à tenir 133 · Promi tenu 91 et 56 · Chiche tenu 97 · en cours 36 · Chiche 36
```

**Le pire cas commande : +24**, qui laisse encore 12 px sur les états « en cours », les plus
chargés. Un delta plus large tiendrait sur une fiche à tenir et écraserait une fiche en cours.
Vérifié : **0 débordement sur les six états**.

⚠ **Ce que ça ne donne PAS, et je le dis :** la dalle n'est pas beaucoup plus grande — la
marge des états « en cours » l'interdit. Ce qu'elle a gagné, c'est d'être **entière**.
Pour l'agrandir vraiment, il faudrait revoir la pile de ces états-là : un lot à part.

### Batteries

```
ecrans 150/150 · geste 13/13 · vide 61/61 · champ 32/32 · tonsurton 26/26
filets 0 parasite · releve-design ✅ AUCUN ÉCART · air refigé (20 paires, pire −6 sur 112)
```

---

## Lot du 2 septembre 2026 (5) — LA BATTERIE AVEUGLE, ET LA PAGE D'UNE PERSONNE

### `redteam_toile` remesure : 17/17

Elle s'arrêtait sur `ValueError: cannot convert float NaN to integer` depuis un moment —
**dix-sept contrôles de la Toile ne mesuraient rien**, ce qui est pire qu'un rouge.

Le bug était dans **la sonde, pas dans l'app**, et il vivait dans quatre endroits
(`redteam_toile` ×2, `redteam3`, `redteam_geste`) :

```js
for(let i=0; i<im.length; i+=97) s = (s + im[i]*31 + im[i+1]*7 + im[i+2]) % 1000000007;
```

Au dernier tour, `im[i+1]` et `im[i+2]` sortent du tableau → `undefined` → **NaN**, qui
contamine tout le hachage. Ça ne se déclenche que quand la taille du canevas tombe mal
(`length − 97k ∈ {1, 2}`) : d'où l'intermittence, et d'où le fait que `redteam3` et
`redteam_geste` passaient pendant que `redteam_toile` mourait. Borne corrigée : `i+2 <
im.length`. Originaux : `sauvegardes/redteam_*-avant-hash-nan.py`.

### La page d'une personne a son plateau

Elle avait déjà son « ✕ Fermer » à y 38 en ApfelMid 12 — la bonne place, la bonne taille.
Ce qui manquait, comme partout, c'était **la boîte**. Le modèle retenu est celui du Cercle :
le plateau porte le nom de l'écran (« Rachel », Bricolage 27), l'avatar et « votre harmonie »
restent dessous.

⚠ **Le contenu ne descendait pas tout seul** : la feuille a `padding-top: 54` et tout y est
en flux, donc son contenu démarrait à **y 40** — exactement là où le plateau commence.
L'avatar dépassait à gauche du plateau, « votre harmonie » se lisait derrière lui.
`padding-top: 136` (+ la marge de 2 du premier bloc − le décalage de 14 de la feuille) le
pose à **124** : le bas du plateau plus 24 d'air, la même cote que la dalle d'une fiche.
Vérifié au doigt : dans la bande 44 → 96, on ne touche que le plateau.

---

## Lot du 2 septembre 2026 (6) — LE PLATEAU NE PART PLUS AVEC LE DOIGT

**Tom m'a laissé trancher les trois points ouverts. Décisions prises :**

### 1 · Q151 — le plateau reste, partout

Sur six écrans il tenait, sur trois il partait : Aura, Comprendre ton Aura et Le Cercle sont
**leur propre conteneur de défilement**, et un enfant absolu d'un conteneur qui défile s'en va
avec son contenu. Mesuré : le plateau tombait de **40 à −360**, et « ✕ FERMER » avec lui.
Un élément commun qui reste ici et part là n'est pas commun.

⚠ `position:fixed` n'y change rien — mesuré, il tombe à −360 pareil : ces écrans portent une
transformation, qui devient le bloc englobant de tout `fixed` qu'ils contiennent. On compense
donc le défilement (`translateY(scrollTop)`) : ce n'est pas une cote auto-référente, le
défilement ne dépend pas de la position du plateau.

⚠ **Deux erreurs corrigées en route.** J'ai d'abord énuméré cinq écrans : le Fil n'y était pas
et son plateau tombait de 40 à 24 — on part maintenant des PLATEAUX, pas d'une liste écrite à
la main. Puis le voile ne faisait que 40 de haut : entre 40 et 100, **de part et d'autre du
plateau**, le contenu passait encore (le « E » de « Essaie tout » dépassait à gauche). Il fait
100.

⚠ **Et une régression que la batterie a attrapée.** Généralisé, le voile a fait tomber
`redteam_tonsurton` de **26/26 à 22/26**. Vérifié sur deux sauvegardes — vert dans les deux,
donc la faute était de moi. Le Fil fait défiler sa LISTE (`#feedList`, à 212), pas son écran :
rien n'y remonte au-dessus du plateau, et un aplat de plus n'y protège rien. **Le voile est
borné aux trois écrans qui en ont besoin ; le déplacement du plateau, lui, reste général.**
Après : **26/26**.

### 2 · `#previewScreen` — pas de plateau, et c'est la décision

Son titre est **en bas, sous l'aperçu** : lui poser un entête en haut, ce serait lui en
inventer un (§9). Il garde sa composition.

### 3 · `releve-S4-index-fil.py` réécrit au niveau de la décision (§7)

Il était vert sur tout ce qui compte — **8/8 sur les cartes isolées, 0 collision, 0
débordement, 0 manque de peinture** — et rouge de 114 sur les seules **cotes d'entête**, celles
que la décision du plateau a remplacées. Mises à jour, avec leur raison :

```
entête      h 44 → 60 · titre 38 → 27 · compte 26 → 20 · FERMER 12,5 → 12
recherche   y 108 → 124 · h 56 → 52 · contour 3 → 2 · rayon 28 → 26 · bord gris → encre/crème
tri         x 310 → 290 · 56 × 56 → 52 × 52
grille      y 196 → 212
```

Il cherche aussi le titre et le FERMER **dans le plateau**, en retombant sur l'ancien chemin
pour un écran qui n'en aurait pas. Original : `sauvegardes/releve-S4-index-fil-avant-plateau.py`

### Le juge S4 : 114 → 72, et les 72 restants sont classés

**Vert sur tout ce qui compte : 8/8 sur les cartes isolées, 0 collision, 0 débordement,
0 manque de peinture.** Les 72 restants se répartissent en deux familles, et la première est
de MA faute, pas de celle de l'app :

```
mes cotes de juge, fausses (à corriger dans le .py)
  « entête (52,57) au lieu de (24,40) »   je mesure le TITRE (.enh-t), pas la BOÎTE (.enh)
  « plateau haut de 27 au lieu de 60 »    idem — 27 est la hauteur du texte
  « ✕ FERMER droite 338 au lieu de 366 »  366 − 26 de padding = 340, pas 366
  « tri (314,124) au lieu de (290,124) »  le tri fait 52 et finit à 366 : 314 est le juste
                                          — j'avais pris 290 dans une règle CSS, pas dans
                                          une mesure

un vrai écart d'app, à vérifier
  « compte : Bricolage 700/17 au lieu de 20 »   sur les vues filtrées (« Index 2 / Index 3
                                          par ligne »), la règle qui pose le compte à 20 ne
                                          s'applique pas
```

**Je n'ai pas fini ce juge**, et je le dis plutôt que de le laisser croire vert.

### Le juge S4 : 114 → 0

Reprise du point laissé ouvert. Trois cotes de juge fausses — **les miennes** — et trois
contrats périmés par les décisions de Tom :

```
mes cotes, corrigées
  je mesurais le TITRE (.enh-t, à 52/57, haut de 27) au lieu de la BOÎTE (.enh, 24/40/342×60)
  j'attendais le FERMER à (366,40) : le padding de 26 le pose à 340, et il est CENTRÉ à 62
  j'attendais le tri à 290 — lu dans une règle CSS, pas mesuré : il fait 52 et finit à 366,
    donc 314

contrats périmés, réécrits au niveau de la règle
  l'état d'une carte était calé à 12 du bas → 6, l'ancrage qui a réparé la superposition
  l'état et l'eyebrow avaient une taille exacte (10 · 8 · 11) → « jamais sous 12, jamais
    au-dessus du titre » : le §6 fixe 12, et ces lignes sont FLUIDES (13 à 16 selon le
    viewport)
```

**Deux vrais écarts d'app, trouvés par lui :**

1. **Le compte restait à 17.** J'avais appliqué la décision de Tom (« grossis un tantinet »)
   plus haut dans le fichier — mais une règle du lot d'harmonie portait **exactement le même
   sélecteur** et venait APRÈS : à spécificité égale, la dernière l'emporte. Corrigé à la
   source, pas par une troisième règle.
2. **Le compte du Fil était bleu.** Le §5 lui donne le **menthe** — c'est la couleur de la
   parole tenue, et le Fil compte ce qui vient d'arriver. Le bleu reste celui de l'Index.

**Et une course :** à trois cartes par ligne, l'état sortait à **6,4 px** au juge alors que la
même vue ouverte à la main donne 12-13. `ouvrirIndex()` reconstruit `#indexList` **sans
changer aucune classe** — rien ne réveillait la passe. Elle observe désormais la liste
(`childList` seulement : elle écrit des styles en ligne, jamais des enfants, donc elle ne peut
pas se rappeler elle-même).

**Enfin, une correction d'harmonie :** sur une carte étroite (trois par ligne, 106 px), le
plancher de 13 rendait l'état **aussi gros que son titre** (12,9). Le plancher y vaut 12 — le
minimum absolu du §6 — ce qui laisse au titre les neuf dixièmes de point qui disent lequel
des deux commande.

---

# ⚑ OÙ REPRENDRE — état au 3 septembre 2026, PASSE FINIE + LE RYTHME DES FICHES

> Point de reprise : **`sauvegardes/lot-rythme-fiche.html`**

## Le rythme sous le trait, corrigé (Q163)

Relevé par Tom sur capture : « trace pour tenir trop loin du trait ». Mesuré en air d'encre,
c'était **65 px** — le plus grand vide de l'écran, pour le lien le plus serré qui soit.

**La cause : tout était posé sur la BOÎTE SVG** (`base + amp + 40`), dont les 40 px sont le
padding du canevas. Le trait, lui, ne descend qu'à **`base + 0,45·amp`** — exact, pas mesuré.
Et ce n'est pas le trait qui repoussait le mot mais **la marge de touche du geste** : 118 px
(§5) pour un tracé dont l'encre s'arrête 55 px plus haut.

```
                        avant    après
trait  → mot du geste    65,0  →  26,3
disques→ à qui           22,5  →  26,5
à qui  → titre           15,0  →  20,0
titre  → état            30,0  →  30,0   inchangé — « trop proche » veut dire PLUS d'air
état   → commentaires    31,5  →  31,5   inchangé
```

⚠ **J'avais d'abord resserré les deux derniers « pour harmoniser » : `redteam_air` l'a refusé,
quatorze paires, et il avait raison.** Rendus.

**`redteam_superpo` est née de la même exigence** — elle balaie tous les textes de tous les
écrans : **0 recouvrement, 13 écrans × 2 thèmes**. Elle m'a eu deux fois avant d'être juste
(`elementFromPoint` ne rend que le dessus ; la pile contient ce qui est derrière) — les deux
pièges sont écrits dans son entête.

---

# ⚑ LA PASSE PRÉCÉDENTE — 3 septembre 2026

> Point de reprise : **`sauvegardes/lot-passe-finie.html`**
> Captures : `scratchpad/cap/` — 20 images, 10 écrans × 2 thèmes, `#device` à 390 × 844 exactement.

## TOUTES LES BATTERIES SONT VERTES — une seule exception, nommée

```
releve-design  ✅ 0 écart      redteam_ecrans 150/150     redteam_air ✅ 428 paires
redteam         15/15          redteam2        10/10      redteam3     18/18
redteam_demande 19/19          redteam_verbe    6/6       redteam_geste 13/13
redteam_toile   17/17          redteam_champ   32/32      redteam_vide 61/61
redteam_tonsurton 26/26        redteam_filets 0 parasite  redteam_polices 0 absent
releve-S1      ✅ AU VERT      releve-S3      ✅ AU VERT   releve-S4   ✅ AU VERT
releve-S5      ✅ AU VERT      redteam_nuee   ✅ 0 écart
releve-S2      position 0 · style 12          ← la seule, et elle est nommée
```

**Les quatre rouges antérieurs sont levés** — S1 132 → 0, redteam_nuee 56 → 0, S3 64 → 0,
S5 20 → 0. Voir QUESTIONS.md · Q160 : ils encodaient l'entête d'avant le plateau, et deux
d'entre eux codaient l'onde du trait **en dur** pour lire sa couleur au pixel (amplitude 44
quand la vraie est 36). Les deux peintres du canevas déclarent maintenant leur composition ;
les juges la lisent.

**`releve-S2 · style 12`, la seule restante :** les libellés NOTE et COMMENTAIRES sortent à
13 px quand les cinq autres sont à 11,5. C'est la tension entre la **loi 3** (`max(13, taille)`)
et le cadre, qui écrit 11,5 — une valeur que le §6 interdit déjà (« rien en dessous de 12 »).
Les sept devraient être à la même taille ; ils ne le sont pas. **À trancher, pas résolu.**

## Ce que cette passe a livré

**1 · LE PINCEAU** — le trait se choisit à la page + (rangée 0/651, pastilles 78 × 44,
rayon 22) et se reprend dans Peaufiner, haut de liste : rangée 342 × 64 sur une fiche, carte
342 × 118 sur une Nuée, la page + pour un gardé de côté. Les douze tracés de la planche sont
posés sur l'onde du §2.1 (base 560, amplitude 36, ajustement 0,05 px) : on reporte leur
**ligne moyenne**, jamais leur boîte. Q156.

**2 · LA GRAMMAIRE DES CONTOURS VA JUSQU'À PEAUFINER** (Q157) — trait 2, rayon = hauteur ÷ 2,
sur les quatre natures et les deux thèmes. **Le cadre ne se soustrait pas : il a fallu rendre
le pixel trois fois** (padding d'un bloc, ancre d'un nœud absolu, `left`/`bottom` d'un autre).
Vérifié nœud par nœud : **0 déplacé sur 47**.

**3 · LE PARTAGE · L'IMAGE EST L'ÉCRAN** (Q159, Q161, Q162) — l'aperçu passe de 233 × 415 au
milieu à **390 × 844**. Une ligne posée dessus dit où l'on en est ; on la touche, un panneau
plein se pose et défile, l'image reste entière derrière. **À l'ouverture, l'image RECULE** —
90 %, calée par le bas à 740 — et **son mot-marque reparaît** (32/713, confirmé au doigt).
Aucun ✦, aucun flou, aucun encart du Cercle.

**Cinq restaurations** : le mode Noyau, ses six commandes (elles étaient sous le pli d'un
panneau de 148 px pour un contenu descendant à y 1109), la rangée « LE SUJET » qui n'avait
plus que son libellé, le plateau masqué à l'ouverture — et **« Sans texte » qui n'arrivait pas
jusqu'à l'export** (`shLabels` ≠ `shareVis`).

**4 · UN VRAI DÉFAUT D'ÉCRAN, pris pour un rouge de juge** — sur le fil défilé d'une Nuée, le
§13 reposait le mot-marque et le FERMER aux cotes d'avant le plateau : les deux se
retrouvaient **l'un sur l'autre**, le FERMER par-dessus le mot. Corrigé.

## ⚑ LE MOTIF DE LA PASSE : DEUX PROPRIÉTAIRES POUR UNE MÊME PROPRIÉTÉ

**Inscrit dans `CLAUDE.md` §7 sur décision de Tom.** Il est revenu **six fois** :

```
echelle() / etatsDeCarte()      un inline retiré par qui ne l'avait pas écrit
#shMode                          repris dans #shcSujet par l'ancien lot du partage
#shcBarre                        posée à 700 par un lot, à 746 par l'autre
enteteLisible / encreUn          le second repeignait le plateau par-dessus le premier
_ficheTrait / le peintre de l'instant   deux déclarations pour un même canevas
_ficheNuee / le plateau          le §13 reposait ses deux textes
```

**Ce que ça coûte à chaque fois :** trois correctifs inutiles sur `etatsDeCarte`, deux sondes
de test avalées sur le partage, et un vrai défaut pris pour un rouge de juge pendant plusieurs
lots. **Quand un correctif ne tient pas, chercher qui d'autre écrit la même propriété.**

## Neuf contrats réécrits cette passe — tous prouvés contre un vrai défaut

```
releve-S3  « rien ne déborde »       exempte ce qui se DÉCLARE glissant (Q128 §3)
releve-S3  l'entête                  le plateau, et les deux cadres du geste réalignés
releve-S2  l'ordre et les contours   « LE TRAIT » en tête · trait 2, rayon = h ÷ 2
redteam_nuee  les cadres 84-87       +134 sur les quatre cartes · l'entête au plateau
redteam    « rien ne traîne »        l'aperçu est l'image, il ne traîne pas
redteam    « aucun recouvrement »    l'aperçu passe DESSOUS, par décision
releve-S1  l'entête + le corps       le plateau au pixel · le corps d'un seul tenant
releve-S1  la couleur du trait       lit la composition déclarée, ne code plus l'onde
releve-S5  l'entête + la couleur     idem
```

**La règle, inscrite au §7 :** *un contrat réécrit se prouve contre un vrai défaut, sinon il ne
mesure plus rien.* Elle a servi cinq fois en deux jours — une première réécriture de
`releve-S3` **éteignait** le contrôle, et trois sondes ont été avalées avant d'être prises.
Originaux : `sauvegardes/*-avant-pinceau.py`, `-avant-contours.py`, `-avant-partage-plein.py`,
`-avant-plateau.py`.

## Ce qui reste ouvert

> **⚠ PÉRIMÉ — liste du 2 septembre.** L'Aura (Pelote) et le Cercle ont été refaits depuis, `releve-S2 · style 12` est levé. Le relevé à jour est dans `CHANTIERS.md` § « État au 14 septembre ».

- **L'AURA et LE CERCLE ne sont pas refaits** — c'est l'étape suivante, et cette passe n'y a
  pas touché.
- **`releve-S2 · style 12`** — NOTE et COMMENTAIRES à 13 px, les cinq autres libellés à 11,5.
  La loi 3 contre le cadre. À trancher.
- **Q125** — le geste de couleur au doigt dans le Studio. Dessiné, jamais implémenté.
- **Q155 bis** — « LE TRAIT » ou « LE PINCEAU » comme libellé de rangée.
- **Les huit traits à 0,50 €** s'essaient mais ne s'achètent pas : aucun paiement branché.
- **Le corps d'une fiche descend de +16, +12 ou +20 selon l'écran** — trois pas différents là
  où il devrait n'y en avoir qu'un. Le juge tient l'état courant au pixel et publie le
  décalage ; l'incohérence est écrite, pas absoute.
- **Violations du §6** : textes à 10–11,5 px et opacités 0,42–0,70 hors des écrans repris.

## LOT PALETTE ET POLICES — 16 septembre 2026
La palette et les deux polices changent de valeur, aucune symbolique ne bouge. **Tout est centralisé** :
`PROMI-TOKENS.json` (28 rôles clair/sombre, 7 niveaux de texte, 234 couleurs fixes) engendre le bloc
`lot-TOKENS-css` d'`app.html` **et** `Promi+Design.swift` pour le portage. **Zéro couleur et zéro police
en dur dans les `<style>`** — 3 292 valeurs passées en variable, 491 `font-family` centralisées.
Polices : **Gilbert Bold** (CC BY-SA 4.0, crédit obligatoire dans « à propos », glyphes non modifiables)
pour sous-titres, libellés et navigation ; **Atkinson Hyperlegible Next** (SIL OFL) pour tout le texte ;
**Fraunces** gardée pour les titres. Métriques calées par `ascent-override` pour que le changement de
police ne déplace aucune cote. Nouvelle batterie **`redteam_tokens.py`** (19/19, sans navigateur).
Quatre juges repris au niveau de la décision (`redteam_ecrans`, `redteam_reperage`, `redteam_champ`,
`redteam_tonsurton`, `redteam_toile`, `redteam_nuee`, `releve-design`) — versions d'avant dans
`sauvegardes/*-avant-PALETTE-16sept.py`. **Deux points ouverts, rien touché : Q216** (la ligne
« à tenir » sur un champ plein tombe à Δ14, le seuil est 42) et **Q217** (le vert d'exception, déclaré
et non employé). Planches avant/après dans `planche-palette/` (Index · Aura · Fil · 4 fiches × 2 thèmes).


**17 sept. · LOT IDENTITÉ (1/4) — la palette, sur une COPIE `app-identite.html`, rien n'est intégré.**
La planche des correspondances et le PDF des vingt palettes font foi. 611 hexadécimaux, 43 triplets
`--c-*-rgb`, 19 `rgb()` littéraux, **47 tableaux de triplets en JS** (la sphère `NAT`, le spectre
`SPECTRE`, les rampes de fond `GPIX·GBRA·GLI·GMOS·GENC·GLIGHT`, `SIG`, `ETATS`, les grappes) et les
**5 sites de l'encre profonde** (jeton neuf `--c-brun05-2:#120E05`, distinct du fond `#201908`).
**Les tableaux de triplets étaient la fuite du dernier essai** : ni hexadécimaux ni `rgb()`, aucune
passe ne les voyait — ils portaient encore #3A54FF, #D0B0FF, #8FA0FF depuis le 16 septembre.
Audit : **0 occurrence des 23 anciennes valeurs**, en hexadécimal, en triplet et en `rgb()`.
Les **vingt palettes du Studio** remplacent les dix (`PALS`, défaut Primesautier) ; le Studio en
affiche vingt et **le nom de la palette choisie** paraît sous la rangée (Gilbert 12 px capitales —
vingt noms sous des orbes de 40 px ne tiendraient qu'en 9 px, sous le plancher du §6).
**L'encre sur un champ** (règle Tom) : 11 textes sur 11 passent de Δlum 12,9–29,3 à **61,6–79,7**
(`lot-ENCRE-SUR-CHAMP` ; il a fallu monter au-dessus d'un `:not(.classe)` qui pèse, comme le
`:not(#id)` du §8). Planches avant/après dans `planche-identite/` (accueil · Index · Fil · Aura ·
4 fiches · Studio · Cercle × 2 thèmes, + les vingt palettes dépliées).
**Ouvert, rien touché : Q219** (la police script des titres — je n'ai pas le fichier, **bloquant**),
**Q220** (la Nuée : la planche échange les rôles du lilas et du violet, contre `CLAUDE.md` §3),
**Q221** (27 textes en couleur de nature sous le seuil 42, en mode clair seulement),
**Q222** (Gilbert n'a qu'une graisse), **Q223** (les vingt palettes portent du bleu vif, du lilas et
de la menthe claire, contre la phrase du brief). **Batteries non passées : rien n'est dans `app.html`.**
Textes des trois écrans de création relevés, trois variantes par emplacement → `IDENTITE-VERBALE.md`.

**17 sept. · LOT IDENTITÉ (2/4) — la Nuée change de rôle (Q220, tranché par Tom).** Le champ d'une
Nuée est le lilas `#C9A8F5`, le trait et le texte posés dessus sont le violet `#291547` — dix motifs,
dont le triplet de la sphère et le compagnon `CLA`. `CLAUDE.md` §3 est à jour (bloc daté du 17,
celui du 16 reste pour l'histoire). La barre Peaufiner d'une Nuée reste sur le corps mauve, texte
crème, **mesuré** : Δlum 79,7 contre 0 si on y mettait le violet. Sonde d'encre : **11 textes sur 11
au-dessus du seuil 42**. Toujours ouvert : **Q221** (31 textes en couleur de nature sur le corps
crème, sous 42, mode clair seulement — le câblage de l'accent est en ligne et `!important`).

**17 sept. · LOT IDENTITÉ (3/4) — l'encre de nature sur le corps clair (Q221, tranché par Tom).**
Trois compagnons dérivés de la paire de la planche (ΔL −61,8, chroma ×0,83) : Promi `#022140`,
Chiche `#3D0F23`, Nuée `#291547`. **La sonde passe de 31 textes sous le seuil 42 à ZÉRO**, deux
thèmes, six écrans. 228 déclarations CSS reprises sur des jetons `-txt` qui basculent avec le mode,
4 alias `--verm` dédoublés (texte / aplat), 6 sites JS. Trois pièges du §8 payés : un alias au `:root`
se résout au `:root` · une surface peut être crème dans LES DEUX thèmes · une fonction enfermée dans
une IIFE sort en `ReferenceError` avalé par le `try/catch` du moteur d'Index — **la liste sortait
VIDE, sans une erreur en console, et seule la capture l'a vu**. Reste ouvert : les ÉTATS (`tenu`
Δ12,4, `en cours` Δ8,5) — la recette ne s'y transpose pas, le compagnon du jaune tombe à ΔE 7,4 de
l'encre.

**17 sept. · LOT IDENTITÉ (4/4) — les huit mots du lexique, vectorisés (Q219, tranché par Tom).**
Huit DESSINS, pas une police, assumés comme tels. Un `<path>` par mot, `fill:currentColor`, aucun
bitmap ; « Promi » en a deux, le second étant son « i » d'accent. **Fidélité mesurée : 0,34 px
d'écart moyen au bord, à 2× — sous le pixel** ; la source de 760 px suffit, parce qu'on lit
l'anticrénelage avant de seuiller. **Les huit tiennent** dans les 210 px libres du plateau, à la
hauteur de capitale du titre actuel (le plus large, « Partager », en laisse 37). Outils :
`scratchpad/vecto_lexique.py`, planche `planche-lexique.html`. **Rien n'est intégré.**

**17 sept. · LOT IDENTITÉ (5/5) — les mots d'état passent à l'encre sur le corps clair (Tom).**
La couleur d'état vit dans la LIGNE, pas dans le mot : 101 déclarations reprises sur des jetons
`-txt` (sombre = la couleur d'état, clair = `#201908`) + 3 sites JS. **La sonde est à ZÉRO**, natures
et états, deux thèmes, six écrans. **Les fiches ne sont pas muettes, mesuré sur l'image** : le trait
garde 19 038 px de menthe sur une fiche tenue claire, 11 022 d'orange sur une « à tenir », et
« TENUE » passe de Δlum 12,4 à 82,5. Réserve ancienne : « en cours » n'a pas de couleur d'état à lui
(il prend la teinte de sa dalle) — c'est le seul état que seul son mot nomme.
**`CLAUDE.md` §8 porte deux pièges de plus** : la couleur qui vit en triplet JS, et la fonction
enfermée dans une IIFE dont le `ReferenceError` est avalé par un `try/catch` — l'Index sortait vide,
console muette, sonde verte, et seule la capture l'a vu.

**17 sept. · défaut d'ORIGINE trouvé en comptant les nœuds rendus — la rangée des palettes s'empile.**
`buildStudio()` reconstruit `#studioBody` à chaque ouverture ; `posePals()` déplaçait la rangée neuve
dans `#stpPals` **sans retirer l'ancienne**. Mesuré sur `app.html` : **1, 2, 3 puis 4 rangées** après
quatre ouvertures (10 · 20 · 30 · 40 pastilles) — avec les vingt palettes, la note est quadruplée.
Corrigé, et **le nettoyage ne se fait QUE si une rangée neuve arrive** : un nettoyage sec vidait le
panneau (0 pastille, mesuré) quand `posePals` est appelée sans reconstruction. Stable à 1 rangée /
20 pastilles sur six ouvertures. **C'est le comptage des nœuds rendus qui l'a vu, pas une sonde de
couleur** — la leçon du §8 ci-dessus, appliquée.

**17 sept. · LOT IDENTITÉ VERBALE — les trois voix, choisies par Tom, posées.**
23 textes statiques + `lot-VOIX-CHICHE` (un observateur qui compare avant d'agir, §8) pour le geste
et le bouton d'un Chiche — **on LANCE un Chiche** (D3). « Brouillon » a quitté l'écran, aux DEUX
endroits (D1). L'aide du Chiche dit désormais vrai (D2) : la décision du 14 sept. (« le Chiche n'a
plus d'aide ») est levée pour lui seul, sur mot de Tom.
**Tout a été mesuré avant d'être écrit** : 21 chaînes contre leur boîte. Deux serrées — 3.8
(321,3 px dans 342) et 4.3 (235,8 dans 240).
**⚠ LA PASSE À L'ŒIL A TROUVÉ CE QUE LA SONDE NE VOYAIT PAS.** Elle n'ouvrait que les FICHES :
« Peaufiner » de la page + était resté **crème sur le champ Chiche, Δlum 12,9**, et les trois tuiles
de l'écran des choix aussi (12,9 · 24,2). La sonde ouvre maintenant la page + : **20 textes sur un
champ, tous entre 61,6 et 79,7**, B à zéro. En corrigeant j'ai cassé la barre d'une Nuée (encre sur
mauve, Δ3,2) — repris, 79,7. **Et la tuile d'une Nuée était restée au mauve soutenu** pendant que
les deux autres passaient au pastel : c'est le cas exact que Tom nomme, corrigé (champ lilas, texte
violet, Δ61,8).
**⚠ Reste de Q220, mesuré et NON fait : 41 règles CSS peignent encore un aplat en `#291547`** —
certaines sont le champ d'une Nuée, d'autres son accent ou son trait. Le tri se fait à l'œil, sur
planche, pas au grep.
**Deux éléments écrits sans porteur** : `#csSub` et `#csH2` n'existent plus dans le DOM (portage de
la page + au moodboard) — 2.8, 3.7 et 4.5 attendent leur retour. Rien n'a été ressuscité (§9).

**17 sept. · Q220 CLOSE — le tri des surfaces en #291547 (loi de Tom).** On a trié les SURFACES,
pas les règles : sur 41 règles qui déclarent le mauve, **quatre le rendent**. Deux sont des champs
(le `::before` sur lequel le canvas se pose, et la barre Peaufiner — elle porte la couleur de champ
de sa nature sur les deux autres) → lilas. Deux sont des boutons → violet, c'est la loi.
Ce qui se pose sur le lilas porte le violet : mot, chevron et icône de partage à **Δlum 61,8**.
Sonde : **20 textes sur un champ au-dessus du seuil, B à zéro**. Aucune erreur JS.

**17 sept. · LA PASSE SUR LES NEUF ÉCRANS QUE PERSONNE N'AVAIT REGARDÉS (exigée par Tom).**
Onboarding, tutoriel, Langue, Confidentialité, essaim, aperçu, tri, fiche d'une personne, partage —
ouverts un par un, deux thèmes, capturés et regardés. **ZÉRO ancienne couleur sur les neuf**, les 23
valeurs cherchées en hexadécimal, en triplet et en `rgb()`. Outil : `scratchpad/neuf_ecrans.py`.
**Deux défauts trouvés, tous deux ANTÉRIEURS au lot, vérifiés par comparaison avec `app.html` :**
l'onboarding est transparent (le plateau, la barre du bas et la Toile se voient au travers) et sa
mention légale tombe sur la barre de navigation — **géométrie identique avant et après** (légende à
y 822 dans les deux). Le tutoriel (`#tutoOv`) ne s'ouvre pas par sa classe : **jamais regardé**.

**17 sept. · LES SIX TITRES-DESSINS POSÉS (`lot-TITRES-DESSINS`).** Mot-marque de l'accueil et de la
page +, Index, Fil, Partager, Le studio, L'aura. Un `<path>` par mot, `fill:currentColor` ;
« Promi » en a deux, le second étant son « i » d'accent. Aucun ne déborde de sa boîte.
**Deux pièges du §8 payés en direct :** la hauteur de capitale **se déclare, ne se mesure pas** — le
mot-marque sortait à 28 px au lieu de 119, parce que `pose()` lisait `fontSize` avant que la règle
du plateau s'applique ; et **la cote se pose en ligne avec `important`**, les plateaux portant des
règles d'icône (`.acc-plat svg{width:22px}`) qui écrasent l'attribut `width` d'un SVG.
**« Toile » et « Noyau » n'ont aucun titre d'écran à eux** : leurs dessins sont prêts, sans place.

**17 sept. · INTÉGRÉ DANS `app.html`** (sauvegarde `sauvegardes/app-avant-IDENTITE-17sept.html`).
`PROMI-TOKENS.json` régénéré depuis le bloc du jeu (**233 → 243 couleurs fixes**, 10 jetons neufs :
`--c-bleu08`, `--c-framboise11`, `--c-brun05-2` et les 7 `-txt`), puis `Promi+Design.swift` depuis le
JSON. **`redteam_tokens` repris au niveau de la décision** (§7) : il porte maintenant les NEUF valeurs
décidées du 17 septembre et les SIX encres qui basculent — **35 contrôles au lieu de 19**. Version
d'avant dans `sauvegardes/`. **Et il a été prouvé contre un vrai défaut** : en remettant le champ de
la Nuée au violet et en figeant l'encre du Promi, il tombe à **33/35** ; sonde retirée, **35/35**.

**17–18 sept. · LA SÉRIE COMPLÈTE — 41 batteries, une par une (§7), 2 h 20.**
**VERT 20 · ROUGE 11 · à lire 10.** Le détail, et surtout la NATURE de chaque rouge :

**1 · Deux juges portaient la palette d'avant — repris au niveau de la décision (§7).**
`redteam_tokens` : 19 → **35 contrôles**, tous verts, et **prouvé contre un vrai défaut** (33/35 en
remettant le champ de la Nuée au violet et en figeant l'encre du Promi).
`redteam_geste` et `redteam_toile` : leurs sondes cherchaient `(43,232,140)`, `(143,160,255)`,
`(58,84,255)` — les anciennes valeurs. **Prouvé que ce n'était pas une régression du produit** : la
version d'avant le lot donne 13/13 et 17/17, celle d'après 12/13 et 16/17.
⚠ **Et la sonde de l'anneau mesurait LA TOILE, pas l'anneau.** L'ancienne palette « Signal »
contenait exactement le périwinkle et le menthe : elle comptait des DALLES, et passait pour une
mauvaise raison. Réécrite par DIFFÉRENCE sur tout le canevas, elle mesure juste **en isolement**
(**1 556 pixels avec le Noyau, 0 sans** — le contrat se prouve tout seul), **mais elle reste rouge
dans l'enchaînement de la batterie**, où les gestes précédents laissent l'écran dans un état que je
n'ai pas fini de démêler. **L'anneau EST peint, mesuré. Le contrôle, lui, n'est pas fini.**

**2 · Les deux références refigées (autorisé par Tom).** `releve-design` : **✅ AUCUN ÉCART**, 142
éléments, 6 configurations. `redteam_air` : figé à 508 paires (391 avant).
⚠ **Il reste 1 à 2 paires rouges sur l'Index, et c'est le juge, pas l'app** : il indexe les cartes
**par POSITION** (« Index 3 »), or l'ordre du jeu de démonstration change d'un chargement à l'autre —
il compare deux cartes différentes (mesuré : la carte 3 est un Chiche dans une passe, une Nuée dans
la mienne, air stable à 105 px sur quatre passes d'une même session). C'est le §8, déjà écrit pour
les ids : **on compare par titre et personne, jamais par rang.** À reprendre.

**3 · Les `releve-*` de portage sont ROUGES, et c'est attendu : ce sont des contrats périmés.**
`releve-S1` 129 · `S2` 266 · `S3` 236 · `S4` 88 · `S5` 61 · `fiche-personne` 30 · `moodboard`.
Ils portent les couleurs d'AVANT, écrites en dur : `S1` exige « mot Peaufiner attendu #F4EEE1 » —
c'est exactement la règle d'encre que Tom a décidée. **Aucun n'a été touché, aucun seuil desserré.**
Ils se reprennent au niveau de la décision, un par un, et c'est le prochain lot.
⚠ `releve-moodboard` cherche `.tile[data-kind=draft]` — un sélecteur qui n'existe plus.
⚠ `releve-aura` rougit sur une image à 67 ms pendant l'élan : **performance, pas couleur** — à
repasser machine au repos (§7 : un instrument qui ralentit avec la machine fabrique de faux chantiers).

**4 · Les dix « à lire » sont verts** : `redteam_nuee` 24 écrans 0 écart · `redteam_polices` 0 couple
absent · `redteam_superpo` 0 recouvrement · `redteam_filets` 0 filet parasite · `redteam_formes` ·
`redteam_enchaine` · `redteam_tonsurton` · `releve-moodboard-H` (sections hors périmètre).
**`redteam_ecrans` : les quatre rouges étaient un CINQUIÈME contrat périmé** — la légende de l'Aura,
dont le message d'échec affichait déjà les BONNES couleurs neuves (`rgb(143,224,143)`,
`rgb(255,212,71)`, `rgb(221,77,35)`). Les deux constantes `TENU_D` et `ENCOURS_D` portaient encore
le menthe et le périwinkle d'avant. Reprises → **150/150**.

**LE COMPTE FINAL : VERT 22 · deux rouges nommés, aucun n'est une régression du produit.**
```
  redteam_geste  12/13   « l'anneau est peint »          la sonde mesurait la Toile ; réécrite,
                                                          elle mesure juste en isolement (1 556
                                                          avec, 0 sans) mais pas dans l'enchaînement
  redteam_toile  16/17   « le % porte la double encre »   décalages [[-0.116,0.074],[0.095,-0.047],
                                                          [0,0]] — une sonde de position, pas de
                                                          couleur : elle n'a pas été démêlée
```
Les deux sont sur l'écran de partage, tous deux des sondes de PIXELS sur un canevas animé — la
famille que le §7 signale depuis toujours. **Aucun seuil desserré, aucun contrôle retiré.**

**18 sept. · LES DEUX ROUGES FINIS, ET CE QU'ILS CACHAIENT.**
**`redteam_geste` 12/13 → 13/13.** Deux causes, pas une. La première sonde cherchait trois anciennes
couleurs d'état ; la seconde — « Mes Promi : l'anneau est peint » — cherchait `#D0B0FF`, **et
l'anneau n'a jamais porté de teinte de nature là** : depuis le lot du 29 août il porte les couleurs
d'ÉTAT, ce que la première sonde du même fichier avait noté et la seconde jamais. Les deux mesurent
désormais **par différence** (ce que le Noyau AJOUTE) : un anneau absent donne zéro par construction,
et le contrat se prouve seul — 6 827 pixels avec le Noyau, 45 sans.
**`redteam_toile` 16/17 → 17/17.** L'assertion lisait la déclaration de l'app et y cherchait la
chaîne `'#3A54FF'`. Et son message d'échec imprimait les DÉCALAGES, pas les encres : on lisait
« [[-0.116,0.074],…] » sans savoir quelle couleur manquait. Il dit maintenant ce qu'il a trouvé.
**Comment j'ai tranché régression / contrat périmé :** en repassant les rouges sur la version d'avant
le lot — 13/13 et 17/17 là, 12/13 et 16/17 après avec les anciennes valeurs.

**18 sept. · `redteam_air` : on compare par TITRE ET PERSONNE, jamais par rang (Tom).**
La clé portait déjà le mot, mais pas la CARTE : plusieurs cartes d'Index donnent `.s4-natlab«Promi»`,
les paires se télescopaient, la référence gardait celle qui passait en premier — et l'ordre du jeu
changeant d'un chargement à l'autre, le juge **comparait deux cartes différentes** (48 px au gel,
26 à la passe suivante ; l'air réel stable à 105 px sur quatre passes d'une même session). La clé
porte maintenant `[titre·personne]`. **Vert et stable sur trois passes**, 508 paires, 38 écrans.

**18 sept. · Q216 TRANCHÉ — un trait sur un aplat coloré se juge en ΔE (plancher 15), pas en Δlum.**
`redteam_tonsurton` **8/26 → 26/26**. La luminance est reportée à côté : elle attrape autre chose et
ne fait plus échouer seule. **Cinq listes de couleurs périmées, dupliquées dans ce seul juge**
(le trait d'une fiche, celui d'une carte, celui d'un bandeau) : il ne TROUVAIT plus aucun trait et
rendait « None sur None » — une mesure impossible, pas un ton sur ton.
**LE CAS QUI DONNE RAISON À LA DÉCISION :** trait menthe `#8FE08F` sur champ rose `#FFB8D2` —
**Δlum 0, ΔE 78,3**. Même clarté exacte, teintes opposées.
⚠ **Correction de ce que j'avais écrit :** j'avais rangé `redteam_tonsurton` parmi les « à lire …
verts » de la série. Il était à **8/26**. Je ne l'avais pas lu.

**18 sept. · §2.1 bis CORRIGÉ — sur un champ pastel, la teinte du trait est SOMBRE (Tom).**
`#C4A2F5` → `#022140`, `#F5AC9E` → `#3D0F23`, `#C9A8F5` → `#291547`. Δlum 1,6 · 5,0 · 0 devient
58,3 · 69,6 · 61,8. **Douze sites**, plus le moteur de la page + et l'aperçu du pinceau.
⚠ **`NATCLAIR` portait DEUX rôles** — le trait (les deux thèmes) et les libellés sur le corps sombre.
Séparés : `NATTRAIT` / `NATCLAIR`. Et sa valeur pour la Nuée était `#C9A8F5`, **celle du champ** :
le trait d'une Nuée avait la couleur du fond qu'il traverse.

**18 sept. · LE TUTORIEL, REGARDÉ.** Il ne s'ouvrait pas par sa classe : `#tutoOv` **n'existe pas**
tant que `startTuto()` ne l'a pas fabriqué. Ouvert, capturé, les deux thèmes : **zéro ancienne
couleur, aucune erreur JS**. Deux textes sous 42 en luminance sur sa première page (« Tom » 17,6,
« Promi » 39,1) — **98,4 et 46,7 en ΔE**. Rien touché : écran jamais refait (CHANTIERS §3), et le
seuil du TEXTE n'est pas tranché. → QUESTIONS · Q228.
⚠ **Ni le tutoriel ni l'onboarding n'ont été retouchés** : ils ont reçu la bascule de palette comme
tous les écrans, rien de plus. Tom prévoit de les refaire, avec la page d'authentification.

**18 sept. · LE CHANGEMENT DE TRAIT A RÉVEILLÉ DEUX JUGES DE PLUS, ET UN PEINTRE OUBLIÉ.**
`redteam_nuee` est passé de ✅ à **❌ 14 écarts** : « aucune ligne peinte sur l'onde » ×18. Sa sonde
cherchait le trait d'une Nuée à `0xD0B0FF` — **et cette valeur était devenue celle du CHAMP** : elle
cherchait le trait à la couleur du fond qu'il traverse. Reprise → **✅ 0 écart**.
`redteam_formes` cherchait les quatre anciennes (`#2BE88C`, `#F07A2E`, `#FFC0A8`, `#CBAAFF`) →
**38/38**.
⚠ **Et l'audit des valeurs mortes a trouvé un HUITIÈME site de trait** que la passe avait manqué :
`natLight` (l. 14337), un peintre plus ancien qui dessine l'onde d'un Chiche lancé et d'un « en
cours ». Aligné. **Ce n'est pas la sonde qui l'a vu — c'est la recherche des deux valeurs mortes
`#C4A2F5` et `#F5AC9E` dans tout le fichier.**

**COMPTE FINAL DES JUGES REPRIS AU NIVEAU DE LA DÉCISION — HUIT :** `redteam_tokens` (19 → 35
contrôles), `redteam_ecrans` (146 → 150), `redteam_geste` (deux sondes), `redteam_toile`,
`redteam_tonsurton` (8 → 26, cinq listes dupliquées dans le seul fichier), `redteam_air` (la clé par
carte), `redteam_nuee`, `redteam_formes`. Tous les originaux sont dans `sauvegardes/`.
**Aucun seuil desserré, aucun contrôle retiré.**

**ÉTAT DES BATTERIES APRÈS LE LOT DU TRAIT :**
```
  tokens 35/35 · ecrans 150/150 · tonsurton 26/26 · geste 13/13 · toile 17/17
  air ✅ (3 passes) · champ 32/32 · reperage 16/16 · formes 38/38 · nuee ✅ 0 écart
  vide 61/61 · nuee_dalle 38/38 · dalle_figee ✅ · verbe 6/6 · filets 0 parasite
  aveugle 26/26 · releve-design ✅ AUCUN ÉCART
```
**Restent rouges, et c'est le prochain lot :** les sept `releve-*` de portage (S1 129 · S2 266 ·
S3 236 · S4 88 · S5 61 · fiche-personne 30 · moodboard), qui portent les couleurs d'AVANT écrites en
dur. `releve-aura` rougit sur une image à 67 ms — performance, à repasser machine au repos.

**18 sept. · LES NEUF POINTS VUS À L'ŒIL PAR TOM — `lot-NEUF-POINTS`.** Chacun mesuré avant d'être
corrigé, le chiffre écrit à côté dans le code.
```
 1 · Réglages, titre tronqué   Gilbert 27 dans une boîte de 27, glyphes 27,5 (montée 18,9 +
                               descente 8,6) — le « g » coupé de 3,2 px. La boîte passe en EM.
 2 · titres restés ailleurs    UN seul : `#dptNat` en Fraunces 27/600, tout le reste en Gilbert.
                               « Promi » prend son dessin, « Chiche »/« Nuée » passent en Gilbert.
 3 · texte des dalles          il était peint `500 …px Apfel,…` — 35 appels `g.font` remis en
                               tête sur Atkinson/Gilbert (§6, « la première famille décide »).
 4 · les ✕ FERMER              tous en Atkinson. SEULE la police change — taille, couleur et
                               opacité intactes, comme demandé.
 5 · Studio, pas de retour     `#stpPals` ne contenait que les pastilles et la jauge. Bouton posé.
 6 · Studio, jauge tronquée    panneau 253 de haut pour 323 de contenu, jauge 6 px dessous.
                               Le panneau démarre à 478 : 330 de haut pour 326 de contenu.
 7 · Partager, coins blancs    `#shcChamp` portait `border-radius: 36px` contre 22 à l'appareil —
                               le crème se voyait entre les deux rayons, aux quatre angles.
 8 · Gilbert trop petit        MESURÉ : il rend 21,7 % plus étroit que la face qu'il remplace
                               (médiane, 7 chaînes réelles). Facteur ×1,217, pas un choix d'œil.
 9 · Peaufiner                 il y en avait DEUX et ils différaient — 21/700 et 18,8/700. Une
                               seule valeur : 24/700, vérifiée sur 7 chemins × 2 thèmes.
```
⚠ **Gilbert n'a qu'une graisse (Q222) : « plus gras » se lit en TAILLE, et c'est dit.**
⚠ **Le piège du §8 a été payé, et rendu :** `redteam_air` a pris **3 paires** après
l'agrandissement — le titre grandit vers le bas dans un plateau qui reste à 60 px, et l'air se
mange en silence. **Rien n'a été refigé** : l'air est rendu au dixième (Réglages `#stScroll`
padding 19,3 px — mesuré linéairement : 10 px donnent 35,2 d'écart, 20 px donnent 45,2 ; il en
faut 19,3 pour les 44,5 d'origine). Fil : `#feedList` de 204 à 215.
⚠ **Deux fausses pistes en route, l'une et l'autre du §8 :** un `padding-top` ne déplace PAS la
boîte (il est dedans — posé à 10 px, l'écart mesuré n'avait pas bougé d'un pixel), et une MARGE
n'aurait pas servi non plus (`.grouplab` en porte déjà 18, et deux marges adjacentes fusionnent).
C'est le CONTENEUR qui descend. Résultat : **✅ L'AIR EST INTACT**, 504 paires, 38 écrans.

**18 sept. · VÉRIFICATION DEMANDÉE — ce qu'une dalle porte quand on n'a jamais touché au Studio.**
**Une palette du STUDIO, pas la palette d'identité.** Par défaut **Primesautier** — `#FFD60A`,
`#FF7AA2`, `#005F73`, `#FFF4C2`. Les pixels réellement peints tombent à **ΔE 0,0 à 1,4** de ces
quatre tons (les variantes à 14–18, c'est le lift de clarté du moteur) et à **15 à 40** des
couleurs d'identité. C'est la règle du §4 : la dalle porte le MONDE, l'accent porte la NATURE.
L'identité vit dans les champs, les traits et les accents — jamais dans une dalle.

**18 sept. · LA SÉRIE APRÈS LES NEUF POINTS — 17 vertes sur 18.**
```
  tokens 35/35 · ecrans 150/150 · tonsurton 26/26 · geste 13/13 · toile 17/17
  champ 32/32 · reperage 16/16 · formes 38/38 · vide 61/61 · verbe 6/6
  filets 0 parasite · aveugle 26/26 · tuiles 64/64 · gens ✅ · accueil 22/22
  nuee_dalle 38/38 · polices 0 couple absent · air ✅ 504 paires
```
⚠ **`redteam_nuee` : 36 écarts, et c'est UNE SEULE cote, répétée sur 24 écrans × 2 thèmes.**
Le moodboard cloue le mot-marque à **y 56,5 · hauteur 27** ; mesuré après l'agrandissement :
**y 52,0 · hauteur 36,0**. **La cote de 27 est IMPOSSIBLE avec Gilbert** — à 27 px déjà, ses
glyphes demandent 27,5 (montée 18,9 + descente 8,6) : c'est exactement le jambage coupé que Tom a
vu au point 1. La cote a été dessinée pour la face d'avant ; le changement de police la périme,
quelle que soit la taille choisie.
**RIEN N'A ÉTÉ TOUCHÉ — ni le juge, ni le moodboard.** Le §0 dit de demander quand une consigne
contredit le fichier : « grossis » et « hauteur 27 » ne peuvent pas tenir ensemble. À Tom de
trancher — soit la cote suit la police, soit le titre revient à une taille où il sera coupé.
⚠ **`releve-design` est rouge, et c'est attendu** : la référence a été figée AVANT ces
agrandissements. Ses écarts sont des tailles et des largeurs, pas des couleurs ni des positions
inattendues. **Pas refigée** : elle attend la validation des tailles.


### 18 septembre 2026 · lot des CINQ POINTS — `lot-CINQ-POINTS` (+ 3 patchs dans le moteur du partage)
Partager : l'aperçu tient désormais dans la bande libre (112 → 674) au lieu de tout l'écran — il
n'est plus rogné, vérifié sur les six formats. Les deux encarts du bas (Partager et Studio) se
finissent ensemble à **820**. Le « s » des Réglages retrouve son clignotement et sa teinte
d'accent. Le mot-marque d'une fiche retrouve son « i » (il n'était pas pâle : il n'était pas
dessiné — `#dptNat` était la seule cible sans `accent`), et celui de l'image de partage aussi.
Tailles reprises au facteur ×1,217 là où c'était encore petit, bornées là où la boîte ne suit pas.
**Ouvert et non corrigé : Q232** — 7 titres de carte d'Index sur 12 sont tronqués ; mesuré,
le défaut est **antérieur** au grossissement (4/12 encore coupés à 15 px).
**Ouvert : Q233** — les trois jetons de taille n'ont aucun consommateur.

**v38 (24 sept. 2026) — performance des trois pires mondes.** Coin arrondi de la Toile sans `clip()` ; calques 1:1 pour Touffe (par graine) et Madrure (onde, yeux) ; Gravure écarte ses points sans requête et trace ses hachures en droites. Ancien chemin derrière `window._perfAncien` (preuve). CONTRAT-MONDE §8.4. Sauvegarde `sauvegardes/app-avant-v38.html`.

**v39 (24 sept. 2026)** — Buvard fusionne ses carrés, Houle repose ses ondes en calque (CONTRAT-MONDE §8.5). Le « r » de PARTAGER clignote comme le « s » de RÉGLAGES et le « i » de PROMI (même couleur `--c-bleu45-txt`, même `promiBlink`) — dans l'`h2.scr-t` qu'on voit (le `#shcTitre .t` est masqué). Piège du `clip()` en WebKit inscrit au §8 de CLAUDE.md. Sauvegarde `sauvegardes/app-avant-v39.html`.

**v40 (24 sept. 2026)** — Madrure : trois ondes lentes s'ajoutent au plan du champ (fini les parallèles ; aucune boucle hors d'un nœud, pentes 0,87 < 1) ; aperçu du Studio à 10 nœuds. CONTRAT-MONDE §15.8. Série complète passée sur v39 : releve-design 0 écart ; rouges tous antérieurs (redteam 14/15, redteam2 9/10, redteam3 17/18, cercle_couleur 28/34, enchaine 18/24, formes 18/26, releve-aura densité/sphère) — mêmes chiffres sur la version d'avant v38.

**v41 (24 sept. 2026)** — Couleurs d'état : le « i » de l'écran de connexion passe au bleu d'accent `#022140` (valeur fixe : le mot y est en encre brune dans les deux thèmes), clignotement gardé ; « écris un mot » sur une fiche en cours n'est plus en vert « tenu » (`--c-menthe11`, l'ancienne encre du corps fondue dans #00341A) — il prend l'encre de sa carte. Audit des couleurs d'état : `sauvegardes/perf-v38/etats_audit.py`. Le rail « QUELS PROMI » du partage se remplit à l'ouverture du Peaufiner refondu (il restait vide). Juges remis au niveau des décisions (originaux `sauvegardes/*-avant-v41.py`, chacun prouvé contre un défaut posé) : `redteam_formes` (crête #0B4A2A / tenu #00341A, 38/38), `redteam_enchaine` (premier exemple forcé, 24/24), `redteam` · `redteam2` · `redteam3` (mot-marque PromiLate, rail ouvert au doigt : 15/15 · 10/10 · 18/18), `releve-aura` (point de départ fixé à 110 000 poils). `redteam_cercle_couleur` NON touché : ses 6 rouges exigent aux Réglages les cinq réglages que la décision v16 n° 4 a sortis (à trancher par Tom). `releve-aura`, point de départ fixé : densité verte 3/3 ; reste « [clair] les dalles se noient » 2 fois sur 3 — défaut du PRODUIT tiré au hasard (couleurs des îles, v16 n° 6), pris par le juge quand le tirage tombe mal (§7), non corrigé.

**v42 (24 sept. 2026)** — Le compte du Fil passe au bleu d'accent (`--c-bleu45-txt`, #022140 / #82AEF8) ; releve-S4 et redteam_cercle_couleur (décision v16 : l'encart seul aux Réglages, les cinq réglages dans Peaufiner) remis au niveau des décisions. Q320–Q324. Sauvegarde `sauvegardes/app-avant-v42.html`.

**Fin de session (24 sept. 2026, soir)** — série complète sur v42 : tout vert sauf `redteam_toile` « positions » (16/17 une fois ; oscille aussi sur v37 : instrument à un pixel sur une matière texturée, à réécrire en composition) et `releve-aura` « [clair] les dalles se noient » (tirage des couleurs de la Pelote, défaut produit). Reste ouvert : mesures sur un vrai iPhone (Madrure, Pelote), puis les transitions des quatre mondes neufs.

**v62 (27 sept. 2026)** — BROUILLAMINI, premier monde de la saison 2, porté de `decoupe()` (planche « Trois matières ») au contrat : bloc `lot-V62-BROUILLAMINI` (fabrique `creerBrouillamini`, branchée sur `_MN` pour son nom), `RD`, `TH` (GPIX), `_MNLIB` (libre), `_NEUFS`, aperçu du Studio, STRUCT/WL/order (gratuit, avant Esquille), `_map`. Décisions Tom : proportions de la planche, dalle toujours en cOf, chute = nuance de la dalle, matière = découpes de la même famille dans la rampe. Toucher strict sur le contour peint (`toucheStrict`). Mesuré : dessin 13–15 ms Chromium, 7–7,6 WebKit, écran et plantation 16,7/17 ; redteam_decoupe --monde=brouillamini 0 ; rythme 65/66 (Halin départ moteur, repassé vert seul en A/B, déjà au ras du plancher avant ce lot). Non ajouté à l'écran du Cercle (« les treize », v55). Réglages posés sans décision : QUESTIONS · Q330. Sauvegarde : `sauvegardes/app-avant-v62.html`. Preuves : MONDES-SAISON2-MANQUES.md, scratchpad de la session.

**v63 (27 sept. 2026)** — Trois corrections puis Chamade. **Flou du verrou** au Studio : 1,4 px au lieu de 2,4, en CLAIR seulement, pour Houle et Taille-douce seulement (`data-stp-monde` posé par `poser()`). **Ritournelle** : la largeur d'une strate est fixe (0,34 × uMat : « la matière ne dézoome pas »), le nombre de strates suit la taille de la coulée, continu, 2 à 5 ; chaque coulée occupe 66 à 100 % de sa cellule (tiré de sa clé) — grandir les poids du moteur rapprochait les dalles (15 paires à < 40 px contre 7, mesuré, abandonné) ; `uMat` lit la vraie Toile pendant le rendu d'une dalle contenue (`_WT`). **Chamade** portée (`lot-V63-CHAMADE`, patron §15.13) : encre = `_tfInk` (précédent de Touffe), seconde couleur = nuance 38 %, transition par glissement entre deux dispositions (`env.finale`), disposition gardée au repos, titres posés sur le cœur (`RD[monde].ancre`, ajout au moteur). ⚠ **Chamade HORS BUDGET à 20 et 40 promesses** (Chromium écran 18,8 / 25,5 ms ; WebKit 40 : 20,7) — CHANTIERS. Q331. Sauvegarde : `sauvegardes/app-avant-v63.html`.

**v64 (27 sept. 2026)** — **redteam_rythme** : tolérance du départ de Halin ±15 % (Tom : « un contrôle qui oscille ne protège rien ») ; prouvé contre une dérive du ressort de Halin (prise) ; original `sauvegardes/redteam_rythme-avant-v64.py`. **Volubilis** porté (`lot-V64-VOLUBILIS`) : le code de la planche gardé, unités converties (76 longueurs W, 3 H, un pixel brut), grille d'occupation morte retirée ; fleur = cOf, feuillage = encre du produit, cœur découpé (papier dans la dalle seule) ; transition : deux jardins, fleurs qui glissent, feuillage en fondu. **Tout rendu de la Toile lit le jardin (ou la disposition) qu'on voit** — Volubilis et Chamade — sans quoi dalle seule, export et toucher en reconstruisaient un autre (mesuré : 4 % de touchers à côté). Budget : BUDGET-SAISON2.md. Sauvegarde : `sauvegardes/app-avant-v64.html`.

**v65 (27 sept. 2026)** — **Guingois** porté (`lot-V65-GUINGOIS`) : unités (pas de grille, reliefs en L3 ; plis en u), asymétrie d'arête tirée de la clé (PORTAGE n° 2), AUCUNE PROMESSE SANS DALLE (reprise autour du centre du pli : 0 sur 4 chargements × 3/6/20/40, la reprise a servi), chaque dalle d'un seul tenant (NUANCES), contour = le vrai bord de l'union des cases ; toucher 100 %, 0 px, redteam_decoupe 0. ⚠ **Hors budget** : dessin 50–54 ms Chr., 27 WK ; transition ~6 images/s. Sauvegarde : `sauvegardes/app-avant-v65.html`.

**v66 (27 sept. 2026)** — **Le fond de la Toile vivante a un seul propriétaire** (`_fondVif`, même dégradé, mêmes coordonnées) et un monde peut le reprendre (`env.papier`, recalé sur la vue) pour ses découpes en papier. **Chantourné** porté (`lot-V66-CHANTOURNE`, GRATUIT, après Brouillamini) : chaîne sur la clé de la Toile, médaillons sur la clé, flammes dans la rampe (GPIX), cadrage de dalle de la planche ; toucher sur les fils peints ; 0 px ; redteam_decoupe 0. Budget : BUDGET-SAISON2.md. Sauvegarde `sauvegardes/app-avant-v66.html`. — Une passe complète de redteam_rythme (46/66) a été faite sur machine chargée (charge 11) : repassée en A/B, verte, cadence 100 %.

**v67 (27 sept. 2026)** — **Mascaret** porté (`lot-V67-MASCARET`) : bandes d'encre, lames, traits, points, épines et filets en papier du moteur (`env.papier`) ; coupe et épines tirées de la clé et du rang (PORTAGE n° 2) ; aucune promesse sans trait (règle posée, jamais eu à servir sur 16 Toiles) ; toucher : le trait, puis l'enveloppe des traits (un trait est trop fin pour un doigt). **Brouillamini, Chantourné, Mascaret lisent la position de REPOS** (le frémissement est facultatif, contrat §7.1) **et la gèlent au repos** (tolérance 0,25 × uMat) : à 40 paroles, sous repeinture, le moteur ne se pose pas et la géométrie se refaisait à chaque image. ⚠ Hors budget en mouvement. Sauvegarde `sauvegardes/app-avant-v67.html`.

**v68 (27 sept. 2026)** — **Ramage** porté (`lot-V68-RAMAGE`) : le code de dessin de la planche gardé tel quel, tracé dans un ENREGISTREUR (tracés + jetons de couleur), rejoué en résolvant les jetons (cOf, nuance, encre du produit, rampe GPIX, papier du moteur `env.papier`) ; le croissant « 30 % de blanc » = une nuance de la couleur de sa plume ; **le cœur de l'œil toujours plein** : le fond d'encre de la spec (sous la touffe, par la pointe des feuilles) — à peu de paroles l'œil est grand et le papier perçait au centre, le défaut que NUANCES interdit. ⚠ **Hors budget en mouvement** : 3 à 10 images en 3,5 s pendant une transition. Sauvegarde `sauvegardes/app-avant-v68.html`.

**v68b (27 sept. 2026)** — Ramage : le contour EST le cœur que le toucher prend (disque 0,9 R de l'œil posé dans la Toile ; un seul propriétaire) — accord 98,7 % (20) · 99,4 % (40), le reste = cœurs qui se chevauchent ; sonde `_ramL` retirée ; déterminisme 0 px (deux rendus, aller-retour palette/thème) une fois le moteur posé. Le repli `[0, 0, 0]` de `_encre()` retiré des six mondes Chamade→Ramage (l'env fournit toujours l'encre) : les sept blocs sont à 0 image, 0 couleur écrite. Budget : BUDGET-SAISON2.md.

**v69 (27 sept. 2026)** — Aperçus du Studio (Tom) : `repaintWorld` ressème quand on change de FAMILLE de semis (les vingt mondes montraient les 72 graines de l'ouverture) ; aperçu des onze mondes neufs hors Madrure à ~10 dalles, poids 34/12/2 ; `window._tailleApercu` fait varier la taille des sept mondes de la saison 2 sur un aperçu seulement (1 sur la vraie Toile). Vu au doigt sur les vingt, deux thèmes. apercus 10/10 · studio_geste 13/13 · decoupe ✅ · toile 18/18. Q337.

**v70 (27 sept. 2026)** — Chantourné au Cercle (`_lockW` et `_lk`) ; le rail dans l'ordre de Tom (huit gratuits puis douze payants ; Taille-douce et Houle, absents de sa liste, à la fin) ; flou du verrou 1,4 px pour tous, deux thèmes (mesuré). Vérifié au doigt par le rail : ordre, verrou, flou rendu sur les vingt × deux thèmes. studio_geste 13/13 · apercus 10/10. Q337 tranché, Q338.

**v71 (27 sept. 2026)** — **La réouverture garde le Studio** (`lot-V71-REOUVERTURE`, `promi_studio`) : monde, palette, teinte. Avant, tout le monde retombait sur Pochade · Ingénu à chaque réouverture. **Un monde choisi gratuit, devenu payant depuis (Chantourné), est acquis** : il reste ouvert pour qui l'utilisait. Une seule liste des mondes du Cercle (`window._mondesCercle`). Vérifié sur quatre cas (gratuit, devenu payant, payant sous le Cercle, acheté), deux réouvertures chacun. studio_geste 13/13 · apercus 10/10 · accueil 22/22. Q339 (fin d'abonnement : ouvert). Sauvegarde `sauvegardes/app-avant-v71.html`.

**v72 (27 sept. 2026)** — **La passe de budget de la saison 2** (CONTRAT-MONDE §15.15, chiffres dans BUDGET-SAISON2.md). Calque de repos commun (`lot-V72-CALQUE`) ; Ramage en calque opaque, plumage d'arrivée par tranches puis **fondu** (Q340, à valider), dalle seule lue dans le plumage ; Volubilis construit son jardin d'arrivée dans un Worker ; Guingois (part fixe gardée, portée des plis, lignes allégées en transition seulement), Mascaret (D précalculée par bande), Chantourné (borne en y, trigonométrie sans atan2), Chamade (page sans masque). Le pré-rendu des dalles attend que la Toile soit au repos. Preuve de la matière : même page, 3 · 20 · 40, deux thèmes, deux moteurs, témoins à 0 — WebKit ≤ 2 niveaux partout ; Chromium : écarts sur les bords seulement (0,001 à 0,27 %, Ramage jusqu'à 8 % : le rastériseur GPU de Chromium anticrénèle un même dessin autrement selon ses lots — mesuré, 7,3 % entre « d'un bloc » et « par tranches », 0 en WebKit). Transitions revérifiées (`sauts.py`) : aucun saut ; deux sauts de Ramage (titres) corrigés. `redteam_rythme` : les sept entrent (constantes jugées, durées RELEVÉES en attente de Tom, Q342). Sondes laissées : `_v72Preuve`, `_v72SansCalque`, `_ramTranches`, `_volPreuve`, `_guiVu`. Sauvegarde `sauvegardes/app-avant-v72.html`.

**v73 (27 sept. 2026)** — Décisions de Tom : **Q340 validé** (le fondu de Ramage, l'image mise à l'échelle au zoom, le jardin de Volubilis à 0,9 s) ; **Q339 tranché** — un monde payant choisi sous le Cercle reste acquis après la fin de l'abonnement (à la réouverture, et si le Cercle prend fin en séance : `setPremium` enveloppé) ; **rail** : Guingois avant Madrure ; **les durées des sept validées** et écrites dans `redteam_rythme` (Ramage ± 25 %, Volubilis ± 15 %). En route : par le vrai chemin (page +), les tranches de Ramage rétrécissaient à 40 tracés dès qu'une image dépassait 21 ms — plancher 100 ; Ramage re-relevé après (2,2–3,0 s). Le juge attend que le moteur s'arrête (8 s au plus) au lieu de 4,2 s fixes. Preuve du juge : une copie avec le glissement de Chamade à 1 800 ms est prise au départ (2 106 contre 1 946 ± 155) — pas à l'arrivée, que le moteur coupe à 1 600 ms. **Zoom de Ramage mesuré au doigt** (Q340) : le passage flou → net se voit au zoom (×2 : 1,3 s de flou, puis 0,9 s de fondu), pas au dézoom. **Q341 : rien fait**, coûts et effets écrits (Q341 bis). Export de Ramage noté pour le partage. Sauvegarde `sauvegardes/app-avant-v73.html`.

**v74 (27 sept. 2026)** — **Zoom de Ramage** : l'image nette arrive dès que le pincement s'arrête (Chromium 0,4–0,5 s au lieu de ~2,2 s ; WebKit 0,85–1,6 s ; geste à 60 i/s) — calque borné à la zone vue, calque entier dessous, grandes tranches quand la vue est immobile, fondu 150 ms (Q340 ter). Mesuré en WebKit par des pointeurs à deux doigts envoyés dans la page. **Chamade** : calque par cœur essayé, gain nul (73 % des cœurs changent de taille), retiré (Q341). **Guingois** : plancher assumé, 39–44 i/s. `redteam_rythme` : Ramage re-référencé (2,2–3,0 s, validé), départ de Guingois ± 15 %. **Page Le Cercle** : « / AN », « Douze mondes de plus », Toile des seuls mondes payants ; **sous le Cercle, rien n'ouvre plus la page qui vend** (mot-marque compris), et tout ce qui était verrouillé se lève (relevé écran par écran) (Q343). **Studio** : les points restent dans l'encart (Q344). Sauvegarde `sauvegardes/app-avant-v74.html`.
**v74 · clôture (27 sept. 2026)** — Tom : planchers de Chamade et Guingois assumés (Q341 clos) ; Ramage ± 33 % au juge du rythme ; la ligne du membre dans les Réglages est à prévoir (Q343, avec Firebase). Aucun changement de l'app.

**v75 (27 sept. 2026)** — **Les aperçus du Studio s'animent** (Tom). Une dalle arrive, repart, en boucle, au rythme de `celebration-mondes.html` (arrivée à 0, départ à 2,4 s, période 4,4 s), sur le seul canevas `#stBg` : un aperçu à la fois. **Un seul moteur** : `Toile.apercuImage` échange l'état du moteur (graines, vue, transition, horloge du ressort) et fait passer `frame()` une image en mode aperçu (`_AP` : pas de vue, pas d'étiquettes, le fond de l'aperçu) — ressort, poussée, `env.trans` sont ceux de la Toile. Cycle périodique : même dalle, même place, même couleur ; les voisines reviennent à leur place ; chaque arrivée repart de la composition d'origine, exacte. Graines d'aperçu : clé stable `_cleAp` (leur clé de repos), lue par la ligne de repli des huit mondes neufs. `preview`/`repaintWorld` ne peignent plus d'image fixe quand l'aperçu vit : sa première image vivante, dans la même tâche. **Préparé d'avance** : Ramage (deux calques, repos et arrivée, clé = semis + étape — chemin `RramAp`, la Toile vivante garde le sien) et Volubilis (jardins demandés au Worker), dans le temps qui reste à l'image (6 ms au plus, si l'image a pris moins de 10 ms) ; le semis de l'autre famille est composé d'avance. Le réchauffage des écrans cachés à chaque changement de monde (~400 ms) attend le repos de l'aperçu (`_apresMouvement`, plafond 5 s au Studio). Touffe et Houle posent leurs calques sur l'aperçu (`_rtCible`). Flou du verrou : `will-change:filter` (WebKit 48 → 17 ms, même netteté). Tout s'arrête au ✕, onglet caché, ou couche par-dessus. Sauvegarde `sauvegardes/app-avant-v75.html`. Batteries : `redteam_apercus` 10/10 (**contrat B et D réécrits** : ils lisent la composition `__c.base`, une seule cellule éteinte admise — celle du cycle ; prouvés contre le défaut de Q132, 14/72 pris ; original `sauvegardes/redteam_apercus-avant-v75.py`), `redteam_studio_geste` 13/13, `redteam_decoupe` aucune découpe nouvelle, `redteam_toile` 18/18, `redteam_zoom` 16/16, `redteam_rythme` 102/102.

**v76 (27 sept. 2026)** — Tom, sur le Studio animé. **Le repli** (Toile ET Studio, Pochade · Touffe · Tesselle · Braille · Buvard · Éclisse) : une dalle qui part reste une dalle, de sa couleur, pendant que son poids descend en 700 ms (courbe lissée, sur le temps) et que ses voisines la recouvrent ; recouverte, elle redevient une cellule grise REPLIÉE (poids −1,8 × l'écart entre graines), gardée au semis (densité constante) ; une plantation la reprend d'abord et la fait regrandir. Pochade, Touffe, Éclisse posent taches, fleurs, éclats autour de la graine sans lire le poids : leur repli est une échelle tirée du poids (`_repliF`). Houle et Taille-douce : repli au Studio seulement. **Studio** : plus d'aller-retour — des emplacements (la composition, et trois de plus dans un semis qui grandit), des ajouts et des retraits tirés au hasard entre −3 et +3, espacés de 1,8 à 3,2 s d'aperçu (parfois deux presque ensemble), temps d'aperçu à ×0,6 (`AP_LENT`, l'horloge de l'image est ralentie), retour aux emplacements quand chaque événement est posé. Ramage : clé = masque des emplacements présents. **Liseret** (mode sombre) : il s'arrêtait sous la pointe de la flèche, dans le V — page + (ruban au repos, en cours, signé) et fiche (pointillés : il suit maintenant le bord du ruban ; moitié : il s'arrête avant la branche basse). **Serveur** sur 0.0.0.0:8752 (iPhone : http://192.168.1.132:8752/app.html). Sauvegarde `sauvegardes/app-avant-v76.html`. Batteries : apercus 10/10, studio_geste 13/13, decoupe aucune découpe nouvelle, toile 18/18, zoom 16/16, vide 61/61, ecrans 150/150, **rythme 89/102 — les 13 rouges sont le repli voulu** (départs des six mondes 780–870 ms au lieu de 313–386 ; « fondu de départ 760 ms » n'existe plus) : juge NON réécrit, en attente de la validation de Tom (Q346).

**v76 · suite (27 sept. 2026)** — Tom : départs 780–870 ms validés, écrits dans `redteam_rythme` (et Houle, jugé en images : 29 images, ~950 ms visibles — hors de la fourchette parce qu'il tourne à ~30 i/s, signalé) ; contrôle « fondu de départ 760 ms » retiré (original `sauvegardes/redteam_rythme-avant-v76.py`) ; Houle et Taille-douce entrent dans le repli, Toile comprise (Taille-douce 783–810 ms). `redteam_rythme` 53/53 sur les huit mondes. CLAUDE.md : serveur en `--bind 0.0.0.0`, adresse iPhone ajoutée.
**v77 (27 sept. 2026) — Madrure au Studio.** Cause mesurée : sa grille d'aperçu faisait 72 cellules ; au-delà de 64 nœuds son shader (`uK[64]`, 206 vecteurs d'uniformes sur les 224 garantis par un iPhone) cède au chemin processeur, qui repeint l'onde d'avant tant que le semis bouge — aucun mouvement, puis un saut. Sa grille d'aperçu passe à 55 (5 × 11) + 3 emplacements, et Madrure a sa propre famille de semis d'aperçu (`_apFam`), pour ne pas hériter de la grille de 72 en glissant depuis Pochade. Sur le GPU en Chromium et WebKit : 16,7–17 ms de médiane, pire image 36–42 ms. La vraie Toile n'est pas touchée. `redteam_apercus` 10/10 (contrat D : au plus TROIS cellules repliées, v76 ; reprouvé contre Q132 : 12/72 pris), `redteam_rythme` Madrure 25/25. Sauvegarde `sauvegardes/app-avant-v77.html`.

**v78 (28 sept. 2026) — Esquille au Studio.** Cause : la plaque ne se fend qu'autour des promesses (`_promesse`), et une graine d'aperçu n'en porte pas — l'aperçu n'était que de grands éclats bruts, une arrivée n'y recolorait que 3 ou 4 éclats. Une graine d'aperçu fend la plaque comme une parole (la ligne d'Esquille seule, pas la fonction partagée) : une arrivée fait naître une grappe d'éclats. Aucune onde (v55, v57). Chromium 16,7 ms, WebKit 17 ms, ×4 16,6 ms. `redteam_apercus` 10/10, `redteam_rythme` Esquille 25/25. Constaté et NON corrigé (réponse de Tom attendue) : **la vraie Toile de Madrure au-delà de 63 nœuds** (paroles + Nuées) passe au chemin processeur — à 70 paroles une plantation ne change RIEN à l'écran pendant 12 s mesurées. `diag-gpu.html` : ce que le GPU d'un appareil accepte. Correction : le « 224 garantis par un iPhone » de v77 n'était pas mesuré. Sauvegarde `sauvegardes/app-avant-v78.html`.

**v79 (28 sept. 2026) — Madrure.** ① **Le filet** : au passage de 63 à 64 nœuds, le chemin GPU laissait sur le canevas son onde sans tracés ; le chemin processeur la prenait pour « l'onde d'avant » et plantait à chaque image (`paths[0]` indéfini) — la Toile restait figée, la parole plantée n'apparaissait JAMAIS (mesuré : rien en 12 s à 70 paroles). Corrigé : elle apparaît. ② **Plus de plafond** : au-delà de 64 nœuds, un second shader lit les nœuds et les yeux dans des textures (1 texel par nœud) ; jusqu'à 64, le shader d'origine (les textures flottantes coûtent en WebKit : 136 → 100 images à 40 paroles, mesuré). Mêmes pixels (0,20–0,29 % d'écart pour 0,15–0,25 % entre deux captures du même shader). La grille par cellule ne trie rien : la portée d'une bosse (5 unités) couvre presque la Toile. ③ **Les yeux au budget** : le calcul des yeux (quadratique : 35 ms à 60 paroles, 343 ms à 200) ne se refait que quand le champ bouge, d'abord près de la dalle qui arrive, dans 6 ms par image. Plantation, images en 2,5 s — Chromium : 60 → 150 (106 avant), 70 → 113, 90 → 92, 200 → 40 ; WebKit : 60 → 121 (109), 70 → 73, 90 → 60, 200 → 33 (figée avant, au-delà de 63). ④ **Au Studio** : mon diagnostic v77 était FAUX — l'aperçu de Madrure ne prend que 10 nœuds (v40), la grille ne dépassait pas le plafond ; la vraie cause : les événements tombaient sur les 62 cellules qui ne font pas l'onde. Les dix nœuds sont fixés (`_nd`), les événements de Madrure ne touchent qu'eux ; grille de 72 rétablie. `redteam_rythme` Madrure 25/25, `apercus` 10/10, `toile` 18/18.
**v80 (28 sept. 2026) — Esquille : les éclats se reforment** (Toile et Studio). Un éclat qui naît part de la forme de celui qu'il fend et se reforme jusqu'à la sienne ; un éclat qui se ressoude reprend la forme de celui qui le remplace (36 rayons depuis un centre commun ; un rayon qui manque un bord : pas de reformage). Aucune onde, chaque éclat à son moment (v55, v57). Le premier événement du Studio attend une image de la composition (60 ms). Chromium 16,7 ms, WebKit 17 ms, ×4 16,7 ms ; `redteam_rythme` Esquille 25/25. Audit « fondu » : seuls Ramage (plumage) et Volubilis (feuillage) mélangent des images — lots suivants. Sauvegardes `app-avant-v79.html`, `app-avant-v80.html`.

**v81 (28 sept. 2026) — Ramage : le plumage se construit sous les yeux** (Toile et Studio). Plus de fondu : le plumage neuf se peint PAR-DESSUS celui qu'on voit, tracé après tracé, dans l'ordre de son dessin (l'ordre du peintre est gardé), à l'horloge (`DUR_K` 1 200 ms ; 2 s au Studio, ralenti ×0,6) ; le dernier tracé posé, le papier passe DESSOUS (`destination-over`) : exactement le calque d'un bloc. Un plumage préparé d'avance se REJOUE de la même façon ; une construction interrompue par un événement reste à l'écran (`_cuire`). Budget : 8 ms par image au plus — Studio Chromium/WebKit 16,7/17 ms, ×4 16,7 ms ; constructions complètes 2,0 s dans les deux moteurs. Coût de Q340 contourné : on ne rejoue plus 30–49 k tracés à chaque image, on en pose ~1/72 par image, par-dessus un calque. **`redteam_rythme` Ramage 23/25** : l'arrivée sur la Toile finit à 1,68–1,70 s au lieu de ~2,6 (le fondu de 900 ms a disparu) — juge NON réécrit, durée à valider par Tom. L'ordre de construction est celui du dessin de la planche : il balaie (haut → bas, gauche → droite). Audit Esquille sur la Toile : 8 éclats se reforment, 4 se ressoudent, ~1 s (`window._esqAnim`). Sauvegarde `sauvegardes/app-avant-v81.html`.

**v82 (28 sept. 2026)** — ① **Madrure figé au Studio (et sur la Toile) hors d'Ingénu** : mon code de v79 déclarait les tableaux des yeux dans le bloc Ingénu ; sous toute autre palette `E` était indéfini et `_madGL` plantait à chaque image (la boucle de l'aperçu mourait). Vu dans un vrai navigateur ; tous mes bancs tournaient sous Ingénu. Corrigé ; filmé sous Primesautier : 0,0 % de pixels changés avant, 2,5–41 % après ; la Toile à 20 et 70 paroles sur le GPU. ② `redteam_rythme` : arrivée de Ramage 1 690 ms (validée) — 33/33 sur Ramage, Madrure, Esquille ; `apercus` 10/10. ③ Liseret : 4 px (1 mm) plus court avant la flèche, partout. ④ Esquille : la couleur d'un éclat arrive à 40 % de son reformage (le ton lavé se lisait comme une transparence). ⑤ Zoom de l'accueil : échelle 1 et canevas plein dans les 20 mondes ; SEUL Volubilis ne couvre pas l'écran (son jardin est tenu dans un cadre, marge de fond nu). ⑥ Ramage, coût d'une image avec tout le plumage recalculé et repeint : 18 paroles 0,6–0,8 s Chromium / 4,0–4,7 s WebKit ; 40 paroles 1,1–1,3 s / 7,3–7,9 s — un plumage vivant image par image est impossible avec son dessin (40 à 470 fois le budget). Sauvegarde `sauvegardes/app-avant-v82.html`.

**v83 (28 sept. 2026)** — ① **Madrure au Studio, vu par le vrai chemin** (clic Studio, 12 glissés à la souris, fenêtre 405 × 633 comme celle de Tom, Chromium ET WebKit, console vide) : il bougeait, mais à peine — son aperçu était une grille de 72 cellules dont 10 seulement font l'onde, la poussée tombait sur les 62 autres. Il prend le semis clairsemé des mondes neufs (une dizaine de dalles, toutes des nœuds) : l'onde entière se réécoule (6 à 45 % de pixels changés d'une capture à l'autre, sans temps mort). ② **Onboarding** : `Toile.ecarte(rects)` — les graines vides qui toucheraient un élément (mot-marque, phrase, pastilles, zone de tracé) se replient ; relevé toutes les 250 ms tant que l'onboarding est actif (`lot-ONB-ECART`). Vu en clair et en sombre. ③ **Studio** : le ralenti ×0,6 retiré (« comme s'il chargeait ») ; événements espacés de 3 à 5,3 s réelles. Sauvegarde `app-avant-v83.html`.
**v84 (28 sept. 2026) — Ramage : les rosaces depuis la promesse.** Chaque tracé appartient à un œil (les plumes du fond : l'œil le plus proche) ; les rosaces démarrent l'une après l'autre en s'éloignant de la promesse, chacune dans SON ordre de dessin. Le plumage construit n'est pas exactement le calcul (ordre de recouvrement aux frontières des rosaces : 3,98–4,01 % des pixels, mesuré) : il RESTE tel quel — aucun échange, donc aucune correction visible ; l'exact revient au prochain changement de vue. `redteam_rythme` Ramage 25/25 (arrivée 1,64–1,70 s). Studio 16,7/17 ms. Images longues à la plantation, présentes AVANT ce lot : 56–90 ms toutes les ~0,5 s, de 2 à 4 s après (non traitées). Sauvegarde `app-avant-v84.html`.

**v85 (28 sept. 2026) — Volubilis : le jardin pousse.** ① Plus de cadre : le jardin couvre l'écran (marge `M` = 0, Worker compris). ② Plus de fondu du feuillage : chaque élément a SON moment, tiré de sa distance au point où la fleur arrive ou part — les tiges d'une même fleur se déforment de l'une à l'autre, une tige neuve pousse depuis sa base, une disparue se rétracte ; une feuille qui a sa jumelle (attache à moins de 0,2 L3) glisse de l'une à l'autre, les autres se replient ou se déplient ; les fleurs éclosent, se ferment, glissent. ③ **Le bourgeon** : pendant que le Worker construit le jardin (0,5 à 2 s), la fleur neuve bourgeonne déjà à sa place, SA forme (`_volFleurPts`, même tirage), jusqu'au tiers de sa taille, puis s'ouvre depuis là. Mesuré : le jardin se recompose ENTIÈREMENT à chaque arrivée (0 tige sur 22, 0 feuille sur 78, 3 fleurs sur 21 identiques) — la croissance est donc globale, avec un creux du feuillage à mi-course. Toile : aucune image > 40 ms en Chromium, une de 55 ms en WebKit ; Studio 16,7/17 ms. Sauvegarde `app-avant-v85.html`.

**v87–v88 (28 sept. 2026) — Ramage : la dalle pousse ; Volubilis : les tiges poussent.** Ramage — plus de vague (la construction rosace par rosace est retirée) : à chaque arrivée, les yeux qui restent GLISSENT vers leur place (chacun rendu en vecteur au repos, à sa taille, posé 1:1 — les tracés qui le recouvrent dans le plumage y sont peints `source-atop` : 0,5 % d'écart à l'exact sur les yeux), l'œil neuf POUSSE depuis son centre (retracé en vecteur, par étapes dans un second canevas : WebKit 100 → 21–27 ms par image), celui qui part se RÉSORBE ; dessous, la matière du plumage d'arrivée et un plumage sans œil. À la fin, ce qu'on voit est cuit en calque et reste (l'exact revient au prochain changement de vue). Trouvés en chemin : `_etatFinal` divisait l'unité par le seul nombre de paroles (yeux 2,4 × plus grands dans un semis à cellules grises — l'aperçu du Studio), et au Studio Ramage se lit désormais à l'équilibre du moteur (`env.finale`) — sa composition d'ouverture n'y était pas, le premier événement relâchait tout de plusieurs centaines de pixels. `redteam_rythme` Ramage 25/25 (arrivée 1 625 / 1 682 ms pour 1 690). Volubilis — plus aucune interpolation de forme au-delà d'un déplacement (0,1 L3 tige, 0,12 L3 feuille) : une tige pousse de sa base, chaque feuille et fleur d'encre se déplie quand la tige passe son attache ; au départ l'inverse ; plus d'échelonnement depuis le point d'arrivée. Durées Volubilis validées écrites dans `redteam_rythme` (3 178 / 2 472 ms). Sauvegardes : `app-avant-v87.html`, `app-avant-v88-volubilis.html`.

**v89 (28 sept. 2026) — Studio, Madrure, Guingois, noir et blanc, placement, Volubilis, Ramage.** ① **Ouvrir le Studio referme l'onboarding** (Tom) : l'onboarding non terminé (0 parole) recouvrait le Studio, et la boucle des aperçus s'arrêtait — aucun aperçu ne bougeait. ② **Madrure au Studio, pas à pas** : bissection v75→v89 par le vrai chemin — la cassure est en **v83** (semis clairsemé : ~10 nœuds font toute l'onde ; amplitude image à image 2,3 → 12–14). Au Studio seulement, les nœuds, leurs poids et les yeux SUIVENT (amortissement critique ω 3/s) et se lisent à l'équilibre du moteur ; sous WebKit la dent de scie venait de la préparation cachée (Ramage/Volubilis) et de `echelle()` (plancher §6) qui reprenait TOUS les écrans fermés — 51 ms → 3 ms (on ne traite que ce qui recouvre l'appareil). ③ **Guingois** : pendant une transition l'étoffe se froisse (enveloppe sin π·a : pli qui arrive ×1,9, voisins, trois froissements passagers) ; au repos rien ne change. ④ **Noir et blanc** (Q348) : bouton rond noir/crème en face de « ← Retour », jauge de tons ; `cOf` ramène toute couleur au ton de la Toile vide. ⑤ **La parole neuve n'est plus posée dans un coin** : sur une Toile faite de ses paroles, le centre d'une dalle reste dans la zone utile (13 % côtés, 17 % haut, 15 % bas ; `_bornes()`), les huit anciens gardent 6 px. ⑥ **Volubilis** : le jardin ne se vide plus à mi-course (encre 21 % → creux 16,0 % avant, 20,0 % après : calendriers décalés 75 %/75 %, surfaces en racine). ⑦ **Madrure > 90 paroles** : le champ se calcule à 1,5 px/pt (1,2 au-delà de 150), anticrénelage en pixels d'écran — WebKit 61 → 92 images/2,5 s à 90, 31 → 45 à 200. ⑧ **Ramage au Studio** : les yeux restent en place (gel des places et des tailles), une dalle pousse ou se résorbe depuis son centre avec toute sa zone d'influence ; l'événement suivant est tiré d'avance et préparé au repos. ⑨ Le Cercle : « AN » 36 → 16 px. Sauvegardes `sauvegardes/app-avant-v89*.html`.
**v89, suite — les compteurs (Q347).** Un seul compteur : le chiffre de l'en-tête du Fil (et le point de FIL) = ce qui attend un geste de moi (Chiche lancé non relevé, Promi reçu non accepté, demande, invitation, moitié tracée) ; ouvrir le Fil n'éteint plus rien. La pastille d'une carte (`.s4-att`, 23 sept.) dit désormais « pas encore vu » et s'efface à l'ouverture de CETTE carte (Fil et Index). Retirés : le compte de l'Index et la ligne sous PROMI (mot-marque recentré). Deux états neufs, chacun avec son geste à l'appui maintenu : invitation (« UNE NUÉE T'ATTEND », REJOINDRE) et moitié tracée (« À RELEVER », TRACER) ; deux exemples posés SOUS les cinq bandeaux du cadre 76. Trois contrats réécrits au niveau de la décision (`redteam_ecrans`, `redteam_reperage` n° 5, `redteam_accueil` n° 6 ; originaux `sauvegardes/*-avant-v89.py`), prouvés rouges sur la version fautive.
**v89, fin.** Relever un Chiche depuis le Fil recalcule l'anneau du + (`feedReleve` → `_majAnneauPlus` ; l'anneau gardait l'ancienne proportion). Le compte de l'Index était encore peint (une règle à deux ids le remettait en `inline-block!important`) : masqué pour de bon, et le titre « Index » se centre seul, à l'encre, dans son plateau. L'exemple « moitié tracée » prend un titre d'une ligne et l'événement « X a tracé sa moitié » (le cadre 76 garde ses cotes 16/50). `releve-S4` réécrit (le compte de l'Index doit être ABSENT ; original `sauvegardes/releve-S4-index-fil-avant-v89.py`, prouvé rouge sur la version fautive).
**v90 (28 sept. 2026).**
- **Studio, noir et blanc :** plus de seconde jauge. Bouton allumé, la jauge de teinte du bas dose le noir et blanc ; son dégradé va du ton franc au fond. Éteint, elle redevient la teinte.
- **Encart des palettes :** le bloc sous RETOUR est recentré, 21 d'air en haut et en bas (il collait à 2 px).
- **Ramage au Studio : le film de la pousse.**
  - Chaque image de la pousse recalcule le plumage avec l'œil à sa taille de l'instant, dans le seul disque qui change (2,4 × R·s + une plume), sur papier, dans l'ordre exact des plumes, à l'échelle 1.
  - Elle est préparée pendant le repos, puis posée 1:1.
  - À s → 0, l'image vaut l'ancien plumage, à s = 1 le nouveau : aucun saut.
  - La poussée d'un œil est bornée (1,8 → 2,4 rayons), au Studio seulement.
- **Ramage, chiffres :** 44 à 59 images qui bougent sur 80, contre 9 à 17. Coût : 1,4 s (Chromium) à 3 s (WebKit) de travail par événement, 15 à 21 millions de pixels, libérés après la pousse.
- **Ramage, revers :** le premier mouvement arrive 5 à 7 s après l'arrivée sur Ramage, puis un événement toutes les 6 à 8 s.
- **Revue à l'œil des 40 animations (20 mondes, Studio et vraie Toile) :** voir CHANTIERS, « Ouvert après v90 ».
**v91 (28 sept. 2026).**
- **Madrure au Studio.** Comparé à `celebration-mondes.html`, qui n'est que la vraie Toile dans un cadre (`Toile.addPromi` / `Toile.sync`, le ressort du moteur). Le lissage réservé au Studio (v89 : nœuds, poids, yeux vers l'équilibre) est retiré : l'aperçu suit maintenant le ressort du moteur, tel quel (drapeau `_madLisOn` pour le rallumer).
  - Mesuré 60 i/s sur le chemin GPU dans Chrome affiché, Chrome sans affichage et WebKit. Tom voit encore de l'image par image dans son Chrome : diagnostic `app.html?mesure=madrure` (`diag-studio.js`), qui envoie un résumé chiffré au journal du serveur.
- **Ramage au Studio : Worker.** Le film de pousse et les plumages entiers se calculent dans un pool de Workers (≤ 3, `OffscreenCanvas` en rendu processeur, même code de planche). Le fil principal ne pose plus que des images.
  - Coûts réduits : rosettes voisines peintes une fois en deux calques ; angles des plumes arrondis à 0,3° dans le film.
  - Lecture du film : une image neuve à chaque affichage, l'horloge en garde-fou. Tailles figées sur l'état visé.
  - Premier film préparé dès l'ouverture du Studio.
  - Mesuré : 2,7 à 5,0 s entre événements (11 sur 45 s, tous filmés), sans saut au début ni à la fin.
- **Ramage passe avant Chantourné** dans le rail du Studio.
- **Volubilis.**
  - Au Studio, les fleurs gardent leur place (`_volGel`).
  - La transition est un tissage : un front part de la fleur ; au même endroit, l'ancien se replie pendant que le nouveau pousse (tige depuis sa base, feuilles au passage de la pointe).
  - Elle est dessinée comme le jardin exact (rubans, courbes, cœurs) : plus de saut d'aspect à l'entrée ni à la sortie.
  - 1,8 s au Studio. L'événement suivant attend la fin du tissage.
  - Mesuré : ≈ 106 images par tissage, au plus 3,2 d'écart d'une image à l'autre, aucun saut, sous Chrome et WebKit.

**v92 (28 sept. 2026).**
- **Madrure : le chemin affiché.** `app.html?chemin` pose un bandeau (`diag-chemin.js`) : GPU (vert) ou PROCESSEUR (rouge), avec la raison et ce que le navigateur offre en WebGL. Mesuré : Chrome avec GPU → GPU (293 images qui bougent sur 361) ; **Chrome, accélération graphique coupée → PROCESSEUR, WebGL refusé (SwiftShader, `failIfMajorPerformanceCaveat`), 2 images qui bougent sur 279 : figé** ; WebKit → GPU. Accepter le WebGL logiciel donne 3 i/s : ce n'est pas un remède. Le remède est dans le navigateur (accélération graphique).
- **Madrure au Studio, vitesse.** Dans l'aperçu, `env.trans` est vide : le poids d'une dalle passait de 0 à 1 d'un coup, seules les graines bougeaient (0,9 à 1,3 s). Le poids y joue maintenant sa transition, à la durée visible de la Toile (1 350 ms d'horloge d'aperçu = 2,25 s), et la graine qui part reste jusqu'à ce qu'il soit nul (`Rmad.partDur` au Studio). Mesuré : arrivée 2,22 s, départ 2,20 s (Toile : 2,25 s).
- **Ramage sur la vraie Toile : le chemin du Studio (film des Workers).** Le fond de la Toile (dégradé pendant une transition) passe au Worker en description (`_fondVifDesc`) — un `CanvasGradient` ne passe pas un `postMessage`, c'est ce qui laissait la Toile immobile. Le film se joue pendant qu'il arrive (production mesurée en pixels, une image en retard fait tenir, jamais sauter) ; l'état d'arrivée a son Worker.
- **La plantation simulée (feu vert Tom, moteur touché).** `Toile.simule(ajouts, retraits, fn)` joue la plantation ou le retrait sur des copies des graines, avec un tirage semé GARDÉ pour le vrai geste (même place, même couleur si la Toile n'a pas bougé : `_simSig`). Ramage (`prepareToile` : film + état d'arrivée) et Volubilis (jardin d'arrivée) s'y préparent : à une pause de la phrase (700 ms), au trait, à l'ouverture de Peaufiner (départ), à la confirmation de suppression. Un film préparé n'est joué que s'il correspond à l'arrivée réelle (places, couleurs) ; sinon lecture progressive.
  - Mesuré, vrai chemin, Chrome : Ramage part **45 à 70 ms** après la fermeture de la page + (avant : 2,6 s), départ **145 à 218 ms** après le toucher (avant : 2,1 s) ; WebKit 70 ms. Prédiction sabotée (`_simOublie`) : le film est refait au trait, départ à 0,98 s.
  - Volubilis : **73 ms** après la fermeture (avant : 1,6 à 2,3 s) ; les fleurs gardent aussi leur place sur la Toile ; durée validée 1,2 s gardée.

**v93 (28 sept. 2026).**
- **Madrure, la raison du refus.** `webglcontextcreationerror` est écouté : le bandeau `app.html?chemin` donne le message exact du navigateur pour quatre essais (webgl2 exigeant, webgl2, webgl, experimental-webgl), et si la page est dans un cadre. Relevé : `--disable-webgl` → « disabled by enterprise policy or commandline switch » ; `--disable-gpu` → « Could not create a WebGL context … BindToCurrentSequence failed ».
- **Madrure sans WebGL, le repli.** Mesuré (`--disable-webgl`) : sur la Toile, la parole plantée paraît et la Toile se réarrange (101 images qui bougent sur 343) ; au Studio, chaque événement se pose d'une image (la parole paraît, sans mouvement). Rien de changé : le repli n'était pas mort.
- **Volubilis : 1,8 s sur la Toile aussi** (décision Tom).
- **celebration-mondes.html prépare comme la page +** : la parole existe, l'app prépare (`_simPrepare`) sur une Toile au repos, on plante 3 s plus tard ; le départ se prépare 1,8 s avant. Le moodboard ne porte que les 13 mondes de la première saison : ni Ramage ni Volubilis n'y sont.
- **redteam_rythme** : le chemin « moteur » prépare comme le moodboard ; la ligne du départ de Ramage est RETIRÉE (deux réécritures ne séparaient pas le défaut) ; Houle au départ ±30 % ; Volubilis relevé à 1,8 s. `Toile.ancrePid(pid)` : où le monde pose la parole (pour les juges).
- **Regardé à l'œil sur la vraie Toile** : Ramage — un œil minuscule à 259 ms, rosette pleine vers 1 s, le plumage crème remplacé autour ; Volubilis — bouton à 380 ms, fleur ouverte en ≈ 1,5 s, tiges et voisine qui se recomposent. Ni fondu ni saut.
- **Fin de session (28 sept. 2026, v89–v93).** Madrure : le refus de WebGL venait du Chrome de Tom ; Safari prend le GPU (bandeau `?chemin`). Tom teste désormais dans Safari, le moteur de l'iPhone. Le repli sans WebGL est gardé tel quel.

**v94 (28 sept. 2026) — retour du test iPhone.**
- **La célébration amande est supprimée** (Tom : elle ne rendait rien) : retirée de CHANTIERS (n° 81) et de QUESTIONS (Q258).
- **La mémoire résiduelle au lancement** : le Fil de démonstration se semait à chaque lancement où le Fil sauvegardé était vide (juste après l'onboarding) ; une sauvegarde sans parole était refusée (le jeu de démonstration revenait) ; l'onboarding rendait sa copie du jeu s'il était fermé par un autre que lui ; et rien ne vidait le jeu si l'onboarding était fait sans sauvegarde relue. Les quatre chemins sont fermés (le dernier et la copie ne valent que hors banc, `navigator.webdriver`). Mesuré (WebKit) : après l'onboarding et un rechargement, Fil vide (« Rien ne bouge encore »), Index = la seule parole.
- **La mémoire de Ramage** : la liste de diagnostic `_ramFL` gardait tous les films (≈ 70 Mo chacun) → bornée à 3 ; un film refusé ferme ses images. (Fermer aussi les films poussés hors de la réserve bloquait le Studio : essayé, mesuré, retiré.)
- **Volubilis au Studio : de petites fleurs** (Q351).
- **L'Aura après l'onboarding : un seul disque « Toi »** — `_isMe` reconnaît « Moi » (l'onboarding l'écrit avec une majuscule). Avant : `['moi','Moi']`, après : `['moi']`.
- **L'aide de l'Aura réécrite**, la Pelote expliquée (Q350).
- Non reproduits en WebKit (Mac) : l'« ancien effet d'onde » de Ramage au premier passage, « Adopte ce design » lent. Voir CHANTIERS.

**v95 (29 sept. 2026).**
- **Aide de l'Aura** : textes validés (Q350) ; la carte du Cercle nomme Ramage, Madrure et Volubilis.
- **Le + de l'accueil** : disque bleu Promi (`--c-bleu45`) dans les deux thèmes, croix à l'encre (§3), 4,4 → 5,6 px. L'anneau ne bouge pas.
- **Le plateau de l'accueil** revient à la grammaire (§5) : 342 × 60, rayon 30 (il avait gardé 88 depuis le retrait du compte, v89). Mesuré : l'encre de PROMI centrée à 70,2 pour un plateau centré à 70 ; les deux ronds à 70,0.
- **L'Aura : trois chiffres sous la légende** (tenues · en cours · à tenir), PromiLate 29, à l'encre de la page, chacun centré sous son entrée (écart ≤ 0,7 px) ; rangés par `place()` : légende → 10 → chiffres (30) → 28 → le bouton, la colonne descend d'autant. Masqués dans l'Aura vide.
- **Studio : chaque toucher rebâtissait ses contrôles** (`poser()` au `pointerup`) : les disques, les tons, les points et l'invite comparent avant d'écrire (état + identité des bascules de l'app). Mesuré (WebKit, toucher) : 288/104 → 101/15 changements du DOM par toucher neutre ; un point change toujours de monde, un disque de thème.
- **redteam_onboarding O22 réécrit au niveau de l'instrument** (original `sauvegardes/redteam_onboarding-avant-v95.py`) : 12 O22 seuls, 0 échec ; la rangée n'est touchée qu'immobile, le panneau est attendu 4 s. Prouvé : rouge sur une copie où la rangée n'ouvre rien, vert sur l'app.
- **Ramage en WebKit, mesuré à la densité de l'iPhone (×3)** : 20 à 24 s pour un premier film, 7 à 15 s ensuite. Le coût est la RASTÉRISATION (WebKit la diffère jusqu'à la prise de l'image : ≈ 750 ms par image, 7 500 tracés, disque ≈ 640 px), pas le transport. Le GPU est pire (51 s). Voir CHANTIERS.
- **L'Aura, l'air du groupe « légende + chiffres »** : le bouton remonte de 3,5 (`cptINK`), l'air à l'ENCRE vaut 30,9 au-dessus du groupe et 30,9 en dessous (WebKit, deux thèmes). La légende déclare le groupe (`data-centre-entre` : 4e champ `.au-cpt`).
- **Contrats réécrits au niveau de la décision (§7)**, originaux `sauvegardes/*-avant-v95.py` : `redteam_accueil` (plateau 60) · `redteam_ecrans` (trois chiffres sous la légende, aucun autre ni % ; centrage du groupe, écart de boîte −2,5) · `redteam_air` (4e champ : ce qui ferme le bloc centré) · `releve-aura` (la colonne sous les chiffres ; seuls les trois chiffres permis ; 8 bis : la dalle est ramenée dans l'appareil, l'Aura rouverte repartant en haut). Preuve de 8 bis au vrai doigt (CDP) : après défilement (338 et 252 pt), toucher la dalle ouvre sa fiche.
- **Batteries** : redteam_accueil 22/22 · redteam_ecrans 152/152 · redteam_air intact · releve-aura au vert 1 fois sur 3 — le reste : « les dalles se noient » en clair, l'aléatoire connu du tirage du sol (ETAT-DES-LIEUX, tableau des aléatoires) · redteam_studio_geste 13/13 · redteam_apercus 10/10 · redteam_onboarding 44/44 · redteam_vide 61/61 · redteam_tokens 46/46. `releve-design` non passé : le plateau et le + changent, référence à refiger après validation.

**v96 (29 sept. 2026).**
- **releve-design refigé** (aucun écart avant : le plateau et le + ne sont pas dans ses 26 éléments). Ancienne référence : `sauvegardes/design-reference-avant-v96.json`.
- **L'accueil aligné** : plateau à 40 du haut, barre à 20 du bas → la barre remonte à 40 du bas (736 → 716) ; le panneau des trois natures (30 d'air) et le rond « recadrer » (12 d'air) suivent. `redteam_accueil` réécrit (716 / 726), original `-avant-v96`.
- **Les textes +12 %** (Tom : « tous les textes sauf PromiLate […] seule l'échelle monte ») : `size-adjust:112%` sur Gilbert et Atkinson (4 faces) — aucune taille déclarée ne bouge, les rapports restent, PromiLate intacte ; vaut aussi pour les canevas. Mesuré identique en WebKit et Chromium (Atkinson +12 %, PromiLate 0, interlignes inchangés). Comparateur avant/après sur 13 écrans (≈ 230 textes) : 9 changements — réparés : « rejouer › » et « › » coupés aux Réglages (rangées à 12 de marge, 8 d'écart : plus aucun débordement) ; « 3,25 €/mois » ne se coupe plus après la barre ; « touche-le » ne se coupe plus au trait d'union (U+2011). Acceptés, sans casse : trois paragraphes de l'aide de l'Aura prennent une ligne ; deux titres de l'Index passent à deux lignes dans leur boîte (la ligne d'état reste à 6 px du bas).
- **La Pelote : l'empreinte suit ce qui touche** — taille et allongement lus en continu sur la surface de contact ; orientation = le sens du geste (avant : une diagonale fixe) ; glisser étire l'empreinte (jusqu'à 0,72). Vu (WebKit) : horizontale, verticale, diagonale suivent le geste.
- **Ramage en WebKit, la piste de l'anneau mesurée — et abandonnée** : 62 % des tracés changent d'une image à l'autre, répartis sur tout le disque (la poussée bornée déplace presque toutes les plumes). Six Workers au lieu de trois : 0 gain (18,5 s contre 17,7). Toile au repos (fil principal libre) : 13 s au lieu de 18–26 s. Le coût est un vrai dessin, partiellement freiné par le fil principal. Voir CHANTIERS.
- **Après les textes +12 %, trois contacts réparés** : le Peaufiner d'une Nuée (« écris un mot… » à 2,5 de sa légende → le mot se centre entre libellé et légende, 5,25 de chaque côté, encre 4,3) ; « STUDIO » et « AURA » à 7,4 (plancher 8) → interlettrage de la barre 0,08 → 0,06 em, centres décidés intacts : 8,6 ; les titres du Fil qui passent à deux lignes suivent la règle déjà décidée (ils grandissent vers le haut depuis 92, l'événement monte jusqu'à 8) — `releve-S4` réécrit pour la connaître (original `-avant-v96`), non prouvé contre un défaut posé.
- **Batteries v96** : redteam_ecrans 152/152 · releve-S1 vert · releve-S3 vert · releve-S4 vert · redteam_vide 61/61 · redteam_onboarding 44/44 · redteam_accueil 22/22 · redteam_zoom 16/16 · redteam_gens 38/38 · redteam_tuiles 64/64 · redteam_verbe 6/6 · redteam_nuee 24 écrans 0 écart · redteam_polices 0 couple absent · redteam_tokens 46/46 · releve-aura : l'aléatoire connu seul (« les dalles se noient ») · releve-S5 : l'intermittent connu · **redteam_air : 79 paires rapprochées** (le texte grandit dans des cotes fixes — c'est la demande) ; la plus serrée 4,3 à l'encre, aucune ne se touche. À refiger (`--figer`) quand Tom aura vu les textes.

**v97 (29 sept. 2026) — sept corrections vues sur iPhone.** Sauvegardes : `sauvegardes/app-avant-v97.html`, `app-avant-v97-halin.html`.
- **Aura** : chiffres écartés de la légende (`cptAIR` 10 → 16), le bouton « Partager ma Pelote » suit (`place()`). Encre : prénoms→légende 30,4 · légende→chiffres 18,8 · chiffres→bouton 30,9. `releve-aura` porte les nouvelles constantes en dur.
- **Titres PromiLate recentrés à l'encre** (`lot-V97-TITRES-css`, propriété `translate`, la mise en page ne bouge pas) : tous à ≤ 0,7 d'écart haut/bas.
- **« écris un mot » sur les fiches** : `caleZone()` (le propriétaire) le centre entre le libellé et la légende quand l'aperçu est visible — 14,3/14,3 (carte 118), 7,3/7,3 (carte 104).
- **Réglages** : la valeur de droite sur la ligne de base du libellé (`.scard .k`, +1,49) → écart 0.
- **Accueil, encart du bas** : mesuré ÉGAL dans toutes les tailles (Playwright WebKit 390×664 → 430×932, et Safari du simulateur iPhone 16e : 92 px / 92 px à 3×, soit 30,7 pt). Rien changé ; l'écart vu par Tom = cache de Safari probable.
- **Studio, jauge des palettes** : 270 de large, centrée (60–330) ; le curseur démarre à 45 au lieu de 27.
- **Halin à une parole** : deux cellules neutres compagnes (graines grises, au plus grand vide, aspect par rang) ; elles partent dès deux paroles ; `autoView` les cadre avec la parole. Zéro parole : semis de la Toile vide inchangé.
- **Mondes à 100/200/500 paroles** (WebKit, `scratchpad/infini.py`) : les huit anciens plafonnent à ~50 dalles (semis constant v35 : `plantOne` rend null, les paroles en trop n'ont pas de dalle) ; les douze neufs grandissent, mais à 500 les libellés deviennent une bouillie illisible, et Mascaret (3 s/image), Chamade (1,2 s), Ramage (1,2 s), Madrure (114 ms) ne tiennent plus. Rien corrigé : rapporté à Tom.

**Clôture (30 sept. 2026).** Tom accepte la perte d'air des blocs à hauteur fixe (pas de défilement de la page +, aucun bloc agrandi) : valeurs inscrites dans CLAUDE.md (« PERTES D'AIR ASSUMÉES »). Rail du pinceau regardé à l'œil, avant/après v96, WebKit (page +, page + d'une Nuée, gardé) : lisible, rien ne se touche, l'écart se voit seulement côte à côte. §8 : « on mesure toujours l'encre, jamais la boîte ». **Les deux écrans sans porte** : la langue est MORTE PAR DÉCISION (règle « la Langue sort : aucune traduction n'existe, un choix qui ne change rien est un cul-de-sac », `#langCard` masqué, écran gardé) ; « Arranger la Toile » est une FONCTION VIVANTE SANS PORTE (`targets()`, `state.sort` lu 7 fois, quatre modes : libre, date, personne, Nuée — réorganise les dalles SUR LA TOILE, ce que le tri de l'Index ne fait pas) — aucune porte dans aucune version sauvegardée, pas même `app-origine.html`, aucune décision écrite : question posée à Tom.

**v105 (30 sept. 2026) — Arranger supprimé ; la phrase des murs reprise ; « Garder ta Toile » ; « Ma Parole ! » aux Réglages. Clôture de session.** Sauvegarde : `sauvegardes/app-avant-v105.html`.
- **Arranger la Toile SUPPRIMÉ** (Tom : « on n'en veut pas ») : la pastille de l'accueil, l'icône, la feuille (`#arrangeSheet`), `targets`/`arrGlyph`/`buildArrange`, `Toile.arrange`, `lot-V104-ARRANGER` ; `relax()` rendu à l'identique. Juge archivé `sauvegardes/redteam_arranger-retire-v105.py`. Les sélecteurs CSS morts qui citent `#arrangeSheet` restent (§9). ⚠ Le premier retrait avait laissé le corps multi-lignes de `targets()` : `node --check` vert, app morte au chargement — §8.
- **La phrase des murs** : plus de plateau ; au centre du mur touché, sur le flou, seule ; 34 px réduite jusqu'à ≤ 3 lignes et à la hauteur visible du mur (dans l'Aura, mur d'une rangée : ≈ 20 px) ; encre `#201908` / crème `#F7F0DE` ; une seule taille (« Ma Parole ! » garde l'orange) ; si le mur est trop peu à l'écran, son conteneur défile pour l'amener ; elle reste 1,4 s + 60 ms/caractère (3 à 5,5 s) puis s'efface ; la 1re fois l'offre s'ouvre à la fin de la lecture (Q354). Flou 4,8 px partout, le Studio intact.
- **« Garder ta Toile »** : à 114 sur l'accueil (40 + 60 + 14 — le 142 venait du plateau de 88) ; il ne se retirait jamais quand un écran s'ouvrait (sous le plateau épais de l'Index, sur la recherche du Fil) — il s'efface tant qu'un écran est vraiment à l'écran (`.rap-cache`, test géométrique : Studio/Aura gardent `.show`).
- **Réglages** : la porte s'appelle « Ma Parole ! » (`#openPlusTop`, `encartReglages`).
- **Juges réécrits au niveau de la décision** : `redteam_murs` (26 ; 20/26 sur v104), `redteam_cercle_couleur` (porte « Ma Parole ! »), `redteam_nuee_dalle` test 5 (sans encart, 4,8 ; 36/38 sur la fautive), `redteam_rythme` (Chantourné départ ± 33 %, Tom). Originaux `sauvegardes/*-avant-v105.py`.
- **Série complète (26 batteries, en série)** : murs 26/26 · cercle_couleur 34/34 · S2 0 · écrans 152/152 · vide 61/61 · flash 32/32 · accueil 22/22 · zoom 16/16 · toile 18/18 · nuee_dalle 38/38 (après réécriture) · dalle_figee 4/4 · découpe 0 · aperçus 10/10 · tuiles 64/64 · gens 38/38 · verbe 6/6 · champ 32/32 · S3 0 · nuee 0 · nuee_entree 24/24 · air 708 intactes · design 0 · studio_geste 13/13 · tokens 46/46 · **rythme 99/99** · **releve-aura 4 écarts : dalles de la Pelote sous ΔE 15 (12,5 à 13,8) — défaut ouvert du tirage, pris à ce passage**.

**v104 (30 sept. 2026) — Arranger range la vraie Toile ; les murs du Cercle.** Sauvegardes : `sauvegardes/app-avant-v104.html` (avant Arranger), `app-avant-v104b.html` (avant les murs).
- **Arranger** (feu vert Tom pour la Toile) : `Toile.arrange(mode, instant)` range les GRAINES — les dalles s'échangent leurs places, les cellules grises et la silhouette ne bougent pas ; chaque dalle reçoit une cible (`_ax/_ay`, que `relax()` respecte 1,8 s) et c'est le mouvement ordinaire du monde qui l'y mène, départ adouci comme une plantation (`_tPlante`, `_tMouv`). Ordre des places : rangées de haut en bas, en serpentin. Date = échéance proche en haut ; Personne = moi d'abord ; Nuée = par Nuée ; Inspi = retour à la place d'avant le premier rangement. `lot-V104-ARRANGER` : gardé (`state.sort`), appliqué SANS mouvement au chargement, ré-appliqué EN MOUVEMENT à chaque `sync` (une parole plantée prend sa place). Mesuré (WebKit, graine au plus long trajet) : mondes neufs posés en 1,4–2 s, plus grand pas 4–8 % ; Touffe 7 % ; Braille/Houle 22 % (leur pas naturel). Juge `redteam_arranger.py` 10/10 (3/10 sur la version d'avant).
- **Murs du Cercle** (`lot-V104-MURS`) : encarts « ✦ Le Cercle » retirés des trois Peaufiner, de l'Aura (« Ce qu'on t'a tenu »), de l'aide (CTA + étiquette « Avec le Cercle ») et du Studio (« Ou débloque-les tous ») ; **un seul flou, 4,8 px** (Tom : « deux fois plus flou, plutôt illisible »), Studio intact. Toucher un mur (reconnu à sa géométrie, au TOUCHER — le Peaufiner ne produit aucun clic au doigt) : la phrase suivante monte du bas et reste ; ensuite un toucher n'importe où ouvre l'offre PAR-DESSUS (`_cercleDessus`, l'écran reste dessous) ; la toute première fois l'offre s'ouvre seule 1,3 s après la phrase 1. 21 phrases en ordre puis hasard sans répétition, compteur global `promi_murs`, remise à zéro après 14 jours (Q352 à valider). « Ma Parole ! » en orange `--c-orange42`, le reste à l'accent `--c-bleu45-txt`, sur un plateau. Gardés : porte des Réglages, achat d'un monde à 1 €. Juge `redteam_murs.py` 22/22 (4/22 sur la version d'avant).
- **Juges réécrits au niveau de la décision** (encart centré à 147 + flou 2,4 → pas d'encart + flou 4,8) : `redteam_cercle_couleur` (34/34 ; 30/34 sur la fautive) et `releve-S2-peaufiner` (0 écart ; 24 sur la fautive). Originaux `sauvegardes/*-avant-v104.py`.
- **Batteries** : toile 18/18 · zoom 16/16 · nuee_dalle 38/38 · dalle_figee 4/4 · découpe 0 · accueil 22/22 · aperçus 10/10 · vide 61/61 · flash 32/32 · écrans 152/152 · S3 0 · nuee 0 · air 708 intactes · design 0 · aura au vert · studio_geste 13/13 · gens 38/38 · tokens 46/46. **Rythme 97/99** : Houle au départ rouge une fois sur deux sous charge, Chantourne au départ rouge (≈ 2 050 ms pour 1 849 ± 147) — **mesuré identique sur la version d'avant le lot (A/B, 2 passes)** : antérieur, ouvert.

**v103 (30 sept. 2026) — une porte pour « Arranger la Toile » ; les flashs retirés ; `redteam_flash.py`.** Sauvegardes : `sauvegardes/app-avant-v103.html` (avant la porte), `app-avant-v103b.html` (avant les flashs).
- **Porte d'Arranger** (`#accArranger`, lot-ZOOM, x 266 à côté du recadrage, cachée dès qu'un écran est ouvert) → ouvre `#arrangeSheet`. **⚠ Mesuré : la fonction ne bouge PAS la vraie Toile.** `targets()` déplace `promises[].x/y`, que seul l'ancien calque SVG de `render()` lit — le moteur (graines) l'ignore : même dérive des dalles qu'un témoin sans arrangement. Question posée à Tom (câbler dans le moteur = toucher la Toile, §9 ; ou retirer la porte). La langue reste cachée (décision Tom).
- **Ouverture** : `.topbar` et `.footer` (l'ancien chrome) paraissaient 250–400 ms en WebKit — la règle qui les cache vivait 37 000 lignes plus bas. Doublée dans `<head>` (`lot-V103-PREMIERE-IMAGE-css`).
- **+ → nature** : la page + se montrait dès sa nature posée puis se composait sous l'œil (plateau vide, champ crème, phrase d'un seul bloc ; pour un Chiche, la phrase du Promi puis celle du Chiche). Elle reste cachée (`acc-passe`) jusqu'à 450 ms après le dernier déclencheur de composition + deux images identiques + plateau bâti (`revele()`, lot-ACCUEIL, plafond 1 s) ; `pose()` bâtit le plateau d'une feuille tenue (`visible()`) ; encre demandée à `encreUn` (`window._encrePlateau`) ; plus de fondu d'entrée (`lot-V103-ENTREE-PLUS-css`) ; le voile ne grise plus l'accueil pendant l'attente ; l'ardoise propre d'un Chiche garde le sens `chiche` (un seul clic de tuile au lieu de deux). **Coût : la page + paraît ~0,45–0,55 s après le toucher, d'un bloc** (avant : dès ~0,2 s, en 3–4 états).
- **Planter** : après la dalle couvrante, la page + reprenait son aspect d'avant (~100 ms) puis glissait, son plateau traînant sur la Toile. On COUPE (`cs-coupe` dans `printTirage`).
- **Juge `redteam_flash.py`** (WebKit + Chromium, au doigt) : 32/32 ; **9/32 sur `app-avant-v103b.html`** (ancien chrome, page + incomplète, page + qui reprend son aspect d'avant, dans les deux moteurs). Batteries : tuiles 64/64 · gens 38/38 · verbe 6/6 · accueil 22/22 · zoom 16/16 · vide 61/61 · champ 32/32 · nuee_dalle 38/38 · nuee_entree 24/24 · S3 0 · découpe 0 · écrans 152/152 · design 0 écart · air 708 paires intactes (journaux : `sauvegardes/journaux/serie-v103.txt`, `v103-*.txt`).

**v102 (29 sept. 2026) — `redteam_air` mesure à l'encre, sur 34 écrans ; les airs d'avant l'agrandissement (v96) rendus là où il y a la place.** Sauvegarde : `sauvegardes/app-avant-v102.html`.
- **Le juge était aveugle à l'agrandissement** : il mesurait les BOÎTES ; sur un écran en cotes fixes, les boîtes ne bougeaient pas et l'encre grandissait dedans (fiche de Nuée : « Avec » → titre 5 → 0, vert). Il mesure maintenant le rectangle du TEXTE (`Range`). Prouvé : sur v100, il prend « Avec » → titre 5 → 0. **15 écrans de plus** (accueil, Studio, Partager, le Cercle, Vie privée, À propos, Conditions, Politique, fiche d'une personne, aide de l'Aura, page + Chiche et Nuée, Peaufiner d'un Chiche, Nuée au fil déroulé, vide et pleine) ; chaque écran part d'un état vierge (Studio, Partager, l'Aura et son aide gardent `.show`). **Inatteignables dans l'app** (aucune entrée) : la langue, « Arranger la Toile ». Référence refigée à l'encre (708 paires, 68 écrans) ; ancienne `sauvegardes/air-reference-avant-v102.json` ; référence d'avant v96 à l'encre : `sauvegardes/air-encre-avant-v96.json` (609 paires resserrées au départ de ce lot).
- **Rendu** : colonne des fiches (Promi, Chiche, l'instant) — `window._echTexte` (1,12) et `window._encreSup(taille)` (0,8 / 0,62 × taille × 0,12) : à-qui, titre, état, champ « écris un mot » ; l'instant (cotes du cadre 96/100, « tenue. » → phrase 472 → 479) ; fiche de Nuée remise sous l'ENCRE des noms des Noyaux (+2) ; cartes du fil d'une Nuée (libellé → titre 5, carte d'une ligne 74 → 79, v16 pour deux lignes) ; page + : la consigne tient sur UNE ligne (approche −0,025 em — elle dépassait de 6,8 et 17,1 px), l'interligne de la phrase porte l'agrandissement (67 → 72).
- **Juges réécrits au niveau de la décision** (originaux `-avant-v102`) : `redteam_nuee` (cartes 79, +3/+8/+11), `redteam_nuee_entree` (bas des Noyaux à l'ENCRE de leurs noms, 18), `releve-S1` (à-qui et titre + l'encre agrandie), `releve-S3` (interligne × 1,12). Prouvés : v101 prise (14 et 28 écarts). `releve-design` refigé (cartes du fil de Nuée 83 → 88).
- **NON RENDU, porté à Tom — des conteneurs à cote fixe, où l'air ne se rend qu'en agrandissant** : le rail du pinceau (règle du mi-chemin, 13 sept.) — page + −8,5/−10,5, page + d'une Nuée −10/−13, gardé de côté −6/−8 : la colonne est pleine (~20 px) ; les cartes de l'Index et du Fil (−3/−4 ; « faire les crêpes » passe sur deux lignes) — leurs titres sont ajustés par plusieurs passes, changer la boîte en a rogné (essayé, retiré) ; les cartes du Peaufiner d'une Nuée (−2,7 à −4) ; la tête du Peaufiner (titre → LE TRAIT −3 ; essayé, retiré : la tête centre son titre, la liste est à cote fixe) ; les rangées des Réglages (−2 à −3,5) ; le panneau de Partager (−3,5) ; « ✕ FERMER » → tri (−1,5 à −2). **Décisions, non touchées** : le recentrage des titres v97 (Fil −3,6, aide de l'Aura −4,1, page + Chiche/Nuée −3), les valeurs des Réglages (v98).
- **Batteries** : air intact (nouvelle référence) · nuee 0 · nuee_entree 24/24 · S1 · S2 · S3 · design au critère · vide 61 · écrans 152 · gens 38 · tuiles 64 · verbe 6 · reperage 16 · découpe 0 · accueil 22 · champ 32.

**v101 (29 sept. 2026) — la colonne d'une fiche de Nuée se dérive de l'encre (Tom : A — « le moodboard date d'avant l'agrandissement des textes : c'est lui qui est périmé »).** Sauvegarde : `sauvegardes/app-avant-v101.html`.
- **Colonne normale** : « Avec » = Noyaux + 125, titre = « Avec » + 35, état = titre + 68 (titre de deux lignes : hauteur + 29,2) ; le fil et l'invitation suivent l'état. Airs mesurés à l'encre : **11 · 19 · 5 · 22** (étaient 11 · 18 · 0 · 19). **État défilé** : titre 100, état 140, fil 187 → titre dès 95, **8** puis **31** (étaient 6 et 30).
- **`redteam_nuee` réécrit au niveau de la décision** (original `sauvegardes/redteam_nuee-avant-v101.py`) : décalages écrits en dur (à-qui +1, titre +6, méta et ce qui la suit +9 ; défilé +2 · +4 · +5). Prouvé : la v100 prise 106 fois, la v101 à 0.
- **Autres écrans dont les cotes datent d'avant l'agrandissement** (air comparé à la référence d'avant v96, `sauvegardes/journaux/v101-air-*.txt` ; 0 paire resserrée sur v95, 90 depuis) — **non corrigés, portés à Tom** : page + (consigne → rail du pinceau et rail → barre Peaufiner −14, lignes de la phrase −5, phrase → consigne −2) · gardé de côté (phrase −5, rail −1) · Peaufiner d'une Nuée (12 paires, −1 à −4 : libellé → texte d'aide, aide → note, note → libellé suivant, nom → LE TRAIT) · Index, Fil, Réglages (« ✕ FERMER » → tri / « Toi » −1,5). Voulus, pas des défauts : titre du Fil −3,5 (v97), valeurs des Réglages −1,5 (v98). `redteam_air` ne couvre pas la fiche de Nuée elle-même (ni son état défilé).
- **Batteries** : redteam_nuee 0 écart · nuee_entree 24/24 · vide 61 · air intact · releve-S2 · design · nuee_dalle 38 · reperage 16 · écrans 152 · aveugle 26.

**v100 (29 sept. 2026) — la première ouverture d'une Nuée ne gèle plus 2 à 3 s ; le mot-marque d'une Nuée à sa place.** Sauvegarde : `sauvegardes/app-avant-v100.html`.
- **Mesuré (WebKit, médianes alternées v99 ↔ v100)** : barre Peaufiner en place **2,5 s → 0,65 s** ; plus longue image **1,2 s → 0,44 s** (0,31 s sur une passe moins chargée). Chromium : 2,2–3,9 s → 0,8–1,1 s, pire image ~1 s → 0,28–0,43 s. La bande se complète ensuite en ~2,5 s, sans bloquer.
- **Ce n'était pas d'abord la relecture de pixels** : la relecture portait le temps de DESSIN (un canevas ne dessine qu'au moment où on le relit). Causes, dans l'ordre : ① la clé du cache des dalles prenait la boîte de la cellule au DIXIÈME de pixel — le frémissement de la Toile cachée (0,1 px) re-rendait toute la bande 1,5 s après l'ouverture → demi-pixel ; ② deux travaux de fond (réchauffage v59, collection de l'écran qui vend) tournaient pendant l'ouverture → ils attendent 2,5 s après tout changement d'écran (`_tEcran`, posé par `closeAll`) ; ③ la fiche et son fil se reposent 2–3 fois en 200 ms et leurs peintres appellent `dalleTrame` sans cache → le moteur retient ses rendus 1,5 s (même dalle, k, monde, options, palette, thème, boîte ½ px, couleur : recopie 1:1, `__dalleInfo` compris ; la Pelote `opts.donnees` passe toujours par le moteur) ; ④ `_ficheDalle` peignait encore l'ancienne grappe mauve sur le canevas de la bande (deux propriétaires) → il laisse la main à `_ficheNuee` ; ⑤ un BUDGET par image (40 ms, `window._budgetTache`) pour la bande et les vignettes : une case pas prête est sautée, rendue plus tard une par tâche, puis la bande seule est repeinte (`window._nueeBande`, jamais toute la fiche). Et `willReadFrequently` sur le canevas d'une dalle (relecture 2 s → 0,6–0,85 s).
- **Reste** : ~0,3 s pour construire la fiche elle-même (`openNueeDetail`, `dpRefresh`, poses) — plus aucune dalle dans cette tâche ; une grosse dalle de bande (~190 ms) ne se coupe pas.
- **Mot-marque d'une Nuée** : la ligne v97 propre à la Nuée (+8,85) retirée → 53,1 (redteam_nuee 0 écart).
- **« Avec » → titre → état : NON corrigé, conflit porté à Tom.** La cause n'est pas v97 mais v96 (`size-adjust:112%` sur Gilbert et Atkinson : les lignes grandissent, les cotes de la Nuée — titre = « avec » + 30, état = titre + 65 — restent figées). Mesuré sur trois versions : avant v96 [5, 22], depuis [0, 19]. Rendre l'air demande +3,5 au titre et +4,5 à l'état ; `redteam_nuee` n'en tolère que 3.
- **Batteries** : redteam_nuee 24/0 · nuee_entree 20/24 (le conflit) · releve-S2 · S1 · S3 · design au critère · vide 61 · air intact · nuee_dalle 38 · reperage 16 · toile 18 · gens 38 · tuiles 64 · verbe 6 · apercus 10 · dalle_figee 4 · accueil 22 · écrans 152/152 · découpe 0 · rythme 89/99 (toutes durées tenues ; cadences sous charge — v99 dans les mêmes conditions : 84/99 ; la machine portait 240 % de CPU d'autres applications) · releve-aura 1 à 3 (« se noient » + « rapporter le livre » intermittent, défaut connu du tirage, pris à ce passage).
- **Piège noté** : `redteam_decoupe` borne le moteur à la première ligne qui commence par `})();` — une IIFE ajoutée dans le moteur doit se fermer autrement (`}());`), sinon tout ce qui suit passe « hors moteur ».

**v99 (29 sept. 2026) — la carte « LE TRAIT » d'une Nuée n'est plus vide.** Sauvegarde : `sauvegardes/app-avant-v99.html`.
- **Cause, mesurée en WebKit (ce n'était PAS deux constructeurs qui alternent, comme écrit en v98)** : `garnitNuee` ne passait qu'à heure fixe après un clic (100 · 320 · 700 ms) ; en WebKit la carte `#npTrait` naît plus tard et restait vide jusqu'au clic suivant (0 pastille à la 2e ouverture, 12 à la 3e) ; et il sautait une carte dont la signature n'avait pas changé, même sans rail. → le placement (`_nueePeaufiner`) l'appelle à chaque ouverture ; une carte sans pastilles se regarnit. Sonde `scratchpad/v99_trait.py` : v99 12 pastilles dès la 1re ouverture (WebKit 3 passes, Chromium 4/4).
- **Trouvé, non corrigé — la première ouverture d'une Nuée gèle 2 s (WebKit) à 3 s (Chromium)** ; la deuxième se pose en 0,1–0,2 s. Profil : 3,9 s dans `Toile.dalleTrame` (dont 2 s de `getImageData`) — les dalles de la petite Toile rendues à froid (`_ficheNuee` → `dalleDe` → `_rendDalle`). Pendant ce temps la barre Peaufiner est hors écran : un toucher tombe à côté. Sondes `scratchpad/v99_barre.py`, `v99_profil.py`.
- **Batteries** : releve-S2 au critère (0 partout) · redteam_vide 61/61 · redteam_air intact (500 paires) · **redteam_nuee 18 écarts et redteam_nuee_entree 20/24, identiques sur v98** (repassés sur la version d'avant) : mot-marque d'une Nuée à y 61,9 au lieu de 52 (probablement le recentrage des titres v97), air sous « Avec » 0 au lieu de 5 — juges ou fiche à reprendre, non touchés.
- Session : capture d'accueil iPhone reçue (plus de films : une capture suffit, Tom). Serveur : l'adresse du Mac est passée à 192.168.1.133.

**v98 (29 sept. 2026) — les mondes tiennent 500 paroles.** Sauvegarde : `sauvegardes/app-avant-v98.html`.
- **Les huit anciens ne perdent plus de paroles** (Tom : « une parole qui n'apparaît pas est inacceptable ») : semis constant tant qu'il y a une cellule vide, puis `_celluleEnPlus` (au plus grand vide, déjà posée). Mesuré : 50→52, 100→102, 200→202, 500→502 dalles colorées ; pire image 82 ms (Houle à 500).
- **Les titres sur la Toile s'effacent** quand la dalle, à l'écran, n'a pas 48 px (écart moyen × zoom) — fondu sur 8 px ; ils reviennent au zoom. Vers 130 paroles (un peu plus tôt dans les anciens). Avant : forcés à 28 px de large, empilés, et 8 700 mesures de texte par image.
- **Mascaret** : les 5 bandes les plus proches sans tout trier (même choix), les seules lames non nulles par bande (mêmes termes, même ordre), budget de construction (> 40 ms → on repeint la précédente, reconstruit après 4 × son coût).
- **Chamade** : voisins par grille au-delà de 80 cœurs (jusqu'à 80, toutes les paires, comme avant), budget de la disposition et du point fixe, clé d'une parole gardée 1 s.
- **Ramage** : clé gardée 1 s, budget du point fixe, couleurs/liste calculées une fois par film, pas de film au-delà de 24 yeux (chargement en masse).
- **Mesuré en WebKit, machine propre, à 500** : Mascaret posé en 2 s puis 60 i/s (plantation : pire 0,5 s) ; Chamade posé en 4 s (plantation : première image 1,65 s) ; Ramage 5,5 s pour la première image du chargement, puis 25 à 60 i/s, plantation 50–60 i/s. À 200 : fluide partout.
- **Régression v97 corrigée** : le libellé NOTE passait à 12 (la zone de texte portait encore sa hauteur par défaut, 56, au moment du centrage) — prise par releve-S2.
- **releve-S2 réécrit au niveau de la décision** (palette du 16 sept./v7, Q221, Gilbert/Atkinson, rangée qui supprime v16) — original `sauvegardes/releve-S2-peaufiner-avant-v98.py` ; prouvé contre une sonde posée (58 écarts pris, 0 sans).
- **Trouvé, non corrigé** : le Peaufiner d'une Nuée a DEUX constructeurs qui alternent d'une ouverture à l'autre (les cartes du lot Nuée, ou la liste de la section 2) ; aux deux premières ouvertures « LE TRAIT » est vide, le rail du pinceau n'apparaît qu'à la troisième. Antérieur à v97.
- **Halin, cadence** : 85 à 100 % sur machine propre (33/33) ; les 39–45 % venaient du simulateur qui tournait Promi en arrière-plan.
- **Références refigées (textes validés par Tom)** : `releve-design` (142 éléments, 0 écart ; ancienne `sauvegardes/design-reference-avant-v98.json`) et `redteam_air` (500 paires, 38 écrans ; ancienne `sauvegardes/air-reference-avant-v98.json`). Les 90 paires rapprochées étaient les textes +12 % (v96), le titre du Fil recentré (−3,5) et les valeurs des Réglages alignées (−1,5).
- **Batteries v98** (machine propre, simulateur éteint — ouvert, il pesait 25 à 73 % et faussait tout) : redteam_vide 61/61 · toile 18/18 · zoom 16/16 · aperçus 10/10 · nuee_dalle 38/38 · découpe 0 · accueil 22/22 · tokens 46/46 · releve-S1 et S3 verts · releve-S2 : style 0, reste l'écran de Nuée « jamais posé » (les deux constructeurs) · releve-aura : 1 (la dalle illisible du tirage, connue ; 2 sur la version d'avant) · redteam_rythme 96/99 (Houle, Tesselle au départ : 29/29 repassés seuls, avant comme après v98).
- **v106 (30 sept.) — le lexique** : la Nuée s'affiche **Cercle**, l'offre **Ma Parole !** (clés internes inchangées) ; 142 textes relevés et changés, accords au masculin ; écran qui vend « MA PAROLE ! · Retourne ta Toile · Bon, allez d'accord » ; Réglages payés « Tu es Membre Ma Parole ! » (la porte reste visible, sans lien) ; phrases des murs en Gilbert. Relevé et propositions : `RENOMMAGE-LEXIQUE.md` (Q355). Juges au nouveau mot (renommage) : accueil, tuiles, repérage, nuee, releve-S2/S3/S4 — originaux `sauvegardes/*-avant-v106.py`. Sauvegarde `sauvegardes/app-avant-v106.html`.
- **v107 (30 sept.)** — « Essayer 14 jours » revient en bouton principal, « Bon, allez d'accord — 39 € / an » sur l'option (l'offre au mois n'y est plus) ; Q355 validée (variantes A) ; `releve-design` refigé (titre « Cercle » 146 px). Sauvegarde `sauvegardes/app-avant-v107.html`.
- **v108 (30 sept.)** — l'offre au mois revient EN PETIT sous les deux boutons de l'écran qui vend : « ou 5,99 € par mois » (`.pc-mois`, 810 ; la mention légale descend de 816 à 828) ; texte seul, pas un bouton. Q352 validée (14 jours). Le « ! » en Gilbert du titre est gardé (Tom). Sauvegarde `sauvegardes/app-avant-v108.html`.
- **v109 (30 sept.) — LES NOTIFICATIONS** (`lot-V109-NOTIFS`). **Ajout validé, hors inventaire** : la question « Je te le rappelle ? · oui · pas besoin » — paraît à la plantation d'une parole datée (à la place du bandeau de l'accueil), jamais au lancement, permission demandée après « oui » seulement ; deux « pas besoin » puis plus rien. Réglages : « Notifications › » ouvre sa page (`#notifScreen`) — Mes paroles datées (gratuit) · Mes paroles en l'air et L'heure (mur Ma Parole !, flou 4,8 + phrase) · Ce qu'on me lance (bientôt, Firebase). Mots de Tom ; **rien quand la date est passée** ; une par jour au plus ; « Rappels activés ✓ » retiré. Envoi : page ouverte seulement (Safari iOS n'a pas l'API hors écran d'accueil — l'envoi réel vient avec le portage). Juge `redteam_notifs.py` (34/34 ; 4/10 sur `app-avant-v109`, et la sonde « date passée » est prise). Q356 à valider. Sauvegarde `sauvegardes/app-avant-v109.html`.
- **v110 (30 sept.)** — Q356 validée ; « C'est aujourd'hui » part à l'heure choisie (était 9 h). `redteam_notifs` 36/36 (contrôle 10 neuf, pris sur `app-avant-v110` à 34/36). Sauvegarde `sauvegardes/app-avant-v110.html`.
- **ASSAINISSEMENT · lot 1 (30 sept.) — LE BANC DE RENDU DE RÉFÉRENCE** `banc_rendu.py` : 20 mondes × (Toile entière clair/sombre, sans titres + 4 dalles — Promi, Chiche, tenue, d'un Cercle — × k 0,5 · 1 · 2) = **280 images**, référence `banc-rendu/ref/` (PNG + manifeste, empreintes). Hasard amorcé avant le chargement, horloge et images de l'app PILOTÉES par le banc après (les caches ne se bâtissent jamais sur le temps réel), chaque monde reposé sous la même graine en passant par l'autre famille. **Déterministe : 0 image différente sur 280 entre deux passes complètes.** Prouvé : une sonde (pas de trame de Tesselle 11 → 12) est prise sur ses 12 dalles et rien d'autre. WebKit. Planche : `banc-rendu/planche-ref.png`. C'est lui qui juge le lot 2 (moteur) et, plus tard, le portage.
- **ASSAINISSEMENT · lot 2 (30 sept.) — LE MOTEUR** (feu vert Tom ; sauvegardes `app-avant-assainissement.html`, `promi-moteur-avant-{reglages,contexte,semis}.js`) :
  · **extrait** dans `promi-moteur.js` (7 829 lignes, les 12 blocs d'origine dans leur ordre : les mondes, le moteur, la clé, la pose des dalles), chargé par l'app à la même place ; les copies périmées `promi-mondes.js` et `promi-mondes-integre-v32.js` rangées dans `sauvegardes/fossiles/` ;
  · **fossiles retirés** : l'ancien moteur SVG (`render()` calculait un Voronoï sur promises[].x/y puis écrivait `svg.innerHTML=''` — il reste un relais qui garde ses seuls effets vivants ; `lloyd`, `anim` retirés), le monde **Éclats** (RD, TH, LIVE, WL, Cercle, STRUCT, Rblok) ;
  · **les 36 tests `theme==='…'` du moteur** et la table du pas de trame deviennent **`REGLAGES_MONDE`** — chaque monde déclare `ressort`, `elanPlante`, `libre`, `grille`, `pasTrame`, `finaleAuRepos`, `relaxLocal`, `ondeNoeuds`, `donneesPropres`, `compagnons`, `apercuPause`, `apercuFilm`, `apercuPetit` ; 0 test par nom restant ; lecture `Toile_reglages(m)` ;
  · **`dalleTrame` à contexte explicite** : `_ctxPrend()` / `_ctxRend()` dans un `finally` — rien de global ne reste modifié, même sur erreur, et elle est réentrante (vérifié : monde, taille, vue, semis identiques après un appel dans un autre monde et un appel qui échoue) ;
  · **LE SEMIS AMORCÉ PAR LA CLÉ DE LA TOILE** : 59 `Math.random()` du moteur passent par `_alea()`, réamorcé à chaque construction du semis (semis de base, synchronisation, plantation) depuis `Toile.cle()` et ce qu'on construit ; changer de famille de monde ressème DEPUIS ZÉRO. Mesuré : **une personne qui rouvre l'app retrouve la même Toile (0 dalle déplacée sur 18, 4 réouvertures × 2) — avant : 18/18 à chaque fois.** ⚠ La toute première ouverture du jeu de démonstration varie encore : l'orchestration du DÉMARRAGE de l'app (hors moteur) appelle sync/reGray dans un ordre qui dépend du minutage.
  · banc : au pixel à chaque étape sauf la dernière (le semis change, par décision) — référence refigée, l'ancienne gardée dans `banc-rendu/ref-avant-semis/`, planche `banc-rendu/planche-semis-avant-apres.png`. Le banc pilote désormais aussi les minuteurs et requestIdleCallback (ceux du démarrage sont repris en temps piloté) ; `--monde=` pose les mondes qui précèdent.
- **ASSAINISSEMENT · lot 3 (30 sept.) — LES DOCUMENTS.** `ETAT-30-SEPTEMBRE-2026.md` (209 lignes) ENGENDRÉ par `etat_generer.py` depuis `PROMI-TOKENS.json` et l'app en marche : lexique affiché ↔ clé, couleurs (rôles), polices et niveaux, les 20 mondes (nom, clé, accès, semis, réglages déclarés), les 24 palettes, l'offre et les 21 phrases des murs, les notifications, les invariants. `PROMI-SPECIFICATIONS.md`, `PARCOURS.md`, `MOODBOARD-VALEURS.md` marqués **ARCHIVE — NE PAS PORTER**. CLAUDE.md : nouvel ordre des sources en tête (plus aucun renvoi à MOODBOARD-VALEURS comme source de vérité) ; note sur « Nuée » / « le Cercle » dans les blocs d'avant v106 ; **socle des §3 à §6 repris — 18 passages contradictoires corrigés ou marqués *(historique)*** : trois tons, couleurs signal, fonds, corps de fiche et célébration, zone haute à l'encre, traits à 150°, champ blanc, seuil 42 / ΔE 15, aplat d'état, « figé à la création », bande de Cercle, huit → vingt mondes, Éclats, palette par défaut, mot-marque, table des polices, titres en Fraunces, niveaux, « six faces ». Ancienne version : `sauvegardes/CLAUDE-avant-assainissement.md`.
- **ASSAINISSEMENT · lot 4 (30 sept.) — LES JUGES.** `SPEC-JUGES.md` ENGENDRÉ par `spec_juges_generer.py`, valeurs lues DANS les juges (arbre Python, rien d'exécuté) : le rythme des 20 mondes et ses tolérances, les 20 constantes du rythme, les murs, les notifications et leurs mots, les gestes (Pelote 380 ms / 8 px, Studio 480 / 390 / 48), les éclairs, l'air, les filets, le contrat visuel. **Réécrits (originaux `sauvegardes/*-avant-assainissement.py`), chacun prouvé contre une sonde :** `redteam_air` (une paire disparue n'est plus sautée — elle a pris ~60 paires « Nuée » renommées ; refigé : 700 paires, 68 écrans, stable) · `redteam_toile` (le % et sa double encre lus au TRACÉ piégé, plus dans `_noyauSig`/`_sigEncres` — sonde prise 12/18) · `redteam_geste` (le Noyau lu sur l'IMAGE par différence, horloge figée, centre comparé au doigt ; couleurs retirées #FFD447/#8FE08F supprimées ; « la Pelote peinte dans son bloc » mesurée DANS le bloc — elle rougissait à tort, antérieur ; « Mes Promi : le % est peint » RETIRÉ, règle abandonnée par Q287, il passait à vide sur les dalles) · `redteam_pelote_partage` (le recouvrement jugé sur les vrais `drawImage` — sonde prise) · `redteam_zoom` (le rond lu à l'écran, jugé quand la main a posé la vue : à la Toile entière il est caché exprès, l'ancien contrôle passait à vide — sonde prise) · `redteam_champ` (condition morte retirée ; un champ non mesuré est nommé) · `redteam_tokens` (lit aussi `promi-moteur.js` ; polices en LISTE BLANCHE — il prend 3 `Georgia`, dont **un défaut réel : le « i » de l'Aura peint en Georgia italique**, non corrigé, l'app n'étant pas dans le périmètre) · `redteam_tonsurton` (le champ de « referme » est l'amande #8FE08F, plus le menthe d'août ; ⚠ pendant ce moment le canevas DÉCLARE encore #82AEF8) · `redteam_decoupe` et `redteam_rythme` (lisent le moteur dans `promi-moteur.js`). **Retiré** : `releve-fiche-personne.py` (33 rouges sur 144 contre une planche abandonnée, hors série) → `sauvegardes/juges-retires/`. **Faux positifs de l'audit, vérifiés** : `redteam_fonctions` (la composition n'y sert qu'à désigner le bandeau ; le verdict est au geste), `redteam_nuee` et `redteam_nuee_entree` (verts). **Non traités** : les flottements connus (toile « intitulés », nuee_dalle 10, releve-S5, releve-aura, Houle) et les 13 juges jamais prouvés.
- **v111 (30 sept.)** — Halin : arrivée acceptée à 2 270 ms (`redteam_rythme`, décision Tom). Le « i » de l'Aura en **Gilbert** (était Georgia italique) ; les deux `Georgia` morts de la fiche passent au jeton de la marque (sans effet à l'écran) — `redteam_tokens` 46/46. **Cercle : plus de filets** sur sa fiche et sa page + (sous le trait, sur les disques) — une exception nommée `_sansFiletCercle`, lue par les trois peintres ; ⚠ sans filet, l'arc « en cours » #291547 se lit mal sur le corps #1B1426. **Cercle : on peut taper** — le Peaufiner à cartes (l'un des deux constructeurs qui alternent) ne peignait que le texte d'invite de DESCRIPTION et COMMENTAIRES ; il emprunte maintenant les vrais champs (#nqNote, #dCommentInput), à la police et à la couleur de la carte, rendus au départ (vérifié au doigt, WebKit, trois ouvertures × deux thèmes ; le simulateur iOS reste à essayer). ⚠ un commentaire de Cercle n'a toujours pas de stockage (`_addComment` ne sert qu'une fiche). **Le compte par l'envie** : sans compte, toucher la photo ouvre le panneau « Garder ta Toile » (`lot-V111-COMPTE-PHOTO`) ; le nom se change librement ; aucun rappel ajouté. Planches à choisir : Q357 (sombre), Q358 (corps Promi / Chiche). Sauvegarde `sauvegardes/app-avant-v111.html`.
- **v112 (30 sept.)** — Les phrases des murs : l'orange devient **#FE5000** (`--c-orange59`, était #F07A2E, « terne, pas invitant ») ; il ne marque plus seulement « Ma Parole ! » (5 phrases sur 21) mais aussi UN mot dans quatre autres — « solution », « habitudes », « essayer », « tradition » — soit 9 sur 21, le texte inchangé ; la phrase passe de 34 à **38 px** au plus (plancher 18 → 20). `redteam_murs` 26/26, `redteam_tokens` 46/46. `redteam_air` refigé (v111 : les deux invites du Peaufiner d'un Cercle sont devenues de vrais champs — posés au même centre, vérifié à l'encre) : 696 paires, stable. Halin au nouveau plancher : moteur 2 286, vrai chemin 2 261 (attendu 2 270). Sauvegarde `sauvegardes/app-avant-v112.html`.
- **v113 (30 sept.)** — Corps sombre de la fiche et de la page + : **option 2** — Promi `#335382` (`--c-bleu35`), Chiche `#7C3F58` (`--c-framboise35`), et le Cercle monte à `#5D4978` (`--c-mauve35`) : c'est ce qui rend l'arc « en cours » `#291547` lisible sans filet (Δlum 52 ; la flèche ΔE 41). Seulement sur `#detailPoster` et `#createSheet` en sombre (lot-V113-CORPS-SOMBRE-css) ; les cartes de l'Index et du Fil ne bougent pas. **Filets retirés** sous le trait, la flèche et autour des disques, pour les trois natures (`window._sansFilet`) — **sauf sur la terre `#2B1020` d'une fiche tenue**, où la crête `#0B4A2A` disparaîtrait sans lui. Jeton : PROMI-TOKENS.json → CSS → Swift, `redteam_tokens` 46/46. Planches : `planche-sombre/serie2/` (mode sombre, 9 fonds de tableau), `planche-pelote/` (6 traitements) — Q357, Q359 à choisir.
- **v114 (30 sept.)** — **La Pelote, seul volume de l'app** : halo de sa couleur (0,10 au bord → 0 à +0,25 D, 0,04 sur le quart inférieur) et ombre (116 × 18,6, 0,12, encre du mode, centre à 7 % D sous la boule) — `lot-V114-PELOTE-css`, #auPeloteHalo / #auPeloteOmbre. Elle descend de **47,24** (haut visible du halo à 128 = plateau + K.AIR, mesuré 128,6 / 127,6), ce qui suit de **65,81** ; bas du bouton 827,3 < 844. Juge **`redteam_volume.py`** (statique, liste blanche nominative, dette de 305 nommée ; `--sonde` rougit). **`redteam_filets.py`** étendu au filet du TRAIT, piégé dans le canevas (il ne le voyait pas) : exception nominative « fiche tenue » (terre), 14/14 ; rougi 9/14 sur app-avant-v113. **Jamais de kaki** (OKLCH h 78–140, C ≥ 0,015) : **`redteam_kaki.py`**, rouge à la naissance sur l'app (fond de Toile, rampes, crème dalle, 15 palettes — décision attendue) ; planche série 3 (noyer · ardoise · graphite × dalles L 0,25 / 0,21) dans `planche-sombre/serie3/`. **Clavier du Cercle** : `focus()` du nom passé DANS le geste (il partait à +30 ms ; champ invisible, donc aucun autre moyen d'écrire) — preuve simulateur `preuves-v114/`, juge **`redteam_clavier.py`** (rougi sur app-avant-v114) ; 7 autres différés listés, non corrigés. CLAUDE.md : kaki, volume, filet, planches @3x, §11 dégradation adaptative.
- **v115 (30 sept.–1er oct.)** — **Aura** : espacement mesuré sur la SILHOUETTE (G1 = G2 = 56, la Pelote monte de 8,1) ; la phrase et tout ce qui suit DESCENDENT de 50,4 (ombre plus loin + G2) → « Partager ma Pelote » à 877,7, sous le pli (Q362) ; légende égalisée (16,71 / 16,68) ; « TOI » en capitales (les noms étaient déjà en Gilbert 700, sa seule graisse). **Couronne de fibres** (`lot-V115-PELOTE`, `_couronnePelote`) : jusqu'à 0,12 D, couleurs de `rampeVelours`, dosée par ΔE00 (6,6–11,6 mesuré), respiration 10 s, Réduire les animations → mi-cycle ; **ombre** 0,45 × 0,07 D à 0,20 D, aucune en sombre. Juges `redteam_couronne.py`, `redteam_volume.py` (couronne en liste blanche, sonde de couronne sur une dalle rougit). **Kaki** borné (L 0,20–0,80, C ≤ 0,10) ; encre de Touffe neutre `#F4F2F0` en sombre (`_tfInkTouffe`, Touffe seul) ; 34 couleurs coupables restantes (planche). **Série 4** du mode sombre (5 planches @3x). **Clavier** : 8 focus synchrones (`redteam_clavier.py`, rougi sur v114) — 5 des 7 chemins sont INJOIGNABLES aujourd'hui. **Page +** : coupe de l'exemple à l'échelle RENDUE (sortait de l'écran sur iPhone) et retour à la ligne plutôt que réduction (`redteam_marges.py`) ; pilules Chiche/Promi à l'encre (1,42 → 10,83 et 1,97 → 7,77 : 1, `redteam_pilules.py`) ; suggestions 1 et 2 fixes puis tirage sans remise (`redteam_suggestions.py`, `listes-suggestions.md`). **Dette de redteam_volume classée** : 6 violations visibles (dont le fond de la Toile, ΔE00 5,1), 299 faux positifs, 0 légitime. `banc_rendu --figer --monde=` fusionne désormais (il écrasait le manifeste).
- **v116 (1er oct.)** — **Couronne de fibres RETIRÉE** (Tom : « des fils cheap ») ; `redteam_contour.py` : rien ne dépasse de la silhouette (le poil natif s'arrête à 124,1 ; la couronne allait à 147). **Ombre à 0,04 D** sous la silhouette : « Partager ma Pelote » revient dans l'écran (840,6 ; était 877,7), G1 = G2 = 56. Respiration : **planche de trois options** dans le contour (`planche-pelote/v116/planche-respiration.png`), non intégrée ; crochet d'essai `window._peloteMod` (sans effet s'il n'est pas posé). **Encre de seiche intégrée** en sombre, −2 % (fond `#050302`, h 54,8°) : moteur (rampes, fond plat, renderTo, fondToile, aperçus, noir et blanc, dalle neutre d'Ingénu, grain) + pages (`--c-brun09` en sombre) ; `redteam_kaki` source : 0 coupable. **« + ajouter quelqu'un »** sur sa ligne, liste dans `.gn-liste` (`redteam_ajouter.py`) ; choix ouvert de la page + : onde base 144 / amp 16, trace 184, phrase 228 (releve-S3 réécrit, original gardé). **Phrases** : `listes-suggestions-v116.md` (4 listes actuelles + 100 propositions).
- **v117 (1er oct.)** — **Phrases** : les listes définitives intégrées telles quelles, avec leurs variantes plurielles et en « vous » (`_ppVar`), les fixes ① ② (① seul pour le Chiche) puis tirage sans remise. **Respiration de la Pelote (Q364 → A)** : la lumière du velours 0 → 0,55, cycle 10 s (4 + 6), départ 0,6 s après la première image, au temps réel, arrêt hors écran, immobile avec Réduire les animations — `redteam_souffle.py` (rougi sur v117b) ; coût mesuré en WebKit @3x : 64 → 71 ms par image. **Ombre** écartée de 60 pt (≈ 1 cm), crème en sombre ; **Pelote** remontée de 6 (G1 = 50) ; la colonne descend de 54, « Partager ma Pelote » à 894,6 (Q367). **Partager depuis une fiche** (Promi, Chiche, Cercle) : le rond appelait `ouvrirPartage`, inexistant, et la barre Peaufiner ne produit aucun `click` (doigt NI souris) → Mon Folio réduit à la parole (au Cercle : ses Promi), sans la Pelote, choix d'avant rendu à la fermeture et jamais sauvegardé — `redteam_partage_fiche.py` 48/48 (12/30 sur v117b), image identique à Mon Folio réduit à la main (écart 0,00). **Bouton photo d'une fiche** : il était RECOUVERT par `#dpMain` (z-index égal, venu après) — injoignable au doigt ; il ouvre maintenant un menu « Importer une image » (sélecteur du système, dans le geste) · « La dalle d'origine » / « Suivre le Studio » (`p.dalleOrigine`, monde de plantation passé partout où la dalle est rendue seule, Toile non touchée) — `redteam_photo_menu.py` 18/18 (6/8 sur v117b) ; Q365, Q366. Vérifié : l'Aura et la Pelote gardent le monde et la couleur de plantation (30/30 appels). Planche « mise en valeur » (Q368). Billet d'or : proposition seulement.
- **v118 (2 oct.)** — **Dépôt git** (branche `main`, `origin` = github.com/Tomot69/promi-2026) : chaque lot finit par un commit, le hash au rapport. **Joignabilité** : `redteam_joignable.py` (elementFromPoint au centre de chaque élément interactif, 36 écrans ; fonctions appelées et nœuds porteurs des gestionnaires), dette nommée `joignable-dette.json` (2 murs, 4 gardes), inventaire `joignable-inventaire.md` ; rougit sur v117b (bouton photo recouvert, `ouvrirPartage` ×5, 4 nœuds disparus). **Q363** : code JS retiré — l'ancien « à qui » de la phrase, `#dpaJoint`, `#dpsCom/#dpsJoint/#dpsPart` + `ouvrePeaufiner`, `#dpBarre` (`dpbCom/dpbJoint/dpbPart`, `vaVers`), `toPseudo`/`prefill` et les deux boutons de l'ancien écran de compte (8 597 caractères) ; le CSS reste (§9) ; `redteam_clavier` (3 champs) et `releve-design` (« fiche · bouton rond » retiré) réécrits, originaux gardés ; « garder de côté » non touché (Q370 : il ferme la page + sans rien garder). **Q365** : la bande haute porte la couleur d'origine sauf ton sur ton (ΔE < 15 → rampe de Q30), `lot-V118-ORIGINE`, `redteam_origine.py` 64/64 (rougi sur v117 et à la sonde). **Q366** : « La dalle du Studio ». **Q367** : « Partager ma Pelote » sous l'ombre (525,5 → 585,5, G2 = 56), l'encre de la phrase à 56 sous le bouton, air à l'encre 27,0 / 27,0 autour de « légende + chiffres » ; `redteam_ecrans` et `air-reference.json` repris (originaux gardés). **Q368** : l'écho décalé (`.au-echo`, `_echoPelote`, `lot-V118-PELOTE`), en liste blanche de `redteam_volume` (`--sonde=echo` rougit) ; D exclu. **`?mesure=1`** : temps par image respiration active / coupée (banc WebKit sans GPU @3x : peinture p50 74 / 64 ms ; Chromium GPU : sans écart) — Q371. **Fond de la Toile à plat en clair** (`#DFCAA4`, `_fondVif` rend une couleur ; dette volume 305 → 304). **2 € le design.** **Le Zzz** (`lot-V118-ZZZ`) : soleil NOAA aux coordonnées du fuseau (429 fuseaux), nuit = coucher + 1 h → lever, bascule au changement d'écran ou au retour au premier plan, sans fondu, cran de nuit (32 jetons crème/blanc, OKLCH L −0,06) ; premier lancement en clair (remplace Q301) ; `redteam_nuit.py` 33/34 — le bouton « Zzz » n'est PAS posé (Q369 : la ligne ne reçoit pas un 3e disque) et le Zzz ne s'active pas seul tant qu'il manque. Planches `planche-v118/`. Rouges d'avant ce lot, inchangés : `releve-S1` 12, `releve-S4` 3, `releve-S5` 13 (fonds sombres `#050302` de v116), `redteam_apercus` 8/10, `redteam_murs` 25/26, `redteam_kaki` 14, `releve-aura` (gabarit d'avant v115 : 42 → 33).

- **v120 (2 oct., retour en arrière)** — **v119 annulé** (`git revert bd156ae`). Cause de la casse du Studio : le Zzz activé au premier lancement — la nuit, thème forcé au sombre, les disques SOMBRE / CLAIR sans effet à l'écran (reproduit au doigt, hors navigateur piloté ; les palettes, elles, sortent pleines sur le banc et au simulateur : non reproduit). **Zzz coupé partout** (`COUPE=true`), passe de nuit absente. **Couleurs d'avant v116 hors de la Toile** : la substitution brun → seiche des pages sombres retirée ; `redteam_couleurs_ref.py` (417 écarts sur l'état d'avant, dont ~380 de seiche). **Pelote pleine** (`redteam_plein.py` 75/75, 36 rouges avant) ; écho retiré, halo et flaque de v119 repris (`redteam_halo` 23/23), `?densite=1|2|3` et `?halo=1|2|3` ; coût Chromium GPU @3x par palier : densité 1 → 20,5 / 17,9 / 16,0 ms, densité 2 → 27,2 / 24,6 / 24,0, densité 3 → 40,8 / 31,8 / 27,3 ; le régulateur vise le palier le plus bas dans les trois cas (75 000, 112 500, 150 000). **Orange des murs `#FB4C0D`** : 2,27 : 1 sur les corps sombres, `redteam_murs` 25/26 — Q373, le lot s'arrête là (§5 non fait). Planches `planche-v120/`.

- **v121 (3 oct.)** — **Couleurs de v118** (la référence de v120 était fausse) : la seiche revient dans les pages sombres ; `redteam_couleurs_ref.py` repointé sur `578ec80` (480 écarts sur l'état d'avant → 0, après reprise sur page fraîche), dalles rendues seules comparées de façon synchrone (108 couleurs, 0 écart). Planche 2 : la fiche « faire les crêpes » de v113 à v119 — seul le plateau sombre change (brun jusqu'à v115, seiche dès v116). **Aura remontée** : ombre −6, G2 sous l'ombre 50, colonne −12 (« Partager ma Pelote » 513,47). **Halo** : niveau 3 par défaut, niveaux 4 et 5, canevas propre sous la boule, trame en niveaux de couleur ; `redteam_halo` 91/91. **Orange des murs** : `#FF7A55` sur les corps sombres de Peaufiner, `redteam_murs` 26/26 (Q373). **§5** : « garder de côté » (18/18) puis violations retirées (dette du volume 290), Studio repassé après chacune. ⚠ `redteam_air` rouge sur 8 paires du Peaufiner dont le texte est une DATE (« mercredi 14 » figé le 2 oct., « jeudi 15 » le 3) : valeurs identiques dans l'app et dans l'état d'avant le lot — la référence suit le calendrier, pas le produit.

- **v122 (3 oct.)** — **Les couleurs.** `serveur.py` (Cache-Control: no-store ; `/version.json`, le commit affiché dans `?mesure=1`) : Safari gardait les fichiers « à l'heuristique », d'où les couleurs d'une autre version sur l'iPhone. Écran rendu = v118, sauf les décisions : en sombre, « à tenir » en crème dès la première image (fiche et cartes, Q290 ; Q374 tranchée : deux propriétaires, la crème posée à la source). **Orange de Ma Parole !** isolé : `--orange-maparole` (#FB4C0D, #FF7A55 sur les corps sombres de Peaufiner), lu par `#murPhrase .mp` seul. **Aura** : −11 / −15 / −12 / −12 pt. Juges neufs : `redteam_decisions.py` (79), `redteam_maparole.py`, `redteam_flash_etat.py` ; `redteam_couleurs_ref` (E6), `redteam_halo` (cotes). Planches : `planche-v122/`. Q375, Q376 ouvertes.

- **v123 (3 oct.)** — **La Pelote** : densité 3 et halo 3 retenus (constantes ; `?densite`, `?halo`, niveaux 4 et 5 retirés) ; **le corps** sous les poils = une autre teinte de la palette, tirée à chaque ouverture, ΔE00 ≥ 15 face au poil, jamais kaki (`redteam_corps.py`) ; **l'ombre en sombre** = ellipse crème (ΔE00 5,05), la flaque retirée. **L'Aura** remontée (−6 −6 −6 −6 −3) : les chiffres finissent à 833,5, entiers à 390 × 844. **Q375** corrigée (trois causes ; `redteam_flash_etat` 10/10). `redteam_couleurs_ref` : la mini-dalle était le juge (canevas nommés par le texte de leur ligne), 0 écart. `serveur.py` affiche l'adresse iPhone. Juges réécrits : `redteam_halo` (un niveau, 23), `redteam_plein`, `redteam_contour`. Planches : `planche-v123/`. Q377, Q378 ouvertes.

- **v124 (3 oct.)** — **L'Aura** encore remontée (−4 −4 −4 −4, la phrase à 20,4 px) : les chiffres finissent à 820, 24 pt d'air à 390 × 844. **« PARTAGER MA PELOTE »** en PromiLate 15 px, d'une couleur de la palette (≠ poils, ≠ corps, ≥ 3:1, jamais kaki ; `redteam_bouton.py`). **« Garder ta Toile »** en gras, teinte retirée à chaque retour sur les Réglages (≥ 4,5:1 ; `redteam_garder_toile.py`). **Tenir une parole est fluide** : la cause nommée (rendus de dalle, passes de tout le document), l'instant armé en capture, les dalles préparées, les passes remises après ; `redteam_fluide.py` 5/5 (la plus longue image 19,8 ms, avant 322). **Régulateur** : six paliers, jusqu'à 75 000 poils (Q378). Planches : `planche-v124/`. Q379–Q381 ouvertes.

- **v125 (3 oct.)** — **La Pelote passe à la carte graphique** (`peintGL`, WebGL 2 : les poils envoyés une fois, rotation + lumière + souffle sur la carte ; banc WebKit 141 → 17 ms p50, 7 → 58 images/s ; ΔE00 moyen 0,3 contre l'ancien rendu ; sous le doigt : 160 → 25–42 ms, Q383). `?mesure=1` ne couvre plus la Pelote (`redteam_mesure`). **La « double zone »** en sombre = le halo lui-même (deux épaules) : fondu du bas adouci, halo à la teinte du corps, flaque (code mort) retirée (`redteam_zone`). **Tirage** : jamais le même sol ni le même corps deux fois de suite, couleur rendue écartée de ΔE00 ≥ 14. **Textes de palette jamais à l'encre** (`_teinte.ajuste` : teinte OKLCH gardée). **Aura** : composition A appliquée (−10 · −8 · −8, 50 pt sous les chiffres), B et C par `?aura=` (Q384). **Onboarding** : mots Promi / Chiche / Cercle en couleur, écart 33, le concept sur la première diapositive (Q382). **Q379** : le travail d'après « tenir » en tâches découpées (77 → 22 ms). Liste des points de latence pour Swift dans QUESTIONS.md.

- **v126 (4 oct.)** — **`CHANTIERS.md`, le registre** (C-001…C-041, `redteam_registre`) ; l'ancien carnet devient `CARNET-CHANTIERS-ARCHIVE.md`. **Aura figée sur B** (cotes dans CLAUDE.md, `releve-aura` refigé : dette de 36 soldée, acquis 7 épinglé au souffle, `?aura=` retiré). **Onboarding** : le concept sur la dernière diapositive, dont le fond est un fragment de Toile posé par le moteur (voisines, 7 en attendant le choix). **La Toile vit au repos** : une ou deux dalles, 1 à 2 s, toutes les 5 à 15 s, douze mondes (huit immobiles : C-031) — `redteam_vivant`. **Le creux du doigt sur la carte graphique** : sous le doigt p95 20 à 25 ms au banc — `redteam_pelote_doigt`. **Geste de couleur du Studio rétabli au doigt** dans tous les sens (`touch-action:pan-y`) — `redteam_studio_geste` 22/22. **Ramage, l'onde ronde : déclencheur nommé (le disque de la pousse), NON corrigé** — `redteam_ramage_onde` rouge. Série de juges allégée (six sentinelles).
- **v127 (4 oct.)** — **Onboarding** : la dalle principale à sa place d'avant v126 (voisines = cellules vides dépliées et teintes, `Toile.voisines`), texte remplacé, tout en Gilbert, phrases à 20 px (C-006, C-043). **Ramage** : le disque de la pousse supprimé, la plume arrive d'un coup (C-009, `redteam_ramage_onde` réécrit, 9/9). **Vie au repos** : retour exact au pixel (`redteam_retour`, 105 mouvements), titre figé ; Éclisse et Madrure bougent, Bobinette réparé ; huit mondes immobiles (C-031 en cours). **Outil de dessin** : planche seule (C-042), exception à la loi des points inscrite.
- **v128 (4 oct.)** — **Loi des points** inscrite (C-044). **Onboarding** : texte d'avant v125 + les trois natures + « Le reste se trace. », voisines en cellules vides (C-006). **Outil de dessin** : planche en parcours, le dessin remplace la dalle, menu compact, « Dessiner » en tête (C-042). **Vie au repos** : cloche pleine (Houle, Éclisse 1 à 2 s), queue de convergence (Bobinette), quatre mouvements écrits dans le peintre — Chamade, Chantourné, Brouillamini, Mascaret (C-031) ; quatre mondes immobiles.
- **v129 (4 oct.)** — **Onboarding** : texte figé en quatre paragraphes, « Deuxio » penché de 3° (C-006). **« CERCLE » centré dans son encart** (C-046, `redteam_motmarque`). **Outil de dessin** : le mode dessin libère l'écran (planche, C-042). **C-031** reporté au portage Swift. **`redteam_couleurs_ref`** : canevas non peints comptés, plus comparés à rien (C-047). **Trait personnalisé** : concept (C-045, `TRAIT-PERSONNALISE-CONCEPT.md`).
- **v130 (5 oct.)** — **Trois récidives nommées et jugées** : les dalles seules sont ENGENDRÉES par le moteur, plus découpées dans la Toile (C-048, `redteam_decoupe` G2) ; la double zone de la Pelote après le Studio (C-002, canevas WebGL orphelin, `redteam_zone` C) ; les écrans suivent l'état réel (C-049, `window._paroles`, `redteam_reactif`). **Tropical Breeze `#8ACBE8`** : corps sombre d'un Promi, texte à l'encre (C-050). **Outil de dessin** : planche de la mise en page, rangée A, rien dans la bande (C-042). Q386–Q388.

## ⚑ À VALIDER SUR IPHONE — liste tenue à jour (ouverte en v123)

Sans iPhone, la preuve est faite au simulateur ou au banc (WebKit) ; l'item reste ici jusqu'à ce que Tom l'ait vu sur l'appareil.

| Depuis | Quoi | Preuve au banc | Ce que Tom regarde |
|---|---|---|---|
| v122 | Le cache : l'iPhone montre la dernière version | `serveur.py` (no-store), commit dans `?mesure=1` | la première ligne du relevé de l'Aura = le hash du rapport |
| v122 | Couleurs des fiches Promi, Chiche, Cercle, clair et sombre | `redteam_decisions` 79/79, `redteam_couleurs_ref` 0 | les fiches, la page +, l'Index |
| v122 | L'orange de « Ma Parole ! » seulement dans la phrase des murs | `redteam_maparole` 12/12 | toucher un réglage flouté de Peaufiner |
| v122 | Plus de flash orange à l'ouverture d'une fiche « à tenir » en sombre | `redteam_flash_etat` | ouvrir « faire les crêpes » en sombre |
| v123 | Pelote : densité 3 (220 000 poils) — fluidité, palier visé | banc : 31,8 ms/image, vise 150 000 (Q378 tranchée en v124) | `?mesure=1` : images/s et « le régulateur vise » — *remplacé par la ligne v125* |
| v123 | Pelote : le corps d'une autre teinte sous les poils ; les îles se lisent-elles ? (Q377) | `redteam_corps`, planche `pelote-densites-corps` | l'Aura, plusieurs ouvertures, deux palettes, clair et sombre |
| v123 | L'ombre crème en sombre | `redteam_halo` E : ΔE00 5,05 | l'Aura en sombre |
| v123 | L'Aura remontée : la ligne des chiffres visible sans défiler | cotes : fin à 833,5 / 844 à 390 × 844 | l'Aura à l'ouverture (⚠ un iPhone plus court que 844 pt la coupera) |
| v123 | La première image d'une fiche porte son état (Q375) | `redteam_flash_etat` 10/10 | ouvrir une fiche juste après une autre |
| v124 | **LE GESTE — tenir une parole : l'animation est-elle fluide ? (validation obligatoire)** | `redteam_fluide` 5/5 : aucune image > 20 ms de travail, p95 5,6 ms ; WebKit : la plus longue image 30–54 ms (562 avant) | tracer le trait d'une parole à tenir : le champ amande paraît sans temps mort, « juste après » une seconde plus tard ; rien ne se fige ensuite (Q379) |
| v124 | L'Aura : la ligne des chiffres avec 24 pt d'air, la phrase un point plus grande | cotes : fin à 820,0 / 844 | l'Aura à l'ouverture |
| v124 | « PARTAGER MA PELOTE » en PromiLate, d'une couleur de la palette | `redteam_bouton` | plusieurs ouvertures de l'Aura, deux palettes, deux thèmes |
| v124 | « Garder ta Toile » en gras, d'une couleur qui change à chaque retour (Q380) | `redteam_garder_toile` 29/29 | Réglages, tout en bas : y revenir plusieurs fois, en sombre et sous une palette vive — *remplacé par la ligne v125* |
| v124 | Le régulateur descend jusqu'à 75 000 poils si l'appareil ne tient pas | six paliers ; banc : vise 150 000 sur ce Mac | `?mesure=1` : « le régulateur vise », puis rouvrir l'Aura — *remplacé par la ligne v125* |
| v125 | **LA PELOTE SUR LA CARTE GRAPHIQUE — bloquant : ≥ 55 images/s ?** | banc WebKit : p50 17 ms, p95 20–22 ms, 58 images/s (7 avant) ; ΔE00 moyen 0,3 | `?mesure=1` sur l'Aura : la ligne « rendu : CARTE GRAPHIQUE », images/s, p50, p95 — et la Pelote à l'œil : un défaut de bord, de couleur, de scintillement ? — **mesuré par Tom (iPhone 16e) : p50 17 ms, p95 25 ms, 54–56 images/s ; reste son avis sur le rendu** |
| v125 | La Pelote SOUS LE DOIGT (Q383) : dessinée par la carte graphique, le contact calculé par le processeur | banc WebKit : 25–42 ms par image (156–175 avant) | poser le doigt sur la Pelote, la faire tourner, la caresser : fluide ? — *remplacé par la ligne v126* |
| v125 | La double zone derrière la Pelote, en sombre : disparue ? Le halo à la teinte du corps | `redteam_zone` 8/8 (30 ouvertures × 2 thèmes), `redteam_corps` 33/33 | l'Aura en sombre, dès l'ouverture, plusieurs ouvertures |
| v125 | La boule change visiblement à chaque ouverture (Q385) | ΔE00 14–17 (médiane) entre deux ouvertures, jamais deux fois le même sol ni le même corps | ouvrir l'Aura cinq fois de suite |
| v125 | « PARTAGER MA PELOTE » et « Garder ta Toile » jamais noirs | `redteam_bouton` 33/33, `redteam_garder_toile` 29/29 (26/29 avant) | Ingénu en clair : l'Aura et le bas des Réglages |
| v125 | L'Aura : choisir A, B (`?aura=B`) ou C (`?aura=C`) (Q384) | planches `aura-A|B|C` | les trois adresses sur l'iPhone — *remplacé par la ligne v126* |
| v125 | L'onboarding : mots en couleur, écart, le concept sur la première diapositive (Q382) | captures des 7 états × 2 thèmes | Réglages → revoir la présentation ; ou une fenêtre privée — *remplacé par la ligne v126* |
| v125 | Après « tenir » : un toucher n'est plus retenu (Q379) | `redteam_fluide` 6/6 : la plus longue tâche 22 ms (66–77 avant) | tenir une parole puis toucher aussitôt FERMER |
| v126 | **LA PELOTE SOUS LE DOIGT (C-029) — validation obligatoire** | banc WebKit : p50 17 ms, p95 20 à 25 ms sous le doigt (cible 22 : 3 passes sur 7) ; `redteam_pelote_doigt` | poser le doigt, faire tourner, caresser : fluide ? le creux est-il le même qu'avant ? |
| v126 | **LE GESTE DE COULEUR DU STUDIO (C-010)** | `redteam_studio_geste` 22/22 (au doigt, verticale et diagonale) | Studio : appui long sur la Toile, puis glisser vers le haut, le bas, en biais — la palette et la teinte suivent ; relâcher fixe |
| v126 | La Toile vit au repos (C-028) | `redteam_vivant` : une ou deux dalles, 1 à 2 s, toutes les 5 à 15 s | l'accueil, sans toucher, une minute — sous Pochade, Touffe, Braille… : est-ce « à peine » ? trop, pas assez ? |
| v126 | L'Aura, composition B figée (C-005) | `releve-aura` : cotes à 0,5 pt | l'Aura à l'ouverture |
| v126 | L'onboarding : le concept sur la dernière diapositive, le fragment de Toile (C-006) | planche A / B / C | revoir la présentation ; choisir 4, 7 ou 10 voisines (`?voisines=`) — *remplacé par la ligne v127* |
| v126 | Ramage : l'onde ronde (C-009) — OUVERT | `redteam_ramage_onde` rouge | *remplacé par la ligne v127* |
| v127 | L'onboarding, dernière diapositive (C-006, C-043) : la grande dalle revenue, sept voisines en couleur, le texte en Gilbert et aéré | cotes à l'image : 158,7 × 155,0 pt, 14 710 pt² (= v125) ; voisines 28–42 % ; planche `onboarding-fin` | une fenêtre privée (ou Réglages → revoir la présentation), en clair et en sombre |
| v127 | Ramage : plus de disque — la plume arrive d'un coup (C-009) | `redteam_ramage_onde` 9/9 (6/9 avec le film) | Studio sur Ramage, et planter une parole sous Ramage : l'apparition d'un coup est-elle acceptable ? |
| v127 | La vie au repos : retour exact, le titre ne bouge plus (C-028) ; Madrure, Éclisse et Bobinette bougent (C-031) | `redteam_retour` : 105 mouvements, 0 pixel ; planche `vie-au-repos-…` | l'accueil une minute sous Madrure, Éclisse, Bobinette : le mouvement se voit-il ? une couture au bord de la dalle ? |
| v127 | L'outil de dessin (C-042) : PLANCHE | `planche-v127/dessin-*` | *remplacé par la ligne v128* |
| v128 | L'onboarding, dernière diapositive (C-006) | planche `onboarding-fin` | *remplacé par la ligne v129 (voisines validées par Tom)* |
| v128 | La vie au repos sous Chamade, Chantourné, Brouillamini, Mascaret (C-031) ; Houle et Éclisse visibles 1 à 2 s (C-028) | `redteam_vivant`, `redteam_retour` ; planche `vie-au-repos-…` | l'accueil une minute sous chacun : « à peine » ? trop ? une couture au bord de la dalle ? |
| v128 | L'outil de dessin (C-042) : PLANCHE en parcours | `planche-v128/dessin-parcours-*` | *complété par la ligne v129* |
| v129 | L'onboarding : le texte figé, « Deuxio » penché de 3° (C-006) | `redteam_onboarding` 46/46 ; planche `planche-v129/onboarding-fin` | une fenêtre privée : le clin d'œil de « Deuxio » se voit-il juste assez ? |
| v129 | « CERCLE » centré dans son encart (C-046) | `redteam_motmarque` 4/4 | ouvrir un Cercle, puis un Promi et un Chiche |
| v129 | L'outil de dessin (C-042) : le mode dessin épuré — choisir la rangée (A, B, C), l'effilé (E1, E2), le symbole (S1, S2) | `planche-v129/dessin-epure-*` | les planches, version téléphone |
| v130 | Les dalles seules sous Buvard, Braille, Tesselle, Taille-douce, Houle (C-048) : contour réel, plus d'éclats des voisines | `redteam_decoupe` G2 | Studio sur Buvard puis une fiche de Cercle en sombre, l'Index, le Fil : les dalles ont leur vraie forme |
| v130 | La Pelote après deux ouvertures du Studio, en sombre (C-002) | `redteam_zone` 12/12 | Aura, Studio, Studio, Aura : un seul contour derrière la Pelote |
| v130 | Les écrans à jour tout de suite (C-049) | `redteam_reactif` 30/30 | tenir puis retirer une parole depuis la liste de l'Aura ; planter, puis l'Index et le Fil |
| v130 | Tropical Breeze, corps sombre d'un Promi (C-050) | `redteam_decisions` 81/81 ; planche `planche-v130/tropical-avant-apres` | fiche Promi et page + en sombre : la bande contre le corps (Q387), le Peaufiner, « Ma Parole ! » sur un mur (Q386) |
| v130 | L'outil de dessin (C-042) : la mise en page — choisir E1/E2, S1/S2, l'écart de 24 pt | `planche-v130/dessin-*` | les planches, version téléphone |
