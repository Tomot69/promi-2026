# SPEC-GESTE — les gestes de Promi, tels que le prototype les fait

> **Pour qui :** celui qui reconstruit Promi en Swift sans relire `app.html`.
> **D'où viennent les valeurs :** du code (cité `fichier:ligne`) ou d'une décision écrite (document et bloc cités).
> Les numéros de ligne sont ceux de la copie de travail du **6 oct. 2026** (`app.html` 38 340 lignes, lot v134 en cours,
> non commité ; `promi-moteur.js` 8 034 lignes). Ils servent à retrouver, pas à porter.
> **Ce qui manque est écrit « ⚠ TROU ».** Rien n'est inventé : là où le prototype n'a pas de seuil, ce document le dit.
> **Unités :** le point d'un écran 390 × 844. Le prototype met l'appareil à l'échelle dans la fenêtre : toute coordonnée
> de doigt y est ramenée à 390 (`clientX − rect.left) × 390 / rect.width`). En Swift, le point UIKit suffit.

---

## 0 · Ce qui vaut pour tous les gestes

| Règle | Source |
|---|---|
| **Un mouvement se calcule sur le temps réel, jamais sur le compte d'images** (vitesse, décroissance, durée). | CLAUDE.md §8, bloc « ⚑ UN MOUVEMENT SE CALCULE SUR LE TEMPS RÉEL » |
| **L'heure d'un mouvement de doigt est celle de l'ÉVÉNEMENT, et chaque événement regroupé compte.** | idem ; `app.html:30740-30760` |
| **Le geste ne se dégrade jamais** : tous les `coalescedTouches` traités, le trait rendu dans la trame du toucher, pleine résolution. | CLAUDE.md §11 |
| **Un geste au doigt se prouve dans TOUTES les directions** (un départ vertical est repris par le défilement du système). | CLAUDE.md §3, bloc v126, C-010 |
| **Une porte s'ouvre sur le lever du doigt sans glisser, pas sur un clic synthétisé** (le « clic fantôme » d'iOS Safari n'existe pas en UIKit ; ne pas porter ses parades `lot-CLIC-FANTOME`). | CLAUDE.md §8, ligne « Une porte s'ouvre et se referme aussitôt » |
| **Le trait part du centre du rond gauche, pas du doigt. Courbes quadratiques, jamais de segments droits.** | CLAUDE.md §5, tableau des composants |
| **Les points disent qu'il manque quelque chose** (une moitié de trait, un mot, un engagement) et ne servent à rien d'autre. Une seule exception : les trois points du choix de taille de l'outil de dessin. | CLAUDE.md §5, « ⚑ LA LOI DES POINTS » (v128, C-044 ; v127) |
| **C'est un geste : la validation de Tom sur iPhone est obligatoire.** | CLAUDE.md §3, bloc v132 |

---

## 1 · LE TRAIT — la géométrie commune à planter, tenir, tracer sa moitié

### 1.1 · L'onde

Une seule formule dans tout le produit (`app.html:14339-14341`, publiée par `window._onde`) :

```
onde(base, amp, per = 1,5, larg = 390) :
    t    = borne(x / larg, 0, 1)
    y(x) = base − (0,34 · amp) · t − (0,62 · amp) · sin(2π · per · t)
```

- **période 1,5 sur 390** pour une fiche et pour la page + ; **période 1 sur SA largeur** pour une carte d'Index
  (CLAUDE.md §8, ligne « Une carte d'Index a la vague d'une FICHE »).
- Le chemin se trace en **Bézier cubiques, un segment par quart de période** (`seg = 390/6`), tangentes exactes
  prises sur la pente de l'onde (`chemin`, `app.html:14343-14348`).

### 1.2 · Base et amplitude, par écran (elles se LISENT, elles ne se déduisent pas)

| Écran | base | amp | mode du trait | Source |
|---|---|---|---|---|
| Fiche · en cours / à tenir / Chiche lancé | 286 | 36 | `moitie` | `app.html:14452` |
| Fiche · gardé de côté | 286 | 36 | `points` | `app.html:14472-14480` |
| Fiche · tenue, sans mot | 400 | 36 | `complet` | `app.html:14483-14486` |
| Fiche · tenue, avec un mot ou des commentaires | 286 | 36 | `complet` | idem |
| Fiche · Chiche tenu à deux | 396 | 36 | `duo` | `app.html:14481-14482` |
| Page + · au repos | `max(196, 344 − 32·(lignes − 1))` | 36 | repos (`plate`) | `app.html:17099-17108` |
| Page + · un choix ouvert | 144 | 16 | repos | idem ; CLAUDE.md §3 bloc v116 |
| L'instant (trois écrans) | 300 | 36 | `arrive` puis `complet` | `app.html:19633-19652` |
| Fiche d'un Cercle | `max(176, 460 − 86·n)` ; état défilé 58 / 16 | — | `complet` | CLAUDE.md §5 (§13) ; `app.html:38128` |

Plancher de la base : **196** (fiche et page +), **176** (Cercle) — CLAUDE.md §4, « LE VIDE EST UN DÉFAUT DU PLANCHER ».
Boîte du trait : `base + amp + 40` sur une fiche (`app.html:14511`), `base + amp + 60` sur la page + (`app.html:17109`).

> ⚠ **Divergences à connaître.** ① Le commentaire d'en-tête de l'instant écrit « amplitude = 44 » (`app.html:19617`) ; le code
> pose **36** sur les trois écrans (`19633`, `19643`, `19648`). ② `TRAIT-PERSONNALISE-CONCEPT.md` §2.1 cite les bases
> « 262 · 372 · 376 » : ce sont les valeurs d'avant la décision du 2 sept. (« le trait descend de 24 », `app.html:14440-14451`) ;
> le code porte **286 · 396 · 400**.

### 1.3 · Les quatre modes du trait (`app.html:14784-14870`)

Épaisseur **10**, bouts ronds. Points : **cercles de rayon 4,5 (Ø 9), un tous les 18**, jusqu'à `390 − 4,5`.

| Mode | Ce qui est peint |
|---|---|
| `moitie` | plein de **0 à 195** (le milieu exact, jamais plus loin) · chevron à 195 · points à partir de `195 + 18` |
| `complet` | plein de **0 à 390** — ni chevron ni points : plus rien ne manque |
| `duo` | plein de 0 à 191, plein de 199 à 390 (un jour de 8 au milieu) |
| `points` (rien n'est tracé) | **amorce effilée** de `x = −0,03·390` à `0,11·390 − 1,5`, épaisseur **22 → 1,5** (ruban perpendiculaire à la courbe, 44 pas) · chevron à `x = 0,11·390 = 42,9` · points à partir de `42,9 + 23,4` |

**Le chevron** (`app.html:14357-14360`) : posé sur la courbe, tourné selon sa pente (`atan2(y(cx+8) − y(cx−8), 16)`) ;
trois sommets `(−7, −10) · (6, 0) · (−7, 10)` × `k = épaisseur / 10` ; trait `6·k`, bouts et jointures ronds.
**Le trait s'arrête en deçà de la pointe** (`cx − 0,15·épaisseur`) : un bout rond dépasse de la moitié de sa largeur
(CLAUDE.md §8, « Une flèche a un trait qui lui sort par la pointe »).

**La flèche d'invite** (page + au repos seulement, `app.html:17349-17365`) : Bézier de `A = (chev + 32, base + 46)` à
`B = (chev + 10, base + 14)`, contrôles `(A.x − 10, A.y − 4)` et `(B.x + 3, B.y + 12)`, épaisseur 4,5, bouts ronds, arrêtée
2,25 avant `B` ; tête : deux ailes à ± 32°, longueur 13, sur la tangente réelle en `B`. `chev = 0,11 × 390`.

**Le filet sous le trait** : 0,8 px, crème adouci (`window._FILET_DOUX`, repli `#F7F0DE`), décalé de
`épaisseur/2 + 0,4` sous la courbe, peint AVANT le trait, seulement sous ce qui est tracé, arrêté derrière le V.
Il paraît dès que le trait est à **moins de 42 de luminosité** du corps qui le porte (`app.html:14826-14862`) ; sur la page +,
en sombre, pour les trois natures (`app.html:17257-17272`). Exception nominative exigée : la terre `#2B1020` d'une fiche tenue
(CLAUDE.md §3, bloc v114 « LE FILET DU TRAIT »).

**La couleur du trait** : il porte l'ÉTAT et se juge en **ΔE ≥ 15** sur son champ (CLAUDE.md §3, Q216). Sur un champ plein il
prend la teinte SOMBRE de sa nature (`NATTRAIT` : Promi `#022140`, Chiche `#3D0F23`, Cercle `#291547`) ; à tenir `#DD4D23` ;
tenue, la crête `#0B4A2A` sur la terre (CLAUDE.md §3, « §2.1 bis CORRIGÉ » et bloc du 21 sept.).
**Le pinceau** (la matière du trait, propre à chaque parole) remplace le plein et l'amorce, jamais la courbe, le chevron ni
les points (`app.html:14788-14800`).

### 1.4 · Où le doigt se pose

Le canevas du geste est **invisible** (opacité 0) : **c'est l'onde qui est le guide** (`app.html:14101-14110`, `16742-16753`).
C'est une bande de **390 × 118**, posée :
- sur une fiche : `top = boîte − 118` (`app.html:15073-15075`) ; absente sur une parole tenue et sur un gardé de côté ;
- sur la page + : `top = base − 59` (`app.html:17743-17745`).

Le composant « deux points, un trait » de 118 px (CLAUDE.md §5) reste la grammaire du geste là où il est visible.

---

## 2 · PLANTER — le trait de lancement de la page +

**Code :** `app.html:12684-12800` (« LOT 1 · le geste pour PLANTER », trois zones : `planterZone`, `planterZoneN`, `planterZoneD`).

| | Valeur | Ligne |
|---|---|---|
| Rond de départ `a` | `x = 390 × 42/308 = 53,2` ; `y = 118 × 52/118 = 52` ; rayon 18 | 12713 |
| Rond d'arrivée `b` | `x = 390 × 266/308 = 336,8` ; même `y` ; rayon 18 | 12713 |
| Où le doigt peut se poser | `x ≤ a.x + 130` (soit ≤ 183,2), à n'importe quelle hauteur de la bande | 12735 |
| Premier point du tracé | **le centre du rond gauche** ; le doigt n'est ajouté que s'il en est à plus de 6 | 12736 |
| « Arrivé » | dès que `x > a.x + 0,66 × (b.x − a.x)` (soit > 240,4) → vibration 14 ms | 12739 |
| Validé au lever | `arrivé` **OU** parcouru en x (dernier point − premier) **> 0,5 × 390** | 12749-12750 |
| Sinon | rien : la zone se referme, aucun message | 12751, 12758 |
| Retour haptique à la validation | `[12, 40, 26]` ms (vibration, pause, vibration) | 12752 |
| Remise à zéro du tracé | 330 ms après le lever | 12759 |

**Ce que le doigt publie pendant le geste :** son abscisse en écran 390 (`window._ppDoigt`), et la page + se repeint
(`_ppTout`) : **le plein va de 0 au doigt, borné au milieu** pour un Promi et un Chiche (`MI = 195`), **à 390 pour un Cercle**
(`ENTIER`, `app.html:17235-17241`), le chevron marque la frontière, et **dès que le doigt trace, le trait entier passe en
`#DD4D23`** (`app.html:17231`). Au repos la couleur est celle de la nature (`NATTRAIT`).

> **Un Cercle se lance en traçant le trait entier** (0 → 390, le mode complet) : il n'est promis à personne, personne ne vient
> à sa rencontre. Un Promi et un Chiche tracent une moitié (CLAUDE.md §4, « UNE NUÉE SE LANCE EN TRAÇANT LE TRAIT ENTIER »).
> ⚠ **Dans le prototype, seul le DESSIN diffère** : le seuil de validation est le même pour les trois natures (66 % de la
> course entre les deux ronds, ou plus de la moitié de la largeur). Le prototype n'exige donc pas d'un Cercle qu'il aille
> jusqu'à 390. **⚠ TROU :** aucune décision écrite ne fixe la part exigée pour un Cercle (cherché : CLAUDE.md §4, §5 ;
> `app.html` autour de `ENTIER` ; `redteam_nuee_entree.py`).

**À la fin** (`app.html:12753-12756`) : clic sur le bouton de la nature active — `#addPromi` (Promi, Chiche),
`#addNuee` (Cercle), `#addDraft` (gardé de côté). Ces boutons passent par `window.printTirage(…)`
(`app.html:3191`, `3196`, `3327`) : `_tirageActive = true`, la page + **coupe** (transition retirée, `closeAll()`), puis la Toile
reçoit la dalle (`Toile.addPromi`). **Une plantation coupe, elle ne fond pas** (CLAUDE.md §8, ligne « Un ancien écran paraît
une fraction de seconde »).

> ⚠ **L'état « signé »** (`e.etat === 'signe'` : le plein arrêté à 195, ou à 390 sans chevron ni points pour un Cercle,
> `app.html:17129`, `17243`, `17289`) est DESSINÉ mais **le geste du prototype ne le pose jamais** : `window._ppSigne` n'est écrit
> que par le relevé `releve-S3-page-plus.py`. À la validation, la page + coupe directement. **⚠ TROU :** combien de temps
> l'état « ma moitié est donnée » doit rester à l'écran avant la coupe — aucune valeur (cherché : `_ppSigne`, `printTirage`).

**Bascule trait / bouton** (`.tenir-alt`, deux petites flèches) : `app.html:12769-12778` ; masquée sur la page + portée
(`app.html:16754-16757`). ⚠ TROU : son sort dans le portage n'est écrit nulle part.

---

## 3 · TENIR — tracer pour tenir sa parole

**Code :** `window._tenirInit`, `app.html:4593-4792`. Bande 390 × 118 posée sur l'onde (§1.4).

| | Valeur | Ligne |
|---|---|---|
| Rond de départ `a` | `x = 38`, à la **hauteur du doigt** dès qu'il s'est posé (le centre de la bande au repos) ; rayon 19 | 4619-4622 |
| Rond d'arrivée `b` | `x = 390 − 38 = 352` ; rayon 19 | 4621 |
| Où le doigt peut se poser | `x ≤ a.x + 130` (soit ≤ 168), à n'importe quelle hauteur | 4700 |
| Premier point | le centre du rond gauche ; le doigt ajouté s'il en est à plus de 6 | 4707-4709 |
| Ouverture de la zone | pendant **340 ms** la zone s'ouvre (`.ouvert`, `.tracant` sur la fiche) : **on ne trace pas**, les points repartent de zéro quand elle est stable | 4711-4725 |
| « Arrivé » | `x > a.x + 0,66 × (b.x − a.x)` (soit > 245,2) → vibration 14 ms, zone `.atteint` (voile amande à 16 %) | 4747-4751 |
| La lenteur | vitesse < **40 px/s** cumulée pendant plus de **300 ms** → `lent = true`, vibration 10 ms, trait de 5 au lieu de 8 | 4731-4739, 4652 |
| Validé au lever | `arrivé` **OU** (`lent` ET plus de 6 points) **OU** parcouru en x **> 0,5 × 390** | 4759-4762 |
| Retour haptique | 6 ms à la pose, 14 ms à l'arrivée, `[12, 40, 26]` à la validation | 4726, 4748, 4767 |
| Remise à zéro | 330 ms après le lever | 4782 |

**Le tracé libre** (visible seulement là où le canevas l'est) : chaque point devient le milieu d'une **courbe quadratique**
(`quadraticCurveTo(p[i], milieu(p[i], p[i+1]))`), trait de 8, bouts ronds (`app.html:4652-4668`).

> **Il n'y a AUCUNE tolérance de distance au tracé.** « L'arrivée se juge sur X seulement : la hauteur change quand l'espace
> s'ouvre, et exiger une position verticale précise rendrait le geste impossible. Le couloir occupe toute la hauteur. »
> « On valide dès les DEUX TIERS parcourus : exiger le dernier pixel rendait le geste anxieux. » « Rien ne doit échouer par
> surprise », « rien ne gronde : tout se referme doucement » (`app.html:4743-4746`, `4757-4758`, `4775`).
> **⚠ TROU :** distance maximale à l'onde — le prototype n'en a pas (cherché : `_tenirInit`, `planterZone`, `redteam_geste.py`).
> `TRAIT-PERSONNALISE-CONCEPT.md` §2.3 parle d'une « bande d'acceptation » : c'est une piste du concept, pas un fait du code.

**À la fin** (`app.html:4763-4772`) : la trace est gardée (`cur.trace = points`, `window._traceTenir`) puis clic sur
`#segStatus button[data-st="tenu"]`, dont le gestionnaire (`app.html:3764`) pose `cur.status = 'tenu'`, `cur.draft = false`,
régénère une parole récurrente (`regenRecur`), écrit au Fil (`feedAdd('kept', 'Tu as tenu « … »')`) et repeint la fiche
(`renderDetail`). Les écrans abonnés suivent (`window._paroles`, CLAUDE.md §3 bloc v130, C-049).

### 3.1 · L'instant — amande 1 000 ms, puis « juste après »

**Code :** `lot-S5`, `app.html:19606-19990`. **Ce n'est pas un mouvement : ce sont deux changements d'état**
(CLAUDE.md §3, bloc v124). Il ne joue ni sur un Cercle ni sur une fiche fermée (`app.html:19913-19914`).

| Écran | Champ | Trait | Dalle | Mots |
|---|---|---|---|---|
| `arrive` — l'autre part arrive | la nature | `#DD4D23` plein 0 → 195, chevron, points ; par-dessus, la moitié de l'autre en amande de 195 jusqu'à `_instantX` (268 sur le cadre) | 180 × 150 à (105, 91) | « l'autre part arrive », centré, y 388 |
| `referme` — le trait se referme | **amande `#8FE08F` pleine** | encre `#201908`, plein 0 → 390 | **228 × 190** à (81, 88) | « tenue. » (Gilbert 64 px, interlettre −0,04 em, y 388) et son mot (20 px, y 479) |
| `apres` — juste après | la nature | amande, plein 0 → 390 | 180 × 150 à (105, 91) | Noyaux y 388, à-qui y 515, titre y 546, quand y 614 |

(`app.html:19633-19652`, `19580-19594`.)

**La chronologie** (`_instantTenue`, `app.html:19911-19935`, horloge `performance.now()` + `requestAnimationFrame`) :

```
t = 0        l'instant est armé EN CAPTURE du clic « tenu » (avant que la fiche se repeigne) → écran « referme »
t ≥ 320 ms   le contenu de la fiche (titre, Noyaux du nouvel état) se remplit dans une image calme ; les Noyaux restent cachés
t ≥ 1 000    → écran « apres » (le champ revient à sa nature)
t ≥ 1 700    fin : le travail remis part en morceaux, une tâche par morceau, une image entre deux (`_enFond`)
garde-fou    3 000 ms : rien ne reste suspendu si l'affichage s'arrête
reprises     à 60, 200 et 600 ms de chaque écran, SEULEMENT si la dalle n'a pas pu être peinte
```

**Les deux dalles de l'instant sont rendues à l'avance** (`prechauffe`, 900 ms après l'ouverture d'une fiche à tenir, jamais
pendant un tracé ni une plantation ; 120 ms entre les deux — `app.html:19941-19957`, `19986`).
**Budget décidé** (`redteam_fluide.py`, CLAUDE.md §3 bloc v124) : aucune image au-delà de **20 ms** de travail du fil principal,
**p95 ≤ 16,7 ms**, la durée (1 000 ms) et les deux états inchangés. Après l'animation, la plus longue tâche : 22 ms (Q379, v125).

**Les couleurs** (Q269, CLAUDE.md §3 bloc du 23 sept. ; v124 ; v29/Q310) : sur la terre `#2B1020` d'une parole tenue, **le tenu
est l'amande, en clair comme en sombre** — texte crème, mention « TENU(E) » en amande ; sur un fond clair le tenu reste
`#00341A`. L'amande ne peint que la célébration et cette mention.

---

## 4 · TRACER SA MOITIÉ — mode moitié, mode complet, chevron, points

Il n'y a pas de troisième geste : **c'est le même tracé (§2, §3), et la moitié est une règle de DESSIN** (§1.3).

- **Mode moitié** — un Promi, un Chiche : celui qui donne sa parole trace de 0 à 195 ; l'autre viendra à sa rencontre.
  Chevron au milieu, points au-delà : ils disent la moitié qui MANQUE.
- **Mode complet** — une parole tenue, un Cercle lancé : 0 → 390, ni chevron ni points.
- **Mode duo** — un Chiche tenu à deux : deux pleins séparés d'un jour de 8 au milieu.
- **Rien n'est tracé** — un gardé de côté, la page + au repos : amorce effilée, chevron à 42,9, points.

**L'arrivée de l'autre moitié** est l'écran `arrive` de l'instant (§3.1) : la sienne monte en amande de 195 jusqu'où elle en est.
**⚠ TROU :** dans le prototype `_instantX` est une constante de cadre (268, `app.html:19622`) ; aucun geste réel d'une autre
personne ne l'alimente (il n'y a pas de serveur). Le protocole des deux moitiés entre deux appareils n'est pas écrit
(cherché : `_instantX`, `type:'moitie'` — une simple entrée du Fil, `app.html:21381`).

**Le trait de validation personnalisé (C-045)** : concept seul, rien n'est construit. S'il est retenu, le chemin est une DONNÉE
de la parole (une liste de points lissés), jamais une image (`TRAIT-PERSONNALISE-CONCEPT.md` ; `portage/A-INTEGRER.md`).

---

## 5 · DESSINER — `lot-V132-DESSIN` (`app.html:38022-38340`)

### 5.1 · Les données — une liste de traits, jamais une image

```
dessin = { v:1, w:390, h:<hauteur de la surface>, fond:<hex>, traits:[…], poses:[…], pose:bool, masque:bool }
trait  = { c:<hex> (vide pour la gomme), t:<taille en points>, g:0|1 (gomme), pts:[x, y, t, p,  x, y, t, p, …] }
           x, y  arrondis au dixième de point, sur la surface 390 × h
           t     l'heure de l'événement, en ms entières (e.timeStamp)
           p     la pression d'un stylet, arrondie au centième ; −1 pour un doigt
```
`traits` = le dessin en cours (gardé si l'on sort) ; `poses` = ce que POSER a posé (la bande, la vue entière et le partage ne
montrent que lui). Chaque trait garde SA couleur. Rangé sur la parole (`p.dessin`), sur le brouillon de la page +
(`_phrase.dessin`) ou par Cercle (`localStorage promi_dessins_cercle`) — `app.html:38060-38070`.

### 5.2 · La mise en page du mode (`window._dessinParams`, `app.html:38036-38049`)

`RANGEE_H` 44 · `SECU_BAS` 34 · `MARGE_BAS` 12 · `MARGE_HAUT` 12 · `MARGE_COTE` 24 · `PAS_OUTIL` 58 · `POSER_L` 104 ·
`ECART_DEPLOI` 16 · `BANDE_RETRAIT` 7 · œil `{x:24, ecart:52}`.
**Hauteur de la surface** = `844 − 34 − 12 − 44 − 12 = 742` (`surfH`, `app.html:38051`). Rangée à `y = 754`.
En Swift : la rangée est centrée entre la surface et le bord bas utile (`safeAreaInsets.bottom`) — `portage/A-INTEGRER.md`, v133.

> ⚠ **Divergence.** CLAUDE.md (bloc v132) écrit `MARGE_BAS` 34, `ECART_DEPLOI` 8, surface 390 × **754**, « pas de bouton de
> sortie (Q392) ». Le code, depuis v133 (commit `ceac9ac`, `CHANTIERS.md` C-042, C-056, C-061), porte `MARGE_BAS` 12 +
> `SECU_BAS` 34, `ECART_DEPLOI` **16**, surface **742**, un **✕ « Quitter le dessin »** dans le contour, et les couleurs du trait
> et du fond derrière le mur de Ma Parole !. **Le code fait foi.**

### 5.3 · Le geste (`debut`, `bouge`, `fin` — `app.html:38264-38274`)

- **`debut`** (`pointerdown`) : refuse un second pointeur et un bouton autre que le principal ; replie ce qui est déployé ;
  capture le pointeur ; crée le trait `{c, t, g, pts}` avec la couleur et la taille courantes ; ajoute le premier point.
- **`bouge`** (`pointermove`, même pointeur) : **ajoute chacun des événements regroupés** (`getCoalescedEvents()`, à défaut
  l'événement), horodatés à **`e.timeStamp`** ; un point à moins de **0,3** en x ET en y du précédent est ignoré ;
  la peinture est demandée **une fois par image** (`requestAnimationFrame`).
- **`fin`** (`pointerup` / `pointercancel`) : le trait est gardé s'il a au moins un point (4 valeurs) ; il est ajouté à
  `traits`, peint dans le calque de fond, **sauvegardé aussitôt** ; la rangée est rebâtie (ANNULER s'allume).
- Le défilement du système est coupé sur la surface (`touchstart`/`touchmove` annulés, `app.html:38187`).
- Un point isolé se peint en disque de diamètre `max(1, taille)`.

### 5.4 · Le trait « stylet » — l'effilé E2 (`cr`, `largeurs`, `traceUn` — `app.html:38085-38107`)

1. **Lissage** : spline de Catmull-Rom uniforme passant par les points, **6 subdivisions par segment (3 au-delà de 240
   points)** ; l'heure et la pression sont interpolées linéairement.
2. **Largeur en chaque point** `w = max(1, taille × k)`, avec, pour une plume (jamais pour la gomme) et si la longueur
   développée `L ≥ 3,2 × taille` :
   ```
   u = abscisse curviligne / L
   début (u < 0,20)       k ×= 1 + 0,38 · (1 − u/0,20)²            → +38 % au départ
   vitesse                k ×= borne(1,06 − 0,42 · v ; 0,72 ; 1,06)   v en points par ms, sur la fenêtre des points i−3 … i+3
                                                                    → jusqu'à −28 % quand le geste est rapide
   fin (u > 0,75)         k ×= ((1 − u) / 0,25)^0,85                 → effilée sur le dernier quart
   ```
   puis, toujours : **pression** `k ×= 1` pour un doigt (`p < 0`), `min(1,35 ; 0,55 + 0,9 · p)` pour un stylet.
   **Jamais sous 1 point.**
3. **Rendu** : un polygone PLEIN (bord gauche puis bord droit, normale = perpendiculaire à la corde des voisins), plus un
   disque de diamètre `w` en chaque point — ni trou dans les virages serrés, ni bout carré. Opaque, contours nets.
4. **La gomme** : le même tracé sans effilé, en `destination-out` (elle rend le fond, elle ne peint pas une couleur).

| | Fin | Moyen | Gros | Ligne |
|---|---|---|---|---|
| Plume (`TAILLES`) | 2,5 | 4,5 | 8 | 38045 |
| Gomme (`TAILLES_GOMME`) | 10 | 18 | 30 | 38046 |
| Les trois points du choix (diamètres affichés) | 6 | 10 | 16 | 38231 |

### 5.5 · Les outils (rangée A, `app.html:38210-38258`)

`PLUME · GOMME · ANNULER · COULEUR · POSER`, à `x = 24 + n × 58`, POSER large de 104 calé à droite.
- **Plume / Gomme** : un toucher choisit l'outil ; **un second toucher sur l'outil déjà choisi** déploie ses trois tailles
  (44 au-dessus de la rangée moins `ECART_DEPLOI`), qui se replient dès le choix fait.
- **ANNULER** : retire le dernier trait de `traits` (un trait de gomme compris), sauvegarde, repeint ; éteint s'il n'y en a pas.
- **COULEUR** : onglets TRAIT et FOND (FOND disparaît après le premier POSER) ; la teinte du trait égale au fond est
  désactivée. **Après le premier POSER le fond est fixé et les nouveaux traits ne prennent que les couleurs déjà présentes.**
  Sans Ma Parole ! : on dessine à l'encre du mode, le panneau est un mur (`app.html:38205`, `38236`).
- **POSER** (`sort(true)`) : s'il y a des traits, `poses = copie de traits`, `pose = true`, `masque = false` ; sinon le dessin
  est retiré. **Tout revient sans fondu** ; la fiche dessous n'a pas été touchée (le mode est une couche pleine).
- **Sortir sans poser** (`sort(false)` : ✕, Échap, l'offre qui passe par-dessus) : le dessin en cours est GARDÉ.
- À la sortie : `_ficheTrait()` ou `_ppTrait()`, puis `bandes()` (la bande montre le dessin posé à la place de la dalle ou de la
  photo, calé en haut, découpé à 7 au-dessus de l'axe du trait d'état).

Juge du prototype : `redteam_dessin.py` (couleurs figées, masquage hors partage, aucun outil sur la surface, retour exact,
joignabilité et VoiceOver, les entrées ; sondes `--sonde=`). En Swift : `PKCanvasView` ne convient pas tel quel (couleurs
figées, effilé E2, gomme qui rend le fond) — un rendu à soi (`portage/A-INTEGRER.md`, C-042).

---

## 6 · Les gestes de navigation qui ont des seuils

### 6.1 · Toucher une dalle de la Toile (`app.html:6719-6779`)

| | Valeur | Ligne |
|---|---|---|
| Déplacement qui fait d'un appui un geste | > **12** en x ou en y pendant le mouvement | 6741 |
| Déplacement toléré au lever | ≤ **14** en x ET en y | 6756 |
| Durée maximale d'un toucher | **700 ms** | 6755 |
| Autre doigt encore posé (`_fingers > 0`) | ce n'est pas un toucher | 6754 |
| Deux doigts à la pose (`_fingers > 1`) | c'est un pincement : jamais un toucher ni un appui long | 6726 |
| Ouverture différée de la fiche | **260 ms** (le temps de savoir s'il vient un second toucher) | 6772 |
| Double toucher | second lever à moins de **320 ms** et moins de **30** du premier → `Toile_recadre()`, l'ouverture en attente est annulée | 6765-6767 |

Le point touché est ramené en coordonnées de la Toile puis passé à `Toile.hit(x, y)` — **la même règle pondérée que le rendu**
(`distance − poids`, SPEC-RENDU §a). Une dalle de Cercle ouvre `openEssaim(clé)`, une dalle de parole `openDetail(id)`.
L'appui long de 480 ms n'ouvre plus rien (Q212 : son minuteur reste inerte, `app.html:6729-6737`).

### 6.2 · Pincer, glisser, recadrer (`promi-moteur.js:6123-6176`, `6682-6688`, `7889-7913`)

| | Valeur |
|---|---|
| Bornes du zoom | `ZMIN` **0,72** · `ZMAX` **5** |
| Au-delà des bornes, pendant le pincement | résistance : `borne × (brut / borne)^0,3` |
| Glissé au-delà des bords | élastique : 35 % du dépassement (`_rub`) |
| La vue appartient à la main | dès **10** de glissé cumulé, ou au premier pincement (`_vueMain`) |
| Élan au lâcher | vitesse sur les **100 dernières ms**, à l'heure de l'événement ; lancé si > **60 pt/s**, plafonné à **2 400 pt/s** ; il faut plus de 8 ms d'historique |
| Décroissance de l'élan | `exp(−4,2 · dt)` ; `exp(−16 · dt)` en plus hors bornes ; arrêt sous 12 pt/s |
| Retour dans les bornes / vers la vue visée | ressort sur le TEMPS : `1 − exp(−7,5 · dt)` |
| Zoom par défaut | `n < 20` paroles : `min(1,1 ; 1 + (20 − n) × 0,005)` ; sinon 1 — jamais sous 1 |
| Les encarts s'effacent en dézoomant | voile de 1 à 0 entre un zoom de 0,88 et 0,74 |
| Ce qui ramène la vue par défaut | le rond « recadrer », le double toucher, une dalle créée ou supprimée — en douceur |

Le zoom persiste d'une page à l'autre (CLAUDE.md §3, v46 ; juge `redteam_zoom.py`).

### 6.3 · Appui maintenu sur un bandeau du Fil (`app.html:19363-19381`)

**480 ms** d'appui déplient la rangée d'actes de CE bandeau (« TENIR · REPORTER »), ou la replient ; un toucher bref ouvre sa
fiche. Annulé au lever, à la sortie, à l'annulation, ou à un mouvement de plus de **3** entre deux événements
(`movementX/Y`). C'est un « ajout validé, hors inventaire » : au repos, le bandeau est celui du cadre 76 (CLAUDE.md §5).

### 6.4 · Le geste de couleur du Studio (`app.html:34099-34219` ; `redteam_studio_geste.py`)

| | Valeur |
|---|---|
| Appui maintenu | **480 ms** (`MAINTIEN`) sans avoir bougé de plus de **12** |
| Horizontale → la teinte | **390** de course = 360° (`COURSE`) |
| Verticale → la palette | **48** par palette (`PAS_PAL`), liste **circulaire** (24 palettes) |
| Sensibilité (Q125) | la valeur se calcule depuis l'ORIGINE du geste, jamais en cumulant : on revient exactement d'où l'on vient |
| Glissement de MONDE (qui garde la main) | part dès **34** d'horizontale, si `|dx| > 1,3 × |dy|` (`app.html:6682`) |
| Invite | « reste appuyé pour changer de couleur » (mot « à valider ») |

Le geste doit marcher **doigt parti à la verticale ou en diagonale** : dans le prototype, le défilement du navigateur le
reprenait (`touch-action: pan-y`) — en UIKit, le reconnaisseur du geste de couleur doit l'emporter dès qu'il est armé.

### 6.5 · Le toucher d'un mur de Ma Parole ! (`app.html:37217-37231`)

Un toucher = appui puis lever **à moins de 10** de distance et **moins de 600 ms**. La phrase paraît ; un nouveau toucher à
moins de **450 ms** de sa montée ne l'emporte pas ; ensuite un toucher n'importe où ouvre l'offre. Durée de lecture :
`borne(1 400 + 60 × caractères ; 3 000 ; 5 500)` ms (`app.html:37192`). Un mur se reconnaît à sa GÉOMÉTRIE (le point tombe
dans son rectangle) : le réglage flouté ne reçoit pas le doigt.

### 6.6 · La caresse de la Pelote (`app.html:29421-29436`, `30673-30846`)

| Constante | Valeur | Sens |
|---|---|---|
| `AUTO` | `2π / 100` rad/s | la rotation de repos, un tour en 100 s (voir la divergence, SPEC-RENDU §c) |
| `SENS` | `0,011 × 142 / R` rad par point | la surface suit la main (R = rayon de la boule, 116 pt) |
| `TAP` | 6 | parcours sous lequel le geste est un toucher |
| `DOUBLE` | 350 ms | deux touchers rapprochés : tout se relisse |
| `VMAX` | 11 rad/s | plafond de l'élan |
| `TAU` | 0,55 s | décroissance de l'élan (`exp(−dt/τ)`), éteint sous 0,0008 rad/s |
| `TANG`, `TANGMAX` | 0,32 · 1,15 | le tangage et sa borne |
| `CEDE`, `CEDE_TAU`, `RESISTE_TAU` | 0,62 · 0,05 s · 0,50 s | l'empreinte cède vite (62 %), puis résiste |
| `PROF` | 0,46 | profondeur du creux = 0,46 × le demi-axe de la pulpe |
| `REPOUSSE_TAU` | 0,15 s | la matière repousse le doigt parti ; creux effacé en ≈ 0,95 s |
| `EMP_FIN` | 0,0004 | l'empreinte se retire quand le creux est à ce reste |
| `W`, `TRACES` | 0,27 rad · 48 | largeur d'une caresse (le diamètre du doigt) ; nombre de traces gardées |
| `PULPE` | pouce `[46,4 ; 0,70]`, index `[30,0 ; 0,73]` | bornes du demi-axe (points) et allongement du contact |
| `TOUR_TAU` | 1,1 s | le tour que fait la Pelote pour présenter une parole de plus |

- **La taille de l'empreinte** se lit sur la surface de contact (`width`/`height` du pointeur), bornée entre l'index et le
  pouce ; sans capteur : le pouce. Elle suit pendant l'appui (lissage 0,35), s'oriente dans le sens du geste (lissage 0,45),
  s'étire en glissant jusqu'à 0,72 × l'allongement (`app.html:30699-30727`).
- **Le poil se couche** : un arc posé au point touché tous les **20** de geste, orienté comme le doigt ; un arc de plus quand
  le point touché s'est déplacé de **0,6 rad** sur l'objet (`app.html:30764-30779`).
- **L'élan** (chantier 73, `app.html:30800-30833`) : fenêtre `FEN = max(90 ms ; 3 × la cadence médiane des derniers mouvements)` ;
  un doigt qui s'ARRÊTE avant de lâcher (attente > `FEN` entre le dernier mouvement et le lâcher) ne lance pas ; la vitesse se
  prend sur la **durée des mouvements** (somme des pas de temps), pas jusqu'au lâcher ; il faut plus de 12 ms.
- **La trace s'inscrit au repos**, jamais au lâcher (doigt levé, élan éteint, creux refermé) ; un simple toucher l'inscrit au
  lâcher (il n'a pas d'élan à saccader).
- **Toucher un Noyau** de l'Aura : parcours + défilement de la rangée ≤ `TAP` (6) → ouvre la personne (`app.html:30849-30862`).

### 6.7 · La Pelote déplaçable dans Mon Folio (`lot-V15`, `app.html:35240-35315`) — et l'ancien geste du Noyau

- **Appui long 380 ms** (`LONG`) sur la Pelote, doigt IMMOBILE : un mouvement de plus de **8** (`TOL`) avant la fin de l'appui
  ne prend rien (il glisse). Prise : vibration 8 ms. Elle se déplace **case par case** (le centre du bloc 2 × 2 au plus près
  du doigt), la planche se recompose autour ; rien ne se superpose. Juge : `redteam_pelote_partage.py` (SPEC-JUGES §4).
- **L'ancien geste du Noyau** (« Ma Toile », `app.html:3975-4050`) : appui long **260 ms** (il ne s'annulait pas au mouvement —
  c'est le défaut que v15 corrige) ; position bornée x 0,12–0,88, y 0,10–0,90 ; **deux aimants** en y — le centre (0,5) et la
  ligne du QR (0,84) — à **24** près, seulement au-dessus de **40 px/s** ; dans le Folio, le bloc change de case, mouvement
  adouci sur **420 ms** (`1 − (1 − t)³`).
  ⚠ **TROU :** ce geste est-il encore joignable ? Depuis v15 la Pelote ne s'ajoute plus sur « Ma Toile » ; le code du Noyau
  reste chargé et `redteam_geste.py` le juge encore, mais aucune décision ne dit s'il se porte (cherché : CLAUDE.md, `lot-V15`).

### 6.8 · Autres seuils lus

| Geste | Seuil | Ligne |
|---|---|---|
| Ouvrir Peaufiner par un geste vers le bas (hors fiche d'un Cercle) | doigt remonté de **26**, ou moins de 60 de défilement restant | `app.html:5054-5066` |
| Fiche d'un Cercle | Peaufiner ne s'ouvre QU'EN TOUCHANT SA BARRE ; le doigt fait défiler le fil | CLAUDE.md §5 (§13) |
| Pincer l'Index (colonnes) | un pas tous les 18 % : rapport < 0,82 ou > 1,22 | `app.html:4434-4448` |
| La barre Peaufiner et son rond Partager | toucher = appui puis lever sans glisser, **< 10, < 600 ms** | CLAUDE.md §8 |
| Jauge de teinte du Studio (élan) | décroissance ×0,92 par image, arrêt sous 0,0006 | `app.html:6704` — ⚠ par image, voir §7 |

---

## 7 · CE QUI DOIT ÊTRE MESURÉ AVEC `UITouch.timestamp` ET `coalescedTouches`

### 7.1 · Ce que le prototype lit DÉJÀ à l'heure de l'événement — à porter tel quel

| Geste | Ce qu'il lit | Ligne |
|---|---|---|
| **Dessiner** | `e.timeStamp` de chaque point, **tous** les événements regroupés (`getCoalescedEvents()`), la pression du stylet | `app.html:38260-38267` |
| **Caresse de la Pelote** | `e.timeStamp` de chaque mouvement regroupé, le **pas de temps** de chacun (`hD`), l'heure du lâcher | `app.html:30736-30754`, `30783` |
| **Glissé de la Toile** | `e.timeStamp` de chaque `pointermove` (historique de 100 ms) | `promi-moteur.js:7892`, `7904` |

En Swift : `touch.timestamp` pour chaque `UITouch` de `event.coalescedTouches(for:)` ; `touch.force / maximumPossibleForce`
pour le stylet ; `touch.majorRadius` pour la surface de contact de la Pelote.

> ⚠ **Le glissé de la Toile ne lit PAS les événements regroupés** (un seul point par `pointermove`). L'horodatage est juste,
> mais l'historique est plus pauvre qu'il pourrait. À porter avec `coalescedTouches`.
> ⚠ **Chromium peut cacher le défaut de la cible** : il regroupe les mouvements et les rend avec leurs heures d'origine ;
> **Safari n'a pas `getCoalescedEvents`** — sur iOS le prototype ne voit qu'un mouvement par appel. Toute mesure de geste faite
> sur le prototype doit l'être regroupement éteint (CLAUDE.md §8, « UN INSTRUMENT QUI RALENTIT… »). En Swift natif le
> regroupement existe : c'est LUI la référence, pas le comportement du prototype dans Safari.

### 7.2 · Ce que le prototype lit ENCORE à l'heure du TRAITEMENT — défauts à NE PAS porter

| Geste | Ce qui est lu au traitement | Conséquence sur un appareil lent | Ligne |
|---|---|---|---|
| **Tenir** — la « lenteur » | `Date.now()` dans `bouge` : vitesse = distance / (maintenant − dernier traitement) | des mouvements livrés groupés après une image lente tombent au même instant : vitesse fausse, `lent` armé ou raté à tort | `app.html:4730-4740` |
| **Tenir** — l'ouverture | `Date.now() + 340` pour la fin de l'ouverture pendant laquelle on ne trace pas | les 340 ms se comptent en temps de traitement ; des points réels du doigt sont jetés | `app.html:4711-4725` |
| **Tenir / Planter** — le tracé | un seul point par `touchmove` (`e.touches[0]`), **aucun point n'est horodaté**, aucun regroupement | la trace gardée (`cur.trace`) n'a pas d'heures ; sous charge elle est anguleuse | `app.html:4693-4697`, `4741` ; `12734-12738` |
| **Toucher une dalle** | `Date.now()` à la pose et au lever (700 ms), au double toucher (320 ms) ; `setTimeout(260)` | un lever traité en retard dépasse 700 ms : le toucher est perdu ; le double toucher rate | `app.html:6727`, `6755`, `6764-6772` |
| **Geste de couleur du Studio** | `setTimeout(480)` armé au traitement du `pointerdown` | l'appui mûrit en retard si le fil est occupé | `app.html:34176-34183` |
| **Appui maintenu du Fil** | `setTimeout(480)` ; annulation sur `movementX/Y > 3` ENTRE deux événements, pas sur la distance à l'origine | un glissé lent ne l'annule jamais ; un mouvement regroupé l'annule à tort | `app.html:19366-19381` |
| **Toucher d'un mur** | `performance.now()` au traitement de la pose et du lever (600 ms) | idem toucher d'une dalle | `app.html:37227-37229` |
| **Ancien geste du Noyau** | `performance.now()` dans `pointermove` pour la vitesse (seuil des aimants, 40 px/s) | vitesse fausse sous charge : l'aimant prend ou lâche à tort | `app.html:4010-4013` |
| **Pelote du Folio** | `setTimeout(380)` | l'appui mûrit en retard | `app.html:35274-35281` |
| **Jauge de teinte du Studio** | élan décroissant de ×0,92 PAR IMAGE, vitesse lissée par événement | l'élan dure plus longtemps quand les images ralentissent | `app.html:6704-6707` |
| **Pelote** — naissance de l'empreinte | `EMP.t0 = performance.now()` à la pose (le reste du geste est à l'heure de l'événement) | écart de quelques ms entre l'heure du contact et celle de l'empreinte | `app.html:30735` |

**La règle pour le portage :** toute durée de geste (700 ms, 600 ms, 480 ms, 380 ms, 320 ms, 300 ms) se compte entre
`touch.timestamp` de la pose et `touch.timestamp` de l'événement jugé ; toute vitesse se calcule sur la somme des pas de
temps des touchers regroupés ; un minuteur d'appui long se vérifie à son échéance contre l'heure du dernier toucher reçu
(ou se confie à `UILongPressGestureRecognizer`, `minimumPressDuration` et `allowableMovement` aux valeurs ci-dessus).

### 7.3 · Le cas d'école — la fenêtre d'élan de la Pelote (chantier 73)

La fenêtre était figée à **90 ms** : « cinq mouvements à 60 images par seconde, une hypothèse de machine rapide déguisée en
durée ». Dès **120 ms** d'écart entre deux mouvements, l'élan sortait à **0,00 rad/s** (neuf essais sur neuf), contre
11 rad/s à cadence normale. Parade en place : la fenêtre suit la cadence observée (`max(90 ; 3 × médiane)`), et la vitesse se
prend sur la durée des mouvements. Elle n'a de sens que parce que chaque mouvement porte **son** heure
(`app.html:30800-30833` ; CLAUDE.md §8, tableau des chantiers 75 et 73).

---

## 8 · Les juges du prototype qui portent ces règles

| Juge | Ce qu'il porte en dur |
|---|---|
| `redteam_geste.py` | le geste du Noyau au partage (13 contrôles ; un contrôle de pixels y oscille — CLAUDE.md §7) |
| `redteam_studio_geste.py` | appui 480 ms, 390 = un tour de teinte, 48 = une palette, retour exact, départ vertical et diagonal |
| `redteam_dessin.py` | couleurs figées, masquage hors partage, aucun outil sur la surface, retour exact après POSER |
| `redteam_fluide.py` | tenir : aucune image > 20 ms de travail, p95 ≤ 16,7 ms, 1 000 ms d'amande, deux états |
| `redteam_pelote_partage.py` | appui 380 ms, tolérance 8 |
| `redteam_pelote_doigt.py` | sous le doigt, image p95 ≤ 22 ms au banc WebKit, ΔE00 ≤ 2 contre le peintre |
| `redteam_zoom.py` | le dézoom tient, planter ne reprend pas la vue, recadrer (rond et double toucher) |
| `redteam_murs.py` | le toucher d'un mur, la durée de lecture, le compteur |
| `redteam_tuiles.py`, `redteam_gens.py` | les choix de la page +, au vrai doigt |

Le portage ne reprend pas Playwright : il reprend ces règles (`SPEC-JUGES.md`, en-tête).
