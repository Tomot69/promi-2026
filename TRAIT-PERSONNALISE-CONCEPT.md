# C-045 · Le trait de validation personnalisé — CONCEPT (v129, rien n'est construit)

> Idée de Tom (4 oct. 2026) : « un appui long sur la flèche du début du trait ouvre un cadre où l'on redessine soi-même le chemin de son
> trait au pinceau choisi. Le trait est légèrement stabilisé, sans tremblement ni angles, avec retour en arrière possible, et il faut aller
> jusqu'au bout pour le poser ; il s'affine un peu si le chemin est long ; il reste ensuite ainsi ; en le baissant, on libère de la place
> pour le dessin. »

Ce document pose le concept et les trois points à résoudre. Chaque point donne ce que le produit fait AUJOURD'HUI (lu dans `CLAUDE.md` et
dans l'app), puis des options. **Rien n'est tranché : c'est à Tom de choisir.**

## 1 · Le parcours, tel que Tom le décrit

1. **L'entrée** : un appui long sur la flèche du début du trait (le rond gauche du geste, §5). Un toucher bref garde son sens d'aujourd'hui
   (tracer pour tenir) ; seul l'appui maintenu ouvre le cadre.
2. **Le cadre** : la zone où le chemin peut passer — toute la largeur (0 → 390), entre un haut et un bas à fixer (point 2.1). Le chemin
   d'aujourd'hui y est montré en fantôme pointillé : il MANQUE un chemin, c'est l'usage que la loi des points autorise.
3. **Le tracé** : on part du rond gauche et on va jusqu'au bord droit, au pinceau choisi sur la page + ou dans Peaufiner (§5, « un réglage
   vit là où vit ce qu'il règle »). Le trait suit le doigt, lissé.
4. **Le retour en arrière** : revenir sur ses pas efface la fin du chemin (le doigt qui recule « rembobine ») ; lever le doigt avant la
   fin laisse le chemin en attente, on le reprend où il s'arrête.
5. **Poser** : seulement quand le chemin touche le bord droit. Sinon rien n'est gardé, l'ancien chemin reste.
6. **Après** : le chemin reste celui de CETTE parole (comme le pinceau) ; un chemin tracé plus bas laisse plus de bande au-dessus de lui.

## 2 · Les trois points à résoudre

### 2.1 · La loi sur la hauteur du trait, figée à la plantation

**Aujourd'hui** : le trait est une onde calculée — une base et une amplitude par écran (fiche : bases 262 · 372 · 376 selon l'état ;
page + : 196 au repos, 144 sur un choix ouvert ; Cercle : `max(176, 460 − 86 n)`, 58 à l'état défilé). La boîte de la dalle se déduit de
la base (`dh = base − amp − 100`), le corps de la fiche commence sous l'onde, et les juges portent ces cotes en dur (`releve-S1`,
`redteam_nuee`, `redteam_formes`). Un chemin libre défait tout cela d'un coup.

**Options**
- **A · Le chemin vit dans un couloir.** Il est libre en x, borné en y entre deux lignes (par exemple base − 60 et base + 40). La base de
  l'écran ne change pas : la mise en page, la boîte de la dalle et les juges restent valables ; « baisser le trait » = le tracer dans le
  bas du couloir. C'est l'option qui casse le moins.
- **B · Le chemin déplace la base.** La base devient le niveau moyen du chemin tracé, figé au moment où on le pose ; le corps de la fiche
  se recale une fois. Plus de liberté (on libère vraiment de la place pour le dessin), mais chaque fiche a sa propre mise en page : les
  cotes absolues des fiches deviennent des cotes relatives à la base, et les juges de cotes sont à réécrire.
- **C · Le chemin ne vaut que pour la bande.** Le trait tracé ne borne que le dessin et la dalle ; le corps garde l'onde d'origine en
  dessous (deux lignes superposées) — à écarter : deux traits pour une parole, la règle des trois tons ne tient plus.

**Ce que « figée à la plantation » peut vouloir dire** : comme le monde et la couleur d'une dalle (§4), le chemin est une propriété de la
parole (`p.trait = {pinceau, chemin}`), posée une fois ; le reprendre est un geste délibéré depuis la fiche. Le chemin par défaut reste
l'onde du §2.1.

### 2.2 · Le mécanisme des deux moitiés

**Aujourd'hui** : un Promi et un Chiche se tracent par moitiés — celui qui donne sa parole trace la sienne, l'autre vient à sa rencontre ;
la moitié qui manque est en pointillé. Un Cercle se lance au trait entier (0 → 390).

**La question** : quand le chemin est personnalisé, quel chemin suit l'autre ?
- **A · Un seul chemin, tracé en entier par celui qui plante.** Il dessine les 390 pt ; tenir = retracer SA moitié sur ce chemin, l'autre
  retrace la seconde. Simple, une seule forme pour la parole ; mais celui qui reçoit n'a rien choisi.
- **B · Chacun sa moitié.** Celui qui plante ne dessine que la première moitié (0 → 195) ; la seconde reste l'onde par défaut jusqu'à ce
  que l'autre trace — et il peut alors la redessiner aussi. Les deux moitiés doivent se joindre : le point de rencontre (x 195) garde une
  hauteur imposée, celle où la première s'arrête.
- **C · Le chemin personnalisé ne vaut que pour une parole à soi et pour un Cercle** (trait entier, une seule main). Promi à quelqu'un et
  Chiche gardent l'onde. Le plus sûr pour une première version.

### 2.3 · La fiabilité du geste

Tenir une parole se fait en traçant : un chemin que la main ne peut pas refaire rendrait la parole impossible à tenir. Garde-fous possibles,
à doser sur un vrai téléphone :
- **Un chemin qui avance** : x toujours croissant (pas de boucle, pas de retour), du rond gauche au bord droit — c'est ce qui rend le retour
  en arrière lisible (reculer = effacer) et le suivi au doigt possible.
- **Une pente bornée** : pas de mur vertical ; au-delà d'un angle, le lissage arrondit.
- **Le lissage** (« sans tremblement ni angles ») : le même que celui de la planche du dessin (C-042) — moyenne glissante sur la position,
  courbe passant par les points ; jamais de segment droit (§5 : courbes, jamais de segments).
- **La longueur** : « il s'affine un peu si le chemin est long » — l'épaisseur baisse quand la longueur développée dépasse celle de l'onde
  d'origine (borne basse à fixer, pour que le trait porte toujours l'état : il se juge en ΔE ≥ 15 sur son champ).
- **La tolérance du suivi** : aujourd'hui le doigt suit une onde douce ; sur un chemin libre, la bande d'acceptation autour du trait doit
  s'élargir dans les courbes serrées. À mesurer au vrai doigt (CDP), dans toutes les directions.
- **L'appui long** : ne doit jamais se déclencher pendant un tracé pour tenir (le doigt part aussitôt) — seuil de durée ET d'immobilité.

## 3 · Ce que le concept touche ailleurs

- **L'outil de dessin (C-042)** : un trait plus bas agrandit la bande ; sur un Cercle (bande de 50 pt) c'est ce qui rendrait le dessin
  possible. Les deux chantiers se décident ensemble.
- **La carte d'Index, le bandeau du Fil, l'instant** : ils montrent le trait en petit (période 1 sur leur largeur). Montrent-ils le chemin
  personnalisé, réduit, ou gardent-ils l'onde ? (Une dalle suit le Studio ; un trait est un état : il devrait rester reconnaissable.)
- **Le portage** : le chemin est une donnée (une liste de points lissés), pas une image — à inscrire au dossier de portage.

## 4 · Ce qu'il faut trancher avant toute planche

1. Le couloir (2.1 A) ou la base qui bouge (2.1 B) ?
2. Qui trace quoi (2.2 A, B ou C) ?
3. Le chemin avance-t-il toujours (pas de boucle) ?
4. Les petites représentations du trait (Index, Fil) suivent-elles le chemin ?
