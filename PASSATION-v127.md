# PASSATION — après le lot v127 (4 octobre 2026)

À coller en tête de la nouvelle conversation. Elle reçoit le choix de Tom pour l'outil de dessin (par exemple « B, E2, S1 ») et reprend
les dix questions une par une. Le lot suivant, v128, est le dossier de portage (C-021).

## Où en est le projet

- Dépôt : `main`, dernier commit **`3188519`** (v127), poussé sur github.com/Tomot69/promi-2026.
- Serveur : `python3 serveur.py` (port 8752, 127.0.0.1) ; adresses : `/app.html`, `/promi-moodboard-H.html`, `/promi-nuee-toile.html` ;
  iPhone : `http://<ipconfig getifaddr en0>:8752/app.html`.
- Ce qui fait autorité : `CLAUDE.md` (bloc v127 en tête du §3, exception à la loi des points au §5), `CHANTIERS.md` (le registre :
  un numéro par demande, jamais supprimé ; seul Tom valide), `ETAT-DES-LIEUX.md` (la liste « À VALIDER SUR IPHONE » à la fin).
- Protocole : patch par `assert count==1` ; `python3 scratchpad/verif.py` après chaque patch ; série courte (juges touchés + six
  sentinelles : couleurs_ref, decisions, joignable, ecrans, volume, registre ; `banc_rendu` et `redteam_rythme` si le moteur est touché) ;
  planches @3x, version téléphone envoyée ; commit « vNNN — résumé » poussé, hash au rapport ; le rapport finit par le tableau des
  chantiers non validés ; toute demande nouvelle reçoit un numéro AVANT le travail.

## Le lot v127 (texte de Tom)

§0 · Réponses — Onboarding : voir §1. Le dessin dans la bande haute prend le numéro C-042. C-001 : la fluidité est acquise sur iPhone ;
l'avis de Tom sur le rendu viendra.
§1 · L'onboarding, dernière diapositive (C-006) — La dalle de la nouvelle parole reprend exactement sa taille et sa place d'avant v126.
Les voisines, gardées à sept (B), un peu plus grandes, au plus 60 % de sa surface, visibles en sombre, aux teintes de la palette.
`?voisines=` retiré. Texte : « Ici, c'est Promi. Et ça veut dire quelque chose. » « Un Promi, tu donnes ta parole. Un Chiche, tu tentes
quelqu'un. Un Cercle, on tient à plusieurs. » — et (message joint, C-043) : tout le texte en Gilbert, phrases espacées.
§2 · Ramage : l'onde (C-009) — le disque est un effet posé : on le supprime ; la plume pousse le long de ses traits ou, si c'est
impossible proprement, apparaît d'un coup.
§3 · La vie au repos (C-028, C-031) — retour exact au pixel (cent mouvements, zéro pixel) ; Houle jamais plus de 15 s ; un
micro-mouvement propre pour les huit mondes immobiles, trois captures par monde.
§4 · PLANCHE SEULE pour l'outil de dessin (C-042) : inventaire, rangée A/B/C, choix de taille (trois points, exception à la loi des
points), trait E1/E2 aux trois tailles, symbole S1/S2, états.

## Le rapport de v127

**§1 · Onboarding (C-006, C-043) — FAIT.** Dalle principale, à l'image, en clair : (131 ; 570 ; 158,7 × 155,0) pt, 14 710 pt² — v125 :
(132–133 ; 570–571 ; 158,7 × 155,0), 14 710 pt² (v125 varie lui-même d'un point d'un passage à l'autre) ; v126 : 63 × 83, 3 686 pt².
Sept voisines : des cellules vides du semis dépliées à 0,62 et teintes (`Toile.voisines`), 28 à 42 % de la surface de la principale,
rose et lilas (aucune bleue : la parole reste la seule bleue), visibles en sombre. Texte remplacé mot pour mot ; tout en Gilbert ;
20 px entre deux phrases (33 sous « Ça y est. »). Les mentions légales (12 px) restent en Atkinson. `redteam_onboarding` 44/44.
Planche `planche-v127/onboarding-fin*.png`. ⚠ Seul Pochade (monde du premier lancement) peint les voisines.

**§2 · Ramage (C-009) — FAIT par le repli prévu.** Le disque est supprimé. Pousser le long des traits n'a pas été fait : une plume qui
arrive redessine tout le plumage (27 % des pixels sur 84 % de la Toile), il faudrait le recalculer à chaque image. La plume arrive donc
d'un coup, en une image, au Studio et sur la vraie Toile. `redteam_ramage_onde` réécrit au niveau de la décision (seuil de 2 % gardé et
étendu à toutes les images ; le contrôle « ≥ 8 images » devient « une arrivée est vue ») : 9/9 ; 6/9 avec l'ancien film (`--film`).

**§3 · Vie au repos (C-028, C-031) — retour exact FAIT, huit mondes NON FAIT pour six.** Retour : 108 mouvements sur 12 mondes, 0 pixel
(`redteam_retour` 26/26 ; rouge sur v126). Le titre ne bouge plus. Constat : Bobinette, Esquille et Brouillamini ne bougeaient que leur
titre en v126. Bougent aujourd'hui (12) : Pochade, Touffe, Tesselle, Braille, Buvard, Houle, Taille-douce, Halin, Ritournelle, Bobinette
(réparé), Madrure et Éclisse (neufs). Immobiles (8) : Volubilis, Guingois, Mascaret, Ramage, Chantourné, Brouillamini, Chamade, Esquille.
Houle : 15,5 et 14,8 s au plus sur deux passages (aucune correction propre à Houle ; les 25 s de v126 non reproduites).
`redteam_vivant` 53/56 — trois rouges ouverts : sous Houle et Éclisse la partie VISIBLE d'un mouvement dure 0,5–0,6 s (règle : 1 à 2 s),
sous Bobinette un changement de 0,02 % hors tirage. Planche `vie-au-repos-madrure-terrazzo-bobinette.png` (Bobinette : la capture
« pendant » a manqué le mouvement).

**§4 · Outil de dessin (C-042) — PLANCHE FAITE, rien dans l'app.** `planche-v127/dessin-*` (clair et sombre, @3x, versions téléphone),
`DESSIN-INVENTAIRE.md`. À choisir : la rangée (A sous la bande, icônes · B au bas de la bande, dans un plateau · C sous la bande, icônes
et mots, rangée qui glisse), l'effilé (E1 court · E2 long), le symbole (S1 quatre quartiers · S2 symbole du Studio). ⚠ Sur un Cercle la
bande ne fait que 50 pt : A et C font descendre la colonne de 56 pt, B recouvre la bande. Les gestes de la planche du trait sont
synthétiques. Exception à la loi des points inscrite (CLAUDE.md §5) — le texte de la loi elle-même n'est écrit nulle part.

**Série.** registre 6/6 · volume ✅ · decisions 79/79 · joignable 5/5 · ecrans 152/152 · onboarding 44/44 · decoupe ✅ · ramage_onde 9/9 ·
apercus 10/10 · flash 32/32 · vide 61/61 · toile 18/18 · accueil 22/22 · dalle_figee 4/4 · tokens 46/46 · polices 0 · banc_rendu 280
images au pixel · rythme 60/60 · retour 26/26 · releve-design 0 écart · couleurs_ref 0 écart. Rouges : `redteam_vivant` 53/56
(ci-dessus) ; `redteam_air` : 10 paires de la référence ne sont plus mesurées — identique sur v126 (C-018, pas de ce lot).

## Les dix questions à reprendre une par une

Elles sont dans `CHANTIERS.md` (C-011 à C-041, état OUVERT) ; les plus pressantes : C-011 (palettes vides au Studio), C-012 (Zzz),
C-013 (îles ternies par le corps), C-015 (#DD4D23 hors état), C-032 (les quatre mondes neufs gratuits ou payants), C-034 (l'écran qui
vend), C-035 (mots de l'achat sans compte), C-038 (aide de l'Aura), C-039 (phrase du mur), C-041 (questions anciennes). S'y ajoute :
le texte de « la loi des points », à dicter.

## Tableau des chantiers non validés

| N° | La demande | État | Lot |
|---|---|---|---|
| C-001 | « BLOQUANT : la Pelote sur iPhone […] la rotation et la lumière se font par la carte graphique, sans recalcule… | FAIT, EN ATTENTE DE TOM | v125 |
| C-002 | « La double zone derrière la Pelote, en sombre. » | FAIT, EN ATTENTE DE TOM | v125 |
| C-003 | « Tom ne voit pas la teinte du corps changer d'une ouverture à l'autre […] Le halo prend la couleur du corps. … | FAIT, EN ATTENTE DE TOM | v125 |
| C-004 | « Les textes en couleur de la palette : jamais noirs. » | FAIT, EN ATTENTE DE TOM | v125 |
| C-005 | « L'Aura : composition B, figée. » | FAIT, EN ATTENTE DE TOM | v126 |
| C-006 | « Les deux phrases du concept […] passent sur la dernière [diapositive]. Le fond […] : un vrai fragment de Toi… | FAIT, EN ATTENTE DE TOM | v127 |
| C-007 | « Le travail remis après "tenir" part en tâche de fond, découpée. » | FAIT, EN ATTENTE DE TOM | v125 |
| C-008 | « Le relevé ?mesure=1 ne décale plus rien […] la Pelote reste visible. » | FAIT, EN ATTENTE DE TOM | v125 |
| C-009 | « Ramage : Tom voit une onde ronde, par intermittence, au Studio et sur la Toile. Trouve ce qui la déclenche e… | FAIT, EN ATTENTE DE TOM | v127 |
| C-010 | « Studio : le geste perdu (appui long, déplacer le doigt fait varier la palette). » | FAIT, EN ATTENTE DE TOM | v126 |
| C-011 | « Palettes vides vues par Tom au Studio. » | OUVERT | à fixer |
| C-012 | « Zzz à réintroduire. » | OUVERT | à fixer |
| C-013 | « Îles ternies par le corps. » | OUVERT | à fixer |
| C-014 | « Tests iPhone en attente. » | OUVERT | chaque lot |
| C-015 | « Usages de #DD4D23 hors état, décision de Tom. » | OUVERT | à fixer |
| C-016 | « Fond de la Toile en clair #DFCAA4, à valider. » | FAIT, EN ATTENTE DE TOM | v118 |
| C-017 | « redteam_kaki. » | OUVERT | à fixer |
| C-018 | « redteam_air et les dates. » | OUVERT | à fixer |
| C-019 | « releve-S5. » | OUVERT | à fixer |
| C-020 | « Code mort et faux positifs de redteam_volume. » | OUVERT | à fixer |
| C-021 | « Dossier de portage » (dossier `portage/`, dix documents, lecture seule). | REPORTÉ | v128 |
| C-022 | « Vibrations et notifications (conversation dédiée). » | REPORTÉ | conversation dédiée |
| C-023 | « Page du trait partagé. » | OUVERT | à fixer |
| C-024 | « Héritage : Fil en ligne de temps, visages, dalle floue de la page +, Ramage à 5,5 s sur 500 paroles, mondes … | OUVERT | à fixer |
| C-025 | « Avant publication : PromiLate, Gilbert, pages légales, version. » | OUVERT | avant publication |
| C-026 | « Avant Swift : archive, VoiceOver de la Toile, StoreKit, Firebase. » | OUVERT | avant Swift |
| C-027 | « Après le portage : délier, le relevé. » | REPORTÉ | après le portage |
| C-028 | « La Toile vit au repos : de temps en temps, la matière d'une ou deux dalles bouge à peine, selon la manière d… | FAIT, EN ATTENTE DE TOM | v127 |
| C-029 | « Le creux sous le doigt passe lui aussi à la carte graphique. Cible au banc : image p95 ≤ 22 ms. Validation d… | FAIT, EN ATTENTE DE TOM | v126 |
| C-030 | « La série de juges, allégée : les juges des chantiers touchés, plus six sentinelles. La série complète un lot… | FAIT, EN ATTENTE DE TOM | v126 |
| C-031 | La vie au repos des huit mondes qui n'ont pas encore leur manière : Volubilis, Guingois, Mascaret, Ramage (rie… | EN COURS | v128+ |
| C-032 | « Les quatre mondes neufs sont-ils gratuits ou [de Ma Parole !] ? » — à valider. | OUVERT | à fixer |
| C-033 | « Le gel de Madrure à la plantation » ; Madrure à surveiller sur un vrai iPhone. | OUVERT | à fixer |
| C-034 | « L'écran qui vend et les six mondes payants » — à trancher. | OUVERT | à fixer |
| C-035 | « Mots de l'achat sans compte » — à valider (payer sans compte, l'achat sera perdu : deux moments). | OUVERT | à fixer |
| C-036 | « Les compteurs — à faire après les cinq mondes. » | OUVERT | à fixer |
| C-037 | « À faire : la palette noir et blanc au Studio. » | OUVERT | à fixer |
| C-038 | « Les textes de l'aide de l'Aura — mots à valider. » | OUVERT | à fixer |
| C-039 | « La phrase du mur : "trop rapide" contre "1,3 s validé" » — choix fait, à confirmer. | OUVERT | à fixer |
| C-040 | « L'inventaire de joignabilité : la dette. » | OUVERT | à fixer |
| C-041 | Questions anciennes dont l'état est à relire avec Tom : Q284 (les trois libellés du partage), Q289 (la Pelote … | OUVERT | à fixer |
| C-042 | « PLANCHE SEULE pour l'outil de dessin. Ne construis rien dans l'app. Tom choisit sur cette planche, et un lot… | PLANCHE EN ATTENTE DU CHOIX DE TOM | lot suivant (après le choix) |
| C-043 | « onboarding mets tout le texte en gilbert ce sera plus beau, et espace les phrases, de moins que entre la pre… | FAIT, EN ATTENTE DE TOM | v127 |
