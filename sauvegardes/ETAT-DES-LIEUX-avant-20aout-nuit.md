# État des lieux — Promi, après le portage au moodboard

> **Ce fichier suffit à reprendre le projet.** Il dit ce qui est porté, ce qui ne l'est pas,
> ce qui a été corrigé dans les documents, quels contrats de test ont changé et pourquoi,
> et ce qui reste ouvert. Écrit sans complaisance : ce qui n'est pas beau à dire est dit.
>
> Dernière mise à jour : **20 août 2026**.
>
> ## ⚠ CHANTIER OUVERT — ET TROIS BATTERIES SONT ROUGES
>
> **Le jeu de démonstration de la planche est en place** (décision Tom, validée). C'est la
> fondation : sans lui, « identique au pixel » ne veut rien dire. **Mais il rougit trois
> batteries qui encodaient l'ANCIEN jeu**, et je n'ai pas eu la marge de les reprendre :
>
> ```
> redteam_ecrans     143/144   « Toile : hit() ignore les cellules grises » (2 thèmes)
> redteam_fonctions   17/19    « TENIR depuis le Fil » · « un bandeau ouvre sa fiche »
> redteam_aveugle     24/26    « Nuée · rien ne se superpose » (2 thèmes)
> ```
>
> **Ce ne sont pas des régressions de dessin : ce sont des contrats qui décrivent des
> données qui n'existent plus** (23 promesses de démonstration, un Fil de 12 événements).
> C'est le cas du §7 de `CLAUDE.md` — un contrôle qui encode un état qu'une décision a
> remplacé. **Ils se mettent à jour au niveau de la décision, pas en revenant en arrière.**
> C'est la première chose à faire au prochain tour, avant toute autre correction.
>
> ## ⚠ LA CONFORMITÉ DE FORME N'EST PAS ATTEINTE
>
> **Tom a rejeté la livraison : le Fil et l'Index ne ressemblent pas au moodboard, et ça se
> voit à l'œil.** Les juges disent vert parce qu'ils comparent des cotes et des couleurs,
> **pas des formes** : un trait à la bonne position avec la mauvaise courbe passe à zéro.
> Le chantier est **commencé, pas fini**. Ce qui suit dit exactement où il en est —
> voir « §4 bis · La conformité de forme ».
>
> Les batteries et les juges restent verts (ils ne mesurent pas ce qui est en cause), et le
> contrat visuel porte le report de polices, qui attend un `--figer`.
> L'état des lieux d'avant le portage est conservé : `sauvegardes/ETAT-DES-LIEUX-v592.md`.

---

## 1 · En une minute

Le **portage au moodboard est terminé**. Les cinq sections prévues par
`AUTONOMIE-CLAUDE-CODE.md` sont livrées ; les cinq lignes du critère d'arrêt sont vraies sur
chacune, et les neuf batteries sont vertes.

```
app.html                    point de reprise : sauvegardes/lot-polices-usage.html
sections portées            5 / 5
juges de section            S1 ✅ · S2 ✅ · S3 ✅ · S4 ✅ · S5 ✅   (tous à zéro écart)
batteries de comportement   144/144 · 15/15 · 10/10 · 18/18 · 19/19 · 16/16 · 13/13 · 6/6 · 0 filet
contrat visuel              releve-design.py  ✅ AUCUN ÉCART
```

### Ce que le lot du 19 août a livré

| | quoi | où c'est écrit |
|---|---|---|
| **1** | **LE VIDE EST UN DÉFAUT DU PLANCHER** — et de lui seul. Fiches et page + gardent la boîte du §2.7 ; la matière ne descend jusqu'à la vague **qu'au plancher** | `CLAUDE.md §4` · `ECARTS-MOODBOARD.md` · Q57 à Q60 |
| **1 bis** | **LA TOILE D'UNE NUÉE** — trois emplacements figés remplacés par la densité de semis du §10.6 (douze graines / 390 × 435) | Q62 · Q63 |
| **2** | **UNE NUÉE SE LANCE AU TRAIT ENTIER** — 0 → 390, mode complet du §2.6, ni chevron ni points | `CLAUDE.md §4` |
| **3** | **LE TUTORIEL NE SURVIT PLUS À `closeAll`** — trois rouges de `redteam_aveugle` pour une seule cause | §5 ci-dessous |
| **4** | **LA HAUTEUR DU TRAIT D'UNE FICHE DE NUÉE** — `base = max(176, 460 − 86 n)`, amplitude 40, Noyaux à `boîte − 29` | `PROMI-SPECIFICATIONS.md` partie II §9 et §12 |

> **⚠ LA PREMIÈRE FORMULATION ÉTAIT TROP LARGE, ET JE L'AI APPLIQUÉE TROP LARGE.**
> « La matière remplit tout le champ, partout » a fait gonfler la dalle d'une fiche sur tout
> son champ — cinq fois sa taille native. Tom a corrigé : **le moodboard des fiches et de la
> page + est juste**, le défaut n'existe **qu'au plancher du trait**. Tout a été restauré,
> puis re-corrigé au bon endroit. **La leçon : quand une consigne dit « ça ne doit pas
> exister », mesurer OÙ ça existe avant de l'appliquer partout.** L'outil qui manquait —
> `scratchpad/mesure_vide.py` — existe maintenant.

**Le relevé qui tranche** (`scratchpad/mesure_vide.py`, deux thèmes, hauteur de couleur nue
entre le bas de la matière et le trait) :

```
                        avant           après
Nuée · 1 Promi     125 abscisses/125 nues     0 nue · médiane 0 · pire 0
Nuée · 3 Promi      28 bandeaux > 24 px       0 bandeau · médiane 0
Nuée · 7 Promi  ←   17 bandeaux > 24 px       0 bandeau · médiane 0     AU PLANCHER
page + · choix ouvert ←  au plancher : rempli · médiane 0               AU PLANCHER
fiche · les 4 états      boîte du §2.7, inchangée — aucune n'est au plancher
```

**Trois sondes réécrites au niveau de la décision** (`CLAUDE.md §7`), aucune desserrée —
`redteam_tonsurton`, `releve-S3-page-plus`, `releve-S5-instant`, plus le contrôle de couleur
du mot-marque de `releve-S1-fiches`. Versions d'origine dans `sauvegardes/*-avant-matiere.py`.
Détail au §6.5.

### Les six contrôles d'USAGE — la mesure qui compte

Les juges disent que le dessin est juste. **Ceux-ci disent que l'app FONCTIONNE.** Ils ont
été écrits après avoir découvert qu'aucune batterie ne remplissait un champ ni ne touchait
une pastille — un champ de 0 × 0 passait tous les contrôles de cote.

```
redteam_champs      22/22   remplir chaque champ, et vérifier que la valeur ARRIVE
redteam_pastilles   12/12   toucher chaque pastille, et vérifier qu'elle CHANGE quelque chose
redteam_enchaine    24/24   enchaîner deux écrans, et comparer le second à lui-même ouvert seul
redteam_fonctions   19/19   l'inventaire des fonctions qu'aucune refonte ne doit faire disparaître
redteam_photo       27/27   la photo de fiche : elle remplace la matière, partout
redteam_tonsurton   26/26   un trait n'est JAMAIS à moins de 42 de son champ
redteam_aveugle     26/26   les trois zones que personne ne regardait
redteam_nuee        24/24   LA FICHE DE NUÉE — les 20 écrans du §12 + les 4 du Peaufiner
redteam_polices      0/0    AUCUNE GRAISSE HORS DES SIX FACES EMBARQUÉES
redteam_toile       17/17   stable sur trois passages — le dernier flake est mort
```

**Aucune batterie n'est rouge.** Le seul écart ouvert est celui du **contrat visuel** — voir
juste dessous, et il est *demandé par le lot*.

**`redteam_aveugle` — 26/26.** Le dernier rouge est tombé avec le portage du Peaufiner
d'une Nuée : « Planter un Promi » y a sa place, et la fiche au repos n'en porte plus.
Il y avait **deux** boutons — `#nqAddPromi` (balisage d'origine, celui qui se posait à y = 0
par-dessus « ✕ FERMER ») et `#nfAdd` — désormais ramenés à un seul. **Rien n'a été retiré du
produit.** Voir `QUESTIONS.md` · Q61.

> ⚠ **`releve-design.py` sort ~35 écarts, et ils SONT le lot des polices.** Tous portent sur
> `fontFamily` / `fontWeight` : `Apfel 700/800 → ApfelMid 500`, `Bricolage 800 → 700`. La
> référence a été refigée après le lot Nuée (validé par Tom) mais date d'avant les polices.
> **Je ne l'ai pas refigée** — `--figer` attend la validation, comme le §8 bis l'exige.
> Ancienne référence : `sauvegardes/design-reference-avant-nuee.json`.

**Ce qui n'est PAS fait, et pourquoi :** trois éléments du moodboard sont des **fonctions,
pas du dessin** — ils demandent une décision de produit, pas une cote. Voir §5.

---

## 2 · Ce qui a été porté, section par section

La méthode, identique partout : **écrire chaque écran depuis son inventaire de la partie 5
de `PROMI-SPECIFICATIONS.md`**, au lieu de réparer l'existant. Un bloc neuf en fin de
`app.html`, jamais une règle existante modifiée. Puis un juge par section, puis des duos
côte à côte moodboard / app, **dans les deux thèmes**.

| | Section | Ce qui est porté | Écrans | Juge |
|---|---|---|---|---|
| **1** | **Les fiches** | Promi, Chiche, Nuée, gardé de côté, états de fiche. Le moteur géométrique (§2) posé une fois pour toutes et **exposé** (`window._onde`, `_ficheEcran`, `_ficheTrait`, `_ficheCotes`, `_visageSvg`) | **8 / 8** | `releve-S1-fiches.py` |
| **2** | **Peaufiner** | La barre, les réglages, les réglages généraux, le bloc du Cercle | **7 / 9** | `releve-S2-peaufiner.py` |
| **3** | **La page +** | La phrase, les trois natures, les choix ouverts, le geste, le Peaufiner de la page + | **16 / 16** | `releve-S3-page-plus.py` |
| **4** | **Index et Fil** | L'écran plein, l'entête, la recherche, la grille, la carte d'Index (deux densités), le bandeau du Fil | **6 / 6** + 8 cartes isolées | `releve-S4-index-fil.py` |
| **5** | **L'instant** | « L'autre moitié arrive », « le trait se referme », « juste après », et la séquence d'une seconde | **6 / 6** | `releve-S5-instant.py` |

### Le critère d'arrêt, section par section

Cinq lignes, toutes à zéro sur les sections 3, 4 et 5 :

```
écarts de position > 3 px · écarts de style · collisions · débordements · présence peinte
```

**La cinquième ligne est la plus importante.** Un bloc à la bonne coordonnée mais invisible
est un faux vert : les juges lisent donc **les pixels réellement peints** — l'aplat de
nature, la dalle, la ligne — et vérifient l'encre de chaque texte contre le fond peint
dessous, seuil de luminosité 42.

### Sections 4 et 5 en détail

**L'Index et le Fil deviennent des écrans pleins** (décision Tom) : entête « Index N » +
✕ FERMER, champ de recherche, grille. Plus de topbar, plus de mot-marque, plus de
`#viewSwitch`, plus de dock. **Les deux seuls éléments de chrome persistants du produit sont
le ✕ FERMER et la barre Peaufiner.**

**L'instant** est le seul endroit du produit où la couleur d'état prend toute la place :
le champ entier passe au menthe **une seconde**, la dalle se recompose plus grande
(604 → 1013 pixels peints, mesuré sur 18 relevés), le mot tombe, puis le champ revient à sa
nature. Le déclencheur réel est le bouton « Tenue » du sélecteur d'état, par lequel passe
le geste qui se referme.

---

## 3 · Les deux trouvailles à ne pas reperdre

### 3.1 · L'Index est une FEUILLE, pas une vue

`window.ouvrirIndex()` appelle `buildIndex()` puis `openSheet(#indexSheet)` : la feuille se
pose **par-dessus** `#stage`, qui garde la Toile. Le code le dit en toutes lettres
(l. 3039) : *« le sélecteur revient sur Toile : l'Index est une feuille, pas une vue »*.

**Conséquence :** mesurer `#stage`, ou le `.on` de `#viewSwitch`, ne peut RIEN montrer — par
construction. Une session entière a été perdue sur ce constat pris pour un blocage.
`#indexSheet` passe bien de `opacity 0 / y 816` à `13,28 · 364 × 787`. Le Fil, lui, **est**
une vue : `setView('fil')` → `#feedView.in`, `#stage` en `display:none`.

> **La leçon, générale :** avant de conclure qu'un écran « ne s'ouvre pas », instrumenter
> **l'élément que le code désigne**, pas celui qu'on suppose. `scratchpad/probe_ix.py`.

### 3.2 · La loi de la carte était dans les chemins SVG du moodboard

Le document donnait les cotes carte par carte, jamais la règle qui les produit. Elle a été
retrouvée en lisant les chemins SVG des cadres 72, 74 et des cartes isolées, et **elle est
désormais inscrite au §3.9 bis de `PROMI-SPECIFICATIONS.md`** :

```
échelle = h/600 · base = hauteur de trait figée × échelle · amplitude = 13 × l/173
boîte   = ⌊ base + amplitude + 20 ⌋ · épaisseur = 5,5 × l/173 · période = 1
```

Elle retrouve les **huit cartes isolées** du document, boîte et dalle, **8 sur 8** — et
`releve-S4-index-fil.py` refait ce contrôle à chaque passage.

> **La leçon, générale :** quand le document donne des cotes sans règle, la règle est
> souvent dans le moodboard lui-même. `python3 scratchpad/dump_cadre.py <n>` sort le HTML
> d'un cadre ; `scratchpad/liste_cadres.py` donne l'ordre réel des 102 cadres — **qui n'est
> pas celui du document.**

---

## 4 · Ce qui a été corrigé DANS LES DOCUMENTS

Trois corrections, toutes validées, toutes inscrites à leur place — pas dans un compte rendu.

| Où | Quoi | Pourquoi |
|---|---|---|
| `PROMI-SPECIFICATIONS.md` **§3.9 bis** | **La loi de la carte**, ajoutée | Elle n'était nulle part ; elle a dû être redéduite deux fois |
| `PROMI-SPECIFICATIONS.md` **§2.5** | **Les bornes `[196, 344]` valent pour la carte sans exception** | Deux fiches du document portent 376 et 372, hors échelle. Reportées sur une carte de 133 px, elles laissaient **10 px au titre** : coupé en plein mot, l'état par-dessus. Un titre coupé n'est pas un dessin, c'est un bug |
| `CLAUDE.md` **§7** | **Un contrôle qui encode une règle abandonnée se met à jour au niveau de la décision** | Voir §6 ci-dessous |

**Un piège à connaître sur la borne :** la **loi** (§3.9 bis) et la **borne** (§2.5) sont
**deux règles distinctes**. La loi ne borne rien ; la borne est un garde-fou sur la valeur
qu'on lui donne. Les appliquer d'un seul geste fait sortir « le potager » à 152 au lieu de
153 — sa base est 346, deux pixels au-dessus du plafond. Chacune se contrôle à son niveau :
`juge_composants` teste la loi **sans** la borne, `juge_borne` vérifie que la borne mord sur
376 et 372, jamais sur une base légitime, et coûte moins de 3 px sur les cas limites.

---

## 4 bis · LA CONFORMITÉ DE FORME — le chantier ouvert

### Le jeu de démonstration de la planche — FAIT

`lot-JEU-PLANCHE`, à la fin de `app.html`. Mêmes promesses, mêmes titres, mêmes personnes,
mêmes états que les deux planches. **Tous les mots viennent des cadres**, lus au texte
(`scratchpad/extrait_jeu.py` → `scratchpad/jeu_planche.json`), aucun inventé.

```
6 hors Nuée   planter un arbre TENUE · faire les crêpes À TENIR · courir dimanche (Chiche,
              relevé, avec Rachel) · nager le mardi EN COURS · le grand plongeoir (Chiche,
              TENU À DEUX) · aller voir la mer À TENIR
6 au potager  arroser tous les soirs TENUE · semer les radis · reprendre l'arrosage
              automatique · réparer le grillage du fond · rapporter la clé du cabanon ·
              chiche de venir désherber samedi        → « 6 PROMI · 1 TENU », le compte du cadre
2 Nuées       le potager (Rachel, Adrien, +3) · l'atelier du samedi (Avec toi seulement)
1 gardé       appeler Mamie
le Fil        les CINQ entrées du cadre 76, dans son ordre, avec ses tournures
```

**Mesuré : l'Index affiche « 12 », comme le cadre 72**, et le Fil montre « Marion te lance
un chiche · à moi · Adrien a planté · à Rachel · Marion a relevé » — les eyebrows de la
planche, obtenus sans les écrire : la carte retire le titre entre guillemets du texte de
l'événement, il suffit d'écrire la tournure du cadre.

> **⚠ « m'appeler » et « venir dimanche » (cadres 8 et 10) n'y sont PAS** : ce sont des
> exemples de PHRASE sur la page +, pas des Promi plantés. Les compter donnait « Index 14 »
> là où le cadre écrit **12**.

**Corrigé au passage :** le nom d'une Nuée était capitalisé d'office (« Le potager ») —
la planche écrit « le potager », en minuscule, dans les trois cadres qui le portent.

### ⚠ CE QUE LA MESURE A APPRIS, ET QUI CHANGE LA CIBLE

Le comparateur descend là où les données convergent — `fiche-tenue` de **30,4 % à 13,8 %**,
`fil` de **48,4 % à 38,4 %**. **Mais il ne descendra pas à zéro, et pas à cause du dessin :**

> **LA MATIÈRE D'UNE TOILE EST ENGENDRÉE, PAS DESSINÉE.** Les dalles de l'app sortent du
> moteur — graines, poids, monde tiré au Studio — et respirent avec `performance.now()`.
> Celles de la planche sont **des courbes dessinées à la main**, cadre par cadre. Sur une
> fiche de Nuée, le champ occupe les deux tiers de l'écran : la mesure y donne **87 à 100 %
> de pixels différents**, et **aucune correction de forme n'y changera rien**.
> **Ce qui peut atteindre zéro, et qui se vérifie : la GÉOMÉTRIE** — chemins, cotes,
> épaisseurs, mots, couleurs. C'est ce que mesure `redteam_formes.py`.
> **Question posée à Tom** (`QUESTIONS.md` · Q74) : le « zéro au pixel » doit-il s'entendre
> comme « zéro sur la géométrie et les mots, la matière exceptée » ?

### Le contrôle de forme — ÉCRIT : `redteam_formes.py`

Celui qui manquait. Il ne lit pas le code : **il lit les pixels peints**, cherche le centre
du trait à chaque ordonnée, et le compare à la loi extraite du cadre. Tolérance 1,5 px.

```
LE BANDEAU DU FIL   x(u) = 121,0 − 4,3·u − 8,425·sin(2πu) · épaisseur 7 · sans chevron
                    4 points r 3,4 aux y 77 · 90 · 103 · 116
LA CARTE D'INDEX    épaisseur 5,5 × l/173 · tenu = entier · à tenir = moitié + chevron + 6 points
```

**Mesuré : la courbe du Fil colle à 1,02 px** après correction des trois coefficients.
**Il oscille encore entre 46 et 50 sur 50** : la dernière carte n'est pas toujours peinte
quand la sonde passe. L'attente sur « liste bâtie ET peinte » l'a amélioré (38→50 puis
46-50), **elle ne l'a pas stabilisé**. À finir.

### L'outil existe : `scratchpad/duo_pixel.py`

Il superpose le cadre de la planche et la capture de l'app, **et mesure**. Il ne dit pas ce
qui ne va pas : il dit **où**, et **combien**. Premier relevé, deux thèmes :

```
fil            dark  48,4 %      fiche-tenue    light 38,5 %
nuee-3         light 40,7 %      index-2        light 31,0 %
index-3        dark  40,6 %      fiche-encours  light 18,0 %
index-2        dark  39,8 %      page-plus      dark  14,7 %
```

> **⚠ CE CHIFFRE NE PEUT PAS TOMBER À ZÉRO, ET IL FAUT LE SAVOIR AVANT DE COURIR APRÈS.**
> La planche montre **ses** données — quatre entrées dans le Fil, « le grand plongeoir »,
> « faire les crêpes », des dalles tirées de ses mondes. L'app montre **les siennes** —
> douze entrées, d'autres titres, d'autres mondes, et une rangée « TENIR · REPORTER » sous
> chaque bandeau que la planche n'a pas. Corriger la forme **ne fera pas** converger le
> pourcentage. Ce qui converge, et qui se mesure, c'est **la géométrie** : chemins, cotes,
> épaisseurs, mots. Le pourcentage sert à **classer les écrans** et à voir **quelles bandes**
> diffèrent, pas à valider.
> **Ce qu'il faudrait pour un vrai zéro : mettre l'app dans les données de la planche** —
> un jeu de démonstration qui reprend les Promi du moodboard. Ce n'est pas fait, et c'est
> la première chose à faire au prochain tour.

### Ce qui est EXTRAIT, et qui fait désormais loi

Relevé au chemin, pas estimé (`/tmp/paths*.py`, à reprendre dans `scratchpad/`) :

**Le bandeau du Fil (cadre 76)** — SVG **143 × 128**, sans viewBox, posé à `left:0;top:0` :
```
champ  M121.0 0 → 24 segments de 5,333 → L116.8 128.0 L0 128 L0 0 Z     fill = nature
       x(u) = 121,0 − 4,3·u − 8,425·sin(2πu)          (base · montée · sinus · période 1)
trait  le MÊME chemin, u de 0 à 0,5 si une moitié manque, 0 → 1 si la parole est entière
       stroke = COULEUR D'ÉTAT · épaisseur 7 · bouts ronds · AUCUN CHEVRON
points 4 cercles r 3,4 aux y 77 · 90 · 103 · 116, sur le chemin, couleur d'état
```
**Corrigé :** l'app portait `0,34 × 358 = 121,72` et `amp 13,5` (montée 4,59, sinus 8,37).
Elle porte maintenant les trois coefficients de la planche. Et ils **ne suivent pas**
`mont = 0,34·amp / a = 0,62·amp` — le bandeau du Fil a ses propres coefficients.

**La carte d'Index (cadre 72)** — SVG **165 × h**, viewBox `0 0 165 h` :
```
champ  M0 base C… (Béziers) … L165 0 L0 0 Z                 fill = nature
trait  le même chemin · stroke = couleur d'état · épaisseur 5,2457 (= 5,5 × 165/173, §3.9 bis)
       tenu → chemin ENTIER, ni chevron ni points
       à tenir → chemin jusqu'à x = 82,5 (la moitié) + CHEVRON `M-3.7 -5.2 L3.1 0 L-3.7 5.2`
                 épaisseur 3,1, puis 6 points r 3,052 aux x 93 · 103,5 · 114 · 124,5 · 135 · 145,4
       Nuée en cours → chemin ENTIER en #D0B0FF, sans points
```
**Pas encore comparé à ce que l'app dessine.** C'est le prochain pas.

### Ce qui est corrigé

| | quoi | preuve |
|---|---|---|
| **le bandeau du Fil** | les trois coefficients de la planche, au lieu de valeurs déduites | chemin extrait du cadre 76 |
| **un Chiche dans une Nuée** | sa ligne disait « en cours », le mot d'un Promi. Elle dit **CHICHE LANCÉ / CHICHE RELEVÉ** — les mots du cadre défilé de `promi-nuee-toile.html` | mesuré : la ligne passe de « en cours » à « CHICHE LANCÉ » |

### Ce qui est VÉRIFIÉ ET N'EST PAS UN DÉFAUT

**Le compte inclut déjà les Chiche.** Mesuré : on met un vrai Chiche dans la Nuée, le compte
passe de **3 à 4**, sur la fiche comme sur la carte d'Index. `promisDeNuee` et le bâtisseur
de cartes filtrent sur `!draft && nuee===k`, sans exclure les Chiche.
**Ce qui manquait n'était pas le compte, c'était le MOT de la ligne** — corrigé ci-dessus.
⚠ Reste à vérifier : l'Aura, le Noyau et les légendes, non mesurés.

### Ce qui est OUVERT, et pourquoi je m'arrête là

1. **Les titres de nature.** Cherchés dans les cadres 72 (Index) et 76 (Fil), texte par texte,
   avec leurs cotes et leurs couleurs : **aucun n'y figure**. Les eyebrows de la planche sont
   « à moi », « à Rachel », « avec +4 », « à Marion », « Marion te lance un chiche »,
   « Adrien a planté » — la nature s'y lit à la COULEUR du champ et de l'accent, pas à un mot.
   **Je ne sais donc pas où Tom les voit**, et je n'invente pas un libellé. **Question posée.**
2. **Les textes qui se touchent dans l'Index**, et **les commentaires qui sortent de leur
   ligne** : signalés, pas encore reproduits ni mesurés.
3. **Le contrôle de forme dans les juges** : pas écrit. C'est le vrai manque de méthode —
   les cinq lignes du critère ne comparent aucune courbe.
4. **Les fiches, la page +, le Peaufiner, l'instant** : le comparateur les classe, aucun n'a
   été corrigé.

## 5 · Ce qui reste à faire — et c'est court

### `redteam_aveugle` — 24/26 · UN seul point, et sa cause est écrite

**Trois rouges sont tombés d'un coup, et ils n'avaient qu'une cause — LE TUTORIEL.**
« tenir au geste » (deux thèmes) et « planter » au second passage échouaient dans le parcours
complet et passaient seuls. Instrumenté à `elementsFromPoint`, sous le doigt :

```
DIV#tutoOv.tuto-ov2 in  [0,0 390x844]  z=120  pe=auto
```

`addPromi` lance le tutoriel du premier Promi **450 ms après la plantation** (`_tutoSeen`).
Il couvre tout l'écran, il prend les événements — et **`closeAll()` ne le connaît pas**. Tout
geste postérieur va donc au tutoriel : le geste de la fiche ne tient rien, et au parcours
suivant le geste de la page + ne plante rien. C'était bien « la même famille que ceux que
`closeAll` a absorbés » : **un calque de chrome qu'aucune fermeture n'atteint.** On le lui a
ajouté, avec **sa propre sortie** (`out`, puis retrait à 340 ms) : rien de réécrit.
L'ordre est sans risque — `addPromi` appelle `closeAll()` **avant** de programmer le
tutoriel ; on ne le tue pas à la naissance, on l'empêche de survivre à l'écran suivant, ce
que dit déjà son bouton final « Explorer mon Promi ». Bloc `lot-TUTO-CLOSEALL`.

> **La leçon, générale :** un rouge qui n'apparaît qu'**en parcours** ne se cherche pas dans
> l'écran qui échoue. **On demande au navigateur ce qu'il y a SOUS LE DOIGT** —
> `elementsFromPoint`, pas `elementFromPoint` : la pile entière, avec `z-index` et
> `pointer-events`. Trois mesures ont suffi, après cinq sessions de suppositions.

**Le rouge restant, le même dans les deux thèmes :** « Nuée · rien ne se superpose ». Le
bouton `#nfAdd` « + Planter un Promi » est peint à y = 776, la barre Peaufiner à y = 760.
**Il n'a pas de place parce qu'il n'en a pas :** aucune ligne « Planter » dans les vingt
écrans du §12, zéro occurrence dans `promi-nuee-toile.html` ; il n'existe qu'au **cadre 86**
— *« Planter un Promi dans la Nuée · DISSOUDRE LA NUÉE → Peaufiner ▴ »*, un contrôle du
**Peaufiner ouvert**. Le déplacer est le prochain lot (le Peaufiner d'une Nuée, cadres 84 à
87) ; le retirer sans l'avoir reposé supprimerait une fonction. `QUESTIONS.md` · Q61.

### La fiche de Nuée — PORTÉE, les 24 écrans à zéro

`redteam_nuee.py` — **22 écrans mesurés, 0 écart**, cinq lignes de critère comme les autres
juges. Sa référence n'est pas dans le fichier : **elle est extraite de
`PROMI-SPECIFICATIONS.md` à chaque passage** pour les vingt écrans du §12, et lue **dans le
moodboard** (cadres 84/86) pour le Peaufiner. Si le document bouge, le juge bouge avec lui.

| | ce qui est porté | où c'est écrit |
|---|---|---|
| **la hauteur du trait** | `base = max(176, 460 − 86 n)`, amplitude 40, Noyaux à `boîte − 29`, méta à titre + 65, fil à méta + 30 | §9 et §12 |
| **la Toile** | densité de semis du §10.6 (douze graines / 390 × 435), dalles du moteur, décalage tiré de l'id | §10.6, §11 · Q62 |
| **l'état vide** | douze graines crème `GLIGHT` dans les deux thèmes, entête à l'encre | §10.6 · Q59 |
| **l'état défilé** | base **58**, amplitude **16**, bande de 114 px, entête 23 / titre 26, fil dès 182 ; la Toile est **la même, remontée** | §9 et §12 · Q64 |
| **le défilement** | le doigt fait défiler **le fil**, pas les réglages ; Peaufiner ne s'ouvre **qu'en touchant sa barre** | §13 |
| **le Peaufiner** | DESCRIPTION · MEMBRES · PIÈCES JOINTES · COMMENTAIRES · Planter · DISSOUDRE | cadres 84 à 87 · Q65 |

**Ce qui reste ouvert, et c'est peu :** Q65 (les cadres 84 et 86 sont deux pages, l'app les
montre d'un seul tenant — s'il faut un geste entre les deux, il manque) ; Q64 (l'entête du
§12 écrit « amplitude = 40 » sur l'écran défilé, contre 16 au §9 et 114 dans son propre
tableau — corrigé dans le sens du §9).

### Le chantier des polices — 0 couple hors face

**En navigateur, une graisse absente se substitue en silence. En Swift, elle casse.** Audit
refait sur l'app d'aujourd'hui (`redteam_polices.py`, qui lit les `@font-face` du fichier —
la liste ne vit que là) : **7 couples absents, 359 éléments**, tous les écrans.

```
                    avant           après
Apfel 500            159 él.   →  ApfelMid 500
Bricolage 800         87 él.   →  Bricolage 700
Apfel 600             32 él.   →  ApfelMid 500
Apfel 400 italique    31 él.   →  Apfel 400        (l'oblique était synthétique)
ApfelMid 400          26 él.   →  Apfel 400
Apfel 700             20 él.   →  ApfelMid 500
Bricolage 400          4 él.   →  Bricolage 600
                     ─────
                     0 couple absent · 0 élément
```

**En JavaScript, et pas en CSS — la raison est écrite dans le bloc `lot-POLICES` :** le
couple dépend de DEUX déclarations, la famille et la graisse, qui vivent rarement dans la
même règle ; réécrire « 800 → 700 » à l'aveugle enverrait un `Apfel 800` sur `Apfel 700`,
tout aussi absent. Et le §9 interdit de nettoyer le CSS. **C'est une couche d'exécution, pas
une correction de source** (Q70) — la table de report fait foi pour le portage Swift.

> **⚠ DEUX PIÈGES PAYÉS SUR CE LOT, tous deux mesurés :**
> **1 · Une graisse lue trop tôt et figée change la hiérarchie.** La première passe posait
> son inline `!important` et n'y revenait plus : « Peaufiner » était lu à 400 avant que la
> feuille pose son 700, reporté sur 600, et gelé là. **La passe se RELIT** — sur un élément
> déjà touché, elle retire d'abord son propre inline, relit la cascade, puis décide.
> **2 · Ne toucher que ce qui porte du texte.** Réécrire la graisse d'un conteneur ne change
> rien à l'écran et pollue le contrat visuel — mesuré : `.dpd-tog` 400 → 600, alors que son
> libellé porte sa propre graisse. 86 écarts sont tombés à 35 avec ce seul filtre.

### Le dernier flake du projet — trois contrôles, une seule cause

`redteam_toile` flottait depuis le début. La cause n'était ni le hasard ni les polices :
**`Toile.dalleTrame` anime la matière avec `performance.now()` et recadre au plus juste sur
l'alpha.** Ni les pixels ni le format d'une dalle ne se répètent d'un rendu à l'autre — un
contrôle bâti dessus ne peut pas être stable.

| contrôle | ce qu'il comptait | ce qu'il compare |
|---|---|---|
| « les intitulés restent » | les pixels clairs de la planche (seuil 200) | `window._plancheComp` — quels intitulés, à quelles cases |
| « le % s'affiche » | les pixels clairs dans le trou de l'anneau | `window._noyauSig` — le chiffre composé, publié par `_sigBloc` |
| « la double encre » | les pixels terracotta et bleus du même trou | `window._sigEncres` — les trois passes décalées, publiées par `_sigText` |

**17/17 sur trois passages consécutifs.** Le principe est inscrit dans `CLAUDE.md §7`, et
c'est le même que celui de `scratchpad/semis_determin.py` : **on compare la composition, pas
la peinture.**

### Le passage d'usage à l'œil — ce que les chiffres ne disaient pas

`scratchpad/usage_oeil.py` : on plante, on remplit, on touche, on enchaîne, dans les deux
thèmes, et **on regarde**. Le parcours passe (planté 25 → 26, tenu au geste, zéro erreur JS).

**Une trouvaille, et aucun juge ne pouvait la voir :** sur un Promi **à moi**, un seul Noyau
à l'écran, la ligne d'état annonçait **« TENUE À DEUX · À L'INSTANT »**. Les mots viennent du
cadre 101, qui montre une parole tenue **avec quelqu'un** — c'est son cas, pas une formule.
Corrigé sans rien inventer : à soi, on écrit le mot que l'app emploie déjà (`STLAB.tenu`),
et rien de plus. **Les cinq lignes du critère mesurent la cote, le style et la peinture —
pas le sens du mot.** Q69.

### Ce que le portage a fait tomber en chemin

| trouvé | ce que c'était |
|---|---|
| **deux boutons « Planter »** | `#nqAddPromi` (balisage d'origine) **et** `#nfAdd`. Le premier se posait à y = 0, par-dessus « ✕ FERMER » — le défaut signalé. Un seul reste, dans le Peaufiner |
| **une bande figée à 232,67 px** | `.dp-nuee::before`, d'un lot antérieur au moteur géométrique. Invisible tant que la boîte était plus haute ; **elle dépasse dès que le champ se réduit**. Elle suit désormais la boîte (Q67) |
| **le crible de la section 2 mord sur la Nuée** | `s2-ouv` passe en `visibility:hidden` ce que SON inventaire ne liste pas. Les cartes d'une Nuée sortaient en `display:block` **et** invisibles (Q66) |
| **un garde pris sur un drapeau** | `bati()` se gardait avec un attribut sur `#dpdCorps` : `openEssaim` rebâtit le poster, les cartes disparaissent, le drapeau reste. **Le garde se prend sur le DOM** |
| **le juge mettait l'app en arrière-plan** | lire la planche dans un second onglet bride `requestAnimationFrame` sur le premier : `_fichePose` repeint sur deux rAF et ne repeignait plus. **On lit la référence d'abord, on ferme, on mesure ensuite** |

### La fiche de Nuée — l'ancien relevé, pour mémoire

`base = max(176, 460 − 86 n)` · amplitude **40** · Noyaux à **`boîte − 29`** · méta à
**titre + 65** · première ligne du fil à **méta + 30**. Mesuré sur une Nuée de trois Promi :
boîte **282**, Noyaux **253**, titre **407**, méta **472**, fil **502 · 588 · 674** —
**l'inventaire au pixel**, et la dernière ligne s'arrête bien à 12 px de la barre.
L'app portait `232 / 282` et `36 / 44`, **deux valeurs qui ne viennent d'aucune règle** : la
fiche de Nuée n'avait jamais été portée.

**Sa Toile aussi est portée** : les trois emplacements figés du cadre 58 ont été remplacés
par la **densité de semis du §10.6** (douze graines pour 390 × 435, soit un pas de 119 px),
jamais moins d'une graine par Promi, les dalles de la Nuée tournant sur les emplacements.
Zéro abscisse nue, à tout n, dans les deux thèmes. Voir Q62.

**Ce qui reste :** les **vingt écrans** du §12 un par un (styles, couleurs, l'état *défilé*
à base 58 / amplitude 16, le §13 « le doigt fait défiler le fil, pas les réglages »), le
**semis de la Nuée vide** (§10.6 : douze graines crème `GLIGHT`, mot-marque à l'encre — à
n = 0 le champ reste mauve nu), les **duos côte à côte** contre `promi-nuee-toile.html`, et le
juge **`redteam_nuee.py`** que le §15 décrit et qui n'existe pas encore.

### L'ancien relevé, pour mémoire — 21/26 · cinq points, deux causes

**Réparés** (en JavaScript, dans `lot-RESIDUS` — le CSS ne pouvait pas : `_ficheCotes` pose
ses `display` en ligne avec `!important`) : **le Cercle payé** ne montre plus ni verre
dépoli ni réclame, et **une Nuée ne se tient pas** (ni trait, ni geste, ni mot de trace).

**Reste :**

| | ce qui ne va pas | ce qu'il faut |
|---|---|---|
| **Nuée · superposition** | `#nqAddPromi` peint à **y = 0**, par-dessus « ✕ FERMER » | une cote. Le §5 le donne à 24 / 46, mais ce y est celui d'un autre cadre. **La fiche de Nuée n'a jamais été portée** — c'est un écran de plus à porter, pas un correctif |
| **parcours · tenir au geste** (×2) | échoue dans le parcours complet, passe seul | trancher : mise en scène du contrôle ou résidu |
| **parcours · planter, 2ᵉ passage** | la page + garde un état du premier | idem |

**Les trois derniers sont probablement UN SEUL défaut** — un état de la page + qui survit à
un parcours entier. C'est le prochain fil à tirer, et le seul qui reste sur l'usage.

⚠ **Un piège payé une fois :** retirer un `display` sans distinction emporte celui que
`_ficheCotes` pose légitimement (les sections 1 et 5 sont tombées à 4 écarts chacune).
**On marque ce qu'on masque et on ne rend que ça.**

### Trois éléments du moodboard restent des FONCTIONS, pas du dessin

Aucun ne manque d'une cote : il leur manque une **décision de produit**. Tous trois sont
dessinés et mesurés là où c'est possible, **aucun n'est branché à un geste**.

| | ce qui manque | état |
|---|---|---|
| **L'Index à trois par ligne** | aucun déclencheur : ni bouton, ni seuil, ni réglage | les deux densités sont portées et mesurées ; la bascule vit dans `window._s4Trois`, qu'aucun doigt n'atteint |
| **« L'autre moitié arrive »** | l'app ne modélise pas l'événement « quelqu'un trace, maintenant » | l'écran est porté et mesuré, avec la position du cadre (`window._instantX = 268`) |
| **« À TENIR · 2 J »** | l'app ne sait pas produire le compte de jours | la carte écrit « À TENIR » seul ; le bandeau du Fil ajoute le temps que l'app affiche déjà |

### Deux écrans de Peaufiner restent à 7 sur 9

Cause identifiée et documentée : `#tenirCv` sort du cadre dès qu'un conteneur positionné
devient son ancêtre (`CLAUDE.md §8`). La parade est de ne jamais faire entrer `#tenirZone`
dans un conteneur de réglages ; les deux écrans restants demandent une réorganisation du DOM
de Peaufiner qui n'a pas été tentée.

---

## 6 · Les contrats de test modifiés — ce qui a changé et pourquoi

**Trois outils ont été touchés. Aucun n'a été desserré.** Le principe, désormais inscrit
dans `CLAUDE.md §7` : *un contrôle qui encode une règle abandonnée se met à jour au niveau de
la décision, jamais en modifiant le comportement pour le faire passer.*

### 6.1 · `redteam_ecrans.py` — de 134/144 à 144/144

Cinq contrôles nommaient l'ancien marquage de l'Index et du Fil (`.ix-bloc`, `.ix-bd canvas`,
`.ix-bj`, `.fd-item`), que la section 4 remplace par `.s4-carte`.

- **Quatre sont de simples renommages** : même intention, nouveau nœud. On le note, on ne
  délibère pas.
- **Un a changé sur le fond** : « **seuls les urgents ont un aplat** » supposait que l'état
  vivait dans le **fond** du bloc (classe `.vif`). **Il vit dans la ligne** — le champ dit
  la nature, la ligne dit l'état, c'est la loi du produit (`CLAUDE.md §3`). Le test était
  **périmé**, comme « sens » et « quand » l'ont été. Il vérifie désormais qu'**aucune carte
  n'est peinte d'une couleur d'état** : il protège la même chose, au niveau de la règle
  actuelle. **Validé par Tom.**

Version d'origine conservée : `sauvegardes/redteam_ecrans-avant-S4.py`.

### 6.2 · `releve-design.py` — le sélecteur, puis le refigement

L'outil ouvrait ses fiches en cliquant `.ix-bloc.vif / .menthe / .nuee` dans l'Index. La
carte porte désormais la même information en attributs (`data-nat`, `data-etat`) et l'outil
les emploie — **rien de neuf, le même renseignement**.

**La référence a été refigée le 18 août 2026**, après validation des cinq sections.
Elle datait d'avant la section 1 et ne mesurait plus rien : **556 écarts identiques avant et
après le portage** (comparaison ligne à ligne des deux relevés — aucune ligne nouvelle).
Elle compte maintenant **6 configurations et 142 éléments**, et rend `✅ AUCUN ÉCART`,
stable sur deux passages consécutifs.
Ancienne référence conservée : `sauvegardes/design-reference-avant-portage.json`.

> ⚠ `CLAUDE.md §8 bis` annonce « 148 propriétés sur 26 éléments ». Le compte a changé avec la
> réécriture des fiches ; l'outil imprime le sien à chaque refigement, c'est lui qui fait foi.

### 6.3 · Trois sondes de juge corrigées — des faux rouges, pas des régressions

Ces trois-là ne mesuraient pas ce qu'elles croyaient. **Aucune n'a été desserrée : elles ont
été rendues justes.**

| Sonde | Ce qu'elle faisait | Ce qui a été corrigé |
|---|---|---|
| Le trait du Fil | Comptait les **colonnes** traversées | **Le trait du Fil est VERTICAL** (§3.10) : on compte les **lignes**. Il devenait invisible dès qu'une dalle était petite |
| La boîte du trait (S5) | Lisait `style.height` | **Mélangeait deux échelles** — `#device` est mis à l'échelle par une transformation. Sortait **412** sur un canevas de **384**. Elle se mesure dans le repère du cadre, comme tout le reste |
| La couleur de la ligne (S5) | Cherchait le premier pixel voisin à ±9 px | **Elle lit LE CENTRE du trait.** Sur « le trait se referme », tout le champ au-dessus de l'onde est menthe : la ligne d'encre passait pour menthe |

### 6.5 · Le lot du 19 août — quatre sondes réécrites, aucune desserrée

**La décision « la matière remplit le champ » a déplacé le nœud que quatre sondes visaient.**
Toutes lisaient **le champ en haut du cadre**, « loin de la dalle et du trait ». Ce point est
désormais **de la matière**. Aucune règle n'a changé, aucun seuil n'a bougé : c'est le point
de lecture qui est faux. `CLAUDE.md §7`, cas « la sonde vise le mauvais nœud ».

| sonde | ce qu'elle lisait | ce qu'elle lit |
|---|---|---|
| `redteam_tonsurton` · le trait | « le pixel le plus ÉLOIGNÉ du champ le long de l'onde » — donc une **dalle** dès qu'il y a de la matière | **la ligne par SA COULEUR**, du jeu du §2.1 bis, en écartant toute couleur trop proche du champ (sinon, sur « le trait se referme », le champ menthe passait pour la ligne) |
| `redteam_tonsurton` · le champ | le pixel en (23, base × 0,06) | **la couleur que l'écran DÉCLARE** (`_ficheEcran().natCol`, `_ppEcran()`) — la valeur de l'app, lue à l'exécution |
| `releve-S3-page-plus` | « la dalle ≠ l'aplat lu en (195,40) », et « un point à plus de 60 de cet aplat » | l'aplat = **`_onde.NATCOL[nat]`** ; les points **par leur couleur** |
| `releve-S5-instant` | le champ en (20,20) | le champ = **la couleur dominante du POURTOUR** du cadre — le seul endroit qu'une matière centrée mise en couverture ne recouvre pas. Toujours au pixel |
| `releve-S1-fiches` | « le mot-marque est `#F4EEE1` » | « le mot-marque est **l'une des DEUX encres** du produit » — c'est le §10.6, généralisé (Q59) |

**Bénéfice inattendu :** la première réécriture a **corrigé un flottement antérieur**.
« bandeau du Fil · le pire » sortait 26/26 **puis** 24/26 sur l'app **inchangée**, deux
passages consécutifs — sa recherche de ligne attrapait la dalle quand celle-ci mordait sur la
colonne du trait. `redteam_tonsurton` rend maintenant **26/26 sur trois passages de suite**.

Versions d'origine : `sauvegardes/redteam_tonsurton-avant-matiere.py`,
`sauvegardes/releve-S1-fiches-avant-matiere.py`, `sauvegardes/releve-S3-page-plus-avant-matiere.py`,
`sauvegardes/releve-S5-instant-avant-matiere.py`.

### 6.4 · Les flakes connus, reconfirmés

- **`redteam_toile`** — « Mes Promi : les intitulés restent », sonde à seuil sur un canevas
  animé. Vu à 15/16 puis 14/16, puis **16/16 et 16/16** sur deux passages consécutifs.
  **Un échec isolé ne prouve rien : il faut relancer.**
- **`redteam_geste`** — « l'anneau est peint à sa nouvelle place », oscille 12↔13/13.
  Même règle. À réécrire un jour : comparer l'anneau à sa propre référence.

---

## 7 · Les questions restées ouvertes

Onze questions, **Q41 à Q51 dans `QUESTIONS.md`**. Trois demandent une décision de produit
(marquées ★) ; les autres sont des choix conservateurs déjà appliqués, à confirmer.

| | Sujet | Ce qui a été fait en attendant |
|---|---|---|
| **Q41** | Le moodboard ne centre pas toujours la dalle d'une carte ; le §2.7 dit « toujours centrée » | Le document est appliqué : **centrée** |
| **Q42** | Les bases 376 et 372 sortent de l'échelle du §2.5 | **Bornées.** Corrigé dans le document — voir §4 |
| **Q43** | « avec +4 » n'a pas de version sans membre | Le mot que `buildIndex` écrit déjà : **« perso »** |
| ★ **Q44** | « À TENIR · 2 J » — l'app ne sait pas produire le compte de jours | **« À TENIR »** seul sur la carte ; le Fil ajoute le temps que l'app affiche déjà |
| ★ **Q45** | L'Index à trois par ligne n'a aucun déclencheur | Les deux densités portées, la bascule non branchée |
| **Q46** | Cinq contrôles de `redteam_ecrans` nommaient l'ancien marquage | Réécrits au niveau de la décision — **validé** |
| ★ **Q47** | « L'autre moitié arrive » n'a aucun déclencheur observable | Écran porté, position du cadre, sans déclencheur |
| **Q48** | La ligne de « le trait se referme » est à l'encre dans les deux thèmes — le §2.1 bis ne prévoit pas ce cas | Porté tel quel ; le §2.1 bis devrait le dire |
| **Q49** | « Rachel vient de tracer sa moitié » — sans autre personne, il manque un mot | La seconde phrase seule : **« Le dessin existe. »** |
| **Q50** | La dalle de l'instant ne suit pas la formule du §2.7 (180 × 150 contre 187 × 156) | **Les valeurs des cadres**, qui font foi |
| **Q51** | Combien de temps dure « juste après » ? | Tant que la fiche est ouverte |

**Questions plus anciennes toujours ouvertes :** Q37 (« planter au bouton » contre « garder
de côté » — deux mots pour un même créneau), Q38 (la taille de la phrase sur un choix
ouvert, écart assumé de 2 px), Q40 (la coupure de la question du cadre 17, obtenue par la
largeur et non par le moyen du document). Et le **point ouvert du §3 de `CLAUDE.md`** : le
décalage de teinte de 150° des traits, que Tom juge parfois hors palette — **non tranché,
ne pas trancher seul.**

---

## 8 · Les pièges qui ont coûté du temps — la liste courte

Ceux de `CLAUDE.md §8` restent tous valables. Ces cinq-là sont ceux que le portage a ajoutés
ou reconfirmés, et qui reviendront :

1. **Un `display` posé EN LIGNE bat un `!important` de feuille.** Le geste restait à l'écran
   sur les trois cadres de l'instant : la section 1 lui pose `display:block!important` en
   ligne. **On le sort en JavaScript, pas en CSS.**
2. **L'encre du CORPS n'est pas celle du CHAMP.** Le corps est **crème en thème clair** : un
   titre posé en crème y disparaît. Vu au duo — le titre « faire les crêpes » purement absent
   du cadre 101 clair. Le juge de présence peinte le rattrape (Δ luminosité < 42).
3. **Peindre après insertion (§4.5).** Une seule passe laissait la dalle vide par
   intermittence. On rejoue à **0, 60, 200 et 600 ms**, comme `peintMinis`.
4. **Un rendu qui remplace son propre marquage doit mémoriser ses entrées.** `_s4Index`
   remplace le contenu de `#indexList` : au second appel les `.ix-bloc` de l'app n'existent
   plus, et l'écran restait figé sur la densité du premier rendu.
5. **Le crible se pose nœud par nœud, jamais sur un conteneur ni une famille.** Deux fois
   déjà, un balayage en bloc a emporté un panneau qu'un doigt ouvre.

---

## 9 · Les outils

| Outil | Ce qu'il fait |
|---|---|
| `releve-S1-fiches.py` … `releve-S5-instant.py` | **Les cinq juges de section.** Cotes, styles, collisions, débordements, présence peinte, dans les deux thèmes |
| `releve-design.py` | Le contrat visuel — 6 configurations, 142 éléments. `--figer` pour recaler après validation |
| `redteam*.py` (8 batteries historiques) | Le comportement. **Aucune livraison si une régresse** |
| **`redteam_champs.py`** | **remplit** chaque champ : atteignable · accepte · la donnée reçoit · l'écran montre |
| **`redteam_pastilles.py`** | **touche** chaque pastille et vérifie qu'elle change quelque chose |
| **`redteam_enchaine.py`** | **enchaîne** deux écrans et compare le second à lui-même ouvert seul |
| **`redteam_fonctions.py`** | l'**inventaire des fonctions** qu'aucune refonte ne doit faire disparaître |
| **`redteam_photo.py`** | la photo de fiche, et sa présence partout où la matière s'affiche |
| **`redteam_tonsurton.py`** | un trait n'est jamais à moins de **42** de son champ (§2.1 bis) |
| **`redteam_aveugle.py`** | le Cercle payé · la Nuée en profondeur · un parcours entier |
| **`redteam_nuee.py`** | **la fiche de Nuée** : les 20 écrans du §12 + les 4 du Peaufiner, cinq lignes de critère. Référence extraite du document et du moodboard, jamais recopiée |
| **`scratchpad/semis_determin.py`** | **le semis d'une Nuée ne change jamais** — 3 ouvertures × 2 thèmes × 2 densités de pixels. Compare LA CASE, pas les pixels |
| **`scratchpad/mesure_vide.py`** | le bandeau de couleur nue entre la matière et le trait, et quelle base est **au plancher** |
| **`redteam_polices.py`** | **aucune graisse hors des six faces embarquées.** Il lit les `@font-face` du fichier : embarquer une face suffit à la lui faire connaître |
| **`scratchpad/duo_pixel.py`** | **superpose le cadre de la planche et la capture de l'app**, rend la part de pixels qui diffèrent, les bandes où ça diffère, et trois images (planche · app · différence). **Il classe, il ne valide pas** — voir §4 bis |
| **`scratchpad/usage_oeil.py`** | **le passage d'usage à l'œil** — planter, remplir, toucher, enchaîner, deux thèmes, et les captures qui vont avec |
| `scratchpad/duo.py <nom> <thème> <dossier>` | Colle le cadre du moodboard et la capture d'app **côte à côte**, avec une règle de cotes. **Un juge à zéro ne fait pas un écran** |
| `scratchpad/cap_s1b/s2/s3/s4/s5.py` | Les captures, cadrées sur le device, onboarding passé |
| `scratchpad/liste_cadres.py` | L'ordre **réel** des 102 cadres du moodboard — il n'est pas celui du document |
| `scratchpad/dump_cadre.py <n>` | Le HTML complet d'un cadre : **c'est là que sont les règles que le document ne donne pas** |
| `scratchpad/probe_ix.py` | Instrumente l'ouverture de l'Index et du Fil |
| **`scratchpad/mesure_vide.py`** | **Le bandeau de couleur nue entre la matière et le trait**, écran par écran, deux thèmes. Dit aussi quelle base est **au plancher**. C'est lui qui tranche « vide » contre « boîte du §2.7 » |

**Le serveur :** `python3 -m http.server 8752`, puis `http://127.0.0.1:8752/app.html`.
**Utiliser `127.0.0.1`, jamais `localhost`** — il bascule en https et échoue.

---

## 10 · Les sauvegardes

```
sauvegardes/avant-matiere-champ.html    l'état d'entrée du lot du 19 août
sauvegardes/lot-matiere-champ.html      la matière remplit le champ + la Nuée au trait entier
sauvegardes/lot-tuto-closeall.html      + le tutoriel que closeAll ne fermait pas
sauvegardes/lot-nuee-hauteur.html       + la hauteur du trait d'une fiche de Nuée
sauvegardes/lot-matiere-tuto-nuee.html  la première formulation, trop large (conservée)
sauvegardes/avant-plancher.html         l'état d'entrée de la correction
sauvegardes/lot-plancher.html           le vide corrigé au plancher
sauvegardes/avant-defile.html           avant l'état défilé
sauvegardes/lot-nuee-vingt-ecrans.html  les 20 écrans du §12 à zéro
sauvegardes/avant-peaufiner-nuee.html   avant le Peaufiner d'une Nuée
sauvegardes/lot-nuee-complete.html      la fiche de Nuée portée
sauvegardes/avant-flake-toile.html      avant la réécriture des contrôles au pixel
sauvegardes/lot-peauf-nuee-defile.html  le Peaufiner d'une Nuée, en deux pages qui défilent
sauvegardes/avant-polices.html          l'état d'entrée du chantier des polices
sauvegardes/lot-polices-usage.html      LE POINT DE REPRISE — polices + passage d'usage
sauvegardes/design-reference-avant-nuee.json   la référence visuelle d'avant le lot Nuée
sauvegardes/s3-complete.html            fin de la section 3
sauvegardes/avant-S4-index-fil.html     état d'entrée de la section 4
sauvegardes/s4-index-fil.html           fin de la section 4
sauvegardes/s5-instant.html             fin du portage (sections 1 à 5)
sauvegardes/reparations-livrees.html    les sept correctifs de CASSE.md
sauvegardes/lot-photo-livre.html        la photo de fiche
sauvegardes/lot-tonsurton.html          l'audit du ton sur ton
sauvegardes/lot-six-verts.html          les six chiffres d'usage au vert
sauvegardes/lot-aveugle-21.html         + le Cercle payé et la Nuée  ← LE POINT DE REPRISE
sauvegardes/redteam_ecrans-avant-S4.py  la batterie avant réécriture des cinq contrôles
sauvegardes/design-reference-avant-portage.json   la référence visuelle d'avant le portage
sauvegardes/ETAT-DES-LIEUX-v592.md      l'état des lieux d'avant le portage
```

---

## 11 · La dette technique — le point le plus grave

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


---

## 12 · Les performances

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

---

## 13 · Ce qui bloque quoi, aujourd'hui

```
Les quatre défauts de redteam_aveugle
   └─ bloquent : rien d'autre — mais ce sont les seuls défauts d'usage qui restent
   └─ deux d'entre eux demandent du JAVASCRIPT, pas du CSS (l'inline de _ficheCotes)

Les trois décisions de produit (l'Index à trois par ligne · « l'autre moitié arrive » ·
le compte de jours)
   └─ bloquent : ces trois écrans, dessinés et mesurés, mais branchés à aucun geste

Les deux écrans de Peaufiner (7/9)
   └─ bloqués par : #tenirCv, qui sort du cadre dans un conteneur positionné

Le décalage de teinte de 150° des traits (CLAUDE.md §3, point ouvert)
   └─ bloque : la validation visuelle définitive de toutes les fiches
```

---

## 14 · Si tu reprends demain

0. **RELANCE LE SERVEUR ET DONNE LES TROIS ADRESSES, EN TÊTE DU PREMIER MESSAGE.**
   `python3 -m http.server 8752 --bind 127.0.0.1`, puis `127.0.0.1:8752/app.html`,
   `/promi-moodboard-H.html`, `/promi-nuee-toile.html`. **Le port est 8752** — tous les outils
   le portent en dur. Vérifie qu'il ne tourne pas déjà : `lsof -nP -iTCP:8752 -sTCP:LISTEN`
   (le processus s'appelle **`Python`**, majuscule — un `grep python` ne le voit pas).
   C'est la première règle de `CLAUDE.md`.

1. **Lis `CLAUDE.md`** — il fait autorité sur tout le reste, et il a deux règles neuves
   (le contrôle périmé, §7 ; les pièges du §8).
2. **`PROMI-SPECIFICATIONS.md` est ta spécification** — cotes absolues et style de chaque
   élément. **Le §3.9 bis contient désormais la loi de la carte : ne la redéduis pas.**
3. **`promi-moodboard-H.html` est l'image de contrôle**, et parfois la source de la règle.
4. **Ouvre le navigateur.** Playwright lit des données, il ne voit pas qu'un écran est cassé.
   **Un juge à zéro ne fait pas un écran** — regarde les duos, dans les deux thèmes.
5. **`QUESTIONS.md` est le journal des décisions prises sans Tom.** Devant une ambiguïté :
   écris la question, prends l'option la plus conservatrice, **et continue**. Et si c'est un
   **mot** qui manque et qu'il n'existe nulle part : écris le plus sobre, note-le « à
   valider », avance (`CLAUDE.md §2`).
6. **Lance les sept contrôles d'usage AVANT de réparer quoi que ce soit.** Un juge de cote
   ne voit pas qu'un champ ne se remplit pas. C'est la leçon la plus chère du projet.
7. **Un contrôle rouge est soit un vrai défaut, soit un contrôle qui vise le mauvais nœud.**
   Sur ce lot, **cinq** rouges sur huit étaient des contrôles qui visaient à côté : les
   pastilles de Peaufiner (elles se déplient), le menu de tri (le voile, pas le panneau),
   `#addPromi` (au repos on trace, le bouton vient après la bascule), le créneau « quand »
   (retiré par Q28), le verbe d'un Chiche (il n'a pas d'alternative).
   **Vérifie toujours au doigt avant de corriger le produit.**
8. **Un rouge qui n'apparaît qu'EN PARCOURS ne se cherche pas dans l'écran qui échoue.**
   Demande au navigateur ce qu'il y a **sous le doigt** : `elementsFromPoint` — la pile
   entière, avec `z-index` et `pointer-events`. C'est ainsi que le tutoriel a été trouvé en
   trois mesures, après cinq sessions de suppositions.
9. **`redteam_polices.py` avant tout lot de dessin.** Une graisse ajoutée sans face part
   en substitution silencieuse ici, et casse en Swift. Le contrôle lit les `@font-face` du
   fichier : si tu en embarques une, il la connaît au passage suivant.
10. **Un rouge qui n'apparaît qu'après un rendu coûteux n'est pas un flottement.**
   `releve-S5-instant` a sorti « 4 écarts » puis « AU VERT », sans rien changer — profil de
   flake. **Ce n'en était pas un :** le rouge est tombé entre le patch de densité et le
   cache par id, quand `dalleTrame` était appelé une fois par case. L'app ramait, le canevas
   n'était pas fini quand le juge l'a lu. Quatre passages consécutifs au vert depuis.
   **Avant de classer flake : cherche ce qui a ralenti le rendu.** Et `redteam_toile` a
   tourné **dix minutes sans rendre la main**, deux fois, pour la même cause (Q63).
11. **LE PORTAGE EST FINI.** Cinq sections + la fiche de Nuée, toutes les batteries vertes,
   `redteam_aveugle` à 26/26. Ce qui reste est une **validation** : `releve-design.py`
   attend un `--figer` de Tom sur les 10 écarts du bouton déplacé, et Q65 attend son avis
   sur les deux pages du Peaufiner. **Le prochain chantier n'est plus du portage** — voir
   les trois décisions de produit du §5 (l'Index à trois par ligne, « l'autre moitié
   arrive », le compte de jours) et la dette CSS du §11. (cadres 84 à 87) : c'est lui qui donne sa
   place à « + Planter un Promi » et à « DISSOUDRE LA NUÉE », et c'est le dernier rouge de
   `redteam_aveugle`. Ensuite, les vingt écrans du §12 et le juge `redteam_nuee.py` (§15).
