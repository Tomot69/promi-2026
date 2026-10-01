# ÉTAT DES LIEUX

## ⚑ L'ORBITE EST DANS L'APP — `lot-AURA-ORBITE` · 10 septembre 2026

> **`app.html` modifié** — md5 avant `61280542751d0d0df5bce546f9a091b1`, **après `e10da6dc1bfb81aef2081b34e0c39b6b`**
> (rotation lente à 2 min — § 7 et Q173 ; retour de l'empreinte fini — § 4 quater ; régulateur de densité
> qui ne change plus rien sous les yeux — § 4 quinquies et Q181).
> Trois insertions intermédiaires ont été ANNULÉES : `8fa52b38…` (rotation plus lente), `a5a69b39…`
> (retour de l'empreinte qui sautait), `17e2e1ca…` (série verte, mais le régulateur changeait la
> matière sous les yeux).
> Sauvegarde : `sauvegardes/app-avant-aura-orbite.html`. Bloc neuf AVANT `</body>` : un `<style>`
> et deux `<script>` (`lot-AURA-ORBITE`, `lot-AURA-ORBITE-MOTEUR`). **Aucune règle existante touchée,
> aucune ligne du moteur de la Toile.** Point de reprise du chantier : `sauvegardes/orbite-velours/`.
> Matériel du lot : `sauvegardes/aura-orbite-lot/` (fabrique, css, js, preuves, mesures, captures, journaux).

### 1 · LE PREMIER CONTRÔLE — LA DENSITÉ. ⚠ PAS SUR UN TÉLÉPHONE.
Aucun appareil physique n'est joignable depuis cette machine. Ce qui suit est une mesure de
**substitution**, et je la dis comme telle : Chromium sur le Mac Intel i5-8279U (celui des bancs),
puis le même processeur **ralenti ×4** (profil « mobile moyen » de Lighthouse) et **×6**.
```
processeur  110 000    90 000    75 000     le gouverneur, parti de 110 000
   ×1      13,7 ms   12,2 ms   10,6 ms     reste à 110 000
   ×4      58,4 ms   51,9 ms   45,7 ms     descend à 75 000 (2 paliers) — 22 images/s
   ×6      88,6 ms   78,9 ms   69,7 ms     descend à 75 000 (2 paliers) — 14 images/s
```
**⚠ Et je le dis franchement : sur un processeur ×4, même le plancher ne tient pas 60 images par
seconde.** Le coût n'est pas proportionnel aux poils — 75 000 coûtent encore 78 % de 110 000. Une part
FIXE (~19 ms à ×4 : vider et verser le tampon 592 × 592, la peau, le comblement) dépasse à elle seule le
budget. **Le levier sur un appareil lent est la résolution du tampon, pas le nombre de poils.** → Q178.
**Ce qui répond au « si ça ne tient pas » : un régulateur, dans l'écran.** Il mesure chaque image ;
si la médiane dépasse une image à 60 Hz (16,7 ms), il VISE le palier le plus dense qui tiendrait
(110 000 → 90 000 → 75 000) ; si le palier du dessus tiendrait sous 15 ms au prorata des poils, il vise
de remonter. **La vise ne s'applique qu'à l'ouverture suivante, jamais sous les yeux** (§ 4 quinquies,
Q181 — un palier change 71 à 78 % des pixels). **La densité cède, jamais le comportement** — prouvé
sous ×6 : la rotation continue, le doigt tourne toujours, et la matière ne bouge pas d'une image.
**Ce qui reste à faire, par Tom : la mesure sur un vrai téléphone.** Servir le dossier sur le réseau
local par un SECOND serveur (le 8752 des outils ne bouge pas), ouvrir l'Aura dans Safari sur l'iPhone,
puis sur le Mac Safari → Développement → l'iPhone → console : `_aura.etat()` rend le palier tenu
(`palier`), la médiane par image (`ms`), le nombre de cessions (`cede`) et le palier visé (`vise`) —
**ouvrir l'Aura deux fois** : la vise ne s'applique qu'à l'ouverture suivante (Q181). **Dans le même geste, lever
la réserve du capteur** (le juge pilote une souris, pas un doigt : la taille du contact lue au capteur
n'est jamais testée) : pendant un appui, `_aura.etat().emp.a` rend le demi-axe réellement lu — 0,40 =
le pouce par défaut (le capteur n'a rien dit) ; entre 0,26 et 0,40 = le capteur a parlé. → Q178.

### 2 · LES CINQ FICHIERS — ET QUATRE RETOUCHES, DITES
Les cinq fichiers de `sauvegardes/orbite-velours/` sont portés **tels quels**, enfermés dans une
fonction (ils définissent `D`, `TAU`, `mix`, `hh`, `peint`… : posés à la racine, ils auraient écrasé
des globales de l'app). Rien ne sort sauf `window.OrbiteMoteur`. Quatre retouches, chacune par motif
`assert count == 1` dans `fabrique.py`, et aucune autre :
- **`batIles` — la source de la dalle.** `Toile.dalleGeneree` n'existe QUE dans la copie du moteur ;
  l'ajouter à `app.html` = toucher la Toile. Dans l'app une île est un Promi réel : sa vraie dalle,
  `Toile.dalleTrame(cv, id, 1, p.monde)`. → QUESTIONS Q168.
- **Le peigne tourne avec l'objet** — voir § 4.
- **Une caresse se retouche en place** (`retoucheTraces`), au lieu de refaire tout le cache — § 4 ter.
- **L'empreinte s'éteint avec sa profondeur** (`PEINT_FE`) — § 4 quater.

### 3 · #auraScreen, RÉÉCRIT EN ENTIER, DEUX THÈMES
Cotes de `ecranAura()` ÷ 0,872 ; Noyaux au §2.9 à la lettre. Le plateau (`Aura`, le i, ✕ FERMER)
reste. L'ancienne Aura est masquée **nœud par nœud** (25 enfants nommés) : ses nœuds restent dans le
DOM, parce que `buildAura()` les adresse par id et que le gestionnaire de `#souffleBtn` n'est pas
protégé. L'ombre de dalle de `.tuto-fond::before` se peignait derrière la sphère : masquée ici seulement.
**Captures finales, à 2×, sur l'app insérée `e10da6dc…`**, regardées une à une avant envoi
(`sauvegardes/aura-orbite-lot/finales/`) :
- `aura_{dark,light}.png` — l'écran au repos : plateau, sphère et ses îles, la phrase, les trois Noyaux,
  la légende, « ce que tu as tenu », le bouton.
- `aura_{dark,light}_caresse.png` + `_caresse_carte.png` — la trace, face à nous (vue d'avant la caresse
  remise, puis figée) ; la carte montre avant | après | l'écart ×8, dite comme telle. **La première
  capture de la caresse ne montrait rien** — le glissement tourne la sphère, les îles partaient derrière
  et la trace ne se voyait pas : refaite (`capture_caresse.py`).
- `aura_{dark,light}_personne.png` — un toucher sur un Noyau ouvre la fiche de la personne : c'est
  l'écran EXISTANT de l'app, pas refait dans ce lot (il porte « COMMENT ÇA ÉVOLUE » — Q183).
- `aura_{dark,light}_vide.png` — l'état vide : sphère sans île, « La première parole laissera sa trace ici. »
- `aura_rotation_20s.webm` — **20 s de rotation lente, en temps réel, à 1×** (les ~11 premières secondes
  du fichier sont le chargement de l'app). Mesuré pendant le film : **1,0489 rad en 20 s = 0,0524 rad/s**,
  la vitesse décidée. Une vitesse ne se juge pas sur une image fixe.
- `retour_film.png` — le retour de l'empreinte, avant/après la correction (§ 4 quater).
- `regulateur/paliers_{dark,light}.png` — les trois paliers de densité à vue égale (§ 4 quinquies).
**⚠ En clair, le pavage de la sphère se lit** — grandes plages bleu nuit à bords polygonaux, et une
tache presque carrée sur la sphère vide. La planche n'a été peinte que sur fond sombre ; en clair, le
crème passe entre les poils courts du sol. Pas un défaut prouvé, mais jamais validé : **Q182, à
trancher** — rien n'est changé en attendant.

### 4 · ⚠ LE PEIGNE ÉTAIT LIÉ À LA VUE — DEUX ACQUIS SE CONTREDISAIENT
Le peigne de la planche est l'horizontale de L'ÉCRAN au moment où le cache se remplit. L'Orbite
tourne toujours : ~41 s plus tard un zéro du peigne — **un épi** — arrive au centre de la face ; et
chaque caresse recuisait le peigne : **une caresse changeait 77 % des pixels**, un relissage laissait
7,8 %. Peigne azimutal (`u = y × p`) : égal au B de la planche au centre de la face, indépendant de la
vue. **Une caresse : 9,2 %. Relissé : 0,0000.** `scratchpad/aura/peigne_comparaison.png`. → Q172.

### 4 bis · TROIS COMPORTEMENTS QUI AURAIENT CÉDÉ SUR UN APPAREIL LENT — corrigés
- **L'élan était perdu quand les images ralentissent.** Les mouvements du doigt étaient horodatés
  à leur TRAITEMENT : livrés groupés après une image lente, ils tombaient « au même instant », la
  vitesse sortait nulle. On lit l'heure de l'ÉVÉNEMENT (`timeStamp`) et chacun des événements
  regroupés (`getCoalescedEvents`).
- **La rotation lente ralentissait avec les images.** La planche bornait le pas de temps à 50 ms :
  à 130 ms par image, la rotation tombait au tiers. Borne portée à 100 ms (le temps réel ; la
  borne ne sert qu'après une pause).
- **Une caresse faisait une saccade au lâcher** (le cache refait pendant l'élan). Elle s'inscrit
  maintenant au repos. → Q171.
- **La densité ne pouvait que descendre, et c'était gardé.** Un passage lent l'aurait abaissée pour
  toujours : elle remonte si le palier du dessus, au prorata des poils, tiendrait sous 15 ms — à
  l'ouverture suivante, comme la descente (§ 4 quinquies).

### 4 ter · ⚠ L'IMAGE DE 267 ms PENDANT L'ÉLAN — TROUVÉE AU PROFILEUR, CORRIGÉE, PROUVÉE
Relevé du juge : la plus longue image de l'élan faisait **267 ms, dont 16 ms pour le peintre**. Tom :
*« c'est le moment précis où l'objet doit être fluide »* — priorité avant tout le reste. Profileur du
navigateur (échantillon 0,5 ms), trois lancers, chaque tâche longue attribuée à ses fonctions
(`scratchpad/aura/profil_elan.py`, `profil_taches.py`).
**Les deux suspects de Tom, écartés ou confirmés :**
- **Le glaneur de mémoire : écarté.** 158 ms sur 20 s (0,8 %). Le peintre n'alloue pas par image.
- **Un recalcul qui n'a rien à faire là : CONFIRMÉ, deux fois.**
  1. **L'ombre de dalle (`frame`, l. 8917) — 27 % du fil.** Elle écrit trois variables héritées sur les
     douze écrans `.tuto-fond`, fermés compris, à chaque image ; la lecture d'`offsetParent` force
     ensuite le recalcul de style de milliers de nœuds cachés. Deux hypothèses fausses d'abord, et je
     les dis : ce n'était pas l'écriture sur l'Aura seule (bloquée : 27 % restait), ni la réassignation
     de taille du canevas du peintre (remplacée par un effacement : 27 % restait). **Prouvé par une
     sonde : 27 % → 1,6 %.** Corrigé en n'ignorant que ces écritures-là, sur l'Aura et sur les écrans
     cachés dessous tant qu'elle est ouverte. Le coût demeure ailleurs dans l'app → Q180, hors lot.
  2. **La reconstruction complète du cache à chaque caresse — 240 à 340 ms.** Pour UNE caresse on
     refaisait les 110 000 poils, relief `phi` compris, qui ne dépend pas des caresses. **La caresse se
     retouche maintenant** (`retoucheTraces`, la seule addition au moteur) : seuls les points proches
     des arcs qui changent. **Prouvé égal à une reconstruction complète** sur trois caresses et un
     relissage : lustre et main identiques point par point, sens du poil à 2·10⁻⁶ près (arrondi 32 bits).
     **10 à 14 ms au lieu de 210 à 320.**
- Et `couvert()` ne consulte plus le navigateur qu'une image sur six (il forçait la mise en page).
**Après :** `frame` 1,7 % ; plus aucune tâche au-delà de 120 ms pendant trois lancers.

### 4 quater · ⚠ LE RETOUR DE L'EMPREINTE SAUTAIT À LA FIN — vu par Tom, corrigé, mesuré

Tom : *« la dernière étape avant que la sphère ne redevienne lisse… ça passe de trop loin encore
déformé à net d'un coup »*. **Deux causes, lues dans le peintre :**
1. **L'empreinte était retirée à p = 0,02**, quand elle était encore profonde de 7 % de son
   maximum (≈ 1,4 pt) et large de 27 % de sa taille — on l'enlevait visible.
2. **Trois de ses effets ne dépendaient pas de la profondeur** : le poil peigné en rosette sous
   le doigt (100 %), l'ombre au fond du creux (jusqu'à −80 % de lumière) et le poil raccourci
   d'un cran sur toute la calotte touchée. Ils restaient ENTIERS jusqu'à la dernière image,
   puis tombaient ensemble.

**Le correctif — une 4ᵉ retouche du peintre, dite (`PEINT_FE` dans `fabrique.py`) :** une part
d'effet `FE = min(1, (d/dmax)/0,3)`, pleine tant que le creux garde 30 % de sa profondeur
(donc **rien ne change pendant l'appui ni au début du retour**), puis proportionnelle à la
profondeur jusqu'à zéro. La rosette, l'ombre, la normale et la position du fond plat la
suivent ; le poil raccourci est **tramé** point par point (une part FE des points). Et
l'empreinte n'est retirée qu'à **p = 0,002** (0,4 pt, effets à 5 %) — quand elle est
invisible. La durée du retour, en usage, ne change pas : c'est le comblement (lié à la
rotation) qui la termine.

**Le contrôle, prouvé dans les deux sens :** `releve-aura.py` enregistre dans la page **chaque
image peinte du retour** et mesure le DERNIER PAS (dernière image déformée → première image
lisse) **en amplitude** — l'écart moyen en niveaux sur la zone du doigt : il ne doit pas
dépasser 3 fois la médiane des 10 pas qui le précèdent (plancher 0,5 niveau).
**⚠ Sa première écriture était MORTE, et c'est la preuve qui l'a dit.** Elle comptait la PART
des pixels qui changent. Un retour lisse en change déjà beaucoup, d'un rien, à chaque image
(médiane 17 %) ; le saut de l'ancienne version (43,9 %) passait dessous — **vert sur la version
fautive**. Réécrite en amplitude avant de juger la version corrigée, et bornée d'un plafond
absolu d'**1 niveau** : la règle relative seule ne prenait l'ancienne version qu'à 3,5 fois la
médiane pour un seuil à 3 — un contrat à marge mince oscille.

```
                     écart au repos, niveaux (zone du doigt)          DERNIER PAS   médiane   images
avant (p 0,02)       40,0 → 36,0 → 31,2 → 25,0 → 17,8 → 8,4 → lisse     8,45        2,48      119   ❌ pris
après (FE, p 0,002)  40,5 → 36,4 → 30,9 → 20,7 →  9,4 → 0,5 → lisse     0,46        0,83      131   ✅
```

Les 14 dernières images d'avant le retrait, corrigée : 4,9 · 4,4 · 4,0 · 3,7 · 3,3 · 2,9 · 2,6 ·
2,4 · 2,0 · 1,7 · 1,5 · 1,0 · 0,67 · 0,46 → lisse. Rien d'autre n'a bougé (rotation 0,0528,
élan à 0 écart de la loi, prise au millième) ; le creux vit 3,52 s au lieu de 3,29 — les
0,2 s de la fin qui manquait. Relevés : `sauvegardes/aura-orbite-lot/retour_{ancien,fe}.txt` ;
planche avant/après des dernières images : `retour_film.png`.

**Tom a validé le diagnostic et la correction, et demandé deux vérifications** (`preuve_retour_trace.py`,
ancienne version contre l'app insérée, trois fois chacune, vue figée, thème sombre) :
1. **Le retour reste-t-il rapide ?** On n'échange pas un saut contre une traîne.
2. **La trace survit-elle au creux ?** Ce qui disparaît, c'est la DÉFORMATION ; le poil couché, le
   lustré et la chroma restent — c'est le cœur du concept.

**Dans le code, d'abord :** `FE` n'est lu qu'à cinq endroits, tous dans le peintre — trois DANS le bloc
du contact (`if(E){`, qui ne tourne que tant qu'un doigt ou un creux existe), deux derrière `mo`
(les points que le contact touche). La trace, elle, vit dans le CACHE du peintre : le poil couché
(`champPoil(…, o.traces)`), le lustré (`m_poli`), la chroma (la boucle sur `o.traces`), et
`retoucheTraces` — **aucun ne lit `FE`**. Creux refermé, seul le cache peint. Et pendant le retour,
la rosette des points touchés se fond vers le sens du poil DU CACHE — celui qui porte déjà la
trace : la trace réapparaît en continu sous le creux qui s'efface, là où le saut la découvrait
d'un coup.

**1 · La durée — mesurée, trois fois chacune** (appui 950 ms, écart moyen au repos sur la zone du
doigt, en niveaux ; le temps compte depuis le lâcher) :
```
             moitié partie   reste 10 %   plus rien à l'œil (< 1 niv)   retirée    ce qui restait au retrait
avant          2,49 s          3,21 s       3,21 s — PAR UN SAUT          3,21 s      8,51 niveaux
après          2,33 s          3,21 s       3,40 s                         3,44 s      0,53 niveau
```
**Pas de traîne.** Le corps du retour est aussi rapide, plus rapide même à mi-course (−0,16 s : les
effets suivent la profondeur au lieu de rester entiers) ; les 10 % derniers tombent au même instant.
Ce qui s'ajoute, ce sont **0,19 s** — le temps que ces 10 % derniers se dissolvent au lieu d'être
coupés. En usage, c'est le comblement lié à la rotation qui termine le retour : il n'a pas changé.

**2 · La trace — elle reste.** Une caresse ; creux refermé et caresse inscrite, on mesure la part de la
boule qui la porte et son amplitude ; puis 5 s plus tard, même vue, contre un relissage pris JUSTE
APRÈS au même palier de densité :
```
                     juste après le creux          5 s plus tard            l'image a bougé de
avant  (110 000)     9,6 % des pixels · 1,48 niv    9,6 % · 1,48 niv         0,000 niv (×3)
après  (110 000)     9,6 % des pixels · 1,50 niv    10,3 % · 1,67 niv ¹      —
après  ( 90 000)     10,3 % des pixels · 1,67 niv   10,3 % · 1,67 niv        0,000 niv (×2)
```
**À densité égale, la trace est la même avant et après la correction** (9,6 % · 1,48 contre 9,6 % ·
1,50), **et elle ne bouge pas d'un niveau en 5 s.** ¹ Une seule image a bougé en entier (10 niveaux) :
le gouverneur venait de descendre de 110 000 à 90 000 poils — la série de batteries tournait à côté et
chargeait la machine. Tous les poils changent alors d'un coup ; la trace, mesurée contre un relissage
au même palier, est toujours là. **⚠ Ma première mesure ne l'avait pas vu** : elle comparait l'image de
5 s à une référence prise AVANT la caresse, donc avant le changement de palier — 3 passes sur 6
annonçaient « 76 % des pixels ont bougé ». C'était l'instrument, pas la trace.
Relevés : `sauvegardes/aura-orbite-lot/preuve_retour_trace.log`, `preuve_trace2.log`.

### 4 quinquies · ⚠ LE RÉGULATEUR DE DENSITÉ CHANGEAIT LA MATIÈRE SOUS LES YEUX — mesuré, tranché (Q181)
Vu en mesurant la trace : sous charge, toute l'image changeait d'un coup. Tom : *« si le régulateur
est nécessaire, il l'est — mais il doit être imperceptible »*. **Mesuré** (`mesure_regulateur.py`,
planches `regulateur/paliers_{dark,light}.png`, même vue figée) :
```
                          pixels qui changent   amplitude   luminance de la boule
sombre  110 000 → 90 000        71,4 %          10,7 niv     93,0 → 90,2   (−2,8)
sombre  110 000 → 75 000        76,1 %          14,1 niv     93,0 → 86,4   (−6,6)
clair   110 000 → 90 000        73,2 %          10,3 niv    106,7 → 111,5  (+4,8)
clair   110 000 → 75 000        77,6 %          14,9 niv    106,7 → 117,9  (+11,2)
premier passage à 90 000, sphère qui tourne : UNE IMAGE DE 783 ms (peintre 526 ms) — contre 50 au plus
sous ×4 : 110 000 → 90 000 à 7,2 s, → 75 000 à 13,9 s ; charge levée : → 90 000 en ≈ 3 s, → 110 000 en ≈ 13 s
```
- **Ça se voit.** Un palier n'est pas un sous-ensemble du précédent : c'est un AUTRE semis (la spirale
  dépend du nombre de poils) — chaque poil change de place. **Et la matière s'éclaircit en clair** : le
  fond crème passe entre les poils, les îles sombres deviennent un semis pâle ; en sombre elles se
  trouent de noir.
- **Ça remonte** — mais chaque remontée est un nouveau changement de toute la texture : un épisode de
  charge en fait QUATRE.
- **Quand** : jugé sur les 45 dernières images, suspendu seulement tant qu'un creux existe. Rien ne
  l'empêchait en plein élan (l'élan dure jusqu'à 5,2 s, le creux se referme en 0,4 s). Possible par le
  code ; **pas observé** dans ma mesure (l'élan s'y était éteint avant le premier palier).

**Tranché, option la plus sobre (Q181, à confirmer) : le régulateur mesure et VISE pendant qu'on
regarde ; la vise ne s'applique qu'à l'OUVERTURE suivante**, pendant que l'écran se bâtit (`prepare`).
Aucun changement de matière, aucune image figée sous les yeux — jamais. Coût, dit franchement : une
session sur un appareil lent reste entière au palier où elle a commencé ; il pèse peu (×4 : 17 images/s
à 110 000, 22 à 75 000 — le vrai levier est la résolution du tampon, Q178). **L'alternative**, si Tom
veut une densité qui s'adapte pendant la vue : des paliers EMBOÎTÉS et un éclaircissement en fondu sur
une ou deux secondes — une retouche du moteur, lot à part.
**Contrat réécrit** (`releve-aura.py`, famille 8 — original `sauvegardes/releve-aura-avant-regulateur.py`) :
sous ×6, le régulateur doit DÉCIDER de céder (vise plus basse gardée), le palier peint ne doit pas
bouger d'une image tant que l'Aura est ouverte, la vise doit prendre effet à la réouverture, et les
gestes doivent tenir. **Prouvé dans les deux sens :** sur la version d'avant (`17e2e1ca…`) il est
PRIS — « le palier a changé sous les yeux : 110 000 / 90 000 » et « aucune vise gardée » ; sur la
version corrigée il passe — palier peint 110 000 d'un bout à l'autre sous ×6, vise 75 000 (une
décision, au prorata du budget), 75 000 à la réouverture, gestes intacts, les huit acquis inchangés.

### 5 · LES VRAIES DONNÉES — et c'était là que tout pouvait mentir
Le jeu de l'app (celui du moodboard) donne **5 paroles tenues**, toutes des Promi → **sol bleu** ;
**2 personnes** (Marion, Rachel, par ordre alphabétique) ; 5 îles peintes pour 5 tenues. Vérifié en
FAISANT MENTIR les données, dans l'app, puis en restaurant :
```
toutes mes tenues passées en Chiche        nature « chiche », sol peint à ~345° (framboise)
toutes passées dans une Nuée               nature « nuee »,   sol peint à ~262° (mauve)
zéro parole tenue                          n = 0, nature « promi » (bleu, la base)
la plus récente plantée en braille/océan   son île porte ['braille','ocean'] et sa dalle tenue
                                           sort dans la palette OCÉAN, pas celle du Studio
le Studio passe en océan                   le monde des dalles déjà plantées ne bouge pas
USER.photo posée                           « toi » prend la vraie photo (data-photo)
tout gardé de côté                         l'état vide : sa phrase, pas de Noyaux, sphère pleine
```
⚠ **Ce que les données disent, et qui n'est pas un défaut :** les cinq Promi du jeu ont tous été figés
en `encre` par le rattrapage `_figeMondesManquants` (« rien n'est tiré de leur date ») : les îles sont
toutes du même monde, là où la planche les mélangeait à la main. La diversité viendra des plantations
futures. Et la COULEUR d'une dalle est tirée au hasard à chaque chargement (moteur, connu) : deux
captures successives n'ont pas les mêmes teintes d'îles.

### 6 · releve-aura.py — LE JUGE
Huit familles, deux thèmes : positions (> 3 px), styles, collisions, débordements (la rangée des
Noyaux exemptée SOUS CONDITION), **présence peinte** (la sphère lue dans ses pixels — disque plein,
transparent autour, teinte du sol ; les îles comptées dans la composition publiée ; arcs, visages et
dalles tenues lus), données, les huit acquis, densité. **La matière respire** : aucune égalité de
pixels n'est exigée ; les égalités se lisent dans `window._auraComp`, les pixels ne disent que « peint /
pas peint » et « a changé / est revenu », à vue figée (`_aura.fige`).
**Trois erreurs du juge lui-même, trouvées en route et dites :** il lisait une composition périmée
(avant de rouvrir) ; il photographiait avant que l'image recalculée soit peinte (il attend désormais
deux images RÉELLEMENT peintes, jamais un délai) ; il prenait une image de 100 ms pour une saccade.
**Le critère de saccade est réécrit au niveau de la règle** — la continuité : chaque vitesse suit
`v·exp(−Δt/0,55)` sur le temps réellement écoulé. Prouvé sur séquences : élan régulier et image de
100 ms passent ; remise à zéro en plein élan PRISE (2,23 rad/s d'écart), vitesse coupée de moitié PRISE.
**Et Playwright ne sait pas lancer** : face à un fil principal occupé, ses mouvements arrivent à
~130 ms les uns des autres et le relâcher 129 ms après le dernier — un doigt qui s'arrête. Les
lancers du juge se jouent donc DANS la page, cadencés à 16 ms.

### 7 · LES HUIT ACQUIS, DANS L'APP — la valeur mesurée de chacun
`releve-aura.py`, Chromium, deux thèmes, sphère en rotation. ⚠ **Une souris, pas un doigt** : le pointeur
est la souris de Playwright ; les lancers sont des événements pointeur joués dans la page, cadencés à
16 ms. **Le chemin qui lit la taille réelle du contact au capteur n'est jamais testé** — c'est la valeur
par défaut du pouce qui joue. À mesurer sur appareil, avec la densité (Q178).
Les deux colonnes sont relevées sur l'app INSÉRÉE finale (`17e2e1ca…`), recopiées telles quelles
depuis les journaux du juge (`table_valeurs.py`) — aucune valeur retapée à la main.
**Un chiffre par acquis, dans les deux thèmes** — extrait des journaux par `table_valeurs` (motifs sur les
lignes du juge, aucun chiffre retapé) :
```
                       SOMBRE                                               CLAIR
1 · rotation lente     0.0528 rad/s (décidé 0,0524)                         0.0528 rad/s (décidé 0,0524)
2 · prise, droite      Δlac +0.809 (att. +0.808)                            Δlac +0.809 (att. +0.808)
2 · prise, bas         Δtan -0.538 (att. -0.538)                            Δtan -0.538 (att. -0.538)
2 · prise, diagonale   Δlac -0.604 · Δtan +0.404                            Δlac -0.604 · Δtan +0.404
3 · élan               9.36 rad/s → éteint 5.2 s → 0.0528 rad/s · écart loi 0.0000 9.66 rad/s → éteint 5.2 s → 0.0518 rad/s · écart loi 0.0000
4 · retour             dernier pas 0.43 niv (médiane 0.88)                  dernier pas 0.56 niv (médiane 0.83)
4 · toucher            p 1.000 / 1.000 · 98.3 % sous le doigt               p 1.000 / 1.000 · 98.0 % sous le doigt
5 · trace              gardée · 9.8 % des pixels                            gardée · 10.7 % des pixels
6 · comblement         creux 3.58 s lâché · 0.39 s lancé                    creux 3.58 s lâché · 0.39 s lancé
7 · relisse            0 caresse · écart 0.000 %                            0 caresse · écart 0.000 %
8 · personne           toucher → « Marion » · glisser 1.14 rad, rien d'ouvert toucher → « Marion » · glisser 1.11 rad, rien d'ouvert
croissance             tour 5 · z = 0.942                                   tour 5 · z = 0.939
palier                 densité 110000 · 13.6 ms/image · ×6 : vise 75000, rouverte à 75000 densité 110000 · 13.4 ms/image · ×6 : vise 75000, rouverte à 75000
```

**Les deux relevés complets, tels que le juge les imprime :**
```
LES VALEURS MESURÉES — acquis joués en thème sombre
   1 · rotation lente   0.0528 rad/s sur 2 s (décidé 0.0524, un tour en 2 min)
   2 · prise, droite    Δlac +0.809 (attendu +0.808) · Δtan +0.000 (attendu +0.000)
   2 · prise, bas       Δlac +0.003 (attendu +0.000) · Δtan -0.538 (attendu -0.538)
   2 · prise, diagonale Δlac -0.604 (attendu -0.606) · Δtan +0.404 (attendu +0.404)
   3 · élan             au lâcher 9.36 rad/s · éteint à 5.2 s · puis 0.0528 rad/s · écart max à la loi 0.0000 rad/s · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s)
   4 · retour           écart au repos (niveaux) : 40.5 → 36.4 → 31.0 → 23.2 → 11.3 → 0.4 → lisse · DERNIER PAS 0.43 niveau (médiane des 10 d'avant 0.88) · 130 images · empreinte retirée à 3.27 s
   4 · toucher          p 1.000 à 250 ms, 1.000 à 950 ms · sous le doigt 98.3 % des pixels changent, hors de portée 1.78 %, bruit 0.00 % · revenu ≈ 3.3 s après le lâcher, écart au repos 0.00 %
   5 · trace            en attente au lâcher : 1 · 0 → 1 caresse(s), gardée(s) : 1 · au repos, 9.8 % des pixels portent la caresse
   7 · relisse          deux touchers à 120 ms : 0 caresse restante · écart à l'objet neuf 0.000 % des pixels
   6 · comblement       le creux vit 3.58 s lâché sur place, 0.39 s lancé (11 %)
   8 · personne         toucher sur « Marion » → ouvre « Marion », fiche affichée · glissement de 30 pt sur la rangée → n'ouvre rien · glissement de 80 pt sur la sphère → Δlac 1.14 rad, personne d'ouvert
   croissance           une parole de plus → tour 5 · la dernière dalle finit face à toi, z = 0.942

palier 110000 · médiane 13.6 ms · 1886 images · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s) · sous ×6 : palier peint 110000 pendant qu'on regarde, vise 75000, 1 décision(s) · à la réouverture : palier 75000
✅  L'AURA AU VERT
```
```
LES VALEURS MESURÉES — acquis joués en thème clair
   1 · rotation lente   0.0528 rad/s sur 2 s (décidé 0.0524, un tour en 2 min)
   2 · prise, droite    Δlac +0.809 (attendu +0.808) · Δtan +0.000 (attendu +0.000)
   2 · prise, bas       Δlac +0.003 (attendu +0.000) · Δtan -0.538 (attendu -0.538)
   2 · prise, diagonale Δlac -0.604 (attendu -0.606) · Δtan +0.404 (attendu +0.404)
   3 · élan             au lâcher 9.66 rad/s · éteint à 5.2 s · puis 0.0518 rad/s · écart max à la loi 0.0000 rad/s · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s)
   4 · retour           écart au repos (niveaux) : 40.4 → 36.7 → 30.1 → 21.3 → 9.9 → 0.6 → lisse · DERNIER PAS 0.56 niveau (médiane des 10 d'avant 0.83) · 132 images · empreinte retirée à 3.27 s
   4 · toucher          p 1.000 à 250 ms, 1.000 à 950 ms · sous le doigt 98.0 % des pixels changent, hors de portée 1.84 %, bruit 0.00 % · revenu ≈ 3.3 s après le lâcher, écart au repos 0.00 %
   5 · trace            en attente au lâcher : 1 · 0 → 1 caresse(s), gardée(s) : 1 · au repos, 10.7 % des pixels portent la caresse
   7 · relisse          deux touchers à 120 ms : 0 caresse restante · écart à l'objet neuf 0.000 % des pixels
   6 · comblement       le creux vit 3.58 s lâché sur place, 0.39 s lancé (11 %)
   8 · personne         toucher sur « Marion » → ouvre « Marion », fiche affichée · glissement de 30 pt sur la rangée → n'ouvre rien · glissement de 80 pt sur la sphère → Δlac 1.11 rad, personne d'ouvert
   croissance           une parole de plus → tour 5 · la dernière dalle finit face à toi, z = 0.939

palier 110000 · médiane 13.4 ms · 1898 images · plus longue image pendant l'élan : 50 ms (dont peintre 13.1 ms), 0 image(s) non échantillonnée(s) · sous ×6 : palier peint 110000 pendant qu'on regarde, vise 75000, 1 décision(s) · à la réouverture : palier 75000
✅  L'AURA AU VERT
```

### 8 · TROIS CONTRATS DE BATTERIE RÉÉCRITS — ET PROUVÉS
**J'ai réécrit des contrats de test** (CLAUDE.md §7) — l'Aura est réécrite, et ses nœuds anciens restent
dans le DOM, masqués : un contrôle qui les viserait passerait VERT sur une interface morte.
- `redteam_ecrans.py` — onze contrôles de l'ancienne Aura, chacun ramené à la décision qui l'a remplacé
  (l'Aura sans chiffre, la porte « Partager mon Noyau » rétablie, la dalle figée à sa plantation, la
  piste neutre du §2.9) ; deux fusionnés et dits (le % en signature et son décalage protégeaient la même
  chose). `DEBORDE` exempte une rangée `data-glisse` SOUS CONDITION (elle tient dans l'appareil et rogne).
  Original : `sauvegardes/redteam_ecrans-avant-aura-orbite.py`.
- `redteam_air.py` — l'Aura entre dans sa liste : c'est ce qui fait MORDRE le contrôle du bloc centré.
  Original : `sauvegardes/redteam_air-avant-aura-orbite.py`.
- **Prouvés contre un vrai défaut, DANS LES DEUX SENS, sur l'app insérée finale** (`e10da6dc…`, sans
  aucune injection — `sauvegardes/aura-orbite-lot/preuve_contrats.py`, relevé `preuve_finale.log`) :
  **les 18 passent tels quels, et les 18 PRENNENT le défaut posé exprès.** Une sonde était fausse au
  premier passage — `overflow-x:visible` à côté d'un `overflow-y:hidden` se recalcule en `auto` : la
  rangée rognait toujours ; la vraie sonde ouvre les deux axes.
- **`releve-aura.py` — un contrat NEUF, pas réécrit** : le retour de l'empreinte (§ 4 quater). Sa
  première écriture était morte ; la seconde prend l'ancienne version (8,45 niveaux) et passe la
  corrigée (0,46).

### ⚠ LA PREMIÈRE SÉRIE APRÈS INSERTION A ROUGI DEUX FOIS — ARRÊT, RESTAURATION, ET CE QUE C'ÉTAIT
Règle de Tom : *batterie verte qui rougit → arrêt immédiat et restauration*. `app.html` a été remis à
`61280542…` aussitôt ; la version insérée gardée à côté (`scratchpad/aura/app-insere-efbe.html`), et
tout le diagnostic fait sur une COPIE (`--copie`), jamais sur le fichier.
- **`redteam_ecrans` 149/150** — « la piste est neutre » en passe **[sombre]**. Ce n'était pas le CSS :
  cette batterie ne pose jamais le thème sombre (sa passe « sombre » n'ajoute simplement pas `.light`),
  et l'app démarre en CLAIR (relevé : `#device.light`, fond crème, `promi_theme = light`). **Mon contrat
  réécrit lisait l'étiquette de la passe au lieu du thème affiché** ; il lit `#device.light`, comme le
  faisait déjà sa preuve. Règle intacte : la piste est neutre pour le thème qu'on voit.
- **`releve-aura` — « une saccade »**. Deux choses mêlées : **mon échantillonneur** avait lu deux images
  de 130 ms comme une seule de 260 et appliqué UNE décroissance au lieu de deux — il lit désormais le
  pas de temps de LA BOUCLE, publié (`tick`, `dtReel`) ; et **de vraies images longues** existent
  pendant l'élan — voir « ce qui n'est pas fait ».
Sur la copie : `redteam_ecrans` 150/150, `releve-aura` au vert. Réinséré (md5 `4cfa48fe…`, identique
à la copie jugée), puis série complète.

### CONTRÔLES
**Série complète, EN SÉRIE (une batterie à la fois), sur l'app insérée finale `e10da6dc…`** — journal
`sauvegardes/aura-orbite-lot/bat_apres6.log`, 17 batteries, aucune sortie en erreur. (La même série était
déjà verte, 17/17, sur `17e2e1ca…` — `bat_apres5.log` — avant la correction du régulateur.)
```
redteam_ecrans      150/150        redteam_vide        61/61
redteam             15/15          redteam_air         ✅ 448 paires, 38 écrans, deux thèmes
redteam2            10/10          redteam_champ       32/32
redteam3            18/18          releve-design       ✅ aucun écart
redteam_demande     19/19          redteam_fonctions   22/22
redteam_toile       17/17          redteam_polices     0 couple absent
redteam_geste       13/13          redteam_superpo     0 recouvrement de texte
redteam_verbe       6/6            releve-aura         ✅ au vert — 8 familles ; sous ×6 le palier
                                                        peint reste 110 000, vise 75 000 à la réouverture
redteam_filets      0 filet parasite
```
Syntaxe : `node --check` sur tous les `<script>` d'`app.html` — OK. Preuve des contrats réécrits sur
cette même app : 18/18 dans les deux sens (§ 8).

### ⚠ CE QUI RESTE OUVERT — trois choses, et aucune n'est dans ce lot
**1 · La densité et le capteur, sur un vrai téléphone.** 110 000 poils est un plafond mesuré sur le Mac
Intel du banc ; sur un processeur ralenti ×4, même le plancher de 75 000 ne tient pas 60 images/s (la
part fixe du tampon domine — Q178). Et **la taille réelle du contact n'a jamais été testée** : le juge
pilote une souris, c'est la valeur par défaut du pouce qui joue. **Ce qu'il faut pour lever la réserve :**
- un iPhone (et si possible un Android de milieu de gamme) sur le même Wi-Fi que le Mac ;
- servir le dossier sur le réseau par un SECOND serveur, sur un autre port que 8752 (qui reste réservé
  aux outils, lié à 127.0.0.1) — c'est Tom qui l'ouvre ;
- ouvrir l'Aura dans Safari sur le téléphone ; sur le Mac, Safari → Développement → l'iPhone → console ;
- **densité** : `_aura.etat()` rend `palier` (le palier tenu), `ms` (médiane par image), `cede`, `vise`
  (le palier visé) — l'ouvrir, la laisser tourner ~10 s, la fermer, la ROUVRIR : la vise ne s'applique
  qu'à l'ouverture suivante (Q181), c'est le palier de la seconde ouverture qui dit ce que l'appareil tient ;
- **capteur** : appuyer du pouce puis de l'index, lire `_aura.etat().emp.a` pendant l'appui —
  **0,40 = la valeur par défaut** (le capteur n'a rien dit), **entre 0,26 et 0,40 = le capteur a
  parlé**. On ne sait pas si Safari iOS remplit `PointerEvent.width/height` pour un doigt : c'est
  précisément ce que la mesure dira ; s'il ne le fait pas, il faudra lire `Touch.radiusX` ou décider
  de s'en passer.
Si la densité ne tient pas sur l'appareil : le levier est la résolution du tampon (`D`), lot à part.

**2 · Le chantier 58 — entier hors de l'Aura.** Le lot n'a neutralisé l'ombre de dalle que sur l'Aura et
sous elle. Partout ailleurs, `frame()` écrit toujours sur les douze écrans à chaque image : **27 % du fil
principal**. C'est une règle d'un autre lot, pas touchée. Inscrit en tête de CHANTIERS.md.

**3 · Le Cercle — pas commencé.** Rien de ce qu'il ajoute à l'Aura n'est dessiné ni codé : les deux
moitiés du trait (*ta moitié · la leur*), la réciprocité, *nuée par nuée*, les graphes d'évolution, et le
chiffre s'il revient. L'entrée d'auteur `#karmaCercle` est sortie avec l'ancienne Aura (Q176). **Rien du
Cercle n'apparaît en gratuit.** Les mots existent en partie (Q165) ; la planche, non.

---

## ⚠ TROIS FOIS LA MÊME DEMANDE — ON MESURE, ON N'AJUSTE PAS · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · sauvegarde du juge :
> `sauvegardes/redteam_air-avant-centre.py`

### CE QUE JE FAISAIS DE TRAVERS
Tom a demandé **trois fois** que la légende de l'Aura soit centrée entre les prénoms et
« CE QUE TU AS TENU ». Les trois fois je l'ai **rapprochée à l'œil** au lieu de relever les
trois boîtes une seule fois. Relevé du défaut, enfin fait :
```
bas des prenoms          490          ecart au-dessus de la legende      8 px
haut de la legende       498
bas de la legende        512
haut de « CE QUE... »    552          ecart en dessous de la legende    40 px
```
**8 contre 40.** La cote se calcule : `(552 − 490 − 14) / 2 = 24` de chaque côté, donc
`top = 514`.

### VÉRIFIÉ SUR L'IMAGE RENDUE, PAS SEULEMENT DANS LE DOM
```
DOM, deux themes                au-dessus 24,00   en dessous 24,00   difference 0,00
image rendue a 2x, sombre       prenoms (954,972)  legende (1032,1050)  titre (1110,1129)
                                au-dessus 59 px    en dessous 59 px     DIFFERENCE 0
image rendue a 2x, clair        idem, DIFFERENCE 0
```

### ⚑ LE CONTRÔLE, POUR QUE ÇA NE REVIENNE PAS
**« Un bloc annoncé centré entre deux voisins a des écarts égaux. »** Posé dans
`redteam_air.py`, tolérance **1 px** (la moitié d'un pixel d'appareil).
**Le bloc se DÉCLARE** — `data-centre-entre="selHaut|selBas"`. Un contrôle qui devinerait
les voisins se tromperait de nœud : c'est l'écran qui sait ce qu'il centre entre quoi. Et
il est **silencieux** tant qu'aucun nœud ne se déclare : il ne coûte rien aux autres écrans.

**⚠ ET IL EST PROUVÉ CONTRE UN VRAI DÉFAUT** — `scratchpad/preuve_centre.py`. Un contrôle
neuf qui ne trouve rien peut être juste **ou éteint**, et les deux se ressemblent dans un
rapport vert :
```
tel quel                             2 blocs declares   PRIS : 0   (24,00 / 24,00)
avec un defaut de 9 px pose expres   2 blocs declares   PRIS : 2   (33,00 / 15,00)
```
*L'écran Aura n'étant pas encore dans `app.html`, le contrôle y trouve zéro nœud déclaré et
se tait — il mordra à la seconde où le portage y posera l'attribut.*

```
redteam_air   OK — l'air est intact, et zero bloc centre en defaut
md5 app.html  61280542751d0d0df5bce546f9a091b1  inchange
```

---

## ⚠ LE BUDGET, CORRIGÉ — IL N'Y A PAS D'ÉTAT IMMOBILE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`)

### ⚠ CE QUE J'AVAIS CONCLU, ET QUI ÉTAIT FAUX
Mon premier relevé donnait **deux régimes** : 360 000 poils au repos (image gardée,
0,00 ms) et 110 000 en mouvement. **Ça supposait un état IMMOBILE — et il n'existe pas.**
La rotation lente est acquise depuis le début du chantier : **l'Orbite tourne toujours**.
Un chiffre mesuré sur un état qui n'existe pas ne vaut rien. **Conclusion retirée.**

### LE VRAI CHIFFRE — ROTATION LENTE PERMANENTE
`scratchpad/banc_lent.py`, au rythme du produit (un tour en ~50 s, **0,0021 rad par
image**), 80 images par palier, dans le vrai `#auraScreen` avec tout l'écran autour :
```
160 000 x1,00   mediane 21,30 ms   9e dec 29,30   80 images sur 80 au-dessus de 20 ms
130 000 x1,00   mediane 18,30 ms   9e dec 18,70    4 sur 80
110 000 x1,00   mediane 16,20 ms   9e dec 16,80    2 sur 80   <- LE PLAFOND
110 000 x1,70   mediane 21,30 ms   9e dec 22,00   80 sur 80
 90 000 x1,70   mediane 18,30 ms   9e dec 18,60    0 sur 80
 75 000 x1,90   mediane 17,30 ms   9e dec 17,60    0 sur 80, mais 0,23 % d'encre
```
**110 000, tout le temps.** Pas de double régime, pas de bitmap gardé.

### ⚑ ET GROSSIR LE BRIN NE RACHÈTE PAS LA DENSITÉ
La couverture vaut `N × surface du brin` : en théorie, moins de poils plus gros devraient
rendre la même matière. **Mesuré : le coût suit exactement la même loi.** À `110 000 × 1,70`
on retrouve la matière de 160 000 — et on en paie le prix au centième près (**21,30 ms les
deux fois**). Il n'y a pas de repas gratuit de ce côté-là.

### LA SPHÈRE À 110 000, REGARDÉE
`0,05 %` du disque encore à l'encre — négligeable. Au zoom 2 elle est **un peu plus grenue**
qu'à 160 000, les brins se lisent un peu plus individuellement ; **à la taille réelle
(342 px) la différence n'est pas perceptible**. La planche est passée à cette densité :
elle montre désormais ce que l'app peut réellement payer.

### ⚠ ET LA MISE EN GARDE TIENT
Mesure sur un **Mac**, dans la vraie page et la vraie géométrie, **pas sur un téléphone**.
**110 000 est un plafond haut, pas une garantie** — à reconfirmer sur appareil dès que
possible, et c'est le premier contrôle du portage.

### ⚑ CE QUE LA SPHÈRE SAIT DÉJÀ FAIRE — ET QUI DOIT SE RETROUVER DANS L'APP
Tout ceci est **acquis et validé**. Le portage n'a pas le droit d'en perdre une ligne :
```
· la rotation lente au repos — elle ne s'arrete jamais
· on la prend au doigt et on la tourne dans tous les sens
· l'elan qui continue, puis se rend a la rotation lente SANS SACCADE
· le toucher qui creuse, resiste, et revient
· la trace qui reste
· le comblement du creux quand on lance
· le geste qui relisse tout
· un toucher ouvre la personne, un glissement tourne
```

### LA SEPTIÈME SILHOUETTE — **AFFORDANCE, PAS DÉBORDEMENT**
Validé par Tom. `24 + 78 + 30 + 6×58 + 5×26 + 24 = 634 px` pour un écran de 390 : trois
personnes tiennent, la quatrième est coupée. Le §2.9 fixe six personnes et des écarts
constants ; **il n'a jamais prévu qu'elles tiennent toutes à l'écran**. Le disque coupé
**dit qu'il y en a d'autres** — la rangée se déclare glissante (`data-glisse`, Q128 §3).

### CE QUI SUIT
```
2 · le portage : les cinq fichiers dans app.html, sans toucher au moteur de la Toile.
    #auraScreen reecrit en entier, deux themes, BLOC NEUF EN FIN DE FICHIER.
3 · les vraies donnees : natures, etats, personnes, mondes de plantation.
4 · releve-aura.py, avec le controle de PRESENCE PEINTE comme les autres juges.
5 · batteries en serie, captures a 2x une par une, ETAT-DES-LIEUX a jour.
```

---

## ⚑ LE BUDGET D'IMAGE, MESURÉ DANS L'APP — AVANT DE PORTER QUOI QUE CE SOIT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) — la mesure **n'a pas touché
> le fichier** : `scratchpad/banc_aura.py` injecte le peintre à l'exécution
> (`addScriptTag`), ouvre le vrai `#auraScreen`, et fait tourner la sphère dans un
> `#device` de 390 × 844 **avec tout l'écran autour**. C'est ce « autour » qui manquait à
> la planche.

### LE RELEVÉ — 70 images par palier, la sphère en rotation
```
360 000 poils   mediane 42,20 ms   9e decile 43,40   70 images sur 70 au-dessus de 20 ms
240 000         mediane 30,00 ms   9e decile 30,80   70 sur 70
160 000         mediane 21,70 ms   9e decile 22,40   70 sur 70
110 000         mediane 16,60 ms   9e decile 17,10   ZERO sur 70      <- le plafond
 75 000         mediane 12,90 ms   9e decile 13,40   zero sur 70
```
**La planche tournait à 3,3 fois ce qu'un téléphone peut payer.** C'était bien la question
à poser avant de porter cinq fichiers.

### ET LA SPHÈRE ALLÉGÉE — REGARDÉE, PAS SUPPOSÉE
`scratchpad/banc_vue.py` rend la même sphère aux quatre densités
(`scratchpad/pav/vel/_densites.png`) :
```
360 000   le velours est une MATIERE continue
160 000   encore juste, un peu plus grenu
110 000   on commence a lire les BRINS au lieu de la matiere
 75 000   ca casse : l'encre du fond repasse entre les poils, la boule se troue
```
**Donc : au plafond des 60 images, la sphère est visiblement dégradée. À 75 000, elle est
perdue.** Si on s'en tenait à un seul chiffre, il faudrait choisir entre la fluidité et
l'objet.

### ⚑ MAIS LA VRAIE QUESTION N'ÉTAIT PAS « COMBIEN DE POILS » — C'ÉTAIT « QUAND »
**Au repos, l'Orbite ne bouge pas.** La repeindre soixante fois par seconde ne sert à rien.
Mesuré, dans les mêmes conditions :
```
une passe pleine densite (360 000)   41,2 ms   UNE FOIS
l'image gardee, reblittee             0,00 ms  par image (sous la resolution du timer)
```
**Le régime est donc double, et il n'y a rien à sacrifier :**
```
AU REPOS            360 000 poils, peint UNE FOIS, garde en bitmap    0 ms / image
EN MOUVEMENT        110 000 poils                                    16,6 ms / image
A LA FIN DU GESTE   une passe pleine densite                         41,2 ms, une fois
                    (une seule image sautee, a l'instant ou le doigt se leve)
```
L'objet qu'on regarde, qu'on partage et qu'on vend est **celui du repos** : il garde sa
pleine matière. Ce qui s'allège, c'est la demi-seconde où la boule tourne — et pendant
qu'elle tourne, personne ne compte les brins.

### ⚠ CE QUE CETTE MESURE NE DIT PAS
Elle tourne sur un **Mac, en Chromium headless**, dans la vraie page et la vraie géométrie
— mais **pas sur un téléphone**. Un appareil réel remplit moins vite : **110 000 est un
plafond haut, pas une garantie.** Le chiffre se reconfirme sur un appareil au moment du
portage, et c'est le premier contrôle du lot suivant.

### ⚑ LA SEPTIÈME SILHOUETTE : LA RANGÉE DÉFILE, IL N'Y EN A PAS UN DE TROP
La cote se calcule, elle ne se devine pas — §2.9, en unités du document :
```
24 + 78 + 30 + 6 x 58 + 5 x 26 + 24 = 634 px   pour un ecran de 390
trois personnes tiennent, la quatrieme est coupee au bord
```
Le §2.9 fixe **six** personnes et des écarts constants ; **il n'a jamais prévu qu'elles
tiennent toutes à l'écran**. Le disque coupé n'est pas un débordement, c'est **l'affordance
du défilement** — c'est lui qui dit qu'il y en a d'autres. La rangée se déclare glissante
(`data-glisse`, Q128 §3) pour que les juges de débordement l'exemptent **sous condition**.

### TRANCHÉ AU PASSAGE
**Le sol à zéro Promi reste bleu** — le bleu est la nature de base, et à zéro rien ne
domine. Choix confirmé par Tom.

### CE QUI SUIT, DANS CET ORDRE
```
2 · le portage : les cinq fichiers dans app.html, #auraScreen reecrit en entier,
    deux themes, BLOC NEUF EN FIN DE FICHIER, jamais une regle existante,
    et rien du code de la Toile (§9)
3 · les vraies donnees : natures, etats, personnes, mondes de plantation.
    C'est la que tout peut mentir — la planche a un jeu de demonstration.
4 · releve-aura.py, avec le controle de presence peinte comme les autres juges
5 · batteries en serie, captures a 2x une par une, ETAT-DES-LIEUX a jour
```

---

## ⚑ L'ORBITE — CLÔTURE DU CHANTIER · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · point de reprise :
> `sauvegardes/orbite-velours/` (les cinq `_v_*.js`, `_m_base.js`, `PLANCHE-VELOURS.html`)
> · `sauvegardes/PROMI-SPECIFICATIONS-avant-piste-neutre.md`

### 1 · ⚠ J'AVAIS RETIRÉ SANS REMPLACER
En enlevant la couleur de nature des visages — elle était **arbitraire**, je l'avais écrite
à la main sans règle derrière — il ne restait que **six silhouettes grises identiques**. En
thème sombre elles disparaissaient, et on ne distinguait plus personne : c'est pourtant à
ça que sert cette rangée. **Retirer un défaut n'est pas une correction tant que rien ne
prend sa place.**

**La réponse existait déjà dans l'app** : `avatarHTML` / `_blobBg`. Une **vraie photo** si
la personne en a une, sinon **l'image abstraite générée**, déterministe à partir du nom,
avec sa palette `_BPAL` (six teintes) et sa **texture de bruit en soft-light**. Reprise à
l'identique, hachage FNV compris : deux personnes n'ont jamais la même image, et la même
personne a toujours la sienne. **C'est ça qui identifie quelqu'un — pas une couleur de
nature.**

### 2 · ⚑ LE §2.9 EST CORRIGÉ, PAS CONTOURNÉ
Le document disait *« piste de l'anneau : teinte de la nature »*. **Une personne n'a pas de
nature** : la règle était inapplicable à la moitié des Noyaux qu'elle décrit, et c'est ce
vide qui avait produit une couleur arbitraire. **La piste est neutre** — `#2A2C34` en
sombre, `#DED7C6` en clair — **et seuls les arcs portent la couleur**, celle de l'ÉTAT.
Ton Noyau à toi suit la même règle : c'est le même composant.
*L'écart n'est pas laissé en suspens : `PROMI-SPECIFICATIONS.md §2.9` est réécrit, avec la
raison et la version d'origine en sauvegarde.*

### 3 · ⚠ LE SOL N'ÉTAIT PAS CALCULÉ DU TOUT
Il sortait **mauve** sur les deux captures. **Pas parce que la Nuée dominait — parce
qu'aucun calcul n'était branché** : le sol prenait simplement la couleur de la palette du
Studio. La rangée des trois natures démontrait la règle ; l'écran ne l'appliquait pas.
**Vérifié dans le moteur** : `Toile.sync()` ne plante que des **Promi** ; une Nuée ne naît
que de `addNuee()`, que la planche n'appelle jamais. **La nature la plus présente est donc
Promi, et le sol doit être BLEU.** Il l'est.
*À zéro Promi aucune nature ne domine : le sol prend le bleu, la nature de base. Choix
noté, pas mesuré.*

### 4 · DEUX RÉGLAGES D'AIR
La légende **remonte de 14 px** vers les anneaux dont elle nomme les arcs ; le titre
« CE QUE TU AS TENU » **gagne 7 px** au-dessus de ses dalles.

### CONTRÔLES — LOT COMPLET
```
node --check sur le JS de app.html            OK
redteam_ecrans   150/150      redteam         15/15
redteam2          10/10       redteam3        18/18
redteam_demande   19/19       redteam_toile   17/17
redteam_geste     13/13       redteam_verbe    6/6
releve-design                 AUCUN ECART, le design est intact
trente-cinq cadres compares   deux couples identiques, et les deux sont des TEMOINS
                              voulus (c-cinq/pg-cinq, pg-trente/q-repos)
circularite  g-vide           rayon 275,9  ecart-type 1,24  soit 0,45 %
             v-30             rayon 565,3  ecart-type 3,17  soit 0,56 %
md5 app.html                  61280542751d0d0df5bce546f9a091b1  INCHANGE
```

### ⚑ CE QUE L'ORBITE EST DEVENUE — RÉCAPITULATIF DU CHANTIER
```
LA SPHERE         le velours, ses dalles dans le monde de leur plantation,
                  et la memoire de la main. RIEN D'AUTRE.
                  Elle n'encode ni les gens ni les etats : une matiere ne sait
                  pas dire un nom, et vingt series ont echoue a le lui demander.
                  Aucun nom dessus => l'image se partage.
LE SOL            la NATURE la plus presente (bleu / framboise / mauve).
                  Menthe et terracotta ne servent qu'aux etats, nulle part ailleurs.
LA CROISSANCE     la dalle plantee se pose du cote qu'on regarde, puis l'Orbite
                  fait UN TOUR pour l'amener au centre. Les anciennes ne bougent
                  pas d'un pouce.
LA MAIN           des caresses au diametre du doigt (0,27 rad), qui couchent le
                  poil dans leur sens : 19,66 % des pixels. Visible sans toucher.
LES SIX           SOUS la sphere, en Noyaux du §2.9 : avatar du produit, piste
                  neutre, trois arcs d'etat, prenom sur la meme ligne de base.
LE MOT            il qualifie L'OBJET dans le registre du rejeu, jamais la
                  personne. Ni note, ni verdict, ni valeur qui descend.
L'ANNEAU          un seul, celui de ton Noyau. Celui de la sphere faisait doublon.
```

### ⚠ CE QUI N'EST PAS FAIT — ET C'EST LE PLUS IMPORTANT DE CE CHAPITRE
**LE PORTAGE DANS `app.html` N'EST PAS FAIT.** Le md5 est inchangé, et ce n'est pas un
oubli : c'est un lot à part entière, pas la fin de celui-ci. Ce qu'il demande —
```
1 · faire entrer cinq fichiers (_v_moteur, _v_iles, _v_semis, _v_peint, _m_base)
    dans app.html, sans toucher au code de la Toile (§9)
2 · reecrire #auraScreen : la sphere, la rangee des Noyaux, la legende, le mot,
    la rangee des dalles tenues, le bouton — deux themes
3 · brancher les VRAIES donnees : natures, etats, personnes, mondes de plantation
4 · le budget d'image sur un vrai telephone (la planche tourne a 180 000 poils
    pour 340 px, ce n'est PAS une densite d'app)
5 · un juge dedie, `releve-aura.py`, avant de figer quoi que ce soit
```
- **Le Cercle** : graphes d'évolution, commentaires sur la hausse, réciprocité, et le
  chiffre s'il revient. **Rien n'en apparaît en gratuit** — c'est de la mesure fine.
- **Le filtre « pas de Nuée dans la rangée »** est une règle d'app : une Nuée est un
  contenant, ce sont les Promi qu'elle porte qui sont tenus.

---

## ⚑ DEUX SYSTÈMES DE COULEUR, ET ILS SE TÉLESCOPAIENT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

### 1 · LE SOL DISAIT « À QUI » AVEC DES COULEURS D'ÉTAT
Menthe, terracotta et mauve pour dire *soi / quelqu'un / un groupe* : sur **le même écran**,
le menthe disait « tenu » dans un anneau et « à toi » sur la sphère. **Une couleur signal
qui dit deux choses** — ce que le §3 interdit.
**Le sol prend les couleurs de NATURE** : bleu `#3A54FF` surtout des Promi, framboise
`#FA2258` surtout des Chiche, mauve `#8A5CF0` surtout en Nuée. **Il dit ce qu'on promet,
pas à qui.** Menthe et terracotta ne servent plus qu'aux états, nulle part ailleurs.

### 2 · ⚠ LA COULEUR DES VISAGES ÉTAIT ARBITRAIRE — RÉPONSE FRANCHE
Je l'avais écrite **à la main** dans le tableau `GENS`, sans règle derrière : ce n'était la
Nuée de personne. **Une personne n'est ni un Promi ni un Chiche : elle n'a pas de nature,
donc pas de couleur de nature.** Le visage passe au **neutre** (l'encre ou la crème du
thème) ; il ne reste de coloré que ce qui porte du sens, les arcs d'état.
**⚠ Et le même défaut touche LA PISTE de l'anneau** : le §2.9 la veut « teinte de la
nature », ce qui n'existe pas pour une personne. Elle passe au neutre aussi — **point à
trancher**.

### 3 · L'ANNEAU DE LA SPHÈRE SORT, LA LÉGENDE DESCEND
Il faisait **doublon** avec le Noyau « toi » juste en dessous : deux anneaux à trois arcs
disant la même chose. Le mien porte mon visage et vit dans la rangée des six ; celui de la
sphère cerclait un objet qui n'est pas moi.
**La légende descend sous la rangée des six** — c'est là qu'elle nomme quelque chose de
précis : **les arcs des Noyaux**, qui sont juste au-dessus d'elle. Elle a son air au-dessus
(22 px) et en dessous (44 px).
**Et les Noyaux portent maintenant TROIS arcs**, pas un seul : une légende à trois entrées
ne pouvait pas nommer un unique arc menthe.

### 4 · ⚠ LE LEXIQUE DU TITRE ÉTAIT FAUX, ET JE NE L'AVAIS PAS VU
« Tes paroles tenues » **ne couvre ni les Chiche ni les Nuées**, alors qu'ils sont là.
**« Ce que tu as tenu »** englobe les trois natures sans en nommer aucune.

**Ce que contient vraiment la rangée, vérifié dans le moteur :** `Toile.sync()` ne plante
que des **Promi** — une Nuée ne naît que de `addNuee()`, que la planche n'appelle jamais.
Les six ids de la rangée (3, 7, 11, 14, 17, 19) résolvent tous en dalles réelles via
`dalleAbs` (qui exclut déjà les cellules vides). **Il n'y a donc aucune dalle de Nuée dans
la rangée de la planche** — mais **la règle reste à écrire côté app** : une Nuée est un
contenant, ce sont les Promi qu'elle porte qui sont tenus.

### 5 · ⚑ LE MONDE DE LA PLANTATION, ENFIN CÂBLÉ
Un Promi porte `{m,p,h}`, figé par sa fabrique au moment où il est planté (lot du
4 septembre). **`dalleTrame` prend ce 4ᵉ argument depuis ce jour-là — il n'avait jamais été
câblé**, et les six dalles sortaient toutes dans le monde courant. C'est une règle du
produit, pas un détail : la diversité des dalles est ce qui rend la Toile vivante. Les
trois dalles visibles sont maintenant en **touffe, sillons, braille**.

### 6 · ⚑ L'ORBITE TOURNE UNE FOIS QUAND UNE PAROLE EST TENUE
Le levier était le **geste**, pas le rendu. La vue qui centre une direction se **calcule** :
```
lac = atan2(-c0, c2)        tan = atan2(c1, hypot(c0, c2))
```
Vérifié en repassant la direction par la transformation directe : **elle rend (0, 0, 1)
exactement**, et les six îles ont toutes `z > 0` — donc **toutes sur la face visible, rien
n'a reculé**.
```
5 -> 6 (la dalle se pose du bon cote)      4,75 % des pixels
6 -> apres le tour                        52,21 %
```

### 7 · LES PHRASES — LE REGISTRE EST CELUI DU REJEU
Mes cinq phrases décrivaient l'objet : **c'était un inventaire, pas une voix**. Le registre
est le clin d'œil complice — *« Tu l'avais dit »*, *« Tiens donc »*. Les cinq de Tom sont en
place, et l'état vide n'en garde que deux :
```
La premiere parole laissera sa trace ici.
   Tout commence par une parole donnee.
```

### CONTRÔLES
```
trente-cinq cadres compares deux a deux   deux couples identiques, et les deux sont VOULUS
                                          (c-cinq/pg-cinq et pg-trente/q-repos : memes
                                          etats, ce sont les temoins de deux rangees)
la derniere dalle, apres le tour          (0, 0, 1) a 1e-6 pres
les six iles apres le tour                z = 0,92 · 0,71 · 0,71 · 0,88 · 0,90 · 1,00
md5 app.html                              61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI RESTE
- **La piste des Noyaux** : neutre par défaut de règle, à trancher.
- **Le Cercle n'est pas dessiné** — graphes, commentaires sur la hausse, réciprocité,
  et le chiffre s'il revient. **Rien n'en apparaît en gratuit.**
- **Le filtre « pas de Nuée dans la rangée »** est une règle d'app, pas de planche.

---

## ⚑ L'AURA SANS CHIFFRE — LE MOT QUALIFIE L'OBJET · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

### 1 · CE QUI SORT, ET POURQUOI
**Le chiffre d'harmonie et le mot qui qualifie la personne.** Les deux font *score*, même
sans le mot : l'un est une note, l'autre un verdict sur quelqu'un. Et **le chiffre baisse
quand on ne tient pas** — une valeur qui décroît par inaction.

### 2 · CE QUI RESTE, ET IL A CHANGÉ DE SUJET
**Un mot revient : il qualifie L'OBJET, jamais la personne.** Pas *« ta parole est
solide »* — mais ce que la sphère est devenue. Cinq phrases proposées, aucune ne compare,
ne mesure ni ne juge :
```
Le velours s'est epaissi.
Plusieurs mondes se cotoient ici.
La main a laisse son passage.
Les premieres dalles sont toujours la.
Les dalles se touchent, maintenant.
```

### 3 · L'ANNEAU ET SA LÉGENDE
**L'anneau est la seule mesure de l'écran, et elle ne se lit pas en chiffres** : trois arcs
autour de la sphère, avec 2,4 % de vide entre eux. La légende — *tenues · en cours · à
tenir* — **nomme** les trois arcs, elle ne quantifie rien. Air au-dessus (34 px), air en
dessous (34 px).
**⚠ Et l'anneau ne doit pas toucher la sphère.** À `R = 0,438` le velours arrivait au ras
des arcs : ça se lisait comme un **cerclage de l'objet**, et le moindre poil qui déborde
salissait l'arc. `R = 0,392` — l'air entre les deux fait que l'anneau se lit comme une
mesure **posée autour**.

### 4 · « LA MOISSON » SORT
Mot d'agriculture, pas du produit : on plante et on tient parole, on ne récolte pas.
Trois propositions, la première est en place : **« Tes paroles tenues »** · *« Ce que tu as
tenu »* · *« Les dalles tenues »*. Le titre dit **ce que c'est**, jamais combien.

### 5 · « PARTAGER MON NOYAU »
La porte manquait sur l'Aura alors que l'aide l'annonce en gratuit et que le mode existe
côté partage. Bouton en bas, à la **grammaire des contours** : 298 × 52, trait 2, rayon 26
(le 342 × 62 du document, ramené au gabarit).

### 6 · L'ÉTAT VIDE EXISTE
```
Le velours est neuf.
La premiere parole y laissera sa dalle.
   Tout part d'une parole donnee — a toi, a quelqu'un, a plusieurs.
```
Deux autres proposées : *« Ici, tout part d'une parole donnée. »* · *« Rien n'est encore
planté. La matière est prête. »* Aucune injonction, aucun point d'exclamation.
**Et la sphère y est déjà belle** : c'est le test décisif, un objet qui n'est beau qu'à
trente est refusé. À zéro, **pas d'anneau** — il n'y a rien à mesurer.

### 7 · LES DEUX CORRECTIONS DE LA CAPTURE
- **Les prénoms sont sur la même ligne de base.** Chaque Noyau est une colonne de hauteur
  fixe (94 px) alignée par le bas, et le libellé a une hauteur de ligne fixe : « toi » ne
  peut plus décrocher de Rachel.
- **Les diamètres sont vérifiés au §2.9** : 78 et 58 dans le document, soit **68 et 51** au
  gabarit (× 0,872). Rapport 1,333 contre 1,345 — l'écart est l'arrondi au pixel, pas un
  accident.

### ⚑ 8 · LA MAIN SE VOIT ENFIN AU REPOS
```
sans traces -> avec traces :  19,66 % des pixels bougent de plus de 3/255
```
**⚠ Une caresse est LARGE, et les arcs ne l'étaient pas.** `m_gestes` donne des arcs de
0,055 à 0,13 rad — **trois à sept degrés, c'est un ongle, pas une pulpe**. La pulpe d'un
pouce couvre 0,27 rad (mesure du lot de l'empreinte). À cette largeur-là une caresse ne
pouvait pas se voir, et c'était pourtant la seule chose que personne d'autre n'a. Les arcs
passent au diamètre du doigt (`0,115 + w × 1,35`) et ce qu'ils ont poli monte.

### CONTRÔLES
```
trente-sept cadres compares deux a deux   zero doublon
5 -> 6 Promi                              4,75 % des pixels
sans traces -> avec traces                19,66 %
circularite v-30                          rayon 565,3  ecart-type 3,17  soit 0,56 %
md5 app.html                              61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI RESTE
- **Le Cercle n'est pas dessiné** : graphes d'évolution, commentaires sur la hausse,
  réciprocité « envers les autres », et le chiffre si on le garde un jour. **Rien de tout
  ça n'apparaît en gratuit** — c'est de la mesure fine, pas de l'information.
- **Les dalles de « Tes paroles tenues » sont toutes dans le monde courant.** Un Promi doit
  garder le monde de SA plantation (4ᵉ argument de `dalleTrame`, écrit, jamais câblé).
- **5 → 6 vaut 4,75 %** : la nouvelle dalle se voit, mais c'est un ajout discret, pas un
  événement. Si Tom veut que ça se voie franchement, le levier est le geste de plantation,
  pas le rendu.

---

## ⚑ UNE MATIÈRE NE SAIT PAS DIRE UN NOM · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

### LA DÉCISION, ET C'EST ELLE QUI COMPTE
On a demandé à la matière d'encoder **qui est qui** : par la position, par la saturation,
par la densité, puis par un **épi** — un tourbillon de poil par personne. Verdict de Tom :
*« ça fait des signes BMW, ni beau ni compréhensible »*. Et la vraie raison n'est pas
l'exécution :

> **UNE MATIÈRE NE SAIT PAS DIRE UN NOM.** Un épi ne peut pas être « Rachel ». Une
> saturation non plus, une densité non plus. **C'est structurel** — et c'est pour ça que
> vingt séries ont échoué au même endroit.

**On arrête de le lui demander.** La sphère ne porte plus que trois choses : **le velours,
ses dalles dans le monde de leur plantation, et la mémoire de la main.** Elle dit *« voilà
ce que j'ai tenu, et j'y ai passé du temps »*.
**Les six et le Noyau vivent sous elle**, en anneaux du §2.9 — piste à la teinte de la
nature, arc menthe, visage, prénom. C'est là qu'on lit la relation, sans deviner.
**Et l'image devient partageable** : aucun nom dessus, indéchiffrable pour un inconnu.

### CE QUE ÇA CHANGE DANS LE CODE
- `champPoil` n'a plus que deux termes : **le peigne** (une direction unique, ses deux zéros
  au limbe) et **les caresses**. Plus d'épis, plus de couronne. Comme tout le reste est
  uniforme, **la main est la seule structure de la surface** — donc la plus visible, ce qui
  est exactement le but.
- Le lustre de la main double le contraste du brin (on **suit** le sens du geste) et monte
  le ton (`_po × 2,6`) et la chroma.
- `disques` et `noyau` restent dans le fichier, **non appelés**.

### ⚑ UN PROMI DE PLUS SE VOIT — ET CE N'ÉTAIT PAS UN PROBLÈME DE RENDU
```
avant ce lot        5 -> 6 Promi :  0,09 % des pixels bougent de plus de 3/255
apres               5 -> 6 Promi :  4,80 %
```
**Aucune variable globale continue ne peut rendre un +1 visible** — un trente-quatrième de
quoi que ce soit est invisible, c'est de l'arithmétique. Ce qui rend un +1 visible, c'est
**la dalle elle-même**, et il y avait une chance sur deux qu'elle tombe **sur la face
cachée** : la grappe pousse par accrétion vers l'extérieur.

**⚠ Et on ne fait pas tourner la boule pour autant.** Essayé, mesuré, regardé : en tournant
l'objet pour présenter la dernière dalle, les cinq précédentes partaient sur le dos — **à
six Promi on en voyait MOINS qu'à cinq** (17,22 % de pixels changés, et une régression de
sens). *« Rien ne recule jamais »* interdit ça.
**La loi de croissance ne bouge pas** (l'accrétion fait la forme) : parmi les positions
valides, on garde **celle qui regarde le plus vers nous**. Les anciennes ne bougent pas d'un
pouce, la nouvelle est devant.

### L'ÉCRAN AURA, EN ENTIER, DEUX THÈMES
`ecranAura()` dans la planche : le titre, la sphère (312 px), **la rangée des Noyaux**
(§2.9 — tien 78→68, personnes 58→51, visages du §2.10, arc menthe, prénom dessous, la
rangée déborde à droite : elle défile), puis **la moisson** en **vraies dalles du moteur**.

**⚠ Deux pièges payés sur la moisson :**
- **`dalleTrame` lit LE PARENT du canvas** : appelée avant que la grille soit disposée, elle
  rend du vide **en silence**. On repasse à 0, 120 et 420 ms (§4, règle 5).
- **Un id hors de la Toile synchronisée rend un canevas vide, en silence.** La planche fait
  `Toile.sync([1..20])` : les ids 37, 58, 73, 91, 104 ne rendaient rien — **cinq dalles sur
  six manquaient**, et rien ne le signalait.

### CONTRÔLES
```
trente-trois cadres compares      deux couples identiques, et les deux sont VOULUS :
                                  c-cinq / pg-cinq  (le meme etat a cinq Promi)
                                  pg-trente / q-repos (le temoin de la rangee du doigt)
circularite  g-vide               rayon 275,9  ecart-type 1,24  soit 0,45 %
             n-marque             rayon 276,8  ecart-type 1,42  soit 0,51 %
md5 app.html                      61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI N'EST PAS FAIT, ET QUI SE VOIT SUR LA PLANCHE
- **Les dalles de la moisson sont toutes dans le monde courant.** Un Promi doit garder le
  monde de SA plantation (4ᵉ argument de `dalleTrame`, déjà écrit, jamais câblé).
- **La rangée des Noyaux déborde** — c'est le §2.9 (elle défile), mais le geste n'est pas
  démontré.
- **Le prénom au toucher sur la sphère n'a plus lieu d'être** : il n'y a plus rien à
  effleurer. `o.effleure` devient mort.
- **La moisson n'est qu'une grille de six** ; ce qu'elle devient à trente n'est pas dessiné.

---

## ⚑ LES ÉPIS — LE NOYAU ET LES SIX SONT DEVENUS DE LA MATIÈRE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

**Trois choses écrivent maintenant le sens du poil, et aucune n'ajoute quoi que ce soit à la
matière : elles SONT la matière.** Tout passe par une seule fonction, `champPoil`.

### 1 · LA COURONNE — le Noyau
Tout pelage a un point d'où il part. Le sien est **au centre de la face qu'on regarde** :
c'est « toi », et ça ne coûte pas un pixel d'interface. Le champ est le gradient de l'angle
à ce point ; ses deux seuls zéros sont **la couronne** (le dessin qu'on veut) et son
antipode, sur le dos, qu'on ne peint pas.
*Avant :* un disque crème de 8 % du rayon, qui se lisait comme **un trou clair percé dans le
velours**.

### 2 · LES ÉPIS — les six
Une personne à qui on a donné sa parole est **un épi** : le poil tourne autour d'elle en
spirale. **Le rayon et le serrage montent avec le cumul** — plus on a tenu parole avec
quelqu'un, plus l'épi est large et serré. `k` ne descend jamais : **un épi ne se défait pas**.
*Avant :* six pastilles sombres à anneau, à intervalle égal, qui **n'encodaient plus rien**
depuis qu'on avait libéré la géométrie. Six trous percés dans le velours, et le §3 les
condamnait.

**⚠ Deux réglages qui décident de tout, et les deux ont été payés :**
- **UN ÉPI EST PETIT.** À `0,15 + 0,33 k` il couvrait **vingt-sept degrés** : sur le disque
  visible, une **cuvette** — et comme toutes les fibres y convergent, elles s'éteignent
  ensemble. Six grands creux sombres, **une balle de golf**. Ramené à trois-huit degrés.
- **UN ÉPI TOURNE PLUS QU'IL NE CONVERGE.** À dominante radiale, tous les brins pointent au
  même endroit et s'éteignent ensemble : petit **cratère** sombre. À dominante tangentielle
  (`0,42 · radial + 0,91 · tour`), la moitié du tour regarde la lumière et l'autre s'en
  détourne : **un croissant clair et un croissant sombre**. C'est à ça qu'on reconnaît un épi
  sur un vrai pelage, et ça ne salit rien.

### 3 · LES CARESSES — et elles reviennent au repos
**⚠ Elles avaient été retirées le matin même, et à raison** : c'étaient des **gravures**
posées au hasard sur un objet neuf. Ce n'est plus la même chose : une caresse ne creuse plus
rien, elle **couche le poil dans son sens**. On lit le parallélisme de quelques milliers de
brins — et **c'est ça, un lustre**. L'objet au repos porte donc ses traces : on voit, sans
toucher, que quelqu'un s'en est occupé. Une Orbite neuve n'en a aucune.

**⚠ Et sans le terme de lustre, une bande peignée sortait SOMBRE** — une salissure, pas une
caresse : les brins alignés s'éteignent tous ensemble. Le poli monte donc **le ton (+1,7
marche) et la chroma** (l'étage saturé de la table). `_PO` ne porte plus que ça : **la
mémoire de la main**. Les six en sont sortis — ils écrivent le SENS, pas le ton, et
mélanger la main et les gens dans une même variable était une faute.

### 4 · LE PRÉNOM NE S'ÉCRIT QU'AU TOUCHER
Rien n'est lisible sur l'Orbite pour un inconnu. `o.effleure` pose le prénom au-dessus de
l'épi effleuré, puis il disparaît. Aucun texte au repos.

### ⚠ LA CROISSANCE — CE QUI EST TENU, ET CE QUI NE L'EST PAS
`pousse` (0 → 1, jamais en arrière) relève le plancher de longueur du poil et monte le ton
d'une marche et demie. **Mesuré, à la vraie question :**

```
pousse  0 -> 34 Promi    59,05 % des pixels bougent de plus de 3/255
pousse  5 -> 34 Promi    57,64 %
pousse  5 ->  6 Promi     2,74 %      (0,09 % avant ce lot)
```

**Sur la longue course, la croissance se voit — franchement.** Sur **un** Promi de plus,
elle reste au ras du seuil, et je ne prétendrai pas l'inverse : **aucune variable globale
continue ne peut rendre un +1 visible** — un trente-quatrième de quoi que ce soit est
invisible, c'est de l'arithmétique.

**Ce qui rendra le +1 visible, c'est LA DALLE ELLE-MÊME** — et aujourd'hui **une chance sur
deux qu'elle tombe sur la face cachée**. La réponse est une règle de PLACEMENT, pas de
rendu : *la dalle qu'on vient de planter se pose face à toi.* **Ce n'est pas fait** — c'est
le lot suivant, et c'est le vrai.


### ⚠ ET ON NE LES VOYAIT PAS — CORRIGÉ LE MÊME JOUR
Tom : *« pas compris ni vu le principe des épis »*. Il avait raison, et deux choses le
rendaient illisible :

- **ILS ÉTAIENT TROP PETITS.** À trois-huit degrés, un épi fait **quatre à dix brins de
  large** : à cette taille on ne lit pas une spirale, on lit une petite salissure. Ils
  passent à **six-dix-huit degrés** (`0,105 + 0,205 k`), soit une trentaine de brins. Le
  creux sombre ne revient pas pour autant : ce qui l'évitait, ce n'était pas la petite
  taille, c'était **la dominante tangentielle**.
- **LE BRIN SE FONDAIT DANS SA PEAU.** Un épi ne se lit que si on **suit les brins qui
  tournent**. Au contraste de la surface plate, ils disparaissaient et il ne restait qu'une
  ombre vague. **L'amplitude du lustre double à l'intérieur de l'épi** (`11,5 → 26,5`) et le
  poil y gagne un cran de longueur — un poil que le peigne redresse est plus long à l'écran.
  Le brin se détache, et c'est **le tour** qu'on lit, pas une tache.

Le poids d'épi est publié par point (`_EW`, porté jusqu'au versement comme `_PO`), donc il
ne coûte pas une seconde boucle sur les six.

**Et une rangée de la planche montre le principe** : trois gros plans, un seul épi, à trois
cumuls — `ep-faible`, `ep-moyen`, `ep-fort`. Sur la page entière un épi fait quelques
dizaines de pixels ; c'est de près qu'on comprend.

### CONTRÔLES
```
vingt-huit cadres compares deux a deux   un seul couple identique, et il est VOULU
                                         (pg-trente / q-repos : meme etat, le temoin
                                         de la rangee du doigt)
circularite  g-vide                      rayon 278,4  ecart-type 0,97  soit 0,35 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **La dalle neuve face à toi** — le vrai correctif du critère 4.
- **Le terracotta contre sa propre grammaire** (§3 : il veut dire « à tenir »).
- **Une dalle orange sur un sol terracotta disparaît** (seuil 42 non tenu).
- **La composition de la page** : la boule occupe le tiers haut.
- `disques` et `noyau` restent dans le fichier, **non appelés** (`o.pastilles` les rallume),
  le temps que Tom confirme qu'on ne revient pas en arrière.

---

## ⚑ LA COULEUR DIT À QUI TU AS TENU PAROLE — JAMAIS CE QUI MANQUE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

### ⚠ LA VARIABLE N'EST PAS L'ÉTAT, ET C'EST TOM QUI A POSÉ LA BORNE
Piloter le sol par l'état majoritaire donnait une sphère terracotta qui dit
**« la plupart de tes paroles sont en retard »** : un état de manquement rendu visible, et
— pire — **une couleur qui change toute seule quand le temps passe**. C'est une valeur qui
décroît par inaction. **Écarté.**

**La variable prise : À QUI LA PAROLE TENUE S'ADRESSAIT.**
L'Orbite ne contient que des paroles **tenues**. On les répartit selon la personne
concernée, et le sol prend la couleur du groupe le plus fourni :

```
menthe      #2BE88C   celles que tu as tenues POUR TOI
terracotta  #F07A2E   celles que tu as tenues POUR QUELQU'UN
mauve       #8A5CF0   celles que tu as tenues AVEC UN GROUPE (une Nuee)
```

Les trois comptes **ne font que monter**. Aucun ne peut baisser, aucun ne bouge quand on ne
fait rien, aucun ne nomme un manquement : les trois disent une parole tenue, seulement pas
à la même personne. La teinte change **en faisant plus**, jamais en laissant filer.

**⚠ ET LE PRIX EST RÉEL, IL FAUT LE DIRE.** Au §3 de `CLAUDE.md`, **terracotta veut dire
« à tenir »**. Lui faire dire ici « tenue pour quelqu'un », c'est **une couleur signal qui
dit deux choses** — exactement ce que la grammaire du produit interdit. Le jeu sans
ambiguïté serait **bleu #3A54FF · framboise #FA2258 · mauve #8A5CF0** (les trois natures,
trois signaux existants, zéro collision) — mais il perd le terracotta et la menthe.
**Arbitrage à Tom, non tranché.**

**Le sol n'est pas une dalle** : la règle du §4 (« la dalle porte le monde ») tient entière
— chaque dalle garde le monde et la couleur de sa plantation.

### ⚑ LA DÉLICATESSE DU POIL VENAIT DE SON ÉPAISSEUR, ET ELLE ÉTAIT TROP FINE
À **0,50 px** d'épaisseur et à pleine opacité, une mèche tombe entre deux pixels : elle sort
**en marches**, et la matière se lit en **grains durs**. La finesse d'un velours ne vient pas
de brins plus maigres — elle vient de brins **qui se fondent**. On élargit d'un tiers de
pixel (`0,82`) et on baisse l'opacité du tampon (`1,00 → 0,78`) : même densité, même sens,
un **fondu** au lieu d'un crénelage. Et la mèche s'allonge d'un tiers (`TAI0` de 1,9-5,5 à
2,5-7,3) : sous quatre pixels de long, l'œil ne lit plus un **brin**, il lit un **grain**.

### ⚠ ET DEUX TACHES RESTAIENT, DE MÊME FAMILLE
- **Les six sortaient en disques saturés.** Le seuil de bascule vers l'étage ressaturé
  était **franc** : un seuil franc sur une calotte donne un disque à bord net — la version
  chroma de « des pois ronds qui ne correspondent à rien ». **Le seuil se tire au poil** :
  la bascule devient un fondu granuleux, à l'échelle de la fibre. Et la ressaturation
  descend de `× 1,34` à `× 1,11`.
- **Le lustre éteignait une région entière.** Là où le peigne pointe vers la lumière, tous
  les poils du coin s'éteignent **en même temps** : ça ne fait pas du grain, ça fait une
  **salissure**, au même endroit sur les trois teintes. Le lustre est donc **borné par le
  bas** : il éclaire librement, il n'assombrit que d'une marche.

### L'ÉCLAIRAGE MONTE D'UN CRAN
Le pied de la rampe passe de **2,2 à 5,4** et la course se resserre (20,0 → 16,4) pour ne
pas écrêter le clair. Mesuré sur la terracotta, diagonale haut-gauche → bas-droit :
**170 · 155 · 119 · 116** de luminance.

### CONTRÔLES
```
vingt-huit cadres compares deux a deux   un seul couple identique, et il est VOULU :
                                         pg-trente et q-repos sont le meme etat (30 Promi,
                                         sans empreinte) — q-repos est le temoin de la
                                         rangee du doigt.
circularite  e-terra-0                   rayon 153,3  ecart-type 0,81  soit 0,53 %
             e-vert-0                    rayon 153,3  ecart-type 0,81  soit 0,53 %
             g-vide                      rayon 276,0  ecart-type 0,99  soit 0,36 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **Le terracotta contre sa propre grammaire** (ci-dessus) — décision produit.
- **Une dalle orange sur un sol terracotta disparaît** : le seuil 42 du §3 n'est pas tenu
  entre le sol et les dalles de même famille. Visible sur `e-terra-30`.
- **L'état à zéro n'a pas de majorité** : quelle teinte porte une Orbite neuve ?
- **La composition de la page** : la boule occupe le tiers haut.

---

## ⚑ LE GRAVIER N'ÉTAIT PAS DU GRAIN — C'ÉTAIT LE FOND QUI PASSAIT · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

Deux reproches : **« ton dégradé, on n'y croit pas »** et **« ça fait des croisillons »**.
Ils avaient la même cause, et ce n'était ni la lumière ni le relief.

### 1 · LE POIL SE COMPOSAIT SUR DU NOIR
Le bord d'un tampon de poil est **doux** : son alpha tombe à 60 ou 100 sur le pourtour.
Comme le versement ne garde que **le plus opaque** et rien d'autre, une foule de pixels
restaient à mi-alpha — et se composaient avec **l'encre du fond**. Mesure : **6,9 % du
disque sous 40 de luminance**, en tirets noirs, partout.
Ce bruit est **à haute fréquence et uniformément réparti** : il écrase mécaniquement une
variation lente. **Tant qu'il était là, aucun dégradé ne pouvait se voir** — on aurait pu
le monter à n'importe quelle amplitude.

**⚠ Et on ne corrige pas ça en opacifiant la fourrure.** Essai fait, regardé, revenu :
toute la forme d'un poil vit dans son **alpha** — sa couleur n'est qu'un aplat de marche.
Forcer alpha à 255 remplace le pelage par des aplats ; la boule est sortie **en bandes
lisses, sans un poil**.

**La parade — une peau.** Un pelage a une peau : entre deux poils on ne voit pas le vide,
on voit la bête. On la fabrique **à partir du dépôt lui-même** — le tampon réduit par
blocs, chaque bloc prenant la moyenne pondérée de ce qui s'y trouve, puis redilaté en
lissage bilinéaire. C'est donc, par construction, **la couleur du lieu, dalles comprises**,
sans un calcul de plus.

**⚠ Trois pièges, tous payés :**
- **Le bloc doit être GRAND devant le poil.** À 7 px — la taille d'un poil — la peau *est*
  la fourrure : elle annule son propre contraste. Bloc **26**, soit trois à quatre poils.
- **La peau s'arrête un bloc AVANT le limbe.** Un bloc à cheval sur le bord est à moitié
  peint ; lui donner un alpha proportionnel faisait sortir **des carrés de couleur** autour
  de la boule. On **érode** : un bloc n'est opaque que si lui *et ses quatre voisins* sont
  pleins. C'est la fourrure, antialiasée, qui dessine seule la silhouette.
- **⚠ ET LE COMBLEMENT SE LIT SUR UNE COPIE, JAMAIS SUR LUI-MÊME.** Écrit en place, un
  balayage en lignes prend pour voisin **ce qu'il vient de combler** : le remplissage se
  propage vers le bas et vers la droite, et la boule sortait avec **un escalier de
  rectangles** hors du limbe — **en bas à droite seulement**. *C'est l'asymétrie qui trahit
  ce bug : un défaut de géométrie serait symétrique.*

### 2 · LE GRAIN VIENT MAINTENANT DE L'ANGLE DE LA FIBRE
Une fois la peau posée, il fallait redonner un dessin au pelage — sans les trous. Sur un
vrai velours, un poil **en travers** de la lumière s'allume, un poil **dans son axe**
s'éteint : c'est le terme de Kajiya-Kay, appliqué ici **à la marche d'un poil entier**, pas
en tache spéculaire. Aucun reflet n'apparaît, seulement des poils un peu plus clairs et un
peu plus sombres que leur voisinage.

**⚠ Et deux réglages le rendaient invisible :**
- **la dispersion d'angle se pose sur LA FIBRE, pas sur le tampon.** Posée juste avant
  `secteur`, elle ne tournait que le **dessin** ; le lustre continuait de lire le peigne
  moyen, donc tous les poils sortaient à la même marche.
- **la rampe ne doit pas saturer.** À `lum × 19,4`, le côté éclairé tombait déjà sur la
  dernière marche : la variation de fibre y était **écrêtée**, et la fourrure sortait lisse
  en haut à gauche et grenue en bas à droite, sans qu'on comprenne pourquoi.

### ⚑ ET LE « CROISILLON » ÉTAIT UNE MOIRE
Depuis que le peigne porte un biais, tous les poils d'une zone tombaient dans **le même
secteur sur vingt-quatre** : le même tampon, au même angle, sur un semis quasi-régulier —
**ça tisse**. Sur un vrai pelage les poils suivent le peigne **à peu près**, et c'est ce
« à peu près » qui fait le soyeux. La dispersion d'angle (0,74 rad) le rend.

### ⚠ ET LA MARGE DE REJET APLATISSAIT LA SILHOUETTE
Un poil dont le tampon sortirait du tampon de pixels écrirait sur la ligne suivante : on le
rejette, à 26 px du bord. Mais à **R = 0,472** la boule laissait **moins de marge que ça** —
le rejet lui coupait donc **quatre méplats**, en haut, en bas, à gauche et à droite. On
lisait un polygone là où la géométrie était un cercle exact. **R = 0,438**, soit un
diamètre de 342 pt dans un écran de 390 : les gouttières du produit.

### ⚠ ET LE BAS DE LA RAMPE NE DOIT PAS REJOINDRE L'ENCRE
À 0,62 vers le fond, le côté sombre **descendait sous le seuil de lecture de sa propre
silhouette** : les 360 rayons s'arrêtaient vingt pixels trop tôt en bas à droite. Une boule
dont le bord se dissout dans le fond n'a plus de contour — et le contour est ce qui la fait
exister. On garde le glissement vers l'encre (c'est lui qui évite le bleu électrique), on
s'arrête avant de la toucher : **0,44**.

### ⚑ LA TAILLE DE L'EMPREINTE SE CALCULE, ELLE NE SE CHOISIT PAS
`a` est le demi-grand axe du contact, **en fraction du rayon de la boule**. Il était à
**0,42** : l'empreinte faisait **84 % du diamètre de l'Orbite** — un doigt aussi large que
l'objet. Ce n'est pas un goût, c'est une cote :

```
ecran            390 pt pour 71,5 mm          =>  5,455 pt / mm
la boule         R = 0,438 x 390              =>  170,8 pt de rayon
pulpe de pouce   17 x 12 mm  => 8,5 et 6,0 mm =>  46,4 et 32,7 pt
pulpe d'index    11 x  8 mm  => 5,5 et 4,0 mm =>  30,0 et 21,8 pt

POUCE  a = 0,272  el = 0,70   soit 27 % du diametre
INDEX  a = 0,176  el = 0,73   soit 18 % du diametre
```

**Et c'est le capteur qui tranche, pas une constante.** Un `Touch` porte `radiusX`,
`radiusY` et `rotationAngle` : l'app lit la pulpe **réelle** et pose `a = radiusX / R`,
`el = radiusY / radiusX`, l'axe à l'angle donné. Les deux jeux ci-dessus sont **les bornes**
entre lesquelles ça tombe — c'est à ça qu'ils servent.
Une rangée de la planche le montre dans la page Aura, avec la pulpe tracée par-dessus à
l'échelle (calque de mesure, pas un élément du produit).

### CONTRÔLES
```
dix-neuf cadres compares deux a deux     zero doublon
circularite  g-vide                      rayon 275,0  ecart-type 0,91  soit 0,33 %
             n-neuf                      rayon 275,3  ecart-type 0,93  soit 0,34 %
             v-30 (grand format)         rayon 561,9  ecart-type 2,07  soit 0,37 %
degrade, diagonale haut-gauche -> bas-droite
  -0,85 (173,136,253) 161   -0,50 (147,100,253) 132   -0,20 (127, 71,250) 108
  +0,20 ( 97, 37,228)  76   +0,50 ( 70, 19,184)  53   +0,85 ( 75, 21,194)  57
cout des deux passes ajoutees, tampon 680 x 680
  comble 1,1 ms   peau 1,6 ms            (median sur onze passages)
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### ⚠ CE QUI N'EST PAS TENU
**Le budget de 60 images par seconde ne l'est pas sur cette planche** : un cadre de la page
Aura coûte **40 ms**, et **34 ms restent même en coupant tout le versement** — c'est la
boucle sur les points et le blit, pas les deux passes ajoutées. La planche tourne à
**180 000 poils** pour un écran de 340 px, là où le banc donnait 36 450 poils à 16,4 ms.
**C'est une densité de planche, pas une densité d'app** : le chiffre à tenir se mesurera
sur la vraie page, avec la densité qu'elle portera.

---

## ⚑ UNE SEULE VARIATION LARGE SUR LA BOULE : LA LUMIÈRE · 10 septembre 2026

> **`app.html` inchangé** (`61280542751d0d0df5bce546f9a091b1`) · `PLANCHE-VELOURS.html`
> + `scratchpad/_v_*.js`, copiés dans `sauvegardes/orbite-velours/`

Deux demandes : **retirer les traces de doigt au repos**, et **un vrai dégradé** — clair
en haut à gauche, violet profond vers le bas-droite. La seconde a ouvert quatre défauts
qui se cachaient les uns derrière les autres.

### 1 · LES TRACES SORTENT DU REPOS
Neuf caresses gravées en permanence **n'ont pas de sens** : au repos l'objet est **neuf**,
et c'est cette uniformité qui donne envie d'y toucher. La trace n'appartient qu'à **la
séquence du doigt** (`d-apres`, `n-marque`), jamais à l'état de repos.

### 2 · UN SEUL DÉGRADÉ, ET LA CLÉ RETROUVE SON AMPLITUDE
J'avais aplati la lumière à **0,16** pour tuer les halos — et j'ai tué le volume avec.
Ce n'était pas la clé qui posait des halos, c'étaient les termes qui posent un **motif**
(lustre de fibre en bandes, contre-jour en anneau, liseré au limbe). Ceux-là restent
coupés ; la clé repasse à **0,30 + 0,70**, et elle est **seule** — donc aucun motif n'est
possible. Mesuré sur la diagonale de `g-vide`, du coin haut-gauche au coin bas-droit :

```
-0,85   (130, 104, 188)   luminance 122
-0,50   (107,  78, 172)              97
-0,20   (100,  74, 161)              91
+0,20   ( 73,  36, 155)              60
+0,50   ( 66,  28, 150)              53
+0,85   ( 68,  27, 160)              54
```

### ⚑ MAIS TROIS AUTRES CHOSES VARIAIENT À LA MÊME ÉCHELLE, ET PASSAIENT DEVANT

**Un dégradé ne se voit que si RIEN D'AUTRE ne varie à sa taille.** Le dégradé était posé
et juste — et illisible, parce que trois mécanismes fabriquaient des taches de la taille
d'un cinquième de boule. Il a fallu les retirer un par un.

**a · LES ÉPIS DU PEIGNE.** Le sens du poil venait d'un seul bruit. Un champ de directions
tiré d'un bruit a des **points critiques** — des épis, comme sur un crâne — et chacun
sortait en large tache grise à centre radial. Un champ tangent sur une sphère **ne peut
pas** être partout non nul (boule chevelue) : il a forcément deux zéros. On choisit donc
**où ils tombent** au lieu de les subir — un biais constant, dans la direction qui sort
**horizontale à l'écran**, met les deux zéros **au limbe gauche et au limbe droit**, là où
la matière est vue de profil. Le bruit reste, à un tiers : il donne l'ondulation, plus la
structure.

**b · LE BAS DU SPECTRE DU RELIEF.** `A × K` est l'inclinaison qu'une onde donne à la
fibre, et les six valaient **0,12 chacune** : la plus basse fréquence inclinait donc autant
que la plus haute, mais sur cinq fois plus de surface. ⚠ **Essai fait et mesuré : faire
monter `A × K` avec `K` sort un QUADRILLAGE de pois pâles.** Dès qu'une fréquence domine,
on lit sa période ; six ondes de même inclinaison se somment en bruit. On ne touche donc
pas à la **répartition** — on divise **l'ensemble** par deux.

**c · L'ENVELOPPE.** Sa fréquence est de l'ordre de la boule : tout ce qu'elle peut
produire est une **tache**. Elle était là pour « faire respirer la matière » — mais la
respiration se lit dans le grain. **Amplitude nulle.**

### ⚑ ET LA PROXIMITÉ DES SIX ÉTAIT CÂBLÉE SUR LE MAUVAIS AXE
« Une personne proche est une matière **plus saturée, plus travaillée**. » Je l'avais
branchée sur **la marche de clarté** : +1,9 marche dans une calotte de 0,19 rad. Résultat,
**six pois ronds pâles** — exactement ce qui avait été refusé. Une marche de clarté **est
de la lumière**, et la lumière de cette boule vient du titre, d'un seul côté : on ne peut
pas s'en servir pour dire autre chose.
La table de couleurs a donc **un second étage** — les mêmes teintes, les mêmes vingt
marches, **ressaturées** (`s × 1,34 + 0,06`). Le poli ne déplace plus la marche, il change
d'étage : la matière devient plus dense **en couleur**, jamais plus claire. Coût par
image : nul, la table se bâtit une fois.

### ⚠ ET LA CLAIRIÈRE DU NOYAU N'AVAIT PLUS DE RAISON D'ÊTRE
Même adoucie à 0,80, elle sortait en **grand disque sombre** autour du Noyau — le « halo
bizarre » refusé, sous un autre nom. Le Noyau est crème sur un velours violet : il se
détache seul. `pres = 1` partout.

### ⚠ ET LE HAUT DE LA RAMPE VIRAIT AU GRIS, COMME LE BAS VIRAIT AU BLEU
Le mur de colorimétrie a **deux bouts**, et `rampeCouleur` ne joue que sur la clarté HSL.
En bas, baisser la clarté d'un violet saturé donne un **bleu électrique** — on mélange donc
vers l'encre du fond. En haut, la monter donne un **gris-lilas délavé** — on monte donc la
clarté de moitié moins (`+0,225` au lieu de `+0,30`) et **on ressature** (`× 1,34`). Le
haut reste violet, il est seulement plus lumineux.

### ⚠ ET LE SIGNE DE LA LUMIÈRE SE VÉRIFIE AU CHIFFRE, PAS AU RAISONNEMENT
J'ai déduit **deux fois de suite** la mauvaise convention pour la normale de vue, et deux
fois le clair est sorti du mauvais côté. Le contrôle tient en trois relevés de couleur
moyenne sur la diagonale (tableau ci-dessus). **On mesure, on ne déduit pas.**

### CONTRÔLES AVANT LIVRAISON
```
seize cadres compares deux a deux        zero doublon
circularite de la silhouette (g-vide)    rayon 295,7  ecart-type 0,87  soit 0,30 %
circularite (v-30, grand format)         rayon 601,3  ecart-type 5,26  soit 0,87 %
md5 app.html                             61280542751d0d0df5bce546f9a091b1  inchange
```

### CE QUI RESTE OUVERT
- **La composition de la page Aura** : la boule n'occupe que le tiers haut de l'écran.
- **Le concept alternatif** reste à construire — la fourrure est le candidat, pas la réponse.

---

## ⚑ LA LUMIÈRE VIENT DU TITRE, ET ELLE EST PRESQUE INVISIBLE · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### CE QUE TOM A DEMANDÉ
La sphère vit dans **l'écran Aura**, le mot-marque **Aura** en haut à gauche. La lumière vient
**de lui**, mais **suggérée** : un dégradé uniforme presque invisible, **et pas de halo** —
« ça complexifie trop ».

### CE QU'ON A COUPÉ, ET POURQUOI
```
la cle              0,42 -> 0,13     un tiers de la boule etait dans l'ombre
le lustre de fibre  0,22 -> 0        il pose UNE BANDE perpendiculaire au peignage ;
                                     sur un velours en volutes, les bandes se croisent
le contre-jour      0,40 -> 0        c'est un ANNEAU : un halo, donc un interdit
le lisere au limbe  +0,22 -> -0,10   un bord plus clair que le centre EST une aureole
le duvet du limbe   coupe
```
**Amplitude totale de la lumière : 0,16 sur 1.** Le volume vient du **grain**, pas de l'ombre.
La direction pointe franchement vers le haut-gauche — vers le titre.

### ⚠ J'AI ACCUSÉ LE CULLING À TORT, ET LA MESURE M'A REPRIS
Je lisais des **facettes** sur le bord et j'ai élargi le seuil des plaques pour « rendre la
frontière aux points ». Mesure ensuite (`scratchpad/mesure_rond.py`, 360 rayons tirés du
centre) : **rayon 296,3, écart-type 1,65 — soit 0,56 %.** **La silhouette était déjà un
cercle.** Ce que je prenais pour des facettes, ce sont les **grands plateaux clairs de la
matière** : l'enveloppe faisait varier l'amplitude du relief de **un à cinq**, d'où des zones
à bord franc qu'une lumière uniforme révèle. Ramenée de un à deux. Seuil de culling remis à
sa valeur, et son surcoût avec.
> **La condition « on doit pouvoir tracer un cercle parfait autour » est donc tenue, et
> mesurée : 0,59 % d'écart après correctif.**

### ET LA TRACE SE CALME
À +4,2 marches elle était lisible sous une lumière sculptée ; sous une lumière uniforme elle
devenait **une grande traînée pâle** qui mange la boule. **Une caresse laisse un lustre, pas
un coup de pinceau.** Ramenée à +1,9.

### CONTRÔLE AVANT LIVRAISON
**Treize cadres comparés deux à deux : zéro doublon.** C'est désormais systématique.

---

## ⚑ LA MÊME FAUTE, DEUX FOIS — et cette fois on supprime la classe · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### LE BUG, ET IL EST GRAVE PARCE QU'IL EST SILENCIEUX
`cadre()` recopiait **à la main** les options qu'elle connaît. La première fois,
`velours`/`contre`/`duvet`/`grade`/`dresse` tombaient dans le trou : huit cadres identiques au
pixel près. **Je l'ai « corrigé » en ajoutant ces cinq noms à la liste.** La faute était
**la liste elle-même** : au lot suivant, `traces` et `six` sont tombés dans le même trou.
```
« marque » et « relisse »   identiques a 0,00 %
les six par la matiere      JAMAIS APPLIQUES, sans une seule erreur
```
> **⚑ LA PARADE, ET C'EST LA BONNE :** `cadre()` recopie désormais **tout** ce que l'appelant a
> posé et que l'objet ne porte pas encore. Une option nouvelle arrive au peintre sans qu'on y
> pense. **Corriger l'occurrence d'un bug de recopie manuelle ne sert à rien — il faut
> supprimer la recopie manuelle.**
> Contrôle systématique ajouté : **treize cadres comparés deux à deux, zéro doublon.**

### ⚑ « LES HALOS AU PIXEL » — c'était une ombre portée déguisée
Les six se dessinaient **dans le tampon de pixels**, cercle par cercle, avec un test
`d² > r²` : **aucun antialiasing possible**, donc un bord en escalier. Et ils portaient un
**halo d'encre** de treize millièmes du rayon — c'est-à-dire **une ombre portée**, l'un des
trois interdits qui font le « cheap ». Le Noyau en avait un de trente-quatre millièmes.
Les deux sont redessinés **au contexte 2D, après le versement** : les arcs y sont antialiasés,
et le halo saute. Il ne reste qu'un **filet** de la couleur du fond pour que le crème ne bave
pas dans le velours — **un filet n'est pas un halo**.
Et leur **position n'encode plus rien** : ils sont posés à intervalle égal, puisque la
proximité se lit maintenant dans la matière.

---

## ⚑ « L'ÉCLAIRAGE EN CROISILLON » — c'était le RELIEF, pas la lumière · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-VELOURS.html` + `scratchpad/_v_*.js`

### LA CAUSE
Le relief valait `Σ amp · sin(fx·x) · sin(fy·y) · cos(fz·z)`. **Un produit de sinus est
SÉPARABLE : ses zéros sont des plans x = cte, y = cte, z = cte.** La surface portait donc
une **grille**, et dès qu'on l'éclairait on voyait un croisillon en travers de la boule.
Ce n'était ni la lumière ni le grain — **c'était la forme même du relief.**

### LA PARADE — UNE SOMME D'ONDES PLANES OBLIQUES
```
avant   3 bandes, produit de sinus sur les axes x, y, z   -> un reseau
apres   6 ondes planes, directions prises sur une spirale de Fibonacci,
        normes 9,7 a 37,7 irrationnelles entre elles      -> isotrope
```
Aucune onde n'est alignée sur un axe, aucune période n'est commune : le relief ne se répète
plus. ⚠ **Et la règle de l'audit tient toujours** — « toutes les fréquences ≥ 8 sur les trois
axes », qui évitait une enveloppe basse fréquence sur un seul axe (une courge) : chaque onde a
un vecteur d'onde de norme ≥ 9 **dans une direction oblique**.
**L'enveloppe aussi** était un produit de sinus : elle reposait son propre réseau, plus
grossier, par-dessus le premier. Passée en somme de deux ondes obliques.
Amplitude totale **divisée par deux** : le relief n'a pas à se voir, il est là pour accrocher
la lumière rasante.

### ET UN ÉCLAIRAGE SIMPLE
Le lustre de fibre (Kajiya-Kay) pose une **bande claire perpendiculaire au peignage** : sur un
velours peigné en volutes, ces bandes **se croisent** et ajoutent leur propre motif. Joli en
mouvement, du bruit sur une image fixe. Ramené de 0,80 à **0,22** — il ne doit plus que tiédir
la matière, pas la dessiner. Contre-jour 0,70 → 0,40, grading 0,9 → 0,55.

### CE QUI RESTE DISCUTABLE
- Le contact sort encore en **tache très saturée** plutôt qu'en compression.
- La boule est maintenant **très uniforme** — subtile, comme demandé, peut-être trop calme.

---

## ⚑ LE VELOURS, ET LA MÉMOIRE DE LA MAIN · 9 septembre 2026

> **`app.html` inchangé** · **`PLANCHE-VELOURS.html`** + `scratchpad/_v_*.js`
> La fourrure est **ressortie** de `sauvegardes/ORBITE-FOURRURE-DEPOSEE/`.
> Les trois concepts du lot précédent (mémoire minérale, fil, fond perdu) sont **refusés en
> bloc** par Tom — concept et design. Ils restent dans `sauvegardes/orbite-memoire/`.

### LES QUATRE CHANGEMENTS
**1 · UN VELOURS, PAS UNE FOURRURE.** Le pelage montait à 13 px sur un cadre de 620 : ça fait
une bête, pas une matière. `[1,9 · 3,3 · 4,3 · 5,5]` — deux fois et demie plus court. **Et le
ras durcit la silhouette**, parce qu'un poil court déborde moins du contour. Semis remonté à
360 000 pour garder la matière pleine.

**2 · LES DALLES SONT TAILLÉES DANS LE MÊME VELOURS.** Le rapport entre la coupe d'une dalle
et celle du sol tombe de **3,8 à 2,3** : une dalle cesse d'être une **inclusion posée dessus**,
elle devient **un endroit où le velours a une autre teinte et une autre coupe** — dans la
couleur et le monde de sa plantation.

**3 · LA MÉMOIRE DU GESTE.** La déformation est réelle sur le moment, puis **la forme revient** :
la silhouette n'est jamais abîmée. Ce qui reste n'est **pas un creux** — c'est le poil couché :
la chroma monte de quatre marches, le grain s'oriente dans le sens du geste, la coupe se tasse.

**4 · TOUT RELISSER.** Un état « neuf » où toutes les traces sont effacées. C'est ce qui rend
le peignage **sans conséquence** : on peut jouer sans rien salir.

### ⚑ LES SIX PAR LA MATIÈRE, PAS PAR LA POSITION
Encoder la proximité par une **distance** force la structure radiale, donc le centre, donc
l'objet centré, donc le contour — **la case qui a tué quinze versions**. Ici une personne
proche est une **matière plus travaillée** : plus saturée, au grain plus fin, **où qu'elle soit
sur la sphère**. Leurs positions sont à intervalle égal et n'encodent rien. La géométrie est
libérée, et *« rien ne recule jamais »* tient toujours — **une matière ne se désature pas.**

### ⚠ UN PIÈGE ÉVITÉ CETTE FOIS
La clé du cache des statiques **ne portait ni les traces ni les six**. Deux cadres qui ne
diffèrent que par la mémoire des gestes se seraient partagé le même cache et seraient sortis
**identiques au pixel près** — exactement la livraison où huit cadres étaient les mêmes.
Ajouté à la clé avant de rendre.

### MESURÉ — les états diffèrent vraiment
```
sous le doigt        40,6 % des pixels different du repos
deux secondes apres  11,2 %
relisse              20,5 %
```

### CE QUI RESTE À JUGER
- Le contact sort en **tache très saturée** plutôt qu'en compression : lisible, mais peut-être
  trop marqué.
- L'état « deux secondes après » garde encore beaucoup — le retour pourrait être plus net.

---

## ⚑ TROIS CONCEPTS EN CANVAS 2D RÉEL — la mémoire de la main · 9 septembre 2026

> **`app.html` inchangé** · **`PLANCHE-MEMOIRE.html`** + `scratchpad/_m_*.js`
> **L'orbite-fourrure est DÉPOSÉE**, pas abandonnée : `sauvegardes/ORBITE-FOURRURE-DEPOSEE/`
> avec son mode d'emploi de retour et les six acquis qui valent pour toute suite.

### LE PARTI, ISSU DE DEUX ÉTUDES INDÉPENDANTES
**Un objet numérique qui se souvient des gestes de son propriétaire.** La patine est
**l'organe**, pas l'ornement. Avec trois conditions posées par Tom :
1. **La forme reste belle** — on doit pouvoir tracer un cercle parfait autour, quelle que soit
   l'histoire des gestes. Une empreinte ne rend jamais l'objet difforme.
2. **La matière résiste** — ni mou, ni slime, ni caoutchouc : entre la céramique crue, la cire
   minérale et la pierre tendre. Une matière qui n'existe pas.
3. **Ça revient** — la déformation est réelle sur le moment, puis la forme sphérique revient.
   **Ce qui reste n'est pas un creux : c'est un lustré, un grain, une chroma qui a monté.**

### COMMENT ON PEINT SANS DÉGRADÉ, SANS OMBRE ET SANS TACHE SPÉCULAIRE
Ce sont **ces trois-là** qui font le « méga cheap ». Donc : **chaque marque est un aplat franc**
pris dans une rampe de vingt marches. Le volume ne vient pas d'un fondu — il vient **du nombre**
de marques et de la marche que chacune prend. C'est la règle du moteur de la Toile, à la lettre.
Le contour se dessine par le **raccourci au limbe** (la matière s'y voit de biais, elle rend
moins), jamais par un liseré lumineux.

### LES TROIS PLANCHES
```
A · LA MEMOIRE DE LA MAIN   une matiere minerale (facettes, pas des poils), et le
                            POLI des gestes : le grain s'affine, se couche dans le
                            sens du geste, la chroma monte d'un ton
B · LE FIL                  le cumul des trajets d'un fil autour du Noyau ; ce qu'on
                            voit est le MOIRE qu'ils forment ensemble
C · A, A FOND PERDU         la meme matiere, sans contour, plein cadre
```

### DEUX BUGS PAYÉS
- **Les fils convergeaient tous en un point.** Je construisais un point puis je le
  **normalisais** — or normaliser rend toujours le même **grand** cercle, quels que soient le
  rayon et l'aplatissement. Tous les fils passaient donc par les deux mêmes pôles. On construit
  maintenant un **petit cercle** directement sur la sphère (axe, hauteur, `c² + r² = 1`).
- **La trace sortait SOMBRE.** Le grain poli était si fin qu'il couvrait *moins* que la matière
  brute : le fond passait entre les marques. Or ce qui reste d'un geste **n'est pas un creux,
  c'est un lustre**. Allongé sans être aminci, il couvre plus — et la chroma monte.

### CE QUE JE VOIS, HONNÊTEMENT
- **A tient son état vide** : une sphère minérale, contour parfaitement circulaire, grain fin,
  et les caresses lisibles comme des bandes lustrées. À 30, les dalles se lisent chacune dans
  son monde. **C'est le seul des trois qui passe le test décisif.**
- **B est superbe à 30** — un échevau de fils avec un vrai moiré — **et rate le test à vide** :
  sept fils ne font pas un objet, ils font des courbes lâchées dans le noir.
- **C répond à la question posée, et la réponse est non** : sans contour, on n'a plus un objet,
  on a un champ de grain. Supprimer le bord **supprime l'objet** au lieu de régler son bord.

### CE QUI N'EST PAS FAIT
- La proximité des six **par la matière** (et non par la position) n'est pas encore câblée.
- La déformation au doigt et son retour lent : c'est du mouvement, invisible sur une planche fixe.

---

## ⚑ « LE DERNIER POSÉ GAGNE » — la ligne qui bloquait tout depuis le début · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### CE QUE TOM A DIT
> *« la sphère n'est pas uniformément poilue ni éclairée, du coup on ne se rend pas compte des
> ajouts de dalles, ça complexifie tout »*

### ⚑ LA CAUSE, ET ELLE TIENT EN UNE LIGNE
`verse()` écrivait **sans relire** — *« le dernier posé gagne »*, une optimisation mesurée
(−18 % par poil) dont le commentaire disait *« acceptable pour une fourrure, un poil en
recouvre un autre »*. **Ce n'était pas acceptable, et voici pourquoi.**

L'alpha d'un brin est **fort à la racine, faible à la pointe**. Le peignage a une direction
dominante : du côté où les poils pointent, ce sont donc **les pointes qui écrasent les racines**
de leurs voisins ; du côté opposé, ce sont les racines. **Une moitié de boule à 49, l'autre à
83** — à couverture égale et à éclairage égal.

**La parade tient en un test : on garde LE PLUS OPAQUE.** L'alpha étant dans l'octet de poids
fort, comparer les entiers compare les alphas — c'est un « max » à une comparaison, pas un
mélange.

### ⚠ TROIS HYPOTHÈSES FAUSSES AVANT DE TROUVER — et c'est la mesure qui a tranché
```
aplatir la cle (0,52 -> 0,12)          aucun effet       59,2 % -> 58,3 %
supprimer les variations de densite    aucun effet
densifier x2,3                         CA EMPIRE         43,9 % -> 52,4 %
```
> **⚑ ET UN INSTRUMENT QUI MESURAIT LE MAUVAIS CHIFFRE.** Mon premier écart-type était pris
> **pixel par pixel** : sur une fourrure il mesure **les poils**, pas l'inégalité d'éclairage —
> 47 sur 80 de moyenne, et il ne bougeait pas d'un point quand je coupais tout l'éclairage.
> On réduit l'image à 40×40 (chaque case moyenne des milliers de poils) et c'est **cette**
> dispersion qui dit si la boule est uniforme.

> **⚑ ET C'EST LA SONDE QUI A DONNÉ LA RÉPONSE.** J'ai instrumenté le peintre pour relever ce
> qu'il **dépose**, quart d'écran par quart d'écran : `lum` 0,95 à 1,00, `mar` 14,5 à 15,0,
> 21 400 points chacun — **identiques**. Et le quart le plus clair en `lum` était **le plus
> sombre à l'écran**. C'est cette contradiction qui a désigné le versement.

### CE QUE ÇA DONNE
```
                        AVANT          APRES
luminance moyenne        81,9          147,7      (cible : 90 a 110)
dispersion basse freq.   43,9 %         15,2 %
moitie sombre / claire   48,9 / 83,2   156,6 / 134,6
```
**Et un dividende : l'éclairage avait été aplati pour compenser ce défaut.** Le défaut corrigé,
un éclairage plat n'avait plus de raison d'être — il donnait un aplat lilas sans relief. La
clé est rendue (0,46 + 0,42), et le volume avec.

### CE QUI N'EST PAS FAIT
- La boule est **au-dessus** de la cible de luminance et un peu **lavée** : à cette clarté le
  lilas se désature (le mur de colorimétrie du lot précédent, dans l'autre sens).
- Le peigné-mémoire, l'inertie, la naissance d'un Promi : toujours pas construits.

---

## ⚑ POIL DE CHAT, DALLES RASÉES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`
> Sauvegarde : `sauvegardes/orbite-fourrure/`

### CE QUE TOM A DEMANDÉ
> *« plus soyeux, plus comme poils de chats ou lapin, plus nets, un peu plus long — et les
> dalles c'est en rasé plus court ? »*

### QUATRE CORRECTIFS

**1 · QUATRE LONGUEURS, ET LA PREMIÈRE EST LA TONTE.** `[3,4 · 7,6 · 10,2 · 13,0]`.
Index 0 = **les dalles**, index 1 à 3 = le pelage par profondeur. **Une zone tondue dans un
pelage se lit d'un coup d'œil** — c'est du relief, pas un aplat de couleur — et le rasé
**montre sa couleur bien mieux**, puisqu'il y a moins de brins qui se recouvrent pour la
moyenner. Le réglage `dresse` (les dalles en relief) sort : elles sont **tondues**, pas dressées.

**2 · PLUS NET.** À 0,86 d'extinction, la pointe disparaissait avant d'arriver et le pelage
sortait **brumeux** — on lisait un voile, pas des poils. Un poil de chat ou de lapin garde sa
matière presque jusqu'au bout : **il s'affine beaucoup, il ne s'efface pas.** On inverse le
partage — extinction `0,86 → 0,42`, affinement `0,78 → 0,88`.

**3 · PLUS SOYEUX : LES BRINS SE SERRENT.** Une fourrure de chat ou de lapin est fine, dense
et **parallèle** — c'est l'alignement qui fait le soyeux. À ±0,44 d'écart les brins partaient
en étoile : ça fait une **brosse**, pas un pelage. Resserré à **±0,20**, allongé, affiné
(`e×0,115 → e×0,095`).

**4 · ON OUVRE L'OMBRE.** À 0,34 d'ambiant contre 0,52 de clé, **la moitié de la boule tombait
dans le noir** : on ne pouvait ni lire ses dalles ni avoir envie d'y toucher. Ambiant `0,50`,
clé `0,40` — ce que fait n'importe quel éclairage de studio : **un remplissage qui ouvre
l'ombre au lieu de la boucher**, sans effacer le volume, puisque c'est le contraste qui
sculpte et pas le noir.

### MESURÉ
```
             luminance   saturation
avant           52,5        0,31
apres           60,5        0,29     cout 10 a 25 ms
```

### CE QUI N'EST PAS FAIT
- **La cible de 90-110 reste hors d'atteinte sur un sol bleu-violet** — c'est le mur de
  colorimétrie du lot précédent, pas un réglage. Le fork (sol chaud contre sol violet) est
  toujours ouvert et il appartient à Tom.
- Les dalles gagnent en lisibilité mais restent peu contrastées sur les mondes creux.
- Le peigné-mémoire, l'inertie, la naissance d'un Promi : toujours pas construits, et c'est là
  qu'est le « donne envie de toucher » qu'une planche fixe ne peut pas montrer.

---

## ⚑ LA LUMINANCE PERÇUE, ET LE MUR DE COLORIMÉTRIE · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### ⚑ CE QUI BLOQUAIT LA CLARTÉ DEPUIS LE DÉBUT — MESURÉ
Le sol sortait à **[77, 9, 225]** : clarté HSL **0,46**, luminance **perçue 54**.
**Le bleu ne pèse que 11 % dans la luminance** (0,299 R + 0,587 V + 0,114 B) : régler une
*clarté HSL* sur une teinte bleu-violet **ne veut rien dire à l'œil**. Je croyais avoir monté
l'objet ; je n'avais monté qu'un nombre.
On résout désormais **en luminance perçue**, par dichotomie ; si la teinte ne peut pas y
arriver à saturation pleine, on désature juste ce qu'il faut — jamais l'inverse. Le sol tombe
alors **exactement sur sa cible**, vérifié : 96.

### ⚑ LES DALLES S'ÉCHELONNENT EN LUMINANCE
*« on reconnaît peu les dalles, faut les préciser ou contraster »* — deux couleurs peuvent
avoir des **teintes très différentes et la même luminance** : l'œil les sépare alors mal,
surtout sous une fourrure qui moyenne tout. On impose donc des luminances **étagées**, toutes
écartées d'au moins **34** du sol. **La teinte dit laquelle ; la luminance garantit qu'on la voit.**

### ⚠ ET LÀ ON TOUCHE UN MUR QUI N'EST PAS UN RÉGLAGE
```
decalage de rampe    luminance de la boule    saturation
+1,9                       46,7                  0,38
+3,6  (retenu)             52,5                  0,31
+5,6                       58,8                  0,23
```
**Monter la clarté d'une teinte la rapproche du blanc.** Une teinte **bleu-violet ne peut pas
être à la fois claire et saturée** — c'est de la colorimétrie, pas un défaut de réglage.
On s'arrête donc où la couleur tient encore, et **le contraste se fait ailleurs** : entre le
sol et les dalles.

**Le vrai fork, et il est de direction artistique :**
- **un sol bleu-violet** — saturé, mais plafonné vers 55 de luminance ;
- **un sol chaud** (l'orange de Signal) — qui peut monter à 100 **et** rester saturé, avec les
  dalles en bleu et violet dessus.
La cible « 90 à 110 » n'est atteignable qu'avec le second.

### CE QUI N'EST PAS FAIT
- La cible de luminance n'est pas atteinte, et **on sait maintenant pourquoi** — ce n'est ni la
  densité (mesuré : +47 % de touffes = rien) ni la rampe seule, c'est **la teinte du sol**.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits — c'est là
  qu'est le « donne envie de toucher », et ça ne se voit pas sur une planche fixe.

---

## ⚑ LE SOL UNIFORME, LES ÎLES SONT DE VRAIES DALLES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`

### CE QUE TOM A DIT
> *« ça doit être uniforme de base, et des dalles de Promi dans leur design et couleur de
> lorsqu'ils ont été créés (ça s'ancre et ne rechange pas, donc diversité de design de dalles
> sur la surface de la sphère). Là ce sont des pois ronds qui correspondent à rien. »*

### DEUX CORRECTIFS, ET LE SECOND EST STRUCTUREL

**1 · LE SOL EST UNIFORME.** J'avais mis trois tons répartis par un champ basse fréquence,
pour éviter l'aplat. **C'était une erreur de lecture :** ce qui doit donner la variété, ce sont
**les dalles**, pas le fond. Un fond à zones fait un camouflage, et les dalles s'y perdent.
Une seule teinte — c'est le relief de la fourrure qui la fait vivre.

**2 · UNE ÎLE EST UNE VRAIE DALLE, DANS LE MONDE DE SA PLANTATION.**
Une île n'est pas une tache de couleur : c'est **le Promi**, avec le design et la couleur qu'il
avait le jour où on l'a planté. **Ça s'ancre et ça ne rechange plus** — c'est la règle du §4 de
CLAUDE.md, « une dalle est figée à sa plantation ». D'où une **diversité de designs à la
surface de la même sphère** : une encre à côté d'une braille à côté d'une gravure.
Le moteur les peint lui-même, une par une, via `Toile.dalleGeneree`, **dans une vraie cellule
de Voronoï** — un rond « ne correspond à rien », une dalle a le contour de sa cellule.

```
la cellule    on rabote un grand carre par les bissectrices de voisines jitterees,
              une graine par ile : chaque dalle a sa propre forme
le monde      tire par ile parmi les huit — c'est ca, la diversite
la pose       la dalle est posee A PLAT dans le plan tangent de son ile, comme
              un ecusson. Au-dela de ~0,3 rad la projection s'etirerait ;
              une ile fait 0,215, on reste dedans.
le pas        la trame se lit AGRANDIE (mag 2,2) : un poil fait 6 a 10 px, un
              carreau de mosaique 11. A l'echelle naturelle le poil l'ecrase —
              c'est la collision d'echelles payee tout au long du chantier.
l'epi         chaque ile garde son peignage propre : sur un vrai pelage, deux
              plages se distinguent par LE SENS DU POIL autant que par la couleur.
```

### MESURÉ
```
zero ile     luminance 38 a 40      cout 10 a 25 ms selon le cadre
trente iles  luminance 40 a 43
```

### CE QUI N'EST PAS FAIT
- **La luminance reste très sous la cible** (38-43 contre 90-110), et on sait où c'est bloqué :
  **dans la rampe de couleur, pas dans la densité** — densifier de 47 % n'avait rien donné.
- **La première île se lit mal** : elle tombe près du Noyau et sa dalle est sombre.
- Plusieurs dalles restent peu contrastées sur le sol violet — les mondes creux (gravure,
  sillons) surtout.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚑ AFFINER LES TOUFFES, DISTINGUER LES ÎLES · 9 septembre 2026

> **`app.html` inchangé** · `PLANCHE-FOURRURE.html` + `scratchpad/_o_*.js`
> Sauvegarde : `sauvegardes/orbite-fourrure/`

### CE QUE TOM A DIT
> *« on ne distingue pas les dalles, et ça ne paraît pas assez doux, faut affiner les touffes »*

### TROIS CORRECTIFS
**1 · SIX BRINS, DEUX FOIS PLUS FINS.** La douceur d'une fourrure ne vient pas de sa longueur,
elle vient de la **finesse** et du **nombre** : c'est le recouvrement de brins qu'on ne
distingue plus qui fait le soyeux. À quatre brins épais on lisait encore chaque trait.
Épaisseur `e×0,19 → e×0,115`. Le coût est faible : deux brins de plus sur la **même racine**
ne paient que leurs pixels, et ils en paient moins puisqu'ils sont plus fins.

**2 · CHAQUE ÎLE A SON ÉPI.** C'est le séparateur le plus fort qu'on ait, et il ne coûte rien.
Sur un vrai pelage, deux plages ne se distinguent pas que par la couleur : elles se
distinguent par **le sens du poil**. Une spirale centrée sur l'île sépare deux îles voisines
même de teintes proches, et elle accroche la lumière rasante autrement que le sol.

**3 · DES CLARTÉS ÉCHELONNÉES POUR LES ÎLES.** Le lilas (208·176·255) et le periwinkle
sortaient presque **blancs** : leur clarté d'origine est trop haute pour servir d'île sur un
sol déjà clair, et deux îles voisines devenaient indistinctes. On garde la **teinte** de la
palette — c'est elle qui lie l'Orbite au Studio — et on impose des **clartés échelonnées**,
toutes écartées du sol. La teinte dit laquelle ; la clarté garantit qu'on les sépare.

### ⚑ CE QUI NE PAIE RIEN — MESURÉ, NE PAS Y REVENIR
Affiner a coûté **cinq points de luminance** (44,4 → 39,5) : des brins plus minces couvrent
moins. J'ai cru compenser en densifiant — **190 000 → 280 000 touffes, +47 % de calcul** — et
la luminance est sortie à **38,6, c'est-à-dire RIEN**. La couverture était déjà saturée :
**ce qui plafonne la clarté n'est pas le nombre de poils, c'est LA RAMPE** (le sol part de
0,46 de clarté et les deux dernières marches sont réservées aux reflets). Retour à 190 000.
**La clarté se traitera dans la couleur, jamais dans la densité.**

### MESURÉ
```
                luminance   saturation
zero ile           38,6        0,46
cinq iles          42,6        0,42
trente iles        40,4        0,42
cout              10 a 24 ms selon le cadre
```

### CE QUI N'EST PAS FAIT
- **La luminance reste très sous la cible** (39 à 43 contre 90 à 110) et **on sait maintenant
  où elle est bloquée** : dans la rampe, pas dans la matière. C'est le prochain chantier.
- Une des quatre couleurs d'île sort **kaki** (l'orange à clarté haute perd sa saturation).
- La clairière du Noyau se lit encore comme un anneau sombre.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚑ CHANGEMENT DE PARTI · LA FOURRURE D'ABORD, LES ÎLES DEDANS · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> **`AUDIT-ORBITE.md` corrigé sur quatre points** (ancienne version :
> `sauvegardes/AUDIT-ORBITE-avant-fourrure.md`).
> Nouveau document : **`PLANCHE-FOURRURE.html`** + `scratchpad/_o_*.js`.
> `PLANCHE-PAVAGE.html` et `ORBITE-REFERENCE` restent intacts.

### CE QUI SORT DE L'AUDIT
1. **« C'est vraiment la Toile de l'utilisateur, vérifié au pixel »** — retiré des acquis.
   Un pavage **partitionne** : sa beauté est fonction de sa densité. À une dalle c'est une
   sphère unie ; il ne devient beau que vers vingt ou trente. Une Orbite neuve doit être belle
   **dès le premier jour**. La bonne géométrie est l'inverse.
2. **« Le rayon dit la date de la dernière parole tenue »** — retiré. C'était **un compte à
   rebours dessiné en rond et pointé vers une personne**. Le rayon encode désormais le
   **cumul** ; rien ne recule jamais.
3. **Le peigné devient une mécanique**, pas un effet : l'objet garde la trace de la main.
4. **Monter en chroma, pas en luminance** ; la palette vient du Studio.

### LES TROIS BUGS DE CE LOT, TOUS MESURÉS
- **Les poils étaient restés courts.** Ils avaient été ramenés à 3,1 px pour ne pas étaler la
  trame d'une dalle — **et il n'y a plus de trame**. Une île fait 0,2 rad, cent fois un poil.
  Retour à 6 / 8 / 10,4, et le semis divisé par deux puisque chaque poil couvre trois fois plus.
- **Le centre de la grappe donné en coordonnées d'OBJET — troisième fois.** La vue est tournée
  de 2,9 rad : la grappe tombait **derrière** la boule, et les états à une et cinq îles étaient
  identiques au vide. On l'écrit dans le repère de la vue puis on le ramène — comme le foyer
  du semis, comme l'empreinte. **L'audit §4 le prescrivait déjà.**
- **Zéro île en donnait une.** La première était posée avant la boucle : l'état « vide » et
  l'état « une » avaient la même luminance à la décimale près.

### ⚑ ET UN PELAGE N'A PAS UNE COULEUR, IL EN A TROIS
Un sol d'une seule teinte sort en aplat violet : on lit du bruit coloré, pas de la fourrure.
Trois tons de la **même famille**, répartis par un champ basse fréquence, suffisent — c'est
la lumière rasante qui fait le reste.

### MESURÉ
```
                 luminance   saturation      (cible : 90-110 de luminance)
zero ile            44,4        0,50
cinq iles           51,9        0,43
trente iles         62,6        0,32
avant ce lot        28,8        --
cout               10 a 22 ms selon le cadre
```

### CE QUI N'EST PAS FAIT — et je ne le maquille pas
- **La luminance reste sous la cible** (44 à 63 contre 90 à 110). L'objet a doublé de clarté,
  il n'a pas atteint le but.
- **Deux couleurs de la palette Signal lisent presque blanc** (le lilas 208·176·255 et le
  periwinkle) : leur clarté d'origine est trop haute pour servir d'île sur un sol clair.
  Il faudra les **rabattre en clarté** pour les îles, ou choisir les couleurs d'île autrement.
- **La clairière du Noyau se lit encore comme un anneau sombre**, pas comme une matière qui
  s'écarte.
- Le peigné-mémoire, l'inertie et la naissance d'un Promi ne sont pas construits.

---

## ⚠ J'AI LIVRÉ HUIT FOIS LA MÊME IMAGE — le bug, et la règle qui en sort · 9 septembre 2026

> **`app.html` inchangé** · **la référence `ORBITE-REFERENCE` n'est pas touchée**
> Variations : `PLANCHE-SEXY.html` + `scratchpad/_s_*.js` · `sauvegardes/orbite-variations/`

### CE QUE TOM A VU AVANT MOI
> *« tu m'as mis plusieurs fois les mêmes images, je vois pas les différences. »*

**Mesuré : les huit cadres étaient identiques AU PIXEL PRÈS.** `cadre()` recopie à la main
les options qu'elle connaît — et rien d'autre. Mes réglages de variation (`velours`, `contre`,
`duvet`, `grade`, `dresse`) n'arrivaient donc **jamais** au peintre. J'ai livré huit fois le
témoin en le présentant comme six propositions.

> ### ⚑ LA RÈGLE QUI EN SORT
> **Quand on ajoute une option à un peintre, on vérifie que deux réglages différents donnent
> deux IMAGES différentes — en comptant les pixels, avant de livrer.**
> Un cadre qui ne bouge pas est un cadre qui ne prouve rien. Le contrôle tient en trois lignes
> (`ImageChops.difference`) et il aurait économisé une livraison entière.

### APRÈS CORRECTIF — l'écart au témoin, mesuré
```
B lustre de fibre   10,7 %      E + grading          15,7 %
C + contre-jour     13,0 %      F tout, pousse       19,7 %
D + limbe duveteux  13,4 %      G les Promi dresses  18,6 %   H pousse  21,1 %
```

### PLUS FOURNI — et ce que ça coûte
Reproche de Tom : *« faut densifier un peu les poils, dans mosaïque ou braille ça fait un peu
peu fourni. »* Juste : sur une trame creuse, la matière ne couvre que la moitié d'une cellule
et le fond se voit entre les marques. **330 000 → 520 000 touffes.**
```
330 000 touffes   22 ms      520 000 touffes   31 a 35 ms
```
**La densité se paie plein pot** — c'est un arbitrage, pas un progrès gratuit. La référence
reste à 330 000 ; seules les variations sont à 520 000.

---

## ⚑ LA RÉFÉRENCE EST FIGÉE — et les variations vivent à part · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> **RÉFÉRENCE : `sauvegardes/ORBITE-REFERENCE/`** — code, images, et un `LISEZ-MOI.md`
> qui dit pourquoi elle fait foi. *« enfin c'est correct merci. on garde ceci comme
> référence désormais. »* — Tom, 9 septembre 2026.
> **`PLANCHE-PAVAGE.html` reste la référence et n'est plus touchée.**
> Les variations vivent dans **`PLANCHE-SEXY.html`** + modules `scratchpad/_s_*.js`
> (copies indépendantes). Sauvegarde : `sauvegardes/orbite-variations/`.

### CE QUI EST CONSTRUIT ET RENDU — huit cadres, une chose à la fois
```
A  la reference                    le temoin
B  + le lustre de fibre            Kajiya-Kay : la clarte suit le SENS DU POIL
C  + le contre-jour                le lisere de pointes translucides au limbe
D  + le limbe duveteux             au bord le poil est vu de profil, donc plus long
E  + le grading                    cle chaude / ombre froide, cuit dans la rampe
F  tout, pousse a 150 %            pour voir ou est le trop
G  LES PROMI TENUS SE DRESSENT     le pelage d'une dalle plantee est plus long
H  le relief, pousse
```

### ⚑ LES DEUX IDÉES QUI COMPTENT, ET POURQUOI
**1 · LE LUSTRE DE FIBRE.** Un velours ne se lit pas à sa couleur, il se lit à son
**anisotropie**. Un poil est un cylindre : il ne renvoie pas dans une direction mais sur un
**cône** — le reflet n'est donc pas une tache, c'est une **bande perpendiculaire au peignage**,
et elle **glisse quand la boule tourne**. C'est la propriété qui rend un velours hypnotique,
et on avait la direction du poil sous la main : elle servait à orienter le tampon dix lignes
plus bas. ⚠ Aucune tache spéculaire n'apparaît — le terme ne dépend que du **sens** du poil,
donc la règle du §6 de l'audit tient.

**2 · LES PROMI TENUS SE DRESSENT.** C'est la proposition que je défends, et elle n'est pas
technique : elle est **éditoriale**. Sur la Toile, 58 % des cellules sont grises. Enroulées
telles quelles, ça donne *un globe gris avec des confettis* — le sujet disparaît. Ici le
pelage d'une dalle plantée est **plus long** : elle se tient plus haut que le fond, la lumière
rasante l'accroche, sa silhouette déborde sur le gris. Ni sa couleur ni son dessin ne changent
— on lui donne du **relief**. **Ce qu'on a tenu est littéralement ce qu'on touche.**
⚠ Et aucune information de cellule n'est nécessaire : sur la Toile un fond est **gris**
(saturation quasi nulle) et une dalle porte une couleur de palette. La **saturation** suffit
à les distinguer, teinte par teinte, une fois pour toutes. Coût : un cran de taille de tampon.

### CE QUI EST PROPOSÉ MAIS PAS CONSTRUIT
- **la mémoire du toucher** — l'empreinte se relève en ~1,2 s avec un léger dépassement, et le
  pelage peigné reste peigné puis se redresse. C'est ce qui transforme un toucher en jeu ;
- **l'inertie et le retard du pelage** — la boule file après une chiquenaude, la fourrure
  traîne de quelques degrés et rattrape. Rien ne dit « vivant » comme un mouvement secondaire ;
- **la naissance d'un Promi** — la boule tourne pour amener la cellule devant, le pelage
  **pousse** depuis son centre en 700 ms avec un bref éclat. C'est le moment de récompense ;
- **le souffle** — au repos, ±0,5 % de rayon sur quatre secondes ;
- **le Noyau dans le pelage** — la fourrure s'écarte autour de lui et il jette une ombre douce
  dedans, au lieu d'être posé dessus.

---

## ⚑ LOT 11 · ON N'ASSEMBLE PLUS RIEN — LA TOILE EST ENROULÉE · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Ajout dans la **copie** du moteur : `Toile.toilePleine`. Planche : `PLANCHE-PAVAGE.html`
> Sauvegarde : `sauvegardes/orbite-lot11/`

### CE QUE TOM A DIT, ET CE QUE JE FAISAIS DE TRAVERS DEPUIS LE DÉBUT
> *« on veut la vraie Toile enveloppée en sphère, mise fluffy. Là je vois bien que c'est des
> images de dalles découpées mises fluffy. »*

**Il a raison, et c'était structurel : je FABRIQUAIS des dalles et je les ASSEMBLAIS.** Même
peintes par le moteur, même dans leur vraie cellule, même avec la bonne phase — ça reste un
montage, et un montage se voit. Dix lots à améliorer un assemblage, alors que le problème
était l'assemblage lui-même.

### ⚑ LE RENVERSEMENT : UNE TOILE, PEINTE EN UNE FOIS, PUIS ENROULÉE
```
1 · `Toile.toilePleine` peint UNE Toile complete, a la densite de l'app
    (cellules de 72 px), assez grande pour couvrir la sphere : 1054 x 1054.
    C'est le moteur, son semis, son pavage, sa grille, ses contours, ses espaces.
2 · chaque poil va lire SA COULEUR DEDANS, a l'endroit ou il se trouve.
```
Plus de dalle à fabriquer, à choisir, à mettre à l'échelle, à raccorder. **Il n'y a plus
qu'un seul dessin**, et c'est celui du moteur.

**Pourquoi `toilePleine` et pas `preview` :** `preview` impose sa densité (`base = pw/5,5`,
soit toujours cinq ou six cellules de large). Pour couvrir une sphère il faut une **grande**
Toile **avec des cellules de la taille de celles de l'app**. Même mécanique, densité demandée.

**La projection : Lambert azimutale équivalente**, `k = √(2/(1+z))`, `u = kx`, `v = ky`.
Elle envoie la sphère (aire 4π) sur un disque de rayon 2 (aire 4π) : **elle conserve les
aires** — une dalle occupe sur la boule la place qu'elle occupe sur la Toile. ⚠ Aucune
projection ne conserve *aussi* les formes (Gauss) : vers le limbe les cellules s'étirent.
C'est ce que fait une image collée sur une balle.

### TROIS BUGS PAYÉS
- **Le point de fuite tombait sur la face visible.** Lambert n'a pas de défaut à son centre,
  elle en a un à **l'antipode**, où toute la Toile se rassemble en un point. Centrée sur
  `(0,0,1)` alors que la vue regarde ailleurs : un tourbillon en plein milieu. On la centre
  sur la direction de la vue — le défaut passe derrière, où rien n'est peint.
- **Le semis était encore dimensionné pour des dalles trouées.** On semait à l'inverse du
  remplissage (400 000 à 800 000 candidats) parce que la plupart tombaient dans le vide. Or
  la Toile enroulée couvre **tout** : chaque candidat peint. **531 000 touffes, 67,6 ms.**
- **La boule sortait plus sombre que la Toile qu'elle enroule** — le gros des poils
  atterrissait dans la moitié basse de la rampe. Recentré.

### CE QUE ÇA COÛTE — et c'est enfin dans le budget
```
                   avant ce lot   apres, 155k touffes   apres, 330k (livre)
hero     cadre 620     28,4 ms          11,7 ms              22,0 ms
m-gravure cadre 470    67,6 ms          10,6 ms              20,1 ms
```
On a repris la moitié du budget gagné **en définition** : à 155 000 touffes de 3,7 px la
couverture n'était que de 3,8 fois et le poil étalait sa couleur sur un carreau de 11 px.
À 330 000 touffes de 3,1 px, la couverture est de onze fois et un poil vaut un quart de carreau.

### CE QUI N'EST PAS FAIT, ET JE NE LE MAQUILLE PAS
- **La boule reste plus sombre et moins saturée que la Toile source.** La moyenne d'un pelage
  éteint toujours un peu ce qu'il recouvre. C'est le chapitre « lumière », pas encore ouvert.
- **La fourrure est devenue un velours ras** (3,1 px). C'est le prix du dessin exact : un poil
  plus long étale la couleur de sa racine et brouille un carreau de 11 px. Le compromis est
  réglable d'un chiffre, et c'est un arbitrage produit.
- 22 ms au grand cadre : au-dessus des 16,5 ms du plafond, à re-mesurer à la taille de l'app.
- `toilePleine` sème avec `Math.random` : **la Toile enroulée n'est pas déterministe** entre
  deux ouvertures. Dans l'app ce sera la Toile de l'utilisateur, donc la question ne se pose
  pas de la même façon — mais sur la planche, si.

---

## ⚑ LOT 10 · UNE SEULE GRILLE POUR TOUTE LA BOULE — la Toile, enfin · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/orbite-lot10/`

### CE QUE TOM A MONTRÉ
Une sphère `mosaique`, et : *« tu vois bien que tu ne prends pas des vrais designs de dalles
avec l'espace de la Toile. Tant que tu ne fais pas le reflet d'une Toile en fluffy, c'est mort. »*
**Deux fautes, toutes deux structurelles.**

### ⚑ 1 · CHAQUE CELLULE REDÉMARRAIT SA GRILLE À ZÉRO
Les trames du moteur sont ancrées sur des coordonnées **absolues** — pois tous les 9,
tesselles tous les 11, carrés tous les 5, sillons tous les 6. Sur la Toile il n'y a donc
**qu'une seule grille pour tout le canevas**, et une frontière de dalle n'est qu'un
**changement de couleur dessus**.
En peignant chaque cellule dans son propre canevas, la grille repartait de l'origine de ce
canevas : les carreaux ne tombaient plus en face d'une cellule à l'autre, et **le raccord se
voyait partout**. `dalleGeneree` prend maintenant une **phase**, et décale son origine d'un
multiple de la période — l'idiome que `dalleTrame` portait déjà.
**La phase globale** se prend dans une paramétrisation dont le gradient suit le repère tangent
commun (est / nord) : `longitude × cos(latitude)` vers l'est, `latitude` vers le nord.
⚠ Aucune paramétrisation ne peut être exacte partout — **c'est Gauss, la sphère n'est pas
développable.** Elle l'est **au premier ordre entre deux cellules voisines**, et c'est tout ce
qu'il faut pour que le raccord ne se voie pas.

### ⚑ 2 · LE FILET NOIR N'EXISTE PAS SUR LA TOILE
On posait **0,017 rad** de joint, « comme entre deux dalles de la Toile ». Or **il n'y en a
aucun** : les cellules y sont jointives, et l'espace qu'on voit est **la gouttière de la trame
elle-même** (2 px sur 11 en mosaïque, le vide entre deux pois en braille). Ce joint ajoutait
**4,5 px de noir à l'écran autour de chaque dalle** — c'est lui qui faisait lire des plaques
séparées au lieu d'une Toile. Ramené à 0,0035 rad, un cheveu.

### CE QU'ON VOIT MAINTENANT
```
braille   une seule grille de pois sur toute la boule, la couleur change par dalle
pixel     des aplats jointifs a bord d'escalier, aucun vide entre eux
mosaique  une seule grille de carreaux, la gouttiere du motif pour seul espace
sillons   des ondes continues d'un bout a l'autre
gravure   l'angle propre de chaque dalle — c'est le moteur qui le veut (`s.ang`)
```

### CE QUE ÇA COÛTE
```
hero      cadre 620   15,9 ms      m-encre   cadre 470   13,0 ms
m-pixel   cadre 470   28,4 ms      m-gravure cadre 470   28,0 ms
```
`pixel` et `gravure` sont les plus chers : leurs cellules sont désormais **pleines de matière
sur toute la boule**, il n'y a plus de vide à ne pas peindre. C'est le prix du dessin complet,
et il n'est pas encore rentré dans le budget des 60 im/s à la taille de l'app.

### CE QUI N'EST PAS FAIT
- **Le coût de `pixel` et `gravure` (28 ms) est au-dessus du budget.** À traiter.
- `encre` et `touffe` restent les mondes les plus clairsemés — leur nature sur la Toile aussi.
- La lumière et les couleurs d'ensemble : toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 9 · UNE DALLE PAR CELLULE — le dernier « à peu près » saute · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/orbite-lot9/`

### LE DÉFAUT QUI RESTAIT, ET IL ÉTAIT SIMPLE À NOMMER
**Vingt dalles pour soixante-dix-sept cellules.** Chaque forme revenait quatre fois, et
**aucune n'était la cellule qu'elle occupait** : on posait une dalle étrangère, mise à
l'échelle, dans un contour qui n'était pas le sien. Désormais le moteur peint, **pour chaque
cellule, une dalle dans le contour exact de cette cellule-là**. Plus de répétition, plus de
mise à l'échelle par cellule, plus de contour d'emprunt.

### ⚠ LA CELLULE NE SE DEVINE PAS, ELLE SE MESURE
L'attribution du semis est `acos(p·s) − w` : **ce n'est pas un Voronoï ordinaire**, et un
polygone reconstruit sans les poids rate le bord de **12 % du rayon**. On lance donc 24 rayons
depuis la graine et on cherche par dichotomie l'angle où l'attribution **bascule**. C'est la
vraie frontière, celle que la fourrure utilise. (`_p_semis.js` publie ses poids pour ça.)

### TROIS BUGS PAYÉS, TOUS MESURÉS AU COMPTEUR DE TOUFFES PEINTES
- **Pixels CSS contre pixels réels.** `dalleGeneree` rend un canevas de `dw × DPR` : un radian
  y vaut `PXR × DPR` pixels. Sans ce facteur l'échantillon tombait deux fois trop loin, hors
  de la dalle — **100 000 touffes peintes → 9 500**.
- **L'espacement pris sur la Toile de l'app, pas sur la cellule.** Les trois mondes libres
  dimensionnent leur marque sur `sp` ; en lui laissant 59 px alors qu'une cellule de sphère en
  fait 45, les lobes débordaient si loin que les voisines les recouvraient — **146 000 → 8 800**.
- **La graine cible peinte EN PREMIER.** `Renc`, `Rterr` et `Rtouf` peignent graine par graine
  et la dernière recouvre : toutes les voisines passaient donc par-dessus la cible. Sur la
  Toile, une graine est **au milieu** de la liste. Remise à sa place : encre **46 000 → 68 900**,
  touffe **31 700 → 59 100**, terrazzo **61 500 → 91 500**.

### CE QUE ÇA COÛTE — encore un gain
```
                    lot 6      lot 8      ce lot
hero      cadre 620  22,8 ms   19,4 ms    15,4 ms
m-encre   cadre 470  18,7 ms   15,7 ms    12,5 ms
```
(`m-pixel` et `m-gravure` remontent à ~25 ms : leurs cellules sont désormais pleines de
matière sur toute la boule, donc il y a plus à peindre. C'est le prix du dessin complet.)
Le coût de **construction** monte, lui : 77 dalles générées par monde, deux rendus chacune.

### CE QUI N'EST PAS FAIT
- **`encre` et `touffe` restent les mondes les plus clairsemés** — c'est leur nature sur la
  Toile aussi, mais sur une sphère ça se voit plus.
- La lumière et les couleurs d'ensemble : toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 8 · LA TOILE, EN SPHÈRE — le vrai dessin, à 100 % · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié avant et après).
> Planche : **`PLANCHE-PAVAGE.html`** · Sauvegarde : `sauvegardes/orbite-lot8/`

### CE QUE TOM A DIT
> *« mets des vrais designs de dalles. Là c'est des formes à peu près ressemblantes si on les
> connaît, mais c'est 10 % du vrai design, on veut 100 %. Ne livre pas si ce n'est pas ça. »*

Le générateur du lot 7 était fidèle (±4,5 points, mesuré). **La perte était dans le peintre**,
et il y en avait quatre.

### LES QUATRE PERTES, ET CE QU'ON A MESURÉ À CHAQUE FOIS

**1 · Le peintre JETAIT les vraies couleurs.** Il ne gardait qu'un écart de clarté reporté sur
la couleur de la *cellule*. Tout ce que le dessin a de propre disparaissait : le liseré crème
et le cœur orange d'une fleur de `touffe`, les recouvrements de lobes d'une `encre`, les
éclats d'un `terrazzo`, le liant d'une `mosaique`. `bat_trames` relevait pourtant déjà les
**96 teintes réellement peintes** du monde. On bâtit la rampe sur celles-là : **chaque poil
porte exactement la couleur que le moteur a posée sous sa racine.**

**2 · Toutes les cellules d'un monde à trame prenaient LA MÊME dalle-source** (celle au plus
grand rectangle inscrit) — c'était possible tant que la couleur venait de la cellule. Avec la
vraie couleur, ça rendait la sphère monochrome. Chaque cellule retire sa propre dalle.

**3 · Le contour venait du PAVAGE, pas de la dalle.** Les cinq trames lisaient leur *rectangle
inscrit* en rabattant l'échantillon sur son bord : la silhouette était un polygone sphérique
et le motif un bout d'intérieur recadré. **C'était ça, « à peu près ressemblant ».**
⚠ Ce correctif avait déjà été tenté au lot 5 et **retiré**, parce qu'il vidait la sphère.
Il est tenable **maintenant, et seulement maintenant**, parce que les cellules non plantées
portent le gris de la Toile : la boule reste pleine pendant que chaque dalle retrouve son bord.

**4 · L'échelle venait de la BOÎTE DU DESSIN, pas de la cellule.** Une dalle de `touffe` a des
tiges qui descendent d'une demi-cellule : sa boîte vaut le double de sa cellule, et caler
cette boîte-là divisait ses fleurs par deux — elles sortaient en mouchetis. On transporte donc
**le polygone et la graine** avec la dalle, et c'est d'eux que vient l'échelle.

**5 · Une cellule vide perdait le dessin.** Peinte en gris uni, elle n'avait plus ni liseré ni
cœur, et les trois quarts de la boule étaient nus. Sur la Toile, une cellule sans Promi porte
**exactement la même trame, seulement sombre**. Elle la porte maintenant.

### ⚠ UNE ERREUR QUE J'AI FAITE, ET CORRIGÉE PAR LA MESURE
J'ai d'abord accusé le **grossissement** de la trame (`mag` 2,7) d'être la cause du « 10 % ».
Je l'ai ramené à 1 — et **la grille de mosaïque a disparu** : à pas réel, une cellule montre
une vingtaine de carreaux là où la Toile en montre 5 à 7, et le motif devient du bruit. **Le
grossissement était juste ; c'est le contour qui ne l'était pas.** Remis à 2,7.

### CE QUE ÇA COÛTE — et c'est un GAIN
```
                    AVANT (lot 6)   APRES (ce lot)
hero      cadre 620     22,8 ms        19,4 ms
m-encre   cadre 470     18,7 ms        15,7 ms
m-pixel   cadre 470     25,7 ms        20,9 ms
m-gravure cadre 470     17,5 ms        18,9 ms
```
Les poils ont raccourci (le tiers du pas lu) et couvrent moins de pixels chacun.

### CE QUI N'EST PAS FAIT
- **`touffe` reste le monde le plus maigre.** Ce n'est pas un défaut du portage : sa dalle
  couvre 11 % de sa cellule sur la Toile aussi. Mais sur une sphère ça se voit plus.
- La lumière et les couleurs d'ensemble ne sont toujours pas traitées.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 7 · LE MOTEUR GÉNÈRE LA DALLE — plus aucun prélèvement · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié avant et après).
> Ajout dans **`scratchpad/toile-extrait.js`** (la COPIE du moteur, jamais l'app) :
> `Toile.dalleGeneree`. Rien n'y est réécrit — c'est un ajout.
> Sauvegarde : `sauvegardes/orbite-lot7/`

### CE QUE TOM A DEMANDÉ
> *« mets les VRAIES dalles aux vrais designs, contours, variations de teintes, pas
> superposées, pas des photos de la Toile détourées encadrées ça jamais — tu as le code de la
> Toile qui génère des dalles donc fais les vraies »*

Il a raison sur le fond : **tout ce qu'on avait PRÉLEVAIT dans une Toile déjà peinte.**
`dalleTrame` coupe les marques en deux ; l'extraction par la couleur rendait des marques
entières mais restait un tri dans une image.

### ⚑ LA CLÉ — ON FABRIQUE LA CELLULE AVEC DES GRAINES, PAS AVEC UN DÉCOUPAGE
La cellule d'une graine est l'intersection des demi-plans de ses bissectrices. Donc, **pour
qu'une graine ait exactement le polygone voulu, il suffit de poser une voisine EN MIROIR de
chaque côté** : la bissectrice entre les deux *est* ce côté. Le moteur décide alors lui-même,
avec sa propre règle, quelle marque appartient à qui — et **une marque reste entière**.
Vérifié numériquement (`scratchpad/probe_poly.py`) : les cellules sont **convexes**, et
**100 %** des points du polygone ont bien la graine cible pour plus proche, sur huit cellules.

### ⚑ ET LA DALLE SE SÉPARE DE SON FOND PAR DIFFÉRENCE DE DEUX RENDUS
Dernier prélèvement supprimé. On peint **deux fois le même jeu de graines, au même instant**,
et on ne change **qu'une** chose : la graine cible redevient grise. Tout ce qui diffère
appartient à cette dalle — **son liseré d'encre et son cœur orange compris**. C'est ce qui
règle `touffe`, dont une fleur porte trois couleurs et que tout tri par teinte mutilait.
⚠ Il faut le **même** jeu de graines (`mk()` tire au sort gray/tone/shade/ang/ph) et le
**même** instant (`cOf` dépend de `now`), sinon la différence est du bruit.

### ⚑ ET L'ESPACEMENT DE LA TOILE, POUR LES TROIS MONDES LIBRES
`Renc`, `Rterr`, `Rtouf` dimensionnent leur marque sur `sp = √(W·H / nb de graines)`. Dans un
canevas de dalle, ni `W·H` ni le nombre de graines n'ont à voir avec ceux de la Toile : les
marques sortaient **beaucoup** trop petites. On truque `W` et `H` pour que `sp` retrouve sa
valeur — l'idiome que `dalleTrame` porte déjà. ⚠ **Uniquement pour eux** : `Rpix` et `Rmos`
*bouclent* sur `W` et `H`.

### LA PREUVE, MESURÉE (`scratchpad/probe_gen2.py`)
Part de matière **dans la même cellule**, sur la Toile / générée, **critère identique des deux
côtés** (une première mesure comparait « la couleur exacte de la dalle » d'un côté et « tout ce
qui est coloré » de l'autre : elle mentait de 20 points sur `touffe`).
```
encre    -4,5      mosaique +0,7     touffe   -3,8     braille  -2,6
pixel    -2,1      terrazzo +3,7     gravure  +1,4     sillons  -0,2
```
**Les huit mondes à ±4,5 points.** Et chaque dalle sort **seule, sur fond transparent** :
rien ne se superpose.

### LES BATTERIES — toutes vertes, `app.html` non modifié
```
redteam_ecrans 150/150 · redteam 15/15 · redteam2 10/10 · redteam3 18/18
redteam_demande 19/19 · redteam_toile 17/17 · redteam_geste 13/13 · redteam_verbe 6/6
redteam_filets 0 parasite · redteam_vide 61/61 · redteam_air 428 paires intactes
redteam_champ 32/32 · redteam_polices 0 couple absent
releve-design : AUCUN ECART
```

### CE QUI N'EST PAS FAIT
- La sphère reste **sombre**. La lumière et les couleurs ne sont pas traitées.
- Le coût par image n'a pas été re-mesuré après ce lot (la génération est un coût de
  CONSTRUCTION, pas de rendu — mais ce n'est pas vérifié).
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit).

---

## ⚑ LOT 6 · UNE BOULE QU'ON A ENVIE D'ÉCRASER · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · modules `_p_{peint,moteur,planche}.js`
> Sauvegardes : `sauvegardes/orbite-lot6/` (avant) · `orbite-lot6-livre/` (après)

### QUATRE CHOSES BRIDAIENT LE FLUFFY, ET DEUX ÉTAIENT ÉCRITES DANS LE CODE

**1 · Le poil RACCOURCISSAIT au bord de sa cellule** — deux crans, avec le commentaire
*« et le contour reste net : à pleine taille il déborde et rend la dalle floue »*. Mais un
bord net, c'est exactement ce qui fait une découpe. **Une fourrure se lit surtout au bord**,
quand les mèches passent par-dessus le vide. On garde la pleine longueur jusqu'au filet et on
ne raccourcit plus qu'au tout dernier rang — juste assez pour que le vide reste lisible.

**2 · Des brins, pas des mèches.** `TAI0` passe de `[4,2 · 5,6 · 7,2]` à `[5,6 · 7,5 · 9,7]`,
et le brin lui-même de `1,75·e` à `2,05·e` avec **un quart de courbure en plus** : les pointes
se rabattent et se croisent, et c'est ce croisement qui fait « mou » à l'œil.

**3 · Les grands vides noirs n'étaient PAS le joint.** Le joint vaut 0,017 rad, soit ~4,5 px à
l'écran ; les vides faisaient 20 à 40 px. C'étaient **les cellules non plantées, qui ne
peignaient rien**. Or l'audit §2 rejette déjà *« une majorité de cellules vides : la silhouette
se creuse, ce n'est plus une boule »* — et la vraie Toile ne fait pas ça : ses cellules sans
Promi sont **sombres mais pleines de matière**. On ajoute donc une teinte à la rampe — le gris
de la Toile — et les cellules vides la portent, **avec leur trame**. La boule redevient
continue et ronde ; le joint reste le seul vide.

**4 · Moins de touffes, puisqu'elles couvrent plus.** 155 000 → 118 000. C'est **la longueur
qui fait la masse, pas le nombre.**

### CE QUE ÇA COÛTE — MESURÉ, PAS ESTIMÉ (`scratchpad/cap_ms.py`, sphère en rotation)
```
                        AVANT      APRES brut   APRES avec le sol allege
hero      cadre 620      22,8 ms     36,7 ms      28,9 ms
m-encre   cadre 470      18,7 ms     28,5 ms      22,4 ms
m-pixel   cadre 470      25,7 ms     38,0 ms      30,8 ms
m-gravure cadre 470      17,5 ms     35,0 ms      28,4 ms
```
Le sol gris se paie : il a fait passer l'image de 22,8 à 36,7 ms. Comme il est **sombre et
sans motif à lire**, il n'a besoin ni de la densité d'une dalle ni de sa longueur : **une
racine sur deux, et un cran plus court**. On récupère les deux tiers du surcoût.

> ### ⚠ ET LE COÛT NE DÉPEND PRESQUE PAS DE LA TAILLE DU CADRE
> Un cadre de 470 px coûte parfois **plus** qu'un de 620 (`m-pixel` 30,8 contre `hero` 28,9).
> Ce n'est pas une anomalie : **c'est le nombre de touffes qui domine, pas les pixels** — le
> banc le disait déjà (*« un poil coûte 0,108 µs dont seulement 0,042 de pixels »*). Corollaire
> qui invalide un raccourci tentant : **on ne peut PAS extrapoler le coût à 390 px en divisant
> par le rapport des surfaces.** Il faudra le mesurer à 390.

### CE QUE JE NE MAQUILLE PAS
- **Le lot coûte +27 % par image** (22,8 → 28,9 sur le grand cadre). C'est le prix du fluffy
  demandé ; ce n'est pas gratuit et je ne le présente pas comme tel.
- **Les 60 images par seconde ne sont PAS vérifiées à la taille de l'app.** Les plafonds de
  l'audit §5 ont été mesurés à 390 px avec un autre grain : ils ne couvrent plus cet état.
- La sphère reste **sombre**. « Belle lumière générale, belles couleurs » n'est toujours pas
  traité — c'est le prochain sujet.
- Ni le limbe, ni le partage, ni la question des six (§7 de l'audit) ne sont revus.

---

## ⚑ LOT 5 · LES VRAIES DALLES DANS LA FOURRURE — et un correctif que j'ai dû retirer · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** (celle de la fourrure, revenue en service)
> Modules touchés : `scratchpad/_f_dalle.js`, `_p_trame.js` · `_p_peint.js` **rétabli à l'identique**
> Sauvegardes : `sauvegardes/orbite-lot5/` (avant) · `sauvegardes/orbite-lot5-livre/` (après)

### ⚠ CE QUE J'AI CASSÉ, ET POURQUOI JE LE NOTE EN PREMIER
Tom a envoyé **deux** images : un gros plan d'une dalle `pixel` au bord sale, et une sphère
`touffe` — en disant *« t'es hyper loin de là où on en était en terme de fluffy, c'est une
grosse régression »*.
**J'ai cru que la première visait la silhouette de la sphère.** Elle visait le **bord de la
dalle plate**. J'ai donc changé `_p_peint.js` pour que la silhouette d'une cellule vienne de
la dalle et non du pavage. Résultat mesuré, avant/après au même cadre : la sphère `touffe`
est passée d'une boule fournie à **des lambeaux** — une trame est vide à 60-80 %, donc la
fourrure ne poussait plus que sur un quart de la surface.
**`_p_peint.js` est rétabli à l'identique depuis la sauvegarde.** Rien de ce correctif ne
subsiste. *(Une tentative de compensation par « silhouette fermée + trou de trame plus
sombre » est également retirée : elle rendait la masse mais éteignait la boule.)*
> **Leçon, et elle est générale :** quand une capture montre un défaut, **identifier l'écran
> d'où elle vient avant de corriger**. J'ai corrigé la sphère pour un défaut de la planche plate.

### CE QUI EST LIVRÉ, ET QUI EST PROUVÉ
**1 · La source des dalles ne passe plus par `dalleTrame`.** Elle coupe les marques en deux
(mesuré, `scratchpad/verite.html`) : demi-points de braille, demi-carreaux de mosaïque, et
l'escalier de `pixel` remplacé par un polygone lisse. `_p_trame.js` prend maintenant
**`DallesDeMonde()`** : marques entières, bord net.

**2 · Sans attendre, et sans toucher à l'app.** `Toile.preview(cv,monde,w,h)` peint
**synchroniquement** (elle appelle `RD[theme]` en ligne) et publie ses graines dans `cv.__c`.
Prélever sur la Toile vivante aurait imposé d'attendre la frame suivante — or `bat_trames`
est synchrone : on aurait lu **l'ancien monde**, sans la moindre erreur. C'est le piège du §8,
en pire. `agrandit()` n'est plus appelée : on ne redimensionne plus la Toile de l'app.

**3 · Le bord se lit par PROJECTION, plus par une bande de tolérance.** La bande gardait, à
alpha partiel, les pixels d'antialiasing **du voisin** — d'où le liseré mauve sale le long de
l'escalier, exactement ce que Tom a montré. Un pixel de bord est un **mélange** entre la
couleur de la dalle et le fond : on projette sur le segment `[fond → dalle]`, la part donne
l'alpha, et **le reste dit avec quoi le mélange se faisait**. Mélangé à une autre dalle, le
reste est élevé : rejeté, net. Vérifié à la loupe ×8 sur pixel, mosaïque et braille.

**4 · Les mondes LIBRE gardent tout ce qui n'est pas le fond.** Une fleur de `touffe` porte
**trois** couleurs (pétale, liseré d'encre, cœur orange) : triée par teinte, elle perd son
contour et son cœur — mesuré, la sphère `touffe` maigrissait. Pour encre, terrazzo et touffe
on garde donc tout ce qui n'est pas le fond, et **la graine la plus proche** dit à qui la
marque appartient — la règle du moteur.

### CE QUE JE NE MAQUILLE PAS
- **Le fluffy est REVENU à son niveau, il n'a pas augmenté.** Avant/après au même cadre :
  équivalent sur les huit mondes. Ce lot corrige la matière source, il n'ajoute pas de fourrure.
- La sphère reste sombre. « Belle lumière générale, belles couleurs » n'est pas traité ici.
- Ni limbe, ni doigt, ni les six ne sont revus.

---

## ⚑ LOT 4 · LE POLYGONE COUPAIT LES MARQUES EN DEUX — les vraies dalles, mesurées · 9 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · sonde : **`scratchpad/verite.html`**
> Modules : `scratchpad/_f_dalle.js` (neuf) · `_f_planche.js` (réécrit)
> Sauvegarde : `sauvegardes/dalles-lot4/`

### CE QUE TOM A DIT
> *« le velours ça marche pas, et c'est encore des screenshots de dalles dans un cadre.
> Tu en mets dans encre et touffe je crois (pas sûr) mais tous les autres c'est archi faux. »*

**Il avait raison, et sur les huit mondes exactement.** Je ne l'ai pas pris à l'estime : j'ai
construit une sonde (`scratchpad/verite.html`) qui confronte, monde par monde, la dalle que je
sortais à **la même dalle prélevée sur la Toile peinte**.

### LE MÉCANISME, MESURÉ
```
encre · touffe · terrazzo    elles coincident.     (les mondes LIBRE du moteur)
mosaique · braille · pixel   elles ne coincident PAS,
gravure · sillons            et toujours de la meme facon.
```
`dalleTrame` refait l'attribution **pixel par pixel** et efface l'alpha des pixels hors
cellule. Il **coupe donc les marques en deux** : demi-points de braille, demi-carreaux de
mosaïque, hachures tranchées net. Et sur `pixel`, **l'escalier de 5 px — la signature du
monde — disparaît** au profit d'un polygone lisse.
Sur la vraie Toile c'est l'inverse : chaque marque appartient à **une** graine et se peint
**entière**. Le bord d'une dalle y est **quantifié par la trame**, jamais lisse.
**C'était ça, « la capture dans un cadre » : le cadre, c'était ce polygone.**

### LA CORRECTION — ON N'EXTRAIT PLUS PAR LA FORME, MAIS PAR L'APPARTENANCE
Le moteur peint la Toile entière, correctement. On y prélève la dalle par **sa couleur** :
le moteur garantit qu'une dalle colorée n'a jamais la couleur d'une voisine (`cc()` écarte
les couleurs des voisines, `tones()` leurs marches de clarté), donc sa teinte est **unique
dans son voisinage**. On garde ses pixels dans la cellule élargie d'une demi-période de
trame — et **les marques restent entières, coupées exactement où le moteur les a coupées**.
```
aucun redimensionnement · aucun deplacement · aucun redessin · echelle 1, pixel pour pixel
```
⚠ Ce n'est **pas** le rejet capital de l'audit §2 : celui-là vise le fait de prendre l'**image**
d'une dalle pour **découper une autre forme**. Ici on ne découpe rien — on garde ce que le
moteur a peint, tel qu'il l'a peint.

### POURQUOI DEUX CHEMINS, ET PAS UN SEUL
L'extraction par la couleur ne sait garder qu'**une** couleur. Or une marque de `touffe` en
porte **trois** : le pétale à la couleur de la dalle, le liseré à l'encre, le cœur orange.
Prélevée par la couleur, la fleur perd son contour et son cœur — **mesuré** : pétales nus,
ou cœurs orange sans pétales. Ce sont exactement les mondes que le moteur appelle **LIBRE**
(encre, terrazzo, touffe) : ceux dont la marque **déborde** de sa cellule et a donc une forme
propre. Pour eux `dalleTrame` est déjà juste, c'est mesuré. La règle reprend donc **la
distinction que le moteur fait déjà** :
```
LIBRE  encre · terrazzo · touffe                 ->  Toile.dalleTrame  (deja juste)
TRAME  mosaique · braille · pixel · gravure ·    ->  extraction par appartenance
       sillons
```

### LE VELOURS EST RETIRÉ
> *« le velours ça marche pas »*

Supprimé de la planche. `_f_velours.js` est conservé mais **seul `Velours.jour()` reste
utilisé** — la lumière générale, montrée sur sa propre colonne pour qu'elle se refuse d'un
coup d'œil. Les quatre lots de traitement de surface (effilochage, ombre portée, relief,
halo grignoté) sont archivés dans `sauvegardes/fibre-lot{1,2,3}/`.

### CE QUI N'EST PAS FAIT
- **La sphère n'existe toujours pas.** Ni limbe, ni doigt, ni les six.
- Sur la Toile les cellules sont **jointives** : le vide entre dalles (exigence 4) viendra du
  recul des plans bissecteurs sur la sphère, pas d'ici.
- **La matière reste à trouver.** Trois pistes ont été essayées et rejetées par Tom : le brin
  dessiné (cheap), le traitement de surface (détourage), le halo (néon). Ce qui est acquis,
  c'est **ce qu'on ne peut pas faire** : déplacer un pixel de la dalle, l'éclaircir vers le
  blanc, ou lui poser quoi que ce soit d'uniforme.
- L'extraction lit les pixels de la Toile : elle exige que le monde soit **peint** avant
  (setTheme + ~1,5 s). Pour la sphère il faudra un chemin qui ne dépende pas de ce délai.

---

## ⚑ LOT 3 · ON NE DÉPLACE JAMAIS UN PIXEL DE LA DALLE · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · module `scratchpad/_f_velours.js`
> Sauvegarde : `sauvegardes/fibre-lot3/`

### CE QUE TOM A REJETÉ
> *« pas des photos détourées dégueulasses, abandonne et plus jamais ça »*

**Trois gestes du lot 2 fabriquaient ce détourage**, et ils sont supprimés :
1. **L'effilochage.** Il prélevait la couleur à une position **déplacée**. Le contour du
   moteur — net, calculé, exact — en sortait **rongé** : bords mordus, irréguliers, sales.
   C'est littéralement l'aspect d'un mauvais détourage.
2. **L'ombre portée.** Une copie sombre décalée sous la matière fait un **autocollant** posé
   sur le fond, jamais une matière.
3. **Le relief à forte amplitude.** Une pente à 0,78 pose un liseré clair d'un côté, sombre
   de l'autre : encore un contour sale.

### ⚑ LA RÈGLE QUI EN SORT, ET ELLE NE SE NÉGOCIE PLUS
**ON NE DÉPLACE JAMAIS UN PIXEL DE LA DALLE.** Le moteur a calculé ce contour : il est la
vérité. Tout ce qu'on ajoute se met **AUTOUR**, ou module la **CLARTÉ** — jamais la forme.

### LE MONTAGE
```
1 · LE DUVET, AUTOUR       deux halos flous de la dalle, poses DESSOUS. Ils
                           debordent du contour : c'est ce debord qui fait le
                           coton. Le dessin, dessus, reste intact — « fluffy,
                           mais que ca reste lisible ».
2 · LE HALO SE GRIGNOTE    un flou gaussien est UNIFORME : sur fond sombre il
                           ne peut faire qu'une aureole — l'outer glow, la
                           signature du toc. On troue son alpha par un bruit
                           etire dans le sens du poil : chaque meche atteint
                           une distance differente, et il reste du VIDE entre.
3 · LE GALBE               une rondeur douce par marque, lue sur un alpha
                           floute. Sur l'alpha brut la pente vaut 255 sur deux
                           pixels : ca fait un lisere blanc, pas une rondeur.
4 · LA LUMIERE EST A LA SCENE, PAS A LA DALLE
                           posee par dalle, elle se repete a l'identique sur
                           chacune et rien ne se tient. Une seule lumiere
                           traverse toute la composition : `Velours.jour()`,
                           appliquee APRES montage. Plus une montee de
                           saturation qui ne touche pas la teinte.
```
Deux réglages ramenés à zéro parce qu'ils faisaient un néon : le duvet ne s'éclaircit
**plus du tout** (`lift = 0`) — c'est sa **découpe** qui dit la fibre, jamais sa clarté.

### UN MORCEAU DE TOILE — c'est là que la lumière se juge
La planche compose un vrai morceau : les vraies dalles du moteur, à leur place, **le vide
entre elles** (exigence 4), une seule lumière par-dessus. C'est le montage qu'aura l'Orbite.
⚠ **Ce qui est approché là, et rien d'autre : la POSITION.** `dalleTrame` recadre au plus
juste et n'expose pas son décalage ; on centre donc chaque dalle sur le centre de sa cellule
(`dalleAbs`). La dalle elle-même — forme, trame, couleurs — est celle du moteur, au pixel.
Une **loupe** est toujours au plus proche, jamais un raster agrandi et lissé.

### CE QUI N'EST PAS FAIT
- **La sphère n'existe toujours pas.** La « belle lumière générale » ne se jugera vraiment
  que sur elle : ici elle est plate.
- Le coût par image n'est pas mesuré. La passe est **par pixel** (deux flous + deux boucles),
  donc les plafonds de l'audit §5, comptés en touffes, **ne s'appliquent pas** — banc à refaire.
- Les mondes creux (gravure, sillons, braille, terrazzo) laissent beaucoup de vide : la
  silhouette de la sphère devra se garantir **au limbe**, ce n'est pas éprouvé.

---

## ⚑ LOT 2 · LA VRAIE DALLE, EN VELOURS — le brin est abandonné · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · module `scratchpad/_f_velours.js`
> Sauvegardes : `sauvegardes/fibre-lot2/` (état livré) · `sauvegardes/fibre-lot1/` (les brins)

### CE QUE TOM A DIT, ET POURQUOI SES DEUX REPROCHES N'EN FONT QU'UN
> *« les poils donnent pas envie de caresser, ça fait cheap visuellement »*
> *« ça doit être les VRAIES dalles »*

En redessinant chaque monde en fibres, le lot 1 produisait **huit approximations** — braille
en étoiles au lieu de points, mosaïque en briques décalées au lieu d'une grille, gravure en
fougères au lieu de hachures, pixel sans son escalier. Et pour que le motif survive, il
fallait des brins **assez gros pour se voir un par un** : c'est précisément ce qui fait cheap.
**À cette échelle, une vraie soie ne montre aucun poil.** Les deux reproches ont la même cause.

### LE RENVERSEMENT
```
1 · LE MOTEUR PEINT LA VRAIE DALLE   Toile.dalleTrame(cv,pid,1,{m,p,h})
    vraie trame, vrai pas, vraie couleur, vraies strates, vraie cellule ponderee.
    Aucune approximation n'est POSSIBLE : c'est lui. On ne redessine plus rien.
2 · LA MATIERE EST UN TRAITEMENT DE SURFACE, jamais un poil trace
    · l'effilochage du bord, anisotrope, a la plus fine periode representable
    · le grain couche dans le sens du peignage
    · les plages claires et sombres du velours froisse
    · le RELIEF de chaque marque, lu sur un alpha floute
    · l'ombre portee, pour que la matiere ne soit pas collee au fond
```
**Aucun brin n'est jamais tracé — on ne peut donc plus en distinguer un.**

⚠ **Ce n'est pas le rejet capital de l'audit §2.** Ce qui est abandonné à tout jamais, c'est
de prendre l'**image** d'une dalle pour **découper une autre forme** — des fausses dalles
détourées. Ici la dalle n'est ni redimensionnée, ni détourée, ni déplacée : le moteur la peint
dans **sa** cellule, et on ne touche qu'à la surface. Le contour reste celui qu'il a calculé.

### LA PREUVE QUE CE SONT LES VRAIES DALLES (`scratchpad/probe_dalle.py`)
Le taux de remplissage rendu par `dalleTrame`, comparé au relevé de référence `pav/_trames.png` :
```
                rendu        reference
encre    65 %          67-73 %
pixel    63 %          50-73 %
terrazzo 60 %          37-54 %
touffe   43 %          35-51 %
mosaique 42 %          34-49 %
braille  27 %          21-32 %
sillons  27 %          21-30 %
gravure  25 %          21-29 %
```

### LES CINQ DÉFAUTS PAYÉS DANS CE LOT, ET LEUR CAUSE RÉELLE
- **Le treillis gaufré** (encre, pixel). Ce n'était pas la grille du bruit de valeur : c'était
  un **repliement de spectre**. J'avais ajouté deux octaves *plus hautes* pour casser le
  réseau ; à ×4,41 en travers leur période tombait à 0,26 px de cellule, sous
  l'échantillonnage — et une fréquence qu'on ne peut pas représenter **se replie**, en moiré
  large. **La règle : la plus fine octave est celle du pixel, on casse le réseau PAR LE BAS.**
- **Toute la dalle assombrie de 17 %.** Le lustre venait du produit fibre·lumière. Le cône du
  peignage étant centré sur 0,33 rad et la lumière sur −2,15, ce produit valait −0,79
  **partout** : un assombrissement global sans la moindre variation. Les plages viennent
  maintenant d'un champ scalaire à part, centré sur 1.
- **Un filtre posé sur une forme plate.** Le grain était là, mais rien ne se soulevait. Il
  manquait **le relief** — la pente de la matière, éclairée d'un côté.
- **Le liseré blanc.** La pente lue sur l'alpha **brut** vaut 255 sur deux pixels : le bord
  sortait en liseré blanc et la couleur se lavait. On la lit sur un alpha **flouté** : la
  marque devient un bourrelet et la lumière la parcourt en entier.
- **Le terrazzo lavé.** Un plafond de clarté **en facteur** traite le lilas comme l'encre.
  Le plafond est maintenant **en niveau de canal** (242 sur le canal le plus haut) : aucun
  écrêtage, donc teinte et saturation exactes quelle que soit la couleur de la palette.
- **L'effilochage en paquets.** Un bruit isotrope de 1,8 px donne des touffes de 1,8 px de
  large : on lit des paquets, pas des fibres. Il est maintenant pris **dans le repère du
  peignage** — 1,1 px de cellule en travers (2,2 px réels, la plus fine période
  représentable), 3,5 px dans le sens.

### CE QUI N'EST PAS FAIT, ET CE QUE JE NE MAQUILLE PAS
- **Ça rend un feutre / un velours brodé, pas une fourrure longue.** C'est la conséquence
  directe du renversement : la fourrure longue exigeait des brins visibles, et les brins
  visibles sont ce que Tom a appelé cheap. **C'est un arbitrage à trancher, pas un réglage.**
- **La sphère n'existe toujours pas.** Planche plate. Ni limbe, ni doigt, ni les six.
- Le coût par image n'est pas mesuré sur une sphère animée : la passe est **par pixel**, pas
  par poil, donc les plafonds de l'audit §5 (comptés en touffes) **ne s'appliquent plus** —
  il faudra un nouveau banc.
- L'approche « un brin dessiné » est archivée dans `sauvegardes/fibre-lot1/` avec son module
  `_f_fibre.js`. Elle garde une chose juste : chaque monde SAIT donner une loi d'implantation.

---

## ⚑ LOT 1 · LA FIBRE EST LE TRAIT DU MONDE — le parti pris change · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-FIBRE.html`** · modules `scratchpad/_f_{fibre,planche}.js`
> Sauvegarde : `sauvegardes/fibre-lot1/`

### LE PARTI PRIS, EN UNE PHRASE
**On ne pose pas de fourrure SUR un dessin : on DESSINE AVEC la fourrure.** Chaque monde du
Studio ne donne plus une image à recouvrir, il donne une **loi d'implantation** — où une
touffe pousse, dans quel sens elle est peignée, quelle marche de clarté elle porte.

### CE QUE ÇA DÉBLOQUE
Le mur des dix derniers tours était une **collision d'échelles** : un poil fait 6 px, un motif
du moteur a un pas de 5 à 11 px. Poil plus petit, il ne se voit pas ; poil plus grand, il
écrase le motif. **Ici il n'y a plus deux grains** : le poil EST la marque du monde. Une
hachure de gravure n'est plus une ligne qu'on duvette — c'est une rangée de fibres couchées,
du **velours côtelé**. Le produit le pensait déjà : un des huit mondes s'appelle **touffe**,
et ses fleurs sont déjà des rosettes de fibres.

```
encre     peluche froissee     mosaique  tapisserie a carreaux
touffe    fleurs en faisceaux  braille   tapis a points (chenille)
pixel     peluche rase         terrazzo  velours froisse en plaques
gravure   velours cotele       sillons   soie moiree
```

Les pas viennent des peintres du moteur **à la lettre** (`Rpix` STEP 5, `Rbra` DOT 9, `Rsil`
SP 6 / AMP 4,5 / WL 0,018, `Rgra` HS 8, `Rmos` T 11, `Renc` 9 ellipses rayon 0,6·sp, `Rterr`
7 tessons, `Rtouf` 3-5 fleurs). Les strates sont `LITS=[0,0.10,0.04,0.14,0.07]`, la loi de
`PALL()`. **Rien n'est inventé : seule la marque change.**

### LES QUATRE DÉFAUTS PAYÉS DANS CE LOT, ET LEUR CAUSE RÉELLE

- **La bogue de châtaigne.** Pas 2,4 · longueur 6,5 · trois brins : un poil couvrait trois
  pas et **se lisait tout seul**. Une fourrure ne se lit jamais brin par brin. Pas 1,05,
  longueur 3,0, **cinq** brins serrés à 0,20 : le recouvrement fait le soyeux, pas la longueur.
- **La dalle plate et pâle** (encre, pixel, deux fois). La longueur d'onde du champ de
  peignage était réglée **à l'échelle de l'écran** : le champ ne tournait pas dans une cellule
  de 67 px, le lustre devenait constant, la dalle sortait en aplat lavé. **La longueur d'onde
  se compte en CELLULES** — ~2,5 tourbillons en travers d'une cellule.
- **Les araignées noires.** Ni un poil noir ni une ombre : **le FOND qui se voit**. Un champ
  de gradient a des points critiques ; la direction y fait un tour complet, les touffes
  s'éventent en rosette et laissent un trou. On ne les rattrape pas une par une : un **biais
  constant plus long que le gradient** (1,35 > 1) enferme la direction dans un cône de ±47°
  et le champ n'a plus de point critique.
- **La feuille d'érable** (touffe) et **le pâté** (terrazzo). Les pétales fondaient faute du
  liseré d'encre : le `_tfStroke(ink)` du moteur est rendu en **fibres crème posées en
  dernier**. Les sept tessons fondaient faute de gouttière : on les **rétrécit de 14 %** vers
  leur centre.

### CE QUI EST MESURÉ (`scratchpad/compte_fibre.py`, pas supposé)

```
touffes par cellule de 67 px     encre 2963 · pixel 3304 · touffe 2547 · mosaique 1978
                                 terrazzo 1269 · braille 924 · sillons 717 · gravure 508
                                 moyenne 1776
sur la sphere, 30 cellules de face (audit §5)
   monde moyen                    53 000 touffes   266 000 poils
   pire monde (pixel)             99 000 touffes   496 000 poils
   plafond mesure (audit §5)     125 000 touffes   500 000 poils a 16,5 ms
```
**Le pire monde tient, à la limite.** Rien n'a été remesuré : ce sont les plafonds de l'audit.

### CE QUI N'EST PAS FAIT — et je ne le maquille pas
- **La sphère n'existe pas dans ce lot.** C'est une planche PLATE : elle prouve la loi
  d'implantation, elle ne prouve ni la boule, ni le limbe, ni le doigt, ni les six.
- Le mariage avec `_q_cellule.js` (le vrai polygone sphérique) n'est pas fait.
- **Terrazzo, gravure, sillons et braille sont clairsemés** par la loi du moteur elle-même.
  Sur une sphère, la silhouette risque de se trouer. La parade acquise est **au limbe**
  (§6 de l'audit) — elle n'est pas encore éprouvée sur un monde creux.
- La question du §7 de l'audit (les six disques DEDANS ou DESSUS) reste **ouverte**.

---

## ⚑ L'AUDIT EST RÉÉCRIT — passation vers un chat neuf · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> **`AUDIT-ORBITE.md` est réécrit en entier** et fait foi. L'ancien est dans
> `sauvegardes/AUDIT-ORBITE-avant-8sept.md`.

**Ce que le nouvel audit ajoute par rapport à celui du 6 septembre :**

- **Un rejet capital et définitif** — on ne découpe plus jamais un raster de dalle pour en
  faire une forme. Avec **le signe qui permet de le reconnaître** : si un défaut résiste à
  trois corrections et qu'en le réparant un autre apparaît ailleurs, ce n'est pas un réglage,
  c'est l'architecture.
- **Ce que Tom demande, dans ses mots**, rassemblé des dix derniers échanges — y compris ce
  qu'il n'avait jamais eu à préciser (§3).
- **Seize bugs payés** au lieu de huit, dont quatre neufs et coûteux : `Toile_resize` lit le
  parent, le bouchon `cc()` doit rendre un index, le cache HTTP, la boucle de rejet du semis.
- **Dix règles de dessin** payées cher, écrites une par une (§6).
- **Les mesures**, avec **ce qui paie et ce qui ne paie rien** — pour qu'on ne refasse pas
  quatre optimisations sans effet (§5).
- **Ce que j'ai mal fait** (§9), pour que le prochain ne le refasse pas.
- **Le prompt de reprise** (§10), qui autorise explicitement à **repenser** l'approche.

**L'état livré :** la version avec les poils (`PLANCHE-PAVAGE.html`, modules `_p_*`) est en
service. La branche « le moteur peint lui-même » est écartée mais gardée entière dans
`sauvegardes/orbite-dalles-8sept/` — **son calcul du vrai polygone d'une cellule
(`_q_cellule.js`) est bon et doit être réutilisé.**

---

## ⚑ RETOUR À LA VERSION AVEC LES POILS · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> **La version en service est de nouveau `PLANCHE-PAVAGE.html`** (moteur `scratchpad/_p_*.js`).

**Décision Tom : on revient à la version avec les poils, avec ses erreurs.** Les cinq modules
`_p_*` n'avaient pas été touchés depuis la sauvegarde du 6 septembre — vérifié par `diff`,
**identiques octet pour octet** à `sauvegardes/orbite-6sept/`. Rien à reconstruire : la planche
est simplement re-horodatée et re-rendue.

```
77 cellules · 76 000 a 162 000 touffes selon le monde · les six et le Noyau en place
```

**La branche « le moteur peint lui-même »** (cellules en vrai polygone, dalle dessinée par
`Toile.dalleTrame`, fourrure par-dessus) est mise de côté **entière** dans
`sauvegardes/orbite-dalles-8sept/` — `PLANCHE-ORBITE-DALLES.html` + `_q_*.js`. Elle reste
servie et consultable ; elle n'est plus la version de travail.

**Ce qu'on garde de cette branche, même écartée** — et c'est écrit dans les mémoires du projet :
le contour d'une dalle **est** sa cellule de Voronoï ; le bouchon `cc()` doit rendre un **index**
de palette (c'est lui qui privait l'Orbite de ses couleurs) ; une tache spéculaire fait un
plastique, un velours est **rétro-réflectif**.

---

## ⚑ ARTY ET FLUFFY — la dalle ne se voit plus, elle colore les poils · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-ORBITE-DALLES.html`** · `scratchpad/_q_{cellule,peint,planche}.js`

### ⚑ LE MONTAGE QUI TIENT LES DEUX

```
1 · LE MOTEUR PEINT LES DALLES sur un calque SOURCE — jamais a l'ecran
    dans le VRAI polygone de chaque cellule (Voronoi spherique, coins arrondis)
2 · LA FOURRURE EST TOUT CE QU'ON VOIT : chaque touffe prend la couleur du pixel
    qu'elle recouvre. Donc la vraie forme de la dalle, la vraie teinte du Studio,
    et le clair-obscur de sa trame — SANS QU'UN SEUL APLAT PLAT N'APPARAISSE.
3 · LE JOINT reste vide : c'est le recul des plans bissecteurs (0,020 rad).
4 · TOUTES les cellules portent leur dalle — c'est ce qui fait la BOULE.
```

**C'est le point 2 qui fait le fluffy** : il n'y a plus de surface lisse nulle part.

### ⚠ TROIS RÉGLAGES QUI DÉCIDENT DE TOUT

- **L'éclaircissement de la pointe.** À 0,30 + 0,42·z, la pointe montait à 72 % vers le blanc
  et **toute la palette se lavait en beige**. Ramené à 0,05 + 0,19·z : c'est le **liseré du
  limbe** qui donne la lumière, jamais le blanchiment de chaque fibre.
- **La racine doit être dans la matière.** Aller chercher une couleur vers l'intérieur quand la
  racine tombe dans le vide **remplit les joints** et rend tout boueux. Le débord vient des
  touffes enracinées **dans** la dalle — et c'est lui qui fait le halo duveteux du contour.
- **Aucune tache spéculaire.** C'est la signature d'une bille de verre. Le velours est
  **rétro-réflectif** : plus clair au bord, sans point chaud.

### ⚠ CE QUI N'EST PAS FAIT

- **30 à 48 ms par image**, soit 20 à 30 im/s. L'essentiel part dans le `getImageData` /
  `putImageData` sur 3,5 Mo (planche à 470 px ; l'app rendra à 390). **Optimisation à faire.**
- Les **mondes creux** (braille, gravure, sillons) sortent plus maigres : la fourrure ne pousse
  que sur la matière de leur trame, et leur trame est clairsemée.
- L'**empreinte du doigt**, la **dérive** et le **partage** ne sont pas reportés sur ce peintre.

---

## ⚑ LE COTON REVIENT — mais PAR-DESSUS la dalle · 8 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-ORBITE-DALLES.html`** · modules `scratchpad/_q_{cellule,peint,planche}.js`

Reproche de Tom sur la version « vraies dalles » : *« c'est mega cheap, on veut nos poils ou
coton doux ».* Il avait raison : en réparant le dessin j'avais jeté la matière, et le résultat
était du **plastique** — une bille de verre à tache spéculaire.

### ⚑ LE BON MONTAGE : LA FIBRE NE PORTE PAS LE DESSIN, ELLE LE RECOUVRE

C'est ce qui débloque la contradiction des dix derniers tours. **Tant que chaque poil devait
dire « ici il y a de la matière du motif », il fallait qu'il soit aussi petit que le motif — et
il l'écrasait.** Maintenant :

```
1 · LE MOTEUR PEINT LA DALLE   dans le vrai polygone de la cellule, a l'echelle 1
2 · LA FOURRURE SE POSE DESSUS et PREND LA COULEUR DU PIXEL DE SA RACINE,
    eclaircie vers sa pointe
```

La fibre n'a plus rien à dire du motif : elle le duvette. Elle peut donc être **fine, courte,
dense**, et **déborder** — et c'est ce débord qui fait le coton.

### ⚑ UN VELOURS, PAS UN PLASTIQUE

Le dégradé radial avec **tache spéculaire blanche** est la signature d'une bille de verre.
Le velours et le coton font l'inverse : leur réflexion est **rétro-réflective** — plus clairs
**au bord**, là où les fibres se voient de profil, et la lumière y tombe sans point chaud.
Ambiant large, clé très molle, **liseré de duvet** au limbe.

### ⚠ DEUX BUGS DANS LA PASSE DE FOURRURE

1. **Je comparais l'alpha sur une image OPAQUE.** `if(al > alpha du fond)` — le fond vaut 255
   partout, le test échouait toujours, **la passe tournait vingt millisecondes en n'écrivant
   rien**. Corrigé en peignant la fourrure sur **sa propre couche transparente**, où la
   comparaison d'alpha redevient valide, et en fondant **une seule fois** au `drawImage`.
2. **La fourrure poussait DANS les joints.** Quand la racine tombait sur le vide, j'allais
   rechercher une couleur vers l'intérieur : le joint se remplissait et tout devenait boueux.
   **Une touffe ne pousse que si sa racine est dans la matière** ; c'est en s'étendant qu'elle
   passe par-dessus le joint et par-dessus la silhouette.

### ⚠ CE QUI N'EST PAS FAIT, ET JE NE LE MAQUILLE PAS

- **33 à 55 ms par image** — soit 20 à 30 images par seconde, pas 60. L'essentiel part dans le
  `getImageData` / `putImageData` sur 3,5 Mo (la planche rend à 470 px ; l'app rendra à 390).
  **Une passe d'optimisation est nécessaire** et elle n'est pas faite.
- **Les joints restent durs.** Le débord adoucit le bord extérieur des dalles, pas le fond du
  joint.
- L'**empreinte du doigt**, la **dérive** et le **partage** ne sont pas encore reportés sur ce
  peintre.

---

## ⚑ LE PEINTRE EST REFAIT — LE MOTEUR DESSINE LUI-MÊME · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Nouvelle planche : **`PLANCHE-ORBITE-DALLES.html`**
> Modules : `scratchpad/_q_{cellule,peint,planche}.js` · l'ancien état est dans
> `sauvegardes/orbite-6sept/`

### ⚠ POURQUOI ON A REPRIS DE ZÉRO — et j'aurais dû le voir dix tours plus tôt

L'ancienne chaîne était : **raster d'une dalle → nuage de points → tampon de poil**. Trois
approximations empilées, et une **contradiction insoluble** :

```
un poil fait 6 px · un motif du moteur a un pas de 5 a 11 px
   poil plus petit que le motif   -> il l'ecrase (pixel illisible, encre en pates)
   motif agrandi pour le sauver   -> une cellule n'en montre plus qu'un ou deux,
                                     et LE MOTIF CESSE D'ETRE UN MOTIF
```

À l'échelle d'une dalle de 67 px, **il n'y a pas de place pour un grain de fourrure entre les
deux**. Aucun réglage n'en sort. Je répondais par des réglages depuis cinq tours.

### ⚑ CE QUE FAIT LE NOUVEAU PEINTRE

1. **Le vrai polygone de chaque cellule**, en sommets : on part d'une calotte large et on la
   rabote par chaque bissectrice (Sutherland-Hodgman sur la sphère). C'est le contour **exact**,
   pas une frontière devinée point par point. `inset` recule chaque plan — c'est le filet.
2. **On projette, on découpe dessus** (coins arrondis, comme le moteur arrondit ses dalles).
3. **`Toile.dalleTrame` peint dedans, à l'échelle 1.** Vrai pas de motif, vraies couleurs,
   vraies strates — parce que c'est le moteur qui peint.
4. **L'ombrage par-dessus, en un seul geste** : un dégradé continu (clé haut-gauche,
   remplissage bas-droite, liseré au limbe). Pas de quantification, donc pas de bandes.

```
COUT : 51 cellules, 2 a 3,5 ms par image — contre 15 ms pour 150 000 tampons.
Le budget n'est plus le sujet.
```

### ⚠ ET UN BUG QUI DATAIT DU PREMIER JOUR

Le bouchon de planche `function cc(){return [200,180,255];}`. Le moteur fait
`s.ci=cc(s); s.c=PAL[s.ci]` : **`cc` rend un INDEX de palette, pas une couleur.** Mon bouchon
rendait un tableau, `PAL[tableau]` valait `undefined`, et **toutes les dalles retombaient sur le
même mauve**. C'est ce bouchon — pas le moteur — qui privait l'Orbite de la palette du Studio
depuis le début. Il rend maintenant un index tiré de la position de la graine, donc stable.

### Où en est chaque monde

Les huit sont lisibles et reconnaissables : encre en aplats francs, mosaïque en tesselles,
**touffe en vraies marguerites avec tiges et cœurs orange**, braille en grille de pois, pixel en
blocs, terrazzo en éclats, gravure en stries par dalle, sillons en ondes.

### Ce qui n'est PAS fait

- **La fourrure n'est plus là.** Elle redevient un traitement de surface à poser par-dessus des
  dalles justes, au lieu d'être ce qui portait le dessin. C'est le prochain lot.
- L'**empreinte du doigt**, la **dérive**, le **partage** : à reporter sur le nouveau peintre.
- L'ancien état complet est dans `sauvegardes/orbite-6sept/` — rien n'est perdu.

---

## ⚑ LE POIL ÉTAIT AUSSI GROS QUE LE MOTIF · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`**

Reproche de Tom : *« pixel illisible et mal fait, terrazzo encre illisibles aussi ça fait des
pâtés »*, et *« ça ne suit pas les contours des designs de dalles »*. Trois causes distinctes,
et je les avais confondues en une seule.

### ⚑ 1 · LE POIL DÉTRUISAIT LE MOTIF QU'IL DEVAIT DESSINER

Les trames du moteur ont des pas de **5 à 11 pixels** — carrés tous les 5, pois tous les 9,
tesselles tous les 11, sillons tous les 6. Un poil en fait **5 à 8**. À l'échelle naturelle,
**le grain est aussi gros que le détail qu'il doit peindre** : il l'écrase. D'où « pixel
illisible » et « des pâtés ».

**On lit donc la trame AGRANDIE** (×2,7) : ses détails passent à 15-30 px, franchement plus gros
que le grain, et une cellule montre trois à cinq périodes — comme une dalle de Toile qu'on
regarde de près. C'est un écart assumé au 1:1, et c'est la légibilité qui le commande.

### ⚑ 2 · UNE DALLE A UNE COULEUR, ET DES STRATES DEDANS

Le moteur ne peint pas une dalle d'un seul aplat : `PALL()` donne **une** couleur de palette
déclinée en cinq éclats, et c'est ce qui fait les strates d'une encre ou d'un terrazzo.
Je ne gardais que « matière ou vide » : les dalles sortaient en pâtés.

La trame livre maintenant **deux choses** : la matière, et de combien chaque pixel est plus
clair ou plus sombre que la médiane de son monde. Ce clair-obscur se reporte **en marches** sur
la couleur de la cellule. Les strates reviennent, et la palette du Studio ne se disperse pas.

⚠ **Et il doit rester DISCRET.** À vingt-six marches par unité de clarté, une strate claire
sautait de sept marches d'un coup — droit dans la partie qui déteint vers la crème — et **toute
la sphère se lavait de blanc**. Trois marches au plus : une strate nuance une dalle, elle ne la
repeint pas.

### ⚑ 3 · LE DESSIN DE « PIXEL » EST DANS SON CONTOUR, PAS DANS SON INTÉRIEUR

Une dalle *pixel* est **pleine** (73 % de remplissage) : ce qui la rend reconnaissable, c'est
que **son bord est calé sur une grille de cinq pixels**. Je cherchais son motif à l'intérieur —
il n'y en a pas — et elle sortait en polygone lisse, illisible. On quantifie donc la **position
qui sert à décider de la cellule** : le bord devient escalier.

### ⚑ 4 · ET LE CONTOUR RESTE NET

Un poil poussé à pleine taille **déborde du bord de sa cellule** et rend la dalle floue. On garde
donc la distance au bord (l'écart au deuxième site) et **le poil raccourcit en s'en approchant** :
deux crans sur les quarante derniers pour-cent. Une dalle a un contour franc.

### Où en est chaque monde

```
ENCRE      des blobs organiques, strates internes visibles
MOSAIQUE   une grille de tesselles, joints nets
TOUFFE     des fleurs entieres, reconnaissables
BRAILLE    de gros pois
PIXEL      un contour en escalier — son dessin
TERRAZZO   des eclats irreguliers
GRAVURE    des stries epaisses, un angle PAR DALLE
SILLONS    des ondes
```

### Ce qui reste ouvert

- **« Les six DEDANS »** attend toujours ton arbitrage (cinquième fois).
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.
- Le **×2,7 sur la trame** est un écart au 1:1 de la Toile, assumé pour la lisibilité : c'est un
  seul nombre si tu veux le rapprocher.

---

## ⚑ DE VRAIES DALLES, AVEC LEURS VRAIS CONTOURS · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`**

Reproche de Tom : *« c'est pas des vraies dalles avec leurs vrais contours, du coup y'a plein
d'erreurs »*. Il avait raison, et c'était une **erreur de conception**, pas un réglage.

### ⚠ CE QUE JE FAISAIS, ET POURQUOI C'ÉTAIT FAUX

Je découpais chaque cellule avec **la silhouette d'une IMAGE de dalle mise à l'échelle**. D'où :
des contours étirés, qui ne se raccordent pas d'une cellule à l'autre, des morceaux flottants,
un pavage qui n'en est pas un.

**Or j'avais déjà la vraie chose sous la main.** Une dalle de Toile, c'est **sa cellule de
Voronoï pondéré** — et j'en ai une, vraie, sur la sphère. Il suffisait de m'en servir comme
contour au lieu d'y plaquer une image.

### ⚑ LE CONTOUR SE LIT DANS LE DIAGRAMME, ET LES COINS S'ARRONDISSENT TOUT SEULS

Le bord d'une cellule, c'est l'écart au deuxième site : `d2 − d1`. En dessous du joint, on ne
peint plus. **Et les coins s'arrondissent gratuitement** : près d'un coin on est proche de
**deux** voisins à la fois, donc la somme `exp(−(d2−d1)/r) + exp(−(d3−d1)/r)` franchit le seuil
plus tôt et le coin se trouve rogné. Une intersection **molle** de demi-espaces — c'est la
définition même d'un arrondi, et c'est exactement ce que le moteur fait avec `round`.

### ⚑ ET LA DISTINCTION EST CELLE DU MOTEUR, PAS LA MIENNE

`dalleTrame` la pose noir sur blanc : `LIBRE = (encre || terrazzo || touffe)`.

```
MOSAIQUE · BRAILLE · PIXEL · GRAVURE · SILLONS   leur trame est DECOUPEE sur la cellule
   -> le contour vient du pavage (arrondi aux coins), l'image ne donne que LA MATIERE,
      prise dans son interieur au pas naturel, sans redimensionnement ni repli
ENCRE · TERRAZZO · TOUFFE                        leur dalle DEBORDE de sa cellule
   -> leur vrai contour est celui de LEUR FORME : on garde la silhouette de l'image,
      mise a l'echelle UNIFORMEMENT (la forme n'est jamais deformee)
```

### ⚑ ET SUR UNE TRAME, LA COULEUR VIENT DE LA DALLE, PAS DU MOTIF

Le moteur peint la trame d'une dalle **dans la couleur de cette dalle** : le motif ne dit que
« matière ou vide ». En prenant la couleur dans l'image du motif, j'étais obligé de choisir la
dalle-source **pour sa taille** — donc de tomber toujours sur les deux ou trois mêmes, et la
sphère sortait presque monochrome. Séparer les deux rend la variété de la palette **et** libère
le choix du motif : on prend celui au plus grand intérieur, celui qui ne rabattra jamais.

⚠ **Le rabattement, justement** : quand une cellule dépassait l'intérieur de sa dalle-source, je
rabattais l'échantillon sur son bord — d'où des **traînées radiales** au bord des cellules.

### L'état

```
77 cellules (la taille de dalle mesuree sur la Toile) · jusqu'a 153 700 touffes = 615 000 poils
banc : 161 156 touffes = 644 624 poils a 15,30 ms sur un ecran de 390 px, sphere en rotation
```

### Ce qui reste ouvert

- **« Les six DEDANS »** attend toujours ton arbitrage (quatrième fois) : le dos n'étant plus
  peint, les disques sont posés après la matière.
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ L'ENTRE-DALLES REDEVIENT VIDE, ET LA LUMIÈRE EST REFAITE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`

### ⚑ 1 · LES « BANDES DIAGONALES » ÉTAIENT MES MARCHES

Reproche de Tom : *« mets pas ces bandes diagonales »*. Ce n'était pas la lampe, c'était **la
quantification**. Je faisais tomber l'éclairement sur **sept marches** — et la sphère se
terrassait en bandes.

**J'appliquais à l'OMBRAGE D'UN VOLUME une règle qui vaut pour LA COULEUR D'UNE DALLE.**
« Un aplat franc, jamais un dégradé » décrit une dalle de Toile, pas la lumière qui glisse
dessus. Une dalle garde sa teinte ; son éclairement doit être **continu**. Vingt marches, l'œil
ne les sépare plus.

### ⚑ 2 · UN VRAI ÉCLAIRAGE, À TROIS TERMES

Une seule directionnelle laissait la moitié de la boule dans le noir. On pose ce que pose
n'importe quel éclairage de studio, et pour les mêmes raisons :

```
LA CLE          en haut a gauche, devant — elle sculpte le volume
LE REMPLISSAGE  en bas a droite, plus faible et plus large — il OUVRE l'ombre
                au lieu de la boucher, sans effacer la forme
LE LISERE       au limbe (Fresnel) — il detache la silhouette et affirme le cercle
+ un ambiant franc : la matiere doit se lire PARTOUT
```

⚠ **Et la moyenne doit tomber dans la partie COLORÉE de la rampe.** À `lum × 19` le gros des
poils atterrissait sur les trois dernières marches — celles qui déteignent vers la crème — et
**la palette du Studio disparaissait sous son propre éclairage**. Les hautes marches sont
réservées aux vrais reflets.

### ⚑ 3 · L'ENTRE-DALLES REDEVIENT VIDE — et c'est ce qui a payé la densité

J'avais rempli toute la sphère pour supprimer les trous noirs. Mais avec **les six disques et le
Noyau** par-dessus, ça surcharge. On ne peint donc que la matière des dalles plantées ; le reste
est du vide, et **ce vide est la place du Noyau et des six**.

Effet de bord décisif : **on peut alors SUPPRIMER du semis les points qui ne peignent rien.**
La compaction se fait une fois, avant le tri par plaques — la boucle ne visite plus que de la
matière, et le semis de départ peut être très dense sans que l'image le paie.

```
MESURE, ecran 390 px, sphere EN ROTATION :
   135 122 touffes = 540 488 poils   mediane 12,90 ms   ZERO image > 20 ms sur 144
   161 156 touffes = 644 624 poils   mediane 15,30 ms   25 images > 20 ms
La planche est reglee a ~134 000 touffes = 535 000 poils sur le monde le plus dense.
```

Le semis se dimensionne **par monde**, à l'inverse du remplissage de sa trame : encre en donnait
180 000 tampons quand gravure en donnait 58 000 pour le même semis.

### Ce que je ne fais pas passer pour fait

- **La règle « les six DEDANS »** reste enfreinte, et elle attend toujours ton arbitrage. Le vide
  entre les dalles leur redonne de la place, mais ils sont posés après la matière.
- L'**animation** n'est jugée qu'au chronomètre. Le **partage** n'est pas maquetté. La
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ 440 000 POILS, ET LA SPHÈRE N'EST PLUS NOIRE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`

Reproche de Tom : *« ça paraît noir et vide encore »*. Deux causes distinctes, et je les avais
confondues — la densité, et **les valeurs**.

### ⚑ 1 · CE QUI FAISAIT LE NOIR : LE VIDE DE LA TRAME

Le vide de la trame — l'entre-deux des pois du braille, des stries de la gravure — était peint
à **0,15 de clarté**, et les cellules vides à 0,17. Or sur un monde creux ce vide occupe **les
trois quarts d'une dalle PLANTÉE** : les trois quarts de la sphère étaient donc noirs, même là
où il y avait un Promi. Remontés à **0,26** et **0,30**, et le côté à l'ombre ne s'efface plus
(présence 0,48 au lieu de 0,26).

**Sur la Toile on accepte ce noir parce que c'est un écran plat.** Sur un volume, la matière
doit se voir partout — sinon on ne lit ni le relief ni le pelage.

### ⚑ 2 · LES POILS POUSSENT EN TOUFFES — c'est ça qui a débloqué la densité

La décomposition du banc donnait : un poil coûte **0,108 µs**, dont seulement **0,042 de pixels
écrits**. **Les deux tiers sont le passage dans la boucle** — lectures, rotation, éclairage,
rangement. Donc tant qu'un tampon ne porte qu'un poil, on paie ce passage pour chacun.

**Quatre poils partant de la même racine ne paient qu'UN passage.** Chaque poil supplémentaire
revient à 0,042 µs au lieu de 0,108 — **deux fois et demie moins cher**. Et une fourrure pousse
en touffes, pas en brins isolés : ce n'est pas un artifice, c'est plus juste.

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
    94 987 touffes = 379 948 poils   mediane 14,50 ms   19 images > 20 ms sur 144
   110 010 touffes = 440 040 poils   mediane 16,60 ms   ZERO image > 20 ms      ← retenu
   124 990 touffes = 499 960 poils   mediane 18,70 ms   ZERO image > 20 ms  (53 im/s)
```

**440 040 poils, c'est 3,5 fois les 125 000 du lot précédent.** Trois variantes de touffe pour
qu'on ne reconnaisse pas deux fois le même bouquet.

### Deux gains de plus, mesurés

- **`Math.atan2` par poil.** Il y en avait un, pour orienter le brin — cinquante à cent
  nanosecondes, plus que tout le reste de la boucle. On n'a besoin que d'un secteur sur
  vingt-quatre : le rapport du petit côté sur le grand, une table de 256 entrées, et l'octant
  se rattrape par des comparaisons de signe.
- **La clairière du Noyau se mesure au carré** : une racine de moins par poil.
  Les deux ensemble : **17,10 → 15,30 ms** à 125 000 poils.

### Ce que je ne fais pas passer pour fait

- **La règle « les six DEDANS »** reste enfreinte : le dos n'étant plus peint, les disques
  sont posés après la matière, dans une clairière d'encre. **À confirmer ou à corriger.**
- La sphère est maintenant **assez pâle** dans ses zones vides. C'est le contraire du défaut
  d'avant ; si c'est trop, c'est un seul nombre.
- L'**animation** n'est jugée qu'au chronomètre, le **partage** n'est pas maquetté, et la
  **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ LA FOURRURE VISIBLE DOUBLE, ET 77 DALLES MESURÉES · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html`
> Compte des dalles : `scratchpad/compte_dalles.html`

### ⚑ 1 · LE DOS N'EST PLUS NI PEINT NI MÊME VISITÉ

Le banc disait que le coût est **par point visité**, pas par pixel. Or la moitié du semis vit
derrière la sphère, où la fourrure ne se lit pas. Le tester point par point coûtait quatre
produits sur cette moitié.

**Parade : le culling par PLAQUES.** La sphère est découpée en **96 plaques**, les points sont
triés dedans (par une table hauteur × azimut, pas une recherche exhaustive : celle-ci coûtait
96 produits par point, soit quarante millions à la construction), et chaque image ne teste que
**96 directions**. Les plaques tournées vers l'arrière ne sont jamais parcourues.

Et dans la foulée, **tout ce qu'un point porte tient dans une seule bande de mémoire** : la
boucle lisait huit tableaux séparés, elle en lit un seul, de dix flottants par point, contigu.

```
RESULTAT, mesure au banc, ecran 390 px, sphere en rotation :
   125 000 poils TOUS DE FACE   mediane 17,10 ms
   c'etait 125 000 peints dont 62 500 de face — la fourrure QU'ON VOIT a donc DOUBLE
   165 000 de face -> 21,80 ms (46 im/s) · 210 000 -> 27,30 ms
```

⚠ **Ce que je n'ai PAS fait :** doubler le nombre *peint* (250 000). Ça coûte 27 ms, soit
37 images par seconde. Ce qui a doublé, c'est la densité **visible**, à budget égal.

### ⚑ 2 · LE NOMBRE DE DALLES EST MESURÉ, PLUS ESTIMÉ

`scratchpad/compte_dalles.html` plante jusqu'à saturation et compte les cellules.

```
LA TOILE, a 390 x 620 (l'ecran de l'app)   54 cellules -> une dalle de 66,9 x 66,9 px
LA SPHERE, meme ecran                       surface 345 237 px2
   a taille de dalle EGALE il en faut 77   (j'en avais 61)
   dont une trentaine visibles de face — comme un ecran de Toile
```

### ⚑ 3 · LE CONTRASTE — pixel et mosaïque ne se lisaient pas

Leurs aplats tombaient tous dans deux marches voisines. La rampe est élargie
(`DL` de −0,34 à +0,28 au lieu de −0,40/+0,22), la marche s'étale sur toute la rampe
(`lum×5,4−0,55` au lieu de `×4,6−0,30`), et la cellule vide descend (clarté 0,17).

⚠ **Et un vrai bug de couleur :** je dérivais le fond d'une cellule vide de **la première
teinte de la trame**. Sur touffe, la teinte la plus fréquente est le **vert des tiges** — et
toute la sphère virait à l'olive. Sur la Toile, les cellules vides prennent une table de gris
bleutés très sombres, jamais la couleur d'une dalle. On part maintenant de l'encre de l'écran.

### ⚠ CE QUI CHANGE UNE RÈGLE ACQUISE, ET QUI DEMANDE UN ARBITRAGE

**« Les six DEDANS et pas dessus »** ne peut plus tenir telle quelle. Les disques étaient
tramés entre la passe de dos et celle de devant ; le dos n'étant plus peint, ils se sont
retrouvés **sous toute la fourrure et ont disparu**. Je les pose donc **après** la matière,
dans une clairière d'encre qui les fait quand même lire comme posés *dans* le pelage.
**C'est un écart à une règle validée : à confirmer ou à corriger.**

### Ce qui reste ouvert

L'**animation** n'est toujours jugée qu'au chronomètre. Le **partage** n'est pas maquetté.
La **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon. Et il reste une **marge** entre
la dalle et le bord de sa cellule, comblée par le ton sombre : ma cellule sphérique n'a pas la
forme de la dalle qu'elle porte.

---

## ⚑ 125 000 POILS, ET LE PAVAGE ENTIER · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html` + `cap_banc.py`

### ⚑ 1 · SUR LA TOILE IL N'Y A AUCUN TROU

C'est le point que je manquais depuis trois lots. **Le canevas est ENTIÈREMENT pavé.** Ce que
je prenais pour des « écarts noirs entre les dalles », ce sont des **cellules sombres** qui
portent la même trame. Je sautais ces points : la sphère se trouait de noir, ce qui ne
ressemble à rien de la Toile.

**Maintenant tout point peint quelque chose** — la couleur de la dalle là où il y a matière,
le ton sombre de la cellule partout ailleurs. Le joint vaut **zéro**. Effet de bord heureux :
plus aucun point n'est gaspillé.

### ⚑ 2 · UNE CELLULE MONTRE UNE DALLE ENTIÈRE

En n'échantillonnant que le **rectangle inscrit** et en repliant au miroir, je découpais les
motifs : les fleurs de touffe devenaient du moucheté, la gravure des losanges. On pose
maintenant **la dalle complète** dans la cellule — sa silhouette, sa matière, ses couleurs.

⚠ Et le calage se fait sur **l'étendue réellement peinte**, pas sur le canevas : `dalleTrame`
ajoute une marge `pad` qui vaut 0,85 fois l'espacement pour encre, terrazzo et **touffe** (ces
trois-là débordent de leur cellule sur la Toile). En calant le canevas, la dalle se retrouvait
deux fois trop petite et noyée dans du fond — **c'est pour ça que touffe ne se voyait pas.**

Et les cellules sont passées de 213 à **59** : la vraie Toile montre une vingtaine de dalles par
écran, pas cent cinquante. C'est ce qui rend le design lisible.

### ⚑ 3 · 56 400 → 125 000 POILS, ET J'AI CHERCHÉ AU MAUVAIS ENDROIT TROIS FOIS

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
   110 000 poils   mediane 14,80 ms    22 images > 20 ms sur 144
   125 000 poils   mediane 16,50 ms   ZERO image > 20 ms sur 144      ← retenu
   140 000 poils   mediane 18,40 ms     3
   160 000 poils   mediane 20,50 ms   123
```

**Trois hypothèses fausses, mesurées et abandonnées :**
1. **Des poils plus petits.** De 13,9 à 9,7 pixels par poil : 19,7 → 19,2 ms. **2,5 %.** Ce ne
   sont donc pas les pixels écrits.
2. **L'atlas en tableau d'objets.** Mis à plat en deux grands tableaux typés (un départ et un
   compte par tampon) : **aucun gain**. Ce n'étaient pas les déréférencements.
3. **Les `push` sur tableaux ordinaires**, remplacés par des tableaux typés préalloués :
   **aucun gain** non plus.

**La mesure qui a tout dit** — décomposer en trois passes (complet / sans versement / sans
rien) : sur **27,4 ms** à 90 000 poils, le **versement n'en coûtait que 3,3** et la projection
**0,7**. Les **23,4 autres** étaient dans la boucle de déformation.

**Et deux causes, toutes deux évitables :**
- **`Math.pow` et `Math.hypot` par point.** `Math.hypot` fait une mise à l'échelle pour éviter
  les débordements — inutile sur des coordonnées entre −1 et 1 ; `Math.sqrt` va cinq à dix fois
  plus vite. `Math.pow(x, 0,6)` se tabule. **27,4 → 16,0 ms.**
- **La boucle de déformation repassait sur TOUS les points à chaque image**, alors qu'elle est
  **statique** : positions, normales et champ de flux vivent dans le repère de l'objet. Elle ne
  dépendait de la vue que par **l'amorti au limbe** — et celui-là se calcule à la **projection**,
  où la profondeur est déjà connue. Il ne reste par image que **la calotte du contact** : un
  produit scalaire par point pour la trouver, la vraie géométrie pour les quelques milliers qui
  y tombent, et on rend ce qu'on a touché à l'image suivante. **16,0 → 12,7 ms.**

### Ce que je ne fais pas passer pour fait

- Le **calage de la dalle sur la cellule** reste un compromis : ma cellule sphérique n'a pas la
  forme de la dalle qu'elle porte. Il reste une marge, comblée par le ton sombre de la cellule.
- L'**animation** n'est toujours pas jugée à l'œil, seulement chronométrée.
- Le **partage** n'est pas maquetté, et la **profondeur du doigt** n'est prouvée qu'à 10,5 % du
  rayon.

---

## ⚑ LA VRAIE TOILE COMME RÉFÉRENCE — et 56 400 poils · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · référence : `scratchpad/vraie_toile.html` + `cap_toile.py`
> Banc : `scratchpad/banc_poils.html` + `cap_banc.py`

**J'ai enfin capturé la vraie Toile dans les huit mondes, et elle a tranché trois débats d'un
coup.** Je réglais mes écarts et mes motifs à l'estime ; la référence existait, il suffisait de
la rendre.

### ⚑ CE QUE LA VRAIE TOILE DIT, ET QUE JE FAISAIS FAUX

```
1 · LES DALLES SE TOUCHENT.       Il n'y a pas de « joint » : un filet, au plus.
    Ce que je prenais pour des ecarts, ce sont LES CELLULES VIDES.
2 · LA PLUPART DES CELLULES SONT VIDES,   presque noires, et elles portent la MEME
    trame. Les dalles colorees sont une GRAPPE au milieu. Je peignais toutes les
    cellules en couleur : ca faisait un vitrail, pas une Toile.
3 · L'ANCRAGE DU MOTIF DEPEND DU MONDE.   braille (pas 9), mosaique (11), pixel (5)
    et sillons (6) sont ancres sur des coordonnees ABSOLUES : leur motif est CONTINU
    d'une dalle a la suivante. Encre, touffe, terrazzo et gravure portent l'angle
    propre de leur graine (`s.ang`) : chaque dalle a SA direction.
```

Je tournais **toutes** les cellules au hasard : la grille du braille partait dans tous les sens.
Puis **aucune** : la gravure devenait un peigne uniforme. **Les deux étaient faux — c'est par
monde**, et c'est le moteur qui le dit, pas moi.

### ⚑ LES MOTIFS — on n'étire plus, on agrandit la Toile

Les trames sont ancrées sur des **pas absolus**. En étirant chaque dalle pour la faire tenir
dans sa cellule, ce pas devenait quelconque : **c'est pour ça que les motifs ne ressemblaient pas
au design.** Maintenant un radian vaut toujours le même nombre de pixels de trame.

Pour que ça marche il faut de **grandes dalles**. `seedGray()` ne repeuple que si la Toile est
vide : on l'amorce petite (46 cellules), puis on **agrandit le canevas** et `relax()` étale ces
mêmes 46 cellules sur toute la surface. Les dalles passent de **72 à 200-380 px**, au pas absolu
inchangé.
⚠ **J'avais écrit `agrandit()` et je ne l'appelais pas.** Les dalles restaient petites, il
fallait donc replier au miroir pour couvrir une cellule — d'où des **chevrons** très visibles sur
la gravure.

⚠ **Et une préférence bien intentionnée écrasait tout :** j'avais ajouté « prendre la dalle au
plus grand rectangle inscrit » pour éviter les replis. Elle **écrasait le tirage au hachage** :
presque toutes les cellules tombaient sur la même dalle et **la sphère sortait monochrome**.
Supprimée — depuis que les dalles sont grandes, il n'y a plus rien à éviter.

### ⚑ LES POILS — 36 450 → 56 400, et deux optimisations mesurées

Le banc décompose le coût : **1,9 ms de fixe** puis **0,28 µs par poil** (13,9 pixels écrits,
24 ns le pixel — c'est l'**accès dispersé** dans un tampon de 2,4 Mo, pas le calcul).

```
MESURE, ecran 390 px, sphere EN ROTATION, intervalle reel entre deux images :
   45 775 poils   mediane 14,40 ms   1 image > 20 ms sur 144
   56 388 poils   mediane 17,00 ms   ZERO image > 20 ms sur 144      ← retenu, 59 im/s
   66 911 poils   mediane 20,10 ms   85 images > 20 ms
```

**Ce qui a payé :**
1. **Une seule passe de tampon au lieu de deux.** Le coût fixe partait dans deux vidages de
   608 000 mots, deux `putImageData` de 2,4 Mo et deux `drawImage`. Les six restent **dedans**
   (règle acquise) : on les trame **dans le tampon**, entre le dos et le devant.
   **4,3 → 1,9 ms.**
2. **Le versement écrit sans relire.** La comparaison `a > (B[oo]>>>24)` ajoutait une **lecture**
   par pixel — donc un défaut de cache de plus et une dépendance. Le dernier posé gagne : c'est
   acceptable pour une fourrure (un poil en recouvre un autre), ça ne l'était pas pour des grains
   isolés. **−18 % par poil.**

**Ce qui n'a rien donné, et qui est noté pour ne pas y revenir :**
- **Des poils plus fins** : 16,40 contre 16,60 ms. Ce n'est pas le nombre de pixels.
- **Les `push` sur tableaux ordinaires** remplacés par des tableaux typés : **aucun gain**.
- **Ranger les poils par bande d'écran** pour grouper les écritures : **aucun gain** (17,7 contre
  17,3). Le comptage coûte ce que le cache économise.
- **Éclaircir le dos** : perte nette, déjà noté au lot précédent.

### Ce que je ne fais pas passer pour fait

- **Il reste du repli au miroir** sur les cellules plus grandes que le rectangle inscrit de leur
  dalle : on voit encore quelques losanges, surtout en gravure. La vraie parade serait de
  détecter le pas du motif et de replier par translation.
- **17,00 ms, c'est 59 images par seconde**, pas 60. Zéro image au-dessus de 20 ms sur 144 — mais
  je ne prétends pas 60.
- L'**animation** n'est toujours pas jugée, et le **partage** n'est pas maquetté.

---

## ⚑ LES ÉCARTS, LA DENSITÉ, ET LE BANC QUI TRANCHE · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · banc : `scratchpad/banc_poils.html` + `cap_banc.py`
> Anti-cache : `scratchpad/bust.py`

### ⚠ 0 · CE N'ÉTAIT PAS LA PLANCHE, C'ÉTAIT LE CACHE — deuxième fois

`python3 -m http.server` n'envoie **aucun** `Cache-Control`. Le navigateur applique sa
fraîcheur heuristique et **ne redemande même pas** le fichier : le serveur ne peut rien, il
n'est jamais interrogé. Ça mord surtout depuis que la planche charge cinq modules externes —
le HTML se recharge, les `.js` non. **Vérifié en `curl` avant de conclure** : les cinq modules
répondaient `200` avec les marqueurs neufs.
**`scratchpad/bust.py`** horodate chaque `<script src>` avec le `mtime` du fichier
(`?v=1788870952`) et pose un `no-store` sur le document. **À relancer après toute édition de
module.**

### ⚑ 1 · LES ÉCARTS ENTRE DALLES — la silhouette ne doit pas découper la cellule

Je découpais chaque cellule avec **la silhouette** de sa dalle. Une dalle dont les proportions
ne collaient pas y laissait une marge énorme, sa voisine presque aucune : des joints **du simple
au triple**, ce qui ne ressemble à aucune Toile.

**Parade : on ne prend que L'INTÉRIEUR de la dalle.** Chaque dalle rendue reçoit son **plus grand
rectangle inscrit** (`inscrit()` : la silhouette est fermée par balayage en lignes *et* en
colonnes, sinon les mondes creux — gravure, 22 % de pixels — n'ont pas d'intérieur du tout). La
cellule se cale sur ce rectangle, et **le joint devient une valeur angulaire constante**,
0,016 rad ≈ 4 % du diamètre d'une dalle — le même filet partout.
⚠ Les trous de la **trame** restent : les pois du braille, les stries de la gravure sont de la
matière absente, pas un bord de dalle.

### ⚑ 2 · CHAQUE MONDE VISE LA MÊME DENSITÉ

Un monde creux peignait deux fois moins de poils qu'un monde plein : l'Orbite en gravure
sortait terne, alors que ce qu'on veut voir c'est **sa trame**, pas sa pénurie. On sème
maintenant en proportion inverse du remplissage du rectangle inscrit (plafonné à ×3,2).

```
MESURÉ, huit mondes, même cadre :  encre 36 616 · mosaique 36 485 · touffe 35 837
   braille 37 076 · pixel 36 575 · terrazzo 35 098 · gravure 35 942 · sillons 38 403
   (avant compensation : de 13 175 pour gravure a 36 460 pour encre)
```

### ⚑ 3 · LE BANC — et il a corrigé DEUX de mes intuitions

Le plafond de l'audit (39 500) avait été mesuré sur des **dalles**, pas sur des poils. J'ai donc
mesuré, sur **l'intervalle réel entre deux images**, sphère **en rotation**, écran de 390 px :

```
36 453 poils   mediane 16,40 ms   9e decile 17,00   1 image > 20 ms sur 144   ← le plafond
42 004         18,10              18,90             3   (≈ 55 im/s)
46 929         20,50              21,20            126   (≈ 46 im/s)
56 658         24,30              25,20            144
```

**Ce qui m'a détrompé :**
1. **Des poils plus FINS ne rendent presque rien.** 36 450 poils fins → 16,40 ms contre 16,60
   pour des gras. Ce n'est donc **pas** le nombre de pixels peints qui domine, c'est **le coût
   par tampon**. La monnaie est le tampon, pas le pixel.
2. **Éclaircir le dos est une PERTE NETTE.** Un point du dos garde son coût de boucle ; on
   n'économise que son tampon. **35 956 poils à 18,40 ms** avec un dos au tiers, contre
   **36 453 à 16,40** avec le dos plein et moins de candidats. Contre-intuitif, et mesuré.

**Ce qui a vraiment payé :** les tableaux par point en **Float32Array** au lieu de Float64 —
17,60 → 16,50 ms à nombre égal, **7 %**. La boucle est liée à la mémoire, pas au calcul.
Et le **cache du travail statique** : relief (six évaluations de `phi` par point), champ de flux
et lecture de trame vivent dans le repère de l'objet — la rotation n'y change rien. L'image ne
paie plus que la projection, la lumière et le versement.

### La réponse honnête à « plus fourni en poils »

**36 450 poils, c'est le plafond des 60 images par seconde** pour ce grain, sur un écran de
390 px. Au-delà on descend : 42 000 → 55 im/s, 47 000 → 46 im/s. Ce qui a réellement rendu la
fourrure plus fournie, ce n'est pas le nombre — c'est que **les dalles sont pleines** depuis
qu'on échantillonne leur intérieur au lieu de les découper à la silhouette, et que **les mondes
creux sont compensés**.

### Ce qui reste ouvert

L'**animation** n'est toujours pas jugée (le banc tourne, mais personne n'a regardé). Le
**partage** n'est pas maquetté. Et la **profondeur du doigt** n'est prouvée qu'à 10,5 % du rayon.

---

## ⚑ LA SPHÈRE EST LA TOILE — synchro Toile · Orbite · Studio · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · moteur : `scratchpad/_p_{moteur,trame,semis,peint,planche}.js`
> Sonde des huit mondes : `scratchpad/sonde_trame.html` · captures : `scratchpad/pav/`

**Décision Tom : la surface de l'Orbite n'imite plus la Toile, elle EST la Toile.**
Chaque cellule du Voronoï sphérique porte **une vraie dalle du moteur** —
`Toile.dalleTrame`, échelle 1 — avec sa forme, sa matière et ses couleurs. Changer de monde ou
de palette au Studio change la Toile **et** l'Orbite, du même geste. C'est la règle 1 du §4
appliquée à la lettre : jamais un polygone, jamais une approximation.

Et le grain devient un **poil** : la matière est duveteuse et **peignée**, comme immergée dans
un liquide transparent.

### ⚠ 1 · `Toile_resize()` LIT LE PARENT DU CANEVAS, PAS LE CANEVAS

```js
var st=host.parentNode; var w=st.clientWidth, h=st.clientHeight;
if(!w||!h) return;                 // ← et il ne se passe plus rien, en silence
```

Mon hôte était dans un `<div style="height:0;overflow:hidden">`. La Toile restait à **0 × 0**,
`seedGray()` ne posait aucune cellule, `plantOne()` rendait `null`, `Toile.count()` valait
**zéro** — et `dalleTrame` sortait des canevas **vides sans une seule erreur**, parce qu'elle
avale la sienne dans un `try/catch`. Une demi-heure perdue à chercher dans la mauvaise fonction.
**Le parent de l'hôte doit avoir une vraie taille** ; on lui donne 390 × 620, la géométrie de
l'app. Vérifier `Toile.count()` avant de croire une dalle.

### ⚠ 2 · TROIS ERREURS D'ÉCHELLE DE SUITE, SUR LE MÊME CALAGE

Poser une dalle du moteur dans une cellule sphérique demande un facteur pixels-par-radian. Je me
suis trompé trois fois, et **chaque erreur avait sa signature à l'écran** :

```
uu = (v·e1) × 480 × ech      ech ETAIT DEJA le facteur : tout tombait hors tableau
                             → LA SPHERE SORTAIT A UNE DALLE PEINTE (1 sur 74 000)
ech = diag/(2·rayon·1,30)    calage sur le CERCLE maximal de la cellule
                             → les cellules allongees restaient aux trois quarts vides
ech = max(w/du, h/dv)        la cellule debordait de l'IMAGE de la dalle
                             → 18 % de couverture, une sphere trouee
ech = min(w/du, h/dv)×0,98   ✓ toute la cellule tombe dans l'image ; le VIDE de la dalle
                             fait le joint d'encre, et c'est la vraie forme qui le decoupe
```

La cellule se cale sur **sa boîte** dans son propre plan tangent (u₀,u₁,v₀,v₁), pas sur son
cercle. Et on choisit pour chaque cellule la dalle dont la boîte lui ressemble le plus — même
allongement, même taille — pour que le grain de la trame garde à peu près sa taille naturelle
d'une cellule à l'autre, comme sur une vraie Toile.

### ⚑ 3 · LE DOIGT PEIGNE LA FOURRURE — sans ça l'empreinte ne se voit plus

Sur une sphère nue, un creux se lit à son ombre. **Sous un pelage, l'ombre est noyée par la
variation des poils eux-mêmes** : le pouce appuyé à fond ne se voyait pas du tout. Un vrai
pelage pressé se couche — les poils se rabattent **radialement**, en rosette, et ils
raccourcissent. C'est ce geste-là qu'on lit, pas l'ombre. Le peigne est plein au bord du
contact et s'éteint à 2,4 fois le rayon.

### Les poils, et pourquoi ils sont peignés

Le poil part de **la racine** (le centre du tampon) : il est donc orienté sur **2π**, pas sur π
comme un fil symétrique — **24 secteurs**. Il s'affine et s'éteint vers la pointe (c'est ce qui
fait doux plutôt que hérissé) et il s'incurve un peu.
**Un hachage par point donne un hérisson ; un champ lisse donne une fourrure.** L'orientation
vient du gradient tangent d'un scalaire basse fréquence : les poils tournent en volutes lentes,
jamais en bandes.

### La couleur ne se reconstruit plus : on la lit dans la dalle

Ce ne sont plus « les quatre couleurs de la palette » rebâties de mon côté, mais **les teintes
réellement peintes par le moteur**, quantifiées sur 5 bits par canal, les 96 plus fréquentes
gardées (encre en sort 6 ; touffe, 119). Le rapprochement se fait **à la demande** — un balayage
complet du cube 32³ coûtait deux millions de distances par monde.
Chaque teinte porte ses sept marches, et **la lumière fait monter la dalle d'une marche dans sa
propre rampe** : un aplat franc, jamais un fondu.

⚠ **La rampe montait trop haut** : la moitié des poils atteignait la marche du reflet et toute
la sphère virait à la crème — la palette du Studio disparaissait sous son propre éclairage.

### Ce qui est mesuré

```
LES HUIT MONDES rendent bien, et differemment (sonde_trame.html, dalles de 48 a 153 px) :
   encre 58-72 % de remplissage · mosaique 41-52 · touffe 37-49 · braille 26-35
   pixel 60-78 · terrazzo 42-52 · gravure 22-27 · sillons 24-34
LES POILS PAR IMAGE   34 366 sur les mondes pleins (encre, pixel) — sous le plafond de 39 500
   les mondes creux en peignent moins (12 900 pour gravure) : ils SONT creux, c'est la trame.
```

### Ce que je ne fais pas passer pour fait

- **L'animation n'est pas jugée.** Les poils sont peignés par un champ qui accepte un paramètre
  de temps (`tflux`), mais rien n'a été rendu en mouvement.
- **La profondeur du doigt n'est pas remesurée** depuis le lot précédent : la preuve en pixels
  vaut pour 10,5 % du rayon, la planche enfonce à 24,5 %.
- **Le grain de la trame varie encore un peu d'une cellule à l'autre** — le calage exact sur la
  boîte l'emporte sur la taille naturelle quand les proportions ne collent pas.
- **Le partage** n'est toujours pas maquetté.

---

## ⚑ LE PAVAGE HABILLÉ — QUATRE BUGS DE FOND · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-PAVAGE.html`** · moteur : `scratchpad/_p_{moteur,semis,peint,planche}.js`
> Preuve : `scratchpad/preuve_pavage.py` + `scratchpad/mesure_pav.html`
> Diagnostics : `scratchpad/diag_pav.html` (les étages du semis), `scratchpad/diag_emp.html` (la carte des zones de contact)

**Le parti pris est tranché : C, le pavage.** La Toile fermée sur elle-même — des dalles
pleines séparées par des joints d'encre, un Voronoï pondéré sphérique. Reproche de Tom sur la
livraison précédente, et il était juste : *« tu as tout éteint pour isoler. Isoler une variable
ne veut pas dire éteindre tout le reste. On ne choisit pas un parti pris sur une maquette
morte. »*

### ⚠ 1 · LE TIRAGE DES SEMENCES NE SORTAIT JAMAIS DE LA CALOTTE NORD

La boucle de rejet s'arrêtait dès qu'elle avait ses M semences :
`while(i<CAND && garde<M)`. Or l'indice d'un réseau de Fibonacci parcourt la sphère **du pôle
nord au pôle sud**. En s'arrêtant à la 240ᵉ acceptée, on ne sortait jamais du **premier quart**
du réseau : les 240 semences étaient toutes au nord. Partout ailleurs les deux plus proches
sites étaient loin **et à égale distance**, donc `d2−d1` tombait sous le joint sur des régions
entières, et le pavage **effaçait des quartiers complets de la boule**.

**Le diagnostic l'a montré en un rendu**, et c'est la leçon de méthode : j'ai peint le semis à
trois étages (brut / joint appliqué / **densité uniforme**). Avec une densité uniforme, **les
mêmes coins noirs** — donc ce n'était pas la densité, comme je le croyais depuis deux passes.
**Parade :** balayer tout le réseau, et régler le taux d'acceptation pour tomber sur M en
moyenne (deux passes, l'une pour la somme).

### ⚠ 2 · CE QUI TUE L'EFFET REPTILE, C'EST LA DENSITÉ DU SEMIS — PAS LE POIDS DES SITES

Je faisais varier le **poids** des sites (diagramme de puissance). Ça ne marche pas : au-delà
d'un écart de l'ordre de l'espacement, un site à poids faible n'est pas une *petite* cellule —
il est **avalé**, il disparaît. Les survivantes se retrouvent donc toutes de la même taille.
C'était exactement ça, la peau de reptile.

**La bonne variable est la DENSITÉ.** Une cellule occupe 1/densité : là où les semences se
serrent, les dalles sont petites ; là où elles s'espacent, elles sont grandes — et **aucune ne
disparaît**. C'est aussi ce que fait une vraie Toile : des grappes serrées et des clairières.
Le poids reste, faible : il casse la régularité locale, il n'avale plus.
Les fréquences du champ de densité valent **4 à 7** — une grappe fait cinq ou six dalles. Plus
bas, la densité varie à l'échelle de la boule et on retombe sur des bandes.

### ⚠ 3 · LA PERTURBATION DU DOIGT PORTAIT À SOIXANTE DEGRÉS

`(u/ub)·exp(1−u/ub)` vaut encore **18 % de son pic à u = 1,4**. Avec un rayon de contact de
0,36 rad, la queue du bourrelet portait jusqu'à 60° du doigt : **la boule entière se soulevait
de 3 % et glissait de 7 %**. L'image sous le pouce ne ressemblait plus à l'image au repos, et ce
n'était pas l'empreinte — c'était un effet global.

**La carte des zones de contact** (bleu = plateau, rouge = paroi, vert = bourrelet) l'a chiffré
d'un coup : **731 points de plateau contre 3 913 de queue de bourrelet.** Le creux était
minuscule et la perturbation immense — l'inverse d'une empreinte.

Et **`U` est un glissement EN RADIANS, pas un coefficient libre** : à 1,85 avec `dmax` 0,215, la
matière glissait de **0,40 rad**. Les dalles ne se tassaient pas, elles **se mélangeaient**, et
le contact sortait en pluie de traits de toutes les couleurs. Le refoulement d'une pulpe vaut le
volume chassé sur la circonférence, soit `d·a/2` = 0,039 rad.

### ⚑ 4 · LE MUR N'EST PAS UN COUTEAU, C'EST UNE CUVETTE LARGE

Je faisais remonter la surface en `exp(−u/0,085)` : le creux revenait à zéro en un cinquantième
de radian et l'empreinte se réduisait à un petit disque terne. **La solution exacte d'un poinçon
plat sur un solide mou est connue** : hors du contact, l'enfoncement vaut **(2/π)·asin(a/r)**.
Elle vaut 1 au bord (la continuité est assurée), **0,46 à une fois et demie le rayon, 0,33 à
deux fois**. C'est une cuvette — et c'est elle qui fait « la matière cède ». Le bord garde sa
cassure de pente (la dérivée y est infinie) ; **le fond reste plat**.

### Deux erreurs d'éclairage, et elles se ressemblent

- **Le fond d'un creux est occulté par son propre bord.** Sans ce facteur, le plateau sortait
  **plus clair que le reste de la boule** — sa normale regarde le doigt, donc la lumière, et
  Lambert le récompensait jusqu'à la marche du reflet : l'empreinte sortait en **cicatrice
  blanche**. Un trou est sombre, même quand sa surface est bien orientée.
- **Seule la part TANGENTE de la lumière creuse une ombre portée, et il faut la normaliser.** Au
  point touché, la lumière était radiale à 88 % : sa part tangente valait 0,47, l'ombre ne
  séparait le fond qu'entre 0,46 et 0,81, et le creux ne se lisait pas comme un creux.

### L'ombre se porte aussi par l'OPACITÉ

L'audit du 5 septembre l'avait annoncé : *« la palette d'un monde n'a pas l'écart de luminosité
de la crème sur l'encre — c'est cet écart qui faisait le volume ; avec des dalles colorées, la
sphère s'aplatit »*. Et elle s'aplatissait : un disque à liseré, pas une boule. On rend cet écart
en laissant le côté à l'ombre **s'éteindre vers l'encre** : la palette reste exacte, c'est sa
**présence** qui baisse. Plus un **liseré de Fresnel** au limbe — c'est lui qui affirme le cercle.

⚠ **Mais la matière ne disparaît pas SOUS le doigt : elle s'assombrit.** En laissant la présence
suivre la lumière dans le creux, les dalles du contact devenaient si pâles qu'on ne voyait plus
la mosaïque — un trou noir, pas un enfoncement. Dans le creux, la présence reste pleine ; c'est
la marche de couleur qui descend.

### La couleur : celle du Studio, et la rampe de la Toile

Une dalle d'Aura **est** une dalle de Toile : une couleur de `Toile.cols()` et une marche de ton
parmi les cinq du moteur (`TON = 1 · 0,76 · 1,24 · 0,88 · 1,12`). **La lumière ne fait pas un
dégradé : elle fait monter la dalle d'une marche dans sa propre rampe** — un aplat franc, jamais
un fondu. C'est la règle de la Toile, et c'est aussi ce qui évite les rayures parallèles pour
lesquelles l'iridescence a été refusée deux fois. Le **reflet d'essence** ne tourne pas la
teinte pixel par pixel : au ras du bord, **une dalle entière bascule** sur la couleur suivante
de la palette, d'un coup — il n'y a pas de dégradé à rayer.

### La technique

```
LE TAMPON NE PORTE PLUS QUE L'ALPHA ; la couleur se compose au versement par un OR.
   Sans ça : 4 couleurs x 7 marches x 3 tailles x 8 orientations x 6 niveaux = 4 032 tampons.
   Avec :    144.
LE GRAIN SE MESURE SUR LE CADRE, pas en pixels absolus — un atlas par taille de cadre.
   Sinon, sur un cadre de 200 px le même grain est trois fois plus gros par rapport à la boule.
LES COTES DU DECOR AUSSI (le Noyau, les six) : en dur, ils mangeaient la moitié des petits cadres.
38 829 DALLES par image — SOUS le plafond mesuré de 39 500 pour 60 im/s. A 90 000 candidats
   on montait a 49 800 : plus joli d'un cheveu, et hors budget.
```

### La preuve, et ce qu'elle ne couvre pas

**Re-mesurée sur le moteur du pavage, à la profondeur de la preuve d'origine** (0,105 et
a = 0,34), pour isoler **le changement de loi de paroi** — une variable à la fois :

```
1 · UN FOND PLAT              rayon ou le profil ne bouge plus (< 15 % de l'amplitude)
      plateau   8,0 -> 2,0 -> 24,0 px        cloche  0 · 0 · 1 px — elle creuse des le centre
2 · LE FOND EST-IL PLAT ?     dans LA MEME fenetre : ecart-type / moyenne, en % de l'amplitude
      plateau   6,8 / +1,9 %   8,5 / +10,2 %   5,5 / −1,2 %     ← le coeur est intact
      cloche   25,6 / −56,6 % 18,3 / −69,9 %  47,4 / −40,7 %    ← elle vide le coeur
3 · LE BOURRELET SE DEPLACE   plateau  34 -> 60 -> 67 px  (x1,97)
      cloche    21 -> 22 -> 22 px  (x1,05)  — sa tache ne grandit pas avec la pression
```

⚠ **CE QUE JE NE FAIS PAS PASSER POUR PROUVÉ.** La planche enfonce à **24,5 %** du rayon, pas à
10,5 %. À cette profondeur la perturbation couvre la moitié de la sphère et **la sonde décroche**
— elle lit alors le limbe autant que le creux, et les profils sortent bruités et asymétriques.
Le plateau et sa cassure de pente sont vrais **par construction** (le code est le même), mais
**la profondeur de la planche n'est pas mesurée**. Et le marqueur « bord franc » ne sépare
toujours pas les deux lois sur cet observable (6/12/8 px contre 4/7/5) : c'est le **fond plat**
qui porte la preuve du bord.

### Ce qui reste ouvert

L'**animation** n'a jamais été jugée sur cette matière. Le **partage** (image seule / intégrée)
n'est pas maquetté. Et le pavage est **statique** : il ne dit rien encore de la vie d'une Toile
qui pousse.

---

## ⚑ LE FORK DE L'ORBITE — ET DEUX BUGS QUI EXPLIQUENT LES CINQ SILHOUETTES RATÉES · 6 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, vérifié).
> Planche : **`PLANCHE-TROIS-MATIERES.html`** · moteur partagé : `scratchpad/_m_{moteur,semis,peint,neuf}.js`
> Preuve : `scratchpad/preuve_empreinte.py` + `scratchpad/mesure_emp.html` · images : `scratchpad/emp/`, `scratchpad/mat/`

### ⚠ 1 · LA SILHOUETTE — « haute fréquence » n'était appliquée QUE SUR UN AXE

Le relief de la dernière série valait `0,060 · sin(16,2x) · sin(0,7y) · cos(0,6z)`. La règle
« haute fréquence, faible amplitude » était **écrite** dans le fichier — et respectée en x
seulement. **0,7 et 0,6 en y et en z, c'est une enveloppe à l'échelle de la boule entière** :
des lobes verticaux, donc une courge. Aucune valeur d'amplitude n'aurait pu rattraper ça.

**Deux règles posées, et la seconde est plus forte que la première :**
1. toutes les fréquences ≥ 8 **sur les trois axes**, amplitude totale ≤ 3,6 % ;
2. **le déplacement radial est amorti au limbe** (facteur `face^0,6`, nul là où la normale est
   perpendiculaire au regard). La silhouette redevient alors un **cercle exact**, quelle que
   soit l'amplitude — le relief vit dans le disque, jamais sur son bord.

### ⚠ 2 · L'AXE DU DOIGT N'ÉTAIT PAS TANGENT — l'empreinte ressortait de l'autre côté

Même famille que le bug n° 1 de l'audit, et il coûtait une seconde empreinte détachée, hors
silhouette. `E.ax` gardait une part **radiale** : `du` mélangeait du tangentiel et du radial, et
la zone `s<1` n'était plus une tache sur la surface mais **un cylindre qui traverse la boule**.
Correctif : on orthogonalise l'axe à la normale, et **on mesure la tache dans le plan tangent**.

Et un troisième, dans la foulée : **le plan du plateau est perpendiculaire à la NORMALE, jamais
à l'axe du doigt.** Perpendiculaire à l'axe (qui est tangent), le « plateau » était un plan qui
**tranche** la boule : on voyait une morsure, pas une pulpe.

### L'EMPREINTE EST REFAITE — et prouvée sur l'image, pas dans le code

Le modèle n'est plus une cloche. **Une pulpe adhère et s'aplatit** : dans le contact la surface
devient **plane** (donc une seule normale, donc un méreau uniformément éclairé), **rien n'y
glisse**, et tout se passe **au bord** — paroi raide puis bourrelet. Et le rayon de contact suit
Hertz : `a = amax·p^(1/3)`, `d = dmax·p^(2/3)`.

```
LA MÊME SCÈNE, LES DEUX LOIS, ÉCLAIRAGE PLAT (l'image = la densité projetée du semis,
donc la géométrie et rien d'autre). Coupe en travers du doigt, lissée sur 13 px.

1 · UN CŒUR INTACT, ET IL GRANDIT     rayon où rien ne bouge (< 15 % de l'amplitude)
      plateau    5,0 px -> 11,0 px -> 14,0 px      ×2,80
      cloche     0,0 px ->  0,0 px ->  0,0 px      aucun : elle creuse dès le centre
2 · LE FOND EST-IL PLAT ?             DANS LA MÊME FENÊTRE, moyenne / amplitude
      plateau    +2,1 % -> +2,6 % -> +3,6 %        (écart-type 7,7 à 8,2 %)
      cloche    −80,1 % -> −76,4 % -> −78,9 %      (écart-type 20 %)
3 · LE BOURRELET                      lobe de signe opposé, au-delà du bord
      plateau    +29 % à 38 px -> +28 % à 53 px -> +32 % à 79 px
      cloche     +55 % à 16 px -> +69 % à 20 px -> +62 % à 24 px
```

**Ce que je ne fais pas passer pour prouvé :** la *raideur du bord* mesurée seule ne sépare pas
les deux lois (5 à 18 px des deux côtés, bruité). C'est le **cœur intact** qui porte la preuve du
bord : un rayon existe en deçà duquel rien ne bouge, et il n'existe pas pour la cloche.

### ⚠ TROIS PIÈGES D'INSTRUMENT PAYÉS SUR CETTE SEULE PREUVE

1. **Je cherchais de l'encre PERDUE au cœur du contact.** Il n'y en a pas : le plateau, étant
   plan et face à la lumière, en **gagne**. La sonde annonçait « fond plat : 0 px » sur un
   plateau parfaitement plat. **On mesure l'écart SIGNÉ, sans préjuger de son signe.**
2. **L'écart brut entre deux images est dominé par LE GRAIN** — un fil déplacé d'un pixel donne
   un couple +200/−200, quand la forme de l'empreinte vaut 20 à 50. On lisse sur 13 px avant de
   profiler. C'est le grain qu'on retire, jamais la forme.
3. **LA LUMINANCE NE DIT PAS LA GÉOMÉTRIE.** Sur une surface courbe vue de biais, une lumière
   directionnelle fabrique un **dipôle clair/sombre** qui noie le profil : ma coupe lisait ce
   dipôle et concluait « le fond n'est pas plat ». Il a fallu un **mode de mesure à éclairage
   plat** — tout grain vaut pareil, l'image devient la densité projetée du semis.
   *Et une quatrième, qui n'est pas un piège mais une erreur de métrique :* je normalisais par
   la valeur **au centre**, qui vaut zéro sur un plateau — c'est exactement ce qu'on cherche à
   prouver, et ça envoyait toutes les mesures à 300 %. **Le bon repère est l'amplitude.**

### LE FORK — trois partis pris, pas trois rendus

Ils ne peuvent pas coexister : un point ne peut pas être à la fois un grain libre, un maillon de
fil et une dalle d'un pavage. Chacun porte **sa** loi de contact.

```
A · LA POUSSIÈRE  des grains indépendants — on lit une DENSITÉ
                  contact : chacun pour soi, chassé vers l'extérieur
B · LE FIL        200 brins CONTINUS enroulés, colatitude ondulée (l'onde)
                  contact : un brin tendu N'ENTRE PAS dans le creux, IL L'ENJAMBE
C · LE PAVAGE     des dalles pleines séparées par des joints d'encre — un Voronoï
                  PONDÉRÉ sphérique, la Toile fermée sur elle-même
                  contact : rien ne se disperse, les dalles fusionnent en un SCEAU
```

⚠ **Ma première version de C ne gardait que les COUTURES** : ça donnait un **globe filaire**, vu
et revu, et vide. Sur la Toile c'est l'inverse — chaque dalle est **pleine**, ce sont les joints
qui sont en encre, et **chaque cellule porte son ton sur cinq marches**. C'est cette mosaïque qui
reste lisible en petit, là où une poussière n'est plus qu'un gris (contrainte du partage : les
silhouettes à relief fin disparaissent à 200 px).

**Le joint doit être plus large que le grain**, sinon le grain le comble et la partition
disparaît : joint 0,038 rad contre un grain de 3 à 5 px. C'est ce qui a fait passer C d'une
boule moussue à une mosaïque.

### CE QUE JE NE FAIS PAS PASSER POUR FINI

**Aucun des trois n'est encore un chef-d'œuvre**, et je le dis avant qu'on me le demande.
A est le déjà-vu assumé (témoin). B est fascinant **sous le doigt** et brouillon au repos.
C a une identité — c'est le seul qui soit Promi — mais il tire encore vers la peau de reptile :
ses dalles restent trop proches en taille, là où une Toile mêle des grandes et des petites.
**Le fork se tranche sur le parti pris, pas sur ce niveau de finition.**

---

## ⚑ LA DÉRIVE, ET UN EXTRAIT DU MOTEUR PÉRIMÉ · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`** · sauvegardes : `avant-derive.html`,
> `toile-extrait-avant-moteur.js`.

**Tom : « je ne vois aucun changement ».** Le serveur servait bien le fichier à jour (vérifié :
`MAS_TEINTE='encre'` présent dans la réponse HTTP) — c'était son cache. Mais deux choses
n'arrivaient réellement pas à l'écran, et les voici.

### ⚠ 1 · L'EXTRAIT DU MOTEUR DATAIT D'AVANT LE LOT DU MONDE FIGÉ

`scratchpad/toile-extrait.js` — la copie de la Toile que les planches utilisent — avait été
extraite **avant** le lot du 4 septembre. Son `dalleTrame` **ignorait silencieusement son
quatrième argument** : je passais le monde, le moteur n'en faisait rien, et les quatre sphères
« quatre mondes » sortaient **identiques**. Aucune erreur, aucun signal.

**Re-extrait depuis `app.html`** (même intervalle de texte, 60 186 octets, `mondeCourant` présent).
Les quatre mondes donnent maintenant quatre grains distincts.

**Leçon générale :** *une planche qui embarque une COPIE du moteur vieillit en silence.* Toute
planche doit vérifier ce qu'elle a — ici `Toile.mondeCourant` — au lieu de le supposer.

### ⚡ 2 · LA DÉRIVE — ce qui manquait au repos

Sans doigt, la sphère tournait **d'un bloc** : belle, et morte. Une masse vivante se **cisaille**.
Chaque bande de latitude glisse à sa propre allure, en permanence.

⚠ **Elle OSCILLE, elle ne s'accumule pas.** Une dérive cumulative décorrélerait les bandes en
quelques minutes : les fils se perdraient et la sphère finirait en bruit uniforme. Chaque bande va
et revient, sur des périodes premières entre elles (37 à 97 s). Et le **tangage respire**
(±0,028 rad sur 83 s).

```
MESURÉ SUR LES IMAGES, rotation d'ensemble NEUTRALISÉE — ce qui change tout seul
   après 1 s   24,68 % des pixels ont changé   ·  écart moyen 26,5
   après 2 s   27,84 %                            30,0
   après 4 s   30,47 %                            33,7
   après 8 s   33,36 %                            37,5
```

Coût : **six sinus par image**. `scratchpad/preuve_repos.py`.

### Les relevés

```
L'IMAGE          16,72 ms · écart-type 0,96 · 1 image > 33 ms sur 300 · coût 8,5 ms
LES DALLES       46 041 par image · teinte ENCRE (forme de la dalle, encre de l'écran)
LA VIE AU REPOS  24,7 % des pixels changent en 1 s, 33,4 % en 8 s
LE CRATÈRE       66,09 → 35,37 → 65,41 d'encre (posé, puis +3,5 s) — 99 % du retour
LA TRAÎNÉE       runH/runV 1,040 au repos → 1,564 en rotation
LE COMBLEMENT    +19 % sans lancer, +45 % avec, en 0,35 s
LES CONTRÔLES    0 recouvrement · 0 hors cadre · langue §6 tout à zéro
```

---

## ⚑ LA PREUVE EN PIXELS — mes chiffres décrivaient une intention · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`** · images : `scratchpad/preuve/`
> outils : `scratchpad/preuve_geste.py` (filme) + `scratchpad/mesure_png.html` (mesure l'image).

**Reproche de Tom, et il était fondé :** *« Rien de ce que tu annonces n'arrive à l'écran. Tes
mesures décrivent une intention, pas ce qui est peint. »* On filme trois séquences et on mesure
**les images rendues**, jamais le code.

### ⚠ DEUX PIÈGES D'INSTRUMENT, ET L'UN M'A FAIT CONCLURE FAUX

1. **Une capture prend 100 à 300 ms.** Photographier « pendant » une rotation lancée, c'est
   photographier **après** : l'élan s'est amorti, le déplacement est nul, et l'image ne montre
   aucune traînée **alors que le code en dessine 67 000**. J'ai d'abord conclu « la traînée
   n'existe pas » sur cette image. Il faut **entretenir la vitesse** pendant toute la capture.
2. **La fenêtre de mesure est fixe à l'écran.** Si la sphère tourne, on compare deux scènes
   différentes — et à pleine vitesse la densité peinte est divisée par trois. Pour le creux on
   **arrête la rotation** ; pour le comblement on **remet la vue exactement où elle était** avant
   de photographier. Sans ça, la première mesure disait « l'encre baisse après un lancer ».

### A · LE CRATÈRE EXISTE

```
rotation ARRÊTÉE · carré de 140 px au point touché · encre = luminance moyenne de l'IMAGE
   avant        66,09   33,33 % de pixels allumés
   posé         35,37    9,53 %     ← −46 % d'encre, −71 % de pixels
   tenu 0,5 s   35,37    9,53 %     ← il TIENT sous le doigt
   +0,5 s       51,31   21,93 %
   +1,5 s       61,42   29,77 %
   +3,5 s       65,41   32,80 %     ← revenu à 99 % de l'état d'avant
```

### B · LA TRAÎNÉE N'EXISTAIT PAS — les deux suspects de Tom étaient les bons

```
vitesse ENTRETENUE à 5,8 rad/s · 10 175 grains peints, 67 576 tampons de traînée
                  encre     part     runH     runV    runH/runV
   au repos       60,85   32,81 %     5,16     4,96     1,040
   en rotation    65,08   42,53 %     6,07     3,88     1,564   ← +50 %
```

Mesure : **la longueur moyenne des suites de pixels allumés**, dans le sens du mouvement et en
travers. Un grain qui traîne allonge l'une **et raccourcit l'autre** — c'est ce qu'on lit.

**Les deux causes, corrigées :**
- **Le pas était calculé, le nombre plafonné.** À pleine vitesse un grain parcourt 57 px par
  image ; quatre tampons dessus, ce sont quatre points isolés tous les 14 px. Maintenant le
  **pas est fixe (2,5 px)** et c'est la **longueur dessinée** qui est bornée (34 px).
- **Le tampon garde le plus opaque, et je peignais la traînée deux niveaux plus sourde** : dans
  une sphère dense elle passait sous n'importe quel grain et ne se voyait jamais. Sa tête est
  maintenant **au même niveau que son grain** ; c'est la queue qui s'éteint.

Le troisième soupçon (un grain sur deux au-delà d'une rotation/seconde) n'était **pas** la cause :
il réduit la densité, il n'efface pas les traînées. Il reste une approximation déclarée.

### C · LE COMBLEMENT PAR LA VITESSE

```
même creux, MÊME point de vue restauré avant la photo, 0,35 s après le lâcher
   SANS lancer    56,15 → 66,80   (+19 %)
   AVEC lancer    50,82 → 73,74   (+45 %)   ← plus de deux fois plus vite
```

### La teinte : basculée (décision Tom)

`MAS_TEINTE = 'encre'` — on garde la **forme** de la dalle du moteur, peinte dans l'encre de
l'écran. Le terracotta d'un monde est exactement « à tenir » ; la matière ne doit pas parler le
langage des états.

### ⚠ CE QUI RESTE, ET QUE JE NE FAIS PAS PASSER POUR FAIT

**Au repos, la sphère ne surprend pas.** Tout ce qui est fascinant naît du **geste** — le creux,
le flux, le comblement. Sans doigt, c'est une belle poussière qui tourne lentement, pas encore
« du jamais vu ». Je n'ai pas d'idée qui ne soit pas un effet gratuit, et je le dis plutôt que
d'en ajouter une.

**Contrôles :** 0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre
32 · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432.

---

## ⚑ LE GRAIN EST UNE DALLE — et je dis ce que ça coûte · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**. Sauvegarde : `sauvegardes/avant-dalles-grain.html`.

### Les cinq mesures demandées

```
L'IMAGE AU REPOS   17,3 ms · écart-type 3,0 · 10 images > 33 ms sur 291 · coût 8,6 ms
L'IMAGE AU DOIGT   18,7 ms · MÉDIANE 16,70 · 63 > 20 ms sur 531 · coût 9,4 ms
                   ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
LES DALLES         46 041 par image · 168 tampons dans l'atlas · tailles 3 · 4 · 6 px
LE CRATÈRE         écartement 34 px au cœur, rayon d'action 66 px
                   monte en 0,09 s · à moitié refermé 0,93 s · DURÉE DE VIE 3,52 s
LE COMBLEMENT      lancé à 0 rad/s → 3,50 s · 3 → 0,93 s · 8 → 0,42 s · 11 → 0,27 s
```

### ⚠ CE QUE JE DOIS DIRE EN PREMIER : le grain-dalle EN COULEUR abîme la sphère

Deux raisons mesurées, aucune n'est une question de goût.

1. **La palette d'un monde n'a pas l'écart de luminosité de la crème sur l'encre.** C'est cet
   écart qui faisait le volume : le limbe brillait, le fond s'éteignait. Avec des dalles
   colorées, **la sphère s'aplatit**. J'ai récupéré une partie du relief en faisant varier la
   TAILLE de la dalle avec la profondeur (devant +1 cran, au fond −1), mais pas tout.
2. **Le terracotta d'un monde est EXACTEMENT « à tenir ».** La matière se met à parler le langage
   des états, juste derrière six anneaux dont c'est le métier. **Conflit de sens.**

**Les deux versions sont livrées côte à côte sur la planche**, même phase, même vue.
**Mon avis : garder la FORME de la dalle et la peindre dans l'encre de l'écran.** C'est toujours
la vraie dalle du moteur ; l'Aura change toujours quand on change de monde — elle change de
**forme** au lieu de changer de **couleur** ; la sphère retrouve son volume ; les six redeviennent
le sujet. **Une ligne bascule tout** (`MAS_TEINTE`). Le cadre vivant est en teinte du monde parce
que c'est ce que Tom a demandé.

### ⚠ Une dalle coûte plus cher qu'un grain rond — mon banc parlait de carrés de 2 à 4 px

```
sur l'écran complet, dalles de 3 · 4 · 6 pixels d'appareil :
   39 500 → 16,72 ms · 1 image > 33 ms sur 300     ← le seuil PROPRE
   46 000 → 17,3 ms  · 10 à 13 sur 290             ← réglé ici
   63 100 → 19,1 ms  · 39 sur 262
   84 100 → 21,6 ms  · 68 sur 232
le coût FIXE (vider les quatre tampons + les verser) = 1,25 ms seulement.
Ce n'est pas la structure qui coûte, c'est le nombre de dalles.
```

Une dalle de 3 à 6 px couvre 9 à 36 pixels ; un grain rond en couvrait 4 à 9. **« 64 000 tiennent
à 16,67 ms » était vrai pour des carrés, pas pour des dalles.**

### Ce qui a été fait

- **Le grain est une vraie dalle du moteur** — `Toile.dalleTrame`, échelle 1, huit dalles ×
  trois tailles × sept niveaux de profondeur, pré-rendues dans l'atlas de tampons. Aucun
  `drawImage` (hors budget d'un facteur trois, mesuré au lot précédent).
- **Le creux est franc et il dure** : 34 px d'écartement sur 66 de rayon, poussée **radiale**,
  durée de vie **3,52 s** (c'était 1,13 s). ⚠ **Elle s'éteint en approchant du limbe** au lieu de
  rabattre les points dessus : la version qui rabattait les empilait et laissait une **baie
  vide** — un objet mordu, pas un objet qui encaisse.
- **Le creux se comble quand on lance**, proportionnellement à la vitesse (on retranche, on ne
  remplace pas) : 3,50 s au repos → **0,27 s à pleine vitesse**.
- **La traînée suit le VRAI chemin** : on garde la position de l'image précédente et on tamponne
  la dalle le long du segment réellement parcouru (jusqu'à 4 tampons tous les 2,2 px, plus petite
  taille, deux niveaux plus sourde). ⚠ **Avant, j'orientais un grain pré-étiré sur la dérivée de
  la rotation SEULE** : le doigt poussait dans un sens, la traînée pointait dans un autre.
  C'était ça, l'effet plaqué.
- **La rotation de repos passe de 84 s à 2 min 45.** C'est le geste qui accélère, pas elle.
- **Le lointain est plus rare** : une dalle sur trois aux deux niveaux les plus lointains, une
  sur deux aux deux suivants, toutes devant. Le fond DOIT être plus clairsemé.

### Ce qui reste vrai

0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre 32, 0 recouvert
sur 9 points × 72 positions × 4 vues · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432 ·
encre sous un mot 0,06 à 0,41 % (seuil 1 %) · une fiche atteignable en 0,11 s au pire.

---

## ⚑ LA SPHÈRE VIVANTE — LE GRAIN, LE CRATÈRE, L'ÉTIREMENT · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**. Sauvegarde : `sauvegardes/avant-grain-organique.html`.

### Les quatre mesures demandées

```
L'IMAGE AU REPOS   16,72 ms · écart-type 0,97 · 1 image > 33 ms sur 300 · coût 7,0 ms
L'IMAGE AU DOIGT   17,64 ms · MÉDIANE 16,70 · 27 images > 20 ms sur 533 · coût 8,6 ms
                   ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
LES GRAINS         42 045 par image · 777 tampons dans l'atlas
LE CRATÈRE         monte en 0,10 s · à moitié refermé en 0,21 s · REFERMÉ en 1,13 s
                   écartement 20 px · l'encre au cœur tombe de 80 à 3 (−96 %)
UNE FICHE          0,11 s au pire (40° de rotation, 63 px de course de doigt)
                   4 personnes sur 6 sont atteignables 100 % du tour ; les autres 89 % et 90 %
```

### ⚑ LE GRAIN N'EST PLUS UN PIXEL — c'est un TAMPON

Le carré aligné faisait « pixel Windows 98 », **et c'était la technique qui l'imposait** :
`putImageData` n'écrit que des entiers. On dessine le grain **une fois** dans un petit canevas
(rond, anticrénelé, bouts ronds), on lit ses pixels, et on les **tamponne**.

```
quatre toiles — L'INTERVALLE RÉEL ENTRE DEUX IMAGES
   carré au pixel   20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,67   64 000 → 16,67
   TAMPON DE GRAIN  20 000 → 16,79 ms   34 000 → 16,67   48 000 → 16,79   64 000 → 16,79
   drawImage        20 000 → 48,55 ms   34 000 → 80,35   48 000 → 112,49  64 000 → 151,11
```

**`drawImage` par grain est hors budget d'un facteur trois — c'est l'APPEL qui coûte, pas les
pixels.** Le tampon ne coûte rien de plus que le carré.

Le grain varie sur **trois axes** : trois épaisseurs (tirées d'une quatrième onde plus serrée que
celles qui creusent les vides) × quatre longueurs d'étirement × douze orientations. Le tampon
garde **le plus opaque**, jamais « le dernier ».

⚠ **Et l'anneau a suivi.** Il était en carrés alignés comme la sphère ; quand la matière est
passée au grain rond, il est resté en pixels — le défaut des « trois langages » revenait par
l'autre bout. **Le grain se décide à un seul endroit et tout le produit le suit.**

### La matière réagit

- **Les grains s'étirent dans le sens du mouvement**, proportionnellement à la vitesse. La
  direction vient de la **dérivée exacte de la rotation** (`Zs`, `sin(tangage)·X`), pas d'une
  différence de positions. Au repos, le plus rapide parcourt 0,2 px par image : aucun étirement,
  et on ne rentre même pas dans la branche.
- **Le cratère se referme** en exp(−t/0,28), et **les contacts s'empilent** (six au plus) : on
  peut toucher ailleurs tout de suite, rien ne se fige jamais.
- **Les traînées ne naissent que de l'accélération** — au repos, aucune. Effilochées : chaque pas
  dispersé d'un cran par un hachage stable, opacité qui saute.
- **Les prénoms s'effacent quand ça tourne vite et reviennent quand ça se pose.** En pleine
  rotation ils sont illisibles et le placement les envoyait loin de leur anneau : on voyait six
  mots errer autour de la sphère.
- **Les visages sortent de la matière** : le dégagement suit la profondeur (0,92 au fond, 0,12
  devant), bord tramé.

### ⚠ Trois pièges payés dans ce lot

1. **Un impact naissant était jeté avant d'avoir grandi.** Le filtre supprimait tout impact dont
   l'enveloppe valait moins de 2 % — or elle vaut zéro à sa première image. Le doigt ne creusait
   rien et le chronomètre rendait « refermé en 0 s » sur les trois seuils. On ne jette que ce qui
   est **lâché ET éteint**.
2. **Le creux était trop grand** (72 px de rayon, 30 d'écartement) : il mangeait un quart de la
   sphère et **cassait sa silhouette**. 56 et 20.
3. **Ma première sonde mesurait le mauvais point.** Elle plaçait l'impact en coordonnées de
   CADRE alors que le code travaille en coordonnées de la BOÎTE de matière (décalée de 23 · 100) :
   « aucun effet », alors que l'effet était de −96 %. Toujours vérifier le repère avant de
   conclure qu'un correctif ne mord pas.

### Trois optimisations, et ce qu'elles coûtent au dessin

1. **On ne stocke que les pixels qui existent, pas la boîte.** Un grain étiré en diagonale occupe
   12 × 12 pixels de boîte pour 30 peints ; chaque tampon est une **liste de décalages**.
   Le calcul d'une image en rotation : **11,1 → 8,6 ms**.
2. **Au-delà d'une rotation par seconde, un grain sur deux n'est pas dessiné.** 14,0 → 11,1 ms.
   C'est invisible en mouvement — mais c'est une vraie approximation, et elle est déclarée.
3. **Le seau d'orientation se calcule sans `atan2`** (six comparaisons de pente).

### Ce qui reste vrai

0 recouvrement · 0 hors cadre · langue §6 tout à zéro · ton Noyau rang 40 contre 32, 0 recouvert
sur 9 points × 72 positions × 4 vues · silhouette 167,0 contre enveloppe 166,0, 0 sortie sur 432 ·
encre sous un mot 0,04 à 0,27 % (seuil 1 %), clairière coupée : 6 sur 6 sont pris.
**Pas de zoom** (décision Tom). **`openPerson` n'existe pas sur la planche.**

---

## ⚑ LA SPHÈRE SE PREND AU DOIGT · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`).
> Planche : **`PLANCHE-AURA-SPHERE.html`**, premier cadre vivant ET manipulable.
> Sauvegardes : `sauvegardes/avant-prise-au-doigt.html`, `sauvegardes/avant-imagedata.html`.

### Ce qui change tout : le TEMPS et le POINT DE VUE sont séparés

Un seul nombre faisait tout — les six avançaient sur leur orbite ET la matière tournait, au même
rythme. **Impossible d'y poser un doigt : tourner l'objet aurait fait avancer le temps.**

```
LE TEMPS         les six voyagent sur leur orbite — un tour en 4 min. C'est la donnée.
LE POINT DE VUE  l'objet tourne sur lui-même — 84 s au repos, et le doigt le prend.
                 Deux angles (lacet, tangage) appliqués à TOUT — matière et personnes —
                 avant la projection. Il ne touche à AUCUNE donnée.
```

**Deux gestes, un seul capteur.** Une surface transparente sur la sphère, et on tranche **à la
levée** : au-delà de 6 px c'était une rotation, en deçà un toucher — et on cherche alors qui est
sous le doigt, le plus proche du regard d'abord. On ne peut pas écouter chaque anneau : le doigt
part souvent d'un anneau et le glissement serait mangé.

**L'élan s'ADDITIONNE à la rotation lente** au lieu de lui rendre la main : il n'y a pas d'instant
de reprise, donc **pas de saccade à la reprise**.

**La matière est entraînée** — six classes de retard prises sur la latitude dans le repère du
flux : l'équateur traîne, les pôles suivent. Cisaillement d'un fluide, pas d'un maillage. Coût :
six cosinus par image.

### ⚠ MON BANC PARLAIT D'UNE PAGE VIDE — et Tom a construit sa demande dessus

J'avais écrit « 26 000 points coûtent à peine plus que 13 000 ». **Vrai sur une page nue. Faux
sur l'écran complet** — mesuré : 14 700 → 17,5 ms · 18 400 → 17,6 · **22 300 → 21,9**.
Le plafond réel du `fillRect` était **13 000**, pas 26 000. J'ai cherché la cause au mauvais
endroit pendant six mesures (nombre de tranches, résolution de la toile, arrondi du cadre,
« une seule toile » — ce dernier test était **faux** : il ne dessinait qu'un quart des points).

**La vraie réponse était de changer de technique.** On n'appelle plus `fillRect` : on écrit les
pixels dans un `Uint32Array` par tranche, et on verse d'un seul `putImageData`. **Un appel de
dessin coûte plus cher que les quatre pixels qu'il pose.**

```
quatre toiles, points carrés sur la grille — L'INTERVALLE RÉEL ENTRE DEUX IMAGES
   fillRect   15 000 → 16,66 ms   24 000 → 16,67   34 000 → 16,79   48 000 → 24,36
   tampon     15 000 → 16,67 ms   24 000 → 16,67   34 000 → 16,67   48 000 → 16,67
```

⚠ **Ce que le tampon change au dessin, et c'est voulu :** il ÉCRASE au lieu de mélanger. Deux
points superposés ne s'additionnent plus — la matière ne se sature plus dans les zones denses.

### Une seule matière sur l'écran

**Un anneau est fait des mêmes points carrés que la sphère**, au même pas (`MAS_GRAIN`), sur la
même grille. Ce n'est plus un trait plaqué sur un fond : c'est la sphère qui se resserre en
cercle. Deux conséquences que la matière a IMPOSÉES :
- **l'arc d'une personne passe de 4 à 7** — à 4 px le grain n'a la place que de deux rangs et
  l'anneau disparaît ;
- **le visage RENTRE dans l'anneau** — §2.9 donne 0,62 du diamètre, on était à **0,94** : l'anneau
  n'était qu'un liseré autour d'un disque plein. C'était ça, les « trois langages ».

### ⚠ Un contrat de test réécrit — « rien ne passe devant ton Noyau »

**La règle n'a pas changé ; sa garantie a changé de nature.** Avant : la géométrie, et ça tenait
*parce que le point de vue était fixe*. Le doigt tournant l'objet dans tous les sens, n'importe
qui peut être amené sur l'axe du regard et **aucune inclinaison ne peut l'empêcher** — Tom l'a
écrit : *« quelqu'un de proche est près du centre, donc partiellement masqué par ton Noyau, et
c'est juste »*. Après : **l'ordre de tracé**, et le contrôle est plus dur :

1. aucun anneau n'atteint jamais le rang de ton Noyau — **72 positions × 4 points de vue**, rang
   le plus haut atteint **32**, ton Noyau à **40** ;
2. **au doigt**, sur neuf points de son disque : **0 recouvert**.

Version d'origine dans `sauvegardes/coll_sphere-avant-vue-libre.py` et
`sauvegardes/ctrl_sphere-avant-vue-libre.py`. Le seuil `derriere` du contrôle de collisions passe
de 20 à 40 pour la même raison. **Et le capteur du doigt sort du test de boîtes** — surface
transparente qui ne peint rien, 91 faux positifs ; sa vraie question est mesurée au geste.

### Les relevés

```
LA MASSE            36 fils · 42 045 points · 4 tranches · 7 niveaux francs
L'IMAGE AU REPOS    16,67 → 16,72 ms · écart-type 0,06 → 0,96 · 0 à 1 image > 33 ms sur 300
                    coût 6,5 ms par image
L'IMAGE AU DOIGT    16,85 ms · médiane 16,70 · 95e centile 16,80 · 2 images > 20 ms sur 457
                    ⚠ la pire (100 ms) est la TROISIÈME : l'instant où le doigt se pose
                    coût 6,7 ms par image
L'ÉLAN               2 rad/s → sous la lente en 1,81 s, éteint en 4,31 s, 0,22 tour
                     5 rad/s → 2,31 s · 4,81 s · 0,49 tour
                    11 rad/s → 2,74 s · 5,24 s · 1,01 tour
LES DEUX GESTES     immobile → Marion · 4 px → Marion · 41 px → rien. Seuil 6 px.
TON NOYAU           rang 40 contre 32 · 0 recouvert sur 9 points
LES SIX DEDANS      silhouette 167,0 · enveloppe 166,0 · 0 sortie sur 432
LA PROFONDEUR       25,4 → 61,8 px · rapport 2,44
LES CONTRÔLES       0 recouvrement · 0 hors cadre · langue §6 tout à zéro
L'ENCRE SOUS UN MOT 0,26 à 0,75 % (seuil 1 %) — clairière coupée : 6 sur 6 sont pris
```

### Deux choses que je n'ai pas faites, et une que je pose

**Pas de zoom** (décision Tom, reprise telle quelle). **Le tangage ne revient pas tout seul** à
sa valeur de repos : une sphère qu'on penche reste penchée, c'est la manipulation de l'utilisateur,
pas un réglage — seulement bornée à ±1,15 rad pour ne pas basculer par-dessus le pôle. Si Tom
préfère qu'elle se redresse doucement, c'est une ligne. **`openPerson` n'existe pas sur la
planche** : le toucher affiche un bandeau qui dit quelle fiche s'ouvrirait ; le geste est réel et
mesuré, le branchement est un lot d'intégration.

---

## ⚑ LA SPHÈRE — LA MASSE D'ABORD, LES SIX ENSUITE · 5 septembre 2026

> **`app.html` inchangé** (md5 `61280542751d0d0df5bce546f9a091b1`, le même que depuis le lot
> du moteur). Planche : **`PLANCHE-AURA-SPHERE.html`**, premier cadre vivant.
> `PLANCHE-AURA-RETENU.html` reste comme trace de l'orbite à six anneaux.

### Le principe, en une phrase

**La sphère est un tissu de trajectoires ; six d'entre elles portent un visage.**

Six anneaux ne feront jamais une sphère, quelle que soit la finition — c'est pour ça que dix
versions ont échoué. **Le volume vient de la DENSITÉ** : vingt-trois fils enroulés d'un pôle à
l'autre, pointillés, ~11 000 points. Chaque fil est un chemin, du même genre que celui que
parcourent les six. La masse ne dit rien d'autre : c'est vivant.

### ⚠ MON PREMIER BANC MESURAIT LE MAUVAIS CHIFFRE — et c'est la leçon du lot

**Le canevas 2D EMPILE les ordres, il ne les exécute pas.** Le temps d'appel de `stroke()` n'est
pas le temps de peinture. Mon premier banc annonçait **0,25 ms pour 4 000 traits** ; l'écran
tournait à **douze images par seconde**. Un banc qui chronomètre les appels ne mesure rien.

**Le bon banc mesure l'intervalle réel entre deux images** (`scratchpad/banc3.py`) :

```
traits    2 400 → 16,9 ms    6 500 → 25,2 ms    13 000 → 50,4 ms
points   13 000 → 17,4 ms   26 000 → 18,4 ms
à couverture CONSTANTE (60 000 px de trait), le coût est dans le NOMBRE :
   15 000 morceaux de 4 px → 59 ms        940 morceaux de 64 px → 20 ms
```

**Le plafond des traits est 2 400. Un point ne coûte presque rien.** La sphère est donc
POINTILLÉE — et un point posé sur un chemin dit encore le chemin. Deux instruments indépendants
concordent : Chromium sans fenêtre, et le navigateur de l'app (mesuré par `javascript_tool`).

### ⚠ ET LA TRAÎNÉE COÛTAIT PLUS CHER QUE LA SPHÈRE

Douze images perdues sur 289. J'ai d'abord accusé la masse et retiré des points — sans effet.
**Profilé, fonction par fonction** (`scratchpad/profil.py`) :

```
la masse    1,94 ms en moyenne · 2,10 au pire   sur 12 900 points
la traînée  0,27 ms en moyenne · 20,30 AU PIRE  sur 200 segments
```

Deux causes, deux correctifs : **sa toile faisait 390 × 844** (1,3 million de pixels effacés par
image) alors que tout ce qu'elle dessine tient dans la sphère → **344 × 344** ; et elle appelait
`stroke()` **une fois par segment**, 200 fois par image — le banc l'avait pourtant dit. Les
segments sont maintenant **groupés par niveau d'opacité** : 6 strokes par personne au lieu de 20.
Et **plus aucune allocation par image** (le ramasse-miettes rendait une image à 20 ms une fois
sur cent cinquante).

```
la traînée au pire   20,3 ms → 0,40 ms
une image au pire    22,6 ms → 3,30 ms
```

### Ce que la sphère a imposé, et que je n'avais pas prévu

**UN SEUL FOYER POUR TOUTE LA SCÈNE — 270.** À deux foyers (180 pour les six, 620 pour la
matière), un anneau au premier plan **sortait de la silhouette de 25 px**. Ce n'était pas un
défaut de dessin : c'était l'incohérence de deux projections. Avec un seul foyer, un corps qui
est DANS la sphère se projette DANS la silhouette, toujours.

**QUATRE TRANCHES DE PROFONDEUR, et c'est ce qui met les six DEDANS.** Une seule toile sous tout
le monde et les anneaux flotteraient dessus. La sphère est tranchée en quatre dalles ; chaque
tranche prend **le z-index que la formule des anneaux lui donnerait** (`20 + z/10`). Un anneau
qui s'enfonce passe derrière la matière ; celui qui vient vers toi passe devant. La tranche la
plus proche reste sous ton Noyau : **rien ne passe jamais devant toi.**

**LA MATIÈRE SE RETIRE SOUS UN PRÉNOM — sans plaque, sans ombre, sans voile.** Un mot posé sur
onze mille points n'est plus lisible. On **efface les points sous le mot** (`destination-out`),
dans les quatre tranches, **à 0,88** : il reste un huitième des points, et le bord de la clairière
ne se lit plus. La forme est une **pilule, rayon = hauteur ÷ 2** — la grammaire du §5, appliquée
à un vide. **Et elle s'allège devant un anneau** (0,76, et seulement dans les tranches vraiment
devant lui) : « toujours nets » est la règle, mais tout effacer enlèverait ce qui les met dedans.

**UN PRÉNOM SANS SON ANNEAU EST UN BUG.** Quand quelqu'un passe derrière ton Noyau, il la masque.
Son prénom, posé vers l'extérieur, resterait seul à flotter : il s'efface avec elle.

### Ce que ce lot COÛTE — je le dis avant qu'il le voie

**Le rapport de profondeur tombe de 3,43 à 2,20.** C'est le prix du foyer unique. En échange, la
profondeur n'est plus portée par la taille toute seule : elle est portée par **l'occultation**,
un indice bien plus fort.

**Les rayons s'ouvrent de 116 à 118 — deux pixels, et c'est tout ce que j'ai pu prendre.**
**La borne a changé de nature** : ce n'est plus le cadre, c'est la sphère. À 122, l'enveloppe des
six passe au-dessus de la silhouette et quelqu'un sort — ce qui contredirait la règle « ils sont
dedans ».

### ⚠ Le contrôle de collisions est AVEUGLE à la masse — et il faut le dire

Le canevas de la masse couvre 344 × 344 : au test boîte-contre-boîte il recouvre tout, et il est
en `pointer-events:none`, donc **la confirmation au doigt ne le rend jamais**. Je l'exempte de ce
test — qui ne mesure rien pour lui — et je mets à la place une **mesure de pixels**, plus dure :
combien d'encre la masse pose-t-elle sous un prénom, et devant un anneau (`scratchpad/ctrl_sphere.py`).

**⚠ Et cette mesure s'est trompée deux fois avant de tenir.** (1) Elle comptait des *pixels
allumés* : un point à 0,94 d'opacité en garde 0,11 après la clairière — au-dessus de tout seuil de
comptage, alors qu'il ne se voit plus. Elle mesure maintenant **l'encre déposée**, la somme des
alphas. (2) Son critère était **relatif** (« l'encre doit tripler ») : ça ne veut rien dire là où
la sphère est déjà creuse. Il est **absolu** : sous le mot, l'encre doit rester **≤ 1 %**.
(3) Et `_nomsALaCible` posait les prénoms à leur cible **sans repeindre la matière** : le trou
restait à l'ancienne place et le contrôle relevait de l'encre qui n'est pas à l'écran.

### Les relevés

```
L'IMAGE (5 passes)   16,72 → 16,83 ms · écart-type 0,97 → 1,66
                     coût d'une image 2,45 ms en moyenne, 3,70 ms au pire
                     images au-delà de 33 ms : 1 à 3 sur 300 (0,3 à 1 %)
                     ⚠ une passe sur six sort à 487 ms : machine saturée, pas le produit
                       — on relance, c'est le piège documenté du §7
LA SPHÈRE            23 fils · 10 928 points · 4 tranches · 7 niveaux francs
                     silhouette 167,0 px · rayon 142 · foyer 270
LES SIX SONT DEDANS  enveloppe 163,4 px · 0 sortie sur 432 (6 × 72 positions)
TON NOYAU            0 anneau devant lui sur 72 positions
LA PROFONDEUR        23,3 → 51,1 px · rapport 2,20
LA BOÎTE             55 · 149 → 321 · 414
LES CONTRÔLES        0 recouvrement · 0 hors cadre · langue §6 tout à zéro
L'ENCRE SOUS UN MOT  0,16 à 0,57 % (seuil de lisibilité 1 %)
                     clairière coupée : 5 prénoms sur 6 passent au-dessus → la mesure mord
L'ENCRE DEVANT       0,3 à 2,7 % de la boîte d'un anneau
```

### Ce qui n'a PAS changé

Le Noyau au centre avec ton visage, le mot en gros dessous, le chiffre en Fraunces 34 px avec sa
couleur d'état, la légende, la moisson avec chaque dalle dans son monde d'alors, le rejeu au doigt
et ses douze phrases, le bouton « Partager mon Noyau ». **Seule l'orbite a bougé.**

---

## ⚑ LE SACCADE — LA CAUSE ÉTAIT AILLEURS, ET JE L'AVAIS MANQUÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, premier cadre vivant.

### Les trois mesures demandées

```
1 · INTERVALLE ENTRE DEUX IMAGES   16,67 ms · écart-type 0,06 ms
                                   médiane 16,70 · 95e centile 16,70 · pire 16,80
                                   0 image au-delà de 20 ms sur 301 · 0 au-delà de 33
2 · COÛT D'UNE IMAGE               0,39 ms en moyenne · 1,90 ms au pire
3 · RAPPORT PETIT / GROS ANNEAU    20,6 px → 68,8 px  ·  3,34
```

**La boucle était déjà parfaite** — rAF, temps continu, position dérivée de l'horloge, aucun
compteur d'images, aucun `setInterval`. **Et une image coûte 0,4 ms.** Ni l'un ni l'autre
n'était le problème.

### ⚠ LA VRAIE CAUSE : les prénoms se téléportaient

```
un anneau avançait de 0,024 px par image        → invisible
CHAQUE PRÉNOM SAUTAIT 46 FOIS EN 10 SECONDES    → jusqu'à 112,6 px d'un coup
```

**Le placement au moindre coût BASCULAIT d'un créneau à l'autre au moindre frémissement** — et
comme la scène, elle, ne bougeait pas visiblement, **le seul mouvement de l'écran était un nom
qui se téléporte**. J'avais accusé la fréquence de ce calcul ; c'était son **instabilité**.

**Trois correctifs, chacun mesuré :**

```
1 · on ne garde un créneau QUE tant qu'il est PARFAIT (il ne recouvre rien), et on
    prend le meilleur dès qu'il cesse de l'être — les bascules entre créneaux
    ÉGALEMENT bons disparaissent
2 · le prénom GLISSE vers sa cible au lieu d'y sauter (le calcul reste à 4 Hz, le
    mouvement se fait à chaque image)
3 · AUCUN PAS NE DÉPASSE 1,2 px — sous ce seuil un déplacement ne se voit pas.
    Un glissement proportionnel seul faisait un premier pas de 4,3 px.
```

```
avant : 46 sauts/nom, le plus gros 112,6 px
après :  0 saut · le plus grand pas est 1,2 px, et c'est le plafond
```

**Et la vitesse : 132 s → 84 s.** À 132 s un anneau avançait de 0,024 px par image : la scène
paraissait **figée**, ce qui rendait le moindre frémissement de prénom d'autant plus visible.

### Le contrôle juge désormais l'état POSÉ

Un prénom qui glisse peut croiser un anneau pendant une demi-seconde — **c'est un déplacement,
pas un recouvrement au repos.** Le contrôle pose les prénoms à leur cible avant de mesurer, et
le dit.

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
boîte de l'orbite sur un tour : 20 · 138 → 353 · 444
langue §6 : tout à zéro
```

⚠ **Les rayons restent 80 → 116.** J'ai réessayé de les ouvrir à 122 comme tu le demandais :
la boîte sortait par la gauche (x = 3) et passait sous « solide » (y = 454). **116 à 268 est
la borne**, mesurée.

---

## ⚑ LA GRAVITATION LENTE — ÉTAT COURANT · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-RETENU.html`**, premier cadre vivant.
> Le rejeu et sa jauge sont **sortis** (décision Tom : un écran qui a besoin d'une légende
> est raté). `PLANCHE-AURA-DEUX-SORTIES.html` reste comme trace.

### Ce qui a changé

```
LA VITESSE     un tour en 48 s → 2 min 12. Assez lent pour qu'aucun mouvement ne se
               remarque, assez pour que la scène ait changé si on la laisse.
LES PLANS      COMPOSÉS À LA MAIN, plus tirés de l'alphabet. Trois plans presque
               couchés se croisent près du centre, deux redressés balaient large,
               un coupe en travers ; les phases sont décalées pour qu'aucun alignement
               régulier ne se produise. LE RAYON RESTE LA DATE — la seule chose
               qu'on ne compose pas.
LA TRAÎNÉE     0,12 → 0,085 du tour · opacité 0,34 → 0,30 · 28 pas.
               Elle est, et elle était déjà, la PROJECTION DU VRAI CHEMIN 3D :
               on échantillonne les positions passées dans l'espace, on projette
               chacune, on relie. Elle s'incline avec l'orbite, s'écrase de profil,
               passe sous ton Noyau quand le chemin y passe.
LE RETOUR      UNE FOIS, À L'OUVERTURE. La personne avec qui tu viens de tenir rentre
               vers le centre en 1,5 s (lissage d'ordre 5), puis l'écran se repose.
               C'est la seule chose que le rejeu laisse derrière lui.
LA FLUIDITÉ    les prénoms se replaçaient 60 fois par seconde (6 noms × 32 essais) :
               4 fois par seconde. C'était ça, le saccade.
```

### ⚠ Ce qui n'a PAS pu être récupéré de l'image fixe

**Les rayons ouverts à 77-149 ne survivent pas à la rotation.** Mesuré : à 128 la boîte sort
de **4 px à gauche** et de **56 px en bas** (elle mordait « solide »). Avec les plans composés
— qui portent les points plus loin que les plans tirés de l'alphabet — **la borne est 116**.
Les rayons sont donc **80 → 116**, pas 77 → 149. J'ai dû aussi **redresser trois inclinaisons**
(74° → 60°) : c'est Nico, le plus lointain, qui sortait par le bas.

```
profondeur : le plus petit 20,6 px · le plus gros 68,8 px · rapport 3,34
la boîte sur un tour : 20 · 142 → 353 · 448
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ LE REJEU — LA JAUGE, ET UNE RÉSERVE QUE JE POSE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-DEUX-SORTIES.html`** — les deux cadres
> sombres sont vivants. Captures : `scratchpad/sorties/`.

### La période est MESURÉE, pas supposée

Critère de Tom : jamais plus de 2-3 s sans événement.

```
période       jours  évén.  écart moyen  trou max   durée pour ≤ 3 s
7 jours           7      2       3,5 j      4 j          5,2 s   illisible
4 semaines       28      6       4,7 j     11 j          7,6 s   illisible
8 semaines       56     15       3,7 j     11 j         15,3 s   ← la seule qui tient
```

**Le trou qui commande tout : jour 33 → jour 44, onze jours sans une seule parole tenue.**
**Retenu : huit semaines en 15 s** — silence max **2,95 s**, écart moyen **1,00 s**.

⚠ **C'est plus RAPIDE que les 28 s d'avant, pas plus lent.** L'impression de vitesse venait
du **saccade**, pas de la durée. Si après le lissage ça paraît encore rapide, 18 s coûte
0,6 s de silence en plus (3,54 s).

### La jauge — trois différences d'un coup avec l'arc d'harmonie

```
elle est DEHORS            rayon 54 contre 36
elle est TROIS FOIS PLUS FINE   5 contre 18
elle n'a AUCUNE PISTE      un arc ouvert qui pousse, pas un anneau fermé
sa teinte est L'ENCRE      aucune des trois couleurs d'état : aucune valeur lisible
```

### La fluidité — deux causes, mesurées

```
les prénoms se replaçaient 60 fois par seconde   (6 noms × 32 essais) → 4 fois par seconde
les QUATRE cadres se repeignaient à chaque image → seuls les deux SOMBRES sont vivants
le retour vers le centre : 2,2 j → 3,5 j, lissage d'ordre 5 (aucun à-coup)
```

### ⚠ EST-CE COMPRÉHENSIBLE ? — non, pas entièrement, et je le dis

**Ce qui se lit :** le **retour vers le centre** est net — on voit qu'il se passe quelque chose,
et la jauge dit qu'on rejoue une période.

**Ce qui NE se lit pas : la dérive.** Entre deux paroles, une personne ne s'écarte que de
quelques pixels en trois secondes. **« ça s'écarte » ne se lit pas comme « le temps passe »** —
il faut le savoir. J'ai ajouté la ligne **« ces huit dernières semaines, rejouées »**, sans
laquelle rien n'est compréhensible ; elle dit qu'on rejoue, elle ne dit pas pourquoi ça s'écarte.

**Ma réserve, entière :** le rejeu demande une explication pour la moitié de ce qu'il montre.
**Le moment où le retour vers le centre se lit sans un mot, c'est celui que tu avais déjà
nommé** — une fois, à l'ouverture, quand tu reviens après avoir tenu : là on vient de tenir,
on voit la personne rentrer, et la cause est évidente parce qu'on l'a provoquée.

```
4 cadres · 0 recouvrement · 0 hors cadre · langue §6 : tout à zéro
```

---

## ⚑ L'AURA — LE REJEU OU L'IMAGE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-DEUX-SORTIES.html`**, les deux premiers
> cadres sont vivants. Captures : `scratchpad/sorties/`.

### Le diagnostic de Tom, repris à mon compte

*« Six anneaux qui tournent en boucle, à vitesse constante, sans qu'aucun événement ne se
produise : ça bouge sans rien raconter. »* **Neuf lots à affiner la finition d'un mouvement qui
n'avait pas de sujet.** C'était le mauvais problème.

### 1 · LE REJEU — le mouvement dit le temps

L'orbite **ne boucle pas** : elle rejoue les huit dernières semaines en 28 s. Chaque personne
**s'éloigne parce que les jours passent**, et **revient d'un coup vers le centre quand une
parole est tenue avec elle**. Les angles ne bougent jamais ; seule la distance respire. La lune
apparaît selon ce qui était en chemin **ce jour-là**.

### 2 · L'IMAGE — une constellation fixe

Elle ne bouge plus. **Tous les anneaux à la même taille** — la seule façon d'être sûr qu'aucune
dimension ne dise une valeur ; ce sont les **places** qui font l'image.
**Les angles sont composés à la main** (autorisé par Tom : le rayon reste la date).
**Les rayons s'ouvrent : 77 → 149** au lieu de 80 → 122 — une image fixe n'a pas de tour à
dégager. **Seule bouge la lune.**

```
la grappe   Maman 77 · Adrien 89 · Marion 108, en haut à gauche — trois distances, deux Nuées
le vide     de 78° à 205° : tout le quart bas-gauche, VOULU
le lointain Nico 149, seul, au bord — cent cinquante jours
```

### Le verdict : la 2 — mais pas pour la raison donnée

**Le rejeu ne tourne pas dans le vide** : il raconte quelque chose de vrai. **Ce qui le
disqualifie, c'est le rythme.** Quinze paroles tenues en huit semaines = quinze événements en
28 s ; entre deux, la scène ne fait que **s'écarter lentement, toutes ensemble, dans la même
direction**. Ce n'est pas une histoire, c'est une dérive. Et si rien n'a été tenu depuis un
mois, l'écran ne fait que reculer, en boucle.

**La 2 tient pour une raison plus simple : l'Aura est un ÉTAT, pas un film.** On l'ouvre pour
savoir où on en est. Une image se lit en une seconde ; un rejeu demande d'attendre.

**Ce que le rejeu mérite quand même :** le mouvement qu'il invente — **le retour vers le centre
quand une parole est tenue** — est exactement ce qui devrait se passer **à l'instant où tu
tiens**. Pas en boucle : **une fois**, quand tu reviens sur l'Aura après avoir tenu. À trancher.

### ⚠ Une règle re-cassée, et reprise

J'avais glissé **une dalle sous le visage** dans chaque anneau. Fausse deux fois : invisible, et
contraire à ce que Tom avait déjà tranché — *« une dalle est la matière d'une PROMESSE »*, pas
d'une personne, et le Noyau agrège toutes tes promesses. **Retirée partout.**

```
4 cadres · 0 recouvrement · 0 hors cadre · langue §6 : tout à zéro
```

---

## ⚑ L'ORBITE AFFINÉE — LA MATIÈRE SERT LA LECTURE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-RETENU.html`**, premier cadre **vivant**.
> Les trois directions de matière (`PLANCHE-AURA-TROIS-DIRECTIONS.html`) sont **abandonnées** —
> gardées comme trace, pas comme candidat.

### La décision de Tom, et pourquoi elle est juste

*« Le diagnostic était juste : l'orbite manquait de matière. La réponse ne l'était pas — mettre
de la trame partout a tué la lisibilité. La matière doit servir la lecture, pas la remplacer. »*

**Les trois directions étaient illisibles.** L'erreur : avoir traité « il manque de la matière »
comme « il faut remplacer les formes par de la matière ». Retour aux **anneaux nets**, et on
affine la composition au lieu d'empiler de la texture.

### Ce qui a changé

```
TON NOYAU     l'arc s'amincit PAR L'INTÉRIEUR : 26 → 18. Le bord extérieur ne bouge
              pas (anneau() trace à R = (d − lw)/2), donc les 8 px rendus vont TOUS
              au creux — et le visage retrouve sa place : 27 → 40.
LA TRAÎNÉE    discrète. Longueur 0,24 → 0,12 du tour · opacité 0,92 → 0,34 ·
              largeur × 0,52 · bouts FRANCS (les bouts ronds qui se chevauchaient
              composaient des perles : la traînée redevenait un motif qu'on regarde).
L'ANNEAU      inchangé — net et simple. C'est ce qui le rendait lisible.
LA COMPOSITION  l'écart des rayons s'ouvre : 118 → 122 (mesuré : 136 sortait du cadre
              par la gauche et mordait le plateau). Profondeur : rapport 3,48.
```

### L'idée ajoutée — et c'est une SOUSTRACTION

**La traînée s'éteint derrière.** Chaque pas est éclairé par sa **profondeur** : vif quand il
vient vers toi, presque nul quand il s'enfonce. Comme une comète.
**Ça divise le bruit par deux ET ça renforce le volume** — la moitié arrière du chemin ne se
dessine plus, elle se devine. Elle ne coûte qu'une ligne : si elle nuit à la lecture, elle sort.

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ L'AURA — TROIS DIRECTIONS DE MATIÈRE · 4 septembre 2026

> **`app.html` inchangé.** Planche : **`PLANCHE-AURA-TROIS-DIRECTIONS.html`** — les trois
> cadres du haut sont **vivants**. Captures : `scratchpad/directions/`.

### Pourquoi le canevas de `/design` ne pouvait pas porter ce lot

**Un canevas `/design` est publié dans un artefact SANS RÉSEAU SORTANT** : il ne peut charger
ni `toile-extrait.js`, ni le moteur, ni rien du produit. Y dessiner la matière aurait voulu dire
**la refaire à la main** — exactement le défaut que Tom venait de nommer (« tu dessines l'orbite
avec les outils d'un diagramme »). Le travail est donc revenu ici, **où le vrai moteur tourne**.

### La règle du moteur que ça impose

**CLAUDE.md §4 : une dalle se rend UNE FOIS, pas une fois par case.** Chaque dalle est peinte
une seule fois dans un canevas caché, puis **tamponnée** — même pixel à toutes les tailles,
sans jamais rappeler le moteur. C'est ce qui rend une traînée de 46 pas tenable.

### Les trois directions

```
A · LES DALLES GRAVITENT   une personne n'est plus un anneau : c'est SA DALLE, du monde
                           de sa dernière parole tenue. L'arc du §2.9 devient un mince
                           CERCEAU autour d'elle. La traînée est la même dalle tamponnée
                           vingt fois — une traînée d'encre, pas un arc dégradé.
B · LA TOILE EST LE CIEL   le fond n'est pas noir : c'est une vraie Toile (Toile.preview),
                           sourde, qui respire. Les gens sont des dalles vives dedans.
                           AUCUNE traînée — le ciel EST la texture.
                           Son risque : deux matières se disputent l'oeil.
C · L'ANNEAU DE MATIÈRE    vu presque de profil, inclinaison commune à 78°. Les traînées,
                           denses (46 pas), se fondent en RUBANS de trame qui s'enroulent
                           autour du Noyau — un ruban de mosaïque, un d'encre, un de
                           terrazzo. Le plus décalé des trois.
                           Ce qu'il perd : chacun n'a plus son plan propre.
```

**Ce qui ne bouge dans aucune des trois :** le rayon dit la date · la vitesse est commune ·
la lune est binaire · la couleur est catégorielle · aucune dalle ne passe devant ton Noyau
(inclinaison cherchée, moitié avant seulement) · les prénoms restent des nœuds droits, à taille
fixe, placés par essais.

**Le Noyau revient à l'arc 20** — le pâté de 26 est corrigé — et il porte **ta dalle**.

```
6 cadres · 0 recouvrement · 0 hors cadre
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'ORBITE — LA TRAÎNÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, **premier cadre vivant**.

### L'idée : la traînée

**On ne voyait pas le VOLUME parce qu'on ne voyait pas les CHEMINS** — six objets bougeaient,
le cerveau n'avait rien à reconstruire. Chaque personne traîne maintenant **un arc de sa propre
orbite** : une trace, pas un filet.

```
elle s'affine et s'efface en s'éloignant de l'anneau
sa LARGEUR suit la perspective — fine au loin, large au premier plan
elle est peinte SOUS ton Noyau : elle disparaît derrière lui et reprend de l'autre côté
   → c'est ÇA qui dit la profondeur, mieux que la taille
elle porte la couleur de la NUÉE, comme la piste de l'anneau
```

**La lune en a une aussi**, minuscule, et tourne à **sa** vitesse — six tours quand l'orbite en
fait un. **Un point qui traîne dit qu'il tourne ; un point posé ne dit rien.**

### La profondeur, poussée et mesurée

```
foyer 420 → rapport 1,3     on voyait un cercle
foyer 230 → rapport 2,59    encore timide
foyer 180 → rapport 3,43    le plus petit 20,0 px · le plus gros 68,8 px
inclinaisons 38° à 78° · échelle bornée [0,44 · 2,15] · anneaux 36 → 32
ton Noyau reste à 90 : rien ne l'atteint jamais
```

### Le Noyau : l'arc double sans grossir

`anneau()` trace à **R = (d − lw)/2** : le bord extérieur reste à **45**, donc **tout l'ajout
mange le centre**. Arc **13 → 26**, creux **64 → 38**, visage **48 → 27**.

⚠ **À signaler : il en devient épais au point de tirer vers le disque.** C'est la conséquence
directe de l'épaisseur demandée. **L'arc à 20 garderait le geste sans le pâté** — à trancher.

### Les douze phrases sont closes

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Évidemment. · Parole tenue. · C'est bien toi. · Comme d'habitude.
Tu ne t'es pas fait prier. · On n'en attendait pas moins. · Tiens donc.
```

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro
```

---

## ⚑ L'ORBITE — LA PROFONDEUR, MESURÉE · 4 septembre 2026

> **`app.html` inchangé.** Planche : `PLANCHE-AURA-RETENU.html`, **premier cadre vivant**.

### La cause du « cercle » n'était pas seulement le foyer

**Deux causes, et la seconde était la mienne.** Le foyer à 420 aplatissait, oui — mais surtout
**j'interdisais tout recouvrement du centre**. Les orbites le **contournaient** : personne ne
passait jamais derrière, tout le monde restait à côté. **C'est ça qui faisait un cercle.**

**La règle corrigée : ce qui est interdit, c'est de passer DEVANT.** La recherche d'inclinaison
ne teste plus que la **moitié avant** ; derrière, ton Noyau masque, franchement.

```
foyer            420 → 230        inclinaisons 20-64° → 34-66°
anneaux          44 → 36          échelle bornée à [0,52 · 1,92]
LA PROFONDEUR    le plus petit 24,9 px · le plus gros 64,7 px · RAPPORT 2,59
                 (à 420 il valait 1,3 — on voyait un cercle)
ton Noyau        90 · rien ne l'atteint jamais
la boîte         45 · 139 → 350 · 407 — dégagée du plateau et du mot
```

⚠ **Un premier essai à foyer 170 a donné un rapport de 4,89** — et un anneau au premier plan à
**129 px**, presque ton Noyau : la hiérarchie s'effondrait et la boîte sortait du cadre.
**Bornée**, la profondeur reste franche sans rien casser.

### Les cinq réglages de mise en page

```
l'orbite descend        centre 262 → 288, et se resserre (rayons 92-140 → 80-118)
le mot et le chiffre    440 → 448 · 526 → 534
la légende              26 px d'air au-dessus, 33 en dessous
« tout ce que tu as tenu »   27 px avant les dalles, au lieu de 11
```

### ⚠ Le placement des prénoms, troisième version

Huit essais avec **repli aveugle** laissaient treize noms l'un sur l'autre. Maintenant :
**trente-deux candidats, chacun évalué par la SURFACE qu'il recouvre**, et on garde le
minimum — ton Noyau pesant quatre fois, un autre nom trois fois. La position parfaite quand
elle existe, la moins mauvaise sinon. **0 recouvrement.**

### Les douze phrases

Cinq sortent sur décision de Tom (plates ou gênantes). Cinq neuves, au calibre du clin d'œil :

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Évidemment. · Parole tenue.
C'est bien toi. · Comme d'habitude. · Tu ne t'es pas fait prier.
On n'en attendait pas moins. · Tiens donc.
```

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau DEVANT ton Noyau sur 72 positions
langue §6 : tout à zéro · les 4 sondes du contrôle passent toujours
```

---

## ⚑ L'ORBITE EN 3D — UN SYSTÈME PLANÉTAIRE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`,
> **le premier cadre est vivant** — un tour en 48 s. Captures : `scratchpad/retenu/`.

### La mécanique

```
CHACUN SUR SON ORBITE PROPRE   un cercle 3D, à SON rayon (la date), dans SON plan.
                               Inclinaison et nœud viennent du NOM : stables.
LA PERSPECTIVE                 foyer 420. Loin = petit. Ce n'est pas une valeur :
                               la taille apparente change en permanence.
LA MÊME VITESSE POUR TOUS      un tour en 48 s.
TA HIÉRARCHIE                  toi 90 / arc 13 · une personne 44 / arc 4
                               (écart volontaire au §2.9 — c'est le soleil)
L'ORBITE RESSERRÉE             rayons 92 → 140, contre 102 → 146 avant
LA MOISSON GAGNE               3 rangées dès le premier écran (la place de « avec qui »)
```

**L'orbite remplace la grille « avec qui »** — les mêmes personnes ne peuvent pas figurer deux
fois. **On touche un anneau, ça ouvre la personne** (`openPerson`).

### ⚠ Aucun anneau devant ton Noyau — ce n'est pas une question de z-index

Une orbite trop inclinée **traverse le centre à l'écran**, quel que soit l'ordre de dessin.
Donc, pour chaque personne, **l'inclinaison est cherchée par dichotomie** : on part de celle que
son nom donne, on échantillonne **96 positions**, et on réduit jusqu'à ce que son anneau **et sa
lune** dégagent le tien. **L'inclinaison retenue est celle qui tient, pas celle qu'on voulait.**
Vérifié par le contrôle sur **72 positions** : **0 écart**.

### ⚠ Trois erreurs de ma part, toutes prises par le contrôle

1. **La lune n'était pas dans le dégagement** — un point terracotta passait devant ton Noyau.
2. **J'ai exempté trop large.** J'avais exempté « personnes entre elles », prénoms compris :
   la moitié gauche est sortie **illisible**, des noms sur des visages, sans que rien ne le
   signale. **Deux anneaux qui se croisent, c'est le sujet ; deux noms qui se croisent, c'est
   une faute.** L'exemption ne couvre plus que les anneaux.
3. **Élargir le rayon d'évitement pour la lune a fait pire** — 30 recouvrements au lieu de 3,
   parce que plus aucune position ne convenait et que le repli s'appliquait partout. La lune
   passe **derrière** le nom (z 45) : elle ne cache rien.

### Deux décisions non prévues

**Le mot « toi » est retiré.** Il occupait la bande sous ton Noyau — là où passe une personne
qui arrive par le bas. Le garder obligeait à pousser l'orbite minimale de 78 à **106 px**,
c'est-à-dire à **grossir** ce qu'il fallait resserrer. Et il ne dit rien qu'on ne voie.

**Les prénoms sont placés par essais.** Huit directions autour de l'anneau, les plus proches du
regard d'abord, première position libre retenue. **Droits, 13,5 px, aucune perspective.**

### Les douze phrases, tirées au hasard

```
Tu l'avais dit. · Et tu l'as fait. · Personne n'en doutait. · Voilà. · Comme prévu.
Tu vois. · Ça y est. · Évidemment. · Parole tenue. · Le trait s'est refermé ici.
Elle a pris sa place. · Tu es venu.
```

Et **la phrase respire** : 20 → **38 px** sous « tenue. ».

```
15 cadres · 0 recouvrement · 0 hors cadre · 0 anneau devant ton Noyau sur 72 positions
langue §6 : tout à zéro · les 4 sondes du contrôle passent toujours
```

---

## ⚑ L'ORBITE — LE RAYON DIT LA DATE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`
> — **vivante**, l'orbite y tourne, un tour en 72 s. Captures : `scratchpad/retenu/`.

### ⚠ J'avais appliqué la règle anti-notation trop large — correction de Tom

J'avais posé **« tout au même rayon »**. **C'était faux**, et c'était moche : un cercle de
disques équidistants est un diagramme d'atome. **Les huit règles interdisent un classement de
VALEUR, pas toute variation.** Une distance qui dit une **date** ne dit aucun mérite.

Ce qui reste vrai de mon raisonnement : **tout ce qui est continu se classe** — donc la vitesse
reste identique pour tous, et ce qui est en chemin reste **binaire** (la lune), jamais un compte.

### La loi — cinq canaux, aucun ne dit un mérite

```
LE RAYON     quand remonte la dernière parole tenue. 102 px pour hier, 146 pour six mois,
             échelle logarithmique. C'est une DATE : loin = « ça fait longtemps »,
             jamais « tu comptes moins ».
L'ANGLE      le nom. LE TOUR EST L'ALPHABET — A en haut, Z après un tour entier.
             Les grappes et les vides viennent des initiales, de rien d'autre.
LA LUNE      ce qui est en chemin. Binaire, UNE SEULE, jamais deux.
LA COULEUR   la Nuée. Catégorielle.
L'ARC        l'harmonie — §2.9, là où le produit l'a déjà mise.
LA VITESSE   la même pour tous : la constellation tourne d'un seul bloc.
AUCUN FILET  ni cercle d'orbite, ni rayon, ni trait vers le centre.
```

Rayons mesurés : **Maman 108 · Adrien 114 · Marion 124 · Rachel 131 · Léa 137 · Nico 144**.

### ⚠ Ce qui a été dur, et que je n'avais pas vu

**La constellation tourne, les prénoms restent droits.** Une mise en place sans recouvrement à
u = 0 ne l'est plus à u = 1/3. **Trois versions ont échoué** (58 recouvrements, puis 19, puis
16) avant de comprendre qu'il fallait une condition **indépendante de la rotation**. Elle est
simple : **la distance entre deux centres.** Le point le plus lointain d'un prénom est à
√(31² + 57²) ≈ 65 de son centre, un anneau peint s'étend à 29 : au-delà de **106**, plus rien
ne se touche, à n'importe quel angle. **Le contrôle balaie désormais douze positions du tour**,
plus un seul instant.

⚠ **Et le rayon ne se corrige jamais.** Une version intermédiaire le remontait pour dégager le
centre : la personne la plus récente se retrouvait **à la même distance qu'une autre** — la
donnée détruite pour arranger le dessin. Le dégagement est tenu par le rayon minimal.

### Le contrôle de collisions gagne une mesure juste (pas un assouplissement)

**Une boîte carrée n'est pas la forme peinte quand la forme peinte est un anneau.** Les canevas
d'anneau déclarent `data-forme="anneau"` et leur rayon ; le contrôle mesure alors la distance du
rectangle **au cercle**. Prouvé : les quatre sondes passent toujours (deux textes ✅, un texte
débordant ✅, une marque sur sa surface exemptée ✅, une boîte bordée ✅).

### Les phrases — les neuf, tirées au hasard, une par rejeu

```
Tu l'avais dit.  ·  Et tu l'as fait.  ·  Personne n'en doutait.  ·  Voilà.
Comme prévu.  ·  Tu vois.  ·  Ça y est.  ·  Évidemment.  ·  Parole tenue.
```

« Tu l'avais dit. » ouvre la série. Sur « Parole tenue. » : gardée sur décision de Tom ; je
maintiens qu'elle est la seule qui **constate au lieu de complicer** — un tirage sur neuf la
rend tenable.

```
6 cadres · 0 recouvrement · 0 hors cadre · 0 écart à la loi · LE TOUR ENTIER : aucun recouvrement
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'AURA — L'ORBITE REMPLACE LA FRISE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`
> — **elle est VIVANTE** : l'orbite y tourne pour de vrai, un tour en 72 s.
> Captures : `scratchpad/retenu/` (10 cadres). Décision Tom : la frise sort, l'orbite revient.

### Ce que j'ai dû dire au lieu de le maquiller

Tom demandait que **le mouvement dise la proximité et l'harmonie du lien**. **Ce n'est pas
tenable sans refabriquer le classement qu'on venait de retirer**, et je l'ai posé plutôt que de
le contourner :

**Tout ce qui est CONTINU se classe.** Le rayon (le défaut de l'audit), mais aussi la vitesse,
l'amplitude, la taille, l'opacité, l'épaisseur. Dès qu'une propriété prend des valeurs graduées,
deux personnes peuvent être rangées — **même sans chiffre à l'écran**.

**Ce qui ne se classe pas est BINAIRE ou CATÉGORIEL.** Le mouvement ne peut donc pas dire un
*degré* d'harmonie. Il dit un **état** : **qui a une parole en chemin, et qui n'en a pas.**
Deux personnes qui ont quelque chose en chemin bougent **exactement pareil**.

### La loi de l'orbite — six règles, et le contrôle les mesure

```
1 · TOUS AU MÊME RAYON          132 px · mesuré : 131,99 → 132,01 sur les cinq
2 · TOUS À LA MÊME VITESSE      un tour en 72 s, la constellation tourne D'UN BLOC
3 · CE QUI VARIE EST BINAIRE    une LUNE terracotta tourne autour de qui a une parole
                                en chemin. UNE SEULE, jamais deux — ce serait un compte.
4 · LA COULEUR EST CATÉGORIELLE la piste porte la Nuée, jamais une valeur
5 · L'HARMONIE RESTE DANS L'ANNEAU   l'arc menthe du §2.9, là où le produit l'a déjà mise
6 · AUCUN FILET                 ni cercle d'orbite, ni rayon, ni trait vers le centre
```

Anneaux au **§2.9 à la lettre** : toi 78 / arc 8 / photo 48 · une personne 58 / arc 6 /
photo 36 · prénom Bricolage 600 / 13,5. Ordre alphabétique — **un cercle n'a pas de début :
placer alphabétiquement répartit, ça n'ordonne pas.**

### ⚠ Le premier dessin de l'orbite était faux, et le contrôle l'a pris

Première version : ceux qui avaient une parole en chemin **avançaient**, les autres restaient.
**Ils se percutaient** — mesuré, deux anneaux à **31 × 31 px** de recouvrement et un prénom
sous un visage. Et un recouvrement entre deux personnes, c'est **l'une devant l'autre** :
encore un rang.

**Correctif : les places sont FIXES, la constellation tourne d'un seul bloc**, et le binaire
passe dans **la lune**. Les écarts angulaires ne changent jamais.

### ⚠ Une troisième exemption au contrôle de collisions — et elle est prouvée

La lune passe au-dessus du **carré** du canevas de son propre anneau (elle dégage le cercle de
4,5 px ; c'est la boîte qui la croise dans son coin). **Deux parties du même objet ne se
percutent pas, elles se composent** : on exempte les nœuds qui partagent le même
`[data-role]`, **et eux seulement**.

```
scratchpad/preuve_collisions.py — quatre sondes, après l'exemption
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une marque sur sa surface          exemptée ✅
  4 · une boîte BORDÉE sur une dalle     PRIS ✅
```

### Les phrases du rejeu

« Tu l'avais dit. » retenue. Sur les quatre de Tom : **« Parole tenue. » est la seule faible** —
ce n'est pas un clin d'œil, c'est une **étiquette**, et c'est déjà le libellé d'état écrit
partout ailleurs. Les trois autres tiennent.
Quatre de plus, même calibre : **« Comme prévu. »** · **« Tu vois. »** · **« Ça y est. »** ·
**« Évidemment. »**

```
10 cadres · 0 recouvrement · 0 hors cadre · 0 écart à la loi de l'orbite
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ L'AURA — LA FRISE, SES ALTERNATIVES, ET LA PRÉSENCE · 4 septembre 2026

> **`app.html` inchangé depuis le lot du moteur.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (13 cadres, regardés un par un à 2×).
> **Le 4ᵉ argument de `dalleTrame` sert ici pour la première fois** : chaque dalle de la
> frise et de la moisson est peinte dans son monde d'alors.

### 1 · La frise — reprise, et trois alternatives dessinées

**Les deux causes étaient justes.** Les dalles étaient génériques : elles sont maintenant
chacune la sienne, à sa **vraie date**, dans son **monde d'alors** — la frise traverse
**deux changements de monde en huit semaines** et ça se voit.

**Ce qui rend le temps lisible, sans graduation ni chiffre :** la réponse était dans l'objet.
**L'onde fait huit ondulations — une par semaine.** C'est la ligne du produit qui respire au
rythme du calendrier. Plus l'espacement **irrégulier** : le rythme est l'information, un creux
de treize jours se voit sans qu'on l'écrive.

```
0 · LA FRISE REPRISE   une ondulation = une semaine        118 px
A · LE RUBAN PLIÉ      trois lignes, 3 × le rythme          194 px
B · LA SPIRALE         un tour = un mois                    214 px
C · LE FIL DES JOURS   un point par jour, 57 points          96 px
```

⚠ **J'avais recommandé « 0 ou A » AVANT de les regarder à 2×. Après les avoir vues, je change
d'avis : c'est C.** Il est le plus informatif d'un coup d'œil — longueur, grappes, silence,
jours ouverts — **et le seul qui ne coûte rien** : à 96 px, « avec qui » reste sur le premier
écran. **A coûte « avec qui »**, et son cadre le montre. **B est la plus belle et la moins
lisible** : le sens de lecture ne se devine pas, le centre s'encombre (deux effleurements
mesurés), et « il y a 8 semaines / aujourd'hui » n'a plus de sens sur une spirale.

**La frise garde sa place**, pour deux raisons que la moisson ne peut pas porter : **le rythme**
(la moisson dit *quoi*, la frise dit *quand*, donc les creux) et **ce qui n'est pas encore
tenu** — les points terracotta sous la ligne. La moisson ne contient que du tenu, par définition.

### 2 · Le chiffre — il ÉTAIT en Fraunces, et c'est pour ça qu'on ne le voyait pas

Vérifié **aux pixels**, pas au style calculé : on compare la largeur d'encre du nœud réel au
même texte rendu dans chacune des six faces embarquées.

```
« 82 » à 24 px / 600      largeur réelle 27,66 px
  écart à Fraunces    0,48   ← la face rendue
  écart à ApfelMid    2,07 · Apfel 2,60 · Bricolage 2,68 · serif 3,66
```

**Le problème n'était pas la face : à 24 px son dessin ne se voit pas, et en crème il se fond.**
**34 px et sa couleur d'état** — menthe ≥ 65, periwinkle 40-64, terracotta en dessous, **mêmes
seuils que le mot** : la couleur et le mot ne peuvent pas diverger.

### 3 · La présence — structure inchangée, trois leviers

```
ce qui est gros l'est plus   le mot 52 → 64 · le Noyau 118 → 134 (trait 38) · le chiffre 24 → 34
ce qui est petit disparaît   « TA PAROLE DANS LE TEMPS » retiré — le plateau dit déjà « Aura »
                             et ce sous-titre ne portait aucune information. Réversible.
l'espace se creuse           sous le plateau 22 → 50 · autour du mot 12 → 22
                             avant la frise 26 → 31 · avant « avec qui » 21 → 39
```

### 4 · Les phrases du rejeu

« Tu l'avais dit. » retenue. Trois autres du même calibre — deuxième personne, passé, nues,
aucune mesure, aucune félicitation : **« Tu es venu. »** · **« C'était une promesse. »** ·
**« C'est toi qui l'as tracée. »**

### Ce que le contrôle a trouvé, et que l'œil n'aurait pas vu

⚠ **Trois paroles tenues dans la même semaine se couvraient l'une l'autre** — 43 dalles prises.
Une grappe doit se voir **comme une grappe**, pas comme une dalle unique : `ecarte()` garde
l'ordre et la date et écarte au minimum (D+2).

⚠ **Le message du contrôle confondait deux défauts très différents** : l'ONDE qui passerait
devant (interdit) et une DALLE VOISINE qui déborde (un défaut d'écartement). **Il nomme
désormais le coupable.** Aucune occurrence de « L'ONDE ❌ INTERDIT » : l'onde ne passe jamais
devant une dalle.

⚠ **`ecarte()` recompressait ce qu'il venait d'écarter** — six effleurements de 2 px. On décale
le **peigne entier**, et on le clampe dans la boîte du trait : sinon la première dalle sortait
de sa frise par la gauche — invisible à l'œil, mais le contrôle avait raison de la voir.

```
13 cadres · 0 hors cadre · 0 onde devant une dalle
recouvrements : 2, tous deux sur LA SPIRALE (8×2 et 6×5 px) — sa faiblesse, mesurée
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
```

---

## ⚑ LE MONDE D'ALORS — LE MOTEUR EST TOUCHÉ · 4 septembre 2026

> **Feu vert explicite de Tom.** Première modification du moteur de la Toile depuis
> l'interdit du §9. Sauvegarde d'avant : **`sauvegardes/avant-monde-fige.html`**.
> Planche : `PLANCHE-AURA-RETENU.html` · captures `scratchpad/retenu/` (8 cadres).

### Ce qui a changé — trois endroits, et pas un de plus

```
1 · dalleTrame prend un 4e argument FACULTATIF        {m:design, p:palette, h:teinte}
    sauvegarde/restauration de theme, palKey, hueShift ET _palLit,
    sur l'idiome que la fonction porte déjà pour g/W/H/seeds/view.
2 · Toile.mondeCourant()                              accesseur en LECTURE SEULE
3 · la fabrique P() fige mondeDuJour() sur chaque Promi
    + window._figeMondesManquants(), passe de rattrapage IDEMPOTENTE,
      appelée au chargement ET dans loadState()
```

⚠ **`_palLit` était le piège.** C'est un **mémo** de la palette calculée, invalidé par
`setPalette`/`setHue`. Sans l'invalider à l'aller, la palette de l'appelant fuit **dans** la
dalle ; sans le restaurer au retour, celle de la dalle fuit **dans la Toile**. Il est dans la
liste de sauvegarde au même titre que `theme`.

**Huit sites plantent un Promi ; tous passent par la fabrique `P()`.** On l'a patchée elle,
jamais les huit — c'est le seul point où un Promi naît.

**Les Promi déjà plantés** (jeu de démonstration comme `promi_state` sauvegardé avant ce lot)
prennent **le monde courant, figé maintenant** — décision Tom. **Rien n'est tiré de leur date :
on n'invente pas un passé qu'on n'a pas.** La moisson sera uniforme jusqu'à aujourd'hui puis se
diversifiera, c'est ce que verrait quelqu'un qui commence.

### La preuve — quatre contrats, `scratchpad/preuve_monde.py`

```
1 · SANS le 4e argument, rien ne change            deux relevés identiques ✅
2 · AVEC, la dalle sort dans le monde demandé      3/3 dalles diffèrent, sur 3 mondes ✅
3 · AUCUNE FUITE : la Toile est intacte après      encre|signal|0 → encre|signal|0 ✅
    et la dalle sans argument redonne la même      ✅
4 · chaque Promi porte un monde, rattrapage idempotent   0 sans monde, 0 touché au 2e passage ✅
0 erreur de page
```

### Les batteries, EN SÉRIE

```
releve-design    ✅ AUCUN ÉCART        ← le contrat visuel, intact
redteam_ecrans   150/150               redteam_toile  17/17     redteam_formes 38/38
redteam_vide      61/61                redteam_champ  32/32     redteam_nuee   24 écrans / 0
redteam_air      ✅ 428 paires
releve-S1 ✅ · S2 ✅ 0·0·0·0·0 · S3 ✅ · S4 ✅ · S5 ✅
```

⚠ **`redteam_tonsurton` a donné 22/26 puis 26/26.** Le premier passage suivait
`redteam_formes` dans la même boucle : la machine n'avait pas rendu la main. **Reconfirmé
seul : 26/26.** C'est le flottement documenté au §7, pas une régression — mais je le dis.

**`releve-design.py --figer` n'a PAS été lancé.** La référence est intacte et sans écart,
ce qui est attendu : **rien de ce lot n'est encore branché sur un rendu.** Le moteur gagne
une capacité, la donnée gagne un champ, aucun pixel ne bouge. Câbler les peintres de dalles
(Aura, Index, Fil) est le lot suivant, et il aura son propre avant/après.

### Les cinq corrections de dessin, sur la planche

```
1 · l'anneau : trait 13 → 33 (× 2,5)   à 13 il faisait diagramme
    ⚠ les anneaux des PERSONNES n'ont pas bougé — le §2.9 leur donne 6 sur 58 (10 %).
      Les épaissir imposerait de descendre le visage de 36 à 32. En attente.
2 · sous le plateau       14 → 22 px
3 · autour du Noyau       13 → 21 au-dessus · 12 → 18 en dessous
4 · autour du mot          8 → 12 sous « solide » · 20 avant la légende
5 · la phrase du rejeu — trois propositions, en attente de ta décision :
      « Tu l'avais dit. »              c'était une parole avant d'être une dalle
      « Le trait s'est refermé ici. »  les mots du cadre 97, le souvenir situé sans date
      « Elle a pris sa place. »        parle de la dalle, pas de toi
```

⚠ **La dalle du rejeu sortait minuscule** : je forçais une hauteur de 190 sur un canevas
carré, et `dalleTrame` **recadre au plus juste sur l'alpha** — la forme était écrasée.
Carré, jamais étiré.

```
8 cadres · 0 recouvrement · 0 hors cadre · 0 onde devant une dalle
langue §6 : 0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre · 0 ton sur ton
air : 0 paire sous 10 px
```

---

## ⚑ L'AURA — LA MOISSON, LE REJEU, L'ONDE DERRIÈRE · 4 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (6 cadres, regardés un par un à 2×).

### ⚠ LE POINT BLOQUANT — le moteur ne sait pas repeindre une dalle dans son monde d'alors

**Vérifié avant de toucher, comme demandé. La réponse est NON, et je n'ai touché à rien.**

```
un Promi ne porte AUCUN champ de monde          Object.keys(p) n'en a pas
theme · palKey · hueShift                        trois variables de MODULE, globales
la même dalle 125, repeinte :
   encre     remplissage 4289   boîte 176 × 138
   mosaïque  remplissage 3963   boîte 178 × 200
   terrazzo  remplissage 1912   boîte 122 × 124
```

Ce n'est pas une nuance : **la forme, la densité et les tons changent.** Changer de monde au
Studio repeint **toute** la Toile, les anciennes dalles comprises. La règle « la dalle est
figée à la plantation » **n'existe pas encore dans le code**. Mesure : `scratchpad/monde_fige.py`.

**Ce que ça demande, en deux morceaux — le premier touche le moteur (§9) :**

1. **`dalleTrame` prend un 4ᵉ argument facultatif**, sur l'idiome de sauvegarde/restauration
   que la fonction porte **déjà** pour `g, W, H, seeds, view` : on y ajoute
   `theme, palKey, hueShift`. **Quatre lignes.** Aucun des six appels existants ne bouge —
   `dalleTrame(cv,id,1)` se comporte exactement comme aujourd'hui.
2. **Un champ `{m,p,h}` posé sur le Promi à la plantation**, dans `addP()` — hors moteur,
   c'est du produit. **Question ouverte que je ne peux pas trancher :** les Promi déjà plantés
   n'en ont pas. Que voient-ils ?

**En attendant, la planche montre la moisson pour de vrai** en basculant le monde et la palette
**autour de chaque peinture** — emploi en **lecture seule** de l'API publique
(`setTheme` / `setPalette`), aucun code du moteur modifié. **Non viable dans l'app** (chaque
bascule repeint toute la Toile), mais ça prouve que le rendu sait faire.

### Ce qui est décidé et dessiné

```
la frise    SORTIE B — l'onde derrière, les dalles à hauteur constante.
            Le trait plat est écarté : sur cet écran il ressemble à un filet.
            ⚠ L'ONDE NE PASSE JAMAIS DEVANT UNE DALLE — vérifié AU DOIGT, dalle
            par dalle, deux thèmes : 0 écart. Chaque dalle est au premier plan,
            opacité 1, filtre none, fusion normal.
la moisson  bloc permanent, chaque dalle dans le monde ET la palette de son jour.
            Taille égale (44, pas de 50) · chronologique, la PLUS RÉCENTE EN
            PREMIER · aucun chiffre, aucun compte, aucun libellé de quantité.
le rejeu    un doigt sur n'importe quelle dalle rejoue sa seconde — cadre 98,
            « tenue. » puis « Le dessin existe. ». Zéro pixel au repos.
P1          SORTI — doublon avec la moisson, qui contient déjà la dernière.
le chiffre  dérivé de l'anneau. Une seule source pour l'anneau, le chiffre, le mot.
```

**Le rognage des dalles n'en est pas un.** Les bords droits qu'on voit sur les dalles d'encre
sont **les frontières de la cellule de Voronoï**, pas une coupe : mesuré, la part du bord opaque
est **identique à 44, 88 et 176 px** (encre 7 % · terrazzo 2 % · mosaïque 13 % · braille 5 % ·
pixel 7 %). `scratchpad/rognage.py`. J'allais signaler un défaut qui n'existe pas.

### ⚠ MON OUTIL DE COLLISIONS — deux angles morts, tous deux prouvés

**1 · `elementsFromPoint` travaille en coordonnées de FENÊTRE.** Les cadres hors de la fenêtre
rendaient une liste vide : l'outil annonçait « 0 » sur des cadres qu'il n'avait pas regardés.
**Tous les « 0 recouvrement » antérieurs de ce projet sont partiels.** Inscrit dans
`CLAUDE.md §8`. Parade : chaque cadre entre dans la fenêtre avant d'être interrogé.

**2 · Il ne regardait que les FEUILLES.** Le bouton « Partager mon Noyau » chevauchait la
dernière rangée de la moisson et l'outil n'a rien dit : un bouton bordé porte un `<span>`, ce
n'est donc pas une feuille. **Une boîte peinte compte, même si elle a des enfants.**

```
scratchpad/preuve_collisions.py — quatre sondes, quatre verdicts
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une dalle DANS la frise            exemptée ✅   (marque sur sa surface)
  4 · une boîte BORDÉE sur une dalle     PRIS ✅       ← l'angle mort n° 2
```

### Ce qui est mesuré sur la planche

```
6 cadres 390 × 844, échelle 1, regardés un par un à 2×
recouvrements confirmés AU DOIGT, cadre par cadre    0
hors cadre                                           0
l'onde devant une dalle                              0
langue (§6)  0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre
             0 graisse hors des six faces · 0 ton sur ton
```

---

## ⚑ L'AURA — LA FRISE, LE CHIFFRE, LA CÉLÉBRATION · 3 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (9 cadres, regardés un par un à 2×).

### 1 · La frise ondulait — le reproche était juste, et mesuré

**Mon propre commentaire disait « la ligne ne code aucune valeur » et mon code dessinait
`per: 1.5` avec une enveloppe.** Mesuré : **une dalle sur une crête est posée 30 px plus haut
qu'une dalle dans un creux**. Sur un écran qui annonce huit semaines, l'œil lit une hauteur.

Deux sorties dessinées et mesurées côte à côte — `window._friseY` publie la position verticale
des dalles, mode par mode :

```
aujourd'hui · per 1.5, la dalle suit la courbe    écart 30,0 px   ← le défaut
sortie A · le trait plat                          écart  0,0 px   bloc 118 → 96
sortie B · l'onde derrière, dalles constantes     écart  0,0 px   l'onde reste
```

⚠ **`0 || 16` vaut 16.** Le premier jet du « trait plat » ondulait encore : `amp=o.amp||16`
avalait l'amplitude nulle, et **les sorties A et B sortaient identiques**. Une amplitude nulle
est une valeur, pas une absence.

**Sortie A implique un écart au §5** (« courbes quadratiques, jamais de segments droits ») :
le §5 gouverne **le geste**, celui qu'on trace au doigt ; la frise n'est pas le geste. Le tracé
reste quadratique dans le code, ses points sont colinéaires. **Signalé, pas caché.**

### 2 · Le chiffre est dérivé de l'anneau

C'était une incohérence de **données**, pas de dessin : l'anneau posé à 62 / 24 / 14, le
chiffre écrit **67** à la main — **15 points d'écart**. Désormais une seule source :

```
PARTS = {tenu:62, encours:24, rate:14}
  → les trois arcs de l'anneau
  → harmonie = 62 / (62+14) = 82
  → harmonyWord(82) = « solide »   (la fonction de l'app, recopiée mot pour mot)
```

### 3 · Célébrer sans mesurer — trois propositions, à trancher

**Le produit avait déjà les mots.** Le **cadre 98** de l'instant écrit **« tenue. »**
(Bricolage 700/64) puis **« Le dessin existe. »** (Bricolage 600/20). Rien n'a été inventé.

```
P1 · LE DESSIN EXISTE   un bloc permanent : ta dernière parole tenue, sa vraie dalle,
                        son jour, la phrase du cadre 98. Coût mesuré : 142 px, et
                        « avec qui » tient ENCORE — seul le bouton passe sous le pli.
P2 · LE REJEU           rien au repos ; un doigt sur une dalle rejoue l'instant.
                        Coût : ZÉRO pixel. Ajout validé hors inventaire (§5).
                        Son défaut : rien ne l'annonce.
P3 · LA MOISSON         toutes les dalles tenues, ensemble, à taille égale.
                        DÉCONSEILLÉE par moi : une matière qui s'épaissit est un
                        compteur déguisé — le piège qu'on vient de retirer du trait.
```

**Recommandé : P2 + P1.** P1 résout le seul défaut de P2 — il annonce que les dalles sont
vivantes.

### ⚠ MON OUTIL DE COLLISIONS ÉTAIT À MOITIÉ AVEUGLE — et je l'ai prouvé

**`document.elementsFromPoint` travaille en coordonnées de FENÊTRE.** Une planche fait
plusieurs milliers de pixels de haut : **les cadres du bas sont hors de la fenêtre, et la
confirmation au doigt y rend une liste VIDE — donc aucun recouvrement, jamais.** L'outil
annonçait « 0 » sur des cadres qu'il n'avait pas regardés. **Tous les « 0 recouvrement » des
livraisons précédentes sont donc partiels.**

Trouvé en essayant de prouver une AUTRE correction : deux textes superposés à dessein dans un
cadre du bas **n'étaient pas pris**. C'est exactement le §8 — *avant d'accuser le dessin, on
vérifie l'instrument*.

**Deux correctifs, et une preuve :**
1. **On amène chaque cadre dans la fenêtre** (`scroll_into_view_if_needed`) avant de
   l'interroger, cadre par cadre.
2. **Une marque posée sur sa surface n'est pas un recouvrement** — une dalle peinte sur la
   frise, un visage tracé dans son anneau. On n'exempte QUE la containment géométrique, et
   seulement sur un canevas ou un SVG : un texte qui **déborde** d'un canevas reste pris,
   deux textes restent comparés intégralement.

```
scratchpad/preuve_collisions.py
  1 · deux textes qui se recouvrent      PRIS ✅
  2 · un texte débordant d'un canevas    PRIS ✅
  3 · une dalle DANS la frise            exemptée ✅
```

**Et il a trouvé un vrai défaut au passage :** les deux repères de la frise étaient deux boîtes
empilées — « aujourd'hui » faisait **342 de large** et passait sous « il y a 8 semaines ». Les
glyphes ne se touchaient pas ; les boîtes, si. Chacun fait désormais **165**.

### Ce qui est mesuré sur la planche

```
9 cadres 390 × 844, échelle 1, regardés un par un à 2×
recouvrements confirmés AU DOIGT, cadre par cadre    0
hors cadre                                           0
langue (§6)  0 sous 12 px · 0 opacité <72 % · 0 dégradé · 0 ombre
             0 graisse hors des six faces · 0 ton sur ton
air          1 paire sous 10 px — « solide » → « 82 », le couple mot/qualificatif, voulu
```

---

## ⚑ L'AURA — LE PARTI A EST RETENU ET CORRIGÉ · 3 septembre 2026

> **`app.html` n'est toujours PAS touché.** Planche : `PLANCHE-AURA-RETENU.html`.
> Captures : `scratchpad/retenu/` (7 images, regardées une par une à 2×).
> **`releve-S2` est réparé et de nouveau au vert** — voir plus bas, c'est le point important.

**Décision Tom : A · le trait déroulé, avec le mot de B greffé.** Trois corrections demandées,
une quatrième proposée, une simplification :

1. **Le centre de l'anneau est nu** — plus de dalle, et plus de visage non plus (« c'est l'arc
   qui parle » ; un visage y parlait autant qu'une dalle). Les anneaux des **personnes**
   gardent leur visage : là il désigne quelqu'un.
2. **Le chiffre en Fraunces 600** — face embarquée, `document.fonts.check` la confirme chargée
   et ses métriques diffèrent du repli (26,47 px contre 24,00 sur « 67 ») : elle n'est pas
   substituée en silence. Le mot « harmonie » reste en ApfelMid 500.
3. **Le mot passe à Bricolage 700 / 52** (au lieu de 34).
4. **PROPOSÉ — les anneaux des personnes ne se doublent PAS avec le Cercle.** Un second anneau
   par personne est **un agrégat par personne, doublé** : la règle 4 enfreinte au moment même
   où on prétend la servir. **Sur l'Aura la réciprocité est GLOBALE — elle vit dans les deux
   moitiés du trait, et nulle part ailleurs.**
5. **Simplification :** « TES HUIT DERNIÈRES SEMAINES » disait ce que les repères sous le trait
   disent déjà. Retiré. Les **30 px** rendus sont ce qui permet au mot de passer à 52.

**`#kEvolve` est ressuscité** — l'évolution Nuée par Nuée, que l'app composait en entier et
jetait faute de nœud. Elle revient **en frises, jamais en rangées** : pas un taux, pas une
barre, pas un ordre de valeur. Elle vit sous le pli, avec le Cercle (3ᵉ cadre de la planche).

**Le mot du Noyau : vérifié, aucun n'est un reproche.** L'échelle est monotone et le cas le
plus bas (« naissante ») est le plus généreux. Une réserve mince, écrite dans `QUESTIONS.md ·
Q165 bis` : « à tisser » est une consigne, pas une description.

### `releve-S2` — l'oscillation est éteinte, et ce qu'elle cachait est corrigé

Le juge posait un **délai fixe** (1100 + 700 ms) puis mesurait. Le Peaufiner d'une **Nuée**
sortait alors à **0 × 0** une fois sur deux — et **le thème fautif changeait d'un passage à
l'autre**. Un délai ne gagne pas une course.

**Correctif : le juge attend une CONDITION, plus une durée** (`POSE` — la liste a sa largeur,
ses blocs ont une hauteur), **puis exige deux relevés identiques**.

⚠ **Et la première version de ce correctif m'a eu.** L'empreinte de stabilité ne prenait que
**la géométrie** : le juge repartait « posé » alors que le **plancher typographique** n'était
pas encore passé, et annonçait **30 à 39 écarts de style — pas les mêmes d'un passage à
l'autre**. L'oscillation avait simplement changé de colonne. **Une empreinte doit couvrir tout
ce que le juge compare** : elle prend désormais la géométrie ET le style.

```
trois passages consécutifs   ✅ position 0 · style 0 · collisions 0 · hors cadre 0 · peinture 0
preuve qu'il MORD encore     scratchpad/preuve_S2.py → ❌ style 6 sur un défaut fabriqué
```

La preuve est **empaquetée et auto-nettoyante** : elle copie l'app, y pose une sonde (un
libellé à 9 px, décalé de 40), relance le juge dessus, et efface tout.
Original : `sauvegardes/releve-S2-peaufiner-avant-attente-posee.py`.

### Ce qui est mesuré sur la planche retenue

```
7 cadres 390 × 844, échelle 1, deux thèmes, regardés un par un à 2×
recouvrements confirmés AU DOIGT   4 — les DEUX du §3.8 (l'encart sur sa scène), × 2 thèmes
hors cadre                          0
langue (§6)                         0 sous 12 px · 0 opacité sous 72 % · 0 dégradé
                                    0 ombre · 0 graisse hors des six faces · 0 ton sur ton
dalles                              VRAI moteur (Toile.dalleTrame, échelle 1)
```

**Les dix-neuf lignes de texte des trois écrans sont listées dans `QUESTIONS.md · Q165`**,
neuves et existantes séparées — douze sont neuves.

---

## ⚑ L'AURA ET LE CERCLE — AUDIT FAIT, TROIS PARTIS POSÉS · 3 septembre 2026

> **`app.html` n'est PAS touché.** Ce lot est un audit et trois planches, à juger avant tout code.
> Planche : `PLANCHE-AURA-TROIS-PARTIS.html` (servie en 8752) · Audit : `AUDIT-AURA-CERCLE.md`
> Outils : `scratchpad/aura_audit.py` · `scratchpad/cap_partis.py` · `scratchpad/juge_partis.py`
> · `scratchpad/air_partis.py` · captures : `scratchpad/partis/` (11 images, regardées une par une)

### Ce que l'audit a trouvé — six blocs morts et une porte manquante

**Mort dans les DEUX modes** (passer premium ne les rend pas) : `#kEvolve` et `#plusCta`
**absents du DOM** alors que le JS les alimente encore (l'évolution par Nuée est composée en
entier et jetée ; le gestionnaire d'achat est inatteignable) · `#kStats` (en cours · résolues ·
**série**) · `#kLegend` — **le graphe n'a donc aucune légende** · `#kPct`/`.kbig` (le grand
chiffre, doublon de celui du Noyau) · `.klabel`.
**La porte manquante :** la fiche d'aide annonce en gratuit « Partager mon Noyau » ; le mode
existe côté partage, **l'Aura ne porte aucun bouton** (`#auraScreen [class*=share]` → 0 nœud).

**Six des huit règles anti-notation sont enfreintes, et cinq le sont en GRATUIT** — dont
`#ksocial` qui écrit un taux **par personne** en 8 px, et dont le **rayon de l'orbite encode la
valeur** : un classement dessiné sans être écrit. Le détail, règle par règle, est dans l'audit.

### Trois partis, un par SUJET — le fork n'est pas la forme

L'exercice a **échoué au premier tour**, et c'est écrit sur la planche : opposer « la
constellation » et « la page de mots » au trait déroulé donnait des concepts qui **coexistent**
(un trait en tête, une constellation dessous — c'est l'Aura d'aujourd'hui). Le fork est **la
seule question à laquelle l'écran répond** :

```
A · LE TRAIT DÉROULÉ   « d'où je viens »   une DURÉE      le trait porte le temps, les dalles
                                                          se plantent dessus, les points dessous
B · LA PIERRE          « où j'en suis »    un INSTANT     un seul objet, un mot, une phrase
C · LA TABLÉE          « avec qui »        une COMPAGNIE  toi puis les tiens, anneaux égaux
```

**Recommandé : A, avec le haut de B greffé** (le mot, gros, sous le Noyau).
**Passent au Cercle :** les graphes (évolution · répartition · composition), les commentaires
sur la hausse, et la réciprocité. **Reste gratuit :** le Noyau, le mot, la frise, la grille
d'anneaux sans chiffre, le partage du Noyau.

### La page du Cercle — une seule, pour les trois partis

Elle **montre** au lieu de dire : la scène voilée à **2,4 px** avec l'encart **net** posé
dessus (§3.8, la seule superposition autorisée), puis trois vignettes voilées légendées.
Le prix s'écrit **29 € · soit 2,42 €/mois · −39 %**, l'année en primaire. Aucun ✦ ne sort de
l'appareil : l'audit a vérifié que le partage n'en porte aucun, et rien n'en ajoute.

### Ce qui est mesuré sur la planche

```
11 cadres 390 × 844, échelle 1, deux thèmes, regardés un par un à 2×
recouvrements confirmés AU DOIGT   4 — les DEUX du §3.8 (l'encart sur sa scène), × 2 thèmes
hors cadre                          0
langue (§6)                         0 texte sous 12 px · 0 opacité sous 72 % · 0 dégradé
                                    0 ombre · 0 graisse hors des cinq faces · 0 ton sur ton
air entre deux textes               4 paires sous 10 px — toutes VOULUES (l'encart 3 px, le prix 6 px)
dalles                              peintes par le VRAI moteur (Toile.dalleTrame, échelle 1)
```

⚠ **`releve-S2` n'est pas au vert sur cette machine.** Deux passages **en série** donnent
`position 29 · style 0 · hors cadre 2`, et **le thème fautif change d'un passage à l'autre** :
le Peaufiner de la Nuée sort mesuré **0 × 0**, il ne s'est pas ouvert à temps. C'est une course
de construction dans le juge, pas une régression de l'app. **`style 0` dans les deux passages :
la correction des sept libellés à 13 est bien en place.** Signalé, pas réglé.

⚠ **Les mots des planches sont NEUFS pour la plupart** — dix-sept, listés un par un dans
`QUESTIONS.md · Q165`, tous **à valider**. Une seule vraie question ouverte : le mot du Noyau
(« solide ») est-il le mot juste, ou un jugement déguisé ?

---


## ⚑ DEUX CORRECTIONS AVANT LE CHANTIER AURA / CERCLE — 3 septembre 2026

> Point de reprise : **`sauvegardes/lot-entete-index-fil.html`**
> Sauvegardes d'étape : `sauvegardes/avant-libelles-13.html` · `sauvegardes/avant-entete-index-fil.html`

⚠ **Le point de reprise annoncé `sauvegardes/lot-passe-finie.html` était en retard d'un lot.**
`app.html` était identique à `sauvegardes/lot-rythme-fiche.html` (le lot du rythme sous le
trait, Q163). Je suis parti de l'app telle qu'elle était, pas de `lot-passe-finie` : repartir
de là aurait perdu ce lot.

### 1 · `releve-S2 · style 12` est levé — les sept libellés à 13

Le dernier rouge du projet. **La cause n'était pas la feuille de style, c'était un repli du
plancher typographique** : sa loi `max(13, taille)` posait bien 13 sur les sept libellés, et
un repli le reprenait aussitôt sur cinq. Ce repli protège un texte qui, en grossissant,
recouvrirait le bloc placé **sous** lui ; son test comparait le bas du texte au haut du frère
suivant **sans vérifier que ce frère est dessous**. Dans une **rangée flex** le frère est **à
côté** — les boîtes se chevauchent verticalement par construction, la condition est vraie
d'emblée, et le libellé redescendait à sa butée de 12 sans qu'aucun recouvrement n'existe.
Dans une **zone** (pile verticale), le repli ne se déclenchait pas : NOTE, COMMENTAIRES et
DESCRIPTION gardaient 13. D'où **deux tailles pour sept libellés de même nature**.

La garde est **géométrique, pas une classe** : le frère ne compte comme « dessous » que s'il
commence dans la moitié basse de la boîte, ou plus bas. Relevé : **24 nœuds du produit**
étaient retenus à 12 sans avoir de voisin dessous.

**Le §6 tranche contre le cadre** — décision Tom : *« ils doivent être identiques, et le §6
interdit 11,5. Ce n'est pas le cadre qui gagne, c'est la loi. »* Erreur de dessin recensée
dans `ECARTS-MOODBOARD.md § 0 bis.4`. Contrat `releve-S2` mis à jour (13 au lieu de 11,5,
tolérance inchangée), **prouvé contre la version fautive : 36 écarts avant, 0 après**.
⚠ Une première sonde a été **avalée** — une règle CSS ne peut rien contre l'inline
`!important` que le plancher écrit ; la preuve s'est faite en rejouant le juge sur la
sauvegarde d'avant.

### 2 · L'air sous l'entête de l'Index et du Fil : 24 → 16

Signalé par Tom sur capture. Le 24 venait du cadre 72 (titre finissant à 84, barre à 108) et
avait été reporté tel quel quand le plateau de 60 a remplacé le titre de 44. **Ce 24 était
l'air d'un titre NU** ; le plateau est une **boîte bordée**. Deux boîtes bordées de la même
grammaire prennent l'**écart de bloc du §3.3 — 16 px**.

```
la barre  .ix-bar     124 → 116        la liste  #indexList/#feedList   212 → 204
le menu de tri        186 → 178        tout ce qui suit remonte de 8
```

Recensé dans `ECARTS-MOODBOARD.md § 0 bis.5`, inscrit dans `PROMI-SPECIFICATIONS §5`.
`releve-S4` mis à jour (116 / 204), **prouvé : 18 écarts sur la version d'avant, 0 après**.

### L'état des batteries après les deux lots

```
releve-S2  ✅ 0 · 0 · 0 · 0 · 0     ← LE DERNIER ROUGE DU PROJET EST LEVÉ
releve-S1  ✅   releve-S3  ✅   releve-S4  ✅   releve-S5  ✅   redteam_nuee  ✅ 24/0
releve-design  ✅ AUCUN ÉCART       redteam_ecrans 150/150     redteam_vide 61/61
redteam_superpo 0 recouvrement      redteam_polices 0 absent
redteam_air ✅ 428 paires           ← refigée DEUX fois, et chaque fois pour la même raison
```

⚠ **`redteam_air` a été refigée deux fois, et je le dis en propres termes.** Les deux fois,
le resserrement est la conséquence arithmétique du changement demandé, jamais un
desserrement : **10 paires à −1 px** entre deux libellés consécutifs (un libellé grandi d'un
pixel vers le bas, le bloc suivant à cote fixe — c'est le §8, « une cote dérivée n'est pas un
espace »), puis **5 paires à −8 px**, toutes « ✕ Fermer → ⇅ », c'est-à-dire la rangée
déplacée et rien d'autre. Aucune autre paire n'a bougé dans l'un ou l'autre cas.

⚠ **`releve-design.py --figer` n'a PAS été lancé** — la référence est intacte et sans écart.

---

## ⚑ LE STUDIO EST REPENSÉ — 1er septembre 2026

**Le pinceau a quitté le Studio.** Un choix de Studio s'appliquait à toutes les fiches d'un
coup : il interdisait de donner son trait à un Promi, à une Nuée, à un gardé de côté. Il part
**à la page +**, à la création, et se reprend **depuis Peaufiner, haut de liste**. La règle
générale est inscrite dans `CLAUDE.md` §5 — *un réglage vit là où vit ce qu'il règle* — avec
son test : **est-ce que ce réglage a un sens différent d'un Promi à l'autre ?**

**Conséquence de dessin :** le trait n'avait plus rien à montrer au Studio. L'onde disparaît,
le corps disparaît, **la Toile prend tout l'écran**, et deux plateaux flottent dessus.

### Où en est le lot

```
FAIT   la planche du Studio sans trait, six pas, sombre et clair   PLANCHE-STUDIO-SANS-TRAIT
FAIT   les cinq fonctions de l'app replacées (voir plus bas)
FAIT   les planches passées au VRAI MOTEUR (Toile.preview)         Q130
FAIT   l'audit complet de la page Partager, 17 commandes, 5 défauts
FAIT   l'intégration dans app.html — lot-STUDIO-PLATEAUX                Q133
FAIT   le frémissement du moteur, mesuré (0,38 px amorti sur 1,1 s)     Q134
FAIT   trois bugs du Studio : verrou collant, monde faux, dégradés      Q135
FAIT   l'air de la consigne de la page + : 29 → 44 px
FAIT   l'onde à 36 partout — la borne basse du §2.4 bis              Q136
FAIT   les deux paires du Studio : écart 20/56 + leurs libellés      Q137
À FAIRE  LE GESTE DE COULEUR AU DOIGT — dessiné, pas codé (Q135)
FAIT   l'encart en haut — ONZE écrans                               Q138
À FAIRE  l'encart sur les QUATRE derniers — un lot chacun, ils ont
         chacun leur grammaire : Personne, l'aperçu, la page +, la fiche
FAIT   Partager sans trait — et les 4 défauts de l'audit corrigés     Q139
FAIT   le saut à l'ouverture du Studio — mesure supprimée          Q140
FAIT   les pages alignées sur la grammaire de l'encart            Q141
FAIT   les coins : les écrans épousent l'arrondi de l'appareil    Q142
À FAIRE  le bouton actif du sujet sort sombre au lieu de crème (Q139)
À FAIRE  l'encart de Partager est #shcTitre, pas .enh — à aligner
FAIT   la passe de collisions — 5 recouvrements trouvés et corrigés  Q143
FAIT   l'Index recalé en conditions RÉELLES (plus de forçage)       Q144
À FAIRE  METTRE À JOUR releve-S4-index-fil.py — 62 écarts voulus,
         il reste rouge tant qu'il n'encode pas la décision (Q144)
FAIT   le FIL (#feedView, pas #feedScreen) — calé comme l'Index     Q145
FAIT   les filets gris retirés — redteam_tonsurton 23/26 → 26/26   Q146
FAIT   LA RÉFÉRENCE = le plateau du Studio, PLEIN + bordé, déployé   Q147
       → même crème #F4EEE1 sur l'encart, la recherche, le tri, les cartes
À FAIRE  violations du §6 PRÉEXISTANTES : textes à 10-11,5 px et
         opacités à 0,42-0,70 sur Réglages, Aura, Index, Nuée, Cercle
         + #plHeroCv qui déborde (x −16, largeur 430) — à vérifier
         contre l'inventaire de chaque cadre avant de toucher (Q143)
À FAIRE  la planche de la page + pour le trait
À FAIRE  la refonte du partage sur la base de l'audit
```

### Les cinq fonctions du Studio, et où elles sont passées

```
.st3-dots    huit points de navigation  → rangée fine sous les disques, cliquables
.st3-hint    « glisse pour changer… »   → invite qui meurt après le premier geste
.st3-pals    Toile.palettes()           → reste le moteur ; la maquette montre 4 tons
#stLockBuy   « Adopte ce design — 1 € » → sur la Toile, au-dessus du plateau
#stLockCta   l'offre du Cercle          → encart §3.8 sur les réglages floutés
```

**Sur un monde verrouillé** (décision Tom) : la matière reste **visible**, floutée à 2,4 px ;
le nom du monde s'affiche **net, 46 px, centré** — il s'affirme même quand on ne l'a pas ;
l'encart couvre une partie des réglages et en laisse voir : **on voit ce qu'on n'a pas**.
On voit **quoi**, jamais **combien**.

### Ce que l'audit du partage a trouvé

**Deux défauts rendent une fonction entière inatteignable** — le mode « Noyau seul » n'a
aucun bouton (`#sealShare` cherche un `data-mode=noyau` qui n'existe pas), et les six
commandes de `#shNoyauParts` sont masquées en dur et jamais démasquées. **La refonte
restaure, elle ne déplace pas.** Trois autres se corrigent au passage : la borne du
sur-mesure (le clamp dit 3840, les boutons s'arrêtent à 2160), deux gestionnaires sans nœud
(`#shOptVis`, `.sh-opts`), et le libellé « Format » en double.

### Points de restauration

```
sauvegardes/avant-studio-sans-trait.html    app.html avant le lot du Studio
sauvegardes/lot-studio-plateaux.html        app.html après le lot, vérifié
sauvegardes/redteam_ecrans-avant-studio-plateaux.py   deux contrats réécrits
scratchpad/c5/painter.js                    la maquette, DÉBRANCHÉE (Q130)
```

---

# État des lieux — Promi, la superposition écran par écran

> **Ce fichier suffit à reprendre le projet.** Il dit ce qui est porté, ce qui ne l'est pas,
> ce qui a été corrigé dans les documents, quels contrats de test ont changé et pourquoi,
> et ce qui reste ouvert. Écrit sans complaisance : ce qui n'est pas beau à dire est dit.
>
> Dernière mise à jour : **30 août 2026 — LE STUDIO ET LE PARTAGE SONT CONÇUS ET POSÉS.**
> Point de reprise : `sauvegardes/lot-studio-partage.html`
> Captures : `scratchpad/studio/` · `scratchpad/partage/` · `scratchpad/final/` (32 images)

---

# ⚑ LE STUDIO ET LE PARTAGE SONT CONÇUS ET POSÉS — 30 août 2026

> **Ce chapitre passe devant.** Le portage était clos ; ce chantier-ci n'en était pas un.
> Le Studio et le partage n'ont **ni cadre ni inventaire** : c'était une CONCEPTION, sortie
> de la grammaire déjà posée. Aucun duo, rien à superposer.
>
> Point de reprise : **`sauvegardes/lot-studio-partage.html`**
> Sauvegarde d'avant le chantier : `sauvegardes/avant-studio-partage.html`
> Captures : `scratchpad/studio/` (6) et `scratchpad/partage/` (4), regardées une par une.

## Ce qui a été livré

| écran | variante retenue | ce qu'elle fait |
|---|---|---|
| **Le Studio** | **B · le champ** | le champ porte la Toile du monde, bornée par l'onde ; **le trait sert deux fois** — il borne le champ ET il montre le pinceau. On **pousse le champ** pour changer de monde ; sous le trait, un **rail de huit points** (les points du §2.2). |
| **Le partage** | **2 · la feuille** | **l'onde est la poignée** : on la tire, les réglages montent, l'image se réduit. Sous l'onde, **le même rail de points** — il ne dit pas où l'on est, il dit **qu'il y a la suite**. |

Deux blocs, posés à la fin du fichier comme tous les lots : **`lot-STUDIO-CHAMP`** et
**`lot-PARTAGE-FEUILLE`** (style + script). **Rien n'a été réécrit** : les commandes
existantes sont **DÉPLACÉES** dans la nouvelle grammaire, jamais refaites.

## LE PINCEAU — la seule fonction neuve, et elle était validée

Concept donné par Tom, jamais implémenté : *« on choisit aussi son pinceau au Studio — la
matière avec laquelle on trace ses moitiés de trait. Le monde est ce qu'on récolte, le
pinceau est ce avec quoi on signe. »* Trois matières : **Plein · Encre · Trame**.
Le choix est **enregistré** (`localStorage.promi_pinceau`, lu par `window.promiPinceau()`)
et le Studio le montre sur son propre trait. **Il ne change pas encore le trait qu'on trace
au doigt** — ce trait est peint par le moteur du geste, et le brancher est un lot à part
(QUESTIONS.md · Q118). Sans branchement, le geste garde le trait plein d'aujourd'hui, qui
est exactement le pinceau « Plein ».

## Aucune fonction perdue — l'inventaire, au complet

**Studio** — déplacés, pas supprimés : `#stBg` (le monde) → le champ · `.st3-dots` → le rail
· `.st3-wn` → sous « LE MONDE » · `.st3-pals` (palettes), `.st3-spec` (teinte), `#thToggle`
(thème), `#txToggle` (texte des dalles) → **derrière la barre Peaufiner** · `#stLockBuy`
(adoption 1 €) et `#stLockCta` (l'offre) → au doigt seulement, sur le champ voilé.

**Partage** — les **quatorze** réglages sont dans la feuille : sujet · cinq formats + sur
mesure · fond de l'image · mot-marque · QR · texte des dalles · Noyau + sa taille · ce qu'il
montre · quels Promi (la portée) · les deux actions · la note des 3 Nuées offertes.
**Disparaissent : le `⋯` et le `↗`** — le tiroir EST la feuille, et `#shGo` ne faisait que
cliquer `#shShareBtn`. Aucune fonction perdue (Q109).

**Tout est gratuit (Q113)** : aucun `✦`, aucun `blur(2.4px)`, aucun encart du §3.8, aucun
réglage grisé sur l'écran de partage ni dans sa feuille. C'est le **seul écran du produit où
le §3.8 est interdit**. La borne d'export monte à **4K** (Q119).

## Un contrat de test réécrit — au niveau de la décision (§7)

| contrat | il exigeait | la décision qui l'a remplacé | original |
|---|---|---|---|
| `redteam_ecrans` · « Studio : groupe centré » | les deux bascules forment un groupe centré **en haut** du Studio | la variante B : le champ occupe le haut, les réglages passent derrière la barre Peaufiner (Q109) ; le §9 interdisant de perdre une fonction, elles sont **déplacées** | `sauvegardes/redteam_ecrans-avant-studio-champ.py` |

**Même intention, nouveau nœud** : on vérifie que les deux bascules **existent encore**,
qu'elles sont **dans le tiroir**, et que la pile est **centrée**. Le contrôle protège
exactement la même chose. Il compte désormais **trois** points au lieu de deux — d'où
**148/148** là où il y avait 146.

## Ce que l'œil a trouvé, et qui est corrigé

| | ce qui ne ressemblait pas | ce que c'était |
|---|---|---|
| **1** | la dalle du Studio sortait en **rectangle noir** posé sur le champ | `Toile.preview` **peint son propre fond**. La boîte du §2.7 ne convient pas : c'est la construction du §10.7 — l'aplat, puis la Toile découpée par le **même chemin**, puis le trait. |
| **2** | le champ et la barre **rognés de 16 px à droite** | **un `.screen` ne coïncide pas avec `#device`** : `#studioScreen` fait **422 px** et commence **16 px à gauche et au-dessus**. D'où `#stcCadre` / `#shcCadre`, un cadre de 390 × 844 **mesuré** sur l'appareil. |
| **3** | l'encart et le bouton du Cercle en **dégradé rose-orangé**, texte illisible | `.enc-fx`, `.eg`, `.eb*` peignent un dégradé animé **par-dessus** le fond plat. §6 : aucun dégradé. Éteints, comme Q23 l'a fait aux Réglages. |
| **4** | en thème **clair**, « Studio » **crème sur crème** et le trait invisible | la Toile recouvre le champ et elle est crème : **ce qui est peint dessous décide** (Q59 étendu au trait — Q116). |
| **5** | le tiroir du Studio **sombre en thème clair** | `.device.light #studioScreen` **ne matche jamais** : l'écran vit sous `.frame`, pas sous `.device` (§8). On **pose** la classe, la CSS la lit. |
| **6** | les dix palettes **débordaient** sur la teinte ; le curseur de teinte **s'échappait à gauche** | des cotes fixes au lieu d'une pile à écart 16 ; et `.st3-spec` passée en `position:static` **perdait son bloc englobant**. |
| **7** | le tiroir sortait dans le **désordre** (thème, texte, palette, teinte) | l'ordre était celui où chaque commande **existe** : `#thToggle` est dans le HTML, `.st3-pals` naît avec `buildStudio`. Les quatre boîtes se créent **d'emblée**. |
| **8** | les deux actions du partage à **~30 px**, débordant du cadre | `.sh-share` porte ses propres taille, interlettre et capitales. §3.6 imposé au `!important`. |
| **9** | la feuille du partage **inatteignable** sous la barre | `#shcCadre` est en `overflow:hidden` : la pile doit porter sa **hauteur bornée** et défiler. |
| **10** | `redteam_geste` tombé de **13/13 à 12/13** — « l'aimant de la ligne du QR attire » | **`shareRender()` dimensionne l'aperçu lui-même.** Ma mise en page ne se rejouait qu'aux événements du doigt : après un `shareRender()` extérieur, le canevas repassait de **218 × 388 à 341 × 607** et le geste tombait à côté. On **repose derrière lui**, comme le lot du Studio derrière `buildStudio`. |
| **11** | le bouton d'adoption disait **« Débloque-le — 1 € »** | un **rotateur** tire le libellé **au hasard** entre trois formulations. On réécrit derrière lui, avec la garde du §8. |

## Tout est vert

```
23 batteries      ecrans 148/148 · 15 · 10 · 18 · demande 19 · toile 17 · geste 13/13
                  verbe 6 · phrase 6 · filets 0 parasite · aveugle 26 · fonctions 22
                  tonsurton 26 · formes 38 · nuee 24 écrans/0 · champs 22 · enchaine 24
                  pastilles 12 · photo 27 · polices 0 absent · vide 61 · air 391 paires
                  champ 32
5 juges           S1 ✅ · S2 ✅ · S3 ✅ · S4 ✅ · S5 ✅
contrat visuel    releve-design.py  ✅ AUCUN ÉCART
l'œil             collisions.py  19 écrans × 2 thèmes → 0 collision
                  10 captures regardées une par une (Studio 6, partage 4)
```

**`releve-design.py --figer` n'a PAS été lancé** : la référence attend ta validation.

## Ce qui reste ouvert

- **Q115 · la transition effilochée** entre deux mondes n'est pas implémentée :
  `Toile.preview` sème avec `Math.random()`, deux mondes ne peuvent pas partager un semis, et
  rendre deux mondes en une passe demanderait **d'ouvrir le moteur de la Toile** (§9). Le
  glissement repeint net, comme avant.
- **Q118 · le pinceau ne trace pas encore** le geste réel — lot à part, il touche au geste.
- **Q117 · trois libellés** de l'app remplacés par la forme du document : à relire.

---

# ⚑ LE PORTAGE EST CLOS — 29 août 2026

> **Décision Tom :** *« C'est bon, le portage est fini. »*
> Ce chapitre suffit à reprendre. Tout ce qui suit, plus bas dans le fichier, est
> l'historique — utile pour comprendre POURQUOI une chose est ainsi, jamais nécessaire
> pour continuer.

## A · Ce qui est porté, et jusqu'où va la spécification

**Le périmètre de la spécification s'arrête à sept écrans**, et ils sont tous portés :

| Écran | Cadres | Juge |
|---|---|---|
| **Les fiches** — Promi tenue · à tenir · en cours · Chiche lancé · relevé · tenu à deux | 42 à 57 | `releve-S1-fiches.py` |
| **Peaufiner** (fiche et Nuée) | 78 à 87 | `releve-S2-peaufiner.py` |
| **La page +** — phrase vide, remplie, choix ouverts, geste, reprise d'un gardé de côté | 2 à 33 | `releve-S3-page-plus.py` |
| **L'Index** (2 et 3 par ligne) **et le Fil** | 72 à 77 | `releve-S4-index-fil.py` |
| **L'instant** — il arrive · le trait se referme · juste après | 96 à 101 | `releve-S5-instant.py` |
| **La Nuée** — avec Promi, vide, son Peaufiner | `promi-nuee-toile.html` 0 à 11 | `redteam_nuee.py` |
| **Les réglages** | — | `releve-design.py` |

**Ce qui n'a NI CADRE NI INVENTAIRE, et n'est donc pas du portage : le Studio, l'Aura, le
partage.** Le prochain chantier est une CONCEPTION, pas une superposition. Ne pas y appliquer
la méthode du duo : il n'y a rien à superposer.

## B · Comment on vérifie — la méthode, en trois temps

1. **`python3 -m http.server 8752 --bind 127.0.0.1`**, puis les trois adresses (voir CLAUDE.md).
   Le port 8752 est **en dur** dans tous les outils.
2. **Les batteries, EN SÉRIE — deux ou trois à la fois au maximum.** Douze Playwright lancés
   d'un coup font ramer la machine et **les rouges qu'on lit alors sont faux** (mesuré et
   revécu quatre fois : `enchaine` 21/24 puis 24/24, `tonsurton` 22/26 puis 26/26, sans
   toucher une ligne). Un rouge apparu dans une passe parallèle **se reconfirme seul**.
3. **L'œil, au duo.** `python3 scratchpad/duo_vue.py scratchpad/final` — le cadre à gauche,
   l'app à droite, échelle 1, 16 écrans × 2 thèmes. **On les regarde toutes, une par une.**
   Trois défauts livrés à tort sont passés par des captures produites et non regardées.

## C · Les 23 batteries et les 5 juges — tous au vert

**Attention au compte :** un `ls redteam_*.py` en donne 20 et **oublie `redteam.py`,
`redteam2.py`, `redteam3.py`**. Il y en a **23**. (J'ai écrit « 22 » dans une livraison :
c'était ce glob, pas la réalité.)

```
redteam_ecrans      146/146   la principale — 146 contrôles d'écran
redteam                15/15   ·  redteam2   10/10  ·  redteam3   18/18
redteam_demande        19/19   redteam_toile      17/17   redteam_geste      13/13
redteam_verbe            6/6   la phrase montre TOUJOURS son verbe + la bascule
redteam_filets     0 parasite  aucun trait horizontal hors moodboard
redteam_aveugle        26/26   redteam_fonctions  22/22   redteam_tonsurton  26/26
redteam_formes         38/38   la courbe peinte contre la loi extraite du cadre
redteam_nuee     24 écrans/0   redteam_champs     22/22   redteam_enchaine   24/24
redteam_pastilles      12/12   redteam_photo      27/27   redteam_phrase       6/6
redteam_polices    0 absent    aucune graisse hors des six faces embarquées
redteam_vide           61/61   UN ÉCRAN N'EST JAMAIS VIDE — il ENCHAÎNE les écrans
redteam_air        391 paires  L'AIR ENTRE LES TEXTES ne se resserre jamais
redteam_champ          32/32   UN CHAMP BLANC N'EXISTE JAMAIS
```

```
releve-S1-fiches · releve-S2-peaufiner · releve-S3-page-plus
releve-S4-index-fil · releve-S5-instant          → les cinq AU VERT
releve-design.py                                  → AUCUN ÉCART (référence figée)
```

**Les trois dernières batteries sont nées de trois défauts livrés à tort.** Chacune a été
**prouvée contre la version fautive**, jamais seulement écrite :

| Batterie | Ce qu'elle protège | Preuve |
|---|---|---|
| `redteam_vide` | un écran ne perd pas ses éléments, et n'en porte pas d'un autre | **28/61** sur la version fautive, 61/61 après |
| `redteam_air` | deux textes ne se rapprochent jamais de leur écart d'origine | **18 rouges** sur « le cran sans les écarts » |
| `redteam_champ` | le champ porte toujours sa nature, jamais la couleur du corps | **2 rouges** sur la version au champ éteint |

**Ces trois-là ENCHAÎNENT ou COMPARENT ; les autres ouvrent chaque écran sur une page
fraîche.** C'est exactement pour ça qu'elles voyaient ce que les autres ne pouvaient pas voir.

## D · Les contrats de test réécrits — et pourquoi

**Règle (CLAUDE.md §7) :** un contrôle qui encode une règle abandonnée **se met à jour au
niveau de la décision**, jamais en changeant le comportement pour le faire passer. On nomme
la règle, on nomme la décision, on garde l'original dans `sauvegardes/`, et **on le dit dans
la livraison**. Six l'ont été en fin de portage :

| Contrat | Il exigeait | La décision qui l'a remplacé | Original |
|---|---|---|---|
| `releve-S1-fiches` | des cotes recopiées une à une, titre à 38 | les cotes **se déduisent** de la règle du 29 août ; le titre a une RÈGLE (42, sauf si la ligne casse — plancher 38), pas une taille | `-avant-29aout.py` |
| `releve-S3-page-plus` | « trace pour planter » sur les huit écrans | le moodboard ne dit ce mot que **deux fois** : « trace ta moitié » au cadre 2, « trace pour planter » au cadre 10 (choix ouvert) et 26 (reprise) | `-avant-29aout.py` |
| `releve-S3-page-plus` | « pas d'aplat sur un gardé de côté » | **un champ blanc n'existe jamais** — l'aplat doit être là, c'est la matière qui manque | `-avant-champ.py` |
| `releve-S4-index-fil` | le titre d'une carte à 20 exactement | il rentre dans sa boîte : **≤ la taille du cadre, ≥ 11** — un titre ne sort pas de sa boîte | `-avant-29aout.py` |
| `releve-S5-instant` | l'état à 12,5 | le cran du 29 août : 13,5, toutes fiches, toutes natures | `-avant-29aout.py` |
| `redteam_vide` (le mien) | un texte sans nœud texte est « vide » ; un titre sur « le trait se referme » | un `<input>` porte des glyphes par son `placeholder` ; **le cadre 98 n'a pas de titre** | — |

**Un renommage de nœud ne relève PAS de cette procédure** — c'est un renommage, l'intention
est intacte : on le note, on ne délibère pas.

## E · Les erreurs de dessin recensées — la planche a tort, et on l'écrit

Recensées dans `ECARTS-MOODBOARD.md § 0 bis`. **Une erreur de dessin n'est pas une règle :**
quand elle contredit une loi du document ou une décision, la loi gagne, et on note pourquoi.

1. **Cadre 58** — une base de champ de Nuée que `base = max(176, 460 − 86 n)` ne produit pour
   aucun `n`. Six points sur six suivent la loi ; ce cadre est un dessin isolé. (Q84)
2. **Cadre 74** — il donne une **dalle** à un gardé de côté. Lui en donner une l'occuperait
   une case de la Toile, donc le planterait. (Q83)
3. **Le bouton ⇅** — dessiné en `content-box` là où sa voisine est en `border-box` : il fait
   **56**, le document et l'app s'accordent contre le cadre. (Q87)
4. **Les cadres CLAIRS qui peignent le trait en couleur pleine** — le trait y prend
   exactement la couleur de l'aplat et **disparaît**. C'est le cas que le §2.1 bis interdit.
   (CLAUDE.md §3)
5. **Les cadres 26/27 et 74 qui dessinent un gardé de côté sur le corps nu** — même famille.
   **Un champ blanc n'existe jamais** (décision du 29 août). C'est la MATIÈRE qui manque à un
   gardé de côté, jamais la couleur.
6. **Le titre qui touche l'état dans une carte d'Index** — le cadre le fait aussi ; un texte
   ne sort pas de sa boîte, l'app le fait rentrer.

**Et deux exceptions déclarées, qui ne sont PAS des erreurs** : la **matière** (une Toile est
engendrée par le moteur, la planche l'a tracée à la main — elles ne peuvent pas coïncider,
Q74) et le **dessin des glyphes** (la planche est en Hanken Grotesk, l'app en Apfel embarqué,
et le §6 l'impose — Q80). **La boîte du texte, elle, se mesure à zéro.**

## F · Ce qui reste ouvert

**Rien ne bloque le prochain chantier.** Trois points de fond, à trancher quand ils gêneront :

- **Q71 · les titres de nature.** Tom les dit manquants dans l'Index et le Fil ; je ne les
  trouve dans aucun cadre, texte par texte, cotes et couleurs à l'appui. **Il faut un cadre
  ou un mot**, sinon ce serait inventer (§9).
- **Q68 · « Apfel 500 » n'existe pas.** Le document l'écrit à plusieurs endroits ; la face
  embarquée est `ApfelMid 500`. Le report est appliqué à l'exécution (`lot-POLICES`), pas
  corrigé à la source du document.
- **Le désaccord de comptes entre les deux planches.** `promi-nuee-toile` écrit « 7 PROMI »
  au potager, `moodboard-H` « Index 12 » ; le jeu réuni donne **9** et **16**, et l'encart
  dit **le contenu réel** (décision Tom : « garde les neuf, ne retire rien »).

**Ce qui est CLOS et ne doit pas être rouvert sans décision :** la teinture est bornée à la
bande haute (Q30 bis) · la bande d'une Nuée montre **les neuf mondes non teintés**, sa
planche le dit en titre (Q94) · l'anneau garde ses **trois** arcs (Q88) · la dalle est
centrée dans une carte d'Index (Q86) · le nombre de l'entête du Fil est « Fil 4 ».

## G · Les cinq lois qu'on reperd toujours

1. **La Toile ne se touche pas.** Son code est validé et fragile (§9). La couleur d'une dalle
   y est **tirée au hasard** (`cc()`) : le même id sort tantôt lavande, tantôt exactement la
   couleur du champ. C'est pour ça que le champ **cède** dans les listes, et que la bande
   haute **teinte** (Q30). Ne jamais juger une couleur de dalle sur un seul chargement.
2. **On ne nettoie pas la CSS.** Cinq tentatives, cinq échecs. L'ordre des 769 règles du
   dernier bloc est significatif.
3. **Rien ne survit à `closeAll`** — ni ce qu'un écran masque (`data-masque`), ni ce qu'il
   pose en ligne (`data-pose`), ni ce qu'il bâtit (`window._rangeurs`).
4. **Une cote dérivée n'est pas un espace, c'est « hauteur du bloc + air ».** Grossir un texte
   ne déplace aucun `top` : l'air se mange en silence. Écrire la cote dans la bonne unité.
5. **On compare la COMPOSITION, pas la peinture.** `dalleTrame` anime la matière avec
   `performance.now()` : un contrôle bâti sur ses pixels flotte. L'app publie ce qu'elle vient
   de composer — `_plancheComp`, `_noyauSig`, `_nueeSemis`, `data-champ`, `data-cede` — et le
   contrôle lit ça.

## H · Les fichiers, dans l'ordre où on les lit

```
CLAUDE.md                 fait autorité sur tout le reste
MOODBOARD-VALEURS.md      l'arbre des neuf écrans, extrait du moodboard
promi-moodboard-H.html    la référence visuelle du parcours (102 cadres, base 390)
promi-nuee-toile.html     fait foi pour la NUÉE
PROMI-SPECIFICATIONS.md   les valeurs (§1.2 palettes, §1.3 corps, §2.x géométrie)
ECARTS-MOODBOARD.md       les erreurs de dessin recensées
QUESTIONS.md              Q1 à Q101 — le raisonnement, décision par décision
ETAT-DES-LIEUX.md         ce fichier
```

**Point de reprise : `sauvegardes/lot-champ-de-nature.html`.**

---

## ⚑ LA MÉTHODE A CHANGÉ — ON NE MESURE PLUS AU PIXEL

> **Décision Tom, 29 août.** « On arrête la mesure au pixel. Le reste est le plancher de
> deux moteurs de rendu, pas un défaut : glisser la capture de −2 à +2 px donne le minimum
> à (0,0). **Tu regardes, tu corriges, tu termines.** »

L'outil est `scratchpad/duo_vue.py` : le cadre à gauche, l'app à droite, à l'échelle 1,
quinze écrans, deux thèmes. Pas de pourcentage — une image.
`scratchpad/collisions.py` complète : il demande au navigateur si deux textes se touchent,
sur dix-neuf écrans, dans les deux thèmes.

## ⚑ CE QUE L'ŒIL A TROUVÉ, ET QUI EST CORRIGÉ

| | ce qui ne ressemblait pas | ce que c'était |
|---|---|---|
| **1** | **Le Peaufiner d'une Nuée survivait à la fiche suivante** | Ses cartes (`np-tete`, `np-carte`) restaient dans `#dpdCorps`, et ses `display:none` en ligne restaient sur `dptQui`, `dptTitre`, `dptQuand`. La fiche passait de **10 à 24 nœuds de texte** et perdait son titre sous « DESCRIPTION · MEMBRES · PIÈCES JOINTES » |
| **2** | **Le bouton photo était écrasé à 2 px de large** | `max-width:100%` résolu sur son porte-à-faux de largeur nulle. À l'écran : un filet vertical au milieu du champ |
| **3** | **Le chevron ▾ de Peaufiner disparaissait** | `opacity:.5` et 13,3 px là où le cadre 48 l'écrit plein, à 15 px |
| **4** | **L'icône de partage était trop maigre** | `svg 19 × 19, trait 1,8` contre `22 × 22, trait 2,6` au cadre |
| **5** | **La pastille du mot de la page + flottait** | Même creux que la pastille du verbe (`2px 17px 6px`) et un interligne cloué à 42 px : **57,8 de haut au lieu de 44**. Le cadre donne `0 15px 3px`, rayon 16, interligne normal |
| **6** | **Le Fil ne montrait qu'une pastille de visage sur trois** | Elle se lisait sur `p.from` — qui a promis — au lieu du `from` de l'ÉVÉNEMENT |
| **7** | **Le fil d'une Nuée disait « TENUE » et coupait ses titres** | Le cadre écrit **TENU** (le sujet est un Promi, pas une parole) et laisse le titre passer sur **deux lignes** |
| **8** | **Un chiche relevé s'affichait « CHICHE LANCÉ »** | La ligne se lisait sur l'état de la PAROLE ; c'est `chicheEtat` qui dit s'il est relevé |
| **9** | **Le Noyau d'une Nuée vide était GRIS** | §3 : « jamais de trait neutre ou gris ». Le cadre 0 de `promi-nuee-toile` l'écrit dans la teinte claire de la nature |
| **10** | **« +N » comptait mal les membres** | Le Peaufiner d'une Nuée sortait « +2 » là où le cadre 86 écrit « +3 » : il oubliait de me compter, contrairement à la ligne « à qui » de la fiche |
| **11** | **Un TROISIÈME bouton « Planter un Promi dans la Nuée »** | La liste de Peaufiner de la section 2 en bâtit un (`.s2-bouton`) que le garde des jumeaux ne voyait pas : **deux textes identiques superposés à 100 %** |
| **12** | **« écris un mot… » sur une fiche** | Le cadre 46 écrit « écris un mot » ; les points appartiennent au champ COMMENTAIRES |

## ⚑ ZÉRO COLLISION, ET TOUT EST VERT

```
scratchpad/collisions.py   19 écrans × 2 thèmes   →   0 collision
```

C'était la dernière ligne de `CASSE.md` — « les textes qui se touchent dans l'Index », « les
commentaires qui sortent de leur ligne ». **Aucun des deux n'est reproductible** ; le seul
recouvrement réel du produit était le troisième bouton « Planter » (ligne 11 ci-dessus).

⚠ **Le premier balayage annonçait 269 collisions : toutes fausses.** La sonde ratissait tout
`#device`, y compris le dock, la barre d'état et les écrans FERMÉS — qui gardent leurs nœuds
en `display:block`, simplement recouverts. Et les écarter un à un ne marche pas non plus :
dans une vraie collision, c'est le texte du DESSOUS qu'on écarterait. On prend donc **la
feuille la plus haute qui couvre l'écran** et on compare ses textes entre eux.

```
redteam_ecrans     146/146   redteam_champs      22/22   releve-S1-fiches      ✅
redteam_fonctions   22/22    redteam_pastilles   12/12   releve-S2-peaufiner   ✅
redteam_aveugle     26/26    redteam_enchaine    24/24   releve-S3-page-plus   ✅
redteam_toile       17/17    redteam_photo       27/27   releve-S4-index-fil   ✅
redteam_formes      38/38    redteam_tonsurton   26/26   releve-S5-instant     ✅
redteam_nuee        24/24    redteam_polices      0/0    redteam_filets    0 filet
redteam 15 · redteam2 10 · redteam3 18 · demande 19 · geste 13/13 · verbe 6 · phrase 6

releve-design.py   ✅  AUCUN ÉCART — référence refigée le 29 août.
```

## ⚑ CE QUI NE PEUT PAS RESSEMBLER, ET POURQUOI — quatre lignes

1. **Les glyphes.** La planche est en Hanken Grotesk et Bricolage Grotesque ; l'app porte ses
   six faces embarquées, que le §6 impose. Un titre passe à deux lignes d'un côté et une de
   l'autre — c'est le cas de « le grand plongeoir », dont la ligne d'état descend alors de
   39 px sur le cadre 56. **Ce n'est pas un écart de dessin** (Q80, tranché).
2. **Le bouton photo** (`ph-photo-btn`) n'existe sur aucun cadre : c'est l'affordance de la
   **photo de champ**, décidée en Q53, et le seul chemin vers elle — les PIÈCES JOINTES de
   Peaufiner sont autre chose (« ce n'est pas une pièce jointe », dit le lot). Il reste,
   discret, comme son propre lot l'exige.
3. **« trace pour planter »** là où les cadres 2 à 10 écrivent « trace ta moitié » : **Q35**,
   tranchée par Tom — un seul mot, qui ne change pas d'un cadre à l'autre.
4. **Le jour d'une échéance** dépend du jour où l'on regarde : le cadre 36 écrit
   « À TENIR · DIMANCHE », le cadre 44 « À TENIR · DANS 2 JOURS », pour la même fiche à deux
   jours. L'app écrit le vrai jour.

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

## 4 ter · LES DIX DÉFAUTS QUE LE DUO A SORTIS, ET QU'AUCUNE BATTERIE NE VOYAIT

Aucun n'était visible d'une batterie : elles mesurent des cotes, des couleurs et des
présences, écran par écran, sur une page fraîche. Le duo compare **l'image**, écran après
écran, dans l'ordre où un doigt les ouvrirait.

### 1 · La classe héritée `dp-nuee` cassait l'écran porté d'une Nuée
`dp-nuee` réveille tout le CSS d'avant le portage. Mesuré, deux thèmes :
`#detailPoster` passe de `flex/absolute/844` à `block/relative/0`, et la barre Peaufiner,
collante, **tombe à y = 0, par-dessus « ✕ FERMER »**. Elle n'arrivait pas toujours :
`renderNueeDetail` la pose, `renderDetail` la retire — **selon qu'une fiche a été ouverte
avant ou non, l'écran était juste ou cassé.** C'est ce que `redteam_aveugle` criait, et que
Q75 avait mis à tort sur le compte du nouveau jeu. Blocs `lot-NUEE-LEGACY` et `lot-NUEE-CLASSE`.

### 2 · La hauteur d'une Nuée survivait à la fiche suivante — et lui volait sa barre
Le fil d'une Nuée défile : `#dpMain` porte sa hauteur en `min-height !important`, et rien ne
la retirait. Après « le potager », `#dpMain` restait à **1092 au lieu de 760** ; la barre
Peaufiner tombait à y = 1092, **hors de l'écran**. La fiche perdait sa barre, en silence.
Le duo le montrait ainsi : `fiche-tenue` **clair à 15,9 %** contre 4,8 % en sombre, sur le
même dessin. Corrigé au garde de `_ficheNuee` — **4,5 % / 4,6 % après.**

### 3 · La carte d'Index dessinait l'onde d'une FICHE
`peintCarte` appelait `O.onde(base, amp)` — qui cloue **période 1,5** (§2.1, une fiche) et
**normalise par 390**, la largeur d'une fiche. Sur une carte de 165, l'abscisse n'atteignait
que t = 0,42 : on voyait deux cinquièmes de la courbe, étirés sur toute la carte. Le §3.9 dit
**période 1**, sur la largeur de la carte. Mesuré contre le chemin du cadre 72 :

```
x        2    38    74   110   146   158
loi   102,3  94,4  98,6 106,8 104,3 100,9     creux à x=41, crête à x=124
avant 102,0  96,0  94,0  98,0 104,0 105,5     creux à x=68, crête à x=165
après 102,0  94,0  98,0 106,0 103,0  99,5     écart médian 0,65 px, maximal 1,65
```

`onde` prend maintenant deux paramètres facultatifs (`per`, `larg`) ; **la fiche ne bouge pas
d'un pixel.**

### 4 · La hauteur du trait était une cote de l'ÉTAT, pas du PROMI
Le §2.5 dit « la hauteur de trait **figée à la plantation** ». L'app la déduisait de la fiche.
Les six cartes du cadre 72 sortaient à `145 · 118 · 108 · 118 · 118 · 145` là où la planche
donne `135 · 107 · 147 · 99 · 123 · 131`. **La preuve que c'est une cote du Promi :** les deux
cadres de l'Index — 2 par ligne (198/600) et 3 par ligne (133/600) — redonnent la même hauteur
à 1,5 px près sur les huit entrées. Portée en `p.ht` / `NUEHT[k]` (Q78).

### 5 · La boîte de la dalle de la page + se tirait de la crête de l'onde
Relevé sur neuf cadres, deux bases : `base 312 → dalle 244 × 200 @ 73` et
`base 280 → 204 × 168 @ 93`, soit **`dh = base − 112`, `dw = 1,2 dh`, centrée**. L'app
calculait `(base − amp) − 100` et sortait **199 × 166 au lieu de 244 × 200** — la matière
d'un cinquième trop petite, et tout son pourtour compté comme un écart. **10,2 % → 1,8 %.**

### 6 · La bande de fond d'une Nuée suivait la boîte, pas la vague
`--nuee-bande` est le fond DERRIÈRE le canevas. Mais le canevas n'est opaque que jusqu'à
l'onde : au-delà de son point le plus haut, la bande se voyait là où le corps commence.
Mesuré sur le potager : boîte 256, vague à 140 → **116 px de mauve à bord franc**, et 100 %
de différence sur les ordonnées 180 à 240. Bornée au minimum de l'onde. **21,5 % → 9,9 %.**

### 7 · Une Nuée gardée de côté gardait son champ plein
« Rien n'est promis, donc il n'y a pas de champ » est déjà la règle d'un Promi gardé de côté
(section 1, page + cadre 27). Le cadre 74 la montre appliquée à une Nuée : « l'atelier du
samedi » y est un corps nu pointillé. L'app y peignait un aplat mauve.

### 8 · L'anneau du Noyau peignait « tenu » en MAUVE
Trois choses le contredisaient, toutes dans le produit : **`CLAUDE.md` §3** (« #2BE88C
menthe tenue »), **sa propre légende** `.klegend` (« #2BE88C tenues · #8FA0FF en cours »),
et **le cadre 48** (anneau terracotta recouvert d'un arc menthe sur 72 % du tour). Le mauve
est la couleur d'une Nuée : sur un anneau qui dit un état, il racontait autre chose.

### 9 · Le comparateur ré-échantillonnait toute la capture
`.frame` se met à l'échelle pour tenir dans la fenêtre : à un viewport de 390 × 844,
`#device` sort à **363,87 × 787,45**, soit 0,933. Les juges le savent ; le comparateur PIXEL,
lui, remontait la capture à 1 — chaque glyphe entre deux pixels, et **aucun écran ne pouvait
tomber à zéro, quoi qu'on corrige.** Mesuré : **430 × 932 donne `#device` exactement
390 × 844.**

### 10 · Et le comparateur capturait avant que l'écran soit composé
À 2 000 ms, `fiche-tenue` sortait **sans sa dalle et sans sa barre Peaufiner**. Le compte de
nœuds visibles se stabilise AVANT que tout soit peint : il faut un plancher de temps ET deux
relevés identiques.

> **La leçon, et elle vaut pour la suite : un comparateur qui redimensionne mesure son
> propre redimensionnement, et un comparateur qui capture trop tôt mesure une transition.**
> Avant d'accuser le dessin, on vérifie l'instrument.

### Et une non-cause, vérifiée : l'app est stable
`scratchpad/stabilite.py` — deux captures du même écran sans rien changer, puis une troisième
après réouverture, hors matière : **0,0 % sur les cinq écrans**. Le grain décoratif
(`.tuto-fond::before`, tiré au `Math.random` et animé) **ne sort pas de la zone de matière**.

---

## 4 quater · CE QUI RESTE — et pourquoi ce n'est pas corrigible

Les décisions de Tom du 29 août ont retiré trois causes sur cinq. Voici les cinq, avec ce
qu'elles coûtent.

### 1 · L'anti-crénelage de deux moteurs — le plancher, ~1,5 à 2 %
Un liseré d'un pixel longe chaque courbe : l'onde d'une fiche, l'anneau d'un Noyau, les
pastilles, les coins arrondis. La planche les dessine en **SVG**, l'app les peint en
**canvas**. Même chemin, même épaisseur, même couleur — deux moteurs de rasterisation.
**Vérifié que ce n'est pas un décalage :** le désaccord minimal est à (0,0), pas à ±1 px.

### 2 · Le modèle de l'anneau du Noyau — ~1,8 % sur une Nuée
La géométrie est **exacte** : 78 px, axe r 35, épaisseur 8 pour « toi » ; 58, r 26, 6 pour
une entité. Mesuré au pixel sur le canevas. **C'est le MODÈLE qui diffère :**

```
la planche   deux arcs   un cercle plein « reste » + un arc « tenu » en dasharray
             cadre 48    reste #F07A2E · tenu #2BE88C sur 72 % du tour
             cadre 10    reste #D0B0FF (la Nuée) · tenu #2BE88C
l'app        trois arcs  tenu #2BE88C · en cours #8FA0FF · à tenir #F07A2E,
                         joints dégradés sur 3 % du tour, proportions réelles
```

L'app dit **trois** états, la planche **deux**. Passer à deux perdrait « en cours » — une
décision de produit, pas une correction. Et les proportions elles-mêmes dépendent des
données. **Les couleurs, elles, sont corrigées** : elles suivent le §3 depuis aujourd'hui.

### 3 · La place de la dalle dans une carte d'Index — ~1 % (Q86, ouvert)
```
carte              planter  crêpes  potager  courir  nager  plongeoir
centre de la dalle    82,5   126,0    62,0    82,5   116,0    82,5    (centre carte 82,5)
```
Trois centrées, trois non — et le cadre 74 place les mêmes dalles à des fractions
**différentes** de la largeur (0,750 contre 0,764 pour « faire les crêpes »). Il n'y a pas de
règle à en tirer : la planche les a posées à la main. **L'app centre.**

### 4 · Le bouton ⇅ — ~0,2 %
Le cadre le rend en `content-box` (**62 × 62**) quand sa voisine, la barre de recherche, est
en `border-box` (270 × 56). Le tableau du §5 écrit **56 × 56** pour les deux, l'app pose
56 × 56, `releve-S4` le valide. **Le document et l'app s'accordent contre un oubli de rendu.**
Voir `ECARTS-MOODBOARD § 0 bis.3`.

### 5 · Les données du potager — sur la Nuée seulement
Les deux planches ne donnent pas les mêmes Promi au potager (voir `ECARTS-MOODBOARD § 0 bis.1`).
Le jeu suit **moodboard-H** pour le contenu — l'Index et le Fil en dépendent — et
**`promi-nuee-toile`** pour la loi du champ, qui fait foi. Les titres diffèrent donc, et
quand l'un tient sur une ligne et l'autre sur deux, la seconde ligne tombe **hors de la boîte
de texte** et se compte. C'est le prix du désaccord entre les deux planches, pas un défaut.

---

## 4 quinquies · CE QUE LES DÉCISIONS DU 29 AOÛT ONT CHANGÉ

| décision | ce qu'elle a retiré | mesuré |
|---|---|---|
| **Q80** · les glyphes sont la seconde exception | la substitution Hanken Grotesk → Apfel comptait comme un écart de dessin sur tous les écrans | écrite en règle au § 8 bis ; `_zonesTexte` couvre désormais aussi les **`<input>` à placeholder** — « ⌕ Rechercher » n'était pas déclaré, faute de nœud texte : la bande 120 de l'Index et du Fil est passée de **10 % à 5 %** |
| **Q84** · `promi-nuee-toile` fait foi | le cadre 58 donne base 232 pour 6 Promi, que la loi ne produit pas ; le cadre 60 donne 282 pour zéro là où la loi donne 460 | `nuee` **17,3 % → 5,2 %** · `nuee-vide` **11,8 % → 5,2 %** |
| **Q83** · un gardé de côté n'a pas de dalle | la boîte de matière était déclarée sur une carte qui ne peint rien — un masque sans matière dessous | `peintCarte` n'annonce sa boîte **qu'après avoir dessiné** |
| **index-3** · la répétition est un artifice | le cadre porte douze cartes dont quatre répètent les premières | mesuré sur les rangées 1 et 2, **fenêtre déclarée et imprimée** : `21,3 % → 2,7 %` |
| **Fil 4** | l'entête comptait `FEED.length` | il compte les gestes qui viennent d'ailleurs — **4**, comme le cadre |

---

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

## 29 août 2026 — lot « rien ne survit » + Q30 levée de sa borne

**Point de reprise : `sauvegardes/lot-rien-ne-survit.html`.**

**Ce qui est fait et vérifié**
- **La cause générale des écrans vides**, en trois couches (Q91) : ce qu'un écran masque
  (`data-masque`), ce qu'il pose en ligne (`data-pose`), ce qu'il bâtit (registre
  `window._rangeurs`). `closeAll` défait exactement ça, et rien de plus.
- **`redteam_vide.py`**, le contrôle qui manquait : il **enchaîne** 15 écrans sans
  recharger, 2 tours × 2 thèmes. **61/61.** Prouvé contre la version fautive : **28/61**.
- **Q92 — la teinture de Q30 n'était appliquée nulle part sur une fiche** (bornée à
  `auPlancher`, faux partout). Levée. La dalle de fiche est stable et lisible : écart de
  luminosité **97** sur le champ bleu, quatre chargements neufs.
- **Les 32 captures ont été regardées une par une.** Aucun écran vide, aucun élément
  d'entête, trait, titre ou état manquant.

**Au vert :** redteam_ecrans 146 · redteam 15 · redteam2 10 · redteam3 18 · demande 19 ·
toile 17 · geste 13 · verbe 6 · filets 0 parasite · aveugle 26 · fonctions 22 ·
tonsurton 26 · formes 38 · nuee 24 écrans 0 écart · polices 0 couple absent · champs 22 ·
enchaine 24 · pastilles 12 · photo 27 · phrase 6 · **vide 61** · S1 · S2 · S3 · S4 · S5 ·
`releve-design` AUCUN ÉCART.

**Ce qui reste ouvert — voir QUESTIONS.md · Q93** (huit écarts vus à l'œil, un lot chacun).
Le premier est un **fork réel** : une dalle peut sortir invisible dans l'Index et le Fil,
et les deux règles qui s'appliquent se contredisent (§3 interdit absolu du ton sur ton
contre §4 / Q30 bis qui borne la teinture à la bande haute).

## 29 août 2026 (soir) — trois corrections de dessin, le champ qui cède, l'écran encombré

**Point de reprise : `sauvegardes/lot-trois-corrections.html`.**

**Ce qui est fait et vérifié**
- **Le tiroir ne se peint plus par-dessus un écran.** Trois couches déjà traitées le matin
  (masque · style en ligne · nœuds bâtis) ; s'y ajoute **l'invariant**, désormais dans
  `redteam_vide.py` : *le corps du tiroir ne se voit QUE s'il est déplié*, et une fiche ne
  porte jamais un nœud du tiroir de Nuée (`.s2-titre`, `.s2-bouton`, `.s2-fermer`).
  On vérifie l'état, plus l'itinéraire. Le contrôle **attend l'écran posé** au lieu d'un
  délai fixe — il sortait un faux rouge une passe sur deux.
- **Q93 pt 1 — le champ cède.** Quand la dalle et le champ se rencontrent, c'est LE CHAMP
  qui bouge : luminosité seule, dans l'espace HSL, la teinte de nature intacte. Le §4 reste
  entier — **aucune teinture hors bande haute**. Mesuré, décision publiée par le peintre
  (`data-cede`) : **minimum 42** sur toutes les cartes d'Index et tous les bandeaux du Fil,
  deux thèmes, deux chargements.
- **Les trois corrections de dessin, toutes fiches, toutes natures** : le mot du geste
  remonte entre le trait et les disques ; les textes centraux montent d'un cran (21→23,
  38→42, 12,5→13,5), le titre redescendant d'un point à la fois si la ligne casse
  (plancher 38) ; sans mot du geste, le bloc remonte de 24.
- **Q30 étendue là où elle manquait** : la teinture s'applique aussi à **l'instant**, qui
  peignait sa dalle non teintée — `releve-S5` le relevait, « le centre a exactement la
  couleur du champ ».
- **Le gardé de côté** : `window._ppGarde` était lu et jamais posé. Posé à `reprendreBrouillon`.
  L'aplat disparaît, « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS » apparaît, le rond photo s'efface.
- **Le titre d'une carte d'Index ne touche plus l'état** (CASSE.md) : 0 débordement,
  0 chevauchement, deux densités, deux thèmes.
- **Le mot du geste de la page +** suit l'état (Q97) ; **« DANS 2 JOURS »** vient du cadre 44
  et ne se calcule plus sur l'horloge.
- **La teinture mauve de la bande d'une Nuée, posée puis RETIRÉE** — Q94, j'avais mal lu la
  planche.

**Au vert :** les 20 batteries · les 5 juges · `releve-design` (refigé : 28 écarts, tous sur
`à qui` / `titre` / `état` d'une fiche, c'est-à-dire le lot, rien d'autre).
**Contrats réécrits au niveau de la décision (§7)**, originaux dans `sauvegardes/` :
`releve-S1-fiches` (les cotes se déduisent de la règle au lieu d'être recopiées ; le titre a
une RÈGLE, pas une taille), `releve-S3-page-plus` (le mot du geste), `releve-S4-index-fil`
(le titre d'une carte), `releve-S5-instant` (l'état à 13,5).

**Les 32 captures ont été regardées une par une.** Aucun écran vide, aucun écran encombré.

**Ce qui reste, et pourquoi je ne l'ai pas fait :** Q95 (le potager à 7 Promi) et Q96
(l'anneau d'une personne) demandent tous deux **d'inventer des Promi de démonstration** —
la planche annonce des nombres qu'elle ne nomme pas. Le §9 l'interdit. Il manque des mots.

## 29 août 2026 (nuit) — l'air, les Réglages, le jeu de démonstration

**Point de reprise : `sauvegardes/lot-air-et-demo.html`.**

- **L'air rendu.** Le cran du soir avait mangé l'espace partout où une cote dérivée était
  calculée pour l'ancienne taille : `à qui → titre` 6,9 → 4,7 sur les cinq états, l'état
  −1,1 sous chaque fiche et chaque Nuée. Les cotes sont réécrites dans la bonne unité
  (« hauteur du bloc + air ») : à l'ancienne taille elles redonnent le moodboard au dixième.
  Et le mot d'un gardé de côté a retrouvé les **23 px** du cadre 26 (il en avait 9).
- **`redteam_air.py`**, la 21ᵉ batterie : l'espace réel entre deux blocs de texte, 36 écrans,
  **391 paires**, référence `air-reference.json`, `--figer` comme `releve-design`.
  Prouvé à **18 rouges** sur la version « cran sans les écarts ».
- **Les Réglages** : l'encart du profil retiré, photo et nom sur le fond (Q99).
- **Le jeu de démonstration** complété avec les mots de Tom (Q100) — potager 9 Promi,
  Index 16, anneau de Rachel à deux arcs. Q95 et Q96 sont closes.

**Au vert :** 21 batteries · 5 juges · `releve-design`. Les 32 captures regardées une à une,
deux thèmes : aucun écran vide, aucun encombré, aucun texte qui touche son voisin, aucun ton
sur ton.

**Prochain : le Studio, l'Aura, le partage.**

## 29 août 2026 — le champ porte toujours sa nature

**Point de reprise : `sauvegardes/lot-champ-de-nature.html`.**

- **Le défaut signalé.** Sur la page + en thème clair, le champ sortait **crème** — la
  couleur du corps : la dalle flottait sur du vide et « trace pour planter » était posé sur
  du crème. Cause : ma lecture fautive de Q83. « Un gardé de côté n'a pas de **dalle** » ne
  dit rien du **champ**, et la même décision précisait « sa carte d'Index garde le champ de
  nature, **sans matière** ». J'avais éteint l'aplat à **trois** endroits — la fiche, la
  page +, la carte d'une Nuée vide. Les trois sont corrigés : l'aplat reste, `sansMatiere`
  prend le relais.
- **`redteam_champ.py`**, la 22ᵉ batterie, 16 écrans × 2 thèmes → **32/32**. Au-dessus du
  trait : aucun pixel de couleur de corps, aucun champ transparent, et **chaque peintre
  déclare ce qu'il a versé** (`data-champ`). Prouvé à **2 rouges** sur la version au champ
  éteint (« le champ est TRANSPARENT à 96 % — le corps se voit dessous »).
- **`releve-S3` réécrit au niveau de la décision** (§7) : il exigeait « pas d'aplat sur un
  gardé de côté », il exige maintenant l'inverse. Original en
  `sauvegardes/releve-S3-page-plus-avant-champ.py`.
- **Le potager garde ses neuf Promi** — l'encart dit le contenu réel (décision Tom).

**Au vert :** 22 batteries · 5 juges · `releve-design`. Les 32 captures regardées une à une,
deux thèmes : aucun écran vide, aucun encombré, aucun texte qui touche son voisin, aucun ton
sur ton, **aucun champ blanc**.

**Prochain : le Studio, l'Aura, le partage.**

---

## Lot du 2 septembre 2026 — LE PLATEAU DU STUDIO, POSÉ PARTOUT À SA PLACE

**Demande de Tom** (1er septembre) : *« on repart de celui de studio qui fait référence,
déploie-le en changeant les titres et les spécificités liées à chaque page ; la mise en
page d'avant était logique, fallait juste du fine tuning. »* Puis : *« go full
verifications et focus. »*

### Ce que la vérification a trouvé, et que le lot précédent avait manqué

Le lot précédent posait l'encart **dans le flux**, à la place de l'ancien titre : il
héritait donc du `padding-top` de chaque écran. Mesuré, chaque écran ouvert **par sa vraie
porte** (jamais en forçant `.show`) :

```
Réglages 0 · La langue 38 · La confidentialité 38 · Aura 54 · Arranger 54
Comprendre ton Aura 76 · Le Cercle 203 · Partager 0 × 0 hors cadre
```

La référence est à **40**. Deux écrans seulement y étaient — l'Index et le Fil, les deux où
je l'avais posé **en absolu**. C'est donc l'absolu qui est la règle.

### `lot-PLATEAU-PARTOUT`

1. **La géométrie se pose EN LIGNE**, pas en feuille — 24 / 40 / 342 × 60, rayon 30,
   padding 26, fond du corps, contour 2 px d'encre, titre Bricolage 700 / 27.
2. **L'écart d'origine est rendu** : `padding-top` = 100 + l'écart mesuré avant le lot
   (28 aux Réglages, 4 à l'Aura, 8 à Arranger / la langue / la confidentialité, 16 à
   Comprendre ton Aura). On préserve l'ÉCART, pas la position.
3. **Le plateau ne défile pas** : aux Réglages il vivait dans `#stScroll`, il est remonté
   en enfant direct de l'écran, comme au Studio.
4. **Partager** : son plateau est `#shcTitre` (contenu `.t` / `.f`, pas `.enh-t` /
   `.closeb`) — conformé nommément ; l'encart en doublon, mesuré 0 × 0 hors cadre, ne se
   peint plus.
5. **Le Cercle** : `.pl-eb` **est** le titre du plateau (déplacé, pas dupliqué) — je
   l'avais masqué, ce qui vidait le plateau. Rétabli.

### Quatre pièges du §8 rencontrés, tous documentés

- **Un `.screen` ne coïncide pas avec `#device`** — `#langScreen`, `#privScreen` et
  `#plusScreen` sont enfants de `.frame`, 422 × 876, l'appareil à 16, 16 dedans. Lu dans
  l'**arbre** (`contains`), jamais dans la disposition : `offsetParent` vaut `null` tant
  qu'un écran est masqué, et le décalage n'arrivait qu'au deuxième passage.
- **Une cote mesurée sur elle-même oscille** — ma première correction comparait deux
  `getBoundingClientRect` **pendant la transition d'ouverture** et a écrit des cotes
  fausses sur trois écrans qui étaient justes (Réglages large de 242,7 · Fil x −20,7 ·
  Index y −65). Repayé le piège de `cale()` au Studio.
- **Piège de spécificité** — `#settingsScreen > :not(#stTrameCv){width:auto!important}`
  pèse **deux ids** (le `:not(#id)` compte l'id qu'il contient) et bat `#device .enh`.
  Le plateau retombait en largeur automatique dans un parent `flex`, donc à la largeur de
  son contenu, et le titre suivait : **342 → 242,7 → 209,4**, titre **27 → 19**, d'une
  passe à l'autre.
- **Une course, pas une cote** — le plateau est BÂTI par `lot-ENCART-HAUT` ; à la
  toute première ouverture, `recale` passait avant que le nœud existe. On chaîne :
  bâtisseur → remonte → polices → recale → `_harmonie` (qui dimensionne les titres, donc
  parle en dernier).

### Deux défauts trouvés au balayage, sur la page Partager

- **`#shNyPctRow` « % d'harmonie »** flottait à **y 58 → 87, sur le plateau du titre**, à
  opacité 0,34. Orphelin de l'ancien Noyau : il vit dans `#shTray`, qui est en
  `display:contents` — donc **rien ne le masque**. Sa fonction est déjà dans le tiroir
  neuf, sous « CE QU'IL MONTRE → Harmonie chiffrée ».
- **Un tap ailleurs ne referme plus le tiroir** — la fonction existait sur l'ancien écran
  et s'était perdue à la refonte.

### `#plHeroCv` recadré

Le héros du Cercle débordait du téléphone de **16 px à gauche et 24 à droite** (il est
dessiné pour le cadre, pas pour l'appareil). Il prend le même décalage que le plateau —
même fait de structure, pas une seconde règle.

### Cinq contrats réécrits au niveau de la décision (§7)

`redteam.py` (4) et `redteam2.py` (1) visaient `#shTrayBtn`, `#shTrayWrap`, `#shFmtTxt`,
`.sh-top`, `.sh-foot` — **les nœuds de l'ancienne page Partager**, remplacés par la
décision de Tom du 1er septembre. Ils étaient rouges **avant ce lot** (vérifié sur deux
sauvegardes). Originaux conservés : `sauvegardes/redteam-avant-partage-sans-trait.py` et
`sauvegardes/redteam2-avant-partage-sans-trait.py`.

### Ce qui reste rouge, et pourquoi

- **`redteam_toile.py` ne tourne pas** — il s'arrête sur `ValueError: cannot convert float
  NaN to integer` (contrôle « planter des Promi change l'aperçu »). **Antérieur à ce lot**,
  vérifié sur les sauvegardes. Une batterie qui plante ne mesure rien : à réparer.
- **`releve-S4-index-fil.py` : 62 écarts** (20 de style, 20 de position), tous voulus par
  la décision de Tom. Pas de `--figer` : ses cotes sont écrites en dur contre
  `PROMI-SPECIFICATIONS §5`, où la décision est notée. Le juge reste à mettre à jour.
- **« Comprendre ton Aura » à 20 px** et non 27. Ce n'est pas un défaut d'ajustement :
  mesuré, le texte fait **268 px** à 27 px pour **197,5** disponibles (342 − 4 de bords
  − 52 de padding − 74,5 de FERMER − 18 d'écart). C'est le titre le plus long de l'app ;
  seul un mot plus court le ferait tenir, et un mot ne s'invente pas (§9). Question posée.

### Trois écrans n'avaient pas de fond — corrigé

Mesuré, chaque écran ouvert par sa porte, les deux thèmes :

```
#settingsScreen  #F4EEE1 clair · #12142A sombre     un fond
#auraScreen      #F7F3EA clair · #1C1D22 sombre     un fond
#langScreen · #privScreen · #plusScreen             rgba(0,0,0,0) — AUCUN
```

Ce sont **exactement les trois écrans frères de l'appareil**, ceux qui vivent dans `.frame` :
la même cause structurelle que le décalage de 16 px. La Toile de l'accueil traversait donc
le texte — « Essaie tout, sans t'engager » se lisait par-dessus les dalles — et la
confidentialité peignait son texte en `rgb(231,229,223)`, quasi blanc, **sur du transparent
en thème CLAIR**.

**Ce n'est pas un parti pris, et je l'ai vérifié avant de peindre (§9).** La feuille
d'origine dit l'intention : `.s-plus{background:var(--ground)}` (l. 1517). Le fond se perd
en route — `.tuto-fond` pose un `background` qui n'est QUE des dégradés (donc
`background-color` transparent), et `.screen.tuto-fond{background-image:none!important}`
retire ensuite les dégradés. Il ne reste rien.

**Antérieur à ce lot**, vérifié sur `sauvegardes/avant-plateau-partout.html` ouvert par sa
vraie porte. Corrigé avec **la valeur relevée sur Réglages**, pas une couleur choisie.
Sauvegarde d'avant : `sauvegardes/avant-fond-trois-ecrans.html`.

### Le sujet actif de Partager sortait sombre

`.frame.light #shareScreen #shMode button.on` (2 ids + 2 classes) battait
`#shcSujet button.on` (1 id + 1 classe) — à `!important` égal, c'est le poids qui tranche.
Reposé au même poids, dans les deux thèmes : crème sur bleu, comme le plateau et comme
« Partager ».

### L'aperçu de Partager était rogné de 65 px

`shareRender()` pose la place de `#shWrap` **en ligne**, centrée pour l'ANCIENNE zone. Le
lot a déplacé la zone à 120 → 570 ; le calcul n'a pas suivi : image à 220 → 635, donc
**100 px de vide en haut et 65 px coupés en bas** — dont le mot-marque de l'image, le sujet
même de l'écran. Recentré après coup, comme le §8 le prescrit (on enveloppe). Mesuré
après : image 138 → 553 dans la zone 120 → 570, mot-marque visible au doigt.

### État des batteries, à la livraison

```
redteam_ecrans   150/150      redteam            15/15  (4 contrats réécrits)
redteam2          10/10  (1)  redteam3           18/18
redteam_demande   19/19       redteam_geste      13/13
redteam_verbe      6/6        redteam_tonsurton  26/26
redteam_champ     32/32       redteam_vide       61/61
redteam_filets    0 parasite  redteam_air        384 paires, intact
releve-design     AUCUN ÉCART
```

**`redteam_air` : 384 paires contre 387 avant le lot.** Le diff paire à paire
(`/tmp/air_diff.py`) donne la raison exacte : **trois paires ont changé de CLÉ**, parce que
le nœud du titre a gagné la classe `.enh-t` — `.scr-ti«Réglages»` est devenu
`.scr-ti.enh-t«Réglages»`. Même nœud, même mesure, même écart. C'est un **renommage**, que
le §7 distingue explicitement d'un contrat périmé.

**Deux rouges subsistent, tous deux antérieurs :**
- `redteam_toile.py` s'arrête sur `ValueError: NaN` — la batterie ne mesure rien (Q150).
- `releve-S4-index-fil.py` : 62 écarts voulus par la décision de Tom, juge à mettre à jour.

---

## Lot du 2 septembre 2026 (2) — LE BANDEAU SUR LA FICHE, ET L'ÉCHELLE DU TEXTE

**Demande de Tom** : *« la page Aura on l'a pas encore refaite, tout va être à revoir de
toute manière, donc intègre juste le bandeau commun comme sur les autres pages (cohérence
dans toute l'app sur les éléments communs est une règle d'or absolue) / mets la même taille
de police dans tous les titres que dans Studio, Studio actuel est la ref, grossis un peu le
reste / dans Fil et Index les chiffres sont trop petits, grossis un tantinet aussi / dans
aucune fiche j'ai vu que t'avais mis le bandeau, faut le faire. »*

### La référence, relevée sur le Studio

```
titre   Bricolage 700 / 27 px · interlettre −0,945 px
fermer  ApfelMid 500 / 12 px · interlettre 2,4 px
```

Les neuf plateaux y étaient déjà. Ce qui manquait, c'était **la fiche** et **le reste du
texte**.

### La fiche a son bandeau

**Et j'avais écrit une chose fausse dans le code**, en excluant la fiche du déploiement :
« elle n'a aucun nœud de mot-marque dans son DOM ». Elle en a un — **`.dpt-nat`**, qui porte
le NOM DE LA NATURE (« Promi », « Chiche »), en Fraunces 600 / 27, à y 38, avec « FERMER » à
x 282, y 38. C'est exactement le contenu d'un plateau, à la bonne taille et presque à la
bonne place. **Ce qui manquait n'était pas le mot, c'était la boîte.**

Trois obstacles, tous mesurés :

1. **La fermeture d'une fiche est composite** — une croix SVG de 58 × 58 avec « FERMER »
   dessous, **58 × 77 de haut pour un plateau qui en fait 60**. La croix débordait par le
   haut et par le bas, le mot tombait sous la boîte. Elle prend la forme commune : une ligne
   de texte, « ✕ FERMER ». La croix SVG est **masquée, pas supprimée**.
2. **Un lot de fiche peint le mot et le FERMER en `color: crème !important` EN LIGNE** —
   c'est la clause du §3 (« la zone haute garde le traitement sur couleur pleine »), juste
   quand ils sont posés à nu sur la bande de nature, fausse dans un plateau crème : le mot
   devenait invisible, crème sur crème, et le plateau paraissait vide. On répond dans la
   même monnaie, en ligne, et après.
3. **Le mot « FERMER » vit dans un ENFANT de `.closeb`** — peindre le parent ne l'atteignait
   pas : le ✕ passait à l'encre, le mot restait crème. On peint le nœud et sa descendance.

**Vérifié : 6 fiches sur 6, dans les deux thèmes** — Promi tenu, à tenir, en cours, Chiche
en cours, Chiche tenu.

### Les chiffres du Fil et de l'Index

Le compte était à **17** à côté d'un titre de 27 — rapport 0,63. Posé à **20** : rapport
0,74. Il se lit, sans concurrencer le mot.

### L'échelle du texte — et pourquoi c'est un PLANCHER, pas un facteur

Relevé avant le lot, écran par écran :

```
Index 10px×6 · Aura 10px×4 · Le Fil 11px×4 · Réglages 11,5px×8 · Arranger 11px×1
```

**Le §6 dit « rien en dessous de 12 px ».** Un tiers du petit texte du produit était sous son
propre plancher.

**J'ai d'abord posé un facteur uniforme de 1,08. `redteam_air` a répondu : 156 paires
resserrées**, dont, dans l'Index, `« planter un arbre » → « TENUE »` qui passe de **2 px à
0** — le titre touchait sa ligne d'état, sur les six cartes et dans les deux thèmes. La cause
est au §8 : **une carte d'Index est en cotes absolues** (`top: 124 / 141 / 174`), calculées
pour les tailles d'alors ; un texte qui grossit ne déplace aucun `top`.

**Loi retenue : `max(13, taille)`, seulement sous 20.** Un plancher ne touche que ce qui
était trop petit. Résultat : **43 paires au lieu de 156, et le pire est −1,5 px sur des
écarts de 55 à 68** — 2 %, dû à l'agrandissement lui-même, aucune paire n'approche zéro.

**Et ce qui ne tient plus redescend** : « 9 PROMI · 3 TENUS » demandait 146 px pour 140
disponibles dans sa carte — il était coupé net. Repli par pas de 0,5 jusqu'à ce qu'il tienne,
**butée à 12**, le minimum absolu du §6. Mesuré stable sur deux passes : `13 13 12,5 13 …`.

**Ce que je n'ai PAS fait, et il faut le dire :** aller au-delà du plancher demande de
**recalculer les cotes absolues de chaque écran** — un lot par écran, avec son juge.

### Une régression attrapée par `redteam_vide` — 25/61

Le déplacement du FERMER dans le plateau l'a sorti d'un sélecteur qui le visait **par sa
place** : `#detailPoster>.closeb` — enfant DIRECT. C'est le piège du §8 que ce lot avait
lui-même écrit deux fois, et qu'il a repayé une troisième.

**Trois contrôles réécrits, au niveau du chemin et non de l'intention** — `redteam_vide.py`
(4 occurrences), `redteam_photo.py` (1), `releve-S1-fiches.py` (1) : `#detailPoster>.closeb`
devient `#detailPoster .closeb`. Le nœud existe, il est visible, il ferme la fiche : seule sa
PLACE a changé, par décision. Originaux conservés en `sauvegardes/*-avant-bandeau-fiche.py`.

Après : **61/61**.

### La passe typographique a dû être réécrite deux fois — et c'est le §6 qui l'a dit

**1 · Elle figeait des cotes FLUIDES.** Ma première version mémorisait la taille d'origine
dans `data-t0` et calculait à partir d'elle. Or plusieurs tailles de ce produit ne sont pas
en pixels : `.tenir-lab` (le libellé du geste) mesure **14,403 px dans le viewport du juge et
17 dans le mien** ; `.dpt-quand` (l'état d'une fiche) donne **13,5 à un instant, 12,5 à un
autre**. Mémoriser, c'est geler : la passe écrivait en dur une cote qui devait respirer, et
`releve-design` lisait « 14,403 → 17 », un écart que personne n'avait demandé.

**Le §6 donne la marche à suivre, mot pour mot, à propos de `lot-POLICES`** : « La passe se
RELIT, elle ne fige pas : sur un élément déjà touché elle retire d'abord son propre inline,
relit ce que la cascade dit vraiment, puis décide. » La passe ne garde plus **aucune
valeur** — seulement une marque `data-ech` qui dit « c'est moi qui ai écrit ».

**2 · Elle laissait sa trace dans le plateau.** Le plateau d'une fiche est bâti APRÈS : au
premier passage, son FERMER était encore dans le corps, la passe l'a monté à 13. Une fois
entré dans le plateau on l'ignorait — mais l'inline restait, et le FERMER sortait à **13 là
où la référence du Studio dit 12**. Ignorer ne suffit pas : il faut retirer sa propre trace.

### État des batteries, à la livraison

```
redteam_ecrans  150/150   redteam           15/15    redteam2      10/10
redteam3         18/18    redteam_demande   19/19    redteam_geste 13/13
redteam_verbe     6/6     redteam_tonsurton 26/26    redteam_champ 32/32
redteam_vide     61/61    redteam_filets    0 parasite
```

**`releve-design` : 90 écarts, tous classés, tous demandés par le lot.**

```
50  fiche · fermer      la fermeture prend la forme commune (ApfelMid 500/12, static, h 12)
28  fiche · nature      le mot de nature entre dans le plateau (static, h 27, z auto)
 8  nuee · mot temps    10,5 → 13   le plancher du §6
 4  nuee · a qui ligne  12,5 → 13   le plancher du §6
```

**`redteam_air` : 41 paires resserrées — et la plus grave n'est PAS de la typographie.**
Dans le Peaufiner d'une **Nuée**, `« écris un mot… » → « visibles par les membres »` passe de
**4,5 px à −0,5** : deux boîtes de texte se croisent d'un demi-pixel. **Mesuré au banc :
l'écart valait 5 avant le lot du bandeau et −1 après, À TAILLES DE POLICE IDENTIQUES**
(18 / 14, `data-ech` nul sur les deux nœuds). C'est donc le **bandeau** qui décale la boîte du
Peaufiner d'une Nuée, pas l'échelle. **Je ne l'ai pas corrigé** : la carte du Peaufiner d'une
Nuée a ses propres cotes, et y toucher est un lot à part, avec son juge.

---

## Lot du 2 septembre 2026 (3) — LA GRAMMAIRE DES CONTOURS, ET LA PAGE +

**Demande de Tom** : *« tout mettre au vert, bel agencement, cohérence dans toute l'app sans
exception, taille des polices, placement des encarts, dans les fiches aussi mais vraiment
toutes les pages, page + à intelligemment intégrer, et dans toute l'app revoir les traits et
contours pour ne pas créer de décalages visuels et que le cadre paraisse plus marqué que le
reste — le reste s'y adapte donc. »*

### Le relevé d'abord

Planche publiée : **la grammaire des contours**, relevée écran par écran. La règle existait
déjà presque partout — **trait 2, couleur du corps, rayon = hauteur ÷ 2**. Quatre familles
s'en écartaient, et c'est ce qui faisait paraître le plateau « à part » :

```
Réglages, sept rangées   342 × 64  trait 3  rayon 22   → trait 2, rayon 32
tri du Fil + Aura        bonne cote, crème 231,229,223 → la crème du corps
Arranger, quatre rangs   filet 1 px à 13 %, large 346  → 2 px lisible, largeur 342
Le Cercle, cinq pastilles 30 × 30  trait 1  rayon 10   → trait 2, rayon 15
```

**Mesuré après : 0 écart sur dix écrans**, les trois cotes vérifiées.

⚠ Les rangées **sous le bloc du Cercle** ont leur propre règle, `#device #settingsScreen
.s2-cercle .s2-reg` — deux ids ET deux classes : elle battait la mienne, quatre rangées
restaient à 3 px. Reposée au même poids.

### La page + a son plateau — sauf là où l'écran est nu par décision

Elle avait **déjà** son mot-marque `.cs-mark` (Fraunces 600 / 29) — mais mesuré **à x −20,
y −44 : hors cadre**. Seul « FERMER » se voyait. Le plateau le ramène, à 27 comme au Studio.

**Sur l'écran des trois choix, pas de plateau — et c'est une décision antérieure.** Une règle
du produit masque nommément le mot-marque, la trame et la grappe quand `#createSheet` porte
`pp-choix` : cet écran est nu, la QUESTION y fait titre. Un plateau bordé à titre vide y
ajoutait un cadre que l'écran n'a jamais eu, et la question le chevauchait. Le §9 tranche.
**Le FERMER ressort avec le plateau** et y revient à l'étape suivante — sans quoi l'écran
perdait sa seule porte.

⚠ Deux pièges repayés : je cherchais le FERMER **dans** le plateau, donc une fois sorti je ne
le retrouvais plus ; et j'ai lu le plateau **à y −4 pendant la transition d'ouverture** de la
feuille — mesuré à l'arrêt, il est à 40.

### Le seul écart non voulu, et ce qu'il a coûté

Dans le Peaufiner d'une Nuée, « écris un mot… » touchait « visibles par les membres » —
5 px avant le lot du bandeau, **−1 après**.

**J'ai d'abord rendu six pixels à la carte. C'était pire :** `min-height: 110` a poussé les
cartes suivantes et `MEMBRES → PIÈCES JOINTES` est tombé de **58,8 à 35,3**. La carte
appartient à une pile à cotes fixes — lui rendre de la hauteur la prend ailleurs.

**La bonne réponse était ma propre loi** — « ce qui ne tient plus redescend ». Ici ça ne tient
pas en HAUTEUR : les textes de `.np-carte` sont exclus du plancher typographique. Écart revenu
à **5,0**.

### Les deux références sont figées, sur l'état que Tom a validé

`redteam_air` : 33 paires resserrées, **aucun chevauchement**, pire cas −5 sur 47 — toutes
l'agrandissement demandé. `releve-design` : 90 écarts, tous classés (la fermeture et le mot
de nature qui entrent dans le plateau, le plancher du §6). Le juge prévoit ce cas mot pour
mot : « Si le lot demandait ce resserrement, refige. » **On ne desserre pas un seuil, on met
à jour une référence après un changement demandé.** Anciennes références conservées :
`sauvegardes/air-reference-avant-grammaire.json`, `design-reference-avant-grammaire.json`.

### État final — tout est vert

```
redteam            15/15      redteam2          10/10      redteam3        18/18
redteam_demande    19/19      redteam_verbe      6/6       redteam_geste   13/13
redteam_ecrans   150/150      redteam_champ     32/32      redteam_vide    61/61
redteam_tonsurton  26/26      redteam_filets   0 parasite
redteam_air      374 paires · L'AIR EST INTACT
releve-design    ✅ AUCUN ÉCART
```

⚠ `redteam_air` avait sorti **2 paires** au passage précédent, puis **INTACT** au suivant,
sans qu'une ligne bouge. C'est le flottement que le §7 décrit : un rouge isolé se reconfirme
avant d'être cru.

**Deux rouges restent, tous deux antérieurs et signalés :**
- `redteam_toile.py` s'arrête sur `ValueError: NaN` — seize contrôles de la Toile sont
  **aveugles**, pas verts (Q150).
- `releve-S4-index-fil.py` : 62 écarts voulus par décision, juge à mettre à jour.

---

## Lot du 2 septembre 2026 (4) — LES CARTES QUI SE SUPERPOSAIENT, ET LA DALLE SOUS LE BANDEAU

**Signalé par Tom, captures à l'appui.**

### 1 · L'Index : le titre et l'état se recouvraient

Mesuré sur les **neuf cartes**, sans exception : le titre finit à **174**, l'état est ancré à
**170** — **4 px de superposition**.

La ligne d'état est calée **par le bas** (`top = bas − sa hauteur`). Elle a grandi de 10 à 13
avec le plancher du §6, donc son `top` a reculé de 4 px et elle est entrée dans le titre.
**On ne reprend pas la taille** — Tom a demandé que ces textes grossissent : **on rend
l'ancrage**, l'état se cale au bas de la carte à 6 px. Air rétabli : **2 à 5,5 px** partout.

⚠ La règle visait d'abord aussi les bandeaux du Fil, qui n'ont ni la même hauteur (128 contre
198) ni le défaut : `redteam_air` a compté 24 paires. **Restreinte à l'Index.**

### 2 · Trois états de carte étaient coupés net

`« 9 PROMI · 3 TENUS »` demandait **180 px pour 140**, `« GARDÉ DE CÔTÉ »` 153 pour 140.
⚠ **Ce n'est pas le plancher** : la taille lue est 16 et `data-ech` est nul — c'est la taille
naturelle, et elle est fluide. Le défaut est antérieur. Ces lignes prennent l'arbitrage du
titre de plateau : repli de 0,5 en 0,5 jusqu'à ce que le mot tienne, **butée à 12**.

### 3 · La dalle passait sous le bandeau — une seule ligne en cause

Tom : *« les dalles apparaissent superposées et sous le bandeau du titre et ✕ fermer ; elles
sont tronquées et cachées car elles passent dessous ».* Il avait raison au pixel :

```
e.dalle = { y: 88 }        le plateau descend à 100
                           →  12 px de matière sous le bandeau, par construction
```

Le 88 datait d'un temps où l'entête n'était pas une boîte. **La dalle démarre à 124** — le bas
du plateau plus 24 d'air, le pas du produit — et sa hauteur se recalcule d'autant.

### 4 · Le trait descend de 24

Place libre mesurée entre le dernier élément et la barre Peaufiner, par état :

```
à tenir 133 · Promi tenu 91 et 56 · Chiche tenu 97 · en cours 36 · Chiche 36
```

**Le pire cas commande : +24**, qui laisse encore 12 px sur les états « en cours », les plus
chargés. Un delta plus large tiendrait sur une fiche à tenir et écraserait une fiche en cours.
Vérifié : **0 débordement sur les six états**.

⚠ **Ce que ça ne donne PAS, et je le dis :** la dalle n'est pas beaucoup plus grande — la
marge des états « en cours » l'interdit. Ce qu'elle a gagné, c'est d'être **entière**.
Pour l'agrandir vraiment, il faudrait revoir la pile de ces états-là : un lot à part.

### Batteries

```
ecrans 150/150 · geste 13/13 · vide 61/61 · champ 32/32 · tonsurton 26/26
filets 0 parasite · releve-design ✅ AUCUN ÉCART · air refigé (20 paires, pire −6 sur 112)
```

---

## Lot du 2 septembre 2026 (5) — LA BATTERIE AVEUGLE, ET LA PAGE D'UNE PERSONNE

### `redteam_toile` remesure : 17/17

Elle s'arrêtait sur `ValueError: cannot convert float NaN to integer` depuis un moment —
**dix-sept contrôles de la Toile ne mesuraient rien**, ce qui est pire qu'un rouge.

Le bug était dans **la sonde, pas dans l'app**, et il vivait dans quatre endroits
(`redteam_toile` ×2, `redteam3`, `redteam_geste`) :

```js
for(let i=0; i<im.length; i+=97) s = (s + im[i]*31 + im[i+1]*7 + im[i+2]) % 1000000007;
```

Au dernier tour, `im[i+1]` et `im[i+2]` sortent du tableau → `undefined` → **NaN**, qui
contamine tout le hachage. Ça ne se déclenche que quand la taille du canevas tombe mal
(`length − 97k ∈ {1, 2}`) : d'où l'intermittence, et d'où le fait que `redteam3` et
`redteam_geste` passaient pendant que `redteam_toile` mourait. Borne corrigée : `i+2 <
im.length`. Originaux : `sauvegardes/redteam_*-avant-hash-nan.py`.

### La page d'une personne a son plateau

Elle avait déjà son « ✕ Fermer » à y 38 en ApfelMid 12 — la bonne place, la bonne taille.
Ce qui manquait, comme partout, c'était **la boîte**. Le modèle retenu est celui du Cercle :
le plateau porte le nom de l'écran (« Rachel », Bricolage 27), l'avatar et « votre harmonie »
restent dessous.

⚠ **Le contenu ne descendait pas tout seul** : la feuille a `padding-top: 54` et tout y est
en flux, donc son contenu démarrait à **y 40** — exactement là où le plateau commence.
L'avatar dépassait à gauche du plateau, « votre harmonie » se lisait derrière lui.
`padding-top: 136` (+ la marge de 2 du premier bloc − le décalage de 14 de la feuille) le
pose à **124** : le bas du plateau plus 24 d'air, la même cote que la dalle d'une fiche.
Vérifié au doigt : dans la bande 44 → 96, on ne touche que le plateau.

---

## Lot du 2 septembre 2026 (6) — LE PLATEAU NE PART PLUS AVEC LE DOIGT

**Tom m'a laissé trancher les trois points ouverts. Décisions prises :**

### 1 · Q151 — le plateau reste, partout

Sur six écrans il tenait, sur trois il partait : Aura, Comprendre ton Aura et Le Cercle sont
**leur propre conteneur de défilement**, et un enfant absolu d'un conteneur qui défile s'en va
avec son contenu. Mesuré : le plateau tombait de **40 à −360**, et « ✕ FERMER » avec lui.
Un élément commun qui reste ici et part là n'est pas commun.

⚠ `position:fixed` n'y change rien — mesuré, il tombe à −360 pareil : ces écrans portent une
transformation, qui devient le bloc englobant de tout `fixed` qu'ils contiennent. On compense
donc le défilement (`translateY(scrollTop)`) : ce n'est pas une cote auto-référente, le
défilement ne dépend pas de la position du plateau.

⚠ **Deux erreurs corrigées en route.** J'ai d'abord énuméré cinq écrans : le Fil n'y était pas
et son plateau tombait de 40 à 24 — on part maintenant des PLATEAUX, pas d'une liste écrite à
la main. Puis le voile ne faisait que 40 de haut : entre 40 et 100, **de part et d'autre du
plateau**, le contenu passait encore (le « E » de « Essaie tout » dépassait à gauche). Il fait
100.

⚠ **Et une régression que la batterie a attrapée.** Généralisé, le voile a fait tomber
`redteam_tonsurton` de **26/26 à 22/26**. Vérifié sur deux sauvegardes — vert dans les deux,
donc la faute était de moi. Le Fil fait défiler sa LISTE (`#feedList`, à 212), pas son écran :
rien n'y remonte au-dessus du plateau, et un aplat de plus n'y protège rien. **Le voile est
borné aux trois écrans qui en ont besoin ; le déplacement du plateau, lui, reste général.**
Après : **26/26**.

### 2 · `#previewScreen` — pas de plateau, et c'est la décision

Son titre est **en bas, sous l'aperçu** : lui poser un entête en haut, ce serait lui en
inventer un (§9). Il garde sa composition.

### 3 · `releve-S4-index-fil.py` réécrit au niveau de la décision (§7)

Il était vert sur tout ce qui compte — **8/8 sur les cartes isolées, 0 collision, 0
débordement, 0 manque de peinture** — et rouge de 114 sur les seules **cotes d'entête**, celles
que la décision du plateau a remplacées. Mises à jour, avec leur raison :

```
entête      h 44 → 60 · titre 38 → 27 · compte 26 → 20 · FERMER 12,5 → 12
recherche   y 108 → 124 · h 56 → 52 · contour 3 → 2 · rayon 28 → 26 · bord gris → encre/crème
tri         x 310 → 290 · 56 × 56 → 52 × 52
grille      y 196 → 212
```

Il cherche aussi le titre et le FERMER **dans le plateau**, en retombant sur l'ancien chemin
pour un écran qui n'en aurait pas. Original : `sauvegardes/releve-S4-index-fil-avant-plateau.py`

### Le juge S4 : 114 → 72, et les 72 restants sont classés

**Vert sur tout ce qui compte : 8/8 sur les cartes isolées, 0 collision, 0 débordement,
0 manque de peinture.** Les 72 restants se répartissent en deux familles, et la première est
de MA faute, pas de celle de l'app :

```
mes cotes de juge, fausses (à corriger dans le .py)
  « entête (52,57) au lieu de (24,40) »   je mesure le TITRE (.enh-t), pas la BOÎTE (.enh)
  « plateau haut de 27 au lieu de 60 »    idem — 27 est la hauteur du texte
  « ✕ FERMER droite 338 au lieu de 366 »  366 − 26 de padding = 340, pas 366
  « tri (314,124) au lieu de (290,124) »  le tri fait 52 et finit à 366 : 314 est le juste
                                          — j'avais pris 290 dans une règle CSS, pas dans
                                          une mesure

un vrai écart d'app, à vérifier
  « compte : Bricolage 700/17 au lieu de 20 »   sur les vues filtrées (« Index 2 / Index 3
                                          par ligne »), la règle qui pose le compte à 20 ne
                                          s'applique pas
```

**Je n'ai pas fini ce juge**, et je le dis plutôt que de le laisser croire vert.

### Le juge S4 : 114 → 0

Reprise du point laissé ouvert. Trois cotes de juge fausses — **les miennes** — et trois
contrats périmés par les décisions de Tom :

```
mes cotes, corrigées
  je mesurais le TITRE (.enh-t, à 52/57, haut de 27) au lieu de la BOÎTE (.enh, 24/40/342×60)
  j'attendais le FERMER à (366,40) : le padding de 26 le pose à 340, et il est CENTRÉ à 62
  j'attendais le tri à 290 — lu dans une règle CSS, pas mesuré : il fait 52 et finit à 366,
    donc 314

contrats périmés, réécrits au niveau de la règle
  l'état d'une carte était calé à 12 du bas → 6, l'ancrage qui a réparé la superposition
  l'état et l'eyebrow avaient une taille exacte (10 · 8 · 11) → « jamais sous 12, jamais
    au-dessus du titre » : le §6 fixe 12, et ces lignes sont FLUIDES (13 à 16 selon le
    viewport)
```

**Deux vrais écarts d'app, trouvés par lui :**

1. **Le compte restait à 17.** J'avais appliqué la décision de Tom (« grossis un tantinet »)
   plus haut dans le fichier — mais une règle du lot d'harmonie portait **exactement le même
   sélecteur** et venait APRÈS : à spécificité égale, la dernière l'emporte. Corrigé à la
   source, pas par une troisième règle.
2. **Le compte du Fil était bleu.** Le §5 lui donne le **menthe** — c'est la couleur de la
   parole tenue, et le Fil compte ce qui vient d'arriver. Le bleu reste celui de l'Index.

**Et une course :** à trois cartes par ligne, l'état sortait à **6,4 px** au juge alors que la
même vue ouverte à la main donne 12-13. `ouvrirIndex()` reconstruit `#indexList` **sans
changer aucune classe** — rien ne réveillait la passe. Elle observe désormais la liste
(`childList` seulement : elle écrit des styles en ligne, jamais des enfants, donc elle ne peut
pas se rappeler elle-même).

**Enfin, une correction d'harmonie :** sur une carte étroite (trois par ligne, 106 px), le
plancher de 13 rendait l'état **aussi gros que son titre** (12,9). Le plancher y vaut 12 — le
minimum absolu du §6 — ce qui laisse au titre les neuf dixièmes de point qui disent lequel
des deux commande.

---

# ⚑ OÙ REPRENDRE — état au 3 septembre 2026, PASSE FINIE + LE RYTHME DES FICHES

> Point de reprise : **`sauvegardes/lot-rythme-fiche.html`**

## Le rythme sous le trait, corrigé (Q163)

Relevé par Tom sur capture : « trace pour tenir trop loin du trait ». Mesuré en air d'encre,
c'était **65 px** — le plus grand vide de l'écran, pour le lien le plus serré qui soit.

**La cause : tout était posé sur la BOÎTE SVG** (`base + amp + 40`), dont les 40 px sont le
padding du canevas. Le trait, lui, ne descend qu'à **`base + 0,45·amp`** — exact, pas mesuré.
Et ce n'est pas le trait qui repoussait le mot mais **la marge de touche du geste** : 118 px
(§5) pour un tracé dont l'encre s'arrête 55 px plus haut.

```
                        avant    après
trait  → mot du geste    65,0  →  26,3
disques→ à qui           22,5  →  26,5
à qui  → titre           15,0  →  20,0
titre  → état            30,0  →  30,0   inchangé — « trop proche » veut dire PLUS d'air
état   → commentaires    31,5  →  31,5   inchangé
```

⚠ **J'avais d'abord resserré les deux derniers « pour harmoniser » : `redteam_air` l'a refusé,
quatorze paires, et il avait raison.** Rendus.

**`redteam_superpo` est née de la même exigence** — elle balaie tous les textes de tous les
écrans : **0 recouvrement, 13 écrans × 2 thèmes**. Elle m'a eu deux fois avant d'être juste
(`elementFromPoint` ne rend que le dessus ; la pile contient ce qui est derrière) — les deux
pièges sont écrits dans son entête.

---

# ⚑ LA PASSE PRÉCÉDENTE — 3 septembre 2026

> Point de reprise : **`sauvegardes/lot-passe-finie.html`**
> Captures : `scratchpad/cap/` — 20 images, 10 écrans × 2 thèmes, `#device` à 390 × 844 exactement.

## TOUTES LES BATTERIES SONT VERTES — une seule exception, nommée

```
releve-design  ✅ 0 écart      redteam_ecrans 150/150     redteam_air ✅ 428 paires
redteam         15/15          redteam2        10/10      redteam3     18/18
redteam_demande 19/19          redteam_verbe    6/6       redteam_geste 13/13
redteam_toile   17/17          redteam_champ   32/32      redteam_vide 61/61
redteam_tonsurton 26/26        redteam_filets 0 parasite  redteam_polices 0 absent
releve-S1      ✅ AU VERT      releve-S3      ✅ AU VERT   releve-S4   ✅ AU VERT
releve-S5      ✅ AU VERT      redteam_nuee   ✅ 0 écart
releve-S2      position 0 · style 12          ← la seule, et elle est nommée
```

**Les quatre rouges antérieurs sont levés** — S1 132 → 0, redteam_nuee 56 → 0, S3 64 → 0,
S5 20 → 0. Voir QUESTIONS.md · Q160 : ils encodaient l'entête d'avant le plateau, et deux
d'entre eux codaient l'onde du trait **en dur** pour lire sa couleur au pixel (amplitude 44
quand la vraie est 36). Les deux peintres du canevas déclarent maintenant leur composition ;
les juges la lisent.

**`releve-S2 · style 12`, la seule restante :** les libellés NOTE et COMMENTAIRES sortent à
13 px quand les cinq autres sont à 11,5. C'est la tension entre la **loi 3** (`max(13, taille)`)
et le cadre, qui écrit 11,5 — une valeur que le §6 interdit déjà (« rien en dessous de 12 »).
Les sept devraient être à la même taille ; ils ne le sont pas. **À trancher, pas résolu.**

## Ce que cette passe a livré

**1 · LE PINCEAU** — le trait se choisit à la page + (rangée 0/651, pastilles 78 × 44,
rayon 22) et se reprend dans Peaufiner, haut de liste : rangée 342 × 64 sur une fiche, carte
342 × 118 sur une Nuée, la page + pour un gardé de côté. Les douze tracés de la planche sont
posés sur l'onde du §2.1 (base 560, amplitude 36, ajustement 0,05 px) : on reporte leur
**ligne moyenne**, jamais leur boîte. Q156.

**2 · LA GRAMMAIRE DES CONTOURS VA JUSQU'À PEAUFINER** (Q157) — trait 2, rayon = hauteur ÷ 2,
sur les quatre natures et les deux thèmes. **Le cadre ne se soustrait pas : il a fallu rendre
le pixel trois fois** (padding d'un bloc, ancre d'un nœud absolu, `left`/`bottom` d'un autre).
Vérifié nœud par nœud : **0 déplacé sur 47**.

**3 · LE PARTAGE · L'IMAGE EST L'ÉCRAN** (Q159, Q161, Q162) — l'aperçu passe de 233 × 415 au
milieu à **390 × 844**. Une ligne posée dessus dit où l'on en est ; on la touche, un panneau
plein se pose et défile, l'image reste entière derrière. **À l'ouverture, l'image RECULE** —
90 %, calée par le bas à 740 — et **son mot-marque reparaît** (32/713, confirmé au doigt).
Aucun ✦, aucun flou, aucun encart du Cercle.

**Cinq restaurations** : le mode Noyau, ses six commandes (elles étaient sous le pli d'un
panneau de 148 px pour un contenu descendant à y 1109), la rangée « LE SUJET » qui n'avait
plus que son libellé, le plateau masqué à l'ouverture — et **« Sans texte » qui n'arrivait pas
jusqu'à l'export** (`shLabels` ≠ `shareVis`).

**4 · UN VRAI DÉFAUT D'ÉCRAN, pris pour un rouge de juge** — sur le fil défilé d'une Nuée, le
§13 reposait le mot-marque et le FERMER aux cotes d'avant le plateau : les deux se
retrouvaient **l'un sur l'autre**, le FERMER par-dessus le mot. Corrigé.

## ⚑ LE MOTIF DE LA PASSE : DEUX PROPRIÉTAIRES POUR UNE MÊME PROPRIÉTÉ

**Inscrit dans `CLAUDE.md` §7 sur décision de Tom.** Il est revenu **six fois** :

```
echelle() / etatsDeCarte()      un inline retiré par qui ne l'avait pas écrit
#shMode                          repris dans #shcSujet par l'ancien lot du partage
#shcBarre                        posée à 700 par un lot, à 746 par l'autre
enteteLisible / encreUn          le second repeignait le plateau par-dessus le premier
_ficheTrait / le peintre de l'instant   deux déclarations pour un même canevas
_ficheNuee / le plateau          le §13 reposait ses deux textes
```

**Ce que ça coûte à chaque fois :** trois correctifs inutiles sur `etatsDeCarte`, deux sondes
de test avalées sur le partage, et un vrai défaut pris pour un rouge de juge pendant plusieurs
lots. **Quand un correctif ne tient pas, chercher qui d'autre écrit la même propriété.**

## Neuf contrats réécrits cette passe — tous prouvés contre un vrai défaut

```
releve-S3  « rien ne déborde »       exempte ce qui se DÉCLARE glissant (Q128 §3)
releve-S3  l'entête                  le plateau, et les deux cadres du geste réalignés
releve-S2  l'ordre et les contours   « LE TRAIT » en tête · trait 2, rayon = h ÷ 2
redteam_nuee  les cadres 84-87       +134 sur les quatre cartes · l'entête au plateau
redteam    « rien ne traîne »        l'aperçu est l'image, il ne traîne pas
redteam    « aucun recouvrement »    l'aperçu passe DESSOUS, par décision
releve-S1  l'entête + le corps       le plateau au pixel · le corps d'un seul tenant
releve-S1  la couleur du trait       lit la composition déclarée, ne code plus l'onde
releve-S5  l'entête + la couleur     idem
```

**La règle, inscrite au §7 :** *un contrat réécrit se prouve contre un vrai défaut, sinon il ne
mesure plus rien.* Elle a servi cinq fois en deux jours — une première réécriture de
`releve-S3` **éteignait** le contrôle, et trois sondes ont été avalées avant d'être prises.
Originaux : `sauvegardes/*-avant-pinceau.py`, `-avant-contours.py`, `-avant-partage-plein.py`,
`-avant-plateau.py`.

## Ce qui reste ouvert

- **L'AURA et LE CERCLE ne sont pas refaits** — c'est l'étape suivante, et cette passe n'y a
  pas touché.
- **`releve-S2 · style 12`** — NOTE et COMMENTAIRES à 13 px, les cinq autres libellés à 11,5.
  La loi 3 contre le cadre. À trancher.
- **Q125** — le geste de couleur au doigt dans le Studio. Dessiné, jamais implémenté.
- **Q155 bis** — « LE TRAIT » ou « LE PINCEAU » comme libellé de rangée.
- **Les huit traits à 0,50 €** s'essaient mais ne s'achètent pas : aucun paiement branché.
- **Le corps d'une fiche descend de +16, +12 ou +20 selon l'écran** — trois pas différents là
  où il devrait n'y en avoir qu'un. Le juge tient l'état courant au pixel et publie le
  décalage ; l'incohérence est écrite, pas absoute.
- **Violations du §6** : textes à 10–11,5 px et opacités 0,42–0,70 hors des écrans repris.
