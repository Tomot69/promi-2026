# Audit des polices — toute l'app

> Relevé mesuré dans le navigateur : chaque couple **police / graisse / style**
> demandé en CSS, croisé avec les faces réellement embarquées en `@font-face`.
> **Lecture seule, aucune correction.** Pour un lot dédié — 370 éléments, tous
> les écrans. Le prototype est la spécification du portage Swift : en Swift, une
> graisse absente **casse**, elle ne se substitue pas en silence.

Généré le 12 août 2026 (sonde `audit_fonts.py`).

---

## Faces réellement embarquées

| Police | Graisses · styles |
|---|---|
| **Fraunces** | 600 normal · 600 italique |
| **Bricolage** | 600 · 700 (normal) |
| **Apfel** | 400 (normal) |
| **ApfelMid** | 500 (normal) |

**17 couples distincts sont demandés en CSS : 5 existent, 12 manquent.**

---

## Les 12 couples ABSENTS des `@font-face` — casseraient en Swift

Triés par nombre d'éléments. Rendu navigateur = substitution silencieuse (graisse
la plus proche, ou oblique synthétique). Swift = rupture.

| Police \| graisse \| style | Éléments | Écrans (nb d'éléments) |
|---|---|---|
| **Apfel \| 600 \| normal** | 106 | Index(31) · Fil(24) · fiche(18) · Onboarding(15) · global(12) · Aura(4) · Studio(2) |
| **ApfelMid \| 400 \| normal** | 65 | Partager(65) |
| **Bricolage \| 800 \| normal** | 37 | fiche(21) · Fil(11) · Index(2) · Réglages(2) · global(1) |
| **Apfel \| 800 \| normal** | 28 | Fil(24) · page +(3) · fiche(1) |
| **Apfel \| 700 \| normal** | 27 | global(15) · Fil(8) · fiche(2) · Toile(2) |
| **ApfelMid \| 600 \| normal** | 27 | page +(12) · Fil(9) · Partager(5) · Aura(1) |
| **Apfel \| 500 \| normal** | 22 | global(11) · puis Partager · Fil · page + · Index · Arranger · fiche · cellule · Aura · Réglages · Studio (1 chacun) |
| **Apfel \| 400 \| italique** | 19 | Aura(7) · Arranger(6) · global(3) · Toile(1) · cellule(1) · Studio(1) |
| **ApfelMid \| 700 \| normal** | 18 | Réglages(12) · Fil(6) |
| **ApfelMid \| 500 \| italique** | 16 | Studio(8) · global(4) · Réglages(4) |
| **Fraunces \| 700 \| normal** | 4 | Partager(2) · global(2) |
| **Apfel \| 600 \| italique** | 3 | global(3) |

**12 couples · ~370 éléments · tous les écrans touchés.**

---

## Les 5 couples qui EXISTENT (rien à faire)

| Police \| graisse \| style | Éléments |
|---|---|
| Apfel \| 400 \| normal | 821 |
| ApfelMid \| 500 \| normal | 101 |
| Bricolage \| 700 \| normal | 84 |
| Bricolage \| 600 \| normal | 14 |
| Fraunces \| 600 \| normal | 5 |

---

## Lecture

- **Apfel est le plus atteint** : demandé en 500/600/700/800 **et** en italique,
  alors qu'**une seule face existe (400 normal)**. À lui seul, 7 des 12 couples
  manquants.
- **Les italiques sont le pire cas** : Apfel et ApfelMid **n'ont aucune italique
  embarquée** → 3 couples (`Apfel 400 it`, `ApfelMid 500 it`, `Apfel 600 it`) sont
  de l'**oblique synthétique**, inexistante en Swift.
- **Bricolage 800** (37 éléments, surtout les **titres de fiche**) : rend en 700
  au navigateur, **absent** en Swift.
- **Fraunces 700** (4, Partager) : Fraunces n'existe qu'en 600.

## Méthode de correction (pour le lot dédié)

Deux voies par couple manquant, à trancher écran par écran : soit **embarquer la
face** (agrandit le fichier), soit **ramener la demande CSS à une graisse existante**
(change le rendu). Ne rien décider ici. Ne pas nettoyer le CSS pour autant
(cf. `CLAUDE.md §9`). Le relevé ci-dessus donne l'ampleur par écran pour découper.
