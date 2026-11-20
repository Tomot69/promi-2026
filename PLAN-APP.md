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

**(d) État au 20 nov. 2026 (branche `app-L1`, C-322)** — porté : le plateau, la barre, le + (anneau, menu des natures sur place), le bandeau « Garder ta Toile », le symbole « recadrer » (en flaques), le grain de l'appareil, le toucher d'une dalle (260 ms, double toucher, tolérance C-239), l'adaptation à l'écran. Identique au prototype au pixel (≤ 2 niveaux) à 390 × 844, clair et sombre, menu fermé et ouvert (`accueil.spec.ts`). La Toile, ses mondes, la vie au repos, le dézoom, déplacer une dalle : faits par le moteur repris (copie octet pour octet), jugés par `banc-rendu.spec`, `entrees.spec` et la vie au repos d'`accueil.spec`. **Juges du lot pas encore portés en tests** : redteam_rythme, redteam_retour, redteam_vivant (durées longues), redteam_deplace, redteam_zoom (le dézoom), redteam_toile_stable, redteam_toile_vide, redteam_evol, redteam_pleine, redteam_decoupe, redteam_dalle_figee, redteam_ritournelle, redteam_ramage_onde, redteam_clair_sombre, et le socle transversal. **Aucun écran destinataire n'existe** : toucher une dalle, une entrée de la barre ou une pilule note la demande (`navigation`), rien ne s'ouvre avant les lots 2 à 9. Trouvé : C-323 (la limite de 44 pt de C-239 n'est pas appliquée par le prototype).

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

---

## Lot 5 · Le Cercle et les membres

**(a) Porté** — SPEC-ECRANS §7 (fiche d'un Cercle : bande des dalles C-231, fil qui défile C-238, « + Planter dans le Cercle » et son menu Chiche/Promi C-230, Peaufiner ouvert par sa barre §13, Dissoudre C-192, la couleur C-150), « Un mot… » du Cercle (`promi_cercle_mots`), le + des membres près du petit disque (C-242, C-254), membres pré-choisis, création unique (C-306), la dalle du Cercle sur la Toile (`kind:'nuee'`), la ligne « Avec … » (C-252).

**(b) Juges** : redteam_nuee, redteam_nuee_entree, redteam_nuee_dalle, redteam_cercle_couleur, redteam_cercle_dalles, redteam_cercle_defile, redteam_cercle_membres, redteam_cercle_plus, redteam_cercle_plus_membres, redteam_cercle_tom, redteam_creation_unique, redteam_avec, redteam_aveugle

**(c) Tom sur l'iPhone**
- Créer un Cercle : un seul Cercle, une seule dalle, une ligne au Fil (#26).
- Toucher la dalle du Cercle sur la Toile : bandeau en bas, « + Planter » au-dessus, le fil défile dessous sans saut ; dix allers-retours, la ligne « Avec … » reste.
- « + Planter dans le Cercle » → Chiche puis Promi : les membres pré-choisis, la parole plantée dans le Cercle.
- Le + des membres à côté du petit disque (Cercle, Promi, Chiche) ouvre les personnes.

---

## Lot 6 · L'Aura et la Pelote

**(a) Porté** — SPEC-ECRANS §10, §11 (l'Aura, composition B figée, deux chiffres R-015, « Ce que tu as tenu » toutes les tenues, la plus récente en premier ; l'aide) ; SPEC-RENDU (c) la Pelote par la carte graphique (`peintGL`), densité et régulateur, sol et corps aux tons exacts (C-275), îles ΔE ≥ 15, aucun halo ni ombre (C-071 — la décision v137 prime sur §c.5), respiration, rotation ×1,5 (C-298) et axe qui dérive (C-302) ; SPEC-GESTE §6.6 caresse, creux sous le doigt et trace (C-029, C-083) ; « PARTAGER MA PELOTE » (C-294).

**(b) Juges** : releve-aura, redteam_aura_latence, redteam_pelote_doigt, redteam_enfonce, redteam_trace, redteam_bord, redteam_fourrure, redteam_plein, redteam_contour, redteam_corps, redteam_halo, redteam_zone, redteam_iles, redteam_souffle, redteam_bouton

**(c) Tom sur l'iPhone**
- Ouvrir l'Aura : la Pelote paraît tout de suite, pleine, sans liseré ni halo, en clair et en sombre.
- La regarder 1–2 min : un tour en ~67 s, la direction change en douceur (#13, #21).
- Caresser, appuyer : le creux suit le doigt, la trace reste dans le sens du geste, fluide.
- « PARTAGER MA PELOTE » sur le fond crème de l'encart, en clair (#14) ; tenir une parole : elle entre dans « Ce que tu as tenu ».

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
