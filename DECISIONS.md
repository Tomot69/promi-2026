# Décisions — tout ce qui n'existe que dans la conversation

> Ce document est le plus important du transfert. Sans lui, ces arbitrages
> disparaissent et seront refaits — probablement autrement.
>
> Chaque entrée dit **la décision**, **pourquoi**, et **ce qui a été rejeté**.

---

## A · Les décisions de conception

### A1 · Un Promi n'est pas une tâche

**Décidé.** Toute décision qui rapproche Promi d'une to-do list est rejetée,
même si elle est pratique.

**Conséquences concrètes :**
- L'échéance n'est **pas obligatoire**. « un jour » est une réponse valable.
- Pas de score, pas de pourcentage, pas de « 3 sur 5 tenus ».
- On ne coche pas, on trace.

**Rejeté :** un bouton « ajouter une échéance ». *Verbatim de l'utilisateur :
« c'est ça qui donne trop crm to do list tache à remplir non ? »*

### A2 · La création est une phrase, pas un formulaire

**Décidé.** La page + affiche une phrase complète dont les mots sont touchables.

```
Je promets ⇄ ✦
à Rachel
de rendre le livre
avant · un jour
```

**Pourquoi :** quatre blocs empilés (onglets, saisie, À QUI, EN PLUS) faisaient
formulaire. Une phrase se lit d'un coup et se complète au doigt.

**Rejeté :** la version à sections, jugée *« ultra moche pas design pas
harmonieux »*.

### A3 · Le même geste pour planter et pour tenir

**Décidé.** Ce sont les deux moments où l'on s'engage. Le même geste les relie,
et l'utilisateur n'apprend qu'une seule chose.

**Exception :** le brouillon. « Garder pour plus tard » n'est pas un engagement,
c'est un report — il garde un bouton simple.

### A4 · Le brouillon choisit sa nature

**Décidé** après analyse contradictoire, contre ma proposition initiale.

Mon argument était « ne pas gêner la capture rapide ». Il ne tient pas : **un
brouillon qu'on doit entièrement remplir plus tard n'a pas fait gagner de temps,
il l'a reporté.**

**La nuance retenue :** le choix est **pré-coché sur « un Promi »**. C'est le cas
le plus fréquent, et on peut écrire sans jamais toucher aux pastilles.

**Les quatre rappels terracotta** quand un brouillon n'est pas encore planté :
- un liseré pointillé de 3 px qui encadre l'écran
- une pastille `BROUILLON` en contour, haut à droite
- le filet du titre en terracotta
- le bouton d'action en terracotta plein

### A5 · Le thème d'une Nuée est supprimé

**Décidé.** Nom + note suffisent.

**Pourquoi :** le thème disait la même chose que le nom, en plus long. Une Nuée
s'appelle *Week-end à Lisbonne* — elle n'a pas besoin d'expliquer en plus qu'elle
parle d'un week-end à Lisbonne.

La **note**, elle, apporte autre chose : une intention, un mot pour le groupe.
Elle est signalée sur la fiche par une pastille.

### A6 · « tout le monde » dans une Nuée

**Décidé.** Dans une Nuée, le premier destinataire est **« tout le monde »**,
coché par défaut. « Moi » passe en deuxième.

**Pourquoi :** *« c'est bizarre de juste se faire un Promi à soi même dans une
nuée »*. Un seul geste doit engager le groupe entier.

Hors Nuée, **« Moi » reste premier et coché par défaut**.

### A7 · Les deux sens de la promesse

**Décidé.** On peut promettre **et** demander une promesse.

```
Je promets ⇄     →   Rachel, promets-moi ⇄
```

**La formulation retenue :** *« Rachel, promets-moi de m'appeler avant dimanche »*.
On interpelle, puis on demande.

**Le problème résolu :** l'option était invisible. Deux mots soulignés ne se
voient pas. La bascule est devenue **une pastille menthe** — la seule couleur de
la phrase — avec une **flèche à deux traits, pointes opposées**.

**Rejeté :** les arcs courbes tête-bêche, qui se lisaient comme un trait continu.

### A8 · La page Partager n'est pas dupliquée

**Décidé.** C'est `shareScreen`, exactement — même bouton, même prévisualisation.

**Seul le sélecteur change** : un onglet s'ajoute en premier, avec **le début du
vrai titre suivi de points de suspension**.

```
depuis le dock      Ma Toile | Mes Promi
depuis un Promi     rendre… | Ma Toile | Mes Promi
depuis une Nuée     Week-end… | Ma Toile | Mes Promi
```

**L'onglet ne s'installe pas.** Qu'on ait partagé ou non, rouvrir depuis le dock
ramène `Ma Toile / Mes Promi`.

**Rejeté :** un résumé inventé (« le livre »). *« un titre inventé à partir du
titre, ce n'est pas clair »*.

### A9 · Aucun statut écrit dans les images partagées

**Décidé.** Pas de « TENUE » sur l'image. La couleur le dit déjà ; un mot en
capitales sur une image est du bruit.

### A10 · Une Nuée se partage en constellation

**Décidé.** Les dalles se chevauchent, les prénoms sur une ligne, le nom en
grand. **Aucun chiffre, aucun compte.**

**Rejeté :** « 7 PROMI · 4 TENUS », jugé *« crm »* — c'est un rapport, pas une
image à publier.

### A11 · Gratuit et Cercle

**Décidé** après trois révisions.

**Le critère :** est-ce que ça sert à tenir sa parole, ou est-ce que ça n'a de
valeur que dans la durée ?

**Les Nuées sont illimitées en gratuit** — membres compris. Corrigé après une
première version qui les limitait à trois : brider le collectif revient à freiner
sa propre croissance.

**Le partage n'est jamais bridé.** C'est le moteur viral.

**Le Cercle** ouvre la réciprocité (*ce que les autres tiennent envers vous*),
la tendance sur trois mois, la récurrence, le rappel intelligent, et quatre
mondes.

### A12 · Les commentaires restent ouverts après validation

**Décidé.** Un Promi tenu se commente encore. La ligne « répondre… » est présente
sur les deux écrans, à la même place.

Et **la note et les fichiers restent signalés** par des pastilles — sinon on ne
sait pas qu'ils sont là.

### A13 · L'iPhone 12 est le plancher

**Décidé** par Tom, 11 septembre 2026 : *« L'iPhone 12 est le plancher. Puce A14, encore massivement en
circulation. »*

Tout ce qui doit tourner partout se juge contre ce palier — la sphère de l'Aura en premier. Le Mac du banc
et le processeur ralenti ×4 / ×6 ne sont que des substituts (QUESTIONS.md · Q178). **La sphère se mesure
contre A14 dès qu'un appareil est joignable** ; si le palier de 110 000 poils n'y tient pas, c'est la
sphère qui change, pas un réglage (CHANTIERS §9, « le téléphone »).

---

## B · Les décisions visuelles

### B1 · La règle des trois tons

**Décidé** après deux corrections.

```
1 · la DALLE     sa couleur propre, issue du monde
2 · le FOND      l'état
3 · les TRAITS   une troisième teinte, dérivée de la dalle
```

**Le problème résolu :** je faisais porter la couleur d'état **à la fois** au
fond et aux traits. Le ton sur ton était inévitable.

**⚠ Point resté ouvert.** La méthode actuelle décale la teinte de la dalle de
150°. L'utilisateur juge le résultat *« joli mais le non sens non »* — le
décalage sort parfois de la palette du monde choisi.

**Deux options à trancher :**
- (a) conserver le décalage, en le réduisant à 90° ou 120°
- (b) piocher une **couleur réelle de la palette du monde actif**

L'option (b) est plus juste conceptuellement mais demande d'exposer les palettes
des neuf mondes, ce qui n'est pas fait.

### B2 · Aucun trait neutre, nulle part

**Décidé.** Un filet gris est un défaut, pas une neutralité.

**Pourquoi :** *« c'est boring », « ça fait fiche morte »*.

**Vérifié :** un détecteur parcourt les six fiches dans les deux modes et mesure
la saturation de chaque filet. Résultat en v588 : **30 traits neutres → 0**.

### B3 · La dalle est toujours au premier plan

**Décidé et répété six fois.** C'est la règle la plus violée du projet.

Le voile de couleur est le **`background` du bloc**, jamais un calque par-dessus.
La dalle est au-dessus (`z-index` supérieur), les textes au-dessus d'elle.

```
opacity: 1  ·  filter: none  ·  mix-blend-mode: normal
```

**Ce qui l'a cassée, à chaque fois :** une règle groupée avec `.tracant` qui
posait `opacity: .5`, invisible dans la liste des sélecteurs.

### B4 · La trame de chaque fiche

**Décidé.**

```
HAUT        176–210 px fixes   la dalle, la nature, ✕ FERMER
TITRE       auto + 24 px       ce qu'on lit en premier
CORPS       le reste           le contenu commence EN HAUT
TRAIT       118 px + 24 px     toujours entier
PEAUFINER   62 px              le même partout
```

**Interdit :** `margin-top: auto` sur le corps. Il crée un trou — la moitié en
haut, la moitié en bas.

### B5 · Le glyphe ✦

**Décidé.** Le même glyphe que le Fil (présent 8 fois dans l'app) ferme la phrase
de création, en menthe.

**Pourquoi :** *« sinon ça fait je te donne un ordre »*. Il enjoue sans expliquer.

### B6 · Les boutons d'action sont des icônes rondes

**Décidé.** Partager, commenter, joindre : **icône seule**, jamais de texte à
côté. Un rond de 56 à 62 px.

**Rejeté :** le bouton « Partager » avec son texte, jugé *« moche, mal intégré »*.

### B7 · Le titre long réduit sa taille

**Décidé.** 34 px pour un titre court, 26 px pour un titre long. **Deux lignes
maximum, hauteur du bloc inchangée** — rien ne bouge en dessous.

### B8 · « avant · un jour »

**Décidé.** *« avant un jour »* n'est pas du français.

Un **point médian** sépare le mot du placeholder. Dès qu'une vraie échéance est
choisie, il disparaît et la phrase redevient correcte : *« avant vendredi »*.

Le point médian est déjà le séparateur de toute l'app.

### B9 · Le trait part du centre du rond

**Décidé.** Pas de l'endroit où le doigt s'est posé — sinon on perd un centimètre
d'espace d'écriture.

Et il est dessiné en **courbes quadratiques**, jamais en segments droits.

### B10 · Les animations sont lentes et discrètes

**Décidé** après une correction.

```
le pouls des cercles   5 s, cubic-bezier(.4,0,.6,1), 16 % d'écart d'opacité
l'éclat sous le doigt  6 traits à 20 %, courts
le flip de la bascule  320 ms, cubic-bezier(.22,1,.36,1)
```

**Rejeté :** 2,4 s avec 50 % d'écart — *« cheap »*.

### B11 · Le mot-marque est toujours là

**Décidé.** « Promi » en Fraunces, haut à gauche, **20 px** sur les écrans,
**15 px** dans les images partagées. Discret mais permanent.

---

### B12 · La pilule cède à 94,5 de haut

**Décidé** par Tom, 11 septembre 2026 : *« rayon = moitié de la hauteur jusqu'à [la hauteur où la pilule commence à manger
le texte], 30 au-delà. Un champ à une ligne garde sa pilule, un champ qui s'ouvre gagne l'air qu'il lui faut. »* Le seuil
est **mesuré sur l'encre** : 94,5 (QUESTIONS.md · Q203). Tout contour de 94,5 ou moins garde rayon = hauteur ÷ 2 ; au-delà,
rayon 30 — le « grand panneau » de la grammaire des contours (CLAUDE.md §5). Un seul propriétaire dans l'app : `rayon()`.

---

## C · Les pièges rencontrés — et leur cause réelle

> Chacun a coûté au moins un tour. Les relire avant de déboguer.

| # | Symptôme | Cause | Version |
|---|---|---|---|
| C1 | Une règle CSS ne s'applique pas | Une règle postérieure l'écrase. Le fichier a **jusqu'à 10 déclarations** de la même propriété sur le même sélecteur. | permanent |
| C2 | Le texte est invisible | `-webkit-text-fill-color` diffère de `color` et l'emporte. | v581 |
| C3 | La dalle est délavée | `opacity: .5` posé par une règle groupée avec `.tracant`. | v559 |
| C4 | La dalle est polygonale | `dalleTrame` appelé à une échelle > 1. Casse mosaïque, braille, pixel, gravure. | v562 |
| C5 | Un canevas est vide | `peintMinis` appelé avant que le canevas soit disposé. Relancer à 0, 60, 200, 600 ms. | v578 |
| C6 | L'app rame, les captures échouent | Un `MutationObserver` s'auto-déclenche : la fonction observée modifie une classe. **Comparer l'état avant d'agir.** | v591 |
| C7 | Un bloc ne bouge pas | Le CSS ne déplace pas les blocs. Réordonner le DOM en JS. | v540 |
| C8 | `cur` est nul | Sur une fiche de Nuée, c'est `curNuee`. | v571 |
| C9 | Un sélecteur ne correspond à rien | `personSheet` vit sous `.frame`, pas sous `.device`. | v579 |
| C10 | Le nom d'une Nuée affiche un identifiant | La table s'appelle **`NUE`**, pas `NUEES` ni `nueeNom()`. | v571 |
| C11 | Le pincement de la Toile ne marche plus | `pointer-events: none` sur `#toileCv` — c'est lui qui porte les écouteurs. | v580 |
| C12 | Un tableau d'ordre cite un id inexistant | `dpSocial` était le nom d'une version antérieure de `dpBarre`. | v576 |
| C13 | Deux barres d'actions identiques | Un ancien bloc faisait le même travail et restait dans l'ordre. | v576 |
| C14 | La classe d'une fiche de Nuée | C'est **`dp-mode-nuee`**, pas `dp-nuee`. La seconde est écrasée à l'ouverture. | v569 |
| C15 | Une teinte inline est ignorée | Une règle générique en `!important` l'écrase. Cibler `[style*=background]`. | v578 |

---

## D · Ce qui a été essayé et abandonné

### D1 · Le nettoyage du CSS — cinq échecs

Voir `ETAT-DES-LIEUX.md § 4`. **Recommandation : ne pas recommencer.**

### D2 · Le souffle permanent de la dalle

Une animation de ±0,6 % sur 9 s a été ajoutée puis retirée. *« ça se voit trop
c'est cheap »*. La fiche hérite du mouvement de la Toile, elle n'en ajoute aucun.

### D3 · La répétition en tuiles

La dalle de fond répétée en quinconce faisait *« un motif de papier peint »*.
Remplacée par **une seule dalle**, grande et nette.

### D4 · Le scroll qui déplie Peaufiner tout seul

Trois approches tentées : garder le corps ouvert en permanence, sortir Peaufiner
du flex, le passer en sticky sur son seul titre. **Les trois cassent l'en-tête**
— les pastilles remontent et chevauchent le titre.

Solution actuelle : ouverture au clic **et** au geste (`touchmove` > 26 px, ou
molette). Le scroll n'est jamais bloqué.

---

## E · Les questions ouvertes

| # | Question | Enjeu |
|---|---|---|
| E1 | **La palette des traits** — décalage de teinte ou couleur réelle du monde ? | Bloque la validation visuelle de toutes les fiches |
| E2 | **La ligne d'aide** sous la phrase — permanente ou disparaît après le 3ᵉ Promi ? | Trop discrète, on peut ne jamais découvrir la bascule |
| E3 | **Le scroll sous Peaufiner** — accepter le recouvrement, ou Peaufiner en bas de contenu ? | Gêne l'utilisateur à chaque test |
| E4 | **Le tap sur une dalle de la Toile** — fonctionne-t-il sur appareil réel ? | Mes tests n'y arrivent pas, mais c'était déjà le cas avant |
| E5 | **Les prénoms de démonstration** — garder Nico, Adrien, Rachel, Maman, Léa ? | Ils viennent du prototype ; les changer demande de changer la simu aussi |
