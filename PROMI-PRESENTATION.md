# Promi — présentation complète

> Pour quelqu'un qui n'a jamais entendu parler de ce projet.
> À lire en premier.

---

## 1. L'idée

**Promi sert à tenir sa parole.**

Quand vous promettez quelque chose à quelqu'un — rendre un livre, appeler
dimanche, réserver le van pour le week-end — vous le « plantez » dans Promi.
La promesse devient une **dalle** : une forme colorée qui prend place sur votre
**Toile**, un canevas personnel qui se remplit avec le temps.

Quand vous tenez votre parole, vous ne cochez pas une case. **Vous tracez un
trait au doigt**, d'un point à l'autre. Le geste compte autant que le résultat.

### Ce que Promi n'est pas

Ce n'est **pas une to-do list**. La différence est de nature, pas de degré :

| Une to-do list | Promi |
|---|---|
| des tâches à soi | des paroles données à d'autres |
| une échéance obligatoire | « un jour » est une réponse valable |
| on coche | on trace |
| efficacité | émotion |
| se vide | se remplit |

Cette distinction gouverne toutes les décisions de conception. Chaque fois qu'un
choix rapproche Promi d'un gestionnaire de tâches, il est rejeté — même s'il est
fonctionnellement pratique.

---

## 2. Le vocabulaire

Ces mots sont **fixes**. Ils ne se traduisent pas, ne se remplacent pas.

**Promi** — une promesse. Invariable au pluriel : *trois Promi*. C'est aussi le
nom de l'application. La dalle et le Promi sont la même chose vue de deux façons.

**Dalle** — la forme colorée qui représente un Promi. Chaque dalle est unique :
sa forme vient d'un algorithme, sa couleur du **monde** choisi.

**Toile** — le canevas principal. Un pavage de Voronoï pondéré où les dalles
s'installent. C'est l'écran d'accueil, et l'objet que l'on partage.

**Nuée** — un collectif de Promi. Un groupe d'amis, un projet, un week-end.
Plusieurs personnes y plantent leurs paroles.

**Brouillon** — une parole notée mais pas encore donnée. Elle n'engage rien.

**Fil** — le flux d'activité : ce qui a été planté, tenu, commenté.

**Aura** — l'écran de progression. Montre les liens avec chaque personne et
leur évolution.

**Studio** — le sélecteur de **monde**. Neuf univers graphiques qui changent
l'apparence de toutes les dalles.

**Peaufiner** — le tiroir de réglages, présent en bas de chaque fiche.

**Le Cercle** — l'abonnement payant.

**Planter** — créer un Promi. **Tenir** — honorer sa parole.

---

## 3. Le ton

**Chaleureux sans être mièvre.** Promi parle de parole donnée, de liens, de
confiance. Le vocabulaire est concret et un peu poétique, jamais sentimental.

**Des questions, pas des libellés.** *« Qu'est-ce que tu promets ? »* plutôt
que *« Titre »*. *« À qui »* plutôt que *« Destinataire »*. *« Pour quand »*
plutôt que *« Échéance »*.

**Le tutoiement**, toujours.

**Jamais de score, jamais de pourcentage.** On ne note pas quelqu'un sur sa
capacité à tenir parole. Une Nuée montre une bande d'harmonie colorée, pas
« 33 % tenus ».

**Un mot qui félicite, pas un chiffre.** À l'arrivée d'un geste :
*« Belle parole. »*, *« C'est fait. »*, *« Une de plus. »* — cinq formulations
qui tournent.

### Ce qui a été banni, et pourquoi

- **« Belle parole » comme bouton** — la formule est juste comme félicitation,
  fausse comme action.
- **« En replanter un »** — sonne mal, mécanique.
- **« Dire un mot » en gros bouton** — occupe un écran entier pour une action
  rare. Devient une ligne discrète sous le dernier commentaire.
- **Les scores dans les Nuées** — culpabilisants.
- **Le mot « tâche »** — l'univers de la to-do list.

---

## 4. La direction artistique

### Les couleurs

Cinq couleurs signalétiques, immuables :

```
#2BE88C   menthe        une parole tenue
#F07A2E   orange        une parole à tenir
#8A5CF0   mauve         une Nuée
#3A54FF   bleu          la création
#F4EEE1   crème         la surface claire
#16171B   encre         la surface sombre
```

**La règle des trois tons.** Une fiche porte toujours trois couleurs distinctes :
la **dalle** (sa matière), le **fond** (son état), les **traits** (une troisième
teinte dérivée de la dalle). Cette règle existe pour une raison précise : sans
elle, le fond et les traits portaient la même couleur d'état, et les traits
devenaient invisibles.

**Aucun trait neutre.** Un filet gris est considéré comme un défaut, pas comme
une neutralité. La justification : une fiche aux traits gris paraît morte.

### La typographie

```
Bricolage Grotesque   les titres, les libellés de section    700/800
Apfel                 les champs, l'interface
Fraunces              la signature « Promi »
```

Les titres sont **grands** — 34 à 48 px sur mobile. Un titre long réduit sa
taille pour tenir sur deux lignes, sans changer la hauteur du bloc.

### Les formes

**Le rayon est généreux** : 999 px pour les pastilles, 18 à 26 px pour les
cartes, 48 px pour le cadre du téléphone.

**Les pastilles disent leur état par leur remplissage** : contour = vide,
aplat plein = rempli. On lit un écran sans lire un mot.

### Les neuf mondes

Le Studio change l'apparence de toutes les dalles :

```
gratuits   Encre · Mosaïque · Touffe · Braille · Pixel
Le Cercle  Terrazzo · Gravure · Sillons · Éclats
```

Chaque monde a sa palette. La couleur des traits d'une fiche en dérive — c'est
ce qui fait que deux utilisateurs n'ont pas la même app.

---

## 5. Les écrans

### La Toile

L'accueil. Les dalles s'y installent selon un pavage de Voronoï pondéré.
On pince pour dézoomer, on touche une dalle pour ouvrir sa fiche.

**Ce code est fragile et validé — il ne se touche pas.**

### La page +

La création. **Une phrase qu'on complète** :

```
Je promets ⇄ ✦
à Rachel
de rendre le livre
avant · un jour
```

Chaque mot en pastille se touche ; ses choix s'ouvrent en dessous, dans le même
écran. La bascule `⇄` retourne la phrase en *« Rachel, promets-moi… »* — car on
peut aussi **demander** une promesse.

### La fiche d'un Promi

Ce qu'on a promis, à qui, où ça en est. Le dernier commentaire en clair, avec une
ligne « répondre… » pour continuer la conversation. Le geste en bas. Peaufiner
pour tout le reste.

### La fiche d'une Nuée

Les dalles du groupe en planche, le nom, qui en est, combien de paroles.
Puis le fil des Promi du groupe, à la même grammaire que le Fil général.
**Pas de geste** — on ne tient pas une Nuée, on l'étoffe.

### L'Index et le Fil

La liste et le flux. Chaque ligne porte le mot du temps, le titre, à qui, et
**la vraie dalle** à droite. L'aplat de la ligne prend la couleur de l'état.

### L'Aura

Les liens avec chaque personne, sous forme de disques de progression.
Un disque en gratuit — *ce que vous tenez*. Le second est du Cercle —
*ce que les autres tiennent envers vous*.

### Partager

Une image à publier. Le sélecteur en haut : `Ma Toile / Mes Promi`, plus un
onglet contextuel si l'on vient d'un Promi ou d'une Nuée. Trois formats :
9:16, 1:1, 4:5.

---

## 6. Le geste — le cœur de l'app

Tenir sa parole se fait **en traçant un trait** entre deux points.

```
au repos     deux points nus sur le fond, 118 px de haut
au contact   la zone s'ouvre à 317 px, symétriquement
le trait     libre, valide aux deux tiers de la largeur
à l'arrivée  vibration [12, 40, 26] ms, le statut passe à « tenue »
```

Le trait **part du centre du point gauche**, pas de l'endroit où le doigt s'est
posé — sinon on perd un centimètre d'espace d'écriture. Il est dessiné en
**courbes quadratiques**, jamais en segments droits : c'est ce qui lui donne
l'aspect d'un tracé à la main.

**Le même geste sert à planter.** Planter et tenir sont les deux moments où l'on
s'engage ; le même geste les relie, et l'utilisateur n'apprend qu'une chose.

Une bascule « bouton » permet de remplacer le trait par un appui, pour ceux qui
préfèrent. Le choix vaut pour les deux écrans.

Après validation, **le trait tracé est conservé** et redessiné sur la fiche —
c'est la trace de votre geste, pas une illustration générique.

---

## 7. Gratuit et Cercle

Le critère : **est-ce que ça sert à tenir sa parole, ou est-ce que ça n'a de
valeur que dans la durée ?**

| | Gratuit | ✦ Le Cercle |
|---|---|---|
| **Promettre** | sans limite · à qui · quand · note · fichiers | récurrence · rappel intelligent |
| **Les Nuées** | **illimitées, membres illimités** | — |
| **Tenir** | le trait · la trace · statut · report · commenter | — |
| **Voir** | Toile · Index · Fil · Aura · ce que **vous** tenez | **ce que les autres tiennent envers vous** · la tendance sur 3 mois |
| **Partager** | tout, toujours | — |
| **Les mondes** | Encre · Mosaïque · Touffe · Braille · Pixel | Terrazzo · Gravure · Sillons · Éclats |

**La valeur du Cercle tient en une phrase :**

> Le gratuit vous dit ce que **vous** tenez.
> Le Cercle vous dit ce que **les autres** tiennent envers vous.

C'est une bascule de sens, pas un quota levé. On ne la veut qu'une fois qu'on a
des gens dans son app — donc une fois qu'elle a déjà circulé.

**Ce qui n'est jamais bridé :** le partage, et le nombre de Promi. Ce sont les
deux moteurs de la circulation ; les limiter reviendrait à payer pour freiner sa
propre croissance.

---

## 8. L'harmonie — ce qui revient partout

Ces éléments sont identiques sur tous les écrans. C'est ce qui fait qu'on
reconnaît Promi.

| Élément | La règle |
|---|---|
| **Le geste** | 118 px, deux points, un trait. Toujours entier. |
| **Peaufiner** | 62 px, en bas, même typographie, même filet. |
| **✕ FERMER** | Haut à droite, 50 px du haut, avec le texte. |
| **Promi** | Fraunces, haut à gauche, 20 px. |
| **« Moi »** | Premier de la liste, avec son avatar dégradé. |
| **Les boutons ronds** | Icône seule, jamais de texte. |
| **Le rythme** | Haut fixe · titre · corps qui respire · geste · Peaufiner |

---

## 9. La cible technique

Le prototype est un **fichier HTML unique** qui sert à la fois de maquette
vivante et de spécification. Il sera porté en **Swift + Firebase**.

Le CSS ne sera pas repris : c'est le rendu validé qui compte, pas la feuille qui
le produit.

Avec Firebase, chaque membre d'une Nuée plantera dans **son propre monde** — la
planche de dalles en haut d'une fiche de Nuée mélangera donc les univers
graphiques de tous les participants. C'est voulu.
