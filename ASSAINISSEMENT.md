# ASSAINISSEMENT — le prototype rangé, à comportement strictement identique (v206, 17 nov. 2026)

Le prototype `app.html` est la référence de la vraie app. On le range **sans rien changer à ce qu'il fait** : chaque lot est court, réversible, et
prouvé identique à la référence `reference-v205` (§0 : `Promi-reference-v205/`). **Un seul écart, et on revient à l'étiquette.**
Le rangement suit les six couches d'ARCHITECTURE.md (données · logique · moteur · animation · design system · écrans).

## a) La dette, du plus sûr au plus délicat

| Rang | Dette | Exemples mesurés | Risque | Méthode |
|---|---|---|---|---|
| 1 | **Le code mort (JavaScript)** | `openCell` (la carte de la Toile, plus appelée depuis C-189), `_dalleReelle` (dans `sharePlanche`, mort depuis v132), les fonctions dont le nom n'apparaît que dans leur propre corps | Très faible | Un nom sans aucune référence ailleurs, ni dans l'app, ni dans le moteur, ni dans un juge |
| 2 | **Les doublons évidents** | Deux déclarations du même nom dans un même bloc (la seconde gagne : la première est morte) ; les drapeaux posés sur `window` sans lecteur | Faible | Le même critère, nom par nom, lu à la main |
| 3 | **Les pointeurs de diagnostic orphelins** | 50 `window._…` jamais lus (pointeurs de juges disparus : `_v187Bande`, `_cm5T`, `_ppHzEtat`…) | Faible, mais ils servent à la console | À trier avec Tom : les garder (une ligne chacun) ou les retirer |
| 4 | **Le CSS mort** (≈ 54 % des règles, mesuré en août ; 9 805 `!important`) | Des règles battues par une règle postérieure, des écrans disparus | **Interdit par CLAUDE.md §9** (« cinq tentatives, cinq échecs ») | **À décider par Tom** : la preuve d'identité au pixel (ci-dessous) rend la chose possible, règle par règle, écran par écran |
| 5 | **Les correctifs empilés** (288 blocs `lot-…`) | `lot-V200-DOUCEUR` → `lot-V203-RETOUR` → `lot-V203-CONTINU` sur la même phrase ; `lot-V184A-FICHE` qui annule `lot-V181A-CERCLE` | Moyen | Fondre un lot dans la fonction qu'il enveloppe, un écran à la fois |
| 6 | **Les états à plusieurs propriétaires** | La hauteur d'une fiche de Cercle (deux observateurs), la phrase de la page + (trois écrivains), `createKind` | Moyen | Nommer UN propriétaire par état ; les autres lisent |
| 7 | **Les minuteries dispersées** (498 `setTimeout`, 50 `setInterval`, 87 observateurs) | Composer par minuteurs (le flash de v103) | Délicat | Un ordonnanceur unique (ARCHITECTURE b-4), écran par écran |
| 8 | **Les noms incohérents** | `nuee` / `NUE` / `curNuee` pour un Cercle ; `ouvreCercle`, `.s2-cercle`, `isPremium` pour Ma Parole ! | Délicat (juges et CSS les nomment) | Une table de correspondance ; renommer avec les juges dans le même lot |
| 9 | **Le découpage d'`app.html` en modules** | 209 `<script>`, 173 `<style>` dans un fichier de 46 524 lignes | Délicat : plusieurs juges lisent la SOURCE d'`app.html` (volume, jetons, clavier, kaki, découpe) | En dernier : les fichiers chargés dans le même ordre, les juges statiques repointés |

## b) La preuve d'identité, exigée pour CHAQUE lot

Contre la référence du §0, dans cet ordre, et rien n'est commité si une ligne rougit :
1. **Une étiquette avant le lot** : `assain-N-avant`.
2. **La syntaxe** : chaque `<script>` passe `node --check`, la page se charge sans aucune erreur (`pageerror`).
3. **`banc_rendu`** : les 280 images au pixel (Ramage excepté : rouge sur la référence elle-même, C-187).
4. **`redteam_aspect`** (A à D) : chaque phrase au repos et pendant son détracé, contre la référence.
5. **La planche de captures** : `scratchpad/v206/captures_ref.py`, les 19 écrans × 2 thèmes × 2 échelles, comparés au pixel à `Promi-reference-v205/captures/`
   (même hasard, même Toile) — une différence se regarde avant d'être crue (le §8 : l'instrument d'abord).
6. **L'état exporté de Tom rejoué** (`banc_tom.contexte_tom`) : `redteam_etat_fiche`, `redteam_haut_fiche` (sentinelle C-255).
7. **Les juges du périmètre et les 5 sentinelles** (C-227), par `serie_juges.py` : aucun rouge nouveau face à la référence passée dans les mêmes conditions.
8. **Les mesures de temps non dégradées** : `redteam_fluide` et `redteam_trace_present`, au calme seulement (charge < 4), sinon « non jugé ».

## c) Le premier lot — le code mort et les doublons évidents

**Étiquette avant le lot : `assain-1-avant`.** **42 lignes retirées** d'`app.html` (46 549 → 46 507 ; 44 supprimées, 2 notes posées à leur place) :
- **la carte de la Toile `#cellCard`** (27 lignes) : `openCell` (plus aucun appel depuis C-189), `closeCard`, `ccId` et les gestionnaires de `#ccKeep`, `#ccPush`,
  `#ccPushOpts button`, `#ccManage`. La carte ne pouvait plus s'afficher (seule `openCell` lui posait `.show`) ; son HTML et son CSS restent (§9) ;
- **`_dalleReelle` et son cache par id** (17 lignes, dans `sharePlanche`) : jamais appelée depuis v132 (la case du Folio passe par `_poseDalle`).

**Comment ils ont été trouvés** : un index de tous les mots d'`app.html`, du moteur, des variantes, des juges et des bancs ; une fonction est morte si son nom
n'apparaît nulle part hors de son propre corps. Quatre faux positifs écartés à la lecture : des fonctions nommées qui s'appellent elles-mêmes (`attendSorti`,
`rend2`, `nomStudio`, `hook`). **Il n'y a presque plus de JavaScript mort franc** : le reste de la dette est dans les rangs 3 à 9.

**La preuve d'identité** (contre `reference-v205`) :

| Point | Résultat |
|---|---|
| Syntaxe, chargement | `node --check` de chaque `<script>` : OK ; aucune erreur de page |
| `banc_rendu` | 266/280 au pixel ; les 14 autres sont toutes de Ramage, rouge sur la référence elle-même (C-187) : identique |
| La planche (`compare_planche.py`) | les 56 captures hors Studio dans le bruit de la référence ; le Studio n'est pas jugeable au pixel (ses aperçus s'animent : la référence contre elle-même varie de 0 à 57 %) |
| `redteam_ecrans`, `redteam_decisions`, `redteam_partage_fiche` | 152/152 · 102/102 · vert |
| `redteam_haut_fiche` (C-255, trois natures) · état de Tom (`redteam_etat_fiche`) · `redteam_couleurs_ref` (8 tranches) | 20/20 ×3 · 11/11 · 0 écart |
| `redteam_aspect` | 48/49 : « Promi planté ! », pas 2, B à 0,65 % — **préexistant, et c'est l'instrument** : v205 servie sous le nom `app.html` donne le même 0,65 % ; le même contenu servi sous un autre nom passe (le serveur réécrit `app.html` en le servant, la référence `zz-v205.html` ne l'est pas) |
| `redteam_joignable` | 4/5 : « LA COULEUR » (mur du Peaufiner d'un Cercle) relevé sans son code couleur — **préexistant** : v205 servie depuis l'archive donne le même 4/5 |
| `redteam_trace_present` | 118/121 : trois cadences d'images pendant les tracés, déjà ouvertes sur la référence (REPRISE b-2) ; aucune présence en défaut |

## d) v207 — l'assainissement recentré sur les modules repris (décision du 17 nov. : Capacitor ; l'app sera reconstruite autour)

L'assainissement ne porte plus que sur ce qui passera dans la vraie app : **le tracé** (`trace-lettres.js`, PromiLate compris), **les flaques**, **les jetons**,
**l'interface d'appel du moteur** (le moteur reste en lecture seule). Le CSS du prototype n'est pas touché (CLAUDE.md §9).

| Module | Ce qui est fait (v207) | Preuve |
|---|---|---|
| `trace-lettres.js` | L'ouvrier refait autour d'une **file tenue par la page** : la lettre qu'un tracé attend passe devant les préparations ; une carte déjà demandée est attendue, jamais recalculée (23 % des cartes l'étaient deux fois) ; trois ouvriers prouvés chacun par l'essai de C-206 ; la médiane 3 × 3 par un réseau de 19 comparaisons (la même valeur ; elle prenait le tiers du temps de la carte) ; le cache évince la plus ancienne carte au lieu de se vider au-delà de 600 ; le relevé dit l'attente d'une lettre et le calcul d'une carte (`R.tl.att`, `R.tl.calc`). 1 287 → 1 356 lignes. | les 114 cartes réelles identiques **bit pour bit** à l'ancien module (WebKit, Chromium) ; `banc_rendu` (seul Ramage, comme la référence) ; `redteam_aspect` 48/49 (le rouge préexistant de l'instrument) ; `trace_present` 25/25 en ouvrier lent ; `premiere` 48/48, `premiere_froid` 30/30, `un_trace` 5/5, `onb_exemple` 11/11, `onb_toucher` 16/16, `ecrans` 152/152, `decisions` 102/102 |
| `flaques.js` | Relu : aucune fonction morte, aucune propriété orpheline. Rien à retirer. | — |
| Les jetons | **Dette trouvée** : `Promi+Design.swift` a été retouché à la main après sa génération (v134–v135 : `cobalt50`, deux commentaires) — le régénérer depuis le JSON les perd ; aucun outil n'engendre le bloc `lot-TOKENS-css` depuis le JSON (`scratchpad/regen_tokens.py` va dans l'autre sens, un rattrapage d'août) ; les deux générateurs vivent dans `scratchpad/` (interdit, v198). `redteam_tokens` 41/43 (23 couleurs et 4 polices en dur, antérieures). | à faire : **un seul générateur à la racine** (JSON → bloc CSS, Swift, TypeScript), prouvé octet pour octet contre l'existant, avant la reconstruction |
| L'interface du moteur | Relevée : l'app appelle 53 méthodes de `Toile` et 15 globales `Toile_*` (les plus employées : `dalleAbs` 46, `dalleTrame` 42, `sync` 40, `cols` 26, `mondeCourant` 23). | à faire : la porte unique du moteur (ARCHITECTURE b-3) se bâtit dans la vraie app, depuis cette liste |

**Ce qui n'est pas fait** : préparer d'avance les lettres du retour de l'exemple (le reste de C-282). Essayé sur une copie exacte de l'exemple : la préparation
a lieu 2,5 s avant le retour, mais ses clés de carte ne sont pas celles du retour (le retour ne trouve rien en cache ; une préparation faite après lui trouve
tout) — la géométrie de l'exemple au retour diffère de celle de sa première apparition, d'une façon non nommée. Retiré. Avec la file, le retour attend 420 ms
au lieu de 883 (ouvrier imité de l'iPhone), et aucune lettre n'est plus « lente ».
