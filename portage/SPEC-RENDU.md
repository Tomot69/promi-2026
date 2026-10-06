# SPEC-RENDU — la Toile, les mondes, la Pelote : ce que le prototype rend, et comment

> **Pour qui :** celui qui reconstruit Promi en Swift sans relire `app.html`.
> **D'où viennent les valeurs :** du code (cité `fichier:ligne`) ou d'une décision écrite (document et bloc cités).
> Numéros de ligne : copie de travail du **6 oct. 2026** (`promi-moteur.js` 8 034 lignes ; `app.html` 38 340 lignes, lot v134
> en cours, non commité). **Ce qui manque est écrit « ⚠ TROU ».** Aucun seuil, aucune durée, aucun chiffre n'est inventé.
> **À lire avec :** `CONTRAT-MONDE.md` (le contrat d'un monde — ce document y RENVOIE, il ne le recopie pas),
> `ETAT-30-SEPTEMBRE-2026.md` §4 (la table vivante des mondes), `SPEC-JUGES.md` §1 (le rythme), `portage/SPEC-GESTE.md`.

---

> ## ⛔ L'INTERDICTION — JAMAIS DE CAPTURE DE TOILE À LA PLACE D'UNE DALLE
>
> **Une dalle seule est ENGENDRÉE par le peintre de son monde, à sa taille finale, et posée 1 : 1.**
> **Jamais découpée dans la Toile. Jamais redimensionnée. Jamais photographiée. Jamais un polygone reconstruit.**
>
> *« Une dalle est peinte par le moteur, dans sa cellule, avec son propre contour, à sa taille finale. Jamais une image
> rognée, jamais un canevas recadré, jamais un morceau de Toile. »* (Tom, 22 sept. 2026 — `CONTRAT-MONDE.md` §9.)
> *« Interdit, définitivement, dans le prototype comme dans Swift. »* (Tom, 5 oct. 2026, C-048 — CLAUDE.md §3 bloc v130.)
>
> - **Partout où une dalle paraît seule** — bande d'une fiche, carte de l'Index et du Fil, fil d'un Cercle, liste de
>   l'Aura, partage, les deux dalles de l'instant — le peintre du monde reçoit **la dalle à peindre et n'engendre qu'elle** :
>   ses carreaux, ses points, ses traits, ses sillons, et eux seuls. **Rogner un rendu plus large est une découpe, même à
>   l'intérieur du moteur.** (CLAUDE.md §3 bloc v130 ; `portage/A-INTEGRER.md`, C-048.)
> - **À sa taille finale** : la même dalle à 40 px et à 200 px est la même image ; toute longueur d'un monde s'écrit
>   « valeur de référence × `UK` » (v29 — CLAUDE.md §4 règle 2 ; `CONTRAT-MONDE.md` §5).
> - **En Swift** : une fonction `dalle(id, taille)` par monde, qui ne reçoit que la graine de cette dalle et ses voisines
>   (pour la forme) ; **aucune `UIImage` / `CGImage` recadrée** (`portage/A-INTEGRER.md`, C-048).
> - **Les familles de la faute**, telles que le juge `redteam_decoupe.py` les nomme (`redteam_decoupe.py:20-33`, `347-359`) :
>   **A** découpe (une dalle recopiée par morceau) · **B** redimension (taille rendue ≠ taille peinte, à plus d'un pixel) ·
>   **C** pixels relus ou reposés · **D** fragment de Toile découpé ou redimensionné · **E** motif ou image tirée d'une dalle ·
>   **F** photo de dalle posée à la place du moteur · **G** canevas de dalle AFFICHÉ à une autre taille que celle où il est
>   peint (à 3 % près) · **G2** (v130) une dalle rendue seule ne porte pas plus de **0,3 %** de pixels d'une autre couleur
>   que la sienne (l'anticrénelage) · **H** une dalle peinte dans un autre monde que celui qu'elle doit porter, sans le déclarer.
> - **Pourquoi c'est revenu deux fois** : depuis v29, cinq mondes à trame peignaient la Toile AUTOUR de la dalle puis
>   rognaient au pixel sur la cellule — bords en marches, éclats des voisines (1,2 à 3,5 % de pixels étrangers). Le juge ne
>   piégeait que les écrans, pas ce que le moteur faisait en lui-même.
> - **Ce qui n'est PAS une découpe** : la Toile entière gardée 1 : 1 sur elle-même pour le retour exact de la vie au repos
>   (§d) ; un calque peint par le monde, à sa taille, posé 1 : 1 (`CONTRAT-MONDE.md` §8.4) ; la Pelote, qui reçoit DU MOTEUR
>   les pixels d'une dalle pour tisser sa fourrure (`opts.donnees`, `CONTRAT-MONDE.md` §5.2 bis).

---

## (a) LA TOILE

### a.1 · Voronoï pondéré — la seule règle de partage

Un point `(x, y)` appartient à la graine `k` qui minimise **`distance(point, graine k) − poids k`**
(`cAt`, `promi-moteur.js:6364` ; `CONTRAT-MONDE.md` §3). La position lue est la position PEINTE (`px, py`, frémissement
compris) quand elle existe, sinon la position de repos. La frontière est **courbe** dès que les poids diffèrent.
**Le toucher, les titres, la dalle d'une fiche lisent la même règle** (`Toile.hit`, `promi-moteur.js:6765`).

Pour ne pas parcourir toutes les graines à chaque point : un index spatial (`_grilleProp`, grille de pas `avg()`), exact
(0 graine différente sur 300 000 points — `CONTRAT-MONDE.md` §8.3).

### a.2 · Les poids

| | Poids | Source |
|---|---|---|
| Une parole (Promi, Chiche) | **3,4** | `promi-moteur.js:6716`, `6737`, `6863` |
| Un Cercle | **14** | `promi-moteur.js:6716`, `6753` |
| Une parole qui arrive (hors mondes `douce` / `sansPoussee`) | naît à **−22**, vise **12**, retombe à 3,4 après **380 ms** | `promi-moteur.js:6959`, `6716` |
| L'ampleur, dans les douze mondes dont le semis grandit | `base + d × avg()`, `d = −0,09 + 0,31·u²` (de −0,09 à +0,22), `u` tiré du **titre et de la personne** (FNV-1a), jamais de l'id ni du hasard | `promi-moteur.js:6745-6753` |

`avg()` = `√(W·H / n)`, l'écart moyen entre graines. Les huit anciens mondes gardent des poids égaux (v45).

### a.3 · Les deux familles de semis (`promi-moteur.js:6729-6762` ; CLAUDE.md §3 blocs v34, v35, v98)

| Famille | Mondes | Ce qu'est la Toile |
|---|---|---|
| **Semis CONSTANT** | les huit anciens : Pochade, Touffe, Tesselle, Braille, Buvard, Éclisse, Taille-douce, Houle | **≈ 68 cellules** ; les paroles COLORENT des cellules du semis ; la vue cadre les colorées. **Tant qu'il reste une cellule vide, le semis ne change pas ; plein, on ajoute UNE cellule** (`_celluleEnPlus`, au plus grand vide, déjà posée au poids 3,4). Leur aspect ne change qu'au-delà d'environ 50 paroles. |
| **Semis QUI GRANDIT** | les douze de `_NEUFS` : Esquille, Bobinette, Ritournelle, Madrure, Halin, Brouillamini, Chamade, Volubilis, Guingois, Chantourné, Mascaret, Ramage | la Toile est **faite de ses seules paroles et de ses Cercles**, vue entière ; une graine neuve se pose **au plus grand vide** (`_auVide`). Seule la Toile SANS parole garde un semis de graines. |

- **`_auVide(i)`** : 24 candidats tirés d'un générateur amorcé par **la clé de la Toile et le rang** `i`
  (`((clé XOR (i+1)·2654435761)`, LCG `×1103515245 + 12345`), dans `[0,1 ; 0,9]` de la largeur et de la hauteur ; on garde le
  plus loin de toutes les graines.
- **La clé de la Toile** (`Toile.cle()`, `promi-moteur.js:7916-7930`) : FNV-1a de `'toile|' + graine sauvegardée de
  l'utilisateur` — stable depuis la première ouverture, ne bouge pas quand on plante.
- **Une parole n'est jamais perdue** : « une parole qui n'apparaît pas est inacceptable » (Tom, v98).
- **Changer de famille au Studio ressème la Toile** ; c'est une incohérence ASSUMÉE (CLAUDE.md §3 bloc v35).
- L'unité de MATIÈRE d'un monde est fixe : `env.uMat = √(W·H / 68) × UK` — elle ne change pas avec le nombre de paroles
  (`promi-moteur.js:6477` ; `CONTRAT-MONDE.md` §15.6).

> ⚠ **Divergence de vocabulaire.** CLAUDE.md (blocs v34–v35) parle des « quatre mondes neufs » ; depuis, huit autres ont rejoint
> la famille. La table `_NEUFS` du moteur et `ETAT-30-SEPTEMBRE-2026.md` §4 en comptent **douze** : c'est ce qui vaut.

### a.4 · Le relâchement (`relax`, `promi-moteur.js:6189`)

Chaque graine est repoussée par chaque voisine trop proche : seuil `w = avg() × (0,92 + 0,026·poids_a + 0,026·poids_b)` ;
si la distance `d < w`, poussée `(w − d)/d × 0,16` le long de l'axe. La cible est bornée (`_bornes`,
`promi-moteur.js:6188`) : **6 du bord** pour les huit anciens ; pour les douze neufs, le CENTRE d'une dalle reste dans la zone
utile — **13 % de la largeur** sur les côtés, **17 % de la hauteur** en haut, **15 %** en bas (les cellules vont toujours
jusqu'au bord). Deux mondes relâchent LOCALEMENT pendant une transition (`relaxLocal` : Esquille, Bobinette — rayon
`1,5 × avg()`, fenêtre = la transition + 4 000 ms). Dans un monde `douce` (Halin), une dalle qui part ne pousse personne.

### a.5 · Le mouvement d'une parole qui arrive ou qui part — l'horloge

- **Tous les mondes suivent l'HORLOGE** (v61) : le ressort se calcule sur le temps — `1 − 0,83^dt` et `1 − 0,78^dt`
  (= 0,17 et 0,22 à 16,67 ms) ; Pochade et Touffe : 0,838 / 0,79 ; les mondes neufs intègrent le temps vrai en sous-pas de
  1/60 s ; un redémarrage de la boucle fait UN pas (`promi-moteur.js:6636`, `6656` ; `REGLAGES_MONDE`, `:5977`).
- **EXCEPTION ÉCRITE — HOULE (`sillons`) RESTE PAR IMAGE**, par décision : à l'horloge elle deviendrait plus rapide que ce
  que Tom a validé ; elle s'étire sous charge (CLAUDE.md §3 bloc v61).
- **Le fondu de couleur** d'une dalle qui arrive ou qui s'éteint : **760 ms** (`cOf`, `promi-moteur.js:6365`).
- **Une dalle qui part** devient une graine `part`, retirée au bout de `PART_DUR` **620 ms** (ou du `partDur` du monde)
  (`promi-moteur.js:6019`, `6622`).
- **Les durées validées, monde par monde** (arrivée, départ, tolérances) : `SPEC-JUGES.md` §1 — c'est la table à porter.
  Le juge : fin du mouvement à ± max(100 ms, 8 %) ; Houle au nombre d'images (± max(3, 20 %)) ; cadence ≥ 60 % de la validée.
- **Le frémissement** de toute la Toile au retour sur l'accueil (`liven`) ne se superpose jamais à une arrivée ou à un
  départ (`promi-moteur.js:6281`).
- **Le vert de célébration sur la Toile est abandonné** (v53) : « la célébration, c'est le mouvement »
  (`promi-moteur.js:6191`).

### a.6 · La vue et le recadrage (`promi-moteur.js:6123-6176`)

Zoom entre **0,72** et **5** ; la Toile se repeint dans sa transformation à chaque image (vectoriel, contours nets).
Vue par défaut : `n < 20` paroles → `min(1,1 ; 1 + (20 − n) × 0,005)`, sinon 1 — **jamais sous 1** : « par défaut la Toile
prend tout l'écran, angles compris, aucun fond autour ». Dans un monde à semis constant et moins de 20 paroles, la vue cadre
la boîte des dalles colorées + une marge de `1,3 × avg()`, zoom entre 1 et 2, zone utile entre **176** (haut) et **H − 138**
(bas), sur 92 % de la largeur ; les bords de la Toile restent collés aux bords de l'écran.
Une vue posée par la main n'est reprise que par le recadrage (le rond, le double toucher) ou par une dalle créée ou
supprimée, en douceur. Gestes et ressorts : SPEC-GESTE §6.2.

### a.7 · Les titres sur la Toile

**Un titre s'efface quand la dalle n'a pas 48 px à l'écran** : `avg() × zoom < 48` → aucun titre ; au-delà, il paraît en
fondu sur 8 px (`min(1, (écran − 48)/8)`) — `promi-moteur.js:6545`, `6565`. On zoome pour lire (CLAUDE.md §3 bloc v98).
Pendant un mouvement de repos, **le titre ne bouge jamais** (§d).

### a.8 · Le fond

| | Valeur | Source |
|---|---|---|
| Clair | **`#DFCAA4`, à plat** (le dégradé `#E6D1AE → #D8C29A` est retiré) | `promi-moteur.js:6039` ; CLAUDE.md §3 bloc v118 |
| Sombre | **encre de seiche `#050302`, à plat** + un grain léger (motif de bruit 160 × 160, alpha 0,05, fusion `overlay`) | `promi-moteur.js:6039`, `6690` ; CLAUDE.md §3 bloc v116 |
| Cellules vides en sombre | OKLCH L 0,136–0,161, h 40–56° ; dalle neutre d'Ingénu en sombre `#1F1611` ; **jamais bleu** | CLAUDE.md §3 bloc v116 ; `promi-moteur.js:6365` (`[31,22,17]`) |

Le coin arrondi de la Toile **ne se découpe pas** (`clip()`) : on peint la matière, puis le fond autour de la forme en
pair-impair — un découpage coûtait 154 ms par image à Touffe sur le moteur de Safari (CLAUDE.md §8 ; `CONTRAT-MONDE.md` §8.4).

### a.9 · La couleur d'une dalle (`cOf`, `promi-moteur.js:6365` ; `CONTRAT-MONDE.md` §4)

- **Un monde ne choisit JAMAIS une couleur** : il la reçoit de `cOf`. Quatre tons par palette (≈ 34 · 28 · 23 · 15 %).
- **Figée** : `p.dalle = {ci, lit}` (l'emplacement dans la palette, la nuance), tirée à la plantation loin des voisines, ou
  du **titre et de la personne** — jamais de l'id (CLAUDE.md §4, Q213). Un code libre choisi à la main (`rgb`) passe devant.
- **L'EXCEPTION INGÉNU** (la palette par défaut, clé `signal`) : **sous Ingénu seulement, la couleur dit la nature** — Promi
  bleu `#82AEF8` (ton 0), Chiche rose `#FFB8D2` (1), Cercle lilas `#C9A8F5` (2), cellule sans parole crème dalle `#EFE3C7` (3) ;
  un ton choisi à la main passe devant. Sous toute autre palette, la dalle garde sa couleur figée (CLAUDE.md §4, v17, Q307).
- **TOUT SUIT LE STUDIO, SAUF L'AURA** (v34) : la Toile, l'Index, le Fil, les fiches, la page +, Partager, la Toile d'un
  Cercle prennent le monde et la palette choisis au Studio. Seules **les îles de la Pelote et la liste « Ce que tu as tenu »**
  gardent le monde et la couleur de plantation (`p.monde = {m, p, h}`, demandé explicitement — 4ᵉ argument ou
  `opts.plantation`). **Les ÉTATS ne suivent jamais rien.**
- **JAMAIS DE KAKI** : est kaki toute couleur de teinte OKLCH **78°–140°**, chroma **0,015–0,10**, luminance **0,20–0,80**.
  Interdit sur toute dalle et toute matière vide produite par l'app ; seule exception, la couleur mère que l'utilisateur
  choisit lui-même. Un mélange peut y faire entrer ce qui n'y est pas (CLAUDE.md §3 blocs v114, v115). ⚠ Le juge
  `redteam_kaki.py` est né ROUGE et la correction attendait une décision (CLAUDE.md §7) — **⚠ TROU :** l'état de la dette
  de kaki au jour du portage n'est écrit dans aucun des documents lus.
- **Dans la bande haute d'une fiche et le champ de la page + — et nulle part ailleurs —** la dalle est remappée sur la rampe
  de sa nature (Q30), peinte PAR LE MOTEUR (`opts.rampe`) ; avec « La dalle d'origine », la couleur d'origine sauf ton sur
  ton (ΔE < 15) (CLAUDE.md §4 ; §3 bloc v118).

### a.10 · Le régulateur et les budgets de la Toile

> **⚠ TROU : LA TOILE N'A PAS DE RÉGULATEUR.** Cherché : `régulateur`/`regulateur` dans `promi-moteur.js` (aucune occurrence),
> `CONTRAT-MONDE.md` (aucune), CLAUDE.md (le mot ne désigne que celui de la Pelote, §c). Le seul régulateur du prototype est
> celui de la densité de la Pelote. Pour la Toile, CLAUDE.md §11 dit : « l'ordre, les paliers et les seuils seront fixés par
> mesure Instruments sur appareil, au premier lot Toile du portage. Aucun chiffre n'est décidé à ce jour. »

Ce que la Toile a, à la place :

- **Une boucle qui s'ARRÊTE.** Rien ne tourne au repos : la boucle d'images démarre sur un événement (`kick`,
  `promi-moteur.js:6195`) et s'éteint quand tout est posé ; entre deux mouvements de repos, un seul minuteur (§d).
- **Le budget d'un monde** (`CONTRAT-MONDE.md` §8.3) : **Toile ≤ 16,7 ms à ×1 et ≤ 50 ms à ×4 ; une dalle de 200 px ≤ 50 ms
  à ×1** — mesuré **au DESSIN forcé**, jamais au calcul seul, sur des canevas distincts (§12 ter, Q5), et **aussi sur le
  moteur de Safari** (§8.4 ; CLAUDE.md §8). Les chiffres mesurés monde par monde : `CONTRAT-MONDE.md` §8.4, §8.5, §15.4,
  §15.15 (`BUDGET-SAISON2.md`). Planchers assumés : Guingois et Chamade (§15.15–15.16).
- **Un cache de rendu dont la clé porte tout ce dont l'image dépend**, et rien d'autre ne l'expire ; une signature prise à la
  précision que l'œil voit (½ px) ; **tant qu'une signature change d'une image à l'autre, on repeint l'état d'avant** et on ne
  reconstruit que posé (CLAUDE.md §8, lignes v29 et v33).
- **Un nombre illimité de paroles** (v98) — `ETAT-DES-LIEUX.md` (l. 9847-9852) relève à 500 paroles, en WebKit : pire image
  82 ms pour les huit anciens (Houle), Ramage 5,5 s pour la première image du chargement ; à 200, fluide partout. Ce sont des
  MESURES du prototype, pas des budgets décidés.
- **Aucune mesure sur appareil** pour la Toile (`CONTRAT-MONDE.md` §8.3 : « tenable sur un téléphone récent, limite sur
  l'iPhone 12 — aucune mesure sur appareil »).

---

## (b) LES MONDES

### b.1 · La table des vingt (`ETAT-30-SEPTEMBRE-2026.md` §4, engendrée de l'app, dans l'ordre du Studio)

| # | Affiché | Clé interne | Accès | Semis |
|---|---|---|---|---|
| 1 | Pochade | `encre` | gratuit | constant |
| 2 | Touffe | `touffe` | gratuit | constant |
| 3 | Brouillamini | `brouillamini` | gratuit | grandit |
| 4 | Halin | `halin` | gratuit | grandit |
| 5 | Esquille | `esquille` | gratuit | grandit |
| 6 | Tesselle | `mosaique` | gratuit | constant |
| 7 | Braille | `braille` | gratuit | constant |
| 8 | Buvard | `pixel` | gratuit | constant |
| 9 | Ramage | `ramage` | Ma Parole ! | grandit |
| 10 | Guingois | `guingois` | Ma Parole ! | grandit |
| 11 | Chantourné | `chantourne` | Ma Parole ! | grandit |
| 12 | Volubilis | `volubilis` | Ma Parole ! | grandit |
| 13 | Madrure | `madrure` | Ma Parole ! | grandit |
| 14 | Chamade | `chamade` | Ma Parole ! | grandit |
| 15 | Ritournelle | `ritournelle` | Ma Parole ! | grandit |
| 16 | Bobinette | `bobinette` | Ma Parole ! | grandit |
| 17 | Mascaret | `mascaret` | Ma Parole ! | grandit |
| 18 | Éclisse | `terrazzo` | Ma Parole ! | constant |
| 19 | Taille-douce | `gravure` | Ma Parole ! | constant |
| 20 | Houle | `sillons` | Ma Parole ! | constant |

Huit gratuits, douze dans Ma Parole !. **Les clés internes ne changent jamais** quand un nom affiché change. Éclats est retiré.
Les réglages que chaque monde déclare au moteur (`ressort`, `grille`, `pasTrame`, `libre`, `relaxLocal`, `compagnons`…) :
même table, colonne « Réglages déclarés » (`REGLAGES_MONDE`, `promi-moteur.js:5977`).

### b.2 · Le contrat d'un monde — RENVOI à `CONTRAT-MONDE.md` (ne pas le recopier)

Ses obligations, en une page ; le numéro de section dit où lire.

| Obligation | § |
|---|---|
| Un monde est **une fonction de peinture** : il reçoit tout du moteur (surface, graines, couleurs, taille) et **ne garde aucun état** d'un appel à l'autre. Cinq chemins l'appellent (Toile vivante, dalle seule, export, aperçus) : il se comporte identiquement dans les cinq. | 0, 1 |
| La **transition** est gardée par le moteur, pas par le monde : il la lit (`env.trans` : arrivée ou départ, sa place, son rang) et déclare sa durée (`transDur`). | 1 (amendé v43), 15.9–15.11 |
| **Signature** : il ne rend rien, dessine en coordonnées de Toile, **ne remplace jamais la transformation**, laisse le contexte comme il l'a trouvé. | 2 |
| **La cellule est implicite** (la règle pondérée) : trame CONTENUE (il cherche la graine propriétaire de chaque échantillon) ou matière LIBRE (déclarée telle). | 3 |
| **Il ne choisit jamais une couleur** : `cOf` seul ; préséance, répartition des quatre tons, ce que la couleur ne porte jamais. | 4 |
| Les **rampes de matière** d'une cellule vide, et le **fond** entre les fragments. | 4 bis, 4 ter |
| **L'échelle** : toute longueur × `UK` — la même dalle à trois tailles est la même image ; plancher de lisibilité vers 40 px. | 5 |
| **Le monde de plantation** se fige sur la parole (`{m, p, h}`) ; tout cache indexé par monde ou palette est interdit ou invalidé. | 6 |
| **Le déterminisme** : au repos, fonction PURE de la géométrie, de la couleur et d'une graine tirée d'une CLÉ STABLE (titre + personne ; nom du Cercle) — jamais `random`, une horloge, la taille du canevas ni l'index de la graine. L'horloge ne sert qu'au frémissement. | 7 |
| **Le budget**, au dessin, à ×1 et ×4, et sur le moteur de Safari. | 8, 12 ter |
| **Ce qu'une dalle n'est jamais** (l'interdiction en tête de ce document). | 9 |
| Où un monde se **branche**, et ce qu'il **passe avant d'être livré** (juges, budget, capture à trois tailles regardée). | 12, 14 |
| Les **dérives** des huit anciens (lues dans le code), à ne pas reproduire. | 11 |
| Les mondes neufs, un par un : unité de matière fixe, transitions, mouvements, budgets de la saison 2. | 15 |

⚠ `CONTRAT-MONDE.md` §7.2 écrit que la FORME d'une cellule n'est pas stable (semis tiré au hasard à chaque chargement).
`ETAT-30-SEPTEMBRE-2026.md` §4 dit depuis : « le semis est amorcé par la clé de la Toile (assainissement, 30 sept.) : même
Toile à chaque ouverture ». L'ordre des sources donne raison à l'ÉTAT.

---

## (c) LA PELOTE — la boule de l'Aura, le seul volume de l'app

### c.1 · Géométrie (points, écran 390 × 844)

Boîte de la boule 296 × 296 à (47 ; 105,532) ; **rayon de la boule 116** (`K.R` 0,392 × 296) ; **silhouette (boule + poil)
121** ; `D` = 232,064 (`app.html:29302`, `29330` ; `SPEC-JUGES.md` §4). Cotes de l'écran, figées sur la composition B :
CLAUDE.md §3 bloc v126 (`COTES_B`, ± 0,5 pt). **Rien ne dépasse jamais de la silhouette** (v116, `redteam_contour.py`).

### c.2 · Le rendu par la carte graphique (v125, v126 — `peintGL`, `app.html:28912-29262`)

**La cause nommée** (iPhone 16e, 75 000 poils : 187 ms par image, 5 images/s) : le peintre repassait en JavaScript sur chaque
poil, à chaque image. **La parade :**

- **L'état des poils est envoyé UNE FOIS** à la carte graphique (position, normale, flux, couleur, poli — dans le repère de
  l'objet, où ils ne bougent pas) ; renvoyé seulement quand il change.
- **À chaque image, le shader fait** la rotation, la projection, la lumière du velours (le souffle compris) et pose le
  tampon du poil : **UN POINT par poil**, seuls les pavés tournés vers l'œil. Le carré du point se cale sur la boîte du
  tampon du poil, pas sur son pixel.
- **Ce sont les mêmes poils aux mêmes pixels** (ΔE00 moyen 0,3 contre le peintre, 98 % des pixels ≤ 2) : **pas de texture
  plaquée sur une sphère, donc ni couture ni pôle** ; la frange de la silhouette reste celle du poil. « Le rendu par les
  poils, pas par une texture : accepté par Tom. »
- La règle « le plus opaque gagne » devient un test de profondeur (profondeur écrite = 1 − alpha).
- **Le contact du doigt est dans le shader** (v126, C-029) : plateau, cuvette en `asin`, bourrelet, cloche ; place, normale
  par la pente, peigne couché, ombre du fond ; l'empreinte arrive en uniformes.
- **Trois mesures à ne pas reperdre** (CLAUDE.md §3 bloc v125) : ① recopier le canevas de la carte dans un canevas 2D coûte
  6 à 20 ms par image — on AFFICHE le canevas de la carte ; ② le coût est celui des SOMMETS, pas des pixels (220 000
  rectangles de quatre sommets : 21–26 ms ; un point par poil : 17) ; ③ le calage du point sur la boîte du tampon.
- **Un canevas qu'on remplace se RETIRE** (contexte perdu après le Studio : l'ancien canevas restait dessous, un second
  contour — CLAUDE.md §3 bloc v130, C-002).
- WebGL 2 ; un WebGL rendu par le processeur est refusé (`failIfMajorPerformanceCaveat`) : le peintre d'origine peint.
  En Swift : Metal — le repli n'a pas d'objet.

Mesuré : banc WebKit 141 → 17 ms au p50, 7 → 58 images/s ; sous le doigt p50 17 ms, p95 20 à 25 ms (la cible de 22 est au
bord du banc) ; **iPhone 16e (Tom, `b116538`) : 220 000 poils, p50 17 ms, p95 25 ms, 54–56 images/s** (CLAUDE.md §3 bloc v126).

### c.3 · La densité et son régulateur (`app.html:29448-29454`, `30543-30583`, `30961-30968`)

- **220 000 poils** au palier haut (densité 3 : ×2, poil ×0,7, reflet adouci — des CONSTANTES, `REG`, `app.html:7783`).
- **Six paliers : 220 000 · 180 000 · 150 000 · 110 000 · 90 000 · 75 000.** À 110 000 et en dessous, le poil reprend
  l'épaisseur (×1) et le reflet de la densité 1 (`reglePoil`). « La fluidité passe avant la densité » (Q378).
- **Un palier n'est pas un sous-ensemble du précédent : c'est un AUTRE semis** (76 à 80 % des pixels changent). Donc :
  **le régulateur MESURE et VISE pendant qu'on regarde ; il n'APPLIQUE jamais sous les yeux.**

```
ce qu'il mesure     le temps d'une image ordinaire : ni celle où le cache est refait, ni celles où un doigt est posé ;
                    4 images sautées après un changement. Sous la carte graphique : max(temps JS ; durée de l'image − 8 ms)
quand il juge       après 45 images ; médiane des 45 dernières
il descend          si la médiane > 16,7 ms (`G.BUDGET`) : vers le palier le plus dense qui tiendrait, au prorata des poils
il remonte          après 90 images, si le palier du dessus, au prorata, tiendrait sous 15 ms (l'écart évite le va-et-vient)
quand il applique   quand l'écran se BÂTIT (`prepare`), quand on QUITTE l'Aura, quand l'app passe en arrière-plan
ce qu'il garde      le palier APPLIQUÉ seulement (`promi_pelote_palier`) — jamais la vise : un pic de trois secondes
                    appauvrissait la Pelote pour toujours (Q237)
première fois GPU   il repart de 220 000
```

### c.4 · La couleur — le sol, le corps, pleine

- **Le sol** (la teinte des poils) : un ton de la palette du Studio, tiré à chaque ouverture ; clarté gardée, chroma
  ressaturée à 0,72 × celle du ton ; décalé (vers le blanc ou le noir, teinte gardée) jusqu'à se détacher de la page —
  on vise 44 pour un seuil de 42 (CLAUDE.md §3, blocs des 21 et 22 sept.).
- **Le corps** (la peau sous les poils) : **une AUTRE teinte de la palette, jamais celle des poils**, tirée avec le sol ;
  **ΔE00 ≥ 15** face au sol ET à chaque marche de sa rampe de velours (`CORPS_ECART`, `app.html:29707`) ; jamais kaki ;
  sinon le ton suivant, puis la teinte écartée en clarté, dernier recours crème ou seiche.
- **Le corps ne se voit jamais seul** : les poils sont translucides, il compte pour **un tiers** de la couleur rendue
  (0,675 poil + 0,325 corps, `app.html:29776`). Le tirage écarte la couleur RENDUE de **ΔE00 ≥ 14** de l'ouverture d'avant,
  jamais le même sol ni le même corps deux fois de suite (`promi_pelote_vue`).
- **PLEINE** : l'intérieur est opaque, toujours — **alpha 255 en retrait de 4 % de D**, aux deux thèmes, à tous les
  paliers ; sous la fourrure, un disque plein jusqu'à **0,972 R**, fondu jusqu'à **1,012 R** (`app.html:28567`, `29218` ;
  `redteam_plein.py`).
- **Les îles** (une par parole tenue) **gardent le monde et la couleur de plantation** ; le moteur fournit leurs pixels
  (`opts.donnees`). Lisibilité d'une île sur le sol : **ΔE ≥ 15** (Q192). Les LÉGENDES, les arcs des Noyaux et les états
  ne suivent jamais le Studio.

### c.5 · Le halo, l'ombre — la seule exception à « aucun volume »

- **Le halo** (`window._haloPelote`, `app.html:7787-7814` ; niveau 3, constante) : **la teinte du CORPS** (clarté écartée du
  fond si ΔE00 < 42) ; **ΔE00 14 au ras** de la silhouette, étendue **0,12 D** ; décroissance exponentielle (mi-chemin à
  2,9/7 du ras) ; plus vif du côté éclairé (lumière en haut à gauche, direction `(−0,58 ; −0,72)`), 0,20 du côté opposé ;
  **le quart inférieur presque nul (0,06), fondu en S sur 45° à partir de l'horizontale** — pas d'épaule ; tramé au grain
  de l'app, dosé en niveaux de COULEUR (± 2,75) ; il a son propre canevas, SOUS la boule (330 × 330, centré) ; son haut est
  à **4,5 ± 0,5** du bas du plateau ; il respire avec le souffle.
- **L'ombre** : une ellipse **104,43 × 16,25** (0,45 D × 0,07 D), centrée, à `y = 391,224` (`app.html:7682`, `29351`) ;
  encre du mode en clair (0,10) ; **en sombre, une ellipse CRÈME à 0,105 → ΔE00 5,05** (décidé : 4 à 6) — même géométrie
  (CLAUDE.md §3 blocs v115, v123).
- Écho, couronne de fibres, halo flou : REFUSÉS. Un trait par parole tenue : **EXCLU DÉFINITIVEMENT** (c'est un compteur
  visuel). Tout halo, ombre floue ou dégradé ailleurs dans l'app est refusé (`redteam_volume.py`).

### c.6 · La respiration et la rotation

- **La respiration est la lumière du velours** (Q364 → A), dans le peintre — rien ne change au-delà de la silhouette.
  `SOUFFLE = {MAX 0,55 ; MONTE 4 s ; DESCEND 6 s ; DEPART 0,6 s}` (`app.html:30433`) : **cycle de 10 s — 4 s de montée, 6 s
  de retour**, en demi-cosinus, 0,6 s après l'affichage (sommet à 4,6 s, retour à 10,6 s). Elle avance au **temps réel**
  (borné à 0,5 s après une pause seulement), seulement quand la Pelote est vue. « Réduire les animations » : immobile à
  mi-niveau.
- **La rotation de repos** : `G.AUTO = 2π / 100` rad/s — **un tour en 100 s** (`app.html:29421` ; `releve-aura.py:78`).

> ⚠ **Divergence.** CLAUDE.md §7 (« UN JUGE QUI LIT LA VALEUR QU'IL VÉRIFIE ») cite `AUTO_DECIDE = 2π/120`, la décision du
> 10 sept. (« un tour en 2 minutes »). Le code ET le juge portent depuis **`2π/100`** (« un tour en 100 s », Tom, 12 sept.).
> **La valeur à porter est `2π/100`** ; CLAUDE.md n'a pas été repris sur ce point.

- **Sur un objet qui tourne, on compare à l'ANGLE et au même SOUFFLE**, jamais à l'instant (CLAUDE.md §8 ; §3 bloc v126).
- La Pelote ne se peint pas quand un autre écran la couvre (jugé au doigt, une image sur six).
- Le toucher, l'élan, l'empreinte : SPEC-GESTE §6.6. Historique des acquis et des rejets : `AUDIT-PELOTE.md` (le peigné est
  une mécanique, l'empreinte est un plateau, le contour reste un cercle exact, le relief est de surface).

---

## (d) LA VIE AU REPOS (v126–v128 — `promi-moteur.js:6196-6280`, `6697`)

**« De temps en temps, la matière d'une ou deux dalles bouge à peine, selon la manière de son monde, pendant 1 à 2 s. »** (C-028)

| | Valeur | Ligne |
|---|---|---|
| Intervalle | tiré entre **5 et 15 s** (`5000 + hasard × 10000`), **compté de la FIN d'un mouvement** ; le premier intervalle est armé 2 s après le démarrage | 6257, 6271 |
| Combien de dalles | **une** (70 %) ou **deux** (30 %, s'il y en a plus d'une) | 6268 |
| Lesquelles | une dalle de parole ou de Cercle (jamais une cellule vide) **visible à l'écran** ; un monde peut dire lesquelles peuvent (`vivPeut`) | 6265-6266 |
| Durée | **1 à 2 s** (`1000 + hasard × 1000`) | 6268 |
| Forme | **en cloche** : `sin(π·u)² × 0,28` (le quart de l'amplitude du frémissement) ; pour sept mondes une cloche PLEINE (`_VIV_PLEIN`, montée et descente sur le premier et le dernier septième, amplitude 0,28 à 0,45) | 6233, 6697 |
| Par quelles voies | celles du frémissement : place, étirement, tour, poids de matière — chaque monde les lit à sa manière | 6200-6203 |
| Le hasard | hors de la suite du moteur (le rythme ne doit pas devenir prévisible) | 6253 |
| Entre deux mouvements | **un seul minuteur ; la boucle d'images est arrêtée** | 6204 |
| La queue | **420 ms** après un mouvement, la boucle tourne encore, la Toile rendue à l'image d'avant à chaque image (les ressorts convergent sans se voir) — sauf les quatre mouvements écrits dans le peintre | 6233 |

**Conditions d'arrêt** (`_vivTire`, `_vivPlan`, `_vivLibre`) : rien si l'écran est **couvert** (jugé au point, au centre de la
Toile), en **arrière-plan**, sous **« Réduire les animations »**, pendant une plantation, ou **dans les 5 s** d'un toucher,
du mouvement précédent, d'une arrivée ou d'un départ, ou de tout changement de la Toile. Un toucher repousse le suivant d'un
intervalle entier ; le moteur occupé un instant : on réessaie 400 ms après.

**LE RETOUR EST EXACT** (v127) : au tirage, **la Toile ENTIÈRE est gardée telle qu'elle est peinte** (1 : 1, sur elle-même —
ni une dalle ni un fragment) et **rendue pixel pour pixel à la dernière image** si rien d'autre n'a changé (signature :
monde, palette, taille, densité, nombre de graines, dernier changement, vue, thème — `_vivSigne`). On restaure l'état
d'origine, on ne rejoue pas le mouvement à l'envers. **Le titre ne bouge jamais.** Un mouvement qui ne déplace que le titre
n'est pas un mouvement de matière. Juge : `redteam_retour.py` (cent mouvements et plus, 0 pixel).

**Les mondes** : sept sont ENFERMÉS (`_VIV_CLOS` : hors de la cellule de la dalle tirée, l'image d'avant est rendue à chaque
image — le mouvement ne gagne jamais la Toile) ; deux lisent une graine PRÊTÉE à sa place du moment (`_VIV_GR` : Madrure,
Bobinette) ; quatre ont un mouvement **écrit dans leur peintre** (v128 : Chamade — le cœur bat ; Chantourné — le médaillon
tourne à peine ; Brouillamini — la dalle pivote sur sa graine ; Mascaret — la lame glisse) : des tracés repeints sous une
transformation, jamais une image déplacée.

> ### SEIZE MONDES BOUGENT. QUATRE RESTENT IMMOBILES ET SONT REPORTÉS À SWIFT (C-031)
> **Volubilis · Guingois · Ramage · Esquille** (`_VIV_NON`, `promi-moteur.js:6231`). Leur matière est construite une fois et
> gardée tant que le semis ne bouge pas (Volubilis, Guingois, Ramage) ; Esquille bougeait par à-coups et sa boucle ne
> s'arrêtait plus. **À écrire dans leur peintre natif : une ou deux dalles, 1 à 2 s, jamais le titre, retour exact à l'image
> d'avant** (`portage/A-INTEGRER.md`, C-031 ; raisons : `CHANTIERS.md`, C-031).

Ramage, par ailleurs : le disque de la pousse est SUPPRIMÉ (v127) — la plume arrive d'un coup, en une image.

---

## (e) LES PALIERS QU'ON PEUT DÉGRADER — le principe, sans chiffres (CLAUDE.md §11, Tom, 30 sept. 2026)

**Raison :** iOS 26 fixe le plancher système à l'iPhone 11. **Promi n'ajoute aucun plancher** : l'app tourne sur tout appareil
supporté et sa qualité s'adapte, pour que personne ne soit exclu et que personne ne subisse une Toile qui saccade.
**Ce qui fait tenir une parole ne se négocie jamais. Seul l'ornement se dégrade, du moins visible au plus visible.**

| NE SE DÉGRADE JAMAIS | PEUT SE DÉGRADER |
|---|---|
| **le geste** — tous les `coalescedTouches` traités, le trait rendu dans la trame du toucher, en pleine résolution | le nombre de dalles animées |
| **les couleurs** — hex exacts, aucune quantification | les transitions de navigation |
| **la lisibilité** — texte natif, contrastes, tailles, Dynamic Type | la complexité des mondes |
| **la composition de la Toile** — toutes les dalles présentes, positions identiques | la densité de la Pelote |
| **VoiceOver** | |

**L'ordre, les paliers et les seuils seront fixés par mesure Instruments sur appareil, au premier lot Toile du portage.
Aucun chiffre n'est décidé à ce jour : n'en invente pas, n'en implémente pas.**

**Le seul modèle chiffré est le régulateur de la Pelote** (§c.3) : six paliers de 220 000 à 75 000 poils ; il mesure et vise
pendant qu'on regarde, il n'applique jamais sous les yeux, il remonte, il ne garde que ce qu'il a appliqué.
(CLAUDE.md §11 écrit « de 110 000 à 75 000 » : c'était l'état d'avant la densité 3 ; depuis v124 les paliers sont six.)
Ce qu'il enseigne pour le reste : **une dégradation ne se voit jamais se faire**, et **elle n'est jamais définitive**.

---

## (f) L'INTERDICTION

Elle est en tête de ce document, en encadré : **jamais de capture de Toile à la place d'une dalle.** Elle prime sur tout ce qui précède.

---

## (g) LE BANC DE RENDU DE RÉFÉRENCE — `banc_rendu.py`, 280 images au pixel

**C'est lui qui juge la matière d'un monde, et il jugera le portage** (`SPEC-JUGES.md` §5 ; `banc_rendu.py:1-23`).

**Ce qu'il fige** — pour chacun des **20 mondes**, palette par défaut, teinte 0 :

| Image | Comment elle est rendue | Nombre |
|---|---|---|
| `toile-sombre`, `toile-clair` | la Toile ENTIÈRE, `Toile.renderTo(cv, 1, clair)`, **sans les titres** des dalles, 390 de large | 2 |
| `dalle-<nature>-k<k>` | `Toile.dalleTrame(cv, pid, k, {m, p, h})` — **4 paroles** (un Promi, un Chiche, une tenue, une d'un Cercle), désignées **par leur titre**, jamais par leur id, × **3 tailles** `k = 0,5 · 1 · 2` | 12 |

Soit **14 images par monde, 280 en tout**, en PNG avec leur empreinte (sha1 des pixels RGBA), dans `banc-rendu/ref/`.

**Ce qui le rend déterministe :**
- **le hasard est amorcé avant le chargement** (`Math.random` → mulberry32, graine `0x5EED2026`) : jeu de démonstration,
  semis, couleurs — tout vient de la même suite ;
- **l'horloge est figée** pendant chaque rendu (`performance.now` → 123 456 ms) ; après le chargement, le banc PILOTE le
  temps : images (`requestAnimationFrame`), minuteurs et rappels de fond n'avancent que quand il les donne — rien ne
  dépend de la machine ; chaque monde reçoit **240 images** (4 s d'horloge virtuelle) après avoir été posé ;
- **le monde doit être AU REPOS** : deux rendus séparés de 1 500 ms doivent être identiques ; au-delà de 20 s il est
  déclaré « instable », et le banc le DIT ;
- moteur : **WebKit** (celui de l'iPhone) ; Madrure y est rendu par le chemin que WebKit sans écran prend.

**Ses modes :** `--figer` pose la référence ; sans option, il compare — **0 pixel différent attendu**, sinon le détail ;
`--deux` passe deux fois sans référence et prouve le déterminisme ; `--monde=` un seul monde.

**Comment il jugera le portage.** Le peintre Swift de chaque monde, nourri du **même semis** (les graines : positions,
poids, couleurs figées, clé de la Toile) et de la **même horloge figée**, doit rendre les mêmes 14 images.

> **⚠ TROUS, à trancher avant le premier lot Toile :**
> 1. **La tolérance.** Le banc exige 0 pixel entre deux passes du MÊME moteur de dessin. Entre le canevas de WebKit et
>    CoreGraphics / Metal, l'anticrénelage différera (le prototype le mesure déjà entre Chromium et WebKit : jusqu'à 7,3 % de
>    pixels différents sur les bords d'un même tracé — CLAUDE.md §8). **Aucun document ne fixe le seuil d'acceptation du
>    portage** (cherché : `banc_rendu.py`, `SPEC-JUGES.md`, CLAUDE.md §7 et §8 bis, `CONTRAT-MONDE.md`). Les seules exceptions
>    écrites à « zéro écart » sont la matière face aux planches et le dessin des glyphes (CLAUDE.md §8 bis).
> 2. **L'export du semis.** Le banc amorce `Math.random` et laisse l'app tirer son jeu de démonstration : les graines de la
>    référence ne sont écrites dans aucun fichier lisible par Swift. Il faudra les exporter (`Toile_graines()` rend
>    `[pid, x, y, nature]`, `promi-moteur.js:6281` — sans les poids ni les couleurs).
> 3. **La densité.** Les images sont à la densité du moteur (plafonnée à 2, `promi-moteur.js:6087`) ; l'iPhone est à 3, et
>    toute planche se fait à 3 (CLAUDE.md §7, v114). Aucune référence @3x n'est figée.
> 4. **Ce que le banc ne couvre pas** : le mouvement (arrivée, départ, vie au repos — c'est `SPEC-JUGES.md` §1 et
>    `redteam_retour` qui les portent), les 23 autres palettes, la Pelote, les titres, le zoom.

---

## Récapitulatif des juges du prototype cités

| Juge | Ce qu'il garde |
|---|---|
| `banc_rendu.py` | la matière des 20 mondes, au pixel (280 images) |
| `redteam_decoupe.py` | une dalle n'est jamais une image découpée (familles A à H, G2) |
| `redteam_rythme.py` | le rythme d'un monde ne dérive pas ; Houle par image ; lancé avec le vrai GPU |
| `redteam_vivant.py`, `redteam_retour.py` | la vie au repos, le retour exact |
| `redteam_dalle_figee.py` | une dalle garde sa couleur et son monde |
| `redteam_kaki.py` | jamais de kaki |
| `redteam_plein.py`, `redteam_corps.py`, `redteam_halo.py`, `redteam_zone.py`, `redteam_contour.py`, `redteam_souffle.py`, `redteam_volume.py` | la Pelote : pleine, son corps, son halo et son ombre, rien derrière, rien ne dépasse, le souffle, le seul volume |
| `redteam_pelote_doigt.py`, `releve-aura.py` | le creux sous le doigt ; les cotes de l'Aura et la vitesse de rotation en dur |
