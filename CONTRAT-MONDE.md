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

> **⚑ §1 AMENDÉ — v43 (24 sept. 2026) : LA TRANSITION.** Un monde ne garde toujours rien d'une image à l'autre ;
> c'est **le moteur** qui garde le moment. Quand une dalle arrive (`addP`, `addMember`) ou part (`sync`, monde neuf),
> il pose `_trans = {t0, kind:'arrive'|'depart', x, y, n}` ; le monde le lit par **`env.trans`**, qui ne vaut quelque
> chose **que sur la Toile vivante** (`frame`) — `null` dans une dalle, un export, un aperçu. Un monde qui anime sa
> transition déclare **`RD[monde].transDur`** (ms) : le moteur tourne tant qu'elle court, et **seulement alors** une dalle
> qui part devient une graine `part` (heure du départ, sans `pid` ; `partPid`/`partNuee` gardent sa clé) retirée au bout
> de `PART_DUR` (620 ms). Un monde sans `transDur` garde le comportement d'avant, au pixel. Tout ce qu'un monde tire
> pour sa transition vient de `cleToile` et de `n` — jamais du hasard. Détail : §15.9.

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

## 4 bis · Les rampes de matière — ce qu'une cellule VIDE porte (v30, 23 sept. 2026)

Une cellule sans parole n'a pas de couleur de palette : elle prend un **gris de matière**, tiré d'une rampe
de **cinq tons**. Lu dans le moteur (≈ l. 7785-7793) :

```js
function grays(){ return isLightM() ? GLIGHT : TH[theme].g; }      // clair : GLIGHT, commun à tous les mondes
var TH = {pixel:{g:GPIX}, braille:{g:GBRA}, sillons:{g:GLI}, gravure:{g:GLI}, mosaique:{g:GMOS},
          encre:{g:GENC}, eclats:{g:GMOS}, terrazzo:{g:GENC}, touffe:{g:GENC}};
```

**Les valeurs, mode SOMBRE** (une rampe par famille de mondes) :

```
            ton 0     ton 1     ton 2     ton 3     ton 4
GPIX       #352A1D   #3D3225   #302618   #44392C   #3B2F21     Pixel
GBRA       #281E0E   #302417   #251A08   #35291A   #2D2113     Braille
GLI        #44392B   #4C4134   #3F3325   #52463A   #483D30     Sillons, Gravure
GMOS       #473C2E   #504536   #413526   #564B3D   #4C4132     Mosaïque (et Éclats)
GENC       #221903   #291F0E   #211501   #2E2414   #271C0A     Encre, Terrazzo, Touffe
```

**Mode CLAIR — une seule rampe pour les huit** : `GLIGHT` `#FDEBCD` `#FAF3E5` `#F8E2C2` `#FEEED4` `#FAE6C7`
(des crèmes chaudes, jamais un gris).

**Comment le gris d'une cellule est choisi** : à la création de la graine (`mk()`), un des cinq tons au hasard ;
puis `_shadeG(gris, tone, shade)` le module — `tone` parmi `TON = [1,0 · 0,76 · 1,24 · 0,88 · 1,12]`, `shade`
entre 0,96 et 1,04. En sombre le ton assombrit vers le noir ou éclaire vers le blanc ; en clair il module à peine
et retire surtout du bleu (l'ombre reste chaude). `Toile.setTheme(monde)` **retire tous les gris** dans la rampe du
monde choisi.

**Un monde neuf DÉCLARE sa rampe — c'est obligatoire, et c'est ce qui manque au banc :**

```js
var GESQ=[[…],[…],[…],[…],[…]];      // cinq tons sombres, dans la famille de sa matière
TH.esquille = {g:GESQ};              // ou {g:GENC} pour partager celle d'Encre
```

⚠ **Sans entrée `TH`, le monde n'existe pas pour le moteur** : `setTheme` le refuse (`if(!TH[t]) return;`) et
`Toile.preview` le remplace par Pixel (`if(!TH[th]) th='pixel'`). C'est le « gris plaqué » du banc : l'aperçu
tombe sur la rampe de Pixel, qui n'est pas la sienne.
**Pour Esquille, proche d'Encre** : partir de `GENC`. Ses cinq tons sont les plus sombres du jeu (L* 7,8 à 14,9, mesuré) :
des fragments posés sur un fond presque noir. Si Esquille a des éclats plus clairs qu'Encre, une rampe à elle se
dérive de `GENC` en gardant sa TEINTE (brun chaud) — **jamais un gris neutre** (CLAUDE.md §3).

## 4 ter · Le fond de la Toile — ce qui paraît ENTRE les fragments (v30)

**Le fond n'appartient à aucun monde : c'est le moteur qui le peint, avant d'appeler le monde.** Un monde ne le
peint jamais, et n'a aucun moyen de le changer aujourd'hui. Il est défini à **quatre** endroits, qui ne disent
pas tous la même chose (lu le 23 sept.) :

```
chemin                         clair                           sombre
frame()      la Toile d'accueil dégradé #E6D1AE → #D8C29A        dégradé #221702 → #150D00      ≈ l. 8103
renderTo()   « Ma Toile »       #EFE2C5                          #201908                        ≈ l. 8396
Toile.fondToile() · repaint     #F1ECD9 (#DDD2B8 tout coloré)     #201908                        ≈ l. 8433
Toile.preview()                 #F1ECD9 (#DDD2B8 tout coloré)     #201908                        ≈ l. 8719
dalleTrame()                    — transparent : une dalle n'a pas de fond, elle se pose sur son champ
```

**Ce que ça veut dire pour un monde à fragments** (Encre, Terrazzo, Touffe, Esquille) : entre ses fragments, on
voit ce fond — le dégradé brun sur l'accueil, le brun `#201908` au partage et dans les aperçus. Les cellules
VIDES aussi portent des fragments (dans leur gris de rampe) : c'est leur recouvrement qui fait la matière. Un
monde qui couvre peu (Touffe couvre ~11 % de sa cellule) laisse voir beaucoup de fond.
⚠ **Les quatre chemins divergent** (le dégradé de l'accueil n'est ni `#201908` ni `#EFE2C5`). Un monde neuf
ne peut donc pas se régler sur « le » fond : il sera jugé sur les quatre. **Donner à un monde son propre fond**
demanderait une entrée `TH[monde].fond = {clair, sombre}` lue par ces quatre chemins — une modification du moteur,
**non faite**, à demander si un monde neuf en a besoin.

## 5 · L'échelle — la même dalle à 40 px sur une carte et à 200 px sur une fiche

### 5.1 · Ce que le moteur fournit (v29, 23 sept. 2026 — feu vert de Tom)

`Toile.dalleTrame(cv, pid, k, monde, opts)` : le facteur **`k` agrandit la GÉOMÉTRIE** — positions des
graines, poids, marge — **et, depuis v29, l'unité des mondes : `UK = k` pendant le rendu.** Le canevas
sort à `≈ (boîte × k + 2·marge) × DPR` pixels.

**L'appelant ne calcule plus `k` lui-même.** Un seul poseur, dans l'app :

```js
window._poseDalle(g, id, x, y, w, h, o)   // rend la dalle À LA TAILLE de la boîte (contain, centrée),
                                          // en pixels de l'appareil, puis la pose 1:1 — rotation gardée
window._rendDalle(id, largeurPx, hauteurPx, o)   // seulement le rendu, à poser avec _poseUn
window._poseUn(g, cv, cx, cy)                    // pose un canevas 1:1, centré, au pixel entier
// o = {monde, rampe:{cols,haut}, decale:{a,b}, donnees:true, haut:'bas'}
```

Il ajuste `k` jusqu'à ce que la dalle tienne dans la boîte à 3 % près — **jamais un agrandissement
après coup**. `redteam_decoupe` le vérifie à chaque passage.

### 5.2 · Ce que le MONDE doit faire — l'unité `UK`

> **Un monde écrit TOUTE longueur — pas de trame, rayon de point, épaisseur de trait, amplitude
> d'ondulation, taille d'éclat — comme « valeur de référence × `UK` ».** La valeur de référence est
> celle de la Toile de l'accueil (`UK = 1`). À `k = 0,3` ou `k = 2,5`, la dalle est alors la MÊME
> image à deux tailles.

C'est ce qui a été fait aux cinq mondes à trame : Pixel `5×UK` · Mosaïque `11×UK` (joint `UK`) ·
Braille `9×UK`, rayons `2×UK` / `2,9×UK` · Sillons `6×UK`, amplitude `4,5×UK`, longueur d'onde
`0,018/UK`, traits `×UK` · Gravure `8×UK`, `5×UK`, traits `×UK`. **À `UK = 1` le rendu de la Toile ne
bouge pas d'un pixel.** L'alignement de la trame sur la Toile (`PER`) suit `k` lui aussi.

Les trois mondes libres (Encre, Terrazzo, Touffe) mesurent déjà tout en `sp`, l'écart des graines, que
`dalleTrame` met à l'échelle : ils n'ont pas eu à changer.

⚠ **Ne pas prendre `avg()` comme unité dans un monde contenu** : dans `dalleTrame`, `W×H` y vaut la
boîte de LA cellule, et `avg()` n'y vaut plus l'écart de la Toile (lu dans le code). `UK` est fait pour ça.

### 5.2 bis · Ce que le moteur peint à la place des appelants — `opts`

Ce que des appelants faisaient APRÈS le moteur, sur les pixels, le moteur le peint lui-même :

```
opts.rampe  = {cols:[[r,g,b]…], haut}  la clarté normalisée remappée sur une rampe
                                       — Q30 (bande haute, haut 2) et Q297 (Ingénu, haut 0,9 ou choisie)
opts.decale = {a, b}                   la teinte déplacée en Lab, clarté gardée — chantier 59 (Pelote)
opts.donnees = true                    le moteur rend aussi SES pixels : `cv.__dalleDonnees`
```

Et **le moteur déclare ce qu'il a peint**, sur le canevas : `cv.__dalleInfo = {sat, satS, lum, lab,
plein}` — la couleur la plus saturée, la clarté moyenne, le Lab moyen, la part pleine. Les appelants qui
relisaient les pixels pour cela (`_teinteDalle`, `_lumDalle`, la Pelote) lisent cette déclaration (§7 de
CLAUDE.md : on lit la composition publiée).

⚠ **La Pelote reçoit les pixels du moteur (`donnees`) pour tisser sa fourrure** : chaque île est une
texture projetée sur une sphère, pas une image posée. C'est la seule chose qui sort encore des pixels
d'une dalle, et elle sort DU MOTEUR.

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

⚑ **v30 (Tom, 23 sept.) — LA RÈGLE EST DANS LE MOTEUR.** Sans monde fourni, `dalleTrame` cherche le Promi et prend
**son** monde. Seuls les écrans qui montrent le monde courant EXPRÈS le passent et le déclarent (`opts.courant`) :
la page + (la dalle qu'on va planter), les aperçus et le curseur du Studio. Le monde employé est publié
(`__dalleInfo.monde`) et `redteam_decoupe` le vérifie (famille **H**), avec un monde courant volontairement
différent de celui de la plantation. Prouvé : la règle retirée, **434 dalles, 6 lignes** prises.
*Ce que ce paragraphe disait avant v30 :* **sur 29 appels à `dalleTrame`, 6 seulement
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

### 8.2 · Après v29 — ce que coûte une dalle À SA TAILLE FINALE (mesuré le 23 sept.)

Même banc. Une dalle de **200 px d'affichage** (400 px d'appareil), médiane sur les 18 dalles du jeu :

```
                 AVANT v29 (k = 1, puis agrandie)      APRÈS v29 (rendue à 200 px, posée 1:1)
                   ×1         ×4                          ×1         ×4
  Encre            4,9       22,1                        25,8      113,7
  Terrazzo         5,7       22,4                        25,4      121,9
  Touffe          15,3       61,7                        32,9      156,8
  Gravure         39,2      161,3                        20,3       94,7
  Sillons         57,3      225,4                        25,3      119,9
  Braille         73,9      226,2                        30,6      115,1
  Mosaïque       142,4      547,2                        39,0      203,2
  Pixel          201,2      740,4                        48,0      225,3
```

**Rendre à la taille finale a d'abord coûté cher** — 1,9 s pour une dalle Pixel de 200 px, mesuré au
premier jet — parce que `dalleTrame` cherchait la graine propriétaire de chaque pixel parmi TOUTES les
graines. Deux corrections dans `dalleTrame`, exactes au pixel près (inégalité triangulaire) : ① ne passer
au monde et au masque que les graines qui PEUVENT posséder un point du canevas ; ② ranger ces graines,
et pour chaque pixel s'arrêter à la première qui ne peut plus gagner. Et le Lab moyen n'est calculé que
pour qui le demande (la Pelote). **Résultat : les mondes à trame coûtent 3 à 4 fois MOINS qu'avant v29 ;
les trois mondes libres coûtent 2 à 5 fois PLUS** (ils n'avaient pas de masque ; ce qui reste, c'est le
nombre de pixels d'une grande dalle).

### 8.3 · Le budget — v30 : LA GRAINE PROPRIÉTAIRE PARMI LES VOISINES, DANS LES CINQ MONDES QUI LA CHERCHENT

Cinq mondes cherchaient, pour chaque échantillon, la graine propriétaire parmi TOUTES les graines : **Pixel,
Braille, Mosaïque, Gravure, et Sillons** (par `cAt`). Encre, Terrazzo et Touffe ne cherchent rien : ils parcourent les
graines une fois pour les dessiner. Un index spatial (`_grilleProp`, grille de pas `avg()`, anneaux de cases, arrêt
dès qu'aucune case restante ne peut faire mieux) les remplace — **exact : 0 graine différente sur 300 000 points
tirés, seconde graine comprise** (Braille s'en sert pour ses bords). La matière ne change pas.

```
la Toile entière (renderTo, 390×844, DPR 2) — médiane de 5
              ×1 avant   ×1 v30     ×4 avant   ×4 v30
  Encre          5,3       3,4        20,2      16,7
  Terrazzo       4,2       4,0        20,7      18,4
  Touffe        13,7       9,0        51,0      46,9
  Mosaïque      21,4       5,0        68,1      23,7
  Braille       29,1       5,7       102,2      27,8
  Sillons       48,9       7,6       183,0      37,5
  Pixel         72,0      14,2       292,2      77,0
  Gravure      499,1      26,2     1 943,5     119,8
```

⚠ **v31 — ces chiffres ne comptaient que le CALCUL** (le canevas exécute ses ordres plus tard). Les chiffres
au DESSIN FORCÉ et à l'écran sont au §12 ter, Q5 : ils les remplacent.

**Verdict (Q309, au calcul seul — voir §12 ter) :**
- **À ×1, sept mondes sur huit tiennent 16,7 ms** ; Gravure est à 26 ms (440 → 26).
- **À ×4 (« mobile moyen »), six tiennent 50 ms** ; **Pixel (77 ms) et Gravure (120 ms) dépassent encore.** Pour Gravure,
  le reste du coût est le tracé : chaque graine balaie ses hachures sur un rayon de 1,85 × l'écart moyen, et la
  plupart des points tombent hors de sa cellule. Pour Pixel, c'est le nombre de carrés (un tous les 5 px d'écran).
  **Tenable sur un téléphone récent, limite sur l'iPhone 12** — aucune mesure sur appareil.
- **Une dalle de 200 px : 18 à 45 ms à ×1, 82 à 215 ms à ×4.**

**Le budget d'un NOUVEAU monde** : Toile ≤ 16,7 ms à ×1 et ≤ 50 ms à ×4 ; une dalle de 200 px ≤ 50 ms à ×1.
**Un monde qui cherche une graine propriétaire appelle `_grilleProp()` une fois par passe** et interroge
`G.prop(x, y)` → `{bi, bd, bd2}` ; il ne parcourt jamais `seeds` pour chaque point.

### 8.4 · v38 (24 sept. 2026) — LES TROIS PIRES SOUS 16,7 ms AU DESSIN

Méthode du §12 ter (10 canevas distincts, dessin forcé), même passe, `_perfAncien` = l'ancien chemin dans la même page.
Outils : `sauvegardes/perf-v38/` (`banc.py`, `plante.py` = images réelles pendant une plantation, `preuve_rendu.py`).
```
                    dessin ×1        dessin ×4         WebKit dessin     plantation, médiane/image (×1 · ×4 · WebKit)
  Touffe          61,5 →  7,9     300  → 36,5       61,8 →  7,7       83 → 16,7 · 483 → 50  · 203 → 17
  Taille-douce    40,7 → 15,5     186  → 70,9       34,0 →  5,5       17 → 16,7 · 217 → 67  ·  31 → 17   (p90 50 → 16,7)
  Madrure         36,9 →  7,5     156  → 23,8       29,0 → 10,9       33 → 16,7 · 100 → 33  ·  21 → 17
```
**Ce qui coûtait, et ce qui a été fait :**
- **Le coin arrondi de la Toile vivante était un `clip()`** (boucle `frame`, tous les mondes). WebKit le faisait payer à
  CHAQUE tracé : Touffe 205 → 51 ms par image à l'écran, Gravure 56 → 33. Remplacé par la matière sans découpage, puis le
  fond (même dégradé) peint autour du rectangle arrondi, en pair-impair.
- **Touffe — les traits d'encre (34 ms) et les aplats (15 ms) de ~1 500 pétales.** Chaque graine peint ses fleurs une fois
  dans un calque à sa taille finale (`_toufGraine` = le corps d'origine), fraction de pixel intégrée, posé 1:1 sur une cote
  entière. Refait si couleur, pas, encre ou densité changent ; en mouvement il se pose à la cote entière la plus proche
  (≤ ½ px d'appareil) et se refait dès qu'il est posé. Chemin direct pour les dalles, les aperçus, l'export (DPR > 3).
- **Gravure — une requête de graine propriétaire par point de hachure (27 ms de calcul).** Le propriétaire du point
  précédent, comparé par la même formule et la même règle d'égalité que `prop`, écarte le point sans requête : **décision
  identique, 0 pixel différent** (27,7 → 7 ms). Et une hachure est une droite : premier et dernier point au lieu de la
  polyligne alignée (20 → 15,5 ms).
- **Madrure — trois remplissages pair-impair de toute l'onde, et ~20 yeux découpés (clip + 4 remplissages) à chaque image.**
  L'onde se peint une fois par construction dans un calque de la taille du canevas (même transformation) ; chaque œil dans
  le sien (`_madCalque`, `_calque` désigné à `_sync`). Posés 1:1.

**Preuve que la matière ne change pas** (`preuve_rendu.py` : renderTo, horloge figée, même page, 3 semis × 2 thèmes ;
témoin ancien/ancien = 0 pixel, second rendu/premier = 0 pixel) :
```
  Gravure (propriétaire)     0 pixel différent
  Madrure (calques)          ≤ 0,002 % des pixels, écart max 3 niveaux, ΔE max 2,0
  Touffe  (calques)          0,13–0,19 % à > 2 niveaux, ΔE moyen 0,03, 99,9 % sous ΔE 2 ; quelques pixels jusqu'à 97
                             niveaux sur des bords de tracés coupés par le bord du canevas (Skia les rastérise autrement)
  Coin arrondi               0,4 % à > 2 niveaux, ΔE moyen 0,03 : l'anticrénelage d'un tracé sous clip diffère un peu
  Gravure (droites)          1,5–5 % des pixels à > 2 niveaux, ΔE moyen 0,1–0,2, max ΔE 20 — SUR LA FRANGE
                             d'anticrénelage le long des hachures ; même géométrie, indiscernable à ×12
```
Aucun changement d'aspect vu à l'œil (accueil dézoomé, trois mondes × deux thèmes, ancien/nouveau côte à côte).
⚠ **La colonne « écran » du banc reste à 17–33 ms** : son forçage (`refigeCouleurs` à chaque image) coûte à lui seul
~10 ms. La mesure juste de l'écran est `plante.py`. ⚠ **La construction de Madrure n'a pas bougé** (69 ms ×1, 263 ×4,
par tranches) : c'est du calcul (le champ et ses lignes de niveau), pas du rendu.
⚠ **Un calque est une IMAGE du monde, peinte par lui, à sa taille, posée 1:1** — jamais redimensionnée ni découpée ;
`redteam_decoupe --monde=` : 0 prise sur les trois.

### 8.5 · v39 (24 sept. 2026) — LES SIX AUTRES MONDES

Mesurés d'abord, après v38 : **le coin arrondi en avait déjà réglé la plupart en WebKit** (plantation, médiane par image :
Braille 180 → 17 ms, Houle 53 → 16, Buvard 18 → 17 (p90 64 → 18), Pochade 18 → 17 (p90 57 → 18), Éclisse 18 → 17).
Au dessin forcé (Chromium ×1), quatre tenaient déjà : **Bobinette 12,9 · Braille 13,9 · Pochade 13,9 · Éclisse 7,5**.
Deux non, traités :
```
                dessin ×1      dessin ×4      WebKit dessin    plantation ×1 (méd · p90)    ×4          WebKit
  Buvard      19,1 → 10,8    86 → 45,7        12,3 → 10,9     16,7·16,8 → 16,7·16,7   100 → 50    63 → 17
  Houle       24,0 →  8,2   108 → 35,2        11,2 →  6,3     16,7·33,3 → 16,7·33,3   133 → 133   58 → 17
```
- **Buvard** fusionne les carrés voisins de même couleur d'une rangée en un rectangle (opaques, sur la grille) : **0 pixel
  différent**.
- **Houle** : ses ondes sont fixes, seules leurs couleurs dépendent du semis. On calcule à chaque image la suite des
  morceaux et sa signature ; inchangée → le calque est reposé 1:1, sinon repeint avec les mêmes tracés dans le même ordre.
  Écart max 2 niveaux (ΔE ≤ 1,7). ⚠ **Pendant une plantation en Chromium, Houle ne gagne rien** : les couleurs changent à
  chaque image, le calque se refait. Son plancher en mouvement est le tracé de ~9 000 segments fins (~16 ms) + le calcul
  (~7) : un dixième des images à 33 ms à ×1, 133 ms à ×4. Regrouper les tracés par couleur n'a rien gagné (le coût est
  par sommet, pas par appel) et changeait les jonctions ; les jonctions en onglet ou biseau ne gagnent rien non plus.
  En WebKit, Houle tient (17 / 20 ms).

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
G · affichage      un canevas de dalle AFFICHÉ par le CSS à une autre taille que celle où il est peint
                   (ajoutée en v29 : c'est la même faute, faite par le navigateur)
```

Il passe **à chaque lot qui touche une dalle**, et il échoue sur toute ligne **nouvelle**.

---

## 10 · La dette — SOLDÉE en v29 (23 sept. 2026)

Au premier passage (22 sept.), le contrôle avait pris l'app en faute à **24 lignes, ~2 100 appels**.
Tom a donné le feu vert aux deux ajouts au moteur ; **`decoupe-dette.json` est vide.** Ce qui a été fait :

| famille | ce que c'était | ce qui le remplace |
|---|---|---|
| B · redimension (13 lignes) | dalles rendues à `k = 1` puis agrandies ou réduites | `_poseDalle` / `_rendDalle` : rendue à la taille finale, posée 1:1 |
| C · pixels (9 lignes) | `_teinteDalle`, Q30, Q297, `_lumDalle`, la Pelote | `opts.rampe`, `opts.decale`, `__dalleInfo`, `__dalleDonnees` — peints ou déclarés par le moteur |
| A · découpe (1) | la trame de la page + | rendue à sa taille, posée 1:1, rotation gardée |
| D · fragment (1) | l'export « Ma Toile » réduit | `renderTo` à l'échelle exacte du cadrage, posée 1:1 |
| F · photo (1) | `promiTrame` posait l'image webp du monde | la vraie dalle d'un Promi ; **les huit images `PROMI_DALLES` sont retirées du fichier (411 Ko)** |

**La famille G, ajoutée en v29, a trouvé deux affichages redimensionnés par le CSS** — les dalles de
« Ce que tu as tenu » et de « Tenu ensemble » (×1,07), et l'aperçu de Partager « Ma Toile » (×0,86) :
rendues désormais à la taille de leur boîte, affichées 1:1.

**Et neuf appelants que le contrôle n'avait pas vus passer** (écrans non ouverts par ses 19 parcours)
ont été corrigés de la même façon : la bande de la fiche (`_ficheDalle`), la bande mauve d'une Nuée,
l'ancienne fiche de Promi, la tuile de Nuée, le bandeau des Réglages, la dalle qui naît et la grappe de
la page +, la silhouette du Studio. **Le contrôle ne voit que ce qu'il parcourt** : un écran neuf
s'ajoute à sa liste `ECRANS`.

## 11 · Les huit mondes suivent-ils le même contrat ? — Non. Les dérives, lues dans le code

| | Encre | Touffe | Mosaïque | Braille | Pixel | Terrazzo | Gravure | Sillons |
|---|---|---|---|---|---|---|---|---|
| **couleur par `cOf` seul** | ✓ | ✓ ¹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **n'appelle pas `setTransform`** | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ |
| **suit le zoom (`view`)** | ✓ (à la main) | ✗ ² | ✓ (à la main) | ✓ | ✓ (à la main) | ✗ ² | ✓ | ✓ |
| **longueurs en unité (`UK` / `sp`)** | ✓ | ✓ | ✓ v29 | ✓ v29 | ✓ v29 | ✓ | ✓ v29 | ✓ v29 |
| **contenu dans sa cellule** | libre | libre | contenu | contenu | contenu | libre | contenu | contenu |
| **déterministe au repos** | ✗ index | ✗ index | ✓ | ✓ | ✓ | ✗ index | ✗ `s.ang` | ✓ |
| **Toile ≤ 16,7 ms à ×1** (v30) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ 26 ms | ✓ |

¹ **Corrigé en v29.** Touffe peignait le cœur de ses fleurs en `[221,77,35]` — `#DD4D23`, la couleur
« à tenir » — et celui d'une cellule vide dans un gris neutre. Le cœur est désormais la couleur de SA
cellule (`cOf`) poussée de 45 % vers l'encre du contour : une nuance, rien d'inventé. Le contour garde
l'encre du thème (`_tfInk`), qui est l'encre du produit, pas un état.
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
  TH            sa rampe de gris en sombre ({g: GXXX}) — OBLIGATOIRE : sans elle setTheme refuse le
                monde et l'aperçu tombe sur Pixel (§4 bis)                ≈ l. 7789
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

## 12 bis · Le renommage des mondes — le terrain (relevé le 23 sept., v30)

Le renommage est décidé ; la correspondance viendra avec les quatre mondes neufs. **Ce qu'il faudra toucher :**

```
dans app.html — le CODE (clés de monde : 'encre', encre:, .encre, [encre])     175 occurrences, 60 lignes
   dont 12 REGISTRES qui nomment ≥ 5 mondes d'un coup                        l. 3190, 6752, 7689, 7785,
                                                                             7978, 8103, 8851, 9423,
                                                                             27417, 31502, 31513, 31570
   dont 9 lignes dans le moteur                                               l. 7785, 7789, 7879, 7978,
                                                                             8061, 8103, 8449, 8549, 8556
dans app.html — les LIBELLÉS affichés (« Encre », « Mosaïque »…)              33 occurrences, 12 lignes
   (la carte du Studio l. 2874-2882, le nom → clé l. 3190, le rail l. 6752, l'onboarding l. 8851, l. 31962)
hors d'app.html — juges, documents, jetons                                    1 039 occurrences, 44 fichiers
   juges qui portent un nom de monde EN DUR : redteam_apercus, redteam_dalle_figee, redteam_decoupe,
   redteam_tokens, releve-S5-instant, releve-aura
```

(Les lignes sont celles du 23 sept. ; « encre » et « pixel » servent aussi à parler d'encre et de pixels —
seules les formes de NOM de monde sont comptées.)

⚠ **ET LES DONNÉES DÉJÀ ÉCRITES — ce qu'aucune recherche dans le code ne voit.** Chaque Promi porte
`monde = {m:'encre', …}`, sauvegardé dans `promi_state` ; le monde choisi est dans `promi_monde`. Renommer les clés
sans MIGRER ces valeurs, c'est ce qui se passerait : `dalleTrame` ne trouve pas `RD[monde.m]` → la dalle se peint
dans le monde courant, **en silence** — exactement la faute que la famille H prend désormais. **Le renommage se fait
donc avec une table ancien → nouveau, appliquée au chargement** (`loadState`, `promi_monde`), et la table reste
dans le code tant qu'une sauvegarde ancienne peut exister.
**Recommandation : renommer les LIBELLÉS, garder les CLÉS** — 33 occurrences sur 12 lignes au lieu de 175 sur 60,
et aucune donnée à migrer. Les clés ne se voient nulle part ; c'est à Tom de trancher.

## 12 ter · Réponses au banc des mondes neufs (23 sept. 2026, v31)

### Q1 · Les bords de cellule ondulent-ils ? — NON. Droits ou très légèrement courbes, jamais ondulés.

La frontière entre deux cellules est l'ensemble des points où `|p−a| − w_a = |p−b| − w_b` (§3). **Mesuré sur la
vraie Toile** (71 cellules, 20 colorées ; bords relevés au pixel, écart maximal de chaque arête à sa corde) :

```
arêtes entre deux poids ÉGAUX (91)      flèche médiane 0,56 px · max 0,94 px   → des DROITES (l'écart est le pixel)
arêtes entre poids DIFFÉRENTS (43)      flèche médiane 0,83 px · max 4,27 px   → des arcs d'HYPERBOLE, convexes,
                                        sur des arêtes de ~51 px                  sans inflexion, jamais une onde
poids en jeu : cellule vide 0 · Promi planté 3,4 · Nuée 14 ; écart moyen entre graines 68 px
```

**Ce qui bouge, et qui n'est pas une ondulation** : pendant le frémissement (850 ms après une plantation ou un
changement de monde, §7.1) les graines se déplacent (`px`, `py`) — les arêtes se déplacent avec, elles restent droites
ou hyperboliques. Et **Encre, Terrazzo, Touffe ne dessinent aucun bord** : leurs formes débordent la cellule (§3, mondes
libres) ; ce qu'on voit comme « bord » y est le contour de leurs taches, pas celui de la cellule.
**Pour Ritournelle** : le moteur ne donnera pas de flaques ondulées. Un monde qui veut un bord qui ondule le dessine
**DANS** sa cellule (une matière qui s'arrête en deçà de la frontière, sur une ligne ondulée à lui) — jamais en
déplaçant la frontière : la dalle d'une fiche est découpée **au pixel** sur la frontière pondérée (`dalleTrame`), un
bord qui la franchirait serait visible sur la Toile et coupé net sur la dalle. S'il doit franchir la frontière, il est
**libre** (liste `LIBRE`, §3) et renonce au découpage pondéré.

### Q2 · `curPAL()` — oui, dans la fermeture du moteur (≈ l. 7751)

```js
function curPAL(){ var base=PALS[palKey].cols;
  return hueShift ? base.map(function(c){ return rotc(c,hueShift); }) : base; }
// → [[r,g,b],[r,g,b],[r,g,b],[r,g,b]]  — QUATRE tons, entiers 0-255, dans l'ordre de la palette (C1 → C4)
```

- **Lecture seule** : sans teinte (`hueShift = 0`) c'est **le tableau même de `PALS`** qui est rendu — le modifier
  corromprait la palette pour tout le produit. Copier avant de transformer.
- **Il suit le monde de l'appel** : `dalleTrame(…, monde)` remplace `palKey`/`hueShift` le temps du rendu (§6), donc
  une dalle plantée sous une autre palette lit SES quatre tons. À appeler **pendant** le rendu, jamais à garder.
- Voisins : `PALL()` = les mêmes quatre tons × cinq clartés (`LITS`), ce que `cOf` emploie ; hors du moteur
  `Toile.cols()` rend `curPAL()` et `Toile.tonsDe(clé, teinte)` les quatre tons de n'importe quelle palette.
- Sous **Ingénu** (palette par défaut), les quatre tons sont bleu `#82AEF8` · rose `#FFB8D2` · lilas `#C9A8F5` ·
  crème dalle `#EFE3C7` — c'est-à-dire, pour les trois premiers, **les couleurs des natures**.

### Q3 · La rampe du §10 — FAITE en v29, et ce qu'elle est exactement

C'est le 5ᵉ argument de `dalleTrame` : `opts.rampe = {cols:[[r,g,b]…], haut}` (§5.2 bis). **N tons, pas quatre** : trois
pour Q30 (`DALPAL`), trois ou **quatre** pour Q297 (la rampe du Chiche a quatre points : prune → rose froid → rose →
clarté). Le moteur l'applique **après** le monde, en remappant la clarté de chaque pixel de la DALLE sur la rampe.
⚠ **Elle ne vaut que pour une dalle** (fiche, page +, cartes, îles de la Pelote) — **jamais sur la Toile** : un monde
n'en reçoit rien et n'a rien à en faire. Si Ritournelle ou Madrure « en dépendent » au sens d'une rampe à eux, c'est
autre chose : c'est la rampe de matière (§4 bis, `TH[monde].g`, cinq tons) ou leurs propres nuances de `cOf`.

**⚑ L'EXCEPTION DE MADRURE — écrite par Tom, 23 sept. 2026.** Madrure lit **trois tons de palette en brut**
(`curPAL()[0..2]`), pas `cOf` : son onde traverse toute la Toile, et **les promesses la découpent sans la colorer**.
Ce que l'exception veut dire, et ce qu'elle ne dit pas :
- **permis à Madrure seul** — tout autre monde reste soumis au §4.1 (`cOf` ou une nuance de `cOf`) ;
- les tons bruts **ignorent** le code libre du Cercle, le ton choisi, la nature sous Ingénu : c'est voulu, la couleur
  de l'onde n'est pas celle d'une parole ;
- ⚠ **sous Ingénu, les trois premiers tons SONT les couleurs des trois natures** — l'onde portera donc du bleu, du rose
  et du lilas sur toute la Toile, là où les dalles disent leur nature. **À regarder à l'écran avant de livrer.**
- toujours interdit : une couleur d'état (§4.4), un gris neutre.

### Q4 · Une clé de Toile — EXPOSÉE en v31 : `Toile.cle()`

Aucune clé stable n'existait : le semis est tiré au hasard à chaque chargement et refait à chaque plantation (§7.2).
**`window.Toile.cle()`** → un entier 32 bits non signé ; **`Toile.cleUnite()`** → le même dans [0, 1).
Tiré de la graine de l'utilisateur **sauvegardée** (`promi_graine`), hachée avec un sel à elle. Mesuré : même valeur
après rechargement, et après une plantation suivie d'un `Toile.sync` (3 294 933 574 dans les deux cas).
Pour l'angle de Madrure : `var an = Toile.cleUnite() * Math.PI;` — le même sur l'accueil, au partage, au Studio et
dans chaque dalle. ⚠ Une remise à zéro des données (`promi_graine` effacé) donne une nouvelle Toile, donc une
nouvelle clé : c'est juste.

### Q5 (Tom) · Le banc comptait-il le dessin ? — NON. Les budgets du §8 étaient sous-évalués.

`Toile.renderTo()` chronométré seul mesure le **calcul et l'enregistrement** des ordres de dessin : le canevas les
exécute plus tard. En **forçant le dessin** (une relecture d'un pixel juste après, qui oblige le canevas à tout
peindre), et en lisant **l'intervalle réel entre deux images à l'écran** pendant que la Toile vivante se repeint :

```
Toile entière, 390×844, DPR 2 — médiane de 5 (ms)
              calcul seul    dessin forcé    image à l'écran    |  ×4 : calcul · dessin · écran
  Encre           4,1           14,6             16,7            |       16 ·   67 ·  117
  Terrazzo        3,9            7,0             16,7            |       17 ·   35 ·   67
  Mosaïque        5,2            7,0             16,7            |       25 ·   36 ·   50
  Braille         6,0           13,4             33,3            |       28 ·   66 ·  100
  Pixel          14,1           21,0             33,3            |       42 ·   84 ·  100
  Sillons         8,3           26,2             33,4            |       38 ·  121 ·  133
  Gravure        27,9           39,0             50,1            |      121 ·  185 ·  217
  Touffe         10,0           61,7             83,3            |       50 ·  302 ·  383
```

**Ce que ça change :**
- **Gravure n'est pas à 26 ms mais à 39 ms de dessin, 50 ms par image à l'écran** (20 images/s). La correction des
  voisines reste vraie (440 → 28 ms de calcul), mais le DESSIN de ses hachures est maintenant la part dominante.
- **Touffe est le monde le plus cher à l'écran** — 62 ms de dessin pour 10 de calcul : six fois. Ses pétales sont des
  courbes remplies et tracées en transparence, et c'est le rendu, pas la logique, qui coûte.
- **À ×1, seuls Encre, Terrazzo et Mosaïque tiennent une image (16,7 ms) à l'écran.** Braille, Pixel, Sillons tiennent
  30 images/s ; Gravure 20 ; Touffe 12.
- ⚠ L'image à l'écran est quantifiée par l'affichage (16,7 · 33,3 · 50…) et porte aussi le reste de la page ; le
  ralentissement ×4 ne bride que le fil principal, pas forcément le dessin. Ni l'un ni l'autre n'est un téléphone.
- **Les dalles (§8.2) étaient, elles, bien comptées** : `dalleTrame` relit ses propres pixels (masque, recadrage),
  ce qui force le dessin avant de rendre la main.

### Q5 bis · La relecture d'un pixel fausse-t-elle la mesure ? — Non, VÉRIFIÉ (23 sept., soir)

Le banc des mondes neufs trouvait 14,9 ms pour une relecture seule. Ici : **0,0 ms** sur un canevas neuf de la taille
de la Toile (un seul petit ordre en attente). Ce que la relecture coûte, c'est le dessin qu'elle déclenche — l'objet
même de la mesure. Trois mesures concordent (Mac, ×1) : 10 canevas distincts, une relecture chacun · l'ancien banc
(une relecture par passe, canevas neuf) · **l'écran, sans aucune relecture** — Touffe 63 · 67 · 90 ms par image.
⚠ **Un amorti dans UN SEUL canevas ment en sens inverse** : `renderTo` efface toute la surface à chaque passe, et le
navigateur jette les ordres recouverts avant de les peindre — Touffe y sortait à 12,6 ms (un dessin sur dix exécuté).
Moyennes à l'écran : Mosaïque 16,7 · Terrazzo 18 · Encre 21 · Pixel 27 · Braille 29 · Sillons 36 · Gravure 55 · Touffe 90 —
**seule Mosaïque tient 60 images par seconde en continu.**

**Le budget d'un monde neuf se mesure donc au DESSIN, jamais au calcul seul** — sur N canevas DISTINCTS, une relecture
chacun, et à l'écran à côté — : `renderTo(c, 2)` puis
`c.getContext('2d').getImageData(0,0,1,1)`, dans le même chronomètre — et l'image à l'écran à côté.

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
        // ⚑ v30 — dans le moteur, ces six lignes sont devenues  bi = _G.prop(qx, qy).bi  (l'index spatial,
        //   construit une fois en tête du monde : var _G = _grilleProp();) — même graine, 440 → 26 ms.
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
redteam_decoupe.py      aucune ligne nouvelle (A à H — dessin, affichage, monde de plantation)
redteam_apercus.py      son aperçu de Studio porte de la matière (plancher PAR MONDE à relever)
redteam_dalle_figee.py  sa dalle garde sa couleur et son monde
redteam_toile.py        la Toile se peint, se zoome, se plante
releve-design.py        aucun écart hors de lui
+ le budget du §8.2, mesuré au même banc, ×1 et ×4
+ une capture de sa dalle à k = 0,3 · 1 · 2,5 — RE-GARDÉE : même image à trois tailles
```

---

## 15 · Les quatre mondes neufs — intégrés en v32 (23 sept. 2026)

**Esquille · Bobinette · Ritournelle · Madrure**, reçus dans `promi-mondes.js` (chat des mondes). Le bloc
`lot-V32-MONDES` de l'app est ce fichier, **à cinq retouches près** ; la version exacte qui tourne est
`promi-mondes-integre-v32.js` (à renvoyer au chat des mondes, c'est désormais la référence).

### 15.1 · Comment ils sont branchés
- **Fabrique gardée**, pas de collage dans l'IIFE : le moteur appelle `creerMondes(env)` avec un environnement à
  **accesseurs** (`get g(){return g;}`…) — `g, W, H, DPR, seeds, view` sont relus à chaque appel, donc les mondes suivent
  les échanges de globales des cinq chemins (§1). Rien n'est gardé côté monde.
- `RD.esquille/bobinette/ritournelle/madrure` ; `TH` : Esquille et Madrure `GENC`, Bobinette `GLI`, Ritournelle `GMOS`.
- `cOf(s, now || performance.now())` — **`cOf(s, 0)` rend le GRIS de départ** d'une dalle colorée (l'animation part de
  `t0`) ; le carnet des mondes l'appelait à 0 et aurait figé des dalles grises.
- `_dalleDeCle(pid)` : l'app avait `_dalleDeCle(p) → {ci, lit}` ; l'environnement rend l'entier FNV de `titre|personne`
  (la même clé stable, jamais l'id).
- `rampe` : **aucune** — la rampe v29 ne vaut que pour une dalle (§12 ter Q3) ; les mondes tournent la palette.
- `cleToile` : `Toile.cle()` · `fondToile()` : `Toile.fondToile()` (un seul propriétaire, v26).
- **Dalle seule** (Esquille, Bobinette, Madrure) : `dalleTrame` appelle `_dalleNeuve` → `seule()` sur la Toile même
  (graines et W×H vrais, seul le contexte change), canevas = `boite()` × k + ½ px × k. Aucune image lue, aucune découpe.
  Ritournelle, contenue, garde le chemin commun (masque pondéré) et **ne peint que la coulée de la dalle** (`env.cible`).
- **Toucher** : `Toile.hit` demande d'abord `toucher()` (la dalle PEINTE), puis retombe sur la règle de la cellule.
- Exposé : `Toile.natureDalle(pid)` ('oeil' · 'fermee' · 'cercle' pour Madrure), `Toile.contourDalle(pid)`,
  `Toile._madrure()` (constructions, dernière durée ; `_madrure(true)` vide le cache).
- Studio : `STRUCT` (nom seul), `WL`, `order` (au bout du rail), `_map`. Gratuits (Q314).

### 15.2 · Les cinq retouches au fichier reçu, et pourquoi
1. **Position de repos pour la géométrie gardée** (`_repos`) : `_idx` lisait `px/py` (le frémissement) alors que la
   signature du cache lit `x/y` — l'onde de Madrure se bâtissait sur une position qui frémit et restait décalée.
2. **Signature au demi-pixel** (au lieu du 1/16) : le relâchement du moteur la changeait encore ~12 images après l'arrêt.
3. **Le cache de Madrure ne reconstruit pas pendant que le semis BOUGE.** À la plantation, le moteur fait grandir la dalle
   et relâche la Toile pendant ~1 s : poids et positions de repos changent à CHAQUE image. Mesuré sur la règle reçue :
   **25 constructions pour une plantation** (×1), et à ×4 **une construction à chaque image, 830 ms chacune — 12 s
   figées**. Désormais : tant que la signature d'une surface change d'une image à l'autre, on repeint son onde d'avant ;
   on construit dès qu'elle est posée (le moteur est relancé pour le voir). **1 construction par plantation, ×1 comme ×4.**
   Et un cache par semis (quatre au plus) : la Toile et les aperçus du Studio ne se chassent plus.
4. **`boite(nom, s)`** — la boîte réellement peinte : les boucles de fil de Bobinette sortent du disque de la bobine, le
   liseré d'une strate fermée déborde de sa courbe ; calé sur le seul contour, ce qui dépasse était coupé net.
5. **`env.cible`** (Ritournelle) : la coulée d'une voisine, rognée par une cellule APPROCHÉE, mordait sur la vraie cellule
   et restait en éclat au bord de la dalle (vu à k = 1 et 2,5).

### 15.3 · Ce qui a été vérifié
- **« pid ou nuee = promesse » : juste**, lu dans le moteur — `pid` n'est posé que sur une graine reliée à un Promi,
  `nuee` sur la dalle d'une Nuée (`sync`). ⚠ **Il existe des cellules COLORÉES sans parole** (`kind:'promi'` sans pid :
  onboarding `_shAllColored`, dalles pas encore reliées, et **toutes les cellules des aperçus du Studio**) : pour les
  mondes neufs ce sont de la matière — pas de bobine, pas d'œil, pas de fragment agrandi dans un aperçu.
- **Cache de Madrure** : au changement de **palette**, 0 construction et l'image change (couleurs relues à chaque image —
  la géométrie ne dépend pas de la palette, elle n'a pas à tomber) ; au changement **clair/sombre**, 1 construction.
- **18 dalles sur 18** dans chaque monde, sans erreur ; Madrure : 11 yeux · 5 strates fermées · 2 cercles.
- **Même dalle aux trois tailles** (k = 0,3 · 1 · 2,5), regardée.
- **Longueurs** : toutes en `u`, `sp` ou `band` ; restent l'index spatial (interne, jamais peint) et le plafond de nœuds.
- **redteam_decoupe à zéro sur cinq configurations** — défaut, et `--monde=` chacun des quatre (option neuve du juge :
  elle PLANTE tous les Promi dans ce monde, sans quoi le juge ne les peint jamais ; original `sauvegardes/redteam_decoupe-avant-v32.py`).
  Il a pris en chemin **un défaut antérieur** : l'Aura (« Ce que tu as tenu ») et la fiche d'une personne affichaient la
  dalle en `width:auto!important` sous un plafond — une dalle rendue sous sa boîte (la seconde passe de `_rendDalle`
  accepte 5 %) était étirée ; mesuré jusqu'à 4,9 % sur **Encre**. Les cotes se posent désormais en ligne, `important`,
  plafonds levés : 1:1 dans tous les mondes.

### 15.4 · Le budget, à la méthode du §12 ter (dix canevas distincts ; même passe que les références)
```
                 calcul   dessin   écran (moyenne/image)   ×4 dessin   ×4 écran
Esquille           5,4      8,4        17,0                  29,4        53
Ritournelle        8,6     21,2        33,3                  96,0       117
Bobinette          8,7     24,4        36,1                  95,8       142
Madrure (cache)    3,5     46,4        63,6                 184,1       234
  Gravure (réf.)  32,2     46,6        64,5                 219,5       282
  Touffe  (réf.)  14,6     80,0       128,8                 285,4       477
Madrure, construction (renderTo, cache vidé)   240 ms médiane · 273 max  |  ×4 : 1 355 médiane · 1 756 max
```
La machine était plus chargée que le matin (Touffe 80 contre 63, Gravure 46,6 contre 40,6) : **on compare dans la
passe**. L'ordre annoncé par le chat des mondes tient (Esquille < Ritournelle < Bobinette < Madrure), mais **Madrure en
cache n'est pas « sous Gravure » : il est À ÉGALITÉ** (46,4 contre 46,6 ; écran 63,6 contre 64,5). Sa construction dans
l'app coûte **1,7 à 2,6 fois** leurs chiffres (91 / 137 ms).

### 15.5 · v33 (23 sept. 2026) — les décisions de Tom sur les mondes neufs
- **Esquille gratuit ; Bobinette, Ritournelle, Madrure au Cercle** (`_lockW`, `_lk`) : le Cercle passe de trois à six mondes.
- **Noms affichés** (clés inchangées) : Encre → Pochade · Mosaïque → Tesselle · Pixel → Buvard · Sillons → Houle ·
  Gravure → Taille-douce · Terrazzo → Éclisse ; Braille et Touffe gardent le leur. Touché : `STRUCT`, `WL`, `_map` (les
  anciens noms restent lus), l'onboarding, l'écran qui vend. Les descriptions des quatre neufs sont dans `STRUCT`.
- **Madrure se construit PAR TRANCHES** (`_madGen`, générateur ; `_madTranches`) : l'ancienne onde reste affichée ; une
  tranche vaut la moitié de l'image précédente (12–150 ms). Mesuré à la plantation, pire image : **×1 100 ms · ×4 450 ms**
  (Gravure, même coût de peinture sans construction : 67 · 300) ; avant : 240 ms · 1 360–1 760 ms d'un seul bloc.
- **L'encre des libellés** se choisit sur ce qui est peint dessous quand le monde le sait : `RD[monde].sous(x, y)`
  (Madrure : la bande du champ φ au point — filet, veine, veine claire ou fond). Cinq points le long du titre, moyenne.

### 15.6 · v34 (23 sept. 2026) — le semis grandit avec les promesses, et l'unité de matière devient fixe
- **Le semis** (moteur) : une cellule par promesse et par Nuée, plus aucune cellule vide dès la première parole ; vue entière.
  Mesuré avant : 68 graines à 6, 20 et 40 promesses. Après : 8 · 22 · 42 (promesses + 2 Nuées).
- **`env.uMat`** = √(W·H/68) × UK : l'unité de matière à la densité historique, indépendante du nombre de promesses. Esquille
  ×0,5, Bobinette ×1,07, Madrure ×1,38 — facteurs relevés côte à côte avec les cadres du PDF « la toile grandit ». Ritournelle
  garde l'écart entre graines : sa coulée remplit SA cellule (conforme au PDF).
- **Esquille** : la plaque se casse sur un semis de matière à pas fixe, ancré sur la Toile et tiré de sa clé ; chaque éclat
  prend la couleur de la promesse qui possède son germe. La cassure est GARDÉE (elle ne dépend que du semis de matière) : à la
  plantation la plaque se recolore, elle ne se recasse plus à chaque image.
- **Madrure** : les nœuds sont les promesses — peu au début ; la bosse d'un nœud est bornée à la moitié de l'écart à son
  plus proche voisin (sans quoi, à 40 promesses et plus, les bosses font un dôme et l'onde tourne en anneaux).
  **Sous Ingénu** (Q315, Tom) : l'onde prend le crème dalle et deux nuances, chaque dalle de promesse (œil, strate fermée,
  cercle) se repeint dans sa couleur de nature — calculées au plus 8 ms par image, gardées au carnet.
- **Ritournelle, dalle seule** : la coulée bute aussi contre les bords de la Toile (`env.bords`), dans le repère de la dalle.
- **Moteur, toute dalle contenue** : elle s'arrête au bord de la Toile (plus au hasard de la marge du canevas). **Rampe** : une
  dalle d'une seule couleur (Pixel, Mosaïque) prend le ton le plus haut de sa rampe ; l'étendue de clarté se lit entre les
  centiles 5 et 95 (0,3 % de pixels de bord la rabattaient sur le premier ton, lilas sur lilas).
- **Le toucher** : hors du rectangle de la Toile (vue reculée) c'est le vide — `hit()` n'y trouve rien, le double toucher y
  recadre (Q212 ; sans cellule vide il n'avait plus de cible — `redteam_zoom` 5).
- **La règle de la dalle d'une seule couleur** ne vaut que pour les bandes de Q30 (rampe pleine, haut ≥ 2). Et la hauteur de
  rampe d'une île de la Pelote en sombre passe de 0,85 à **1,4** : les cellules ont doublé (80 × 62 → 143 × 153 pour
  « rapporter le livre »), l'île sortait plus sombre (L* 48 → 41) et tombait à ΔE 7–14 du sol (plancher 15). À 1,4 : 18 et 21.

### 15.7 · v35 (23 sept. 2026) — corrections de Tom
- **Le semis qui grandit ne vaut que pour les quatre neufs** : les huit anciens retrouvent le semis constant et le `sync`
  d'origine, mot pour mot (incohérence assumée, CLAUDE.md). Changer de famille au Studio ressème la Toile.
- **Madrure sous Ingénu** : l'onde garde les trois tons de la palette ; seules les dalles des promesses prennent leur nature.
- **Ritournelle au Studio** : une cellule d'aperçu tourne la palette comme une promesse (ses strates variaient à peine).
- **Le geste de couleur du Studio** parcourt les 24 palettes en CERCLE (48 px le pas, constante gardée) : bornée, la liste
  ne permettait pas d'atteindre Atrabilaire ni Taciturne depuis Ingénu d'un glissement.

### 15.8 · v40 (24 sept. 2026) — MADRURE : L'ONDE N'EST PLUS UN PLAN (Tom)

*« Là ça me fait que des lignes parallèles et des nœuds parfois ; on veut des vagues. Les traits parallèles, c'est perdre
l'âme de la madrure. »* Le champ valait `x·cos θ + y·sin θ` + une bosse par nœud : hors des nœuds, les lignes de niveau d'un
plan SONT des parallèles, à chaque ouverture. **Trois ondes lentes s'y ajoutent**, tirées de `cleToile` (stables pour une
Toile, différentes d'une Toile à l'autre) : deux LE LONG des lignes (longueurs 3,2–4,8 u et 6–9 u, pentes 0,40 et 0,25 —
les lignes ondulent), une EN TRAVERS (2,2–3,2 u, pente 0,22 — elles se resserrent et s'écartent, comme un veinage).
**La somme des pentes (0,87) reste sous celle du plan (1)** : le champ croît toujours dans le sens θ, donc aucune boucle
fermée ne naît hors d'un nœud — pas de faux œil. À vide, la tendance reste des lignes qui courent. `phi` (que relisent les
yeux) reçoit les mêmes ondes que la grille. **L'aperçu du Studio porte 10 nœuds** (au lieu de 5, Tom : « deux fois plus »).
**Ce que ça coûte :** construction 69 → 104 ms (×1), 263 → 483 (×4) ; dessin 7,5 → 8,6 ; pendant une plantation, médiane
16,7 ms mais un dixième des images à 33 (était 17). Sauvegarde : `sauvegardes/app-avant-v40.html`.

### 15.9 · v43 (24 sept. 2026) — RITOURNELLE : LA TRANSITION (Tom)

*« Les coulées se tirent comme si des doigts les étiraient depuis l'extérieur de l'écran, puis se reforment en suivant leurs
contours. »* **Trois à quatre doigts** posés hors de l'écran (le premier dans la direction de la dalle qui arrive ou part),
tirés de `cleToile` et du numéro de transition. Chaque doigt tire un champ continu : nul au centre de l'écran, plein au bord,
étroit en travers (σ = 0,30–0,46 × la demi-largeur) — les coulées voisines s'étirent ensemble. Dans une coulée prise, c'est
le bord **tourné vers le doigt** qui part (cos^2,2) : une langue, jamais un glissement en bloc. Les strates intérieures sont
tirées à proportion de leur rayon (centre ancré) et **en retard de 85 ms par strate** : elles suivent le contour.
Temps : tirée 460 ms (sortie cubique), puis ressort amorti (τ 260 ms, période 760 ms, rebond ≈ 23 % vers l'intérieur) ;
doigts décalés de 40 à 190 ms ; `transDur` 1 900 ms. Pendant la transition le rayon **continu** remplace le rayon marché
(le pas de 0,05 sp faisait frémir le bord à chaque image), et le rayon marché revient dans les 350 dernières ms — au repos,
la coulée est celle d'avant. **Le départ** : la coulée partie se retire dans sa cellule en 560 ms, ses voisines prennent
la place. Publié : `window._ritTrans` ({tt, n, doigts, trq}).
**Mesuré** (plantation et départ, 2,2 s, intervalle entre images) : Chromium ×1 **16,7 / 16,7 / 16,7** (méd · p90 · max) ;
WebKit **17 / 17**, max 34–41 au départ ; Chromium ×4 **50 / 50–67** — **identique à v42 sans transition** (même banc) :
la transition ne coûte rien de mesurable. ⚠ **Un saut d'une image de ~100 ms en WebKit, à la PREMIÈRE plantation d'une
séance**, ~170 ms après `addPromi` — il existe **aussi dans Pochade et dans v42** : ce n'est pas la transition (CHANTIERS).
Outils : `sauvegardes/transitions-v43/` (`film.py`, `duo.py`, `depart.py`, `perf_trans.py`). Sauvegarde `app-avant-v43.html`.

### 15.10 · v44 (24 sept. 2026) — LE MOUVEMENT JUSQU'AU BOUT, ESQUILLE (Tom)

*« On veut la matière qui évolue, jamais de saut saccadé, tout doux, logique, puis se stabilise ; là ça saute à la fin. »*
**L'instrument** (`sauvegardes/transitions-v43/sauts.py`) : pour chaque image après le geste, l'écart moyen avec la précédente
(Toile à 1/4, niveaux) ; un saut = une image > 3 × la médiane de ses voisines et > 1,5 ; la fin = la dernière image qui change.
**Avant (v43), mesuré :** Madrure saute à la fin (29 niveaux à l'arrivée, 24 au départ, voisines 0,1 — l'onde reconstruite
d'un coup) ; Ritournelle saute au départ (4,3 à 631 ms, le retrait de la graine partie) ; Esquille et Bobinette partent d'une
image à l'autre (fin à 224–265 ms).
- **Le moteur, dans les quatre mondes neufs seulement** : les graines bougeaient de 22 % de la distance À CHAQUE IMAGE — vitesse
  maximale dès la première image, traîne coupée net à 0,6 px, et une vitesse liée à la cadence (§8 de CLAUDE.md). Désormais un
  **ressort à amortissement critique** sur le temps réel (position ω 9, poids ω 8 rad/s) : vitesse nulle au départ, pas de
  rebond, posé en ~0,7 s, arrêt sous 0,1 px. Les huit anciens gardent leur mouvement d'origine.
- **Ritournelle** : une voisine qui arrive ne coupe la coulée que peu à peu, une voisine qui part cesse peu à peu de la
  borner ; la coulée neuve naît de rien ; le passage au rayon continu entre en 300 ms (posé d'un coup, TOUTES les coulées
  bougeaient de quelques pixels à la première image : 11,8 niveaux).
- **Esquille** (`transDur` 2 600) : un éclat qui change de propriétaire SE CASSE (rétracté à 66 %, pivot ≤ 0,25 rad, écart de
  0,28 u dans le sens du mouvement, 460 ms) et sa couleur bascule au creux — aucune couleur inventée. État gardé : la couleur
  affichée et l'heure de la cassure, sur le germe du cache, seulement sur la Toile vivante (`env.vive`).
- **`env.trans` s'éteint à la fin de `transDur`** ; `window._transCoupe` coupe la transition (preuve).
**Mesuré après :** aucun saut, arrivée et départ, Chromium et WebKit (Esquille max 1,8 niveau par image, fin 2,0 s ; Ritournelle
fin ~2,1 s). **Au repos, identique au pixel** avec et sans transition (`repos.py`, 0 px sur 1 316 640 ; la sonde d'une teinte
décalée est prise à 585 600). Coût : Esquille Chromium ×1 16,7 / 16,7, WebKit 17 / 17 (max 19), ×4 50.
**Le saut WebKit de la première plantation** venait de `lot-CERCLE-TOILE` : Safari n'a pas `requestIdleCallback`, le repli
rendait une dalle de ~100 ms toutes les 420 ms quoi qu'il arrive — une tranche n'est plus rendue que Toile au repos et 700 ms
après le dernier toucher (collection toujours bâtie : 18/18).
**Et un second voleur, trouvé au ralenti ×4** (une image de 200–233 ms à l'arrivée) : le `transitionend` de `#studioScreen`
remonte de toute transition de ses descendants ; à une plantation il appelait `poser()` Studio FERMÉ, qui repeignait `#stBg`
et lançait 1,1 s de frémissement sur un canevas invisible (40–64 ms par image à ×4). `lot-STUDIO-PLATEAUX` ne peint plus un
Studio sans `.show`. Pire image à ×4 : 200–233 → 100 ms, p90 67. Outil : `saut.py` (WebKit) / `saut4.py` (Chromium ×4) —
chaque rappel de plus de 15 ms nommé, avec son origine.

### 15.11 · v45 (24 sept. 2026) — LE PDF, MONDE PAR MONDE, ET LES TROIS AUTRES TRANSITIONS (Tom)

**Esquille — la répartition** (*« trop fragmenté, tous les fragments de la même taille ; on veut de grands axes coupants qui
traversent la plaque et une vraie diversité de tailles ; le fragment d'une promesse nettement plus gros que la matière »*).
Un ARBRE DE CASSURES fixe pour une Toile (clé + taille, jamais les promesses) : 4 à 6 droites traversantes, puis la refente
(en travers de la plus grande longueur, à une place variable). On peint une COUPE de l'arbre décidée par les promesses : un
morceau à plusieurs promesses se refend ; à une promesse il s'arrête à ≤ 1,6 × Ap (c'est SA dalle) ; sans promesse, à
Ap × (0,3 + 0,55 v²) (v tiré par morceau). Ap = min(0,62 × aire par promesse, aire / 7). Couleur : l'éclat d'une promesse
porte sa couleur ; la matière, un autre ton de la palette de la promesse la plus proche (le sien une fois sur six). La dalle
d'une fiche = son grand éclat. Publié : `window._esqComp`. **Mesuré** (`esq_comp.py`) :
```
             graines   éclats de promesse   matière   médiane promesse / matière   couvert par les promesses
 3 paroles      5              5               17            5,6                         61 %
 9 paroles     11             11               23            3,4                         71 %
20 paroles     22             22               61            3,5  (matière 395 → 5 970 px²)  64 %
40 paroles     42             42              137            3,4                         58 %
```
(les graines comptent les Nuées : 20 paroles + 2 Nuées = 22 formes). Le mouvement de v44 est gardé ; une refente ne
réduit plus parent et enfants chacun autour de son centre (les surfaces ne coïncidaient pas : saut) — les éclats neufs
prennent la place à pleine taille dans la couleur de ce qu'ils remplacent, puis se cassent.

**L'ampleur — les quatre mondes neufs** (*« il en faut de tailles un peu différentes, comme dans le PDF »*) : chaque parole
reçoit un poids stable (titre et personne) de −0,09 à +0,22 × l'écart moyen, réparti vers le haut (`_ampleur`, `_amplifie`).
±0,3 donnait des coulées minuscules et des étiquettes chevauchées. Le toucher et les fiches lisent la même règle pondérée.

**Bobinette — les fils se retissent** (`transDur` 2 400) : un arc qui change (couleur, sens de tuile, épaisseur de bobine)
se retire le long de son arc puis le nouveau se tisse le long du sien (520 ms). La trame se lit sur la position de REPOS (le
frémissement faisait sauter une bobine de case).

**Madrure — l'œil dans le champ, et le GPU.** (1) *« L'onde se referme d'elle-même autour de chaque promesse »* (PDF) : la
bosse d'un nœud passe de 7,5–9,5 band sur 0,36–0,48 sp à **10–12,5 band sur 0,26–0,34 sp** — un nœud sur trois n'avait pas
d'œil (dalle `fermee`, fermée de force : le galet coupé de bandes). Mesuré : 12 yeux sur 18 → **18 sur 18**. Strate de plus
une fois sur quatre au plus (était 0·1·1·2). (2) **Rendu GPU de la Toile vivante** (WebGL2, `_madGL`) : le champ
(`_madParams`, les mêmes nombres que la construction CPU) évalué par pixel à chaque image, classé comme le dessin ; les bosses
montent (800 ms) et descendent (560 ms) ; la borne de la bosse par la voisine entre au même rythme (d'un coup : |Δφ| 0,57 à la
première image) ; sous Ingénu l'œil est teinté DANS le shader — un point en est s'il n'est au-dessus de son niveau QUE par la
bosse de ce nœud (le critère « au-dessus du niveau dans un rayon » teintait la pente montante en coin) ; niveau, rayon et
teinte d'un œil glissent (0,17 s). Sans vrai GPU (`failIfMajorPerformanceCaveat` : SwiftShader rendait 1 image/s) ou
au-delà de 64 nœuds, chemin CPU. Fiches, exports, aperçus : CPU. Publié : `window._madGPU`.
**Mesuré** (`champ_mad.py` — le MOUVEMENT DU CHAMP, pas les pixels : sous GPU la copie du canevas lit parfois une image en
retard, Esquille y montrait les mêmes faux pics) : aucun saut, WebKit et Chromium-GPU, arrivée et départ ; posé en ~2,2 s.
Coût : WebKit 17 / 18 ms (max 27 · 47 au départ) ; Chromium-GPU 16,7 / 16,7 ; ×4 33 / 33 (CPU : 50 et plus).
**Au repos, identique** avec et sans transition dans les quatre mondes (0 px ; WebKit : 1 px de bruit, témoin compris).
Sauvegarde : `app-avant-v45.html` ; l'ancien Esquille : `sauvegardes/Resq-avant-v45.js`. Outils : `transitions-v43/`.
⚠ Vu en passant, non touché : dans `_labels`, `fs` est lu avant d'être posé — la sonde `sous` lit donc toujours le fond,
l'encre des libellés de Madrure ne suit jamais la bande (défaut antérieur, sans effet de mouvement).

### 15.12 · v48 (24 sept. 2026) — CABOCHON, TREIZIÈME MONDE, GRATUIT

Le dessin du moodboard de la célébration, figé à la demande de Tom (« exactement comme il est »). `Rcab` : pour chaque parole, sa cellule pondérée (bissectrice décalée par les poids, bornée à 0,06–0,94 de l'écart, douze voisines), reculée d'un demi-jour, arrondie aux coins (`_traceArrondi`). Jour 0,09 u, rayon 0,17 u (u = écart médian entre graines). Une seule couleur : `cOf`. Branché : RD, TH (`GMOS`), `_NEUFS` (une cellule par parole), STRUCT, WL, order (avant Esquille), `_map`. Monde CONTENU (pas dans `_MNLIB`) : la dalle seule est sa cellule (`env.cible`, `env.bords`). `transDur` 1 600 : la cellule neuve naît de rien (600 ms), celle qui part se retire vers son centre (560 ms). Mesuré : Chromium ×1 16,7 / 16,7 ; WebKit 17 / 17 ; aucun saut ; repos identique (0 px).

**Les bulles.** Dans les jours, sous les dalles : une goutte en triangle arrondi à une jonction sur trois (dans le vide ≈ 0,58·jour + 0,155·rayon), une bulle en œuf dans un jour sur huit. Tirées des CLÉS des voisines (`_fnv`), couleur d'une voisine (`cOf`), jamais dans une dalle seule.

**v49 — le retrait va au bout.** Un monde qui dessine ses propres cellules doit laisser la dalle qui part céder TOUTE sa place avant que le moteur la retire (PART_DUR, 620 ms) : sinon la fin est un saut. Cabochon : frontière `_cabFront`, celle qui part → 0, ses voisines → au-delà d'elle, en 520 ms. Les bulles se taillent dans l'espace libre mesuré (`_cabBulle`), jamais par une forme posée à l'estime.

### 15.13 · v62 (27 sept. 2026) — BROUILLAMINI, PREMIER MONDE DE LA SAISON 2

Porté de `decoupe()` (planche « Trois matières »). **Fabrique à part** (`creerBrouillamini(env)`, bloc `lot-V62-BROUILLAMINI`) : elle reçoit le
même environnement que les mondes v32 (`_envM`, prototype) plus `rampeMat` (= `grays()`), et `_MN.seule/contour/toucher/nature/boite` lui
passent la main pour son nom. **C'est le patron pour les six suivants** : un monde neuf ne s'écrit plus dans `creerMondes`.
- **Géométrie** : pour chaque dalle, la place direction par direction (200 rayons) jusqu'à la part de l'écart qui lui revient — la moitié au
  repos, `f_p/(f_p+f_o)` pendant une arrivée ou un départ (`f` = facteur d'arrivée ou de retrait) : la frontière bouge d'un seul calcul, rien
  ne saute. u = avg(), le compte des graines pondéré par ces facteurs (sinon u saute de √(n/(n+1)) à la plantation).
- **Gardé** : le profil, les méplats, le trou et la chute se tirent de la CLÉ une fois pour toutes ; la géométrie et ses tracés se gardent tant
  que positions (½ px), facteurs, W×H, u, uMat et clé de Toile ne bougent pas.
- **Matière** : semis de découpes à pas propre (tiré de `Toile.cle()`, unité `uMat`), chacune RÉTRÉCIT continûment pour tenir hors des
  dalles à un jeu près (0,07 uMat) — jamais une apparition d'un coup.
- **Toucher strict** (`RD.brouillamini.toucheStrict`) : hors de ce qui est peint, `hit()` ne retombe PAS sur la cellule — mesuré 99,4–99,9 %
  d'accord avec le pixel peint ; 16–22 % des points (matière, joints) n'ouvrent rien.
- **Mesuré** (méthode §12 ter) : dessin 13–15 ms Chromium ×1 (Pochade 20,7 dans la même passe), 7–7,6 ms WebKit ; écran et plantation 16,7 / 17 ms
  (max isolé 33 Chromium, 30 WebKit, à 40 promesses) ; aucun saut à l'arrivée ni au départ (`sauts.py`, les deux moteurs) ;
  0 pixel entre deux rendus et après un aller-retour de palette et de thème.
- ⚠ **Le semis n'est pas le même d'un chargement à l'autre, même clé de Toile** (§7.2, vrai aussi pour Halin) : la silhouette d'une dalle,
  qui dépend de ses voisines, change donc avec lui. Le monde n'y peut rien ; c'est le semis du moteur.

### 15.14 · v63 (27 sept. 2026) — CHAMADE, ET CE QU'UN MONDE QUI DÉPLACE SES DALLES DOIT FAIRE
- **Une disposition globale ne se refait pas à chaque image.** La relaxation de la planche (les cœurs s'écartent, rétrécissent) repart de
  zéro : refaite image par image sur des graines qui glissent, elle faisait bouger tous les cœurs par à-coups. Pendant une transition :
  deux dispositions (celle qu'on voyait, celle d'arrivée sur `env.finale`), un glissement de l'une à l'autre (1 200 ms). Au repos la
  disposition d'arrivée RESTE : recalculée, elle tombe sur un autre point fixe du moteur (un cœur sautait de 42 px à la fin).
- **Le titre va où la dalle est peinte** : `RD[monde].ancre(s) → [x, y, largeur]` (ajout au moteur, `_labels`).
- **L'ancre et le toucher lisent la géométrie de la dernière image peinte** : relire l'horloge dans une ancre refaisait toute la
  géométrie une fois par titre (images de 170 ms).
- **`uMat` pendant le rendu d'une dalle contenue** vaut celui de la Toile (`_WT`) : W×H y est la boîte de la cellule.
- Mesuré : aucun saut (Chromium, WebKit), redteam_decoupe 0, toucher 100 % sur le contour, 0 pixel au repos ; **hors budget à 20/40** (CHANTIERS).

### 15.15 · v72 (27 sept. 2026) — LA PASSE DE BUDGET DE LA SAISON 2

Chiffres avant/après : `BUDGET-SAISON2.md`. Bancs : Chromium avec le vrai GPU, WebKit (processus GPU). Preuve de la matière : ci-dessous.

**Ce qui vaut pour tous — le calque de repos (`window._calqueRepos`, bloc `lot-V72-CALQUE`).** Au repos, la Toile ne change pas :
le monde se peint une fois dans un calque TRANSPARENT de la taille du canevas, avec la transformation du canevas, et se repose 1:1.
La signature (fournie par le monde) porte tout ce dont l'image dépend hors de la vue ; la vue est ajoutée par le calque. Tant que la
vue ou le contenu bouge (deux images différentes de suite), on peint directement. Guingois, Chamade, Chantourné, Mascaret, Volubilis.

**Par monde :**
- **Ramage** — le plumage (28 000 à 75 000 tracés) se peint une fois dans un calque OPAQUE (le fond du moteur d'abord) et se pose 1:1.
  À la plantation, le plumage d'arrivée (places `env.finale`, couleurs acquises) se CONSTRUIT PAR TRANCHES — les plumes de la planche
  mises en file (`_parure(…, Q)`, même ordre, mêmes tirages), puis rejouées dans le calque, un nombre de tracés par image réglé sur la
  durée RÉELLE des images (le temps de JavaScript ne dit rien de la rastérisation qui suit) — et passe sur l'ancien EN FONDU (ARR,
  900 ms). **La transition change d'aspect : Q340, à valider.** Au repos, le plumage d'arrivée reste tant que les mêmes paroles sont
  là (§15.14). La dalle seule lit l'œil dans le plumage de la Toile (tracés marqués de leur œil) au lieu de tout recalculer en mode
  « only » (~150 ms par dalle, payés par le pré-rendu de l'Index et du Fil).
- **Volubilis** — le jardin d'arrivée se construit dans un **Worker** (les fonctions de la planche, recopiées par `toString()`), le
  jardin affiché reste pendant ce temps ; le glissement part à son arrivée. Même jardin au bit près (vérifié : JSON identique).
- **Guingois** — chaque pli et chaque bosse à sa portée (3,6 σ : < 10⁻⁵ px) ; la PART FIXE de l'étoffe (ondes, bosses, cassures de
  fond) gardée par étoffe, seuls les plis des paroles se recalculent, dans le même ordre d'addition ; les points de quadrillage
  partagés, déformés une fois ; le bord d'une dalle à la demande ; `closePath` retiré des remplissages. **En transition seulement** :
  une ligne échantillonnée tous les c/4,5 (au lieu de c/9) et 5 points par côté de case (au lieu de 10) — corde de 3 px sur un arc de
  rayon ≥ 30 px : < 0,04 px.
- **Mascaret** — D (la hauteur de la page) était recalculée pour CHAQUE lame dans la boucle des traits (40 fois la même valeur) ; sur
  une bande, le facteur vertical de chaque lame est constant et le facteur horizontal ne dépend que de la grille des échantillons :
  les deux se précalculent, D devient une somme des MÊMES produits dans le même ordre. L'épaisseur d'un trait calculée une fois par
  point (les deux bords la relisaient). Un poids qui ne peut pas dépasser le meilleur n'est pas calculé (décision identique).
- **Chantourné** — un fil n'interroge un médaillon qu'à moins de 2,72 R en y (au-delà : ee ≥ 1,2375, il ne peut ni gagner le point ni
  changer le liseré) ; `hypot`, `atan2` et les deux sinus du bosselage par la racine et les polynômes de l'angle multiple (10⁻¹⁵).
- **Chamade** — sur la Toile vivante, la page se peint d'un bloc (en calque quand la vue est posée) puis le PAPIER du moteur sous chaque
  cœur : même mélange au bord (bande × (1 − c) + fond × c), sans le masque pair-impair de toute la page.
- **Hors des mondes** : le pré-rendu des dalles (`rechauffe`, v59) attend aussi que la Toile soit au repos (`Toile_state().running`) —
  il se lançait pendant un fondu et coûtait une image de 100 à 330 ms.

**La preuve** (`scratchpad/preuve_v72.py` de la session, sondes `window._v72Preuve` et `window._v72SansCalque` laissées dans l'app) :
même page, même semis, 3 · 20 · 40 promesses, deux thèmes, deux moteurs, témoins à 0.
```
                       géométrie (ancienne formule / nouvelle)      Toile vivante : calque / peinture directe
  Guingois             0,001 px ; 0,001–0,003 % des pixels          Chr 0,002–0,09 % (ΔE moy. 1,3–3,9) · WK ≤ 2 niveaux
  Mascaret             7·10⁻⁶ px ; 0 pixel                          Chr 0,004–0,16 % (ΔE moy. 1,4–3,7) · WK ≤ 2 niveaux
  Chantourné           2·10⁻¹⁵ ; 0 pixel                            Chr 0,05–0,15 % (ΔE moy. 1,2–1,6) · WK ≤ 1 niveau
  Chamade              —                                            Chr 0,08–0,27 % (ΔE moy. 1,5–4) · WK ≤ 2 niveaux
  Volubilis            Worker = sur place : JSON identique          Chr 0,07–0,13 % (ΔE moy. 1,8–2,4) · WK ≤ 2 niveaux
  Ramage, dalle seule  0 pixel (œil lu dans le plumage / « only »)
  Ramage, Toile        —                                            Chr : 0 à 3 · 1,2 à 8,5 % à 20–40 (voir ⚠) · WK ≤ 1 niveau
```
⚠ **Chromium sur GPU anticrénèle un même tracé autrement selon l'endroit où il vide son lot.** Mesuré : le même plumage peint d'un bloc,
puis par tranches (une relecture d'un pixel entre deux) → **7,3 % des pixels différents, sur les bords seulement** ; en WebKit : 0.
Les écarts du calque de Ramage en Chromium sont exactement cela (il est peint par tranches) : ni la géométrie, ni les couleurs.

**Pièges trouvés en route** (voir aussi CLAUDE.md §8) :
- un `// commentaire` ajouté au milieu d'une fonction écrite sur UNE ligne commente la fin de la ligne : tout le bloc de Ramage ne se
  chargeait plus, et une preuve a été « verte » sur un monde absent. **Après chaque patch : `node --check`, bloc par bloc.**
- `Object.keys()` range les clés ENTIÈRES par valeur : un cache « supprime la première clé » jetait la plus petite (parfois celle qu'on
  venait de faire) — Ramage et Guingois se reconstruisaient sans fin. Un cache s'évince par ordre d'entrée (un tableau à côté).
- une file de construction qui relit ses entrées à chaque image les voit bouger : Volubilis demandait un nouveau jardin au Worker à
  chaque image. Les places d'arrivée se lisent UNE fois, à la première image de la transition.
- le moteur ne se pose pas exactement aux places annoncées (`env.finale`) : une graine à 100 px. Un état d'arrivée se garde sur les
  CLÉS (mêmes paroles, même Toile), jamais sur les positions — sinon un second fondu, une seconde après le premier.

### 15.16 · v74 (27 sept. 2026) — LE ZOOM DE RAMAGE, ET CE QUI N'A PAS MARCHÉ POUR CHAMADE
- **Ramage, quand seule la vue change** (zoom, glissé) : le calque se pose mis à l'échelle PENDANT le geste (Q340 validé), puis se refait
  net dès que l'échelle est posée — borné à la zone vue (+ 8 %), le dernier calque entier posé dessous pour qu'aucun dézoom ne découvre
  de trou, en grandes tranches si la vue est immobile depuis 120 ms (~45 ms par image : rien ne bouge), fondu de netteté 150 ms. Une
  plume hors de la zone ne dépose aucun pixel : le calque est le même.
- **Chamade, un calque par cœur (la méthode de Touffe, v38) : essayé, RETIRÉ.** Elle suppose une forme qui ne change pas de taille ;
  pendant une plantation, 73 % des cœurs en changent à chaque image. Gain mesuré : nul. À retenir avant de la reproposer ailleurs :
  **compter d'abord combien d'objets gardent leur taille pendant le mouvement.**
- **Guingois : plancher assumé** (Tom) — l'étoffe se recalcule à chaque image de la plantation ; c'est sa matière.
- **Pour mesurer un zoom en WebKit** (pas de toucher CDP) : deux `PointerEvent` de type `touch` envoyés dans la page, sur l'élément sous
  le point — la Toile écoute les pointeurs, pas les touches.
