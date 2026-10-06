# DETTE — ce que le prototype traîne, et ce qu'il faut décider avant de reconstruire

> Dossier de portage (C-021), écrit le 6 oct. 2026 sur l'état v134. **Lecture et extraction seulement.** Une ligne par élément,
> avec sa source et **ce qu'il faut décider**. Les comptes viennent des fichiers eux-mêmes (lus le 6 oct.), de `CLAUDE.md`,
> de `CHANTIERS.md` et de `QUESTIONS.md`. Ce qui n'a pas été trouvé : **⚠ TROU**.
>
> **Le principe qui règle la moitié de ce document** : l'app Swift est reconstruite de zéro. Une dette du prototype ne se
> porte pas ; elle ne coûte que si l'on recopie sans savoir. La colonne « À décider » dit donc, le plus souvent, *ne pas
> porter* — et nomme la règle qui, elle, se porte.

---

## A · Le code mort

| N° | Élément | Source | À décider |
|---|---|---|---|
| A-01 | **Le CSS : « 2 400 règles dont 54 % sont mortes »** ; l'ordre des 769 règles du dernier bloc est significatif, cinq tentatives de nettoyage ont échoué | CLAUDE.md §7, §9 | Rien à nettoyer : **aucune règle CSS ne se porte**. Le Swift part de `PROMI-TOKENS.json` et des cotes des documents de portage |
| A-02 | **`_dalleReelle`** (dans `sharePlanche`) : code mort, la case du Folio passe par `_poseDalle` (1 occurrence dans `app.html`) | CLAUDE.md v132, piège ② | Ne pas porter. La case du Folio = la dalle engendrée (C-048) |
| A-03 | **Éclats**, neuvième monde : « retiré du code » le 30 sept., absent du Studio depuis Q102 ; il reste 3 occurrences du mot dans `app.html` et 3 dans `promi-moteur.js` | CLAUDE.md §4 ; Q102 | Confirmer : vingt mondes, pas vingt et un. Ne rien porter d'Éclats |
| A-04 | **Le Zzz** : `COUPE=true` dans `lot-V118-ZZZ` (ni thème de nuit, ni cran de nuit) ; `BOUTON_POSE` (4 occurrences) ; `?zzz=1`, `?nuit=1` | CLAUDE.md v118, v120 ; C-012 ; Q369 | Tom : le Zzz revient-il au portage, et où tient son bouton ? Tant que non : ne pas porter (voir MANQUES) |
| A-05 | **`lot-V130-TROPICAL`** : la passe « texte à l'encre sur corps pastel » est COUPÉE depuis v131, « ses portes restent, inertes » (`e.corpsPastel`, `_tropicalSous`) | CLAUDE.md v130, v131 | Ne pas porter. Aucun corps pastel n'existe (corps sombre d'un Promi : `#0E78F2`, v134) |
| A-06 | **Les anciens chemins de saisie** (Q363) : l'ancien « à qui », la note par `#dpaJoint`, le champ visé par `#dpsCom`/`#dpsJoint`, le commentaire par `#dpbCom`, le pseudo de l'ancien onboarding — JS retiré en v118, **le CSS ne se nettoie pas** | CLAUDE.md v118 ; Q363 ; `redteam_clavier` | Ne pas porter. Trois champs restent exigés (voir `redteam_clavier`, `EXIGES`) |
| A-07 | **`#fToAll · onchange`** : « nœud disparu : code mort hors de Q363 — à retirer sur décision » | `joignable-dette.json` (source) ; Q372 ; C-040 | Ne pas porter |
| A-08 | **`ouvrirPersonne()` et `renderPerson()`** : gardes mortes, `openPerson` fait le travail | `joignable-dette.json` (source) | Ne pas porter ; une seule porte vers la fiche d'une personne |
| A-09 | **`promiDeconnexion()`, `promiConnexion`** : points de branchement vides, « voulus », en attente de Firebase | `joignable-dette.json` ; Q294 ; `app.html` l. 36509 | À brancher : voir MANQUES (Firebase) |
| A-10 | **`_flaquePelote` / `#auPeloteFlaque`** : déclarés « morts depuis v123, retirés » en v125 ; 3 occurrences de `_flaquePelote` restent dans `app.html`, et la liste blanche de `redteam_volume` les nomme encore, avec `_couronnePelote` (0 occurrence) | CLAUDE.md v123, v125 ; `redteam_volume` (`BLANCHE`) | Ne pas porter : en sombre l'ombre est une ellipse crème (v123). Nettoyer la liste blanche si le juge survit |
| A-11 | **L'ancien `buildAura`** : « `syncAll` appelait l'ancien `buildAura`, qui ne peint plus cet écran » (13 occurrences) | CLAUDE.md v130 (C-049) | Ne pas porter : un seul modèle observable (C-049) |
| A-12 | **`PROMI_DALLES`** : les images de dalles déposées au projet (un webp par monde, 6 occurrences) — famille F de `redteam_decoupe`, « jamais une photo » | CLAUDE.md §4 règle 1 ; `redteam_decoupe` | Ne pas porter, ne pas embarquer ces images |
| A-13 | **Le film de la pousse de Ramage** (`_ramFilmOn`, coupé par défaut, gardé « pour comparer ») | CLAUDE.md v127 ; C-009 | Tom : la plume qui arrive d'un coup est-elle acceptée (« à valider », QUESTIONS v127) ? Sinon, un vrai mouvement à écrire en natif |
| A-14 | **Les chemins témoins de performance** : `_peloteEmpCPU` (le contact par le processeur), `peint` (secours sans WebGL 2), `_perfAncien` (18 occurrences dans le moteur) | CLAUDE.md v125, v126 ; mémoire « perf v38 » | Ne pas porter : en Metal le contact est dans le shader (QUESTIONS v125, point 1) |
| A-15 | **Les passes « tout le document »** : lisibilité (`data-lis`), polices (`lot-POLICES`), plancher des tailles (`echelle()`), filets (`_filetsDisques`), `etatsDeCarte` — 13 à 50 ms après chaque toucher | CLAUDE.md §6, §7, v124 ; QUESTIONS v125, point 6 (« À NE PAS PORTER ») | Ne pas porter : chaque couleur et chaque taille se décide à la source, par les jetons |
| A-16 | **L'ancien chrome** `.topbar`, `.footer`, `.statusbar`, caché par une règle doublée dans `<head>` | CLAUDE.md §8 (v103) ; `redteam_flash` | Ne pas porter |
| A-17 | **L'ancien carrousel de la page +**, qui écoute encore le doigt sous l'écran des choix | CLAUDE.md §8 ; `redteam_tuiles` | Ne pas porter |
| A-18 | **L'ancien tiroir du partage** `#shTray` (`display:contents`) et son orphelin `#shNyPctRow` (« % d'harmonie ») | CLAUDE.md §8 ; Q149 (« rangé, à confirmer ») | Tom : « % d'harmonie » a-t-il une place dans le partage ? À défaut, ne pas porter |
| A-19 | **`#demoTg` et `#karmaCercle`**, masqués avec l'ancienne Aura | Q176 (« à confirmer ») | Ne pas porter, sauf avis contraire de Tom |
| A-20 | **L'ancien calque SVG de `render()`** et `promises[].x/y` (ce que rangeait Arranger, supprimé en v105) | CLAUDE.md §8, v105 | Ne pas porter : la position d'une dalle vient des graines du moteur |
| A-21 | **Les paramètres d'adresse retirés** : `?bleu=` (v134), `?aura=` (v126), `?halo`, `?densite` (v123), `?voisines` (v127) ; **restent** : `?mesure=1`, `?mesure=<monde>` | CLAUDE.md v123–v134 | Tom : faut-il un relevé de performance dans l'app Swift (C-027, « après le portage ») ? |
| A-22 | **Les clés internes aux anciens noms** : `nuee`, `NUE`, `curNuee` (un Cercle) ; `isPremium`, `ouvreCercle`, `.s2-cercle` (Ma Parole !) ; `encre`, `mosaique`, `pixel`, `terrazzo`, `gravure`, `sillons`, `cabochon` (Pochade, Tesselle, Buvard, Éclisse, Taille-douce, Houle, Halin) ; `signal` (Ingénu) | CLAUDE.md §2, §4 ; `RENOMMAGE-LEXIQUE.md` ; Q325 | Décider les identifiants Swift : au lexique d'aujourd'hui (recommandé par le renommage), avec une table de correspondance pour relire les juges |
| A-23 | **Les rangées de test des Réglages** : « Réinitialiser (test) · toile vide + 1 Cercle », et le jeu de démonstration (les Promi du moodboard) | `app.html` l. ≈ 2766 ; mémoire « jeu de la planche » | Ne pas livrer ; garder le jeu comme données de test (`banc_rendu` cherche ses paroles par TITRE) |
| A-24 | **Les parades propres au navigateur** : `lot-CLIC-FANTOME`, `touch-action`, le cache de Safari (`serveur.py`), le canevas WebGL orphelin, `MutationObserver` sur `.show` | CLAUDE.md §8, v122, v126, v130 | Sans objet en Swift. Garder les RÈGLES qui en sont nées (un test passe par le chemin de l'utilisateur ; toute porte se prouve au doigt) |
| A-25 | **Les juges périmés dans leur texte** : `redteam_polices` (docstring : Fraunces, Bricolage, Apfel), `redteam_ramage_onde` (« ROUGE »), `redteam_photo_menu` (ligne F), `redteam_plein` (trois paliers), `SPEC-JUGES.md` §2 (« 21 phrases ») | lus le 6 oct. | Corriger les textes avant de s'en servir comme source (hors de ce lot : lecture seule) |
| A-26 | **`AUDIT-POLICES.md`** : audit du 12 août (Apfel, Bricolage, Fraunces), antérieur aux trois polices | `AUDIT-POLICES.md` ; CLAUDE.md §6 (22 sept.) | Le tenir pour une archive ; la source des polices est CLAUDE.md §6 et `PROMI-TOKENS.json` |

**C-020** (« Code mort et faux positifs de `redteam_volume` », OUVERT) couvre A-10 et la section B-1.

---

## B · Les dettes nommées dans des fichiers

| N° | Fichier | Compte | Nature | À décider |
|---|---|---|---|---|
| B-01 | **`volume-dette.json`** | **290** occurrences (retrouvées 290, soldées 0 — série v134) | Par motif : `linear-gradient` 106 · `radial-gradient` 82 · `box-shadow` avec flou 39 · `repeating-linear-gradient` 21 · `drop-shadow` 13 · `text-shadow` 10 · `createLinearGradient` 7 · `shadowBlur` 6 · `createRadialGradient` 4 · `conic-gradient` 2. Par lieu : hors bloc 208 · `atelier-da` 33 · `lot-ACHAT-SANS-COMPTE` 20 · `lot-NEUF-POINTS` 7 · `lot15-bitonal-plus` 4 · `lot-V111-FILETS-CERCLE` 3 · dix autres blocs 14 · `promi-moteur.js` 1. Une part sont des MASQUES (`-webkit-mask-image:linear-gradient`), pas des volumes visibles | C-020. Pour Swift : **zéro dette** — la règle « la Pelote est le seul volume » s'applique dès la première ligne. Tom : les fondus de masque (bord d'une liste qui défile) sont-ils des volumes ? |
| B-02 | **`joignable-dette.json`** | **6** : 2 au rendu, 4 à la source | Rendu : le réglage LA COULEUR flouté du gratuit, deux fois (mur de Ma Parole !, « sans prise par décision », v104). Source : `#fToAll` (A-07), `promiDeconnexion` (A-09), deux gardes mortes (A-08) | C-040, Q372. En Swift : un mur n'est pas un défaut de joignabilité — le test l'exempte nommément |
| B-03 | **`decoupe-dette.json`** | **0** ligne (24 à la naissance, le 22 sept. ; soldée en v29, le 23 sept.) | Les découpes d'écran sont soldées ; `decoupe-releve.json` compte ce que le MOTEUR fait en lui-même (`getImageData` 1 715, découpes 605, `putImageData` 636) — hors du périmètre du juge jusqu'à G2 | Rien. En Swift : aucune découpe, moteur compris (C-048) |
| B-04 | **`kaki-coupables.json`** | **14** images coupables (sur 40 Toiles : 20 mondes × 2 thèmes) | De 0,8 % à 10,5 % de pixels kaki : Touffe clair 10,5 % · Guingois clair 7,6 % · Chantourné clair 7,4 % · Houle sombre 6,8 % · Chamade clair 6,0 % · Taille-douce sombre 5,8 % · Mascaret clair 5,4 % · Ramage clair 5,0 % · Braille sombre 3,3 % · Volubilis clair 2,4 % · Bobinette sombre 2,0 % · Touffe sombre 1,1 % · Pochade sombre 0,8 % · Éclisse sombre 0,8 %. ⚠ CLAUDE.md v115 et C-017 parlent de « 34 couleurs coupables » (`planche-sombre/kaki-coupables.png`) : deux comptes de deux natures | **C-017 (OUVERT)** : Tom a dit « on ne touche à aucune palette » (Q360). Décider avant le portage : la règle « jamais de kaki » vaut-elle pour le rendu Swift (les rampes des cellules vides, le fond), ou reste-t-elle une dette acceptée ? |
| B-05 | **`air-reference.json`** | **686** paires de textes, **68** écrans-thèmes | Une PHOTO des écarts de l'app (à l'encre), pas une décision ; 10 paires ne sont plus retrouvées (8 dates du Peaufiner, 2 du bouton de l'Aura renommé) ; les pertes d'air de v96 sont ASSUMÉES, avec leurs valeurs (CLAUDE.md v102) | **C-018 (OUVERT)**. Pour Swift : Tom valide les écrans, puis on fige une table d'écarts neuve ; celle-ci sert de point de départ |
| B-06 | **`design-reference.json`** | 6 configurations (clair / sombre × à tenir, tenue, Cercle), 17 à 25 cibles chacune | Photo des propriétés CSS calculées, figée le 30 sept. ; les couleurs n'y sont PAS comparées | Ne pas porter (voir TESTS, `releve-design`) |
| B-07 | **`releve-S5-instant`** | **13** écarts de dette | ⚠ TROU : la nature des 13 écarts n'est écrite ni dans CHANTIERS.md ni dans CLAUDE.md | **C-019 (OUVERT)** : les nommer avant de porter l'instant |
| B-08 | **`banc-rendu/ref/`** | 280 images | Refigé en v130 : les 60 images de dalles des cinq mondes à trame ont changé (la correction de C-048), les 220 autres sont au pixel | La référence du portage du moteur. Décider la tolérance natif / WebKit (voir TESTS, TROUS) |
| B-09 | **`joignable-inventaire.md`** | — | L'inventaire complet des éléments interactifs, écran par écran, écrit par le juge | À reprendre comme liste de contrôle des éléments joignables en Swift |

---

## C · Les faux positifs connus des juges

| N° | Juge | Le faux positif | Source | À décider |
|---|---|---|---|---|
| C-f01 | `redteam_toile` | « Mes Promi : les intitulés restent » oscille 14↔16/16 — il échantillonne un canevas animé | CLAUDE.md §7 ; C-024 | En Swift : horloge figée, comparer la composition |
| C-f02 | `redteam_geste` | « l'anneau est peint à sa nouvelle place » oscille 12↔13/13 ; deux échecs de suite ne suffisent pas | CLAUDE.md §7 ; C-024 | Comparer l'anneau à sa propre référence |
| C-f03 | `releve-aura` | Deux contrôles dépendent du tirage du sol : « sol hors des tons », « les dalles se noient » | C-024 ; Q297, Q182 | ⚠ Ce n'est pas un instrument qui flotte : c'est le PRODUIT qui tire au hasard (§7, 11 sept.). Tom : le plancher des îles (ΔE 15) doit-il être garanti par le tirage ? (C-013, Q377) |
| C-f04 | `redteam_couleurs_ref` | Canevas vide d'un seul côté (« ΔE 99 » face à rien) ; canevas nommé par son rang sur une liste qui défile ; dalle à 3,11 % (une rampe déclarée) | C-047 ; CLAUDE.md v123, v129, v131 | Corrigés dans le juge ; règles à garder pour tout comparateur |
| C-f05 | `redteam_volume` | Les masques en dégradé et les ombres d'avant la règle sont comptés (dette B-01) | C-020 | Voir B-01 |
| C-f06 | `redteam_kaki` | L'encre `#201908` est dans la plage de teinte du kaki (h 87°) ; un mélange sRGB y fait entrer une couleur qui n'y est pas (Touffe) | CLAUDE.md v114, v115, v124 | La règle juge les teintes TIRÉES et les dalles, pas une page ni un repli décidé |
| C-f07 | `redteam_fluide` | L'intervalle entre deux images, page au repos, donne déjà p95 18,3 ms et 26,7 ms au pire | CLAUDE.md v124 | Mesurer le TRAVAIL par image, sur appareil |
| C-f08 | `redteam_pelote_doigt` | La cible de 22 ms n'est tenue que 3 passes sur 7 : le banc plafonne à 19–20 ms sans rien peindre | CLAUDE.md v126 ; C-029 | Mesure sur iPhone (Tom : p95 25 ms sur iPhone 16e) |
| C-f09 | `redteam_origine` | Les cas à moins de 2 du seuil ΔE 15 ne sont pas jugés sur le choix origine / rampe | docstring du juge | Garder la marge |
| C-f10 | `redteam_vivant` | Mesuré à la naissance : une fois sur dix la dalle ne revenait pas exactement (corrigé en v127) ; sous Houle un intervalle de 25 s | CLAUDE.md v126, v127 | Houle : sa boucle tourne par image (voir E-02) |
| C-f11 | `redteam_nuit` | 33/34 avant la coupe : la ligne « premier lancement : Zzz activé » ne pouvait pas passer sans bouton | CLAUDE.md §7 | Voir A-04 |
| C-f12 | Toute la série | Lancées en parallèle, les batteries donnent des rouges FAUX (boîtes à 0 × 0, classes qui bavent) ; le simulateur ouvert fausse les mesures | CLAUDE.md §7 (20 août), §8 | En Swift : tests de mesure isolés, jamais en parallèle |
| C-f13 | Toute capture d'un nœud animé | Sort entièrement noire | CLAUDE.md §8 (12 sept.) | Mesurer les pixels, recapturer le conteneur |
| C-f14 | Les chantiers 75 et 73 de l'ancien carnet | Nés d'un instrument qui ralentit avec la machine (`setTimeout`, souris Playwright) | CLAUDE.md §8 (12 sept.) | Un geste s'injecte avec un horodatage par événement |

---

## D · Les rouges permanents et les défauts ouverts

| N° | Quoi | État | Source | À décider |
|---|---|---|---|---|
| D-01 | `redteam_nuit` | Rouge par décision : le Zzz est coupé | CLAUDE.md v120 ; C-012 | Voir A-04 |
| D-02 | `redteam_kaki` | Rouge de naissance | C-017 ; B-04 | Voir B-04 |
| D-03 | `releve-S5-instant` | 13 écarts | C-019 | Voir B-07 |
| D-04 | `redteam_air` | 10 paires non retrouvées | C-018 | Voir B-05 |
| D-05 | **La Toile sourde au doigt** sous certains mondes (Ramage) — BLOQUANT, **non reproduit** ; `redteam_toucher` 21/21 ; deux pistes non prouvées (`_fingers` resté > 0 ; seuil de 700 ms lu à l'heure de traitement) | OUVERT | C-058 ; Q396 | Tom : le chemin exact (monde, zoom, geste d'avant). En Swift : compter les doigts sur les événements du système, jamais sur un compteur à soi |
| D-06 | **Le bas des fiches en clair** : rien modifié, le défaut vu par Tom n'est pas identifié | OUVERT | C-059 ; Q397 | Une capture de Tom |
| D-07 | **Palettes vides vues au Studio** : pas reproduit ni mesuré | OUVERT | C-011 | Une capture ; (C-057 a corrigé un autre défaut du même menu — Q398 : est-ce celui-là ?) |
| D-08 | **Ramage** : la plume arrive d'un coup (27 % des pixels en une image) ; 5,5 s sur 500 paroles | Fait, à valider ; héritage | C-009 ; C-024 | Voir A-13 |
| D-09 | **Deux planchers de cadence assumés** pendant une plantation à 40 paroles : Chamade 51–52 images/s, Guingois 39–44 | Clos (« on n'y revient pas ») | Q341 | En natif : remesurer, ne pas reprendre le plancher comme une cible |
| D-10 | **Madrure** à surveiller sur un vrai iPhone ; construction 104 ms (×1), 483 ms (×4) | OUVERT | C-033 ; Q316, Q322 | Mesure Instruments au premier lot Toile |
| D-11 | **Le texte crème sur `#0E78F2` : 3,70:1** — les petites mentions sont sous 4,5:1 | Exception NOMMÉE, décidée par Tom | CLAUDE.md v134 | Rien : aucun test ne doit « corriger » ce texte. À signaler à la revue d'accessibilité de l'App Store |
| D-12 | **La phrase lilas de la page + sur `#0E78F2`** : 4,5:1 hors d'atteinte (le blanc pur fait 4,21:1) ; posée à `#F4EEFF` (3,71:1) | À valider | Q403 | Tom : `#F4EEFF`, `#FBF9FF` (4:1) ou la crème |
| D-13 | **Le trait « à tenir » `#DD4D23` sur `#0E78F2`** : Δlum 1,7, contraste 1,03:1 ; il se lit par la teinte seule (ΔE 126) | À savoir | Q404 ; Q216 | Tom, sur iPhone : se lit-il ? (daltonisme : aucun écart de clarté) |
| D-14 | **« Ma Parole ! » en `#FED0C3`** sur ce bleu : « un pêche très pâle » (un quart de la chroma de l'orange) | À voir sur iPhone | Q403 | Tom |
| D-15 | **Les usages de `#DD4D23` hors état** : « Supprimer mon compte » aux Réglages garde l'orange ; inventaire à faire | OUVERT | C-015 ; Q393 | Tom : une couleur de danger distincte, ou l'encre |
| D-16 | **Les îles ternies par le corps de la Pelote** | OUVERT | C-013 ; Q377 | Tom, sur iPhone |
| D-17 | **La Pelote sous le doigt** au bord de sa cible | Fait, en attente | C-029 | Mesure sur appareil |
| D-18 | **Un iPhone plus court que 844 pt coupe la ligne des chiffres de l'Aura** | Noté | ETAT-DES-LIEUX, liste « à valider sur iPhone » (v123) | Voir MANQUES (tailles d'écran) |
| D-19 | **Un prénom accentué tombe en Gilbert dans une phrase du trait en capitales** | Vu | Q291 | Voir MANQUES (polices) |
| D-20 | **`_teinte.ajuste` assombrit** dès que le fond dépasse 0,18 de luminance (le bleu : 0,20) — elle rendait `#621600` et `#1C0035` | Contourné : les deux dérivés sont des jetons calculés hors de l'app | CLAUDE.md v134 | En Swift : réécrire `ajuste` avec un sens (éclaircir / assombrir) explicite, et le tester sur ce bleu |

---

## E · Les incohérences assumées

| N° | L'incohérence | Décision | À décider pour Swift |
|---|---|---|---|
| E-01 | **Le semis par famille** : huit anciens mondes gardent le semis constant (≈ 68 cellules) tant qu'une cellule est vide ; les mondes neufs ont une Toile faite de ses seules paroles. Changer de famille au Studio ressème la Toile ; la rampe des îles de la Pelote dépend du semis en place | CLAUDE.md v34, v35, v98 ; Q318 | La reprendre telle quelle (aspect validé), ou unifier ? Une décision de Tom, pas du portage |
| E-02 | **Houle (`sillons`) reste PAR IMAGE** : tous les autres mondes suivent l'horloge ; elle s'étire sous charge, par décision | CLAUDE.md v61 ; `redteam_rythme` | À 120 Hz, « par image » double sa vitesse : fixer sa cadence de référence (≈ 30 images/s sur la page validée) ou la passer à l'horloge à vitesse égale |
| E-03 | **Quatre mondes immobiles au repos** : Volubilis, Guingois, Ramage, Esquille (huit en v126, quatre depuis v128) | CLAUDE.md v126–v129 ; C-031 (REPORTÉ au portage) | À écrire dans leur peintre natif : une ou deux dalles, 1 à 2 s, retour exact (A-INTEGRER) |
| E-04 | **Madrure a deux chemins** : la carte graphique, et un secours processeur (construction par tranches) quand WebGL refuse | CLAUDE.md v61 ; Q316, Q322 | En Metal : un seul chemin ? Quel repli sur un appareil lent (voir MANQUES, dégradation) |
| E-05 | **Tout suit le Studio, sauf l'Aura** : la Pelote et « Ce que tu as tenu » gardent le monde et la couleur de plantation | CLAUDE.md v34 | Porter telle quelle : le monde de plantation est une donnée de la parole |
| E-06 | **L'exception Ingénu** : sous la palette par défaut seulement, la couleur d'une dalle dit sa nature | CLAUDE.md §4 (21 sept.) ; Q292, Q297 | Porter telle quelle |
| E-07 | **L'onboarding en Gilbert, en minuscules** : exception à « Gilbert en capitales » ; « Deuxio » penché de 3° ; les mentions légales en 12 px restent en Atkinson | CLAUDE.md v127, v129 ; C-043 | Porter telle quelle |
| E-08 | **Le Studio garde ses flous** : seul écran dont les murs ne sont pas à 4,8 px | CLAUDE.md v104–v105 | Porter telle quelle |
| E-09 | **Les pertes d'air de v96** : écarts resserrés de 1,5 à 13 pt, assumés avec leurs valeurs | CLAUDE.md v102 | Reprendre les valeurs ; ne pas « corriger » |
| E-10 | **Le filet crème** : interdit partout, EXIGÉ sur la terre d'une fiche tenue | CLAUDE.md v113, v114 | Porter telle quelle |
| E-11 | **La loi des points** et son unique exception (le choix de taille du dessin) | CLAUDE.md §5 (v127, v128) ; C-044 | Porter telle quelle |
| E-12 | **« Zzz »** s'écrit ainsi même parmi des capitales ; **« Le studio »** n'est pas en capitales ; les **É** des titres sont composés du E de PromiLate et de son apostrophe | CLAUDE.md v118 ; Q319 | Voir MANQUES (polices) |
| E-13 | **Trois caractères viennent de la police du système** : `‹ ›`, `→` (et `✕ ✦ ●` depuis toujours) | CLAUDE.md §6 (22 sept.) | En Swift : des symboles SF ou des tracés à soi ? À décider (rendu différent d'un système à l'autre) |
| E-14 | **Les tolérances de rythme** : Ramage ± 33 %, Chantourné départ ± 33 %, Volubilis ± 15 % | Q342 ; `redteam_rythme` | Remesurer en natif avant de reprendre les tolérances |
| E-15 | **Les documents nomment « Nuée » ce que l'app affiche « Cercle »**, et « le Cercle » ce qu'elle affiche « Ma Parole ! » (blocs d'avant le 30 sept.) | CLAUDE.md, tête | Le dossier de portage écrit au lexique d'aujourd'hui |
| E-16 | **Le corps du Cercle sombre `#5D4978`** : « valeur posée par v113, pas une citation de Tom », puis « validé » (v123) | CLAUDE.md v122, v123 | Rien |
| E-17 | **L'achat d'un design** : « 2 € » dans l'app depuis v118 ; les blocs d'avant écrivent 1 € | CLAUDE.md v118 | 2 € |

---

## F · Les jetons déclarés sans consommateur

| N° | Jeton | Constat | À décider |
|---|---|---|---|
| F-01 | **`--t-titre-taille`, `--t-sous-titre-taille`, `--t-libelle-taille`** | Déclarés (1, 2 et 2 fois) ; **zéro `var()`** dans `app.html` (relu le 6 oct.). Les sept niveaux de `PROMI-TOKENS.json` ne sont pas câblés dans le prototype | **Câbler en Swift** : les sept niveaux deviennent les styles de texte de l'extension. ⚠ Les tailles RÉELLEMENT rendues ne sont pas celles du JSON (36 · 22 · 16 · 16 · 14 · 13 · 15) : le prototype rend 27 à 35 pour les titres, 43 · 36 · 33 · 28 · 24 par règles explicites, +12 % par `size-adjust` (v96). Tom : quelle table fait foi ? |
| F-02 | **Les 33 rôles `--p-*`** | Déclarés, aucun consommateur dans les règles — voulu : « c'est ce que le portage Swift emploie » | Les employer en Swift, **en vérifiant chacun** : le prototype peint par `--c-*` fixes, un rôle n'a jamais été éprouvé à l'écran |
| F-03 | **36 jetons `--c-*` sans `var()`** : `--c-bleu35` (`#335382`, mort pour le corps d'un Promi), `--c-seiche21`, `--c-orange59`, `--c-crete27`, `--c-bleu62`, `--c-mauve50`… | Relevé le 6 oct. (353 jetons déclarés, 69 sans consommateur `var()`, dont les 33 rôles) ; certains peuvent être lus en JavaScript | Ne porter dans l'extension Swift que les jetons employés |
| F-04 | **Les corps clairs `#CFE5FE` · `#FFF4FC` · `#EEE4F8`** | Dans le JSON (`corps-promi.clair`…), mais « ne peignent pas le corps » : le corps clair d'une fiche est la crème `#F7F0DE` | Corriger le JSON avant d'engendrer le Swift, sinon le rôle `corps-promi` est faux en clair |
| F-05 | **Des noms fossiles** : `--c-cobalt50` vaut `#0E78F2` (plus un cobalt) ; `--c-orange-maparole-cobalt` vaut `#FED0C3` ; `--c-lilas85` vaut `#F4EEFF` ; `--c-menthe*` pour l'amande ; `--c-framboise54` pour le rose | CLAUDE.md v131–v134 ; `PROMI-TOKENS.json` | Renommer par RÔLE dans l'extension Swift (`corpsPromiSombre`, `maParoleSurPromi`…) |
| F-06 | **`--c-tropical78`** | Cité par CLAUDE.md v130 ; absent du JSON et de `app.html` aujourd'hui | Rien (retiré) |
| F-07 | **Le vert `#00341A` « surface d'exception, déclarée, pas encore employée »** | Q217 (16 sept.) ; depuis, c'est la valeur de l'état « tenu » | Rien : c'est un état, pas une surface |

---

## G · Les questions ouvertes

### G-1 · Les chantiers non validés (`CHANTIERS.md`, état v134)

Compté par script le 6 oct. : 63 chantiers (C-001 à C-063) — 25 OUVERT, 3 EN COURS, 4 REPORTÉ, 31 FAIT EN ATTENTE DE TOM. **Aucun n'est à l'état « VALIDÉ PAR TOM » ni « ABANDONNÉ PAR TOM »** : les 63 lignes sont donc toutes non validées ; elles sont rangées par état.

**OUVERT (25)**

| N° | Objet | Décision attendue |
|---|---|---|
| C-011 | Palettes vides vues au Studio | Une capture ; reproduire |
| C-012 | Le Zzz à réintroduire | Revient-il, et où tient le bouton (Q369) |
| C-013 | Les îles ternies par le corps de la Pelote | Avis de Tom sur iPhone |
| C-014 | Les tests iPhone en attente | La liste « à valider sur iPhone » d'ETAT-DES-LIEUX.md |
| C-015 | Les usages de `#DD4D23` hors état | Inventaire, puis une couleur par usage |
| C-017 | `redteam_kaki`, rouge de naissance | Corriger les rampes, ou accepter la dette |
| C-018 | `redteam_air` et les dates | Refiger 10 paires |
| C-019 | `releve-S5`, 13 écarts | Les nommer, corriger ou refiger |
| C-020 | Code mort et faux positifs de `redteam_volume` | Solder la dette de 290 (sans objet en Swift) |
| C-023 | La page du trait partagé | Tout est à définir (MANQUES) |
| C-024 | Héritage : Fil en ligne de temps, visages, dalle floue de la page +, Ramage à 500 paroles, saison 2, contrôles intermittents | Ordre et périmètre |
| C-025 | Avant publication : PromiLate, Gilbert, pages légales, version | Juriste ; MANQUES |
| C-026 | Avant Swift : archive, VoiceOver de la Toile, StoreKit, Firebase | MANQUES |
| C-032 | Les quatre mondes neufs, gratuits ou payants | ⚠ Q314 est notée « TRANCHÉ » dans QUESTIONS.md (Esquille gratuit ; Bobinette, Ritournelle, Madrure payants) : le chantier reste « OUVERT » au registre — à refermer par Tom |
| C-033 | Le gel de Madrure ; Madrure sur un vrai iPhone | Mesure sur appareil |
| C-034 | L'écran qui vend et les mondes payants | ⚠ Q317 notée « TRANCHÉ ET FAIT » ; le texte dit aujourd'hui « Douze mondes de plus » — à refermer |
| C-035 | Les mots de l'achat sans compte | Valider les deux textes (Q326) |
| C-036 | Les compteurs | « À faire après les cinq mondes » (Q347) |
| C-037 | La palette noir et blanc au Studio | À faire (Q348) |
| C-038 | Les textes de l'aide de l'Aura | Valider les mots (Q350) |
| C-039 | La phrase du mur : « trop rapide » contre « 1,3 s validé » | Confirmer le temps de lecture 3–5,5 s (Q354) |
| C-040 | L'inventaire de joignabilité : la dette | Solder les 6 lignes (Q372) |
| C-041 | Anciennes questions à relire : Q284, Q289, Q301, Q357 | Les confirmer une par une |
| C-058 | La Toile ne répond plus au doigt (BLOQUANT) | Le chemin exact (Q396) |
| C-059 | Le bas des fiches en clair | Une capture (Q397) |

**EN COURS (3)**

| N° | Objet | Décision attendue |
|---|---|---|
| C-050 | Le corps sombre d'un Promi | **Décidé en v134 : `#0E78F2`, définitif** ; le registre dit encore « EN COURS » — reste Q403 (la phrase lilas) |
| C-060 | Le symbole du bouton photo | Tom choisit A (le feutre), B (la plume sur le cadre) ou C (le cadre et le trait) |
| C-062 | La diversité des tailles de dalles | Tom : que voit-il de monotone (Q402), puis un mécanisme |

**REPORTÉ (4)**

| N° | Objet | Reporté à |
|---|---|---|
| C-021 | Le dossier de portage | v134 (ce dossier) |
| C-022 | Vibrations et notifications | Une conversation dédiée (MANQUES) |
| C-027 | Après le portage : délier, le relevé | Après le portage |
| C-031 | La vie au repos des quatre mondes immobiles | Le portage Swift (E-03) |

**FAIT, EN ATTENTE DE TOM (31)** — chacun attend « validé » ou « à reprendre »

| N° | Objet | Ce que Tom regarde |
|---|---|---|
| C-001 | La Pelote sur la carte graphique | Le rendu (la fluidité est acquise) |
| C-002 | La double zone derrière la Pelote | En sombre, après deux ouvertures du Studio |
| C-003 | La teinte du corps change à chaque ouverture | Cinq ouvertures de l'Aura |
| C-004 | Les textes de palette jamais noirs | Ingénu en clair |
| C-005 | L'Aura, composition B figée | L'Aura à l'ouverture |
| C-006 | L'onboarding, dernière diapositive | Le texte figé, « Deuxio » à 3° |
| C-007 | Le travail remis après « tenir » | Tenir puis toucher FERMER |
| C-008 | Le relevé `?mesure=1` | — |
| C-009 | Ramage : l'onde ronde | La plume d'un coup : acceptable ? |
| C-010 | Le geste de couleur du Studio | Au doigt, dans tous les sens |
| C-016 | Le fond de la Toile en clair `#DFCAA4` | L'accueil en clair |
| C-028 | La Toile vit au repos | Une minute sans toucher : « à peine » ? |
| C-029 | Le creux sous le doigt | Caresser la Pelote |
| C-030 | La série de juges allégée | — |
| C-042 | L'outil de dessin | Le parcours au doigt (obligatoire) |
| C-043 | L'onboarding en Gilbert, aéré | La présentation |
| C-044 | La loi des points | — |
| C-045 | Le trait de validation personnalisé (concept) | Quatre décisions avant toute planche |
| C-046 | « CERCLE » centré dans son encart | Un Cercle, un Promi, un Chiche |
| C-047 | `redteam_couleurs_ref` : les 2 écarts | — |
| C-048 | Des captures de Toile à la place des dalles | Buvard, puis une fiche de Cercle en sombre |
| C-049 | Les écrans ne réagissent plus | Tenir, retirer, planter |
| C-051 | Voir une photo en entier | Une fiche avec photo |
| C-052 | « Ce que tu as tenu », complète | La plus récente en premier |
| C-053 | « SUPPRIMER CE PROMI » en crème | Peaufiner, en sombre et en clair (Q393) |
| C-054 | La phrase lilas éclaircie | Dépassée par v134 (Q403) |
| C-055 | Les phrases des murs extraites | — |
| C-056 | Sortir du dessin sans poser | Le ✕ |
| C-057 | Le menu des palettes du Studio | Est-ce le défaut vu (Q398) ? |
| C-061 | Les couleurs du dessin dans Ma Parole ! | Le mur du panneau COULEUR ; la ligne de l'offre (Q401) |
| C-063 | Les dix-huit phrases des murs | Dix-huit touches |

### G-2 · Les questions de `QUESTIONS.md` sans réponse écrite

Relevé par les mots « OUVERT », « OUVERTE », « À VALIDER », « à valider », « À TRANCHER », « À DÉCIDER », « À CHOISIR », « À CONFIRMER », « À REGARDER », en écartant chaque question qu'une ligne postérieure dit tranchée, validée ou close. **Les plus récentes d'abord.**

**Q386 à Q404 (lots v130 à v134) — toutes**

| N° | Objet | État | Décision attendue |
|---|---|---|---|
| Q386 | « Ma Parole ! » ne tient plus 3:1 sur Tropical Breeze | Close (v131) | — |
| Q387 | La bande contre le corps Tropical Breeze | Close (v131) | — |
| Q388 | « La liste de l'Aura est incomplète » | Close (v131 : toutes les tenues) | — |
| Q389 | Deux textes sous 4,5:1 sur le cobalt | Close (v132) | — |
| Q390 | « Ordre chronologique » : du plus ancien au plus récent | Close (v132 : la plus récente d'abord) | — |
| Q391 | Les disques s'effacent en mode dessin | Close (v132 : surface plein écran) | — |
| Q392 | Sortir du dessin sans poser | Tranchée (v133 : le ✕) | — |
| Q393 | « SUPPRIMER CE PROMI » à l'encre en clair ; les Réglages gardent l'orange | **À VALIDER** | Valider ; C-015 pour les Réglages |
| Q394 | Tailles de la gomme, fond par défaut, cinq fonds, dessin d'un Cercle hors partage | Validée (v133) | — |
| Q395 | Index et Fil gardent la dalle | Validée (v133) | — |
| Q396 | La Toile sourde au doigt, non reproduite | **OUVERTE** (C-058) | Le chemin exact |
| Q397 | Le bas des fiches en clair | **OUVERTE** (C-059) | Une capture |
| Q398 | La capture du Studio n'est pas arrivée | **OUVERTE** (C-057) | Est-ce le défaut corrigé ? |
| Q399 | Les dérivés suivent le bleu | Tranchée (v134) | — |
| Q400 | La rangée centrée coûte 12 pt à la surface de dessin (754 → 742) | **À VALIDER** (C-042) | Valider |
| Q401 | « Douze mondes de plus, les couleurs du dessin » sur deux lignes ; teintes floutées du mur du dessin | **À VALIDER** (C-061) | Valider |
| Q402 | Le coefficient de variation des tailles ne baisse pas | **OUVERTE** (C-062) | Ce que Tom voit de monotone |
| Q403 | La phrase lilas ne peut pas atteindre 4,5:1 sur `#0E78F2` | **À VALIDER** (C-050) | `#F4EEFF`, `#FBF9FF` ou la crème ; « Ma Parole ! » en `#FED0C3` |
| Q404 | Le trait « à tenir » sans écart de clarté sur `#0E78F2` | **À SAVOIR** | Voir sur iPhone |

**Q357 à Q385 (lots v111 à v125)**

| N° | Objet | État | Décision attendue |
|---|---|---|---|
| Q357 | Le mode sombre : fond de Toile, cellules vides, encarts — sept familles | À CHOISIR ; la seiche (v116) y répond pour le fond ; C-041 | Confirmer que v116 clôt la question, encarts compris |
| Q369 | Le bouton « Zzz » ne tient pas dans la ligne | À DÉCIDER (C-012) | Écarter les paires (84) ou une autre place |
| Q371 | La respiration : les chiffres de l'iPhone | À DÉCIDER ; dépassée par la carte graphique (v125 : « la respiration n'ajoute rien ») | À refermer |
| Q372 | L'inventaire de joignabilité : la dette | À DÉCIDER (C-040) | Solder |
| Q377 | Ce que le corps de la Pelote change aux îles | À REGARDER sur iPhone (C-013) | Avis de Tom |
| Q378 | À 220 000 poils ce Mac ne tient pas 60 images/s | Tranchée (v124 : six paliers) ; iPhone 16e : 54–56 images/s | — |
| Q385 | Le corps ne se voit jamais seul (un tiers de la couleur) | À VALIDER (C-003) | Veut-on VOIR le corps ? Une décision de dessin |

**Q284 à Q354**

| N° | Objet | État | Décision attendue |
|---|---|---|---|
| Q284 | On ne partage plus son Noyau ; trois libellés du partage | À choisir ; C-041 | Confirmer (« Mon Folio » existe depuis) |
| Q289 | La Pelote dans « Ma Toile » : deux compositions | À choisir ; C-041 ; depuis : « jamais dans Ma Toile » (24 sept.) | À refermer |
| Q291 | Un prénom accentué tombe en Gilbert dans une phrase du trait | Vu | Voir MANQUES (PromiLate) |
| Q294 | Les mots neufs des Réglages ; le numéro de version « Promi · 0.16 » | À trancher | Voir MANQUES (version) |
| Q295 | Pour un juriste : chiffrement de l'App Store × CC BY-SA ; notre WOFF2 de Gilbert ; licence de PromiLate inconnue | Ouvert | Juriste (C-025) |
| Q301 | L'onboarding : ce que la planche propose | À trancher ; intégré depuis (v20, v125–v129) ; C-041 | À refermer |
| Q326 | Les mots de l'achat sans compte | À valider (C-035) | Valider les deux textes |
| Q332 | Volubilis : description, transition en fondu | À valider (C-024) | Valider |
| Q333 | Guingois : description, une dalle d'un seul tenant | À valider | Valider |
| Q334 | Chantourné : description ; en clair sans promesse la soie est très pâle | À valider | Une rampe claire propre, ou laisser |
| Q335 | Mascaret : description ; le toucher par l'enveloppe des traits | À valider | Valider |
| Q336 | Ramage : description ; l'œil, le croissant | À valider | Valider |
| Q343 | La ligne du membre dans les Réglages | Tranchée : « À PRÉVOIR », avec Firebase | Voir MANQUES |
| Q347 | Les compteurs | « À faire après les cinq mondes » (C-036) | Périmètre |
| Q348 | La palette noir et blanc au Studio | À faire (C-037) | Périmètre |
| Q350 | Les textes de l'aide de l'Aura | Mots à valider (C-038) | Valider |
| Q354 | La phrase du mur : le temps de lecture | Choix fait, à confirmer (C-039) | Confirmer 1,4 s + 60 ms par caractère, 3–5,5 s |

**Avant Q284 — questions restées sans clôture écrite** (anciennes ; la plupart sont probablement réglées par des lots ultérieurs — « à confirmer une par une, sans rien présumer », comme C-041)

| N° | Objet | Décision attendue |
|---|---|---|
| Q2 | Index et Fil : « ✕ Fermer » mord peut-être sur le titre | Sans objet depuis le plateau ; refermer |
| Q120 | Les mots neufs du Studio | Valider les mots |
| Q148 | « Comprendre ton Aura » ne tient pas à 27 px dans le plateau | Trancher la taille du titre de l'aide |
| Q149 | « % d'harmonie », orphelin de l'ancien partage | Confirmer qu'il sort (A-18) |
| Q151 | Le plateau défile sur trois écrans | Trancher : fixe partout ? |
| Q152 | Le plateau sur une fiche déroge à une phrase du §3 | Confirmer |
| Q153 | La croix SVG d'une fiche est masquée | Confirmer (ne pas porter) |
| Q155 bis | « LE TRAIT » ou « LE PINCEAU » comme libellé de rangée | Valider « LE TRAIT » |
| Q165 | L'Aura : les mots, à trancher d'un coup | Recouper avec Q350 |
| Q168 | Les îles prennent la vraie dalle du Promi | Valider |
| Q170 | Les vraies données de l'Aura : sept réglages au plus sobre | Valider (dont « Ce que tu as tenu » = mes Promi tenus) |
| Q172 | Le peigne tourne avec l'objet | Valider |
| Q173 | La rotation de repos : la valeur | Valider à l'œil ; ⚠ 100 s (juge) ou 120 s (CLAUDE.md) |
| Q174 | La pulpe : a = 0,40 | Confirmer |
| Q176 | `#demoTg`, `#karmaCercle` sortent | Confirmer (A-19) |
| Q204 | L'écran qui vend : une seule version | Confirmer |
| Q218 | Le nom d'un écran dans le plateau en casse naturelle | Dépassée par Q319 (capitales PromiLate) ; refermer |
| Q236 | Les couleurs de la Toile par défaut | Dépassée par Ingénu ; refermer |

---

## H · TROUS

- ⚠ TROU : **les 13 écarts de `releve-S5-instant`** (C-019) ne sont nommés nulle part.
- ⚠ TROU : **le compte du kaki** — `kaki-coupables.json` porte 14 images, CLAUDE.md v115 et C-017 disent « 34 couleurs coupables » : deux relevés, aucun ne renvoie à l'autre.
- ⚠ TROU : **la table des tailles de texte qui fait foi** — les sept niveaux du JSON ne sont pas câblés ; les tailles rendues sont dispersées dans des règles explicites, un plancher (`echelle()`) et un `size-adjust` de 112 %.
- ⚠ TROU : **le registre et QUESTIONS.md se contredisent sur C-032 / Q314 et C-034 / Q317** (ouverts d'un côté, tranchés de l'autre) ; et C-050 est « EN COURS » alors que v134 dit « définitif ».
- ⚠ TROU : **le compte des règles CSS** (« 2 400 dont 54 % mortes ») date d'août ; `redteam_tokens` parle de 3 292 déclarations de couleur ; aucun compte récent.
- ⚠ TROU : **les restes d'Éclats** (3 + 3 occurrences) n'ont pas été qualifiés (commentaires ou code vivant).
- ⚠ TROU : **Q1 à Q283** n'ont été balayées que par mots-clés ; une question ouverte rédigée sans l'un de ces mots n'apparaît pas ici.
