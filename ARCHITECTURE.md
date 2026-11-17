# ARCHITECTURE — Promi construit de zéro, proprement (étude « copie blanche », v206, 17 nov. 2026)

Aucune ligne de code ici. Ce document propose une façon de construire la vraie app (iOS et Android) pour qu'une seule personne, aidée d'agents IA,
puisse la faire vivre pendant des années. **Rien ne démarre avant l'accord de Tom.** Le prototype `app.html` est figé comme référence
(étiquette `reference-v205`, dossier `Promi-reference-v205`).

## a) L'audit du prototype

### Ce qui est solide, et se garde

| Pièce | Pourquoi elle vaut de l'or |
|---|---|
| **Le moteur de la Toile** (`promi-moteur.js`, 8 373 lignes, 20 mondes) | Validé monde par monde par Tom. Déterministe : `banc_rendu` le juge au pixel sur 280 images (20 mondes × clair, sombre, sans titres, plus des dalles à trois tailles). Il est déjà presque un module : une porte d'entrée (`Toile.*`), des déclarations lues par l'app (`__dalleInfo`, `dalleAvenir`). |
| **Le tracé des lettres** (`variantes/trace-lettres.js` et ses trois tables de chemins) | Le langage d'animation de l'app (C-125, C-279) : un seul module, une seule cadence (40 car/s), le détracé, le repli sans ouvrier (C-206). |
| **Les flaques** (`variantes/flaques.js`) | La matière de toutes les transitions (C-130, C-271). |
| **Les jetons de design** (`PROMI-TOKENS.json`, 460 lignes) | Une seule source, déjà engendrée vers le CSS et vers Swift (`Promi+Design.swift`). Les couleurs de Tom sont exactes (C-204). |
| **Les juges** (267 `redteam_*.py`, 12 relevés et bancs) | Ce sont des **spécifications de comportement exécutables** : chacun écrit en dur une décision de Tom (une cote, une durée, une couleur, un ordre) et rougit sur la version fautive. `SPEC-JUGES.md` en donne la liste. |
| **Le dossier `portage/`** (10 documents, 5 300 lignes, un schéma JSON de 27 définitions) | Les données, les écrans, le geste, le rendu, les textes mot pour mot, les règles. Écrit pour Swift, mais presque entièrement indépendant de la technologie. |
| **Les textes** (`portage/TEXTES.json`) et **la grille anti-coercition** (CLAUDE.md §12) | Le ton et les interdits du produit, prêts à porter. |

### La dette, avec des exemples précis

1. **Un seul fichier de 46 524 lignes**, fait de **288 blocs `lot-…`** posés les uns sur les autres : 209 `<script>` et 173 `<style>`. Un correctif de v205
   enveloppe une fonction de v203, qui enveloppait celle de v186. Pour comprendre une fiche, il faut lire dix lots dans l'ordre.
2. **9 805 `!important`, et environ 54 % de règles CSS mortes** (mesuré en août) : une règle tardive en bat une autre, une troisième la rebat. CLAUDE.md
   §8 en garde dix pièges (`#createSheet>*`, `:not(#id)` qui pèse un id, un `!important` battu par une animation dans WebKit…).
3. **Des états à plusieurs propriétaires.** La phrase de la page + a eu trois écrivains (la frappe, le curseur, la composition — C-274) ; la hauteur
   d'une fiche de Cercle, deux observateurs qui se répondaient sans fin (la page figée, v203) ; la nature de la page +, deux variables `createKind`
   (C-224) ; « Peaufiner ouvert » vivait à deux endroits (C-228). **779 propriétés `window._…`** servent de messagerie entre les lots.
4. **Des minuteries dispersées** : 498 `setTimeout`, 50 `setInterval`, 244 `requestAnimationFrame`, 87 `MutationObserver`. Une composition qui se
   fait « par minuteurs » se montre avant d'être finie (le flash de v103, `redteam_flash`).
5. **L'état lu dans le DOM** : un écran est « ouvert » parce qu'il porte `.show` — et le Studio et l'Aura ne la perdent jamais (§8, trois défauts).
6. **Des mesures en deux unités** : `clientWidth` (mise en page) comparé à `getBoundingClientRect` (écran) — la ligne d'état d'une fiche à 11 pt de sa
   place sur l'iPhone de Tom (C-207, Q592).
7. **Des doublons** : plusieurs chemins pour la même chose (un ancien carrousel qui écoutait encore le doigt et changeait la nature — 13 sept., §8 ; l'ancien
   chemin « garder de côté » qui ne gardait que le titre — C-149), le code des écrans abandonnés resté en place.
8. **Le fil principal surchargé sur l'iPhone** (relevé du 15 nov.) : l'ouvrier du tracé est prouvé, mais lent (600 à 924 ms par lettre en file) ; une
   lettre calculée sur le fil coûte ≈ 100 ms (11 au banc).

**Ce qu'il faut retenir** : le **comportement** du prototype est juste et prouvé ; c'est sa **forme** qui ne peut plus porter des années de mises à jour.

## b) L'architecture cible, en six couches

Chaque couche ne parle qu'à celle du dessous. Une information n'a **qu'un propriétaire**.

1. **Les données et l'état unique.** Un seul magasin : les paroles, les Cercles, les personnes, les réglages, les achats. Il est décrit par le schéma
   de `portage/SPEC-DONNEES.schema.json`, versionné (champ `schema`), sauvegardé en une écriture atomique au moment du geste (la leçon de C-226 :
   une parole plantée est écrite AVANT toute animation). Toute modification passe par une **action nommée** (`planter`, `tenir`, `renommer`…) ; aucun
   écran n'écrit directement. Les écrans **s'abonnent** à ce qu'ils montrent (le principe de `_paroles` de v130, généralisé).
2. **La logique métier**, sans écran : les natures (Promi, Chiche, Cercle), les deux états (en cours, tenu — C-210), les parts à plusieurs (`p.parts`),
   l'échéance comme date (C-160), les membres d'un Cercle, et demain Délier (C-082). Ce sont des fonctions pures, testées seules, en millisecondes.
3. **Le moteur de la Toile**, inchangé, derrière une porte unique : on lui donne les paroles et le monde, il rend une Toile, une dalle, une Pelote. Il
   ne lit jamais le reste de l'app.
4. **Un seul système d'animation** : un **ordonnanceur** qui possède l'horloge, les images et les transitions. Il porte les trois verbes de l'app :
   *tracer / détracer* (le module de C-125), *flaques* (naître, couvrir, se retirer), *glisser* (une boîte va de sa place vue à sa nouvelle place, C-278).
   Il sait à tout instant ce qui s'anime (la règle v201 ② : aucun travail lourd pendant une animation de texte) et répartit le travail de fond dans les
   temps morts. **Aucun écran n'appelle `setTimeout` pour composer.**
5. **Le design system** : les jetons (couleurs exactes, cinq faces de police, l'échelle typographique, les rayons, l'air), engendrés depuis
   `PROMI-TOKENS.json`, et une vingtaine de **composants** (le plateau, la barre, le trait et sa flèche, la pastille, la carte, l'encart « Un mot… »,
   le mur de Ma Parole !…). Un composant porte sa géométrie ; un écran ne pose jamais une cote.
6. **Les écrans**, minces : ils assemblent des composants, lisent l'état, déclenchent des actions. L'accueil, la page +, la fiche, Peaufiner, l'Index,
   le Fil, l'Aura, le Studio, Partager, les Réglages, l'onboarding et le guide.

### Les règles qui empêchent de recréer la dette

- **Un propriétaire par information** : chaque donnée et chaque propriété visible ont un module propriétaire, écrit dans une table. Deux écrivains = refus en revue.
- **Aucun correctif empilé** : on corrige la fonction elle-même, jamais en l'enveloppant d'un lot.
- **Aucune cote dans un écran** : elles vivent dans les jetons ou dans le composant.
- **Aucune minuterie de composition** : l'ordonnanceur seul gère le temps.
- **L'état ne se lit jamais dans l'affichage** (une classe CSS, une hauteur rendue) : on le demande à son propriétaire (C-172).
- **Chaque décision de Tom devient un test**, nommé par son chantier (C-xxx), qui rougit sur la version fautive (la règle des juges, gardée).
- **Chaque module a une taille plafond** (≈ 400 lignes) : au-delà, il se découpe.

## c) iOS et Android en même temps : cinq voies comparées

| | Fidélité Toile et tracé (60 i/s) | Vibrations, notifications, achats | Firebase | Une personne + agents | Vitesse des mises à jour | Juges → tests | Réutilisable de `portage/` |
|---|---|---|---|---|---|---|---|
| **Deux apps natives** (Swift + Kotlin) | Moteur réécrit **deux fois** (CoreGraphics, Skia) : jamais identique au pixel | Excellent (Core Haptics, StoreKit 2, Play Billing) | Excellent | **Lourd** : deux langages, deux apps à tenir | Lente (deux revues, deux codes) | À réécrire deux fois | Tout le texte ; rien du code |
| **Flutter** (Dart) | Moteur réécrit **une fois** en Dart ; très fluide (Impeller) ; proche mais pas identique au pixel | Bon (paquets officiels ; motifs Core Haptics par un petit pont) | Bon (FlutterFire) | Bon : un langage | Bonne | Tests « golden » au pixel : bon terrain | Tout le texte ; le moteur à porter |
| **Kotlin Multiplatform** (+ Compose) | Logique partagée ; l'interface iOS encore jeune ; moteur à réécrire | Bon | Bon | Moyen : outillage iOS moins mûr | Bonne | Moyens | Tout le texte |
| **React Native** | Le moteur Canvas 2D ne tourne pas tel quel (il faudrait Skia) | Bon | Bon | Bon | Bonne (mises à jour à distance possibles) | Partiels | Une partie du JavaScript |
| **Le moteur JavaScript gardé, dans une vue web** (une coquille native mince : Capacitor) | **Identique par construction sur iOS** : la vue web d'iOS est le moteur de Safari, celui sur lequel Tom a validé chaque écran | Bon par greffons (Haptics, notifications locales, achats StoreKit 2 / Play Billing) ; un petit greffon Swift pour les motifs Core Haptics | Bon (SDK web, ou greffons natifs pour la connexion Apple) | **Le meilleur** : un seul langage (TypeScript), celui que les agents connaissent le mieux | La plus rapide (une seule base ; correctifs JavaScript possibles à distance, dans les limites d'Apple) | **Presque directs** : les juges tournent déjà dans WebKit | Le moteur, le tracé, les flaques, les jetons, les juges, les textes |

**Les risques de la vue web, mesurés plutôt que supposés** : la fluidité sur iPhone (le relevé montre des images longues pendant les tracés : il faut
l'ordonnanceur et l'ouvrier bien employés, pas une autre technologie) ; Android rend avec Chromium (un moteur différent : il faut un banc Chromium au
pixel, en plus de WebKit) ; le clavier et le défilement natif (déjà maîtrisés : `visualViewport`, Q598) ; la revue d'Apple (acceptée quand l'app apporte
des fonctions natives : notifications, achats, vibrations).

### La recommandation : le moteur gardé, l'app reconstruite autour, en TypeScript, dans une coquille Capacitor

1. **La fidélité est le cœur du produit**, et c'est la seule voie où la Toile, le tracé et les flaques sont **ceux que Tom a validés**, au pixel, sans
   rien réécrire. Réécrire 20 mondes en Swift, en Kotlin ou en Dart, c'est des mois, et des écarts visibles à rattraper un par un.
2. **Une seule personne et des agents** : une base, un langage, des tests qui existent déjà. C'est le critère qui décide sur des années.
3. **On n'hérite pas de la dette** : seuls le moteur, le tracé, les flaques et les jetons passent tels quels. Les écrans sont **réécrits** dans les six
   couches, avec les juges comme cahier des charges.
4. **Ce qui n'est pas pris** : la sensation 100 % native de SwiftUI. Si un jour un écran l'exige, il peut devenir natif seul (la coquille le permet).
5. **Ce que ça change à ce qui était prévu** : `portage/` visait Swift. Ses documents restent la spécification ; `Promi+Design.swift` sert si un écran
   devient natif. **C'est une décision de Tom** (question 1).

## d) Le plan de migration

Le prototype figé (`reference-v205`) reste la référence : **chaque écran neuf est jugé contre lui**, avec les mêmes juges, au pixel quand c'est possible.

| Étape | Contenu | Ce qui se porte tel quel | Estimation |
|---|---|---|---|
| 0 | Le squelette : TypeScript, la coquille iOS et Android, l'intégration continue, les juges branchés sur la nouvelle app | les juges, `banc_rendu` | 2 lots |
| 1 | Le magasin de données et la logique métier (paroles, natures, états, parts, échéance), leurs tests | le schéma JSON, `_migreEtats` (lecture de l'état de Tom) | 2 lots |
| 2 | Le moteur derrière sa porte, l'ordonnanceur d'animation, le tracé, les flaques | moteur, `trace-lettres`, `flaques` | 2 lots |
| 3 | Le design system : jetons, polices, les vingt composants | `PROMI-TOKENS.json` | 2 lots |
| 4 | Les écrans, un par lot, du plus simple au plus délicat : Réglages, Index, Fil, Aura, Studio, Partager, fiche, Peaufiner, page +, onboarding et guide | les textes, les juges de l'écran | 11 lots |
| 5 | Le natif : vibrations, notifications locales, achats (StoreKit 2, Play Billing), Firebase (comptes, Cercles partagés, parts à plusieurs) | les règles §12, `redteam_notifs` | 4 lots |
| 6 | La recette : l'état de Tom rejoué, ses testeurs, TestFlight et le test interne Google Play | — | 2 lots |

**Environ 25 lots.** L'ordre protège Tom : rien de visible ne change avant l'étape 4, et chaque écran porté est comparé à la référence avant d'être livré.

## e) Les mises à jour pour la suite

- **Versions** : numéro sémantique (1.4.2) ; chaque version porte son commit (comme `?diag=1` aujourd'hui).
- **Schéma de données versionné** : chaque changement de forme a sa migration, testée sur l'état réel de Tom (`etats/`). Aucune perte de parole.
- **Fonctions activables à distance** (Firebase Remote Config) : une fonction neuve part éteinte, s'allume pour Tom, puis pour ses testeurs, puis pour tous.
- **Tests automatiques** : la logique (rapide, à chaque modification), les juges d'écran en WebKit et en Chromium, `banc_rendu` au pixel.
- **Intégration continue** (GitHub Actions) : rien ne fusionne si un test rougit ; la porte A1–A6 devient automatique.
- **Distribution** : TestFlight (iOS) et le test interne de Google Play (Android) à chaque version ; Tom valide sur son iPhone avant la publication.

## f) Les questions pour Tom (5)

1. **La voie technique** : le moteur JavaScript gardé dans une coquille native (Capacitor), plutôt que Swift (prévu jusqu'ici) puis Kotlin ?
   *Recommandé : oui* — la fidélité au pixel de ce que tu as validé, et une seule base à tenir.
2. **Android en même temps qu'iOS, ou juste après ?** *Recommandé : la même base dès le départ, publiée sur Android un ou deux lots après iOS* (le
   rendu Chromium se vérifie à part).
3. **Les comptes et les Cercles partagés (Firebase) dès la première version publique, ou une version 1 seule sur l'appareil ?**
   *Recommandé : une version 1 sur l'appareil, Firebase en version 1.1* — le cœur (planter, tenir, la Toile) sort plus tôt.
4. **Les correctifs à distance du JavaScript (sans passer par la revue d'Apple)** : on s'en sert ?
   *Recommandé : seulement pour corriger un défaut, jamais pour une fonction neuve* (c'est la limite d'Apple).
5. **L'assainissement du prototype (ASSAINISSEMENT.md) continue-t-il pendant la construction ?**
   *Recommandé : non, au-delà des lots sûrs* — le prototype est la référence ; chaque heure va à la vraie app.
