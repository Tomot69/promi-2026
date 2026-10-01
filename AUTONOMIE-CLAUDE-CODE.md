# Faire itérer Claude Code seul jusqu'au bout

**Version 2 — après l'arrivée de `PROMI-SPECIFICATIONS.md`.** Remplace la v1,
dont le critère d'arrêt supposait une carte de correspondance devenue inutile.

---

## 1 · Ce qui change

La v1 demandait d'apprendre à un outil quel nœud du moodboard correspond à quel
élément de l'app. **Ce détour n'existe plus.**

`PROMI-SPECIFICATIONS.md` donne, pour chacun des 128 écrans, **les coordonnées
absolues et le style complet de chaque élément**. On compare donc l'app
directement aux chiffres du document. Plus de mapping, plus de DOM à parcourir.

**Le document est la spécification. Le moodboard est l'image de contrôle.**
En cas de doute, le document tranche — il est généré depuis le code qui a dessiné
le moodboard.

---

## 2 · Le critère d'arrêt

Une section est finie quand **les cinq lignes sont vraies en même temps** :

```
écarts de position > 3 px         0
écarts de style (police, taille, couleur)   0
collisions de blocs               0   (sauf l'encart du Cercle)
éléments au-delà de y = 844       0
batteries redteam                 au vert
```

**Tant que les cinq ne sont pas vraies, il continue. Il ne demande rien.**

Les six contrôles de la partie 7 du document sont le minimum ; ils ne remplacent
pas la comparaison écran par écran.

---

## 3 · Les cinq garde-fous

**Une sauvegarde par section**, avant d'y toucher.

**La règle des trois essais.** Un écart qui ne descend pas après trois
tentatives : il note la cause dans `QUESTIONS.md` et il passe. Sous 3 px avec une
cause identifiée : il note et il passe tout de suite.

**`QUESTIONS.md` remplace l'arrêt.** Devant une ambiguïté : il écrit la question,
prend l'option la plus conservatrice, **et continue**. Il ne s'arrête pas, et il
ne décide pas en silence.

**Interdiction de trancher un point de produit.** Un mot, une formulation, une
fonction ajoutée ou retirée : jamais. Le document contient déjà presque tous les
mots ; s'il n'y est pas, il note.

**Une régression compte double.** Une batterie verte qui passe au rouge :
arrêt immédiat. Un flake connu se reconfirme en relançant.

---

## 4 · L'ordre des sections

| | Section | Écrans | Pourquoi ici |
|---|---|---|---|
| **1** | **Les fiches** | 22 | le trait et le bandeau s'y vérifient ; tout en dépend |
| **2** | **Peaufiner** | 18 | partagé page + / fiche, il hérite des deux |
| **3** | **La page +** | 34 | le plus gros volume |
| **4** | **Index et Fil** | 6 + 26 composants | reprennent la hauteur de trait des fiches |
| **5** | **L'instant** | 6 | dépend de tout le reste |

**Cinq livraisons. Tom regarde cinq fois, pas cent vingt-huit.**

---

## 5 · La consigne d'ouverture

> **Tu travailles seul jusqu'au bout d'une section. Tu ne me demandes rien.**
>
> **Ta spécification : `PROMI-SPECIFICATIONS.md`.** Il donne les coordonnées
> absolues et le style de chaque élément des 128 écrans. Tu ne devines aucune
> valeur : tu la lis. `promi-moodboard-H.html` est l'image de contrôle, à ouvrir
> dans un second onglet.
>
> **390 px, aucune homothétie.** Le facteur 1,108 ne s'applique nulle part ici.
> Tu ne dépasses jamais une valeur du document, même si elle te paraît petite.
> Une mesure prise sur l'app constate un état, elle ne le valide jamais.
>
> **Une section est finie quand :** 0 écart de position au-delà de 3 px · 0 écart
> de style · 0 collision · 0 débordement · batteries au vert. Tant que ce n'est
> pas vrai, tu continues.
>
> **Ce que tu ne fais jamais :** nettoyer le CSS — bloc neuf en fin de fichier,
> jamais une règle existante · réécrire un écran « proprement », on patche ·
> toucher au moteur de la Toile · trancher un point de produit.
>
> **Devant une ambiguïté :** tu l'écris dans `QUESTIONS.md`, tu prends l'option la
> plus conservatrice, **et tu continues**.
>
> **Trois essais** puis tu notes et tu passes. **Sauvegarde avant chaque
> section.** **Une batterie verte qui rougit = arrêt immédiat**, sauf flake connu
> reconfirmé en relançant.
>
> **Sers-toi du navigateur.** Playwright lit des données, il ne voit pas qu'un
> écran est cassé. Ouvre, navigue, regarde. **Ne livre pas un écran que tu juges
> raté** — *est-ce que ça donne envie ? est-ce que quelqu'un comprend en une
> seconde ?*
>
> **À la fin d'une section :** les cinq lignes du critère, une capture de chaque
> écran dans les deux thèmes, `QUESTIONS.md`. Puis tu passes à la section
> suivante sans attendre de réponse.

---

## 6 · Ce que Tom regarde, à chaque livraison

1. **Les cinq lignes du critère** — trente secondes
2. **`QUESTIONS.md`** — c'est là que se cache ce qui a été décidé sans lui
3. **Les captures** — et seulement ça, pas les comptes rendus

**Si `QUESTIONS.md` est vide sur une section entière, se méfier.** Un exécutant
qui n'a aucune question sur vingt écrans n'a pas regardé.
