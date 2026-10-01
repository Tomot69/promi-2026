# L'onboarding — point de départ (préparé le 21 sept. 2026, fin du lot v19)

> À lire en ouvrant la session neuve, après CLAUDE.md et le point de reprise d'ETAT-DES-LIEUX.
> **Rien n'est commencé.** Ce document dit ce qui existe, ce que Tom a décidé, et ce qu'il faut lui demander.

## 1 · La décision de Tom

**L'onboarding est refait entièrement, avec l'idée du premier trait : on ne l'explique pas, on le fait tracer.**
Idée d'origine (audit du 21 sept., acceptée comme direction) : après le prénom, une demi-courbe en pointillés ;
le doigt la trace ; la **première dalle naît sous le doigt** et part se poser sur une **Toile vide**. Le seul geste du
produit est appris en le faisant. Les quatre diapositives disparaissent.

## 2 · Ce qui existe aujourd'hui (relevé dans le code, pas dans un document)

| quoi | où | état |
|---|---|---|
| le conteneur | `#promiOnb`, `app.html` ≈ l. 8578 | écran unique à étapes, posé **par-dessus l'accueil** |
| le verrou « déjà vu » | `localStorage 'promi_onb'` (écrit ≈ l. 8918, lu ≈ l. 8984) | tient depuis le 14 sept. |
| le rejeu | Réglages › « Revoir la présentation » → `replayIntro()` (≈ l. 3482) | efface le verrou |
| le prénom | `#pseudoInput` → `USER.name` (≈ l. 8752) | la graine du visage en dépend (`_grainePropre`) |
| le tutoriel intérieur | `startTuto(first)` (≈ l. 6635), overlay `#tutoOv` | lancé 420 ms après la fin de l'onboarding |
| le geste | `window._tenirInit` (≈ l. 4598, `#tenirZone`/`#tenirCv`), la page + (`#planterZone`/`#planterCv`) | le moteur du trait existe ; il est fait pour une fiche et pour la page + |
| une Toile vide | `promi_fresh` (≈ l. 2941 : vide `promises` et `NUE`) | existe pour le test |

**Les étapes d'aujourd'hui** (captures dans ce dossier, `onb1…6.png`, `onb_grille.png`) :
1. le mot-marque, « Tes promesses, tenues. », « En continuant, tu acceptes les Conditions et la Politique de confidentialité » ;
2. « Enchanté · Qui es-tu ? · Toi : [ton nom ou pseudo] · Suivant · Tu pourras le changer plus tard. » ;
3. « Tes Promi, deux vues » (**faux depuis longtemps** : le Fil n'est plus une vue de tes Promi) ;
4. une phrase « Promi… À : Moi » ;
5. « Choisis un style » — Encre · Braille · Sillons · Gravure · Terrazzo · Touffe · **Signal** (⚠ nom mort : la
   palette s'appelle Ingénu, et ce rail mêle mondes et palette) — « explore au moins un autre style pour continuer ».

**Ce que l'audit a relevé et qui doit disparaître avec la refonte** : le plateau et la barre de l'accueil visibles
dessous, des textes qui passent sous le plateau ou s'écrivent sur STUDIO · AURA · INDEX ; « Pas de note ni de score »
illustré par un cadran « HARMONIE 78 % » ; « ton Noyau grandit » ; des maquettes grises d'une autre époque.

## 3 · Ce qu'il faut demander à Tom — UNE question par tour (§10), dans cet ordre

1. **Les mots.** Aucun n'existe au moodboard. « promets-toi quelque chose » était une proposition de l'audit, pas un
   mot validé. Il faut les mots de chaque étape (§9 : on n'invente pas une phrase).
2. **Le premier Promi : que plante-t-on ?** Un titre tapé par la personne, ou une parole proposée ? À soi (« Je me
   promets ») forcément — personne d'autre n'existe encore.
3. **Ce qui reste des étapes d'aujourd'hui** : le prénom (oui, il donne le visage) ; le consentement CGU / politique
   (obligatoire juridiquement — où, et sous quelle forme ?) ; le choix du monde (maintenant, ou plus tard au Studio —
   Ingénu est la palette par défaut, décision du 21 sept.) ; le tutoriel intérieur (`startTuto`) : gardé, refait, ou
   supprimé puisque le geste est appris ?
4. **La permission des notifications** : à quel moment la demander ?

## 4 · Les règles qui s'appliquent déjà (à relire avant d'écrire une ligne)

- **Planche d'abord, intégration ensuite** (le moodboard fait foi) : une planche des étapes, deux thèmes, vraie Toile.
- **Le geste** (§5) : 118 px, deux points, un trait, courbes quadratiques, part du centre du rond gauche. Réutiliser le
  moteur existant, jamais une copie.
- **La dalle qui naît est la vraie dalle du moteur** (§4, `Toile.dalleTrame`, échelle 1) ; sous Ingénu elle est **bleue**
  (un Promi), et elle se pose sur la vraie Toile par `Toile.addPromi`.
- **Au doigt** : toute porte, tout geste se prouve au vrai doigt (CDP, `has_touch`) ; le clic fantôme (§8).
- **Rien ne survit à `closeAll`** (§8) ; l'onboarding ne laisse aucun nœud derrière lui.
- **Rien de l'accueil sous l'onboarding** : un écran plein.
- **Mesurer à l'encre**, pas à la boîte (leçon du lot v18).

## 5 · Le juge à écrire AVANT d'intégrer (et à faire rougir sur la version d'aujourd'hui)

`redteam_onboarding.py` : premier lancement (stockage vide) → aucun élément de l'accueil visible pendant l'onboarding ;
le trait se trace **au doigt** et plante **un** Promi, qui apparaît sur la Toile avec sa dalle ; le verrou `promi_onb`
est posé ; un rechargement ne relance pas ; « Revoir la présentation » relance ; `closeAll` ne laisse rien ; les deux
thèmes. La version d'aujourd'hui doit y rougir (accueil visible dessous, aucun trait).
