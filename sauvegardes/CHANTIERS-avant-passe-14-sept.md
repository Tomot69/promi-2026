# Promi — CHANTIERS

**Inventaire complet, unique, à cocher.** — **v3**, 11 août 2026,
après lecture du compte rendu complet de Claude Code (lot zéro + lot 1).
Établi le 11 août 2026, au point exact où le chat précédent a saturé.

Ce document remplace les listes éparpillées : `§22`, `§37.2`, `§49.4`, `§56.4`,
`§59.4`, `§64.5`, `§65.5` de l'addendum v6, plus `LOTS-SUIVANTS.md` (7 lots) et
`DECISIONS.md § E` (5 questions). **Rien n'a été retiré. Tout est ici.**

---

## 0. Comment lire

| Marque | Sens |
|---|---|
| **✓** | fermé, prouvé par un test |
| **▸** | ouvert |
| **◐** | commencé, non fini |
| **?** | à confirmer contre `ETAT-DES-LIEUX.md` (voir §1.3) |
| **[V]** | décidé, verrouillé | 
| **[O]** | à trancher — personne n'a le droit de décider seul |

**Le dossier local est la source de vérité.** Le Projet claude.ai est un
historique. Ce qui est mesuré dans `app.html` l'emporte sur ce qui est écrit
dans les documents — cette règle a été apprise trois fois pendant le lot 1.

---

## 1. Le point exact

### 1.1 Où en est la machine

```
Dossier      /Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026
Mac          Intel x64 · Python 3.9 (Xcode) · Playwright 1.60 · Node v24.19.0
app.html     1592 Ko — au départ identique à promi-v592.html du Projet
sauvegardes/ app-origine.html · app-avant-lot1.html
```

**Les 24 fichiers sont en place**, `verifier-installation.py` l'a confirmé.

### 1.2 Où en est le chantier

| Étape | État |
|---|---|
| Lot zéro — lecture, tests, témoin | **✓ fait**, 142/142 |
| Référence design refigée sur ton Mac | **✓ fait**, `✅ AUCUN ÉCART` |
| Sauvegarde avant lot 1 | **✓ faite** |
| **Lot 1 — page + : en-tête et trait** | **✓ accepté** — voir ci-dessous |
| **Chantier 50 — fiabiliser le contrôle design** | **▸ à faire AVANT le lot 2** |
| Lots 2 à 7 | **▸ non commencés** |

### Lot 1 — verdict

**Accepté.** Le travail est bon et honnêtement rendu.

| Preuve | Résultat |
|---|---|
| `redteam_geste` | **13/13**, deux fois — le moteur du geste est intact |
| Les 6 autres batteries | au score attendu |
| Le trait, mesuré fiche vs page + | **identique au pixel** sur 7 propriétés |
| Débordements | 0 |
| `_tenirInit` | **non touché** |

**Les 12 écarts de `releve-design.py` ne sont pas une régression du lot 1.** Ils
portent tous sur **un seul élément** — le mot de nature en Fraunces sur la
**fiche**, un écran que le lot n'a pas touché — et uniquement sur sa `width`.
Aucune couleur, aucune position, aucune taille de police.

**La cause est trouvée** → chantier 50.

### 1.3 L'angle mort à combler — important

L'addendum v6 décrit fidèlement le fichier **jusqu'à la v467 environ**. L'app est
à la **v592**. Entre les deux, une centaine de versions dont l'historique ne vit
que dans `ETAT-DES-LIEUX.md`, sur ton Mac.

Conséquence : les lignes marquées **?** ci-dessous peuvent déjà être faites.
**Deux mesures faites à l'instant sur la v592 disent qu'au moins une ne l'est
pas — et qu'elle a empiré :**

| Mesure | Addendum v6 | Réel sur v592 |
|---|---|---|
| Handlers orphelins | 26 | **36** |
| Classes mortes | 161 | **317** |
| Blocs `plus-*` | 14 | 1 |

Le code mort a doublé depuis que le document a été écrit. Ce n'est pas grave —
rien ne plante — mais **ça trompe la lecture**, et Claude Code lit ce fichier à
chaque lot.

**Ce qu'il faut pour lever le doute, en un geste :** ouvre `ETAT-DES-LIEUX.md`
dans TextEdit, ⌘A ⌘C, et colle-le-moi ici. Je fusionne et je supprime tous
les **?**.

### 1.4 Le bug de fond — trouvé le 11 août

Le contrôle du design donne un résultat différent à chaque passage : **0, puis 28,
puis 12 écarts**, sur un fichier qui n'a pas bougé. `redteam_toile` oscille de la
même façon, 14 / 15 / 16. Claude Code l'a signalé trois fois et a eu raison de
refuser de livrer dessus.

**Les écarts ne sont pas aléatoires, ils progressent :** la largeur du mot de
nature en Fraunces passe de `82,01` → `87,08` → `93,80` px. Ce sont trois états
de chargement de police, pas du bruit.

**La cause : le script mesure avant que les polices soient prêtes.**

Les écarts frappent uniquement des boîtes dont la largeur est calculée **autour
d'un texte** — nature, fermer, nom lien, mot lien, bascule, pastille. Jamais une
couleur, jamais une position, jamais une hauteur. Une largeur de texte qui change
sans que rien d'autre bouge, c'est une police qui n'était pas encore chargée au
moment de la mesure.

**Ce n'est pas seulement Fraunces.** « fermer » est en **Apfel**, une police
embarquée en base64, sans réseau — et elle dérive quand même. Les polices
embarquées se chargent elles aussi de façon asynchrone.

**Un aggravant s'ajoute par-dessus**, à traiter en second :

```
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500..700&display=swap">
```

L'app va chercher Fraunces sur le réseau — d'où le
`⚠ ERREURS JAVASCRIPT : A network error occurred`. Et cette requête est
probablement inutile :

| Fait | Mesure |
|---|---|
| Graisses de Fraunces utilisées dans le CSS | **600 uniquement**, sur 21 règles |
| Fraunces embarqué en base64 dans le fichier | **normal 600 et italique 600** |
| Ce que la requête réseau demande | 500 à 700 — dont rien n'est utilisé |

**Le vrai correctif est d'attendre `document.fonts.ready` avant de mesurer.**
Retirer le `<link>` est un second geste, à faire seulement si la preuve tient.

**Conséquence si on ne corrige pas :** la porte de sortie de chaque lot
(`releve-design.py` doit afficher ✅) est un tirage au sort. Une vraie régression
passerait inaperçue au milieu des écarts fantômes. **Et ne pas re-figer :** on
figerait une valeur au hasard parmi trois, pour la troisième fois.

**Ce n'est donc pas le lot 2 qui vient, c'est le chantier 50.**

---

## 2. Ce que le lot 1 a corrigé dans les documents

Claude Code a mesuré l'app trois fois et **mes chiffres écrits étaient faux trois
fois**. La mesure fait foi. À reporter dans `PARCOURS.md` :

| Point | `PARCOURS.md` dit | Réalité mesurée |
|---|---|---|
| Hauteur du trait | 118 px | **164 px** |
| Forme | pastille, rayon 26 px | **bande pleine largeur, rayon 0** |
| Libellé | 13 px, à 14 px du bas | **17 px, graisse 800, à 26 px du bas** |
| Point gauche | r = 18, plein | **r = 19, plein** |
| Point droit | r = 18 contour + r = 6, α .45 | **r = 19 contour α .4 + r = 6 plein α .4** |
| Fond clair | — | **rgba(22,23,27,.055)** |
| Fond sombre | — | **rgba(255,255,255,.12)** |
| Haut-gauche de la fiche | « mot-marque Promi 20 px » | **`#dptNat`, la nature, Fraunces 30 px** — il n'existe aucun mot-marque 20 px sur la fiche |
| Conteneur du trait | — | **176 px**, le canvas peint fait 164 |

**Décision prise pendant le lot 1 [V] :** le trait de la page + est une
**seconde implémentation assumée**, avec ses propres règles CSS dans le dernier
bloc. Le CSS du trait de la fiche est scopé `#detailPoster` et l'élargir
imposerait de toucher 30 règles anciennes en cascade avec `!important` — ce que
`CLAUDE.md` interdit, à raison. **À mutualiser plus tard, dans un lot dédié,
quand le design sera figé.** → devient le chantier **46**.

`PARCOURS.md § 2` et `§ 9` sont à corriger.

---

## 3. Chantiers fermés — ne pas rouvrir

| # | Chantier | Preuve |
|---|---|---|
| **1** | L'aperçu de Partager montre la **vraie** Toile | `Toile.renderTo()` · batterie 5 |
| **2** | Règle de matière par monde | §24.1 |
| **3** | Sélecteur du Noyau — deux groupes séparés | — |
| **4** | Le Noyau se pose sur Ma Toile | — |
| **5** | Le Noyau en Mes Promi — bloc 2 × 2 | §52.2 |
| **6** | Le % du Noyau porte la double encre | §53 |
| **7** | Le % de l'Aura en vraie signature | §54 · contrôle anti-dérive |
| **8** | Le Noyau du bouton + est celui de l'Aura | §55 |
| **13** | Noyau déplaçable au doigt, deux aimants | §60.2 · batterie 6 |
| **14** | Réorganisation des cases en Mes Promi | §60.3 |
| **35** | Motif de couverture — extraction ligne à ligne | §50 |

**Le n° 1 était le seul bloquant du projet. Il est fermé.** Plus rien
n'empêche d'avancer.

---

## 4. Bugs ouverts

### n° 75 · ⚑ CE CHANTIER N'EXISTE PAS — FERMÉ LE 12 SEPTEMBRE 2026, C'ÉTAIT MON INSTRUMENT

**Je l'ai ouvert sur une mesure fausse, et je le ferme sur la mesure.** `redteam_verbe` donnait **3/6**, les trois rouges
en thème sombre avec `h=0`, et j'en avais conclu à un défaut du produit « antérieur au lot ». Repassé **machine au repos**,
il donne **6/6 sur QUATRE versions de l'app** — l'actuelle, `app-avant-ch59`, `app-avant-src-valide`, et surtout
`app-avant-cercle-toile` (md5 `3ac4975c`), **celle-là même sur laquelle j'avais « prouvé » que le défaut préexistait**.
Trois passes d'affilée, 6/6, `h=43,9` et bouton `h=58` dans les deux thèmes.

**Et ce n'est pas non plus un défaut d'appareil lent** : passé au **bridage CPU du CDP ×1, ×4, ×6 et ×10**, dans les deux
thèmes, le verbe et le bouton sortent à leur hauteur les huit fois (`sauvegardes/ch59/verbe_sous_charge.py`).

**Ce que le 3/6 mesurait :** la machine. La passe d'origine tournait pendant une autre mesure Playwright — exactement le
piège que `CLAUDE.md §7` décrit (« douze Playwright lancés d'un coup font ramer la machine, et les rouges qu'on lit alors
sont faux : boîtes à 0 × 0 »). J'avais même écrit qu'un rouge apparu en parallèle se reconfirme en série : **je ne l'ai pas
fait, et j'ai inscrit un chantier là-dessus.** La leçon n'est pas nouvelle, elle est mal appliquée.

**Ce qui reste vrai et ne se perd pas :** mon bâti de fond du Cercle, lui, VOLAIT le fil principal (≈ 100 ms toutes les
260 ms) et faisait bien tomber la batterie à **0/6** — le clair rendait `h=0` lui aussi. Ça, c'était un défaut réel, il est
corrigé (`requestIdleCallback`), et c'est ce qui m'a fait croire que le 3/6 restant avait la même nature.

*Texte d'origine de cette fiche, conservé :* le rouge portait sur « la phrase montre son verbe » (`je me promets`,
`je promets`) et « la bascule mène à un vrai bouton » (`bouton={'f':1,'h':0,'vis':False}`) en sombre.


| # | Chantier | Détail | État |
|---|---|---|---|
| **9** | Angles arrondis de l'image exportée | bloqué par le n° 22 | ▸ |
| **10** | Onboarding relancé à chaque chargement | verrou de persistance `promi_onb` | ▸ ? |
| **11** | Padding bas non unifié | 22 / 40 / 80 selon l'écran | ▸ ? |
| **12** | Tailles hors échelle | 14 et 15 px · rayons 13 et 15 | ▸ ? |
| **22** | Assainir la pile `save/restore` de `shareToile` | débloque le n° 9 | ▸ |
| **39** | `shareVis` inerte sur Ma Toile | depuis `renderTo()`, le chemin qui peint les libellés n'est plus emprunté — le bouton bascule sans effet | ▸ |
| **40** | Lisibilité du chiffre sur dalle claire | par contraste de texte, **sans fond** | ▸ |
| **44** | Titre du Studio à 24 px | écart assumé ou à corriger ? | ▸ [O] |
| **63** | **Les chemins vers la fiche d'une personne** (Tom, 11 sept. : « une seule fiche par personne, quel que soit le chemin — un chemin manquant, pas une seconde fiche à créer ») | Relevé au doigt, nom par nom, visage par visage (QUESTIONS.md Q195) : **aucun chemin n'ouvre autre chose que la fiche** ; **cinq endroits affichent une personne sans y mener** — ① **la fiche de Nuée** : « Avec Rachel, Adrien, +3 » inerte, et aucun disque de membre : **depuis une Nuée, aucun chemin vers ses membres** ; ② Peaufiner d'une Nuée (« Rachel · Adrien · +3 ») ; ③ la ligne « À Rachel » d'une fiche de Promi ou de Chiche (les disques dessous mènent) ; ④ les valeurs « Rachel » des rangées de Peaufiner ; ⑤ « toi » (Aura et disque de fiche) — le mode « moi » sans porte, avec `#profileScreen` inatteignable (`openProfile`, aucun appel). Un chemin manquant se branche sur `openPerson`, **jamais une seconde fiche**. ① demande une FORME (où toucher un membre) : pas de forme inventée (§9) — à dessiner avec Tom. Ouvert : le nom dans une carte du Fil ou de l'Index (Q195). **◐ FAIT le 11 sept. (`lot-CHEMINS-PERSONNE`) pour ①②③ :** les noms écrits dans `#dptQui` et `.np-val` mènent à `openPerson` (preuve au doigt 12/12, 7 ratés sur l'app d'avant). **④ tranché par Tom : la rangée « À QUI » reste un réglage, sans porte.** **✔ FERMÉ par Tom, 11 sept. (« le 63 est fermé »).** Ses deux restes vivent ailleurs : « toi » relève du mode « moi » (décision de produit, AUDIT-FICHE-PERSONNE § B bis) ; les noms DANS une carte restent la question Q195. | ✔ |
| **69** | **Aucun Promi ne garde son pinceau** (trouvé le 11 sept. à l'audit du Cercle — Tom : « fais-la après le Cercle […] c'est un lot à part ») | Choisir un pinceau à la page + puis planter : le Promi neuf a `p.trait` vide, sa fiche trace « Plein » (mesuré, deux thèmes, `sauvegardes/audit-cercle/audit_complement.py` partie B). Cause lue et validée par Tom : l'accroche de `lot-PINCEAU` (≈ l. 24227–24241, « LE TRAIT PLANTÉ GARDE SON PINCEAU ») lit `window.promises` — or `promises` est un `let` global (l. 2856), **pas une propriété de `window`** : le même piège que `cur` et `curNuee`, déjà documenté par `lot-PINCEAU-CIBLE`. À faire : prouver le défaut par le vrai geste (le contrôle doit rougir sur l'app d'avant), corriger dans un bloc neuf avec l'identifiant nu, vérifier `#addNuee` et `#addDraft`, batteries en série. **Après le Cercle.** Les pinceaux payants (0,50 €) relèvent du Cercle, pas de ce lot. **✔ FAIT le 11 sept., nuit** : `lot-PINCEAU` lit la vraie liste (`promises`, un `let`) — plus `window.promises` (undefined). `verif_69.py`, de bout en bout, deux thèmes : on touche « Coulé » / « Peigné » sur la page +, on plante → le Promi né porte ce trait et sa fiche l'affiche dans Peaufiner ; prouvé sur l'app d'avant (trait `None`, fiche « Plein »). Leçon d'instrument : un `scrollIntoView({block:'center'})` avant le toucher faisait défiler la page et le doigt tombait à côté (le piège du §8) — `nearest`. `#addNuee` et `#addDraft` passent par le même écouteur : non rejoués un par un. | ✔ |
| **64** | **Le bandeau du Peaufiner de la page +** (relevé le 11 sept., lot du Cercle — Tom : « note ceux qui restent comme chantier ») | Par un chemin utilisateur pur (touchers seuls, `sauvegardes/audit-cercle/probe_bandeau.py`), deux thèmes : la pastille de la page + (`#createSheet .enh`, 342 × 60 à 24/40) **reste peinte sous l'en-tête du Peaufiner** — son « FERMER » (`span.cb-mot`) tombe sur le titre (`.s2-titre`), recouvrement confirmé au doigt ; le **rond photo** de la page + (`.ph-photo-btn`, 34 × 34 à 332/230) reste peint sur la rangée AVANT. Le Peaufiner d'une fiche n'a aucun des deux. **Au produit, pas à la maquette** ; masqués (et déclarés) sur `PLANCHE-CERCLE-3.html`. Le mur du Cercle entre sur cet écran : à corriger dans le même lot. **✔ FAIT le 11 sept., nuit (`lot-CH64`)** : relevé nœud par nœud (`probe_haut_pp.py`), on retire, SEULEMENT Peaufiner ouvert (`#createSheet.pp-peauf`), le plateau de la page + (`.enh`, son « FERMER » tombait sur le titre) et le rond photo (`.ph-photo-btn`) ; au repos de la page + ils sont là comme avant ; le Peaufiner garde son propre en-tête et se ferme par son « ✕ FERMER » (qui referme la feuille, comme avant). `verif_64.py` : 16 / 16 (page + et gardé de côté, deux thèmes) ; prouvé sur l'app d'avant (plateau et rond visibles, « FERMER ∩ Promi », « FERMER ∩ appeler Mamie »). | ✔ |
| **65** | **Les champs à trois lignes et plus serrent leur contour** (Tom, 11 sept.) | Le début de la 1re et de la dernière ligne est à **3,0 / 2,5 px** de la courbe sur NOTE et COMMENTAIRES (fiche, page +), **7,4 / 5,8** sur DESCRIPTION et COMMENTAIRES d'une Nuée — contre 12,9 / 13,7 pour le champ à deux lignes et 21,9 pour un réglage. Cause : rayon = hauteur ÷ 2 (grammaire des contours) → une boîte de 118 est une pilule de rayon 59. Mesuré (`cale_lignes.py`, `planche3_captures.py`) : tenir l'écart de la norme par l'interligne seul ne laisse aucun air à trois lignes et est impossible à quatre. **Deux versions sur la planche 3 : T (l'interligne resserré) / P (rayon 30, le grand panneau).** **✔ FAIT le 11 sept. (`lot-CERCLE-MUR`) — Tom a pris P (Q202)** : rayon 30 sur NOTE, COMMENTAIRES (fiche, page +), DESCRIPTION et COMMENTAIRES d'une Nuée ; texte du milieu centré (46 / 46, 39 / 39) ; début des lignes extrêmes 14,1 / 13,5. `releve-S2` réécrit au niveau de la décision, prouvé rouge sur l'app d'avant. **Repris le 11 sept. (Q203) : la règle de CLASSE devient une règle de HAUTEUR, mesurée sur l'encre — rayon h ÷ 2 jusqu'à 94,5, 30 au-delà** (un seul propriétaire, `rayon()`). | ✔ |
| **66** | **PIÈCES JOINTES d'une Nuée : même champ, autres cotes** | La carte `#npFich` (92) écarte ses deux lignes (libellé à 14,8, bas à 60,3) : **6,35 px** de la courbe, contre **12,9** pour le même champ sur une fiche. Alignée sur la fiche dans la planche 3 (les deux versions). CLAUDE §5 : un composant commun ne se décline pas. **✔ FAIT le 11 sept. (`lot-CERCLE-MUR`, à la source dans `lot-NUEE-PEAUFINER`)** : libellé 23, bas 50,8, comme la fiche. `redteam_air` refigé : cette carte resserre de 14,2 (23,5 → 9,3) — c'est l'alignement, montré sur la planche 3. | ✔ |
| **67** | **LE TRAIT d'une Nuée : le libellé à 5,3 px de la courbe** | Carte `#npTrait` (118, libellé + rail de pinceaux) : le libellé est calé en haut d'une pilule de rayon 59. Vu en mesurant les champs, pas corrigé. **En partie le 11 sept. (Q203)** : la bascule du rayon passe la carte à 30 — le libellé n'est plus contre la courbe (encre à 1,6 en pilule). **Reste :** la rangée de pinceaux est à 14,25 du bord droit ; au rayon 30, son encre est à **11,1** du contour mesuré à l'écran (12,9 sur l'analyse hors écran), sous l'air des champs ouverts (15,19). Déclarée comme défaut connu dans `verif_seuil.py`, pas comptée. **✔ FAIT le 11 sept., nuit (`lot-CH67`)** : la rangée remonte de `bottom:14px` à 22 — la cote se calcule (≥ 20 pour tenir 15,19 au coin) et 22 est l'air du libellé en haut : la carte devient symétrique (24 / 24 vus du bord). Encre au contour **16,68** (11,14 avant) ; le toucher sur une pastille change toujours le trait. `verif_67.py` 8 / 8, prouvé sur l'app d'avant (4 rouges) ; l'exemption de `verif_seuil` est retirée. **Le troc, mesuré et dit :** la carte gagne son air au CONTOUR et perd 8 px d'air INTÉRIEUR — `redteam_air` a pris les quatre paires (`LE TRAIT → Plein` 19 → 11, `Plein → Sec` 15 → 7, deux thèmes) ; c'est le resserrement demandé par ce chantier, **référence refigée** (avant : `sauvegardes/air-reference-avant-ch67.json`). | ✔ |
| **68** | **Une note de trois lignes déborde sur sa ligne de visibilité** (vu le 11 sept., en calant les champs à trois lignes) | Peaufiner d'une fiche, NOTE avec un texte qui passe à trois lignes (« prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare ») : le `textarea` est PEINT sur **56 px** alors que sa `max-height` déclarée vaut **44**, son contenu fait 68 — la troisième ligne passe **sous « visible par Rachel »** (air 0,5 px, dernière ligne à −0,8 de la courbe), deux thèmes (`sauvegardes/audit-cercle/planche3_captures.py`, cas « note5 », captures `planche3/deborde_note5_*.png`). **Au produit.** Mon premier instrument l'avait caché : il ne comptait que les lignes sous la `max-height` déclarée — il compte désormais jusqu'au bord VISIBLE du champ. **✔ FAIT le 11 sept. (`lot-CERCLE-MUR`, Tom : « c'est le même problème de géométrie »)** : le champ grandit d'une ligne (22,5) par ligne de texte, le textarea montre toutes ses lignes ; à deux et trois lignes de texte : 15 d'air sous le libellé, 14,6 au-dessus de la visibilité (1,3 avant), écart constant 14,1 / 13,5. **Complété le 11 sept. (Q203, « c'est la même géométrie ») :** sur la PAGE +, la zone de la note est rebâtie sans cesse ; entre un rebâtissage et l'image suivante, la zone neuve restait à 118 avec trois lignes de texte (dernière ligne à 0,5 de la courbe, relevé `seuil_pilule.py`). Elle est désormais recalée dans la foulée de la mutation (micro-tâche), avant toute image — sonde d'observateur dans `verif_seuil.py`. | ✔ |
| **73** | **L'élan de l'Aura tombe à 0 quand les images approchent 100 ms** (vu le 11 sept., nuit, machine chargée) | `releve-aura` seul, quatre passes alternées sur deux versions de l'app (`sauvegardes/audit-cercle/journaux/aura_alt*.log`) : quand la médiane par image dépasse ~24 ms et que la plus longue image pendant l'élan atteint 83–100 ms (peintre 20 à 36 ms), la vitesse au lâcher sort à **0,00 rad/s** et le lancer ne comble plus le creux — sur l'app d'avant le lot du Cercle comme sur l'actuelle. À 50 ms (peintre 14 ms), 9,6 à 10 rad/s. **Soit le juge ne sait plus lancer sous charge** (le lancer est joué dans la page, cadencé — CLAUDE §8), **soit le produit perd l'élan sur un appareil lent** : c'est exactement ce que la mesure contre l'iPhone 12 (A13) doit dire. Non tranché. **⚑ PRIORITÉ (Tom, 11 sept., nuit) : « le chantier 73 doit être testé EN PREMIER quand tu auras l'iPhone 12 — avant la densité, parce qu'une sphère dense et morte ne vaut rien. Un téléphone lent tue le geste qui rend la sphère vivante. »** **✔ TRANCHÉ ET CORRIGÉ LE 12 SEPTEMBRE 2026 — SANS TÉLÉPHONE, et je dis où le substitut s'arrête.** **① LE « 0,00 rad/s » DU CHANTIER ÉTAIT MON INSTRUMENT.** Le lancer était joué dans la page, cadencé par `setTimeout` — qui se dilate avec le bridage : à ×4, ×6, ×10, le DOIGT ralentissait avec la machine (balayage de 100 ms devenu 474 ms, livré en UN mouvement). Même famille que le `mouse.move` de Playwright que le §8 dénonce déjà. Rejoué avec `Input.dispatchMouseEvent` du CDP — horodatage explicite par mouvement, envoyé depuis le processus navigateur, donc un doigt qui balaie 132 pt en 100 ms quel que soit le bridage : **11,00 rad/s (le plafond) aux douze essais, à ×1, ×4, ×6 et ×10**, et **sur la version d'avant aussi**. Avec un doigt normal, l'élan n'a jamais été perdu. **② MAIS LE DÉFAUT EXISTE, ET IL EST PIRE QUE CE QUE JE CROYAIS : IL NE DÉPEND PAS DE LA CHARGE, IL DÉPEND DE L'ÉCART ENTRE DEUX MOUVEMENTS.** La fenêtre de l'élan était figée à **90 ms** — cinq mouvements à 60 images/s, une hypothèse de machine rapide déguisée en durée. Dès que deux `pointermove` sont espacés de plus de 90 ms, le plus ancien sort de la fenêtre, il ne reste qu'un INSTANT — et un instant n'est pas une durée : `dtt` vaut 0 et la vitesse reste nulle. Mesuré (`sauvegardes/ch73/elan_images_lentes.py`, doigt CDP, regroupement éteint pour simuler Safari) sur la version d'avant : écart 16 ms → 11,00 · 60 ms → 11,00 · **120 ms → 0,00 · 200 ms → 0,00 · 320 ms → 0,00**, neuf essais sur neuf. **③ LA CORRECTION, en deux points, `lot-AURA-ORBITE` seulement.** (a) La fenêtre suit la cadence observée : `max(90, 3 × écart médian des derniers mouvements)` — **jamais moins que les 90 ms d'origine**, donc le cas rapide ne bouge pas d'un cheveu. (b) **Chaque mouvement porte SON pas de temps** (`DG.hD`), y compris le premier depuis le toucher : la vitesse se calcule sur la somme de ces pas, donc elle existe avec UN échantillon comme avec cinq. Après : écart 120 ms → **7,40** · 200 ms → **4,44** · 320 ms → **2,78** rad/s (trois essais identiques chacun) — et ces valeurs sont physiquement justes : le même balayage sur plus de temps, c'est un doigt plus lent. **④ CE QUE LA FENÊTRE PROTÉGEAIT EST INTACT — vérifié, pas supposé :** un doigt qui balaie vite puis TIENT IMMOBILE avant de lâcher ne lance pas. Lâcher immédiat → 11,00 rad/s ; immobile 120, 300 et 600 ms → **0,00**. **⑤ POURQUOI ÇA COMPTE POUR L'iPHONE, et c'est la vraie trouvaille :** Chromium regroupe les mouvements (`getCoalescedEvents`) et rend le paquet avec les horodatages d'origine — il CACHAIT donc le cas dur. **Safari n'a pas cette API** : sur iOS l'app ne voit qu'un mouvement par appel. Les mesures ci-dessus sont faites regroupement ÉTEINT, donc dans les conditions de la cible. **⚠ CE QUE LE SUBSTITUT NE REMPLACE PAS, et le test sur iPhone 12 reste à faire :** le GPU, la mémoire et la chauffe d'un A13 (le bridage CDP ne ralentit que le fil principal) ; le moteur de rendu de Safari ; et la cadence réelle à laquelle iOS livre les `touchmove` quand le fil est bloqué — c'est elle qui dira où l'on tombe dans le tableau du ③. Outils prêts : `elan_vrai_doigt.py` (doigt CDP sous bridage), `elan_images_lentes.py` (l'écart entre mouvements), `elan_sous_charge.py` (gardé pour mémoire, avec l'explication de son mensonge). Sauvegarde d'avant : `sauvegardes/app-avant-ch73.html`. | ✔ |
| **74** | **Des portes mènent au Cercle sans passer par un Promi** (Tom, 11 sept., nuit : « personne n'arrive sur le Cercle sans avoir rien planté […] Si tu trouves un chemin qui mène au Cercle depuis un état vide, note-le — c'est probablement lui qu'il faut corriger. ») | `sauvegardes/audit-cercle/portes_vides.py`, deux thèmes : **quatre portes** ouvrent l'écran qui vend sans qu'on règle aucun Promi — la porte de l'**accueil** (`#cercleTopBtn`), l'encart des **Réglages** (`#openPlusTop`), le verrou d'un **monde payant au Studio** (`#stLockCta`), le bouton de l'**aide de l'Aura** (`#ahCercleCta`) ; toutes visibles, prises au doigt. Le mur de la **page +** se rencontre en créant son premier Promi. Dans ce prototype, aucun chemin utilisateur n'atteint ZÉRO Promi (le démarrage neuf `promi_fresh` est rempli derrière par le jeu, chantier 71) : chez un vrai nouvel utilisateur, ce sont ces quatre portes qui mènent au Cercle depuis un état vide. L'écran qui vend sait l'afficher (rangée cachée, prix remonté — Q205). **À trancher par Tom : lesquelles doivent exister avant le premier Promi.** | [O] |
| **72** | **Des juges visent un Promi par son NUMÉRO — et les numéros du jeu changent d'un chargement à l'autre** (vu le 11 sept., nuit) | ⚠ **Corrigé le 11 sept. (nuit) — j'avais écrit que la fiche 126 était « passée ratée dans la soirée, son échéance tombée » : c'est FAUX.** « faire les crêpes » est ratée dès le jeu (`P(…,'rate')`, « À TENIR · 2 J ») ; ce qui change, c'est son NUMÉRO — 126 dans un chargement sur quatre, 142 dans les trois autres (`probe_ids.py`, chantier 71). Tout contrôle qui ouvre 126 en dur ne voit une fiche qu'une fois sur quatre. **`releve-fiche-personne`** (l. 243, `openDetail(126)`) : porte 8 « le disque de Rachel sur une fiche ouvre SA nouvelle fiche » rouge dans les deux thèmes, **à l'identique sur l'app d'avant le lot du Cercle** (`journaux/fiche_personne_avant.log`) — ce n'est pas un défaut du produit, c'est le juge. Mes propres outils (`verif_integration`, `verif_seuil`) choisissent désormais le premier Promi en cours adressé à quelqu'un, comme `releve-S2`. `releve-aura` vise aussi le Promi 139 (acquis 8 bis). **À faire :** que chaque juge choisisse sa fiche par ses PROPRIÉTÉS (et vérifie qu'il l'a trouvée), jamais par un numéro. Non corrigé dans ce lot : c'est une batterie, pas l'écran qui vend. **✔ FAIT le 11 sept., nuit** : dans les batteries, UN seul juge visait un numéro — `releve-fiche-personne` (porte 8). Réécrit au niveau de la même intention : la fiche de « faire les crêpes » adressée à Rachel (sinon le premier Promi planté pour Rachel), et le juge DIT s'il ne la trouve pas ; il attend l'ouverture comme une condition (jusqu'à 3 s) et dit le temps mis (mesuré 315 à 1 413 ms, jamais de disque rebâti sous le doigt). Original `sauvegardes/releve-fiche-personne-avant-72.py` ; prouvé par `SONDE_PORTE8=1` (le disque intouchable). Mes outils (`verif_integration`, `verif_seuil`) : même correction. (`releve-aura` « Promi 139, attendu 139 » compare à la dalle qu'il vient de toucher, pas à un numéro en dur.) | ✔ |
| **71** | **Les numéros du jeu de démonstration changent d'un chargement à l'autre** (vu le 11 sept., soir ; ⚠ ma première note parlait de « deux tableaux » : FAUX, corrigé) | Un SEUL tableau, `promises` (`let`, l. 2856 — **rien n'écrit jamais `window.promises`**, qui vaut `undefined`). Le jeu de la planche (`_jeuPlanche`, ≈ l. 20699 : `promises.length = 0` puis ses 16 Promi repoussés par la fabrique `P()`, qui numérote par un compteur `nid`) est rebâti à 400 ms — et, mesuré sur 4 chargements (`sauvegardes/audit-cercle/probe_ids.py`), il PASSE DEUX FOIS dans 3 sur 4 : `nid` finit à 157 (ids 141 → 156, « faire les crêpes » = 142) au lieu de 141 (ids 125 → 140, « faire les crêpes » = 126). Mêmes Promi, mêmes titres, **numéros décalés de 16**. D'où les « trois derniers plantés » 153–155 dans une page, 137–139 dans l'autre, et la fiche 126 qui n'existe qu'une fois sur quatre (chantier 72). **Pas cherché qui rappelle le jeu une seconde fois.** Et le démarrage neuf (`promi_fresh`) n'atteint jamais zéro Promi : le jeu se remplit derrière. **✅ 14 sept. : garde sur DOMContentLoaded, ids stables (126 sur 4 chargements).** | ✅ |
| **70** | **La page + rebâtit la liste de son Peaufiner sans cesse** (vu le 11 sept., en calant la note) | Sonde `sauvegardes/audit-cercle/sonde_pp_note2.py` : la zone de la note est un NŒUD NEUF à +100, +700, +1500 ms après une saisie, et encore au défilement — six zones en 2,5 s, sans aucun toucher. Le lot du Cercle suit (il recale dans la foulée), mais c'est du travail à chaque passe et une source de « deux propriétaires ». **Pas cherché qui rebâtit** (`peaufBati` et ses minuteries 90 / 280 / 650 ms sont les premiers suspects). Observation, non corrigée. **Conséquence mesurée le 11 sept. (soir) — un toucher perdu :** l'encart du mur est rebâti SOUS LE DOIGT, entre l'appui et le relâcher ; le clic part sur un autre nœud et l'écran du Cercle ne s'ouvre pas. `sauvegardes/audit-cercle/repro_encart_v4.py`, 20 touchers par thème : app d'avant le lot du seuil **38 / 40** (les deux ratés : encart DÉTACHÉ pendant le geste), app du lot **40 / 40** ; pris aussi par `verif_integration` (1 fois, en clair). Défaut du produit, tiré au hasard, antérieur au lot. **✔ FAIT le 11 sept., nuit** : la cause — `tout()` (le repeintre de la page +) appelle `peaufBati()` à chaque repeinte, et `peaufBati` VIDAIT la liste puis la rebâtissait, sans que rien n'ait changé. Désormais il calcule la SIGNATURE de ce qu'il va bâtir (nature, titre, à qui, échéance, Nuée, fichiers, compagnon, membres) et ne rebâtit que si elle change ou si un contrôle emprunté est reparti (comparer avant d'agir, §8). `verif_70.py`, deux thèmes : **0 rebâtissage** en 3 s de repos + 3 s de défilement (**6 + 6** avant), l'encart ouvre le Cercle **20 / 20** (des « introuvables » avant), une vraie modification rebâtit toujours (le titre suit), le mur posé une fois. | ✔ |
| **62** | **Page + : l'aide sous la phrase passe sous la rangée des pinceaux** (relevé le 11 sept., à l'intégration de la fiche d'une personne) | `.ph-hint` suit la hauteur de la phrase, `#csPinceau` est fixe à y 651 : dès que la phrase prend une ligne, ils se recouvrent. **Préexistant** sur le Chiche par le chemin normal (aide 636 → 685, pinceaux 651 → 695) ; sur le Promi dès que la phrase porte une personne — c'est ce que fait « + Planter un Promi » depuis la fiche d'une personne (« à Rachel » : l'aide descend de 26 pt). `redteam_superpo` ne le voit pas (il ne compare pas un texte à une rangée de réglage). La parade connue : la cote se dérive du bas réel de la phrase (CLAUDE.md §8, « un espacement qui revient »). || ✔ 13 sept. |
| **61** | **Les libellés des cartes et le §6 — CHANTIER DE POLICES, sur tout le produit** (Tom, 11 sept.) | Le sens d'une carte d'Index (« à Rachel », « avec +4 ») et d'un bandeau du Fil (« Marion a relevé ») est en **Bricolage 600** (16 et 14 px, mesuré). Le §6 réserve Bricolage aux « titres, libellés de section » en **700/800** et donne l'interface à Apfel. **Soit le §6 est incomplet** (il ne prévoit ni le libellé d'une carte, ni la graisse 600), **soit les cartes ont dérivé.** À trancher plus tard, sur l'ensemble du produit — pas sur un écran. En attendant, **la fiche de la personne suit les cartes** (Bricolage 600 sur ses libellés), pour ne pas créer un troisième système. | ▸ |
| **60** | **« à le groupe »** — défaut de grammaire PRÉEXISTANT (Tom, 11 sept. : « note-le ») | Le sens d'une parole adressée à une Nuée s'écrit « à le groupe » au lieu de « au groupe » : sur la carte d'Index (« reprendre l'arrosage automatique ») et dans les rangées de la fiche d'une personne (`relLabel`, l. 3402 ; le mot de la carte vient de `motQui`). Relevé à l'audit de la fiche de la personne. **✅ 14 sept. : « au groupe » (`_aQui`).** | ✅ |
| **58** | **L'OMBRE DE DALLE ÉCRIT SUR LES DOUZE ÉCRANS À CHAQUE IMAGE — 27 % DU FIL PRINCIPAL** · **PRIORITAIRE** (Tom, 10 septembre 2026) — probablement la plus grosse trouvaille de performance du projet | `frame()` (script anonyme ≈ l. 8917 d'`app.html`) anime l'ombre de dalle des écrans `.tuto-fond`, `#createSheet`, `#settingsScreen`. Elle tient pour « visible » tout élément dont **`offsetParent` n'est pas nul** — or un écran fermé n'est pas en `display:none`, il est **glissé hors champ** et garde son `offsetParent`. Elle écrit donc `--gx`, `--gy`, `--grot` (variables **héritées**) sur **les douze** écrans, fermés compris, **à chaque image** ; sa lecture d'`offsetParent` à l'image suivante force le recalcul de style de milliers de nœuds cachés. **Mesuré au profileur (CDP, échantillon 0,5 ms), pendant l'Aura : 27 % du temps du fil principal — autant que tout le peintre de la sphère ; 1,6 % avec ces écritures ignorées sur les écrans cachés (24 480 écritures en 20 s).** Symptôme vécu : l'élan de l'Aura figé par des images de 267 ms (50 ms après). **Le coût existe partout** (Toile, Fil, Index, fiches), pas seulement sur l'Aura. **Ce qui est fait :** le lot de l'Aura (`lot-AURA-ORBITE`) n'ignore ces écritures que sur l'Aura et sur les écrans cachés dessous tant qu'elle est ouverte — la boucle elle-même n'est PAS touchée (règle existante d'un autre lot). **Ce qui reste :** corriger la boucle — un écran est visible s'il porte `.show`, jamais sur sa géométrie (CLAUDE.md §8). À prouver par un profil avant/après sur l'accueil (Toile), le Fil et l'Index ; batteries en série. Outils prêts : `sauvegardes/aura-orbite-lot/profil_elan.py`, `profil_taches.py`. Voir QUESTIONS.md Q180. **✔ FAIT LE 12 SEPTEMBRE 2026 — et c'était bien pire que 27 %.** La boucle suit désormais LES CLASSES QUE LE CODE POSE : `ouvert(e) = e.classList.contains('show') || e.classList.contains('in')`. Plus une seule lecture d'`offsetParent`. **⚠ « .show » SEUL AURAIT ÉTEINT L'OMBRE SUR LE FIL, et je l'ai vérifié AVANT d'écrire la parade** (`sauvegardes/ch58/equivalence_show.py`, 8 portes × 2 thèmes, 12 nœuds) : `#feedView` est VISIBLE sans porter `.show` — il s'ouvre avec la classe **`.in`** et `display:''`, et l'app le lit elle-même comme ça (≈ l. 19208). Un seul désaccord sur 96 relevés, et c'était celui-là. D'où les deux classes. **CE QUE ÇA VALAIT, au profileur (CDP, échantillon 0,5 ms, 8 s par écran — `sauvegardes/ch58/profil_ombre.py`) :** la part du fil principal passée dans `frame` tombe de **65,87 % à 0,00 %** sur l'accueil (la Toile), de **72,03 % à 0,09 %** sur le Fil, de **64,82 % à 0,01 %** sur l'Index, de **67,76 % à 0,13 %** aux Réglages, et de 2,09 % à 0,02 % sur l'Aura (où `lot-AURA-ORBITE` la neutralisait déjà). **Les 27 % mesurés le 10 septembre étaient le chiffre de l'Aura protégée : partout ailleurs, cette boucle prenait DEUX TIERS du fil principal.** **LES ÉCRITURES, comptées au piège sur `style.setProperty` (`sauvegardes/ch58/preuve_ombre.py`, 1,2 s par écran) :** sur les écrans FERMÉS, **1 650 à 7 227 → 0** ; sur l'écran OUVERT, **inchangé** (216 à 660) — la correction n'éteint rien de ce qui sert. Le Fil garde ses 648/657. **⚑ ET UNE TROUVAILLE EN PASSANT, mesurée, non corrigée :** ce `::before` est **masqué sur 8 des 12 écrans**, et par DÉCISION (page + et Réglages : « on le remplace par un canvas qui porte la VRAIE dalle du monde actif » ; Aura, Fil, fiche personne, écran qui vend). Il ne reste affiché que sur **shareScreen, arrangeSheet, auraHelp, langScreen** — et même là, deux captures à 900 ms d'écart donnent **0,00 % de pixels changés, écart max 1 niveau** : son mouvement ne se voit pas. La boucle animait donc, aux deux tiers du fil principal, une ombre que presque rien n'affiche. **Je ne l'ai PAS supprimée** — §9 : on ne retire pas un élément masqué sans savoir pourquoi il l'est, et le §4 règle 6 laisse la question ouverte de ce qui doit vivre derrière ces quatre écrans. Elle coûte maintenant 0,0 %. ⚠ Le contournement de `lot-AURA-ORBITE` (l'enveloppe de `style.setProperty`) est devenu redondant : **laissé en place**, il ne fait que supprimer, il n'écrit rien — le retirer serait toucher un lot qui marche pour rien. Sauvegarde d'avant : `sauvegardes/app-avant-ch58.html`. | ✔ |
| **76** | **LE MOTEUR PEINT DU CRÈME ENTRE LES MOTIFS — jusqu'à 76 % de la surface d'une dalle** (Tom, 12 sept. : « note-le comme chantier. 76 % sur Gravure, masqué par le recouvrement mais pas supprimé. Ça ressortira le jour où la densité baissera. ») | Mesuré à l'intégration de l'écran qui vend, en thème CLAIR, sur une dalle rendue par `Toile.dalleTrame` seule (sans rien derrière) : la part de pixels à la couleur du fond crème `#F4EEE1`, **à l'intérieur** de la cellule — **gravure 76,4 %** · braille 71,7 % · sillons 70,1 % · terrazzo 64,8 % · touffe 46,7 % · mosaïque 34,1 % · encre 24,9 % · **pixel 0 %**. Ce n'est pas une transparence : le moteur PEINT le crème entre les traits du motif, donc rien posé dessous ne remonte. Conséquence : une dalle de Gravure ou de Braille est à trois quarts crème et ne « couvre » pas — sur l'écran qui vend, le vide n'est tombé à 1–6 % que parce que **140 poses se recouvrent** ; le crème est masqué par la dalle du dessus, pas supprimé. **Dès que la densité baissera** (un cadre plus grand, moins de poses, un appareil lent qui en pose moins), il reparaîtra. **⚠ La cause est DANS LE MOTEUR (§9) : rien à corriger sans autorisation explicite de Tom.** Pistes non essayées, à trancher avec lui : ① le motif peint sa couleur de fond seulement là où la cellule est pleine (retouche moteur) ; ② les mondes de ligne (gravure, braille, sillons) reçoivent un fond tiré de la palette au lieu du crème ; ③ on l'assume et l'écran qui vend garde sa densité comme CONTRAT (c'est déjà le cas : `verif_cercle.py` refuse plus de 8 % de fond). **✅ FERMÉ le 14 sept. — LE DIAGNOSTIC DE DÉPART ÉTAIT FAUX.** Le moteur ne peint pas de crème : les creux de Gravure, Braille et Sillons sont TRANSPARENTS (76,1 · 76,7 · 79,8 %% d'une dalle rendue seule, crème opaque ≈ 0). Le crème mesuré le 12 sept. était le fond de l'écran qui vend, vu à travers. Corrigé À L'ENDROIT DU DÉFAUT (Tom) : sur l'écran qui vend seulement, ces trois mondes sont posés sur leur silhouette dilatée, peinte d'un ton de leur couleur (`Toile.colorOf`). Moteur, Toile et cartes inchangés — une dalle reste identique partout. `verif_cercle` 89/89. | ✅ |
| **77** | **⚑ PORTAGE SWIFT · PRIORITAIRE — LE GESTE SE PERD QUAND LES ÉVÉNEMENTS S'ESPACENT, ET LE BANC CHROMIUM LE CACHE** (Tom, 12 sept. : « c'est exactement ce qui casserait sur iPhone sans qu'on le voie ici. Note-le comme chantier prioritaire pour le portage Swift. ») | **Deux faits mesurés, et ils vont ensemble.** **① L'élan tombe à ZÉRO dès 120 ms entre deux mouvements** — pas sous la charge, sous l'ESPACEMENT. La fenêtre de vitesse était figée à 90 ms (cinq mouvements à 60 images/s : une hypothèse de machine rapide déguisée en durée) ; au-delà, le mouvement précédent en sort, il ne reste qu'un instant, et un instant n'est pas une durée. Mesuré au doigt CDP horodaté (`sauvegardes/ch73/elan_images_lentes.py`) : écart 16 ms → 11,00 rad/s · 60 ms → 11,00 · **120 ms → 0,00 · 200 ms → 0,00 · 320 ms → 0,00**, neuf essais sur neuf. **Corrigé dans le prototype** (chantier 73) : la fenêtre suit la cadence observée (`max(90, 3 × écart médian)`, jamais moins que 90) et **chaque mouvement porte son propre pas de temps** — la vitesse existe donc avec UN échantillon comme avec cinq (120 → 7,40 · 200 → 4,44 · 320 → 2,78 rad/s). **② CHROMIUM CACHE CE DÉFAUT, SAFARI NON.** Chromium regroupe les `pointermove` (`getCoalescedEvents`) et rend le paquet **avec les horodatages d'origine** : sur le banc, l'app reçoit 7 échantillons dans 100 ms même à ×10 de bridage, et tout paraît sain. **Safari n'a pas cette API** — sur iOS l'app ne verra qu'UN mouvement par appel. C'est pour ça que la mesure ci-dessus se fait **regroupement éteint** (`PointerEvent.prototype.getCoalescedEvents = function(){ return []; }`). **CE QUE LE PORTAGE SWIFT DOIT FAIRE, et c'est la raison de ce chantier :** en UIKit, `UITouch` porte son `timestamp` et `coalescedTouches(for:)` rend les touches intermédiaires — **les deux doivent être utilisés**, jamais `CACurrentMediaTime()` au moment du traitement. Et toute vitesse (élan de l'Orbite, défilement inertiel, tout geste lancé) se calcule sur la somme des pas de temps réels, avec une fenêtre qui suit la cadence — **jamais une fenêtre en millisecondes calibrée à 60 images/s**. **À VÉRIFIER SUR L'iPHONE 12 (A13), en premier :** à quelle cadence iOS livre réellement les `touchmove` quand le fil est bloqué — c'est elle qui dit où l'on tombe dans le tableau du ①. Le bridage CPU du CDP ne remplace ni le GPU, ni la mémoire, ni la chauffe d'un A13. | ▸ |
| **78** | **AUCUNE MODIFICATION NE SURVIT AU RECHARGEMENT — le jeu de démonstration écrase la sauvegarde** (vu le 13 sept., lot de la couleur au Cercle ; Tom : « plus grave que la couleur ») | Mesuré (`scratchpad/sonde_persist.py`) : un titre changé puis `saveState()` est bien écrit dans `localStorage.promi_state` ; au rechargement, `loadState()` le relit, puis `lot-JEU-PLANCHE` (`jeu()`, l. ~20860) vide et repeuple **sans condition** `NUE`, `NUEEMEM`, `promises` et `FEED`. Le jeu est une décision (Tom, 20 août : peupler l'app avec les Promi des planches pour les comparer) ; **qu'il efface ce que l'utilisateur a fait n'a jamais été décidé**. Tout est perdu : titres, plantations, Nuées, couleurs, états tenus. ⚠ Beaucoup de juges supposent le jeu présent à chaque chargement (titres, « 15 paroles · 2 Nuées ») : la correction (ne poser le jeu que s'il n'y a pas de sauvegarde, ou derrière un interrupteur de démo) doit être décidée par Tom et se prouver sur ces juges. **⚑ Tranché et fait le 14 sept. (Tom) : le jeu ne se charge que s'il n'y a pas de sauvegarde** (`window._etatRelu`, posé par `loadState` au chargement). | ✅ |
| **79** | **⚑ PRIORITAIRE — UN ABONNÉ NE GAGNE RIEN SUR L'AURA** (Tom, 14 sept. : « c'est l'argument principal de l'écran qui vend : « L'autre moitié de ta Toile ». C'est un vrai manque. ») | Ce que le Cercle ajoute à l'Aura n'est pas dessiné (Q196.2) : graphes, évolution, réciprocité n'existent pas sur l'Orbite. Mesuré le 14 sept. : l'Aura payante montre exactement la même chose que la gratuite. La fiche d'information n'annonce plus rien pour le Cercle côté Aura (seulement ses réglages et ses designs). À concevoir DANS l'Aura, puis à montrer voilé sur l'écran qui vend. **✅ 14 sept. : intégré — les deux moitiés (§2.9 corrigé) + « Ce qu'on t'a tenu », voilés en gratuit. Reste le chantier 80 (que la rangée se remplisse).** | ✅ |
| **80** | **L'ÉCHANGE — QUE LA RANGÉE « CE QU'ON T'A TENU » SE REMPLISSE** (Tom, 14 sept. : « c'est le vrai sujet ») — conception d'échange, pas du dessin : se décide avant de dessiner, **ne se fera pas dans le prototype** (pas de serveur) | Une parole envers toi n'existe que si l'autre l'a plantée. Cinq sources, par ordre de poids : **① « Promets-moi »** (la demande existe : tu demandes, l'autre répond, sa promesse arrive chez toi) · **② le Chiche relevé** (l'autre tient sa moitié) · **③ la Nuée** (ce que les membres promettent au groupe) · **④ recevoir sans compte** — rejoint une décision ancienne : **un demi-trait ne se diffuse pas, il s'envoie, et la seule façon d'y répondre est de tracer** ; celui qui répond fait le geste central avant d'avoir rien lu, son tracé devient sa première parole — **le partage devient l'acquisition** · **⑤ le partage et l'invitation**, porte d'entrée. **① et ④ sont ceux qui comptent**, les autres suivent. Règle protectrice (Q215·2) : celui qui tient déclare, tu reçois — jamais l'inverse. | ▸ |

---

## 5. Fonctionnalités décidées, non codées

| # | Chantier | Notes |
|---|---|---|
| **15** | **Demande de Promi** | état en attente, réception, acceptation, expiration silencieuse à 1 mois. **Le plus gros morceau du produit.** Une batterie existe déjà : `redteam_demande.py` |
| **16** | Onboarding et tutoriel | à refaire entièrement |
| **17** | Paiement | feuille native · prix TTC, durée et reconduction dans l'encart (§7.5) |
| **18** | Les trois fonctions Cercle | Promi récurrent · en étapes · la mémoire (« il y a un an… ») |
| **19** | Filtre « pour toi » dans le Fil | gratuit |
| **20** | Retirer une personne | disque retiré, Promi conservés, **aucune notification** |
| **21** | Le `+` de la fiche Nuée | remplacer « ✦ Planter un Promi dans la Nuée » |
| **33** | Trois dalles **distinctes** dans les tuiles de Créer | aujourd'hui c'est la même dalle en trois couleurs — pas crédible |
| **34** | Dalle de Nuée **en triple**, étalée | trois exemplaires décalés, lisibles à 40 px de côté. Une Nuée *est* une dalle, et les Promi qu'elle contient créent les leurs |
| **57** | Monde de plantation par dalle (Nuée) | le bandeau de la fiche Nuée rend aujourd'hui **toutes** les dalles dans le monde **courant** (`Toile.dalleTrame` → `curWorld`, app.html l.4515+). Le **per-plantation** — chaque dalle au monde de qui l'a plantée, qui *contraste* si le Studio a changé (c'est voulu) — est un **futur Firebase** (le code le dit en commentaire). **Décidé : on garde le monde courant pour l'instant.** |
| **59** | **Écarter du sol la couleur d'une dalle, à la plantation** (Tom, 10 septembre 2026) — **non urgent, mais ne doit pas se perdre** | **Décision : quand une dalle est trop proche du sol, sa couleur doit être écartée à la plantation.** Le défaut : la couleur d'une dalle est tirée au hasard (`cc()`, `Math.random` — code de la Toile) ; quand le tirage tombe près de la couleur de nature du sol, la dalle ne se lit plus (bleu sur bleu). Mesuré sur la sphère de l'Aura : sur 10 chargements, **6** portent au moins une dalle sous le plancher (ΔE 15) ; **12 dalles sur 99** relevées ; la pire à **ΔE 8,0** (cas réel, rien de posé — `preuve_cas_reel.py`). Q192 pour le détail. **Touche la plantation** (la fabrique `P()` fige déjà le monde d'un Promi) **et peut-être le moteur** (§9 : demande explicite). **En attendant, `releve-aura` rougit en nommant la dalle** — c'est ce qu'on lui demande, on ne le desserre pas. **⚠ Repris le même jour (Tom) : c'est un problème de CONCEPTION, pas de tirage** — le sol bouge : c'est la nature la plus présente parmi les Promi tenus (`natureMaj`), il change quand la majorité change. *Nuance mesurée dans le code : il ne prend que TROIS valeurs (bleu, framboise, mauve).* **Piste préférée de Tom : « le peigné » — la matière fait le travail, sans toucher ni au sol, ni aux dalles, ni à leur mémoire. MESURÉE, elle ne suffit pas** (`sauvegardes/aura-orbite-lot/clair/peigne/`, copie expérimentale jamais insérée) : le peigné EXISTE DÉJÀ — chaque île a son épi (`_v_peint.js` l. 474–489) ; sur 6 dalles rouges réelles, l'épi actuel apporte **+3,7 à +5,0** de ΔE (sans épi 4,6–8,6 → avec 9,6–12,4) ; un poil couché à 90° du peigne n'apporte **rien de plus** (7,1–10,8). Le pire, « rapporter le livre » en sombre : 4,6 → 9,6 → 9,7. **Aucune des 6 ne passe le plancher. Autre chose à trouver** (Tom : « on regardera autre chose plutôt que de maquiller »). Voie écartée d'avance : le lustre des caresses (`_PO`) — une décision inscrite dans le peintre (l. 467–472) le réserve à la mémoire de la main. **⚑ VOIE RETENUE (Tom, 10 sept.), dans ses mots : « la mémoire du monde est préservée, seule la teinte cède, et ça ne touche que les dalles concernées. » On n'y touche pas maintenant.** ⚠ Tom l'a appelée « ta piste 4 » et « C60 » : je n'ai proposé aucune quatrième piste, et le chantier est celui-ci, le n° 59 — la voie est la sienne, notée telle quelle. À préciser à l'ouverture : quelle teinte, vers où, à partir de quel écart (le plancher du juge, ΔE 15), et l'exception au §4 qu'elle suppose (sur la Toile, la dalle garde son monde — ici, seule sa teinte céderait). **◐ FAIT EN SOMBRE LE 12 SEPTEMBRE 2026, PAS EN CLAIR — et le clair est déclaré avec son chiffre.** Corrigé HORS MOTEUR (§9 : `cc()` n'est pas touché), hors sol, hors mémoire du Promi : la dalle RENDUE est remappée sur une autre couleur DE SA PALETTE (celle du Studio, donc du même monde), chaque pixel gardant sa clarté — la forme ne bouge pas, c'est l'idiome de Q30. `lot-AURA-ORBITE` seulement, et seulement sur la SPHÈRE (la moisson n'est posée sur aucun sol). **Mesuré, 10 chargements par thème** (`sauvegardes/ch59/mesure_plancher.py`, l'instrument du juge : ΔE des couleurs moyennes avec l'île et sans elle, vue figée) — **sombre : 0 dalle sous le plancher sur 10 chargements, contre 7 sur 8 avant** (5 chargements fautifs sur 8) ; **clair : 4 dalles sur 10 chargements, comme avant — inchangé.** **⚑ TROIS CRITÈRES ESSAYÉS, DEUX JETÉS SUR LA MESURE, et c'est la leçon du chantier.** ① l'écart de couleur entre la dalle et le sol, avant le peintre : le rapport à ce qu'on mesure À L'ÉCRAN va de **×0,06 à ×13** (30 couples par thème) — une dalle à 48,8 du sol sort à 5,0 à l'écran, une autre à 23,8 sort à 26,4. **Il ne prédit rien.** ② la part PLEINE de la dalle (le vide se peint en sol) : le tiers le moins lisible remplit 65 %, le tiers le plus lisible 68 % — **aucune corrélation.** ③ **LE MASQUE, après `batIles` :** chaque pixel de dalle transparent garde l'indice 0, et l'indice 0 EST LE SOL (`TCOL[0]=o.sol` dans le peintre) — une île est un MÉLANGE de sa dalle et du sol dans la proportion de son masque. Rapport masque→écran : **médiane 0,96** dans les deux thèmes. C'est le bon instrument : on bâtit, on mesure sur le masque, on fait céder les seules îles sous le plancher, on rebâtit (3 tours au plus, et un tour qui ne gagne rien est le dernier — sans cette sortie la boucle rebâtissait 4 fois pour rien). **⚑ NI MENTHE NI TERRACOTTA (§3).** Première capture : la couleur la plus éloignée du sol bleu EST le terracotta de la palette — **trois îles sur cinq y passaient**, et la légende « ● à tenir » est juste dessous, dans la même couleur. La sphère se mettait à parler le langage des états. Les deux couleurs d'état sont exclues des candidates, comme Tom l'a tranché pour l'accent de l'écran qui vend (`sauvegardes/ch59/apres_dark.png` contre `final_dark.png`). **⚑ POURQUOI LE CLAIR N'EST PAS FAIT, mesuré :** ① le rapport masque→écran y va de **×0,18 à ×6,97** — l'instrument n'y prédit rien, donc il ne peut pas piloter de correction ; appliquée quand même, elle fait passer le compte de **4 chargements fautifs sur 8 à 6 sur 8**. Un instrument dont on a mesuré qu'il mentait ne décide de rien. ② Il faudrait viser 15/0,36 ≈ **42** sur le masque, et **la palette d'un monde ne le permet pas** : lilas, bleu, pervenche sont de la famille du sol, et la seule assez loin est le terracotta, interdit. Essayé : les cinq îles cèdent à chaque tour et rien ne converge (restes [5,5,5,5]). **Le résidu du clair est le lavage de la peau pâle — la question ouverte Q182, pas le tirage de la couleur.** **⚑ ET C'EST RÉGLÉ LE MÊME JOUR, PAR LE SOL, PAS PAR LES DALLES — Tom a tranché Q210 : A.** En clair, le poil du sol s'assombrit (la nature ×0,38, sa teinte gardée) et la peau va au crème du corps : **0 île sous le plancher sur 8 chargements, la plus faible à 20,6** (4 sur 10 avant). Aucune dalle n'est touchée en clair — la cession de teinte reste bornée au SOMBRE. Le degré est mesuré sur 5 pages et 25 îles (`sauvegardes/q210/balaye_sol.py`) : ×0,80 ne règle rien (4/25), ×0,44 tient de justesse (15,8), ×0,38 tient avec la marge du sombre (18,1). **Ce que ça coûte :** l'écart boule ↔ page passe de 84 à 116 — la cote du juge est RECENTRÉE sur la nouvelle décision (§7), tolérance et planchers inchangés. Détail complet et voie de repli : **QUESTIONS · Q210**. Avant/après à l'œil : `sauvegardes/ch59/final_light.png` contre `sauvegardes/q210/livre_light.png`. **⚠ CE QUI RESTE EN SOMBRE :** la cession décide sur le masque, dont le rapport à l'écran descend à ×0,48 — sur les 8 derniers chargements, **1 dalle est encore passée sous le plancher (13,7)**. Très loin des 7 sur 8 d'avant, mais ce n'est pas une garantie. Sauvegarde d'avant : `sauvegardes/app-avant-ch59.html`. |

---

## 6. Dette de cohérence

| # | Chantier | Détail |
|---|---|---|
| ~~**41**~~ | ~~Nettoyer le code mort~~ | **ANNULÉ — passé en interdit, voir §10.** L'addendum v6 le recommandait « par lots de dix ». `CLAUDE.md` l'interdit, et il a raison : **cinq tentatives ont produit jusqu'à 6 384 écarts.** Retirer une règle décale l'ordre des suivantes dans la cascade. Le code mort reste, on écrit dans un bloc neuf. *(Le n° 38 de l'addendum était le même chantier, numéroté deux fois.)* |
| **55** | **La palette des traits — décalage 150°** | **[O] et bloquant.** Laissé ouvert dans `CLAUDE.md §3` et `DECISIONS.md B1/E1`. **Il bloque la validation visuelle de toutes les fiches** : tant qu'il n'est pas tranché, on ne peut pas dire si une fiche est juste. Personne n'a le droit de décider seul |
| **56** | **La liaison phrase → formulaire de la page +** | passe par `dispatchEvent` : **casse en silence** si un champ change de nom, et **aucune batterie ne l'attrape**. Risque de régression invisible. À couvrir par un test avant tout lot qui touche la page + |
| **42** | Écart gratuit / Cercle | les blocs `prem-only` ne correspondent pas au §7.2 — à reprendre bloc par bloc. 11 en HTML, 4 en CSS |
| **43** | Alignement et actualisation des six écrans | Index, Fil, Partager, Aura, Toile, fiche : cohérence des gabarits **et rafraîchissement immédiat** |
| **45** | Fil et Index dans le dock | ◐ **fait à moitié.** Reste : retirer la ligne « Fil d'actu » de l'Index (le doublon subsiste) · rapprocher l'Index de la Toile dans l'ordre · vérifier le dock à six boutons sur un vrai écran |
| **46** | **Mutualiser le trait** page + / fiche | nouveau — né du lot 1 (§2) |
| **47** | Fusion des surcharges de la page + | §47.4 — quatorze blocs se neutralisent |
| **50** | **Rendre le contrôle du design déterministe** | **priorité absolue** — retirer les deux lignes Google Fonts (Fraunces est embarqué, graisse 600, la seule utilisée) et attendre `document.fonts.ready` avant toute mesure. Tant que ce n'est pas fait, aucun lot n'est vraiment validé (§1.4) |
| **51** | Convention pour `redteam_toile` | oscille 14–16 sur le contrôle « Mes Promi : les intitulés restent » — même cause que le 50, à revérifier après |
| **57** | **Réécrire le contrôle « l'anneau est peint à sa nouvelle place »** (`redteam_geste`) | ▸ ouvert. Sonde pixel à **seuil absolu** sur le **fond Toile animé de l'écran Partage** (shCanvas, échantillons à 1,3 s) → **oscille 12↔13/13**. Deux échecs de suite ne prouvent PAS une régression (le dessin de l'anneau est correct : sonde isolée +1513 stable, `drawEmblem`/`drawKRing` inchangés). **À réécrire :** comparer l'anneau à **sa propre référence** (avant/après), comme la convention Toile, au lieu d'un seuil absolu. Même famille que §51. |
| **52** | Un `\n` littéral parasite | en haut à gauche, **hors du cadre du téléphone** — nœud texte perdu dans le HTML. Préexistant |
| **53** | Le libellé du trait en sens « Promets-moi » | dit encore « glisse pour planter → » alors que le bouton disait « Demander ce Promi ». **[O]** quel verbe ? |
| **54** | Le trait de la page + ne s'ouvre pas au toucher | la fiche l'étend à 340 px, la page + reproduit le repos seulement. Le geste plante quand même (validation aux 2/3). **[O]** veux-tu l'expansion ? |

---

## 7. Décisions en attente — personne ne tranche seul

| # | Sujet | Question |
|---|---|---|
| **23** | Pointillé de la Toile | le déplacer de « à rattraper » vers « brouillon » ? |
| **24** | **Animation de Nuée** | direction jamais arrêtée. Ouvert depuis juillet. Tu la trouves ennuyeuse — il faut une direction avant toute ligne de code |
| **25** | **Monde Éclats** | moodboards A→F revus, choix non tranché. Le code `Rblok` est conservé, le monde est retiré de la table du Studio (vestige) |
| **26** | Paiement hors application | **avis juridique requis.** Ne pas décider sur la base d'un document écrit par une IA |
| **44** | Titre du Studio à 24 px | (aussi en §4) |
| **A** | Aura — direction « Le Calage » | la mesure devient la DA. **Retenue par le chat de design, jamais codée.** §57 et §58 en ont porté une partie (le % en signature, le Noyau ne porte que le mot) |
| **B** | Les trois mots du barème | `net / vibré / flottant` **contre** `harmonyWord()` qui existe déjà : *rayonnante · solide · installée · naissante · à tisser*. Deux familles de mots, une de trop. Avis du chat de design : assumer deux registres — l'encre pour toi, le tissage pour les liens. **Non tranché** |
| **C** | Partager — planche de tirage + passe-partout | croix de repérage, barre de contrôle, filigrane composé en marge comme une note manuscrite. **Non codé** |
| **D** | Teinte de la fiche par la couleur du Promi | le `::before` était du code mort (`content:none`, md5 identiques). À refaire proprement via le paramètre `tint` qui existe déjà, ou à abandonner |
| **E** | Ordre des mondes — Terrazzo en dernier | décidé : il reste payant mais passe en dernier. **À vérifier dans la table du Studio** |

**Verrouillé au passage [V] — la clause de réciprocité :** la réciprocité se lit
**en lien, jamais en classement de personnes**. Pas de podium dans une Nuée, pas
de pourcentage nu à côté d'un prénom, aucune notification « X ne t'a pas tenu
parole ». Conséquence de dessin : **les personnes s'affichent en grille
d'anneaux, jamais en liste de barres** — une liste de barres est un classement
même quand on ne le veut pas.

**Verrouillé [V] — la page + (lot 4-5) : Version B, un seul écran qui glisse.**
Pas deux écrans. Départ **fond encre + cartes de choix seules** ; au choix d'une
nature, le **fond vire vers la couleur** et la **phrase apparaît en dessous** —
on descend de la question vers la réponse, la transition porte le sens et
économise un geste. Le choix reste atteignable en remontant. **Version A (deux
écrans) annulée.** Détail dans `PARCOURS.md §2`. Reste à finir (lot 5) : la
grappe de dalles en tête (moteur, disposition du bandeau Nuée), le glissement
encre→couleur, la teinte des dalles de cartes.

---

## 8. Documentation restante

| # | Manque |
|---|---|
| **28** | Cotes du Fil, de la recherche d'Index, du sceau de l'Aura |
| **29** | États d'erreur et de chargement de chaque écran |
| **30** | Textes de l'onboarding — après le n° 16 |
| **31** | Écrans de paiement — après le n° 17 |
| **32** | Accessibilité mesurée au-delà des contrastes |
| **48** | **Corriger `PARCOURS.md`** avec les mesures du §2 — nouveau |
| **49** | **Fusionner l'addendum v6 et `ETAT-DES-LIEUX.md`** : le document décrit la v467, l'app est à la v592 — nouveau |

---

## 9. Ordre recommandé

> **⚑ L'ORDRE FIXÉ PAR TOM, 11 septembre 2026 — il prime sur le tableau ci-dessous :**
> **63 · le Cercle · 59 · 62 · 61 · 60 · 58 · le téléphone.**
> *« Le Cercle passe avant les chantiers de fond. C'est le seul écran du produit jamais refait, et c'est celui qui porte
> le revenu. Les chantiers 58 à 63 sont des dettes réelles, mais aucune n'empêche d'utiliser l'app ; le Cercle, lui,
> manque. »* **63 d'abord**, parce qu'il rend le lot de la fiche d'une personne incomplet. **Le Cercle : audit d'abord**,
> comme pour le partage et la fiche d'une personne — il porte du revenu, rien ne doit se perdre. **Le téléphone** ne se
> lève pas ici, mais ce n'est pas une formalité de fin : c'est le seul point qui peut remettre en cause un choix de
> conception (si le palier de 110 000 poils ne tient pas sur un iPhone, c'est la sphère qui change, pas un réglage).
> Le tableau ci-dessous est l'arriéré plus ancien, non revérifié (voir ETAT-DES-LIEUX, fiche d'une personne § 6).

```
PRIORITAIRE    58                       L'OMBRE DE DALLE — 27 % du fil principal,
(10 sept.)                               partout dans l'app. Un écran est visible
                                          s'il porte .show, jamais sur offsetParent.
                                          Profil avant/après, batteries en série.

MAINTENANT     50                       le contrôle design déterministe
                                        — rien ne sert de coder avant
               51                       revérifier redteam_toile après
               48                       corriger PARCOURS.md
               52                       le \n parasite (2 minutes)

PHASE A        56                       couvrir la liaison phrase → formulaire
cohérence                                — sinon la page + casse en silence
               45 · 43 · 47             cohérence des écrans — c'est l'objectif
               11 · 12                  padding et échelle
               42                       gratuit / Cercle bloc par bloc

PHASE B        22 → 9                   la pile save/restore débloque les angles
dessin         39 · 40                  shareVis · lisibilité du chiffre
               33 · 34                  les trois dalles de Créer
               46                       mutualiser le trait

PHASE C        55                       LA PALETTE DES TRAITS (150°)
identité                                 — bloque la validation de TOUTES
                                          les fiches, à trancher en premier
               24 · 25 · 23 · B · D     moodboards à trancher AVANT de coder
               A · C                    Aura « Le Calage » · Partager

PHASE D        15                       la demande de Promi — le gros morceau
produit        16 → 30                  onboarding, puis ses textes
               17 → 31 · 26             paiement, puis ses écrans, puis le juriste
               18 · 19 · 20 · 21        Cercle, Fil, personnes, Nuée

PHASE E        10 · 28 · 29 · 32 · 49   finitions et documentation
```

**Règle de la phase A : rien ne s'invente pendant un lot de correction.**
L'objectif est la cohérence, pas l'identité. Les moodboards viennent après.

---

## 10. Les interdits — à relire avant chaque lot

**Sur la dalle**
- La dalle est **toujours au premier plan**, opacité 1. Aucun filtre, aucun voile,
  aucun `mix-blend-mode`, aucun `backdrop-filter` (ça produit un « gris dur »).
- **Jamais de polygone reconstruit ni de dalle simplifiée.** Une dalle affichée
  est une dalle rendue par le moteur. Rejeté explicitement, plusieurs fois.
- Jamais de dalle répétée en motif.
- Aucun fond animé ou généré sur une page qui doit montrer une dalle de référence.

**Sur la couleur**
- Aucun boost de saturation, aucune « amélioration » spontanée. Les
  multiplicateurs `TON` inférieurs à 1 assombrissent vers le kaki — c'est un
  piège connu.
- **Aucun filet neutre ou noir.** La couleur suit l'état : menthe = tenue,
  orange = à tenir, teinte de la dalle = en cours.
- Terracotta et mauve **ne passent pas en texte sur fond clair** (2,83:1 et
  1,55:1 — non conformes).

**Sur le vocabulaire**
- Promi = promesse = dalle, invariable. Toile · Nuée · Brouillon · Fil · Aura ·
  Studio · Le Cercle · Peaufiner · Index.
- Rejetés : « Belle parole » · « En replanter un » · les gros boutons « Dire un
  mot » · les pourcentages de score dans une Nuée.
- Le prix s'écrit « 29 € · soit 2,42 €/mois · −39 % ». **Jamais « 2 mois
  offerts »** — c'est faux, 3,99 × 12 = 47,88.

**Sur la méthode**
- Un lot = un sujet. Jamais de refactoring pendant un lot de correction.
- Un patch = un script Python avec `assert S.count(old) == 1` sur chaque ancre.
- `node --check` avant tout Playwright.
- **Ne jamais nettoyer le CSS.** 3 158 règles, dont beaucoup mortes. Retirer une
  règle, même prouvée sans effet, **décale l'ordre des suivantes dans la
  cascade**. Cinq tentatives, jusqu'à **6 384 écarts**. On écrit dans un bloc
  neuf, on ne nettoie pas. *(Cet interdit annule le chantier 41 de l'addendum
  v6 — c'est `CLAUDE.md` qui fait autorité.)*
- **Ne jamais réécrire un écran « proprement ».** On patche. Une valeur étrange
  — un `-66px`, un `.42` — est étrange pour une raison.
- **Ne jamais toucher au code de la Toile** sans demande explicite.
- **La règle des trois tons :** une fiche porte toujours trois couleurs
  distinctes — la dalle (sa matière), le fond (l'état du Promi), les traits
  (une teinte dérivée de la dalle). Jamais de ton sur ton.
- **Deux pièges de spécificité, pas un.** Ils écrasent tout `position` posé
  ailleurs et coûtent un tour à chaque fois :
  - `#shareScreen>*:not(#shareToileBg)` — documenté §11.2, porte son
    avertissement dans le fichier
  - `#createSheet>*:not(#csTrameCv):not(.closeb):not(.pd-drift){position:relative;z-index:1;max-width:84%}`
    — **découvert pendant le lot 1, non documenté.** La parade idiomatique est
    celle du `.closeb` : `position:absolute!important` + `max-width:none!important`
- Les identifiants DOM font ombre aux fonctions globales : `replayOnb` est
  devenu `promiReplayOnb` pour cette raison.
- Ne jamais éditer `promi-reference.md` — il se régénère.

---

## 11. Ce que tu autorises sans réfléchir dans Claude Code

| Autorise | Montre-moi d'abord |
|---|---|
| `python3` · `ls` · `cat` · `grep` · `node` | `rm` — ça supprime |
| « Toujours autoriser » sur les batteries | `>` ou `mv` **sur `app.html`** hors du travail demandé |
| Les captures d'écran | **Toute question à choix multiples** — c'est là que se prennent les décisions |

Quand Claude Code pose une question à trois options : **envoie-la-moi.** Trois
fois pendant le lot 1, il avait raison contre mes documents.
