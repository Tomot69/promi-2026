# CONTRAT-MONDE — ce qu'un monde de la Toile doit respecter

> **Pour qui :** celui qui écrit un nouveau monde et ne connaît pas Promi.
> **Ce qui fait foi :** le code du moteur (`app.html`, bloc de la Toile, l. 7746–8604 au 22 sept. 2026),
> CLAUDE.md §3-§4-§9, et les décisions de Tom citées. Tout ce qui suit a été **lu dans le code ou
> mesuré** ; ce qui ne l'a pas été est dit.
> **Écrit le 22-23 sept. 2026**, pour les quatre mondes qui arrivent.

---

## 0 · En une phrase

Un monde est **une fonction de peinture** que le moteur appelle pour dessiner **toutes les cellules
d'une Toile d'un coup**, dans un contexte 2D qu'il a préparé. Le monde ne choisit ni ses couleurs, ni
ses cellules, ni sa taille : **il reçoit tout du moteur et peint dans chaque cellule, avec le contour de
la cellule, à la taille où le moteur l'appelle.** Le moteur se charge du reste — découper une dalle,
la figer dans son monde de plantation, la rendre sur une carte ou une fiche.

Le moteur lui-même **ne se modifie pas** (CLAUDE.md §9). Un monde s'y **ajoute** ; il ne le change pas.

---

## 1 · Où vit un monde, et le registre

Tous les mondes vivent dans la même fermeture (l'IIFE qui commence par
`var host=document.getElementById('toileCv')`). Ils sont déclarés dans **un seul registre** :

```js
var RD={pixel:Rpix, braille:Rbra, sillons:Rsil, gravure:Rgra, mosaique:Rmos,
        encre:Renc, eclats:Rblok, terrazzo:Rterr, touffe:Rtouf};      // ≈ l. 7942
```

`eclats` existe dans le registre mais **n'apparaît pas au Studio** (Q102) : ne pas le remettre dans un rail.

Le moteur appelle `RD[theme](now, x0, y0, x1, y1)` depuis **cinq** chemins, et un monde doit se
comporter identiquement dans les cinq :

| chemin | qui l'appelle | ce que valent `g`, `W`, `H`, `view` |
|---|---|---|
| `frame(now)` | la Toile de l'accueil, à chaque image animée | le canevas `#toileCv` ; `W×H` = la Toile ; `view` = le zoom du doigt ; transformation `view.s·DPR` déjà posée, **et un `clip` aux coins arrondis** |
| `Toile.dalleTrame(cv, pid, k, monde)` | **toute dalle hors de la Toile** (fiche, carte, Fil, Pelote…) | un canevas neuf à la taille de LA cellule ; `W×H` = la boîte de la cellule + marge ; `view = {s:1,ox:0,oy:0}` ; transformation `DPR` |
| `Toile.renderTo(cv, ech, clair)` | l'image partagée « Ma Toile » | la Toile entière à l'échelle `ech` ; `view` identité |
| `Toile.repaint(pcv)` / `repaintWorld` | les aperçus du Studio | une Toile d'aperçu (`pcv.__c`), graines à elle |
| `Toile.preview(pcv, th, pw, ph)` | fond de Partager, carte du Studio | une grille d'aperçu tirée à la volée |

**Pendant l'appel, le moteur a ÉCHANGÉ ses globales** (`g`, `W`, `H`, `seeds`, `view`, `theme`,
`palKey`, `hueShift`, `_palLit`) et il les **restaure après**. Conséquence : **un monde ne garde aucun
état entre deux appels** (pas de cache de `W`, de `seeds`, de palette) — il fuirait d'une dalle à la
Toile ou l'inverse. C'est exactement le piège de `_palLit` décrit au §4 de CLAUDE.md.

---

## 2 · La signature

```js
function Rnom(now, x0, y0, x1, y1){ … }      // ne rend RIEN ; peint dans `g`
```

| reçoit | sens |
|---|---|
| `now` | `performance.now()` en ms. **À ne lire que pour le frémissement** (voir §7.1) — jamais pour tirer une forme. |
| `x0, y0, x1, y1` | le rectangle **visible**, en coordonnées de Toile (déjà divisé par le zoom). Un monde PEUT s'en servir pour ne pas peindre hors champ ; il ne doit rien en déduire d'autre. |

| lit dans la fermeture (lecture seule) | sens |
|---|---|
| `g` | le contexte 2D, **transformation déjà posée** |
| `W`, `H` | la taille de la surface, en coordonnées de Toile |
| `DPR` | la densité (≤ 2) |
| `seeds` | le tableau des cellules (§3) |
| `view` | `{s, ox, oy}` — le zoom ; **identité** dans une dalle, un export, un aperçu |
| `cOf(s, now)` | **la couleur d'une cellule** — la seule source de couleur autorisée (§4) |
| `avg()` | l'écart moyen entre graines, `√(W·H / n)` — **l'unité de longueur d'un monde** (§5) |
| `cAt(x, y)` | la cellule qui possède le point `(x, y)` (règle pondérée exacte) |
| `isLightM()` | le thème (clair / sombre) de la surface peinte |

**Ce qu'il rend : rien.** Il laisse `g` dans l'état où il l'a trouvé (`save()` / `restore()` s'il
change `lineCap`, `globalAlpha`, une transformation…).

**Règle de transformation — la seule à retenir :** un monde **dessine en coordonnées de Toile et
n'appelle jamais `setTransform`**. La transformation posée par l'appelant contient déjà le zoom, la
densité et l'échelle d'export ; la remplacer, c'est les perdre. (Cinq mondes existants dérogent, §11.)

---

## 3 · La cellule : ce que le monde reçoit — et ce qu'il ne reçoit PAS

**Il ne reçoit ni chemin, ni masque, ni boîte.** Il reçoit **toutes les graines** (`seeds`), et la
cellule d'une graine est **implicite** : c'est l'ensemble des points qu'elle possède selon la règle
pondérée du moteur —

```js
// le point (x, y) appartient à la graine k qui minimise :
Math.hypot(x - kx, y - ky) - seeds[k].w
// où (kx, ky) = (s.px ?? s.x, s.py ?? s.y)   ← px/py : la position PEINTE (frémissement compris)
```

C'est une frontière **courbe** dès que les poids `w` diffèrent. Le monde a donc deux façons de
respecter sa cellule :

1. **Une trame contenue** (Pixel, Mosaïque, Braille, Sillons, Gravure) : pour chaque échantillon, le
   monde cherche la graine propriétaire (`cAt`, ou la boucle équivalente) et peint **dans sa couleur**.
   Le contour de la dalle naît de la trame elle-même. C'est la voie recommandée.
2. **Une matière libre** (Encre, Terrazzo, Touffe) : le monde pose des formes **autour** de la graine,
   qui débordent de la cellule. Il doit alors être **déclaré libre** (la liste `LIBRE` de
   `dalleTrame`) : le moteur isole la graine, peint, et **n'applique pas** le masque pondéré.

**Ce que porte une graine** (`mk()`, ≈ l. 7800) — lecture seule :

```
x, y         position de repos           px, py     position peinte (frémissement)
w            poids (taille de la cellule) kind       'gray' | 'promi' | 'nuee'
pid          id du Promi (null si vide)   nuee       clé de Nuée (dalle de Nuée)
ci, lit      couleur figée (index, clarté) rgb, choisi, nat, apercu   → lus par cOf, pas par le monde
gray, gc     gris d'une cellule vide     tone, shade  modulation d'un gris
ang          un angle (Gravure)           ph, am     phase et amplitude du frémissement
dw, dsx, dsy, drot   déformation du frémissement (0 / 1 / 1 / 0 au repos)
```

**Et la boîte ?** Elle existe, mais pour l'APPELANT, pas pour le monde : `Toile.dalleAbs(pid)` rend
`{poly, minx, miny, w, h}` — un **polygone approché** (`_cellPoly`, bissectrices décalées par les
poids). `dalleTrame` s'en sert pour dimensionner le canevas, puis **refait l'attribution pixel par
pixel** avec la règle exacte ci-dessus. Un monde n'a jamais besoin de `dalleAbs`.

---

## 4 · Les couleurs

### 4.1 · Un monde ne choisit JAMAIS une couleur

**Toute couleur de cellule s'obtient par `cOf(s, now)` → `[r, g, b]`.** Un monde peut en dériver des
nuances (plus clair, plus sombre, une opacité) — il ne peut **ni en inventer une, ni en écrire une en
dur**. `cOf` encode tout ce qui suit ; un monde qui le contourne casse l'une de ces règles sans le voir.

### 4.2 · L'ordre de préséance (lu dans `cOf`, ≈ l. 7925 — décisions Q213, 13 sept. ; Q297 / v17 ; Q307 bis / v27)

```
1 · cellule vide (ci == null)              → son gris : s.gray modulé (_shadeG), rampe du monde
                                              (TH[monde].g en sombre, GLIGHT en clair)
2 · CODE LIBRE du Cercle (s.rgb)           → exactement ce code
3 · TON CHOISI À LA MAIN (s.choisi)        → PALL()[s.ci][s.lit]      — même sous Ingénu (Q307 bis)
4 · INGÉNU (palette par défaut, clé
    'signal') hors aperçu                  → la NATURE : PALL()[s.nat ?? 3][s.lit]
                                              Promi 0 bleu · Chiche 1 rose · Nuée 2 lilas · cellule
                                              colorée sans parole 3 crème dalle
5 · toute autre palette                    → PALL()[s.ci][s.lit]      — la couleur figée à la plantation
```

Plus une transition : une cellule qui vient de changer glisse **du gris vers sa couleur en 760 ms**
(`s.t0`). C'est le seul usage de `now` dans la couleur.

### 4.3 · Les quatre couleurs de la palette, et leur répartition

- **La palette** : `curPAL()` rend les **quatre** tons de la palette du Studio (`PALS[palKey].cols`),
  tournés de `hueShift` degrés. `PALL()` les étend à **cinq clartés** chacun
  (`LITS = [0, .10, .04, .14, .07]`, un relèvement de clarté HSL — la teinte et la saturation ne
  bougent jamais ; `LITS[0]` est le code exact de la palette).
- **La répartition entre cellules est faite par le MOTEUR, à la plantation, pas par le monde** :
  - le **ton** (`ci`) : `cc(s)` tire, parmi les quatre, un ton qu'aucune voisine (rayon 1,6 × `avg`)
    ne porte ;
  - la **clarté** (`lit`) : `tones()` donne la plus petite clarté qu'aucune voisine (rayon 1,5 × `avg`)
    ne porte ;
  - puis `_dalleFigee` l'écrit sur le Promi (`p.dalle = {ci, lit}`) : **elle ne bouge plus**
    (§4 de CLAUDE.md, Q213).
- **Ce que le monde fait de la couleur** : il la pose. Il peut la moduler DANS sa cellule (strates,
  grain, liant) à condition que **la couleur dominante reste celle de `cOf`** — c'est elle que l'œil,
  l'Index et le contrôle `redteam_dalle_figee` reconnaissent.

### 4.4 · Ce que la couleur d'un monde ne peut jamais porter

- **une couleur d'état** (`#DD4D23`, `#291547`, `#00341A`, l'amande `#8FE08F`) : un état qui décore
  cesse d'être un signal (CLAUDE.md, « la frontière Studio / état ») ;
- **une couleur de nature** hors du chemin 4 de `cOf` ;
- **un gris neutre** pour un trait (CLAUDE.md §3, « jamais de trait neutre ou gris »).

---

## 5 · L'échelle — la même dalle à 40 px sur une carte et à 200 px sur une fiche

### 5.1 · Ce que le moteur fournit

`Toile.dalleTrame(cv, pid, k, monde)` : le facteur **`k` agrandit la GÉOMÉTRIE** — positions des
graines, poids, marge — et le canevas sort à `≈ (boîte × k + 2·marge) × DPR` pixels.
Mesuré (22 sept., une dalle, DPR 2) : `k = 0,3` → **53 × 44** px · `k = 1` → **174 × 145** · `k = 2,5` → **435 × 363**.

Pour une taille d'affichage visée :

```js
var D = Toile.dalleAbs(pid);
var k = tailleVisee / Math.max(D.w, D.h);     // 40 px sur une carte, 200 sur une fiche
Toile.dalleTrame(cv, pid, k, p.monde);        // puis on POSE cv à 1:1 — jamais redimensionné
```

### 5.2 · Ce que le MONDE doit faire pour que ça marche — la règle neuve

`k` n'agrandit que la géométrie. **Tout ce que le monde mesure en pixels absolus ne suit pas.** Un
pas de trame de 5 px reste de 5 px : à `k = 0,3` la dalle n'a plus que cinq carrés de large, à
`k = 2,5` elle en a quarante — **ce n'est plus la même dalle**. C'est la vraie raison de la règle
« l'échelle est toujours 1 » (CLAUDE.md §4, règle 2).

> **Un nouveau monde exprime TOUTE longueur — pas de trame, rayon de point, épaisseur de trait,
> amplitude d'ondulation, taille d'éclat — en fraction de l'unité `u = avg()`, jamais en pixels.**
> Alors la même dalle, rendue à `k = 0,3` ou `k = 2,5`, est la même image à deux tailles.

⚠ **Piège lu dans `dalleTrame` (pas mesuré séparément)** : pour un monde **contenu**, `W×H` y vaut la
boîte de LA cellule, donc `avg()` n'y vaut plus l'écart de la Toile (il est calculé sur la petite
surface). Le moteur ne le corrige que pour les mondes **libres** (il y pose `W = H = spReal·√n`).
Sur Gravure l'effet est masqué par le poids `s.w` ajouté au rayon — capture regardée : la dalle est
entièrement hachurée. **Un monde contenu doit donc
lire son unité sur le poids ou sur la distance à la graine voisine**, pas sur `avg()` — ou demander au
moteur de publier l'écart réel (voir §10, c'est une modification du moteur).

### 5.3 · Le plancher

Au-dessous d'environ **40 px d'affichage**, un motif à 5-8 répétitions devient illisible. Un monde
déclare le **nombre minimal de répétitions** de son motif dans une cellule ; l'appelant ne descend pas
sous la taille qui les garde.

---

## 6 · Le monde figé à la plantation

- À la plantation, la fabrique `P()` (≈ l. 2898) écrit sur le Promi
  **`monde = {m: design, p: palette, h: teinte}`** (`mondeDuJour()` → `Toile.mondeCourant()`).
- `dalleTrame(cv, pid, k, monde)` reçoit ce `monde` en 4ᵉ argument. Présent, le moteur **remplace
  pendant l'appel** `theme ← monde.m`, `palKey ← monde.p`, `hueShift ← monde.h`, **invalide `_palLit`**,
  peint, puis **restaure les quatre**. Absent, la dalle se peint dans le monde COURANT.
- **Ce que ça impose au monde :** rien, s'il respecte le §1 — il lit `theme`, `curPAL()`, `cOf` au
  moment de l'appel et ne garde rien. **Tout cache indexé par monde ou palette est interdit**, ou il
  doit être invalidé exactement comme `_palLit`.

⚠ **Constaté dans les appelants (lu dans le code, 22 sept.) : sur 29 appels à `dalleTrame`, 6 seulement
passent le monde de plantation** (Index, Fil, Pelote, Mon Folio — l. 19393, 19897, 29281, 30711,
32180, 35577). La fiche, la page +, les pastilles `peintMinis` et 19 autres appellent **sans** : leur
dalle suit le monde courant du Studio. Ce n'est pas l'affaire du monde ; c'est une dette des
appelants, à reprendre avec celle du §10.

---

## 7 · Le déterminisme

### 7.1 · La règle, pour un nouveau monde

> **Au repos, la dalle est une fonction PURE de : la géométrie des graines, la couleur rendue par
> `cOf`, et une graine de hasard tirée d'une CLÉ STABLE de la dalle.** Même dalle, même image — à
> chaque rendu, dans les deux thèmes, sur n'importe quel appareil.

- **Interdit** : `Math.random()`, une horloge, la taille du canevas, **l'index de la graine dans
  `seeds`** (il change à chaque `Toile.sync`, donc à chaque plantation).
- **La clé stable** : pour une dalle de Promi, celle que le moteur emploie déjà pour la couleur —
  **titre + personne** (`_dalleDeCle`, FNV-1a, ≈ l. 2930), **jamais l'id** (il change d'un chargement
  à l'autre sur le jeu de démonstration, chantier 71) ; pour une Nuée, **son nom** ; pour une cellule
  vide, sa position arrondie. Le monde la lit via `s.pid` → le Promi, ou `s.nuee`.
- **Le générateur** : un LCG local à la cellule, amorcé par cette clé (le patron existe déjà,
  `sd = (sd*1103515245 + 12345) & 0x7fffffff`).
- **`now` ne sert qu'au frémissement** : quand `s.dw > 0` (une seconde après une plantation ou un
  changement de monde), le monde PEUT déformer ; à `s.dw === 0` il rend l'image de repos, identique au
  pixel.

### 7.2 · Ce que le moteur garantit aujourd'hui — et ce qu'il ne garantit PAS (lu dans le code)

| | stable ? |
|---|---|
| la **couleur** d'une dalle (`p.dalle`) et son **monde** (`p.monde`) | **oui** — figés (4 et 13 sept.) |
| la **forme** de la cellule (positions `x, y`) | **non** — le semis de la Toile d'accueil est tiré au hasard à chaque chargement (`seedGray`, `Math.random`), rien n'est sauvegardé |
| `s.ang`, `s.ph`, `s.tone`, `s.shade`, `s.gray` | **non** — tirés par `mk()` à chaque `sync()`, donc à chaque plantation |
| les éclats d'Encre / Terrazzo / Touffe | **non** — amorcés par l'**index** de la graine |

**Un nouveau monde ne peut pas réparer la forme** (c'est le semis du moteur) ; il peut — et doit — ne
pas ajouter d'instabilité à la sienne. Les mondes existants qui en ajoutent sont listés au §11.

---

## 8 · Le budget

### 8.1 · Ce que coûtent les huit mondes — MESURÉ

Chromium, Mac Intel i5-8279U ; ×4 = processeur ralenti ×4 (« mobile moyen » Lighthouse, la même
substitution que Q178 — **aucun téléphone mesuré**). DPR 2. 18 dalles du jeu × 2 passes.
Script : `scratchpad/budget.py` de la session du 22 sept.

```
                 une dalle, k = 1 (ms)            la Toile entière, 390×844 (ms)
                 médiane ×1   max ×1   méd. ×4     ×1        ×4
  Encre             4,9        9,9      22,1        5,3      20,2
  Terrazzo          5,7       14,6      22,4        4,2      20,7
  Touffe           15,3       27,4      61,7       13,7      51,0
  Gravure          39,2       61,0     161,3      499,1    1 943,5    ⚠
  Sillons          57,3       81,8     225,4       48,9     183,0
  Braille          73,9      126,5     226,2       29,1     102,2
  Mosaïque        142,4      205,3     547,2       21,4      68,1
  Pixel           201,2      433,6     740,4       72,0     292,2
```

**Deux lectures qui comptent :**
- **Gravure, le plus simple à lire, est la Toile la plus lente — 499 ms, une demi-seconde par image**
  à ×1 : pour chaque point de chaque hachure, il cherche la graine propriétaire parmi TOUTES les
  graines (graines × points × graines).
- **Une dalle coûte plus que sa Toile** pour les mondes contenus (Mosaïque : 142 ms la dalle, 21 ms
  la Toile). Ce n'est pas le monde : c'est le **masque pixel par pixel** de `dalleTrame`
  (pixels × graines). À `k = 2,5`, une dalle Pixel prend **1,07 s** à ×1, **4,4 s** à ×4.

### 8.2 · Le budget d'un nouveau monde — PROPOSÉ, à valider par Tom (Q309)

```
la Toile entière (renderTo, 390×844, DPR 2)   ≤ 16,7 ms à ×1   (une image à 60 i/s)
                                               ≤ 50 ms à ×4     (20 i/s sur un mobile moyen)
une dalle, à sa taille finale                  ≤ 8 ms à ×1 (médiane), ≤ 16,7 ms (max)
                                               — une Index de 12 cartes se peint en ~0,1 s
```

Aujourd'hui **seuls Encre et Terrazzo tiennent les deux** ; Touffe tient la Toile à ×1 et frôle ×4.
La cause de la plupart des dépassements est commune et nommée : **chercher la graine propriétaire
en parcourant toutes les graines**. Un nouveau monde qui en a besoin la cherche **une fois par
échantillon de trame**, jamais une fois par point d'un tracé.

---

## 9 · Ce qu'une dalle n'est JAMAIS — et le contrôle qui le vérifie

> *« Une dalle est peinte par le moteur, dans sa cellule, avec son propre contour, à sa taille
> finale. Jamais une image rognée, jamais un canevas recadré, jamais un morceau de Toile. »* (Tom, 22 sept.)

`python3 redteam_decoupe.py` piège le canevas **à l'exécution**, sur 19 écrans × 2 thèmes, et nomme la
ligne fautive :

```
A · découpe        drawImage à neuf arguments d'une dalle
B · redimension    drawImage d'une dalle à une taille rendue ≠ sa taille
C · pixels         getImageData / putImageData sur une dalle
D · fragment       un morceau de Toile découpé ou redimensionné ailleurs
E · motif / image  createPattern / toDataURL d'une dalle
F · photo          une image de dalle déposée au projet (PROMI_DALLES) posée à la place du moteur
```

Il passe **à chaque lot qui touche une dalle**, et il échoue sur toute ligne **nouvelle**.

---

## 10 · La dette, et pourquoi elle touche le moteur

**Au premier passage (22 sept.), le contrôle a pris l'app en faute sur cinq familles, à 24 lignes,
~2 100 appels par passage.** Elles sont figées dans `decoupe-dette.json`, imprimées à chaque passage.

| famille | lignes | ce que c'est |
|---|---|---|
| B · redimension | 3442 · 3696 · 4884 · 7643 · 9374 · 15432 · 15954 · 17759 · 19427 · 19922 · 20152 · 32187 · 35308 | **toutes les dalles hors de la Toile** : rendues à `k = 1` puis agrandies ou réduites (fiche ×1,5-2,3 ; carte d'Index ×0,27 ; Folio ×0,8…) |
| C · pixels | 4205 · 17850/17865 · 19261 · 27190 · 29537 · 34894/34902 · 15329 | la teinte dominante (`_teinteDalle`), **la teinture de la bande haute (Q30)**, la clarté recalée sur la rampe de nature (**Q297**, cartes et îles de la Pelote) |
| A · découpe | 4574 | la trame de la page + (neuf arguments, source entière, agrandie ×4) |
| D · fragment | 7358 | l'export « Ma Toile » : la Toile rendue puis réduite à ×0,94 |
| F · photo | 9374 | `promiTrame` sans source pose **l'image webp du monde** (`PROMI_DALLES`) — Aura, Fil, Index, Nuée, page + |

**Pourquoi on ne peut pas la solder sans toucher au moteur :**
1. **B** — rendre chaque dalle à sa taille finale veut dire appeler `dalleTrame` avec `k ≠ 1`. Or les
   cinq mondes à trame ont un pas **en pixels** (§5.2, §11) : à `k ≠ 1` ils changent de dessin. Il
   faut que le moteur exprime leurs pas en unité `u`.
2. **C** — la teinture Q30 et le recalage Q297 sont des **décisions de Tom** ; elles sont écrites
   aujourd'hui comme une retouche de pixels APRÈS le moteur. Pour qu'elles soient peintes PAR le
   moteur, `dalleTrame` doit accepter une rampe de couleurs (un 5ᵉ argument) que `cOf` emploierait.
3. **A, D, F** — se corrigent chez l'appelant, sans toucher au moteur.

**Ce lot n'a rien corrigé** : le §9 de CLAUDE.md interdit de toucher au moteur sans demande
explicite. **C'est la question posée à Tom.**

---

## 11 · Les huit mondes suivent-ils le même contrat ? — Non. Les dérives, lues dans le code

| | Encre | Touffe | Mosaïque | Braille | Pixel | Terrazzo | Gravure | Sillons |
|---|---|---|---|---|---|---|---|---|
| **couleur par `cOf` seul** | ✓ | ✗ ¹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **n'appelle pas `setTransform`** | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ |
| **suit le zoom (`view`)** | ✓ (à la main) | ✗ ² | ✓ (à la main) | ✓ | ✓ (à la main) | ✗ ² | ✓ | ✓ |
| **longueurs en unité `u`** | ✓ | ✓ | ✗ 11 px | ✗ 9 px, rayon 2,9 | ✗ 5 px | ✓ | ✗ 8 / 5 px, trait 2 | ✗ 6 px, amplitude 4,5 |
| **contenu dans sa cellule** | libre | libre | contenu | contenu | contenu | libre | contenu | contenu |
| **déterministe au repos** | ✗ index | ✗ index | ✓ | ✓ | ✓ | ✗ index | ✗ `s.ang` | ✓ |
| **Toile ≤ 16,7 ms à ×1** | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗✗ | ✗ |

¹ **Touffe peint le cœur de ses fleurs en `[221,77,35]` — c'est `#DD4D23`, la couleur « à tenir »**,
et ses contours dans une encre écrite en dur (`_tfInk`). Un état qui décore (§4.4).
² **Terrazzo et Touffe remplacent la transformation par `setTransform(DPR…)` et n'appliquent pas
`view` à la main** : lu dans le code, ils ne devraient pas suivre le pincement. **Non vérifié à
l'écran** — à mesurer avant d'y croire.

Et trois registres parallèles doivent être tenus à la main pour chaque monde — c'est aussi une
dérive (§12) : `LIBRE` et `PER` dans `dalleTrame`, `_isG` et `LIVE` dans `frame`.

---

## 12 · Brancher un monde — la liste complète des endroits (lue le 22 sept.)

Un monde n'est pas branché tant qu'il n'est pas dans **chacun** de ces registres :

```
MOTEUR (l. 7746–8604) — ajout, jamais modification d'une ligne existante
  RD            le registre de peinture                               ≈ l. 7942
  TH            sa rampe de gris en sombre ({g: GXXX})                ≈ l. 7786
  LIBRE         s'il déborde de sa cellule (dalleTrame ET dalleCapture) ≈ l. 8407, 8491
  PER           s'il a une trame ANCRÉE (pas en px, pour l'alignement)  ≈ l. 8498
  _isG / LIVE   l'amplitude du frémissement / l'animation continue   ≈ l. 8025, 8067
APP
  la carte du Studio (label, description)                            ≈ l. 2877
  WL, order     le rail du Studio ; _lockW s'il est du Cercle (deux lignes) ≈ l. 6758-6769
  _map          nom affiché → clé                                      ≈ l. 3189
  shareMosaicFull  sa branche de rendu d'aperçu                        ≈ l. 7690
  onboarding    order + boutons .obd                                   ≈ l. 8646, 9218
  MONDES_O      la Pelote                                              ≈ l. 27157
  MONDES / POIDS / PLEIN / LIGNE / HAUT   le Studio (cadre 346×206)    ≈ l. 31240-31308
NE PAS FAIRE
  PROMI_DALLES  n'y ajoute AUCUNE image : c'est la famille F du contrôle
```

---

## 13 · L'exemple complet — Gravure

Gravure (≈ l. 7929), tel qu'il est dans le moteur, **mis en page et commenté**. Il respecte le
contrat pour la cellule, la couleur et la transformation ; il y déroge pour l'unité (8 px, 5 px,
trait 2), le déterminisme (`s.ang`) et le budget (§8.1). **Un nouveau monde reprend sa structure, pas
ces trois dérives.**

```js
function Rgra(now, x0, y0, x1, y1){
  g.lineCap = 'round'; g.lineJoin = 'round';
  var HS = 8,            // écart entre deux hachures   ⚠ en px : devrait être u × 0,13
      SS = 5,            // pas d'échantillonnage le long d'une hachure  ⚠ idem
      ac = avg();        // l'unité : écart moyen entre graines
  for (var ci = 0; ci < seeds.length; ci++){
    var s = seeds[ci];
    // hors du rectangle visible (avec une marge) : on ne peint pas
    if (s.x < x0-100 || s.x > x1+100 || s.y < y0-100 || s.y > y1+100) continue;
    var R  = ac*1.85 + s.w,                              // demi-longueur des hachures autour de la graine
        an = s.ang,                                      // ⚠ angle tiré par mk() → change à chaque sync
        dx = Math.cos(an), dy = Math.sin(an),            // direction des hachures
        px = -dy, py = dx,                               // direction perpendiculaire (on les empile)
        c  = cOf(s, now),                                // LA couleur de la cellule — jamais en dur
        cl = (s.kind !== 'gray');
    g.strokeStyle = 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';
    g.lineWidth   = cl ? 2 : 1.05;                       // une cellule vide se grave plus fin
    for (var off = -R; off <= R; off += HS){             // une hachure tous les HS
      var ox = s.x + px*off, oy = s.y + py*off, run = false;
      for (var t = -R; t <= R; t += SS){                 // on avance le long de la hachure
        var qx = ox + dx*t, qy = oy + dy*t, bd = 1e18, bi = 0;
        // LE CONTOUR : à qui appartient ce point ? règle pondérée exacte du moteur
        for (var k = 0; k < seeds.length; k++){          // ⚠ toutes les graines, à chaque point : 499 ms
          var _kx = seeds[k].px == null ? seeds[k].x : seeds[k].px,
              _ky = seeds[k].py == null ? seeds[k].y : seeds[k].py,
              ex = qx - _kx, ey = qy - _ky,
              d  = Math.sqrt(ex*ex + ey*ey) - seeds[k].w;
          if (d < bd){ bd = d; bi = k; }
        }
        var ins = (bi === ci) && qx >= x0-2 && qx <= x1+2 && qy >= y0-2 && qy <= y1+2;
        if (ins && !run){ run = true; g.beginPath(); g.moveTo(qx, qy); }   // on entre dans la cellule
        else if (ins){ g.lineTo(qx, qy); }                                 // on y reste
        else if (run){ g.stroke(); run = false; }                          // on en sort : le trait s'arrête au contour
      }
      if (run) g.stroke();
    }
  }
}
```

**Ce que le même monde deviendrait, écrit au contrat** (esquisse, non branchée, non mesurée) :
`HS = u*0.13`, `SS = u*0.08`, `lineWidth = u*0.033` avec `u` lu comme au §5.2 ; `an` tiré du LCG
amorcé par la clé stable (§7.1) ; la graine propriétaire cherchée **parmi les voisines seulement**
(les graines dont la distance à `s` est < 3 u), ce qui ramène le coût de graines² × points à
voisines × points.

---

## 14 · Ce qu'un nouveau monde passe avant d'être livré

```
redteam_decoupe.py      aucune ligne nouvelle (A à F)
redteam_apercus.py      son aperçu de Studio porte de la matière (plancher PAR MONDE à relever)
redteam_dalle_figee.py  sa dalle garde sa couleur et son monde
redteam_toile.py        la Toile se peint, se zoome, se plante
releve-design.py        aucun écart hors de lui
+ le budget du §8.2, mesuré au même banc, ×1 et ×4
+ une capture de sa dalle à k = 0,3 · 1 · 2,5 — RE-GARDÉE : même image à trois tailles
```
