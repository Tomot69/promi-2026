# Vérifier sans lire le code

> Pour Tom. Aucune connaissance technique requise.

---

## 1 · Les trois commandes

Ouvrez le Terminal dans le dossier du projet et tapez :

```bash
python3 redteam_ecrans.py
```

**Ce que ça affiche à la fin :** un nombre sur un autre.

```
142/142     ✅ tout va bien
139/142     ❌ trois choses sont cassées
```

Puis les autres batteries, une par une :

```bash
python3 redteam.py            attendu : 15/15
python3 redteam2.py           attendu : 10/10
python3 redteam3.py           attendu : 18/18
python3 redteam_demande.py    attendu : 19/19
python3 redteam_toile.py      attendu : 16/16  (15/16 acceptable, voir § 5)
python3 redteam_geste.py      attendu : 13/13
python3 redteam_phrase.py     attendu : 6/6
```

`redteam_phrase.py` (8ᵉ batterie, chantier 56) attrape la casse **silencieuse** de la
liaison phrase → formulaire de la page + : si un champ change de nom (ou de libellé pour
« quand »), il passe sous 6/6. À lancer avec les autres à chaque livraison.

**La règle :** si un nombre a baissé, quelque chose est cassé. Peu importe quoi.

---

## 1 bis · LA commande qui protège le design

C'est la plus importante. Elle vérifie que **rien n'a bougé sans qu'on le demande**.

```bash
python3 releve-design.py
```

### Ce que ça affiche

```
✅  AUCUN ÉCART. Le design est intact.
```
→ Le lot n'a rien cassé ailleurs. Vous pouvez déposer.

```
❌  14 ÉCARTS avec la référence :
    clair/tenue · fiche · titre · fontSize : 34px -> 28px
    …
```
→ Quelque chose a changé **sans qu'on le demande**. Ne déposez pas.

```
❌  3 COULEURS FAUTIVES :
    sombre/nuee · fiche · rang lien : trait NEUTRE rgb(128,128,132)
```
→ Un trait gris est apparu. Ne déposez pas.

### Comment le lire sans connaître le code

Chaque ligne d'écart se lit comme une phrase :

```
clair/tenue  ·  fiche · titre  ·  fontSize  :  34px  ->  28px
   ↑              ↑                 ↑            ↑        ↑
 quel écran    quel élément    quoi         avant    après
```

**La question à vous poser :** est-ce que j'ai demandé ce changement dans le lot ?

- **Oui** → normal, c'est ce que vous vouliez
- **Non** → régression, à corriger

### Après un lot que vous validez

```bash
python3 releve-design.py --figer
```

Cela enregistre le nouveau design comme référence. **Ne le faites que quand vous
êtes satisfait** — sinon vous figez une erreur.

---

## 2 · Les captures à exiger

À chaque livraison, demandez **au minimum** :

### Pour un écran modifié

- **Avant / après**, côte à côte, au même format
- **Les deux modes** : clair et sombre
- **Les états concernés** : à tenir, tenue, en cours, Nuée si l'écran en a

### Formulez comme ça

> « Livre-moi l'avant/après en clair et en sombre, avec les mesures. »

### Les mesures à exiger

Un chiffre vaut mieux qu'une affirmation. Exigez systématiquement :

| Ce qui est modifié | La mesure à demander |
|---|---|
| une couleur | la valeur RGB calculée par le navigateur |
| une position | la distance en pixels par rapport au bord |
| une dalle | le nombre de points peints dans le canevas |
| un texte | la taille de police calculée |
| une mise en page | le nombre de débordements et de chevauchements |

**Si la réponse ne contient aucun chiffre, la vérification n'a pas eu lieu.**

---

## 3 · À quoi vous reconnaissez que c'est cassé

### Sur les captures

| Signe | Ce que ça veut dire |
|---|---|
| Un trait **gris ou noir** | La règle des couleurs n'est pas appliquée |
| Un texte **de la couleur du fond** | `-webkit-text-fill-color` diffère de `color` |
| Une dalle **délavée ou floue** | Un filtre ou une opacité est passé devant |
| Une dalle **anguleuse, en polygone** | L'échelle d'appel est mauvaise |
| Un élément **coupé par le bas** | La trame n'est pas respectée |
| Deux éléments **superposés** | Le DOM n'a pas été réordonné |
| Un **grand vide** entre deux blocs | Un `margin-top: auto` traîne |
| **Deux barres identiques** | Un ancien bloc n'a pas été supprimé |

### Sur l'appareil

| Signe | Ce que ça veut dire |
|---|---|
| L'app **rame** ou chauffe | Une boucle d'animation tourne en permanence |
| Une capture d'écran **échoue** | Même cause |
| Le **scroll est bloqué** | Un `position: sticky` mal posé |
| Un écran est **transparent** | Un sélecteur ne correspond à rien |
| Rien ne change **alors qu'on a dit que si** | Une règle postérieure écrase |

---

## 4 · Que faire quand c'est cassé

### Étape 1 — ne pas accepter la livraison

Ne déposez pas le fichier. Répondez :

> « Batterie X à N/M au lieu de M/M. Ne livre pas, corrige. »

ou

> « Sur la capture, [le problème]. Mesure-le et corrige avant de livrer. »

### Étape 2 — demander la cause, pas le symptôme

> « Pourquoi ? Donne-moi la cause, pas une nouvelle règle par-dessus. »

C'est le point critique. **Ajouter une règle CSS pour masquer un problème est ce
qui a créé la dette actuelle** — 2 400 règles dont 54 % sont mortes.

### Étape 3 — si ça se répète

Après deux tentatives infructueuses sur le même point :

> « Arrête. Reviens à la version précédente et dis-moi ce qui bloque. »

Une version qui marche vaut mieux qu'une version à moitié corrigée.

---

## 5 · Les faux positifs connus

**`redteam_toile.py` donne parfois 15/16 — cause connue, ce n'est pas une régression.**
Le sous-contrôle « Mes Promi : les intitulés restent » compte des pixels clairs sur la
toile de partage, dont les **dalles respirent** (leur forme oscille avec le temps écoulé
depuis le chargement — `Renc(now,…)`, aucun aléa). Selon l'instant du snapshot, le compte
varie. **Convention : 15/16 compte comme un succès. À 14/16 ou moins, on regarde.**
(Un jour ce contrôle sera réécrit — comparer une dalle à sa propre référence plutôt que
compter des pixels clairs ; chantier futur, voir `ETAT-DES-LIEUX.md § 3`.)

**Le tap sur une dalle de la Toile ne fonctionne pas dans les tests.**
Vérifié : c'était déjà le cas avant les dernières corrections. Ce peut être une
limite du test automatisé. **À confirmer sur votre iPhone.**

---

## 6 · La checklist avant de déposer un fichier

```
□  releve-design.py affiche AUCUN ÉCART
□  Les sept batteries sont au niveau attendu
□  J'ai vu l'avant/après en clair ET en sombre
□  La réponse contient des chiffres, pas seulement des affirmations
□  Ce qui n'a pas été fait est dit explicitement
□  Aucun trait gris sur les captures
□  Les dalles sont nettes et à leurs couleurs
□  Rien ne dépasse, rien ne se superpose
```

**Si une case n'est pas cochée, ne déposez pas.**

---

## 7 · Comment demander un lot

Un bon lot :

```
LOT · [nom de l'écran]

Ce que je veux :
  · [point 1]
  · [point 2]
  · [point 3]

Référence : PARCOURS.md § [numéro]

Livre-moi :
  · l'avant/après en clair et en sombre
  · les sept batteries
  · les mesures
  · ce que tu n'as pas fait
```

**Un lot = un écran.** Ne jamais en enchaîner plusieurs : c'est ce qui a produit
les régressions les plus coûteuses.
