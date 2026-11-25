# LES JUGES DEVENUS DES TESTS (C-326)

> Tom, 20 nov. 2026 : « LE LOT 1 N'EST PAS CLOS TANT QUE SES JUGES NE SONT PAS DES TESTS. » Chaque juge du prototype (`redteam_*.py`, à la
> racine) est porté en test Playwright (WebKit) qui juge **la vraie app**, avec sa décision écrite **en dur** (et sa source), et **au moins une
> sonde** : le défaut qu'il doit prendre, posé dans la page quand `PROMI_SONDE` porte son nom (`tests/rendu/aides.ts`, `sonde()`), inscrit dans
> `tests/rendu/sondes/<fichier>.json`. `npm run sondes` rejoue chaque test avec sa sonde et exige qu'il ROUGISSE. L'intégration continue passe
> les tests ET les sondes à chaque commit (quatre parts en parallèle chacun). Un juge du socle parcourt `ECRANS_PORTES` (aides.ts) : chaque lot
> y ajoute ses écrans, et le juge les couvre sans qu'on le touche.
>
> **Un lot n'est clos que quand ses juges sont ici, verts, et leurs sondes prises.** Ce qui vise un écran pas encore porté s'étend au lot dit.

Fichiers : `accueil.spec.ts` (acc), `toile-a.spec.ts` (A), `toile-b.spec.ts` (B), `socle-1.spec.ts` (S1), `socle-2.spec.ts` (S2),
`banc-rendu.spec.ts`, `entrees.spec.ts`, `demarrage.spec.ts`, `ecrans.spec.ts`, `socle.spec.ts`, et les tests unitaires (`tests/unitaires/`).

## Lot 1 — l'accueil et la Toile vivante (20 juges)

| juge                     | test(s)                                                                                  | sonde(s)                                                                                        | ce qui n'est pas porté → où, ou ce qui le remplace                                                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| banc_rendu               | banc-rendu.spec (images figées au pixel ; contre le prototype vivant)                    | — (au pixel contre la référence : tout écart rougit)                                            | —                                                                                                                                                                                         |
| redteam_rythme           | A › les constantes ; le rythme de chaque monde (20)                                      | rythme-constante, rythme-ressort                                                                | chemin réel (page +, Supprimer) → lots 2, 3 ; cadence ≥ 60 % → relevé de l'iPhone. **Mascaret, départ : 2 000 ms pour 1 834 ± 147 décidés, prototype identique (C-328, décision de Tom)** |
| redteam_vivant           | A › la vie au repos (11 mondes vivants, 4 immobiles, Réduire les animations)             | vivant-fixe, vivant-tous, vivant-reduit                                                         | « hors écran, l'Index par-dessus » → lot 4. **Touffe : préexistant dans le prototype (C-327)**                                                                                            |
| redteam_retour           | A › le retour exact (16 mondes)                                                          | retour-sans-rendu                                                                               | « cent mouvements » avec `PROMI_COMPLET=1`                                                                                                                                                |
| redteam_toucher          | B › vingt mondes, image longue, Ritournelle ; acc › toucher une dalle                    | toucher-mauvaise, toucher-heure, ritournelle-monde, toucher-dalle-voisine, double-toucher-sourd | la fiche → lot 3a (on juge la demande) ; le doigt d'iOS → VALIDATION.md                                                                                                                   |
| redteam_toucher_tolerant | B › le toucher tolérant ; tests/unitaires/accueil.test.ts                                | tolerant-rayon                                                                                  | — (C-323 : 22 pt sans la limite de 44, décision de Tom)                                                                                                                                   |
| redteam_zoom             | A › le zoom, sombre et clair                                                             | zoom-encarts, zoom-double                                                                       | persistance après fiche et Index → lots 3, 4                                                                                                                                              |
| redteam_recadre_bouton   | B › recadrer (clair, sombre) ; B › le bas de son encre ; acc › recadrer                  | recadre-rond, recadre-place, recadre-bas                                                        | durée de naissance jugée au calme                                                                                                                                                         |
| redteam_deplace          | B › déplacer sous cinq mondes ; acc › déplacer (C-324)                                   | deplace-place-perdue, deplace-selection                                                         | le geste réel d'iOS → VALIDATION.md (#6)                                                                                                                                                  |
| redteam_accueil          | B › l'accueil clair, sombre ; B › atteignable à dix zooms ; acc › identité au pixel (×4) | accueil-cote, accueil-atteinte, identite-decale, animations-anneau                              | les écrans des portes → lots 4 à 8                                                                                                                                                        |
| redteam_barre            | B › cinquante touchers ; acc › la barre                                                  | barre-chevauche, barre-studio-sourd                                                             | —                                                                                                                                                                                         |
| redteam_toile_stable     | A › T (l'état de Tom), X, S, M                                                           | stable-empile, stable-abimees, stable-saine, stable-menu                                        | les sept pages → lots 2 à 8                                                                                                                                                               |
| redteam_toile_vide       | A › la Toile vide                                                                        | vide-colore                                                                                     | premier lancement → lot 9 ; VALIDATION.md (#4)                                                                                                                                            |
| redteam_evol             | B › une dalle arrive puis part, cinq mondes                                              | evol-recadre, evol-travail                                                                      | la Pelote → lot 5 ; durées au calme                                                                                                                                                       |
| redteam_pleine           | B › une Toile pleine                                                                     | pleine-rendu                                                                                    | Fil et Index à jour → lot 4                                                                                                                                                               |
| redteam_decoupe          | B › une dalle n'est jamais une image découpée                                            | decoupe-fragment, decoupe-affichage                                                             | fiche, Index, Fil, Aura, Studio, Partager → lots 3 à 8                                                                                                                                    |
| redteam_dalle_figee      | B › la même couleur à chaque ouverture ; B › une dalle plantée garde sa couleur          | dalle-hasard, dalle-perdue                                                                      | cartes de l'Index et du Fil → lot 4                                                                                                                                                       |
| redteam_ritournelle      | A › Ritournelle, 1 à 15 paroles                                                          | ritournelle-serre                                                                               | le vrai chemin de plantation → lot 2                                                                                                                                                      |
| redteam_ramage_onde      | A › Ramage, la plume d'un coup                                                           | ramage-film                                                                                     | l'aperçu du Studio → lot 7                                                                                                                                                                |
| redteam_clair_sombre     | B › la bascule (1, 5, 25, 50 paroles), l'ouverture, la dalle seule, l'image              | cs-bascule, cs-ouverture, cs-dalle, cs-image                                                    | Studio → lot 7 ; Partager → lot 8                                                                                                                                                         |

## Le socle transversal (27 juges, rejoués à chaque lot)

| juge                 | test(s)                                                                   | sonde(s)                                                          | s'étend à                                                                |
| -------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------ |
| redteam_couleurs_ref | S1 › couleurs nœud par nœud contre le prototype                           | couleurs-encre                                                    | chaque écran porté ; les dalles des cartes → lots 2 à 4                  |
| redteam_decisions    | S1 › décisions de couleur de Tom                                          | decisions-i                                                       | fiches, page +, Index, Fil → lots 2 à 4                                  |
| redteam_joignable    | S1 › chaque élément touchable reçoit le doigt                             | joignable-recouvert                                               | « chaque fonction appelée existe » : TypeScript strict (`npm run types`) |
| redteam_ecrans       | S1 › chaque écran s'ouvre, rien ne déborde ; S1 › l'accueil               | ecrans-deborde, ecrans-pastille                                   | écrans des lots 2 à 9 ; le compteur du Fil → lot 4                       |
| redteam_volume       | S1 › sources ; S1 › rendu                                                 | volume-source, volume-rendu                                       | l'ombre de la Pelote → lot 5                                             |
| redteam_air          | S1 › l'air à l'encre, jamais plus serré que le prototype                  | air-rapproche                                                     | blocs centrés de l'Aura → lot 5                                          |
| redteam_flash        | S1 › rien ne paraît une fraction de seconde                               | flash-couche                                                      | page + composée, plantation qui coupe → lot 2                            |
| redteam_superpo      | S1 › deux textes ne se recouvrent jamais                                  | superpo-texte                                                     | —                                                                        |
| redteam_aspect       | S1 › aspect A ; S1 › aspect B                                             | aspect-place, aspect-image                                        | détracé pas à pas (D) → lots qui tracent (2, 3, 9)                       |
| redteam_filets       | S1 › aucun trait hors moodboard ; aucun filet crème dans un canevas       | filets-dom, filets-canevas                                        | canevas des fiches → lot 2                                               |
| redteam_tonsurton    | S1 › l'anneau du + se détache de la barre                                 | tonsurton-anneau                                                  | fiche, page +, cartes, Fil, l'instant → lots 2 à 4                       |
| redteam_lexique      | S1 › aucun terme banni ; la loi des points                                | lexique-terme, lexique-point                                      | —                                                                        |
| redteam_emoji        | S1 › aucun champ n'accepte un emoji (« non jugé » au lot 1 : aucun champ) | emoji-champ                                                       | champs → lots 2, 3                                                       |
| redteam_secs         | S1 › aucun changement sec                                                 | secs-texte                                                        | parcours des lots 2 à 8                                                  |
| redteam_secs2        | S2 › le symbole « recadrer » naît et part en flaques                      | secs-recadre                                                      | contrats A à G → lots 2 à 8                                              |
| redteam_croix        | S2 › × FERMER est un seul X                                               | croix-fermer, croix-taille                                        | les écrans à croix → lots 3a à 8                                         |
| redteam_vide         | S2 › un écran n'est jamais vide (enchaîné, sans recharger)                | vide-reste                                                        | écrans des lots 2 à 5                                                    |
| redteam_enchaine     | S2 › enchaîner deux écrans                                                | enchaine-classe                                                   | couples page +, fiche, Index, Fil → lots 2 à 4                           |
| redteam_tokens       | S2 › les jetons font autorité (statique)                                  | tokens-valeur, tokens-couleur-dur, tokens-police-dur, tokens-face | JSON ↔ CSS ↔ Swift : `npm run jetons:verifie`                            |
| redteam_polices      | S2 › aucune graisse hors des cinq faces                                   | polices-graisse                                                   | —                                                                        |
| redteam_lettres_bleu | S2 › les lettres qui clignotent (C-281)                                   | bleu-terni                                                        | Partager, Réglages → lot 8 ; l'onboarding → lot 9                        |
| redteam_kaki         | S2 › la source ; S2 › la Toile des vingt mondes                           | kaki-palette, kaki-rendu                                          | —                                                                        |
| releve-design        | S2 › le contrat visuel contre le prototype                                | design-ecart, design-neutre                                       | les 26 cibles de la fiche et du Cercle → lots 3a, 5                      |
| redteam_app          | S2 › la red team de l'app (390 × 844, 330 × 714, 390 × 651)               | app-recouvre, app-erreur                                          | —                                                                        |
| redteam_fonctions    | S2 › l'inventaire des fonctions de l'accueil                              | fonction-perdue                                                   | planter, tenir, chercher, trier, Peaufiner → lots 2 à 8                  |
| redteam_champs       | S2 › le contrôle qui remplit (rien à remplir au lot 1)                    | champ-sourd                                                       | page +, fiche, recherche → lots 2 à 4                                    |
| redteam_pastilles    | S2 › le contrôle qui touche                                               | pastille-morte                                                    | Peaufiner, la phrase → lots 2, 3b                                        |

## Trouvé en portant, et corrigé dans la vraie app (C-326)

- **La couleur d'une dalle plantée** n'était pas gardée par le magasin : au rechargement, elle en changeait. La façade rend maintenant au magasin la couleur que le moteur fige (et celle de chaque Cercle), et pose la couleur tirée du titre et de la personne (Q213).
- **Les zones de toucher de la barre** n'étaient pas celles du prototype (C-106) : l'AURA prenait 5 pt du mot STUDIO, le FIL 3 pt d'INDEX.
- **Le symbole « recadrer »** était 2 pt trop bas (C-188).
- **Le frémissement de la Toile** 1,5 s après le chargement (le prototype, app.html ≈ l. 7271) n'était pas porté : sans lui, les graines restent jusqu'à 0,6 pt de leur place.

## Lot 2a — la page + et la phrase (21 juges de 2a ; les 27 autres du lot 2 : 2b, 2c)

Fichiers : `page-plus.spec.ts` (PP, identité au pixel), `page-plus-juges.spec.ts` (PJ), `tests/unitaires/page-plus.test.ts` (U).
**Fin du 2a (ce commit)** : le choix d'un Cercle, la saisie (« DÉJÀ PROMIS », le mouvement de Q598/C-234), « un prénom… » (C-122), Peaufiner (ses rangées ;
les choix qu'on y fait sont au 2b, sauf la note), le menu photo et la photo importée. Contrat remis au niveau du prototype rendu : `redteam_clavier` attendait une
place remplie à contour plein — le prototype la peint crème, sans contour. Écart admis P4 (identité) : le curseur qui clignote, caché des deux côtés.
⚠ (historique, avant ce commit) **PARTIEL** : la page + n'est pas encore dans `ECRANS_PORTES` (elle est prête dans `PAGES_PLUS`, aides.ts) — jugée par le socle en partie :
joignable et écrans y ont trouvé deux défauts, corrigés (l'accueil restait visible et touchable sous la page + ; le rail ne déclarait pas
qu'il glisse — `redteam_joignable` porté excuse maintenant, comme `redteam_ecrans`, ce qui est hors de la vue d'une rangée `data-glisse`) ;
les 25 autres juges du socle n'ont pas tourné sur elle : au 2b.
Contrats remis au niveau de la décision (la pilule OUVRE maintenant la page +, qui couvre l'accueil) : `redteam_fonctions` (socle-2), « l'accueil
(direction B) » (toile-b) et la barre (accueil.spec) referment la page + par son X (`refermerPagePlus`) avant le geste suivant ; `redteam_champs` ne compte
plus un champ sans boîte rendue (un écran fermé : `#phIn` dans la page + cachée). Rouge préexistant, vu sur `4d6c959` : « une dalle n'est jamais une
image découpée » (un fragment de Toile recopié hors du moteur au menu du +).

| juge                   | test(s)                                                                                                                                                                                                              | sonde(s)                  | ce qui n'est pas porté → où, ou ce qui le remplace                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| releve-S3-page-plus    | PP › identité au pixel (Promi, Chiche, Cercle ; les choix ouverts d'un Chiche et d'un Cercle ; la saisie, un titre tapé, « un prénom… » ; Peaufiner ×3 ; le menu photo ×2 ; clair, sombre)                           | pp-identite-decale        | la page validée (le trait et sa genèse) → 2b                                                                                              |
| redteam_pages_plus     | PP › identité au pixel                                                                                                                                                                                               | pp-identite-decale        | le mot du trait et le trait (C-157) → 2b                                                                                                  |
| redteam_menu_plus      | PJ › le menu du + : chaque pilule ouvre SA page +, à chaque fois ; le X la referme en glissant                                                                                                                       | menu-nature               | —                                                                                                                                         |
| redteam_tuiles         | PJ › le menu du + (au pointeur, deux tours, trois natures)                                                                                                                                                           | menu-nature               | le doigt d'iOS → VALIDATION.md                                                                                                            |
| redteam_pilules        | PJ › les trois pilules se lisent, ≥ 4,5:1 (clair, sombre)                                                                                                                                                            | pilules-illisibles        | —                                                                                                                                         |
| redteam_phrase         | PJ › la phrase de chaque nature, le cycle du verbe                                                                                                                                                                   | verbe-sourd               | la phrase alimente la parole plantée → 2b                                                                                                 |
| redteam_verbe          | PJ › le cycle du verbe (« la bascule mène à un vrai bouton »)                                                                                                                                                        | verbe-sourd               | —                                                                                                                                         |
| redteam_demande        | PJ › promets-moi (la place du prénom, l'exemple de C-309)                                                                                                                                                            | verbe-sourd               | le pluriel « promettez-moi » sur deux personnes : écrit, non jugé                                                                         |
| redteam_suggestions    | PJ › les exemples (1, 2, puis sans remise, la liaison) ; U › le tirage                                                                                                                                               | exemple-fige              | —                                                                                                                                         |
| redteam_marges         | PJ › la phrase tient dans ses marges (trois natures)                                                                                                                                                                 | marges-deborde            | 375 pt et le profil iPhone réduit → l'adaptation (ecrans.spec) au 2b                                                                      |
| redteam_gens           | PJ › le choix des personnes ; PJ › le choix d'un Cercle (« Moi » en tête, Gilbert 23,1, #291547, 25 pt sous la phrase) ; PP (Cercle, choix ouvert)                                                                   | gens-sourd, cercle-chiche | Peaufiner (À QUI, AVEC : retirés de la page + en v163b) ; MEMBRES d'un Cercle dans Peaufiner → 2b                                         |
| redteam_ajouter        | PJ › « + ajouter quelqu'un » sur sa ligne, 16 pt au-dessus de Peaufiner                                                                                                                                              | gens-sourd                | —                                                                                                                                         |
| redteam_ajout_personne | PJ › ajouter une personne (C-122 : la zone est le champ, le « + » #FB4C0D à la hauteur des capitales, Retour, un nom connu garde son écriture, la ligne 8 pt au-dessus du clavier simulé) ; PP (« un prénom… » tapé) | plus-sourd                | planter à plusieurs (UNE parole) → 2b ; la fiche (D) → lot 4                                                                              |
| redteam_moi_toucher    | PJ › « moi » à la place touchée (C-304)                                                                                                                                                                              | gens-sourd                | —                                                                                                                                         |
| C-332 (Tom)            | PJ › le choix des personnes, promi · chiche · nuee : « Moi » se coche et se décoche, coexiste, revient ; la phrase par détracé puis tracé                                                                            | moi-exclusif, moi-sec     | —                                                                                                                                         |
| redteam_moi_phrase     | —                                                                                                                                                                                                                    | —                         | « moi » après la validation (C-269) → 2b (la validation)                                                                                  |
| redteam_je             | PJ › la saisie ×3 (« rien ne part d'un coup » : DÉJÀ PROMIS, le rail, « garder de côté », la barre ; un nœud rebâti à sa place n'est pas un départ)                                                                  | deja-sec                  | la phrase elle-même (la bascule du verbe, C-296 ; un mot qui change) → 2c                                                                 |
| redteam_garder         | PJ › « garder de côté » (inactif, actif, la page entière au magasin, la place, l'inclinaison)                                                                                                                        | garder-rien               | le message « gardé de côté — dans l'Index » (un toast, §26) → lot 8                                                                       |
| redteam_garder_reprise | U › la reprise met à jour le gardé de côté (`repris`)                                                                                                                                                                | —                         | rouvrir depuis l'Index → lot 4 (la carte d'un gardé de côté)                                                                              |
| redteam_pinceau_rail   | PJ › le rail glisse ; les murs                                                                                                                                                                                       | rail-fige                 | la phrase du mur au toucher → lot 8 (§21)                                                                                                 |
| redteam_clavier        | PJ › la saisie : le clavier s'ouvre dans le geste                                                                                                                                                                    | clavier-differe           | —                                                                                                                                         |
| redteam_clavier_doux   | PJ › la saisie ×3 (Q598, C-234 : la page monte et revient d'un mouvement, 360 ms ; aucun pas > 35 % au calme, durée ≤ 460 ms sur le Mac)                                                                             | saisie-seche              | le libellé du trait (« trace pour … ») → 2b ; échelle 0,79 et les deux thèmes : PP seulement                                              |
| (C-213, C-229)         | PJ › à l'ouverture, rien du trait et l'horizon bas                                                                                                                                                                   | trait-ouverture           | la montée de l'horizon et la genèse → 2b                                                                                                  |
| (lot-CURSEUR, §5)      | PJ › la saisie d'un titre : la place remplie crème, sans contour ; le curseur 3 pt × 0,82 em, 1,06 s                                                                                                                 | place-pointillee          | —                                                                                                                                         |
| redteam_peaufiner      | PJ › Peaufiner ×3 (C-134 : il reste ouvert ; la note s'écrit sur place ; 60 pt ne referment pas, 220 referment ; son X)                                                                                              | peauf-reste               | les choix DANS Peaufiner (l'échéance, le Cercle, les pièces jointes, MEMBRES) → 2b ; la sonde du chemin inconnu (D) et la fiche → lot 4   |
| redteam_peauf_x        | PJ › Peaufiner ×3 (C-220 : refermé, aucun texte du tiroir ; la page à ses cotes d'avant ; rouvert, ses rangées)                                                                                                      | peauf-reste               | l'échelle 0,79 → PP                                                                                                                       |
| redteam_photo_menu     | PJ › le menu du bouton photo (« Dessiner » en tête ; « Importer une photo » : le sélecteur DANS le geste ; la photo remplace la dalle ; « Retirer la photo » ; un Cercle : « Dessiner » seul) ; PP (menu ouvert ×2)  | photo-sourd               | « Dessiner » (l'outil) → le lot du dessin ; la dalle d'origine et le partage (A, C, D, E) → la fiche, lot 4                               |
| (A3, porte de qualité) | PJ › A3, à 0,79 (330 × 714) : la page + dans chacun de ses états — rien ne sort de l'écran, aucun nom coupé net, le X de Peaufiner atteignable                                                                       | a3-fixe                   | trouvé et corrigé en le jugeant : le choix d'un Cercle à deux colonnes de 162 fixes, ses noms coupés net, le X de Peaufiner posé à 304 pt |
| redteam_cercle_membres | —                                                                                                                                                                                                                    | —                         | « + Planter dans le Cercle » → la fiche d'un Cercle, lot 4 : non porté                                                                    |

## Lot 2b — le trait, la genèse, et ce qui reste de la page +

| Juge du prototype                                         | Test (PP = page-plus.spec, PJ = page-plus-juges.spec)                                                                                                                                                                                                                      | Sonde(s)                              | Reste                                    |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ---------------------------------------- |
| redteam_invite_page_plus (C-209, C-229)                   | PJ › l'invite à tracer ×3 (rien avant la validation ; l'horizon remonte, PUIS le trait naît en flaques ; le libellé tracé ; le départ clignote avec le I) ; PP « prete » ×3                                                                                                | invite-sec, invite-fixe               | —                                        |
| redteam_moitie, redteam_plantation_durable (C-237, C-226) | PJ › planter ×3 (lâché avant : rien ; au milieu : écrite avant le lever, la dalle naît et vole, la page part ; rechargée : là)                                                                                                                                             | plante-sans-ecrire, plante-sans-toile | la fiche ouverte après le vol → lot 4    |
| redteam_peaufiner (les choix), C-197                      | PJ › Peaufiner, ses choix (l'échéance et le calendrier, DANS UN CERCLE → « Je promets … à tout le monde », les pièces jointes ; planter les emporte)                                                                                                                       | peauf-choix-sourd, peauf-choix-perdus | —                                        |
| redteam_gens (MEMBRES d'un Cercle)                        | PJ › Peaufiner d'un Cercle : MEMBRES (coché reste coché, la rangée ouverte ; décoché il part)                                                                                                                                                                              | peauf-membres-sourds                  | —                                        |
| (§2.10, le visage)                                        | PP « personne » ×2 (un prénom validé : la pastille porte son visage) ; PP « cercle » ×2 (le Cercle choisi dans Peaufiner : la phrase, le visage, l'exemple au pluriel, la barre)                                                                                           | pp-identite-decale                    | —                                        |
| redteam_dessin (C-042, C-056, C-061, C-085, C-086)        | PJ › le dessin de la page + (tracer à l'encre du mode, les tailles 2 · 6 · 22, ANNULER, le X sans poser, POSER dans la bande — la photo part —, « Retirer le dessin », la photo qui le remplace, la parole plantée le porte) ; PP « dessin », « tailles », « couleurs » ×2 | dessin-sourd, dessin-bande-vide       | la fiche et le partage du dessin → lot 4 |
| redteam_garder_reprise (C-149)                            | PJ › la photo et le dessin d'un gardé de côté (gardés avec la page, rendus à la reprise, le même gardé mis à jour)                                                                                                                                                         | garde-sans-photo                      | la porte de la reprise (l'Index) → lot 3 |

## Lot 2c — les textes longs, les liaisons, les changements secs, le glissement continu ; le lot 2 relié en entier

Fichier : `page-plus-2c.spec.ts` (P2C) ; l'identité au pixel (PP) gagne trois cas « long » ×2 thèmes (une parole de 280 caractères, Promi et Chiche ; un nom de Cercle de 40).
**Porté** : `continu.ts` (lot-V202A-TAILLE, lot-V203-LIAISONS, lot-V203-CONTINU : la taille de la phrase par `scale`, les mots de liaison tracés et détracés, le glissement de ce qui change de place) ; `douceur.ts` (lot-V200-DOUCEUR : une place qui change se détrace pendant que l'encart va à sa largeur, la pastille se remplit ou se vide en flaques, le mot neuf se trace ; la première lettre — l'exemple part en 150 ms, C-282 ; la place vidée — l'exemple revient en se traçant, C-274 ; à la bascule du sens, la place qui part se détrace à sa place, celle qui arrive se trace ; un nœud en transition regreffé dans la phrase rebâtie) ; v46 (la taille de la phrase comme si la parole était courte, seul le titre se réduit) et la coupe « … » de C-244 §5.1 ; « + ajouter quelqu’un » ↔ « un prénom… » par détracé puis tracé.
**Trouvé en portant, et corrigé** : ① sans v46, un Cercle au nom long faisait tomber toute sa phrase à 16 pt (le prototype : 28, le nom à 12) ; ② la ligne « un prénom… » rebâtie à chaque appel perdait son tracé ; ③ un mot de liaison neuf rebâti pendant son tracé le perdait ; ④ une place qui ARRIVE rebâtie pendant son tracé restait sur son ancien mot (« qui ? » au lieu du prénom de « promets-moi ») ; ⑤ la bascule du sens se lisait après que la boucle avait rendu l'ancien texte au nœud neuf (le piège de v202a) ; ⑥ l'enveloppe du tracé laissée dans le verbe et dans un exemple coupé (le ⇄ sur sa propre ligne, « vous emmenervoir la mer ») — elle ne reste que dans la pastille d'un prénom (son visage) ; ⑦ la mesure d'un encart hors du flux, sans la largeur de la phrase, mettait une parole collée de 280 caractères sur une seule ligne de 3 651 pt.
**Écart nommé, plus doux que le prototype** : à l'entrée dans la saisie, le prototype ne fait rien glisser (Q620, dès le champ ouvert) et ses mots sautent de 5 pt (`redteam_page_plus_continu --seq=efface` rouge sur le prototype) ; dans l'app, Q620 ne vaut qu'à partir de la première lettre tapée — l'entrée glisse.
**Protocole d'identité (cas « long »)** : le prototype mesure le plafond de C-240 (`_ppPhCap`) aussi pendant le mouvement du clavier et le garde pour la parole — sa taille finale varie d'une passe à l'autre (16, 21, 30 pt relevés sur le même Promi) ; la référence est sa composition de la page POSÉE (le mouvement du clavier fini, plafond effacé, une passe de plus). La parole entre d'un coup (`insertText`).
**Instruments corrigés** (sans rien desserrer) : `redteam_page_plus_continu` — l'heure d'une image est celle de `requestAnimationFrame` ; la vitesse des voisines se lit aussi sur les images longues (entre deux images longues, toute image courte d'un glissement régulier était un « saut ») ; la place d'un mot est sa première ligne (sur deux lignes, sa boîte englobante part de la seconde). `redteam_premiere` — l'instant de la frappe est l'événement dans la page ; les 150 ms ne se jugent que sur des images de 34 ms au plus (C-227 §5). La taille de la phrase : sa mise à l'échelle se lit sur l'animation ; les valeurs intermédiaires, sur des images courtes. L'attente « page posée » des tests compte les transitions de `douceur.ts` et les mouvements de `continu.ts` (`etat().mouvement`).

| Juge du prototype                                                                                                                               | Test                                                                                                                                                                                                                                                                                                                                                                          | Sonde(s)                   | Reste                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| redteam_page_plus_continu (C-278 §4)                                                                                                            | P2C › la phrase change de place par un seul mouvement continu (valider, le sens ×3, le titre effacé : aucun saut, immobile en ≤ 4 s)                                                                                                                                                                                                                                          | continu-saut               | —                                                                                                                                                                                                                             |
| redteam_liaison (lot-V203-LIAISONS, C-278 ⑥, C-312)                                                                                             | P2C › les mots de liaison (« à » arrive : tracé ; part : détracé à sa place ; « de » → « d’ » de même)                                                                                                                                                                                                                                                                        | liaison-sec                | —                                                                                                                                                                                                                             |
| redteam_textes_longs, redteam_phrase_lignes, redteam_titres_longs (page +)                                                                      | P2C › les textes longs ×3 (la limite 280 / 40, tapée et collée ; la parole entière, rien ne se recouvre, l'air du rail 12 · 44 · 12) ; PP « long » ×3 ×2 thèmes                                                                                                                                                                                                               | long-deborde               | la fiche (le titre long, son dépliage) → lot 4                                                                                                                                                                                |
| redteam_moi_douceur, redteam_premiere, redteam_premiere_froid, redteam_exemple_retour, redteam_retours (les places de la page +), redteam_secs2 | P2C › les places de la phrase changent en douceur (la première lettre : l'exemple part en 150 ms, la lettre dans la première image ; vidée : les flaques, l'exemple retracé ; une personne ajoutée : l'encart en douceur, les flaques, le nom tracé) ; P2C › la bascule du sens (le verbe détracé puis tracé, la place qui arrive tracée, celle qui part détracée à sa place) | places-seches, sens-sec    | la fiche (« moi », la ligne de la phrase) → lot 4 ; les recherches de l'Index et du Fil → lot 3 ; « Un mot… » → lot 4 ; un navigateur relancé à chaque essai (premiere_froid) : non porté — chaque test part d'une page neuve |
| (v203 clôture §2, AUDIT-SECS)                                                                                                                   | P2C › « + ajouter quelqu’un » se détrace, « un prénom… » se trace ; « un prénom… » part et revient par le tracé                                                                                                                                                                                                                                                               | ajout-sec                  | —                                                                                                                                                                                                                             |
| (lot-V202A-TAILLE, C-273, AUDIT-SECS point 2)                                                                                                   | P2C › la taille de la phrase change en douceur en entrant dans la saisie et en la quittant (`scale`, 320 ms)                                                                                                                                                                                                                                                                  | taille-seche               | —                                                                                                                                                                                                                             |
| redteam_nature_plus (C-224 ; C-223)                                                                                                             | P2C › la page + lit sa nature (un Cercle fermé par son X, puis un Promi, un Chiche, un Cercle : chacun plante sa nature) ; C-223 : PJ › l'invite à tracer ×3 (le premier toucher arrête le clignotement)                                                                                                                                                                      | nature-collee, invite-fixe | —                                                                                                                                                                                                                             |
| redteam_prenom_alterne (C-309)                                                                                                                  | P2C › « promets-moi » : le prénom alterne à chaque retour et à chaque réouverture                                                                                                                                                                                                                                                                                             | prenom-fige                | l'échelle 0,79 : jugée par le test A3 de la page +                                                                                                                                                                            |
| redteam_genese_nature (C-278), redteam_bandeau (C-218)                                                                                          | P2C › la genèse du trait interrompue (le sens basculé à sept instants, puis une autre nature : la genèse se refait entière, aucun calque de passage ne reste) ; PJ › l'invite à tracer ×3 (effacée, tout repart)                                                                                                                                                              | genese-reste               | —                                                                                                                                                                                                                             |
| redteam_dalle_fixe (C-234)                                                                                                                      | P2C › la dalle de la page + ne zoome jamais ×2 (chaque dalle posée piégée : une taille, 18 pt de course au plus, aucun saut)                                                                                                                                                                                                                                                  | dalle-zoom                 | —                                                                                                                                                                                                                             |
| redteam_frappe_douce (C-234)                                                                                                                    | PJ › la saisie ×3 (la page monte et revient d'un mouvement de 360 ms, jamais d'un coup) — 2a                                                                                                                                                                                                                                                                                  | saisie-seche, deja-sec     | —                                                                                                                                                                                                                             |
| redteam_exemples, redteam_liaison_exemples (E4 point 4, C-312)                                                                                  | U › les exemples des pastilles vides (le sac, jamais deux fois de suite ; « de » / « d’ ») ; PJ › les exemples des pastilles vides — 2a                                                                                                                                                                                                                                       | (2a)                       | l'onboarding → lot 6                                                                                                                                                                                                          |
| redteam_dalle_unique, redteam_vol_dalle, redteam_pose_dalle (C-241, C-237, Q611)                                                                | PJ › planter ×3 (une seule dalle à la fois : la page + ne peint plus la sienne, celle qui naît est là ; elle naît et vole ; la graine reçue par le moteur) — 2b                                                                                                                                                                                                               | plante-sans-toile          | **non porté** : l'atterrissage au demi-point sur la dalle vivante et les 30 images constantes ensuite — à porter avec la Toile vivante (lot 3a)                                                                               |
| redteam_trace_lettres, redteam_un_trace, redteam_trace_present (C-125, C-279, C-206)                                                            | le module est repris octet pour octet (`outils/reprendre.py --verifie`) ; P2C (chaque transition de la page + passe par lui : tracé, détracé, découpe lue image par image)                                                                                                                                                                                                    | (P2C)                      | les textes de l'onboarding et du guide → lots 6 et 7                                                                                                                                                                          |

## Lot 3a-1 — la fiche au repos (Promi, Chiche ; chaque état, deux thèmes)

Fichiers : `fiche.spec.ts` (F, l'identité au pixel : douze cas × deux thèmes, contre le prototype ouvert par `openDetail`), `fiche-juges.spec.ts` (FJ),
`tests/unitaires/fiche.test.ts` (U) ; l'état du banc : `banc-etats/etat-fiches.json` (un cas par état de fiche). La fiche est dans `ECRANS_PORTES` : tout le
socle la couvre (sur l'état de Tom, la première parole sans mot — la liste des mots est au lot 3b).
**Porté** : `src/ecrans/fiche/` (`fiche.ts` l'écran, `ligne.ts` le trait et ses parts, `noyaux.ts` les Noyaux), `src/metier/fiche.ts` (la phrase complète,
la ligne d'état, la consigne, les parts, le mode du trait) ; `?jour=+N` et le recompte des échéances au retour au premier plan (C-160) ; l'ouverture
qui monte du bas et la fermeture qui y redescend (`.poster`) ; l'accueil couvert sous la fiche (`.couvert`, comme la page +).
**Écarts nommés** : M1 la matière de la dalle (§8 bis) ; M2 le grain des anneaux (le prototype le tire au hasard ; jugé à part, FJ) ; M3 le fondu à droite
de la rangée des Noyaux quand elle déborde (un dégradé d'août, dette de volume du prototype : la vraie app s'arrête net).
**Pas encore (étapes suivantes)** : tracer et tenir (3a-2), la jonction au défilement (3a-3), le titre modifiable (3a-4) ; le menu photo, Peaufiner, les
mots, le + des membres (3b ; ils se déclarent `aria-disabled` d'ici là) ; Partager (lot 8) ; la fiche d'une parole d'un Cercle (son disque de Cercle,
lot 5).

| Juge du prototype                                                                                                     | Test                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| releve-S1-fiches, redteam_fiches_theme (C-132), redteam_motmarque (C-046), redteam_formes, redteam_champ              | F › identité au pixel : la fiche — douze cas × deux thèmes                                                |
| redteam_fiches_orange (C-214, C-215), redteam_depart_orange (fiches), redteam_ronds (C-143), redteam_trait_k (fiches) | F (le départ orange, le libellé « trace pour … », aucun rond, l'épaisseur × 1,3)                          |
| redteam_contraste_trait (C-140), redteam_deux_etats (C-210)                                                           | F (le trait sombre de la nature, deux états, les anneaux à deux arcs) ; FJ › les anneaux des Noyaux       |
| redteam_phrase_fiche (C-069)                                                                                          | U › la phrase complète (onze formes) ; FJ › « + x personnes » se déroule ; F (cinq personnes)             |
| redteam_echeance (C-160, D5)                                                                                          | U › la ligne d'état ; FJ › une date passée s'écrit comme une date (`?jour=+120`) ; F (date passée)        |
| redteam_etat_fiche (C-207)                                                                                            | FJ › la fiche à l'échelle 0,79 : chaque cote en pt est celle de 390 × 844                                 |
| redteam_flash_etat (Q374)                                                                                             | F (la fiche posée d'un seul geste, sans repasse) ; FJ › la fiche monte du bas et y redescend              |
| redteam_part (le rendu des parts, C-115)                                                                              | F (Chiche à Rachel et Marion, une part tracée : la part pleine, l'initiale, la part fine) ; U › les parts |

## Lot 3a-2 — tracer et tenir (le geste, le ruban, le rideau, l'instant, les parts)

Fichiers : `tenir.spec.ts` (T, l'identité au pixel : six fiches × deux thèmes, deux instants — le rideau posé, « juste après »), `tenir-juges.spec.ts` (TJ),
`tests/unitaires/fiche.test.ts` (U, « tenir »). **L'horloge est PILOTÉE des deux côtés** (la vraie app : `?pilote=` ; le prototype : PILOTE de banc_rendu) :
chaque instant se lit en images, à toute charge.
**Porté** : `src/ecrans/fiche/tenir.ts` (la zone de 118 pt, le geste et sa fenêtre d'ouverture de 340 ms, le trait qui suit le doigt et revient, le ruban
amande, le rideau et sa phrase, le toucher qui presse et qui est avalé), l'instant dans `fiche.ts` (« le trait se referme », « juste après » — qui reste tant que
la fiche est ouverte, comme le prototype), `magasin.tenir` (la parole tenue, son trait, `vuTenue`, la ligne du Fil, la parole récurrente qui renaît ; ma part),
`src/natif/haptique.ts` (l'impact fort de la preuve Capacitor, validé par Tom). **Corrigé en passant (lot 2)** : les lignes du Fil prennent les guillemets
insécables et « à l'instant » du prototype (`ligneFil`, `insecable` l. 38296).
**Pas encore** : la célébration fixe pendant un défilement (C-311) et la jonction après tenir (`banc_apres_tenir`, J1–J3) — 3a-3 ; le rideau « revu » quand un
autre trace la dernière part (`_maree.revoir`) — il faut le réseau (1.1) ; l'atterrissage de la dalle au demi-point sur la dalle vivante (repris du lot 2) — 3a-3.

| Juge du prototype                                                           | Test                                                                                                             |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| releve-S5-instant, redteam_tenir (l'image), redteam_validation (seul)       | T › identité au pixel : tenir — six fiches × deux thèmes, le rideau posé et « juste après »                      |
| redteam_trait (C-107)                                                       | TJ › le seuil de 60 pt : les décisions de la vraie app sont celles du prototype                                  |
| redteam_retour_trait (C-264)                                                | TJ › lâché avant le seuil, le trait revient : image par image, la suite du prototype                             |
| redteam_ruban (C-148)                                                       | TJ › le ruban amande naît du trait au seuil                                                                      |
| redteam_tenir (la descente, la remontée), redteam_centre_validation (C-144) | TJ › le rideau descend à vitesse constante, « Parole tenue ! » centrée, remonte à 2 150 ms                       |
| redteam_tenir_presse (C-167)                                                | TJ › un toucher pendant que le vert est posé le fait remonter, et il est avalé                                   |
| redteam_tenir_e3 (E3)                                                       | TJ › « Réduire les animations » : la fiche passe tenue d'un coup                                                 |
| redteam_part (le geste), redteam_validation (ma part, C-156)                | TJ › ma part, sans être la dernière : la vague seule ; U › tenir : ma part, la dernière part, pas un des tenants |
| redteam_tenu_trait (C-189), banc_apres_tenir (les données)                  | TJ › ce que tenir écrit, comme le prototype ; U › tenir : seul, récurrente                                       |
| redteam_premier_toucher (C-263)                                             | TJ › le premier toucher prend le trait : cinq fiches de suite (le défilement : 3a-3)                             |
| redteam_fluide (C-102)                                                      | TJ › le moment « tenir » est fluide — jugé au calme seulement (C-137 : « non jugé » au-delà d'une charge de 4)   |
| redteam_celebration_fixe (C-311)                                            | 3a-3 (la fiche qui défile pendant la célébration)                                                                |

## Lot 3a-3 — défiler : la jonction (la bande, la vague, le trait plat, le geste accroché, les places sûres) et « Les Mots »

Fichier : `jonction.spec.ts` (J). **L'horloge est PILOTÉE des deux côtés**, les animations CSS gelées ; la fiche porte les trois mots de banc_jonction (Marion,
Rachel, Nico) : elle défile (257 pt). À chaque pas (0 → le bout, serré à la rencontre de 120 à 150 pt, puis retour), **l'écran entier** est comparé au pixel.
**Porté** : `src/ecrans/fiche/jonction.ts` (lot-V187-HAUT, lot-V189-JONCTION : la bande collée 0 → 112, la vague z 7, la fenêtre découpée colonne par colonne
sous le dernier pixel plein de la vague, le trait plat collé à 110 ; le geste coupé accroché ; les aimants et les places sûres a et z ; un toucher sous la bande
avalé), `src/ecrans/fiche/mots.ts` (« Les Mots » et la liste, affichées : le titre à 780, la liste à 832, le visage `_blobBg`, le nom coupé à 180 pt, la date de
`_noms.date` ; la saisie, l'envoi, les mots neufs : 3b), la fiche en deux couches (`#dpDefile` défile ; le plateau et la barre Peaufiner restent posés), la hauteur
du contenu (`ajusteLigne` : le bas + 96 au-delà de 748). **Écarts nommés** : M4, le chevron de Peaufiner que le prototype retourne en bas de la fiche (Q626) ; le visage d'un mot (le `_blobBg` du prototype, un dégradé)
en exception nommée du juge du volume (`VOLUME_BLANCHE`, Q627).
M5 : au passage à « juste après » sur une fiche défilée, la hauteur du contenu du prototype retombe un instant et son défilement en est borné (un saut
de 3 pt, sec) ; la vraie app reste où elle est (le test le vérifie, puis compare à la place du prototype). M1 couvre aussi la copie de la matière dans la bande.
**Non repris** : l'extinction de la fenêtre au repos (`eteint`, v201b) — mesuré : au repos au-dessus de `a`, le trait plat est déjà hors de la fenêtre ; le
rognage à 112 (`_v184Rogne`) — la phrase est sous la bande dans la vraie app, le prototype la pose au-dessus puis la rogne : même image.
**Corrigé en passant (CI Linux)** : la croix d'un plateau se repose quand une police finit de se charger (`poserCroix`) ; « + 3 personnes » est un mot de la phrase
(en ligne, sans apparence de bouton), comme le prototype.

| Juge du prototype                                                                 | Test                                                                                                       |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| banc_jonction, redteam_jonction, redteam_jonction_fiche, redteam_jonction_plat    | J › identité au pixel : la jonction — Promi, Chiche, Promi tenu × deux thèmes, chaque pas, aller et retour |
| redteam_points_plat, redteam_trait_entier, redteam_trait_retour, redteam_un_trait | J › identité au pixel (les points plats, le trait entier à chaque pas, le retour exact en haut)            |
| redteam_haut_fiche (sentinelle C-255 : la place du haut à chaque pas)             | J › identité au pixel (en WebKit ; le doigt dans Safari : à voir sur l'iPhone)                             |
| redteam_jonction_fiche E (le geste accroché)                                      | J › le geste accroché ne prend plus le doigt ; décroché, il le reprend                                     |
| redteam_repos_fiche (v201 ①)                                                      | J › les places sûres : les bornes et les aimants du prototype                                              |
| redteam_celebration_fixe (C-311), banc_apres_tenir (T1)                           | J › tenir une fiche à mots défilée, puis défiler pendant que le vert est posé                              |
| redteam_elan, redteam_jonction_rebond (l'élan et le rebond de Safari)             | non jugé au banc (WebKit piloté n'a ni élan ni rebond) : sur l'iPhone (A-VERIFIER-3A3.md)                  |
| redteam_mots_fiche, redteam_les_mots (l'affichage)                                | J › identité au pixel (« Les Mots » et la liste en vue) ; le reste : 3b                                    |

## Lot 3a-4 — le titre modifiable (C-280, C-244, Q621)

Fichier : `titre.spec.ts` (TI), `tests/unitaires/fiche.test.ts` (U, « renommer »). **L'horloge est PILOTÉE des deux côtés.**
**Porté** : `src/ecrans/fiche/titre.ts` (lot-V203-TITRE : le toucher, la modification dans le titre lui-même, le curseur au point touché, 280 caractères
sans retour à la ligne ni emoji, Retour / un toucher dehors / Échap, le titre vidé qui revient en se traçant, la fiche qui glisse au-dessus du clavier),
le dépliage d'un titre coupé dans `fiche.ts` (C-244, `bascule` de lot-V181B-TEXTES : 360 ms, « Un mot… » garde son air), `magasin.renommer` (le titre,
la clé de plantation gardée, les lignes du Fil, la dernière action) et la clé posée à chaque écriture (lot-V203-CLE, Q621). **Corrigé en passant** :
le moteur lit les paroles du magasin après chaque écriture (`facade.rafraichir`) — sans cela il gardait l'ancien titre et, depuis 3a-2, l'ancien état
d'une parole tenue ; un renommage repeint la Toile (`Toile.redraw`).
**Écart nommé** : les lignes du Fil sont réécrites (la décision C-280) ; le prototype ne les réécrivait plus depuis v21 (il cherche « avant » entre
guillemets à espaces ordinaires, ses lignes ont des guillemets insécables).
**Pas jugé au banc** : le clavier de l'iPhone (la fiche qui glisse au-dessus de lui) — sur l'iPhone (A-VERIFIER-3A4.md).

| Juge du prototype                               | Test                                                                                                                  |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| redteam_textes_longs D (C-244 : le dépliage)    | TI › un titre coupé se déplie au premier toucher, comme le prototype — à mi-mouvement et posé                         |
| redteam_titre_encart (C-280 §1)                 | TI › le second toucher modifie un titre coupé, sans aucun encart : l'écran du prototype en modification               |
| redteam_titre_fiche, redteam_renomme (Q621)     | TI › Retour renomme comme le prototype : le titre neuf, la clé gardée, la Toile la même (Brouillamini) ; U › renommer |
| redteam_titre_fiche (Échap, vidé, titre entier) | TI › Échap, ou le titre vidé : l'ancien revient ; un titre entier se modifie au premier toucher                       |

## Lot 3a — la fin : un Promi d'un Cercle ; et le calendrier de la page + (retour de Tom, 24 nov.)

**Porté** : les Noyaux d'une parole d'un Cercle (`noyauxDe`, `rangeeNoyaux` : « Toi » puis UN disque, le Cercle, son nom entier, l'agrégat de
toutes ses paroles — `openDetail` et `auraDisques` du prototype). La parole du banc (`PAROLE_CERCLE`) est plantée dans le prototype par sa page +.
**Le calendrier** (« AVANT » › « une date… », prototype ET app, la même solution) : la séance de Tom relevée sur son iPhone
(`banc-calendrier.html`) a nommé deux causes — ① iOS pose la date du jour dès l'ouverture (`input`, `change`), et l'appliquer rebâtissait Peaufiner :
le champ retiré de la page, iOS fermait son calendrier ; ② la rangée AVANT affichait le libellé de la pastille. La date s'applique sur `input`,
`change` et `blur` ; elle change sur place ; Peaufiner ne se rebâtit pas calendrier ouvert ; la rangée se replie à la fermeture.

| Juge                                         | Test                                                                                           | Sondes                                                         |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| releve-S1-fiches (la parole d'un Cercle)     | F › identité au pixel : la fiche — Promi d'un Cercle, deux thèmes ; U › les Noyaux d'un Cercle | fiche-cercle-sans-disque                                       |
| redteam_tenir (la parole d'un Cercle)        | T › identité au pixel : tenir — Promi d'un Cercle, deux thèmes                                 | (tenir-identite-decale, sur « Promi à soi »)                   |
| la séance de Tom (24 nov.), prototype et app | PJ › le calendrier de « une date… », la séance de Tom — prototype ; — app                      | cal-referme-_, cal-non-lu-_, cal-hors-doigt-* (les deux côtés) |

## Lot 3b-1 — Peaufiner sur la fiche ; SUPPRIMER (la feuille, « Annuler », la pierre tombale)

Fichiers : `fiche-peaufiner.spec.ts` (FP, l'identité au pixel), `fiche-peaufiner-juges.spec.ts` (FPJ), `tests/unitaires/peaufiner.test.ts`.

**Porté** : la barre « Peaufiner » de la fiche ouvre la page de réglages de la parole (`src/ecrans/fiche/peaufiner.ts`, `bati()` et `ouvre()` de lot-S2) :
la tête (son titre, le X), LE TRAIT (l'aperçu de son pinceau, 96 pt, relevé tel que `_pinceauEchantillon` le pose), À QUI / QUI OSE ?, AVEC (vide :
en pointillés), AVANT (le même choix que la page +, devenu une brique commune : `echeance` — les pastilles et le calendrier de L2), DANS UN CERCLE, la
NOTE, les PIÈCES JOINTES, les murs (LA COULEUR : la couleur que la Toile peint pour la dalle, `facade.couleurDalle`, `rgbDe` de lot-CERCLE-COULEUR),
SUPPRIMER. Un choix s'écrit tout de suite (`magasin.peaufiner`) ; une parole tenue le reste (R-005 : le prototype la repassait « en cours »
quand on changeait son échéance, un vestige d'avant v173). SUPPRIMER : la feuille (`src/ecrans/feuilles/`, `conf` et `annulable` de lot-V16), puis
`magasin.effacer` (la pierre tombale `id|titre`, v187) et le bandeau « Annuler » (`magasin.deterrer`).
**Écarts nommés** : Peaufiner, la feuille et le bandeau paraissent et partent en FLAQUES (C-130, C-271) ; le prototype les posait d'un coup ou les fondait.
Les COINS de l'appareil, Peaufiner ouvert (C1 de fiche-peaufiner.spec) : le prototype sort sa barre du masque arrondi de son banc.
**Le X de la fiche sous Linux (la CI, depuis 29,5) — DEUX CAUSES, NOMMÉES PAR UN RELEVÉ** : ① l'app posait le titre de ses plateaux d'un décalage
FIXE relevé sur le Mac (`translate` 2,94 pt — fiche, page + ; 1,3 — accueil), le prototype le calcule sur les métriques de la police
(lot-V210-ENCART) : sous Linux, 0,08 pt d'écart, et la croix, posée sur le titre, changeait de pixel — l'app le calcule maintenant comme lui
(`centrerTitre`, commun.ts ; sur le Mac : 2,94 et 1,3, inchangés) ; ② la croix du prototype garde une place calculée pendant l'ouverture tant que
l'écart est sous 0,3 pt (6,18 puis 6,45 pt d'un test à l'autre) — protocole nommé du banc (`fichesPilotees`) : sa propre passe (`_croix.passe`) la
repose, fiche posée.
**Trouvé en portant** : la feuille de confirmation était cachée par la règle `.couvert` de l'appareil (une fiche ouverte masque le reste) ; le
champ de fichiers natif (« Choose Files ») des PIÈCES JOINTES n'était caché que par la feuille de la page + — la règle est
dans les styles communs. Le prototype ajoute au chargement un fichier de démonstration (« photo-repere.jpg ») à la première parole d'un Cercle : l'état
du banc déclare la liste de fichiers de `PAROLE_CERCLE` (vide).

| Juge du prototype                                        | Test                                                                                                                  | Sondes                                     |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| releve-S2 (Peaufiner d'une fiche), redteam_peauf_rangees | FP › identité au pixel : Peaufiner sur la fiche — chaque fiche du banc, deux thèmes (ouvert, défilé au bout, refermé) | peauf-fiche-decale, peauf-fiche-avec-plein |
| redteam_peaufiner (C-134), redteam_peauf_x (C-220)       | FPJ › Peaufiner sur la fiche : la barre l'ouvre, un choix le laisse ouvert, 60 / 220 pt, son X                        | peauf-fiche-sourd                          |
| redteam_echeance (C-160), redteam_peaufiner (choix)      | FPJ › Peaufiner sur la fiche, ses choix : AVANT, DANS UN CERCLE, la NOTE, relus après rechargement                    | peauf-fiche-choix-perdus                   |
| redteam_effacer (v187), redteam_audit_v163               | FPJ › SUPPRIMER : la feuille, « Garder », « Supprimer », la pierre tombale, « Annuler »                               | supprimer-sans-tombe                       |

## Lot 3b-2 — écrire un mot sur la fiche ; les mots neufs, vus à la fermeture

Fichier : `fiche-mot.spec.ts` (FM : l'identité au pixel et les juges de comportement, contre le prototype).

**Porté** : la ligne « Un mot… » de la fiche s'ouvre au toucher (`src/ecrans/fiche/saisie-mot.ts` ; `ouvre`, `ferme`, `envoie`, `glisse` de
lot-V145-COMM) : le champ, son filet crème, la flèche ; « Un mot… » part et revient par le tracé (`motLigne`). Envoyer (la flèche, Retour) : le mot
s'écrit (`magasin.ajouterMot` : signé de mon prénom, vu ; la ligne du Fil « Tu as commenté « … » · à qui »), son texte vole jusqu'à sa place en tête
de la liste (240 ms), la fiche glisse s'il tomberait sous la barre. Le nombre de mots touché fait glisser la fiche jusqu'au premier mot neuf (C-257).
Un mot neuf porte la pastille « pas encore vu » (C-253, `.s4-att`) ; les mots passés à l'écran entre l'en-tête et la barre sont vus quand la fiche se
ferme (`magasin.motsVus` ; ni `derAct`, ni le Fil : voir n'est pas agir).
**Trouvé en portant** : au premier mot d'une parole tenue, toute la fiche remontait de 76 pt (son trait passe de 362 à 286 dès qu'elle porte un mot,
`traitFiche`) — un changement sec ; le prototype ne repose pas la fiche à l'envoi : la vraie app non plus (elle prend sa place à la réouverture).
**Écarts nommés** : M4 (Q626) — envoyé, la fiche glisse jusqu'à 60 pt de son bas, et le prototype retourne le chevron de Peaufiner (le dépli d'août)
sur un tiroir fermé ; la vraie app non. M5 — le X du prototype referme la fiche sans passer par les rangeurs de `closeAll`, où vit `_motsVus` : ses
mots ne deviennent vus qu'à la fermeture générale suivante ; la vraie app les marque quand la fiche se ferme, comme l'écrit C-253. Le curseur du
champ (sans phase commune) est caché des deux côtés. Et le toucher qui referme la saisie avale, dans le prototype, tout clic des 450 ms qui suivent
(le juge les laisse passer avant le X).
**Le juge Q621 sous Linux (titre.spec, « Retour renomme ») — rouge à chaque run de la CI depuis au moins 67f700f, vert sur le Mac** : il reçoit son
TÉMOIN (la Toile, sans renommer, sur la même durée — CLAUDE.md : « un juge de rien-ne-change fait d'abord son témoin »), et, en cas d'écart, les deux
images et la boîte des pixels écartés dans les résultats de la CI : la cause se lira là.

| Juge du prototype                                          | Test                                                                                                           | Sondes                            |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| redteam_commentaires, redteam_envoi_mot, redteam_retours ④ | FM › écrire un mot sur la fiche, comme le prototype — ouverte, tapé, envoyé ; le mot, le Fil (deux thèmes)     | mot-sans-filet, mot-signe-moi     |
| redteam_nombre_mots (C-257), redteam_mots_neufs (C-253)    | FM › le nombre de mots fait glisser la fiche jusqu'au premier mot neuf ; un toucher ailleurs referme la saisie | mot-reste-ouvert, mots-jamais-vus |

## Lot 3b-3 — le bouton photo d'une fiche : le menu, la photo, la dalle d'origine

Fichier : `fiche-photo.spec.ts` (FPh : l'identité au pixel, les entrées du menu, la décision Q365, contre le prototype).

**Porté** : `src/ecrans/fiche/photo.ts` (`_photoMenu` de lot-V117-PHOTO-MENU, ses entrées de lot-V132-DESSIN, `_photoPeint` de lot-PHOTO) — le menu
compact à gauche du bouton (« Dessiner », « Importer une photo », « La dalle d'origine » / « La dalle du Studio », « Retirer la photo ») ; la photo
REMPLACE la dalle (en couverture, bornée par l'onde ; cadrée si `photoCadre`) et le dessin ; le bouton porte alors le signe du retour ;
`magasin.photo`. La dalle d'origine : peinte dans le monde de sa plantation, sa couleur gardée sauf ton sur ton face au champ (Q365, ΔE 15 :
`src/metier/origine.ts`, le Lab du prototype ; le Lab de la dalle, déclaré par le moteur : `facade.labDalle`). Le bouton survolé ou pressé est plein
(`:hover`, `:active` : sur l'iPhone le survol reste après le toucher). La photo de la page + suit la parole à la plantation (elle se perdait : un
manque du lot 2).
**Trouvé, caché par le masque M1** : la vraie app rendait la dalle de la fiche et de la page + dans le thème de l'app — en clair, une dalle claire
sur un corps sombre ; le prototype les rend « comme en sombre » (C-132, `lot-V146-FICHE` : `_shThemeOverride` le temps de l'appel). La façade le
fait maintenant (`enSombre` : `poserDalle`, `dalleAvenir`, `labDalle`). C'est la décision Q365 (le ΔE déclaré des deux côtés) qui l'a prise.
**Le juge Q621 sous Linux — la cause, lue sur les images de la CI** : le témoin passe (la Toile se répète sans renommer) ; au renommage, UN pixel du
bord d'une dalle change dans l'app (488, 556 du canevas) — et le PROTOTYPE, rejoué à côté, change 14 412 pixels de sa Toile. Le juge : la Toile de
l'app ne change pas plus que celle du prototype (le nombre de pixels, et leur boîte dans la sienne) ; sur le Mac, 0 et 0 ; la sonde reste prise.
**Écarts nommés** : « Dessiner » est dans le menu, inactif jusqu'au 3b-5 (le dessin sur la fiche) ; le menu paraît et part en flaques (C-271 ; le
prototype le posait d'un coup). La dalle d'origine est sous M1 : jugée par sa décision (Q365), pas au pixel.

| Juge du prototype                        | Test                                                                                             | Sondes                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| redteam_photo_menu (v117), redteam_photo | FPh › le bouton photo d'une fiche : le menu, la photo importée, la dalle d'origine (deux thèmes) | menu-photo-large, origine-garde-photo, dalle-fiche-en-clair |
| redteam_origine (Q365)                   | FPh › (le même) : la décision « origine » / « rampe » et son ΔE, déclarés des deux côtés         | dalle-fiche-en-clair                                        |

## Lot 3b-4 — la photo d'une fiche en entier, et cadrée au doigt

Fichier : `fiche-entier.spec.ts` (FE : l'identité au pixel et le cadrage écrit, contre le prototype ; les touchers à deux doigts posés dans la page).

**Porté** : `src/ecrans/fiche/entier.ts` (lot-V131-ENTIER C-051, lot-V139-CADRE C-085, v141 C-098, lot-V140-ENREGISTRER C-091) — un toucher sur la
bande quand elle porte une photo l'ouvre en entier (la seiche pleine, l'image entière, le X, « Enregistrer » : la feuille de partage du téléphone,
sinon un téléchargement) ; un nouveau toucher la referme. Deux doigts zooment (1:1), le point sous leur milieu y reste, la photo tourne de l'angle
des doigts ; un doigt la déplace ; z de 0,3 à 8 ; le cadrage s'écrit à la fin du geste (`magasin.cadrer`). VoiceOver : la bande se déclare « Voir la
photo en entier » quand elle porte une photo. Le X : sans titre, centré sur la boîte d'origine du « X », puis la croix commune (`poserCroix`).
**Trouvé en portant** : la vue était ouverte mais cachée par la règle de l'appareil couvert (`.device.couvert`) — elle en est exemptée, comme la feuille.
**Ajouté ensuite (L3b-6)** : la même chose sur la page + (v136, C-067) — la brique est rangée dans `src/ecrans/photo/` (la vue, et la peinture
de la photo cadrée), la vue est UNE et partagée (chaque écran ne répond que pour ce qu'il a ouvert) ; le cadrage de la page + suit la parole à la
plantation (v139). Juge : PJ › « la photo de la page + en entier, puis cadrée au doigt » (les valeurs du geste calculées dans le test : 1:1, l'écart
et l'angle des doigts ; sonde `pince-page-plus-sans-zoom`).

| Juge du prototype                                                     | Test                                                                    | Sondes                              |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------- |
| redteam_entier (C-051), redteam_cadre (C-085), redteam_tourne (C-098) | FE › la photo d'une fiche en entier, puis cadrée au doigt (deux thèmes) | entier-translucide, pince-sans-tour |

## Lot 3b-5 — le dessin sur la fiche

Fichier : `fiche-dessin.spec.ts` (FD : l'identité au pixel et le dessin écrit, contre le prototype).

**Porté** : « Dessiner » (le menu photo de la fiche) ouvre le mode dessin — LE MÊME que la page + (`modeDessinPartage` : sa racine `#dessinMode`
est unique) ; POSER pose le dessin dans la bande (`dessin-fiche.ts`, `bande()` de lot-V132-DESSIN : une couche pleine, son fond et ses traits, calés en
haut, découpés 7 pt au-dessus du trait) et retire la photo (v140, C-086) ; l'œil (34 pt, x 24, 52 pt au-dessus du trait) le masque pour soi ;
« Retirer le dessin » ; le dessin posé s'ouvre en entier (jamais cadré). `magasin.dessin`.
**Relevé en portant** : le filet de l'œil fait 1 pt (deux règles du prototype s'y disputent, la dernière gagne).
**Pas encore** : le dessin d'un Cercle (lot 5) ; le partage du dessin (lot 8).

| Juge du prototype                                       | Test                                                                              | Sondes                          |
| ------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------- |
| redteam_dessin (C-042, C-061), redteam_remplace (C-086) | FD › le dessin sur une fiche : posé dans la bande, masqué par l'œil (deux thèmes) | dessin-fiche-absent, oeil-sourd |

**Ouvert, préexistant (rouge sous Linux depuis la fin du lot 3a, `1b9e2c9` ; vert sur le Mac)** : socle-2 › « × FERMER est un seul X »
(redteam_croix, C-173) — sous Linux, l'encre lue de la croix du plateau de la page + et de la fiche fait 24,3 × 21,3 pt pour 25,0 × 21,7 au X
de référence (PromiLate 29,5) ; la taille et la police déclarées sont justes. Cause non nommée (la phase de la croix dans le pixel, ou la mesure
de PromiLate par le canevas sous Linux : à relever, comme pour le X de la fiche au 3b-1). Même croix, même cause probable : socle-1 › « aspect B » (le « X » de la fiche, 2,04 % de pixels écartés, sombre et clair), rouge sous Linux sur 827cd63 et 8f5c640.

## Lot 3b-7 — LE TRAIT choisi depuis Peaufiner ; la matière des pinceaux (lot-PINCEAU, lot-PINCEAU-PEAUFINER, lot-V163B-PINCEAU ; Q128, C-196)

Porté : les tracés des douze pinceaux, relevés du prototype (`lot-PINCEAU-data`) dans un JSON engendré par `outils/reprendre.py`
(`src/animation/repris/pinceaux-traces.json`, jamais retouché), derrière `src/animation/trace/pinceau.ts` (`matiereTrait` : la ligne moyenne de la
planche reportée sur l'onde de l'écran). La matière remplace le plein du trait de la fiche (`ligne.ts` : la moitié plantée, la moitié tracée, la
crête, les parts — et donc l'instant et le trait plat de la jonction), et l'amorce, la part tirée et la moitié signée de la page + (`trait.ts`).
**Avant ce lot, un pinceau choisi sur la page + ne changeait rien au trait** : c'est corrigé. Dans Peaufiner, la rangée LE TRAIT déplie le rail
(298 pt qui glissent, douze pastilles ; ceux de Ma Parole ! en murs flous) ; un toucher choisit, la rangée se replie, le trait se refait.

| Juge du prototype                                                                | Test                                                                                    | Sonde                                 |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------- |
| le rail de Peaufiner, le choix, la fiche dans la matière (lot-PINCEAU-PEAUFINER) | `fiche-pinceau.spec` (4 fiches × 2 thèmes : en cours, tenue, à plusieurs, tenue à deux) | `trait-sans-matiere`, `rail-sans-mur` |
| le trait de la page + dans la matière choisie (lot-PINCEAU)                      | `page-plus.spec` › « … prete, pinceau Coulé / Sec »                                     | `pinceau-plein`                       |

**Repris du prototype, relevé sur son rendu** : l'échantillon d'une pastille à 72 % (`#detailPoster [style*="opacity"]` l'atteint) ; déplié, « LE
TRAIT » à 12 pt et le nom d'un pinceau à 13 (le plancher d'`echelle()`). **Exception nommée N1** (après un choix) : le champ de la NOTE — le
prototype rebâtit Peaufiner et repose sa marge par une mesure (15,6 ou 16,3 pt selon l'instant). **Protocole** : le prototype posé — sa passe des
plateaux (`_plateauPartout`, le plancher des textes) passée une fois après le choix, comme il le fait de lui-même.

**La CI (Tom, 25 nov.)** : les tranches de rendu tournent sur macOS (macos-15, gratuites : le dépôt est public) — le WebKit de l'iPhone ; hors
macOS, le X d'une croix jugé à 1 pt de son encre (exception nommée). Les jugements fins (durées image par image, bords lissés, dettes relevées)
restent ceux du **Mac de Tom** (`MAC_DE_TOM` : macOS hors CI) — la machine macOS de la CI est plus lente et lisse autrement les coins de l'appareil.

## Lot 3b-8 — les personnes choisies depuis Peaufiner (le prototype : `_gensFiche`, `rend` et la saisie `SA` de lot-GENS ; C-122, C-269)

Porté : la brique des personnes, UNE pour la page + et Peaufiner (`src/ecrans/personnes/gens.ts` : la liste — « Moi » en tête, les choisies, les
connues, « + ajouter quelqu'un » ; l'ajout — l'entrée invisible, le « + » orange tracé, le clavier suivi). La page + y a été ramenée sans changer
un pixel (`page-plus.spec` : le choix ouvert, le prénom, la personne ; ses juges du choix, de l'ajout, du Cercle). Dans Peaufiner, À QUI / QUI
OSE ? et AVEC déplient la liste dans la rangée ; une personne touchée s'ajoute, sa croix la retire, « Moi » retire tout le monde ; écrit sur la
parole (`magasin.peaufiner` : `qui`, `avec`) ; la rangée reste ouverte.

| Juge du prototype                                                                            | Test                                                                                                          | Sonde                                      |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| la liste dans Peaufiner, l'ajout au toucher et au clavier, la fiche (lot-GENS, `_gensFiche`) | `fiche-gens.spec` (Promi à Marion — À QUI ; Chiche lancé à Adrien — AVEC ; × 2 thèmes)                        | `gens-fiche-sourd`, `gens-fiche-page-plus` |
| le « + » des membres près du petit disque (C-254, `ouvreGens` de lot-V181A-CERCLE)           | `fiche-gens.spec` › « le + des membres ouvre Peaufiner sur les personnes » (Promi à soi, Chiche ; × 2 thèmes) | `plus-membres-sans-glisse`                 |

**Écart nommé V1** : après un ajout, la valeur de la rangée suit le choix (« Marion, Lou ») ; le prototype la laisse à l'ancienne tant que
Peaufiner n'est pas rebâti — vérifiée en texte, masquée au pixel. **Protocole** : le prototype du banc garde des membres de Cercles de
démonstration (`NUEEMEM` : « famille », « projet ») que l'état du banc n'a pas : ils sont retirés avant de juger. **Repris du prototype** : déplié,
le libellé de toute rangée est à 12 pt (le plancher d'`echelle()`).

**La CI sur macOS — trois jugements de machine, rendus au Mac de Tom** : les sauts image par image de la page + (`page-plus-2c`, une cadence) ;
hors du Mac de Tom, un pixel isolé de 8 niveaux au plus (la couture de la tuile du grain de l'appareil) — exception nommée d'`ecart` ; la photo en
entier attendue (5 s au plus) plutôt qu'un délai fixe.

## Lot 4-1 — l'Index au repos : l'encart, la recherche, le ⇅, la grille des cartes (lot-S4, lot-V210-ENCART C-301, C-147, C-149, C-151, Q93, Q158, Q213, Q297)

Porté : l'écran de l'Index (`src/ecrans/index/index.ts`), monté par la porte INDEX de la barre ; la carte (`src/ecrans/index/carte.ts`, réutilisable
par la fiche d'une personne) — sa géométrie (`geo`), son champ qui cède à la dalle (Q93), sa dalle (la rampe de sa nature sous Ingénu, Q297), la
petite Toile d'un Cercle (Q213), son trait d'une période, son corps de fiche (C-147), son pointillé de gardé de côté (C-149), son titre ajusté
(C-151, v203) et son état resserré (Q158) ; ce que l'Index liste et dans quel ordre (`src/metier/index.ts` : « Récents », C-245). Une carte touchée
ouvre sa fiche (un Cercle : sa fiche, lot 5 ; un gardé de côté : sa reprise dans la page +).

| Juge du prototype                                                                               | Test                                                                                                    | Sonde                                   |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| releve-S4 (l'Index), redteam_titres_cartes (C-151), redteam_recents (C-245)                     | `index.spec` › « l'Index au repos et défilé au bout » (25 paroles ; × 2 thèmes) — au pixel, et les mots | `ordre-plantation`, `carte-creme-clair` |
| redteam_garde_index (C-149), redteam_reperage (Q213 : la nature et la petite Toile d'un Cercle) | `index.spec` › « l'Index avec un Cercle de deux paroles et un gardé de côté » (× 2 thèmes)              | `garde-sans-pointille`                  |
| (la règle, sans navigateur)                                                                     | `unitaires/index.test.ts` : l'ordre, la recherche, les filtres, les mots                                | —                                       |

**Exception nommée M1** : la matière de chaque dalle (sa boîte déclarée `data-matiere`, 8 pt autour) — elle respire (§8 bis). **Protocole** : le
prototype est ouvert par son bouton de la barre, puis ses images avancent par tranches (ses passes des titres partent d'un observateur, qui ne
tourne qu'entre deux tâches). **Jetons ajoutés** (vraie app) : les rampes d'Ingénu (`--c-ingenu-*`) et le pointillé sombre d'un gardé de côté
(`--c-garde-sombre`) ; `redteam_tokens` compte ces jetons propres à la vraie app parmi ses écarts au bloc du prototype (préexistant, 11 avant).
Les tests de l'accueil qui touchent INDEX referment maintenant l'Index (`fermerIndex`) avant le toucher suivant.

## Lot 4-2 à 4-5 — le menu ⇅, les écrans vides, la fiche ouverte depuis l'Index et son retour, l'ouverture (lot-S2 de l'Index, Q578, C-185, C-191, E4 v178c, C-193, C-250, C-271)

| Juge du prototype                                                            | Test                                                                                                | Sonde                |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | -------------------- |
| redteam_menu_tri (Q578), redteam_tri_menus (C-191), redteam_tri_fond (C-185) | `index.spec` › « le menu ⇅ de l'Index, ses tris et ses filtres » (× 2 thèmes : 5 choix, au pixel)   | `tri-personne-sourd` |
| redteam_vides (E4, v178c)                                                    | `index.spec` › « les écrans vides de l'Index » (× 2 thèmes) et « l'Index sans aucune parole »       | `vide-ligne-sourde`  |
| redteam_pile_retour (C-193), redteam_index_fil (C-250, le retour)            | `index.spec` › « une carte de l'Index ouvre sa fiche ; son X ramène l'Index tel qu'il était » (× 2) | `retour-en-haut`     |
| (C-271 : aucun changement sec)                                               | `index.spec` › « l'Index monte du bas à l'ouverture et y redescend au X »                           | `index-sec`          |

**Protocole** : un masque de matière (M1) ne couvre jamais le panneau du menu ouvert. **Repris du prototype** : la recherche vide écrit ses
guillemets avec des espaces insécables. **Pas encore porté** : le texte d'exemple de la recherche qui se retrace au focus (C-271, `_retour.champ`) ;
l'Index à l'échelle 0,79 (A3).

## Lot 4-6 à 4-9 — le Fil : au repos, son menu, ses écrans vides, le retour d'une fiche, le glissement, l'appui maintenu (lot-S4, `buildFeed`, C-301, C-191, C-245, C-250, C-271, Q75, Q347, C-160)

| Juge du prototype                                                   | Test                                                                                                         | Sonde                 |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------- |
| releve-S5 (le Fil), redteam_reperage, redteam_recents_fil (C-245)   | `fil.spec` › « le Fil au repos et défilé au bout » (× 2 thèmes : repos, milieu, bout, au pixel, et les mots) | `fil-tenu-sans-terre` |
| redteam_tri_menus (C-191), redteam_menu_tri (Q578)                  | `fil.spec` › « le menu ⇅ du Fil, ses tris et ses filtres » (× 2 thèmes : 6 choix, au pixel)                  | `fil-filtre-sourd`    |
| redteam_vides (E4, v178c)                                           | `fil.spec` › « les écrans vides du Fil » (la recherche, un filtre sans rien)                                 | `fil-vide-sourd`      |
| redteam_index_fil (C-250)                                           | `fil.spec` › « un bandeau du Fil ouvre sa fiche ; son X ramène le Fil tel qu'il était »                      | `fil-retour-en-haut`  |
| (C-271 : aucun changement sec)                                      | `fil.spec` › « le Fil glisse de la droite à l'ouverture et y repart au X »                                   | `fil-sec`             |
| redteam_fonctions (Q75, C-189), redteam_echeance (C-160 : REPORTER) | `fil.spec` › « l'appui maintenu sur un bandeau déplie ses gestes ; TRACER, REPORTER » (× 2 thèmes, au pixel) | `fil-appui-ouvre`     |
| (la règle, sans navigateur)                                         | `unitaires/fil.test.ts` : REPORTER depuis une échéance passée, la ligne reportée, la dernière action d'abord | —                     |

**Exception nommée M1** : la matière de chaque dalle, sa boîte seule (marge 0 : la dalle d'un bandeau est rendue pour y tenir). **Écart nommé T1** :
le toast « Reporter… » du prototype vit dans la FENÊTRE (`body`, 98 pt de son bas), hors de l'appareil — au banc 430 × 932 il tombe 44 pt plus bas que
dans l'appareil ; la vraie app le pose à 98 pt du bas de l'appareil, sans son ombre portée (une dette de volume du prototype, v137). Il est jugé sur ses mots et
ses choix, pas au pixel. **Repris du prototype** :
le panneau du menu bordé de bleu dans les deux thèmes (l'Index, en sombre, le borde de mauve) ; le bandeau « Garder ta Toile » caché sous le Fil
(`.rap-cache`) ; REPORTER crème dans les deux thèmes. **Trouvé en écrivant le test unitaire, corrigé** : la date d'échéance d'une parole plantée
n'était posée qu'à la relecture suivante, comptée depuis ce jour-là — une échéance ne passait jamais (C-160) ; elle se pose maintenant à chaque
écriture du magasin, comme `noteTout` du prototype. **Pas encore porté** : RELEVER et REJOINDRE (aucun événement de ce genre dans l'état des
fiches) ; la pastille d'un mot neuf d'un CERCLE (son magasin de mots n'est pas encore porté : lot 5) ; le Fil à l'échelle 0,79 (A3). **Repris
aussi** : la migration `promi_mots_v184` du prototype (C-253 : à l'import, les mots d'avant v184 sont comptés vus, une fois).

## Lot 4-10 — la fiche d'une personne (SPEC-ECRANS §22 ; lot-FICHE-PERSONNE, lot-DALLE-PORTE, lot-V146-NOMS ; Q184, Q193, E4 v178c)

| Juge du prototype                                                    | Test                                                                                                                  | Sonde                 |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------- |
| redteam_fiche_personne (PLANCHE-FICHE-PERSONNE-4), redteam_reperage  | `personne.spec` › « la fiche d'une personne au repos » (Rachel, Marion × 2 thèmes : au pixel, et ce qu'elle montre)   | `personne-etat-ecrit` |
| redteam_vides (E4 : « Rien entre vous pour l’instant. »)             | `personne.spec` › « une personne sans parole » (au pixel)                                                             | —                     |
| redteam_noms (C-128 : un nom se touche), redteam_pile_retour (C-193) | `personne.spec` › « un nom touché dans la phrase d'une fiche ouvre la fiche de sa personne ; « + Planter un Promi » » | `nom-sourd`           |

**Exception nommée M1** : la matière (la boîte déclarée d'une carte, 8 pt autour ; une dalle de « Tenu ensemble », sa boîte entière). **Repris du
prototype** : l'état n'est plus écrit sous les cartes (« le trait le dit », Tom) — le titre est ajusté AVANT que le mot d'état soit retiré, comme le
prototype (sinon il garde 20 au lieu de 18) ; le titre en Gilbert, interlettre −0,05 em, qui rogne ce qui dépasse de sa boîte (l'accent d'un « é ») et
dont la place avant recentrage est celle du prototype (le même arrondi au centième). **Corrigé en chemin** : un écran qui s'ouvre passe devant ceux
qui sont ouverts (la fiche, l'Index, le Fil, la personne : même z ; la fiche d'une personne s'ouvrait SOUS la fiche d'où l'on venait). **Écart
nommé P1** : ouverte depuis une fiche, la fiche d'une personne monte PAR-DESSUS elle, et son X la redécouvre ; le prototype referme la fiche
(`closeAll`) puis la rouvre au X (C-193, sa porte) — même image au repos, un mouvement de moins. **Pas encore** : les noms des Noyaux et des mots
(la même porte, jugée sur la phrase seulement).

## Lot 4-11 — A3 : l'Index, le Fil et la fiche d'une personne s'adaptent à l'écran (L0 §2)

| Juge du prototype                                          | Test                                                                                                                  | Sonde       |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------- |
| redteam_titres_cartes (C-151), releve-S3 (débordement), A3 | `listes-a3.spec` › « A3, à 0,79 (330 × 714) : l'Index, le Fil, la fiche d'une personne » (× 2 thèmes, à 390 et à 330) | `a3-titres` |

**Trouvé par le juge A3, corrigé** : à 330 de large, la vraie app (qui s'adapte à l'écran, elle ne se réduit pas comme le prototype) gardait les
cotes de 390 — la seconde colonne de cartes finissait à 366, le ⇅ à 351, hors de l'écran. La recherche, le ⇅, la liste, les cartes (deux par
rangée, 24 des bords, 12 entre elles : `deux(largeur)`), les bandeaux du Fil (16 de chaque côté) et la fiche d'une personne (ses dalles, ses
cartes, ses deux boutons) suivent maintenant la largeur ; à 390, ce sont exactement les cotes du prototype (les juges au pixel le gardent).
