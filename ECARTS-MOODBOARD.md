# Écarts moodboard ⟷ app — relevé vérifié

**Deux fichiers vont ensemble :**

- **`MOODBOARD-VALEURS.md`** — l'arbre complet des neuf écrans, extrait
  automatiquement, sans interprétation. **C'est la source de vérité.**
- **ce document** — les écarts constatés, avec la **cascade CSS de `app.html`
  réellement résolue** (spécificité, `!important`, ordre du fichier calculés).
  Chaque ligne « App » est la valeur qui gagne à l'écran.

En cas de doute, `MOODBOARD-VALEURS.md` l'emporte : il n'est pas écrit par moi,
il est extrait du fichier.

---

## 0 quater · UN ÉCART ASSUMÉ — LE COMPTE DE L'INDEX (cadre 72)

**Le cadre 72 écrit « Index 12 », gardés de côté compris. Le produit s'en écarte** (décision Tom, 13 sept. 2026, Q212) :
un même objet ne donne jamais deux chiffres selon l'écran. L'accueil et l'Index comptent la même chose —
**N paroles** (Promi et Chiche plantés, dans une Nuée ou non) **· N Nuées** (toutes, vides comprises : une Nuée est
un contenant, pas une somme). Les gardés de côté restent listés dans l'Index, ils ne sont plus comptés.
Un juge qui exige « 12 » encode la règle abandonnée : il se réécrit au niveau de cette décision (§7).

**Et le cadre 74 aussi** : il dessine « l'atelier du samedi », une Nuée sans Promi, en gardé de côté. Décision Tom du 13 sept. (Q213) : une Nuée vide reste une Nuée — champ et trait pleins. Q83 ne vaut plus que pour un Promi gardé de côté.

## 0 ter · UN ÉCART ASSUMÉ — LES CADRES 84-87 ET LA RANGÉE « LE TRAIT »

> **Décision Tom, 2 septembre 2026.** *« Le décalage est accepté. Les cadres 84-87 ne sont
> plus superposables sur ce point, c'est un ajout demandé. Note-le comme écart assumé, pas
> comme erreur de dessin. »*

**Ce n'est pas une erreur du moodboard, et ce n'est pas une dérive de l'app.** C'est une
**fonction ajoutée après le dessin** : le pinceau se reprend depuis Peaufiner, **haut de
liste**, sur une fiche comme sur une Nuée (Q128, Q156). Les cadres 84 à 87 dessinent le
Peaufiner d'une Nuée **avant** que cette fonction existe.

**Ce qui bouge, et rien d'autre.** Une carte « LE TRAIT » de 342 × 118 vient en tête de la
page 1 ; les quatre cartes qui la suivent descendent de **134** (118 + l'écart de 16 que les
cartes ont déjà entre elles) :

```
                cadres 84-87      l'app, depuis le 2 septembre
LE TRAIT             —                     110   (h 118)
DESCRIPTION         110                    244
MEMBRES             230                    364
PIÈCES JOINTES      310                    444
COMMENTAIRES        418                    552
DISSOUDRE LA NUÉE   884 (page 2)           884   inchangé
```

La page 1 finit à **656** pour 760 : rien ne déborde, l'écart de 16 est tenu partout.

**Pourquoi 118 et pas 64, alors qu'une fiche prend 64.** Les cartes d'une Nuée sont en
**position absolue, à cote fixe** : une rangée qui se déplie recouvrirait la suivante, ou
obligerait à déplacer quatre cartes en JavaScript à chaque doigt. La carte porte donc son
rail **en permanence**, dans la hauteur haute que le cadre emploie déjà pour une NOTE.

**Ce que ça oblige :** `redteam_nuee` connaît le décalage (+134 sur les quatre cartes) et
`releve-S2` la rangée en tête. Les deux originaux sont dans `sauvegardes/`. Un contrôle qui
attendrait encore 110 pour DESCRIPTION est **périmé**, pas l'écran.

**Le §5 de `CLAUDE.md` dit qu'un ajout hors inventaire « ne décale AUCUNE cote du cadre ».**
Cette règle vise un ajout qu'un **geste** fait paraître et qui se referme. Ici la consigne est
postérieure et explicite : une rangée permanente, demandée en tête de liste. Les deux ne se
contredisent pas — elles ne parlent pas de la même chose.

---

## 0 bis · DEUX CADRES DE LA PLANCHE SONT DES ERREURS DE DESSIN

> **Décisions Tom, 29 août 2026 (Q83 et Q84).** Le moodboard fait foi — mais un cadre qui
> contredit une **loi vérifiée sur six points** ou une **règle de produit déjà tranchée**
> est un dessin isolé, pas une règle. Les deux cas ci-dessous sont les seuls connus ;
> ils se citent, ils ne se généralisent pas.

### 0 bis.1 · Le cadre 58 donne une base que la loi du champ ne produit pas

`promi-nuee-toile.html` **fait foi pour la Nuée.** Ses six cadres donnent six points, et
tous les six tombent sur la loi du §9 :

```
n     =   0     1     2     3     4     7
base  = 460 · 374 · 288 · 202 · 176 · 176        base = max(176, 460 − 86 n)
```

**Le cadre 58 du moodboard H donne base 232 pour 6 Promi.** Aucun n ne produit 232
(il faudrait n = 2,65). C'est un dessin **antérieur à la loi**.

**Conséquence pour la mesure :** la fiche de Nuée se compare aux **cadres 10/11 de
`promi-nuee-toile`** (n = 7 → base 176, comme notre potager à 6). Elle y est à **5,1 %**
hors glyphe. Contre le cadre 58, on lisait 17 % — et ce n'était pas un défaut de dessin.

⚠ **Les DONNÉES du potager restent celles du moodboard H** (« 6 PROMI · 1 TENU » : arroser
tous les soirs, semer les radis), parce que l'Index et le Fil en dépendent — le cadre 72
écrit « 6 PROMI · 1 TENU », le cadre 76 « LE POTAGER · 6 PROMI ». C'est **la loi du champ**
qui vient de `promi-nuee-toile`, pas le contenu.

### 0 bis.2 · Le cadre 74 donne une dalle à un gardé de côté

Les cartes « gardé de côté » du cadre 74 portent une DALLE — 49 × 41 pour « l'atelier du
samedi », 43 × 36 pour « appeler Mamie ». **C'est une erreur de dessin.**

**Un gardé de côté ne pose RIEN sur la Toile, parce que rien n'a été promis.** Lui donner
une dalle voudrait dire la lui faire occuper une case — mesuré : syncer un gardé dans la
Toile lui donne bien une dalle, **et 119 relevés au `hit`**, c'est-à-dire qu'il est planté.
Ce serait contredire ce qu'est un gardé de côté.

**Ce que porte sa carte d'Index :** le champ de sa NATURE **en pointillé**
(`outline:2px dashed <natCol>`, `outline-offset:-2px`, le cadre l'écrit ainsi),
**sans matière**. Rien d'autre.

### 0 bis.3 · Le bouton ⇅ du cadre est en `content-box`, sa voisine en `border-box`

Mesuré au rendu, cadre 72 :

```
⌕ Rechercher   x 24  y 108   270 × 56   box-sizing: border-box     ← comme l'app
⇅              x 310 y 108    62 × 62   box-sizing: content-box    ← 56 + 2 × 3 de bordure
```

Deux contrôles voisins, même rangée, même bordure de 3 px — **et deux `box-sizing`
différents.** Le tableau du §5 écrit **56 × 56** pour les deux, l'app pose 56 × 56, et
`releve-S4` le valide. **Le document et l'app s'accordent contre un oubli de rendu.**
On garde 56. Coût mesuré au duo : un anneau de 3 px, ~0,2 % de l'écran.

---

### 0 bis.4 · Les libellés de réglage à 11,5 px — sous le minimum du produit

> **Décision Tom, 3 septembre 2026.** *« Les sept passent à 13. Ils doivent être identiques,
> et le §6 interdit 11,5. Ce n'est pas le cadre qui gagne, c'est la loi. »*

Les cadres 78 à 87 écrivent le libellé d'un réglage en **Apfel 500 / 11,5** — c'est aussi ce
que transcrivent le §3.3 et le §3.4 de `PROMI-SPECIFICATIONS.md`. **Le §6 de `CLAUDE.md` dit
l'inverse, et il fait autorité : « Tailles minimales : rien en dessous de 12 px ».** Un cadre
ne peut pas descendre sous le minimum du produit : c'est une **erreur de dessin**, de la même
famille que les cadres clairs au trait invisible (0 bis, cas 4 de la liste d'`ETAT-DES-LIEUX § E`).

**Ce que ça donnait à l'écran, et c'était pire qu'une valeur unique.** Les sept libellés de
Peaufiner sortaient à **deux tailles** :

```
                              avant      après
NOTE · COMMENTAIRES            13         13     dans une ZONE (§3.4) — pile verticale
DESCRIPTION (Nuée)             13         13
À QUI · AVANT · DANS UNE NUÉE  12         13     dans une RANGÉE (§3.3) — flex en ligne
PIÈCES JOINTES · RELANCER      12         13
```

**La cause n'était pas la feuille de style, c'était le plancher typographique.** Sa loi
(`max(13, taille)`, 2 septembre) posait bien 13 sur les sept ; **un repli le reprenait
aussitôt sur cinq d'entre eux**. Ce repli protège un texte qui, en grossissant, viendrait
recouvrir le bloc placé **sous** lui — mais son test comparait le bas du texte au haut du
**frère suivant**, sans vérifier que ce frère est bien dessous. Dans une **rangée flex**, le
frère est **à côté** : les deux boîtes se chevauchent verticalement par construction, la
condition est vraie d'emblée, et le repli redescendait le libellé jusqu'à sa butée de 12
sans qu'aucun recouvrement n'existe. Dans une **zone**, la pile est verticale : le repli ne
se déclenchait pas, et le 13 restait. D'où deux tailles pour sept libellés de même nature.

**Le correctif est géométrique, pas une classe :** le frère ne compte comme « dessous » que
s'il **commence dans la moitié basse de la boîte du texte, ou plus bas**. Une pile passe, une
rangée ne passe pas. Relevé : **24 nœuds du produit** étaient retenus à 12 par ce repli sans
avoir de voisin dessous — dont des libellés des Réglages, de l'Aura et du Cercle.

**Ce que ça coûte, et c'est la conséquence demandée :** `redteam_air` a compté **10 paires à
−1 px**, toutes entre deux libellés consécutifs. C'est le §8 mot pour mot — « une cote dérivée
n'est pas un espace » : le libellé a grandi d'un pixel vers le bas, le bloc suivant est à cote
fixe, l'air d'encre perd ce pixel. Les blocs, eux, n'ont pas bougé (`releve-S2` position 0).
Référence refigée.

**Contrat mis à jour :** `releve-S2-peaufiner.py` attend **13** au lieu de 11,5, tolérance
inchangée à 0,6. **Prouvé contre la version fautive : 36 écarts avant, 0 après.** Original
dans `sauvegardes/releve-S2-peaufiner-avant-libelles-13.py`.
⚠ **Une première sonde a été avalée** — une règle CSS à 11,5 posée en fin de fichier ne peut
rien contre l'inline `!important` que le plancher écrit. La preuve s'est faite en rejouant le
juge sur `sauvegardes/avant-libelles-13.html`, c'est-à-dire contre le vrai défaut.

---

### 0 bis.5 · L'air sous l'entête de l'Index et du Fil — 24 reportait l'air d'un TITRE NU

> **Décision Tom, 3 septembre 2026.** *« La ligne avec encart Rechercher et bouton tri, dans
> l'Index et dans le Fil, rapproche-la un peu de l'encart titre et ✕ fermer, sinon ça fait
> bizarre — ça remonte du tout les éléments en dessous un peu. »*

**Ce n'est pas un écart de report, c'est un report qui a cessé de valoir.** Le cadre 72 pose
le titre à `top 38, hauteur 34` (§3.1) — il finit donc à **84** — et la barre de recherche à
**108** : **24 px d'air**. Quand le plateau de 60 a remplacé le titre de 44 (Q147), la
colonne entière est descendue de 16 et le 24 a été reporté tel quel — barre à 124, liste à 212.

**Le report était faux, et il l'était en silence.** Le titre du cadre est du **texte nu** ; le
plateau est une **boîte bordée**. L'œil compte l'air à partir du **trait**, et le trait du
plateau descend là où l'encre du titre ne descendait pas : les 24 px se lisent alors comme un
trou, et la barre ne fait plus paire avec l'entête. C'est la même famille que « une cote
dérivée n'est pas un espace » (§8) — on a reporté un nombre là où il fallait reporter une
intention.

**La valeur n'est pas inventée : c'est l'écart de bloc du §3.3**, « écart entre deux réglages :
16 px » — celui que Peaufiner, les Réglages et le Cercle emploient déjà entre deux boîtes
bordées. Le plateau et la recherche portent la même grammaire de contours (2 px, rayon =
hauteur ÷ 2) : ce sont deux boîtes de la même famille, elles prennent son écart.

```
                        avant    après
la barre  .ix-bar        124  →   116        (l'air passe de 24 à 16)
la liste  #indexList      212  →   204        tout ce qui suit remonte de 8
le menu de tri .ix-sort   186  →   178
```

**Rien d'autre ne bouge** : largeurs (342 · 270 · 52), hauteurs (52), contours, rayons et
l'écart barre → liste (36) sont inchangés. Vérifié dans les deux thèmes et aux deux densités
de l'Index.

**Contrats mis à jour :** `releve-S4-index-fil.py` attend 116 et 204, tolérance inchangée à
3 px — **prouvé contre la version d'avant : 18 écarts, 0 après** (original dans
`sauvegardes/releve-S4-index-fil-avant-air-16.py`). `redteam_air` a compté **5 paires à −8**,
toutes « ✕ Fermer → ⇅ », c'est-à-dire le déplacement demandé et rien d'autre ; référence
refigée. `releve-design`, `redteam_superpo`, `redteam_ecrans` et `redteam_vide` sont
inchangés.

---

## 0 · Deux angles morts qui expliquent tout

### 0.1 L'outil ne voit que six écrans sur neuf

`releve-moodboard.py` couvre `ph-0` à `ph-5`. **Le moodboard en contient neuf.**

| Écran | Contenu | Couvert |
|---|---|---|
| `ph-0` à `ph-5` | le parcours de création | ✅ |
| **`ph-6`** | **fiche · titre court (34px) · À TENIR** | ❌ |
| **`ph-7`** | **fiche · titre long (26px) · À TENIR** | ❌ |
| **`ph-8`** | **fiche · TENUE · avec le tracé du geste** | ❌ |

Le « zéro écart » est vrai sur ce qui est regardé, aveugle sur le reste.

### 0.2 L'erreur de méthode qui a tout contaminé

Au lot 1, la consigne était : *« la mesure fait foi »*. **La mesure de l'app**,
pas celle du moodboard. Le panneau du geste a donc été relevé sur la fiche
— 176 px, rayon 0 — et ces valeurs ont été prises pour référence.

**Elles étaient fausses.** Le moodboard dit **118 px, rayon 26**.

Conséquence aujourd'hui :

| | Moodboard | Page + | Fiche |
|---|---|---|---|
| Hauteur du panneau | **118px** | 118px ✅ | **176px** ❌ |
| Rayon | **26px** | 26px ✅ | **0** ❌ |
| Libellé | **13px / 800** | 13px ✅ | **17px** ❌ |

La page + a été corrigée par le relevé moodboard. La fiche est restée sur
l'ancienne mesure. **Les deux écrans ont divergé.**

**Règle à inscrire dans `CLAUDE.md` :** le moodboard fait foi. Une mesure prise
sur l'app ne fait jamais référence — elle constate un état, elle ne le valide pas.

---

## 1 · La fiche — `ph-6`, `ph-7`, `ph-8`

### 1.1 La tête — cascade résolue

| Élément | Moodboard | App (valeur qui gagne) | Écart |
|---|---|---|---|
| **Titre** | **34px** court · **26px** long · `line-height:1.06` · `letter-spacing:-.05em` | **54px** · `line-height:.98` · `letter-spacing:-.055em` | **+20px** |
| Règle de titre long | 26px, deux lignes, **hauteur de bloc inchangée** | aucune | **absente** |
| **« à Rachel »** | **17px / 700** · opacité **.78** · prénom en `<b>` opacité 1 | **25px** · opacité **1** | **+8px** |
| **Mot-marque « Promi »** | `position:absolute` `left:22px top:48px` · **20px** / 600 · opacité .9 | `.dpt-nat` **30px** · opacité .9 | **+10px** |
| **« À TENIR »** | **10.5px** · `ls:.16em` · **700** · `margin-top:13px` · opacité **.74** (À TENIR) / **.64** (TENUE) | `.dpt-quand` **12.5px** · `ls:.16em` · opacité **.66** | **+2px** |
| Padding du bloc | `24px 22px 24px` (À TENIR) · `24px 22px 20px` (TENUE) | **`24px 24px 30px`** | **+2 / +6** |
| **Filet sous le titre** | **aucun** | `.dpt-titre::after` — 3 à 6px de haut, 46 à 72px de large | **à supprimer** |
| FERMER | `right:22px top:50px` · 11px · `ls:.14em` · opacité .78 · **croix SVG** 13×13 stroke 1.8 | `✕ Fermer` en texte | **structure** |

**Le titre à 54px pour une cible de 34, c'est l'écart le plus visible.** C'est
lui qui « casse tout vers le haut et vers le bas ».

### 1.2 Le corps

| Élément | Moodboard |
|---|---|
| Conteneur | `flex:1 1 auto` · `padding:0 22px` · `min-height:0` |
| Carte message | `padding:17px 19px 4px` · `radius:20px` · fond `rgba(255,255,255,.15)` — sur Tenue : `rgba(6,35,26,.1)` |
| Entête de message | `RACHEL, HIER` · 10.5px · `ls:.14em` · opacité .78 · `margin-bottom:8px` |
| Le message | 15px · `line-height:1.5` |
| « répondre… » | 14px · opacité .55 · bulle SVG 17×17 stroke 1.8 · `gap:11px` · `padding:14px 4px 0` |
| Filet | `height:1.2px` · `rgba(255,255,255,.24)` — Tenue : `rgba(6,35,26,.2)` · `margin-top:10px` |

**Les pastilles — une seule ligne.** Le moodboard l'écrit deux fois, dans la note
et dans les corrections.

| | Moodboard |
|---|---|
| Conteneur | `display:flex` · `gap:7px` · `margin-top:12px` |
| Pastille | `padding:11px 15px` · `radius:999px` · **12.5px** · `white-space:nowrap` |
| Contour | `inset 0 0 0 1.3px rgba(255,255,255,.34)` — Tenue : `rgba(6,35,26,.26)` |
| Icônes | SVG 15×15 · stroke 1.8 · `gap:7px` |
| Libellés dans une Nuée | **`note` · `1` · `Famille`** |
| Libellés hors Nuée (`ph-8`) | **`note` · `1`** — deux seulement |

### 1.3 Le geste — les valeurs justes

| Élément | Moodboard | App | Écart |
|---|---|---|---|
| Enveloppe | `padding:22px 22px 12px` | — | |
| **Panneau** | **`height:118px`** · **`radius:26px`** · fond `rgba(255,255,255,.14)` | **176px** · **rayon 0** | **+58px** |
| Point gauche | `cx:42 cy:52 r:18` plein | r=19 | +1 |
| Point droit | `cx:266 cy:52 r:18` contour stroke 2.2 opacité **.45** · **plus** `r:6` plein opacité .45 | r=19 · opacité .40 | +1 · −.05 |
| **Libellé** | **« glisse pour tenir → »** · **13px / 800** · `bottom:14px` | **17px** · `bottom:26px` | **+4px · +12px** |
| Pastille | « bouton » · `right:14px top:12px` · 10.5px · opacité .5 · `padding:5px 11px` · `inset 0 0 0 1px currentColor` | 10.5px ✅ | |

### 1.4 La barre Peaufiner

| Élément | Moodboard | App | Écart |
|---|---|---|---|
| Hauteur | `62px` | `62px` | ✅ |
| Padding | **`0 22px`** | **`0 24px`** | **+2px** |
| **Taille** | **17px** | **22px** | **+5px** |
| Police | Bricolage 800 · `ls:-.035em` | idem | ✅ |
| Filet haut | `inset 0 1px 0 rgba(255,255,255,.3)` | teinte de dalle, épaisseur variable | à aligner |
| Chevron ▾ | opacité .5 · 12px · `gap:16px` | — | à vérifier |
| Icône partage | SVG **19×19** stroke 1.8 | — | à vérifier |

### 1.5 Le tracé de la fiche tenue — `ph-8`, jamais implémenté

Quand un Promi est tenu, **le panneau du geste disparaît** et un tracé prend sa
place, **en haut du corps** :

```
conteneur   text-align:center · margin-bottom:24px
svg         viewBox "0 0 300 62" · width 82% · height 62px
path        M20,44 C56,10 96,52 138,28 C176,6 220,46 278,20
            fill none · stroke #06231A · stroke-width 4.6 · linecap round
```

C'est la trace du geste, gardée comme signature. **Vérifie ce que fait l'app
aujourd'hui sur une fiche tenue et aligne-toi.**

---

## 2 · La section « Les corrections » — jamais traitée

Quatre règles écrites dans le moodboard :

| Point | Correction |
|---|---|
| **La flèche illisible** | **Deux arcs tête-bêche avec de vraies pointes.** L'un part à droite en haut, l'autre à gauche en bas — **un retournement, pas un trait continu** |
| **Le bouton « échéance »** | **Supprimé.** « avant *un jour* » est dans la phrase dès le départ, en gris |
| **Deux lignes de pastilles** | **Une seule ligne**, libellés courts : `note · 1 · Famille` |
| **« à qui » dans une Nuée** | « tout le monde » **en premier et par défaut** · Moi **en dernier** |

---

## 3 · Page + — ce qui reste faux

### 3.1 Le retour vers le haut

On tombe **directement** sur les cartes. Il faut **un espace qui n'existe que
pendant le mouvement** — on doit sentir qu'on quitte une page et qu'on entre dans
une autre. **Sans toucher à la mise en page du haut.**

### 3.2 La zone haute déborde

L'encart du haut ne tient pas ses **210px** dans tous les états. Chaque écran
garde la structure du moodboard : **210 en haut · corps `flex:1` · 62 en bas.**

### 3.3 Les menus qui s'ouvrent au toucher d'un mot

Le chooser « à qui » est aligné. **Les autres ne le sont pas** — celui de
« Je promets ⇄ promets-moi », celui du titre, celui de « avant ». Tous doivent
suivre le même système :

```
libellé    11px · letter-spacing .16em · opacité .6 · MAJUSCULES
pastille   padding 13px 19px · radius 999 · 14.5px
  contour  inset 0 0 0 1.3px rgba(255,255,255,.4) · texte #fff
  pleine   fond #fff · texte couleur de nature · graisse 800
```

### 3.4 Les textes des boutons Tri, Fil, Index

Relève-les et aligne-les sur les mêmes tokens.

---

## 4 · Ordre de travail

**1.** Inscris dans `CLAUDE.md` : *le moodboard fait foi ; une mesure prise sur
l'app ne fait jamais référence.*

**2.** Ajoute `ph-6`, `ph-7`, `ph-8` à `releve-moodboard.py`, **chaque nœud
mappé** — tête, carte message, chaque pastille, panneau, barre, tracé.

**3.** Sors la liste complète des écarts de la fiche. Elle sera longue.

**4.** Corrige jusqu'à zéro, **dans le dernier bloc uniquement**.

**5.** Les quatre corrections de la section 2.

**6.** Les quatre points de la page + de la section 3.

**Ne livre que lorsque `releve-moodboard.py` affiche zéro écart réel sur les
NEUF écrans** et que les neuf batteries passent.

---

## 5 · Méthode — pourquoi trois heures

**Les sondes jetables.** Une trentaine de fichiers Python créés pour une mesure
puis abandonnés. **Un seul outil paramétrable**, réutilisé.

**Les allers-retours d'un pixel.** Chercher 1,4px pendant vingt minutes, poser
puis retirer un padding : sans valeur. Quand un résidu tient sous 2px avec une
cause structurelle identifiée, **note-le et passe**.

**Et surtout : les écarts sont structurels, pas subtils.** 54px contre 34,
176px contre 118. Ce sont ces valeurs-là qu'il faut chercher en premier — pas
les décimales.

---

## 6 · Détails de DA qui ne sont dans aucun tableau

Tirés de `MOODBOARD-VALEURS.md`, faciles à manquer :

**En état « à qui » :**
- la zone dalle passe de **210 à 150px**, et la dalle change de position et de taille
- la phrase passe à **22px, opacité .6**, `line-height 1.58`
- le padding du bloc phrase passe à **`22px 22px 26px`**
- **le mot en cours d'édition** prend un **contour blanc de 2px**, pas un fond plein
- **les autres mots remplis** deviennent `rgba(255,255,255,.34)`
- pastilles : `gap:9px` · `flex-wrap:wrap` — pas 7px

**Dans la phrase :**
- liaisons « à / de / avant » à opacité **.45**
- l'étoile ✦ en `#2BE88C`, `font-size:.74em`, `vertical-align:.2em`
- pastille « Je promets » : `radius 13` · `padding 2px 13px 4px` · `ls -.045em` · `gap 9px`

**La flèche de retournement, le panneau du geste et le tracé de la fiche tenue**
sont donnés en SVG complet à la fin de `MOODBOARD-VALEURS.md`. Copie-les.

---

## ⚠ SECTION CORRIGÉE PAR TOM LE 19 AOÛT 2026 — LIRE LA CORRECTION D'ABORD

**Ce qui suit était trop large, et c'est moi qui l'ai écrit trop large.** Les cadres de fiche
et de page + du moodboard **ne sont PAS une erreur de dessin** : une dalle centrée avec de la
couleur de nature autour, c'est la boîte du §2.7, et elle est juste.

**L'erreur de dessin est ailleurs, et elle est étroite :** elle n'existe **qu'au plancher du
trait**. Sur `promi-nuee-toile.html`, l'espace entre le bas des dalles et le trait est
correctement occupé **jusqu'à trois éléments** (cadres 0 à 6) ; le bandeau de couleur nue ne
se creuse dans les ventres de l'onde qu'à partir de **« Quatre »** — cadres **8** et **10** —
c'est-à-dire dès que `base` touche **176**. Ce sont **ces deux cadres-là**, et leurs
équivalents partout où une base atteint son plancher, qui sont fautifs.

La règle complète et à jour est dans `CLAUDE.md §4`, « LE VIDE EST UN DÉFAUT DU PLANCHER ».
Le relevé qui l'établit : `scratchpad/mesure_vide.py`.

---

## (version d'origine, conservée) — la matière arrêtée à mi-hauteur

**Décision Tom, 19 août 2026.** Sur **tous** les cadres de fiche, de page + et de Nuée, les
moodboards de référence (`promi-moodboard-H.html`, `MOODBOARD-parcours.html`) montrent la
matière — la dalle, ou la Toile d'une Nuée — **enfermée dans une petite boîte centrée**, avec
un large vide de couleur de nature autour d'elle et, surtout, **au-dessus de l'onde**.

**C'est une erreur de dessin, pas une règle.** La règle était déjà écrite, pour l'encart
d'une Nuée — `PROMI-SPECIFICATIONS.md` §10.7 :

> Le masque est le **champ lui-même**, jamais un rectangle : la Toile passe sous le bandeau
> en haut et **se termine sur la vague en bas, jamais sur une ligne droite**.

Elle vaut **partout** : la matière remplit tout le champ, **du haut de l'écran jusqu'à la
vague qui la borne en bas**, dans les deux thèmes. Le champ garde sa couleur de nature
**dessous** : là où la matière ne couvre pas — les coins, le pourtour de la silhouette, les
creux du monde — **on voit la nature, jamais du vide**.

### Les cadres concernés

| cadres | écran | ce qu'ils montrent | ce qui fait foi |
|---|---|---|---|
| **34 à 61, 68 à 71** | les fiches (Promi, Chiche, Nuée, tous états) | dalle ≈ 180 × 150 centrée, vide de nature autour | la matière remplit le champ |
| **2 à 33** | la page + (les trois natures, les choix ouverts) | idem | idem |
| **40, 41, 58 à 61** | les fiches de Nuée | trois dalles dans une bande haute, vide au-dessus de l'onde | la Toile passe sous le bandeau et se termine sur la vague |

### Ce qui reste hors de la correction, et pourquoi

- **Les cadres 96 à 101 — l'instant.** La couleur du champ y **est** le sujet (le menthe
  d'une seconde). Mesuré : en couverture, la matière recouvre jusqu'au pourtour et le menthe
  disparaît. Les trois boîtes d'inventaire restent. Voir `QUESTIONS.md` · Q58.
- **Les cadres 62 à 67, 92, 93 — gardé de côté.** Pas d'aplat, donc **pas de champ** : il n'y
  a rien à remplir.
- **Une fiche à photo.** La photo remplace la matière et doit rester sous l'entête (Q53) :
  elle garde sa boîte. Voir `QUESTIONS.md` · Q57.

### Deux corollaires, tous deux déjà écrits ailleurs

1. **La bande haute d'une fiche teinte sa dalle** (`CLAUDE.md §4 · Q30). La fiche ne le
   faisait pas ; à pleine boîte, une dalle bleue occupait un champ framboise. Voir Q60.
2. **Le mot-marque et ✕ FERMER ont deux encres** (§10.6, généralisé) : ils suivent ce qui
   est peint sous eux — crème ou encre, jamais un troisième ton. Voir Q59.

---

## ⚑ 18 septembre 2026 · LA HAUTEUR DU MOT-MARQUE — la police gagne, le moodboard cède

**Décision Tom :** *« La cote de 27 a été dessinée pour une face qui n'existe plus. Une cote qui
rend un jambage impossible n'est pas une règle, c'est un reste. »*

```
              moodboard        app (Gilbert 33)      raison
  hauteur         27                 36              les glyphes en demandent 33,6
  y               56,5               52,0            conséquence : la boîte est centrée
                                                     dans les 60 px du plateau
```

**CE N'EST PAS UN ARBITRAGE DE GOÛT, C'EST UNE IMPOSSIBILITÉ MESURÉE.** Gilbert, **à 27 px déjà**,
demande **27,5 px** de boîte — montée 18,9 + descente 8,6. La cote de 27 coupait donc le jambage
du « g » de « Réglages » **quelle que soit la taille choisie** : c'est le défaut que Tom a vu à
l'œil (point 1 du 18 septembre). Elle a été dessinée pour la face d'avant le changement de police.

**Ce qui reste vrai du moodboard, et qui n'a pas bougé :** le mot-marque est **centré dans le
plateau** (342 × 60 posé à 40), son x reste **52** (24 + 2 de contour + 26 de padding), et le
plateau lui-même ne bouge pas d'un pixel.

**Contrôlé par** `redteam_nuee.py`, cote reprise au niveau de la décision (§7). Version d'avant :
`sauvegardes/redteam_nuee-avant-COTE-GILBERT.py`.


## 18 septembre 2026 — LA TUILE BORNE LE FACTEUR DE TAILLE

**Écart : 0,9 px sur `.hsub`, la sous-ligne d'une tuile de la page +.**
Le facteur mesuré ×1,217 portait 16,8 à **20,4**. Mesuré dans la tuile : la place est de
**190 px**, et « une parole qu'on donne » en demande **191** à cette taille. Elle passait à la
ligne, et la ligne en trop mangeait l'air de « CHOISIR → ».
**Retenu : 19,5 px** — la plus grande taille où les TROIS sous-lignes tiennent sur une ligne.
**Raison :** le facteur restitue une largeur perdue ; il ne peut pas créer de la place qui
n'existe pas. Même arbitrage que « la police gagne, le moodboard cède » : ici **la tuile gagne**.

**Second écart, même famille : AUX RÉGLAGES, SEUL `.grouplab` MONTE.**
`.grouplab` passe de 13 à **15,8** (13 × 1,217) — il est seul sur sa ligne. Les deux autres
familles de libellés restent à **13**, et chacune pour une raison mesurée :

· **`.scard .k`** — « THE STUDIO », « REVOIR L'INTRO & LE TUTO ». Mesuré taille par taille sur la
  valeur de chaque rangée : 13 ne coupe rien, **13,5 coupe déjà « rejouer › » de 7 px**, 15,8 de
  47. Le libellé le plus long du produit remplit déjà sa colonne.
· **`.s2-lab`** — « RÉCURRENCE », « RAPPEL », « LA COULEUR ». Monté à 15,8, `redteam_air` l'a pris
  **huit fois**, les deux thèmes :
  ```
     .s2-lab → .s2-lab        67   → 64,2   (−2,8)
     .s2-lab → #openStudio2   39,5 → 38,1   (−1,4)
  ```
  La boîte d'un `.s2-lab` vaut **exactement** sa taille (13 → 13 · 15,8 → 15,8) et le libellé est
  CENTRÉ dans une rangée à hauteur fixe : il grandit de 2,8, donc 1,4 de chaque côté — d'où 2,8
  entre deux libellés (les deux bords) et 1,4 avant la carte suivante (un seul bord). Le compte
  tombe juste. **Et on ne peut pas lui rendre sa boîte :** Gilbert à 15,8 demande **15,73** de
  haut (montée 15,54 + descente 0,19, mesuré au canevas) ; la clouer à 13 couperait les jambages.
  **L'air du §8 passe avant la taille.** Après retour à 13 : `redteam_air` ✅ 504 paires intactes.
