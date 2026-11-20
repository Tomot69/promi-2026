# REPRISE — pour une session neuve (19 nov. 2026 : le chapitre v206 est clos et fusionné, main = v214b)

À lire avec `CLAUDE.md` (il fait autorité), `CHANTIERS.md` (le registre) et `QUESTIONS.md`. En tête de chaque session : `python3 serveur.py` (port 8752, IP relue par `ipconfig getifaddr en0`), donner les trois adresses.

## 0000) LOT 1 — L'ACCUEIL ET LA TOILE VIVANTE (20 nov. 2026, branche `app-L1`, C-322) — EN ATTENTE DE TOM

- L0 est clos (validé par Tom : plein écran, glissé entre les mondes ; CI verte). L'état embarqué : l'export de Safari de Tom du 20 nov. (2 paroles de test), copié dans `Promi-reference-v205/etat-de-tom/`.
- **Porté** : `promi/src/ecrans/accueil/` (plateau, barre, menu du +, bandeau « Garder ta Toile », symbole « recadrer » en flaques), le toucher d'une dalle (`ecrans/toile.ts`, `toucher-tolerant.ts`), le passage en flaques (`animation/flaques/passage.ts`), la navigation (`navigation/` : aucun écran destinataire au lot 1, la demande est notée). Identique au prototype au pixel à 390 × 844, clair et sombre, menu ouvert et fermé (`tests/rendu/accueil.spec.ts`) ; s'adapte (SE, 16e, 16 Pro Max, Android).
- **Pièges payés** : mémoire `portage-ecran-pieges` (l'outil duo, `navigator.webdriver`, le gel à 3 id, brun09 = seiche en sombre, le grain `#device::after`). Sur la CI (WebKit sans carte graphique) la Toile rend une image toutes les 0,7 s : les gestes se jugent à l'horloge de l'app, dans la page.
- **Pas encore portés en tests** : la plupart des juges du lot (liste dans PLAN-APP.md, lot 1 (d)). **C-323** : la limite de 44 pt de C-239 n'est pas appliquée par le prototype — décision de Tom.

## 000) NOUVEAU CHAPITRE : LA VRAIE APP (20 nov. 2026, lot L0, branche `app-L0`)

- **La vraie app vit dans `promi/`** (TypeScript strict, Vite, Capacitor iOS et Android). `npm run verifier` (jetons, types, lint, format, tests unitaires) ;
  `npx playwright test` (WebKit : banc_rendu porté, entrées du moteur, socle). L'intégration continue : `.github/workflows/ci.yml`. L'app s'adapte à chaque écran (Tom, L0 §2) : `tests/rendu/ecrans.spec.ts`.
- **Le plan des lots suivants : `PLAN-APP.md`** — ils attendent que Tom le valide. Les règles : en tête de CLAUDE.md et d'ARCHITECTURE.md.
- **Ce que L0 prouve** : banc_rendu porté, **266 images sur 266 identiques au pixel** (contre les images figées et contre le prototype vivant ; Ramage non jugé,
  C-187) ; sur l'état de Tom, les entrées du moteur identiques et la vue de son export retrouvée ; l'import de ses exports sans perte.
- **L'app « Promi » (`fr.autier.promi`) est sur l'iPhone 16e de Tom** (profil gratuit, 7 jours : PREUVE-CAPACITOR.md, « La vraie app sur l'iPhone »).
- `app.html` (main = v214b) est **figé** : le cahier des charges.

## 00) Le chapitre v206 est CLOS ET FUSIONNÉ (19 nov. 2026, v214)

- **`main` = v214**, commit de fusion `98e3762` (sur `ce8d9e1`) ; étiquette **`avant-fusion-v206`** = `main` d'avant (ec27c77, v205). La branche `v206` est gardée, identique. Le serveur sert `main` ; `?diag=1` affiche « v214 » en haut de chaque écran.
- **Ce que le chapitre a livré (v206 → v214)** : le prototype devenu la référence (`reference-v205`, VALIDATION.md, ARCHITECTURE.md, ASSAINISSEMENT.md) ; **Capacitor retenu** (preuve sur la branche `preuve-capacitor`, « Promi preuve » installée sur l'iPhone 16e de Tom) ; C-282 à C-318 au registre. Les règles de méthode R1–R4 et « la vraie app sera propre » sont en tête de CLAUDE.md.
- **Le dernier lot, v214 (Tom : « considère que c'est validé »)** : C-316 PROMI de l'accueil ouvre Ma Parole ! en gratuit (`redteam_promi_porte`) ; C-317 l'encart des Réglages, « Ma Parole ! » au bleu Promi #82AEF8, sans ombre, 25 px ; C-318 Soutenir : 150 € dans la rangée, « Autre montant » est un champ de chiffres qui déroule les paliers (`redteam_soutien_autre`). **Non vus sur l'iPhone** — VALIDATION.md 36 à 38. **Validés** : C-311 à C-315.
- **Après la fusion, v214b (sur `main`)** : C-319 — Soutenir, le paiement validé : il ne reste que le prix payé, centré, et « Un grand » (Gilbert) « Merci » (PromiLate), tracé ; aucun changement sec (`redteam_soutien_paye`, 80/80). **Non vu sur l'iPhone** (VALIDATION.md 39). C-316 à C-318 validés par Tom.
- **À trancher par Tom avant le portage** : le montant tapé dans Soutenir (Apple n'accepte pas de montant libre — le régler au palier le plus proche, ou ne garder que les paliers ; PREUVE-CAPACITOR.md, achats).
- **Rouges connus, déjà là avant v214** : `redteam_trace_present` (cadences d'images de l'onboarding et du guide : 125/137 sur v213 comme sur v214) ; `banc_rendu` Ramage seul (14 images, C-187).
- **« Promi preuve »** sur l'iPhone porte encore v213 : la reconstruire depuis `main` (`SOURCE=` une extraction `git archive`, `VERSION=v214 sh construire.sh`, PREUVE-CAPACITOR.md) si Tom veut v214 dans l'app.

## a) L'état

- **Branche `main`, v205 — CHAPITRE CLOS** — commit `90f5786` (sur `e6bfecb` : C-282 — l'exemple part en entier en 150 ms dès la première lettre ; C-286 — plus aucun reste pendant un détracé, `redteam_aspect` D). Étiquettes `avant-fusion-v203`, `avant-q621`. Le serveur sert `main` ; `?diag=1` affiche « v205 » en haut de chaque écran.
- **Le relevé des images ne tourne plus par défaut** : `?releve=1` (ou `?mesure=1`) le rallume ; `python3 resume_releve.py <fichier>` le lit (`mesures/`).
- **Le moteur (`promi-moteur.js`) reste en lecture seule.** Seule exception de ce chapitre, autorisée par Tom : Q621 (deux lectures du titre remplacées par la clé de plantation `p.cle`).
- **Validé par Tom dans ce chapitre** : la jonction du trait (C-259, C-263, C-265, C-267), la validation de l'onboarding (C-270), la page + et sa genèse (C-277, C-278), un seul langage de tracé (C-279), le guide (C-268, C-277), l'exemple qui revient (C-274 suite), le titre long de l'Index (C-276), modifier le titre d'une fiche sans encart (C-280), la dalle qui garde sa forme quand on renomme (Q621 : les deux lignes du moteur acceptées), les lettres qui clignotent en #82AEF8 et le plateau de l'accueil sans grain (C-281), Mascaret (C-272), l'Aura et la Pelote aux couleurs exactes (C-275), PromiLate gardé tel quel. Tranchées : Q618 (l'intérieur de la Pelote au ton le plus contrasté), Q619 (la lumière du velours retirée), Q620 (la première lettre immédiate) — faites en v203.
- **Validés par Tom** : sur f56219a, C-282 pour l'effacement et le §2 pour la recherche de l'Index ; sur 076966b, C-283 ; sur e6bfecb, C-284 (une seule phrase du guide à la fois), le §2 de v204 (« Le reste s'explore à ton rythme ! » en PromiLate bleu vif), C-285 ; `guide_rafale` D jugé bon sur l'iPhone (fermé : on ne retouche pas le dessin de l'eau).
- **Livré en dernier, à voir par Tom (v205)** : **C-282** — à la première lettre, le texte d'exemple part en entier, toutes ses lettres ensemble, en 150 ms (opacité qui baisse à chaque image, sortie amortie), la lettre tapée au-dessus, l'encart inchangé (page + et onboarding) ; **C-286** — plus de bandeau en haut des lettres pendant un détracé (T'APPARTIENT et toutes les phrases détracées), et les mots « ou », « par ce + . » de la phrase du + à leur place pendant leur tracé. Juges : `redteam_premiere`, `redteam_aspect` (D).
- **Les textes qui reviennent (§2), et ce qui les porte** : l'onboarding, prénom et parole (`_douceur.place`) · la page +, titre d'un Promi et d'un Chiche, nom d'un Cercle (`_douceur.place`) · « de » / « d’ » de la page + et de l'onboarding (`_retour.liaison`) · le titre vidé d'une fiche (C-280, son tracé) · la recherche de l'Index et du Fil, avec l'échange « Rechercher » ↔ « … » du curseur au focus (`_retour.champ`) · la description d'un Cercle dans Peaufiner et tout autre champ à texte d'exemple (`_retour.champ`) · « Un mot… » (`_retour.motLigne`) · l'ajout d'une personne, « + ajouter quelqu’un » et « un prénom… » (`_retour.remplace`, `_retour.bascule`). Juges : `redteam_onb_exemple`, `redteam_retours`, `redteam_exemple_retour`, `redteam_titre_fiche`.

## b) Ce qui reste ouvert (chapitre clos ; une ligne chacun, par importance pour le produit)

1. **La fluidité sur l'iPhone** — une lettre tracée coûte ≈ 100 ms au fil principal (11 au banc) : vérifier l'ouvrier du tracé (`R.tl` du relevé, `?releve=1`) ; la préparation de la Pelote (blocs de 650 à 780 ms) ; le flou d'« Adopte ce design » (571 ms). Objectif par animation : p95 < 16,7 ms, aucune image > 33 ms.
2. **Les cadences de `redteam_trace_present`** — des images de 20 à 54 ms pendant les tracés de l'onboarding et du guide, au calme ; f56219a de même (43 ms au pire, A/B du 16 nov.).
3. **`redteam_page_plus_continu` 11/12** — un saut de 2,5 à 10 pt à la bascule du sens, pas toujours le même cas ; f56219a de même.
4. **`redteam_trace_lettres` non jugé** — il dépasse ses 10 minutes (aucun rouge avant l'arrêt).
5. **Ramage au banc de rendu** (C-187) — la référence attend l'œil de Tom avant d'être refigée ; `banc_rendu` reste rouge sur Ramage seul.
6. **C-241** — sous Esquille et Tesselle, la dalle de la page + n'a pas la forme de la dalle vivante (le moteur pose la dalle par relâchement) : lot moteur.
7. **C-262** — la page s'est figée une fois après « tenir » (titre de cinq lignes, défilé puis revenu) : jamais reproduit ; la boîte noire (`promi_boite_noire`) est là pour le prendre.
8. **Q573, Q575** — Mascaret au Studio et le ressemis entre familles de semis : le coût est dans le moteur (lot moteur, après les testeurs).
9. **Le départ du mouvement du clavier** (Q598) — accepté par Tom.

## c) Les grands sujets pas commencés (ce qui dépend de quoi)

1. **Portage Swift** (`portage/`, dix documents, `PROMI-TOKENS.json` → `Promi+Design.swift`) — le socle de tout le reste. Avant lui : C-026 (archive, VoiceOver de la Toile, StoreKit, Firebase) et le banc de rendu comme référence au pixel.
2. **Invitations réelles par Firebase** (C-023, le Cercle et les parts à plusieurs, `p.parts`, `p.vuTenue`) — dépend du portage (comptes, réseau) ; le dessin collaboratif (C-093) en dépend aussi.
3. **Notifications et vibrations** (C-022) — le crochet `promiHaptique` est posé, vide ; Core Haptics et les notifications locales viennent avec Swift (Safari iOS ne vibre pas). La règle des notifications (§12, R-020 à R-026) est déjà écrite et jugée.
4. **Engagement E5 et E6** (C-079 phrases d'accueil ; C-080 E6A la Pelote qui s'enrichit, maquette d'abord ; C-081 E6B intégration après validation) — indépendants du portage, faisables dans le prototype ; C-082 « Délier » (issue d'un Promi jamais tenu) doit venir avant ou avec eux (la grille anti-coercition, critère 1).
5. **Android** — rien d'écrit : il suit le portage Swift (mêmes spécifications `portage/`, mêmes jetons).
6. **Avant publication** (C-025, C-090) — licences des polices (Gilbert CC BY-SA : crédit obligatoire), pages légales, prix de Ma Parole !.
7. **Dégradation adaptative** (CLAUDE.md §11) — à étalonner sur appareil, au premier lot Toile du portage.

## d) Les 146 chantiers « faits, en attente de Tom », par écran (pour les valider en bloc)

(Le registre en compte 187 non validés : 146 faits et en attente, le reste ouvert, en cours ou reporté — section b et `CHANTIERS.md`.)

- **Onboarding et guide** : C-282 (et le §2 des textes qui reviennent), C-286, C-006, C-043, C-073, C-074, C-075, C-095, C-123, C-124, C-126, C-136, C-138, C-159, C-162, C-165, C-169, C-208, C-209, C-211, C-212, C-266.
- **Page +** : C-045, C-054, C-067, C-078, C-140, C-149, C-150, C-152, C-154, C-157, C-184, C-192, C-196, C-201, C-223, C-264, C-269.
- **Fiches, tenir, trait, commentaires** : C-007, C-046, C-048, C-050, C-051, C-059, C-069, C-077, C-084, C-085, C-091, C-096, C-098, C-101, C-111, C-118, C-128, C-160, C-189, C-193, C-194, C-197, C-199, C-207, C-210, C-242, C-246, C-248, C-253, C-254, C-255, C-257.
- **Toile, accueil et mondes** : C-009, C-016, C-028, C-049, C-058, C-062, C-070, C-087, C-099, C-119, C-121, C-131, C-187, C-188.
- **Aura et Pelote** : C-001, C-002, C-003, C-005, C-008, C-029, C-052, C-064, C-071, C-072, C-120.
- **Studio, Ma Parole !, achat** : C-004, C-010, C-055, C-057, C-061, C-063, C-092, C-100, C-170, C-175, C-190, C-198.
- **Index et Fil** : C-151, C-191, C-200, C-250, C-251, C-252, C-256.
- **Partager, dessin, photo** : C-042, C-056, C-060, C-068, C-086, C-097.
- **Réglages, veille, effacer** : C-104, C-195, C-249, C-258.
- **Règles et méthode (rien à voir à l'écran)** : C-015, C-021, C-030, C-044, C-047, C-053, C-065, C-066, C-102, C-103, C-114, C-130, C-137, C-178, C-179, C-202, C-204, C-206.
