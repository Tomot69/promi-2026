# CASSE.md — ce qui est cassé dans l'app

> **Passe d'usage du 18 août 2026.** Je me suis servi de l'app au lieu de la mesurer :
> j'ai planté, rempli les champs, touché les pastilles, ouvert chaque fiche, chaque
> Peaufiner, l'Index, le Fil, les Réglages, l'Aura, le Studio, le Partage — dans les
> deux thèmes. **Rien n'a été corrigé.** `app.html` n'a pas été touché.
>
> **Pourquoi mes cinq juges n'ont rien vu :** ils mesurent des coordonnées et des pixels
> peints. Aucun ne remplit un champ, aucun ne touche une pastille, aucun ne compare deux
> écrans successifs. Un champ de 0 × 0 px passe le contrôle de position ; une pastille sans
> effet passe le contrôle de style ; un résidu d'écran précédent n'est jamais regardé parce
> que chaque juge repart d'un état propre. **C'est la leçon de la section 1, en plus grave :
> cette fois ce n'est pas le dessin qui manque, c'est le fonctionnement.**
>
> Les sondes sont dans `scratchpad/casse/` (`p1` à `p9`), les captures dans
> `scratchpad/casse/shots/` et `shots2/`. Chaque ligne ci-dessous a été **constatée**, pas
> déduite. Quand je n'ai pas su reproduire à coup sûr, je l'écris.

---

## ⚑ CLOS — 29 août 2026, passe à l'œil, écran par écran

**Toutes les lignes A, B et C de ce document sont couvertes par une batterie verte**, et le
dernier point ouvert — « les textes qui se touchent dans l'Index », « les commentaires qui
sortent de leur ligne » — **n'est plus reproductible** :

```
scratchpad/collisions.py    19 écrans × 2 thèmes    →    0 collision
```

Le seul recouvrement réel qui subsistait dans le produit n'était sur aucune de ces listes :
**un TROISIÈME bouton « Planter un Promi dans la Nuée »**, bâti par la liste de Peaufiner de
la section 2 (`.s2-bouton`), que le garde des jumeaux `#nfAdd` / `#nqAddPromi` ne voyait pas
— deux textes identiques superposés à 100 % dans `#dpdCorps`. Rangé, comme le jumeau : ils
mènent tous au même geste.

⚠ **Le premier balayage annonçait 269 collisions, toutes fausses.** La sonde ratissait tout
`#device`, écrans FERMÉS compris — ils gardent leurs nœuds en `display:block`, simplement
recouverts. Et les écarter un à un ne marche pas : dans une vraie collision, c'est le texte
du DESSOUS qu'on écarterait, et la collision disparaîtrait de la mesure. **On prend la
feuille la plus haute qui couvre l'écran, et on compare ses textes entre eux.**

Ce que la passe à l'œil a trouvé en plus, et qui n'était sur aucune liste : voir
`ETAT-DES-LIEUX.md` § « CE QUE L'ŒIL A TROUVÉ » — douze points, tous corrigés.

---

## Ce qui fonctionne — pour ne pas le retester

Ces quatre-là marchent, vérifiés au doigt :

- **Tenir une parole au geste** sur une fiche à tenir : `rate → tenu`. ✔
- **Planter un Promi au geste** depuis la page + : 25 → 26 Promi. ✔
- **Toucher une carte de l'Index** ouvre la fiche. ✔
- **Toucher un bandeau du Fil** ouvre la fiche. ✔

---

# A · NE FONCTIONNE PAS

### A1 · La phrase de la page + n'affiche jamais ce qu'on écrit
**Écran** page + · les trois natures · **Geste** toucher le mot « rendre le livre… », puis
écrire.
**Devrait** la phrase montre le mot qu'on tape.
**Constaté** `window._phrase.titre` devient bien « la Bretagne », mais la phrase affichée
continue d'écrire **« rendre le livre… »**. Mesuré deux fois, sur deux mots différents.
Vérifié une troisième fois en plantant : `.pp-phrase` ne contient pas « aller voir la mer »
alors que le Promi se plante avec ce titre. **On écrit à l'aveugle.**

### A2 · Le panneau de choix a une hauteur de zéro
**Écran** page + · **Geste** toucher un mot de la phrase.
**Devrait** un panneau s'ouvre sous la phrase (cadres 18 à 23).
**Constaté** `#csChoix` prend bien la classe `.ouvert` — et mesure **342 × 0**. Le champ de
saisie `#phIn` existe (342 × 24) mais le panneau qui doit le porter est plat.
*(C'est le piège déjà documenté dans `CLAUDE.md §8` — « la cote mesurée sur elle-même » —
mais ici il est resté à zéro.)*

### A3 · La phrase d'un Promi ne porte que deux mots
**Écran** page + · Promi · **Geste** regarder la phrase.
**Devrait** un créneau par élément : le sens, à qui, le titre, quand (§2.8).
**Constaté** deux créneaux seulement : `sens` et `titre`. **Il n'y a rien à toucher pour
« à qui » ni pour « quand »** — toucher `[data-ph=qui]` ou `[data-ph=quand]` ne trouve
aucun nœud.

### A4 · Aucune pastille de la page + n'est atteignable
**Écran** page + · Promi, Chiche et Nuée · **Geste** toucher une pastille.
**Devrait** choisir une personne, une échéance, une Nuée.
**Constaté** **zéro** pastille de largeur non nulle. « Moi · Maman · Nico · Léa · Adrien ·
Marion », « un jour · 2 j · 5 j · 2 sem · + tard », « Aucune · Famille · Moi-même · Le
projet · Weekend à Lisbonne » : toutes présentes dans le DOM, toutes de taille nulle.

### A5 · Les champs `#fTitle` et `#fWho` sont à 0 × 0, hors cadre
**Écran** page + · **Geste** écrire dans le titre.
**Devrait** le champ reçoit le texte.
**Constaté** boîte **0 × 0** posée à **x = −14**. Playwright abandonne au bout de 30 s.
Les mêmes valeurs pour `#nName`, `#nInvite`, `#nFirst`, `#dfTitle`, `#dfWho`.
*(Ces champs sont censés être pilotés par la phrase — mais A1 à A3 montrent que la phrase
ne les pilote pas.)*

### A6 · La recherche de l'Index ne filtre rien
**Écran** Index · **Geste** taper « crêpes » dans le champ de recherche.
**Devrait** la grille se réduit aux Promi qui correspondent.
**Constaté** **28 cartes avant, 28 cartes après**. Le champ accepte le texte, la grille ne
bouge pas. *(C'est ma section 4 : mon rendu remplace le contenu de `#indexList` et la
liaison de `#ixSearch` ne le retrouve plus.)*

### A7 · On ne peut plus tenir une parole depuis le Fil
**Écran** Fil · **Geste** chercher « TENIR » / « REPORTER » sur un Promi à tenir.
**Devrait** le Fil porte le geste — *« on ne valide pas une tâche, on tient sa parole »*
(commentaire de `buildFeed`).
**Constaté** **zéro** bouton d'action visible. *(C'est ma section 4 : mon bandeau remplace
le contenu de `#feedList` et n'a jamais reposé les actions. **Une fonction du produit a été
perdue.**)*

### A8 · Ouvrir une fiche après une autre laisse Peaufiner à moitié ouvert
**Écran** fiches · **Geste** ouvrir une fiche, ouvrir son Peaufiner, fermer, ouvrir une
autre fiche.
**Devrait** la seconde fiche s'ouvre propre, Peaufiner fermé.
**Constaté** la classe **`s2-ouv` survit**. Sur la seconde fiche : le mot-marque `#dptNat`
est **invisible**, le mot de trace `#dptTrace` est **invisible**, le geste disparaît, et les
réglages se peignent par-dessus la fiche. Constaté sur « à tenir » et sur le Chiche.

### A9 · Le bouton « planter » est introuvable
**Écran** page + · **Geste** chercher le bouton.
**Constaté** `#addPromi` est en `display:none`, boîte 0 × 0. Le geste tracé fonctionne (voir
plus haut), mais **la bascule vers le bouton ne mène nulle part** — alors que
`redteam_verbe` affirme le contraire (6/6). Le contrôle regarde un autre état que celui d'un
usage normal.

---

# B · SE SUPERPOSE OU DÉBORDE

### B1 · Toute la liste de Peaufiner se peint en colonne au bord gauche
**Écran** page + · **Geste** ouvrir Peaufiner sur un Promi, fermer, rouvrir le + et choisir
une autre nature.
**Constaté** « Promi · ✕ FERMER · À QUI · moi · AVANT · un jour · DANS UNE NUÉE · aucune ·
NOTE · PIÈCES JOINTES · 0 fichier · IMPORTANT · ·· · URGENT · ·· » **empilés en colonne à
x ≈ 0**, par-dessus le champ framboise, par-dessus le mot-marque.
**Capture : `scratchpad/casse/shots/pp_chiche_dark.png`.** C'est le plus visible de tous.
⚠ **Je n'ai pas su le reproduire à coup sûr** en rejouant le geste lentement : il dépend du
moment où l'on rouvre. La capture prouve qu'il arrive.

### B2 · La barre Peaufiner recouvre les deux derniers réglages — sur toutes les fiches
**Écran** toutes les fiches · **Geste** ouvrir Peaufiner et descendre.
**Constaté** `#dpdTog « Peaufiner ▾ »` recouvre **à 100 %** `« C'EST IMPORTANT ? »` et
`« RÉCURRENCE »`, et à 80 % leurs valeurs. Constaté sur Promi, à tenir, tenue, Chiche.

### B3 · Sur une fiche tenue, l'état est posé sur la carte de commentaire
**Écran** fiche tenue · **Constaté** `#dptQuand « TENUE »` recouvre **à 100 %**
`.dpm-head « NICO, HIER »`. Et `.dpm-txt « merci d'y penser ♥ »` recouvre `« répondre… »`
à 75 %.

### B4 · « À QUI » apparaît deux fois dans Peaufiner, dont une haute de 1408 px
**Écran** Peaufiner d'une fiche · **Constaté** la liste commence par un bloc « À QUI » de
**1408 px de haut** (le conteneur entier compté comme un réglage), puis le vrai réglage
« À QUI » de 64 px à sa place.

### B5 · L'encart « C'EST IMPORTANT ? » fait 304 px de haut
**Écran** Peaufiner d'une fiche · **Constaté** 304 px là où tous les autres réglages font
**64** (§3.3). C'est l'encart trop grand.

### B6 · Le menu de tri de l'Index couvre tout l'écran et se superpose aux cartes
**Écran** Index · **Geste** toucher `⇅`.
**Constaté** le menu s'ouvre en **390 × 844** ; `.ix-mi « Par Nuée »` recouvre **à 100 %**
`.s4-eb « avec +2 »` et `.s4-eb « perso »`, et à 44 % les titres « Famille » et
« Moi-même ». `.ix-mg « NE MONTRER QUE »` recouvre « Famille » à 56 %.

### B7 · Le bouton de tri recouvre le mot « TRIER »
**Écran** Index, menu ouvert · **Constaté** `#ixTriBtn « ⇅ »` ⨯ `.ix-mg « TRIER »`, 48 %.

### B8 · « ✕ Fermer » est posé sur le titre — sur quatre écrans
**Constaté** `.closeb` recouvre le titre de l'écran :
Réglages **100 %** (« Réglages ») · Aura **100 %** (« Aura ») · Studio **100 %**
(« The Studio ») · Partage **67 %** (« Partager »).
*(Ces quatre écrans n'ont jamais été portés — c'est probablement antérieur au portage.)*

### B9 · Le Studio déborde par la droite
**Écran** Studio · **Constaté** `.st3-p` et `.st3-orb` vont de **x = 352 à 392**, et un
autre de **408 à 448** — hors du cadre de 390. 14 débordements au total.

### B10 · L'Aura déborde en bas
**Écran** Aura · **Constaté** 10 débordements, dont `#kBalance` à y = 858, `#kLens` à 919,
`#kchart` à 1150. ⚠ **Sous réserve** : l'écran défile peut-être légitimement.

### B11 · Une pastille REMPLIE porte le contour pointillé du vide
**Écran** page + · Chiche · **Constaté** `.ph-m.ph-vide « courir dimanche »` (283 × 63) en
**pointillé**, alors qu'elle porte une valeur. Idem sur la Nuée :
`« le nom »` et `« tout le monde »` en pointillé.
Le pointillé doit dire « il manque quelque chose » (§2.6) — ici il ne dit rien.

### B12 · Le compagnon vide d'un Chiche s'affiche en pointillé sur la fiche
**Écran** fiche Chiche · **Constaté** `.s2-reg.s2-vide « AVEC / personne »` (342 × 64) en
pointillé. **Voir C9 : décision prise, il ne doit pas s'afficher vide.**

---

# C · DIT UN MOT FAUX OU ABANDONNÉ

### C1 · ★ « URGENT » existe encore — décision : supprimé partout
**Décision Tom, 18 août 2026 : le concept est abandonné, il ne doit rester nulle part dans
l'interface.** Constaté à quatre endroits :
- **Peaufiner de la page +** : un réglage plein « **URGENT** », valeur « ·· ». C'est **moi**
  qui l'ai remonté (section 3, l. 16680) alors que la ligne 9705 de l'app dit en toutes
  lettres *« Urgent supprimé (décision : on garde Important, comme la fiche) »* et le masque
  dans le formulaire. **Je l'ai ressuscité.**
- **Formulaire de la page +** : le champ « **Urgent ?** ».
- **Toile · modes d'arrangement** (l. 2597) : « **Urgence** » et sa description
  « **les plus urgents se densifient au cœur** ».
- Le commentaire l. 336 : « Aplat de couleur pour l'urgent ».

### C2 · ★ « C'est important ? » est en gratuit — décision : c'est un réglage du Cercle
**Décision Tom : « C'est important ? » est un réglage du Cercle, dans le bloc flouté avec
récurrence, rappel et mémoire. Jamais en gratuit.** Constaté à trois endroits, toujours
**hors** du bloc flouté :
- **fiche** : « C'EST IMPORTANT ? » à y = 818, **au-dessus** de l'encart du Cercle (y = 923).
  Les trois réglages floutés sont RÉCURRENCE, RAPPEL, LA MÉMOIRE — l'importance manque.
- **page +** : réglage « IMPORTANT » en clair, aucun bloc du Cercle sur cet écran.
- **Réglages généraux** : « C'EST IMPORTANT ? » à y = 331, l'encart du Cercle à y = 435.

### C3 · L'encart du Cercle se contredit lui-même
**Écran** fiche · **Constaté** l'encart écrit **« importance, récurrence, rappels,
mémoire »** — il annonce l'importance comme un réglage payant, alors que « C'EST IMPORTANT ? »
est posé juste au-dessus, en gratuit. Le texte est déjà juste ; c'est le réglage qui est au
mauvais endroit.

### C4 · La valeur d'« important » est illisible
**Constaté** le réglage affiche « **·** », « **··** », « **···** » — sans libellé. Sur la
page + la valeur lue est « **·· ·** ». Rien ne dit ce que ça vaut.

### C5 · Un Chiche lancé dit « EN COURS » au lieu de « LANCÉ »
**Écran** fiche Chiche · **Constaté** `#dptQuand` = « **EN COURS** ». Le moodboard
(cadres 72 à 77) écrit « **LANCÉ** » pour cet état, et « **TENU À DEUX** », « **À
RELEVER** » pour les autres. *(Ma section 4 écrit bien « LANCÉ » sur la carte d'Index :
**la fiche et la carte se contredisent donc sur le même Promi.**)*

### C6 · ★ Les textes d'explication d'un Chiche sont à revoir
**Décision Tom : les textes d'un Chiche sont à revoir.** Les deux constatés :
- **fiche Chiche**, sous le trait : « **Marion complètera si elle relève** » (l. 14415 —
  construit par concaténation, `p.who` ou « elle » par défaut).
- **page + Chiche**, sous la phrase : « **le compagnon et l'échéance sont dans Peaufiner** ».
  Cette phrase dit à l'utilisateur d'aller chercher ailleurs ce que la phrase devrait porter.

### C7 · ★ La phrase d'un Chiche n'a pas de créneau « avec qui »
**Décision Tom, mot pour mot : « Le second créneau est le compagnon — “avec qui” — et il ne
s'affiche pas quand il est vide. »**
**Constaté** la phrase d'un Chiche porte « **à qui ?** · *Chiche* · **de courir dimanche** »
— **aucun créneau compagnon**. Le compagnon n'existe que dans Peaufiner, sous le libellé
« AVEC », et il s'y affiche en pointillé quand il est vide (B12).

### C8 · « En replanter un » — terme banni
**Écran** après avoir tenu une parole · **Constaté** l. 6016, un bouton
`#dptEncore` intitulé « **En replanter un** ». `CLAUDE.md §2` le liste dans les termes
bannis, et un commentaire de l'app le sait déjà (l. 12398) sans l'avoir retiré.

### C9 · « Belle parole. » — terme banni
**Constaté** l. 6025, premier des mots de félicitation : « **Belle parole.** ».
`CLAUDE.md §2` l'interdit **comme bouton** ; ici c'est un mot de célébration. **À trancher :
le bannissement vaut-il aussi hors bouton ?**

### C10 · Le mot d'état d'une carte d'Index ne dit pas le délai
**Constaté** la carte écrit « **À TENIR** » là où le moodboard écrit « **À TENIR · 2 J** ».
Déjà noté en Q44 : l'app ne sait pas produire le compte de jours. **Ce n'est pas une
régression, c'est une fonction absente.**

---

## Ce que je n'ai pas pu trancher

- **B1** : je n'ai pas su reproduire la colonne parasite à coup sûr. Elle est sur la capture.
- **B10** : les débordements de l'Aura sont peut-être du défilement légitime.
- **C9** : « Belle parole. » est banni comme bouton ; ici c'est autre chose.
- Je n'ai **pas** ouvert le Cercle payant (`isPremium = false` partout) : ce que voit un
  abonné n'a pas été regardé.
- Je n'ai **pas** testé le brouillon (« gardé de côté ») : le jeu de données n'en contient
  aucun (`draft = null`).
- Je n'ai **pas** testé la Nuée en profondeur — sa fiche, ses membres, l'ajout d'un Promi.

---

## Ce que j'ai cassé moi-même — à mettre à mon compte

**A6** (la recherche de l'Index), **A7** (TENIR/REPORTER perdus dans le Fil) et **C1** (le
réglage « URGENT » ressuscité) viennent **directement de mes sections 3 et 4**. Mes juges
ne pouvaient pas les voir : ils ne tapent pas dans un champ, ne cherchent pas un bouton
qu'ils ne connaissent pas, et ne relisent pas ce que l'app avait décidé de masquer.

**Ce qu'il manque à l'outillage**, si on veut que ça ne recommence pas :
1. un contrôle qui **remplit chaque champ et vérifie que la valeur arrive** ;
2. un contrôle qui **touche chaque pastille et vérifie qu'elle change quelque chose** ;
3. un contrôle qui **enchaîne deux écrans** au lieu de repartir propre — c'est là que vivent
   les résidus ;
4. un **inventaire des fonctions** (tenir depuis le Fil, chercher dans l'Index, planter au
   bouton) qu'aucune refonte ne doit faire disparaître.

---

# ADDENDUM — les réparations, livrées

**Les sept correctifs sont en place** (`sauvegardes/reparations-livrees.html`), les cinq
juges sont au vert et les neuf batteries aussi. Ce qui suit corrige aussi **deux erreurs de
mon propre rapport**.

## LE PRÉFIXE MORT N'EXISTE PAS — je m'étais trompé

J'ai écrit que **234 règles `#device #detailPoster …` ne peignaient rien** parce que le
poster vivait sous `.frame`. **C'est faux.** Mesuré proprement, au repos comme fiche
ouverte comme Peaufiner ouvert : `#detailPoster` est **sous `#device`**
(chaîne `#device < .frame`), le sélecteur touche bien ses quatre `.s2-reg`, et le flou du
Cercle **s'appliquait déjà**. Même chose pour `#indexSheet`, `#createSheet`, `#feedView`,
`#shareScreen`, `#auraScreen`, `#settingsScreen`.

**Ce qui m'a trompé :** j'ai fait cette mesure sur l'app QUI PORTAIT MES RÉPARATIONS
CASSÉES — et là, le poster était bel et bien sorti de `#device`. J'ai pris la conséquence
d'un bug pour la cause. **Deux écrans seulement vivent réellement hors `#device` :
`#studioScreen` et `#plusScreen`.**

## LE COUPABLE DES 212 ÉCARTS — une erreur de découpe, pas un conflit

Réapplication des sept correctifs **un par un**, `releve-S2-peaufiner.py` après chacun :

```
                                     S2      S4
(état restauré)                       0       0
A6 · la recherche de l'Index          0       0
A7 · TENIR et REPORTER au Fil         0      10
A1 · la phrase suit le doigt          0      10
C7 · le compagnon du Chiche           0      10
C5 · un Chiche dit « LANCÉ »          0      10
C1 · URGENT retiré                  212     194   ← LE COUPABLE
§3.8 · le Cercle flouté             212     194
```

**C1**, et pour une raison bête : mon motif de retrait du champ « Urgent ? » s'arrêtait sur
le `</div>` de `.impseg` et **laissait celui de `.field` orphelin**. Le HTML se
déséquilibrait, toute la structure du formulaire se décalait — d'où l'entête mesurée à
`(-16, 1528)`. Motif corrigé pour retirer le `.field` en entier : **S2 reste à 0 sur toute
la séquence.**

Ma bissection précédente m'avait innocenté C1 à tort : j'avais rétabli **une** de ses trois
parties. *Aller dans l'ordre, un par un, était la bonne méthode.*

## LES 10 ÉCARTS DE LA SECTION 4 — contrôle réécrit au niveau de la décision

Les cinq bandeaux du moodboard ne portent **aucune action** : le pas y est constant, 140.
Le Fil de l'app en porte, et **cette fonction ne se perd pas** (décision Tom). Un bandeau
qui porte TENIR / REPORTER emmène sa rangée de pastilles (§3.5, hauteur 50) sous lui, soit
**62 px de plus**. Le juge encodait le pas constant : il a été réécrit au niveau de la
décision, avec **un contrôle neuf** — *« AUCUN geste dans le Fil : TENIR et REPORTER ont
disparu »*. Ce qui reste vérifié sans changement : le bandeau fait 358 × 128, rayon 22, à
x = 16. Version d'origine : `sauvegardes/releve-S4-avant-geste-du-fil.py`.

## LES TROIS ZONES AVEUGLES — enfin regardées

### Zone 1 · Le Cercle payant — **on payait pour un verre dépoli**
En forçant `setPremium(true)`, les quatre réglages du bloc restaient **`blur(2.4px)` et
`pointer-events:none`**. La règle de l'app (l. 14992) floute **sans condition**. Corrigé
par une levée additive `#device.premium …` — la règle existante n'est pas touchée.
**Vérifié : Cercle non payé → flou ; Cercle payé → net et touchable.**

### Zone 2 · Le brouillon — **sa fiche n'est pas celle d'un gardé de côté**
Un Promi `draft:true` ouvre une fiche qui dit **mot-marque « Promi »**, **état « EN COURS »**,
**« trace pour tenir »**, avec les classes `dp-promi f-encours` — alors que
`_ficheEcran` prévoit pour un brouillon : pas d'aplat, trait tout en points, « Gardé de
côté », « trace pour planter ». **La classe `dp-draft` n'est jamais posée**, donc l'écran
« Gardé de côté » du §5 n'est jamais atteint. `#dpMain` descend à **y = 1604**.
*La carte d'Index, elle, est juste* : `data-etat=garde`, « GARDÉ DE CÔTÉ », contour pointillé.

### Zone 3 · La Nuée en profondeur — **deux écrans à la fois**
`openEssaim` ouvre `#essaimSheet` **et** laisse `#detailPoster` peindre une fiche de Nuée.
Résultat : `#dptTrace « trace pour tenir »` recouvre **à 100 %** `#dptTitre « Famille »`, et
le fil de la Nuée recouvre la barre Peaufiner à 100 %. `#essaimSheet` déborde de 11 blocs.
**Une fiche de Nuée ne devrait pas porter « trace pour tenir » : on ne tient pas une Nuée.**

## UN TROU FONCTIONNEL DE PLUS — les pastilles de Peaufiner

**Toutes les pastilles empruntées par Peaufiner mesurent 0 × 0** : « un jour · en l'air ·
demain · 5 jours · 2 semaines · ce mois-ci · une date précise… », « Aucune · Famille ·
Moi-même · … ». Elles sont dans le DOM, `display:block`, `pointer-events:auto` — et de
taille nulle. **On ne peut donc changer ni l'échéance ni la Nuée depuis Peaufiner**, ni sur
la fiche ni sur la page +. C'est ce que dit `redteam_pastilles` avec ses « 0 trouvées ».

## Ce qui reste rouge, et pourquoi

- **`#addPromi` est en `display:none`** : la bascule ne mène à aucun bouton « planter ».
  Le geste tracé fonctionne ; le bouton n'existe pas.
- **Le menu de tri de l'Index couvre 844 px** et se pose sur les cartes.
- **La phrase n'a pas de créneau « quand »** — et je ne l'ajoute pas : il faudrait un mot de
  liaison que ni le document ni le moodboard ne donnent. `CLAUDE.md §9` : *si tu ne trouves
  pas, tu demandes.* **Question ouverte.**
- **Les pastilles de Peaufiner à 0 × 0** (ci-dessus).
- **La fiche d'un brouillon** et **la fiche d'une Nuée** (ci-dessus).

## LES QUATRE CHIFFRES — avant et après

```
                        avant   après
redteam_champs           6/19   21/22      remplir les champs
redteam_pastilles        3/10    3/10      toucher les pastilles
redteam_enchaine         8/24   11/24      enchaîner deux écrans
redteam_fonctions       11/18   16/19      l'inventaire des fonctions
```

`redteam_pastilles` ne bouge pas, et c'est le chiffre le plus parlant : **les pastilles de
Peaufiner sont à 0 × 0** et **la phrase n'a que deux créneaux**. Ces deux trous-là n'ont pas
été rebouchés.

Les cinq juges sont au vert, les neuf batteries aussi (144/144 · 15/15 · 10/10 · 18/18 ·
19/19 · 13/13 · 6/6 · 0 filet · 16/16 après relance du flake `redteam_toile`), et
`releve-design.py` rend **✅ AUCUN ÉCART**.


---

# ADDENDUM 2 — le lot du 18 août (pastilles, photo)

## Ce qui est réparé et prouvé

**Les pastilles de Peaufiner ne sont pas mortes — mon contrôle l'était.** Un réglage
**se déplie** (§3.3) : ses pastilles vivent dans un `.s2-ctl` masqué tant qu'on n'a pas
touché le réglage. Les chercher sans l'ouvrir donnait « 0 pastille ». Vérifié au doigt :
toucher « AVANT » ouvre 7 dates, en choisir une pose `due = 5` ; toucher « DANS UNE NUÉE »
passe de `famille` à `lisbonne`. **Une promesse peut avoir une date.**
`redteam_pastilles` va **réglage par réglage** maintenant — les ouvrir tous puis les
toucher en série refermait les autres, et toutes passaient pour mortes.
**3/10 → 9/12**, et deux contrôles neufs de bout en bout sur l'échéance (Q28 : c'est
désormais le seul endroit où on la pose).

**La photo de fiche est livrée — `redteam_photo.py` 25/25.** Elle remplace la dalle dans sa
boîte exacte, recadrée au centre, opacité 1, **bornée par l'onde**, l'aplat de nature
dessous. Le bouton suit **l'onde au droit de lui**, pas la base : l'écart ne bouge pas quand
le trait change. Le même bouton rend la dalle. Fiche et page +, trois natures.

## Ce qui reste, et où j'en suis

**Le brouillon (point 2) — diagnostic affiné, non réparé.** `openDetail(id)` sur un
`draft:true` laisse **`cur` à null** et n'ajoute même pas `show` au poster : `#dptNat`
n'existe pas dans le DOM. Ce n'est donc pas `dp-draft` qui manque — **la fiche ne s'ouvre
pas du tout**. `_ficheEcran` a pourtant sa branche complète (pas d'aplat, trait tout en
points, « trace pour planter », « Gardé de côté »), et l'inventaire du §5 la décrit en
entier : base 262 / amp 44, dalle 141 × 118 à (124, 88), les quatre blocs texte en
`#3A54FF`, « GARDÉ DE CÔTÉ · 2 AVRIL ». **Tout est prêt sauf le chemin qui y mène.**
Je n'ai pas trouvé qui refuse l'ouverture, et je n'ai pas voulu deviner.

**La Nuée (point 3), `#addPromi` et le menu de tri (point 4), `redteam_enchaine` (point 5) :
pas faits.** L'ordre a été tenu jusqu'au point 1, puis j'ai porté le point 6 en priorité —
c'était le seul livrable neuf, et le seul entièrement spécifié.


---

# ADDENDUM 3 — le ton sur ton, et deux corrections d'honnêteté

## L'AUDIT DU TON SUR TON — 26/26, un seul défaut, et il était de moi

`redteam_tonsurton.py` mesure, **sur les pixels peints**, l'écart de luminosité entre chaque
trait du produit et le champ qui le porte. Seuil 42 (§3). Cinq sections, deux thèmes.

```
                              sombre   clair
fiche · en cours                Δ92     Δ92
fiche · à tenir                 Δ51     Δ51
fiche · tenue                   Δ94     Δ94
fiche · Chiche                 Δ120    Δ120
page + · Promi                  Δ92     Δ92
page + · Chiche                Δ120    Δ120
page + · Nuée                   Δ76     Δ76
carte d'Index · le pire des 10  Δ51     Δ51
bandeau du Fil · le pire        Δ51     Δ51   ← était Δ1
l'instant · l'autre moitié      Δ51     Δ51
l'instant · le trait se referme Δ163    Δ163
l'instant · juste après         Δ94     Δ94
```

**Le seul ton sur ton du produit était dans le Fil, en thème clair, et c'est moi qui l'avais
écrit.** La branche de repli de `_s4Fil` peignait le trait en **couleur pleine** en clair —
posé sur un champ de cette même couleur pleine : **Δ 1**. C'est exactement le défaut que
portent les cadres clairs du moodboard, et que le §2.1 bis interdit. Corrigé : la teinte
claire, **dans les deux thèmes**. Δ 1 → Δ 51.

**Q4 est close.** Le trait porte toujours la teinte claire. Les cadres clairs du moodboard
qui le peignent en couleur pleine sont une **erreur de dessin**, inscrite comme telle dans
`CLAUDE.md §3`. Le contrôle est permanent.

## DEUX CORRECTIONS D'HONNÊTETÉ

**Le brouillon n'est pas cassé — c'est une décision.** Sentinelle sur dix fonctions :
`renderDetail` n'est jamais atteint. La ligne 9415, lot 17, dit en clair qu'*« un brouillon
n'ouvre PAS une fiche — il ROUVRE la page + dans son état »*. Le §5 décrit pourtant trois
écrans « Gardé de côté » complets. **Le document et l'app se contredisent : point de
produit, non tranché.** Voir Q54.

**Les pastilles de Peaufiner n'étaient pas mortes** (addendum 2) : c'était mon contrôle.

## Q53 POSÉE — la photo partout

Une carte d'Index et un bandeau du Fil montrent désormais **la photo**, au même cadrage
centré et aux mêmes cotes que la dalle. `redteam_photo.py` : **27/27**.


---

# ADDENDUM 4 — les résidus d'écran, et deux mots

## `redteam_enchaine` : 11/24 → 20/24

**Le nettoyage des résidus avait purement disparu du fichier.** Il vivait dans le bloc que
j'ai perdu en restaurant `avant-reparations.html` avant de rejouer les sept correctifs un
par un : il n'en faisait pas partie. Reposé comme bloc autonome — et **accroché à
`closeAll`**, passage obligé de tous les chemins, le doigt comme le programme. Un crochet
sur le clic ne voyait que le doigt.

Deux temps :
1. **retirer les classes** — `s2-ouv`, `dpd-ouv`, `pp-peauf`, `in`, `s4-plein`, `v-fil` :
   **11 → 17**.
2. **rendre à la page + ses contrôles empruntés** (`_ppPeaufOuvre(false)`), et **rendre la
   Toile** que le Fil laissait en `display:none` : **17 → 20**.

Le second temps est celui qui avait fait tomber la section 2 à 212 écarts quand je l'avais
mis dans `openDetail`. Dans `closeAll`, il s'exécute **avant** que l'écran suivant s'ouvre :
S2 et S3 restent à 0.

## Deux mots interdits étaient à l'écran

Balayage de treize écrans, deux thèmes, sur « valider · urgent · score · tâche · brouillon ·
objectif » : **« Brouillon(s) »** (quatre endroits) et **« le score »** (un). Remplacés par
les mots que le produit emploie déjà — **« Gardés de côté »**, **« Garder de côté »** — et
par **« l'Aura »**, celui-là à valider. Voir Q55. Nouveau balayage : **aucun mot interdit à
l'écran.**

## Deux constats de CASSE.md étaient FAUX — les miens

- **La Nuée n'ouvre pas deux écrans.** Mesuré : `#essaimSheet` n'a pas `show`, le poster est
  en `dp-mode-nuee`, `#dptTrace` est **absent**, le geste est **absent**, `#tenirCv` est
  masqué. Une Nuée ne porte ni trait, ni geste, ni mot de trace. Mon constat venait d'un
  enchaînement d'écrans, pas de l'écran.
- **Le menu de tri ne couvre rien.** `#ixMenu` est le voile transparent ; le panneau fait
  346 × 604 et il est opaque. Mon contrôle visait le voile. Voir Q56.

## Ce qui reste rouge, et c'est court

- **`#addPromi` est en `display:none`** : la bascule ne mène à aucun bouton « planter ».
  Le geste tracé plante ; le bouton n'existe pas. ⚠ `redteam_verbe` affirme pourtant 6/6 sur
  « la bascule mène à un vrai bouton » — les deux contrôles ne regardent pas le même état.
  **À démêler avant de toucher quoi que ce soit.**
- **`redteam_fonctions` · « on tient sa parole au geste depuis la fiche »** reste rouge dans
  la batterie alors que le geste fonctionne quand on l'essaie seul (mesuré deux fois,
  `rate → tenu`). C'est la mise en scène du contrôle qui est en cause, pas la fonction.
- **`redteam_enchaine` 20/24** : il reste le retour à la page + après Peaufiner.
- **Q54 · le brouillon** : décision de produit, non tranchée.


---

# ADDENDUM 5 — LES SIX CHIFFRES SONT AU VERT

```
                        début du lot   fin
redteam_champs              21/22     22/22
redteam_pastilles            9/12     12/12
redteam_enchaine            20/24     24/24
redteam_fonctions           17/19     19/19
redteam_photo               27/27     27/27
redteam_tonsurton           26/26     26/26
```

Cinq juges au vert · huit batteries au vert · `releve-design` **AUCUN ÉCART**.
État livré : `sauvegardes/lot-six-verts.html`.

## `#addPromi` — la contradiction démêlée : AUCUNE DES DEUX BATTERIES N'AVAIT TORT

`redteam_verbe` clique **`#planterAlt`** — la bascule trait ↔ bouton — **avant** de mesurer.
Mon `redteam_fonctions` mesurait `#addPromi` **au repos**. Or au repos, il n'y a pas de
bouton : **on trace.** Le bouton n'apparaît qu'après la bascule, et c'est le produit.
**Rien n'était cassé** : mon contrôle visait le mauvais état. Corrigé — il actionne la
bascule, comme un doigt. C'est le troisième contrôle de la série à viser à côté ; les deux
autres étaient le menu de tri et les pastilles de Peaufiner.

## Ce qui a vraiment été réparé

- **`closeAll` retire la liste de Peaufiner** en plus des classes : rendre les contrôles
  empruntés ne suffisait pas, les blocs fabriqués restaient peints sur l'écran suivant.
- **Le Fil se referme aussi dans son `display`.** Une fonction de l'app (l. 4116) synchronise
  le sélecteur Toile/Index sur `feedView.style.display` : tant qu'il n'est pas `none`, elle
  croit le Fil ouvert et garde « Toile » et « Index » masqués. Retirer la classe `in` ne
  suffisait pas.
- **Le sélecteur rend son inline** au lieu qu'on le contredise.

## Trois contrôles remis au niveau de la décision

- **le créneau « quand »** : je l'exigeais dans la phrase ; **Q28 l'a retiré** il y a
  plusieurs lots. Le contrôle vérifie désormais l'inverse — que la phrase n'en porte pas —
  et que l'échéance est atteignable là où elle vit, dans Peaufiner.
- **le verbe d'un Chiche** : il n'ouvre rien, et c'est juste — un Chiche n'a pas d'autre
  sens. Le compter mort réclamait en creux une fonction que le produit n'a pas.
- **le menu de tri** : `#ixMenu` est le voile, `.ix-menu-p` est le panneau.

## LE BALAYAGE DES TROIS ZONES AVEUGLES — `redteam_aveugle.py`, 17/26

Nouveau contrôle, écrit à la fin du lot. **Il trouve quatre défauts que je n'ai PAS réparés**
— les ouvrir aurait été rouvrir un chantier alors que la session se remplissait.

| | ce qui ne va pas |
|---|---|
| **Cercle payé** | l'encart « ✦ Le Cercle » **ne s'efface pas** pour un abonné : il n'a plus rien à vendre, et il occupe la place. Les réglages, eux, sont bien nets et touchables. |
| **Nuée** | « **trace pour tenir** » reste peint quand on arrive sur une Nuée **depuis une fiche de Promi**, et recouvre son titre à 100 %. Une Nuée ne se tient pas. C'est un résidu d'écran de plus — celui-là, `closeAll` ne l'attrape pas. |
| **parcours · tenir au geste** | échoue dans le parcours complet alors qu'il passe seul (`redteam_fonctions` 19/19). Mise en scène ou vrai résidu : **non tranché**. |
| **parcours · planter (2ᵉ passage)** | le second parcours ne plante pas — la page + garde un état du premier. |

**J'ai tenté de corriger les deux premiers en CSS et j'ai échoué** : `_ficheCotes` pose
`display` **en ligne avec `!important`**, ce qu'aucune feuille ne peut battre (piège connu,
`CLAUDE.md §8`). Il faut les sortir **en JavaScript**, dans le même geste que les autres
résidus. L'essai a été annulé et l'app remise à l'état vérifié.


---

# ADDENDUM 6 — les zones aveugles, 17 → 21/26

État livré : `sauvegardes/lot-aveugle-21.html`. Les six contrôles d'usage restent au vert,
les cinq juges aussi, `redteam_ecrans` 144/144, `releve-design` **AUCUN ÉCART**.

## Réparé, en JavaScript — parce que le CSS ne pouvait pas

`_ficheCotes` et `cercle()` posent leurs `display` et leurs `filter` **en ligne avec
`!important`** : aucune feuille ne les bat (`CLAUDE.md §8`). Les deux correctifs vivent
donc dans le bloc `lot-RESIDUS`, en JavaScript, et repassent après chaque geste.

1. **Le Cercle payé ne montre plus de verre dépoli ni de réclame.** L'encart « ✦ Le Cercle »
   s'efface pour un abonné, les quatre réglages redeviennent nets et touchables. La règle de
   l'app, qui floute sans condition, n'est pas touchée : on la lève.
2. **Une Nuée ne se tient pas.** « trace pour tenir », la zone du geste et `#tenirZone`
   sortent de l'écran sur une fiche de Nuée. Le mot survivait à l'écran précédent et
   recouvrait le titre de la Nuée à 100 % quand on y arrivait depuis une fiche de Promi.

**Un piège de plus, payé une fois :** retirer `display` sans distinction emportait celui que
`_ficheCotes` pose légitimement — le geste caché sur une fiche tenue — et **les sections 1 et
5 sont tombées à 4 écarts chacune**. On marque désormais ce qu'on masque (`data-nuee-masq`)
et **on ne rend que ça**.

## Ce qui reste rouge — 5 sur 26, et pourquoi je n'y touche pas

| | ce qui ne va pas | pourquoi c'est laissé |
|---|---|---|
| **Nuée · superposition** | `#nqAddPromi` « ✦ Planter un Promi dans la Nuée » est peint à **y = 0**, par-dessus « ✕ FERMER ». J'ai posé sa largeur et sa hauteur du §5 (342 × 62) ; **le y reste à 0** | le §5 le donne à **24 / 46** — mais ce y est celui d'un autre cadre, et l'y poser le remettrait sur l'entête. **Je ne devine pas une cote.** La fiche de Nuée n'a jamais été portée : elle est hors des cinq sections |
| **parcours · tenir au geste** (×2) | échoue dans le parcours complet, passe seul (`redteam_fonctions` 19/19, vérifié trois fois) | mise en scène du contrôle, ou résidu d'enchaînement que `closeAll` n'attrape pas : **non tranché** |
| **parcours · planter, 2ᵉ passage** | le second parcours ne plante pas — la page + garde un état du premier | même famille que le précédent |

**Les trois derniers sont probablement le même défaut**, vu deux fois : un état de la page +
qui survit à un parcours entier. C'est le prochain fil à tirer, et c'est le seul.
