# PROMI — brief pour une étude psycho / design

*À coller tel quel dans un chat neuf. Ce document se suffit à lui-même :
le chat qui le lit ne connaît rien au projet.*

---

## 0 · CE QU'ON TE DEMANDE, ET COMMENT ON JUGERA TA RÉPONSE

On construit une application mobile française qui existe déjà, dont le design est le
fruit de plusieurs centaines d'itérations, et dont **l'écran signature n'est pas encore
au niveau**. On veut une **étude pointue** — pas un catalogue de biais cognitifs.

**Ce qu'on attend :**

1. **Les mécanismes psychologiques qui font qu'on TIENT SA PAROLE** — engagement,
   cohérence, identité, coût irrécupérable, témoin social, aversion à la perte.
   Lesquels sont robustes ? Lesquels sont surestimés ? Que dit la réplication ?
2. **Ce qui fait qu'un objet numérique devient un OBJET AUQUEL ON TIENT** — possession,
   effet de dotation, soin, matérialité perçue, « pet mechanics » (Tamagotchi, Pou,
   Neko Atsume), collections, jardins. Pourquoi certains marchent des années et d'autres
   deux semaines ?
3. **La ligne rouge.** Notre produit refuse les mécaniques d'anxiété : pas de série à ne
   pas briser sous peine de perdre, pas de compte à rebours culpabilisant, pas de score.
   **Où passe la frontière entre « fidélisant » et « toxique » ?** Donne-nous des critères
   opérationnels, pas des principes.
4. **Ce qui rend une image virale sans être vulgaire.** L'écran signature doit être
   partagé spontanément. Qu'est-ce qui déclenche le partage d'un objet visuel personnel ?
5. **Le contre-argument.** Dis-nous ce qui, dans notre parti pris, est probablement faux.

**Ce qu'on ne veut pas :** une liste de biais avec une phrase chacun. Des « gamification
best practices ». Du growth hacking. Des recommandations qui marcheraient pour n'importe
quelle app.

**Le ton attendu :** on préfère une thèse tranchée et argumentée à un panorama équilibré.
Cite ce qui est solide, signale ce qui est fragile.

---

## 1 · CE QU'EST PROMI

Une application mobile pour **tenir sa parole**.

On y « plante » des promesses — les **Promi**. Chacune devient une **dalle colorée** sur
une **Toile** personnelle, un pavage vivant qui est le portrait de ce qu'on a dit et de
ce qu'on a fait. **On tient sa parole par un geste tracé au doigt**, jamais par une case
à cocher : le doigt suit une courbe, et c'est ce geste qui engage.

**Ce n'est pas une to-do list.** Toute décision qui rapprocherait le produit d'un
gestionnaire de tâches est rejetée, même si elle est fonctionnellement pratique. Le
produit doit provoquer une **émotion**, pas de l'efficacité.

**Public :** grand public, usage social et affectif. Français d'abord.

### Le vocabulaire — il est invariable et il porte le produit
```
Promi       une promesse, une dalle. Invariable : « trois Promi »
dalle       la forme coloree d'un Promi sur la Toile
Toile       le canevas principal, un pavage de Voronoi vivant
Nuee        un collectif de Promi (un groupe, un projet)
Fil         le flux d'activite
Aura        l'ecran de progression
Studio      le selecteur de monde graphique
Le Cercle   l'abonnement payant
Peaufiner   le tiroir de reglages
planter     creer un Promi
tenir       honorer sa parole
```

**Mots bannis, y compris en interne :** « tâche », « to-do », « objectif », « échéance »,
« valider », « urgent », « score », « brouillon ». On dit **tenir sa parole**, **tracer**,
**planter**, **lancer**. Un brouillon est un **gardé de côté**.

⚠ **Ce lexique n'est pas cosmétique.** Il encode le parti pris : on ne gère pas des
tâches, on tient une parole. Si ton étude propose une mécanique, elle doit pouvoir se
dire dans ces mots-là.

---

## 2 · LA DIRECTION ARTISTIQUE

### Le cadre de décision, dans cet ordre
**ÉVIDENT → SIMPLE → BEAU.** Le test après chaque écran : *quelqu'un qui ne connaît pas
l'app comprend-il en une seconde ce qu'il doit faire ?* Si non, ce n'est pas fini, même
si c'est beau.

### Une règle qui gouverne tout
**Un élément coloré ne reste que s'il porte du SENS ou une ACTION.** S'il décore, il
dégage — même s'il est joli. Un seul trait coloré qui sert vaut mieux que cinq qui bruitent.

### Les couleurs signal — la nature de la chose regardée
```
bleu        #3A54FF   un Promi
framboise   #FA2258   un Chiche (un defi lance a quelqu'un)
mauve       #8A5CF0   une Nuee
terracotta  #F07A2E   a tenir
menthe      #2BE88C   tenu
creme       #F4EEE1   surface claire
encre       #16171B   surface sombre
```
**La couleur dit la NATURE, jamais l'état.** L'état vit dans le trait. Exception unique,
et elle dure une seconde : à l'instant où une parole est tenue, tout l'écran passe au
menthe, la dalle se recompose plus grande, puis revient.

### La typographie
```
Bricolage Grotesque   titres, libelles      700/800
Apfel                 champs, interface
Fraunces              la signature « Promi »
```
Rien sous 12 px. Aucune opacité sous 72 % sur du texte lisible.

### Les huit mondes graphiques
Chaque utilisateur choisit un **monde** au Studio : il change le dessin de toutes ses
dalles. `Encre` (des lobes organiques) · `Mosaïque` (des carreaux) · `Touffe` (des fleurs
dessinées à la main) · `Braille` (une grille de pois) · `Pixel` (des aplats à bord
d'escalier) · `Terrazzo` (des éclats) · `Gravure` (des hachures) · `Sillons` (des ondes).
Trois sont réservés aux abonnés.

### Le ton
Sobre, matériel, un peu artisanal. **Jamais** de vocabulaire de productivité, jamais de
mascotte, jamais d'exclamation. La récompense n'est pas un badge : c'est **la matière qui
change**.

---

## 3 · L'ÉCRAN SIGNATURE — L'PELOTE

C'est celui sur lequel on travaille, et c'est le sujet de l'étude.

**L'Pelote, c'est la Toile de l'utilisateur, fermée sur elle-même : une sphère.**
Techniquement, le moteur peint la vraie Toile en une fois et on l'enroule sur la boule —
mêmes dalles, mêmes contours, mêmes espaces. La surface est **duveteuse** : des centaines
de milliers de touffes de poils, peignées, qui se couchent sous le doigt et se relèvent.

- au centre, le **Noyau** : soi ;
- autour, six disques qui gravitent — les personnes à qui on a promis quelque chose. Le
  rayon de chacun dit la date de sa dernière parole tenue ;
- la matière se raréfie au centre pour leur laisser la place ;
- **quand on la touche, elle cède comme une vraie matière.**

**Intention produit :** c'est un objet dont on doit avoir envie de s'occuper. Il sera
**partageable et payant** — une pelote gratuite par défaut, les autres à 1 €, incluses
dans l'abonnement. Il doit donc tenir dans une image, rester lisible à 200 px, et donner
envie de l'acheter.

**Le critère, non négociable :** si en la manipulant deux minutes on n'a pas envie de
continuer, ce n'est pas fini.

**L'état honnête aujourd'hui :** le dessin est juste — c'est vraiment la Toile de
l'utilisateur, vérifié au pixel. **Mais la boule vit à 13 % de luminance** (moyenne 32 sur
255) : elle est belle et elle est sombre, et à ce niveau d'obscurité aucune subtilité de
lumière ne se lit. **On est à un carrefour de direction artistique, et c'est pour ça qu'on
demande cette étude.**

---

## 4 · LES QUESTIONS PRÉCISES

1. **L'engagement par le geste.** On fait tracer une courbe au doigt au lieu de cocher.
   Est-ce que l'effort physique d'un geste renforce réellement l'engagement, ou est-ce
   une croyance de designer ? Que dit la littérature sur l'engagement incarné, la
   signature manuscrite, le coût d'action ?

2. **L'objet dont on prend soin.** La boule est le portrait de nos paroles tenues. Quels
   mécanismes font qu'on s'attache à un objet numérique qu'on a fabriqué soi-même ?
   Où est la limite entre l'attachement et la corvée ?

3. **La récompense.** On refuse points, badges, séries. Notre récompense est
   **matérielle** : la boule devient plus dense, plus lumineuse, plus belle. Est-ce
   suffisant pour créer un retour régulier ? Que sait-on des récompenses esthétiques
   contre les récompenses chiffrées ?

4. **Le social.** Une promesse est faite à quelqu'un ; les six disques sont des personnes.
   Quelle est la bonne dose de témoin social avant que ça devienne de la pression ?

5. **Le partage.** Qu'est-ce qui fait qu'on partage spontanément une image générée à
   partir de ses propres données ? Qu'est-ce qui fait qu'on ne le fait pas ?

6. **La monétisation.** Vendre une skin d'un objet personnel à 1 € : que sait-on de la
   disposition à payer pour de la personnalisation esthétique, hors jeux vidéo ?

7. **La lumière et la couleur.** Notre écran signature est sombre — c'est un choix de
   sobriété. Que dit-on de l'effet d'un fond sombre sur la perception de valeur, de
   technicité, de préciosité ? Un objet lumineux se partage-t-il davantage ?

8. **Et ce qu'on ne voit pas.** Quel est le risque principal de ce parti pris, du point
   de vue du comportement ?

---

## 5 · L'AMBITION

On ne veut pas une app de plus. On veut un objet dont les gens parlent, qu'ils montrent,
et qui change un peu la façon dont on se tient à sa parole. **L'Pelote doit être un
chef-d'œuvre graphique**, au même titre que la Toile — l'écran qu'on montre, celui qui
donne envie d'y revenir et d'y jouer.

Si ton étude conclut qu'il faut **changer** le parti pris plutôt que le parfaire, dis-le
franchement, avec ce que ça gagne et ce que ça coûte.
