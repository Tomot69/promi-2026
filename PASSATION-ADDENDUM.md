# Addendum à la passation — état au 16 août 2026

À ranger dans `Promi 2026`, à côté de `PASSATION.md` et `CHANTIERS.md`.
**Remplace la version du 16 août 09h**, qui reprenait des faits du 11 août
périmés depuis. Ce qui suit est à jour.

---

## 0 · Trois faits datés — ne pas les rouvrir

Le PDF `convpromi8` date du **11 août au matin**. Cinq jours de travail ont
suivi. Trois points y semblent contradictoires avec la passation : ils ne le
sont pas, c'est une chronologie.

| | Le 11 août | Depuis |
|---|---|---|
| **Panneau du geste** | 164 px, arbitré au lot 1 | **131 px** — soit 118 × 1,108. Le 164 venait de la page + copiant la fiche ; `releve-moodboard.py` l'a corrigé. **Le 164 est mort.** Et la question tombe avec le moodboard H : le panneau n'y est plus une boîte à mesurer, c'est l'horizon. |
| **Batteries** | 142/142 | **144/144** — `phrase`, `verbe` et `filets` ont été ajoutés. |
| **Référence figée** | ✅ aucun écart | Ce figeage est **antérieur à l'homothétie**. Les ~390 écarts sont apparus quand on a appliqué le 1,108. Les deux états sont vrais, à cinq jours d'écart. |
| **Vérification du lot 1** | non faite | **Faite le 11 août.** `redteam_geste` 13/13 deux fois. `releve-design` 12 écarts, tous sur le mot de nature en Fraunces — cause : polices chargées de façon asynchrone. Corrigé : c'était le **chantier 50**. **Lot 1 validé.** |

---

## 1 · `promi-moodboard-H.html` — la référence

**28 écrans · 8 sections · 390 × 844 · 1 024 styles inline · direction
« L'Horizon composé ».** Livré, présent dans le Projet.

**Aucune homothétie.** Il est dessiné à la bonne échelle. **Le facteur 1,108 ne
s'y applique pas.**

**Sa loi remplace nos règles éparses :**

> Le champ dit la **nature**. La ligne dit l'**état**. La hauteur de l'horizon
> dit la **promesse** — fixe, la même de la fiche à la carte d'Index au bandeau
> du Fil.

**Le trait n'est pas posé sur la fiche : il est la frontière du bitonal.**
Une moitié manquante **aplatit l'horizon et le pointille** — une parole
suspendue se voit à la forme de l'écran, avant qu'on ait lu un mot.

**Le chantier 55 est fermé.** La palette des traits n'est plus une question
ouverte : la ligne porte la couleur d'état, jamais grise, jamais neutre, et
**c'est la seule ligne de l'app**.

**Reste à trancher — Tom, en regardant les 28 écrans :** le moodboard H
remplace-t-il `MOODBOARD-parcours.html`, ou les deux coexistent-ils ?

### Deux pièges quand on l'apprendra à `releve-moodboard.py`

1. **L'exclusion « %-dérivés d'une valeur absolue, base 352 ↔ 390 » devient
   fausse pour ce fichier.** Laissée en place, elle masquerait de vrais écarts —
   exactement le mécanisme qui a caché l'erreur d'homothétie pendant des jours.
   L'outil doit connaître **deux bases**, pas une.
2. **Il demande des graisses non embarquées :** Bricolage **500** (86
   occurrences) et **800** (112). Embarquées : 600/700. Hanken Grotesk y remplace
   Apfel — doublure de fichier, normale. **Le chantier polices est plus lourd que
   les 12 couples d'`AUDIT-POLICES.md`.**

### Trois questions laissées par le chat de design, jamais arbitrées

- **« Trace ta moitié »** comme verbe d'action principal, à la place de « Tenir »
- L'état **Chiche refusé** — quand la personne défiée ne répond pas
- Le contraste **en cours / brouillon** dans les mondes pâles

---

## 2 · Le code mort — mesuré, jamais écrit

Sur la v592 : **36 handlers orphelins** (contre 26) et **317 classes CSS mortes**
(contre 161). **Le code mort a doublé.**

Rien ne plante. **Le risque est ailleurs :** Claude Code lit `app.html` à chaque
lot et croit que ces fonctionnalités existent.

**Ce n'est pas une autorisation de nettoyer** — l'interdiction reste absolue. La
parade est une **liste noire nommée dans `CLAUDE.md`** : les identifiants morts
connus, à ne jamais rebrancher ni prendre pour une fonctionnalité.

## 3 · `ETAT-DES-LIEUX.md` — toujours manquant

Réclamé deux fois le 11 août, jamais fourni. L'addendum v6 décrit fidèlement la
**v467** ; l'app est à la **v592**. **~125 versions ne vivent que dans ce
fichier.** Ce n'est pas « fusionner deux documents » (chantier 49), c'est leur
seule trace.

## 4 · Les lots — nommer par le contenu

Deux numérotations coexistent : celle du chat de dev (lot zéro, lot 1 = les
fiches) et celle de la passation (lots 1→4 = la suite Chiche). **Toute consigne
nomme le lot par son contenu, jamais par son numéro seul.**
