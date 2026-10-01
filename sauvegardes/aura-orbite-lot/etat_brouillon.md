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
