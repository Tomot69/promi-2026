# Lot v146 — notes de travail (pour le rapport ; à relire après une reprise)

## Fait
- Registre : C-117 validé ; C-119…C-135 inscrits (scratchpad/v146/registre_v146.py) ; C-127 = numéro sauté par le brief (Q497 à écrire).
- `PROMI_VERSION.lot = 'v146'`.
- Jeton `--c-orange-depart: #FB4C0D` (JSON + CSS + Swift `orangeDepart`) ; redteam_tokens 46/46. ⚠ `redteam_maparole` à remettre au niveau en §5 (l'hex existe maintenant sous deux jetons).
- **§1 C-122 FAIT** : `lot-GENS` — la zone `.ph-add` est un div ; `saOuvre/saValide/saDecor/saSuis` ; entrée invisible `#gnSaisie` dans `#device` ;
  `cfg.cle` par liste (ph-qui, ph-avec, nuee-neuve, pg-*, fi-*) ; clavier lu par `visualViewport` → ce qui défile défile, sinon `translate` sur `#device` ;
  CSS `lot-V146-AJOUT-css`. Cause du blocage : le toucher remplaçait la zone par un second encart plein (`.gn-barre`), focus avec `preventScroll`,
  et RIEN dans l'app ne lisait la hauteur du clavier → sur l'iPhone la ligne restait dessous.
  Juge `redteam_ajout_personne.py` 122/122 (27/102 sur sauvegardes/app-avant-v146.html). Planche `planche-v146/PLANCHE-1-ajout-personne.png`.
  `redteam_part` rejoué par le vrai chemin (plante_a réécrit : prénoms écrits dans la zone, + / Retour, trait) : 55/55.
  Juges remis au niveau : `redteam_gens` (38/38), `redteam_clavier` (4 champs) ; originaux `sauvegardes/*-avant-v146.py`. `redteam_ajouter` ✅.
  ⚠ redteam_gens et redteam_ajouter ont flotté une fois lancés à la suite (charge) : à repasser en fin de lot.
  À valider sur iPhone : le clavier réel (visualViewport), le « + » touché au doigt, la ligne qui remonte.

## À faire (ordre du brief)
§2 C-131 · §3 C-135 · §4 C-094 · §5 C-121 · §6 C-119 · §7 C-120 · §8 C-132/133 · §9 C-134 · §10 C-088 · §11 C-123/124 · §12 C-126 ·
§13 C-125 (agent a789b9eb49b7e6849 en fond) · §14 C-118 · §15 C-116/128 · §16 C-129 · §17 décisions · §18 C-112/C-102
- **§2 C-131** : juge `redteam_clair_sombre.py` (A bascule 20 mondes × 1/5/25/50 ; B ouverture ; C dalle seule ; D Studio ; E Partager ; tableau `planche-v146/clair-sombre.md`).
  Mesuré : l'app est IDENTIQUE (graines, poids, vue, carte du toucher, silhouette d'une dalle seule 1,0000). États `banc-etats/etat-1.json` et `etat-5.json` créés.
  Le moodboard H (statique, SVG) : 43 paires sombre/clair, tracés identiques dans les 43. La source du doute : MA page `promi-tenir-variantes.html` (v145) —
  `variantes/dalle-promi-clair.png` ≠ `dalle-promi-sombre.png` (deux sessions, deux paroles plantées au hasard). À CORRIGER en §14 : capturer clair ET sombre
  dans la MÊME session (une seule parole). Le juge complet tourne en fond → scratchpad/v146/cs_complet.log, sonde → cs_sonde.log.
- **§2 C-131 (suite) — LE VRAI DÉFAUT TROUVÉ** : `Toile.reGray` / `reGrayStudio` (moteur) retiraient AU HASARD le gris de chaque cellule vide à chaque bascule de thème.
  Preuve par l'image (N=5, aller-retour clair→sombre→clair) : v145 = 32–34 % des pixels changés sous Pochade, 33–39 % Tesselle, 8 % Touffe, 9,6 % Braille ; v146 = 0 %.
  Corrigé dans promi-moteur.js (`_grisRang`, chaque cellule garde son RANG ; `Toile_grisRangs` pour le juge). ⚠ banc_rendu à repasser (le sombre peut changer → refiger).
  Le juge : + F (image), + rang des gris, D réécrit (Studio vivant : on juge l'instant de la bascule), `pose_ferme`, `_vivantOff`. 7/7 à 25 ; preuve sur l'app+moteur d'avant : A, D, F rouges.
  Faux positifs écartés : 0,3 pt sous Tesselle/Éclisse = relâchement pas fini après un ressemis (pas le thème) ; Studio « différent » = aperçu vivant.
- **§3 C-135** : `prechauffe` (au repos : atlas, semis, ton, dalles, îles, carte), `chaud()`, `peintUne()`, `ouvre()` peint dans le geste, `viseGL()`. `_aura.pre()`. `?mesure=1` → `_mesureNote` (quoi:'aura').
  Avant (banc WebKit) : 1re ouverture 1,95–2,33 s ; réouvertures 0,80–0,93 s. Après : réouvertures 28–42 ms dans l'image de l'écran. La 1re : corrigée (abonnement `_paroles` tardif + palier) → À REMESURER AU CALME.
  Juge `redteam_aura_latence.py` (MAX 120 ms en dur). Étapes de préparation les plus longues ≈ 400 ms (carte), 240 (semis), 200 (atlas) : au repos seulement.
- **§5 C-121** croix du + en `--c-orange-depart` ; **§6 C-119** `#enrToile` retiré (lot-V140-ENREGISTRER : reste `_enr.icone/fichier`) ; **§7 C-120** noms `.acc-barre .dctrl .l` en `--c-bleu45-txt` (#022140) en clair seulement
  (sombre : 1,27:1 → gardé crème ; proposition #82AEF8 9,17:1 ; planche `planche-v146/PLANCHE-5-accueil.png`). CSS `lot-V146-ACCUEIL-css` (fin du fichier).
  `redteam_partage_toile` réécrit (original sauvegardé) : enregistrement par la page Partager (fichier PNG 2160×3840 à la feuille de partage ; téléchargement sinon). 9/10 sous charge (Touffe à revoir au calme : isolé = conforme).
- **§2 FINI** : redteam_clair_sombre 24/24 (complet). Tableau `planche-v146/clair-sombre.md`. Preuve : sonde (A, B rouges), version d'avant (A, D, F rouges ; F = 34 % Pochade).
- **§3 FINI** : redteam_aura_latence 11/11. Après : 1re ouverture Pelote à 108 ms du toucher (96 ms du clic), dans l'image où l'écran paraît ; 2e et 5e : 39 ms ; après une tenue (1,6 s) : 33 ms.
  Préparation au repos : total ≈ 1,0–1,2 s en 6 étapes, la plus longue 316–357 ms (carte) ; calme = 0,9 s sans toucher. `peintMoisson` passe après la 1re image.
  Pour comparer l'ancienne version : `zz-avant-v146.html` (copie à la racine de sauvegardes/app-avant-v146.html + moteur d'avant) — à SUPPRIMER avant le commit.
- **§13 C-125 (agent terminé)** : `variantes/trace-lettres.js` (API `TraceLettres.trace(cible, contenu, {cps, vitesse, depart, toutDeSuite, manuel, attributs})`), `variantes/trace-chemins-gilbert.js` (270 glyphes),
  `promi-trace-lettres.html`, `redteam_trace_lettres.py` 14/14 (sondes fondu/bloc → 10/14). PromiLate NON livré (chemins trop grossiers). Défauts restants au ralenti extrême : dents sur `g`, fente sur `é` départ bas,
  barres de `t`/`f` non tracées de gauche à droite, bosse au flanc du fût (`h n b d`). À ×1 une lettre dure ≈ 20 ms : on voit des lettres arriver une à une, le tracé se lit à partir de ×0,25.
  Contraintes : canevas frère de la cible (offsetParent), cible = texte seul, un `transform` sur un mot n'est pas suivi (« Deuxio » penché serait tracé droit). À RELIRE (captures scratchpad/v146/trace/) et À MONTRER À TOM AVANT de brancher.
- **§8 C-132 en cours** : CSS transformée (647 + 426 sélecteurs, 5 416 règles lues avant/après), bloc `lot-V146-FICHE-SOMBRE-css` (37 variables), `lot-V146-THEME` (`_ficheClair`, `_clairPour`, `_enSombre`),
  sites JS passés à `_ficheClair` (lot-S1B-geo ×5, lot-S5 ×3, lot-NUEE-PEAUFINER ×2, lot-PINCEAU, lot-V145-PARTS, lot-PHOTO, plateau `encreUn`, filet du trait). Outils : scratchpad/v146/p8_theme_css.py (rejouable), p8_vars.py, p8_js.py.
  Sauvegarde d'avant §8 : scratchpad/v146/app-avant-p8.html. Juge `redteam_fiches_theme.py` écrit (A identité, B fond du bas, C chevron). RESTE : écarts 0,2 % (à localiser), chevron orange (C-133, `data-depart` à déclarer), dalles du moteur en sombre, juges de couleur à remettre au niveau.
- **§8 C-132/C-133 FAIT (cœur)** : `redteam_fiches_theme.py` 81/81 (22/79 sur zz-avant-v146.html). + `lot-V146-FICHE` (enveloppe les poseurs sous `_enSombre`), chevron `dep` (6e argument) + `data-depart`,
  `_orangeDepart()`. La matière (dalle) jugée à part (elle respire : témoin clair/clair jusqu'à 0,16 %). Cadre du téléphone masqué (0,19 % sur le pourtour = la page, pas la fiche).
  RESTE §8 : remettre au niveau les juges de couleur (decisions, couleurs_ref, tonsurton, champ, air, murs, maparole, flash_etat, S1…), CLAUDE.md (« corps clair = crème » remplacé), planche pour Tom.
  Cartes de l'Index/Fil et instant « tenu » : chevron NON orange (on n'y trace rien) — à dire dans le rapport.

## 14 oct. — reprise après résumé
- §4 juge `redteam_guide.py` RÉÉCRIT (flaques) : 59/60 machine moyennement chargée ; seul rouge = cadence (jonction couverture→étape 15–21 ms).
  Corrigé : l'entourage (10 ms) précalculé avant la couverture (`preCible`), l'étape passe à l'image suivante ; le + : sansCible → image → preCible → image → étape.
  CADENCE À REMESURER AU CALME (`python3 redteam_guide.py --cadence`). Preuve sur zz-avant-v146 : 15 rouges sur 25 avant un goto en délai (charge).
- `redteam_decisions` remis au niveau de C-132 (original sauvegardé) : à repasser au calme. À vérifier : page + [light] corps rendu #050302 (la page + en clair n'a pas le corps cobalt ?).
- Série `serie_a.sh` ARRÊTÉE (charge 65–107 : l'autre session lance xctest + simulateur). Reste à passer : barre, joignable, volume, tokens, lexique, polices, filets, trait, gestes + tout le reste en fin de lot.
- §9 FAIT : lot-V146-PEAUFINER (garde de closeAll pendant un geste dans Peaufiner + 4 s, refus gardés avec pile, envoyés avec ?mesure=1 ; ouvreCercle → _cercleDessus ; sortie par glissement vers le bas, la fiche se découvre). Chemin de Tom NON reproduit au banc (à dire). redteam_peaufiner 19/19 ; 13/19 sur zz-avant.
- 29 commentaires recopiés devant les sélecteurs jumeaux retirés (6 107 car.) ; 5 414 règles (5 416 avant p8 : écarts expliqués).
- §10 FAIT (moteur) : Rrit borne les coulées de la Toile par RIT_CADRE [-0.015,0.105,1.015,0.848] (une parole seule est peinte) ; _ritPart(n) 0,10 jusqu'à 9 puis
  retrouve 0,34 à 19 ; vue Ritournelle s = 1 ; _bornes mb 0,21H sous Ritournelle (aucune graine sous la barre) ; _ecarte (0,42 écart) dans _semisFinal et relax
  (deux graines confondues dans un coin : une seule coulée, deux titres — défaut d'avant, mesuré). window._ritFormes publié. redteam_ritournelle RÉÉCRIT 63/63
  (original sauvegardé) ; sur zz-avant : D rouge (1 % à une parole), B rouge. Mesure d'avant (même chemin) : 3 à 40 % de chaque coulée visible.
  ⚠ banc_rendu Ritournelle à refiger (c'est la correction) ; redteam_toucher, redteam_deplace (Q496) à repasser.
- §11 FAIT : C-123 voisines (moteur : vt0/vf0, _voisF, _voisAnim, _voisPousse, voisinesEtat, voisinesBande ; app : depart 2500, pas 140 ; départ vif:true pas 85 ;
  Toile d'avant + dalle en vol retirées EN FLAQUES (retireFond) ; première parole plantée à place [0.42,0.74]). C-124 textes (lot-V146-ONB-css, bloc de fin
  réécrit, finPlace dessus/dessous, reste au toucher : découpe gauche→droite provisoire, ?trace=1 = TraceLettres). C-126 trace en #00341A (clair).
  redteam_onboarding_texte 42/42 ; 10 rouges sur zz-avant. ⚠ redteam_onb_sorties (texte de fin en dur), redteam_onboarding (O22 Deuxio) à remettre au niveau.
  ⚠ Les fondus de texte de l'onboarding (onbHaut .5 s) restent : à remplacer par le tracé (§13) quand Tom aura validé. QUESTIONS : phrase sous « La suite… ».
- §14 FAIT : lot-V146-MAREE (couche #tenirMaree, crible contourné en !important ; trait épaissi 12→46 pt puis nappe Flaques.Nappe descente 120+640 ms,
  remontée à 2 s à sa propre horloge, 560 ms ; ?mareeLent=4 ; l'état « referme » garde champ de nature, dalle 180×150, trait vert quand la marée est là).
  redteam_tenir 28/28 (clair/sombre × Promi/Chiche), 5 rouges sur zz-avant. Page des variantes : B et C retirées (original sauvegardé). Cercle : pas de geste tenir.
  ⚠ redteam_fluide (C-102) à rejouer au calme ; redteam_decisions/flash_etat/air touchés par l'instant à repasser.
- §15 FAIT : lot-V146-NOMS (_noms.court/date/lien, geste → openPerson) ; commentaires refaits (visage rond sans cerclage, nom 16 = texte 16, date sobre) ;
  kr-n des Noyaux (3 gabarits) ; liste des parts. redteam_noms 15/15 (nouveau), redteam_commentaires 28/28 (remis au niveau + F), redteam_part 55/55 (Q487).
- §16 FAIT : lot-V146-EMOJI (beforeinput, paste, input, saveState, localStorage prénom/mots du Cercle) ; redteam_emoji 11/11.
- §17 : Q486 (Cercle : avec = parts), Q487 (initiales sous parts tracées), Q496 (déplacement désactivé sous Ritournelle : _TIRE_NON ; redteam_deplace remis
  au niveau pour Ritournelle), ligne « Un mot… » du Cercle (lot-V146-CERCLE-MOT, promi_cercle_mots). CHANTIERS corrections à faire.
