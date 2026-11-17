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
