# État des lieux — v592

> Écrit sans complaisance. Ce qui n'est pas beau à dire est dit.

---

## 1. Ce qui est terminé et validé

| Écran | État | Notes |
|---|---|---|
| **La Toile** | ✅ solide | Voronoï pondéré, pincement rétabli en v580. **Ne pas y toucher.** |
| **L'Index** | ✅ | Lignes colorées par état, vraies dalles à droite, tri fonctionnel |
| **Le Fil** | ✅ | Même grammaire que l'Index |
| **L'Aura** | ✅ | Disques de progression, courbe d'évolution |
| **Le geste de tenir** | ✅ | Trait courbe, part du rond, trace conservée et redessinée |
| **L'onboarding** | ✅ | Réparé, mode clair, rejouable depuis les Réglages |
| **Le mode signature** | ✅ | Bricolage ↔ Fraunces au toucher du titre |
| **La page de personne** | ✅ | Fond corrigé en v579 |

**Sept batteries de tests, 233 contrôles**, toutes vertes en v592.

---

## 2. Ce qui est à moitié fait

### La page + — la phrase (lots 1→4, Version B)

**Fait :** refondue sur `MOODBOARD-parcours.html`. Fond **plein coloré** par
nature (bleu Promi, mauve Nuée, `#B8552B` brouillon), texte clair, titre-question,
**trois cartes empilées** à dalles entières, pastilles blanches, ligne d'aide
« touche … pour inverser le sens », panneau translucide + geste (rond crème,
pastille « bouton »), **barre Peaufiner** en bas. Habillage dans un seul bloc
`<style id="lot4-moodboard">` + `<script id="lot4-peaufiner-bottom">` en fin de
body. **Version B verrouillée** (un écran qui glisse — voir `PARCOURS.md §2`).

> **Découverte (lot 4) — la page + était conçue pour un fond coloré dès l'origine.**
> Le CSS d'origine (l.2220-2224) porte tout un design **sombre/coloré** pour
> `#createSheet` : texte crème `#F3EFE6`, champs blancs translucides, chips bleu,
> gradients nav(dark) / gradients colorés par `data-kind`. **Un lot ancien l'a
> forcée en crème** — le bloc « plus-rebuild » (`#createSheet{background:var(--surf)!important}`,
> l.9051, « PAGE + reconstruite sur la DA Index ») + un `setProperty('background','var(--surf)')`
> à l'ouverture. Le lot 4 n'a pas eu à tout réinventer : il a **levé ce forçage**
> et rétabli le fond coloré natif. Leçon : avant de rebâtir un écran, vérifier
> s'il n'existe pas déjà un design d'origine masqué par un override postérieur.

**Reste (lot 5) :** la grappe de dalles en tête, le glissement encre→couleur au
choix, la teinte des dalles de cartes.

**Risque :** la phrase pilote le formulaire par `dispatchEvent`. Si un champ
change de nom ou de comportement, la liaison casse **en silence** (filet :
`redteam_phrase.py`). À vérifier après chaque modification du formulaire.

### La fiche d'un Promi

**Fait :** structure en blocs, dalle au premier plan, trois tons, geste,
Peaufiner en bas avec le partage.

**Pas fait :**
- **« répondre… » sous le dernier commentaire** — le moodboard le prévoit comme
  une ligne dans la carte. Actuellement les commentaires sont dans Peaufiner.
- Le titre long ne réduit pas sa taille (prévu 34 → 26 px).

### La fiche d'une Nuée

**Fait :** planche de dalles opaques, en-tête avec nom et compte, fil des Promi
aux couleurs d'état avec dalles, teinte suivant la dernière dalle plantée,
partage.

**Pas fait :**
- Les membres ne sont pas des jetons avec avatar (prévu au moodboard).
- Pas d'écran de création de Nuée à la grammaire de la phrase.

### Le brouillon

**Quasi rien.** Le bloc « Ce brouillon deviendra » existe avec trois options,
mais :
- Pas de liseré pointillé terracotta
- Pas de pastille `BROUILLON`
- Pas de choix de nature pré-coché
- L'écran n'a pas été repris depuis le moodboard

### Les Réglages

**Fait :** la dalle en trame de fond, le ✕ repositionné.

**Pas fait :** l'écran entier n'a pas été repensé. C'est un empilement de lignes
qui fonctionne mais ne porte aucune identité.

---

## 3. Ce qui est cassé ou douteux

| Problème | Gravité | Détail |
|---|---|---|
| **La palette des traits** | ⚠ moyenne | Le décalage de 150° sort parfois de l'harmonie du monde choisi. L'utilisateur l'a signalé deux fois. **Décision attendue.** |
| **`redteam_toile.py`** | ⚠ faible | Oscille **14–16/16** sur le sous-contrôle « Mes Promi : les intitulés restent ». **Cause établie (Chantier 50) : les dalles respirent** — `Renc(now,…)` (app.html l.6961) anime leur forme avec `performance.now()`, sans aucun aléa, et la toile de partage est peinte **une fois** → le compte de pixels clairs dépend de la phase de respiration au snapshot (spectre continu 178→1350, figé par run, insensible à l'attente). **Convention : 15/16 = succès ; 14 ou moins = on regarde.** Seuil, Toile et app.html **intacts**. **Chantier futur :** réécrire ce contrôle — comparer une dalle à sa propre référence plutôt que compter des pixels clairs (ce test mesure la mauvaise chose : une dalle qui respire *doit* varier). Pas maintenant. |
| **Le scroll sous Peaufiner** | ⚠ moyenne | Le contenu passe **sous** la barre collante quand la fiche dépasse l'écran. C'est le comportement normal de `sticky`, mais l'utilisateur le trouve gênant. Trois approches tentées, toutes cassent l'en-tête. |
| **Le tap sur une dalle de la Toile** | ❓ à vérifier | Mes tests automatisés n'arrivent pas à ouvrir une fiche en tapant sur la Toile. Vérifié : c'était déjà le cas avant mes corrections. **Peut être une limite du test, pas un bug.** À confirmer sur appareil réel. |
| **Glyphe polygone de la fiche Nuée** | ⚠ latente | `_peintGlypheNuee` (app.html l.8800) peint un **polygone 7 points reconstruit**, couleur figée `#E4CEFD`, ombre portée + 4 cercles blancs, dans `#dForm` — appelé par `renderNueeDetail`. **Invisible aujourd'hui** : en `dp-mode-nuee` le parent `.mg-head` est `display:none` (rect 0×0, hors viewport). Donc **pas une violation visible**, mais du **code mort qui contredit « jamais de polygone reconstruit »**. **À supprimer le jour où on refait la fiche Nuée** (voir CHANTIERS #34) — pas maintenant (CLAUDE.md interdit de nettoyer). |

---

## 4. La dette technique — le point le plus grave

### Les chiffres

```
fichier              1 535 Ko
règles CSS           2 400
dont mortes          54 %
!important           2 415
blocs <style>        24
blocs <script>       33
```

### Le problème

Le dernier bloc `<style>` fait **116 Ko et contient environ 70 sections**
ajoutées au fil des tours, dont beaucoup se contredisent. Certaines propriétés
sont déclarées **jusqu'à dix fois** sur le même sélecteur.

Conséquence directe : **une modification peut ne rien changer visuellement** si
une règle postérieure l'écrase. C'est arrivé de nombreuses fois et c'est la
première cause de perte de temps.

### Cinq tentatives de nettoyage, cinq échecs

| Méthode | Gain | Écarts mesurés |
|---|---|---|
| Déduplication des propriétés (dernier bloc) | 127 → 116 Ko | **0** ✅ appliquée |
| Compactage de tous les blocs | 582 → 454 Ko | 67 ❌ |
| Suppression des règles mortes (relevé DOM) | 42 % | 554 ❌ |
| Suppression par analyse statique | 16 % | 4 351 ❌ |
| Fusion des sélecteurs identiques | 116 → 113 Ko | 814 ❌ |
| Retrait des règles prouvées sans effet | 116 → 94 Ko | 6 384 ❌ |

**La conclusion, vérifiée :** retirer une règle, même prouvée sans effet visuel,
change les index des suivantes et donc leur ordre dans la cascade. Deux règles
de même spécificité échangent leur priorité.

### La recommandation

**Ne pas nettoyer.** Le coût du risque dépasse le gain.

À la place : **écrire les nouvelles règles dans un bloc neuf, discipliné** — une
déclaration par propriété, pas d'`!important` sauf nécessité prouvée. La dette
existante reste, mais elle cesse de croître.

Pour le portage Swift, ce CSS ne sera de toute façon pas repris.

---

## 5. Les performances

```
ouverture Index    465 ms
ouverture Fil      268 ms
ouverture Aura     185 ms
requestAnimationFrame   38 / seconde  (était 186 avant correction v591)
```

**Corrigé en v591 :** un `MutationObserver` qui s'auto-déclenchait faisait
tourner une boucle en permanence — 3 rAF par image. C'est ce qui faisait ramer
l'app sur iPhone et empêchait même les captures d'écran d'aboutir.

**Corrigé en v561 :** `syncAll()` reconstruisait les cinq surfaces à chaque
changement, même celles hors écran. Il ne reconstruit plus que ce qui est visible.

---

## 6. Ce qui bloque quoi

```
La refonte de la page + (phrase)
   └─ bloque : le trait pour planter
   └─ bloque : la création de Nuée à la grammaire de la phrase
   └─ bloque : le brouillon (il partage le même écran)

La décision sur la palette des traits
   └─ bloque : la validation visuelle de toutes les fiches

Le scroll sous Peaufiner
   └─ bloque : rien, mais gêne l'utilisateur à chaque test
```

---

## 7. Historique des versions récentes

| Version | Ce qui a changé |
|---|---|
| v561 | `syncAll` ne reconstruit que le visible — fin des lags |
| v573 | Déduplication CSS, 281 déclarations retirées, 0 écart |
| v580 | Pincement de la Toile rétabli (`pointer-events` était à `none`) |
| v583 | Partager dans la ligne Peaufiner |
| v585 | « un jour » ajouté aux échéances avec point médian |
| v587 | La règle des couleurs : fond = état, traits = matière |
| v589 | Trois tons — décalage de teinte de 150° |
| v590 | Une Nuée suit sa dernière dalle plantée |
| v591 | Dalles de Nuée opaques + boucle infinie corrigée |
| **v592** | **La page + devient une phrase** |
