# SPEC-ECRANS — chaque écran de Promi, pour le portage Swift

> Document d'extraction (6 oct. 2026, état du prototype à v134 — commit `ceac9ac` (v133) + les modifications de v134, non commitées au moment de l'écriture).
> **Rien n'est inventé.** Chaque affirmation porte sa source : `app.html:ligne`, un bloc `lot-…` de `app.html`, ou un document + section.
> Ce qui n'a pas été trouvé est écrit « ⚠ TROU ». Les cotes sont en **points sur 390 × 844**, origine en haut à gauche.
> Lexique : « Nuée » dans le code = **Cercle** à l'écran (masculin) ; l'offre payante = **Ma Parole !** (clés internes `ouvreCercle`, `#plusScreen`, `isPremium`, `.premium`).
> Ordre des sources en cas de doute : `ETAT-30-SEPTEMBRE-2026.md` → `PROMI-TOKENS.json` → `CONTRAT-MONDE.md` → `SPEC-JUGES.md` → `CLAUDE.md` (les blocs « ⚑ » les plus récents corrigent les plus anciens).
> Les couleurs ne sont citées ici que lorsqu'elles décident d'un état d'écran ; la table complète est dans `PROMI-TOKENS.json`.
> Tous les titres d'écran sont en **PromiLate, en capitales** (sauf « Le Studio ») — `lot-V35-TITRES-MAJ`, app.html:36702.

## Sommaire

0. [Règles communes à tous les écrans](#0)
1. [L'accueil — la Toile](#1)
2. [L'onboarding](#2)
3. [La page + (Promi, Chiche, Cercle)](#3)
4. [La fiche d'une parole (Promi, Chiche ; à tenir, en cours, tenue ; gardé de côté ; à photo ; avec dessin)](#4)
5. [L'instant de « tenir »](#5)
6. [Peaufiner (Promi, Chiche)](#6)
7. [La fiche d'un Cercle (fil, état défilé, « Planter dans le Cercle ») et son Peaufiner](#7)
8. [L'Index](#8)
9. [Le Fil](#9)
10. [L'Aura](#10)
11. [L'aide de l'Aura](#11)
12. [Le Studio](#12)
13. [Partager](#13)
14. [Les Réglages](#14)
15. [Notifications](#15)
16. [La langue](#16)
17. [La confidentialité (« Vie privée »)](#17)
18. [Légal — Conditions, Politique](#18)
19. [À propos](#19)
20. [L'offre Ma Parole ! (la page)](#20)
21. [Les murs de Ma Parole !](#21)
22. [La fiche d'une personne](#22)
23. [Le menu du bouton photo](#23)
24. [Le mode dessin](#24)
25. [Voir en entier](#25)
26. [Confirmations, « Annuler », toasts, bandeaux](#26)
27. [Récapitulatif des trous](#27)

---

<a id="0"></a>
## 0 · Règles communes à tous les écrans

**Sources** : CLAUDE.md §5 (« Les composants communs », « La grammaire des traits et des contours »), §8 ; ETAT-30-SEPTEMBRE-2026.md §8 ; `lot-PLATEAU-PARTOUT`, `lot-ENCART-HAUT`.

| Composant | Règle | Source |
|---|---|---|
| **Le plateau** (encart du haut) | x 24 · y 40 · 342 × 60 · trait 2 px couleur du corps · rayon 30. Porte le titre à gauche et « ✕ FERMER » à droite. Il ne défile jamais : le contenu qui défile COMMENCE sous lui et rogne. | CLAUDE §5 (tableau des contours), §8 (« un enfant absolu d'un conteneur qui défile défile ») |
| **« ✕ FERMER »** | en haut à droite, dans le plateau. Relevé : boîte 84 × 18 centrée en (296 ; 70) sur les écrans, 80 × 12 centrée en (298 ; 70) sur une fiche. | `joignable-inventaire.md` §C |
| **La barre Peaufiner** | 342 × 62, rayon 31, trait 2, en bas de chaque fiche et de la page + ; « Peaufiner » à gauche, rond Partager (46 × 46, icône seule) à droite. Zone de toucher relevée : 390 × 84 centrée en (195 ; 802), soit y 760 → 844 ; rond Partager centré en (343 ; 802). | CLAUDE §5 ; `joignable-inventaire.md` (`#dpdTog`, `.dpd-part`) ; `lot-BARRE-PEAUFINER` app.html:21526 |
| **Le geste** | zone de 390 × 118, toujours entière, jamais rognée ni superposée. Le trait est l'onde du produit (voir ci-dessous). | CLAUDE §5 ; `#tenirZone`, `#planterZone` 390 × 118 dans l'inventaire |
| **L'onde** | une seule formule : `y(t) = base − amp·0,34·t − amp·0,62·sin(2π·1,5·t)`, t = x/390. Amplitude **36** partout ; **16** quand un choix est ouvert sur la page + et sur un Cercle défilé ; loi propre de la carte d'Index (`amp = 13 × largeur/173`, période 1). Épaisseur du trait 10 ; points de rayon 4,5 tous les 18. | `lot-PINCEAU` app.html:24843 ; app.html:17100–17108 ; `lot-ONB-V20` app.html:36294 ; `lot-S4` app.html:18737 |
| **Grammaire des contours** | trait 2 px, couleur du corps, rayon = hauteur ÷ 2 jusqu'à **94,5** de haut, **30** au-delà. | CLAUDE §5 ; `lot-CERCLE-MUR` (`rayon()`, `SEUIL_PILULE`) app.html:31500 |
| **Un Noyau** (anneau) | trois arcs au plus : tenu `#00341A` · en cours `#291547` · à tenir `#DD4D23` ; jours de 3 px d'arc ; filet crème 1 px sur le seul bord extérieur quand il est posé sur du sombre. | CLAUDE §3 (22–23 sept.), §5 ; ETAT §8 |
| **Fermer** | `closeAll()` ferme feuilles et fiches ; rien ne survit (masques, styles en ligne, nœuds bâtis). **Le Studio, l'Aura et Partager ne perdent pas leur état « ouvert » de la même façon** (dans le prototype leur classe `.show` reste) : en Swift, ne rien accrocher à « l'écran vient de s'ouvrir » qu'on ne rejoue pas à chaque ouverture. | CLAUDE §8 |
| **Un toucher** | partout où le prototype lit un « toucher » lui-même : appui puis lever, moins de 10 px de déplacement, moins de 600 ms. | `lot-V104-MURS` app.html:37222 ; `lot-V131-ENTIER` app.html:37941 |
| **Changement d'écran** | une ouverture, une fermeture, une plantation **coupent** : rien ne paraît une fraction de seconde, pas de fondu d'entrée sur la page +. | CLAUDE §8 (v103) ; `redteam_flash.py` |
| **Thème** | premier lancement en **clair** ; le Zzz (mode nuit automatique) est **coupé** jusqu'à nouvel ordre. | `lot-ONB-V20` app.html:36604 ; CLAUDE §3 bloc v120 |

**Navigation générale** (toutes sources ci-dessous, écran par écran) :

```
accueil ── + ──► trois pilules ──► page + (Promi | Chiche | Cercle) ── tracer ──► accueil (dalle plantée)
   │  toucher une dalle ─► fiche d'une parole ── tracer ─► l'instant ─► fiche tenue
   │  toucher la dalle d'un Cercle ─► fiche d'un Cercle ──► page + (dans ce Cercle) / fiche d'une de ses paroles
   │  barre : STUDIO · AURA · [+] · INDEX · FIL
   │  plateau : « PROMI » ─► l'offre Ma Parole ! (gratuit seulement) · Partager · Réglages
   └─ Réglages ─► Ma Parole ! · Le Studio · Revoir la présentation · Notifications · Vie privée · Garder ta Toile · Légal · À propos
fiche ─► Peaufiner (barre) · Partager (rond) · bouton photo ─► menu (Dessiner · Importer une photo · La dalle d'origine…) · un Noyau ─► fiche d'une personne
Aura ─► aide (i) · Partager (Ma Pelote) · fiche d'une personne (un Noyau) · fiche d'une parole (une île, une dalle tenue)
```

---

<a id="1"></a>
## 1 · L'accueil — la Toile

**Nom à l'écran** : mot-marque « PROMI » (le « I » en couleur, il clignote). **Id interne** : `#device` / `#stage` / `#toileCv` (la Toile), `#accPlat` (plateau), `#accBarre` (barre), `#accChoix` (pilules), `#accRecadre`.

### Accès
- Écran de repos de l'app ; on y revient à chaque fermeture (`closeAll`).
- Mène à : fiche d'une parole, fiche d'un Cercle, Studio, Aura, Index, Fil, page +, Partager, Réglages, l'offre.

### Éléments (de haut en bas)
| Élément | Cotes | Détail | Source |
|---|---|---|---|
| La Toile (`#toileCv`) | 0 → 844, bord à bord, derrière tout | canevas du moteur (`promi-moteur.js`) ; toutes les dalles ; titres sur les dalles, effacés sous 48 px à l'écran | `joignable-inventaire.md` ; CLAUDE §3 bloc v98 |
| Plateau `#accPlat` | x 24 · y 40 · 342 × 60 · rayon 30 · trait 2 | fond et trait inversés selon le thème (clair : fond crème, trait encre) | `lot-V95-ACCUEIL-css` app.html:36856 |
| — mot-marque « PROMI » | gauche 26 dans le plateau, haut 13,5 ; PromiLate 27 px | porte vers l'offre (rôle bouton, « Ma Parole ! » pour VoiceOver) — **retirée quand on est Membre** | `lot-ACCUEIL-css` app.html:32817 ; `lot-V12-js` app.html:34690 ; `lot-V74-CERCLE-PAYE` app.html:36787 |
| — Partager `#shareBtn` | rond 44, centre (284 ; 70) | icône seule (flèche montante dans un bac) | inventaire ; `lot-ACCUEIL` ICO.share |
| — Réglages `#settingsBtn` | rond 44, centre (334 ; 70) | icône seule (deux curseurs) | inventaire ; ICO.regl |
| (le compte « N paroles · N Cercles ») | — | **retiré de l'accueil** (v89 : `#accLigne{display:none}`) ; il reste sur l'Index | app.html:33769 |
| Bandeau « Garder ta Toile » `#accRappel` | x 24 · y 114 · 342 × 52 · rayon 26 | voir §26 ; n'apparaît qu'à certaines conditions | `lot-ONB-V20-css` app.html:36216 |
| Rond « recadrer » `#accRecadre` | 44 × 44, x 322 · y 660 | n'existe que si la main a déplacé la vue ; glyphe : trois dalles pleines | `lot-ZOOM-css` app.html:32982 ; `lot-V95-ACCUEIL-css` app.html:36876 |
| Les trois pilules `#accChoix` | bloc x 40 · y 476 · 310 × 210 ; chaque pilule 310 × 62, rayon 31, trait 2 ; hauts à 0 · 74 · 148 dans le bloc | de haut en bas : Cercle (fond `#C9A8F5`, texte `#291547`) · Chiche (fond `#FFB8D2`, texte encre) · Promi (fond `#82AEF8`, texte encre). Titre Gilbert 22 à gauche, sous-titre Atkinson 13 à droite | `lot-ACCUEIL-css` app.html:32852 ; `lot-ACCUEIL` app.html:32899 ; app.html:36875 |
| Barre `#accBarre` | x 24 · y 716 · 342 × 88 · rayon 44 · trait 2 | cinq entrées, centres en x : 70 · 124 · **195** · 266 · 320 ; y 760 | `lot-ACCUEIL-css` app.html:32825 ; `lot-V95-ACCUEIL-css` app.html:36870 ; inventaire |
| — STUDIO · AURA · INDEX · FIL | zone 90 × 51, icône 28 + libellé Atkinson 500, 12 px, capitales, interlettrage 0,06 em | | app.html:32827–32836, 36874 |
| — le **+** `#createBtn` | disque 68, centre (195 ; 760) | disque **bleu Promi** `#82AEF8`, croix à l'encre épaisse (5,6) ; son bord est un anneau à trois arcs (tenu · en cours · à tenir) qui **tourne lentement** (un tour en 48 s) ; le + ne tourne pas | `lot-ACCUEIL-css` app.html:32839–32850 ; `lot-V95-ACCUEIL-css` app.html:36851 |
| — pastille du Fil `#filDot` | 10 × 10 sur l'entrée FIL | « pas encore vu » | app.html:32837 |

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher une dalle (≤ 700 ms, ≤ 14 px) | ouvre la fiche de la parole **260 ms plus tard** (le temps de savoir s'il vient un second toucher) ; sur la dalle d'un Cercle : ouvre la fiche du Cercle | app.html:6750–6776 |
| Double toucher (2ᵉ à moins de 320 ms et de 30 px), n'importe où | ramène la vue au cadrage par défaut | app.html:6767–6770 |
| Pincer / glisser sur la Toile | zoome / déplace la vue ; le rond « recadrer » paraît | app.html:6723 ; `lot-ZOOM` app.html:32999 |
| Dézoomer loin | plateau, barre, pilules et rond s'effacent progressivement (zooms 0,88 → 0,74) puis ne prennent plus le doigt : on voit la Toile entière | `lot-ZOOM-V46` app.html:32992 |
| Toucher le rond « recadrer » | recadre, le rond disparaît | `lot-ZOOM` |
| Appui long sur la Toile | **rien** (l'ancien raccourci vers le Studio est retiré) | app.html:6735 |
| Toucher le **+** | ouvre les trois pilules **sur place** ; second toucher, ou toucher ailleurs : les referme | `lot-ACCUEIL` app.html:32950 |
| Toucher une pilule | ouvre la page + dans cette nature, **déjà composée** (jamais l'ancien écran des tuiles au passage) | `lot-ACCUEIL` app.html:32923 |
| STUDIO / AURA / INDEX / FIL | ouvrent ces écrans | `lot-ACCUEIL` app.html:32880 |
| « PROMI » | ouvre l'offre Ma Parole ! (gratuit) ; rien si Membre | `lot-V12-js`, `lot-V74-CERCLE-PAYE` |
| La Toile au repos | toutes les 5 à 15 s, une dalle (70 %) ou deux bougent 1 à 2 s puis reviennent **exactement** ; rien si un écran la couvre, en arrière-plan, sous « Réduire les animations », ou dans les 5 s d'un toucher. Seize mondes bougent ; **Volubilis, Guingois, Ramage, Esquille : à écrire en Swift** | CLAUDE §3 blocs v126–v128 ; `portage/A-INTEGRER.md` (C-031) |

### États vides et d'erreur
- **Toile sans parole** : la Toile garde son semis de graines vides (CLAUDE §3 bloc v34 : « seule la Toile SANS promesse garde le semis de graines »). Le bloc de texte d'origine (`#toileEmpty` : « Ta Toile n’attend que toi » / « Plante ton premier Promi — touche le + » / « chaque parole tenue devient une dalle ») **est masqué** (`.toile-empty{display:none!important}`, app.html:2075). ⚠ TROU : aucune décision écrite ne dit si ce texte doit revenir ; cherché `toileEmpty`, `te-t` dans app.html et CLAUDE.md.
- Après l'onboarding, la Toile porte toujours au moins la première parole.
- ⚠ C-058 (OUVERT) : « sous certains mondes la Toile ne répond plus au doigt » — non reproduit dans le prototype (`CHANTIERS.md`).

### Textes exacts
« PROMI » · « STUDIO » · « AURA » · « INDEX » · « FIL » · pilules : « Un Cercle » / « un groupe, un projet » · « Un Chiche » / « un défi lancé » · « Un Promi » / « à quelqu’un, ou à toi » · VoiceOver du rond : « recadrer » ; du mot-marque : « Ma Parole ! ».

### Sources
`lot-ACCUEIL-css`, `lot-ACCUEIL` (app.html:32809–32981) · `lot-V95-ACCUEIL-css` (36848) · `lot-ZOOM*` (32982–33014) · `lot-V12-js` (34690) · `lot-V74-CERCLE-PAYE` (36787) · app.html:6723–6776 · `redteam_accueil.py`, `redteam_zoom.py` (SPEC-JUGES.md).

### Trous
- Texte / dessin de la Toile vide (ci-dessus).
- Zoom mini / maxi de la Toile et cadrage par défaut selon le nombre de paroles : dans `promi-moteur.js`, non extraits ici (voir le document du moteur).

---

<a id="2"></a>
## 2 · L'onboarding

**Nom à l'écran** : aucun titre ; le mot-marque « Promi ». **Id interne** : `#promiOnb.onb-v20` > `#onbV` ; étapes `prenom` → `parole` → trait → fin → compte.

### Accès
- Au **premier lancement** (clé `promi_onb` absente) : thème clair, Toile **vide** (aucune donnée de démonstration).
- Rejeu : Réglages → « Revoir la présentation » (`obReplay`) : la Toile existante se tait le temps du rejeu, le prénom connu saute la première étape, et le panneau du compte n'est pas reproposé si le compte est fait.
- Pendant l'onboarding, plateau, barre, pilules et bandeau de l'accueil sont cachés ; la Toile **s'écarte** des éléments de l'onboarding.
- Sort vers : l'accueil, avec la première dalle plantée.
- Jamais de demande de notification, pas de tutoriel.

### Éléments et déroulé
| Étape | Élément | Cotes | Source |
|---|---|---|---|
| toutes | mot-marque « Promi » (le i en couleur) | x 24 · y 54 · PromiLate 29 | `lot-ONB-V20-css` app.html:36172 |
| 1 · prénom | la phrase : « Toi, c’est [ton prénom] ? » — Gilbert 700, 35 px, interligne 66 ; la pastille vide est en pointillé (3 px), remplie elle est pleine (fond encre du mode, texte inversé), curseur clignotant | x 24 · y 228 · largeur 342 | app.html:36174–36179, 36352 |
| 1 | bouton « → » (rond plein 52, VoiceOver « Suite ») | x 314 ; y = bas de la phrase + 14 ; **n'apparaît que si le prénom est rempli** | app.html:36182, 36362–36367 |
| 2 · parole | ligne du haut : « {Prénom}, donc. » (Gilbert 700, 16 px) | x 24 · y 176 | app.html:36173, 36385 |
| 2 | la phrase : pastille-verbe bleue « Je me promets » + « de » / « d’ » (élision selon le premier mot tapé) + pastille de la parole (exemple en pointillé : « ne plus dire “je commence lundi” ») | x 24 · y 228 | app.html:36293, 36355 |
| 2 | sous la phrase : « Petite ou grande promesse, elle compte. » | bas de la phrase + 20 | app.html:36322, 36361 |
| 2 | bouton « → » : visible si la parole est remplie **et** le champ a le focus ; il retire le clavier | sous la ligne précédente + 16 | app.html:36365 |
| 3 · trait | mot « TRACE POUR PLANTER » (PromiLate 15, capitales) | x 82 · y 556 | app.html:36184, 36324 |
| 3 | le trait : zone 390 × 118 à y **590** ; onde base 70 (dans la zone), amplitude 36 ; au repos : amorce effilée, chevron à x ≈ 43, puis points ; **paraît dès que la parole n'est pas vide** | y 590 → 708 | app.html:36292, 36325, 36396–36410 |
| 4 · la dalle | la dalle naît sous le doigt au milieu du trait (échelle 0,08 → 0,85 en 0,5 s), le haut s'efface à 650 ms, la dalle vole vers sa place sur la Toile (0,9 s à partir de 950 ms) | — | app.html:36478–36488 |
| 5 · dernière diapositive (à 1 900 ms) | quatre paragraphes (texte figé ci-dessous) ; bloc x 24, largeur 342, posé à y **150** si la dalle est dans la moitié basse, sinon à **620** (remonté pour ne jamais dépasser 816) ; « C’est planté. » Gilbert 700 35/44 ; les suivants Gilbert 700 16/23 ; 33 sous le premier, 20 entre les autres | — | app.html:36189, 36236–36247, 36490–36495 |
| 5 | fond : la vraie Toile, avec la nouvelle dalle ; des cellules voisines **vides, non colorées** | — | CLAUDE §3 blocs v127–v128 |
| 6 · le compte | panneau `.onbv-compte` : x 24, à 24 du bas, largeur 342, rayon 30, trait 2 ; il monte du bas (0,45 s) | — | app.html:36198–36206, 36510 |

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher la phrase / la pastille | donne le focus au champ (clavier) ; prénom : 24 caractères max, capitale aux mots ; parole : 80 caractères max | app.html:36336–36341 |
| Entrée au clavier, ou « → » | étape suivante (prénom → parole) ; à l'étape parole : retire le clavier | app.html:36331, 36371 |
| **Tracer** : poser le doigt dans les 30 % gauches de la zone, à moins de 48 de l'onde, glisser vers la droite en restant à moins de 52 de l'onde | le trait plein suit le doigt ; arrivé au **milieu (x 195)** : la parole est plantée (à soi, « en cours ») | app.html:36412–36427 |
| Lâcher avant le milieu | le trait se retire en 300 ms, rien n'est planté | app.html:36428–36432 |
| Toucher l'écran sur la dernière diapositive | **pas avant 4 s** d'affichage ; ouvre le panneau du compte (ou termine, en rejeu avec compte fait) | app.html:36496–36505 |
| « Continuer avec Apple » / « Continuer avec Google » | note la demande (`promi_compte = demande-apple|google`), appelle `promiConnexion` (point de branchement Firebase), ferme, termine | app.html:36520–36528 |
| « Plus tard » | note `plus-tard`, ferme, termine | idem |

### États vides et d'erreur
- Prénom ou parole vide : « → » ne fait rien d'autre que redonner le focus.
- L'onboarding fermé par un autre que lui : l'accueil revient ; sur un vrai téléphone le jeu de démonstration ne revient jamais.

### Textes exacts
- Étape 1 : « Toi, c’est » · exemple « ton prénom » · «  ? ».
- Étape 2 : « {Prénom}, donc. » · « Je me promets » · « de » / « d’ » · exemple « ne plus dire “je commence lundi” » · « Petite ou grande promesse, elle compte. » · « trace pour planter » (affiché en capitales).
- **Dernière diapositive, mot pour mot (v129, texte FIGÉ)** :
  1. « C’est planté. »
  2. « Ton premier Promi, ta première dalle sur ta Toile. Plus qu’à le tenir. »
  3. « Primo, un Promi, c’est ta parole donnée. Deuxio, un Chiche, c’est un coup de culot. Tertio, un Cercle, c’est tout cela à la fois, mais à plusieurs. »
  4. « Le reste se découvre en traçant. La suite t’appartient. »
  - « Promi », « Chiche », « Cercle » prennent la couleur de leur nature (teinte gardée, clarté ajustée jusqu'à 5:1 sur le fond de la Toile vide) ; **« Deuxio » est le seul mot penché, de 3°** (même police, même graisse, même couleur).
- Le compte : « Garder ta Toile » · « Pour la retrouver sur un autre téléphone. » · « Continuer avec Apple » · « Continuer avec Google » · « Plus tard » · « En continuant, tu acceptes les Conditions et la Politique de confidentialité. »
- Règle d'élision (« de » → « d’ ») : devant voyelle, h muet, « y » et « en » ; « de » devant h aspiré (hurler, haïr, hausser, heurter, hisser, hâter, harceler, hacher, hanter, héler), y consonne, onze, onzième, oui, un chiffre ; pastille vide : « de ». Un seul propriétaire : `_promiElide`.

### Sources
`lot-ONB-V20-css` (app.html:36162) · `lot-V125-ONB-css` (36231) · `lot-ONB-ECART` (36249) · `lot-ONB-V20` (36260–36678) · CLAUDE §3 blocs v125–v129 · `redteam_onboarding.py`.

### Trous
- Le texte « Conditions » et « Politique de confidentialité » du panneau du compte n'ouvre rien dans le prototype (simples soulignés) ; les pages légales elles-mêmes sont « Bientôt disponible. » (§18).
- Le concept sur la **première** diapositive (v125, Q382) a été retiré en v126 : la fonction `concept(true)` existe encore mais n'est plus appelée.

---

<a id="3"></a>
## 3 · La page + (Promi, Chiche, Cercle)

**Nom à l'écran** : le mot-marque du plateau dit la nature : « PROMI », « CHICHE », « CERCLE ». **Id interne** : `#createSheet` (classes `pp`, `pp-promi|pp-chiche|pp-nuee`, `pp-ouvert` choix ouvert, `pp-cours` pendant le trait, `pp-garde` reprise d'un gardé de côté, `pp-peauf` Peaufiner ouvert, `pp-choix` ancien écran des tuiles).

### Accès
- Accueil : + puis une pilule.
- Fiche d'une personne : « + Planter un Promi » / « + Lancer un Chiche » (la personne est déjà choisie).
- Fiche d'un Cercle : « Planter dans le Cercle » (le Cercle est déjà choisi).
- Index : toucher un **gardé de côté** rouvre la page + sur lui.
- Sort vers : l'accueil (plantation, ou « garder de côté », ou ✕ FERMER).
- **L'ancien écran des trois tuiles** (« Qu’est-ce que tu promets ? » ; « Un Promi / une parole qu'on donne », « Un Chiche / tu oses le lancer », … « CHOISIR → ») n'est plus montré par aucun chemin du doigt (il reste atteint par un clic scripté). ⚠ Ne pas le porter sans décision.

### Éléments (de haut en bas)
| Élément | Cotes | Détail | Source |
|---|---|---|---|
| Le champ | de y 0 jusqu'à l'onde | couleur pleine de la **nature** (bleu / rose / lilas), jamais blanc ; la dalle d'ambiance dessus | CLAUDE §3 (« un champ blanc n'existe jamais ») ; app.html:17150 |
| Plateau | 24 / 40 / 342 × 60 | mot-marque de la nature + « FERMER » (boîte 83 × 34 centrée en (297 ; 70)) | inventaire ; app.html:17401 |
| La dalle de la page + | y 88 ; hauteur `dh = min(300, base − 112)`, largeur `min(320, 1,2 × dh)`, centrée | vraie dalle du moteur ; **teintée sur la rampe de sa nature** (Q30) ; à base 312 : 244 × 200 ; à base 280 : 204 × 168 | app.html:17109–17124 ; CLAUDE §4 (Q30) |
| Bouton photo | rond 34, x centre 349 ; y relevé 215 (Promi), 151 (Chiche), 183 (Cercle) | ouvre le menu (§23) : « Dessiner », puis l'import | inventaire ; `lot-V132-DESSIN` app.html:38302 |
| Le trait (`#planterZone` / `#planterZoneN`) | 390 × 118 ; centre y relevé 280 (Promi, 2 lignes), 216 (Chiche, 4 lignes), 248 (Cercle, 3 lignes) | onde `base`, amplitude 36 (16 si choix ouvert) ; au repos : amorce effilée, chevron, points ; matière = le pinceau choisi | inventaire ; app.html:17142 ; `lot-PINCEAU` |
| Le mot de trace `.pp-trace` | x 82 · y `boîte − 60` (boîte = base + amp + 60) ; choix ouvert : y 184 | voir Textes | app.html:17408–17436 |
| La phrase `#csPhrase` / `#nueePhrase` | x 24, largeur 342 ; relevé : verbe à y 420–480, objet à 492–549 (Promi) | Gilbert 700 ; taille 36 si ≤ 3 lignes, 34 à 4, 30 au-delà, **réduite tant qu'une ligne dépasse 342** (plus petite de l'estimation et de la mesure) ; interligne `⌊taille × 1,2⌋ + 24` ; part de 30 sur un choix ouvert. Le **verbe** est une pastille pleine (rayon 18), chaque **mot à remplir** une pastille ; vide = contour pointillé + exemple | app.html:17437–17470 ; CLAUDE §8 (§2.8, coefficient **0,44** avec Gilbert) |
| La consigne `.ph-hint` | sous la phrase, une ligne (approche −0,025 em) | Promi : « **{verbe}** se retourne — touche-le » ; Chiche : « un Chiche se lance, il ne se retourne pas » ; absente sur un Cercle, pendant le trait et sur un choix ouvert | app.html:5402–5405 ; `lot-V102-CONSIGNE-css` app.html:36879 |
| Le rail du pinceau `#csPinceauRail` | pastilles 78 × 44, pas de 88, première centrée à x 63 ; y relevé 707 (Promi) · 727 (Chiche) · 690 (Cercle) · 645 (gardé de côté) ; rangée qui **glisse** horizontalement | douze pinceaux (voir Textes) ; le choisi est plein | inventaire ; `lot-PINCEAU-data` app.html:24814 |
| « garder de côté » `.pp-garder` | x 24 · y 708 ; Gilbert 16, souligné, teinte de la nature | **n'apparaît que dès qu'un mot de la phrase est rempli** ; absent sur un choix ouvert, pendant le trait, et sur la reprise d'un gardé de côté déjà gardé | app.html:16732–16740, 13566, 13593 |
| Barre Peaufiner `#csBotBar` | y 760 → 844 (zone), pilule 342 × 62 | ouvre le Peaufiner de la page + | inventaire |

**La base du trait** (app.html:17100–17138, CLAUDE §4) : elle dépend du nombre de lignes de la phrase — **312** pour deux lignes, **280** pour trois, 32 de moins par ligne supplémentaire, plancher **196** (atteint sur un choix ouvert, base 196 / amplitude 16, et sur six lignes et plus). ⚠ TROU partiel : la formule exacte de `base` en fonction de `nl` n'a pas été relue ligne à ligne (`ecran()` de `lot-S3-page-plus`, app.html ≈ 17060–17100) ; les valeurs 312 / 280 / 196 sont, elles, écrites.

### La phrase, nature par nature (app.html:5237–5405, 13187–13197)
| Nature | Lignes (une par ligne) |
|---|---|
| **Promi à soi** (défaut) | [Je me promets ⇄] · de/d’ [exemple] |
| **Promi à quelqu'un** | [Je promets ⇄] · de/d’ [exemple] · à [qui ?] |
| **Promi demandé** | [Rachel,] (pastille avec visage ; vide : « Rachel ») · [promets-moi ⇄] (« promettez-moi » au pluriel) · de/d’ [exemple] |
| **Chiche** | à [qui ose ?] · [Chiche] (verbe fixe, sans ⇄ ; « chiche » en bas de casse quand un prénom le précède) · de/d’ [exemple] · avec [qui en est ?] |
| **Cercle** | [Je lance un Cercle] (verbe fixe) · nommé [exemple de nom] · avec [tout le monde] (ou les membres séparés par « · », ou « Moi ») |

- Casse française : majuscule au premier mot de la phrase seulement.
- La virgule appartient à la pastille du prénom (« [Marion,] »).
- Le visage dans la pastille d'une personne : disque de la couleur de la nature, silhouette crème, 0,76 × la taille du texte.
- L'échéance et « dans un Cercle » ne sont **pas** dans la phrase : ils sont dans Peaufiner.

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher le verbe d'un Promi (⇄) | cycle : « Je me promets » → « Je promets … à … » → « promets-moi » → retour | app.html:5413–5420 |
| Toucher la pastille de l'objet | ouvre le **choix ouvert** : un champ de saisie (clavier ouvert dans le geste), invite = l'exemple courant (Chiche : « ce que tu n’as jamais osé lui lancer… ») ; la pastille suit la frappe, l'élision aussi, à chaque caractère | app.html:5461–5463, 5527–5552 |
| Toucher la pastille d'une personne (« qui ? », « qui ose ? », « qui en est ? », « avec ») | ouvre le choix des personnes : « Moi » en tête (dans un Cercle : « tout le monde » puis « Moi »), puis les personnes connues (initiale + prénom), puis sur sa propre ligne « + ajouter quelqu’un ». Toucher une personne l'ajoute ; sa croix la retire ; « + ajouter quelqu’un » ouvre un champ « un prénom… » avec les connus filtrés dessous. La liste défile dans son propre espace, le bouton reste dessous (16 d'air), au-dessus de la barre Peaufiner | `lot-GENS` app.html:32418–32480 ; CLAUDE §3 bloc v116 |
| Toucher « nommé » (Cercle) | champ « LE NOM DU CERCLE » ; Entrée ou sortie du champ valide | app.html:13201–13212 |
| Toucher un pinceau | le trait prend cette matière ; ce choix appartient à **cette** parole (`p.trait`) | `lot-PINCEAU` app.html:24850 |
| **Tracer** — Promi et Chiche : **sa moitié** (0 → 195) ; Cercle : **le trait entier** (0 → 390) | pendant le geste : le mot devient « continue → », la consigne et « garder de côté » disparaissent, le trait passe à la couleur « à tenir » ; à la fin : plantation, la page + **coupe**, retour à l'accueil, la dalle arrive sur la Toile avec l'animation de son monde | app.html:17420–17436, 17233–17240 ; CLAUDE §4 (« une Nuée se lance en traçant le trait entier ») ; CLAUDE §8 (v103) |
| Lâcher avant la fin | rien n'est planté | ⚠ seuil exact non relu (voir Trous) |
| « garder de côté » | garde le titre et la personne de la phrase, ferme, toast « gardé de côté — dans l'Index » | app.html:13595–13619 ; `redteam_garder.py` |
| Barre Peaufiner | ouvre le Peaufiner de la page + (ci-dessous) | app.html:17970 |
| « FERMER » | ferme sans rien garder | — |
| Après la plantation d'une parole **datée** | 1,9 s plus tard, sur l'accueil : la question « Je te le rappelle ? » (§15) | `lot-V109-NOTIFS` app.html:37370 |

### Le Peaufiner de la page + (`peaufBati`, app.html:17884–17966)
Tête : le titre tapé (sinon « Promi » / « Chiche » / « Cercle ») + « ✕ FERMER ». Puis, dans l'ordre :
- **Promi / Chiche** : « À QUI » (« À QUI JE LANCE » pour un Chiche ; absente pour un Promi à soi) · « AVEC » (Chiche ; vide : « personne », contour pointillé) · « AVANT » (la liste unique des échéances, §6) · « DANS UN CERCLE » (pas sur un Chiche) · « NOTE » (sous-ligne « privée — visible par toi seul » ou « visible par {X} ») · « PIÈCES JOINTES » (« N fichier(s) », sous-ligne « privées — visibles par toi seul » ou « visibles par {X} ») · puis **le mur de Ma Parole !** (les cinq réglages floutés, §6) en fin de liste.
- **Cercle** : « MEMBRES » (valeur : deux prénoms « · +N », ou « personne encore ») · « INVITER » (« → ») · « LES PROMI DU CERCLE » (« N Promi »).
- Pas de commentaires, de relance ni de suppression sur la page +.

### États vides et d'erreur
- Phrase vide : chaque pastille montre son exemple en pointillé ; le trait reste traçable.
- Cercle sans nom : toast « Donne un nom à ton Cercle », rien n'est lancé (app.html:3196).
- Cercle lancé avec des premiers Promi : toast « N Promi plantés » (app.html:3195).
- ⚠ TROU : ce que plante un Promi dont l'objet est resté vide (titre vide ? exemple ?) n'a pas été relu.

### Textes exacts
- Mots de trace : Promi au repos « trace ta part » ; Promi avec un choix ouvert « trace pour planter » ; Chiche et Cercle « trace pour lancer » ; reprise d'un gardé de côté « trace pour planter » (Promi) / « trace pour lancer » ; pendant le geste « continue → » ; une fois la moitié donnée : « À TENIR · {JOUR} » s'il y a une date, « UN JOUR » ou « EN L’AIR » sinon. (app.html:17408–17436, 17862–17867, 14474)
- Titres des panneaux de choix (présents dans le code, **non affichés** sur les trois cadres « choix ouvert ») : « À QUI », « TU PROMETS QUOI », « QUI TU DÉFIES », « QUI EN EST », « LE NOM DU CERCLE » (app.html:5449–5451, 16900).
- Pinceaux, dans l'ordre : **Plein · Coulé · Peigné · Sec** (libres) · Tressé · Frangé · Doublé · Fendu · Cranté · Vrillé · Semé · Perlé (à l'unité : la valeur s'écrit « {nom} — 0,50 € » dans Peaufiner). Descriptions : « le ruban franc, bord net » · « la plume charge et décharge, elle pose des gouttes » · « peigné de barres perpendiculaires » · « le feutre se rompt et s'amenuise » · « deux brins qui se croisent » · « le bas du trait s'effiloche » · « un second trait accompagne le premier » · « le trait s'ouvre en deux lèvres » · « des crans mordus dans le bord haut » · « le ruban se tord » · « le trait se disperse en grains » · « le trait se noue en perles ». (app.html:24814, 25238)
- **Les suggestions (exemples des pastilles vides)** — `lot-EXEMPLES-V20` (app.html:36024–36046), listes de Tom, mot pour mot. Règle : ouverture 1 → la phrase 1 ; ouverture 2 → la phrase 2 (Chiche : une seule fixe) ; ensuite tirage **sans remise** dans les suivantes, gardé d'une ouverture à l'autre ; un tirage par ouverture de la page +. Une phrase « A / B » porte sa variante plurielle (B).
  - **à soi** : me coucher le jour même · finir ce livre avant d’en ouvrir trois · arroser mes plantes avant qu’elles m’en veuillent · prendre des nouvelles avant d’avoir une raison · me garder une soirée pour moi · retourner voir cet endroit que j’ai adoré · commencer sans attendre le bon moment · m’engager pour cette cause · apprendre à jouer d’un instrument · planter quelque chose que je pourrai manger · réparer plutôt que racheter · laisser mon téléphone à la maison un dimanche · apprendre un truc par jour · apprendre à reconnaître les oiseaux · apprendre à repriser · m’offrir des fleurs · ranger · finir un stylo · apprendre à faire mon pain · voir ce tableau en vrai
  - **à quelqu'un (« je te promets »)** : t’emmener voir la mer / vous emmener voir la mer · te ramener quelque chose de là-bas / vous ramener quelque chose de là-bas · m’y mettre · t’écrire une vraie lettre / vous écrire une vraie lettre · te faire découvrir cet endroit / vous faire découvrir cet endroit · te fabriquer quelque chose / vous fabriquer quelque chose · te planter un arbre / vous planter un arbre · venir te chercher à la gare / venir vous chercher à la gare · venir te chercher après ton premier jour · te ramener vivant de cette idée · te donner un double des clefs, un jour / vous donner un double des clefs, un jour · m’acquitter des 23 centimes · régulariser la situation du Tupperware · honorer ma dette de trois frites · mettre un terme au dossier des cintres · rendre le tournevis avant 2030
  - **« promets-moi »** : m’écrire quand tu es chez toi / m’écrire quand vous êtes chez vous · me prévenir si j’ai du persil entre les dents · ne jamais parler comme sur Linkédine · me dire si je commence à dire « ça fait sens » · me dire si je commence à dire « disruptif » · me dire si je commence à parler de « synergies » · me donner ta recette, la vraie / me donner votre recette, la vraie · me rappeler cette histoire quand on sera vieux · m’envoyer une carte postale de là-bas · prendre cette sabbatique avec moi · me garder une chaise à ton procès / me garder une chaise à votre procès · aller voter · faire pipi assis · me montrer ton coin à champignons / me montrer votre coin à champignons · me donner une bouture de celle-là
  - **Chiche** : dire oui pour une fois · te baigner en janvier · te lever pour voir le soleil se lever · dormir à la belle étoile · choisir une ville au hasard · partir dans une heure · faire cette chose qu’on n’a jamais faite · nous faire confiance et voir où ça mène · dire oui sans demander pourquoi · faire le Mont Blanc · te mettre à la salsa · monter un groupe · prendre un cours de trapèze · courir notre premier marathon · apprendre une nouvelle langue · apprendre à jouer d’un instrument · faire un trek de plusieurs jours · apprendre à naviguer · y aller en stop · bivouaquer · monter notre festival · traverser un pays à pied · monter un refuge · aller courir maintenant · adopter un animal à la SPA · planter dix arbres · retaper cette baraque · restaurer ce vieux bateau · racheter le bar du village
  - **Cercle (le nom)** : Week-end à Marseille · La coloc · Le club de lecture · Le club de running · L’apéro qu’on repousse depuis mars · La maison qu’on veut construire · Notre tour du monde · La maison de campagne · Le projet qu’on mijote depuis deux ans · Le road trip des parkings de supermarché · Le road trip en Meuse · Le road trip des plus beaux ronds-points · Le road trip des zones pavillonnaires · Le road trip des sous-préfectures · Le road trip des ZAC · Le road trip des zones commerciales · Le road trip des aires de repos · Le mariage de Philippine et Pascal · Le mariage de Huguette et Jean-Roch · Le mariage de Blandine et Bruno-Stanislas · Le mariage de Nadine et Bernard-Guy · Le mariage de Monique et Didier-Régis · Le mariage de Chantal et Jean-Guy · Le mariage de Fabienne et Thierry-Alain · Le mariage de Corinne et Michel-Régis · Le mariage de Raymonde et Gérard-Yves · Le mariage de Gisèle et Rodolphe · Le mariage de Huguette et Mireille · Le mariage de Ginette et Gisèle · Le mariage de Jean-Roch et Jean-Guy · Le mariage de Didier-Régis et Rodolphe · Le mariage de Bruno-Stanislas et Pascal · Le mariage de Thierry-Alain et Bernard-Guy · Le mariage de Michel-Régis et Gérard-Yves · Le mariage de Jean-Noël et Alain-Gilbert · Le mariage de Guy · L’UTMB du dimanche · Le voyage aux 42 onglets ouverts · Le dîner des inconnus connus · La traversée des Pyrénées
- Mise en page des suggestions : marge droite = marge gauche, **retour à la ligne plutôt que réduction**, même mise en page à 390 et 375 (CLAUDE §7, `redteam_marges.py`).
- Sur le corps sombre d'un Promi (`#0E78F2`, v134), la phrase lilas de la page + est **`#F4EEFF`** (teinte gardée, portée au niveau de la crème : 3,71:1 — 4,5:1 est hors d'atteinte sur ce bleu ; Q403, à valider).

### Sources
`lot-S3-page-plus` (app.html:16440–18600) · app.html:5230–5700 (`_phraseRendu`, `_phraseChoix`) · app.html:13187 (`_nueePhraseRendu`) · `lot-GENS` (32418) · `lot-PINCEAU*` (24790–25445) · `lot-EXEMPLES-V20` (36016) · `lot-V102-CONSIGNE-css` (36879) · CLAUDE §3 blocs v115–v116, §4, §5, §8 · `redteam_tuiles.py`, `redteam_gens.py`, `redteam_suggestions.py`, `redteam_flash.py`.

### Trous
- Formule exacte de `base(nl)` (ci-dessus).
- Seuils du geste de plantation (largeur du couloir, point d'armement, validation) : le moteur du geste de la page + n'a pas été relu ; l'onboarding (§2) et la fiche (§4) donnent les leurs.
- L'achat d'un pinceau à 0,50 € : aucun parcours d'achat n'a été trouvé (cherché `0,50`, `pc-verrou`) ; l'inventaire ne montre que les quatre libres visibles sans glisser.
- Le contenu exact des réglages « INVITER » et « LES PROMI DU CERCLE » dépliés (champs d'origine `#nInvite`, `#nFirst` : « Les Promi du Cercle — on en plante autant qu'on veut, puis on lance », app.html:2588) n'a pas été relevé au rendu.

---

<a id="4"></a>
## 4 · La fiche d'une parole

**Nom à l'écran** : mot-marque « PROMI » ou « CHICHE ». **Id interne** : `#detailPoster` (classes `dp-promi`, `dp-chiche`, `f-atenir`, `f-encours`, `f-tenue`, `dp-draft`) ; la parole courante est `cur`.

### Accès
- Depuis : une dalle de l'accueil, une carte de l'Index, un bandeau du Fil, une ligne du fil d'un Cercle, une carte de la fiche d'une personne, une île ou une dalle tenue de l'Aura.
- Un **gardé de côté** ne s'ouvre pas en fiche : il rouvre la page + (app.html:13842).
- Mène à : Peaufiner (barre), Partager (rond), menu du bouton photo, fiche d'une personne (un Noyau), voir en entier (bande à photo ou à dessin), l'instant (le geste).

### Éléments (de haut en bas) — cotes de `ecran()` (app.html:14426–14585) et du poseur (14940–15070)
| Élément | Cotes | Détail |
|---|---|---|
| **La bande haute** (le champ) | y 0 → l'onde | couleur pleine de la **nature** (`#82AEF8` Promi, `#FFB8D2` Chiche), dans les deux thèmes, quel que soit l'état |
| Plateau | 24 / 40 / 342 × 60 | mot-marque de la nature ; « FERMER » avec une croix ; texte à l'encre sur le champ pastel |
| **La dalle** | y **124** ; `dh = min(300, (base − amp) − 124 − 12)` ; largeur `min(320, 1,2 × dh)` ; centrée | vraie dalle du moteur, rendue à sa taille finale, **teintée sur la rampe de la nature** (Q30) ; suit le monde et la palette du Studio (sauf « La dalle d'origine », §23) ; une **photo** ou un **dessin** la remplacent |
| Bouton photo | rond 34, centre x 349 ; y relevé 221 (à tenir, en cours, Chiche lancé), 331–335 (tenue) | VoiceOver « Photo » |
| **Le trait** (`#tenirZone`, 390 × 118) | onde `base` / amp 36 ; relevé : zone centrée y 303 pour base 286 | porte l'**état** ; modes : `moitie` (plein 0 → 195, chevron, points), `complet` (plein 0 → 390), `duo`, `points` (gardé de côté) ; matière = le pinceau de la parole |
| Le mot du geste `#dptTrace` | y `yTrace = ⌊yEncre + 25⌉`, centré ; `yEncre = base + 0,45·amp + 5` | seulement s'il reste quelque chose à tracer |
| **Les Noyaux** `#dAura` | x 24, y `yNoyau = yTrace + 44` (sans mot du geste : `yEncre + 27`) ; rangée de 342 | « toi » (78) puis les personnes concernées (58) avec leur prénom ; un Promi à soi n'a que « toi » ; relevé : un Noyau de personne = boîte 70 × 83 |
| **À qui** `#dptQui` | y `yQui = yNoyau + 128` (+ correction d'encre) ; Gilbert 23 (21 en duo) | un seul ton |
| **Le titre** `#dptTitre` | y `yTitre = yQui + quiFs × 1,10 + 11,9` (à l'encre) ; Gilbert **42**, réduit d'un point à la fois jusqu'à tenir sur une ligne (plancher 38) ; titre long : deux lignes, trois au plus (jusqu'à 24 px), puis points de suite | le texte tapé n'est jamais modifié |
| **La ligne d'état** `#dptQuand` | y `yTitre + hauteur du titre + 26,3` (+ jambage de la dernière ligne) ; 13,5 px, capitales | « TENUE » en amande `#8FE08F` |
| Zone de message `#dpCorps` | **en cours** : champ 342 × 66, rayon 33, contour 3, à `état + 13,5 × 1,1 + 28,25` ; **tenue avec note ou commentaire** : carte 342 × 76, rayon 22, à `titre + 23` ; **sinon : rien** (une fiche à tenir n'a pas de zone de message) | invite « écris un mot » (ou « répondre » s'il y a déjà un commentaire) ; en-tête « {AUTEUR}, {QUAND} » ou « TA NOTE » |
| Barre Peaufiner | y 760 → 844 | « Peaufiner » + rond Partager |

**Les cas** (app.html:14460–14500) :
| État | base | mode du trait | couleur du trait | couleur des libellés (à-qui, mot du geste, état) | mot du geste | mot d'état |
|---|---|---|---|---|---|---|
| **Promi en cours** | 286 | moitié | teinte sombre de la nature (`#022140`) | `#291547` en clair · crème en sombre | « trace pour tenir » | « EN COURS » |
| **Promi à tenir** (`status:'rate'`) | 286 | moitié | `#DD4D23` | `#DD4D23` en clair · crème en sombre | « trace pour tenir » | « À TENIR » (+ « · {JOUR} ») |
| **Promi tenue** | 400 (286 s'il y a une note ou un commentaire) | complet | crête `#0B4A2A` + filet crème dessous | crème ; état en amande | — | « TENUE » (+ « · {JOUR} ») |
| **Chiche lancé** | 286 | moitié | teinte sombre du Chiche (`#3D0F23`) | comme « en cours » | « {Prénom} tracera sa part si elle ose » | « LANCÉ » |
| **Chiche à relever** | 286 | moitié | `#DD4D23` | comme « à tenir » | « trace pour tenir » | « À RELEVER » |
| **Chiche tenu** | 400 / 286 | complet | crête | crème / amande | — | « TENUE » |
| **Chiche tenu à deux** (`avec`) | 396 | duo | crête | crème / amande | — | « TENU À DEUX » (+ « · 3 AOÛT ») |
| **Gardé de côté** (rendu de fiche, non atteint au doigt) | 286 | points | couleur de la nature | couleur de la nature | « trace pour planter » / « trace pour lancer » | — ; à-qui = « Gardé de côté » ; pas de Noyaux ; champ de la nature **sans matière** |

**Le corps (sous l'onde)** :
- clair : **crème `#F7F0DE`** pour les trois natures (CLAUDE §3, correction v122) ; texte à l'encre.
- sombre : Promi **`#0E78F2`, DÉFINITIF** (v134, décision Tom ; `#1A52F0`, `#273CEB`, `#8ACBE8`, `#335382` sont morts pour ce rôle) ; Chiche `#7C3F58` ; texte crème `#F7F0DE`. **Exception nommée** : sur le bleu d'un Promi le texte crème ne fait que 3,70:1 — par décision, aucune passe de lisibilité ne doit le repeindre. Le trait « à tenir » `#DD4D23` y a la clarté du corps : c'est sa teinte seule qui le sépare (ΔE 126).
- **tenue** : la **terre `#2B1020`** dans les deux thèmes ; texte crème, marques d'état en amande ; le filet crème sous le trait y est **exigé**.

**Rythme sous le trait** (app.html:14553–14557) : 26 d'encre entre deux blocs (trait, mot, disques, état, commentaires), 20 dans le bloc de la promesse (à-qui · titre), 30 sous le titre.

### Actions
| Geste | Effet | Source |
|---|---|---|
| **Tracer** sur le trait : poser le doigt dans la partie gauche (x ≤ 168), à n'importe quelle hauteur ; glisser vers la droite | la parole est **tenue** si, au lever : le doigt a franchi **les deux tiers** de la course (jugé sur x seulement), **ou** a parcouru plus de la moitié de la largeur, **ou** a tracé lentement (< 40 px/s pendant 300 ms) plus de six points. Le tracé réel est gardé (`p.trace`). Vibrations : 6 ms au départ, 12-40-26 à la réussite. Sinon tout se referme doucement, rien ne gronde | app.html:4690–4790 |
| Tenir | déclenche l'instant (§5) ; le Fil, l'Index, l'Aura se mettent à jour à l'image suivante | `lot-S5` ; `lot-V130-REACTIF` |
| Toucher la bande quand elle porte une **photo** ou un **dessin** | ouvre « voir en entier » (§25) ; une dalle n'ouvre rien | `lot-V131-ENTIER` |
| Toucher le bouton photo | menu (§23) | `lot-V117-PHOTO-MENU` |
| Toucher un Noyau de personne | fiche de cette personne (§22) | inventaire (`.kring«Rachel»`) ; `lot-CHEMINS-PERSONNE` |
| Toucher le champ de message (en cours) | ⚠ voir Trous | — |
| Toucher la barre Peaufiner | ouvre Peaufiner (§6) ; un second toucher le referme | `lot-S2-peaufiner` app.html:16378 |
| Toucher le rond Partager | Partager, réduit à cette parole (§13) — se lit sur le geste, pas sur un clic | `lot-V117-PARTAGE-FICHE` |
| « FERMER » | retour à l'écran d'où l'on vient (accueil) | — |

### Fiche **à photo**
- La photo remplace la dalle dans la bande ; elle reste **sous** le plateau (Q53) ; la matière ne remplit pas le champ (exclusion du §4 de CLAUDE.md).
- Toucher la bande l'ouvre en entier ; VoiceOver « Voir la photo en entier ».
- Le menu propose alors « Retirer la photo ».
- ⚠ TROU : le cadrage de la photo dans la bande (recadrage, alignement) n'a pas été relevé (`lot-PHOTO`, app.html:20041, non relu).

### Fiche **avec dessin** (v132)
- Le dessin **remplace** la dalle ou la photo : une couche pleine (le fond du dessin puis ses traits, à l'échelle 1, calée **en haut**), découpée à **7 pt au-dessus de l'axe du trait d'état** ; la fiche en montre le haut.
- Un bouton de masquage (œil, rond 34, trait 1) : x 24, à 52 pt au-dessus du trait ; pour soi seul, mémorisé par fiche ; **un dessin masqué n'est jamais emporté dans un partage** ; masquer fait revenir la dalle. VoiceOver « Masquer le dessin » / « Afficher le dessin ».
- Toucher la bande : « Voir le dessin en entier ».
- Sources : `lot-V132-DESSIN` app.html:38060–38140, paramètres `BANDE_RETRAIT` 7, `OEIL {x:24, ecart:52}` (app.html:38047–38048).

#### Le dessin à plusieurs (Tom, 10 oct. 2026, v140 — C-093) — À CONSTRUIRE AVEC FIREBASE, rien n'existe dans le prototype
> « Le dessin est collaboratif entre les personnes d'un Promi, d'un Chiche ou d'un Cercle. » Données : SPEC-DONNEES §5 bis.
- **La bande** montre le dessin posé de TOUS (les éléments posés, dans l'ordre d'arrivée au serveur). Un trait posé par un autre pendant que la
  fiche est ouverte paraît **sans fondu** (A2), sans déplacer quoi que ce soit.
- **Le mode dessin** : je vois les éléments posés des autres SOUS mon dessin en cours ; je ne peux ni les déplacer ni les effacer autrement que
  par la gomme (qui est mon élément). « ANNULER » ne défait que les miens. « POSER » pose les miens.
- **Qui a tracé quoi** : jamais un compteur ni un classement. Si l'auteur d'un trait doit se lire, c'est par un toucher sur le trait, en
  plein écran — **À TRANCHER** (rien n'est décidé ; par défaut : on ne l'affiche pas).
- **Signaler** : dans la vue en entier du dessin, une entrée « Signaler » (icône seule, la grammaire des icônes de fiche) quand le dessin
  porte un élément d'un autre ; le contenu signalé se retire de mon écran aussitôt ; « Bloquer » la personne. Mots à valider par Tom.
- **Hors ligne** : je dessine, mes éléments partent à la reconnexion et se posent au-dessus (ordre d'arrivée).
- **Le partage** : l'image est le dessin entier, photos importées comprises (v140, Q435) — donc avec ce que les autres y ont posé : **À TRANCHER**.

### États vides et d'erreur
- Parole sans échéance : la ligne d'état ne porte que le mot (« EN COURS »).
- Titre très long : coupé à trois lignes avec « … » (affichage seul).
- Suppression : confirmation puis « Annuler » pendant 5 s (§26).

### Textes exacts
- À qui : « À moi » · « À {Prénom} » · Chiche avec compagnon tiers : « À {Prénom} · avec {Prénom} » · « Gardé de côté ».
- État : « EN COURS » · « À TENIR » · « TENUE » · « LANCÉ » · « À RELEVER » · « TENU À DEUX » ; suite « · {JOUR EN CAPITALES} » quand l'app la connaît (échéance : « AUJOURD'HUI », « DEMAIN », un jour de la semaine…).
- Mot du geste : « trace pour tenir » · « {Prénom} tracera sa part si elle ose » (sans prénom : « elle tracera sa part si elle ose »).
- Message : « écris un mot » · « répondre » · « TA NOTE ».
- Barre : « Peaufiner » ; VoiceOver du rond : « Partager » ; du bouton photo : « Photo ».

### Sources
`lot-S1B-cotes`, `lot-S1B-geo` (app.html:13944–15690) · app.html:12340–12440 (textes de la fiche) · app.html:4590–4790 (le geste) · `lot-V7-CORPS-TENU` (33974) · `lot-V113-CORPS-SOMBRE-css` (7834) · `lot-V132-COBALT-css` (37964) · CLAUDE §3 (v122, v131, v133, **v134**), §4, §5.

### Trous
- v134 (corps sombre d'un Promi `#0E78F2`) est écrit dans CLAUDE.md mais **non commité** au moment de l'écriture : les lignes d'`app.html` citées dans ce document sont celles du fichier de travail et ont pu glisser de quelques lignes. `ETAT-30-SEPTEMBRE-2026.md` §2 porte encore `corps-promi` sombre `#1A52F0` : à régénérer.
- C-059 (v133, « en clair, le corps d'une fiche Promi prend le même traitement que Chiche et Cercle ; retirer en clair le filet autour des disques et sous le trait ») : état non vérifié ici (`CHANTIERS.md`).
- Le symbole du bouton photo attend le choix de Tom (C-060, `planche-v133/symboles`).
- L'action d'un toucher sur le champ de message d'une fiche en cours (ouvre-t-il Peaufiner sur COMMENTAIRES ?) n'a pas été relue.
- La fiche d'une **demande** (`p.req`, « promets-moi ») : le code d'origine porte « En attente de ta parole » et un bouton « Je promets » (app.html:4131) ; son rendu actuel n'a pas été vérifié.
- La récurrence, le rappel, l'importance sur la fiche : réglages de Ma Parole ! (floutés au gratuit) ; leur comportement au payé n'a pas été relevé.

---

<a id="5"></a>
## 5 · L'instant de « tenir »

**Nom à l'écran** : aucun (c'est la fiche). **Id interne** : `window._instant` = `'arrive'` · `'referme'` · `'apres'` ; classes `inst-*` sur `#detailPoster`. Ne concerne pas un Cercle.

### Accès
- `referme` puis `apres` : quand le geste d'une fiche se referme (la parole passe à « tenue »).
- `arrive` : quand l'autre personne trace sa moitié (état du produit ; dans le prototype il se rejoue par `_instantJoue('arrive')`).

### Éléments — les trois écrans (`lot-S5`, app.html:19602–19660) ; tous : base 300, amplitude 36, boîte 384
| Écran | Champ | Dalle (x, y, l × h) | Trait | Sous le trait |
|---|---|---|---|---|
| **l'autre part arrive** | couleur de la nature | 105, 91, 180 × 150 | orange `#DD4D23` plein 0 → 195 + chevron ; **amande** plein 195 → 268 (l'autre trace) ; points orange dès 213 | mot « l’autre part arrive » à y 388 ; Noyaux à 432 / 442 ; à-qui à 559 (orange) ; titre à 590 |
| **le trait se referme** | **amande `#8FE08F` plein** | 81, 88, 228 × 190 | **encre** plein 0 → 390 | rien (Noyaux cachés) |
| **juste après** | couleur de la nature | 105, 91, 180 × 150 | **amande** plein 0 → 390 | Noyaux à 388 / 398 ; à-qui à 515 ; titre à 546 ; état à 614 |

- Couleur des mots : sur la terre d'une parole tenue, amande (dans les deux thèmes) ; « l'autre part arrive » est posé sur le corps crème : `#00341A` en clair, amande en sombre.

### Actions / déroulé
- Le geste se referme → **1 000 ms** d'amande (« le trait se referme »), puis « juste après » ; fin à **1 700 ms** ; la fiche tenue ordinaire se pose ensuite, par morceaux.
- **La célébration** (CLAUDE §3) : une seconde dalle de la même forme apparaît sous la première, en amande, se décale, puis disparaît. L'amande ne peint que cela et la mention « TENU(E) ».
- Fluidité exigée : aucune image au-delà de 20 ms de travail pendant l'animation ; les deux dalles de l'instant sont rendues **à l'avance** quand la fiche à tenir est posée ; aucune passe de tout le document pendant l'animation.
- Fermer la fiche met fin à l'instant.
- Après une série : toast « Belle série — partage ton Noyau » avec le bouton « Partager » (app.html:3042, 6906). ⚠ Ce mot (« Noyau ») date d'avant le remplacement par la Pelote au partage (v13) : à valider avant de le porter.

### Textes exacts
« l’autre part arrive ».

### Sources
`lot-S5-css`, `lot-S5` (app.html:19568–19980) · CLAUDE §3 blocs v124, v125, « célébration » · `redteam_fluide.py`.

### Trous
- Le dessin exact de la célébration (décalage, durée de la seconde dalle amande) : décrit en mots dans CLAUDE.md §3 ; les valeurs n'ont pas été relevées dans le code.

---

<a id="6"></a>
## 6 · Peaufiner (Promi, Chiche)

**Nom à l'écran** : « Peaufiner » (la barre) ; la tête du panneau porte **le titre de la parole**. **Id interne** : `#detailPoster.s2-ouv` ; contenu `#dpdCorps .s2-liste` ; rangées `.s2-reg`, zones `.s2-zone`, bloc de Ma Parole ! `.s2-cercle`.

### Accès
- Fiche → barre Peaufiner (toucher). La barre est fixée en bas et ne bouge jamais ; les réglages défilent au-dessus.
- Sur la fiche d'un **Cercle**, Peaufiner ne s'ouvre **qu'en touchant sa barre** (le doigt qui descend fait défiler le fil) — §7.

### Éléments (ordre de `bati()`, app.html:16262–16361 ; positions relevées dans `joignable-inventaire.md`)
| # | Rangée | Géométrie | Valeur / contenu | Toucher |
|---|---|---|---|---|
| 0 | Tête : titre + « ✕ FERMER » | « ✕ FERMER » 91 × 13 centré (321 ; 56) | le titre de la parole | ferme la fiche |
| 1 | « LE TRAIT » | 342 × 64, centre y 142 | le nom du pinceau (« Plein » ; « {nom} — 0,50 € » s'il n'est pas libre) | déplie le rail des pinceaux |
| 2 | « À QUI » (Chiche : « À QUI JE LANCE ») — **absente pour un Promi à soi** | 342 × 64 | le prénom (ou « moi ») | déplie le choix des personnes (ajouter, retirer) |
| 3 | « AVEC » (Chiche seulement) | 342 × 64 | le compagnon ; vide : « personne », contour pointillé | idem |
| 4 | « AVANT » | 342 × 64 | l'échéance (« dimanche 18 », « un jour »…) | déplie la **liste unique** : « un jour » · « en l’air » · « demain » · « 5 jours » · « 2 semaines » · « ce mois-ci » · « une date précise… » (sélecteur de date natif, pas avant aujourd'hui) |
| 5 | « DANS UN CERCLE » (pas sur un Chiche) | 342 × 64 | le nom du Cercle ou « aucune » | déplie les Cercles (« Aucune » + chaque Cercle) |
| 6 | « NOTE » | zone 342 × 118 (grandit de 22,5 par ligne ; rayon 30 au-delà de 94,5 de haut) | champ de texte ; ligne du bas : « privée — visible par toi seul » ou « visible par {X} » | saisie |
| 7 | « PIÈCES JOINTES » | 342 × 92 | « N fichier(s) » ; ligne du bas « privées — visibles par toi seul » / « visibles par {X} » ; vide déplié : « aucun fichier — appuie sur + » | déplie |
| 8 | « COMMENTAIRES » | zone 118 (104 sur un Chiche) | invite « écris un mot… » ; ligne du bas « privé — personne d’autre ne le voit » ou « visible par {X}, qui peut y répondre » | saisie |
| 9 | « RELANCER {PRÉNOM} » — seulement si une relance est possible | 342 × 64 | « → » | relance la personne |
| 10 | **Le bloc de Ma Parole !** (cinq réglages) | rangées 342 × 64 | « RÉCURRENCE » — « chaque semaine » · « RAPPEL » — « la veille à 19:00 » · « C'EST IMPORTANT ? » — « · ·· ··· » · « LA MÉMOIRE » — « réveille tes « en l’air » » · « LA COULEUR » — le code de la couleur (ex. « #FFB8D2 ») | **au gratuit : floutés à 4,8 px, sans prise, sans encart, sans explication** — c'est un mur (§21). Au payé : nets et réglables |
| 11 | « SUPPRIMER CE PROMI » / « SUPPRIMER CE CHICHE » | 342 × 64 ; crème en sombre, encre en clair (jamais `#DD4D23`) | — | confirmation (§26) |
| — | Barre Peaufiner | y 760 → 844 | inchangée | referme |

- « LA COULEUR » (payé) : une des quatre couleurs de la palette de la dalle, ou un code libre ; la dalle la prend sur la Toile (`lot-CERCLE-COULEUR`, app.html:33050).
- Chaque rangée : trait 2, rayon = hauteur ÷ 2 (pilule) jusqu'à 94,5 ; libellé en capitales (Gilbert) à gauche, valeur à droite, sur la même ligne de base.
- L'ordre universel des réglages et le crible : un nœud qui n'est pas dans cette liste ne se peint pas.

### Actions
Voir la colonne « Toucher ». En plus :
- Changer l'échéance = la repousser (il n'y a pas de bouton « repousser ») ; « un jour » et « en l'air » valent tous deux « pas de date » mais restent **deux valeurs distinctes**.
- Toucher un mur → la phrase du mur (§21).
- Le rond Partager de la barre garde sa fonction (§13).

### États vides et d'erreur
- Aucune pièce jointe : « 0 fichier ».
- « AVEC » vide : pointillé.

### Textes exacts
Tous les libellés du tableau, plus « ✕ FERMER ». Confirmation de suppression : §26.

### Sources
`lot-S2-peaufiner` (app.html:15692–16440) · `lot-PINCEAU-PEAUFINER` (25167) · `lot-CERCLE-MUR` (31439) · `lot-CERCLE-COULEUR` (33050) · `lot-V104-MURS-css` (37061) · `joignable-inventaire.md` (écrans « Peaufiner », « Peaufiner Chiche ») · CLAUDE §3 bloc v132 (« SUPPRIMER CE PROMI » crème).

### Trous
- Le contenu déplié et le fonctionnement **au payé** de RÉCURRENCE, RAPPEL, C'EST IMPORTANT ?, LA MÉMOIRE (les valeurs affichées sont des exemples figés dans `cercle()`, app.html:16233–16236) : non relevés. Le code d'origine porte « Aucune · Quotidien · Hebdo · Mensuel » pour la récurrence (app.html:2683) — non confirmé au rendu.
- La rangée « LE TRAIT » : hauteur dépliée et place exacte du rail sur une fiche (sur un Cercle : carte de 118, §7).
- La forme de la relance (« RELANCER ») : ce qui est envoyé n'a pas été relu.

---

<a id="7"></a>
## 7 · La fiche d'un Cercle et son Peaufiner

**Nom à l'écran** : mot-marque « CERCLE » (centré dans son encart comme « PROMI » et « CHICHE », v129). **Id interne** : `#detailPoster.dp-nuee` / `.dp-mode-nuee` ; le Cercle ouvert est `curNuee` (`cur` est nul) ; table des noms `NUE`, membres `NUEEMEM` ; fil `#dpNueeFil`.

### Accès
- Depuis : la dalle du Cercle sur la Toile, sa carte dans l'Index, un bandeau du Fil.
- Mène à : la fiche d'une de ses paroles (une ligne du fil), la page + dans ce Cercle (« Planter dans le Cercle »), Peaufiner (la barre), Partager (rond), « Dessiner » (bouton photo).

### Éléments, état POSÉ (app.html:15120–15460 ; `lot-NUEE-ENTREE-css` 32794)
| Élément | Cotes | Détail |
|---|---|---|
| Le champ | lilas `#C9A8F5` ; texte et trait posés dessus : violet `#291547` / brun encre | il porte **la petite Toile du Cercle** : les vraies dalles de ses paroles (semis déterministe : même Cercle, même composition à chaque ouverture) |
| Plateau | 24 / 40 / 342 × 60 | « CERCLE » + « FERMER » |
| Bouton photo | rond 34, x centre 349 | VoiceOver « Dessiner sur ce Cercle » ; ouvre le menu (« Dessiner », « Retirer le dessin ») |
| **Le trait** | `base = max(176, 460 − 86 × n)`, amplitude 40 (⚠ voir Trous : 36 depuis le 1er sept. ?) ; **n = nombre de lignes du fil, « Planter dans le Cercle » comprise** | Cercle vide : n = 1 → base 374 ; à partir de quatre lignes : plancher 176 |
| Les Noyaux | y = boîte − 29 | deux : « Toi » (78) puis **celui du Cercle** (58, sous son nom) |
| « Avec … » | y = Noyaux + 127 ; Gilbert 19 | « Avec Rachel, Adrien, +3 » (deux nommés, puis le reste **moi compris**) · « Avec toi seulement » |
| Le titre | y = « Avec » + 35 ; Gilbert 38 | le nom du Cercle, **dans sa casse** (« le potager ») |
| La méta | y = titre + 68 | « N Promi · M tenu(s) » (+ « · une note », « · N fichier(s) », « · N mot(s) ») ; vide : « encore aucune parole » |
| **Le fil** `#dpNueeFil` | première ligne à méta + 30 ; cartes 342 de large, 79 de haut (94 avec deux lignes de titre), pas de 12 | une carte par parole : libellé d'état (« à tenir », « en cours », « TENU », « CHICHE RELEVÉ »…), titre, « à {qui} », la vraie dalle à droite ; **toutes** les paroles (pas de coupe) |
| **« Planter dans le Cercle »** `#nfAdd` | pilule 342 × 62, rayon 31, trait 2, fond violet `#291547`, texte crème Gilbert 18 ; un rond crème de 40 portant le + ; **dernière ligne du fil**, 12 sous la dernière carte (16 sous la méta d'un Cercle vide) | |
| Barre Peaufiner | y 760 → 844 ; elle prend le **corps violet `#291547`** dans les deux thèmes, texte crème | |

### État DÉFILÉ (§13 de la spécification, CLAUDE §5)
- Le doigt qui descend fait défiler **le fil**, pas les réglages : l'encart, les Noyaux, le titre remontent et disparaissent sous le trait ; les paroles prennent toute la place.
- Butée haute : **base 58, amplitude 16** ; le champ se réduit à une **bande de 114 px** ; la Toile qu'on y voit est **la même**, simplement remontée.
- C'est un **état que le code pose** (une classe), jamais une géométrie déduite.

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher une ligne du fil | ouvre la fiche de cette parole | inventaire (`.nf-item`, « on… ») |
| Toucher « Planter dans le Cercle » | page + avec ce Cercle déjà choisi (« tout le monde » en tête des destinataires, « Moi » ensuite) | app.html:5792 ; CLAUDE §5 |
| Glisser verticalement | passe de posé à défilé et retour | `window._nueeDefile` |
| Toucher la barre Peaufiner | ouvre le Peaufiner du Cercle | `lot-NUEE-PEAUFINER` |
| Rond Partager | Partager : **Mon Folio réduit aux paroles de ce Cercle** | `lot-V117-PARTAGE-FICHE` app.html:37575 |
| Bouton photo → « Dessiner » | mode dessin ; le dessin d'un Cercle est gardé par Cercle | `lot-V132-DESSIN` |

### Le Peaufiner d'un Cercle (`lot-NUEE-PEAUFINER`, app.html:20553–20580 ; cartes en cotes absolues, x 24, largeur 342)
| Carte | y | hauteur | Libellé | Valeur / invite | Ligne du bas |
|---|---|---|---|---|---|
| Tête | — | — | le nom du Cercle + « ✕ FERMER » | | |
| `npTrait` | 110 | 118 | « LE TRAIT » | le nom du pinceau ; **son rail est permanent** (pastilles 78 × 44) | |
| `npDesc` | 244 | 104 | « DESCRIPTION » | invite « présente le Cercle, son but… » | « visible par tous les membres » |
| `npMemb` | 364 | 64 | « MEMBRES » | « Rachel · Adrien · +3 » (au-delà de trois : deux nommés + « +N », N comptant les non nommés, moi compris) ; vide : « personne encore » | |
| `npFich` | 444 | 92 | « PIÈCES JOINTES » | « N fichier(s) » ; vide : « aucun fichier » | « visibles par le Cercle » |
| `npComm` | 552 | 104 | « COMMENTAIRES » | invite « écris un mot… » | « visibles par les membres du Cercle » |
| (mur) | relevé y ≈ 482 | 64 | « LA COULEUR » | la couleur de la dalle du Cercle | flouté au gratuit |
| page 2 | — | 62 | bouton « Planter dans le Cercle » (le même `#nfAdd`, déplacé) | | |
| `npDiss` | page 2 + 124 | 64 | « DISSOUDRE LE CERCLE » | « → » | |

- « DISSOUDRE LE CERCLE » : toast à deux choix « Dissoudre « {nom} » ? » — « Libérer les Promi » / « Tout supprimer » ; puis « « {nom} » dissoute » avec « Annuler » (5 s). (app.html:9266, `lot-V16`)

### États vides et d'erreur
- **Cercle vide** : champ lilas avec les graines vides de la Toile ; « Avec toi seulement » ; « encore aucune parole » ; le fil ne porte que « Planter dans le Cercle » (relevé : centre y 717 posé, 218 défilé). L'ancienne invitation (« Plante le premier Promi… ») et « aucun Promi ici pour l’instant » sont **masquées**.
- Un Cercle sans aucune parole est listé dans l'Index comme **gardé de côté**.

### Textes exacts
« CERCLE » · « Avec {A}, {B}, +{N} » · « Avec toi seulement » · « {N} Promi · {M} tenu(s) » · « encore aucune parole » · « Planter dans le Cercle » · VoiceOver « Dessiner sur ce Cercle », « Partager » · libellés du Peaufiner (tableau).

### Sources
app.html:5739–5850 · `lot-S1B-geo` (15120–15460) · `lot-NUEE-BANDE`, `lot-NUEE-PEAUFINER` (20479–20970) · `lot-NUEE-ENTREE-css` (32794) · `lot-NUEE-CERCLE` (33169) · `joignable-inventaire.md` (« Nuée », « Nuée défilée », « Nuée vide », « Peaufiner Nuée ») · CLAUDE §4, §5 (§13), §8 · `redteam_nuee.py`, `redteam_nuee_entree.py`, `redteam_nuee_dalle.py`.

### Trous
- **Amplitude de l'état posé** : le commentaire d'app.html:15132 dit 40 ; la décision du 1er sept. (« l'onde passe à 36 partout », app.html:17100) dit 36 avec deux exceptions qui ne citent pas le Cercle. La valeur réellement posée (`ampPose`) n'a pas été relue.
- Les libellés d'état des lignes du fil (« à tenir », « en cours », « TENU », « CHICHE RELEVÉ ») sont relevés de l'inventaire ; la table complète des mots et leur casse n'a pas été extraite.
- Le sélecteur « LA COULEUR » d'un Cercle au payé (`NUEDALLE`) : contrôle non relevé.
- Le Peaufiner du Cercle ne porte pas les quatre autres réglages de Ma Parole ! (récurrence…) : seul « LA COULEUR » y figure dans l'inventaire.

---

<a id="8"></a>
## 8 · L'Index

**Nom à l'écran** : « INDEX » (le X en couleur). **Id interne** : `#indexSheet` (une feuille) ; liste `#indexList`, cartes `.s4-carte`.

### Accès
- Accueil → INDEX. Mène à : fiche d'une parole, fiche d'un Cercle, page + (un gardé de côté).

### Éléments (de haut en bas)
| Élément | Cotes relevées | Détail |
|---|---|---|
| Plateau épais | x 24 · y 40 · 342 × **88**, rayon 44 (`#indexSheet.s4 .enh`, app.html:32783 : il porte deux lignes) ; « ✕ Fermer » centré (296 ; 84) | titre « INDEX » + le compte : **« N parole(s) · M Cercle(s) »** (les gardés de côté et les demandes ne sont pas comptés) |
| Recherche `#ixSearch` | champ 270 × 52, rayon 26, trait 2 ; texte centré vers (174 ; 170) | invite « Rechercher » |
| Tri `#ixTriBtn` | rond 52, centre (340 ; 170) | « ⇅ », ouvre le menu |
| La grille `#indexList` | commence à y **212**, défile sous le plateau et rogne | **Deux par ligne** : cartes **165 × 198**, centres x 107 · 284 ; **Trois par ligne** : **106 × 133**, centres x 77 · 195 · 313, pas vertical 145 ; rayon 22 |

**Une carte** (`lot-S4`, app.html:18737–19200) :
- haut : le **champ de la nature** (couleur pleine) avec la **vraie dalle** (dans le monde et la palette du Studio, **non teintée**) ; si la dalle et le champ se confondent, c'est le champ qui cède (Q93) ;
- une étiquette de nature en haut à gauche (pastille crème de 22 de haut, rayon 11, PromiLate 13) : « Promi » · « Chiche » · « Cercle » ;
- le **trait** : même grammaire que la fiche, à l'échelle — `échelle = hauteur / 600`, `base = hauteur du trait figée à la plantation × échelle`, `amplitude = 13 × largeur / 173`, période 1 sur la largeur de la carte, épaisseur `5,5 × largeur / 173` ; il porte l'**état** ;
- bas (corps : crème en clair, corps de la nature en sombre) : sur-titre (« à moi », « à Rachel », « de Nico », « avec +4 », « perso », « gardé de côté »), le **titre** (24 px, deux lignes au plus puis points de suite — jamais de réduction), l'état.
- Un **Cercle** remplace ses paroles : une seule carte, avec une **petite Toile** de ses dalles ; sous-ligne « N Promi · M membre(s) » (ou « perso »).
- Un **gardé de côté** : le champ de sa nature **en pointillé, sans matière**.

### Actions
| Geste | Effet |
|---|---|
| Toucher une carte | fiche de la parole / du Cercle ; gardé de côté → page + |
| Taper dans la recherche | filtre sur le titre, la personne, le Cercle |
| « ⇅ » | menu : **TRIER** — « Récents » · « À tenir en premier » · « Par personne » · « Par Cercle » ; **NE MONTRER QUE** — « Tout » · « En suspens » · « Manquées » · « Promi » · « Cercles » · « Gardés de côté » · « Demandes » ; **QUADRILLAGE** — « Deux par ligne » · « Trois par ligne » · « Quatre par ligne » (le choix courant porte un point) |
| « ✕ Fermer » | retour à l'accueil |

- **Ordre au repos : celui de la plantation** (chronologique, neutre — jamais un tri par urgence) ; un Cercle se range à sa première plantation ; les gardés de côté ferment la liste.

### États vides et d'erreur
- Rien à montrer (liste vide ou filtre sans résultat) : « Rien ici » / « Touche le **+** pour planter un Promi. »

### Textes exacts
« INDEX » · « {N} parole(s) · {M} Cercle(s) » · « Rechercher » · les entrées du menu ci-dessus · « Rien ici » · « Touche le + pour planter un Promi. » · mots du temps d'une carte : « tenue » · « à tenir » · « un jour » · « aujourd'hui » · « demain » · un jour de la semaine (≤ 7 jours) · au-delà : ⚠ voir Trous · états : « TENUE », « TENU À DEUX », « LANCÉ », « À TENIR », « EN COURS », « GARDÉ DE CÔTÉ ».

### Sources
app.html:2642 (structure et menu) · app.html:3480–3625 (liste, ordre, compte, vide) · `lot-S4-css`, `lot-S4` (18602–19568) · `lot-REPERAGE` (32750) · `joignable-inventaire.md` (« Index 2 », « Index 3 ») · CLAUDE §8 (`#indexList{top:212px}`) · `redteam_reperage.py`.

### Trous
- **Quatre par ligne** : taille des cartes non relevée (l'inventaire ne couvre que 2 et 3).
- Cotes internes d'une carte (place du sur-titre, du titre, de l'état, boîte de la dalle) : dans `peintCarte` (app.html ≈ 18900–19060), non extraites ; les vérifications du document donnent les boîtes du trait : 135 (165 × 198), 97 (106 × 133).
- `motDuTemps` au-delà de 7 jours (app.html:6260 et suivantes) : non relu.
- « Manquées » et « En suspens » sont des mots du menu d'origine ; « manquée » n'est pas dans le lexique des états (à tenir · en cours · tenu) — à valider avant de les porter.

---

<a id="9"></a>
## 9 · Le Fil

**Nom à l'écran** : « FIL » (le L en couleur). **Id interne** : `#feedView` (classe `in` quand il est ouvert) ; liste `#feedList` ; journal `FEED`.

### Accès
- Accueil → FIL. Mène à : fiche d'une parole, fiche d'un Cercle.

### Éléments (de haut en bas)
| Élément | Cotes relevées | Détail |
|---|---|---|
| Plateau | 24 / 40 / 342 × 60 ; « ✕ Fermer » centré (296 ; 70) | « FIL » ; le compte à côté du titre est masqué |
| Recherche `#fdSearch` | centre (174 ; 142) | invite « Rechercher » |
| Tri `#fdTriBtn` | rond 52, centre (340 ; 142) | « ⇅ » |
| Les bandeaux | **358 × 128**, x 16, rayon 22, pas vertical **140** ; premier centré à y 268 | un par événement du journal |

**Un bandeau** (app.html:19240–19330) :
- à gauche (0 → 145 environ) : le champ de la nature, la vraie dalle, et le **trait vertical** (la même onde tournée d'un quart de tour) ; étiquette de nature en haut à gauche (« Promi » / « Chiche » / « Cercle ») ;
- à droite, x 145, largeur 197 : **l'événement** (y 16, hauteur 28 ; un visage de 26 si l'événement nomme quelqu'un d'autre que moi) · **le titre** (y 50, boîte 42, 24 px ; deux lignes au plus puis points de suite, il grandit vers le haut) · **l'état** (y 98, 11 px, capitales) ;
- une pastille « pas encore vu » sur le bandeau : elle s'efface quand on ouvre **ce** bandeau, jamais à l'ouverture du Fil.
- **Le bandeau dit l'événement, pas l'état courant de la parole** (un journal).

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher bref un bandeau | ouvre la fiche (ou le Cercle) | app.html:19355 |
| **Appui maintenu 480 ms** (sans bouger de plus de 3 px) sur un bandeau qui porte un geste | déplie sous lui une rangée de boutons (hauteur 50, rayon 25 ; le bouton principal a un contour 3 px) ; un second appui la replie ; elle se referme dès qu'elle a servi | app.html:19361–19410 ; CLAUDE §5 (« ajout validé, hors inventaire ») |
| « TENIR » | tient la parole depuis le Fil | `feedKeep`, app.html:6906 |
| « REPORTER » | toast « Reporter… » avec « +1 j » · « +3 j » · « +1 sem » | app.html:6921 |
| « RELEVER » | relève un Chiche reçu | app.html:6878 |
| « REJOINDRE » | rejoint un Cercle (invitation) | app.html:6881 |
| « TRACER » | trace sa moitié | app.html:6883 |
| « ✧ bravo » / « ✦ bravo » | réaction à un événement d'un proche (bascule) | app.html:6889 |
| « ⇅ » | menu : **TRIER** — « Récents » · « Par personne » · « Par Cercle » ; **NE MONTRER QUE** — « Tout » · « Ce qui attend un geste » · « Paroles tenues » · « Demandes » · « À tenir » · « Cercles » · « Mes Promi » · « Mes proches » | app.html:2555 |

### États vides et d'erreur
- Journal vide : « ✦ » · « Rien ne bouge encore » · « les gestes de tes proches / apparaîtront ici ».
- Recherche sans résultat : « Rien ne correspond » · « essaie un autre mot ».
- **Le Fil ne montre jamais une parole qui n'existe plus** (une parole retirée emporte ses événements) — `lot-V130-REACTIF`, `A-INTEGRER.md` C-049.

### Textes exacts
- « FIL » · « Rechercher » · menu ci-dessus · « TENIR » · « REPORTER » · « RELEVER » · « REJOINDRE » · « TRACER » · « bravo ».
- Événements (jeu de démonstration, formes à porter) : « {Prénom} a relevé » · « à {Prénom} » · « {Prénom} a planté » · « à moi » · « {Prénom} te lance un chiche » · « {Prénom} a tracé sa moitié » · « {Prénom} t’invite à rejoindre « {Cercle} » ».
- États : « RELEVÉ · À TENIR À DEUX » · « À RELEVER » · « {NOM DU CERCLE} · {N} PROMI » · « {N} PROMI · {M} TENU(S) » · et ceux de l'Index.
- Les guillemets « » d'un titre sont insécables.

### Sources
app.html:2555 · app.html:6848–6925 (`buildFeed`, gestes) · `lot-S4` (19200–19420) · `lot-FIL-V21` (35977) · `lot-V89-COMPTEURS` (33772) · `lot-JEU-PLANCHE` (21365) · `joignable-inventaire.md` (« Fil ») · `lot-V130-REACTIF` (37751).

### Trous
- Quels types d'événement portent quels gestes (la correspondance type → boutons se lit dans `buildFeed`, app.html:6870–6890) : seule la forme des boutons a été extraite.
- La pastille de l'entrée FIL de la barre (« ce qui attend un geste de moi », Q347) : règle de comptage non relue (`_filAttente`).

---

<a id="10"></a>
## 10 · L'Aura

**Nom à l'écran** : « L’AURA ». **Id interne** : `#auraScreen.au2` ; cadre `#auCadre` ; la Pelote `#auBoule` + `#auBouleGL` (moteur `PeloteMoteur`) ; halo `#auPeloteHalo`, ombre `#auPeloteOmbre`.

### Accès
- Accueil → AURA. Mène à : l'aide (i), Partager (sujet « Ma Pelote »), fiche d'une personne (un Noyau), fiche d'une parole (une île de la Pelote, une dalle de « Ce que tu as tenu »).
- L'Aura **défile** sous le plateau ; elle reste à jour quand une fiche ouverte par-dessus tient ou retire une parole.

### Éléments — **composition B, FIGÉE** (CLAUDE §3 bloc v126 ; cotes haut → bas, phrase de deux lignes)
| Bloc | y haut → y bas | Détail |
|---|---|---|
| Plateau | 40 → 100 | « L’AURA » + bouton « i » (20 × 20, centre (218 ; 78)) + « ✕ Fermer » |
| Halo | commence à 4,5 sous le plateau | seul volume de l'app avec l'ombre : teinte du **corps**, décroissance douce, plein côté éclairé, presque nul sur le quart inférieur, tramé ; respire ± 20 % avec le souffle |
| **La Pelote** (silhouette) | 132,53 → 374,53 (Ø 242) ; zone de prise 296 × 296 centrée (195 ; 254) | **pleine** (opaque) ; fourrure (220 000 poils, paliers 180 000 · 150 000 · 110 000 · 90 000 · 75 000 selon la machine, jamais sous les yeux) ; son **sol** prend un ton de la palette du Studio, son **corps** une autre teinte de la palette (jamais celle des poils, jamais kaki), tirés à chaque ouverture ; les **îles** sont les dalles des paroles tenues, **dans le monde et la couleur de leur plantation** ; **rien ne dépasse du contour** |
| Ombre | 391,22 → 407,45 | ellipse ; encre du mode en clair, **crème** en sombre |
| « PARTAGER MA PELOTE » | 435,47 → 495,47 ; 342 × 60 | PromiLate 15, capitales ; **couleur du texte : un ton de la palette tiré à chaque ouverture**, ≥ 3:1, jamais celui des poils ni du corps, jamais kaki (la clarté seule est ajustée, jamais de repli sur l'encre) |
| La phrase | 515,59 → 566,56 (une ligne : jusqu'à 541,07) ; 20,4 px | une des cinq phrases (voir Textes) |
| **Les Noyaux** | 582,77 → 689,77 ; rangée 366 × 107 qui glisse | « Toi » (78) puis chaque personne (58) avec son prénom ; l'anneau = les trois états de ce qui se promet **entre vous, dans les deux sens, une fois**, pondéré par le nombre de paroles |
| La légende | 709,05 → 733,30 | « tenues » · « en cours » · « à tenir », chacune avec sa pastille d'état |
| Les trois chiffres | 752,02 → 782,02 ; PromiLate 29 | un chiffre centré sous chaque entrée de la légende |
| « Ce que tu as tenu » | titre à 800,52 (62 pt d'air sous les chiffres) | **toutes** les paroles tenues, **la plus récente en premier**, en vraies dalles (boîte 105 × 56, trois par rangée) avec leur titre ; l'Aura défile |
| « Ce qu’on t’a tenu » | à la suite | les trois dernières ; **au gratuit : flouté à 4,8 px** (mur, §21) ; absent s'il n'y a rien |

### Actions (les « huit acquis » de la Pelote, `lot-AURA-PELOTE` app.html:29281–29288)
| Geste | Effet |
|---|---|
| Au repos | la Pelote tourne lentement, sans jamais s'arrêter : **un tour en 2 minutes** ; elle « respire » par la lumière du velours (cycle de 10 s : 4,6 s de montée) ; immobile avec « Réduire les animations » |
| Glisser sur la Pelote | la tourne dans tous les sens ; au lâcher, l'élan **s'additionne** à la rotation lente (vitesse lue sur l'heure réelle des événements du doigt) |
| Poser le doigt | creuse la fourrure (un plateau, une cuvette, un bourrelet), résiste et revient ; la trace reste ; un geste la relisse |
| **Toucher** (sans glisser) une île | ouvre la fiche de cette parole |
| Toucher un Noyau | ouvre la fiche de la personne ; glisser la rangée la fait défiler |
| Toucher une dalle de « Ce que tu as tenu » | ouvre la fiche |
| « PARTAGER MA PELOTE » | ferme l'Aura et ouvre Partager sur le sujet « Ma Pelote » |
| « i » | ouvre l'aide |
| Toucher « Ce qu'on t'a tenu » (gratuit) | la phrase du mur |
| « ✕ Fermer » | accueil |

- Toute porte s'ouvre sur le **toucher achevé**, jamais au simple lever d'un glissement (le « clic fantôme »).

### États vides et d'erreur
- **Aucune parole** (`au-vide`) : à la place de la phrase, l'invite « La première parole laissera sa trace ici. » suivie de « Tout commence par une parole donnée. » ; pas de Noyaux ; chiffres masqués ; pas de « Ce que tu as tenu ».
- **Des paroles, aucune tenue** : la phrase est « La première parole laissera sa trace ici. » ; « Ce que tu as tenu » est absent.
- Sans carte graphique (WebGL 2 dans le prototype) : le peintre du processeur prend le relais, mêmes poils.

### Textes exacts
- « L’AURA » · « PARTAGER MA PELOTE » (VoiceOver « Partager ma Pelote ») · « Toi » · « tenues » · « en cours » · « à tenir » · « Ce que tu as tenu » · « Ce qu’on t’a tenu ».
- **Les cinq phrases** (choisie par `nombre de paroles tenues modulo 5` : elle change en tenant, jamais au hasard) :
  0. « Rien de ce qui est ici n’a été dit à la légère. »
  1. « Tout ça, tu l’as dit. Et tu l’as fait. »
  2. « On ne dirait pas comme ça, mais c’est du solide. »
  3. « Il y en a, des paroles tenues. »
  4. « Et dire que tout ça, c’est toi. »
- Vide : « La première parole laissera sa trace ici. » · « Tout commence par une parole donnée. »

### Sources
`lot-AURA-PELOTE-CSS`, `lot-AURA-PELOTE-MOTEUR`, `lot-AURA-PELOTE` (app.html:26034–31066) · `lot-V95-AURA-CPT-css` (36908) · `lot-V114-PELOTE-css`, `lot-V119-PELOTE` (7656–7816) · `lot-DALLE-PORTE` (31286) · CLAUDE §3 blocs v114–v131, §7, §8 · `releve-aura.py` (cotes B en dur), `redteam_corps.py`, `redteam_bouton.py`, `redteam_halo.py`, `redteam_plein.py`, `redteam_souffle.py`, `redteam_pelote_doigt.py`.

### Trous
- La géométrie de la grille de « Ce que tu as tenu » (pas horizontal et vertical, place du titre sous la dalle) n'a pas été relevée ; la fiche d'une personne emploie 117 × 101 pour la même cellule (§22) — à ne pas transposer sans vérifier.
- Les paramètres du toucher de la Pelote (rayon et profondeur de l'empreinte, durée du retour, constantes d'élan `G`) sont dans `lot-AURA-PELOTE` : à prendre dans le document de la Pelote, non extraits ici.
- La légende écrit « tenues » ; l'aide « TENUES / EN COURS / À TENIR » ; pas de contradiction, casse différente.

---

<a id="11"></a>
## 11 · L'aide de l'Aura

**Nom à l'écran** : « L’AURA ». **Id interne** : `#auraHelp`.

### Accès
- Aura → « i ». « ✕ Fermer » revient. Défile sous le plateau.

### Éléments (`lot-HUIT`, app.html:33239–33276)
1. Plateau : « L’AURA » + « ✕ Fermer ».
2. Légende : trois pastilles d'état — « TENUES » `#00341A` · « EN COURS » `#291547` · « À TENIR » `#DD4D23`.
3. Étiquette « En gratuit », puis cinq cartes (une icône 48 × 48 + un titre + une phrase) :
   - « La Pelote » — « Chaque parole tenue y devient une île : elle s’étoffe à mesure que tu tiens. Touche une île pour la revoir. »
   - « La phrase » — « Sous la Pelote, quelques mots pour te rappeler ce que tu as déjà tenu. »
   - « Les Noyaux » — « **Toi**, puis chaque personne avec qui tu échanges des paroles. L’anneau dit où vous en êtes : **tenu**, **en cours**, **à tenir**. »
   - « Ce que tu as tenu » — « Tes paroles tenues, dans l’ordre où tu les as tenues. Touche-en une pour la revoir. »
   - « Partager ma Pelote » — « Une image à partager : on y voit que tu tiens parole, jamais ce que tu as promis. »
4. Étiquette « Avec Ma Parole ! » — **masquée au gratuit** ; l'encart « ✦ Ma Parole ! » est **masqué** (v104).
5. Deux cartes **floutées à 4,8 px au gratuit** (mur) :
   - « Peaufiner, avec Ma Parole ! » — « Récurrence, rappel, importance, mémoire et **la couleur** de ta dalle — sur chaque Promi, Chiche et Cercle. »
   - « Les designs signature » — « Ramage, Madrure et Volubilis pour ta Toile. »

### Actions
- Toucher les cartes floutées (gratuit) : la phrase du mur (§21). Rien d'autre n'est interactif.

### États vides et d'erreur
Aucun.

### Sources
`lot-HUIT` (app.html:33230) · `lot-V104-MURS-css` (37068, 37075) · app.html:8559.

### Trous
- ⚠ **Contradiction à trancher** : la carte « Ce que tu as tenu » dit « dans l’ordre où tu les as tenues » ; depuis v132 la liste montre **la plus récente en premier** (CLAUDE §3 bloc v132). Le texte de l'aide n'a pas été repris.
- Les mots de l'aide sont « à valider » (Q350).

---

<a id="12"></a>
## 12 · Le Studio

**Nom à l'écran** : « Le Studio » (le seul titre qui ne passe pas en capitales). **Id interne** : `#studioScreen.st-plat` ; cadre `#stpCadre` (390 × 844) ; Toile d'aperçu `#stBg` ; plateaux `#stpHaut`, `#stpBas` ; panneau des palettes `#stpPals` (classe `stp-pals` sur l'écran) ; monde verrouillé `stp-verrou`.

### Accès
- Accueil → STUDIO ; Réglages → « Le Studio ». Ouvrir le Studio pendant l'onboarding le termine.
- Ce qu'il règle est **global** : le monde, la palette (et sa teinte), l'écran (sombre / clair), le texte sur les dalles. **Tout suit le Studio, sauf l'Aura** (la Pelote et « Ce que tu as tenu » gardent le monde de plantation). Le pinceau n'y est pas (il appartient à une parole).

### Éléments (`lot-STUDIO-PLATEAUX-css`, app.html:21720–21930)
| Élément | Cotes | Détail |
|---|---|---|
| La Toile d'aperçu | 390 × 844, bord à bord, derrière tout | le **vrai moteur**, vivant, toutes les cellules colorées ; elle montre le monde **affiché** (même verrouillé) |
| Plateau du haut `#stpHaut` | 24 / 40 / 342 × 60, rayon 30, trait 2 | « Le Studio » (Gilbert 27) + « ✕ FERMER » (boîte 91 × 19 centrée (293 ; 70)) |
| Le nom `#stpNom` | x 24 · y 330 · largeur 342, centré | trois lignes : **le monde** (Gilbert 46) · « en » (Atkinson 22) · **la palette** (Atkinson 22) — le seul texte posé sur la Toile nue |
| Plateau du bas `#stpBas` | x 24 · y 555 · 342 × 253, rayon 30, trait 2 | (remonté/abaissé de 12 le 18 sept. pour s'aligner sur Partager : ⚠ voir Trous) |
| — les quatre tons `#stpTons` | y 581 ; disques de 54 | les quatre couleurs de la palette courante |
| — les mots `#stpLab` | y 649,5 ; deux mots de 108 de large | l'état courant de chaque paire : « sombre » ou « clair » · « avec texte » ou « sans texte » |
| — les quatre disques `#stpVue` | y 690 ; disques de 44, trait 2 ; 20 entre deux disques d'une paire, 56 entre les paires | sombre (`#201908`) · clair (`#F7F0DE`) | avec texte (trois barres) · sans texte ; relevé : centres x 81 · 145 pour la première paire, y 724 |
| — les points des mondes `#stpDots` | y 768 ; 9 px (14 pour le courant) ; rangée de 298 de large (x 46 → 344), écart calculé, 13 au plus | vingt points |
| L'invite `#stpInv` | x 24 · y 764 · largeur 342 | « ‹ glisse pour changer de monde › » ; **elle meurt dès que le geste a été fait une fois** ; pendant un appui : « reste appuyé pour changer de couleur » |
| Monde verrouillé | la Toile est floutée à **1,4 px** | bouton « Adopte ce design — 2 € » : x 24 · y 473 · 342 × 62, rayon 31 ; les réglages du plateau du bas deviennent des **murs** ; l'encart « Ou débloque-les tous / Avec Ma Parole ! » est **masqué** (v104) |

### Le panneau des palettes (`stp-pals`)
- S'ouvre en touchant un des quatre tons ; il remplace le contenu du plateau du bas.
- Contenu, dans l'ordre : bouton « ← Retour » (en haut à gauche du panneau, VoiceOver « Revenir au menu ») · **la grille des 24 pastilles** (quatre rangées de six ; **Primesautier en premier**, l'ordre des autres inchangé) · **le nom** de la palette (Gilbert 12, capitales) · **la jauge de teinte**.
- Les 24 palettes et leurs tons : `ETAT-30-SEPTEMBRE-2026.md` §5. Défaut : **Ingénu** (sous Ingénu seulement, un Promi est bleu, un Chiche rose, un Cercle lilas).
- À chaque ouverture, la rangée, le nom et la jauge sont rebâtis : **on retire les anciens** et on repose dans l'ordre grille · nom · jauge (défaut C-057 de la « deuxième ouverture »).

### Actions
| Geste | Effet | Source |
|---|---|---|
| Glisser horizontalement sur la Toile (dès 34 px) | change de monde (suivant / précédent) | `lot-V7-STUDIO-COULEUR` en-tête, app.html:34092 |
| Toucher un point | va à ce monde | `poseDots`, app.html:22108 |
| **Appui maintenu 480 ms** sur la Toile, puis glisser | **le geste de couleur** : horizontal = la **teinte** (390 px pour un tour complet de 360°) ; vertical = la **palette** (48 px par palette) ; la valeur se calcule depuis l'origine du geste — on revient exactement d'où l'on vient en refaisant le chemin ; fonctionne dans **toutes les directions de départ** ; un vrai glissement avant les 480 ms l'annule (le changement de monde garde la main) | app.html:34070–34110 ; CLAUDE §3 bloc v126 (C-010) |
| Toucher un ton | ouvre le panneau des palettes | `poseTons`, app.html:22100 |
| Toucher une pastille de palette | applique la palette ; le nom suit | `redteam_palettes.py` |
| Jauge de teinte | décale la teinte de la palette | — |
| « ← Retour » | revient aux disques | `lot-NEUF-POINTS-js`, app.html:33559 |
| Disques sombre / clair | change le thème de l'app, d'un coup (sans fondu) | app.html:22058 |
| Disques avec / sans texte | affiche ou non les titres sur les dalles | idem |
| « Adopte ce design — 2 € » | achète ce monde ; toast « Design débloqué ✓ » | app.html:8567 ; CLAUDE §3 bloc v118 |
| Toucher un mur (monde verrouillé, gratuit) | la phrase du mur | `lot-V104-MURS` app.html:37144 |
| « ✕ FERMER » | accueil ; la Toile prend le monde et la palette choisis | — |

- Mondes gratuits (8) et de Ma Parole ! (12), dans l'ordre : `ETAT-30-SEPTEMBRE-2026.md` §4.
- Changer de **famille** de mondes ressème la Toile (CLAUDE §3 bloc v35).

### États vides et d'erreur
- Aucun état vide : l'aperçu est toujours coloré, même sans parole.
- Monde verrouillé : voir tableau.

### Textes exacts
« Le Studio » · « ✕ FERMER » · « en » · « sombre » · « clair » · « avec texte » · « sans texte » · « glisse pour changer de monde » · « reste appuyé pour changer de couleur » (à valider) · « ← Retour » · « Adopte ce design — 2 € » · toast « Design débloqué ✓ » · les vingt noms de mondes et les vingt-quatre noms de palettes (ETAT §4, §5).

### Sources
`lot-STUDIO-PLATEAUX-css`, `lot-STUDIO-PLATEAUX` (app.html:21720–22467) · `lot-V7-STUDIO-COULEUR` (34070) · `lot-NEUF-POINTS-js` (33559) · `lot-V10-STUDIO` (34308) · `lot-V12` (34651) · `lot-V71-REOUVERTURE` (36804) · CLAUDE §3 blocs v118, v126, v133, §5 (« un réglage vit là où vit ce qu'il règle ») · `redteam_studio_geste.py`, `redteam_palettes.py`, `redteam_apercus.py`.

### Trous
- Le « Zzz » (mode nuit) devait prendre place au milieu de la ligne des disques : **non posé**, et la fonction est **coupée** (CLAUDE §3 blocs v118, v120). Ne pas le porter.
- Les cotes du panneau des palettes (place de la grille, taille des pastilles — 40 px selon CLAUDE §3 —, place du nom et de la jauge) n'ont pas été extraites (`lot-V10-STUDIO`, `lot-NEUF-POINTS`).
- Le décalage de 12 px du plateau du bas (« l'encart du bas du Studio vient s'aligner » sur la barre de Partager, `lot-CINQ-POINTS`, app.html:33840) : valeurs finales non relues — les cotes du tableau sont celles de `lot-STUDIO-PLATEAUX-css`.
- Le rotateur d'origine alternait trois libellés d'achat ; il est **figé** sur « Adopte ce design — 2 € ». ⚠ `ETAT-30-SEPTEMBRE-2026.md` §6 écrit encore « un monde à l'unité 1 € » : contradiction avec v118 (2 €) — CLAUDE.md prime sur ce point daté.
- Le parcours de paiement réel (StoreKit) : hors prototype.

---

<a id="13"></a>
## 13 · Partager

**Nom à l'écran** : « PARTAGER ». **Id interne** : `#shareScreen.sh-plein` ; cadre `#shcCadre` ; aperçu `#shWrap` / `#shCanvas` ; la ligne `#shcPeaufiner` ; le panneau `#shcPile` (classe `shc-ouvert`) ; sujets `#shMode` (`toile`, `mosaic` = Mon Folio, `pelote`).

### Accès
- Accueil → Partager (plateau) : sujet « Ma Toile ».
- Aura → « PARTAGER MA PELOTE » : sujet « Ma Pelote ».
- Fiche d'une parole / d'un Cercle → rond Partager : **Mon Folio réduit à cette parole** (ou aux paroles de ce Cercle), sans la Pelote ; ce que l'on avait choisi au partage est **rendu à la fermeture** et jamais sauvegardé entre-temps.
- **Le partage est entièrement gratuit** : aucun ✦, aucun flou, aucun mur sur cet écran.

### Éléments (`lot-PARTAGE-PLEIN-css`, app.html:25526 ; `lot-PARTAGE-PLEIN` 25780)
| Élément | Cotes | Détail |
|---|---|---|
| **L'image** | 0 → 844 : **l'image est l'écran**, entière | relevé : aperçu 316 × 562 centré (195 ; 393) pour le format Story |
| Plateau | 40 → 100 | « PARTAGER » + « ✕ Fermer » ; il ne part jamais |
| **La ligne** `#shcPeaufiner` | 342 × 62, y **686** → 748 (centre relevé 717) | dit où l'on en est : « {sujet} · {format} » (ex. « Ma Toile · Story ») + « › » ; ouverte : « Peaufiner » + « ‹ » |
| La barre | y **758** → 820 ; deux boutons 168 × 62, centres x 108 · 282 | « Inviter » · « Partager » |
| Panneau ouvert | la ligne monte à y 120 → 182 et devient la poignée ; le panneau va de 198 à 736 environ et **défile** ; l'image reste entière derrière ; la barre ne bouge pas | |
| Mot-marque de l'image `#shBadge` | relevé 71 × 17 vers (85 ; 656) | « Mon Promi » sur l'aperçu |

**Le panneau, dans l'ordre** (`lot-V13-PELOTE`, app.html:34999) :
1. « LE SUJET » — « Ma Toile » · « Mon Folio » · « Ma Pelote ».
2. « DANS L’IMAGE » (ex-« Ce qu'il montre ») — il n'y reste que « Promitteurs »… ⚠ lui-même retiré en v14 (« Promitteurs ne fait rien ici, il sort ») : voir Trous.
3. « QUELS PROMI » — ouvre la feuille « Afficher · masquer » : groupes « Cercles » (chaque Cercle, « N Promi ») et « Promesses » (chaque parole, « à qui · Cercle »), cases à cocher ; « ✕ Fermer ».
4. « LE FORMAT » — « Plein écran » (9:19.5 · immersif) · « Story » (9:16) · « Post carré » (1:1) · « Paysage » (16:9) · « Édito » (4:5) · « Définir » (Largeur / Hauteur, pas de 120, de 540 à 3840, rapport borné entre 0,42 et 2,5).
5. « LE FOND DE L’IMAGE » — « Sombre » · « Clair ».
6. « LE MOT-MARQUE » — **sorti** (masqué, v14).
7. « LE QR » — « QR ».
8. « LE TEXTE DES DALLES » — « Avec texte » · « Sans texte ».

**Les trois sujets** :
- **Ma Toile** : la Toile ; on pince pour zoomer (0,4 à 5), on glisse pour placer. La Pelote ne s'y ajoute pas.
- **Mon Folio** : la planche de ses dalles, **une case par parole** ; la Pelote peut y occuper un bloc de quatre cases, **déplaçable** : un doigt **immobile 380 ms** sur elle la prend (un doigt qui bouge de plus de 8 px avant ne prend rien), on la glisse, la planche se recompose autour. Un dessin masqué n'y est jamais emporté.
- **Ma Pelote** : la Pelote **seule**, au centre, sur le fond choisi, avec le mot-marque et le QR si on le veut. (On ne partage jamais son Noyau : ce serait partager des proportions.)

### Actions
| Geste | Effet | Source |
|---|---|---|
| Toucher la ligne | pose / retire le panneau | `lot-PARTAGE-PLEIN` |
| « Partager » | exporte l'image **par les mêmes peintres que l'aperçu** (l'image partagée EST l'aperçu), grand côté **3840 px** (jamais multiplié par la densité de l'écran), fichier « mon-promi.png », feuille de partage du système (titre « Mon Promi », texte « Ma composition Promi ») ; sinon téléchargement | app.html:7616 ; `lot-V15` 35207 |
| « Inviter » | feuille de partage du système avec le texte « Je tiens mes promesses sur Promi. Rejoins-moi : 3 Cercles offerts pour toi et pour moi. » et le lien `https://promi.app` ; sinon copie + toast « Invitation copiée » ; sinon toast « Invitation prête à partager » | app.html:7618–7625 |
| Pincer / glisser l'aperçu (Ma Toile) | zoom / déplacement de l'image | app.html:7632–7640 |
| « ✕ Fermer » | retour (accueil, ou la fiche d'où l'on vient avec ses choix rendus) | `lot-V117-PARTAGE-FICHE` |

### États vides et d'erreur
- Fiche d'un Cercle sans parole : le partage s'ouvre comme depuis l'accueil (`ouvrirPartage`, app.html:37597).
- ⚠ TROU : aperçu d'un Folio sans aucune parole — non relevé.

### Textes exacts
« PARTAGER » · « Ma Toile » · « Mon Folio » · « Ma Pelote » · « Peaufiner » · « Inviter » · « Partager » · libellés du panneau ci-dessus · invite sur l'aperçu « pince pour zoomer · glisse pour placer » · « Afficher · masquer » · « Cercles » · « Promesses » · le texte d'invitation ci-dessus · toasts « Invitation copiée », « Invitation prête à partager ».

### Sources
app.html:2597–2640 (structure) · app.html:7605–7641 · `lot-PARTAGE-FEUILLE` (22563) · `lot-PARTAGE-SANS-TRAIT` (24224) · `lot-PARTAGE-PLEIN*` (25526–26033) · `lot-V13-PELOTE` (34918) · `lot-V14-js` (35114) · `lot-V15` (35207) · `lot-V117-PARTAGE-FICHE` (37564) · `joignable-inventaire.md` (« Partager ») · `redteam_partage_fiche.py`, `redteam_pelote_partage.py`.

### Trous
- **« DANS L'IMAGE »** : v13 n'y laisse que « Promitteurs », v14 le retire ; v15 dit que « la rangée DANS L'IMAGE sort » sur Ma Toile. Ce que la rangée contient encore (un interrupteur de la Pelote dans Mon Folio ?) n'a pas été relevé au rendu.
- Le pied de l'image exportée : v15 dit que le mot-marque est « relevé sur l'aperçu lui-même » (plus « Mon Promi » en haut / « promi.app » en bas des fonctions d'origine) ; le dessin exact du mot-marque et du QR sur l'image n'a pas été extrait.
- La note d'invitation (« 3 Cercles offerts, pour toi et la personne invitée ») : le mécanisme de l'offre n'existe pas dans le prototype.
- Le sujet par défaut de la ligne au repos affiche le format courant ; le format par défaut (« Plein écran » ou « Story ») n'a pas été vérifié (l'inventaire montre un aperçu 9:16).

---

<a id="14"></a>
## 14 · Les Réglages

**Nom à l'écran** : « RÉGLAGES » (le S en couleur, il clignote). **Id interne** : `#settingsScreen`.

### Accès
- Accueil → Réglages (plateau). Défile sous le plateau. « ✕ Fermer » → accueil.

### Éléments, dans l'ordre (app.html:2759–2771, corrigé par `lot-V16`, `lot-V106-LEXIQUE-css`, `lot-V109-NOTIFS`, app.html:33325, 35436)
Rangées : pilules 342 × 64 (rayon = h ÷ 2, trait 2, marge intérieure 12), libellé à gauche, valeur à droite.

| Groupe | Rangée (id) | Libellé | Valeur | Toucher |
|---|---|---|---|---|
| « Toi » | le visage `#setAva` (78 × 78, centre (195 ; 218)) | — | — | choisir une photo de profil (sélecteur du système) ; une croix la retire (« Photo retirée » + « Annuler ») |
| | le prénom `#setNameInput` | — | le prénom, modifiable | saisie |
| — | `#openPlusTop` (342 × 90) | « Ma Parole ! » · « › » | — | ouvre l'offre. **Au payé** : la mention « Tu es Membre Ma Parole ! », sans lien |
| — | `#openStudio2` | « Le Studio » | « visuels & humeurs › » | ouvre le Studio |
| — | `#replayOnb` | « Revoir la présentation » | « rejouer › » | rejoue l'onboarding |
| « Partager » | `#setInvite` | « Inviter sur Promi » | « › » | l'invitation (même texte qu'au §13) |
| « App » | `#notifCard` | « Notifications » | « › » | ouvre la page Notifications |
| | `#privCard` | « Vie privée » | « privé & partagé › » | ouvre la page |
| « Données » | (sans id) | « Sauvegarde locale » | « active ✓ » · « enregistré HH:MM » · « indisponible ici » | — |
| | `#resetData` | « Réinitialiser mes données » | « effacer › » | confirmation (§26) |
| « Compte » | `#compteCard` (**seulement sans compte**) | « Garder ta Toile » | « › » | ouvre le panneau du compte (§2). Texte en **Atkinson 700**, d'un **ton de la palette retiré à chaque retour sur la page**, ≥ 4,5:1, jamais kaki |
| | `#logoutCard` | « Se déconnecter » | « › » | confirmation ; toast « À bientôt » |
| | `#delAccount` | « Supprimer mon compte » | — | confirmation |
| « Légal » | `#cguCard` | « Conditions d’utilisation » | « › » | page Légal |
| | `#polCard` | « Politique de confidentialité » | « › » | page Légal |
| | `#aboutCard` | « À propos » | « › » | page À propos |
| pied | — | « Tes Promi perso restent sur ton appareil. / Privé par défaut, partagé quand tu le choisis. Pas de pub. » | | |

- **Masquées** : « Langue » (`#langCard`), « Réinitialiser (test) » (`#resetApp`), les réglages de Ma Parole ! (ils vivent dans Peaufiner).

### États vides et d'erreur
- Stockage indisponible : « indisponible ici ».
- Après « Réinitialiser mes données » : toast « App réinitialisée » (app.html:3232) — ⚠ après la confirmation de `lot-V16` c'est « Données effacées » avec « Annuler » pendant 5 s (§26) ; les deux existent dans le code.

### Textes exacts
Tous ceux du tableau ; titres de groupe « Toi », « Partager », « App », « Données », « Compte », « Légal ».

### Sources
app.html:2759–2771 · `lot-REGLAGES-PROFIL` (21411) · `lot-V16` (35567 ; `arme()` ≈ 35875–35912) · `lot-V95-ACCUEIL-css` (36859–36865) · `lot-V106-LEXIQUE-css` (37414) · `lot-V109-NOTIFS` (37404) · `lot-V124-GARDER` (37640) · `joignable-inventaire.md` (« Réglages ») · `redteam_garder_toile.py`.

### Trous
- « Se déconnecter » et « Supprimer mon compte » s'affichent-ils sans compte ? Le code ne masque que « Garder ta Toile » quand le compte est fait (`arme()`), rien pour les deux autres. À décider avec Firebase.
- La valeur « privé & partagé › » de « Vie privée » et « visuels & humeurs › » du Studio sont d'origine ; non revalidées.
- Les positions y de chaque rangée ne sont pas données : l'écran défile, l'inventaire relève des coordonnées de rangées hors de la vue.

---

<a id="15"></a>
## 15 · Notifications

**Nom à l'écran** : « NOTIFICATIONS ». **Id interne** : `#notifScreen` ; état `promi_notifs2` `{datees, lair, heure, refus}`.

### Accès
- Réglages → « Notifications ». « ✕ Fermer » **revient aux Réglages**.
- **Jamais de demande de permission au lancement.**

### Éléments (`remplit()`, app.html:37382–37389)
| Rangée | Libellé | Sous-ligne | À droite | Toucher |
|---|---|---|---|---|
| 1 | « Mes paroles datées » | « un petit mot la veille » | interrupteur | bascule ; à l'activation : demande la permission du système |
| 2 (mur de Ma Parole !) | « Mes paroles en l’air » | « de temps en temps, une douce relance » | interrupteur | payé : bascule (et demande la permission) ; gratuit : flouté, la phrase du mur |
| 3 (mur) | « L’heure » | — | « le matin, vers 8 h » · « à midi » · « le soir, vers 19 h » | payé : passe à l'heure suivante (8 h → midi → 19 h) ; gratuit : 19 h, flouté |
| 4 (désactivée) | « Ce qu’on me lance » | « Chiches, invitations, réponses · bientôt » | interrupteur éteint | rien |

### La question à la plantation (`#rapQuestion`)
- **1,9 s après la plantation d'une parole DATÉE** (la sienne, en cours), sur l'accueil, sous le plateau : « Je te le rappelle ? » · « oui » · « pas besoin ».
- « oui » : active « Mes paroles datées » **pour toutes** les paroles datées, puis demande la permission du système.
- « pas besoin » : cette parole n'aura pas de rappel ; **deux « pas besoin » d'affilée, puis la question ne revient plus**.
- Elle s'en va seule au bout de **12 s** (sans compter comme un refus) ; elle se cache derrière un écran ouvert ; jamais pendant l'onboarding ; jamais si la permission a été refusée au système.

### Ce qui part, et quand
- **La veille**, à l'heure choisie (19 h au gratuit). Si la veille était déjà passée à la plantation : **le jour même**, à l'heure choisie.
- **Rien quand la date est passée.** **Une notification par jour au plus.** Aucune qui reproche, ni série, ni score.
- Paroles en l'air (Ma Parole !) : une au plus par semaine.
- App fermée, et tout ce qui vient d'une autre personne : attend Firebase.

### Textes exacts
- Titres / corps des notifications :
  - parole à soi, la veille — titre « Promi », texte « Demain, c’est « {titre} ». »
  - parole à quelqu'un, la veille — titre « « {titre} » », texte « Tu as promis ça à {Prénom}. Demain. »
  - Chiche, la veille — titre « Promi », texte « Ton Chiche à {Prénom} arrive demain. »
  - le jour même — titre « « {titre} » », texte « C’est aujourd’hui. »
  - en l'air — titre « Promi », texte « « {titre} » flotte toujours. Un de ces jours ? »
- Page : libellés du tableau. Question : « Je te le rappelle ? » · « oui » · « pas besoin ».

### Sources
`lot-V109-NOTIFS-css`, `lot-V109-NOTIFS` (app.html:37235–37413) · ETAT §7 · `redteam_notifs.py`.

### Trous
- (Relevé) `#rapQuestion` : x 24 · y 114 · 342 × 52, rayon 26, trait 2, la grammaire du bandeau « Garder ta Toile » ; Gilbert 13, capitales ; la question à gauche, « oui » et « pas besoin » à droite (app.html:37240).
- Les deux heures « 8 h » et « midi », et « une par semaine » pour l'en l'air, sont « à valider » dans le code.

---

<a id="16"></a>
## 16 · La langue

**Nom à l'écran** : « LA LANGUE ». **Id interne** : `#langScreen`.

### Accès
- ⚠ **Inatteignable aujourd'hui** : la rangée « Langue » des Réglages est masquée (`#langCard{display:none!important}`, app.html:35436 ; confirmé par `redteam_air.py` : « inatteignables dans l'app aujourd'hui : la langue »).

### Éléments (app.html:2731–2737, 3236–3255)
- Plateau : « La langue » + « ✕ Fermer ».
- « Promi te parle dans la langue que tu choisis. »
- Liste : « Français » · « English » · « Español » · « Deutsch » · « Italiano » · « Português » ; la langue choisie porte « ✓ ».
- Pied : « Le vocabulaire de Promi — Promi, Toile, Cercle, Fil, Aura — ne se traduit pas : c'est le même partout. »

### Actions
- Toucher une langue : la coche ; si ce n'est pas le français : toast « {Langue} arrive bientôt · Promi reste en français ».

### Trous
- Aucune décision ne dit si l'écran revient au portage : **ne pas le porter sans demander**.

---

<a id="17"></a>
## 17 · La confidentialité (« Vie privée »)

**Nom à l'écran** : « VIE PRIVÉE » (la rangée des Réglages s'appelait « Confidentialité » ; elle est renommée « Vie privée », `lot-V16`). **Id interne** : `#privScreen`.

### Accès
- Réglages → « Vie privée ». « ✕ Fermer » revient.

### Éléments (app.html:2741–2755)
| Élément | Texte | Valeur |
|---|---|---|
| Plateau | « Vie privée » + « ✕ Fermer » | |
| Phrase | « Privé par défaut. Partagé seulement quand tu le choisis. » | |
| Ligne | « Tes Promi » | le nombre (`#pvCount`) |
| Ligne | « Tes Promi perso » | « privés sur ton appareil » |
| Ligne | « Ce que tu partages » | « synchronisé pour tes proches » |
| Ligne | « Compte » | « seulement si tu partages » |
| Ligne | « Traceurs » | « aucun » |
| Bouton `#pvExport` (342 × 54, centre y 525) | « Exporter mes données » | « copier › » |
| Bouton `#pvReset` (342 × 54, centre y 585) | « Tout effacer » | « effacer › » |
| Pied | « Tes Promi perso restent sur ton téléphone. Ce que tu déposes dans un Cercle est partagé avec ses membres — rien d'autre ne sort. » | |

### Actions
- « Exporter mes données » : copie les données dans le presse-papier ; toast « Tes données sont dans le presse-papier » ; échec : « Copie impossible ici ».
- « Tout effacer » : confirmation « Tout effacer ? » (§26), puis « Tout est effacé » avec « Annuler » 5 s, puis tout est effacé et l'app repart de zéro.

### Sources
app.html:2741–2755, 3274–3277 · `lot-V16` (≈ 35902–35912) · `joignable-inventaire.md` (« Vie privée »).

### Trous
- La forme de l'export (JSON brut dans le presse-papier) est celle du prototype ; le format à porter n'est décidé nulle part.

---

<a id="18"></a>
## 18 · Légal — Conditions, Politique

**Nom à l'écran** : « LÉGAL ». **Id interne** : `#legalScreen` (page bâtie par `lot-V16`).

- Accès : Réglages → « Conditions d’utilisation » ou « Politique de confidentialité ». « ✕ Fermer » ferme.
- Contenu : le titre de la page demandée (« Conditions d’utilisation » ou « Politique de confidentialité ») puis **« Bientôt disponible. »**
- Source : `_v16Legal`, app.html ≈ 35853–35856.
- ⚠ TROU : les deux textes n'existent pas (chantier juridique). « ✕ Fermer » revient-il aux Réglages ou à l'accueil ? Non vérifié (la page retire `.show` des Réglages à l'ouverture).

---

<a id="19"></a>
## 19 · À propos

**Nom à l'écran** : titre de page « PROMI ». **Id interne** : `#aboutScreen`.

### Accès
- Réglages → « À propos ». Défile. « ✕ Fermer ».

### Contenu, mot pour mot (`APROPOS`, app.html:35834 ; crédits ≈ 35858–35868)
**À propos**

Une promesse est une drôle de chose.

On se lance des « promis » toute la journée.

> « Promis, on se raconte tout. »
> « Promis, je te rends ça demain. »
> « Promis, cette fois, on le fait. »
> « Promis, on ne laisse pas tomber. »

Sur le moment, on le pense vraiment. Puis la vie passe par là, les jours s’empilent, et certaines paroles s’effacent. D’autres nous suivent pendant des années. Certaines n’arrivent même pas jusqu’à vendredi.

**Promi est né pour ces paroles-là.**

Planter une promesse, c’est en faire un **Promi**. Elle prend place sur la Toile, sous la forme d’une dalle de couleur. Une parole en devenir, puis une trace lorsqu’elle est tenue.

Un **Chiche**, c’est autre chose : tenter quelqu’un — ou soi-même — avec un peu plus d’élan. Une petite bravade.

Et quand plusieurs personnes ont quelque chose à vivre ensemble, un **Cercle** permet de mettre leurs Promi et leurs Chiches au même endroit : un week-end à Marseille, une virée, un projet, une soirée qui mérite de ne pas rester au stade du « on devrait ».

**Promi ne compte pas les promesses. Il leur donne une place.**

La Toile garde les paroles en cours comme celles qui ont été tenues. Elle devient peu à peu le paysage de tout ce qu’on a décidé de ne pas laisser tomber.

**Les lettres**

Le texte est composé en **Atkinson Hyperlegible**, créée pour le **Braille Institute** afin de rendre les caractères plus faciles à distinguer, notamment pour les personnes malvoyantes.

Les titres sont en **Gilbert**, créée dans le cadre de **Type With Pride** en hommage à **Gilbert Baker**, artiste et créateur du drapeau arc-en-ciel original.

Deux polices pour deux idées simples : rendre les choses lisibles, et leur donner de la couleur.

**Crédits**

- **Gilbert** — « Type With Pride, en hommage à Gilbert Baker. Copyright 2017, 2019 Ogilvy & Mather. Dessin : Robyn Makinson, Kazunori Shiina, Hayato Yamasaki. Distribuée sous licence Creative Commons Attribution – Partage dans les mêmes conditions 4.0 International (CC BY-SA 4.0) : creativecommons.org/licenses/by-sa/4.0. Glyphes non modifiés. Fournie telle quelle, sans garantie. » (le lien s'ouvre dans le navigateur)
- **Atkinson Hyperlegible Next** — « © 2020, 2024 Braille Institute of America, Inc. Noms de police réservés : Atkinson, Hyperlegible. Distribuée sous SIL Open Font License, version 1.1. » + un dépliant « Lire la licence (SIL OFL 1.1) » (le texte de la licence).
- « Promi · {version} » (prototype : « 0.16 »).

### Trous
- ⚠ Le texte dit « Les titres sont en Gilbert » alors que les titres d'écran sont en **PromiLate** (CLAUDE §6) ; PromiLate n'est pas créditée. À faire valider par Tom avant de porter (le crédit de Gilbert, lui, est **obligatoire**, CC BY-SA 4.0).

---

<a id="20"></a>
## 20 · L'offre Ma Parole ! (la page)

**Nom à l'écran** : « MA PAROLE ! » (« PAROLE » en couleur, « MA » et « ! » à l'encre). **Id interne** : `#plusScreen` ; cadre `#pcCadre` (390 × 844) ; `ouvreCercle()` ; ouverte par-dessus un Peaufiner : classe `cercle-dessus`.

### Accès
- Réglages → « Ma Parole ! » ; accueil → « PROMI » ; la première rencontre d'un mur (automatiquement, à la fin de la lecture de la phrase) ; un toucher pendant qu'une phrase de mur est affichée.
- **Au payé, rien n'ouvre plus cette page** (toutes les portes y passent par une seule garde).
- Ouverte depuis un mur, elle se pose **par-dessus** sans rien fermer : on retrouve l'écran où l'on était (la phrase en cours de la page + n'est pas perdue) ; l'achat ramène au même Peaufiner, réglages nets.

### Éléments (`lot-CERCLE-TOILE-css`, app.html:31652–31720 ; `bati()` 32270–32300)
| Élément | Cotes | Texte / détail |
|---|---|---|
| « ✕ Fermer » | centre (296 ; 70) | |
| La Toile qui vend `.pc-toile` | x 22 · y 98 · 346 × 206 | un pavage serré de vraies dalles des **douze mondes payants**, sans cellule vide ; une dalle change de matière toutes les 4,5 s (mue de 0,9 s) |
| Titre `.pc-h` | x 49,5 · y 336 · largeur 291 ; PromiLate 32 | « MA PAROLE ! » |
| Sous-titre `.pc-sub` | y 382 | « Retourne ta Toile » |
| Trois arguments `.pc-arg` | y 434 · 488 · 542 ; x 49,5, largeur 291 | « L’autre moitié de ta Toile » / « ce que tes proches tiennent envers toi » · « Chaque parole se peaufine » / « récurrence, rappel, importance, mémoire » · « Ta Toile change de matière » / « Douze mondes de plus, les couleurs du dessin » |
| Prix `.pc-prix` | y 612 | « 39 € / AN » (« AN » deux fois et quart plus petit) · « soit 3,25 €/mois » |
| Bouton principal `#buyMonth` | 346 × 58, centre (195 ; 709) | « Essayer 14 jours » · « › » (un éclat le traverse) |
| Option `#buyYear` | 346 × 44, centre (195 ; 778) | « Bon, allez d’accord — 39 € / an » |
| Petite ligne `.pc-mois` | sous les deux boutons | « ou 5,99 € par mois » |
| Mention `.pc-legal` | en bas | « Sans engagement · résiliable à tout moment » |

### Actions
- « Essayer 14 jours » / « Bon, allez d’accord — 39 € / an » : passe Membre (dans le prototype : immédiat) ; toast « Tu es Membre Ma Parole ! · Cercles illimités » ou « Tu es Membre Ma Parole ! ✓ · tout Promi débloqué ».
- « ✕ Fermer » : revient d'où l'on vient.

### Ce que Ma Parole ! ouvre (ETAT §6)
L'autre moitié de la Toile (ce qu'on te tient), la récurrence, le rappel à l'heure choisie, l'importance, la mémoire des paroles en l'air, la couleur de la dalle, douze mondes, les Cercles illimités, les couleurs du dessin.

### Sources
`lot-CERCLE-TOILE-css`, `lot-CERCLE-TOILE` (app.html:31632–32325) · `lot-CERCLE-MUR` (31439) · `lot-V12` (34651) · `lot-V74-CERCLE-PAYE` (36787) · app.html:3164, 3182, 31578 · ETAT §6 · `joignable-inventaire.md` (« le Cercle »).

### Trous
- La limite de Cercles au gratuit (« Cercles illimités » au payé) : le nombre n'a pas été trouvé (cherché « illimités »).
- Le texte d'origine de la page (« Essaie tout, sans t'engager. », « ou un design à l'unité — 1 €, ou 4 pour 3 € », app.html:2783–2794) est recouvert par `pcCadre` ; s'il reste visible sous le cadre n'a pas été vérifié — **ne porter que le tableau ci-dessus**.
- Le parcours d'achat réel (essai de 14 jours, StoreKit, restauration) : hors prototype.
- ⚠ `ETAT` §6 dit « l'écran qui vend : bouton principal « Essayer 14 jours », option « Bon, allez d'accord — 39 € / an » » : cohérent.

---

<a id="21"></a>
## 21 · Les murs de Ma Parole !

**Id interne** : `lot-V104-MURS` ; la phrase `#murPhrase` ; compteur `promi_murs` `{n, t, der, decouvert}`.

### Où sont les murs (gratuit seulement — `murs()`, app.html:37140–37150)
1. Le bloc des cinq réglages dans **Peaufiner** d'une fiche (Promi, Chiche) et de la page +.
2. « LA COULEUR » dans le Peaufiner d'un Cercle.
3. « **Ce qu’on t’a tenu** » dans l'Aura.
4. Les deux cartes « Avec Ma Parole ! » de l'aide de l'Aura.
5. « Mes paroles en l’air » et « L’heure » dans Notifications.
6. La zone des teintes du **mode dessin** (le panneau COULEUR).
7. Au **Studio**, sur un monde verrouillé : les tons, les disques, les mots, les points du plateau du bas.

### Règles
- Un réglage réservé est **flouté à 4,8 px**, sans encart, sans explication, **sans prise** (rien de flouté ne s'ouvre). **Le Studio garde ses propres flous** (1,4 px sur la Toile d'un monde verrouillé) : « on doit voir le monde pour avoir envie de l'acheter ».
- Un mur se reconnaît à sa **géométrie** : le toucher tombe dans son rectangle.
- **Au toucher** : une phrase paraît **au centre du mur touché, sur le flou, seule** — ni plateau, ni fond, ni cadre. Gilbert 700 ; **38 px**, réduite par pas de 1 jusqu'à tenir en **trois lignes** au plus et dans la hauteur visible du mur (plancher 20) ; largeur ≤ 342 ; centrée ; **encre `#201908` sur clair, crème `#F7F0DE` sur sombre**, une seule taille ; elle monte de 8 px en 0,45 s.
- Si le mur n'est pas assez à l'écran, **son conteneur** défile pour l'amener au centre, puis la phrase se pose.
- Elle reste **le temps d'être lue** : `1,4 s + 60 ms par caractère`, bornée entre **3 s et 5,5 s**, puis s'efface.
- **La toute première fois**, l'offre s'ouvre automatiquement à la fin de la lecture. **Ensuite**, tant que la phrase est là, **un toucher n'importe où** ouvre l'offre (pas dans les 450 ms qui suivent son apparition).
- **Compteur global** (toutes zones) : les dix-huit phrases **dans l'ordre**, puis **au hasard sans répéter la précédente** ; remis à zéro après **14 jours** sans toucher un mur (à valider).
- **Les mots en orange** : dans chaque phrase, seuls les mots listés prennent l'orange de Ma Parole ! — `#FB4C0D` ; `#FF7A55` sur les corps sombres de Peaufiner d'un Chiche et d'un Cercle ; **`#FED0C3`** sur le corps sombre d'un Promi (`#0E78F2`, v134 : même teinte, éclaircie jusqu'à 3,01:1). « ! » n'apparaît que dans « Ma Parole ! ».
- Au payé : aucun mur, aucune phrase.

### Les dix-huit phrases, mot pour mot (`TEXTES`, app.html:37116–37134) — entre crochets : les mots en orange
1. « Eh non. Mais avec Ma Parole !, oui. » [Ma Parole !]
2. « La solution commence par Ma et finit par Parole ! » [Ma] [Parole !]
3. « Toujours non. Ma Parole !, toujours oui. » [Ma Parole !] [oui]
4. « Je vois bien que ça te titille. Ma Parole ! aussi. » [Ma Parole !]
5. « Tiens tiens, on dirait que ça commence à t’intéresser… » —
6. « Tiens tiens. Vous ici. » —
7. « Tu sais où trouver Ma Parole ! maintenant. » [Ma Parole !]
8. « On maintient cette position officielle, alors ? » [officielle]
9. « Allons bon. Nous y voilà à nouveau. » —
10. « Entre nous, le mystère s’amenuise. » [mystère]
11. « Les pourparlers se prolongent, je vois. » [pourparlers]
12. « Tu peux continuer. Je tiens le registre. » [registre]
13. « Ici, tout restera entre nous. » —
14. « Je commence à soupçonner une stratégie. » [stratégie]
15. « On pourrait presque en faire une tradition. » [tradition]
16. « Regarde-nous, avec nos petites habitudes. » [habitudes]
17. « Dis donc, tu viendrais presque pour moi. » [moi]
18. « On se retrouve ici tout à l’heure ? » —

Les mots en orange sont cherchés **dans l'ordre**, chacun après le précédent : dans la phrase 3, le « oui » coloré est celui qui suit « Ma Parole ! » (le dernier mot) ; dans la phrase 2, « Ma » puis « Parole ! ».

### Sources
`lot-V104-MURS-css`, `lot-V104-MURS` (app.html:37061–37234) · CLAUDE §3 blocs v104–v105, v112, v122, v131, v133 · ETAT §6 · `MA-PAROLE-PHRASES.md` (les 21 phrases d'avant, histoire) · `redteam_murs.py`, `redteam_maparole.py`.

### Trous
- Aucun propre aux murs ; la valeur « à valider » est signalée ci-dessus (14 jours).

---

<a id="22"></a>
## 22 · La fiche d'une personne

**Nom à l'écran** : le prénom. **Id interne** : `#personSheet` ; cadre `#psCadre` (390 × 844) ; `openPerson(nom)`.

### Accès
- Depuis : un Noyau de l'Aura, un Noyau d'une fiche. Mène à : fiche d'une parole (une carte, une dalle), page + (deux boutons).

### Éléments (`openPerson`, app.html:31245–31283) — la colonne défile sous le plateau
| Élément | Cotes | Détail |
|---|---|---|
| Plateau | 24 / 40 / 342 × 60 | le prénom (700) + « ✕ Fermer » |
| Le Noyau | x 24 · y 124 · Ø 58, trait 6 | piste neutre, trois arcs d'état (tenu · en cours · à tenir) calculés sur **toutes les paroles partagées** (elle est « à qui », « de qui », ou « avec ») ; le visage au centre ; **aucun chiffre** |
| La légende | x 100 · y 145 | « tenues » · « en cours » · « à tenir » — seulement s'il y a des paroles |
| « Tenu ensemble » | titre à y 214 ; cellules à partir de y 244, pas horizontal 117 (x 24 · 141 · 258), pas vertical 101 | une cellule par parole tenue : la vraie dalle (boîte 105 × 56) + son titre ; absent s'il n'y a rien de tenu |
| « Ce que tu partages avec {Prénom} » | 32 sous le bloc précédent ; titre + 30 | les paroles partagées en **vraies cartes d'Index**, trois par ligne (106 × 133) ; la ligne du bas de chaque carte **n'écrit plus l'état** (le trait le dit) : elle garde le temps quand l'app le sait, et le nom du Cercle de la parole en capitales |
| Deux boutons | 167 × 62, x 24 et 199 ; y = max(760, bas du contenu + 28) (relevé : centre y 791) | « + Planter un Promi » · « + Lancer un Chiche » |

### Actions
- Toucher une carte ou une dalle tenue : la fiche de la parole.
- « + Planter un Promi » : page + en Promi, **« Je promets … à {Prénom} » déjà posé**.
- « + Lancer un Chiche » : page + en Chiche, « à {Prénom} » déjà posé.
- « ✕ Fermer » : retour.

### États vides et d'erreur
- Personne sans aucune parole partagée : le Noyau (piste neutre seule), pas de légende, aucun des deux blocs, les deux boutons à y 760.

### Textes exacts
« Tenu ensemble » · « Ce que tu partages avec {Prénom} » · « + Planter un Promi » · « + Lancer un Chiche » · « tenues » · « en cours » · « à tenir ».

### Sources
`lot-FICHE-PERSONNE-CSS`, `lot-FICHE-PERSONNE` (app.html:31080–31285) · `lot-PERSONNE-AVEC` (31066) · `lot-CHEMINS-PERSONNE` (31344) · `joignable-inventaire.md` (« personne »).

### Trous
- La fiche de **soi** (toucher le Noyau « Toi ») : comportement non relu (`_isMe` existe ; s'ouvre-t-elle ?).
- Tout le reste de l'ancienne fiche (mot d'harmonie, compte, courbe, second anneau, équilibre) est **sorti sans remplacement** : ne pas le porter.

---

<a id="23"></a>
## 23 · Le menu du bouton photo

**Id interne** : `.ph-photo-btn` (le rond, 34 × 34) ; `.ph-photo-menu.dz-compact` ; `_photoMenu`.

### Accès
- Le bouton photo d'une **fiche** (Promi, Chiche), de la **page +** (Promi, Chiche, Cercle) et d'une **fiche de Cercle**. Le rond est à x centre 349.

### Éléments
- Le menu se pose **au-dessus du bouton, à sa gauche**, aligné à droite sur la marge (x 366) ; **compact** : chaque ligne est une pastille de **33 de haut**, rayon 17, trait 2, texte Gilbert 13 en capitales ; **4 px** entre deux.
- Lignes, de haut en bas (une ligne n'existe que si elle a un sens) :
  1. « Dessiner » — toujours en tête.
  2. « Retirer le dessin » — s'il y a un dessin (posé ou en cours). ⚠ ordre exact entre 1 et 2 : voir Trous.
  3. « Importer une photo » — sur une parole (fiche, page +).
  4. « La dalle d’origine » — sur une parole plantée ; devient « La dalle du Studio » quand l'option est active.
  5. « Retirer la photo » — s'il y a une photo.
- Relevé sur une fiche sans photo ni dessin : « Dessiner » (94 × 33, centre (277 ; 262)) · « Importer une photo » (171 × 33, centre (238 ; 299)) · « La dalle d’origine » (162 × 33, centre (243 ; 336)) ; le rond à (349 ; 335).
- Sur la fiche d'un Cercle : « Dessiner » (et « Retirer le dessin »).

### Actions
| Ligne | Effet |
|---|---|
| « Dessiner » | ouvre le mode dessin (§24) |
| « Importer une photo » | ouvre le **sélecteur du système**, dans le geste ; la photo remplace la dalle dans la bande (une promesse n'a pas deux visages : la photo vaut aussi sur les cartes et au partage) |
| « La dalle d’origine » | la dalle de CETTE parole est rendue dans le monde, la forme et la couleur **de sa plantation**, partout où elle paraît seule (fiche, cartes, partage) ; la Toile ne bouge pas ; retire la photo ; la bande haute prend alors la couleur d'origine, **sauf si elle se confond avec le champ (ΔE < 15) : alors la rampe de la nature** |
| « La dalle du Studio » | revient au défaut : la dalle suit le monde et la palette du Studio |
| « Retirer la photo » | rend la dalle |
| « Retirer le dessin » | rend la dalle (ou la photo) |
| Toucher ailleurs, ou retoucher le rond | referme le menu |

### Sources
`lot-V117-PHOTO-MENU-css`, `lot-V117-PHOTO-MENU` (app.html:37433–37532) · `lot-V118-ORIGINE` (37533) · `lot-V132-DESSIN-css` (38016–38018), `lot-V132-DESSIN` (≈ 38290–38310) · `lot-PHOTO` (20041) · `joignable-inventaire.md` (« menu photo ») · CLAUDE §3 blocs v118, v128, v132, v133 · `redteam_photo_menu.py`, `redteam_origine.py`.

### Trous
- L'ordre exact de « Retirer le dessin » par rapport à « Dessiner » (le code ajoute « Retirer le dessin » avant d'appeler l'ajout de « Dessiner » marqué « en tête ») : à vérifier à l'écran.
- Le **symbole** du rond attend le choix de Tom (C-060).
- Pièces acceptées, recadrage et poids d'une photo importée : non relevés.

---

<a id="24"></a>
## 24 · Le mode dessin

**Nom à l'écran** : aucun (VoiceOver : « Dessiner »). **Id interne** : `#dessinMode` (couche pleine dans `#device`, z au-dessus de tout sauf « voir en entier ») ; paramètres `window._dessinParams` ; API `window._dessin`.

### Accès
- Menu du bouton photo → « Dessiner » : fiche d'une parole, page + (Promi, Chiche, Cercle), fiche d'un Cercle.
- Sortie : « POSER », ou le ✕ (sans poser) ; **sans fondu** ; la fiche dessous n'a pas été touchée (retour exact).
- Si l'offre s'ouvre depuis le mur des couleurs, on sort du mode (dessin gardé).

### Éléments (v132 corrigé par v133 ; `P`, app.html:38036–38050)
| Élément | Cotes | Détail |
|---|---|---|
| **La surface de dessin** | 390 × **742** (y 0 → 742) : `844 − 34 (zone de sécurité du bas) − 12 − 44 − 12` | fond = le fond du dessin ; **rien ne s'y superpose** sauf le ✕ |
| Contour de l'encart du haut | 24 / 40 / 342 × 60, rayon 30, **trait fin 1 px**, sans fond ni texte | il ne reste que le contour |
| **✕** « Quitter le dessin » | 44 × 44 à x 307 · y 48 (l'emplacement de « ✕ FERMER ») ; croix de 18 | sort **sans poser** ; le dessin en cours est gardé |
| **La rangée d'outils** | hauteur 44 ; y 754 → 798 (12 sous la surface, 12 au-dessus du bord bas utile à 810) ; marges de côté 24 | de gauche à droite, disques de 44 au pas de **58** : **PLUME** (x 24) · **GOMME** (x 82) · **ANNULER** (x 140) · **COULEUR** (x 198) ; à droite **POSER** (pilule 104 × 44, x 262 → 366) |
| Déploiement des tailles | pilule 118 × 44, **16** au-dessus de la rangée, au-dessus de l'outil concerné | trois points côte à côte, de taille croissante, à l'encre du mode : « Fin » · « Moyen » · « Gros » |
| Déploiement des couleurs | panneau x 24 · 342 × 114, rayon 30, 16 au-dessus de la rangée | deux onglets « TRAIT » · « FOND » (159 × 44 chacun ; « FOND » disparaît après le premier POSER, « TRAIT » occupe alors 326) ; dessous, les teintes : disques de 44 |

- Disque d'outil : trait 2 à l'encre du mode, fond le corps ; choisi : plein (encre) ; indisponible : contour **pointillé**.
- Couleurs du mode : le corps est celui de l'écran d'où l'on vient ; l'encre celle qui s'y lit.
- **La loi des points** : seuls les trois points du choix de taille y échappent (CLAUDE §5).

### Actions
| Geste | Effet |
|---|---|
| Tracer au doigt (ou au stylet) sur la surface | un trait plein, opaque, à bords nets, **effilé E2** : début + 38 %, fin effilée sur le dernier quart ; plus fin quand le geste est rapide (jusqu'à − 28 %) ; la pression d'un stylet module la largeur ; jamais sous 1 pt |
| Toucher PLUME / GOMME | la choisit ; **un second toucher** déploie ses trois tailles (plume : 2,5 · 4,5 · 8 pt ; gomme : 10 · 18 · 30 pt) ; le choix fait, le déploiement se replie |
| Gomme | rend le fond |
| ANNULER | retire le dernier trait (indisponible s'il n'y en a pas) |
| COULEUR | déploie / replie le panneau. **Avec Ma Parole !** : onglet TRAIT → la couleur des traits à venir (les tons de la palette ; celui du fond est barré) ; onglet FOND → le fond du dessin. **Sans Ma Parole !** : le panneau est un **mur** (flouté 4,8 px, rien ne s'y choisit, la phrase du mur monte dessus) ; on dessine **à l'encre du mode sur le champ de la nature** |
| **POSER** | pose le dessin (`poses` = copie des traits, `pose = true`, démasqué) et sort ; POSER sans aucun trait retire le dessin |
| ✕ | sort sans poser ; les traits en cours sont gardés pour la prochaine fois |

### Le modèle (à porter tel quel — `A-INTEGRER.md` C-042)
- **Un dessin est une liste de traits, jamais une image** : `{fond, traits:[{c, t, g, pts:[x, y, t, p …]}], poses:[…], pose, masque}`, en points sur la surface.
- `c` = la couleur du trait (un hex, **figée** : changer de palette ne touche que les traits à venir) ; `t` = la taille ; `g` = 1 pour la gomme ; `pts` = position, temps, pression.
- `traits` = le dessin en cours ; `poses` = ce que POSER a posé — **la bande, la vue entière et le partage ne montrent que lui**.
- **Après le premier POSER, le fond est fixé** et les nouveaux traits ne prennent que **les couleurs déjà présentes**.
- Rangement : sur la parole (`p.dessin`, sauvegardé avec elle) ; sur le brouillon de la page + (il suit la parole ou le Cercle à la plantation) ; par Cercle.
- En Swift : pas de `PKCanvasView` tel quel ; un rendu à soi (chemins remplis), le même modèle de largeur.

### États vides et d'erreur
- Aucun trait : ANNULER en pointillé ; POSER retire le dessin.

### Textes exacts
« Poser » (affiché en capitales) · « Trait » · « Fond » (onglets, capitales). VoiceOver : « Dessiner » · « La surface de dessin » · « Les outils du dessin » · « Plume » (choisie : « Plume, choisie. Toucher de nouveau pour la taille ») · « Gomme » (idem) · « Annuler le dernier trait » · « Couleur » · « Poser le dessin » · « Quitter le dessin » · « La taille de la plume » / « La taille de la gomme » · « Fin » · « Moyen » · « Gros » · « Les couleurs du dessin » (gratuit : « Les couleurs du dessin, avec Ma Parole ! ») · « La couleur du trait » · « La couleur du fond » · « Trait, teinte N sur M » (+ « , c’est la couleur du fond ») · « Masquer le dessin » / « Afficher le dessin ».

### Sources
`lot-V132-DESSIN-css`, `lot-V132-DESSIN` (app.html:37976–38330) · CLAUDE §3 blocs v127–v133, §5 (loi des points) · `portage/A-INTEGRER.md` (C-042, v133) · `redteam_dessin.py` (79 contrôles, huit sondes).

### Trous
- Le modèle de largeur exact (`largeurs` : la loi de l'effilé, du lissage, de la vitesse) est dans `lot-V132-DESSIN` : non recopié ici — à extraire dans le document du dessin.
- Le symbole de l'outil COULEUR (« S2, celui du Studio ») et les icônes plume / gomme / annuler : tracés SVG non recopiés.
- **C'est un geste : la validation de Tom au doigt sur iPhone est obligatoire** (CLAUDE §3 bloc v132) ; tout est « FAIT, EN ATTENTE DE TOM ».
- Le nombre et l'ordre des teintes proposées (`choixTrait`, `choixFond`, `palette`) : non relevés.

---

<a id="25"></a>
## 25 · Voir en entier

**Nom à l'écran** : aucun (VoiceOver : « La photo en entier » / « Le dessin en entier »). **Id interne** : `#entierVue` (couche pleine dans `#device`).

### Accès
- Sur une fiche, **toucher la bande quand elle porte une photo ou un dessin posé et non masqué** — jamais une dalle. Le toucher doit tomber sur ce que la bande **peint** (au-dessus de l'onde), et sur rien d'autre (ni le plateau, ni le bouton photo, ni un menu, ni un texte).
- En SwiftUI : `fullScreenCover` sans transparence (`A-INTEGRER.md` C-051).

### Éléments
- Un fond **plein**, la seiche (`--c-seiche10`, `#050302`) — ni transparence, ni ombre, ni fondu.
- L'image **entière**, sans recadrage (`contain`), par-dessus tout l'appareil : on y voit ce que la bande recadrait.
- « ✕ FERMER » en haut à droite (à 24 du bord, y 40, hauteur 60 ; Gilbert 13, capitales, crème).

### Actions
- Un nouveau toucher n'importe où, ✕, la touche Échap / Entrée / Espace, ou `closeAll` : referme. La fiche dessous est **intacte**.

### Accessibilité
- La bande ne se déclare commande que lorsqu'elle porte une photo ou un dessin : « Voir la photo en entier » / « Voir le dessin en entier ».
- Texte de remplacement de l'image : « La photo de cette parole, en entier » / « Le dessin de cette parole, en entier ».

### Sources
`lot-V131-ENTIER-css`, `lot-V131-ENTIER` (app.html:37888–37963) · CLAUDE §3 bloc v131 · `redteam_entier.py`.

### Trous
- Le dessin vu en entier est rendu à l'échelle 3 depuis la liste des traits (`sourceVue`, app.html:38323) ; un Cercle ne porte pas de photo aujourd'hui.

---

<a id="26"></a>
## 26 · Confirmations, « Annuler », toasts, bandeaux

### La confirmation (`conf`, `lot-V16`)
Une boîte modale (`alertdialog`) : un titre, un texte, deux boutons (refus à gauche, action à droite) ; toucher hors de la boîte la ferme.

| Titre | Texte | Refus | Action | Suite |
|---|---|---|---|---|
| « Supprimer ce Promi ? » | « « {titre} » quitte ta Toile. » | « Garder » | « Supprimer » | la dalle part avec l'animation de départ de son monde ; « Promi supprimé » + « Annuler » |
| « Supprimer ce Chiche ? » | idem | « Garder » | « Supprimer » | « Chiche supprimé » + « Annuler » |
| « Supprimer ton compte ? » | « Tous tes Promi seront effacés de cet appareil. » | « Garder » | « Supprimer » | ⚠ suite non relue |
| « Se déconnecter ? » | « Tes Promi restent sur cet appareil. » | « Rester » | « Se déconnecter » | toast « À bientôt » |
| « Réinitialiser tes données ? » | « Tous tes Promi seront effacés de cet appareil. » | « Garder » | « Effacer » | « Données effacées » + « Annuler », l'effacement n'a lieu qu'après 5 s |
| « Tout effacer ? » | idem | « Garder » | « Effacer » | « Tout est effacé » + « Annuler », puis redémarrage |

### « Annuler » (`annulable`)
Un bandeau : le message + le bouton « Annuler » ; il reste **5 s**. « Annuler » remet l'état d'avant (la dalle revient sur la Toile). Messages : « Promi supprimé » · « Chiche supprimé » · « Photo retirée » · « « {nom} » dissoute » · « Données effacées » · « Tout est effacé ».

### Les toasts (`toast`, app.html:6461) — texte seul, ou avec un à trois boutons
| Texte | Boutons | Quand |
|---|---|---|
| « gardé de côté — dans l'Index » | — | « garder de côté » sur la page + |
| « Donne un nom à ton Cercle » | — | Cercle lancé sans nom |
| « {N} Promi plantés » | — | Cercle lancé avec ses premiers Promi |
| « Promi planté sur la Toile » | — | app.html:3806 — ⚠ contexte non relu |
| « Reporter… » | « +1 j » · « +3 j » · « +1 sem » | REPORTER dans le Fil |
| « Dissoudre « {nom} » ? » (ou « Dissoudre le Cercle ? ») | « Libérer les Promi » · « Tout supprimer » | DISSOUDRE LE CERCLE |
| « Belle série — partage ton Noyau » | « Partager » | après une parole tenue (⚠ mot à valider, §5) |
| « Tu es Membre Ma Parole ! · Cercles illimités » | — | achat |
| « Tu es Membre Ma Parole ! ✓ · tout Promi débloqué » | — | achat |
| « Design débloqué ✓ » | — | achat d'un monde |
| « Invitation copiée » · « Invitation copiée · promi.app » · « Invitation prête à partager » | — | Inviter |
| « Tes données sont dans le presse-papier » · « Copie impossible ici » | — | Exporter mes données |
| « {Langue} arrive bientôt · Promi reste en français » | — | La langue (écran inatteignable) |
| « App réinitialisée » | — | réinitialisation |
| « À bientôt » | — | déconnexion |

### Le bandeau « Garder ta Toile » (`#accRappel`, `lot-ONB-V20` app.html:36640–36672)
- Sur l'accueil : x 24 · y 114 · 342 × 52, rayon 26, trait 2 ; deux mots : « GARDER TA TOILE » (à gauche) et « PLUS TARD » (à droite), Gilbert 13, capitales.
- Il paraît **tant qu'aucun compte n'existe**, jamais pendant l'onboarding, jamais par-dessus un écran ouvert : la première fois après la **troisième parole** ou **deux jours** d'usage ; après chaque « Plus tard », plus loin : **5, puis 10, puis 20** nouvelles paroles, ou **3, puis 7, puis 14** jours (le premier des deux).
- « Garder ta Toile » : ouvre le panneau du compte (§2) sur un voile sombre à 50 %. « Plus tard » : le range.
- Il cède la place à la question « Je te le rappelle ? » quand elle est là.

### Sources
`lot-V16` (app.html ≈ 35750–35912) · app.html:6461 · `lot-ONB-V20-css` (36207–36229), `lot-ONB-V20` (36640–36678).

### Trous
- La géométrie et le dessin du toast, de la boîte de confirmation et du bandeau « Annuler » (`.v16-conf-p`, `.v16-toast`, `#_toast`) : CSS non extrait.
- « Promi planté sur la Toile » : chemin qui l'affiche non identifié.

---

<a id="27"></a>
## 27 · Récapitulatif des trous

| # | Écran | Trou |
|---|---|---|
| 1 | tous | v134 n'était pas commité à l'écriture : numéros de ligne d'`app.html` à quelques lignes près ; `ETAT-30-SEPTEMBRE-2026.md` §2 (corps-promi sombre) et §6 (1 € l'unité) sont en retard sur CLAUDE.md. |
| 2 | Accueil | Toile sans parole : le texte d'origine est masqué ; aucune décision sur ce qui s'y montre. |
| 3 | Accueil | Zoom mini / maxi et cadrage par défaut : dans le moteur, non extraits. |
| 4 | Accueil | C-058 : Toile sourde au doigt sous certains mondes — non reproduite, ouverte. |
| 5 | Onboarding | Les liens « Conditions » et « Politique » du panneau du compte n'ouvrent rien. |
| 6 | Page + | Formule exacte de la base du trait selon le nombre de lignes ; seuils du geste de plantation. |
| 7 | Page + | Achat d'un pinceau à 0,50 € : aucun parcours trouvé. |
| 8 | Page + | Contenu déplié de « INVITER » et « LES PROMI DU CERCLE » ; ce que plante une parole à l'objet vide. |
| 9 | Fiche | C-059 (corps clair d'une fiche Promi, filets en clair) non vérifié ; phrase lilas `#F4EEFF` à valider (Q403). |
| 10 | Fiche | Symbole du bouton photo (C-060) ; cadrage d'une photo dans la bande. |
| 11 | Fiche | Toucher sur le champ de message ; fiche d'une demande (« promets-moi ») ; réglages de Ma Parole ! au payé. |
| 12 | Instant | Valeurs de la célébration (seconde dalle amande) ; toast « partage ton Noyau » à valider. |
| 13 | Peaufiner | Contenu et fonctionnement au payé de RÉCURRENCE, RAPPEL, C'EST IMPORTANT ?, LA MÉMOIRE ; la relance. |
| 14 | Cercle | Amplitude de l'état posé (40 ou 36) ; table des mots d'état des lignes du fil ; « LA COULEUR » au payé. |
| 15 | Index | Quatre par ligne ; cotes internes d'une carte ; mots du temps au-delà de 7 jours ; « Manquées », « En suspens » à valider. |
| 16 | Fil | Correspondance type d'événement → gestes ; règle de la pastille de l'entrée FIL. |
| 17 | Aura | Grille de « Ce que tu as tenu » ; constantes du toucher de la Pelote. |
| 18 | Aide de l'Aura | Contradiction : « dans l'ordre où tu les as tenues » contre « la plus récente en premier » (v132). |
| 19 | Studio | Cotes du panneau des palettes ; décalage de 12 px du plateau du bas ; Zzz non posé et coupé ; ETAT §6 dit 1 € l'unité contre 2 € (v118). |
| 20 | Partager | Contenu de « DANS L'IMAGE » ; pied de l'image exportée ; format par défaut ; Folio vide. |
| 21 | Réglages | « Se déconnecter » et « Supprimer mon compte » sans compte ; positions des rangées. |
| 22 | Notifications | Heures (8 h, midi) et fréquence de l'en l'air « à valider » dans le code. |
| 23 | La langue | Écran inatteignable ; aucune décision. |
| 24 | Légal | Textes inexistants (« Bientôt disponible. ») ; retour de « ✕ Fermer ». |
| 25 | À propos | « Les titres sont en Gilbert » alors qu'ils sont en PromiLate. |
| 26 | Offre | Limite de Cercles au gratuit ; texte d'origine sous le cadre ; parcours d'achat réel. |
| 27 | Murs | Remise à zéro du compteur après 14 jours : « à valider ». |
| 28 | Personne | La fiche de soi. |
| 29 | Menu photo | Ordre « Dessiner » / « Retirer le dessin » ; contraintes d'une photo importée. |
| 30 | Dessin | Loi des largeurs ; icônes ; nombre et ordre des teintes ; validation de Tom au doigt en attente. |
| 31 | Confirmations | Dessin du toast, de la confirmation, du bandeau « Annuler » ; suite de « Supprimer ton compte » ; origine de « Promi planté sur la Toile ». |
| 32 | hors liste | Écrans d'origine présents dans le code et **non atteints** : l'écran des trois tuiles de la page +, « Fil d'actu » (`#feedScreen`), l'aperçu « Appliquer cette Toile » (`#previewScreen`), l'ancienne feuille de Cercle (`#essaimSheet`), « Mon Promi » (`#sealOv`), la carte de cellule (« Tenue · Reporter · Gérer › », `#cellCard`). Aucun n'est décrit ici : ne pas les porter sans décision. |
