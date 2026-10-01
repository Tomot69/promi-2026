# Chantier 50 — rendre le contrôle du design déterministe

> À coller dans Claude Code. **Avant le lot 2.**
> Ce chantier ne change rien à l'écran. Il répare la porte de sortie.

---

Le lot 1 est validé. `redteam_geste` reste à 13/13, le trait est identique au
pixel sur sept propriétés, zéro débordement, `_tenirInit` intact. Et merci
d'avoir refusé de trancher seul trois fois — tu avais raison les trois fois, mes
documents étaient périmés.

**On ne lance pas le lot 2.** Avant, on répare le contrôle du design : il est non
déterministe et il sert de porte de sortie à tous les lots suivants.

**Ne relance pas `--figer`.** On figerait une troisième valeur au hasard.

---

## Ce que je sais de mon côté

Trois passages du même script sur un fichier inchangé : **0, puis 28, puis 12
écarts**. Et les écarts ne sont pas aléatoires, ils progressent — la largeur du
mot de nature passe de `82,01` → `87,08` → `93,80` px.

**Ton analyse est juste sur le mécanisme, mais la cause est plus large que les
polices manquantes.** Preuve : parmi les 28 écarts du lot zéro il y a
« **fermer** ». Or `.closeb` est en **Apfel**, embarqué en base64, sans réseau.
Il dérive quand même.

**Donc : le script mesure avant que les polices soient prêtes.** Les polices
embarquées se chargent elles aussi de façon asynchrone. C'est ça qu'il faut
corriger en premier.

Un aggravant s'ajoute par-dessus, à traiter **en second** :

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:...&display=swap">
```

L'app va chercher Fraunces sur le réseau — d'où ton
`⚠ ERREURS JAVASCRIPT : A network error occurred`.

---

## Ce que tu fais

### 1 · Prouve avant de corriger

Lance `releve-design.py` **cinq fois de suite**, donne-moi les cinq résultats.

Puis relance-le cinq fois avec `fonts.googleapis.com` bloqué côté Playwright
(`page.route`). Compare les deux séries.

Je veux la preuve chiffrée, pas l'hypothèse.

### 2 · Corrige `releve-design.py` — pas `app.html`

Avant **toute** mesure, dans chaque configuration :

```js
await document.fonts.ready
await document.fonts.load('600 40px "Fraunces"')
await document.fonts.load('italic 600 40px "Fraunces"')
await document.fonts.load('500 40px "ApfelMid"')
await document.fonts.load('400 40px "Apfel"')
await document.fonts.load('700 40px "Bricolage"')
```

puis un `requestAnimationFrame` avant de lire les largeurs.

### 3 · Le `<link>` — seulement si l'étape 1 le prouve

Vérifie d'abord toi-même : **quelles graisses de Fraunces sont réellement
utilisées** dans le CSS, et **lesquelles sont embarquées** en `@font-face` ?

Si tout ce qui est utilisé est déjà embarqué, le `<link>` est un vestige.
**Demande-moi avant de le retirer** — c'est une suppression dans `app.html`.

### 4 · Vérifie

- `releve-design.py` cinq fois → **le même résultat cinq fois**
- les sept batteries → aucune baisse
- `redteam_toile` cinq fois → dis-moi s'il s'est stabilisé (il oscille 14–16 sur
  le contrôle « Mes Promi : les intitulés restent », qui est aussi un test de
  largeur de texte : même cause probable)

### 5 · Corrige tes mémoires

Tu as enregistré que « le contrôle design ne peut pas être vert sur cette
machine ». Ce n'est pas vrai : il **peut** l'être, c'est le script qui mesure
trop tôt. Mets-les à jour quand le correctif est prouvé.

### 6 · Puis demande

Une fois stable et vert cinq fois de suite, demande-moi l'autorisation de
re-figer la référence. Pas avant.

---

## Ce que tu ne fais pas

- Aucun changement visuel.
- Ne touche pas au code de la Toile ni à `_tenirInit`.
- **Ne nettoie pas le CSS** — je confirme la règle de `CLAUDE.md`, elle a été
  payée cinq fois.
- Ne commence aucun lot.

---

## Ce que tu me livres

1. Les **cinq résultats avant** correction, puis les **cinq après**. Sortie telle
   quelle.
2. Les mêmes cinq avec le réseau bloqué.
3. Ce que tu as trouvé sur Fraunces : graisses utilisées contre graisses
   embarquées.
4. Les sept batteries avec le score attendu.
5. Ce que tu n'as pas réussi à faire.

Si après deux tentatives le contrôle reste instable, arrête-toi et explique-moi
ce qui coince. Une porte de sortie fiable vaut mieux qu'un lot de gagné.

---

## Trois choses que j'ai notées de ton compte rendu, pour plus tard

Ne les traite pas maintenant, je les ai inscrites dans `CHANTIERS.md` :

- **La palette des traits (150°)** — tu as raison, elle bloque la validation
  visuelle de toutes les fiches. C'est à moi de trancher, je m'en occupe.
- **La liaison phrase → formulaire par `dispatchEvent`**, qui casse en silence
  sans qu'aucune batterie l'attrape. C'est le chantier 56, à couvrir par un test
  avant tout lot qui touche la page +.
- **Le sélecteur `#createSheet>*:not(...)` de la ligne 9017** qui t'a coûté un
  tour : il est désormais documenté comme deuxième piège de spécificité du
  projet, à côté de celui de `#shareScreen`.
