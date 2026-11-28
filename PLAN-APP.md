# PLAN-APP — construire la vraie app, lot par lot (L0, 20 nov. 2026)

> Le prototype `app.html` (main = v214b) est le **cahier des charges figé**. La vraie app (`promi/`, TypeScript strict, Capacitor) est écrite
> de zéro ; seuls le moteur, le tracé, les flaques et les jetons sont repris, chacun derrière son interface. **Chaque écran porté est
> identique au prototype** : même rendu, mêmes textes, mêmes couleurs, mêmes transitions, même comportement. Un écart non demandé est un défaut.
> **Les lots suivants attendent que Tom valide ce plan.**

## 0) Ce que L0 a posé (branche `app-L0`)

| Couche | Où | Ce qui le prouve |
|---|---|---|
| Outillage | `promi/` : Vite, TypeScript strict, ESLint (strict, typé), Prettier, Vitest, Playwright WebKit | `npm run verifier` · CI `.github/workflows/ci.yml` |
| Coquille | Capacitor 8 : `ios/` (profil gratuit de Tom, équipe B77VBMD9BF), `android/` préparé | l'app « Promi » installée sur l'iPhone 16e de Tom |
| Schéma v1 + migrations | `src/donnees/` (`schema.ts`, `migrations/`, `stockage.ts`) | `tests/unitaires/donnees.test.ts` |
| Import des données de Tom | `src/donnees/migrations/prototype.ts` | `import.test.ts` : chaque export (etats/, Promi-reference-v205, banc-etats/) revient **sans perte** |
| Magasin d'état unique | `src/etat/magasin.ts` : actions nommées, écriture au geste (C-226), abonnés | `donnees.test.ts` |
| Horloge unique | `src/animation/horloge.ts` : la seule boucle d'images, le seul échéancier (pièces reprises comprises) ; un mode piloté | `horloge.test.ts`, `socle.spec.ts` |
| Façade du moteur | `src/moteur/facade.ts` (seule à toucher `window.Toile` — le lint l'impose), `types.ts` (l'inventaire des appels) | `entrees.spec.ts`, `banc-rendu.spec.ts` |
| Tracé, flaques | `src/animation/trace/`, `src/animation/flaques/` (copies octet pour octet, `repris.test.ts`) | `socle.spec.ts` |
| Jetons, polices | `outils/jetons_engendrer.py` → `src/design/jetons.{css,ts}` ; `outils/polices_extraire.py` → les cinq faces du prototype | `npm run jetons:verifie` (CI) |
| Export de l'état (à venir) | l'équivalent de `?export=1` dans la vraie app (le diagnostic, et le passage de l'iPhone au Mac) — **décision de Tom, 20 nov. 2026 : « État envoyé au Mac » ne paraît que si le serveur a confirmé la réception (`{ok:true, fichier}`) ; sinon « Envoi impossible : vérifie l’adresse du Mac. »** (comme le prototype depuis ce jour) | un test qui coupe la réponse, renvoie 400, puis une réponse sans `ok` : jamais « envoyé » |
| Synchro | `src/synchro/synchro.ts` : l'interface, l'implémentation locale (Firebase en 1.1) | — |
| Achats | `src/metier/achats.ts` (la grille Soutenir, les designs), `src/natif/achats.ts` (local ; RevenueCat au lot 7), `achats/Promi.storekit` engendré | `soutien.test.ts` |
| Preuve : la Toile | `src/ecrans/toile.ts` — la Toile de Tom au repos (le glissé qui changeait de monde, preuve de L0, est retiré : C-325) | **banc_rendu porté : 266/266 images identiques au pixel** (figées et prototype vivant) ; entrées du moteur identiques sur l'état de Tom ; la vue de son export retrouvée |

## 1) La méthode d'un lot

1. Le lot porte un écran ou un ensemble cohérent, **en s'appuyant sur le précédent**, dans les couches de ARCHITECTURE.md (b) ; aucun écran ne pose une cote, aucun ne touche le moteur, aucun n'appelle `setTimeout`.
2. **Le test d'identité** : chaque écran porté est comparé au pixel à celui du prototype, dans le même WebKit, aux échelles 1 et 0,79 — la vraie app contre le prototype vivant sur la même machine (le juge de l'intégration continue), et contre les images figées quand elles existent. Avant de comparer un écran vivant, le lot neutralise côté prototype les travaux de fond des écrans pas encore portés (ils laissent des caches dans le moteur : voir `tests/rendu/banc-rendu.spec.ts`).
3. **Les juges du prototype rangés dans le lot deviennent des tests** (Playwright, WebKit) — chacun garde sa décision écrite en dur et rougit sur la version fautive. La liste ci-dessous range les **294 juges**, chacun dans un seul lot.
4. **Tom vérifie sur son iPhone, dans l'app** (R3), sur les trois natures. Le rapport dit pour chaque demande : tenu, non tenu, ou non vu (R4).

| Lot | Juges |
|---|---|
| 1 · accueil, Toile — dont **socle transversal** (rejoué à chaque lot) | 20 + 27 = 47 |
| 2 · page + et genèse | 48 |
| 3a · fiche et tenir | 46 |
| 3b · Peaufiner, commentaires, photo, dessin | 26 |
| 4 · Index et Fil | 14 |
| 5 · Cercle et membres | 13 |
| 6 · Aura et Pelote | 15 |
| 7 · Studio et achats | 15 |
| 8 · Réglages, Partager, Soutenir, Ma Parole ! | 21 |
| 9 · onboarding et guide | 34 |
| 10 · veille | 5 |
| 11 · notifications et vibrations | 1 |
| 12 · Android | 0 (rejoue la série) |
| Engagement | 1 |
| Non portés | 8 |

Sources : `portage/SPEC-ECRANS.md` (§ cités), `SPEC-GESTE.md`, `SPEC-RENDU.md`, `ARCHITECTURE.md` §h (les 42 états rares), `SPEC-JUGES.md`, `VALIDATION.md` (lignes #), `CHANTIERS.md`.
⚠ Choix de rangement à arbitrer : les juges « mixtes » (couvrant deux lots) sont mis au lot qui pose le composant en premier ; notés ⇄ ci-dessous.

---

## Lot 1 · L'accueil et la Toile vivante

**(a) Porté** — SPEC-ECRANS §1 (accueil : plateau, mot PROMI et son I clignotant, barre 5 entrées 710 → 810, le + de 45 pt), §0 (règles communes) ; SPEC-RENDU (a) Toile Voronoï pondéré, deux familles de semis, relâchement, horloge (rythme v60/v61, Houle par image), vue et recadrage, titres, fond, couleur `cOf` / Ingénu ; (b) les vingt mondes derrière la façade du moteur ; (d) la vie au repos et le retour exact (C-028) ; SPEC-GESTE §6.1 toucher une dalle (+ tolérance 22 pt, C-239), §6.2 pincer/glisser/recadrer (C-099, C-188), déplacer une dalle (C-101) ; Toile vide (C-136) ; fluidité planter/retirer sur Toile pleine (C-112) ; Ramage sans disque (C-009), Ritournelle cadrage E1 (C-088). Le socle : jetons générés, cinq faces, `_tailleX`, aucun volume, kaki.

**(b) Juges du lot** : banc_rendu, redteam_rythme, redteam_vivant, redteam_retour, redteam_toucher, redteam_toucher_tolerant, redteam_zoom, redteam_recadre_bouton, redteam_deplace, redteam_accueil, redteam_barre, redteam_toile_stable, redteam_toile_vide, redteam_evol, redteam_pleine, redteam_decoupe, redteam_dalle_figee, redteam_ritournelle, redteam_ramage_onde, redteam_clair_sombre

**Socle transversal** (posé au lot 1, rejoué à chaque lot — sentinelles C-227 et porte A1) : redteam_couleurs_ref, redteam_decisions, redteam_joignable, redteam_ecrans, redteam_volume, redteam_air, redteam_flash, redteam_superpo, redteam_aspect, redteam_filets, redteam_tonsurton, redteam_lexique, redteam_emoji, redteam_secs, redteam_secs2, redteam_croix, redteam_vide, redteam_enchaine, redteam_tokens, redteam_polices, redteam_lettres_bleu, redteam_kaki, releve-design, redteam_app, redteam_fonctions, redteam_champs, redteam_pastilles

**(d) État au 20 nov. 2026 (branche `app-L1`, C-322)** — porté : le plateau, la barre, le + (anneau, menu des natures sur place), le bandeau « Garder ta Toile », le symbole « recadrer » (en flaques), le grain de l'appareil, le toucher d'une dalle (260 ms, double toucher, tolérance C-239), l'adaptation à l'écran. Identique au prototype au pixel (≤ 2 niveaux) à 390 × 844, clair et sombre, menu fermé et ouvert (`accueil.spec.ts`). La Toile, ses mondes, la vie au repos, le dézoom, déplacer une dalle : faits par le moteur repris (copie octet pour octet), jugés par `banc-rendu.spec`, `entrees.spec` et la vie au repos d'`accueil.spec`. **Juges : les 20 du lot et les 27 du socle sont des tests** (C-326, `promi/JUGES-TESTS.md` : juge → test → sonde ; `npm run sondes` exige que chaque test rougisse sur son défaut ; l'intégration continue passe tests et sondes à chaque commit, en quatre parts). Trouvés en portant et corrigés : la couleur figée d'une dalle gardée par le magasin, les zones de la barre (C-106), le symbole « recadrer » 2 pt trop bas, le frémissement à 1,5 s ; à trancher par Tom : C-327, C-328, C-329. **Aucun écran destinataire n'existe** : toucher une dalle, une entrée de la barre ou une pilule note la demande (`navigation`), rien ne s'ouvre avant les lots 2 à 9. Trouvé : C-323 (la limite de 44 pt de C-239 n'est pas appliquée par le prototype).

**(c) Tom sur l'iPhone**
- Accueil en clair et sombre : la Toile vit au repos (une ou deux dalles bougent 1–2 s), rien ne saccade en plantant ou retirant sur sa Toile pleine.
- Toucher une dalle ouvre la bonne fiche, dans trois mondes dont Ritournelle ; une dalle de Cercle, de Promi, de Chiche.
- Appui 0,8 s, glisser, lâcher, recharger : la place est gardée (VALIDATION #6).
- Tout effacer puis six rechargements : la Toile vide jamais colorée (#4).
- Pincer, recadrer : le symbole des quatre coins naît en flaques et part après 4 s.

---

## Lot 2 · La page + et la genèse

**(a) Porté** — SPEC-ECRANS §3 (page + Promi, Chiche, Cercle ; menu du + §3/C-142), §23 (bouton photo de la page +) ; SPEC-GESTE §2 planter (la moitié, 195 pt, C-237 ; Cercle trait entier) ; la phrase-pastilles (verbe, sens, « promets-moi », liaisons « de/d' » C-305/C-312, « moi » C-269/C-304, C-296), l'invite qui naît après validation (C-209, C-213, C-222, C-229), l'horizon et la dalle fixe (C-234), un seul mouvement de mise en page (C-278 §4), exemples et première lettre (C-274, C-282), la naissance et le vol de la dalle (C-237, C-241, Q611), « garder de côté » (C-149), ajouter une personne (C-122), rail du pinceau (C-196), plantation écrite au trait (C-226), les textes longs (C-244, C-240). **Le module de tracé des lettres** (TraceLettres, ouvrier, repli C-206, C-292).

**(b) Juges** : releve-S3-page-plus, redteam_pages_plus, redteam_invite_page_plus, redteam_page_plus_continu, redteam_genese_nature, redteam_nature_plus, redteam_menu_plus, redteam_tuiles, redteam_pilules, redteam_phrase, redteam_verbe, redteam_demande, redteam_je, redteam_moi_phrase, redteam_moi_douceur, redteam_moi_toucher, redteam_liaison, redteam_liaison_exemples, redteam_prenom_alterne, redteam_exemples, redteam_exemple_retour, redteam_premiere, redteam_premiere_froid, redteam_retours, redteam_suggestions, redteam_marges, redteam_phrase_lignes, redteam_textes_longs ⇄3, redteam_titres_longs, redteam_clavier, redteam_clavier_doux, redteam_frappe_douce, redteam_dalle_fixe, redteam_dalle_unique, redteam_moitie, redteam_vol_dalle, redteam_pose_dalle, redteam_bandeau, redteam_garder, redteam_garder_reprise, redteam_gens, redteam_ajouter, redteam_ajout_personne, redteam_pinceau_rail, redteam_plantation_durable, redteam_trace_lettres ⇄9, redteam_trace_present ⇄9, redteam_un_trace ⇄9

**(d) État au 22 nov. 2026 (branche `app-L2`) — L'ÉTAPE 2a EST FINIE ; 2b (le trait et la genèse) attend le retour de Tom sur l'iPhone.** Porté : la page + des trois natures ouverte par sa pilule, qui MONTE en glissant (C-331 : le mouvement de sa fermeture à l'envers) et refermée par son X ; le menu du + en flaques (C-329) ; le plateau, le champ de la nature, la dalle d'avance du moteur (C-241, C-234), l'horizon bas et rien du trait (C-213, C-229) ; la phrase-pastilles, sa taille, le cycle du verbe, les exemples et leur liaison (C-312) ; « moi » à la place touchée (C-304) ; le choix des personnes, d'un Promi, d'un Chiche et d'un Cercle (« Moi » en tête, Gilbert 23,1) ; la saisie (« DÉJÀ PROMIS », l'onde à 144, la phrase à 230, la barre cachée §2.11) et le mouvement qui y mène et en revient (Q598, C-234, 360 ms ; C-303) ; le champ « un prénom… » (C-122) ; le rail du pinceau et ses murs ; « garder de côté » (C-149 ; inactif à la teinte de sa nature, C-330) ; Peaufiner (ses rangées ; la note s'écrit ; C-134, C-220 ; les autres choix au 2b) ; le menu du bouton photo et la photo importée ; aucun emoji (C-129). **Identique au pixel** (`page-plus.spec`, 28 cas, clair et sombre ; écarts nommés : la matière, C-330, C-331, P3, P4). **Le socle parcourt la page +** (`ECRANS_PORTES`). **A3** : à 0,79 (330 × 714) la page + dans chacun de ses états (test A3 de `page-plus-juges.spec`) — trouvé et corrigé : le choix d'un Cercle sortait de l'écran, ses noms coupés net, le X de Peaufiner hors de l'écran. **Pas encore** : les choix de Peaufiner autres que la note, l'outil de dessin, la photo d'un gardé de côté (2b) ; deux changements secs (« + ajouter quelqu'un » → « un prénom… », la taille de la phrase en entrant dans la saisie : 2c) ; le toast « gardé de côté » (lot 8). Juges : `promi/JUGES-TESTS.md`, « Lot 2a ».

**(e) État au 22 nov. 2026, soir — L'ÉTAPE 2b EST FINIE (au banc ; à voir sur l'iPhone de Tom).** Porté : C-332 (« Moi » se coche et se décoche) et Q624 (« moi » en dernier, après « et », app et prototype) ; l'invite à tracer (C-209, C-213, C-229 : rien avant la validation, l'horizon remonte PUIS le trait naît en flaques, le libellé tracé, le départ clignote avec le I) ; le geste de la moitié et la plantation (C-237, C-226 : écrite au milieu du trait, avant le lever ; un Cercle au trait entier), la naissance de la dalle et son vol jusqu'à la Toile (C-241, Q611 : une seule dalle à l'écran) ; Peaufiner, tous ses choix (l'échéance et son calendrier, DANS UN CERCLE → « Je promets … à tout le monde », les pièces jointes, MEMBRES ; planter les emporte) ; le visage des personnes dans la phrase (§2.10) ; l'outil de dessin (C-042 : plume, gomme, annuler, le mur des couleurs, photos dans le dessin, POSER dans la bande, « Retirer le dessin ») ; la photo et le dessin d'un gardé de côté, rendus à sa reprise (`pagePlus().reprendre`, sa porte : l'Index, lot 3). **Identique au pixel** : `page-plus.spec`, 44 cas (deux thèmes). **Pas encore** : les textes longs, les liaisons et les deux changements secs (2c) ; le glissement continu de la phrase quand elle change de place (C-278 §4 — sous Peaufiner il ne se voit pas ; 2c). Juges : `promi/JUGES-TESTS.md`, « Lot 2b ».

**(f) État au 23 nov. 2026 — L'ÉTAPE 2c EST FINIE ; LE LOT 2 (LA PAGE +) EST CLOS (au banc ; à voir sur l'iPhone de Tom).** Retours de Tom sur 2b traités : « une date… » (le calendrier s'ouvre sur l'iPhone, la date se pose par détracé puis tracé, elle est enregistrée) ; le mode dessin paraît et part en flaques ; le juge « flash » stabilisé (la cause : le test touchait trop tôt). Porté au 2c : les textes longs (v46 — la taille de la phrase se calcule comme si la parole était courte, seul le titre se réduit ; la coupe « … » de C-244 §5.1) ; `continu.ts` (la taille de la phrase par `scale`, les mots de liaison tracés et détracés, le glissement continu de la phrase, de ses mots et du rail : C-273, C-278) ; `douceur.ts` (lot-V200-DOUCEUR : toute place qui change se détrace pendant que l'encart va à sa largeur, se remplit ou se vide en flaques, puis le mot neuf se trace ; la première lettre — C-282 ; l'exemple qui revient — C-274 ; la bascule du sens) ; « + ajouter quelqu’un » ↔ « un prénom… ». **Identique au pixel** : `page-plus.spec`, 50 cas. **Les 48 juges du lot 2 sont reliés** (`promi/JUGES-TESTS.md`, lots 2a, 2b, 2c) ; non porté, nommé : l'atterrissage de la dalle au demi-point sur la dalle vivante (lot 3a), un navigateur relancé par essai (`redteam_premiere_froid`). **Écart nommé** : l'entrée dans la saisie glisse (dans le prototype, ses mots sautent de 5 pt). **Défauts du prototype nommés, non corrigés (il est gelé)** : son plafond de taille C-240 lu pendant le mouvement du clavier (une parole de 280 caractères finit à 17, 21, 28 ou 30 pt selon l'instant) ; son calendrier de « une date… » sur l'iPhone (le même défaut que l'app avait).

**(c) Tom sur l'iPhone**
- Le + → Promi, Chiche, Cercle : à l'ouverture rien du trait ; le texte validé (Retour), l'horizon monte puis le trait naît en flaques, le départ clignote avec le I.
- Toucher le titre et taper aussitôt : l'exemple part en 150 ms, jamais un éclair (#1) ; effacer : il revient en se traçant.
- Toucher le verbe trois fois, la place du destinataire, « promets-moi » : liaisons et prénoms se détracent puis se tracent, aucun rectangle ne reste (#11, #23, #24, #29, #30, #32).
- Chiche : taper puis Retour — « DÉJÀ PROMIS » descend avec le clavier (#22).
- Planter (Promi, Chiche à moitié ; Cercle entier) : une seule dalle, qui naît et vole à sa place ; recharger, la parole est là.

---

## Lot 3a · La fiche et tenir (la fiche, tenir, le trait et la jonction, deux états, échéance, titre modifiable)

**(a) Porté** — SPEC-ECRANS §4 (fiche Promi/Chiche, en cours/tenue), §5 (l'instant) ; SPEC-GESTE §1 (l'onde, les quatre modes), §3 et §3.1 (tenir, rideau, « Parole tenue ! » C-311), §4 (moitié, chevron, points) ; deux états seulement (C-210), échéance en date (C-160), la phrase complète (C-069), titre modifiable (C-280, Q621), jonction et trait plat collé (C-259, C-267, C-297), le haut stable (C-255), les parts à plusieurs (C-115) ; crochet haptique au lever (C-022, branché au lot 11).

**(b) Juges (46)** : releve-S1-fiches, releve-S5-instant, banc_apres_tenir, banc_jonction, redteam_trait, redteam_trait_k, redteam_ronds, redteam_depart_orange, redteam_contraste_trait, redteam_formes, redteam_champ, redteam_ruban, redteam_tenir, redteam_tenir_e3, redteam_tenir_presse, redteam_tenu_trait, redteam_fluide, redteam_validation, redteam_celebration_fixe, redteam_centre_validation, redteam_part, redteam_un_trait, redteam_repos_fiche, redteam_retour_fiche, redteam_retour_trait, redteam_premier_toucher, redteam_trait_entier, redteam_trait_retour, redteam_points_plat, redteam_jonction, redteam_jonction_fiche, redteam_jonction_plat, redteam_jonction_rebond, redteam_elan, redteam_haut_fiche, redteam_etat_fiche, redteam_flash_etat, redteam_fiches_orange, redteam_fiches_theme, redteam_deux_etats, redteam_echeance, redteam_phrase_fiche, redteam_titre_fiche, redteam_titre_encart, redteam_renomme, redteam_motmarque

**(d) Le découpage (23 nov. 2026), comme le lot 2 — chaque étape finit par la CI verte, la porte A1–A6 et l'app sur l'iPhone de Tom :**
- **3a-1 · La fiche au repos** — l'écran `fiche` (`src/ecrans/fiche/`), Promi et Chiche, chaque état (en cours, date passée, tenue, lancé, à relever, tenu, tenu à deux, à plusieurs), deux thèmes, échelles 1 et 0,79, comparé au pixel au prototype ; s'ouvre d'une dalle de la Toile, se ferme par le X. Juges : releve-S1-fiches, redteam_champ, redteam_formes, redteam_contraste_trait, redteam_ronds, redteam_depart_orange (fiches), redteam_fiches_orange, redteam_fiches_theme, redteam_deux_etats, redteam_echeance, redteam_phrase_fiche, redteam_etat_fiche, redteam_flash_etat, redteam_motmarque, redteam_trait_k (fiches), redteam_part (le rendu des parts).
- **3a-2 · Tracer et tenir** — le geste (60 pt), le trait qui suit le doigt et revient, le ruban, le rideau et « Parole tenue ! », l'instant, la fiche tenue ; le premier toucher ; les parts tracées. Juges : redteam_trait, redteam_retour_trait, redteam_premier_toucher, redteam_ruban, redteam_tenir, redteam_tenir_e3, redteam_tenir_presse, redteam_tenu_trait, redteam_fluide, redteam_validation, redteam_celebration_fixe, redteam_centre_validation, releve-S5-instant, redteam_part (le geste), banc_apres_tenir. Repris du lot 2 : l'atterrissage de la dalle au demi-point sur la dalle vivante.
- **3a-3 · Défiler : la jonction** — le trait plat collé, la bande, le haut stable, l'élan, le rebond, le repos sûr. Juges : banc_jonction, redteam_un_trait, redteam_repos_fiche, redteam_retour_fiche, redteam_trait_entier, redteam_trait_retour, redteam_points_plat, redteam_jonction, redteam_jonction_fiche, redteam_jonction_plat, redteam_jonction_rebond, redteam_elan, redteam_haut_fiche (sentinelle).
- **3a-4 · Le titre modifiable** — C-280, Q621. Juges : redteam_titre_fiche, redteam_titre_encart, redteam_renomme.

**(e) État au 23 nov. 2026 — L'ÉTAPE 3a-1 (LA FICHE AU REPOS) EST FAITE (au banc ; à voir sur l'iPhone de Tom).** Porté : l'écran `fiche` (`src/ecrans/fiche/` : le champ et la dalle teintée par la rampe de sa nature, Q30 ; le trait et ses quatre modes, les parts à plusieurs, C-115 ; les Noyaux — deux arcs, le jour de 3 pt, l'anneau vide, le visage, le « + » des membres C-254 ; la phrase complète C-069 et « + x personnes » qui se déroule ; le titre qui s'ajuste, C-244 ; la ligne d'état et sa date passée, C-210 D5 ; « Un mot… » et son nombre, C-257 ; la barre Peaufiner fermée), `src/metier/fiche.ts` ; `?jour=+N` et le recompte des échéances au retour au premier plan (C-160) ; l'ouverture qui monte du bas et la fermeture qui y redescend ; l'accueil couvert dessous. **Identique au pixel** : `fiche.spec`, douze cas × deux thèmes. La fiche entre dans `ECRANS_PORTES` (tout le socle la juge). **Écarts nommés** : le grain des anneaux (tiré au hasard par le prototype) ; le fondu à droite des Noyaux quand ils débordent (une dette de volume du prototype, non reprise). **Pas encore** : tracer et tenir (3a-2) ; la jonction (3a-3) ; le titre modifiable (3a-4) ; le menu photo, Peaufiner ouvert, les mots, le + des membres (3b, `aria-disabled` d'ici là) ; Partager (lot 8) ; la fiche d'une parole d'un Cercle (lot 5). Juges : `promi/JUGES-TESTS.md`, « Lot 3a-1 ».

**(f) État au 23 nov. 2026 — L'ÉTAPE 3a-2 (TRACER ET TENIR) EST FAITE (au banc ; à voir sur l'iPhone de Tom).** Porté : `src/ecrans/fiche/tenir.ts` (la zone de 118 pt, la fenêtre d'ouverture de 340 ms du prototype — Q625 —, le plein qui suit le doigt, le retour à la pointe en 300 ms, le ruban amande, le rideau à vitesse constante et « Parole tenue ! » / « Défi relevé ! », la remontée à 2 150 ms ou au toucher qui presse, avalé), l'instant dans `fiche.ts` (« le trait se referme » sous le rideau, puis « juste après », qui reste tant que la fiche est ouverte), `magasin.tenir` (tenue, son trait, `vuTenue`, la ligne du Fil, la récurrente qui renaît ; ma part à plusieurs), l'haptique (Capacitor Haptics, l'impact fort de la preuve). **Identique au pixel** : `tenir.spec`, six fiches × deux thèmes × deux instants, l'horloge pilotée des deux côtés. **Corrigé (lot 2)** : les lignes du Fil prennent les guillemets insécables et « à l'instant » du prototype. **Reporté au 3a-3** : la célébration fixe pendant un défilement (C-311), la jonction après tenir (`banc_apres_tenir`), l'atterrissage de la dalle de la page + au demi-point. Juges : `promi/JUGES-TESTS.md`, « Lot 3a-2 ».

**(g) État au 23 nov. 2026 — L'ÉTAPE 3a-3 (DÉFILER : LA JONCTION) EST FAITE (au banc ; sur l'iPhone avec le 3b).** Porté : la fiche en deux couches (`#dpDefile` défile ; le plateau et la barre Peaufiner restent posés), `src/ecrans/fiche/jonction.ts` (la bande collée 0 → 112, la vague, la fenêtre découpée sous son dernier pixel plein, le trait plat collé à la jonction ; le geste coupé accroché ; les aimants et les places sûres ; un toucher sous la bande avalé), `src/ecrans/fiche/mots.ts` (« Les Mots » et leur liste, affichés : ils rendent la fiche défilable, comme dans le prototype). **Identique au pixel** : `jonction.spec`, trois fiches × deux thèmes, l'écran entier à chaque pas de défilement, aller et retour ; tenir sur une fiche défilée puis défiler pendant que le vert est posé (C-311, banc_apres_tenir). **Écarts nommés** : M4, le chevron de Peaufiner que le prototype retourne en bas de la fiche (Q626) ; le visage d'un mot, un dégradé repris du prototype en exception nommée du volume (Q627). **Corrigé en passant (CI Linux)** : la croix d'un plateau reposée quand une police finit de se charger ; « + 3 personnes » en ligne, sans apparence de bouton ; le test de la montée de la fiche lit sa transition ; le test du symbole « recadrer » relève la naissance dès la première image du geste ; une sonde est prise au premier test qui rougit. **Pas encore** : l'élan et le rebond de Safari (à voir sur l'iPhone : la vraie app ne sait pas encore écrire de mot, une fiche n'y défile qu'avec le 3b) ; le titre modifiable (3a-4). Juges : `promi/JUGES-TESTS.md`, « Lot 3a-3 ».

**(h) État au 23 nov. 2026 — L'ÉTAPE 3a-4 (LE TITRE MODIFIABLE) EST FAITE (au banc ; à voir sur l'iPhone de Tom).** Porté : `src/ecrans/fiche/titre.ts` (C-280), le dépliage d'un titre coupé (C-244), `magasin.renommer` et la clé de plantation posée à chaque écriture (Q621). **Identique au prototype** : `titre.spec` (le dépliage au pixel, la modification sans encart au pixel, le renommage, Échap et le titre vidé) ; Q621 jugée sur la Toile sous Brouillamini. **Corrigé en passant** : le moteur suit le magasin après chaque écriture (`facade.rafraichir`) — il gardait l'ancien titre, et l'ancien état d'une parole tenue. **Écart nommé** : le Fil réécrit au renommage (le prototype ne le faisait plus). **LE LOT 3a EST FAIT** (3a-1 à 3a-4) ; la fiche défilante se verra sur l'iPhone avec le 3b (« Un mot… »). Juges : `promi/JUGES-TESTS.md`, « Lot 3a-4 ».

**(i) État au 24 nov. 2026 — LE LOT 3a EST FINI (au banc ; à voir sur l'iPhone de Tom).** Ajouté : la fiche et « tenir » d'un Promi d'un Cercle (le disque du Cercle dans les Noyaux, `noyauxDe` ; la parole du banc plantée dans le prototype). Corrigé en passant (CI Linux) : les trois croix de la page +, de Peaufiner et du dessin posées par `poserCroix` à la taille des titres (29,5, Q623) ; le prototype du banc réglé comme en usage (l'Index montré). **Le calendrier de la page +** (retour de Tom, sa séance relevée sur l'iPhone par `banc-calendrier.html`) : deux causes nommées, corrigées dans le prototype ET l'app (validé par Tom dans Safari). Juges : `promi/JUGES-TESTS.md`, « Lot 3a — la fin ».

**(c) Tom sur l'iPhone**
- Tenir un Promi, un Chiche, un Promi d'un Cercle : « Parole tenue ! » / « Défi relevé ! » toujours à la même place, le vert remonte (#31).
- Défiler juste après tenir, puis lentement et d'un coup, jusqu'au rebond : le trait s'accroche à plat sous le bandeau, jamais au-dessus ni dessous (#12, #17, #25).
- `?jour=+30` : « EN COURS · 12 OCT. » (#3).
- Toucher le titre pour le modifier : aucun encart ; renommer ne change pas la forme de la dalle.

## Lot 3b · Peaufiner, les commentaires, la photo, le dessin, effacer, la fiche d'une personne

**(a) Porté** — SPEC-ECRANS §6 (Peaufiner), §22 (fiche d'une personne), §23–25 (menu photo, mode dessin, voir en entier) ; SPEC-GESTE §5 (dessiner) ; commentaires « Un mot… » et « Les Mots » (C-116, C-248, C-257, C-260, C-261), mots neufs (C-253), le + des membres (C-254), photo cadrée/tournée (C-085, C-098), dessin (C-042, C-056, C-061, C-086), effacer sans retour (C-258).

**(b) Juges (26)** : releve-S2-peaufiner, redteam_photo_trait, redteam_peaufiner, redteam_peauf_fermer, redteam_peauf_x, redteam_peauf_rangees, redteam_effacer, redteam_commentaires, redteam_commentaires_liste, redteam_envoi_mot, redteam_les_mots, redteam_mots_fiche, redteam_mots_neufs, redteam_mot_neuf_essai, redteam_nombre_mots, redteam_noms, redteam_plus_disque, redteam_photo, redteam_photo_menu, redteam_origine, redteam_cadre, redteam_tourne, redteam_entier, redteam_remplace, redteam_dessin, redteam_dessin_photo

**(c) Tom sur l'iPhone**
- Peaufiner › Supprimer puis recharger : la parole ne revient pas (#2) ; le X de Peaufiner le ferme seul.
- Envoyer deux mots de suite : le clavier reste, le mot paraît sans délai ; le nombre « +N » glisse jusqu'au mot neuf.
- Bouton photo › Importer, toucher la bande : la photo en entier (#7) ; › Dessiner : outils en bas, ✕ sort sans poser (#8).
- La fiche d'une personne : les noms se touchent, « Tenu ensemble » s'ouvre.

**(d) État au 24 nov. 2026 — LE LOT 3b EST FAIT EN PARTIE (au banc ; installé sur l'iPhone de Tom, `487b82b`).** Fait, en six étapes commitées (L3b-1 à L3b-6) : Peaufiner sur la fiche (ses rangées, ses choix, SUPPRIMER, la feuille, « Annuler », la pierre tombale) ; écrire un mot (« Un mot… », l'envoi, le vol, le Fil) et les mots neufs (la pastille, « +N » qui glisse, vus à la fermeture) ; le bouton photo (son menu, la photo importée, la dalle d'origine Q365 ; les dalles de la fiche rendues comme en sombre, C-132) ; la photo en entier et cadrée au doigt, sur la fiche et sur la page + (C-051, C-067, C-085, C-098) ; le dessin sur la fiche (posé dans la bande, l'œil, « Retirer le dessin », en entier). **Identique au prototype** : `fiche-peaufiner`, `fiche-mot`, `fiche-photo`, `fiche-entier`, `fiche-dessin`, `page-plus-juges` (chacun avec sa sonde). **Pas encore** : choisir LE TRAIT (le rail du pinceau) et les personnes depuis Peaufiner ; le + des membres (C-254) ; la fiche d'une personne. Juges : `promi/JUGES-TESTS.md`, « Lot 3b » ; à vérifier : `promi/A-VERIFIER-LOT-3B.md`.

**(e) État au 25 nov. 2026 — LE LOT 3b EST FAIT, SAUF LA FICHE D'UNE PERSONNE (installé sur l'iPhone de Tom, `4379eb5`).** Ajouté : LE TRAIT depuis Peaufiner et la matière des douze pinceaux sur le trait (fiche, page +, instant, jonction) ; les personnes depuis Peaufiner (la brique des personnes, une pour la page + et la fiche) ; le « + » des membres (C-254). La CI juge l'identité au pixel sur macOS (Tom) ; les jugements fins restent ceux du Mac de Tom (`MAC_DE_TOM`). **Reporté au lot 4** : la fiche d'une personne — elle porte les vraies cartes de l'Index (trois par ligne), que le lot 4 construit. À vérifier : `promi/A-VERIFIER-LOT-3B-FIN.md`.

---

## Lot 4 · L'Index et le Fil

**(a) Porté** — SPEC-ECRANS §8 (Index : cartes construites comme la fiche C-147, titres ajustés C-151, gardé de côté pointillé C-149, ⇅ et tris C-191/C-256, recherche), §9 (Fil : bandeaux au repos du cadre 76, appui maintenu TRACER/REPORTER, filtres, « Récents » = dernière action C-245), écrans vides E4 (C-078) ; un seul magasin réactif (C-049) ; le X rend l'écran d'origine au même défilement (C-193, C-250) ; pastilles de mot neuf (C-253).

**(b) Juges** : releve-S4-index-fil, redteam_index_fil, redteam_recents, redteam_recents_fil, redteam_fil_nombre, redteam_titres_cartes, redteam_garde_index, redteam_menu_tri, redteam_tri_menus, redteam_tri_fond, redteam_reperage, redteam_reactif, redteam_pile_retour, redteam_vides

**(c) Tom sur l'iPhone**
- Ouvrir l'Index et le Fil : même encart, même recherche, même ⇅ (#19) ; les natures se lisent sur chaque carte.
- Planter, tenir, retirer : l'Index et le Fil sont à jour aussitôt, sans doublon.
- Carte du Fil → fiche → X : le Fil revient tel quel, au même défilement ; idem depuis l'Index.
- Fil : appui maintenu sur un bandeau → TRACER · REPORTER ; REPORTER compte depuis aujourd'hui.
- Écrans vides (Index, Fil, recherche) : la seconde ligne mène à son action.

**(d) État au 25 nov. 2026, soir — LE LOT 4 EST FAIT (au banc ; à voir sur l'iPhone de Tom).** Porté, en dix étapes commitées (L4-1 à L4-10) :
l'Index (ses cartes construites comme la fiche, un Cercle et sa petite Toile, un gardé de côté ; la recherche, le menu ⇅, ses tris et filtres ; les
écrans vides ; une carte ouvre sa fiche, le X ramène l'Index tel qu'il était ; l'entrée par le bas) ; le Fil (l'écran d'une liste, une brique avec
l'Index, C-301 ; ses bandeaux du cadre 76 ; son compte, Q347 ; « Récents », C-245 ; l'appui maintenu : TRACER, REPORTER et son toast ; les écrans
vides ; le retour d'une fiche au même défilement ; le glissement de la droite) ; la pastille « pas encore vu » (Q347, C-253) ; la fiche d'une
personne (§22 : le Noyau, « Tenu ensemble », les cartes, les deux boutons ; un nom touché y mène). **Identique au pixel** : `index.spec`,
`fil.spec`, `personne.spec` (deux thèmes, chacun avec ses sondes). **Corrigé en chemin** : la date d'échéance d'une parole plantée se pose à
l'écriture (C-160 ; elle ne passait jamais) ; la migration `promi_mots_v184` ; un écran qui s'ouvre passe devant. **Écarts nommés** : T1 (le toast
du prototype vit dans la fenêtre), P1 (la fiche d'une personne monte par-dessus la fiche au lieu de la refermer). **Pas encore** : RELEVER et
REJOINDRE (sans événement de ce genre avant la synchro) ; la pastille d'un mot neuf d'un Cercle (lot 5) ; le texte d'exemple de la recherche qui se
retrace au focus (C-271 : une brique pour tous les champs, Peaufiner compris). **A3** : à 330 de large, les listes suivent la largeur (le juge
l'a trouvé : la seconde colonne et le ⇅ sortaient de l'écran). Ils entrent dans le socle (les sentinelles portées y ont trouvé une liste 8 pt trop longue, un emoji accepté dans la recherche, un état rogné à 330). Juges :
`promi/JUGES-TESTS.md`, « Lot 4 ».

---

## Lot 4b · La brique commune des champs (C-271)

**(a) Porté** — « Aucun changement sec à l'écran » (C-271, v203 clôture §2 : `_retour` de lot-V203-RETOUR, le « … » du focus de lot-CURSEUR) : tout
texte d'exemple d'un champ part et revient en se traçant, par UNE brique (`src/animation/trace/retour.ts`) — la recherche de l'Index, du Fil et de
la fiche d'une personne (« Rechercher » ↔ « … » au focus), la NOTE de Peaufiner (fiche et page +), la DESCRIPTION d'un Cercle (`champExemple`) ;
« Un mot… » (`bascule`) ; « un prénom… » et « + ajouter quelqu'un » (`remplacer`, `detracerCopie`). Un seul module de tracé (C-125, C-279).

**(b) Juges** : redteam_retours (§2, ③ et ④), redteam_un_trace (C-279) — `promi/tests/rendu/champs.spec.ts`, trois sondes.

**(c) Tom sur l'iPhone**
- Index, Fil : toucher la recherche — « Rechercher » se détrace, « … » se trace ; une lettre, « … » part ; tout effacé, il revient en se traçant.
- Peaufiner › NOTE, Peaufiner d'un Cercle › DESCRIPTION : même chose.

**(d) État au 27 nov. 2026 — LE LOT 4b EST FAIT (au banc).** Écart nommé : le prototype laisse le « … » natif visible sous la copie qui se trace
(recherche ouverte, page +) — la vraie app le cache (C-271). Préexistant, hors du lot : le prototype agrandit la NOTE d'une ligne dès la première
lettre ; la vraie app non (à trancher par Tom s'il le veut identique). Juges : `promi/JUGES-TESTS.md`, « Lot 4b ».

---

## Lot 5 · Le Cercle et les membres

**(a) Porté** — SPEC-ECRANS §7 (fiche d'un Cercle : bande des dalles C-231, fil qui défile C-238, « + Planter dans le Cercle » et son menu Chiche/Promi C-230, Peaufiner ouvert par sa barre §13, Dissoudre C-192, la couleur C-150), « Un mot… » du Cercle (`promi_cercle_mots`), le + des membres près du petit disque (C-242, C-254), membres pré-choisis, création unique (C-306), la dalle du Cercle sur la Toile (`kind:'nuee'`), la ligne « Avec … » (C-252).

**(b) Juges** : redteam_nuee, redteam_nuee_entree, redteam_nuee_dalle, redteam_cercle_couleur, redteam_cercle_dalles, redteam_cercle_defile, redteam_cercle_membres, redteam_cercle_plus, redteam_cercle_plus_membres, redteam_cercle_tom, redteam_creation_unique, redteam_avec, redteam_aveugle

**(c) Tom sur l'iPhone**
- Créer un Cercle : un seul Cercle, une seule dalle, une ligne au Fil (#26).
- Toucher la dalle du Cercle sur la Toile : bandeau en bas, « + Planter » au-dessus, le fil défile dessous sans saut ; dix allers-retours, la ligne « Avec … » reste.
- « + Planter dans le Cercle » → Chiche puis Promi : les membres pré-choisis, la parole plantée dans le Cercle.
- Le + des membres à côté du petit disque (Cercle, Promi, Chiche) ouvre les personnes.

**(d) État au 26 nov. 2026, soir — LE LOT 5 EST FAIT (au banc ; à voir sur l'iPhone de Tom).** Porté, en quatre étapes commitées (L5-1 à L5-4) :
la fiche d'un Cercle, un mode de la fiche (`dp-mode-nuee`) — la bande (la grille C-231, les graines d'un Cercle vide), la vague qui est le trait de
jonction, les Noyaux et le + des membres, « Avec … », le nom, la ligne d'état, le fil et ses lignes (C-238, C-259 : il défile sous la tête collée),
« Un mot… » et « Planter dans le Cercle » collés au bas, son menu (C-230 : la page + rattachée au Cercle, ses membres choisis) ; Peaufiner d'un Cercle
par sa barre (§13 : LE TRAIT, DESCRIPTION, MEMBRES, PIÈCES JOINTES, « Planter », le bloc de Ma Parole ! et LA COULEUR, DISSOUDRE et son annulation,
C-192, C-242) ; les mots d'un Cercle (« LES MOTS » au bout du fil, l'envoi, la ligne du Fil). Le schéma passe en v3 (`infosCercles` : la description,
les pièces, le trait, les mots d'un Cercle — le prototype perdait les trois premiers au rechargement), avec sa migration et l'import. **Identique au
pixel** : `cercle.spec` (au repos, vide et plein, deux thèmes), `cercle-gestes.spec` (le défilement, le menu, Peaufiner en haut et défilé, les mots,
l'envoi, A3 à 0,79), `cercle-peaufiner.spec` (dissoudre, membres, description). **Le socle parcourt la fiche d'un Cercle** (`ECRANS_PORTES`) ;
**exception nommée** : le prototype n'y atteint pas toujours son repos en temps réel (sa passe `_v16Passe` : une ligne du fil à 74 ou 79 pt d'une passe
à l'autre, même état) — les juges nœud à nœud la passent (`reposAuPixel`), elle est jugée au pixel par ses tests sur le banc piloté. **Pas encore** :
le dessin d'un Cercle (son bouton photo se déclare inactif) ; les murs de Ma Parole ! de Peaufiner (lot 8) ; ce que LE TRAIT d'un Cercle change
ailleurs ; les mots neufs d'un Cercle venus d'un autre (synchro, 1.1). Juges : `promi/JUGES-TESTS.md`, lots 5-1 à 5-4 ; à vérifier :
`promi/A-VERIFIER-LOT-5.md`.

**(e) Le 27 nov. 2026 — LE DESSIN D'UN CERCLE EST PORTÉ** (C-042, v132 : `boutonCercle`, le `_photoMenu` d'un Cercle, sa `bande`) : le bouton photo de
la fiche d'un Cercle (« Dessiner sur ce Cercle ») ouvre son menu — « Dessiner » seul (un Cercle ne porte pas de photo), « Retirer le dessin » quand
il en a un ; le mode dessin (le même que la fiche) ; POSER : le dessin REMPLACE les dalles dans la bande, l'œil le masque pour soi, la bande touchée
l'ouvre en entier. Gardé par Cercle dans la clé du prototype (`promi_dessins_cercle`, celle où la page + d'un Cercle le pose déjà). **Identique au
pixel** : `cercle-dessin.spec` (deux thèmes, une sonde). Son partage : lot 8 (Partager).

---

## Lot 6 · L'Aura et la Pelote

**(a) Porté** — SPEC-ECRANS §10, §11 (l'Aura, composition B figée, deux chiffres R-015, « Ce que tu as tenu » toutes les tenues, la plus récente en premier ; l'aide) ; SPEC-RENDU (c) la Pelote par la carte graphique (`peintGL`), densité et régulateur, sol et corps aux tons exacts (C-275), îles ΔE ≥ 15, aucun halo ni ombre (C-071 — la décision v137 prime sur §c.5), respiration, rotation ×1,5 (C-298) et axe qui dérive (C-302) ; SPEC-GESTE §6.6 caresse, creux sous le doigt et trace (C-029, C-083) ; « PARTAGER MA PELOTE » (C-294).

**(b) Juges** : releve-aura, redteam_aura_latence, redteam_pelote_doigt, redteam_enfonce, redteam_trace, redteam_bord, redteam_fourrure, redteam_plein, redteam_contour, redteam_corps, redteam_halo, redteam_zone, redteam_iles, redteam_souffle, redteam_bouton

**(c) Tom sur l'iPhone**
- Ouvrir l'Aura : la Pelote paraît tout de suite, pleine, sans liseré ni halo, en clair et en sombre.
- La regarder 1–2 min : un tour en ~67 s, la direction change en douceur (#13, #21).
- Caresser, appuyer : le creux suit le doigt, la trace reste dans le sens du geste, fluide.
- « PARTAGER MA PELOTE » sur le fond crème de l'encart, en clair (#14) ; tenir une parole : elle entre dans « Ce que tu as tenu ».

**(d) État au 27 nov. 2026, soir — LE LOT 6 EST COMMENCÉ.** L6-1 : ce que l'Aura DIT, sans rien peindre (`src/metier/aura.ts`, le prototype :
`mesPromi`, `ordreTenus`, `natureMaj`, `parts`, `personnes`, `envers`, `gensRecip`, `donnees`, `remplit`, `comptes`) — mes paroles, les tenues dans
l'ordre où elles sont apparues, la nature du sol, les anneaux (deux états), les personnes (ordre alphabétique) et ce qu'on te tient (Q215), la
phrase (cinq mots, E4), « Ce que tu as tenu » (toutes, la plus récente en premier), les deux chiffres (R-015) ; `tests/unitaires/aura.test.ts`
(valeurs en dur). **À trancher par Tom avant la Pelote (Q-L6)** : le moteur de la Pelote (`lot-AURA-PELOTE-MOTEUR`, 3 150 lignes : le velours, ses
îles, son semis, son peintre WebGL 2) n'est pas l'une des quatre pièces reprises (moteur de la Toile, tracé, flaques, jetons). Soit il devient la
CINQUIÈME, reprise octet pour octet derrière une interface typée (comme le moteur de la Toile : le rendu est garanti identique) ; soit il est
réécrit en TypeScript (plusieurs jours, et l'identité au pixel à reprouver poil par poil). Recommandation : la reprise.

**(e) État au 28 nov. 2026 — Q-L6 TRANCHÉE (Tom : « Oui, le reprendre »).** L6-2 : le moteur de la Pelote est la CINQUIÈME pièce reprise, octet pour
octet (`src/moteur/repris/pelote-moteur.js`), derrière SA façade (`src/moteur/pelote.ts`) — le lint interdit `PeloteMoteur` et `_pelote…` ailleurs.
L6-3 : l'ÉCRAN (`src/ecrans/aura/`) — la colonne de la composition B (cotes en dur dans le juge), les Noyaux (deux arcs, un jour de 3 px d'arc, le filet
crème en sombre), la légende et ses deux chiffres, « Ce que tu as tenu », « Ce qu'on t'a tenu » (flouté en gratuit), « PARTAGER MA PELOTE » (sa couleur
tirée de la palette) ; la Pelote : ses couleurs (`src/metier/pelote-couleurs.ts`, 41 tests contre les fonctions du prototype), sa rotation
(`src/metier/derive.ts`, la dérive de C-302 rejouée tirage pour tirage), ses préparations, sa respiration, son régulateur de densité ; ses gestes
(`gestes.ts` : la prise, l'élan, le creux, la trace sous le doigt, l'appui, le double toucher). Juges : `aura.spec.ts` (au repos, au pixel, deux thèmes,
Pelote comprise — exceptions M1 et G nommées), `aura-gestes.spec.ts` (les gestes, à événements égaux). Pas encore porté : l'aide (« i »), la
préparation au repos (C-135 : l'app prépare à l'ouverture), le partage de la Pelote (lot 8).

---

## Lot 7 · Le Studio et les achats

**(a) Porté** — SPEC-ECRANS §12 (vingt mondes, 24 palettes, aperçus vivants, jauge, Sombre/Clair, Avec/Sans texte, pagination en barrettes) ; SPEC-GESTE §6.4 geste de couleur (480 ms, 390 px = un tour, 48 px = une palette, C-010) ; murs du Studio (C-092, C-198) ; achats : « Adopte ce design pour 4 € / 6 € » (C-216), « Avant d'acheter » / « Plus tard » (C-190), flou en flaques puis net dès la validation (C-170), déverrouillage sans image périmée ; StoreKit (C-026) ; fluidité (C-175, Q577).

**(b) Juges** : redteam_studio_geste, redteam_studio_mur, redteam_studio_tom, redteam_studio_saccade, redteam_studio_arrivee, redteam_ramage_jauge, redteam_palettes, redteam_curseur_couleur, redteam_apercus, redteam_deverrouille, redteam_achat_fond, redteam_achat_net, redteam_achat_valide, redteam_avant_acheter, redteam_prix

**(c) Tom sur l'iPhone**
- Glisser entre les mondes, sous Mascaret, Ramage, Guingois : sans saccade.
- Appui long puis glisser horizontal, vertical, en diagonale : teinte et palette changent, on revient d'où l'on vient.
- Monde payant › « Adopte ce design » › « Plus tard » : rien acheté ; achat (bac à sable) : le Studio net aussitôt, aucune ancienne Toile (#9).
- Toucher un réglage flouté : la phrase du mur se pose sur le panneau.

---

## Lot 8 · Les Réglages, Partager, Soutenir et Ma Parole !

**(a) Porté** — SPEC-ECRANS §13 Partager (Mon Folio, Ma Toile = l'écran affiché C-105, Pelote déplaçable §6.7, partage d'une fiche C-097, d'un dessin C-068), §14 Réglages (fonds C-314, « Découvre Ma Parole ! » C-315/C-317, « Garder ta Toile », Tout effacer sans délai C-195/C-233, mention d'un dessin partagé), §16–19 (langue, Vie privée, légal, à propos — crédit Gilbert C-025), §20 l'offre, §21 les murs (dix-huit phrases C-063, flou 4,8 px, compteur global, C-100), Soutenir (C-217, C-313, C-318, C-319 ; montant libre à trancher pour Apple), PROMI ouvre Ma Parole ! en gratuit (C-316), §26 confirmations et toasts.

**(b) Juges** : redteam, redteam2, redteam3, redteam_toile, redteam_geste, redteam_partage_toile, redteam_partage_fiche, redteam_partage_dessin, redteam_pelote_partage, redteam_murs, redteam_murs_toucher, redteam_maparole, redteam_promi_porte ⇄1, redteam_soutien, redteam_soutien_autre, redteam_soutien_paye, redteam_tout_effacer, redteam_effacer_net, redteam_garder_toile, redteam_v164b ⇄4, redteam_audit_v163 ⇄3

**(c) Tom sur l'iPhone**
- Partager › Ma Toile : l'image est la Toile affichée (même cadrage, couleurs, thème) ; une fiche (Promi, Chiche, Cercle) se partage seule.
- Réglages › Tout effacer : la feuille, puis l'aplat de l'onboarding, « Toi, c'est … ? » (#5).
- Soutenir Promi : rangée jusqu'à 150 €, « Autre montant » ouvre le clavier de chiffres, le prix payé remonte, « Un grand Merci » (#33, #38, #39).
- En gratuit : PROMI de l'accueil ouvre Ma Parole ! ; toucher un mur (Peaufiner, Aura, Réglages) : la phrase seule, puis l'offre (#36).
- Réglages et Ma Parole ! en clair et en sombre : même fond que l'Index, encart « Découvre Ma Parole ! » au bleu Promi (#34, #35, #37).

---

## Lot 9 · L'onboarding et le guide

**(a) Porté** — SPEC-ECRANS §2 (prénom « [Prénom], donc. », parole, trait, « Promi planté ! » pas à pas, compte) ; le verrou (C-073) ; textes de Tom mot pour mot (C-006, C-124, C-159, C-165) ; l'échelle unique (C-138) ; ordre d'apparition (C-211, C-212, C-266) ; transitions en flaques (C-141) ; clavier (C-164) ; parole longue (C-180) ; validation sans sursaut (C-270) ; le guide (C-094, C-146, C-203, C-205, C-268, C-277, C-284) : Studio obligatoire, + et Partager facultatifs, phrase 2, flèches en goutte, lettres de « Studio » exactes (C-204). Le tracé des lettres y est vu en premier par Tom.

**(b) Juges** : redteam_onboarding, redteam_onboarding_complet, redteam_onboarding_texte, redteam_onb_exemple, redteam_onb_mots, redteam_onb_ordre, redteam_onb_rejeu, redteam_onb_sorties, redteam_onb_toucher, redteam_onb_validation, redteam_verrou_onboarding, redteam_clavier_onb, redteam_echelle_onboarding, redteam_transitions_onb, redteam_fleche_onb, redteam_suite_libelle, redteam_parole_longue, redteam_appartient, redteam_mots_sombre, redteam_naissance_onb, redteam_guide, redteam_guide_calme, redteam_guide_cloture, redteam_guide_conditions, redteam_guide_fleche, redteam_guide_fond, redteam_guide_phrase, redteam_guide_rafale, redteam_guide_retour, redteam_guide_studio, redteam_ordre_guide, redteam_cloture_delai, redteam_passages, redteam_couleurs_exactes

**(c) Tom sur l'iPhone**
- Données effacées, en clair puis en sombre : prénom, parole courte puis longue, tracé — chaque texte se trace, jamais d'un coup ; la flèche et « trace pour planter » arrivent avec le trait.
- « Promi planté ! » : quatre touchers, texte qui remonte et dalles qui descendent, « La suite t'appartient. » lettre à lettre aux tons exacts.
- Guide : flou en flaques, seul le Studio net ; toucher ailleurs redit la phrase ; Studio refermé → le + puis Partager, puis « Le reste s'explore à ton rythme ! ».
- Relancer l'app : ni onboarding ni guide ne reviennent ; « Revoir la présentation » les rejoue.

---

## Lot 10 · La veille

**(a) Porté** — `lot-V161-VEILLE` : départ après 75 s sans toucher (C-249), jamais en saisie ni en geste, compteur des doigts posé avant tout écouteur (C-181 §3), le temps de sommeil ne compte pas (C-232), logo aux couleurs exactes ×1,5 (C-300), bords de l'app et forme de l'écran / découpe de la caméra (`__ecranForme`, C-300), amande au coin, entrée et sortie en flaques, toucher qui n'actionne rien ; écran retenu allumé (Wake Lock / `isIdleTimerDisabled`, C-236).

**(b) Juges** : redteam_veille, redteam_veille_60, redteam_veille_bords, redteam_veille_depart, redteam_ecran_allume

**(c) Tom sur l'iPhone**
- Ne plus toucher : la veille part à 75 s, pas avant, depuis l'accueil, une fiche, l'Aura (#10).
- Le fond couvre tout l'écran, le logo rebondit jusqu'aux bords et coins du bas, jamais à travers l'île (#16, #20).
- Verrouiller puis rouvrir : la veille ne part pas aussitôt ; l'écran ne s'éteint pas seul pendant l'usage.
- Toucher la veille : l'écran d'avant, rien d'actionné.

---

## Lot 11 · Les notifications et les vibrations

**(a) Porté** — SPEC-ECRANS §15 (page Notifications : paroles datées, en l'air, l'heure, ce qu'on me lance) ; R-020 à R-026 (« Je te le rappelle ? » après une parole datée, deux « pas besoin » puis plus rien, rien quand la date est passée, une par jour, mots au caractère près) ; notification locale (preuve §4, VALIDATION #18) ; vibrations : `promiHaptique('tenir')` → Haptics (C-022, crochet E3).

**(b) Juges** : redteam_notifs
(Le crochet haptique est vérifié par redteam_tenir_e3, rangé au lot 3 — à étendre ici d'un test du branchement Haptics.)

**(c) Tom sur l'iPhone**
- Planter une parole datée : « Je te le rappelle ? » ; « oui » demande la permission, pas avant ; deux « pas besoin » → plus jamais.
- Une parole pour demain, l'heure choisie proche : la notification arrive, mot pour mot ; date passée : rien.
- Quitter l'app une minute : la notification arrive ; revenu avant : non (#18).
- Tenir une parole : la vibration se sent au lever du doigt (rien sous « Réduire les animations » si décidé).

---

## Lot 12 · Android

**(a) Porté** — la même app dans la coquille Capacitor Android : WebView Chromium, zones sûres et bords, retour système (le X et la pile C-193), Wake Lock, notifications locales et permission Android 13+, Haptics, achats Google Play (paliers Soutenir), polices embarquées.

**(b) Juges** : aucun propre — **toute la série des lots 1–11 se rejoue sur l'appareil Android** (gestes au doigt : studio_geste, premier_toucher, elan ; banc_rendu au pixel).
⚠ Rappel §8 : Chromium regroupe les `pointermove` (`getCoalescedEvents`) — sur Android c'est le comportement réel, l'inverse du banc iOS.

**(c) À vérifier sur un Android** (pas l'iPhone)
- Le parcours onboarding → planter → tenir sur les trois natures, fluide.
- Bouton retour système : ferme Peaufiner seul, puis la fiche, puis rend l'Index/Fil au même défilement.
- La veille à 75 s, l'écran retenu ; la notification à une minute ; la vibration de tenir.
- Le Studio : glissés et achat de test Google Play.

---

## Le chapitre de l'engagement (à part)

**Chantiers** : C-073 E0 garde-fous (spéc de test ; verrou porté au lot 9) · C-074 E1 (main fantôme — supprimée, C-139 : **le chevron orange / demi-trait est l'invitation**, rien d'animé) · C-075 E2 (onboarding d'avant v140, `ENGAGEMENT-E2.md` = histoire) · C-076 E2bis **abandonné** (remplacé par le guide C-094) · C-077 E3 validé (porté au lot 3 : redteam_tenir_e3 R4) · C-078 E4 (porté au lot 4 : redteam_vides ; exemples au lot 2) · **à construire** : C-079 E5 phrases d'accueil · C-080 E6A la Pelote qui s'enrichit (maquette, Pelote « peignée » à zéro, accrétion, fil par personne) · C-081 E6B intégration après validation · C-082 Délier · C-027 le relevé. Amendements A1–A7 de `ENGAGEMENT.md` prioritaires ; grille anti-coercition CLAUDE.md §12.

**(b) Juges** : redteam_engagement (R1–R7, A2, A3 — à jouer aussi en sentinelle dès le lot 1)

**(c) Tom** : E5 — une phrase par lancement, jamais la même deux fois, rien vers un achat ; E6A — la planche des neuf états (0 · 1 · 3 · 12 · 40 tenus…) en clair et sombre avant toute intégration ; Délier — une issue pour un Promi jamais tenu, sans reproche.

## La 1.1 (Firebase, vraies invitations)

C-023 (page du trait partagé), C-026 (Firebase, comptes), C-093 (dessin collaboratif, SPEC-DONNEES §5 bis), les parts à plusieurs réelles (`p.parts`, `p.vuTenue` — aujourd'hui simulées par `?parts=1`). **Aucun juge propre** : redteam_part et redteam_validation (lot 3) y seront rejoués avec de vrais autres comptes.

---

## Non portés, avec la raison

| Juge | Raison |
|---|---|
| redteam_registre | hygiène de `CHANTIERS.md` (méthode), pas du produit |
| redteam_mesure | outil `?mesure=1` du prototype (le relevé de l'app réelle se teste autrement) |
| redteam_trait_105 | remplacé par redteam_trait_k (v163a), obsolète |
| redteam_nuit | le Zzz est coupé par décision (v120) ; à réécrire s'il revient |
| redteam_sans_main | la main n'existe pas dans la vraie app : rien à vérifier par construction |
| banc_tom | module de banc (WebKit, doigt, état de Tom), pas un juge — remplacé par le harnais de tests |
| releve-moodboard | compare au moodboard d'août (archive) ; la référence est désormais le prototype (`reference-v205`) |
| releve-moodboard-H | idem (juge du portage d'août, LOT 0) |

## Décisions à prendre (Tom)

1. ~~Les écrans d'une autre taille que 390 × 844~~ — **TRANCHÉ (Tom, 20 nov. 2026) : l'app S'ADAPTE à chaque écran**, elle n'est ni réduite ni centrée. 390 × 844 reste la référence (identique au pixel au prototype ; les tests d'identité y tournent). Ailleurs : largeur fluide, marges et cotes du prototype, ancrées aux bords et aux zones sûres (C-299, C-300) ; la Toile et les fonds remplissent tout l'écran, aucune bande vide. Posé dans le socle : `mise_en_page` de PROMI-TOKENS.json (`--marge-g`, `--marge-d`, `--ancre-haut`, `--ancre-bas`) ; chaque écran porté est jugé sur l'iPhone SE, le 16e, le 16 Pro Max et une taille Android (`tests/rendu/ecrans.spec.ts`, captures dans `resultats/ecrans/`).
2. **Ramage** (C-187) — reporté à son lot (Tom, 20 nov.) : sa référence de rendu attend ton œil ; dans la vraie app il entrera dans la comparaison au lot 7 (le Studio prépare sa silhouette, ce qui laisse un état dans le moteur).
3. **Le prix de Ma Parole !** (C-090) — reporté à son lot : l'abonnement n'est pas dans le fichier StoreKit tant qu'il n'est pas fixé.
4. **La re-signature hebdomadaire** — le compte développeur : reporté à son lot : avec le profil gratuit, l'app cesse de s'ouvrir au bout de 7 jours ; la reconstruire et la réinstaller (une commande, PREUVE-CAPACITOR.md) — ou ouvrir le compte développeur.
