# Promi — spécifications techniques exhaustives

**Compagnon de `promi-moodboard-H.html` et de `promi-nuee-toile.html`. Pour Claude Code.**

Ce document est **généré depuis le code qui a produit les deux planches** : chaque valeur
qui suit est celle qui a réellement été dessinée, jamais une valeur recopiée. Si une
planche et ce document divergent, c'est un bug de génération, pas une interprétation.

**Il contient deux parties.**

- **Partie I — le produit** (sections 1 à 7) : les constantes, le moteur géométrique du
  trait, les composants partagés, le code de référence, l'inventaire des 128 écrans du
  moodboard, les règles de comportement et la vérification.
- **Partie II — la fiche de Nuée** (sections 8 à 15) : ce qu'une Nuée contient, sa règle
  de hauteur de trait propre, **le moteur de rendu de la Toile en entier**, l'inventaire
  de ses 20 écrans, sa règle de défilement, ce qui reste à trancher.

Le moodboard `promi-moodboard-H.html` est **validé et ne bouge plus**. La partie II
décrit une proposition en cours sur la fiche de Nuée, et le dit à chaque écart.

**Comment le lire :** les sections 1 à 4 et 9 à 11 donnent les constantes, les formules et
les composants — c'est là que se trouve l'essentiel, parce que **tout écran est un
assemblage de ces briques**. Les sections 5 et 12 donnent, écran par écran, l'inventaire
complet des éléments avec leurs coordonnées exactes.

**Périmètre.** Ce document couvre **la page +, les fiches (Promi, Chiche, Nuée, gardé de
côté), l'instant où une parole est tenue, l'Index, le Fil, Peaufiner, les réglages
généraux, et le moteur de rendu de la Toile**. Il ne couvre **pas** l'Aura, le Studio, le
partage ni l'onboarding : ces écrans existent dans le produit, ils n'ont simplement pas
encore été redessinés. L'absence d'un écran ici ne veut jamais dire qu'il doit disparaître.

**Comptes.** Le moodboard contient **102 écrans** ; la partie I en inventorie **128** — les
102, plus **26 composants isolés** (8 cartes d'Index et 5 bandeaux du Fil, dans les deux
thèmes) sortis de leur écran pour que leurs coordonnées soient lisibles. La planche de
Nuée contient **20 écrans**, tous inventoriés en partie II. Un outil qui compte les écrans
du moodboard doit trouver 102.

**Repère.** Tous les écrans font **390 × 844 px**, coins 36. L'origine est en haut à
gauche. Toutes les valeurs sont en points logiques (px CSS = pt iOS à ×1).

## Sommaire

1. Les constantes
2. Le moteur géométrique
3. Les composants partagés
4. Le code de référence — le trait
5. Inventaire écran par écran — le produit
6. Les règles que la géométrie ne dit pas
7. Vérification — le produit
8. Ce qu'une Nuée contient
9. La hauteur du trait — règle propre à la fiche de Nuée
10. L'encart : le moteur de la Toile
11. Le code de référence — la Toile
12. Inventaire écran par écran — la fiche de Nuée
13. Le défilement — règle unique dans le produit
14. Ce qui reste à trancher
15. Vérification — la fiche de Nuée

---

# Partie I — le produit

## 1 · Les constantes

### 1.1 Couleurs signal — immuables

| Rôle | Hex | Usage |
|---|---|---|
| Promi | `#3A54FF` | champ d'une fiche Promi, verbe de la phrase, accents |
| Chiche | `#FA2258` | champ d'une fiche Chiche |
| Nuée | `#8A5CF0` | champ d'une fiche Nuée |
| à tenir | `#F07A2E` | ligne d'état, méta, légende |
| tenu | `#2BE88C` | ligne d'état, méta, arc des Noyaux |
| crème | `#F4EEE1` | corps en thème clair, texte sur couleur pleine |
| encre | `#16171B` | texte sur crème |

### 1.2 Teintes de dalle — la palette du monde par défaut

| Nature | Teintes (3, alternées) |
|---|---|
| Promi | `#E7DAFF` · `#CBAAFF` · `#AE86F2` |
| Chiche | `#FFE2D2` · `#FFC0A8` · `#F2977A` |
| Nuée | `#F3EAFF` · `#DCC6FF` · `#C2A4F7` |

**Attention, deux jeux distincts.** La palette ci-dessus est celle des **dalles**. La
**teinte claire de la nature**, qui sert au trait non tracé et aux libellés secondaires
posés sur le champ plein, est un jeu séparé :

| Nature | Teinte claire |
|---|---|
| Promi | `#CBAAFF` |
| Chiche | `#FFC0A8` |
| Nuée | `#D0B0FF` |

Pour le Promi et le Chiche, elle coïncide avec la deuxième teinte de dalle. **Pour la
Nuée, non** : c'est `#D0B0FF`, et non `#DCC6FF`. C'est cette valeur qu'emploient tous les
inventaires.

### 1.3 Corps d'écran

| Contexte | Thème sombre | Thème clair |
|---|---|---|
| Fiche Promi | `#12142A` | `#F4EEE1` |
| Fiche Chiche | `#25101A` | `#F4EEE1` |
| Fiche Nuée | `#1A1230` | `#F4EEE1` |
| Carte d'Index / bandeau Promi | `#1C2049` | `#F4EEE1` |
| Carte d'Index / bandeau Chiche | `#37141F` | `#F4EEE1` |
| Carte d'Index / bandeau Nuée | `#271B45` | `#F4EEE1` |
| Écran d'Index et de Fil | `#0E0F12` | `#E8E0D0` |

### 1.4 Polices — quatre graisses, pas une de plus

| Police | Graisses | Rôles |
|---|---|---|
| Bricolage Grotesque | **600** et **700** | titres, valeurs, actions, phrase, légendes |
| Apfel / ApfelMid | **400** et **500** | petits libellés en capitales, prose de légende |
| Fraunces | **600** | le mot-marque en haut à gauche, et rien d'autre |

Aucune autre graisse n'existe dans le fichier. Dans le moodboard, Apfel est remplacée par
Hanken Grotesk (400 et 500), qui joue les mêmes rôles.

### 1.5 Marges et gabarit

| | |
|---|---|
| Écran | 390 × 844, rayon 36 |
| Marge latérale | **24 px**, aucune exception — largeur utile **342 px** |
| Entête | haut 38, hauteur 34 |
| Barre Peaufiner | hauteur **84**, collée en bas (y = 760), toujours |
| Bas d'écran | consigne de dessin : **30 px** entre le dernier élément et la barre. Le contrôle automatique refuse en dessous de **26 px** — c'est une tolérance de 4 px pour les arrondis, pas une seconde règle. |

## 2 · Le moteur géométrique

Ces formules produisent tout ce qui n'est pas un rectangle. Elles doivent être portées
telles quelles : c'est d'elles que dépend l'identité du produit.

### 2.1 L'onde — la frontière entre le champ et le corps

Un **seul sinus** traverse l'écran, plus une montée vers la droite. Il est **canonique** :
identique pour toutes les promesses. `base` est la hauteur du trait, `amp` son amplitude
(46 sur la page +, 36 à 52 sur les fiches).

```python
per, mont, a = 1.5, amp * 0.34, amp * 0.62

def y(x):                      # x de 0 à 390
    t = min(1.0, max(0.0, x / 390))
    return base - mont * t - a * math.sin(2 * math.pi * per * t)
```

Le chemin est tracé en **Bézier cubique, un segment par quart de période**, avec les
tangentes exactes du sinus — sinon le plein s'écarte des points :

```python
seg = 390 / (per * 4)          # = 65 px
h   = (x_b - x_a) / 3
C1  = (x_a + h, y(x_a) + y'(x_a) * h)
C2  = (x_b - h, y(x_b) - y'(x_b) * h)
```

### 2.1 bis La couleur du trait — c'est la moitié de la loi

Le trait porte **la couleur d'état**, jamais celle de la nature :

| État | Couleur du trait |
|---|---|
| à tenir | terracotta `#F07A2E` |
| tenu, tenu à deux | menthe `#2BE88C` |
| en cours, Chiche lancé, rien de tracé | **teinte claire de la nature** — `#CBAAFF`, `#FFC0A8`, `#D0B0FF` |
| gardé de côté | couleur pleine de la nature, mais **tout le trait est en points** |

Il ne porte jamais la couleur pleine de la nature quand il est posé sur le champ : ce
serait du ton sur ton. La teinte claire vaut **dans les deux thèmes** — elle ne dépend pas
du thème mais du fond sur lequel le trait est posé, qui est toujours le champ plein.

### 2.2 Les points — jamais un pointillé étiré

Des **cercles pleins de 9 px de diamètre** (r = 4,5), posés un par un **tous les 18 px**
en x, chacun à `y(x)`. Un `stroke-dasharray` sur la courbe donne un espacement irrégulier
dans les pentes : c'est interdit.

### 2.3 L'amorce effilée et le chevron

- L'amorce va de **x = −10** (hors cadre, donc flush au bord) à **x = 42**.
- Son épaisseur passe de **22 px à 1,5 px** : elle finit en pointe.
- Elle est construite en décalant la courbe perpendiculairement de ±épaisseur/2,
  échantillonnée sur 40 points, aller-retour, chemin fermé.
- Le **chevron** est posé à x = 42, orienté selon la pente locale
  (`atan2(y(x+8) − y(x−8), 16)`), tracé `M−7 −10 L6 0 L−7 10`, épaisseur 6, bouts et
  jointures ronds.
- **Règle absolue :** la pointe de l'amorce s'arrête au sommet du chevron et ne dépasse
  jamais de ses branches.

### 2.4 La flèche d'invite

Courbe de Bézier légèrement bombée **vers la gauche**, épaisseur 4,5, bouts ronds :

```python
A  = (chevron_x + 32, base + 46)     # départ, au ras du mot
B  = (chevron_x + 10, base + 14)     # pointe : elle désigne, elle ne touche pas
C1 = (A.x - 10, A.y - 4)
C2 = (B.x + 3,  B.y + 12)
```

La **tête** est calculée sur la tangente réelle en B (`B − C2`), deux ailes à ±32°,
longueur 13. Elle n'est jamais posée à la main.

### 2.4 bis `base`, `amp`, et la boîte SVG — trois choses différentes

- **`base`** est la hauteur du trait au repos : l'ordonnée autour de laquelle le sinus
  oscille. C'est elle que donne la formule du §2.5.
- **`amp`** est l'amplitude de l'oscillation. Ce n'est pas une constante globale : c'est
  **une constante par écran**, figée avec la composition. Elle vaut **46 sur la page +**
  et **36 à 52 sur les fiches**. La valeur exacte de chaque écran est donnée en tête de
  son inventaire, partie 5, sous la forme `trait : base = X, amplitude = Y`.
- **La boîte SVG** qui porte le trait n'est ni l'un ni l'autre :
  `hauteur = base + amp + 40` sur une fiche, `base + amp + 60` sur la page +.
  C'est pourquoi les hauteurs relevées dans les tableaux (346, 366, 424…) ne figurent pas
  dans la suite des `base` — **ce sont des boîtes, pas des hauteurs de trait.**

**Une exception, et une seule : `amp = 22`** sur les trois écrans où un choix est ouvert
— écrire un mot, choisir une personne, l'échéance. C'est voulu : le champ y est réduit à
`base = 196` pour laisser la place au choix, et **l'onde s'aplatit d'autant**. Une
amplitude normale sur un champ aussi bas ferait toucher la dalle. La règle est donc :
`amp = 22` dès qu'un panneau de choix occupe le corps, la valeur d'écran sinon.

La règle de choix de `amp` pour un écran neuf, hors ce cas : **amp ≈ 0,17 × base, borné à
[36, 52]**.
Elle reproduit les valeurs du moodboard à ±4 px près. Pour reproduire le moodboard à
l'identique, prendre la valeur donnée écran par écran.

### 2.5 La hauteur du trait — elle dit le remplissage

```python
def hauteur_trait(n_elements_remplis):
    return max(196, 344 - 32 * (n_elements_remplis - 1))
```

`n` est le **nombre de lignes de la phrase**, verbe compris, minimum 1. Une phrase d'une
ligne donne **344** — trait bas, grande dalle ; deux lignes **312** ; trois **280** ;
quatre **248** ; cinq **216** ; plancher **196**. Chaque élément rempli ajoute une ligne
et fait donc **monter le trait de 32 px**. **Une seule exception, la fiche de Nuée** : elle compte ses éléments en lignes de fil, pas en lignes de phrase, donc son pas est de 86 px et ses bornes sont 460 et 176. Sa règle est donnée au §9 — ne pas lui appliquer celle-ci. **À la plantation, la valeur se fige** : elle devient la composition de
cette promesse, reprise à l'identique sur sa fiche et sur sa carte d'Index.

> **CORRECTION (section 4, validée) — les bornes valent pour la CARTE sans exception.**
> Les inventaires de la partie 5 donnent, pour deux fiches, des bases **hors de cette
> échelle** : `376` (« Promi · tenue ») et `372` (« Chiche · tenu à deux »). Ce sont des
> cotes d'écran, posées à la main sur 844 px de haut. Reportées telles quelles sur une carte
> d'Index de 133 px, elles ne laissaient plus que **10 px au titre** : le titre sortait coupé
> en plein mot, l'état par-dessus. **Un titre coupé en plein mot n'est pas un dessin, c'est
> un bug.** La base employée par une carte est donc toujours `max(196, min(344, base))`.
> Les bases que le moodboard emploie pour ses propres cartes tiennent toutes dans
> `[204, 348]` : la borne est celle qu'il applique déjà.
>
> **Deux cartes du moodboard dépassent le plafond de peu** — « le potager » à 346 et 348.
> La borne leur coûte **1 px de boîte**, sous la tolérance de 3. C'est le prix, et il est
> connu. **La borne est un garde-fou sur la valeur, pas un morceau de la loi de la carte**
> (§3.9 bis) : les deux se contrôlent séparément, sans quoi ce pixel se lit comme une erreur
> de géométrie alors qu'il est une décision.

### 2.6 Les états du trait

| État | Plein | Points |
|---|---|---|
| rien de tracé | amorce seule, 0 → 42 | 64 → 390 |
| en cours | 0 → position du doigt (max 195) | après le doigt |
| ma moitié donnée | **0 → 195**, le milieu exact | 195 → 390 |
| tenu | 0 → 390 | aucun |
| tenu à deux | 0 → 191 et 199 → 390 | aucun |

### 2.7 La dalle

- Toujours **centrée** horizontalement.
- Jamais au-dessus de **y = 88**, jamais à moins de **12 px** du trait.
- Hauteur disponible : `(base − amp) − 88 − 12`, bornée à 300 ; largeur = 1,2 × hauteur,
  bornée à 320.
- **Opacité 1**, aucun voile, aucun mélange.
- Elle est figée à la création : changer de monde au Studio ne repeint pas les dalles déjà
  posées. Une Nuée porte donc **les dalles de tous ses Promi**, de palettes différentes.
- **Un gardé de côté ne pose rien sur la Toile** : sa dalle est visible sur sa fiche, pas
  sur la Toile.

### 2.8 La phrase — une ligne par élément

```python
taille = 36 si <= 3 lignes, 34 si 4 lignes, 30 si >= 5 lignes
                                           # 30 au départ si un choix est ouvert (§2.4 bis)
tant que largeur_estimee(ligne) > 342 ou largeur_rendue(ligne) > 342 : taille -= 1
interligne = int(taille * 1.2) + 24        # ~13 px francs entre deux pastilles
largeur_estimee = somme(nb_caracteres * taille * 0.53 + 32 par pastille + 11 par écart)
```

> **RÈGLE — `taille = min(estimation, mesure)`.** (Décision Tom, 18 août 2026.)
> **L'ESTIMATION EST LA RÈGLE DE COMPOSITION** : c'est elle qui a dessiné le moodboard, et
> elle redonne les tailles des dix-sept cadres au caractère près —
> `29 · 29 · 31 · 36 · 35 · 33 · 33 · 29 · 28 · 30`.
> **LA MESURE NAVIGATEUR NE SERT QU'À EMPÊCHER LE DÉBORDEMENT** : l'estimation est
> optimiste sur certaines chaînes (« courir dimanche… ») et laisse une ligne passer à la
> ligne — ce qui décale tout ce qui suit de 32 px (§2.5).
> **On prend la plus petite des deux, jamais la mesure seule** : la mesure remplit toujours
> les 342 px et sort la phrase trop grosse (`35 · 36 · 35 · 36 · 35 · 32 · 33 · 34 · 30`).
> **La « correction du §2.8 » du lot précédent — la mesure remplaçant l'estimation — est
> annulée pour de bon.**

- Chaque ligne est un `flex` horizontal, `align-items:center`, `white-space:nowrap`.
- Écart liaison / mot : **11 px**, ramené à **3 px** en cas d'élision.
- **Élision :** « de » devient « d' » devant voyelle ou h muet, collé au mot.
- Pastille pleine : rayon **18**, padding **4 / 17 / 8**.
- Pastille vide : mêmes cotes, contour **3 px pointillé** dans la teinte de la nature.
- Pastille avec visage : `inline-flex`, écart 0,22 × taille, visage 0,76 × taille,
  padding gauche ramené à 9.

### 2.9 Les Noyaux

| | Le tien | Une personne |
|---|---|---|
| Diamètre | **78** | **58** |
| Épaisseur de l'arc | 8 | 6 |
| Photo au centre | 48 | 36 |
| Libellé dessous | « toi », Bricolage 700 / 14 | prénom, Bricolage 600 / 13,5 |
| Écart au libellé | 11 px | 11 px |

Piste de l'anneau : teinte de la nature. Arc : menthe. **Aucun chiffre, aucun
pourcentage, aucun mot d'état.** Écart du tien au groupe : **30 px** ; entre deux
personnes : **26 px**. Ordre alphabétique ou chronologique, jamais par valeur.
Le Cercle ajoute un **second anneau** à +9 px, épaisseur 0,7 ×.

### 2.10 Le visage — emplacement de photo de profil

Cercle de diamètre `d`, `border-radius:999px`, fond = couleur de la nature, silhouette en
crème :

```
tête     : cercle  cx = d/2, cy = 0.78·d/2 ... r = 0.19·d
épaules  : arc     de (d/2 − 0.30·d, 0.98·d) à (d/2 + 0.30·d, 0.98·d)
           rayons  0.30·d horizontal, 0.27·d vertical, chemin fermé
```

Tailles employées : **48** au centre de ton Noyau, **36** dans celui d'une personne,
**38** dans la rangée de membres d'une Nuée (superposés de 12 px, puis « +N » à 26 px),
**30** dans une pastille de choix, **26** dans un bandeau du Fil, **0,76 × la taille du
texte** dans une pastille de prénom.

### 2.11 Le clavier système

Représenté, pas conçu : trois rangées `azertyuiop` / `qsdfghjklm` / `wxcvbn`,
touches de **32 × 50**, rayon 9, pas horizontal de **36 px**, rangées espacées de
**62 px**, première rangée à y = 640. Fond des touches `#2A2D34` en thème sombre,
`#DCD4C2` en clair, lettre Bricolage 600 / 17. La barre Peaufiner est masquée pendant la
saisie — c'est le seul cas où elle n'est pas visible.

### 2.12 Le rendu d'une dalle (emplacement)

Les dalles du moodboard sont des amas de formes organiques : 4 à 7 blobs, chacun un
chemin fermé de 9 points reliés par des quadratiques, rayon jitteré de ±30 %, disposés en
couronne autour du centre, puis **recadrés pour remplir la boîte**. Le moteur réel les
remplacera : seules **la position, la taille et le nombre** comptent.

## 3 · Les composants partagés

Tout écran est un assemblage de ces briques. Les coordonnées sont données pour un écran
de 390 px de large.

### 3.1 Entête
`left 24 · top 38 · hauteur 34`, `flex` justifié aux extrémités.
Mot-marque **Fraunces 600 / 27**, interlettre −0,01em, couleur crème sur champ plein,
encre sinon. À droite, `✕` en 15 px puis **FERMER** en Apfel 500 / 12,5, interlettre
0,20em, écart 9 px.

### 3.2 Barre Peaufiner
`top 760 · 390 × 84`, fond = couleur de la nature. « Peaufiner » **Bricolage 700 / 21**,
crème. À droite, `▾` en 15 px, puis l'icône Partager dans un cercle de **46 px**,
contour 3, icône 22 px. **Pas d'icône Partager sur la page +.**

### 3.3 Réglage
`342 × 64`, rayon **22**, contour **3 px**, padding latéral 22.
Libellé Apfel 500 / 11,5 interlettre 0,18em dans la teinte de la nature ; valeur
Bricolage 700 / 18. Écart entre deux réglages : **16 px**.
Variante avec ligne de visibilité : hauteur **92**, écart interne 7.
Variante vide : contour **3 px pointillé** dans la teinte.

### 3.4 Zone de texte
`342 × 104 à 118`, rayon 22, contour 3, padding 16 / 22.
Libellé en haut (Apfel 500 / 11,5), contenu Bricolage 600 / 18 à 9 px dessous, ligne de
visibilité Bricolage 600 / 14 collée en bas à 14 px.

### 3.5 Pastille d'action
Hauteur **50**, rayon 25, contour 3, padding latéral 19, texte Bricolage 700 / 16.

### 3.6 Bouton
`342 × 62`, rayon 31, texte Bricolage 700 / 19 à 20.

### 3.7 Champ
`342 × 66`, rayon 33, contour 3, padding latéral 24, texte Bricolage 600 / 18,
chevron `→` 20 px à droite.

### 3.8 Bloc du Cercle
Quatre réglages de 64 px espacés de 16, **floutés à `blur(2.4px)`**.
Par-dessus, centré verticalement sur le bloc, l'encart : `342 × 90`, rayon 26, fond crème
en thème sombre et encre en thème clair, titre « ✦ Le Cercle » Bricolage 700 / 22 et
sous-titre Bricolage 600 / 15 — **tous deux dans la teinte de la dalle**.
**C'est la seule superposition autorisée du produit.**

### 3.9 Carte d'Index
`173 × 208` à deux par ligne (`(390 − 48 − 12) / 2`), rayon 18, écart 12.
À trois par ligne : `110 × 138`. Le trait y a une période et une amplitude réduites
(per = 1, amp = 13 × échelle), points r = 3,2 tous les 11 px.
Contenu : eyebrow Bricolage 600 / 13, titre Bricolage 700 / 21 interligne 1, état Apfel
500 / 10,5 collé en bas à 12 px.

#### 3.9 bis La loi de la carte — elle vaut pour TOUTE carte, à toute taille

**Cette règle n'était écrite nulle part.** Le document donnait les cotes carte par carte ;
la loi qui les produit était dans les chemins SVG du moodboard. Elle est inscrite ici pour
ne plus jamais être redéduite. `l` et `h` sont la largeur et la hauteur de la carte.

```
échelle    = h / 600
base       = hauteur de trait figée à la plantation × échelle     (§2.5)
amplitude  = 13 × l / 173         ← le « 13 × échelle » du §3.9 : 173 est la carte de référence
boîte      = ⌊ base + amplitude + 20 ⌋     ← l'analogue du « + 40 » du §2.4 bis, à l'échelle de la carte
période    = 1                    (une seule oscillation, contre 1,5 sur un écran — §2.1)
épaisseur  = 5,5 × l / 173        points : r = 3,2 × l/173, tous les 11 × l/173
dalle      = hauteur  base − amplitude − 13,7 × h/198
             largeur  1,2 × hauteur          y = 0,0455 h          CENTRÉE (§2.7)
```

Le trait lui-même — onde, amorce, chevron, points — est celui du §4 : **une seule formule
d'onde existe dans le produit**, on l'appelle avec `l` pour largeur.

**Les blocs de texte** suivent la boîte, et non le haut de la carte : c'est ce qui fait que
le titre descend quand le trait descend. Vérifiés aux trois tailles du document :

| | 106 × 133 | 165 × 198 | 173 × 208 |
|---|---|---|---|
| eyebrow | boîte − 14 | boîte − 10,5 | boîte − 10 |
| titre | eyebrow + 11 | eyebrow + 17 | eyebrow + 18 |
| bas du bloc titre | h − 15 | h − 24 | h − 26 |
| état, collé en bas | 8 | 12 | 12 |
| marge latérale · largeur utile | 7 · 90 | 12 · 140 | 13 · 147 |
| eyebrow / titre / état | 8,0 / 12,9 / 6,4 | 12,4 / 20,0 / 10,0 | 13,0 / 21,0 / 10,5 |

L'écart d'eyebrow suit la hauteur presque linéairement (`≈ 20,9 − 0,052 h`) et celui du
titre lui est proportionnel (`≈ 0,086 h`) ; **pour une taille du document, prendre la
colonne, jamais l'approximation.**

##### Le contrôle — la loi retrouve les cartes du document, sans exception

Pour une hauteur de trait de 312, la boîte retombe sur **135** à 165 × 198, **97** à
106 × 133 et **141** à 173 × 208 — les trois valeurs des tableaux, au pixel près. Et les
**huit cartes isolées** de la partie 5 sont retrouvées **8 sur 8**, boîte et dalle :

```
boîte 141 → dalle  97×81      boîte 128 → dalle  81×68
boîte 112 → dalle  62×52      boîte 137 → dalle  92×77
boîte 153 → dalle 111×93      boîte 124 → dalle  76×64
boîte 103 → dalle  51×43      boîte 116 → dalle  67×56
```

`releve-S4-index-fil.py` exécute ce contrôle à chaque passage (`juge_composants`).

##### ⚠ LA BORNE NE VAUT QUE POUR UN TRAIT DE PHRASE (décision Tom, 18 août 2026)

`[196, 344]` est la borne d'une hauteur de trait **comptée en lignes de phrase** (§2.5).
**Elle ne s'applique pas à une fiche de Nuée**, qui compte ses éléments **en lignes de
fil** : sa règle propre est `base = max(176, 460 − 86 n)` — partie II, §9.
**Une carte d'Index de Nuée dérive de cette même base par la loi ci-dessus, SANS passer par
la borne.** Une base de 460 donne donc, à 165 × 198, une boîte de `⌊460×0,33 + 12,4 + 20⌋`
= **184** — et c'est juste : une Nuée porte plus haut parce qu'elle contient plus.

##### ⚠ La loi et la borne sont DEUX règles — ne pas les confondre

**La loi ne borne rien** : elle transforme une hauteur de trait en géométrie. **La borne du
§2.5 est un garde-fou sur la valeur qu'on lui donne** (voir la correction au §2.5). Les
appliquer d'un seul geste fait sortir « le potager » à 152 au lieu de 153 — sa base est
**346**, deux pixels au-dessus du plafond de 344. Chacune se contrôle donc à son niveau :
`juge_composants` teste la loi **sans la borne**, `juge_borne` vérifie que la borne mord sur
376 et 372, jamais sur une base légitime, et que là où elle mord un cas limite du moodboard
elle coûte **moins de 3 px**.

---
## 4 · Le code de référence — le trait
Ces fonctions sont celles qui ont dessiné le moodboard, extraites telles quelles. **En cas de doute, elles priment sur toute reformulation.** Une seule formule d'onde existe : `per = 1.5`, `mont = amp × 0.34`, `a = amp × 0.62`.

### Le trait complet : onde, amorce, chevron, points, flèche

```python
def ligne(base, nat, theme, etat="plate", amp=46, seed=11, fx=130, fond=True):
    """Un seul sinus traverse l'écran. Ma moitié va de 0 au milieu exact, jamais plus loin.
       L'amorce s'effile, les points prennent le relais au même calibre.
       Couleur : toujours la teinte claire de la nature — sur le champ plein, un bleu sur
       bleu serait du ton sur ton."""
    field = FIELD[nat]
    c = CLAIR[nat] if etat == "plate" else TERRA
    per, mont, a = 1.5, amp * .34, amp * .62
    def y(x):
        t = max(0., min(1., x / W))
        return base - mont * t - a * math.sin(2 * math.pi * per * t)
    def dyy(x):
        return y(x + .5) - y(x - .5)
    def chemin(x0, x1):
        seg = W / (per * 4)
        xs = [x0]; k = math.ceil(x0 / seg) * seg
        while k < x1 - .5:
            xs.append(k); k += seg
        xs.append(x1)
        d = f"M{xs[0]:.2f} {y(xs[0]):.2f}"
        for i in range(len(xs) - 1):
            p, q = xs[i], xs[i + 1]; h = (q - p) / 3.
            d += (f"C{p+h:.2f} {y(p)+dyy(p)*h:.2f} {q-h:.2f} {y(q)-dyy(q)*h:.2f} "
                  f"{q:.2f} {y(q):.2f}")
        return d
    def ruban(x1, e0=22, e1=9):
        n = 44; haut = []; bas = []
        x0 = -10                       # on part hors cadre : le trait est flush au bord
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n; e = (e0 + (e1 - e0) * (i / n)) / 2
            d_ = dyy(x); L = math.hypot(1, d_)
            haut.append((x - d_ / L * e, y(x) + e / L))
            bas.append((x + d_ / L * e, y(x) - e / L))
        d = f"M{haut[0][0]:.1f} {haut[0][1]:.1f}"
        d += "".join(f"L{p:.1f} {q:.1f}" for p, q in haut[1:])
        d += "".join(f"L{p:.1f} {q:.1f}" for p, q in reversed(bas))
        return d + "Z"
    coupe = {"plate": DEP, "cours": min(fx, MI), "trace": MI}[etat]
    fin_plein = coupe + 6          # le plein finit en pointe, au sommet même du chevron
    pts, x = [], coupe + 22
    while x < W - 3:
        pts.append(f'<circle cx="{x:.1f}" cy="{y(x):.1f}" r="4.5" fill="{c}"/>'); x += 18
    # le chevron à deux traits, exactement là où le plein rencontre les points
    ang = math.degrees(math.atan2(dyy(coupe + 8) - 0, 1)) if False else \
        math.degrees(math.atan2(y(coupe + 8) - y(coupe - 8), 16))
    chev = (f'<g transform="translate({coupe:.1f} {y(coupe):.1f}) rotate({ang:.1f})">'
            f'<path d="M-7 -10 L6 0 L-7 10" stroke="{c}" stroke-width="6" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    fleche = ""
    if etat == "plate":
        # la flèche et le mot forment un seul bloc, posé plus bas que le trait
        ax, ay = coupe + 32, base + 46          # départ, au ras du mot
        bx_, by_ = coupe + 10, base + 14         # pointe : elle vise le chevron, sans l'atteindre
        c1x, c1y = ax - 10, ay - 4              # ventre léger à gauche
        c2x, c2y = bx_ + 3, by_ + 12            # dernier contrôle dans l'axe de la pointe
        vx, vy = bx_ - c2x, by_ - c2y           # tangente réelle à la pointe
        L = math.hypot(vx, vy); vx, vy = vx / L, vy / L
        def aile(deg):
            r = math.radians(deg)
            return (bx_ - (vx * math.cos(r) - vy * math.sin(r)) * 13,
                    by_ - (vx * math.sin(r) + vy * math.cos(r)) * 13)
        g1, g2 = aile(-32), aile(32)
        fleche = (f'<path d="M{ax} {ay} C{c1x} {c1y} {c2x} {c2y} {bx_} {by_}" '
                  f'stroke="{c}" stroke-width="4.5" '
                  f'stroke-linecap="round" fill="none"/>'
                  f'<path d="M{g1[0]:.1f} {g1[1]:.1f} L{bx_} {by_} L{g2[0]:.1f} {g2[1]:.1f}" '
                  f'stroke="{c}" stroke-width="4.5" fill="none" stroke-linecap="round" '
                  f'stroke-linejoin="round"/>')
    hh = int(base + amp + 60)
    return (f'<svg width="{W}" height="{hh}" viewBox="0 0 {W} {hh}" fill="none" '
            f'style="position:absolute;left:0;top:0">'
            + (f'<path d="{chemin(0, W)} L{W} 0 L0 0 Z" fill="{field}"/>' if fond else "")
            + f'<path d="{ruban(fin_plein, 22, 1.5)}" fill="{c}"/>{chev}{"".join(pts)}{fleche}</svg>')
```

### Le trait d'une fiche

```python
def trait(w, base, field, col, mode="moitie", amp=46, per=1.5, ep=10, r=4.5, esp=18,
          hauteur=None, fond_=True, chevron=True):
    """mode : moitie (ma part tracée, le reste en points) · complet · duo · points (rien de tracé)"""
    y = _onde(w, base, amp, per)
    mid = w / 2
    plein, pts = [], []
    if mode == "complet":
        plein = [(0, w)]
    elif mode == "duo":
        plein = [(0, mid - 4), (mid + 4, w)]
    elif mode == "moitie":
        plein = [(0, mid)]
    x = (mid + esp) if mode == "moitie" else esp / 2
    if mode in ("moitie", "points"):
        x0 = mid + esp if mode == "moitie" else esp
        x = x0
        while x < w - r:
            pts.append(f'<circle cx="{x:.1f}" cy="{y(x):.1f}" r="{r}" fill="{col}"/>')
            x += esp
    sp = "".join(f'<path d="{_chemin(y, a, b, w, per)}" stroke="{col}" stroke-width="{ep}" '
                 f'stroke-linecap="round" fill="none"/>' for a, b in plein)
    # le chevron : là où le plein rencontre les points. Et quand rien n'est tracé,
    # une amorce effilée part du bord gauche, comme sur la page +.
    chev = ""
    dyy = lambda xx: y(xx + .5) - y(xx - .5)
    if chevron and mode in ("moitie", "points"):
        cx = mid if mode == "moitie" else w * .11
        if mode == "points":
            sp = f'<path d="{_ruban(y, dyy, -w*0.03, cx + ep*.6, ep*2.2, ep*.15)}" fill="{col}"/>'
            pts = []
            x = cx + esp * 1.3
            while x < w - r:
                pts.append(f'<circle cx="{x:.1f}" cy="{y(x):.1f}" r="{r}" fill="{col}"/>')
                x += esp
        ang = math.degrees(math.atan2(y(cx + 8) - y(cx - 8), 16))
        k = ep / 10.
        chev = (f'<g transform="translate({cx:.1f} {y(cx):.1f}) rotate({ang:.1f})">'
                f'<path d="M{-7*k:.1f} {-10*k:.1f} L{6*k:.1f} 0 L{-7*k:.1f} {10*k:.1f}" '
                f'stroke="{col}" stroke-width="{6*k:.1f}" fill="none" stroke-linecap="round" '
                f'stroke-linejoin="round"/></g>')
    sp += chev
    hh = int(hauteur or base + amp + 40)
    fill = (f'<path d="{_chemin(y, 0, w, w, per)} L{w} 0 L0 0 Z" fill="{field}"/>'
            if fond_ else "")
    return (f'<svg width="{w}" height="{hh}" viewBox="0 0 {w} {hh}" fill="none" '
            f'style="position:absolute;left:0;top:0">{fill}{sp}{"".join(pts)}</svg>')
```

### La hauteur du trait

```python
def hauteur_trait(n_lignes):
    """La règle : une promesse vide a son trait bas et sa dalle grande ; à chaque
       élément rempli le trait monte, le corps s'ouvre. À la plantation, la hauteur
       se fige — c'est la composition de cette promesse, pour toujours."""
    return max(196, 344 - 32 * (max(1, n_lignes) - 1))
```

### La composition d'une phrase

```python
def phrase(lignes, y, nat, theme, size_max=36):
    """Une ligne par élément. Les lignes facultatives encore vides sont écrites plus
       petit, dans la teinte de la nature : elles n'encombrent pas la phrase. Dès
       qu'un mot y est posé, elles reprennent la taille et le contraste des autres."""
    lignes = [(l[:-1], True) if l and l[-1] == "opt" else (l, False) for l in lignes]
    lignes = [(elide(l), o) for l, o in lignes]
    def vide(l):
        return all(k != "plein" and k != "visage" for k, *_ in l if k != "fixe")
    obl = [l for l, o in lignes if not (o and vide(l))]
    n = len(obl) or 1
    size = min(size_max, 30 if n >= 5 else (34 if n == 4 else 36))
    while size > 20 and max(_largeur(l, size) for l in obl) > LARG:
        size -= 1
    petit = max(19, int(size * .62))
    out, yy = [], y
    for l, o in lignes:
        s_ = petit if (o and vide(l)) else size
        pas = int(s_ * 1.2) + (16 if s_ == petit else 24)
        toks = "".join(_token(k, t, nat, theme, s_, *(r or [""])) for k, t, *r in l)
        colle = any(k == "fixe" and t.endswith("'") for k, t, *_ in l)
        out.append(f'<div style="position:absolute;left:24px;top:{yy}px;width:{LARG}px;'
                   f'height:{pas}px;display:flex;align-items:center;gap:{3 if colle else 11}px;'
                   f'white-space:nowrap">{toks}</div>')
        yy += pas
    return "".join(out), yy
```

### L'élision

```python
def elide(l):
    """« de » + voyelle = « d' », collé au mot. La liaison ne reste jamais entière."""
    out = []
    for i, (kind, txt, *r) in enumerate(l):
        if kind == "fixe" and txt == "de" and i + 1 < len(l):
            suiv = l[i + 1][1].lstrip("'").lower()
            if suiv and suiv[0] in "aeiouyéèêh":
                out.append(("fixe", "d'", *r)); continue
        out.append((kind, txt, *r))
    return out
```


> ### ⚑ DÉCISION DU 1er SEPTEMBRE 2026 — L'ENCART DU HAUT DEVIENT LA RÉFÉRENCE
>
> **Décision Tom, littérale :** *« déploie à toutes les pages et toutes les fiches l'encart
> en haut »*, et *« le trait de l'encart est la réf, mais du coup ça change les boutons tri
> et barre recherche du Fil et de l'Index, qui doivent devenir cohérents avec l'encart »*.
>
> **Elle REMPLACE, sur l'Index et le Fil, les cotes relevées du cadre.** Comme la décision
> du même jour sur l'amplitude de l'onde (QUESTIONS.md · Q136), c'est un arbitrage de Tom
> qui prend le pas sur un relevé — ce n'est pas une correction de bug, et il faut le lire
> comme tel.
>
> ```
> LA GRAMMAIRE DE L'ENCART, commune à tous les écrans
>   x 24 · largeur 342 · hauteur 60 · rayon 30 · bord 2 · padding 26 · titre 27
>
> CE QUI CHANGE SUR L'INDEX ET LE FIL          avant (cadre)      après (décision)
>   l'entête                                   Bricolage 700/38   Bricolage 700/27
>   le compte                                  Bricolage 700/26   Bricolage 700/17
>   la recherche : rayon                       28                 26
>   la recherche : contour                     3                  2
>   la barre                                   top 108            top 116
>   la liste                                   top 196            top 204
> ```
>
> Le décalage de **+16 px** de toute la colonne est la différence entre le plateau (60) et
> le titre qu'il remplace (44). Sans lui, le plateau recouvrait la barre de recherche de
> 6 px — mesuré.
>
> ⚑ **ET L'AIR SOUS L'ENTÊTE PASSE DE 24 À 16 — décision Tom, 3 septembre 2026.**
> *« Rapproche la ligne Rechercher / tri de l'encart titre et ✕ fermer, sinon ça fait
> bizarre ; ça remonte du tout les éléments en dessous un peu. »*
> Le premier report gardait les **24 px** du cadre (titre finissant à 84, barre à 108) et
> posait donc la barre à **124** et la liste à **212**. Ce 24 était l'air d'un **titre nu** ;
> le plateau est une **boîte bordée**, dont le trait descend là où l'encre du titre ne
> descendait pas. Deux boîtes bordées de la même grammaire prennent l'**écart de bloc du
> §3.3, 16 px** — celui de Peaufiner, des Réglages et du Cercle. La barre tombe à **116**,
> la liste à **204**, le menu de tri à **178** : tout ce qui suit remonte de 8.
> **Rien d'autre ne bouge** — largeurs, hauteurs, contours, rayons, et l'écart barre → liste
> (36) sont inchangés. Recensé dans `ECARTS-MOODBOARD.md § 0 bis.5` ; juge mis à jour, sa
> version d'avant est dans `sauvegardes/releve-S4-index-fil-avant-air-16.py`.
>
> ⚠ **Ce qui NE change pas** : la couleur du compte (`#3A54FF`), la famille et la graisse
> de l'entête (Bricolage 700), la loi de la carte d'Index (§3.9), la borne du §2.5.
> Le juge `releve-S4-index-fil.py` est mis à jour en conséquence ; sa version d'avant est
> dans `sauvegardes/releve-S4-avant-encart.py`.

## 5 · Inventaire écran par écran — le produit
**128 écrans.** Pour chacun : le fond, puis chaque élément positionné avec ses coordonnées absolues et son style complet. `x` et `y` sont le coin haut-gauche. Les SVG sont les traits, les dalles et les anneaux.

---

## Fiches Promi

### Promi · à tenir — sombre

*Ma moitié est tracée depuis la plantation, celle de dimanche reste en points. Les Noyaux ouvrent le corps : le tien, puis celui de Rachel. Aucun chiffre, aucun classement.*

Fond `#12142A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · DANS 2 JOURS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · en cours — sombre

*Rien n'est dû : la ligne prend la teinte de la dalle, pas le terracotta.*

Fond `#12142A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #CBAAFF · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #CBAAFF · interlettre -.01em | À moi |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | nager le mardi |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #CBAAFF · interlettre .20em | EN COURS · DEPUIS LE 4 AVRIL |
| bloc texte | 24 | 647 | 342 | 66 | Bricolage 600 / 18 · couleur #F4EEE1 · contour 3px solid #CBAAFF · rayon 33 | écris un mot |
| · dedans | interne | interne | — | — | — | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · tenue — sombre

*Les deux moitiés sont tracées : le trait est plein d'un bord à l'autre. C'est la signature de cette parole, et elle reste.*

Fond `#12142A` · **trait : base = 376, amplitude = 48, boîte SVG = 464**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 464 | — |  |
| bloc | 58 | 88 | — | — | — |  |
| DALLE | interne | interne | 273 | 228 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 468 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc texte | 24 | 592 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 622 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 687 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE · 12 MARS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · titre long — sombre

*Deux lignes à 36 px au lieu d'une à 42 : la composition ne dépend pas du texte.*

Fond `#12142A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 36 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | aller voir la mer avant l'automne |
| bloc texte | 24 | 640 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · CE SOIR |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Fiches Chiche

### Chiche · lancé — sombre

*Ma moitié est tracée, celle de Marion n'existera que si elle relève. La ligne garde la teinte de la dalle : tant que le chiche n'est pas relevé, rien n'est dû par personne.*

Fond `#25101A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Marion |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #FFC0A8 · interlettre -.01em · aligné center | Marion complètera si elle relève |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #FFC0A8 · interlettre -.01em | À Marion |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #FFC0A8 · interlettre .20em | LANCÉ · PAS ENCORE RELEVÉ |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Chiche · relevé — sombre

*Marion a relevé : la ligne passe au terracotta, et le compagnon apparaît en second Noyau. Deux créneaux, jamais fusionnés.*

Fond `#25101A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Marion |
| bloc | 220 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | avec Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 19 · couleur #F07A2E · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | RELEVÉ · À TENIR À DEUX |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Chiche · tenu à deux — sombre

*Les deux moitiés se rejoignent au milieu : le dessin n'existe que parce que les deux ont tenu.*

Fond `#25101A` · **trait : base = 372, amplitude = 44, boîte SVG = 456**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 456 | — |  |
| bloc | 58 | 88 | — | — | — |  |
| DALLE | interne | interne | 273 | 228 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 460 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 470 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Marion |
| bloc texte | 24 | 584 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Marion |
| bloc texte | 24 | 614 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le grand plongeoir |
| bloc texte | 24 | 718 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENU À DEUX · 3 AOÛT |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Fiches Nuée

### Nuée · avec des Promi — sombre

*La zone haute porte <b>les dalles de tous les Promi plantés dans la Nuée</b>, pas une dalle unique. Chaque Promi se lit en réduction de sa carte d'Index : sa dalle, son trait, sa couleur d'état.*

Fond `#1A1230` · **trait : base = 232, amplitude = 36, boîte SVG = 308**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 308 | — |  |
| bloc | 30 | 96 | — | — | — |  |
| DALLE | interne | interne | 108 | 86 | — |  |
| bloc | 150 | 88 | — | — | — |  |
| DALLE | interne | interne | 118 | 94 | — |  |
| bloc | 278 | 100 | — | — | — |  |
| DALLE | interne | interne | 92 | 74 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 312 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 322 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 436 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 466 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 531 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 6 PROMI · 1 TENU |
| bloc | 24 | 561 | 342 | 74 | fond #271B45 · rayon 20 |  |
| DALLE | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| DALLE | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | arroser tous les soirs |
| bloc | 24 | 647 | 342 | 74 | fond #271B45 · rayon 20 |  |
| DALLE | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| DALLE | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | semer les radis |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Nuée · vide — sombre

*Aucun Promi, donc aucune dalle : la zone haute est nue et la Nuée n'attend qu'une chose.*

Fond `#1A1230` · **trait : base = 282, amplitude = 44, boîte SVG = 366**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 366 | — |  |
| bloc | 112 | 88 | — | — | — |  |
| DALLE | interne | interne | 165 | 138 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 370 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 380 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | l'atelier |
| bloc texte | 24 | 494 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec toi seulement |
| bloc texte | 24 | 524 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | l'atelier du samedi |
| bloc texte | 24 | 628 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | AUCUN PROMI ENCORE |
| bloc texte | 24 | 672 | — | — | Bricolage 700 / 18.5 · couleur #D0B0FF · interlettre -.01em | plante le premier Promi de la Nuée ↑ |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Gardé de côté

### Gardé de côté · Promi — sombre

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#12142A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #3A54FF · interlettre -.01em | trace pour planter |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #3A54FF · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | appeler Mamie |
| bloc texte | 24 | 481 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · 2 AVRIL |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Gardé de côté · Chiche — sombre

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#25101A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #FA2258 · interlettre -.01em | trace pour lancer |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #FA2258 · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le grand plongeoir |
| bloc texte | 24 | 520 | — | — | Apfel 500 / 12.5 · couleur #FA2258 · interlettre .20em | GARDÉ DE CÔTÉ · PERSONNE DE DÉFIÉ |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Gardé de côté · Nuée — sombre

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#1A1230` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #8A5CF0 · interlettre -.01em | trace pour lancer |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #8A5CF0 · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | l'atelier du samedi |
| bloc texte | 24 | 520 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | GARDÉ DE CÔTÉ · PERSONNE D'INVITÉ |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## États de fiche

### Avec commentaires — sombre

*Blocs pleins, jamais de rectangle translucide. Le nom prend la couleur d'état.*

Fond `#12142A` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 474 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Rachel |
| bloc texte | 24 | 504 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc | 24 | 566 | 342 | 76 | Bricolage 400 / — · couleur #F4EEE1 · fond #1C2049 · rayon 22 |  |
| · dedans | interne | interne | — | — | couleur #2BE88C | Rachel |
| · dedans | interne | interne | — | — | — | elles étaient parfaites. |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Sans commentaire — sombre

*L'invitation est une phrase, pas un champ vide.*

Fond `#12142A` · **trait : base = 338, amplitude = 46, boîte SVG = 424**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 424 | — |  |
| bloc | 80 | 88 | — | — | — |  |
| DALLE | interne | interne | 230 | 192 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 428 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc texte | 24 | 552 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 582 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 654 | 342 | 66 | Bricolage 600 / 18 · couleur #F4EEE1 · contour 3px solid #CBAAFF · rayon 33 | personne n'a rien dit — commence |
| · dedans | interne | interne | — | — | — | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## L'instant

### L'autre moitié arrive — sombre

Fond `#12142A` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 105 | 91 | — | — | — |  |
| DALLE | interne | interne | 180 | 150 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 388 | 342 | — | Bricolage 700 / 17 · couleur #2BE88C · aligné center | l'autre moitié arrive |
| bloc | 24 | 432 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 442 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 556 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 586 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le trait se referme — sombre

Fond `#12142A` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 81 | 88 | — | — | — |  |
| DALLE | interne | interne | 228 | 190 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 388 | 342 | — | Bricolage 700 / 64 · couleur #F4EEE1 · interlettre -.04em · interligne 1 | tenue. |
| bloc texte | 24 | 472 | 342 | — | Bricolage 600 / 20 · couleur #F4EEE1 · interligne 1.3 | Rachel vient de tracer sa moitié. Le dessin existe. |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Juste après — sombre

Fond `#12142A` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 105 | 91 | — | — | — |  |
| DALLE | interne | interne | 180 | 150 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Rachel |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE À DEUX · À L'INSTANT |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Index et Fil

### Index 2 par ligne — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.035em | Index |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #3A54FF | 12 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 | ⇅ |
| bloc | 24 | 196 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #1C2049 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 135 | — |  |
| bloc | 36 | 9 | — | — | — |  |
| DALLE | interne | interne | 92 | 77 | — |  |
| bloc texte | 12 | 124 | — | — | Bricolage 600 / 12.4 · couleur #2BE88C | à moi |
| bloc texte | 12 | 141 | 140 | 33 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 201 | 196 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #1C2049 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 107 | — |  |
| bloc | 97 | 9 | — | — | — |  |
| DALLE | interne | interne | 58 | 49 | — |  |
| bloc texte | 12 | 97 | — | — | Bricolage 600 / 12.4 · couleur #F07A2E | à Rachel |
| bloc texte | 12 | 114 | 140 | 60 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 24 | 406 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #271B45 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 147 | — |  |
| bloc | 9 | 9 | — | — | — |  |
| DALLE | interne | interne | 106 | 89 | — |  |
| bloc texte | 12 | 136 | — | — | Bricolage 600 / 12.4 · couleur #D0B0FF | avec +4 |
| bloc texte | 12 | 153 | 140 | 21 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #D0B0FF · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 201 | 406 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #37141F · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 99 | — |  |
| bloc | 58 | 9 | — | — | — |  |
| DALLE | interne | interne | 49 | 41 | — |  |
| bloc texte | 12 | 89 | — | — | Bricolage 600 / 12.4 · couleur #FFC0A8 | à Marion |
| bloc texte | 12 | 106 | 140 | 68 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #FFC0A8 · interlettre .18em | LANCÉ |
| bloc | 24 | 616 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #1C2049 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 123 | — |  |
| bloc | 77 | 9 | — | — | — |  |
| DALLE | interne | interne | 78 | 65 | — |  |
| bloc texte | 12 | 113 | — | — | Bricolage 600 / 12.4 · couleur #CBAAFF | à moi |
| bloc texte | 12 | 130 | 140 | 44 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #CBAAFF · interlettre .18em | EN COURS |
| bloc | 201 | 616 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #37141F · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 131 | — |  |
| bloc | 39 | 9 | — | — | — |  |
| DALLE | interne | interne | 87 | 73 | — |  |
| bloc texte | 12 | 120 | — | — | Bricolage 600 / 12.4 · couleur #2BE88C | à Marion |
| bloc texte | 12 | 137 | 140 | 37 | Bricolage 700 / 20.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #2BE88C · interlettre .18em | TENU À DEUX |

### Index 3 par ligne — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.035em | Index |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #3A54FF | 12 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 | ⇅ |
| bloc | 24 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 97 | — |  |
| bloc | 22 | 6 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 7 | 83 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à moi |
| bloc texte | 7 | 94 | 90 | 24 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 142 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 78 | — |  |
| bloc | 60 | 6 | — | — | — |  |
| DALLE | interne | interne | 39 | 33 | — |  |
| bloc texte | 7 | 64 | — | — | Bricolage 600 / 8.0 · couleur #F07A2E | à Rachel |
| bloc texte | 7 | 75 | 90 | 43 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 260 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #271B45 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 105 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 72 | 60 | — |  |
| bloc texte | 7 | 91 | — | — | Bricolage 600 / 8.0 · couleur #D0B0FF | avec +4 |
| bloc texte | 7 | 102 | 90 | 20 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #D0B0FF · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 24 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #37141F · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 73 | — |  |
| bloc | 36 | 6 | — | — | — |  |
| DALLE | interne | interne | 33 | 28 | — |  |
| bloc texte | 7 | 59 | — | — | Bricolage 600 / 8.0 · couleur #FFC0A8 | à Marion |
| bloc texte | 7 | 70 | 90 | 48 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #FFC0A8 · interlettre .18em | LANCÉ |
| bloc | 142 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 89 | — |  |
| bloc | 47 | 6 | — | — | — |  |
| DALLE | interne | interne | 52 | 44 | — |  |
| bloc texte | 7 | 75 | — | — | Bricolage 600 / 8.0 · couleur #CBAAFF | à moi |
| bloc texte | 7 | 86 | 90 | 32 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #CBAAFF · interlettre .18em | EN COURS |
| bloc | 260 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #37141F · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 94 | — |  |
| bloc | 24 | 6 | — | — | — |  |
| DALLE | interne | interne | 58 | 49 | — |  |
| bloc texte | 7 | 80 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à Marion |
| bloc texte | 7 | 91 | 90 | 27 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENU À DEUX |
| bloc | 24 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #271B45 · rayon 11 · outline 2px dashed #8A5CF0 |  |
| DALLE | 0 | 0 | 106 | 86 | — |  |
| bloc | 28 | 6 | — | — | — |  |
| DALLE | interne | interne | 49 | 41 | — |  |
| bloc texte | 7 | 72 | — | — | Bricolage 600 / 8.0 · couleur #8A5CF0 | gardé de côté |
| bloc texte | 7 | 83 | 90 | 35 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | l'atelier du samedi |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #8A5CF0 · interlettre .18em | GARDÉ DE CÔTÉ |
| bloc | 142 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 · outline 2px dashed #3A54FF |  |
| DALLE | 0 | 0 | 106 | 81 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 43 | 36 | — |  |
| bloc texte | 7 | 67 | — | — | Bricolage 600 / 8.0 · couleur #3A54FF | gardé de côté |
| bloc texte | 7 | 78 | 90 | 40 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | appeler Mamie |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #3A54FF · interlettre .18em | GARDÉ DE CÔTÉ |
| bloc | 260 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 97 | — |  |
| bloc | 22 | 6 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 7 | 83 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à moi |
| bloc texte | 7 | 94 | 90 | 24 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 24 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #1C2049 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 78 | — |  |
| bloc | 60 | 6 | — | — | — |  |
| DALLE | interne | interne | 39 | 33 | — |  |
| bloc texte | 7 | 64 | — | — | Bricolage 600 / 8.0 · couleur #F07A2E | à Rachel |
| bloc texte | 7 | 75 | 90 | 43 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 142 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #271B45 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 105 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 72 | 60 | — |  |
| bloc texte | 7 | 91 | — | — | Bricolage 600 / 8.0 · couleur #D0B0FF | avec +4 |
| bloc texte | 7 | 102 | 90 | 20 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #D0B0FF · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 260 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #37141F · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 73 | — |  |
| bloc | 36 | 6 | — | — | — |  |
| DALLE | interne | interne | 33 | 28 | — |  |
| bloc texte | 7 | 59 | — | — | Bricolage 600 / 8.0 · couleur #FFC0A8 | à Marion |
| bloc texte | 7 | 70 | 90 | 48 | Bricolage 700 / 12.9 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #FFC0A8 · interlettre .18em | LANCÉ |

### Fil — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.035em | Fil |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #2BE88C | 4 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #F4EEE1 · contour 3px solid #5D636D · rayon 28 | ⇅ |
| bloc | 16 | 196 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #37141F · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FFC0A8 | Marion te lance un chiche |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | le grand plongeoir |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #FFC0A8 · interlettre .18em | À RELEVER |
| bloc | 16 | 336 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #1C2049 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | à moi |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | planter un arbre |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | TENUE · IL Y A 2 H |
| bloc | 16 | 476 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #271B45 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #D0B0FF | Adrien a planté |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | semer les radis |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #D0B0FF · interlettre .18em | LE POTAGER · 6 PROMI |
| bloc | 16 | 616 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #1C2049 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #F07A2E | à Rachel |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | faire les crêpes |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 16 | 756 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #37141F · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | Marion a relevé |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | courir dimanche |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | RELEVÉ · À TENIR À DEUX |

---

## Cartes d'Index isolées

### Carte 1 · planter un arbre — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #1C2049 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 141 | — |  |
| bloc | 38 | 10 | — | — | — |  |
| DALLE | interne | interne | 97 | 81 | — |  |
| bloc texte | 13 | 131 | — | — | Bricolage 600 / 13.0 · couleur #2BE88C | à moi |
| bloc texte | 13 | 149 | 147 | 33 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENUE |

### Carte 2 · faire les crêpes — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #1C2049 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 112 | — |  |
| bloc | 101 | 10 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 13 | 102 | — | — | Bricolage 600 / 13.0 · couleur #F07A2E | à Rachel |
| bloc texte | 13 | 120 | 147 | 62 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |

### Carte 3 · le potager — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #271B45 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 153 | — |  |
| bloc | 10 | 10 | — | — | — |  |
| DALLE | interne | interne | 111 | 93 | — |  |
| bloc texte | 13 | 143 | — | — | Bricolage 600 / 13.0 · couleur #D0B0FF | avec +4 |
| bloc texte | 13 | 161 | 147 | 21 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #D0B0FF · interlettre .18em | 6 PROMI · 1 TENU |

### Carte 4 · courir dimanche — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #37141F · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 103 | — |  |
| bloc | 61 | 10 | — | — | — |  |
| DALLE | interne | interne | 51 | 43 | — |  |
| bloc texte | 13 | 93 | — | — | Bricolage 600 / 13.0 · couleur #FFC0A8 | à Marion |
| bloc texte | 13 | 111 | 147 | 71 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #FFC0A8 · interlettre .18em | LANCÉ |

### Carte 5 · nager le mardi — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #1C2049 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 128 | — |  |
| bloc | 82 | 10 | — | — | — |  |
| DALLE | interne | interne | 81 | 68 | — |  |
| bloc texte | 13 | 118 | — | — | Bricolage 600 / 13.0 · couleur #CBAAFF | à moi |
| bloc texte | 13 | 136 | 147 | 46 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #CBAAFF · interlettre .18em | EN COURS |

### Carte 6 · le grand plongeoir — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #37141F · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 137 | — |  |
| bloc | 40 | 10 | — | — | — |  |
| DALLE | interne | interne | 92 | 77 | — |  |
| bloc texte | 13 | 127 | — | — | Bricolage 600 / 13.0 · couleur #2BE88C | à Marion |
| bloc texte | 13 | 145 | 147 | 37 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU À DEUX |

### Carte 7 · l'atelier du samedi — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #271B45 · rayon 18 · outline 3px dashed #8A5CF0 |  |
| DALLE | 0 | 0 | 173 | 124 | — |  |
| bloc | 48 | 10 | — | — | — |  |
| DALLE | interne | interne | 76 | 64 | — |  |
| bloc texte | 13 | 114 | — | — | Bricolage 600 / 13.0 · couleur #8A5CF0 | gardé de côté |
| bloc texte | 13 | 132 | 147 | 50 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | l'atelier du samedi |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #8A5CF0 · interlettre .18em | GARDÉ DE CÔTÉ |

### Carte 8 · appeler Mamie — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #1C2049 · rayon 18 · outline 3px dashed #3A54FF |  |
| DALLE | 0 | 0 | 173 | 116 | — |  |
| bloc | 10 | 10 | — | — | — |  |
| DALLE | interne | interne | 67 | 56 | — |  |
| bloc texte | 13 | 106 | — | — | Bricolage 600 / 13.0 · couleur #3A54FF | gardé de côté |
| bloc texte | 13 | 124 | 147 | 58 | Bricolage 700 / 21.0 · couleur #F4EEE1 · interlettre -.025em · interligne 1 | appeler Mamie |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #3A54FF · interlettre .18em | GARDÉ DE CÔTÉ |

---

## Bandeaux du Fil isolés

### Bandeau 1 · le grand plongeoir — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #37141F · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FFC0A8 | Marion te lance un chiche |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | le grand plongeoir |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #FFC0A8 · interlettre .18em | À RELEVER |

### Bandeau 2 · planter un arbre — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #1C2049 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | à moi |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | planter un arbre |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | TENUE · IL Y A 2 H |

### Bandeau 3 · semer les radis — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #271B45 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #D0B0FF | Adrien a planté |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | semer les radis |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #D0B0FF · interlettre .18em | LE POTAGER · 6 PROMI |

### Bandeau 4 · faire les crêpes — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #1C2049 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #F07A2E | à Rachel |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | faire les crêpes |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |

### Bandeau 5 · courir dimanche — sombre

Fond `#0E0F12`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #37141F · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | Marion a relevé |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #F4EEE1 · interlettre -.025em · interligne 1.04 | courir dimanche |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | RELEVÉ · À TENIR À DEUX |

---

## Les Noyaux

### Noyaux · Promi à soi — sombre

Fond `#12142A` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE · 12 MARS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · Promi à Rachel — sombre

Fond `#12142A` · **trait : base = 268, amplitude = 44, boîte SVG = 352**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 352 | — |  |
| bloc | 121 | 88 | — | — | — |  |
| DALLE | interne | interne | 148 | 124 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 356 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc | 24 | 392 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Rachel |
| bloc texte | 24 | 516 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 546 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 611 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · DIMANCHE |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · Chiche à deux — sombre

Fond `#25101A` · **trait : base = 268, amplitude = 44, boîte SVG = 352**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 352 | — |  |
| bloc | 121 | 88 | — | — | — |  |
| DALLE | interne | interne | 148 | 124 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 356 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc | 24 | 392 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Marion |
| bloc | 220 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | avec Rachel |
| bloc texte | 24 | 516 | — | — | Bricolage 600 / 19 · couleur #F07A2E · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 546 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 611 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | RELEVÉ · À TENIR À DEUX |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · dans une Nuée — sombre

Fond `#1A1230` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | semer les radis |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | DANS LE POTAGER |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · l'anneau du Cercle — sombre

Fond `#25101A` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | Marion |
| bloc | 220 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | avec Rachel |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 19 · couleur #2BE88C · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENU À DEUX · 3 AOÛT |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Page +

### Choix des trois natures — sombre

Fond `#16171B`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 40 | — | 34 | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 96 | 342 | — | Bricolage 700 / 46 · couleur #F4EEE1 · interlettre -.035em · interligne .95 | Qu'est-ce que tu promets ? |
| bloc | 16 | 246 | 358 | 174 | fond #3A54FF · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Un Promi |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | à quelqu'un, ou à toi |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |
| bloc | 16 | 436 | 358 | 174 | fond #FA2258 · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Un Chiche |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | un défi lancé |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |
| bloc | 16 | 626 | 358 | 174 | fond #8A5CF0 · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Une Nuée |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | un groupe, un projet |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |

### Promi · phrase vide — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · contour 3px dashed #CBAAFF · rayon 16 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 574 | 342 | — | Bricolage 600 / 17.5 · couleur #CBAAFF · interligne 1.4 | touche ⇄ pour changer d'intention · touche un mot pour l'écrire  |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · à soi rempli — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · à Rachel — sombre

Fond `#12142A` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 453 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #CBAAFF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | faire les crêpes |
| bloc | 24 | 514 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #CBAAFF · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em · interligne 1.1 · écart 7px | Rachel |
| VISAGE | interne | interne | 23 | 23 | fond #3A54FF · rayon 999 |  |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · promets-moi — sombre

Fond `#12142A` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em · interligne 1.1 · écart 8px | Rachel, |
| VISAGE | interne | interne | 27 | 27 | fond #3A54FF · rayon 999 |  |
| bloc | 24 | 459 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | promets-moi |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 526 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #CBAAFF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | m'appeler |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · promettez-moi — sombre

Fond `#12142A` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em · interligne 1.1 · écart 8px | Rachel, Nico, |
| VISAGE | interne | interne | 26 | 26 | fond #3A54FF · rayon 999 |  |
| bloc | 24 | 458 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | promettez-moi |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 524 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #CBAAFF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | venir dimanche |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Chiche · vide — sombre

Fond `#25101A` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · contour 3px dashed #FFC0A8 · rayon 16 · interlettre -.03em | qui ? |
| bloc | 24 | 455 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #FA2258 · rayon 18 · interlettre -.03em | Chiche |
| bloc | 24 | 518 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · contour 3px dashed #FFC0A8 · rayon 16 · interlettre -.03em | courir dimanche |
| bloc texte | 24 | 615 | 342 | — | Bricolage 600 / 17.5 · couleur #FFC0A8 · interligne 1.4 | le compagnon et l'échéance sont dans Peaufiner |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Chiche · rempli — sombre

Fond `#25101A` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em · interligne 1.1 · écart 7px | Marion, |
| VISAGE | interne | interne | 25 | 25 | fond #FA2258 · rayon 999 |  |
| bloc | 24 | 455 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #FA2258 · rayon 18 · interlettre -.03em | chiche |
| bloc | 24 | 518 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FFC0A8 · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | courir dimanche |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #FFC0A8 · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Nuée · écriture — sombre

Fond `#1A1230` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #8A5CF0 · rayon 18 · interlettre -.03em | Je lance une Nuée |
| bloc | 24 | 450 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #D0B0FF · interlettre -.03em | nommée |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | Lisbonne |
| bloc | 24 | 508 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #D0B0FF · interlettre -.03em | avec |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | Rachel · Adrien |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #D0B0FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Choix ouvert · écrire un mot — sombre

Fond `#12142A` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 57 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 337 | 342 | 57 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer\| |
| bloc texte | 24 | 420 | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .20em | DÉJÀ PROMIS |
| bloc texte | 24 | 446 | — | 50 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 25 | nager le mardi |
| bloc texte | 201 | 446 | — | 50 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 25 | appeler Mamie |
| bloc texte | 17 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | a |
| bloc texte | 53 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | z |
| bloc texte | 89 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | e |
| bloc texte | 125 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | r |
| bloc texte | 161 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | t |
| bloc texte | 197 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | y |
| bloc texte | 233 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | u |
| bloc texte | 269 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | i |
| bloc texte | 305 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | o |
| bloc texte | 341 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | p |
| bloc texte | 17 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | q |
| bloc texte | 53 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | s |
| bloc texte | 89 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | d |
| bloc texte | 125 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | f |
| bloc texte | 161 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | g |
| bloc texte | 197 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | h |
| bloc texte | 233 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | j |
| bloc texte | 269 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | k |
| bloc texte | 305 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | l |
| bloc texte | 341 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | m |
| bloc texte | 89 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | w |
| bloc texte | 125 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | x |
| bloc texte | 161 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | c |
| bloc texte | 197 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | v |
| bloc texte | 233 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | b |
| bloc texte | 269 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #F4EEE1 · fond #2A2D34 · rayon 9 | n |

### Choix ouvert · choisir une personne — sombre

Fond `#12142A` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je promets |
| bloc | 24 | 340 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #CBAAFF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | faire les crêpes |
| bloc | 24 | 400 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #CBAAFF · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #CBAAFF · contour 3px dashed #CBAAFF · rayon 16 · interlettre -.03em | qui ? |
| bloc texte | 24 | 486 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · fond #3A54FF · contour 3px solid #3A54FF · rayon 26 · écart 10px | Rachel |
| · dedans | interne | interne | 28 | 28 | couleur #3A54FF · fond #F4EEE1 · rayon 999 | R |
| bloc texte | 198 | 486 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 26 · écart 10px | Nico |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | N |
| bloc texte | 24 | 546 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 26 · écart 10px | Marion |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | M |
| bloc texte | 198 | 546 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 26 · écart 10px | Léo |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | L |
| bloc texte | 24 | 606 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 26 · écart 10px | Adrien |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | A |
| bloc texte | 198 | 606 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 26 · écart 10px | Camille |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | C |
| bloc texte | 24 | 680 | 342 | 52 | Bricolage 700 / 16 · couleur #CBAAFF · contour 3px dashed #CBAAFF · rayon 26 | + ajouter quelqu'un |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Choix ouvert · l'échéance — sombre

Fond `#12142A` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #CBAAFF · interlettre -.03em | avant |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #CBAAFF · contour 3px dashed #CBAAFF · rayon 16 · interlettre -.03em | quand ? |
| bloc texte | 24 | 366 | — | 50 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 25 | ce soir |
| bloc texte | 131 | 366 | — | 50 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 25 | demain |
| bloc texte | 230 | 366 | — | 50 | Bricolage 700 / 16 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 25 | dimanche |
| bloc | 24 | 428 | 342 | — | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 24 · couleur #F4EEE1 · interlettre -.02em | mai |
| · dedans | interne | interne | — | — | Bricolage 700 / 19 · couleur #CBAAFF | 2026 › |
| bloc texte | 24 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | L |
| bloc texte | 73 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | M |
| bloc texte | 122 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | M |
| bloc texte | 171 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | J |
| bloc texte | 220 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | V |
| bloc texte | 269 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | S |
| bloc texte | 318 | 466 | 42 | — | Apfel 500 / 11 · couleur #CBAAFF · interlettre .14em · aligné center | D |
| bloc texte | 221 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 1 |
| bloc texte | 270 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 2 |
| bloc texte | 319 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 3 |
| bloc texte | 25 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 4 |
| bloc texte | 74 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 5 |
| bloc texte | 123 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 6 |
| bloc texte | 172 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 7 |
| bloc texte | 221 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 8 |
| bloc texte | 270 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 9 |
| bloc texte | 319 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 10 |
| bloc texte | 25 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 11 |
| bloc texte | 74 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · fond #3A54FF · rayon 17 | 12 |
| bloc texte | 123 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 13 |
| bloc texte | 172 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 14 |
| bloc texte | 221 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 15 |
| bloc texte | 270 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 16 |
| bloc texte | 319 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 17 |
| bloc texte | 25 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 18 |
| bloc texte | 74 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 19 |
| bloc texte | 123 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 20 |
| bloc texte | 172 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 21 |
| bloc texte | 221 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 22 |
| bloc texte | 270 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 23 |
| bloc texte | 319 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 24 |
| bloc texte | 25 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 25 |
| bloc texte | 74 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 26 |
| bloc texte | 123 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 27 |
| bloc texte | 172 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 28 |
| bloc texte | 221 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 29 |
| bloc texte | 270 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 30 |
| bloc texte | 319 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · rayon 17 | 31 |
| bloc texte | 24 | 680 | 162 | 56 | Bricolage 700 / 17 · couleur #CBAAFF · contour 3px solid #CBAAFF · rayon 28 | un jour |
| bloc texte | 198 | 680 | 162 | 56 | Bricolage 700 / 17 · couleur #CBAAFF · contour 3px solid #CBAAFF · rayon 28 | en l'air |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Garder de côté — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Gardé de côté · après — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace pour planter |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 558 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · RIEN N'EST PROMIS |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Le geste · au repos — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #F4EEE1 · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 702 | — | — | Bricolage 600 / 16 · couleur #CBAAFF · underline | planter au bouton |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le geste · pendant — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 160 | 372 | — | — | Bricolage 700 / 18.5 · couleur #F07A2E · interlettre -.01em | continue → |
| bloc | 24 | 454 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 512 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le geste · signé — sombre

Fond `#12142A` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 180 | 372 | — | — | Bricolage 700 / 18.5 · couleur #F07A2E · interlettre -.01em | planté · à tenir avant l'été |
| bloc | 24 | 454 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 512 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #CBAAFF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #16171B · fond #F4EEE1 · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Peaufiner

### Peaufiner Promi · haut — sombre

Fond `#12142A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.03em | aller voir la mer |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | À QUI |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | Rachel |
| bloc | 24 | 190 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | dimanche |
| bloc | 24 | 270 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | DANS UNE NUÉE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | le potager |
| bloc | 24 | 350 | 342 | 118 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | NOTE |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #CBAAFF · interligne 1.25 | ajoute un mot, un contexte… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #CBAAFF | visible par Rachel |
| bloc | 24 | 484 | 342 | 92 | contour 3px solid #F4EEE1 · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | 2 fichiers |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #CBAAFF | visibles par Rachel |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Promi · suite — sombre

Fond `#12142A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 46 | 342 | 118 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #CBAAFF · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #CBAAFF | visible par Rachel · vous pouvez répondre |
| bloc | 24 | 180 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RELANCER RACHEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | → |
| bloc | 24 | 260 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | · ·· ··· |
| bloc | 24 | 340 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | chaque semaine |
| bloc | 24 | 420 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | la veille à 19:00 |
| bloc | 24 | 500 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | réveille tes « en l'air » |
| bloc | 24 | 368 | 342 | 90 | fond #F4EEE1 · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #AE86F2 · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #AE86F2 | importance, récurrence, rappels, mémoire |
| bloc | 24 | 668 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | SUPPRIMER CE PROMI |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le bloc du Cercle — sombre

Fond `#12142A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 70 | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.02em | Le Cercle |
| bloc | 24 | 130 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | · ·· ··· |
| bloc | 24 | 210 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | chaque semaine |
| bloc | 24 | 290 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | la veille à 19:00 |
| bloc | 24 | 370 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | réveille tes « en l'air » |
| bloc | 24 | 238 | 342 | 90 | fond #F4EEE1 · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #AE86F2 · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #AE86F2 | importance, récurrence, rappels, mémoire |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Nuée · haut — sombre

Fond `#1A1230`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.03em | le potager |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 104 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #D0B0FF · interlettre .18em | DESCRIPTION |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #D0B0FF · interligne 1.25 | présente la Nuée, son but… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #D0B0FF | visible par tous les membres |
| bloc | 24 | 230 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #D0B0FF · interlettre .18em | MEMBRES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | Rachel · Adrien · +3 |
| bloc | 24 | 310 | 342 | 92 | contour 3px solid #F4EEE1 · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #D0B0FF · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | 2 fichiers |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #D0B0FF | visibles par la Nuée |
| bloc | 24 | 418 | 342 | 104 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #D0B0FF · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #D0B0FF · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #D0B0FF | visibles par les membres de la Nuée |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Nuée · bas — sombre

Fond `#1A1230`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 46 | 342 | 62 | Bricolage 700 / 19 · couleur #F4EEE1 · fond #8A5CF0 · contour 3px solid #8A5CF0 · rayon 31 | Planter un Promi dans la Nuée |
| bloc | 24 | 124 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #D0B0FF · interlettre .18em | DISSOUDRE LA NUÉE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | → |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Chiche · haut — sombre

Fond `#25101A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.03em | courir dimanche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | À QUI JE LANCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | Marion |
| bloc | 24 | 190 | 342 | 64 | contour 3px dashed #FFC0A8 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | AVEC |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #FFC0A8 | personne |
| bloc | 24 | 270 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | l'été |
| bloc | 24 | 350 | 342 | 118 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | NOTE |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #FFC0A8 · interligne 1.25 | ajoute un mot, un contexte… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #FFC0A8 | visible par Marion |
| bloc | 24 | 484 | 342 | 92 | contour 3px solid #F4EEE1 · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | 1 fichier |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FFC0A8 | visibles par Marion |
| bloc | 24 | 592 | 342 | 104 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #FFC0A8 · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #FFC0A8 | visibles par Marion · vous pouvez répondre |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Chiche · bas — sombre

Fond `#25101A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 46 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | RELANCER MARION |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | → |
| bloc | 24 | 126 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | · ·· ··· |
| bloc | 24 | 206 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | chaque semaine |
| bloc | 24 | 286 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | la veille à 19:00 |
| bloc | 24 | 366 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | réveille tes « en l'air » |
| bloc | 24 | 234 | 342 | 90 | fond #F4EEE1 · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #F2977A · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #F2977A | importance, récurrence, rappels, mémoire |
| bloc | 24 | 534 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FFC0A8 · interlettre .18em | SUPPRIMER CE CHICHE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | → |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Fiche gardée de côté — sombre

Fond `#12142A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 350 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 336 | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.02em | planter un arbre |
| bloc texte | 24 | 396 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · RIEN N'EST PROMIS |
| bloc texte | 24 | 430 | 342 | 62 | Bricolage 700 / 19 · couleur #F4EEE1 · fond #3A54FF · contour 3px solid #3A54FF · rayon 31 | Planter |
| bloc | 24 | 508 | 342 | 64 | contour 3px dashed #CBAAFF · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #CBAAFF | pas encore |
| bloc texte | 24 | 588 | 342 | 62 | Bricolage 700 / 19 · couleur #F4EEE1 · contour 3px solid #F4EEE1 · rayon 31 | Reprendre l'écriture |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Réglages généraux — sombre

Fond `#12142A`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.035em | Réglages |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 112 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | NOTIFICATIONS |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | activées |
| bloc | 24 | 190 | 342 | 92 | contour 3px solid #F4EEE1 · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | ASSISTANCE DU TRAIT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | moyenne |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #CBAAFF | lisse le tremblement sans redresser ton geste |
| bloc | 24 | 296 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | THÈME |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | automatique |
| bloc | 24 | 374 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | · ·· ··· |
| bloc | 24 | 454 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | chaque semaine |
| bloc | 24 | 534 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | la veille à 19:00 |
| bloc | 24 | 614 | 342 | 64 | contour 3px solid #F4EEE1 · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #CBAAFF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #F4EEE1 | réveille tes « en l'air » |
| bloc | 24 | 482 | 342 | 90 | fond #F4EEE1 · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #AE86F2 · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #AE86F2 | importance, récurrence, rappels, mémoire |

---

## Fiches Promi

### Promi · à tenir — clair

*Ma moitié est tracée depuis la plantation, celle de dimanche reste en points. Les Noyaux ouvrent le corps : le tien, puis celui de Rachel. Aucun chiffre, aucun classement.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · DANS 2 JOURS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · en cours — clair

*Rien n'est dû : la ligne prend la teinte de la dalle, pas le terracotta.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #3A54FF · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #3A54FF · interlettre -.01em | À moi |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | nager le mardi |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | EN COURS · DEPUIS LE 4 AVRIL |
| bloc texte | 24 | 647 | 342 | 66 | Bricolage 600 / 18 · couleur #16171B · contour 3px solid #3A54FF · rayon 33 | écris un mot |
| · dedans | interne | interne | — | — | — | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · tenue — clair

*Les deux moitiés sont tracées : le trait est plein d'un bord à l'autre. C'est la signature de cette parole, et elle reste.*

Fond `#F4EEE1` · **trait : base = 376, amplitude = 48, boîte SVG = 464**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 464 | — |  |
| bloc | 58 | 88 | — | — | — |  |
| DALLE | interne | interne | 273 | 228 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 468 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc texte | 24 | 592 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 622 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 687 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE · 12 MARS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Promi · titre long — clair

*Deux lignes à 36 px au lieu d'une à 42 : la composition ne dépend pas du texte.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 36 · couleur #16171B · interlettre -.025em · interligne 1.02 | aller voir la mer avant l'automne |
| bloc texte | 24 | 640 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · CE SOIR |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Fiches Chiche

### Chiche · lancé — clair

*Ma moitié est tracée, celle de Marion n'existera que si elle relève. La ligne garde la teinte de la dalle : tant que le chiche n'est pas relevé, rien n'est dû par personne.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Marion |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #FA2258 · interlettre -.01em · aligné center | Marion complètera si elle relève |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 21 · couleur #FA2258 · interlettre -.01em | À Marion |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #FA2258 · interlettre .20em | LANCÉ · PAS ENCORE RELEVÉ |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Chiche · relevé — clair

*Marion a relevé : la ligne passe au terracotta, et le compagnon apparaît en second Noyau. Deux créneaux, jamais fusionnés.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Marion |
| bloc | 220 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | avec Rachel |
| bloc texte | 24 | 474 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc texte | 24 | 510 | — | — | Bricolage 600 / 19 · couleur #F07A2E · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 540 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 605 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | RELEVÉ · À TENIR À DEUX |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Chiche · tenu à deux — clair

*Les deux moitiés se rejoignent au milieu : le dessin n'existe que parce que les deux ont tenu.*

Fond `#F4EEE1` · **trait : base = 372, amplitude = 44, boîte SVG = 456**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 456 | — |  |
| bloc | 58 | 88 | — | — | — |  |
| DALLE | interne | interne | 273 | 228 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 460 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 470 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Marion |
| bloc texte | 24 | 584 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Marion |
| bloc texte | 24 | 614 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le grand plongeoir |
| bloc texte | 24 | 718 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENU À DEUX · 3 AOÛT |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Fiches Nuée

### Nuée · avec des Promi — clair

*La zone haute porte <b>les dalles de tous les Promi plantés dans la Nuée</b>, pas une dalle unique. Chaque Promi se lit en réduction de sa carte d'Index : sa dalle, son trait, sa couleur d'état.*

Fond `#F4EEE1` · **trait : base = 232, amplitude = 36, boîte SVG = 308**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 308 | — |  |
| bloc | 30 | 96 | — | — | — |  |
| DALLE | interne | interne | 108 | 86 | — |  |
| bloc | 150 | 88 | — | — | — |  |
| DALLE | interne | interne | 118 | 94 | — |  |
| bloc | 278 | 100 | — | — | — |  |
| DALLE | interne | interne | 92 | 74 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 312 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 322 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 436 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 466 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 531 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 6 PROMI · 1 TENU |
| bloc | 24 | 561 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| DALLE | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| DALLE | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | arroser tous les soirs |
| bloc | 24 | 647 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| DALLE | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| DALLE | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | semer les radis |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Nuée · vide — clair

*Aucun Promi, donc aucune dalle : la zone haute est nue et la Nuée n'attend qu'une chose.*

Fond `#F4EEE1` · **trait : base = 282, amplitude = 44, boîte SVG = 366**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 366 | — |  |
| bloc | 112 | 88 | — | — | — |  |
| DALLE | interne | interne | 165 | 138 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 370 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 380 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | l'atelier |
| bloc texte | 24 | 494 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec toi seulement |
| bloc texte | 24 | 524 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | l'atelier du samedi |
| bloc texte | 24 | 628 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | AUCUN PROMI ENCORE |
| bloc texte | 24 | 672 | — | — | Bricolage 700 / 18.5 · couleur #8A5CF0 · interlettre -.01em | plante le premier Promi de la Nuée ↑ |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Gardé de côté

### Gardé de côté · Promi — clair

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #3A54FF · interlettre -.01em | trace pour planter |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #3A54FF · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | appeler Mamie |
| bloc texte | 24 | 481 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · 2 AVRIL |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Gardé de côté · Chiche — clair

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #FA2258 · interlettre -.01em | trace pour lancer |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #FA2258 · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le grand plongeoir |
| bloc texte | 24 | 520 | — | — | Apfel 500 / 12.5 · couleur #FA2258 · interlettre .20em | GARDÉ DE CÔTÉ · PERSONNE DE DÉFIÉ |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Gardé de côté · Nuée — clair

*Aucun champ plein, le trait est en points sur toute sa longueur. La dalle, elle, est déjà pleine et déjà posée sur la Toile — la matière existe, la parole non.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 350 | — | — | Bricolage 700 / 17 · couleur #8A5CF0 · interlettre -.01em | trace pour lancer |
| bloc texte | 24 | 386 | — | — | Bricolage 600 / 21 · couleur #8A5CF0 · interlettre -.01em | Gardé de côté |
| bloc texte | 24 | 416 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | l'atelier du samedi |
| bloc texte | 24 | 520 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | GARDÉ DE CÔTÉ · PERSONNE D'INVITÉ |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## États de fiche

### Avec commentaires — clair

*Blocs pleins, jamais de rectangle translucide. Le nom prend la couleur d'état.*

Fond `#F4EEE1` · **trait : base = 262, amplitude = 44, boîte SVG = 346**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 346 | — |  |
| bloc | 124 | 88 | — | — | — |  |
| DALLE | interne | interne | 141 | 118 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 350 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 360 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 474 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Rachel |
| bloc texte | 24 | 504 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc | 24 | 566 | 342 | 76 | Bricolage 400 / — · couleur #16171B · fond #E7DFCE · rayon 22 |  |
| · dedans | interne | interne | — | — | couleur #2BE88C | Rachel |
| · dedans | interne | interne | — | — | — | elles étaient parfaites. |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Sans commentaire — clair

*L'invitation est une phrase, pas un champ vide.*

Fond `#F4EEE1` · **trait : base = 338, amplitude = 46, boîte SVG = 424**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 424 | — |  |
| bloc | 80 | 88 | — | — | — |  |
| DALLE | interne | interne | 230 | 192 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 428 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc texte | 24 | 552 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 582 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 654 | 342 | 66 | Bricolage 600 / 18 · couleur #16171B · contour 3px solid #16171B · rayon 33 | personne n'a rien dit — commence |
| · dedans | interne | interne | — | — | — | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## L'instant

### L'autre moitié arrive — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 105 | 91 | — | — | — |  |
| DALLE | interne | interne | 180 | 150 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 388 | 342 | — | Bricolage 700 / 17 · couleur #2BE88C · aligné center | l'autre moitié arrive |
| bloc | 24 | 432 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 442 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 556 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 586 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le trait se referme — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 81 | 88 | — | — | — |  |
| DALLE | interne | interne | 228 | 190 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 388 | 342 | — | Bricolage 700 / 64 · couleur #16171B · interlettre -.04em · interligne 1 | tenue. |
| bloc texte | 24 | 472 | 342 | — | Bricolage 600 / 20 · couleur #16171B · interligne 1.3 | Rachel vient de tracer sa moitié. Le dessin existe. |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Juste après — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 105 | 91 | — | — | — |  |
| DALLE | interne | interne | 180 | 150 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À Rachel |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE À DEUX · À L'INSTANT |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Index et Fil

### Index 2 par ligne — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.035em | Index |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #3A54FF | 12 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #16171B · contour 3px solid #9A9384 · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #16171B · contour 3px solid #9A9384 · rayon 28 | ⇅ |
| bloc | 24 | 196 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 135 | — |  |
| bloc | 36 | 9 | — | — | — |  |
| DALLE | interne | interne | 92 | 77 | — |  |
| bloc texte | 12 | 124 | — | — | Bricolage 600 / 12.4 · couleur #2BE88C | à moi |
| bloc texte | 12 | 141 | 140 | 33 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 201 | 196 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 107 | — |  |
| bloc | 97 | 9 | — | — | — |  |
| DALLE | interne | interne | 58 | 49 | — |  |
| bloc texte | 12 | 97 | — | — | Bricolage 600 / 12.4 · couleur #F07A2E | à Rachel |
| bloc texte | 12 | 114 | 140 | 60 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 24 | 406 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 147 | — |  |
| bloc | 9 | 9 | — | — | — |  |
| DALLE | interne | interne | 106 | 89 | — |  |
| bloc texte | 12 | 136 | — | — | Bricolage 600 / 12.4 · couleur #8A5CF0 | avec +4 |
| bloc texte | 12 | 153 | 140 | 21 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #8A5CF0 · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 201 | 406 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 99 | — |  |
| bloc | 58 | 9 | — | — | — |  |
| DALLE | interne | interne | 49 | 41 | — |  |
| bloc texte | 12 | 89 | — | — | Bricolage 600 / 12.4 · couleur #FA2258 | à Marion |
| bloc texte | 12 | 106 | 140 | 68 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #FA2258 · interlettre .18em | LANCÉ |
| bloc | 24 | 616 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 123 | — |  |
| bloc | 77 | 9 | — | — | — |  |
| DALLE | interne | interne | 78 | 65 | — |  |
| bloc texte | 12 | 113 | — | — | Bricolage 600 / 12.4 · couleur #3A54FF | à moi |
| bloc texte | 12 | 130 | 140 | 44 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #3A54FF · interlettre .18em | EN COURS |
| bloc | 201 | 616 | — | — | — |  |
| · dedans | interne | interne | 165 | 198 | fond #F4EEE1 · rayon 17 |  |
| DALLE | 0 | 0 | 165 | 131 | — |  |
| bloc | 39 | 9 | — | — | — |  |
| DALLE | interne | interne | 87 | 73 | — |  |
| bloc texte | 12 | 120 | — | — | Bricolage 600 / 12.4 · couleur #2BE88C | à Marion |
| bloc texte | 12 | 137 | 140 | 37 | Bricolage 700 / 20.0 · couleur #16171B · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 12 | — | — | — | Apfel 500 / 10.0 · couleur #2BE88C · interlettre .18em | TENU À DEUX |

### Index 3 par ligne — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.035em | Index |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #3A54FF | 12 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #16171B · contour 3px solid #9A9384 · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #16171B · contour 3px solid #9A9384 · rayon 28 | ⇅ |
| bloc | 24 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 97 | — |  |
| bloc | 22 | 6 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 7 | 83 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à moi |
| bloc texte | 7 | 94 | 90 | 24 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 142 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 78 | — |  |
| bloc | 60 | 6 | — | — | — |  |
| DALLE | interne | interne | 39 | 33 | — |  |
| bloc texte | 7 | 64 | — | — | Bricolage 600 / 8.0 · couleur #F07A2E | à Rachel |
| bloc texte | 7 | 75 | 90 | 43 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 260 | 196 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 105 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 72 | 60 | — |  |
| bloc texte | 7 | 91 | — | — | Bricolage 600 / 8.0 · couleur #8A5CF0 | avec +4 |
| bloc texte | 7 | 102 | 90 | 20 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #8A5CF0 · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 24 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 73 | — |  |
| bloc | 36 | 6 | — | — | — |  |
| DALLE | interne | interne | 33 | 28 | — |  |
| bloc texte | 7 | 59 | — | — | Bricolage 600 / 8.0 · couleur #FA2258 | à Marion |
| bloc texte | 7 | 70 | 90 | 48 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #FA2258 · interlettre .18em | LANCÉ |
| bloc | 142 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 89 | — |  |
| bloc | 47 | 6 | — | — | — |  |
| DALLE | interne | interne | 52 | 44 | — |  |
| bloc texte | 7 | 75 | — | — | Bricolage 600 / 8.0 · couleur #3A54FF | à moi |
| bloc texte | 7 | 86 | 90 | 32 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #3A54FF · interlettre .18em | EN COURS |
| bloc | 260 | 341 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 94 | — |  |
| bloc | 24 | 6 | — | — | — |  |
| DALLE | interne | interne | 58 | 49 | — |  |
| bloc texte | 7 | 80 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à Marion |
| bloc texte | 7 | 91 | 90 | 27 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENU À DEUX |
| bloc | 24 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 · outline 2px dashed #8A5CF0 |  |
| DALLE | 0 | 0 | 106 | 86 | — |  |
| bloc | 28 | 6 | — | — | — |  |
| DALLE | interne | interne | 49 | 41 | — |  |
| bloc texte | 7 | 72 | — | — | Bricolage 600 / 8.0 · couleur #8A5CF0 | gardé de côté |
| bloc texte | 7 | 83 | 90 | 35 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | l'atelier du samedi |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #8A5CF0 · interlettre .18em | GARDÉ DE CÔTÉ |
| bloc | 142 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 · outline 2px dashed #3A54FF |  |
| DALLE | 0 | 0 | 106 | 81 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 43 | 36 | — |  |
| bloc texte | 7 | 67 | — | — | Bricolage 600 / 8.0 · couleur #3A54FF | gardé de côté |
| bloc texte | 7 | 78 | 90 | 40 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | appeler Mamie |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #3A54FF · interlettre .18em | GARDÉ DE CÔTÉ |
| bloc | 260 | 486 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 97 | — |  |
| bloc | 22 | 6 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 7 | 83 | — | — | Bricolage 600 / 8.0 · couleur #2BE88C | à moi |
| bloc texte | 7 | 94 | 90 | 24 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #2BE88C · interlettre .18em | TENUE |
| bloc | 24 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 78 | — |  |
| bloc | 60 | 6 | — | — | — |  |
| DALLE | interne | interne | 39 | 33 | — |  |
| bloc texte | 7 | 64 | — | — | Bricolage 600 / 8.0 · couleur #F07A2E | à Rachel |
| bloc texte | 7 | 75 | 90 | 43 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 142 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 105 | — |  |
| bloc | 6 | 6 | — | — | — |  |
| DALLE | interne | interne | 72 | 60 | — |  |
| bloc texte | 7 | 91 | — | — | Bricolage 600 / 8.0 · couleur #8A5CF0 | avec +4 |
| bloc texte | 7 | 102 | 90 | 20 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #8A5CF0 · interlettre .18em | 6 PROMI · 1 TENU |
| bloc | 260 | 631 | — | — | — |  |
| · dedans | interne | interne | 106 | 133 | fond #F4EEE1 · rayon 11 |  |
| DALLE | 0 | 0 | 106 | 73 | — |  |
| bloc | 36 | 6 | — | — | — |  |
| DALLE | interne | interne | 33 | 28 | — |  |
| bloc texte | 7 | 59 | — | — | Bricolage 600 / 8.0 · couleur #FA2258 | à Marion |
| bloc texte | 7 | 70 | 90 | 48 | Bricolage 700 / 12.9 · couleur #16171B · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 7 | — | — | — | Apfel 500 / 6.4 · couleur #FA2258 · interlettre .18em | LANCÉ |

### Fil — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.035em | Fil |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #2BE88C | 4 |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 108 | 270 | 56 | Bricolage 600 / 16 · couleur #16171B · contour 3px solid #9A9384 · rayon 28 · écart 12px | ⌕ Rechercher |
| bloc texte | 310 | 108 | 56 | 56 | couleur #16171B · contour 3px solid #9A9384 · rayon 28 | ⇅ |
| bloc | 16 | 196 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FA2258 | Marion te lance un chiche |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | le grand plongeoir |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #FA2258 · interlettre .18em | À RELEVER |
| bloc | 16 | 336 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | à moi |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | planter un arbre |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | TENUE · IL Y A 2 H |
| bloc | 16 | 476 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #8A5CF0 | Adrien a planté |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | semer les radis |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #8A5CF0 · interlettre .18em | LE POTAGER · 6 PROMI |
| bloc | 16 | 616 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #F07A2E | à Rachel |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | faire les crêpes |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |
| bloc | 16 | 756 | — | — | — |  |
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | Marion a relevé |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | courir dimanche |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | RELEVÉ · À TENIR À DEUX |

---

## Cartes d'Index isolées

### Carte 1 · planter un arbre — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 141 | — |  |
| bloc | 38 | 10 | — | — | — |  |
| DALLE | interne | interne | 97 | 81 | — |  |
| bloc texte | 13 | 131 | — | — | Bricolage 600 / 13.0 · couleur #2BE88C | à moi |
| bloc texte | 13 | 149 | 147 | 33 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | planter un arbre |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENUE |

### Carte 2 · faire les crêpes — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 112 | — |  |
| bloc | 101 | 10 | — | — | — |  |
| DALLE | interne | interne | 62 | 52 | — |  |
| bloc texte | 13 | 102 | — | — | Bricolage 600 / 13.0 · couleur #F07A2E | à Rachel |
| bloc texte | 13 | 120 | 147 | 62 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | faire les crêpes |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |

### Carte 3 · le potager — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 153 | — |  |
| bloc | 10 | 10 | — | — | — |  |
| DALLE | interne | interne | 111 | 93 | — |  |
| bloc texte | 13 | 143 | — | — | Bricolage 600 / 13.0 · couleur #8A5CF0 | avec +4 |
| bloc texte | 13 | 161 | 147 | 21 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | le potager |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #8A5CF0 · interlettre .18em | 6 PROMI · 1 TENU |

### Carte 4 · courir dimanche — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 103 | — |  |
| bloc | 61 | 10 | — | — | — |  |
| DALLE | interne | interne | 51 | 43 | — |  |
| bloc texte | 13 | 93 | — | — | Bricolage 600 / 13.0 · couleur #FA2258 | à Marion |
| bloc texte | 13 | 111 | 147 | 71 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | courir dimanche |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #FA2258 · interlettre .18em | LANCÉ |

### Carte 5 · nager le mardi — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 128 | — |  |
| bloc | 82 | 10 | — | — | — |  |
| DALLE | interne | interne | 81 | 68 | — |  |
| bloc texte | 13 | 118 | — | — | Bricolage 600 / 13.0 · couleur #3A54FF | à moi |
| bloc texte | 13 | 136 | 147 | 46 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | nager le mardi |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #3A54FF · interlettre .18em | EN COURS |

### Carte 6 · le grand plongeoir — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 |  |
| DALLE | 0 | 0 | 173 | 137 | — |  |
| bloc | 40 | 10 | — | — | — |  |
| DALLE | interne | interne | 92 | 77 | — |  |
| bloc texte | 13 | 127 | — | — | Bricolage 600 / 13.0 · couleur #2BE88C | à Marion |
| bloc texte | 13 | 145 | 147 | 37 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | le grand plongeoir |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU À DEUX |

### Carte 7 · l'atelier du samedi — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 · outline 3px dashed #8A5CF0 |  |
| DALLE | 0 | 0 | 173 | 124 | — |  |
| bloc | 48 | 10 | — | — | — |  |
| DALLE | interne | interne | 76 | 64 | — |  |
| bloc texte | 13 | 114 | — | — | Bricolage 600 / 13.0 · couleur #8A5CF0 | gardé de côté |
| bloc texte | 13 | 132 | 147 | 50 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | l'atelier du samedi |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #8A5CF0 · interlettre .18em | GARDÉ DE CÔTÉ |

### Carte 8 · appeler Mamie — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 173 | 208 | fond #F4EEE1 · rayon 18 · outline 3px dashed #3A54FF |  |
| DALLE | 0 | 0 | 173 | 116 | — |  |
| bloc | 10 | 10 | — | — | — |  |
| DALLE | interne | interne | 67 | 56 | — |  |
| bloc texte | 13 | 106 | — | — | Bricolage 600 / 13.0 · couleur #3A54FF | gardé de côté |
| bloc texte | 13 | 124 | 147 | 58 | Bricolage 700 / 21.0 · couleur #16171B · interlettre -.025em · interligne 1 | appeler Mamie |
| bloc texte | 13 | — | — | — | Apfel 500 / 10.5 · couleur #3A54FF · interlettre .18em | GARDÉ DE CÔTÉ |

---

## Bandeaux du Fil isolés

### Bandeau 1 · le grand plongeoir — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FA2258 | Marion te lance un chiche |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | le grand plongeoir |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #FA2258 · interlettre .18em | À RELEVER |

### Bandeau 2 · planter un arbre — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | à moi |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | planter un arbre |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | TENUE · IL Y A 2 H |

### Bandeau 3 · semer les radis — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #8A5CF0 | Adrien a planté |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | semer les radis |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #8A5CF0 · interlettre .18em | LE POTAGER · 6 PROMI |

### Bandeau 4 · faire les crêpes — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #F07A2E | à Rachel |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | faire les crêpes |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #F07A2E · interlettre .18em | À TENIR · 2 J |

### Bandeau 5 · courir dimanche — clair

Fond `#E8E0D0`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| · dedans | interne | interne | 358 | 128 | fond #F4EEE1 · rayon 22 |  |
| DALLE | 0 | 0 | 143 | 128 | — |  |
| bloc | 5 | 19 | — | — | — |  |
| DALLE | interne | interne | 110 | 89 | — |  |
| bloc | 145 | 16 | 197 | 28 | écart 9px |  |
| VISAGE | interne | interne | 26 | 26 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #2BE88C | Marion a relevé |
| bloc texte | 145 | 50 | 197 | 42 | Bricolage 700 / 20 · couleur #16171B · interlettre -.025em · interligne 1.04 | courir dimanche |
| bloc texte | 145 | 98 | 197 | 16 | Apfel 500 / 11 · couleur #2BE88C · interlettre .18em | RELEVÉ · À TENIR À DEUX |

---

## Les Noyaux

### Noyaux · Promi à soi — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 21 · couleur #2BE88C · interlettre -.01em | À moi |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | planter un arbre |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENUE · 12 MARS |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · Promi à Rachel — clair

Fond `#F4EEE1` · **trait : base = 268, amplitude = 44, boîte SVG = 352**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 352 | — |  |
| bloc | 121 | 88 | — | — | — |  |
| DALLE | interne | interne | 148 | 124 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 356 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc | 24 | 392 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #3A54FF · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Rachel |
| bloc texte | 24 | 516 | — | — | Bricolage 600 / 21 · couleur #F07A2E · interlettre -.01em | À Rachel |
| bloc texte | 24 | 546 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | faire les crêpes |
| bloc texte | 24 | 611 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | À TENIR · DIMANCHE |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · Chiche à deux — clair

Fond `#F4EEE1` · **trait : base = 268, amplitude = 44, boîte SVG = 352**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 352 | — |  |
| bloc | 121 | 88 | — | — | — |  |
| DALLE | interne | interne | 148 | 124 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 356 | 342 | — | Bricolage 700 / 17 · couleur #F07A2E · interlettre -.01em · aligné center | trace pour tenir |
| bloc | 24 | 392 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Marion |
| bloc | 220 | 402 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | avec Rachel |
| bloc texte | 24 | 516 | — | — | Bricolage 600 / 19 · couleur #F07A2E · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 546 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 611 | — | — | Apfel 500 / 12.5 · couleur #F07A2E · interlettre .20em | RELEVÉ · À TENIR À DEUX |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · dans une Nuée — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | semer les radis |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | DANS LE POTAGER |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Noyaux · l'anneau du Cercle — clair

Fond `#F4EEE1` · **trait : base = 300, amplitude = 44, boîte SVG = 384**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 384 | — |  |
| bloc | 101 | 88 | — | — | — |  |
| DALLE | interne | interne | 187 | 156 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 388 | 82 | — | aligné center |  |
| NOYAU | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 48 | 48 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | Marion |
| bloc | 220 | 398 | 70 | — | aligné center |  |
| NOYAU | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| VISAGE | interne | interne | 36 | 36 | fond #FA2258 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | avec Rachel |
| bloc texte | 24 | 512 | — | — | Bricolage 600 / 19 · couleur #2BE88C · interlettre -.01em | À Marion · avec Rachel |
| bloc texte | 24 | 542 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | courir dimanche |
| bloc texte | 24 | 607 | — | — | Apfel 500 / 12.5 · couleur #2BE88C · interlettre .20em | TENU À DEUX · 3 AOÛT |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Page +

### Choix des trois natures — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 40 | — | 34 | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 96 | 342 | — | Bricolage 700 / 46 · couleur #16171B · interlettre -.035em · interligne .95 | Qu'est-ce que tu promets ? |
| bloc | 16 | 246 | 358 | 174 | fond #3A54FF · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Un Promi |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | à quelqu'un, ou à toi |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |
| bloc | 16 | 436 | 358 | 174 | fond #FA2258 · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Un Chiche |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | un défi lancé |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |
| bloc | 16 | 626 | 358 | 174 | fond #8A5CF0 · rayon 28 |  |
| bloc | — | 24 | — | — | — |  |
| DALLE | interne | interne | 120 | 96 | — |  |
| bloc texte | 26 | 28 | — | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.03em | Une Nuée |
| bloc texte | 26 | 82 | 190 | — | Bricolage 600 / 17 · couleur #F4EEE1 · interligne 1.25 | un groupe, un projet |
| bloc texte | 26 | — | — | — | Apfel 500 / 11.5 · couleur #F4EEE1 · interlettre .20em | CHOISIR → |

### Promi · phrase vide — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · contour 3px dashed #3A54FF · rayon 16 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 574 | 342 | — | Bricolage 600 / 17.5 · couleur #3A54FF · interligne 1.4 | touche ⇄ pour changer d'intention · touche un mot pour l'écrire  |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · à soi rempli — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · à Rachel — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 453 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #3A54FF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | faire les crêpes |
| bloc | 24 | 514 | 342 | 61 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #3A54FF · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 31 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em · interligne 1.1 · écart 7px | Rachel |
| VISAGE | interne | interne | 23 | 23 | fond #3A54FF · rayon 999 |  |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · promets-moi — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em · interligne 1.1 · écart 8px | Rachel, |
| VISAGE | interne | interne | 27 | 27 | fond #3A54FF · rayon 999 |  |
| bloc | 24 | 459 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | promets-moi |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 526 | 342 | 67 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #3A54FF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 36 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | m'appeler |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Promi · promettez-moi — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 392 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em · interligne 1.1 · écart 8px | Rachel, Nico, |
| VISAGE | interne | interne | 26 | 26 | fond #3A54FF · rayon 999 |  |
| bloc | 24 | 458 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | promettez-moi |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 524 | 342 | 66 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #3A54FF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 35 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | venir dimanche |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Chiche · vide — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · contour 3px dashed #FA2258 · rayon 16 · interlettre -.03em | qui ? |
| bloc | 24 | 455 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #FA2258 · rayon 18 · interlettre -.03em | Chiche |
| bloc | 24 | 518 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · contour 3px dashed #FA2258 · rayon 16 · interlettre -.03em | courir dimanche |
| bloc texte | 24 | 615 | 342 | — | Bricolage 600 / 17.5 · couleur #FA2258 · interligne 1.4 | le compagnon et l'échéance sont dans Peaufiner |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Chiche · rempli — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Chiche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em · interligne 1.1 · écart 7px | Marion, |
| VISAGE | interne | interne | 25 | 25 | fond #FA2258 · rayon 999 |  |
| bloc | 24 | 455 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #FA2258 · rayon 18 · interlettre -.03em | chiche |
| bloc | 24 | 518 | 342 | 63 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #FA2258 · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 33 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | courir dimanche |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #FA2258 · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Nuée · écriture — clair

Fond `#F4EEE1` · **trait : base = 280, amplitude = 46, boîte SVG = 386**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 386 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 326 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour lancer |
| bloc | 24 | 392 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #8A5CF0 · rayon 18 · interlettre -.03em | Je lance une Nuée |
| bloc | 24 | 450 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #8A5CF0 · interlettre -.03em | nommée |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | Lisbonne |
| bloc | 24 | 508 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #8A5CF0 · interlettre -.03em | avec |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | Rachel · Adrien |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #8A5CF0 · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Choix ouvert · écrire un mot — clair

Fond `#F4EEE1` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 57 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 337 | 342 | 57 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 28 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer\| |
| bloc texte | 24 | 420 | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .20em | DÉJÀ PROMIS |
| bloc texte | 24 | 446 | — | 50 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 25 | nager le mardi |
| bloc texte | 201 | 446 | — | 50 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 25 | appeler Mamie |
| bloc texte | 17 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | a |
| bloc texte | 53 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | z |
| bloc texte | 89 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | e |
| bloc texte | 125 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | r |
| bloc texte | 161 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | t |
| bloc texte | 197 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | y |
| bloc texte | 233 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | u |
| bloc texte | 269 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | i |
| bloc texte | 305 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | o |
| bloc texte | 341 | 640 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | p |
| bloc texte | 17 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | q |
| bloc texte | 53 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | s |
| bloc texte | 89 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | d |
| bloc texte | 125 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | f |
| bloc texte | 161 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | g |
| bloc texte | 197 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | h |
| bloc texte | 233 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | j |
| bloc texte | 269 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | k |
| bloc texte | 305 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | l |
| bloc texte | 341 | 702 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | m |
| bloc texte | 89 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | w |
| bloc texte | 125 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | x |
| bloc texte | 161 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | c |
| bloc texte | 197 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | v |
| bloc texte | 233 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | b |
| bloc texte | 269 | 764 | 32 | 50 | Bricolage 600 / 17 · couleur #16171B · fond #DCD4C2 · rayon 9 | n |

### Choix ouvert · choisir une personne — clair

Fond `#F4EEE1` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je promets |
| bloc | 24 | 340 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #3A54FF · interlettre -.03em | de |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | faire les crêpes |
| bloc | 24 | 400 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #3A54FF · interlettre -.03em | à |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #3A54FF · contour 3px dashed #3A54FF · rayon 16 · interlettre -.03em | qui ? |
| bloc texte | 24 | 486 | 162 | 52 | Bricolage 700 / 16 · couleur #F4EEE1 · fond #3A54FF · contour 3px solid #3A54FF · rayon 26 · écart 10px | Rachel |
| · dedans | interne | interne | 28 | 28 | couleur #3A54FF · fond #F4EEE1 · rayon 999 | R |
| bloc texte | 198 | 486 | 162 | 52 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 26 · écart 10px | Nico |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | N |
| bloc texte | 24 | 546 | 162 | 52 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 26 · écart 10px | Marion |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | M |
| bloc texte | 198 | 546 | 162 | 52 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 26 · écart 10px | Léo |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | L |
| bloc texte | 24 | 606 | 162 | 52 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 26 · écart 10px | Adrien |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | A |
| bloc texte | 198 | 606 | 162 | 52 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 26 · écart 10px | Camille |
| · dedans | interne | interne | 28 | 28 | couleur #F4EEE1 · fond #3A54FF · rayon 999 | C |
| bloc texte | 24 | 680 | 342 | 52 | Bricolage 700 / 16 · couleur #3A54FF · contour 3px dashed #3A54FF · rayon 26 | + ajouter quelqu'un |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Choix ouvert · l'échéance — clair

Fond `#F4EEE1` · **trait : base = 196, amplitude = 22, boîte SVG = 278**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 278 | — |  |
| bloc | 149 | 92 | — | — | — |  |
| DALLE | interne | interne | 91 | 75 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 236 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour planter |
| bloc | 24 | 280 | 342 | 60 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #3A54FF · interlettre -.03em | avant |
| · dedans | interne | interne | — | — | Bricolage 700 / 30 · couleur #3A54FF · contour 3px dashed #3A54FF · rayon 16 · interlettre -.03em | quand ? |
| bloc texte | 24 | 366 | — | 50 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 25 | ce soir |
| bloc texte | 131 | 366 | — | 50 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 25 | demain |
| bloc texte | 230 | 366 | — | 50 | Bricolage 700 / 16 · couleur #16171B · contour 3px solid #16171B · rayon 25 | dimanche |
| bloc | 24 | 428 | 342 | — | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 24 · couleur #16171B · interlettre -.02em | mai |
| · dedans | interne | interne | — | — | Bricolage 700 / 19 · couleur #3A54FF | 2026 › |
| bloc texte | 24 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | L |
| bloc texte | 73 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | M |
| bloc texte | 122 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | M |
| bloc texte | 171 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | J |
| bloc texte | 220 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | V |
| bloc texte | 269 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | S |
| bloc texte | 318 | 466 | 42 | — | Apfel 500 / 11 · couleur #3A54FF · interlettre .14em · aligné center | D |
| bloc texte | 221 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 1 |
| bloc texte | 270 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 2 |
| bloc texte | 319 | 488 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 3 |
| bloc texte | 25 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 4 |
| bloc texte | 74 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 5 |
| bloc texte | 123 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 6 |
| bloc texte | 172 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 7 |
| bloc texte | 221 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 8 |
| bloc texte | 270 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 9 |
| bloc texte | 319 | 524 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 10 |
| bloc texte | 25 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 11 |
| bloc texte | 74 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #F4EEE1 · fond #3A54FF · rayon 17 | 12 |
| bloc texte | 123 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 13 |
| bloc texte | 172 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 14 |
| bloc texte | 221 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 15 |
| bloc texte | 270 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 16 |
| bloc texte | 319 | 560 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 17 |
| bloc texte | 25 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 18 |
| bloc texte | 74 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 19 |
| bloc texte | 123 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 20 |
| bloc texte | 172 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 21 |
| bloc texte | 221 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 22 |
| bloc texte | 270 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 23 |
| bloc texte | 319 | 596 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 24 |
| bloc texte | 25 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 25 |
| bloc texte | 74 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 26 |
| bloc texte | 123 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 27 |
| bloc texte | 172 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 28 |
| bloc texte | 221 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 29 |
| bloc texte | 270 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 30 |
| bloc texte | 319 | 632 | 34 | 34 | Bricolage 700 / 16 · couleur #16171B · rayon 17 | 31 |
| bloc texte | 24 | 680 | 162 | 56 | Bricolage 700 / 17 · couleur #3A54FF · contour 3px solid #3A54FF · rayon 28 | un jour |
| bloc texte | 198 | 680 | 162 | 56 | Bricolage 700 / 17 · couleur #3A54FF · contour 3px solid #3A54FF · rayon 28 | en l'air |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Garder de côté — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Gardé de côté · après — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace pour planter |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 558 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · RIEN N'EST PROMIS |
| bloc texte | 24 | 708 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | garder de côté |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |

### Le geste · au repos — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 82 | 358 | — | — | Bricolage 700 / 18.5 · couleur #16171B · interlettre -.01em | trace ta moitié |
| bloc | 24 | 424 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| · dedans | interne | interne | — | — | — | ⇄ |
| bloc | 24 | 482 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc texte | 24 | 702 | — | — | Bricolage 600 / 16 · couleur #3A54FF · underline | planter au bouton |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le geste · pendant — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 160 | 372 | — | — | Bricolage 700 / 18.5 · couleur #F07A2E · interlettre -.01em | continue → |
| bloc | 24 | 454 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 512 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le geste · signé — clair

Fond `#F4EEE1` · **trait : base = 312, amplitude = 46, boîte SVG = 418**

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 418 | — |  |
| bloc | 73 | 88 | — | — | — |  |
| DALLE | interne | interne | 244 | 200 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 · interlettre -.01em | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em · écart 9px | FERMER |
| · dedans | interne | interne | — | — | — | ✕ |
| bloc texte | 180 | 372 | — | — | Bricolage 700 / 18.5 · couleur #F07A2E · interlettre -.01em | planté · à tenir avant l'été |
| bloc | 24 | 454 | 342 | 58 | écart 11px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #3A54FF · rayon 18 · interlettre -.03em | Je me promets |
| bloc | 24 | 512 | 342 | 58 | écart 3px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #3A54FF · interlettre -.03em | d' |
| · dedans | interne | interne | — | — | Bricolage 700 / 29 · couleur #F4EEE1 · fond #16171B · rayon 18 · interlettre -.03em | aller voir la mer |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

---

## Peaufiner

### Peaufiner Promi · haut — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.03em | aller voir la mer |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | À QUI |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | Rachel |
| bloc | 24 | 190 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | dimanche |
| bloc | 24 | 270 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | DANS UNE NUÉE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | le potager |
| bloc | 24 | 350 | 342 | 118 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | NOTE |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #3A54FF · interligne 1.25 | ajoute un mot, un contexte… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #3A54FF | visible par Rachel |
| bloc | 24 | 484 | 342 | 92 | contour 3px solid #16171B · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | 2 fichiers |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #3A54FF | visibles par Rachel |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Promi · suite — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 46 | 342 | 118 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #3A54FF · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #3A54FF | visible par Rachel · vous pouvez répondre |
| bloc | 24 | 180 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RELANCER RACHEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | → |
| bloc | 24 | 260 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | · ·· ··· |
| bloc | 24 | 340 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | chaque semaine |
| bloc | 24 | 420 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | la veille à 19:00 |
| bloc | 24 | 500 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | réveille tes « en l'air » |
| bloc | 24 | 368 | 342 | 90 | fond #16171B · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #CBAAFF · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #CBAAFF | importance, récurrence, rappels, mémoire |
| bloc | 24 | 668 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | SUPPRIMER CE PROMI |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | → |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Le bloc du Cercle — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 70 | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.02em | Le Cercle |
| bloc | 24 | 130 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | · ·· ··· |
| bloc | 24 | 210 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | chaque semaine |
| bloc | 24 | 290 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | la veille à 19:00 |
| bloc | 24 | 370 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | réveille tes « en l'air » |
| bloc | 24 | 238 | 342 | 90 | fond #16171B · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #CBAAFF · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #CBAAFF | importance, récurrence, rappels, mémoire |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Nuée · haut — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.03em | le potager |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 104 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #8A5CF0 · interlettre .18em | DESCRIPTION |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #8A5CF0 · interligne 1.25 | présente la Nuée, son but… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #8A5CF0 | visible par tous les membres |
| bloc | 24 | 230 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #8A5CF0 · interlettre .18em | MEMBRES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | Rachel · Adrien · +3 |
| bloc | 24 | 310 | 342 | 92 | contour 3px solid #16171B · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #8A5CF0 · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | 2 fichiers |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #8A5CF0 | visibles par la Nuée |
| bloc | 24 | 418 | 342 | 104 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #8A5CF0 · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #8A5CF0 · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #8A5CF0 | visibles par les membres de la Nuée |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Nuée · bas — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc texte | 24 | 46 | 342 | 62 | Bricolage 700 / 19 · couleur #F4EEE1 · fond #8A5CF0 · contour 3px solid #8A5CF0 · rayon 31 | Planter un Promi dans la Nuée |
| bloc | 24 | 124 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #8A5CF0 · interlettre .18em | DISSOUDRE LA NUÉE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | → |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Chiche · haut — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 36 | — | 40 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.03em | courir dimanche |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 110 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | À QUI JE LANCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | Marion |
| bloc | 24 | 190 | 342 | 64 | contour 3px dashed #FA2258 · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | AVEC |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #FA2258 | personne |
| bloc | 24 | 270 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | l'été |
| bloc | 24 | 350 | 342 | 118 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | NOTE |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #FA2258 · interligne 1.25 | ajoute un mot, un contexte… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #FA2258 | visible par Marion |
| bloc | 24 | 484 | 342 | 92 | contour 3px solid #16171B · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | PIÈCES JOINTES |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | 1 fichier |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #FA2258 | visibles par Marion |
| bloc | 24 | 592 | 342 | 104 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | COMMENTAIRES |
| · dedans | interne | interne | — | — | Bricolage 600 / 18 · couleur #FA2258 · interligne 1.25 | écris un mot… |
| bloc texte | 22 | — | — | — | Bricolage 600 / 14 · couleur #FA2258 | visibles par Marion · vous pouvez répondre |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Peaufiner Chiche · bas — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 46 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | RELANCER MARION |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | → |
| bloc | 24 | 126 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | · ·· ··· |
| bloc | 24 | 206 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | chaque semaine |
| bloc | 24 | 286 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | la veille à 19:00 |
| bloc | 24 | 366 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | réveille tes « en l'air » |
| bloc | 24 | 234 | 342 | 90 | fond #16171B · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #FFC0A8 · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #FFC0A8 | importance, récurrence, rappels, mémoire |
| bloc | 24 | 534 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #FA2258 · interlettre .18em | SUPPRIMER CE CHICHE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | → |
| bloc | 0 | 760 | 390 | 84 | fond #FA2258 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▴ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Fiche gardée de côté — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TRAIT | 0 | 0 | 390 | 350 | — |  |
| bloc | 93 | 88 | — | — | — |  |
| DALLE | interne | interne | 204 | 168 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Promi |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 336 | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.02em | planter un arbre |
| bloc texte | 24 | 396 | — | — | Apfel 500 / 12.5 · couleur #3A54FF · interlettre .20em | GARDÉ DE CÔTÉ · RIEN N'EST PROMIS |
| bloc texte | 24 | 430 | 342 | 62 | Bricolage 700 / 19 · couleur #F4EEE1 · fond #3A54FF · contour 3px solid #3A54FF · rayon 31 | Planter |
| bloc | 24 | 508 | 342 | 64 | contour 3px dashed #3A54FF · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | AVANT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #3A54FF | pas encore |
| bloc texte | 24 | 588 | 342 | 62 | Bricolage 700 / 19 · couleur #16171B · contour 3px solid #16171B · rayon 31 | Reprendre l'écriture |
| bloc | 0 | 760 | 390 | 84 | fond #3A54FF |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 · interlettre -.01em | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| VISAGE | interne | interne | 22 | 22 | — |  |

### Réglages généraux — clair

Fond `#F4EEE1`

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| bloc | 24 | 40 | — | 44 | — |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.035em | Réglages |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 112 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | NOTIFICATIONS |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | activées |
| bloc | 24 | 190 | 342 | 92 | contour 3px solid #16171B · rayon 22 · écart 7px |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | ASSISTANCE DU TRAIT |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | moyenne |
| · dedans | interne | interne | — | — | Bricolage 600 / 14 · couleur #3A54FF | lisse le tremblement sans redresser ton geste |
| bloc | 24 | 296 | 342 | 64 | contour 3px solid #16171B · rayon 22 |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | THÈME |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | automatique |
| bloc | 24 | 374 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | C'EST IMPORTANT ? |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | · ·· ··· |
| bloc | 24 | 454 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RÉCURRENCE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | chaque semaine |
| bloc | 24 | 534 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | RAPPEL |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | la veille à 19:00 |
| bloc | 24 | 614 | 342 | 64 | contour 3px solid #16171B · rayon 22 · **blur(2.4px)** |  |
| · dedans | interne | interne | — | — | Apfel 500 / 11.5 · couleur #3A54FF · interlettre .18em | LA MÉMOIRE |
| · dedans | interne | interne | — | — | Bricolage 700 / 18 · couleur #16171B | réveille tes « en l'air » |
| bloc | 24 | 482 | 342 | 90 | fond #16171B · rayon 26 · écart 5px |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 22 · couleur #CBAAFF · interlettre -.02em | ✦ Le Cercle |
| · dedans | interne | interne | — | — | Bricolage 600 / 15 · couleur #CBAAFF | importance, récurrence, rappels, mémoire |

---

## 6 · Les règles que la géométrie ne dit pas

**La loi.** Le champ dit la nature, la ligne dit l'état, la hauteur du trait dit la
composition. Les points disent qu'il manque quelque chose — une moitié de trait, un mot,
un engagement pas encore donné.

**Le geste.** On trace, on ne valide pas : aucun bouton ne double le trait, nulle part.
Planter, c'est tracer sa première moitié. Tenir, c'est tracer la seconde. Une parole
tenue ne se défait pas. Le tracé est **légèrement assisté** — le tremblement est lissé,
le geste n'est pas redressé — avec trois niveaux réglables ; une assistance trop forte
rendrait toutes les signatures identiques.

**L'instant.** Quand la seconde moitié se referme, **le champ entier prend la couleur
d'état pendant une seconde**, la dalle se recompose plus grande, et le mot tombe. C'est le
seul moment du produit où la couleur d'état occupe toute la place.

**Peaufiner.** Sa barre est fixée en bas et ne bouge jamais : on descend au doigt ou on la
touche, les réglages défilent au-dessus d'elle. Rien ne monte, rien ne recouvre.

**La visibilité.** Tout ce qu'on ajoute à une promesse est vu par ceux qu'elle engage —
note, pièces jointes, commentaires, même règle, aucune exception.

**Les doublons interdits.** « À qui » et « Avant » sont les mêmes contrôles que la
phrase, jamais des champs parallèles. `Relancer` et `Partager` n'existent que sur la
fiche, jamais sur la page +. `Relancer` n'existe pas sur une Nuée.

**Les quatre formes du Promi**, que le ⇄ fait tourner : *Je me promets*, *Je promets … à
X*, *X, promets-moi*, *X, Y, promettez-moi*. Un Chiche a un destinataire, qui peut être
soi. Une Nuée porte son nom et ses membres.

**Le Cercle** offre quatre choses : importance, récurrence, rappels, mémoire.

**La longueur des mots.** 18 caractères en confort, 40 en limite dure, au-delà c'est la
note.

**Interdits absolus.** Aucun dégradé, aucun filet, aucune transparence molle, aucune
ombre portée, aucun ton sur ton. Le flou n'existe qu'au Cercle, à 2,4 px. Aucune
superposition, sauf l'encart du Cercle sur ses réglages floutés.

**Lexique.** Les mots « tâche », « objectif », « valider », « compléter », « brouillon »,
« urgent » n'existent pas. On dit : promettre, tenir, tracer, planter, lancer, garder de
côté, reprendre.

---

## 7 · Vérification — le produit

Après portage, ces six contrôles doivent passer sur chaque écran, dans les deux thèmes :

1. aucun chevauchement de blocs — sauf l'encart du Cercle sur ses réglages
2. aucun élément au-delà de y = 844
3. aucun élément à moins de 26 px de la barre Peaufiner — la consigne de dessin étant 30
4. un trait présent sur tout écran de promesse
5. la dalle centrée à 3 px près, sauf la mosaïque d'une Nuée
6. quatre graisses seulement : Bricolage 600/700, Apfel 400/500, plus Fraunces 600


---

# Partie II — la fiche de Nuée

**Statut : proposition.** Cette partie décrit la fiche de Nuée telle qu'elle est dessinée
dans `promi-nuee-toile.html`. Elle n'est pas encore intégrée au moodboard. Chaque écart à
une règle de la partie I y est signalé explicitement.

## 8 · Ce qu'une Nuée contient

Une Nuée porte **des Promi et des Chiche, indifféremment**. Ce sont les mêmes engagements
que partout ailleurs, rangés ensemble : un Promi qu'on se fait à soi, un Promi fait à
quelqu'un, un Chiche lancé à un membre, un Chiche relevé. Chacun garde sa nature, sa
couleur d'état et sa dalle.

Trois conséquences pour l'implémentation :

- **Depuis une Nuée, on plante l'un ou l'autre.** La page + s'ouvre avec **la Nuée déjà
  sélectionnée** : la phrase commence, la Nuée est acquise, aucun écran ne redemande de
  choisir. Le choix qui reste est celui de la nature — se promettre, promettre à
  quelqu'un, lancer un Chiche — exactement comme ailleurs.
- **Le fil ne trie pas.** Promi et Chiche se suivent dans l'ordre de plantation.
- **La Toile ne distingue pas.** Rien ne différencie une dalle de Chiche d'une dalle de
  Promi : elle ne connaît que des paroles données.

## 9 · La hauteur du trait — règle propre à la fiche de Nuée

Une fiche de promesse compte ses éléments en **lignes de phrase**, à 32 px :
`base = max(196, 344 − 32 (n − 1))`.

Une fiche de Nuée les compte en **lignes de fil**, à 86 px — 74 de hauteur plus 12
d'écart. D'où un pas différent, pour la même idée :

```
base = max(176, 460 − 86 n)        n = nombre de Promi et de Chiche
```

- **n = 0 → base 460.** Le trait est au plus bas de tout le produit : rien n'est
  posé sous lui, la Toile occupe 435 px.
- **Chaque Promi ou Chiche le fait monter de 86 px** — exactement la hauteur de la ligne
  qu'il ajoute. `base` diminue quand le trait monte.
- **Plancher 176.** Au-delà de trois éléments il ne monte plus, le défilement
  prend le relais. C'est **20 px plus haut que le plancher d'une fiche de promesse**, qui
  est 196 : écart assumé, pour que trois lignes du fil tiennent entières.

| n | base | lignes affichées | dernière ligne entière |
|---|---|---|---|
| 0 | 460 | 0 | s'arrête à 12 px de la barre |
| 1 | 374 | 1 | s'arrête à 12 px de la barre |
| 2 | 288 | 2 | s'arrête à 12 px de la barre |
| 3 | 202 | 3 | s'arrête à 12 px de la barre |
| 4 | 176 | 4 | s'arrête à 38 px de la barre |
| 7 | 176 | 4 | s'arrête à 38 px de la barre |
| 12 | 176 | 4 | s'arrête à 38 px de la barre |
| 30 | 176 | 4 | s'arrête à 38 px de la barre |
| 100 | 176 | 4 | s'arrête à 38 px de la barre |

**Deux états, et deux seulement.**

| État | base | quand |
|---|---|---|
| **posé** | `max(176, 460 − 86 n)` | la fiche telle qu'elle s'ouvre |
| **défilé** | **58**, amplitude **16** | dès que le doigt a fait remonter le fil |

> **⚠ CORRECTION DU DOCUMENT — 19 août 2026 (validée par Tom).** Les deux écrans « Le fil,
> après défilement » du §12 annonçaient en entête `base = 58, **amplitude = 40**`. C'était
> **faux** : leur propre tableau donne la Toile à **114 px**, et `58 + 16 + 40 = 114` quand
> `58 + 40 + 40` ferait 138. L'entête reportait le gabarit des autres écrans. **Les deux
> entêtes sont corrigées à 16**, en accord avec ce paragraphe et avec les tableaux.
> Voir `QUESTIONS.md` · Q64.

L'état **défilé** n'est pas une valeur de la formule : c'est **la butée haute du
défilement**. Le champ s'y réduit à une bande de 114 px, juste assez pour que la Toile
reste présente sans occuper l'écran. Un contrôle qui vérifie la formule doit donc exclure
cet état, sinon il le comptera comme une erreur. La Toile qu'on y voit est **la même**,
simplement remontée de `base_posé − 58` : jamais une seconde composition.

**Règle de mise en page qui en découle**, et qui doit être respectée au pixel :

- **1, 2 ou 3 éléments** : toutes les lignes sont entièrement visibles, et la dernière
  s'arrête à **12 px de la barre** — exactement l'écart qu'il y a entre deux lignes.
- **4 et plus** : trois lignes entières, et la **quatrième dépasse de 26 px sous la
  barre**. C'est ce dépassement qui dit qu'il y en a d'autres.
- Le pas entre deux lignes est **toujours 12 px**, sans exception.

## 10 · L'encart : le moteur de la Toile

Repris de `promi-v592.html`. **Une dalle n'est ni une tache ni un polygone : c'est une
graine** — une position, un poids, une couleur. Le monde choisi au Studio ne colorie pas
la dalle, il **rastérise l'ensemble des graines**.

### 10.1 Les graines

```python
W_FIN = 3.4                     # le poids de croisière d'une dalle
SP0   = 96.0                    # l'espacement de croisière, constant

# la métrique du moteur : distance euclidienne MOINS le poids de la graine
def proche(x, y, S):
    return min(S, key=lambda s: hypot(x - s.x, y - s.y) - s.w)
```

Les positions sont **relaxées façon Lloyd** — quatre passes : on calcule le diagramme de
Voronoï, chaque graine se replace au centre de sa cellule. La cellule n'est **jamais
dessinée** : elle ne sert qu'à répartir.

### 10.2 Le zoom — la densité ne change jamais

C'est `toileScale()` du prototype. L'espacement reste 96 px dans le repère de la Toile ;
c'est **la vue** qui s'éloigne :

```python
k   = sqrt(n * SP0**2 / (largeur * hauteur))    # facteur de la boîte virtuelle
svg = f'<g transform="scale({1/k})">…</g>'      # on rend puis on met à l'échelle
```

| n | zoom | taille d'une dalle | lisibilité |
|---|---|---|---|
| 1 | ×3,4 | tout l'encart | — |
| 7 | ×1,3 | ~130 px | tous les mondes se lisent |
| 12 | ×1,0 | ~96 px | tous les mondes se lisent |
| 30 | ×0,62 | ~60 px | les trames restent lisibles |
| 100 | ×0,34 | ~33 px | Encre, Mosaïque, Terrazzo tiennent ; Pixel et Braille deviennent une texture |

**Il n'y a pas de plafond de dessin.** Le nombre de Promi et de Chiche d'une Nuée n'est pas
limité. Si une borne technique s'impose au rendu, elle est haute et elle se dit :
**cent dalles affichées, trois cents au Cercle**, les plus récentes, le compte exact
restant dans la méta. C'est une décision de produit, pas de dessin.

### 10.3 Les couleurs

Par dalle, jamais globale. `cc()` du prototype choisit un index **que les voisines n'ont
pas** ; ici on le durcit : **une dalle ne reprend jamais une couleur déjà posée** tant
qu'il en reste de libres. Comme chaque dalle tire aussi sa palette, deux dalles jumelles
deviennent improbables.

Les cinq palettes de `promi-v592.html` — **et la jauge du Studio en donne bien plus** ;
ce qui compte est que l'encart soit **toujours synchronisé au design et aux couleurs
choisis au Studio**, et qu'il suive quand ils changent :

| Palette | Couleurs |
|---|---|
| Nuit Cobalt (`cobalt`) | `#2c3690` · `#3b3094` · `#2734a8` · `#262076` · `#332d86` · `#3d33a0` · `#27379c` |
| Terre Promi (`terre`) | `#D98A4A` · `#C8682E` · `#E0A23C` · `#b5762f` · `#A85C32` · `#caa07a` · `#d49a5e` |
| Aurore Fraise (`aurore`) | `#E59CA6` · `#F0C9A0` · `#A9C5A0` · `#C9B8E0` · `#9FC0D8` · `#E6B8C2` · `#D8B0A0` |
| Jardin Promi (`jardin`) | `#8fc83e` · `#4fc0b0` · `#dccb46` · `#a85fb0` · `#4f9ad8` · `#7bcb56` · `#c9d050` |
| Craie Marine (`craie`) | `#23407a` · `#3f6fa0` · `#88a8c8` · `#cfdae6` · `#5a86b0` · `#b1c3d6` · `#2c5286` |

### 10.4 Les huit moteurs de rendu

`RD = {pixel, braille, sillons, gravure, mosaique, encre, terrazzo, touffe}`.
Éclats n'existe pas. Constantes exactes du prototype :

| Monde | Rendu |
|---|---|
| **Pixel** | grille de 5 px ; chaque case prend la couleur de la graine la plus proche |
| **Braille** | trame de points tous les 9 px, rayon 2,9 — et 2 quand `bd2 − bd < 5`, c'est-à-dire près d'une frontière |
| **Mosaïque** | tesselles de 11 px avec 2 px de joint |
| **Sillons** | lignes tous les 6 px, échantillonnées tous les 6, épaisseur 2,6 ; ondulation `4.5·sin(x·0.018 + l·0.55) + 2.79·sin(x·0.0432 − l·0.42 + 1.2)` ; la couleur change en cours de ligne selon la graine survolée |
| **Gravure** | hachures espacées de 7, échantillonnées tous les 5, épaisseur 3, un angle par dalle, coupées net à la frontière |
| **Encre** | **neuf ellipses** par graine, opacité 0,9, dans un rayon de `0.52 × sp` |
| **Terrazzo** | sept éclats polygonaux de 4 à 6 côtés dans un rayon de `0.46 × sp` |
| **Touffe** | 3 à 5 fleurs par graine, pétales en ellipses, cœur terracotta `#F07A2E` |

Le semis interne utilise **le générateur du prototype**, à reproduire tel quel :

```python
sd = ((k + 1) * 2654435761) & 0xFFFFFFFF
def rnd():
    global sd
    sd = (sd * 1103515245 + 12345) & 0x7FFFFFFF
    return sd / 0x7FFFFFFF
```

### 10.5 Le mélange — chaque dalle garde son monde

**Règle produit :** une dalle garde le monde et la palette **du jour où elle a été
plantée**. Changer de monde au Studio ne repeint pas les dalles déjà posées.

C'est un écart au prototype, où `theme` est global. L'écart est assumé, mais il impose
**une contrainte de rendu absolue** :

> Chaque dalle est peinte **seule, autour de sa graine**, sur un rayon de `0.62 × sp`.
> La trame s'arrête d'elle-même — tuile par tuile, point par point, ligne par ligne.
> **Aucune cellule n'est dessinée, aucune frontière n'est tracée, aucun cadre polygonal
> n'existe.** Les mondes se rencontrent en s'effilochant, jamais en se coupant.

Sans cette règle, deux trames voisines se touchent par une arête droite — c'est le défaut
qu'il faut absolument éviter.

En dessous de cinq dalles, le tirage se restreint aux **mondes en masse** — Encre,
Mosaïque, Terrazzo, Braille, Pixel : Sillons et Gravure sont linéaires et, à deux ou trois
dalles, on ne les distingue plus de leur voisine.

### 10.6 L'état vide

Aucune forme inventée. La Toile sans promesse est semée de **graines grises** —
`seedGray()` du prototype — rendues par le moteur du monde, dans ses tons neutres. **Douze graines : c'est une densité de semis, pas un plafond.** Le nombre est choisi pour que le champ soit occupé sans être chargé ; il ne préjuge de rien, et surtout pas du nombre de Promi que la Nuée accueillera. Sur le champ mauve d'une Nuée on emploie les **tons crème** (`GLIGHT`), dans les
deux thèmes : les gris sombres du prototype y feraient des trous noirs.

```
GLIGHT = #FAF3E5 · #FFFAEF · #F4EBDB · #FCF6EA · #F7EFE0
```

**Conséquence sur le mot-marque :** la Toile vide étant crème dans les deux thèmes, le mot
« Nuée » et « ✕ FERMER » passent à **l'encre `#16171B`** — sinon c'est blanc sur blanc.
Dès qu'un Promi est planté, le champ redevient mauve et ils repassent en crème `#F4EEE1`.

### 10.7 Le masque et l'ordre de peinture

L'ordre est **imposé** :

1. l'aplat du champ, tracé par le chemin de l'onde ;
2. **la Toile**, découpée par ce même chemin ;
3. **le trait** — plein, chevron, points, tout ce qui n'est pas l'aplat.

Les dalles passent donc **sous le trait**, pointillés compris. Le masque est le **champ
lui-même**, jamais un rectangle : la Toile passe sous le bandeau en haut et se termine sur
la vague en bas, jamais sur une ligne droite. Les graines sont semées jusqu'à
`base − 0.62 × amplitude`, pour qu'aucune bande vide ne subsiste au-dessus du trait.

## 11 · Le code de référence — la Toile

Extrait tel quel du générateur.

### Le rendu complet : graines, zoom, mélange

```python
def toile(w, h, n, monde="encre", mood="cobalt", seed=0, x0=0, y0=0, fond=None,
          contour=False, clair=False, melange=False):
    """Rend n dalles dans la boîte (x0, y0, w, h).

       La densité est constante — c'est la VUE qui zoome, comme toileScale() dans le
       prototype : peu de dalles, on est près et elles sont grandes ; beaucoup de dalles,
       on s'éloigne. Sans ça, une seule dalle s'étale et trois se chevauchent pour rien."""
    n = max(1, n)
    k = math.sqrt(n * SP0 * SP0 / (w * h))      # facteur de la boîte virtuelle
    vw, vh = w * k, h * k
    bb = (0, 0, vw, vh)
    pts = graines(n, bb, seed)
    sp = math.sqrt(vw * vh / n)                 # = SP0, par construction
    import random as _r
    tir = _r.Random(seed * 7 + 3)
    # Sillons et Gravure sont linéaires : à deux ou trois dalles on ne les distingue
    # pas de leur voisine. En dessous de cinq dalles on tire parmi les mondes en masse.
    LISIBLES = ["encre", "mosaique", "terrazzo", "braille", "pixel"]
    mondes_dispo = LISIBLES if n <= 4 else [m for m in RD if m != "touffe"]
    pal = MOODS[mood]
    S = []
    for i, p in enumerate(pts):
        if melange:
            monde_i = mondes_dispo[tir.randrange(len(mondes_dispo))]
            mood_i = list(MOODS)[tir.randrange(len(MOODS))]
            pal = MOODS[mood_i]
        # cc() du prototype : on prend un index que les voisines n'ont pas déjà
        # cc() du prototype, durci : une dalle ne reprend jamais une couleur déjà posée
        # tant qu'il en reste de libres. Deux dalles jumelles deviennent impossibles.
        deja = {q["c"] for q in S}
        libres = [k for k in range(len(pal)) if pal[k] not in deja]
        if not libres:
            voisins = sorted(S, key=lambda q: (q["x"]-p[0])**2 + (q["y"]-p[1])**2)[:3]
            pris = {q["c"] for q in voisins}
            libres = [k for k in range(len(pal)) if pal[k] not in pris] or list(range(len(pal)))
        ci = libres[(i * 3) % len(libres)]
        S.append({"x": p[0], "y": p[1], "w": W_FIN, "ci": ci, "c": pal[ci],
                  "ang": (i * 1.7) % 3.1416,
                  "monde": (monde_i if melange else monde), "k": i})
    if melange:
        # Chaque dalle garde le monde ET la palette de sa plantation. Elle est peinte
        # seule, autour de sa graine, sur un rayon de 0,62 × l'espacement : la trame
        # s'arrête tuile par tuile. Aucune frontière n'est dessinée, donc aucune arête.
        corps = "".join(RD[s2["monde"]]([s2], bb, sp, centre=(s2["x"], s2["y"]),
                                        R=sp * 0.62) for s2 in S)
    else:
        corps = RD[monde](S, bb, sp)
    if contour:
        # aucun Promi : la Toile est semée de graines GRISES, comme seedGray() du prototype.
        # On n'invente aucune forme — c'est le même moteur, dans les tons neutres du monde.
        # sur un champ mauve, les gris sombres du prototype font des trous noirs :
        # on prend ses tons crème, qui sont ses neutres du mode clair.
        gris = GLIGHT
        for i, s2 in enumerate(S):
            s2["c"] = gris[i % len(gris)]
        corps = RD[monde](S, bb, sp)
    ech = 1 / k
    bg = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{fond}"/>' if fond else ""
    return (bg + f'<g transform="translate({x0} {y0}) scale({ech:.4f})">{corps}</g>')
```

### Le semis et la relaxation de Lloyd

```python
def graines(n, bb, seed=0, relax=4):
    """Positions relaxées façon lloyd() du prototype."""
    import random as _r
    rnd = _r.Random(seed)
    x0, y0, x1, y1 = bb
    cols = max(1, round(math.sqrt(n * (x1 - x0) / max(1, (y1 - y0)))))
    rows = max(1, math.ceil(n / cols))
    pts = []
    for i in range(n):
        c, r = i % cols, i // cols
        pts.append([x0 + (x1 - x0) * (c + .5 + rnd.uniform(-.2, .2)) / cols,
                    y0 + (y1 - y0) * (r + .5 + rnd.uniform(-.2, .2)) / rows])
    for _ in range(relax):
        for i, cell in enumerate(_voronoi(pts, bb)):
            if len(cell) >= 3:
                pts[i] = [sum(p[0] for p in cell) / len(cell),
                          sum(p[1] for p in cell) / len(cell)]
    return pts
```

### Encre — le monde par défaut

```python
def Renc(S, bb, sp, only=None, centre=None, R=None):
    """Renc : neuf ellipses par dalle, semées par le LCG du prototype, opacité .9.
       C'est le monde par défaut — les taches d'encre débordent de leur cellule."""
    out = []
    for k, s in enumerate(S):
        if only is not None and s["monde"] != only:
            continue
        rnd = _lcg(k)
        rad = sp * 0.52
        for b in range(9):
            ex = (rnd() - .5) * rad * 1.2
            ey = (rnd() - .5) * rad
            rx = rad * (.32 + rnd() * .42)
            ry = rad * (.16 + rnd() * .32)
            ea = rnd() * 3.14
            out.append(f'<ellipse cx="{s["x"]+ex:.1f}" cy="{s["y"]+ey:.1f}" rx="{rx:.1f}" '
                       f'ry="{ry:.1f}" transform="rotate({math.degrees(ea):.1f} '
                       f'{s["x"]+ex:.1f} {s["y"]+ey:.1f})" fill="{s["c"]}" opacity=".9"/>')
    return "".join(out)
```

### La hauteur du trait d'une Nuée

```python
def hauteur_trait_nuee(n):
    """LA RÈGLE PROPRE À LA FICHE DE NUÉE.

       Une fiche de promesse compte ses éléments en lignes de phrase : 32 px chacune.
       Une fiche de Nuée les compte en lignes de fil : 86 px chacune (74 + 12 d'écart).
       D'où un pas différent, pour la même idée — le trait monte à mesure que le
       contenu s'installe sous lui.

           base = max(176, 460 − 86 n)      n = Promi et Chiche de la Nuée

       460 quand elle est vide : le trait est au plus bas de tout le produit, la Toile
       occupe 435 px. Chaque Promi ou Chiche le fait MONTER de 86 px — soit exactement
       la hauteur de la ligne qu'il ajoute. À 176 il ne monte plus : c'est le
       défilement qui prend le relais."""
    return max(PLANCHER, PLAFOND - 86 * n)
```

### La mise en page

```python
def compose(theme, n, meta=None):
    """La mise en page découle de la règle, elle ne la contredit jamais.
       1, 2 ou 3 : toutes les lignes entières, la dernière à 12 px de la barre.
       4 et plus : trois entières, la quatrième visible sur 27 px sous la barre."""
    base = hauteur_trait_nuee(n)
    return base, (n if n <= 3 else 4)
```

## 12 · Inventaire écran par écran — la fiche de Nuée
**20 écrans.** Coordonnées absolues, coin haut-gauche, style complet.

### Nuée vide — thème sombre

Fond `#1A1230` · **trait : base = 460, amplitude = 40** · 0 Promi ou Chiche · 0 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 540 | — |  |
| TOILE | 0 | 0 | 390 | 540 | — |  |
| TOILE | 0 | 0 | 390 | 540 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 511 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 521 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 635 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 665 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 730 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | AUCUN PROMI ENCORE |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Nuée vide — thème clair

Fond `#F4EEE1` · **trait : base = 460, amplitude = 40** · 0 Promi ou Chiche · 0 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 540 | — |  |
| TOILE | 0 | 0 | 390 | 540 | — |  |
| TOILE | 0 | 0 | 390 | 540 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #16171B | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #16171B · interlettre .20em | ✕ FERMER |
| bloc | 24 | 511 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 521 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 635 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 665 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 730 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | AUCUN PROMI ENCORE |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Un Promi — thème sombre

Fond `#1A1230` · **trait : base = 374, amplitude = 40** · 1 Promi ou Chiche · 1 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 454 | — |  |
| TOILE | 0 | 0 | 390 | 454 | — |  |
| TOILE | 0 | 0 | 390 | 454 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 425 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 435 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 549 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 579 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 644 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 1 PROMI · 1 TENU |
| bloc | 24 | 674 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Un Promi — thème clair

Fond `#F4EEE1` · **trait : base = 374, amplitude = 40** · 1 Promi ou Chiche · 1 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 454 | — |  |
| TOILE | 0 | 0 | 390 | 454 | — |  |
| TOILE | 0 | 0 | 390 | 454 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 425 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 435 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 549 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 579 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 644 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 1 PROMI · 1 TENU |
| bloc | 24 | 674 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Deux — thème sombre

Fond `#1A1230` · **trait : base = 288, amplitude = 40** · 2 Promi ou Chiche · 2 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 368 | — |  |
| TOILE | 0 | 0 | 390 | 368 | — |  |
| TOILE | 0 | 0 | 390 | 368 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 339 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 349 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 463 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 493 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 558 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 2 PROMI · 1 TENU |
| bloc | 24 | 588 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 674 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Deux — thème clair

Fond `#F4EEE1` · **trait : base = 288, amplitude = 40** · 2 Promi ou Chiche · 2 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 368 | — |  |
| TOILE | 0 | 0 | 390 | 368 | — |  |
| TOILE | 0 | 0 | 390 | 368 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 339 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 349 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 463 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 493 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 558 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 2 PROMI · 1 TENU |
| bloc | 24 | 588 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 674 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Trois — thème sombre

Fond `#1A1230` · **trait : base = 202, amplitude = 40** · 3 Promi ou Chiche · 3 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 282 | — |  |
| TOILE | 0 | 0 | 390 | 282 | — |  |
| TOILE | 0 | 0 | 390 | 282 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 253 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 263 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 377 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 407 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 472 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 3 PROMI · 1 TENU |
| bloc | 24 | 502 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 588 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 674 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Trois — thème clair

Fond `#F4EEE1` · **trait : base = 202, amplitude = 40** · 3 Promi ou Chiche · 3 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 282 | — |  |
| TOILE | 0 | 0 | 390 | 282 | — |  |
| TOILE | 0 | 0 | 390 | 282 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 253 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 263 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 377 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 407 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 472 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 3 PROMI · 1 TENU |
| bloc | 24 | 502 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 588 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 674 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Quatre — thème sombre

Fond `#1A1230` · **trait : base = 176, amplitude = 40** · 4 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 4 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Quatre — thème clair

Fond `#F4EEE1` · **trait : base = 176, amplitude = 40** · 4 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 4 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Sept — thème sombre

Fond `#1A1230` · **trait : base = 176, amplitude = 40** · 7 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 7 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Sept — thème clair

Fond `#F4EEE1` · **trait : base = 176, amplitude = 40** · 7 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 7 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Douze — thème sombre

Fond `#1A1230` · **trait : base = 176, amplitude = 40** · 12 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 12 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Douze — thème clair

Fond `#F4EEE1` · **trait : base = 176, amplitude = 40** · 12 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 12 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Trente — thème sombre

Fond `#1A1230` · **trait : base = 176, amplitude = 40** · 30 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 30 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Trente — thème clair

Fond `#F4EEE1` · **trait : base = 176, amplitude = 40** · 30 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 30 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Cent — thème sombre

Fond `#1A1230` · **trait : base = 176, amplitude = 40** · 100 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #F4EEE1 | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #F4EEE1 | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #D0B0FF · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #F4EEE1 · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 100 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Cent — thème clair

Fond `#F4EEE1` · **trait : base = 176, amplitude = 40** · 100 Promi ou Chiche · 4 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| TOILE | 0 | 0 | 390 | 256 | — |  |
| bloc | 24 | 38 | — | 34 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 27 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc | 24 | 227 | 82 | — | aligné center |  |
| SVG | interne | interne | 78 | 78 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 48 | 48 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 14 · couleur #16171B | toi |
| bloc | 136 | 237 | 70 | — | aligné center |  |
| SVG | interne | interne | 58 | 58 | — |  |
| bloc | 50% | 50% | — | — | — |  |
| SVG | interne | interne | 36 | 36 | fond #8A5CF0 · rayon 999 |  |
| · dedans | interne | interne | — | — | Bricolage 600 / 13.5 · couleur #16171B | le potager |
| bloc texte | 24 | 351 | — | — | Bricolage 600 / 19 · couleur #8A5CF0 · interlettre -.01em | Avec Rachel, Adrien, +3 |
| bloc texte | 24 | 381 | 342 | — | Bricolage 700 / 38 · couleur #16171B · interlettre -.025em · interligne 1.02 | le potager |
| bloc texte | 24 | 446 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 100 PROMI · 1 TENU |
| bloc | 24 | 476 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 562 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 648 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 734 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Le fil, après défilement — thème sombre

Fond `#1A1230` · **trait : base = 58, amplitude = 16** · 8 Promi ou Chiche · 8 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 114 | — |  |
| TOILE | 0 | 0 | 390 | 114 | — |  |
| TOILE | 0 | 0 | 390 | 114 | — |  |
| bloc | 24 | 20 | — | 30 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 23 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 98 | — | — | Bricolage 700 / 26 · couleur #F4EEE1 · interlettre -.03em | le potager |
| bloc texte | 24 | 136 | — | — | Apfel 500 / 12.5 · couleur #D0B0FF · interlettre .20em | 8 PROMI · 2 TENUS |
| bloc | 24 | 182 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 268 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 354 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 440 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 24 | 526 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | réparer le grillage du fond |
| bloc | 24 | 612 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #FFC0A8 · interlettre .18em | CHICHE LANCÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | chiche de venir désherber samedi |
| bloc | 24 | 698 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | semer la première planche |
| bloc | 24 | 784 | 342 | 74 | fond #271B45 · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #F4EEE1 · interlettre -.02em · interligne 1.05 | rapporter la clé du cabanon |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

### Le fil, après défilement — thème clair

Fond `#F4EEE1` · **trait : base = 58, amplitude = 16** · 8 Promi ou Chiche · 8 ligne(s) de fil

| type | x | y | largeur | hauteur | style | contenu |
|---|---|---|---|---|---|---|
| TOILE | 0 | 0 | 390 | 114 | — |  |
| TOILE | 0 | 0 | 390 | 114 | — |  |
| TOILE | 0 | 0 | 390 | 114 | — |  |
| bloc | 24 | 20 | — | 30 | — |  |
| · dedans | interne | interne | — | — | Fraunces 600 / 23 · couleur #F4EEE1 | Nuée |
| · dedans | interne | interne | — | — | Apfel 500 / 12.5 · couleur #F4EEE1 · interlettre .20em | ✕ FERMER |
| bloc texte | 24 | 98 | — | — | Bricolage 700 / 26 · couleur #16171B · interlettre -.03em | le potager |
| bloc texte | 24 | 136 | — | — | Apfel 500 / 12.5 · couleur #8A5CF0 · interlettre .20em | 8 PROMI · 2 TENUS |
| bloc | 24 | 182 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | monter la serre avant les gelées |
| bloc | 24 | 268 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | reprendre l'arrosage automatique |
| bloc | 24 | 354 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | récupérer les plants de tomates |
| bloc | 24 | 440 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | CHICHE RELEVÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | vider le composteur à deux |
| bloc | 24 | 526 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | réparer le grillage du fond |
| bloc | 24 | 612 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #FFC0A8 · interlettre .18em | CHICHE LANCÉ |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | chiche de venir désherber samedi |
| bloc | 24 | 698 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #2BE88C · interlettre .18em | TENU |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | semer la première planche |
| bloc | 24 | 784 | 342 | 74 | fond #E7DFCE · rayon 20 |  |
| SVG | 0 | 0 | 103 | 74 | — |  |
| bloc | 8 | 9 | — | — | — |  |
| SVG | interne | interne | 70 | 56 | — |  |
| bloc texte | 108 | 15 | — | — | Apfel 500 / 10.5 · couleur #F07A2E · interlettre .18em | À TENIR |
| bloc texte | 108 | 34 | 222 | — | Bricolage 700 / 19 · couleur #16171B · interlettre -.02em · interligne 1.05 | rapporter la clé du cabanon |
| bloc | 0 | 760 | 390 | 84 | fond #8A5CF0 |  |
| · dedans | interne | interne | — | — | Bricolage 700 / 21 · couleur #F4EEE1 | Peaufiner |
| · dedans | interne | interne | — | — | Bricolage 400 / 15 · couleur #F4EEE1 | ▾ |
| · dedans | interne | interne | 46 | 46 | contour 3px solid #F4EEE1 · rayon 999 |  |
| SVG | interne | interne | 22 | 22 | — |  |

---

## 13 · Le défilement — règle unique dans le produit

Sur la fiche d'une Nuée, **le doigt qui descend fait défiler le fil**, pas les réglages.
L'encart, les Noyaux, le titre et la méta remontent et disparaissent sous le trait ; les
Promi et les Chiche prennent toute la place, et il n'en reste qu'une bande de Toile en
haut. La Toile affichée dans cette bande est **la même**, simplement remontée : ce n'est
jamais une seconde composition.

**Conséquence directe : sur cette page, Peaufiner ne s'ouvre qu'en touchant sa barre.**
Partout ailleurs c'est l'inverse. Sans cette exception écrite, le comportement sera
implémenté comme les autres écrans.

---

## 14 · Ce qui reste à trancher

- **La borne d'affichage.** Cent dalles, trois cents au Cercle ? Le nombre de Promi et de
  Chiche d'une Nuée, lui, n'est pas plafonné.
- **Le plancher à 176** au lieu de 196 : écart assumé pour tenir trois lignes entières, ou
  retour à 196 en n'affichant que deux lignes et demie.
- **Le contraste de six teintes** sur le champ mauve : `#a85fb0`, `#A85C32`, `#C8682E`,
  `#b5762f`, `#3f6fa0`, `#5a86b0` ont moins de 0,06 d'écart de luminance avec `#8A5CF0`.
  Elles viennent du prototype, où le fond est sombre. Soit on les écarte de l'encart d'une
  Nuée, soit on assombrit le champ derrière la Toile.

---

## 15 · Vérification — la fiche de Nuée

Le script `redteam_nuee.py` repasse ces contrôles sur chaque écran, dans les deux thèmes :

1. ordre de peinture — la Toile sous le trait
2. masque = le champ, jamais un rectangle
3. marges latérales 24 / 366
4. aucun chevauchement de blocs
5. corps conforme au thème
6. aucun ton sur ton
7. mot-marque encre sur Toile vide, crème sinon
8. Fraunces réservée au seul mot-marque
9. barre unique, à y = 760
10. pas de 12 px entre lignes, et **12 px** sous la dernière ligne entière
11. quatrième ligne visible sur 26 px, tolérance 20 à 34
12. nombre de dalles conforme
13. méta cohérente avec le nombre de Promi
14. aucune dalle de la couleur du champ
15. aucun dégradé, filet ni ombre
16. quatre graisses seulement
17. lexique
