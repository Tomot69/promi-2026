# Chantier ENGAGEMENT — guider et stimuler sans gamifier

Octobre 2026 · consignes pour Claude Code · lots E0 à E6

> **IMPORTANT — Les AMENDEMENTS DU CHEF DE CHANTIER, en fin de document, priment sur tout le reste.** En cas de contradiction, ce sont eux qui s'appliquent.

## Règles de ce chantier (à lire avant tout lot)

1. **Inscrire E0 à E6 dans `CHANTIERS.md`** avec les prochains numéros libres, avant le premier patch. Chaque lot se termine par un compte rendu qui coche ou reporte **chaque** point numéroté de sa consigne. Rien ne disparaît en silence.
2. **Chercher avant d'écrire** : `startTuto`, `renderOb`, `obReplay`, `obFinish`, `OB[]`, la seconde de menthe, l'ordre de coloration progressive, la pression longue (260 ms) existent déjà. Les retrouver dans `app.html` actuel (pas dans les vieilles références) et les réutiliser.
3. **La grille anti-coercition s'applique à chaque lot** (étude 1) : aucun état « raté / en retard » visible ; rien qui décroît par inaction ; aucun manquement mis en évidence ; aucune récompense à la fois annoncée et proportionnelle ; rien que la personne ferait autrement si on lui expliquait le fonctionnement exact ; aucune réparation payante.
4. **Lexique** : Promi invariable. Mots interdits partout, y compris dans le code nouveau et les commentaires : tâche, to-do, objectif, échéance, valider, urgent, score, badge, série, streak, niveau, classement, points (au sens de récompense), bravo, félicitations, record.
5. **Tout lot qui touche au trait** (E2, E3) se conclut par une validation de Tom sur son iPhone 16e. « Vérifié au simulateur » ne vaut pas validation.
6. **Textes** : tous les textes de ce document sont provisoires. Les marquer `/* TEXTE PROVISOIRE — Tom */` dans le code et les regrouper dans un seul objet `TEXTES_ENGAGEMENT` pour que Tom les réécrive en un endroit.
7. **Ordre d'exécution** : E0 → E1 → E2 → E3 → point d'arrêt → E4 → E5 → E6A → (validation Tom) → E6B.

---

## E0 — Garde-fous, avant tout autre lot

**But.** Rendre la grille vérifiable par machine, et s'assurer que l'onboarding ne se relance plus.

1. **Verrou de l'onboarding** (ancien B9 / n° 10). Playwright : stockage vierge → l'onboarding s'affiche ; le terminer ; recharger deux fois → il ne s'affiche plus. Si le test échoue, corriger d'abord.
2. **Créer `redteam_engagement.py`** (Playwright sync, Chromium headless, pattern habituel `goto(file://…)` + `wait_for_timeout(2200)`). Il doit passer à la fin de **chaque** lot E. Contrôles :
   - **R1 Lexique.** Collecter le `textContent` de tous les éléments visibles de chaque écran parcouru, plus toutes les chaînes de `TEXTES_ENGAGEMENT`. Échec si une regex de la liste interdite (règle 4, insensible à la casse, frontières de mots) trouve une occurrence. Liste blanche explicite, une ligne par exception avec sa justification (ex. « trois points » des tailles de plume).
   - **R2 Absence et temps.** Sur `TEXTES_ENGAGEMENT` : échec si une chaîne contient `depuis|longtemps|toujours pas|encore rien|tu n'as|oubli|manqu|retard|hier|reviens|revenu|attend`.
   - **R3 Aucun chiffre sur la Pelote.** Sur l'écran de la Pelote, échec si un nœud texte visible contient `\d`.
   - **R4 Invariance du moment tenir** (actif à partir de E3). Deux Promi qui diffèrent sur tout (soi / destinataire nommé, `un jour` / `demain`, texte de 3 mots / 30 mots, Cercle / sans). Déclencher le tenir par le crochet de test déjà utilisé par `redteam_geste.py`. Mesurer la durée de la séquence (du trait reconnu au retour au repos) : échec si les deux durées diffèrent de plus de 16 ms ou si l'une dépasse 1000 ms.
   - **R5 Rien ne se thésaurise.** Clés de `localStorage` avant / après trois tenir : échec si une clé nouvelle apparaît hors liste blanche (les drapeaux de E1 et E2 y figurent, aucun compteur).
   - **R6 Sortie à un geste.** À chaque étape de l'onboarding, présence d'une sortie visible activable en un tap. Échec sinon.
   - **R7 Âge invisible.** Sur la Toile et sur une fiche à tenir, échec si un texte visible matche `il y a|depuis \d|\d+ ?j(ours)?\b` (les libellés de la liste d'échéance — `demain`, `5 jours`… — sont en liste blanche, ils disent un horizon, pas un âge).
3. **Délier.** Vérifier que « Délier » (étude 2 : issue pour un Promi jamais tenu) figure dans `CHANTIERS.md`. Sinon l'y inscrire, avec la mention : *ce chantier-ci augmente le nombre de Promi créés, donc le stock de dalles à tenir ; sans Délier, l'état « à tenir pour toujours » devient le critère 1 de la grille.*

**Preuve à rendre.** Sortie complète de `redteam_engagement.py` (R4 marqué « inactif avant E3 »), sortie du test de verrou.

---

## E1 — Gestes appris en situation (le composant passe en premier)

**But.** Chaque geste s'apprend une fois, au moment exact où il devient utile, en le voyant faire — jamais dans un tutoriel en amont.

1. **Un seul composant** `GesteFantome` : une main fantôme (forme sobre, crème à 60 % en clair, brun à 60 % en sombre, pas de mascotte, pas d'ombre portée) qui exécute le chemin réel du geste au-dessus de sa cible. API : `GesteFantome.montrer(idGeste, elementCible, chemin)` et `GesteFantome.oublier(idGeste)`.
2. Comportement : s'affiche après 600 ms d'inactivité sur l'écran concerné ; joue le geste deux fois maximum (pause 900 ms) ; disparaît au premier toucher n'importe où ; drapeau `geste_vu_<id>` posé dès la première apparition. Plus jamais réaffiché, sauf rejeu volontaire.
3. **Inventaire** : rendre un tableau de tous les gestes de l'app (au minimum : tracer pour tenir, tracer sa moitié de Chiche, appui long sur le Noyau, toucher la Pelote, gestes de la bande de dessin si elle est intégrée), avec pour chacun l'écran et la condition où il devient utile. Brancher `GesteFantome` sur chacun.
4. **Rejeu** : le point d'entrée existant de `obReplay` devient « Revoir les gestes » et efface les drapeaux `geste_vu_*`. Ne pas créer d'autre entrée, ne rien ajouter au Studio.
5. `prefers-reduced-motion` : la main apparaît immobile au point de départ du geste, avec une flèche du trajet. Aucune animation.

**Preuve.** Pour chaque geste de l'inventaire : capture de la première apparition ; rechargement → absent ; rejeu → présent. R1, R5, R6 au vert.

---

## E2 — Le premier Promi, tenu en une minute

**But.** Remplacer le tutoriel par une boucle complète vécue une fois : écrire → planter → faire → tracer → sentir. Les testeurs ne savent pas quoi faire parce qu'ils n'ont jamais vu la boucle se fermer.

1. **État des lieux d'abord.** Lister les étapes actuelles de `OB[]` dans un tableau : garder / supprimer / remplacer. **Garder intactes** les étapes d'identification (compte, pseudo) et l'étape Studio si elle existe. Supprimer les étapes qui *expliquent*. Aucune étape supprimée sans figurer dans le tableau.
2. **Nouvelle séquence**, après l'identification :
   - Un seul écran : titre « Promi garde ta parole. » · sous-titre « Commence par une toute petite, tenable tout de suite. » Un bouton « Allons-y », une sortie « Plus tard ».
   - Ouverture de la **vraie page +**. Phrase fantôme dans le champ, tirée parmi : « Je me promets de boire un verre d'eau. » · « Je me promets d'ouvrir la fenêtre. » · « Je me promets de m'étirer trente secondes. » Un toucher sur le fantôme le remplit ; la personne peut écrire la sienne. Destinataire : soi. Réglages par défaut. Rien d'autre n'est montré.
   - Plantation : animation existante. Le Promi est **réel** (a un `pid`, compte partout). La règle « Toile décor pendant l'onboarding » ne s'applique plus ici : l'onboarding s'achève avant la Toile.
   - Une ligne : « Fais-le. Puis reviens le tenir. » La fiche est ouverte ; `GesteFantome.montrer('tenir', …)` s'y déclenche.
   - Tenir → moment E3 (s'il n'est pas encore livré : comportement actuel).
   - Dernière ligne, une seule fois : « La prochaine, dis-la à quelqu'un. » Un toucher ferme. Drapeau `ob_fini`.
3. « Plus tard » à chaque étape : un tap, mène à la Toile vide (écran vide de E4). Le premier Promi n'est jamais redemandé.
4. L'ordre de coloration progressive reste réservé aux démonstrations, jamais à ce parcours.

**Preuve.** Playwright, stockage vierge : identification → écran unique → page + → toucher le fantôme → planter → tenir par le crochet de test → assertions : Promi à l'état tenu, `pid` présent, `ob_fini` posé ; recharger → aucun onboarding. Compter les interactions jusqu'au tenu : **au plus 5 taps + 1 trait** après l'identification. Captures de chaque étape en clair et en sombre. R1, R2, R5, R6 au vert. **Puis validation de Tom sur iPhone** : le parcours complet, chronométré par lui.

---

## E3 — Le moment « tenir »

**But.** Donner l'accusé de réception que réclame la « petite étoile », sous forme de sensation et non de monnaie : immédiat, identique à chaque fois, bref, rien à accumuler.

1. **Séquence**, à partir de la reconnaissance du trait (t = 0), durée totale ≤ 900 ms :
   - t = 0 : le trait se fige ; appel `promiHaptique('tenir')` (voir point 4).
   - 0 → 140 ms : la dalle passe en menthe pleine chroma (réutiliser la seconde de menthe existante, ne pas en écrire une seconde).
   - 80 → 700 ms : **l'onde**. Les dalles voisines au sens Voronoï se soulèvent (échelle 1 → 1,03 → 1, courbe ease-out) par rangs : rang 1 à 80 ms, rang 2 à 160 ms, rang 3 à 240 ms, amplitude divisée par deux à chaque rang. La Toile accuse réception, puis se repose.
   - Aucun texte, aucune particule, aucun son par défaut.
2. **Invariance absolue** : la séquence ne dépend d'aucune propriété du Promi (importance, destinataire, ancienneté, longueur). Contrôle R4.
3. `prefers-reduced-motion` : menthe seule, sans onde.
4. **Haptique** : écrire seulement le crochet `promiHaptique(nom)` (fonction vide documentée). Le motif appartient au chantier haptique, mené en conversation dédiée. À noter dans `CHANTIERS.md` pour ce chantier-là : **Safari iOS n'implémente pas `navigator.vibrate`** ; sur l'iPhone de Tom, le prototype ne vibre donc pas du tout, quel que soit le code — c'est très probablement la cause du manque ressenti au premier test. Le rendu réel viendra de Core Haptics au portage Swift.
5. Performance : aucune tâche longue > 50 ms pendant la séquence (Playwright, `PerformanceObserver` sur `longtask`), en mode monde le plus coûteux de la liste.

**Preuve.** R4 au vert avec les deux mesures affichées ; enregistrement vidéo Playwright de la séquence en clair et en sombre ; mesure longtask. **Validation de Tom sur iPhone.**

---

## Point d'arrêt après E3

Livrer E1, E2 et E3, puis s'arrêter. Tom fait repasser ses deux testeurs (consigne pour eux : « fais ce que tu veux pendant trois minutes », sans aide). Rien ne démarre avant son retour.

---

## E4 — Écrans vides qui invitent, et phrases d'exemple à la page +

**But.** Qu'aucun écran ne laisse sans savoir quoi faire, et que la personne comprenne ce qui compte comme un Promi : une phrase qu'on a déjà dite.

1. **Inventaire** de tous les états vides (chercher les conditions de liste vide dans le code) : tableau écran / condition / texte actuel. Au minimum : Toile sans Promi, Index sans Promi, Cercle sans membre, Fil, liste des Chiche, recherche sans résultat.
2. Chaque état vide reçoit **deux lignes et un seul geste** : ligne 1 dit l'état, sobrement ; ligne 2 invite ; un toucher sur la ligne 2 mène à l'action. Jamais deux invitations. La règle [V] reste : un vide de recherche ne dit jamais la même chose qu'un vide de contenu.
3. Textes provisoires :
   - Toile vide : « Rien n'est planté. » / « Qu'as-tu dit aujourd'hui que tu comptes tenir ? » → page +
   - Index vide : « Pas encore de parole. » / « La première se plante en une phrase. » → page +
   - Cercle vide : « Un Cercle, c'est des gens. » / « Ajoute la première personne. » → ajout
   - Chiche vide : « Aucun défi en cours. » / « Lance un Chiche. Le pire qui puisse arriver, c'est un oui. » → page + en mode Chiche
   - Les autres : proposés par Claude Code, marqués provisoires.
4. **Page +, phrase fantôme** quand le champ est vide (hors onboarding) : tirée d'un ensemble de verbatims ordinaires, jamais la même deux fois de suite, effacée à la première frappe. Ensemble provisoire : « Je te rappelle demain. » · « Je passe samedi t'aider. » · « Je te rends ton livre. » · « Promis, j'arrête de râler le lundi. » · « Je t'envoie les photos ce soir. » · « Je viens à ton anniversaire. » · « Je cours dimanche. » · « Je relis ton texte. » · « J'appelle mamie. » · « Je te dois un café. » · « Je répare la porte. » · « Je t'apprends à faire la pâte. »

**Preuve.** Tableau d'inventaire complet ; capture de chaque état vide en clair et en sombre ; test : chaque état vide contient exactement un élément interactif d'invitation ; test de non-répétition sur 50 ouvertures de la page +. R1, R2 au vert.

---

## E5 — Phrases d'accueil

**But.** Un mot drôle et décalé à l'ouverture, qui suggère sans relancer.

1. **Données** : un tableau unique `PHRASES_ACCUEIL` d'objets `{id, texte, cible}` avec `cible ∈ {creer, envoyer, chiche, studio, aucune}`.
2. **Affichage** : une phrase par lancement de l'app, à l'arrivée sur la Toile, jamais pendant l'onboarding. Emplacement : centrée au-dessus de la barre basse, Atkinson Hyperlegible, opacité 0,6, aucun cadre, aucun bouton. Disparaît au premier toucher n'importe où (fondu 300 ms). Un toucher **sur** la phrase ouvre sa cible.
3. **Sélection** (fonction pure, testable) :
   - jamais la même que la précédente ;
   - exclure toute phrase dont la cible a été faite par la personne dans les 7 derniers jours (redemander un choix déjà fait est un critère de risque) ;
   - exclure toute cible `studio` si l'action suggérée n'est pas gratuite selon le gating en vigueur — aucune phrase ne pousse vers un achat ;
   - aucune phrase ne parle de la personne absente, du temps écoulé, ni d'un destinataire qui attendrait (R2).
4. Corpus provisoire (Tom réécrit) :
   - aucune : « Ici on ne compte rien. On garde. » · « Pas d'étoile ici. Juste ta parole, et ce qu'elle devient. »
   - creer : « Une parole en l'air, c'est joli. Posée ici, c'est mieux. » · « Les promesses poussent mieux avec un nom dessus. » · « Promettre, c'est facile. L'écrire, c'est déjà un peu tenir. »
   - envoyer : « Et si tu promettais quelque chose à quelqu'un d'autre que toi ? » · « Une promesse à deux, ça se trace à quatre mains. »
   - chiche : « Lance un Chiche. Le pire qui puisse arriver, c'est un oui. » · « Un Chiche, c'est un défi poli. Enfin, presque. »
   - studio : « Même parole, autre matière. » · « Change de palette. Tes promesses ne t'en voudront pas. »

**Preuve.** Tests unitaires de la sélection (non-répétition, exclusion 7 jours, exclusion payante) ; capture en clair et en sombre ; R1, R2 au vert.

---

## E6A — La Pelote qui s'enrichit : maquette d'abord

**But.** Que ce qu'on tient se voie, sans jamais devenir un compte. **Aucune intégration avant validation de Tom.**

Règles de conception, non négociables :

1. **La Pelote est toujours pleine et belle à zéro** (décision actée, densité 3). Elle ne « part pas de rien » : elle part d'une matière unie, peignée.
2. **Pas de seuils de comptage.** Un seuil « au 5ᵉ tenu, il se passe X », même silencieux, échoue au critère 5 : expliqué, il pousse à fabriquer des Promi pour l'atteindre.
3. **Accrétion continue** : chaque Promi tenu laisse une inclusion dans la fourrure dont la **forme dérive du trait réellement tracé** (chemin du doigt simplifié) et la position est tirée d'une graine `pid`. Taille indépendante de toute propriété du Promi. Rien ne se retire jamais ; un Promi délié voit son inclusion se fondre dans la fourrure, sans disparaître.
4. **Un fil par personne** : chaque destinataire envers qui une parole a été tenue ajoute un fil de couleur (palette du Studio) qui s'enroule autour de la Pelote ; son épaisseur suit le cumul envers cette personne, monotone, jamais décroissante (étude 1, décision 1).
5. **Premières fois** : changements qualitatifs, chacun une seule fois, jamais annoncés, **jamais listés nulle part** (une liste rendrait visibles ceux qui manquent : critère 3). Proposition : premier tenu → première inclusion ; premier Chiche relevé → un nœud apparaît sur un fil ; premier trait partagé fermé → deux fils se croisent et se nouent.
6. Rendu déterministe : même données → même image (aucun `Math.random` dans l'accrétion ; la teinte intérieure tirée au hasard reste un choix d'affichage indépendant).

**Livrable E6A** : un HTML autonome montrant neuf états côte à côte, en clair et en sombre : 0 tenu · 1 · 3 · 12 · 40 · 40 avec 1 destinataire · 40 avec 6 destinataires · après premier Chiche · après premier trait partagé. Lisibilité à 200 px vérifiée par une vignette réduite de chaque état.

## E6B — Intégration (après validation de Tom seulement)

**Preuve.** Test de monotonie : ajouter 20 tenus un à un, l'ensemble des inclusions de l'état n est inclus dans celui de l'état n+1 ; test de déterminisme (deux rendus identiques au pixel) ; R3 au vert ; 60 im/s sur 390 px (mesure frame timing).

---

## AMENDEMENTS DU CHEF DE CHANTIER — prioritaires sur tout ce qui précède

**A1 · E3** : supprimer l'onde sur les dalles voisines et la menthe de célébration. Elles sont interdites par la loi « aucun effet posé sur la Toile », et le vert de célébration a été écarté. Le moment « tenir » reste la transformation existante de la matière. On garde l'invariance (R4), le crochet `promiHaptique` et la mesure des tâches longues.

**A2 · Aucune transparence ni fondu.** La main fantôme (E1) est dessinée au trait plein, opaque, à l'encre du mode. La phrase d'accueil (E5) est opaque, dans une couleur de texte secondaire, et apparaît et disparaît sans fondu. `redteam_engagement` contrôle qu'aucun élément du chantier n'a une opacité inférieure à 1 ni de fondu.

**A3 · Aucun texte à l'impératif, aucune injonction** : réécrire tous les textes provisoires qui en contiennent (« Fais-le. Puis reviens le tenir. », « La prochaine, dis-la à quelqu'un. », « Ajoute la première personne. », « Lance un Chiche. »…), et ajouter ce contrôle à R1. Les textes restent provisoires : Tom les réécrit.

**A4 · R1** : la liste interdite s'aligne sur le lexique de `CLAUDE.md`. « Échéance » en est retiré si l'app l'emploie.

**A5 · E6A** : sur la maquette, le fil par personne est montré sans épaisseur cumulée (un fil par personne, d'épaisseur constante). Tom tranche.

**A6 · NOUVEAU, E2bis : l'interface se dévoile.** Au premier lancement, la barre du bas ne porte que le +, réduite à sa taille. Chaque élément apparaît à sa place définitive, à sa première fois et jamais à un compte : l'Index à la première plantation ; l'Aura et sa Pelote au premier tenu (la main fantôme la désigne) ; le Studio juste après ; le Fil dès qu'une chose arrive des autres ou à la première parole adressée à quelqu'un. La barre s'élargit au fil des apparitions et reste asymétrique tant que tout n'est pas là. Rien ne disparaît une fois apparu. Garde-fous : « Plus tard » dans l'onboarding fait tout apparaître ; un réglage « Tout afficher » existe ; tout ce qui arrive des autres fait apparaître le Fil aussitôt. Juge : stockage vierge, parcours E2 complet, et à la fin tout est visible ; parcours « Plus tard », et tout est visible d'emblée ; aucun élément ne disparaît dans aucun parcours.

**A7 · Ordre** : E0 → E1 → E2 et E2bis → E3 → point d'arrêt (Tom fait repasser ses testeurs) → E4 → E5 → E6A → validation de Tom → E6B.
