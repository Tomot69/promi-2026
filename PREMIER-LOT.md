# Le premier lot — à coller dans Claude Code

> **À faire seulement après un lot zéro réussi.**
> Copiez tout ce qui suit la ligne.

---

## LOT 1 · La page + — l'en-tête et le trait

Un seul écran. Deux changements. Rien d'autre.

**Référence :** `PARCOURS.md § 2`

---

## Avant de commencer

**1. Sauvegarde le fichier :**

```bash
mkdir -p sauvegardes
cp app.html sauvegardes/app-avant-lot1.html
```

**2. Prends l'état de départ :**

```bash
python3 releve-design.py
```

Il doit afficher `✅ AUCUN ÉCART`. Sinon, **arrête-toi et dis-le-moi**.

**3. Capture l'écran avant modification** — la page +, en mode clair et en mode
sombre. Nomme-les `avant-clair.png` et `avant-sombre.png`.

Pour ouvrir la page + :

```javascript
document.getElementById('createBtn').click()
```

---

## Ce que tu fais — et rien d'autre

### A · Supprimer l'en-tête

L'écran affiche actuellement, en haut :

```
Nouveau
Promi
une parole donnée — elle devient une dalle
```

**Ces trois éléments disparaissent.** À leur place, il ne reste que :

- le mot-marque **« Promi »** en Fraunces 20 px, en haut à **gauche**,
  à 48 px du haut, à 22 px du bord
- **`✕ FERMER`** en haut à **droite**, à 50 px du haut, à 22 px du bord,
  taille 11 px, interlettrage `.14em`, opacité 78 %

C'est exactement le même en-tête que sur les fiches. **Reprends le composant
existant, n'en crée pas un second.**

La phrase de création remonte donc et gagne de la place.

### B · Remplacer le bouton par le trait

L'écran affiche en bas un bouton **« PLANTER LE PROMI »**.

**Il est remplacé par le trait** — le même composant que sur les fiches :

- hauteur **118 px**
- deux points : un plein à gauche, un en contour à droite
- libellé **`glisse pour planter →`**, 13 px, graisse 800, centré, à 14 px du bas
- rayon **26 px**, fond `rgba(255,255,255,.12)`
- précédé de **24 px** d'espace

**Réutilise le composant existant `#tenirZone`.** Ne crée pas une seconde
implémentation : c'est la règle la plus importante de `CLAUDE.md § 5`.

Le bouton reste accessible par la bascule « bouton », comme sur les fiches.

---

## Ce que tu ne fais PAS

- Ne touche à **aucun autre écran**
- Ne touche **pas** au code de la Toile
- Ne change **pas** les trois cartes de nature (Promi / Nuée / Brouillon) —
  c'est le lot 2
- Ne change **pas** la palette des traits — question ouverte, `DECISIONS.md § E1`
- Ne nettoie **pas** le CSS
- N'invente **rien** qui ne soit pas décrit ci-dessus

---

## La méthode

- **Lis le code avant de le modifier.** Ne devine pas.
- `assert S.count(old) == 1` avant chaque remplacement.
- **N'écris que dans le dernier bloc `<style>`**, en fin de fichier.
  Ne modifie aucune règle antérieure.
- Vérifie qu'une règle s'applique **réellement** : le fichier contient
  2 400 règles dont beaucoup se contredisent. Une déclaration peut être écrasée
  sans que ce soit visible.
- **Tu patches, tu ne réécris pas.** Une valeur qui paraît étrange l'est pour une
  raison.

---

## Ce que tu me livres

**1. Les captures avant / après**, côte à côte, en mode clair **et** en mode
sombre — quatre images.

**2. Le contrôle du design :**

```bash
python3 releve-design.py
```

Colle la sortie telle quelle.

Les **seuls** écarts acceptables concernent l'en-tête supprimé et le bouton
remplacé par le trait. **Tout autre écart est une régression** — corrige-la avant
de livrer.

**3. Les sept batteries**, dans un tableau avec le score attendu.

**4. Trois mesures**, prises dans le navigateur :

| Quoi | Comment |
|---|---|
| hauteur du trait | `document.getElementById('tenirZone').getBoundingClientRect().height` |
| position du ✕ | `document.querySelector('#createSheet .closeb').getBoundingClientRect()` |
| débordements | compter les éléments dont `right > cadre.right + 2` |

**5. Ce que tu n'as pas réussi à faire**, explicitement.

---

## Les règles d'arrêt

**Ne livre pas** si une batterie a baissé. Dis-le et explique pourquoi.

**Ne livre pas** si `releve-design.py` signale un écart que ce lot ne demandait
pas.

**Ne livre pas** si le résultat ne correspond pas à ce qui est décrit. Une
livraison fausse coûte plus cher qu'un tour perdu.

**Si tu bloques après deux tentatives**, arrête-toi, restaure la sauvegarde et
explique-moi ce qui coince.

---

Quand c'est fait, attends ma validation avant tout lot suivant.
