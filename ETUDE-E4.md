# Étude E4 · étape 1 — les écrans vides (aucun code)

1er nov. 2026 · lot v177 · C-079. Textes **provisoires** : Tom les écrit ou les valide avant tout code. Aucun impératif (A3), aucune transparence (A2), rien posé sur la Toile (A1).

Règle d'E4 : **deux lignes, un seul geste.** Ligne 1 : l'état, sobrement. Ligne 2 : une invite sans impératif ; la toucher mène à l'action. Jamais deux invitations. Un vide de recherche ne dit jamais la même chose qu'un vide de contenu.

**Comment lire « texte actuel »** : relevé à l'écran (WebKit, 390 × 844) quand c'est écrit **vu** ; sinon lu dans le code. Les conditions sont lues dans `app.html`.

## Les écrans

| Écran | Condition du vide (code) | Texte actuel | Proposition provisoire (ligne 1 / ligne 2) | Au toucher de la ligne 2 |
|---|---|---|---|---|
| **Toile sans parole** | `n===0`, `n` = paroles hors gardées et demandes (7050) | **vu : aucun texte.** `#toileEmpty` existe, masqué (2137) : « Ta Toile n’attend que toi » | « Rien n’est planté. » / « Qu’as-tu dit aujourd’hui que tu comptes tenir ? » (texte d'ENGAGEMENT, sans impératif ; Q584 attend Tom) | page + d'un Promi |
| **Index sans parole** | `!ent.length`, sans recherche ni filtre (3841) | **vu :** « Rien ici » / « Touche le + pour planter un Promi. » (impératif ; le « + » n'est pas touchable) | « Pas encore de parole. » / « La première se plante en une phrase. » | page + d'un Promi |
| **Index filtré sans résultat** | `!ent.length`, `ixFiltre` posé : suspens, promi, nuees, demandes (3841) | **vu :** le même texte que l'Index vide | « Rien sous ce tri. » / « Toutes les paroles sont dans Tout. » | remet le filtre sur Tout |
| **Gardés de côté, vide** | `!ent.length`, `ixFiltre='brouillons'` (3841, 42432) | le même texte que l'Index vide | « Rien de gardé de côté. » / « Toutes les paroles sont dans Tout. » | remet le filtre sur Tout |
| **Recherche de l'Index, sans résultat** | `!ent.length`, `ixQuery` non vide (3497, 3841) | **vu :** le même texte que l'Index vide (la règle [V] est violée) | « Rien pour « mot ». » / « Retour à tout l’Index. » | vide le champ |
| **Fil vide** | `!_list.length`, `_q` vide (7102) | **vu :** ✦ « Rien ne bouge encore » / « les gestes de tes proches apparaîtront ici » (rien à toucher) | « Rien ne bouge encore. » / « Une parole donnée à quelqu’un, et le Fil s’anime. » | page + d'un Promi, à quelqu'un |
| **Recherche du Fil, sans résultat** | `!_list.length`, `_q` non vide (7102) | **vu :** ✦ « Rien ne correspond » / « essaie un autre mot » (impératif) | « Rien pour « mot ». » / « Retour à tout le Fil. » | vide le champ |
| **Fil filtré, vide** | `fdFiltre` posé, `_filTrieFiltre` retire tout (4496, 19925) | **vu : aucun texte, page muette** (un défaut, pas un choix) | « Rien sous ce tri. » / « Retour à tout le Fil. » | remet le filtre sur Tout |
| **Cercle sans membre** | `NUEEMEM[k]` vide (16018) | **vu :** « Avec toi seulement » · « ENCORE AUCUNE PAROLE » · « Planter dans le Cercle » | « Un Cercle, c’est des gens. » / « La première personne s’ajoute ici. » (« Ajoute… » est refusé par A3) | ajout d'une personne (MEMBRES) |
| **Cercle avec membres, sans parole** | `lst.length===0` (6092) | « ENCORE AUCUNE PAROLE » · « Planter dans le Cercle » ; « aucun Promi ici pour l’instant » masqué (14765) | Rien de neuf : le bouton existant est déjà la ligne 2 | planter dans le Cercle |
| **Liste des Chiche** | **n'existe pas** : ni liste, ni filtre (menus 2823, 2736) ; les Chiche sont mêlés aux Promi | — | Si Tom veut le filtre : « Aucun défi en cours. » / « Le pire qui puisse arriver, c’est un oui. » (« Lance un Chiche. » est refusé par A3) | page + d'un Chiche |
| **Aura sans aucune parole** | `D.P.length===0` (31196) | **vu :** « La première parole laissera sa trace ici. » / « Tout commence par une parole donnée. » (rien à toucher, sauf la Pelote et son bouton) | Le même texte : la ligne 2 devient touchable | page + d'un Promi |
| **Aura, des paroles, aucune tenue** | `D.n===0`, `D.P.length>0` (31203) | « La première parole laissera sa trace ici. » ; Noyaux et légende visibles, « Ce que tu as tenu » masqué (31224) | « Rien de tenu pour l’instant. » / « Une parole tenue prendra place ici. » (sans mot de manque, R2) | l'Index (la parole en cours) |
| **Fiche d'une personne, rien en commun** | `L.length===0` (32372) | aucun texte ; le Noyau, « + Planter un Promi », « + Lancer un Chiche » (32410) | « Rien entre vous pour l’instant. » / aucune ligne 2 : les deux boutons restent (voir la question 3) | les deux boutons existants |
| **Pièces jointes, vide** | `!list.length` (9467) | « aucun fichier — appuie sur + » (impératif) | « Aucun fichier. » / le + existant, sans phrase | sélecteur de fichiers |
| **Partager, Toile vide** | `promises` vide (7878) | **non établi** : aucun message dans le code lu, rendu non regardé | Pas de proposition avant d'avoir vu l'écran | — |

Hors sujet, déjà pleins : les Notifications (une page de réglages), « Ce qu'on t'a tenu » (masqué quand il est vide), la ligne « Un mot… » (toujours présente).

## Ce que le lot a montré en plus

- **Quatre textes actuels sont des impératifs** : « Touche le + », « essaie un autre mot », « appuie sur + », et « Plante le premier Promi de ton Cercle → » (code, 14202 ; pas vu à l'écran).
- **Le Cercle n'a été regardé que vide** : la fiche d'un Cercle sans membre mais avec des paroles reste à voir à l'écran, avant tout code.
- **R2 limite les mots** : « attend », « manqu… », « toujours pas », « encore rien » sont refusés par `redteam_engagement`. Les propositions ci-dessus les évitent.
- **Il n'y a pas d'amendement A8** dans `ENGAGEMENT.md` : il s'arrête à A7. L'étude tient compte d'A1 à A7. Aucun texte proposé ne parle de « à tenir » : l'app n'a plus que deux états.

## Page + : ce qui existe et ce qui manque (point 4 d'E4)

**Existe déjà** (`lot-EXEMPLES-V20`, 37566) :
- cinq listes : 20 phrases à soi, 16 à quelqu'un, 15 demandes, 29 Chiche, 40 noms de Cercle ;
- une phrase par ouverture, les premières fixes (deux par liste, une pour le Chiche), puis un sac sans remise gardé d'une ouverture et d'une séance à l'autre ;
- effacée à la première frappe (pastille et `placeholder`), jamais écrite comme parole ;
- hors onboarding dans ce qui a été lu (l'onboarding n'a pas été lu en entier).

**Manque :**
1. **« Jamais la même deux fois de suite » n'est pas garanti** : quand le sac se vide, la dernière phrase peut ressortir la première (1 chance sur 18 pour « à soi », 1 sur 28 pour un Chiche). `redteam_suggestions` ne regarde pas cette jonction.
2. **Les verbatims d'E4 n'ont pas la forme de la page +** : la phrase est « Je me promets de … », elle attend un infinitif, pas « Je te rappelle demain. ». Transposés, sans impératif : à soi « courir dimanche », « appeler mamie », « arrêter de râler le lundi » ; « réparer la porte » ; à quelqu'un « te rappeler demain », « passer samedi t’aider », « te rendre ton livre », « t’envoyer les photos ce soir », « venir à ton anniversaire », « relire ton texte », « t’apprendre à faire la pâte », « t’offrir le café que je te dois » (« Je te dois un café. » n'a pas d'infinitif direct).
3. **Un écart sur le Chiche** : un champ vidé après la frappe affiche « ce que tu n’as jamais osé lui lancer… » et non l'exemple tiré.

## Décisions à prendre par Tom

1. **Toile vide (Q584) :** garder le texte d'ENGAGEMENT, ou ton texte ? Proposition : celui d'ENGAGEMENT, en texte sous le plateau, jamais peint sur la Toile.
2. **Liste des Chiche :** un filtre « Chiche » dans l'Index est une fonction neuve, elle n'existe pas aujourd'hui. Proposition : l'ajouter au menu Trier, sinon cette ligne tombe.
3. **Deux invitations sur deux écrans :** « un seul geste » contredit la fiche d'une personne (deux boutons) et le Cercle sans membre (« Planter dans le Cercle » et l'ajout). Proposition : garder les boutons existants, l'invite neuve du Cercle remplace seulement le texte d'état.
4. **Phrases de la page + :** ajouter les douze verbatims transposés aux listes, et corriger la jonction du sac. Proposition : oui aux deux.
