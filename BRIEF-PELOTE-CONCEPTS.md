# L'PELOTE — appel à concepts radicalement différents

*À coller tel quel dans un chat neuf. Ce document se suffit à lui-même.*

---

## 0 · CE QU'ON TE DEMANDE, ET COMMENT ON JUGERA

On construit l'**écran signature** d'une application mobile française. Il existe déjà en
plusieurs versions, aucune ne nous satisfait, et **on ne veut pas une variation de plus** :
on veut **quatre à cinq concepts radicalement différents**, chacun fondé sur un principe
propre.

**La règle qui gouverne tout ton travail :**

> **Si deux de tes propositions pouvaient coexister sur le même objet, ce sont des variantes.
> Recommence.** Chaque concept doit reposer sur un **principe organisateur différent** —
> une autre physique, une autre matière, une autre façon dont le temps ou la donnée
> s'inscrivent dans la forme. Pas une autre couleur, pas un autre effet.

**Auto-contrôle obligatoire, à faire avant de nous répondre :** écris en une phrase le
principe de chaque concept. Si deux phrases peuvent être vraies en même temps du même objet,
tu n'as qu'un seul concept.

**Ce qu'on ne veut pas :** un catalogue de dix idées avec une ligne chacune. Des « moodboards »
de références. Des mots-clés. Du growth hacking. Quatre concepts profonds valent mieux que
douze survolés.

---

## 1 · CE QU'EST PROMI, EN UN PARAGRAPHE

Une application pour **tenir sa parole**. On y « plante » des promesses — les **Promi**.
Chacune devient une **dalle colorée** sur une **Toile** personnelle, un pavage vivant qui est
le portrait de ce qu'on a dit et de ce qu'on a fait. **On tient sa parole par un geste tracé
au doigt**, jamais par une case à cocher : le doigt suit une courbe, et c'est ce geste qui
engage.

**Ce n'est pas une to-do list.** Toute décision qui en rapprocherait le produit est rejetée,
même si elle est pratique. Le produit doit provoquer une **émotion**, pas de l'efficacité.

**Vocabulaire invariable** — il encode le parti pris, et toute mécanique que tu proposes doit
pouvoir se dire dans ces mots-là :
```
Promi   une promesse, une dalle. Invariable : « trois Promi »
Toile   le canevas principal, un pavage vivant
Noyau   soi, au centre
Studio  le selecteur de monde graphique (huit mondes : encre, mosaique,
        touffe, braille, pixel, terrazzo, gravure, sillons)
planter / tenir / tracer
```
**Mots bannis, y compris en interne :** tâche, to-do, objectif, échéance, valider, urgent,
**score**, badge, série (streak), gamification. La récompense n'est **jamais** un chiffre :
c'est **la matière qui change**.

**Ton :** sobre, matériel, un peu artisanal. Jamais de mascotte, jamais d'exclamation.
Cadre de décision, dans cet ordre : **ÉVIDENT → SIMPLE → BEAU.**

---

## 2 · CE QU'EST L'PELOTE, ET CE QU'ELLE DOIT FAIRE

**L'Pelote est l'objet qui représente l'ensemble de mes paroles tenues.** Aujourd'hui une
sphère, mais **la forme n'est pas imposée** : c'est justement ce qu'on te demande de rouvrir.

Ce qu'elle doit porter :
- **le Noyau** au centre : soi ;
- **six entités** qui gravitent : les personnes à qui on a promis quelque chose. Leur
  proximité encode le **cumul** des paroles tenues avec elles. ⚠ **Rien ne recule jamais** :
  pas de compte à rebours, pas d'éloignement quand le temps passe ;
- **une dalle par Promi**, dans le **design et la couleur qu'il avait le jour de sa
  plantation** — ça s'ancre et ça ne rechange plus. D'où une **diversité** de designs sur le
  même objet.

**Rôle produit :** c'est l'écran qu'on montre. Il sera **partageable et payant** — une pelote
gratuite par défaut, les autres à 1 €. Il doit donc tenir **dans une image fixe**, rester
lisible à **200 px**, et donner envie de l'acheter.

---

## 3 · LES CRITÈRES, ET ILS NE SE NÉGOCIENT PAS

1. **L'ÉTAT NEUTRE DOIT ÊTRE MAGNIFIQUE.** C'est le test décisif. À **zéro Promi**, l'objet
   doit déjà être beau, désirable, partageable. Un objet qui n'est beau qu'à trente Promi est
   refusé : il est vendable dès le premier jour.
   ⚠ Corollaire dur : **tout principe qui PARTITIONNE est suspect.** Un pavage divise un tout —
   à une dalle c'est un objet uni, à trois un quartier d'orange. Il ne devient beau que vers
   vingt ou trente. Cherche des principes qui **ajoutent** au lieu de diviser.
2. **DONNE ENVIE DE TOUCHER.** On doit avoir envie de poser le doigt dessus, et d'y revenir.
   Si en le manipulant deux minutes on n'a pas envie de continuer, c'est raté.
3. **DOPAMINE SANS TOXICITÉ.** Ni score, ni série à ne pas briser, ni compte à rebours, ni
   culpabilité. La récompense est **matérielle et esthétique**. Dis-nous précisément par quel
   mécanisme ton concept donne envie de revenir **sans** ces béquilles.
4. **LA CROISSANCE SE VOIT.** On doit percevoir qu'un Promi s'est ajouté — d'un coup d'œil,
   sans légende. *« Un écran qui a besoin d'une légende est raté. »*
5. **UNE IMAGE FIXE DOIT SUFFIRE À LE VENDRE**, et il doit être encore plus beau en mouvement.
6. **IL DOIT ÊTRE À NOUS.** Pas un objet vu ailleurs. Si on peut le nommer d'une référence
   existante en trois mots, c'est perdu.

---

## 4 · LES CONTRAINTES TECHNIQUES, RÉELLES

```
rendu        canvas 2D (pas de WebGL, pas de moteur 3D, pas de shaders)
budget       60 images par seconde sur un ecran de 390 px de large
fond         encre tres sombre (#16171B). Il ne change pas.
palette      celle choisie par l'utilisateur au Studio (quatre couleurs)
mesure       on mesure tout : luminance moyenne, dispersion, cout par image
```
⚠ **Ces contraintes sont une ressource, pas une punition.** Un concept qui les prend au sérieux
sera souvent plus original qu'un concept qui les ignore. Si ton idée exige de les casser, dis
exactement laquelle et pourquoi ça les vaut.

---

## 5 · CE QUI A DÉJÀ ÉTÉ ESSAYÉ ET REFUSÉ — ne le repropose pas

```
six anneaux plats en cercle          « ennuyeux parce que plat »
trainees en arc degrade              « pas arty du tout, un CRM maquille »
le rejeu du temps, une timeline      « un ecran qui a besoin d'une legende est rate »
une image fixe qui ne bouge pas      ne vit pas assez
du liquide au centre                 prend la place du Noyau
gouttes, ondes, formes non convexes  « le contour exterieur est toujours tres laid »
squircle, ovoide, lentille, capsule  « boring, vu et revu »
une sphere de points nue             « on en a tous vu mille »
rendu lisse facon vitrail, avec
une tache speculaire                 « mega cheap », c'est du plastique
une majorite de cellules vides       la silhouette se creuse
quantifier la lumiere sur 7 marches  des bandes diagonales en travers
la Toile enroulee sur une sphere     un pavage n'est beau qu'a forte densite
```
**La fourrure** (une sphère couverte de centaines de milliers de poils peignés) a été explorée
très longuement. Elle n'est pas interdite, mais **si tu la reproposes il faut une raison
neuve**, pas une amélioration.

---

## 6 · CE QU'ON ATTEND, CONCEPT PAR CONCEPT

Pour **chacun** de tes 4 ou 5 concepts :

1. **LE PRINCIPE, EN UNE PHRASE.** Ce qui l'organise — pas ce à quoi il ressemble.
2. **POURQUOI IL EST BEAU À ZÉRO PROMI.** Décris précisément l'état neutre.
3. **CE QU'UN PROMI Y AJOUTE**, et à quoi ressemble l'objet à 1, à 5, à 30.
4. **CE QUE FAIT LE DOIGT.** Le geste, la réponse, et ce qui **reste** après — un objet qui
   garde la trace de la main donne envie d'y revenir.
5. **LE MÉCANISME DE DÉSIR**, nommé : par quoi ça accroche le cerveau, et pourquoi ce n'est
   pas une mécanique anxiogène.
6. **COMMENT ON LE DESSINE EN CANVAS 2D À 60 IMAGES/SECONDE.** Concrètement : quelles
   primitives, combien d'éléments, ce qui se précalcule. Une phrase d'algorithme vaut mieux
   qu'un adjectif.
7. **CE QUI PEUT LE FAIRE ÉCHOUER**, honnêtement.
8. **UNE DESCRIPTION VISUELLE ASSEZ PRÉCISE POUR ÊTRE DESSINÉE** — un développeur doit pouvoir
   en faire une planche sans t'appeler.

Et **pour terminer**, deux choses :
- **le classement**, du plus fort au plus faible, avec ton pari personnel et pourquoi ;
- **la proposition qu'on ne t'a pas demandée** : si tu penses que le problème est mal posé —
  que ce ne devrait pas être un objet, ou pas au centre, ou pas visuel — dis-le, avec ce que
  ça gagne et ce que ça coûte. On préfère une thèse tranchée à un panorama équilibré.

---

## 7 · LE NIVEAU ATTENDU

C'est **l'écran signature** d'un produit qui veut marquer. On vise le niveau d'un studio de
design premium : un objet dont les gens parlent, qu'ils montrent, et qu'ils achètent parce
qu'ils le trouvent beau. **Vise le remarquable, pas le correct.** Si l'une de tes idées te
paraît trop ambitieuse pour être faisable, propose-la quand même et dis ce qu'il faudrait.
