# QUESTIONS — décisions prises sans toi, à relire

> Protocole AUTONOMIE-CLAUDE-CODE.md : quand je rencontre une ambiguïté, j'écris la
> question ici, je prends l'option **la plus conservatrice**, et je continue.

---

## LOT 0 — le juge (`releve-moodboard-H.py`)

### Q0 · Détecteur RESSERRÉ (122 → 1 candidat) — fait
Corrigé au lot suivant : (1) mesure de l'**encre du texte** (Range) au lieu de la boîte
→ un titre pleine largeur avec texte à gauche ne « collisionne » plus un bouton à droite
(faux positif Index/Fil éliminé, confirmé à l'œil : « Index 23 » et « ✕ FERMER » nettement
séparés — **PAS une collision**, réponse au point 3) ; (2) exclusion des **feuilles cachées**
par suffixe d'id (`[id$=Sheet/Screen/View/Poster]` + auraHelp) → les ~15 « ✕ Fermer » empilés
en bas de la Toile disparaissent ; (3) **débordement horizontal seulement** pour l'app (elle
défile → le vertical >844 n'est pas un bug ; le vertical ne compte que sur un cadre FIGÉ =
moodboard). **Résultat : Toile/Index/Fil/fiches/page+ = 0/0.** Reste **1 candidat** :
`page+ phrase « Promi » ∩ « Un Chiche »` — **PROUVÉ transitoire** (état posé mesuré : mot-marque
y=75, tuile y=471, aucun chevauchement ; le flag est un cliché à mi-animation du glissement que
la lib de scroll rejoue après mon snap). **Ce n'est pas un vrai problème.** À finir : mesurer
après stabilisation complète des animations du createSheet.

### Q5 · §3 (fiches) — structure DÉCODÉE, mapping node-à-node à finir
Le cadre #52 (Chiche « lancé/pas encore relevé ») confirme la rangée de disques (Décision Tom)
DANS le moodboard : `r/3` disque « toi » + `r/4` disque « Marion », **prénom seul, aucun mot ni
chiffre** (= §9.6). Structure : `r/0` dalle-band → `r/2` header [`r/2/0` mot-marque nature fs27
Fraunces · `r/2/1` FERMER] → `r/3`+`r/4` disques → `r/5` sous-titre statut → `r/6` « À Marion »
fs21 → `r/7` titre fs38 → `r/8` état fs13 → `r/9` barre Peaufiner [`r/9/0` mot · `r/9/1` actions].
**Correspondances app évidentes** (à câbler dans l'outil, PAS d'approximation) : r/0→#dpTrameCv,
r/2/0→#dpTete .dpt-nat, r/2/1→.closeb, r/3→#dAura .kring-moi, r/3/1→.kring-moi .kr-n, r/4→#dAura
.kring[data-p], r/6→.dpt-qui, r/7→.dpt-titre, r/8→#dptQuand, r/9→barre Peaufiner.
**Non trivial :** les 14 cadres §3 sont des VARIANTES (natures Promi/Chiche/Nuée × états à
tenir/tenu/en cours × titre court/long × « lancé/relevé » du Chiche). Plusieurs états du
moodboard (ex. Chiche « lancé, pas encore relevé ») n'ont PAS d'équivalent d'état dans l'app →
ces nœuds seront déclarés **non mappés**, pas devinés. Le mapping des 14, écran par écran, est
le travail restant — je NE livre PAS un mapping approximatif (« pire que pas de mapping »).

### Q8 · §3 — TRAIT calé sur le path exact, filet retiré, variantes codées
- **Vague calée sur les coordonnées EXACTES du cadre #44** (7 ancres tous les 65px, contrôles
  Bézier 1/3–2/3, décalées par la hauteur de composition) — plus d'estimation à l'œil.
- **Filet parasite retiré** : `#dpTete::before` restait allumé en f-atenir malgré la règle 12183
  (une règle cachée de spécificité ≥2 ids+2 classes le rallumait) → battu par `#device #detailPoster
  #dpTete::before` (3 ids). Vérifié à l'œil : frontière propre, la vague seule.
- **Variantes codées** (Redteam moodboard) : un Chiche LANCÉ (pas de compagnon `p.avec`) → ligne
  en teinte claire de nature, PAS terracotta (rien n'est dû tant que non relevé) ; un GARDÉ DE
  CÔTÉ (brouillon) → TOUT le trait en points.
- **RESTE §3** : l'ORDRE (déplacer #dAura au-dessus de #dpTete + label « trace pour tenir »),
  le soulignement du titre (`dptTitre::after`, absent du moodboard), et la VÉRIF des 14 variantes
  une par une (2 thèmes) + captures + détecteur 0. Batteries : filets 0 ; ecrans oscille 142–144
  (flake « Toile hit », retouche 144 au relancer — pas une régression de fiche).

### Q7 · §3 — le TRAIT construit (composant), affinages restants
Bande = NATURE posée (3 natures, 2 thèmes, CLAUDE.md §3 réécrit). **Le trait est CONSTRUIT**
(`window._ficheTrait`, bloc script neuf, try/catch) : vague sinus 1,5 période, moitié pleine
0→195px + guide en cercles Ø9 tous les 18px, chevron, couleur d'ÉTAT (à tenir orange, tenu
menthe, en cours = teinte claire de nature), hauteur = 344−32×(éléments), plancher 196 ; fiche
TENUE = le vrai `cur.trace`. Rendu vérifié à l'œil sur Promi à tenir — proche de #44.
**Affinages restants (notés, sous le seuil / 3 essais) :**
- **Amplitude/forme** : le sinus du moodboard #44 est plus prononcé (1,5 période nette) ; le
  mien est plus plat (A=20). À caler sur le path exact du SVG #44.
- **Filet parasite** : une ligne horizontale orange subsiste au-dessus de la vague (ancien
  filet de bande/titre) — à masquer.
- **Amorce effilée** (22→1,5) et **flèche** (24px incurvée) du §7 : pas encore posées.
- **§7 vs décision Tom — couleur du trait** : §7 dit « toujours la teinte claire de la nature » ;
  le SVG #44 (à tenir) montre la vague en ORANGE (état), et Tom dit « l'état vit dans la ligne ».
  J'ai suivi le SVG + Tom (trait = état ; en cours = teinte claire de nature). **À confirmer.**
**Reste pour finir §3 :** l'ORDRE (bande → trait → disques → « trace pour tenir » → à qui →
titre → état → Peaufiner) et la déclinaison des 14 variantes + captures 2 thèmes + détecteur 0.

### Q6 · §3 fiches — la fiche du moodboard est une REFONTE, pas un ajustement (juge à l'œil)
Comparaison directe cadre #44 (Promi « à tenir ») ↔ app même état. Écarts STRUCTURELS :
1. **Couleur de bande — CONFLIT à trancher (je ne décide pas).** Moodboard : bande du haut
   = **couleur de NATURE** (Promi = BLEU #3A54FF), l'état se lit aux accents (« À Rachel »
   orange, « À TENIR » orange). App aujourd'hui : bande = **couleur d'ÉTAT** (à tenir = ORANGE),
   par CLAUDE.md §3 (« la zone haute est en couleur d'état pleine »). **Le moodboard fait foi
   → bande = nature.** Mais ça CONTREDIT frontalement CLAUDE.md §3 (le bitonal d'état). C'est
   une décision qui change une règle écrite : **elle te revient.** (Option conservatrice en
   attendant : je ne touche pas la couleur de bande.)
2. **LE TRAIT manquant.** Le moodboard pose LE GESTE comme une **grande vague orange** qui
   traverse le milieu de l'écran (solide 0→195px puis pointillé, §9.2/9.3), avec « trace pour
   tenir » dessous. L'app n'a AUCUN trait de ce genre sur la fiche à tenir — juste un petit
   filet rose sous le titre + les boutons ronds. **C'est le cœur du moodboard, absent de l'app.**
3. **Ordre des blocs.** Moodboard : bande → TRAIT → disques → « trace pour tenir » → À Rachel
   → titre → état. App : bande → à Rachel → titre → état → disques → carte message. Ordre
   différent (disques+trait AU-DESSUS du titre au moodboard).
4. **Carte message** (« NICO, HIER · merci d'y penser ») : présente dans l'app, **absente du
   moodboard #44**. (À confirmer sur les autres cadres §3 — peut-être propre à l'état « tenue ».)
5. **Filet** : app = rose/magenta (--accent dérivé 150°) ; moodboard = **orange** (couleur d'état).
6. **DÉFAUT app clair** : le libellé du 1ᵉʳ disque s'affiche « t » (tronqué) au lieu de « toi ».

**Conclusion honnête :** §3 n'est pas « 14 écrans à ajuster de quelques px » — c'est une
**refonte de l'architecture de la fiche** (trait-vague central, ordre, logique de couleur de
bande), déclinée sur 14 variantes. Faire ça « proprement en un tour » est impossible et
« réécrire un écran » est interdit — il faut patcher par lots, écran-structure par
écran-structure. **Le point 1 (couleur de bande) contredit une règle écrite : j'ai besoin de
ta décision avant de refondre**, sinon je refais le bitonal dans un sens que tu réprouveras.

### Q1 · Le détecteur de collisions a des faux positifs résiduels (Toile, geste de fiche)
**Ambiguïté :** que compte comme « collision » quand l'app superpose légitimement des blocs ?
**Options écartées / retenues :**
- La **Toile** est un Voronoï (dalles qui se chevauchent par construction) + un dock de nav
  en bas + des feuilles cachées encore dans le DOM. Restent 47 « collisions » à y≈842
  (« Promi » ∩ « Index/Aura/Nuée » = mot-marque d'une feuille masquée ∩ libellés du dock).
  **Conservateur retenu :** je clippe déjà à la bande visible 0–844 et j'ignore les nœuds
  `sticky`/`fixed`, mais la Toile reste bruyante. **Je ne la déclare pas « à zéro » ; je la
  signale comme écran à cadrer** (racine plus précise que `.device`).
- **Fiche « à tenir » : « tenir » déborde à bas 907** = le geste « glisse pour tenir » sous le
  pli, atteignable au défilement — faux positif (mon `scrollable()` ne détecte pas le conteneur
  de défilement réel de la fiche). Conservateur : je le laisse **affiché** plutôt que de le
  masquer par une exception trop large qui cacherait un vrai débordement.
- **page + phrase : « Promi »/« FERMER » ∩ « Un Chiche »** = l'en-tête collant au-dessus des
  tuiles quand le glissement n'a pas fini dans l'état scripté. Probable faux positif de timing.
**→ à trancher :** faut-il une racine par écran (au lieu de `.device` pour la Toile) et une
liste blanche explicite (dalles de Toile, geste) ? Je penche pour **oui**, mais c'est un choix
d'outil, pas de produit — je le laisse ouvert.

### Q2 · Collisions qui ressemblent à de VRAIS défauts (à confirmer, pas corrigés)
- **Index & Fil : « ✕ Fermer » ∩ le titre (« Index »/« Fil »)** — recouvre 52×12 px en haut.
  Le bouton Fermer mord peut-être sur le titre. **Non corrigé** (LOT 0 ne dessine pas). À
  vérifier à l'œil au prochain lot.

### Q3 · La carte de correspondance — le gros du travail, DÉMARRÉ, pas fini
**Fait :** l'assertion 102 cadres (échoue si moins), les deux bases (H = 390, **pas
d'homothétie** ; parcours = 352 ×1,108), l'énumération par section, le détecteur
collisions/débordements sur l'app (2 thèmes).
**Reste (déclaré, non deviné) :** le mapping **nœud-à-nœud** du moodboard H vers l'app,
section par section. L'ancien `releve-moodboard.py` mappe la fiche contre l'**ancien** parcours
352 ; le **portage vers H (390)** — §3 (fiches) puis §5 (Peaufiner) — est le chantier restant.
Tant qu'il n'est pas fait, la passe de couverture qui-échoue ne peut pas s'appliquer nœud par
nœud (elle n'aurait aucun nœud mappé à opposer).
**Sections déclarées NON COUVERTES au lot 0** (app pas encore équivalente ou hors périmètre) :
SECTION 0 (0 cadres), 1 (34), 2 (10), 4 (6), 6 (6), 7-8-9 (texte). **Cibles :** SECTION 3
(28 cadres) et SECTION 5 (18 cadres).

### Q4 · La §9 du moodboard confirme la décision « disques »
La §9.6 (« LES NOYAUX ») dit : **« Aucun chiffre, aucun pourcentage, aucun mot de performance,
aucun classement. »** C'est exactement la correction que tu viens de demander (retirer le mot
sous le disque global). Cohérent — aucune ambiguïté, je le note pour trace.
La §9.11 confirme l'**unique collision tolérée** : l'encart du Cercle sur ses réglages floutés
(codée en exception dans le détecteur).

### Q5 · SECTION 3 (fiches) — ce qui est FAIT et vérifié à l'œil
Intégré au moodboard `promi-moodboard-H.html`, **à l'œil** (pas le mapping auto), bloc neuf en
fin de fichier (`lot-S3-fiches` + `lot-S3-trait`), aucune règle existante touchée :
- **LE TRAIT** (`window._ficheTrait`) — la frontière champ/corps. Coordonnées **EXACTES du
  cadre #44** (fill + onde), pas à l'œil : moitié pleine 0→195, guide en cercles Ø9 tous les
  18px, chevron à la jonction, hauteur = 344 − 32×(éléments) plancher 196, **couleur = état**
  (à tenir orange / tenu menthe / en cours = teinte claire de nature). Nuances Redteam
  moodboard respectées : Chiche **lancé** → teinte de la dalle (jamais terracotta) ; **gardé
  de côté** → tout le trait en points ; **tenue** → le vrai `cur.trace` (signature). Vérifié à
  l'œil sur Promi en cours (2 thèmes) : forme conforme au #44, moitié pleine + guide.
- **Filet parasite** `#dpTete::before` supprimé (3 ids) — c'est la vague qui tient ce rôle.
  `redteam_filets` = 0.
- **Soulignement de titre** retiré (absent du #44).
- **Défaut « toi » tronqué** corrigé (kring-moi flex-colonne).
Batteries : `redteam_ecrans` **144/144**, `redteam_filets` **0**. JS OK.

### Q6 · Bande = NATURE — écart STRUCTUREL, pas mécanique (DÉCISION ATTENDUE)
CLAUDE.md §3 : « la zone haute (la bande) est en couleur de NATURE pleine ». Le **moodboard
#44** confirme la structure cible : un **SVG plein-cadre nature de 0 à 346** (r/0, 390×346) +
une **dalle CENTRÉE de 141×118** posée dessus (r/1 @124,88). L'**app** fait autre chose : elle
peint une **dalle plein-cadre OPAQUE** sur `#dpTrameCv` (0-209, couleur du monde, ex. mauve
clair 208,176,255) — cette dalle **couvre** tout fond CSS posé derrière. Mon approche
`#dpTrameCv{background:#3A54FF}` est donc **inopérante en pratique** (elle ne se voit qu'en
thème sombre, par coïncidence de la dalle sombre). **Faire bande=nature correctement exige
soit** (a) teiner la dalle du bandeau à la couleur de nature (comme la bande de Nuée en mauve,
via `_teinteDalle` — « vraies dalles teintées », CLAUDE.md §4), **soit** (b) refondre le
peintre du bandeau pour dessiner un aplat nature + une dalle centrée façon #44. Les deux
touchent le pipeline de peinture des dalles (fragile, §4/§9). **Ce n'est pas mécanique — je ne
tranche pas seul.** Question : (a) teinter la dalle plein-cadre, ou (b) refondre le bandeau au
#44 ? En attendant, la bande garde la dalle du monde (état non régressé).

### Q7 · L'ORDRE (disques au-dessus de à-qui/titre) — bloqué par #dpTete (DÉCISION ATTENDUE)
Le #44 place les **disques à y350**, AU-DESSUS de à-qui/titre/état. L'app fond **l'espace-bande
ET le texte** dans un seul `#dpTete` (le texte est calé en bas d'un bloc haut qui réserve la
bande) ; le flex `order` prime sur le DOM. Réordonner les disques au-dessus du seul texte
exige de **scinder `#dpTete`** (sortir dptQui/dptTitre/dptQuand sous les disques) = restructurer
l'écran, ce que le contrat visuel interdit sans demande. **3 essais** (reorder DOM, flex order,
analyse) → je **note et je passe**. Ordre laissé propre (à-qui/titre → disques → corps →
geste), sans chevauchement. Question : scinder `#dpTete` pour atteindre l'ordre exact, oui/non ?

### Q8 · Le mot « trace pour tenir » — RETIRÉ (lié à Q7)
Le #44 pose « trace pour tenir » sous les disques, au-dessus de à-qui. Posé dans l'app, il
**chevauchait la carte message** (l'app a déjà « glisse pour tenir ta parole → » dans le panneau
du geste — possible doublon). `_ficheOrdre` neutralisé (no-op), CSS retiré. À reprendre AVEC la
décision Q7 (même zone). Question : garde-t-on « glisse pour tenir ta parole → » (app) ou
« trace pour tenir » (#44) ? — c'est un **mot**, donc un point produit : je ne tranche pas.

### Q9 · BANDEAU REFONDU au #44 (décision Tom = option b) — FAIT (Promi + Chiche)
Décision Tom : **aplat plein-cadre NATURE + vraie dalle CENTRÉE non teintée** (la dalle porte le
monde, l'aplat porte la nature — teinter contredirait la règle fondatrice §4). Résout Q6 + Q7 +
Q8 d'un coup (le bandeau, couche à part, sépare l'aplat du texte).
**Mécanique (bloc `lot-S3-trait`, `_ficheTrait` réécrit en peintre CANVAS synchrone sur
dpTrameCv) :** aplat nature (bleu #3A54FF / framboise #FA2258), bord bas = la vague #44 ; **vraie
dalle du moteur** (Toile.dalleTrame, échelle 1) centrée aux cotes #44 (141×118 @124,88, jamais
au-dessus de y=88, jamais à moins de 12px de la vague), **ombre derrière** (la détache quand le
monde de la dalle partage la teinte de la nature — §4 respecté, aucun voile dessus) ; vague +
chevron + guide = couleur d'ÉTAT. **Canvas (pas SVG `<image>`)** car le dataURL décodait en
asynchrone → la dalle « flashait » absente. **Mot-marque + FERMER en BLANC** franc sur l'aplat
(vérifié 2 thèmes). **ORDRE #44 débloqué :** réserve d'espace-bande déplacée de #dpTete vers
#dpMain (padding-top) + flex order → **disques AVANT à-qui/titre**.
**Vérifié à l'œil (captures `scratchpad/s3b/`) :** Promi (à tenir/en cours/tenu) + Chiche
(lancé rose / relevé orange), **2 thèmes**. Batteries : ecrans **144/144**, filets **0**, geste
**13/13** (reconfirmé), JS OK. Collisions fiches **0/0** (2 thèmes).
**RESTE (déclaré) :**
- **NUÉE** : sa fiche a une structure SÉPARÉE (#dpNuee, dpMain hors écran) et NE s'ouvre pas dans
  le harnais de test (flux closeAll → hauteur 0). Je l'ai donc EXCLUE de la refonte et LAISSÉE
  intacte (bande cluster mauve existante, `_ficheDalle` d'origine préservé, pas de régression).
  La refonte #44 y reste à appliquer une fois son ouverture vérifiable. **Point ouvert.**
- **geste** : « trace pour tenir » (#44) vs « glisse pour tenir ta parole → » (app) disent la même
  chose — Tom tranche lequel garder maintenant que le bandeau est fait. Toujours retiré côté #44.
- **corps tenu** : le fond menthe de l'état f-tenue apparaît sous l'aplat (état dans le fond, pas
  seulement dans la ligne). Cohérent thématiquement (parole tenue = menthe) mais c'est une
  question de COULEUR DE CORPS, distincte du bandeau. À trancher si on veut corps=nature strict.
- `releve-design` : ~373 écarts = la refonte + le réordonnancement demandés (bandeau, titre/état/
  FERMER/disques repositionnés). À **figer** (--figer) après validation Tom.

================================================================================
## SECTION 1 — LES FICHES (protocole AUTONOMIE v2 + PROMI-SPECIFICATIONS.md)
================================================================================
Sauvegarde `sauvegardes/avant-S1-fiches.html`.

### S1-A · Couche MATIÈRES & COULEURS — FAITE et vérifiée (Promi + Chiche, 2 thèmes)
Réponses de Tom appliquées, toutes lues dans la spec :
- **Ombre de détachement RETIRÉE** (interdit absolu §6 « aucune ombre portée »).
- **Dalle = palette §1.2** : Promi lavande `#CBAAFF`, Chiche pêche `#FFC0A8` (2e teinte, milieu).
  On teinte la VRAIE dalle du moteur (blend color + luminance, alpha d'origine — §4, aucune
  forme inventée). Elle se détache seule de l'aplat (lavande/bleu, pêche/framboise). C'était
  la cause du « flash sans dalle » : mauvaise palette, pas besoin d'ombre.
- **Corps = nature, jamais l'état (§1.3)** : Promi `#12142A`/`#F4EEE1`, Chiche `#25101A`,
  Nuée `#1A1230`. Le fond menthe/orange (état) SUPPRIMÉ — dont un `background` menthe posé sur
  le canvas dpTrameCv lui-même (rendu transparent en inline).
- **Trait « teinte claire » = §2.1bis** : `#CBAAFF`/`#FFC0A8` (corrigé depuis mes `#8FA0FF`).
- **Mot-marque + FERMER = crème `#F4EEE1`** (§3.1), plus blanc pur.
Batteries : ecrans **144/144**, JS OK. Captures `scratchpad/s3b/`.

### S1-B · Portage en COORDONNÉES ABSOLUES — RESTE (le gros du critère 5 lignes)
La spec donne chaque élément en (x,y,w,h) absolu par écran (§5). L'app est en flux ; pour
atteindre « 0 écart de position > 3px » il faut positionner en absolu. Non fait, déclaré :
- **Trait par FORMULE** (§2.1/§4) `per=1.5, mont=amp·0.34, a=amp·0.62`, avec **base+amp par
  écran** (lus en tête d'inventaire, ex. à tenir base=262 amp=44, tenue base=376 amp=48). Mon
  trait actuel part encore des coordonnées figées du #44 décalées — à remplacer par la formule.
- **Positions exactes** : « trace pour tenir » y=474 (Bricolage 700/17, couleur d'état,
  centré) · à-qui y=510 · titre y=540 (Bricolage 700/38) · état y=605 (Apfel 500/12.5) ·
  Noyau toi bloc 24,350 (Ø78) · Noyau personne bloc 136,360 (Ø58). Aujourd'hui en flux, ~à
  quelques dizaines de px près.
- **Le mot du geste** « trace pour tenir » (décision Tom) remplace « glisse pour tenir ta
  parole → » ET le panneau de geste/le champ « écris un mot » n'apparaît que sur l'écran
  « en cours » (y=647) — à recomposer selon l'inventaire écran par écran.
- **Tailles de dalle par écran** : à tenir 141×118 @124,88 ; **tenue 273×228 @58,88** (grande) ;
  la hauteur dispo = (base−amp)−88−12 (§2.7). Aujourd'hui figée à 141×118.
- **Fiche TENUE = trait COMPLET** (0→390, la signature), pas la vague générique + un tracé crème
  séparé plus bas. À unifier (§2.6 « tenu : 0→390 »).
- **NUÉE** : refonte demandée aussi. Sa fiche `#dpNuee` s'ouvre à hauteur 0 dans le harnais
  (flux closeAll). Cause à trouver (piste _lot7Fiche / verrou nth-child) avant de porter ses
  cotes (§5 « Fiches Nuée »). Laissée intacte pour l'instant (pas de régression).
- **Gardé de côté / États (commentaires)** : écrans d'inventaire non encore portés.
`releve-design` NON figé (consigne Tom : figer seulement quand toutes les sections sont finies).

### S1-B · PORTÉ — les cinq lignes du critère sont à ZÉRO
Outil neuf : **`releve-S1-fiches.py`** (le juge de la section 1). Il compare l'app aux cotes
absolues de l'inventaire §5, écran par écran, **deux thèmes**, et sort les cinq lignes.
Résultat : **0 / 0 / 0 / 0**, batteries au vert (`ecrans` 144/144 · `redteam` 15/15 ·
`redteam2` 10/10 · `redteam3` 18/18 · `demande` 19/19 · `geste` 13/13 · `verbe` 6/6 ·
`filets` 0 · `toile` **15/16 — le flake connu, vérifié IDENTIQUE sur la sauvegarde d'avant
le lot : ce n'est pas une régression**).

**Ce qui a été posé** (bloc neuf `lot-S1B-cotes` + `lot-S1B-geo` en fin de fichier ; aucune
règle existante touchée) :
- **La dalle du bandeau N'EST PLUS TEINTÉE** (correction demandée). Le lot précédent la
  peignait en `#CBAAFF`/`#FFC0A8` selon la nature : faute frontale contre la règle fondatrice
  (§4 : la dalle porte le MONDE) et contre le moodboard §8. C'est désormais la vraie dalle du
  moteur, telle quelle, opacité 1.
- **Le trait par la FORMULE** (§2.1/§4) : un seul sinus `per=1.5, mont=amp·0.34, a=amp·0.62`,
  Bézier cubique par quart de période, tangentes exactes. Plus une seule coordonnée figée.
  `base`/`amp` **par écran**, relevés cadre par cadre sur le moodboard ET dans l'inventaire :
  à tenir/en cours/Chiche lancé/relevé **262 · 44** · tenue **376 · 48** · Chiche tenu à deux
  **372 · 44** · Nuée avec des Promi **232 · 36** · Nuée vide **282 · 44** · avec commentaires
  **262 · 44** · sans commentaire **338 · 46**. Boîte = base + amp + 40 : les quatre valeurs
  346/464/456/308/366/424 se retrouvent au pixel.
- **Les quatre modes du trait** (§2.6) : `moitié` (0→195 + chevron + cercles Ø9 tous les 18) ·
  `complet` (0→390, **la fiche tenue**) · `duo` (0→191 et 199→390, le Chiche tenu à deux) ·
  `points` (amorce effilée 22→1,5 + 18 cercles, le gardé de côté). Vérifiés contre les SVG
  des cadres 44 à 71 : mêmes bornes, mêmes cercles, même chevron.
- **Les cotes absolues** : noyau « toi » = boîte + 4 · noyau de personne + 10 · premier bloc
  texte 124 px sous les noyaux · « trace pour tenir » puis à-qui + 36 · titre + 30 · état =
  bas du titre + 26,3. Ces quatre règles reproduisent les 14 inventaires **exactement**
  (350/474/510/540/605, 468/592/622/687, 460/584/614/718, 312/436/466/531, 370/494/524/628,
  350/386/416/481…). Le champ « écris un mot » à état + 42.
- **Les Noyaux (§2.9)** : Ø78 / Ø58, blocs 82 et 70, écarts 30 et 14 (→ x = 24, 136, 220),
  libellés Bricolage 700/14 et 600/13.5 à 11 px, aucun chiffre ni mot d'état.
- **Le VISAGE (§2.10)**, absent de l'app, posé au centre de chaque Noyau : 48 et 36, fond =
  couleur de nature, tête et épaules **calculées** par la formule du document.
- **La barre Peaufiner (§3.2)** : 84 px à y = 760, fond de NATURE, Bricolage 700/21 crème,
  cercle Partager 46 contour 3, icône 22.
- **L'entête (§3.1)** : bloc 24/38/34, Fraunces 600/27 crème, ✕ 15 px + FERMER Apfel 500/12.5
  interlettre .20em.
- **LA NUÉE, refondue** : elle avait sa structure à part et restait hors du portage. Elle
  prend la même grammaire — champ mauve, onde complète, **les vraies dalles de ses Promi aux
  trois emplacements de l'inventaire** (chacune dans SON monde, non teintée), Noyaux
  « toi » + celui de la Nuée (bâtis avec `karmaRing`/`drawKRing`, les composants de l'app),
  phrase, et cartes 342 × 74 rayon 20 avec la dalle du Promi à gauche et l'eyebrow en couleur
  d'état.

---

#### Q1 · LA DALLE EST PEU LISIBLE SUR L'APLAT — constaté, **pas compensé** (ta consigne)
Sur un Promi dont le monde donne une dalle bleu foncé, la dalle **disparaît** dans l'aplat
bleu du champ ; idem pêche sur framboise, mauve sur mauve. C'est la conséquence directe et
attendue de la règle fondatrice : la dalle porte le monde, l'aplat porte la nature, et rien
ne les sépare (aucune ombre — §6 l'interdit ; aucun voile — §4 l'interdit). **Je n'ai rien
compensé.** Sur les mondes contrastés (orange, lavande) elle éclate ; sur les mondes proches
de la nature elle s'efface. **Question :** est-ce voulu (la matière se fond dans sa nature),
ou faut-il un moyen de détachement que le document n'a pas prévu ?

#### Q2 · LE PANNEAU DU GESTE n'existe dans AUCUN des 14 inventaires de fiche
Le moodboard fait du **TRAIT** la surface où l'on trace : « trace pour tenir » est un libellé
posé à y = 474, et rien d'autre n'apparaît. L'app, elle, a un panneau de 118 px (deux points,
un trait — CLAUDE.md §5). Il n'a **aucune place** dans la composition : entre la ligne d'état
(bas ≈ 620) et la barre (760) il ne reste pas de quoi le poser sans violer la consigne des
30 px de bas d'écran.
**Option conservatrice retenue :** je ne retire pas la fonction. `#tenirZone` est posé
**entier** sur la bande du champ, calé au bas de la boîte du trait — là où l'onde passe — et
reçoit le doigt exactement comme avant. En revanche **son canevas ne peint plus** : ses deux
points de guidage tombaient au milieu du champ, par-dessus la dalle, et le moodboard n'en
montre aucun. Le guide, c'est l'onde. Le retour du geste passe par la teinte menthe de la
zone (`.atteint`).
**Question :** confirmes-tu que l'on trace **sur l'onde** (et que le panneau à deux points
disparaît de la fiche), ou faut-il garder le panneau visible — auquel cas il faut me dire
**où**, car l'inventaire ne lui laisse pas de place.

#### Q3 · Trois blocs de l'app absents des inventaires — retirés de la fiche, rien n'est perdu
- **Les boutons ronds commenter / joindre** (`#dpBarre`) : absents des 14 écrans. Commenter
  passe par le champ (§3.7), joindre par Peaufiner, partager par la barre (§3.2).
- **Les pastilles note / pièce jointe** (`#dpPast`) : absentes. L'information est dans Peaufiner.
- **La zone de message sur une fiche « à tenir »** : l'inventaire ne la pose que sur « en
  cours » (le champ à 647), « avec commentaires » (la carte à 566) et « sans commentaire »
  (l'invitation à 654). Sur « à tenir », le corps est nu — c'est ce que j'ai fait.
**Question :** d'accord pour que la fiche « à tenir » ne porte plus de zone de commentaire ?

#### Q4 · §2.1 bis CONTRE le moodboard clair — j'ai suivi le DOCUMENT
Les cadres **clairs** du moodboard (47, 53, 59, 61) peignent le **trait** dans la couleur
PLEINE de la nature, posée sur un champ de la même couleur pleine : le trait y est invisible.
La §2.1 bis interdit explicitement ce cas (« il ne porte jamais la couleur pleine de la
nature quand il est posé sur le champ : ce serait du ton sur ton ») et dit que la teinte
claire « vaut dans les deux thèmes » ; le code de référence §4 fait pareil (`c = CLAIR[nat]`).
CLAUDE.md interdit aussi le ton sur ton. **J'ai suivi le document et le code** : le TRAIT
garde la teinte claire dans les deux thèmes ; **les LIBELLÉS** (à-qui, état, mot de trace),
eux, sont posés sur le corps et prennent bien la couleur pleine en thème clair, comme
l'inventaire clair le donne. Si c'est le moodboard qui a raison, un mot suffit — c'est une
ligne à changer.

#### Q5 · La Nuée — deux points d'inventaire que je n'ai pas tranchés seuls
- **« Nuée · vide » : dalle ou pas ? — TRANCHÉ, plus une question.** Une Nuée est un
  contenant : sa matière vient des promesses qu'on y plante, exactement comme un gardé de côté
  ne pose rien sur la Toile tant que rien n'a été promis. Le champ reste plein, en mauve, sans
  dalle. Le cadre 60 se contredit (son dessin en montre une, sa légende dit l'inverse) :
  **c'est une erreur du moodboard**, notée comme telle.
- **« + Planter un Promi »** n'est dans aucun des deux écrans de Nuée. C'est pourtant la
  fonction même d'une Nuée : je ne l'ai pas retiré, je l'ai posé **sous** les cartes (il
  défile). La ligne « à Maman » des cartes, elle, est masquée : l'inventaire ne pose que
  l'état et le titre, et l'information reste dans la fiche du Promi.
**Question :** garde-t-on le bouton « + Planter un Promi » sur la fiche de Nuée, et où ?

#### Q6 · Ce que l'app ÉCRIT et que je n'ai pas touché (ce sont des mots, donc ton domaine)
Aucun de ces écarts n'est de la géométrie ; je ne réécris pas un libellé sans toi.
- **le mot-marque d'un Chiche** : l'app écrivait toujours « Promi » (table `NAT`, l.5409).
  Je l'ai corrigé — « Chiche », « Nuée », « Promi » sont les trois mots du vocabulaire
  (CLAUDE.md §2) et l'inventaire les donne explicitement. **Signalé, pas inventé.**
- **« à Léa » contre « À Rachel »** : l'inventaire met une capitale, l'app une minuscule.
  Non touché.
- **la ligne d'état** : l'app écrit « À TENIR », l'inventaire « À TENIR · DANS 2 JOURS » ;
  « TENUE » contre « TENU À DEUX » sur un Chiche tenu à deux. Non touché.
- **l'eyebrow des cartes de Nuée** : l'app y met le mot du temps (« MERCREDI »), l'inventaire
  l'état (« À TENIR »). Non touché — j'ai seulement mis la couleur d'état.
- **le mot du Chiche lancé** : l'inventaire dit « Marion complètera si elle relève ». J'ai
  substitué le prénom réel ; la tournure est celle du moodboard.

#### Q7 · Les anneaux des Noyaux — deux règles qui se contredisent, j'ai gardé celle de l'app
La §2.9 dit : « Piste de l'anneau : teinte de la nature. Arc : menthe. » L'app peint les
**proportions tenu / en cours / à tenir**, et CLAUDE.md défend explicitement ce choix
(« l'anneau Aura reste, sa couleur DIT quelque chose »). **Option conservatrice : je n'ai pas
touché à la peinture des anneaux**, seulement à leurs cotes (78 / 58) et à leurs libellés.
**Question :** l'anneau garde-t-il ses proportions, ou passe-t-il à piste-nature + arc-menthe ?

#### Q8 · Trois écrans de l'inventaire n'ont PAS d'équivalent dans l'app — déclarés non portés
- **« Gardé de côté » (Promi, Chiche, Nuée)** : dans l'app, un brouillon **rouvre la page +**,
  il n'ouvre pas de fiche. Le moteur est en place (mode `points`, aplat transparent, mots
  « trace pour planter » / « trace pour lancer », cotes 350/386/416/481) et s'allumera dès
  qu'une fiche de brouillon existera. **Rien n'a été deviné, rien n'a été forcé.**
- **« Promi · titre long »** n'est pas un état : c'est le même écran avec deux lignes de
  titre. La règle « état = bas du titre + 26,3 » le produit toute seule (540 → 640 mesuré).
- **« Avec / sans commentaire »** : portés dans le moteur (base 262 avec carte, 338 sans),
  mais ils dépendent du contenu réel d'un Promi tenu — non isolés dans le juge.

### S1-B bis · LE JUGE VALIDAIT DES ÉCRANS CASSÉS — repris à l'œil, cadre par cadre

Tu avais raison et je le note noir sur blanc : **mes cinq lignes à zéro ne prouvaient rien.**
`releve-S1-fiches.py` mesurait les BOÎTES que je venais de poser — jamais ce qui est peint.
Un anneau à 80 % de sa boîte, un prénom collé à droite, un chevron vert sur vert : tout
passait. Un contrôle qui valide un écran cassé est pire qu'aucun contrôle.

**Ce que j'ai changé de méthode.** Outil neuf `scratchpad/duo.py` : il colle le cadre du
moodboard et la capture de l'app **côte à côte**, avec une règle de cotes (88, 232, 262, 346,
474, 510, 540, 605, 760, 844) tracée sur les deux. Les 102 cadres sont extraits en PNG par
`scratchpad/cadres_mb.py`. J'ai regardé les **16 duos** un par un.

**Ce que l'œil a trouvé — et que la mesure ne voyait pas :**
1. **Le prénom décalé.** `.kr-n` portait un `align-self:end` hérité de la grille de l'Aura :
   le disque et son mot ne partageaient plus la même origine. Le mot était 15 px à droite de
   son disque, sur les 8 écrans. **Corrigé.**
2. **L'anneau ne remplissait que 80 % de sa boîte.** `drawKRing` trace à `KR_R = .33` de la
   largeur du canevas, épaisseur `KR_LW = .14` → diamètre peint 0,80 × boîte : **63 px là où
   le §2.9 demande 78**. Le juge mesurait 78 (la boîte) et validait. **Corrigé** en passant à
   `drawKRing`, *le temps de l'appel seulement*, la géométrie du §2.9 (78/8 et 58/6) puis en
   rendant les constantes globales intactes — l'Aura et `_sigBloc` n'y voient rien.
3. **Le chevron « → » du champ (§3.7) était absent**, remplacé par l'icône de bulle de l'app ;
   une fois posé il héritait du vert sombre du corps et restait illisible. **Corrigé** (icône
   retirée, chevron posé, couleur forcée sur la ligne).
4. **La Nuée écrivait « Fermer » en bas de casse, avec l'ombre de l'ancienne DA** — élément
   jamais converti. **Corrigé.**
5. **Les cartes du fil de Nuée n'avaient ni bloc de champ ni trait.** Le §5 les veut « en
   réduction de leur carte d'Index : sa dalle, son trait, sa couleur d'état ». **Posés** : le
   bloc de champ mauve 103 × 74 et le **trait vertical** (per 1, points r 3,2 tous les 11 px,
   plein sur la moitié tracée puis en points).
6. **« à qui » était peint à 70 % d'opacité** sur les fiches tenues — sous le plancher du §6.
   C'est le NOUVEAU contrôle qui l'a débusqué, pas moi. **Corrigé.**

**Le juge a gagné un cinquième contrôle : LA PRÉSENCE PEINTE.** Un élément à la bonne
coordonnée mais invisible fait désormais échouer. Pour un texte : il a du texte et son encre
n'est pas sous 72 %. Pour un canevas : combien de pixels opaques, et **sur quelle étendue le
dessin porte réellement** (c'est ce qui manquait). Pour la dalle et le trait, qui vivent dans
les pixels du champ et dont le DOM ne sait rien : on lit le rectangle de la dalle (§2.7) et
trois points de l'onde, et on vérifie que ce n'est pas seulement l'aplat de nature.

**Sur la « dalle absente » : c'était une capture périmée, pas un bug.** Je l'ai instrumenté
plutôt que deviné — journal des appels au contexte 2D (`clearRect`/`drawImage`), valeur de
retour de `dalleTrame`, puis lecture des pixels **dans la capture elle-même** : la dalle est
peinte et visible sur les 6 écrans Promi/Chiche, dans les deux thèmes. Ce qui reste est le
**contraste** (Q1), non compensé.

#### COMBIEN D'ÉCRANS SE SUPERPOSENT VRAIMENT : **8 sur 8**
(6 sur 8 à la livraison précédente ; les deux écrans de Nuée ont été finis.)
- ✅ **Promi à tenir · Promi en cours · Promi tenue · Chiche lancé · Chiche relevé · Chiche
  tenu à deux** — structure, cotes, trait, dalle, Noyaux, phrase, barre : superposables aux
  cadres 44 à 57, dans les deux thèmes.
- ✅ **Nuée avec des Promi** — champ, trois vraies dalles du moteur, Noyaux, phrase, cartes.
  **La carte porte enfin le Promi en réduction** : ce n'est plus un rectangle de champ plus un
  trait posé à côté, c'est UN SEUL SVG de 103 × 74 où l'onde borne le champ mauve et porte la
  ligne d'état, exactement comme le cadre 58. **Les valeurs ne sont pas à l'œil** : relevées
  sur le path du cadre 58 puis retrouvées par la formule du §2.1 — `base = 86`, `per = 1`
  (§3.9), `amp = 8,6` (les « 13 × échelle » du §3.9 pour une carte réduite à 74 de haut),
  plein 0 → 37 (la moitié exacte, §2.6) puis points `r = 2,6` tous les 10 px ; complet 0 → 74
  sur une parole tenue. **L'eyebrow porte l'ÉTAT** (§5) et non plus le mot du temps ; les mots
  sont ceux de l'app (`STLAB`), rien d'inventé. Le trait de la carte garde la teinte claire
  dans les deux thèmes (§2.1 bis) — en couleur pleine il disparaissait sur le champ en clair.
- ✅ **Nuée vide** — **tranché : une Nuée vide n'a pas de dalle.** Une Nuée est un contenant ;
  sa matière vient des promesses qu'on y plante. Le champ reste plein, en mauve, borné par
  l'onde. Aucune forme inventée, aucun polygone.
  **ERREUR DU MOODBOARD, pas une question ouverte :** le cadre 60 se contredit lui-même — son
  dessin montre une dalle de 165 × 138, sa légende dit « aucun Promi, donc aucune dalle : la
  zone haute est nue ». C'est le dessin qui a tort. La technique le confirme :
  `Toile.dalleTrame` n'accepte que l'id d'un Promi existant (testé : `'projet'`,
  `'nuee:projet'`, `9001` → tous faux). Le bouton « + Planter un Promi » est un **ajout VALIDÉ
  par Tom**, hors inventaire mais fonction même d'une Nuée (Q5) — il reste, posé sous les
  cartes.

Deux divergences ASSUMÉES et documentées valent pour les huit écrans : la couleur des anneaux
(**Q7**) et le trait en teinte claire en thème clair (**Q4**). Tu les tranches maintenant que
les huit se superposent.

#### Q9 · `releve-design.py` : **551 écarts** — c'est le portage, pas une régression
Le relevé compare à une référence figée **avant** le portage, et tout ce qui bouge ici a été
demandé : le bandeau, les Noyaux, la phrase, la barre Peaufiner, le corps. **0 couleur
fautive.** **Non figé** (ta consigne : figer quand toutes les sections seront finies).

================================================================================
## SECTION 2 — PEAUFINER : COMMENCÉE, **ARRÊTÉE ET REVERTÉE**. Rien n'est livré.
================================================================================
Sauvegarde `sauvegardes/avant-S2-peaufiner.html`. Tentative conservée telle quelle dans
`scratchpad/s2-tentative-peaufiner.html` — elle n'est PAS dans `app.html`.

**Pourquoi l'arrêt.** Ma tentative a fait passer `redteam_ecrans` de **144/144 à 142/144**,
puis à **141/144** après ma correction : « Fiche : rien ne déborde », dans les deux thèmes.
Ce n'est pas le flake connu (celui-ci porte sur « Toile hit ») — c'est une vraie régression,
causée par la marge latérale que je posais sur `#dpPromiBody`. Le protocole ne laisse pas le
choix : **une batterie verte qui rougit = arrêt immédiat.** J'ai restauré la sauvegarde ;
`redteam_ecrans` est revenu à **144/144** et la section 1 est intacte (0/0/0/0/0).

**L'état des lieux, lu et vérifié — c'est ce qui reste utile pour la reprise.**
- Les 9 écrans Peaufiner du moodboard sont extraits en PNG (`scratchpad/mb/peauf_*.png`,
  cadres 78 à 95), prêts pour `duo.py`.
- **L'app est encore la liste « logiciel »** : titres verts, pastilles nues, fond crème même
  en thème sombre, aucun réglage en carte, pas d'entête, pas de bloc du Cercle. L'écart avec
  l'inventaire est de la même ampleur que celui des fiches avant S1-B — c'est une refonte,
  pas un ajustement.
- **Les règles du §5 sont relevées et sûres**, elles n'auront pas à être re-déduites :
  · réglage 342 × 64, rayon 22, contour 3, padding latéral 22, écart **16 px** entre deux ;
  · variante avec ligne de visibilité **92**, zone de texte **104 à 118** ;
  · libellé Apfel 500/11,5 interlettre .18em en teinte claire de nature, valeur Bricolage 700/18 ;
  · **l'encart du Cercle est centré sur le bloc des quatre réglages** : `y = premier + 107`
    (vérifié sur les quatre écrans qui le portent : 260→368, 126→234, 130→238, 374→482) ;
  · titre et sous-titre de l'encart dans **la teinte de la dalle** (§3.8) — 3ᵉ teinte du §1.2 :
    `#AE86F2` Promi, `#F2977A` Chiche, `#C2A4F7` Nuée.
- **Ce qui a fait déborder** : `#dpPromiBody` avec `padding:0 24px` sans `box-sizing:border-box`.
  Mon correctif `border-box + width:390` a empiré (141/144) — la cause est ailleurs, il faut
  l'instrumenter, pas la deviner. **C'est le premier travail de la reprise.**

#### Q10 · Réglages de la page + contre réglages de la fiche — À VÉRIFIER, PAS À HARMONISER
Ta consigne : mêmes libellés, mêmes options, même ordre ; seule différence assumée, pas
d'icône Partager sur la page + (§3.2). **Je n'ai pas encore fait la comparaison** — elle vient
juste après la refonte. Toute divergence trouvée ira ici, sans que je l'harmonise moi-même.

#### Q11 · Deux réglages de l'app / du moodboard qui ne se correspondent pas
Relevé en lisant l'inventaire, avant l'arrêt :
- **« STATUT » (Tenue / En cours / À tenir)** existe dans l'app, **absent des 9 écrans** de
  l'inventaire Peaufiner. Retirer un moyen de changer l'état est un point de produit : je ne
  touche pas.
- **« LA MÉMOIRE » (« réveille tes "en l'air" »)** est le 4ᵉ réglage du bloc du Cercle dans
  l'inventaire, sur les quatre écrans qui le portent. **Il n'existe pas dans l'app.** Le poser
  serait créer une fonction — je ne le fais pas.
- **L'ordre diverge** : l'inventaire met « AVANT » (l'échéance) en 2ᵉ position, l'app la met en
  7ᵉ. L'ordre n'est pas un mot ; je l'aurais aligné sur l'inventaire — noté pour la reprise.

================================================================================
## SECTION 2 — PEAUFINER : LIVRÉE. 7 écrans sur 9 se superposent.
================================================================================
Sauvegarde `sauvegardes/avant-S2-peaufiner-v2.html`. Juge neuf : `releve-S2-peaufiner.py`.
Test de fonctions : `scratchpad/test_s2_fonctions.py` (25/25). Captures : `scratchpad/s2/`,
duos côte à côte : `scratchpad/duo_peauf_*.png`.

#### Q12 · LA RÉGRESSION D'AVANT — la cause était `#tenirCv`, pas la marge. INSTRUMENTÉE.
Je n'ai pas deviné : j'ai rejoué la batterie sur la tentative conservée
(`scratchpad/instr_batt.py`, une copie de `redteam_ecrans` qui imprime QUI déborde). Verdict :

    #tenirCv   x=27   dépasse=27   w=390   dans #tenirZone < .s2-reg < #dpPromiBody

**Le geste, pas la marge.** La section 1 cloue `#tenirZone` en `position:absolute · left:0 ·
width:390` (l. 14095) et `#tenirCv` en `width:390px!important · max-width:none`. Dès qu'un
conteneur POSITIONNÉ de Peaufiner devenait son bloc englobant, le canevas de 390 px repartait
de x = 27 et sortait de 27 px — un élément par thème, d'où 144 → 142. Le « correctif »
border-box en ajoutait un troisième : il resserrait la boîte sans toucher au canevas.
**La parade n'est pas un border-box : c'est de ne jamais faire entrer le geste dans la page
de Peaufiner.** Il reste sur la fiche, où la section 1 l'a posé ; aucun conteneur de mon bloc
n'est son ancêtre. `redteam_ecrans` est à **144/144**.

#### Q13 · LES NEUF CADRES SONT QUATRE PAGES QUI DÉFILENT — interprétation, arithmétique à l'appui
C'est le seul vrai choix de lecture de la section, et il est vérifiable. Chaque cote d'un
cadre « bas / suite » se déduit du cadre précédent par l'écart de 16 px du §3.3, **sans une
seule exception** : Promi 46 → 180 → 260 (118+16 puis 64+16) · Chiche 46 → 126 · Nuée 46 →
124. Les « pages » du moodboard sont donc des pages de DESSIN, pas des écrans. L'app rend une
liste continue à partir de 110 ; les cadres se retrouvent en amenant leur premier bloc à sa
cote (`scratchpad/cap_s2b.py` le fait, cadre par cadre). **Si tu voulais de vraies pages
paginées, c'est un point de produit et je ne l'ai pas tranché.**
Le seul écart qui n'est pas 16 est celui de l'inventaire APRÈS le bloc du Cercle : **104 px**
(Promi 564 → 668, Chiche 430 → 534). Il est reproduit tel quel.

#### Q14 · L'encart du Cercle est à **108**, pas 107
La note de reprise disait « y = premier + 107 » (le centrage théorique : bloc 304, encart 90,
(304−90)/2 = 107). Les quatre écrans qui le portent donnent tous **108** : 260→368, 126→234,
130→238, 374→482. J'ai suivi le dessin, pas le calcul.

#### Q15 · STATUT — supprimé, comme tu l'as tranché
Le sélecteur à trois positions n'apparaît plus dans Peaufiner. **Il reste dans le DOM, masqué**
(`#segStatus`, `#labStatut`) : le retirer casserait des chemins de l'app qui l'interrogent.
L'état se change par le trait, sur la fiche. Rien d'autre n'a bougé.

#### Q16 · LA MÉMOIRE — créée, comme tu l'as tranché
4ᵉ réglage du bloc du Cercle sur les quatre écrans qui le portent, avec les mots de
l'inventaire : « LA MÉMOIRE · réveille tes "en l'air" ». **C'est un affichage, pas une
fonction** : comme ses trois voisins, il est flouté à 2,4 px et inerte (`pointer-events:none`).
Le jour où Le Cercle s'ouvre, c'est là qu'elle se branchera.

#### Q17 · L'ordre — aligné sur l'inventaire
À QUI · AVANT · DANS UNE NUÉE · NOTE · PIÈCES JOINTES · COMMENTAIRES · RELANCER X · [Cercle]
· SUPPRIMER. L'échéance est bien en 2ᵉ. Un Chiche intercale AVEC en 2ᵉ et n'a pas de Nuée ;
une Nuée a DESCRIPTION · MEMBRES · PIÈCES JOINTES · COMMENTAIRES · bouton · DISSOUDRE, et
**pas de bloc du Cercle** — ses deux cadres n'en portent pas.

#### Q18 · UN MOT CHANGÉ : « écrire un commentaire… » → « écris un mot… »
Le champ des commentaires portait le mot de l'app ; l'inventaire écrit **« écris un mot… »**
sur les trois natures. J'ai suivi la référence — le mot vient du moodboard, pas de moi — mais
c'est un mot, donc je te le signale. Un seul autre mot est calculé par moi, avec les mots de
l'inventaire : la ligne de visibilité (voir Q19).

#### Q19 · « VISIBLE PAR X » VISE LA PERSONNE, PAS LA NUÉE
Le cadre 78 montre un Promi **dans « le potager »** dont la note est « visible par Rachel ».
L'app mettait la Nuée d'abord et écrivait « visible par les membres de Famille ». J'ai suivi
le moodboard et le §6 (« ceux qu'elle engage ») : **personne d'abord, Nuée seulement à défaut.**
Si c'est l'inverse que tu veux, c'est une ligne à changer.

#### Q20 · PIÈCES JOINTES quand il n'y en a aucune
L'inventaire ne montre jamais le cas vide. J'affiche le compte (« 0 fichier ») plutôt que
d'inventer un mot. Option conservatrice ; la variante pointillée du §3.3 attend ton mot.

#### Q21 · LE DÉPLIEMENT D'UN RÉGLAGE — un comportement ajouté, pour ne rien retirer
Un réglage de l'inventaire montre une VALEUR (« Rachel », « dimanche »). Les contrôles de
l'app qui la produisent (pastilles d'échéance, pastilles de Nuée, liste de fichiers, membres)
ne tiennent pas dans 64 px. **Je n'ai supprimé aucun contrôle** : chacun est DÉPLACÉ dans son
réglage et se déplie au doigt. Le rendu au repos est celui de l'inventaire ; le dépliement
n'y figure pas. C'est le seul comportement que j'ai ajouté, et il n'ajoute aucune fonction.

#### Q22 · ✕ FERMER sur la page de Peaufiner ferme LA FICHE
L'inventaire montre « ✕ FERMER » en tête des pages de Peaufiner sans dire ce qu'il ferme.
J'ai gardé le sens qu'il a partout ailleurs dans l'app : il ferme la fiche. Pour refermer la
seule page de Peaufiner, il y a le **▴** de la barre — l'affordance du moodboard lui-même.

#### Q23 · RÉGLAGES GÉNÉRAUX — DA portée, contenu NON réduit (divergence assumée)
L'écran de l'app porte douze réglages ; l'inventaire n'en dessine que trois plus le bloc du
Cercle. **Réduire l'app à trois lignes serait retirer des fonctions : je ne l'ai pas fait.**
Ce qui est porté : l'entête à 24/40 (Bricolage 700/38, mesurée), la grammaire du réglage
(342 × 64, rayon 22, contour 3, libellé en capitales dans la teinte, valeur Bricolage 700/18),
le corps de nature (#12142A / crème), le bloc du Cercle complet — et **le dégradé animé du
Cercle est éteint** (§6 : aucun dégradé ; il était peint par `.enc-fx` et un `::after`).
Trois points restent ouverts, tous des points de produit :
- **ASSISTANCE DU TRAIT n'existe pas dans l'app.** Le §6 la décrit (« trois niveaux
  réglables ») mais la brancher, c'est toucher au moteur du geste. **Non créée.**
- **THÈME : l'app a « Sombre / Clair », l'inventaire dit « automatique ».** Le troisième
  choix n'existe pas. **Non créé.**
- L'app pose en tête un bloc de profil (photo, prénom) que l'inventaire ne montre pas.
  Il reste, à la grammaire du réglage.
**Cet écran ne se superpose donc pas** — il est de la bonne famille, pas au même contenu.

**TRANCHÉ (Tom) : on n'y touche plus.** La DA portée suffit. Voici la liste exacte, pour
mémoire — DOUZE réglages relevés dans l'app (plus le profil et l'encart), TROIS dans
l'inventaire :

| l'app, dans l'ordre | l'inventaire (§5 « Réglages généraux ») |
|---|---|
| *Toi* — profil (photo + prénom) | — |
| ✦ Le Cercle (encart) | l'encart, au centre du bloc de quatre réglages |
| The Studio · visuels & humeurs | — |
| Revoir l'intro & le tuto · rejouer | — |
| Réinitialiser (test) · toile vide + 1 Nuée | — |
| *Partager* — Inviter sur Promi · 3 Nuées offertes | — |
| *App* — Langue · Français | — |
| Notifications · (bascule) | **NOTIFICATIONS · activées** |
| *Données* — Sauvegarde locale · enregistré hh:mm | — |
| Réinitialiser mes données · effacer | — |
| *Légal* — Confidentialité · privé & partagé | — |
| Conditions d'utilisation · lire | — |
| Supprimer mon compte · définitif | — |
| — | **ASSISTANCE DU TRAIT · moyenne** (n'existe pas dans l'app) |
| — | **THÈME · automatique** (l'app a « Sombre / Clair », pas d'automatique) |

Seul **NOTIFICATIONS** est commun aux deux. Les deux autres réglages de l'inventaire sont
des fonctions à créer ; les onze autres de l'app sont des fonctions à retirer. **Ni l'un ni
l'autre n'est un écart de dessin.**

#### Q24 · FICHE GARDÉE DE CÔTÉ — non portée, et deux inventaires se contredisent
1. **Dans l'app, un brouillon rouvre la page +** — vérifié en capture, il n'ouvre pas de
   fiche. Faire qu'il ouvre une fiche est un changement de navigation, donc un point de
   produit. **Non fait.** (C'était déjà le constat de S1/Q8.)
2. **Le moodboard donne DEUX écrans différents pour la même chose.** Cadres 62/63 (« Gardé de
   côté · Promi ») : trait en points, « trace pour planter », « Gardé de côté », titre 38,
   « GARDÉ DE CÔTÉ · 2 AVRIL ». Cadres 92/93 (« Fiche gardée de côté ») : pas de mot de
   trace, titre 26 à 336, « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS », bouton **Planter**, réglage
   AVANT pointillé « pas encore », bouton **Reprendre l'écriture**. **Choisir entre les deux
   est un point de design : je ne tranche pas.** La section 1 avait déjà porté le moteur de
   62/63 ; il attend.
3. **TRANCHÉ (Tom) : on la laisse.** Ce n'est pas un écart de dessin, c'est un comportement
   à décider — et la contradiction du moodboard (**cadres 62/63 contre cadres 92/93**) reste
   ouverte tant que tu ne l'as pas tranchée. **7 sur 9 est la bonne réponse pour la section 2 ;
   on ne cherche pas le 9.**

#### Q10 · PAGE + CONTRE FICHE — la comparaison, faite. **Je n'ai rien harmonisé.**
- **La page + n'a AUCUN réglage aujourd'hui.** Elle porte la phrase, les pastilles et
  « garder de côté » ; il n'y a ni page de Peaufiner ni barre à ouvrir. La fiche en a douze.
  **La divergence est donc totale**, et c'est le travail de la section 3 : la page + recevra
  la même page, bâtie par le même code, **sans l'icône Partager** (§3.2), et sans les
  réglages qui n'existent que sur une fiche (RELANCER, SUPPRIMER, COMMENTAIRES — §6 :
  « Relancer et Partager n'existent que sur la fiche »).
- **Les mots de l'échéance divergent déjà**, et ce n'est pas un détail :
  page + → `un jour · 2 j · 5 j · 2 sem · + tard`
  fiche  → `repousser +2 j · +1 sem. · +1 mois · aujourd'hui`
  Deux vocabulaires pour le même contrôle. **Je ne les ai pas alignés** : ce sont des mots.
  ⚠ Et « **+ tard** » est porteur : la liaison phrase→formulaire cherche la pastille par ce
  libellé (CLAUDE.md §8) — le renommer casse la page + en silence.

**TRANCHÉ (Tom) — à appliquer en SECTION 3 :**
- **Une seule liste partout**, celle du sélecteur : `un jour · en l'air · demain · 5 jours ·
  2 semaines · ce mois-ci · une date précise…`
- **Sur la fiche, le choix courant est marqué** ; en changer, c'est repousser.
- **Le mot « repousser » disparaît.**
- ⚠ **La liaison passe par `data-d`, jamais par le libellé** — c'est exactement le piège de
  CLAUDE.md §8 (« + tard » cherché par son texte). Refaire la liste sans refaire la liaison
  casserait la page + en silence.

#### Q25 · `redteam_toile` — le flake connu, mesuré des deux côtés
Huit passages sur l'app : 16, 15, 15, 14, 13, **16, 16**, 15 · cinq sur la sauvegarde
d'avant la section : 15, 16, 15, 16, 15. **L'app atteint 16/16 comme la sauvegarde.** Les contrôles qui oscillent sont **les sondes pixel sur la Toile animée**
(« les dalles sont aux bonnes positions », « Mes Promi : les intitulés restent », « le % »).
Deux preuves qu'il ne s'agit pas d'une régression : **aucun sélecteur de mon bloc ne sort de
`#detailPoster` ou de `#settingsScreen`** (vérifié par script, 0 occurrence de `toileCv`,
`Toile`, `dalleTrame`, `body`, `.screen`), et l'écran des Réglages est **hors cadre et à
opacité 0 dans les deux versions** (`translateY(844)`, mesuré) — il ne recouvre rien.
L'app est descendue à 13 une fois sur huit — l'amplitude du flake, pas une régression.

================================================================================
## SECTION 3 — LA PAGE + : COMMENCÉE, **ARRÊTÉE ET RESTAURÉE**. Rien n'est livré.
================================================================================
Sauvegarde `sauvegardes/avant-S3-page-plus.html`. Tentative conservée telle quelle dans
`scratchpad/s3-tentative-page-plus.html` — elle n'est PAS dans `app.html`.
`app.html` est revenu à l'état livré : `redteam_ecrans` 144/144, section 1 au vert,
section 2 à 0/0/0/0/0.

**Pourquoi l'arrêt.** Pas une batterie qui rougit : **un écran que je juge raté**, et le
protocole dit de ne pas le livrer. La capture est dans `scratchpad/s3/`. Le premier jet
pose bien les couleurs (le verbe reprend le BLEU de la nature — l'app le peignait en
MENTHE, la couleur de la parole tenue) mais la mise en page casse : la question et les
tuiles restent au-dessus de la phrase, l'onde ne se peint pas, l'entête disparaît.

**La cause, comprise et pas devinée — c'est structurel, pas cosmétique.**
La fiche est un **cadre fixe** : `#detailPoster` fait 390 × 844, il ne défile pas, et la
section 1 a pu y poser chaque bloc en absolu. **La page + est une FEUILLE QUI DÉFILE** :
`#createSheet` empile `.cs-top` (233 px) puis `#csMid`, qui contient lui-même `#csQuest`,
`.tiles`, `#promiForm` et la barre. Rendre ses enfants absolus sans neutraliser d'abord la
pile fait remonter les tuiles sous la phrase. **Il faut donc, avant toute cote :**
1. sortir `#csQuest` et `.tiles` du flux dès qu'une nature est choisie (l'écran « Choix des
   trois natures » est le seul des 17 qui les montre) ;
2. figer `#createSheet` à 390 × 844 sans défilement, comme le poster ;
3. seulement ensuite poser l'onde, la dalle, l'entête, le mot de trace, la phrase, la barre.

**Ce qui est acquis et qu'il ne faut pas refaire :**
- **Les 34 cadres du moodboard sont extraits** (`scratchpad/mb/pp_*.png`) — ce sont les
  cadres **0 à 33**, dans l'ordre exact de l'inventaire (`scratchpad/index_cadres.py` donne
  la table des 102 cadres avec leur signature de texte).
- **Les primitives de l'onde sont exposées** : la section 1 publie désormais
  `window._onde = {onde, chemin, ruban, chevron, W, NATCOL, NATCLAIR, …}`. La page + trace
  la MÊME onde que la fiche, sans dupliquer une seule formule. *(Ce petit ajout est dans
  `app.html`, il est inoffensif et déjà vérifié : 144/144.)*
- **La formule du §2.5 est confirmée sur l'inventaire de la page +** : `base = max(196,
  344 − 32 × (n − 1))` donne 312 pour 2 lignes, 280 pour 3, 196 au plancher — exactement les
  trois valeurs des 17 écrans. Et **l'interligne du §2.8 reproduit toutes les hauteurs de
  ligne du document** : `int(taille × 1,2) + 24` donne 58 pour 29, 61 pour 31, 63 pour 33,
  66 pour 35, 67 pour 36, 57 pour 28, 60 pour 30. **Aucune de ces valeurs n'est à deviner.**
- **La structure de la page + est relevée** : `#createSheet` > `#csTrameCv` · `.cs-top`
  (`.closeb`, `.cs-mark`, `#csGrappe`) · `#csMid` (`#csQuest`, `.tiles`, `#promiForm` avec
  `#csPhrase` et `#planterZone`, `#csBotBar`, `#promiExtra`).
- **La phrase est du texte en ligne** (`.ph-txt` avec des `<br>`, `.ph-b` le verbe, `em` les
  liaisons, `.ph-m` les mots), pas des lignes flex. On peut lui donner le rendu du §2.8 en
  CSS sans toucher à sa structure — c'est ce qu'il faut faire, la réécrire casserait la
  liaison phrase→formulaire.

#### Q26 · Trois écarts de la page + relevés, pas encore tranchés
- **Le verbe est peint en MENTHE** (`#2BE88C`) par l'app. C'est la couleur de la parole
  tenue ; l'inventaire le veut en couleur de NATURE (`#3A54FF` / `#FA2258` / `#8A5CF0`).
  **Ce n'est pas une question, c'est un bug** — il sera corrigé avec le reste.
- **Un ✦ vert est posé à côté du verbe** (`.ph-e`). Il n'existe dans aucun des 17
  inventaires. Décoration ou marque du Cercle ? **Je ne l'ai pas retiré.**
- **La ligne d'aide dit « touche Je me promets pour changer d'engagement »**, l'inventaire
  dit « touche ⇄ pour changer d'intention · touche un mot pour l'écrire ». Deux phrases,
  deux sens. **Je n'ai pas changé le mot.**

### S3 · REPRISE — LA GRAMMAIRE DE LA PAGE + EST POSÉE (le squelette des 13 écrans à phrase)
Sauvegarde `sauvegardes/avant-S3-page-plus-v2.html`. Toutes les batteries au vert après
chaque étape, pas seulement à la fin : `redteam_ecrans` 144/144, `redteam_phrase` 6/6,
`redteam_verbe` 6/6, `redteam_demande` 19/19, sections 1 et 2 intactes.

**Ce qui est posé et vérifié à l'œil (duo `scratchpad/duo_pp_promi_vide_dark.png`) :**
l'onde qui borne le champ (la même que la fiche, primitives partagées), la dalle du moteur
centrée à 88, l'entête à 24/38, le mot de trace, la phrase à sa typographie, « garder de
côté », et la barre 390 × 84 clouée à 760 **sans icône Partager**.

**Trois défauts trouvés en cours de route, chacun mesuré avant d'être corrigé :**
1. **`display:block!important` sur les formulaires a fait tomber `redteam_ecrans` à 140.**
   Le contrôle « Créer : une seule forme visible » compte les formulaires dont le display
   n'est pas `none` ; en forcer deux le cassait ([2,2,2] mesuré). **L'app gère elle-même
   quelle forme se montre — on ne touche qu'au positionnement.** Corrigé, 144/144.
2. **La taille de la phrase ne rétrécissait jamais.** Je bouclais sur `scrollWidth`, mais
   `.ph-txt` passe à la ligne : sa largeur ne dépasse jamais son conteneur. La phrase restait
   à 36 là où l'inventaire la veut à 29. **Corrigé en portant la formule du §2.8 telle
   quelle** — `Σ(caractères × taille × 0,53) + 32 par pastille + 11 par écart` — qui redonne
   exactement 29 sur « d' aller voir la mer ».
3. **L'aide et « garder de côté » se recouvraient.** Ils sont EXCLUSIFS dans le moodboard :
   l'écran « phrase vide » porte l'aide à 574 et pas de lien, les écrans remplis portent le
   lien à 708 et pas d'aide. C'est la logique du document, pas une invention.

**Q26, appliqué (tes trois réponses) :** le verbe porte la couleur de NATURE (l'app le
peignait en menthe) · le **✦ vert est retiré** — le ✦ appartient au Cercle · la ligne d'aide
porte **le mot du moodboard** (« touche ⇄ pour changer d'intention · touche un mot pour
l'écrire ») à la place de « touche Je me promets pour changer d'engagement ».

### S3 · Q28 TRANCHÉ ET APPLIQUÉ — l'échéance a quitté la phrase
**La phrase ne garde que VERBE et OBJET.** L'échéance descend dans Peaufiner, en tête, avec
la liste unique. C'est le même chemin qu'avait pris « dans une Nuée » avant elle, et le
commentaire du code le disait déjà : *trois choix à remplir, c'est déjà beaucoup*.

**Les trois conséquences, traitées ensemble :**
1. **`base` passe de 280 à 312** et tout ce qui suit remonte de 32. Le moteur le fait seul —
   mais un **`<br>` orphelin** restait en fin de phrase (les trois branches finissaient par
   `… + '<br>' + lignesFin`, lignesFin devenu vide) : la phrase comptait encore 3 lignes et
   l'onde passait 32 px trop haut. Trouvé au duo, pas à la mesure. **Corrigé.**
2. **`redteam_phrase` est mis à jour, pas contourné.** L'ancien contrôle « quand » vérifiait
   la liaison phrase → pastille « + tard » : il est périmé, exactement comme « sens » l'a
   été. Le nouveau se place au niveau de la décision — *la phrase ne porte plus de créneau
   « quand »*, et *aucune pastille d'échéance n'est adressable par son seul texte*. Il tombe
   si une pastille est ajoutée sans prise. **6/6.**
3. **La liaison passe par une prise stable, jamais par le libellé.** Le contrôle a trouvé
   le trou tout de suite : la pastille **« un jour » est injectée à l'exécution** (l. 4934)
   et n'a pas de `data-d` — elle porte `data-q="jour"`. Les autres ont bien `data-d`. Le
   contrôle exige donc `data-d` **ou** `data-q` sur chacune : plus aucune n'est joignable
   par son texte.

**Ce qui reste de Q28, et qui n'est PAS fait :** la liste unique
(`un jour · en l'air · demain · 5 jours · 2 semaines · ce mois-ci · une date précise…`)
n'est pas encore posée dans le réglage AVANT de Peaufiner — celui-ci montre toujours
`repousser +2 j · +1 sem. · +1 mois · aujourd'hui`. La liste existe déjà dans l'app (c'est
l'`opts` du choix de la phrase, l. 5195) : c'est elle qu'il faudra brancher. **Le mot
« repousser » n'a pas encore disparu.**

#### Q28 bis · CE QUE DISAIT L'ANCIEN ÉTAT (conservé pour mémoire)
C'est le seul écart qui reste sur ces écrans, et il est de produit, pas de dessin. L'app
écrit **trois** lignes (verbe / objet / avant), le moodboard **deux** — et sa ligne d'aide
dit explicitement « l'échéance, la Nuée et le reste sont **dans Peaufiner** ». Le moteur
suit correctement : trois lignes donnent `base = 280`, deux donnent `312` (§2.5), et tout ce
qui est dessous se décale de 32 px. **Je n'ai pas retiré la ligne** — l'échéance est reliée
à la phrase et `redteam_phrase` la couvre. Si l'échéance doit quitter la phrase pour
Peaufiner, c'est ta décision, et elle se combine avec la liste unique déjà tranchée.

#### Q27 · Les trois cadres du geste montrent un rond dans la barre de la page +
Les cadres 28 à 33 (« Le geste · au repos / pendant / signé ») dessinent, dans la barre
Peaufiner, le cercle de 46 px avec son icône — alors que le **§3.2 écrit noir sur blanc
« Pas d'icône Partager sur la page + »**, ce que tu as reconfirmé. **J'ai suivi la règle,
pas le dessin** : pas de rond sur la page +. **TRANCHÉ (Tom) : le §3.2 est la spécification,
les trois cadres sont une erreur de dessin du moodboard.** Ce n'est donc pas une question
ouverte — c'est une erreur constatée, à corriger côté moodboard.


### S3 · LA LISTE UNIQUE EST BRANCHÉE · `releve-S3` EXISTE — DÉCOMPTE : **0 sur 17**
Point de reprise : `sauvegardes/s3-liste-unique.html`.

**1 · La liste unique de l'échéance est posée dans AVANT — 8/8 au test dédié**
(`scratchpad/test_echeance.py`). Elle est **branchée, pas recréée** : ce sont les mots de
l'`opts` du sélecteur de la phrase. Les trois règles sont vérifiées par le test, pas
affirmées :
- **« repousser » a disparu.** L'ancien contrôle faisait un décalage relatif
  (`cur.due = (cur.due||0) + d`) ; c'est devenu un choix absolu. Le choix courant est
  simplement marqué.
- **« un jour » et « en l'air » ne fusionnent pas.** Les deux donnent `due = null`, mais
  `enLair` est un drapeau séparé — le test compare les deux états et échoue s'ils
  deviennent identiques.
- **Sans choix explicite, aucune pastille active** (`dueChoisi` porte l'explicite).
- La liaison passe par `data-q` / `data-d` / `data-datepick`, jamais par le libellé.
`test_s2_fonctions` est mis à jour de la même façon (« +1 sem. » n'existe plus) : **25/25**.

**2 · `releve-S3-page-plus.py` est écrit, avec la présence peinte.** Il ne réécrit aucune
cote à la main : il les DÉRIVE des formules (§2.5, §2.4 bis, §2.7) écran par écran, et il
lit les pixels du canevas pour l'aplat, la dalle et les points. Premier passage sur
**12 cadres (6 écrans × 2 thèmes)** :

    position 0 · collisions 0 · hors cadre 0 · style 9 · peinture 35

**3 · Ce que le juge a trouvé, trié mais PAS ENCORE CORRIGÉ — et je ne compte donc rien.**
- **RÉEL : `.ph-hint` est peinte à opacité 0,6.** Mon `opacity:1!important` ne gagne pas ;
  le §6 ne descend jamais sous 72 %.
- **RÉEL À CONFIRMER : sur un Chiche, la sonde ne trouve aucun point sur l'onde.** Soit le
  canevas n'est pas repeint au changement de nature, soit la scène ne bascule pas vraiment
  en Chiche. À instrumenter, pas à deviner.
- **DÉTECTEUR À CORRIGER : « ton sur ton » sur le mot-marque, ✕ FERMER, le mot de trace et
  « Peaufiner ».** Ces textes sont posés SUR le champ peint dans le canevas ou sur la barre
  de nature ; mon contrôle les compare au `background-color` CSS de la feuille, qui n'est
  pas ce qu'on voit. Il faut **lire le pixel réellement peint sous l'élément**, comme le
  fait déjà la sonde du trait. C'est le même piège que la section 1 : un contrôle qui
  mesure autre chose que ce qui est peint.

**DÉCOMPTE FRANC : 0 écran sur 17.** Douze cadres sont mesurés et à zéro sur la position,
les collisions et le débordement — mais aucun n'est à zéro partout, et un écran ne compte
que mesuré **et** regardé. Reste : les 9 écarts de style, les 2 défauts réels ci-dessus, le
détecteur à corriger, puis les 11 écrans non encore jouables (promettez-moi, la Nuée, les
trois choix ouverts, les deux gardé de côté, les trois du geste, le choix des natures), et
enfin le Peaufiner de la page +.

### S3 · LE JUGE EST À ZÉRO SUR 12 CADRES — ET L'ŒIL DIT ENCORE NON. **DÉCOMPTE : 0 / 17.**
Point de reprise : `sauvegardes/s3-six-ecrans.html`. Batteries : `redteam_ecrans` 144/144,
phrase 6/6, verbe 6/6, demande 19/19 · sections 1 et 2 intactes.

**Les deux diagnostics demandés, faits à l'instrument :**
- **`.ph-hint` à 0,6** — je n'ai pas surenchéri en `!important`. J'ai demandé au navigateur
  quelle règle l'impose : `.device #createSheet[data-kind="promi"] #csPhrase .ph-hint`
  (2 id + 3 classes) battait mon sélecteur (2 id + 2 classes) **d'un seul cran**. Ajouter
  `#csPhrase` (3 id) suffit. Battue précisément, pas à coups de masse.
- **Le Chiche sans points** — journal des appels au contexte 2D : **211 appels, nature
  `chiche`, base 280**. Le canevas EST repeint ; c'était **ma sonde** qui ne comparait que
  le canal rouge, et sur un Chiche l'aplat `#FA2258` et les points `#FFC0A8` n'ont que 5 de
  différence en rouge. Elle compare désormais les trois canaux.

**Ce que le juge a fait tomber, et qui était RÉEL :**
- en thème clair, **le mot de trace était crème sur crème** (Δ0) : il est posé sous l'onde,
  donc sur le CORPS. L'inventaire clair le donne en `#16171B`. Corrigé.
- en thème clair, **liaisons, pastilles vides, aide et « garder de côté » en teinte claire**
  sur le corps crème : Δlum 35, sous le seuil de 42. L'inventaire clair les donne en
  **couleur pleine de la nature**. Corrigé pour les trois natures.

**Ce que L'ŒIL a trouvé et que le juge laissait passer (encore) :**
- **la pastille pleine s'inverse en thème clair** — fond encre, texte crème. Mon juge
  acceptait les deux ; le cadre clair tranche. Corrigé, et **le juge resserré**.
- **le lien « garder de côté » de l'app restait posé tout en haut du cadre**, au-dessus du
  mot-marque. Masqué : le nôtre le remplace à sa cote.

**POURQUOI JE NE COMPTE AUCUN ÉCRAN, malgré 0 / 0 / 0 / 0 / 0 sur 12 cadres.**
Le duo du Chiche montre deux divergences que le juge ne regarde pas encore :
1. **la liaison « à » manque devant le prénom** — le moodboard écrit « à Marion, » ;
2. **l'app ajoute « ＋ avec quelqu'un »**, une pastille d'ajout de créneau qui n'est sur
   aucun des 17 cadres ;
3. et la **dalle du Chiche est celle d'un Promi** (mauve) : `_ppDalleId` prend la dernière
   promesse, pas une de la nature courante.
Tant que ces trois-là ne sont pas traités, **aucun écran n'est superposable**. Un juge à
zéro ne fait pas un écran : c'est exactement la leçon de la section 1.

#### Q29 · Deux points de produit relevés sur la phrase du Chiche
- **« ＋ défier quelqu'un » / « ＋ avec quelqu'un »** n'existent dans aucun cadre. Ce sont
  des fonctions (ouvrir un créneau absent), pas de la décoration : **je ne les retire pas.**
- **La liaison « à » devant le prénom** : le moodboard l'écrit, l'app ne la met pas sur un
  Chiche. C'est un mot — **je ne l'ajoute pas.**

### S3 · Q29 APPLIQUÉ — le Chiche se superpose presque. **DÉCOMPTE : 0 / 17.**
Point de reprise : `sauvegardes/s3-q29-applique.html`. `redteam_ecrans` 144/144 · phrase 6/6
· verbe 6/6 · demande 19/19 · sections 1 et 2 intactes · `releve-S3` 0/0/0/0/0 sur 12 cadres.

**1 · La liaison « à » est posée** — « à Marion, chiche de courir dimanche ». Le mot vient
du document.
**2 · Le créneau du compagnon ne montre plus rien quand il est vide** — ni le mot, ni la
pastille, ni le « ＋ ». C'était bien le bug que le duo montrait : l'app affichait
« ＋ avec quelqu'un » sur un Chiche sans compagnon. **La fonction reste** : on ajoute le
compagnon par le réglage AVEC de Peaufiner (section 2), qui existe déjà et que l'inventaire
dessine en pointillé quand il vaut « personne ».
Le créneau « qui je défie », lui, **se montre même vide** — le cadre « Chiche · vide » écrit
« à qui ? » en pastille pointillée. Deux créneaux, deux comportements, comme tu l'as dit.
**3 · La dalle prend la nature courante.** `_ppDalleId` retombait sur la dernière promesse
posée ; un Chiche portait donc la dalle mauve d'un Promi. Corrigé : on cherche d'abord une
promesse de la nature écrite.

**TROIS RÉSIDUS VUS À L'ŒIL SUR « Chiche · rempli », ET C'EST POURQUOI JE COMPTE ZÉRO :**
1. **la virgule tombe HORS de la pastille** — l'app écrit « [Marion] , », le cadre écrit
   « [Marion,] ». Un caractère, mais il casse la forme de la pastille.
2. **le verbe est capitalisé** — l'app « Chiche », le cadre « chiche ». Le cadre « Chiche ·
   vide » le met bien en capitale, parce qu'il ouvre la phrase ; sur l'écran rempli il suit
   « à Marion, » et passe en bas de casse. **C'est une règle de casse, donc un mot : je ne
   l'ai pas changée.**
3. **le visage manque dans la pastille du prénom** — le cadre pose un visage de 25 px
   (§2.10) avant « Marion, ». Non porté.

**0 écran sur 17.** Le juge est à zéro sur 12 cadres, mais trois divergences visibles
subsistent sur le Chiche et je n'ai pas re-regardé les six écrans après les deux derniers
correctifs. Un écran ne compte que mesuré ET regardé, après le dernier changement.

================================================================================
## SECTION 3 — LA PAGE + : LIVRÉE EN L'ÉTAT. **4 écrans sur 17.**
================================================================================
Sauvegarde `sauvegardes/avant-S3-page-plus-v2.html` · point de reprise
`sauvegardes/s3-phrase-complete.html` · juge `releve-S3-page-plus.py`.

**Les cinq lignes, sur les 12 cadres que le juge sait jouer :**

    position 0 · style 0 · collisions 0 · hors cadre 0 · présence peinte 0
    redteam_ecrans 144/144 · phrase 6/6 · verbe 6/6 · demande 19/19 · geste 13/13
    filets 0 parasite · section 1 au vert · section 2 à 0/0/0/0/0 · fonctions S2 25/25

**LES 4 ÉCRANS QUE JE COMPTE** — mesurés à zéro dans les deux thèmes ET regardés en duo
après le dernier changement qui les touche :
`Promi · à soi rempli` · `Promi · promets-moi` · `Chiche · rempli` · `Promi · phrase vide`.
Pour chacun j'ai regardé **un** thème ; le juge couvre les deux.

**LES 2 QUE JE NE COMPTE PAS, bien que le juge soit à zéro dessus :**
`Promi · à Rachel` et `Chiche · vide` — mesurés, mais **pas re-regardés** après l'ajout du
visage, de la virgule, de la casse et de l'élision. Un écran ne compte que mesuré ET
regardé, après le dernier changement.

**CE QUI A ÉTÉ FAIT DANS CE LOT**
- **La casse française** : majuscule au premier mot de la phrase, bas de casse ailleurs. Le
  verbe n'ouvre la phrase que si rien de REMPLI ne le précède — ce qui reproduit les deux
  cadres du Chiche sans exception (« Chiche » au-dessus d'un placeholder vide, « chiche »
  au-dessus d'un prénom).
- **La virgule appartient à la pastille** : « [Marion,] » est un seul objet touchable.
- **Le visage (§2.10)** entre dans la pastille du prénom, à 0,76 × la taille, padding gauche
  9. La construction du visage est **exposée** par la section 1 (`window._visageSvg`) — une
  seule construction du visage existe dans le produit.
- **L'élision (§2.8 / §4)** : « de » devient « d' » devant voyelle ou h muet, collé au mot,
  l'écart tombant de 11 à 3 px. L'app écrivait « de aller voir la mer ».
- **La dalle prend la nature courante** (elle prenait la dernière promesse posée).

#### Q30 · La dalle d'un Chiche sur la page + — option conservatrice, à trancher
**Aucun Chiche n'existe dans les données de démonstration** (0 sur 23 promesses, mesuré).
La page + ne peut donc pas montrer la dalle d'un Chiche existant : elle retombe sur celle
d'un Promi. Le §1.2 donne pourtant une palette de dalle PAR NATURE (`#FFE2D2 · #FFC0A8 ·
#F2977A` pour le Chiche), et les cadres la montrent. Mais **teinter une dalle par sa nature
est interdit par CLAUDE.md §4**, sauf sur la bande haute d'une fiche — or le champ de la
page + EST cette bande. **Option conservatrice prise : on ne teinte pas.** La dalle reste
celle du moteur, non teintée. À trancher.

#### CE QUI RESTE SUR LA SECTION 3 — 13 écrans
1. **Re-regarder** `Promi · à Rachel` et `Chiche · vide` (mesurés, pas revus).
2. **Les 11 écrans que le juge ne sait pas encore jouer** : `Choix des trois natures`,
   `Promi · promettez-moi`, `Nuée · écriture`, les trois `Choix ouvert` (écrire un mot,
   choisir une personne, l'échéance — tous à `amp = 22`, `base = 196`), `Garder de côté`,
   `Gardé de côté · après`, et les trois du geste (au repos, pendant, signé).
   Leur mise en scène doit être **forcée dans la capture Playwright**, jamais dans les
   données — c'est ce qui avait pollué le localStorage en section 1.
3. **Le Peaufiner de la page +** : brancher le bloc de la section 2, même libellés, même
   ordre, **sans icône Partager**. Non commencé. Le point d'attention tient : ce bloc a été
   bâti dans un cadre fixe et la page + est une feuille qui défile — la parade `#tenirCv`
   (aucun ancêtre positionné entre le geste et `#createSheet`) est déjà en place dans le
   bloc S3, elle devra être maintenue, et `redteam_ecrans` vérifié avant d'aller plus loin.


================================================================================
## SECTION 3 · LIVRAISON — **4 écrans sur 17.** La méthode « depuis l'inventaire »
## a fait rougir une batterie : ARRÊT ET RESTAURATION, cause isolée.
================================================================================
Point de reprise `sauvegardes/s3-livraison.html` · tentative conservée dans
`scratchpad/s3-tentative-inventaire.html`, hors de `app.html`.

**Les batteries, à la livraison :**

    redteam_ecrans 144/144 · phrase 6/6 · verbe 6/6 · demande 19/19 · geste 13/13
    filets 0 parasite · redteam_toile 16/16 (flake connu, reconfirmé)
    section 1 au vert · section 2 à 0/0/0/0/0 · section 3 à 0/0/0/0/0 sur 12 cadres

**Q30 appliqué : on ne teinte pas la dalle.** L'exception du §4 porte sur l'APLAT, qui
affirme la nature ; la dalle posée dessus reste elle-même.
**Deux Chiche ajoutés au jeu de démonstration** — un lancé (« courir dimanche », Marion),
un relevé (« le grand plongeoir », Marion, avec Rachel). Vérifié isolément : les batteries
restent au vert (verbe 6/6), et la page + a enfin une dalle de Chiche.

#### ⚠ LA MÉTHODE « ÉCRIRE DEPUIS L'INVENTAIRE » A CASSÉ UNE BATTERIE — arrêt immédiat
J'ai posé la règle générale « ce que l'inventaire ne liste pas ne se peint pas » d'un seul
coup sur la page + (masquer tout dans `#promiForm` sauf la phrase et le geste, tout dans
`#csPhrase` sauf le texte). **`redteam_verbe` est passé de 6/6 à 4/6** :

    « la bascule mène à un vrai bouton »  KO  bouton={f:1, h:0, vis:false}   (deux thèmes)

**Cause isolée, pas devinée.** J'ai retiré les règles une à une puis restauré, et rejoué la
batterie à chaque fois : **le seed des deux Chiche est innocent (6/6 seul)** ; c'est le
balai qui ferme aussi les panneaux qu'un GESTE ouvre — `#csChoix` et le bouton où mène le
⇄. **La leçon :** « ce que l'inventaire ne liste pas ne se peint pas » vaut pour ce qui est
peint AU REPOS, pas pour les panneaux qu'un geste déplie — que les trois cadres « Choix
ouvert » montrent justement. **Le crible doit être posé écran par écran, avec la liste des
nœuds autorisés de CET écran**, jamais d'un seul coup sur tout le formulaire.
`app.html` est restauré à l'état vert ; la tentative est conservée hors du fichier.

#### CE QUI RESTE — 13 écrans, et le Peaufiner de la page +
1. **Le crible par écran** (au lieu du balai) : pour chacun des 17, la liste des nœuds que
   son inventaire liste, et le masquage de tout le reste — en laissant vivre les panneaux
   de choix, qui sont des écrans à part entière (cadres 18 à 23).
2. **Re-regarder** `Promi · à Rachel` et `Chiche · vide` (mesurés à zéro, pas revus depuis
   le visage, la virgule, la casse et l'élision).
3. **Les 11 écrans que le juge ne sait pas encore jouer** : choix des trois natures,
   `promettez-moi`, `Nuée · écriture`, les trois `Choix ouvert` (`amp = 22`, `base = 196`),
   `Garder de côté`, `Gardé de côté · après`, les trois du geste. Mise en scène forcée dans
   la capture, jamais dans les données.
4. **Le Peaufiner de la page +** : non commencé. Bloc de la section 2, sans Partager,
   `redteam_ecrans` vérifié avant d'aller plus loin.


================================================================================
## SECTION 3 · LIVRAISON — **4 écrans sur 17.** Le crible par écran est posé.
================================================================================
Point de reprise `sauvegardes/s3-crible.html`.

    redteam_ecrans 144/144 · phrase 6/6 · verbe 6/6 · demande 19/19 · geste 13/13
    filets 0 parasite · S1 au vert · S2 0/0/0/0/0 · S3 0/0/0/0/0 sur 12 cadres

**LE CRIBLE PAR ÉCRAN est en place** — et il ne casse plus rien (`redteam_verbe` 6/6).
Il énumère les nœuds hors inventaire (`.ph-slots`, `.ph-addslot`, invites héritées, lien de
brouillon) et ne les ferme **que dans l'état au repos** : dès qu'un panneau de choix est
ouvert, il relâche tout, parce que l'écran courant devient « Choix ouvert · … », qui a son
propre inventaire. **Le piège est noté dans CLAUDE.md §8**, à côté de `#tenirCv`.

**LES 4 ÉCRANS COMPTÉS :** `Promi · phrase vide` · `Promi · à soi rempli` ·
`Promi · promets-moi` · `Chiche · rempli`.

#### Q31 · `Chiche · vide` — DEUX DÉFAUTS VUS AU DUO, non corrigés (fin de lot)
1. **La phrase passe à la ligne.** Le placeholder de l'app est « courir dimanche… » (avec
   les points de suspension) là où le cadre écrit « courir dimanche » : la pastille ne tient
   plus sur sa ligne et tombe à 592 au lieu de 538. **La formule du §2.8 dit qu'elle tient**
   (`nb_car × taille × 0,53 + 32`), le navigateur dit non — l'estimation est optimiste sur
   cette chaîne. **Il faut mesurer la ligne rendue, pas seulement l'estimer**, ou compter le
   placeholder sans ses points. Non corrigé : je ne lance pas un correctif que je ne peux
   plus vérifier dans ce lot.
2. **La ligne d'aide est celle du Promi.** Le cadre du Chiche écrit « le compagnon et
   l'échéance sont dans Peaufiner » ; l'app y met la phrase du Promi. C'est un mot du
   moodboard, donc à prendre — mais par nature, pas globalement.

#### CE QUI RESTE — 13 écrans
1. **Q31** : la ligne qui passe à la ligne, et l'aide par nature.
2. **Re-regarder `Promi · à Rachel`** (mesuré à zéro, duo produit, pas encore regardé).
3. **Les 11 écrans que le juge ne sait pas jouer** : choix des trois natures,
   `promettez-moi`, `Nuée · écriture`, les trois `Choix ouvert` (`amp = 22`, `base = 196`),
   `Garder de côté`, `Gardé de côté · après`, les trois du geste. Mise en scène forcée dans
   la capture, jamais dans les données.
4. **Le Peaufiner de la page +** : toujours non commencé. Bloc de la section 2, sans
   Partager, `redteam_ecrans` vérifié avant d'aller plus loin.


================================================================================
## SECTION 3 · LIVRAISON FINALE — **5 écrans sur 17.**
================================================================================
Point de reprise `sauvegardes/s3-livraison-finale.html`.

#### CORRECTION DU §2.8 — l'estimation de largeur est remplacée par une MESURE
Le document estimait la largeur d'une ligne par
`Σ(caractères × taille × 0,53) + 32 par pastille + 11 par écart`. **Cette estimation est
optimiste** : elle déclare qu'une ligne tient là où le navigateur la fait passer à la ligne
(constaté sur « courir dimanche… »). **Et une ligne qui passe à la ligne décale tout ce qui
suit de 32 px** (§2.5) — c'est la classe de bug la plus coûteuse de la section.
**La page + mesure désormais la ligne rendue** : en `white-space:nowrap` les `<br>` font
toujours les lignes et `scrollWidth` donne la plus large ; on rétrécit tant qu'elle dépasse
342. L'estimation reste en secours si la mesure est indisponible. **À porter dans
`PROMI-SPECIFICATIONS.md` §2.8** — c'est une correction du document, pas un contournement.

**Les deux autres réponses de Q31 sont appliquées :** le placeholder prend le mot du cadre
(« courir dimanche », sans points de suspension) · **la ligne d'aide est par nature** — le
Chiche écrit « le compagnon et l'échéance sont dans Peaufiner ».

**RÈGLE GÉNÉRALE ACTÉE (décision Tom) :** quand le moodboard écrit un mot et l'app un
autre, **on prend celui du moodboard et on note**. On ne s'arrête que si deux cadres du
moodboard se contredisent entre eux.

#### LES 5 ÉCRANS COMPTÉS
`Promi · phrase vide` · `Promi · à soi rempli` · `Promi · promets-moi` ·
`Chiche · rempli` · `Chiche · vide` — mesurés à zéro dans les deux thèmes et regardés en
duo après le dernier changement qui les touche.

#### CE QUI RESTE — 12 écrans
1. **Re-regarder `Promi · à Rachel`** : mesuré à zéro, duo produit, jamais regardé.
2. **Les 11 écrans que le juge ne sait pas jouer** : `Choix des trois natures`,
   `Promi · promettez-moi`, `Nuée · écriture`, les trois `Choix ouvert` (`amp = 22`,
   `base = 196`), `Garder de côté`, `Gardé de côté · après`, les trois du geste.
   Mise en scène forcée dans la capture Playwright, jamais dans les données.
3. **Le Peaufiner de la page +** : non commencé. Bloc de la section 2, mêmes libellés,
   même ordre, **sans icône Partager**. Morceau à risque : un bloc bâti dans un cadre fixe
   qui entre dans une feuille qui défile — parade `#tenirCv` à maintenir, `redteam_ecrans`
   à vérifier avant d'aller plus loin.


================================================================================
## SECTION 3 · LIVRAISON — **12 écrans sur 17.** Le juge en joue 12, l'œil les a vus.
================================================================================
Point de reprise `sauvegardes/s3-douze-ecrans.html` · sauvegarde d'entrée
`sauvegardes/avant-S3-suite.html` · juge `releve-S3-page-plus.py` (12 écrans × 2 thèmes).

**Les cinq lignes, sur les 12 cadres que le juge sait jouer :**

    position 0 · style 0 · collisions 0 · hors cadre 0 · présence peinte 0
    redteam_ecrans 144/144 · phrase 6/6 · verbe 6/6 · demande 19/19 · geste 13/13
    filets 0 parasite · redteam 15/15 · redteam2 10/10 · redteam3 18/18 · toile 16/16
    section 1 AU VERT · section 2 à 0/0/0/0/0
    releve-design : 555 écarts AVANT comme APRÈS — sa référence est périmée depuis le
    portage de la section 1, elle n'a pas bougé de ce lot (mesuré des deux côtés).

#### LES 12 ÉCRANS COMPTÉS — mesurés à zéro dans les deux thèmes ET regardés en duo
`Promi · phrase vide` · `Promi · à soi rempli` · `Promi · à Rachel` · `Promi · promets-moi`
· `Promi · promettez-moi` · `Chiche · vide` · `Chiche · rempli` · `Nuée · écriture` ·
`Choix des trois natures` · `Choix ouvert · écrire un mot` ·
`Choix ouvert · choisir une personne` · `Gardé de côté · après`.
(+ `Le geste · pendant`, mesuré et regardé, mais je le compte dans les 5 restants — voir
plus bas : son frère « signé » n'est pas fait, la séquence n'est pas entière.)

---

### CE QUE CE LOT A TROUVÉ ET CORRIGÉ

**1 · LA FLÈCHE D'INVITE (§2.4) N'ÉTAIT PEINTE SUR AUCUN CADRE DE LA PAGE +.**
Le code de référence du §4 la dessine sur l'état « plate » ; l'app ne la dessinait jamais.
Portée telle quelle : Bézier bombée à gauche, tête calculée sur la tangente réelle en B,
ailes à ±32°, longueur 13. **Les cinq écrans déjà livrés en avaient besoin aussi** — c'est
pour ça que `Promi · à Rachel` ne superposait pas.

**2 · `choixOuvert()` NE VOYAIT PAS LE PANNEAU DE L'APP.** Il cherchait `#csKeyboard`,
`#csPersonnes`, `#csDates`, `#csChoixPanel` ; le panneau s'appelle **`#csChoix`**. Les trois
cadres « Choix ouvert » restaient donc à `base = 312/280` au lieu de 196 — le mot de trace
à 358 au lieu de 236, cent px trop bas.
**⚠ Et il ne faut JAMAIS tester la hauteur RENDUE du panneau :** dès que ses éléments
passent en absolu (les cotes du §5), `#csChoix` retombe à 0 de haut, « ouvert » devient
faux, les cotes reviennent au repos, les éléments repassent en flux — et l'écran **oscille
d'une passe à l'autre** (constaté : le mot de trace à 236 et la phrase à 392 dans le même
relevé). La classe `.ouvert` EST l'état.

**3 · LA TAILLE DE LA PHRASE : L'ESTIMATION DU §2.8 EST LA RÈGLE, PAS UN PIS-ALLER.**
Le lot précédent l'avait remplacée par une mesure navigateur (Q31). **C'était une erreur**,
et elle touchait les cinq écrans déjà comptés. Vérifié cadre par cadre :

    cadre            vide  soi  Rachel  promets  promettez  Chiche  Nuée  mot  personne
    document          29    29    31      36        35        33     29    28     30
    estimation §2.8   29    29    31      36        35        33     29    29     30   ✅
    mesure seule      35    36    35      36        35        32     34    30     30   ✗

La mesure remplit **toujours** les 342 px : la phrase sortait systématiquement trop grosse.
Mais l'estimation reste optimiste sur certaines chaînes (« courir dimanche… », le bug de
Q31). **On prend désormais la PLUS PETITE DES DEUX** : l'estimation compose, la mesure
garantit qu'aucune ligne ne casse. À porter dans le document — la note « §2.8 corrigé » du
lot précédent est à annuler.

**4 · LA PHRASE DE LA NUÉE EXISTAIT MAIS N'ÉTAIT PAS UNE PHRASE.** `#nueePhrase` écrivait
« Je lance une Nuée » en **texte nu** au lieu d'une pastille, hors cotes, dans un formulaire
que le moteur S3 ne regardait pas. La boîte active est maintenant marquée `.pp-phrase`
(c'est la prise que suit le juge), et **le CSS de la phrase est la COPIE EXACTE de celui de
`#csPhrase`, au seul nom près** — une seule grammaire de phrase existe dans le produit.

**5 · LE GESTE DE LA NUÉE ET DU BROUILLON N'ÉTAIENT PAS PORTÉS.** `#planterZoneN` peignait
encore son panneau gris à 640 sur l'écran `Nuée · écriture`. Les trois zones suivent
maintenant la même règle que `#planterZone`.

**6 · LA TUILE DU CHICHE N'ÉTAIT JAMAIS PEINTE.** Sa teinte figurait dans la table `T`, son
canevas dans le DOM, mais **aucune ligne ne l'appelait** : la carte « Un Chiche » du cadre
17 restait vide. Une ligne ajoutée, calquée sur celle du Promi.

**7 · LE PLURIEL.** « Rachel, Nico, » suivi de « promets-moi » : une faute de français que
l'app écrivait parce qu'elle ne voyait le pluriel que dans « tout le monde ». Deux prénoms
suffisent — c'est ce que montre le cadre `Promi · promettez-moi`.

**8 · LA PHRASE S'AFFADISSAIT À 60 %** dès qu'un choix s'ouvrait
(`#createSheet:has(#csChoix.ouvert) #csPhrase .ph-txt`, l.12155). Les trois cadres la
montrent pleine, et **le §6 n'admet aucune opacité sous 72 %** sur du texte lisible.

**9 · GARDÉ DE CÔTÉ : PAS D'APLAT.** Le cadre 27 n'a pas de champ — rien n'est promis. La
dalle et les points sont posés sur le corps nu, et en thème clair l'entête passe à l'encre
(elle était crème sur crème, Δ0). C'est la même règle que la fiche d'un gardé de côté
depuis la section 1 (`e.aplat = false`) ; elle n'avait pas été portée sur la page +.

**10 · LES MOTS DU MOODBOARD PRIS, ET NOTÉS** (règle générale actée) :
`quelqu'un` → **`qui ?`** (pastille vide du destinataire) · le `+` du chooser →
**`+ ajouter quelqu'un`** · la question du cadre 17 se coupe **toute seule**
(« Qu'est-ce que tu / promets ? ») là où le `<br>` codé en dur la mettait sur trois lignes.

**11 · UNE RÉGRESSION, ATTRAPÉE ET DÉFAITE DANS LE MÊME LOT.** J'ai mis `#addPromi` et
`#addNuee` dans le balai « hors inventaire » : `redteam_verbe` est tombé de 6/6 à **4/6**
(« la bascule mène à un vrai bouton », deux thèmes). **Ce sont les boutons où mène la
bascule du geste** — des écrans qu'un doigt ouvre, pas de la décoration au repos. Règle
retirée, 6/6 rétabli. C'est **le piège du §8 de CLAUDE.md**, à l'identique, une deuxième
fois : le crible se pose nœud par nœud, jamais en bloc.

---

### LES QUESTIONS

#### Q32 · Les trois cadres « Choix ouvert » ne suivent pas la dérivation générale
Partout `trace = boîte − 60` et `phrase = boîte + 6`. Sur ces trois cadres, le document
écrit **236** (et non 218) et **280** (et non 284). J'ai pris **les cotes écrites**, qui
font foi (§5), et je les ai mises dans une table nommée du juge. **La formule du §2.4 bis
ne les explique pas** — soit l'amplitude réelle y est autre chose que 22, soit ces trois
compositions ont été calées à la main. **Non tranché : je note.**

#### Q33 · La taille de départ de la phrase sur un choix ouvert
Les trois cadres donnent 30 · 30 · 28. La formule du §2.8 part de 36 à trois lignes.
J'ai posé **30 au départ dès qu'un choix est ouvert** (même logique que l'onde qui
s'aplatit : le champ est réduit, la phrase suit) puis le rétrécissement normal.
Reste **1 px d'écart** sur `écrire un mot` (29 chez moi, 28 au cadre) : le cadre compte le
**curseur** comme un caractère de plus. Sans conséquence de position.

#### Q34 · « Choix ouvert · l'échéance » est PÉRIMÉ PAR Q28 — non porté
Le cadre montre « avant [quand ?] » **dans la phrase**. Or Q28 (ta décision) a fait sortir
l'échéance de la phrase, pour Peaufiner, et **la ligne d'aide du moodboard le dit
elle-même** (« l'échéance, la Nuée et le reste sont dans Peaufiner »). Le cadre ne peut donc
plus être atteint tel qu'il est dessiné. **Option conservatrice : je ne le porte pas et je
ne ressuscite pas la ligne.** Le panneau qu'il décrit (les trois pastilles, la grille du
mois, « un jour » / « en l'air ») vit maintenant dans le réglage AVANT de Peaufiner.
**À trancher : le cadre est-il à refaire côté moodboard, ou l'échéance doit-elle revenir ?**

#### Q35 · « Le geste · au repos » et « Promi · à soi rempli » se contredisent sur le lien
Même écran, même composition, mais le lien du bas change : `garder de côté` à 708 sur les
cadres 2 à 8, **`planter au bouton` à 702** sur le cadre 28. Les deux ne peuvent pas
coexister et **aucun cadre ne dit quand on passe de l'un à l'autre**. L'app garde
`garder de côté` au repos (c'est la fonction réelle), et la bascule trait/bouton reste où
elle est. **Non tranché.**

#### Q36 · « Le geste · signé » attend un mot d'échéance que l'app ne sait pas écrire
Le cadre écrit « planté · à tenir **avant l'été** ». Le vocabulaire d'échéance de l'app est
`un jour · en l'air · demain · 5 jours · 2 semaines · ce mois-ci · une date précise` — « à
tenir un jour » ne se dit pas. **Composer cette phrase serait inventer une tournure**
(CLAUDE.md §9). `pendant` est fait et vérifié ; **`signé` ne l'est pas.** Il appartient
d'ailleurs à la section 5 (« L'instant »), où le sujet sera traité en entier.

#### Q30 (RAPPEL, AGGRAVÉ) · la dalle de la page + est en ton sur ton
Décision en cours : **on ne teinte pas** la dalle par la nature. Conséquence vue au duo :
sur `Promi · promettez-moi` et `Choix ouvert · choisir une personne`, la dalle est **bleue
sur bleu** — à peine visible ; sur `Nuée · écriture` elle est lilas très clair sur mauve.
Les cadres, eux, montrent toujours une dalle **claire** sur le champ plein.
**CLAUDE.md §3 interdit le ton sur ton (seuil de luminosité 42)** — la règle et la décision
se contredisent ici. Je n'ai pas tranché seul. **Deux sorties possibles :** teinter la dalle
de la page + avec la teinte CLAIRE de la nature (§1.2), ou choisir la dalle d'un monde
contrastant. **Ça se voit sur 8 des 17 cadres.**

#### Q37 · La carte « Une Nuée » du cadre 17 montre QUATRE dalles, le cadre en montre UNE
L'app peint la tuile Nuée avec la disposition à quatre dalles du bandeau de fiche
(décision du lot 3 : « la Nuée porte les dalles de ses Promi »). L'inventaire du cadre 17
ne liste **qu'une** DALLE de 120 × 96. J'ai gardé les quatre — elles disent « un groupe »,
et ce sont de vraies dalles du moteur. **À confirmer ou à ramener à une.**

#### Q38 · « DÉJÀ PROMIS » : deux pastilles au cadre, une seule dans l'app
Le cadre montre « nager le mardi » et « appeler Mamie » — deux titres courts. **Les mots
viennent des promesses réelles** (CLAUDE.md §9), et « le grand plongeoir » + « courir
dimanche » ne tiennent pas dans les 342 px. **La seconde est retirée quand elle
déborderait.** Le cadre en montre deux parce que les siens sont courts.

#### Q39 · Le clavier du cadre 19 n'est PAS dessiné, et c'est voulu
§2.11 : « représenté, pas conçu ». L'app ouvre le **vrai clavier système** ; le champ de
saisie garde le focus mais ne se peint plus — **la pastille EST le champ**, comme au cadre.
En capture Playwright il n'y a donc pas de clavier : ce n'est pas un manque.

---

### CE QUI RESTE SUR LA SECTION 3 — **5 écrans**
1. **Le Peaufiner de la page +** — *non commencé, et c'est le morceau à risque*. Le bloc de
   la section 2 a été bâti dans un cadre fixe ; la page + est une feuille qui défile. La
   parade `#tenirCv` est en place (aucun ancêtre positionné entre le geste et
   `#createSheet`) et doit le rester. **Attention aussi à `#csPeaufTail`** : j'ai mis sa
   hauteur à 0 sous `.pp:not(.pp-peauf)` parce qu'elle sortait du cadre — la cale devra
   reprendre sa hauteur le jour où Peaufiner défilera (le sélecteur est déjà prêt).
2. **`Le geste · au repos`** — Q35 (le lien qui change de mot).
3. **`Le geste · signé`** — Q36 (le mot d'échéance), à traiter avec la section 5.
4. **`Choix ouvert · l'échéance`** — Q34 (périmé par Q28).
5. **`Garder de côté`** — son inventaire est **mot pour mot celui de `Promi · à soi
   rempli`** (même base, même dalle, même mot de trace, même lien). Je ne le compte pas
   deux fois : si tu confirmes que c'est le même écran, la section est à 13 sur 17.

### CE QUI N'A PAS ÉTÉ COMMENCÉ
**Section 4 (Index et Fil — 6 écrans + 26 composants) et section 5 (L'instant — 6 écrans) :
rien. Pas une ligne.** La session a été employée entièrement à la section 3.


================================================================================
## SECTION 3 — LA PAGE + : **LIVRÉE. 16 écrans sur 16.**
================================================================================
Point de reprise `sauvegardes/s3-complete.html` · sauvegardes intermédiaires
`avant-S3-peaufiner-plus.html`, `s3-peaufiner-page-plus.html`, `avant-S3-choix-natures.html`.

**Les cinq lignes du critère :**

    position 0 · style 0 · collisions 0 · hors cadre 0 · présence peinte 0
    (juge `releve-S3-page-plus.py`, 28 cadres = 14 écrans × 2 thèmes)

    redteam_ecrans 144/144 · phrase 6/6 · verbe 6/6 · demande 19/19 · geste 13/13
    filets 0 parasite · redteam 15/15 · redteam2 10/10 · redteam3 18/18
    redteam_toile 16/16 · 16/16 · 15/16 → flake documenté, reconfirmé au vert
    SECTION 1 au vert · SECTION 2 à 0/0/0/0/0

**LE DÉCOMPTE FRANC — 16 sur 16.** L'écran de l'échéance est sorti du décompte (Q34), la
section compte donc 16 écrans et non 17. Les 16 sont mesurés **et** regardés en duo dans
les deux thèmes après le dernier changement qui les touche.

#### CE QUI A ÉTÉ FAIT DANS CE LOT
1. **LE PEAUFINER DE LA PAGE + — le morceau à risque, pris seul et en premier.**
   Le bloc de la section 2 est **porté, pas dupliqué** : ses briques (`reg`, `zone`,
   `bouton`, `tete`, `emprunte`/`rentre`) sont exposées par `window._s2Briques`, et son CSS
   est une **copie mécanique** au seul nom du porteur près (`#detailPoster` →
   `#createSheet.pp-peauf`). Les réglages tombent sur les cotes de la fiche au pixel :
   **110 · 190 · 270 · 350 (118) · 484 (92)**, barre clouée à 760, **pas d'icône Partager**.
   Test dédié `scratchpad/test_peauf_aller_retour.py` : **11/11** — ouverture par la barre,
   sept réglages, rien au-dessus de la barre, rien hors cadre, et surtout **tous les
   contrôles empruntés rentrent chez eux à la fermeture** (sinon le plantage ne les lit
   plus). `#csPeaufTail` reprend bien sa hauteur sous `.pp-peauf`.
   **Le piège qui a coûté deux passes :** mes règles de fermeture avaient EXACTEMENT la
   même spécificité que celles de la page + (2 id + 2 classes des deux côtés). Placé plus
   haut dans le fichier, le bloc ne fermait rien — `display:flex` sur un `.cs-mark` que la
   règle ciblait pourtant. **Il est désormais le dernier bloc du fichier**, et c'est écrit
   dans son entête.
2. **Q30 appliqué puis BORNÉ.** Ton sur ton mesuré avant : **16 en médiane** sur les huit
   cadres à champ bleu, seuil 42. Après remappage sur la rampe du §1.2 : **109**. La règle
   est ensuite bornée à la bande haute (voir Q30 bis ci-dessous).
3. **Q35 · un seul mot, jamais deux.** Le mot de trace dit « trace pour planter » (Promi)
   ou « trace pour lancer » (Chiche, Nuée), **partout, au repos**. L'app en portait deux
   pour la même chose. Il disparaît dès que le doigt trace.
4. **Q36 · aucun vocabulaire de saison.** « planté · à tenir avant l'été » n'existe plus :
   après signature le mot dit **« À TENIR · <jour> »**, **« UN JOUR »** ou **« EN L'AIR »**
   — l'échéance que l'app sait produire, lue sur sa prise, jamais un libellé.
5. **Le geste · signé** est porté (§2.6, « ma moitié donnée » : plein 0 → 195, le milieu
   exact, points au-delà). Vu au duo : **le ⇄ et « garder de côté » restaient affichés**
   alors que ni le cadre 29 ni le cadre 30 ne les portent — corrigé.
6. **Choix des trois natures** (cadre 17), le seul écran jamais porté : question à 24 / 96
   en Bricolage 700/46, trois cartes 358 × 174 à 246 · 436 · 626, dalle du moteur 120 × 96,
   « CHOISIR → » en pied. Ni trait, ni champ, ni barre.
7. **§2.8 remis à la règle** : `taille = min(estimation, mesure)`. Inscrit dans
   `PROMI-SPECIFICATIONS.md`. La « correction » qui remplaçait l'estimation par la mesure
   est annulée.
8. **Les deux pièges inscrits dans `CLAUDE.md` §8** : le crible en bloc, et la cote mesurée
   sur elle-même.

#### Q30 bis · LA TEINTURE EST BORNÉE — vérifié, pas seulement écrit
La règle telle que je l'avais écrite mangeait le §4. **Réécrite (décision Tom) :** la dalle
prend la palette de nature **dans la bande haute d'une fiche et de la page +, et nulle part
ailleurs**. Index, Fil, Toile, encart de Nuée : le monde, et rien d'autre.
**Vérifié par `scratchpad/probe_hors_bande.py` — 5/5 :** un seul site d'appel dans tout le
fichier, **0 teinture hors bande haute** en parcourant Toile · Index · Fil · Partage ·
Aura · Studio, et la teinture agit bien dans le champ de la page +. La comparaison pixel
avant/après ne prouvait rien (les dalles de la Toile sont animées et tirées au hasard) : le
contrôle instrumente l'appel lui-même.

#### Q37 · « planter au bouton » — DEUX MOTS POUR UN MÊME CRÉNEAU, non tranché
Le cadre 28 (« le geste · au repos ») écrit **« planter au bouton »** à 24 / 702 ; les huit
autres cadres au repos écrivent **« garder de côté »** à 24 / 708. **Or c'est le même état
d'app** — rien n'est tracé, la phrase est remplie : l'app ne peut pas distinguer les deux
écrans. Deux cadres se contredisent donc sur le même créneau.
**Option conservatrice prise, dans l'esprit de Q35 (un seul mot, jamais deux) :** le
créneau porte **« garder de côté »** partout. La bascule vers le bouton reste atteignable —
`redteam_verbe` le vérifie (6/6, « la bascule mène à un vrai bouton »). **À trancher :** si
« planter au bouton » doit exister, il lui faut son propre déclencheur, pas le même état.

#### Q38 · La taille de la phrase sur un choix ouvert — écart assumé de 2 px
Les trois cadres « Choix ouvert » composent la phrase à **28 · 30 · 30**, là où la règle du
§2.8 (départ 30 sur un choix ouvert, puis rétrécissement) donne **30** partout. L'écart ne
porte que sur « écrire un mot » : 30 au lieu de 28, soit ~5 px sur la deuxième ligne.
Aucune règle du document n'explique le 28. **Je garde la règle**, je ne code pas la valeur.

#### Q39 · Les dalles des trois cartes du cadre 17
Elles sont peintes par `renderTileIcons()` avec une teinte par nature — **c'est du code
d'origine, pas ma teinture** : la borne de Q30 n'est pas franchie. J'ai seulement remis les
teintes du §1.2 (le Chiche sortait en **rose `#FCA6B8`** là où sa palette est **pêche
`#FFC0A8`**, constaté au duo). Écart de luminosité sur le champ : 115, aucun ton sur ton.

#### Q40 · La coupure de la question du cadre 17
Le `<br>` posé dans le markup **ne tient pas** : un script de l'app le reprend à chaque
passe (mesuré — 0 `<br>` dans le DOM une seconde après l'avoir posé, la ligne se coupait
après « tu »). Je n'ai pas trouvé l'auteur en trois essais (piégeage d'`innerHTML`, de
`textContent`, de `removeChild`, `MutationObserver`). **Coupure obtenue par la largeur** :
le bloc reste à 342 (§5), la ligne de texte est bornée à 306 — largeur à laquelle
« Qu'est-ce que tu » (319 mesurés) ne tient plus. Le résultat est celui du cadre ; le moyen
n'est pas celui du document. À reprendre si l'auteur du retrait est identifié.


================================================================================
## SECTION 4 — INDEX ET FIL : **COMMENCÉE, RIEN DE PORTÉ.** Point de reprise ci-dessous.
================================================================================
`app.html` est à l'état livré de la section 3 (identique à `sauvegardes/s3-complete.html`).
**Aucune modification n'a été faite pour la section 4** — seul le repérage l'a été.

#### CE QUI EST ACQUIS ET NE SERA PAS À REFAIRE
1. **L'ORDRE RÉEL DES 102 CADRES DU MOODBOARD EST RELEVÉ** — outil
   `scratchpad/liste_cadres.py`, qui imprime le texte de chaque cadre avec son indice.
   **L'ordre du moodboard n'est PAS celui du document** : je l'avais déduit et je me suis
   trompé (96 est « l'autre moitié arrive », pas l'Index). Les indices justes, désormais
   dans `scratchpad/cadres_mb.py` :

       Index 2 par ligne   72 · 73        L'autre moitié arrive   96 · 97
       Index 3 par ligne   74 · 75        Le trait se referme     98 · 99
       Fil                 76 · 77        Juste après            100 · 101

   Les six cadres de la section 4 et les six de la section 5 sont **capturés** dans
   `scratchpad/mb/` (`ix_deux`, `ix_trois`, `fil`, `inst_arrive`, `inst_referme`,
   `inst_apres`, chacun en `_dark` et `_light`).
2. **`scratchpad/cap_s4.py`** existe (capture + relevé de l'Index et du Fil de l'app).

#### CE QUI BLOQUE, ET QU'IL FAUT RÉSOUDRE EN PREMIER
**Je n'arrive pas à ouvrir la vue Index dans une page Playwright.** Ni `setView('index')`
ni le clic sur le bouton « Index » de `#viewSwitch` ne basculent : après 2,6 s, `#toile`
occupe toujours `#stage` et c'est « Toile » qui porte `.on` (mesuré, deux fois). Le Fil non
plus (`#filBtn`). **Sans mise en scène, ni juge ni duo ne sont possibles** — c'est le
premier travail de la reprise, avant toute cote.

#### L'ÉCART DE STRUCTURE, VU ET NON TRAITÉ
Le moodboard fait de l'Index un **écran à lui** : entête « Index 12 » + ✕ FERMER à 24 / 40,
champ de recherche 270 × 56 à 24 / 108, bouton de tri 56 × 56 à 310 / 108, puis la grille
de cartes 165 × 198 à x = 24 et 201, première ligne à 196.
**L'app en fait une VUE** partagée avec la Toile : la topbar, le mot-marque, `#viewSwitch`
et le dock restent à l'écran (mesurés : topbar 0/54 390×110, dock 47/740 296×56).
Ce n'est pas un écart de cote, c'est un écart de structure — du même ordre que la refonte
de la fiche au lot 6. **À trancher avant de porter :** l'Index devient-il un écran plein
(avec son ✕ FERMER, sans topbar ni dock), comme le moodboard le montre ?
Je n'ai pas tranché : c'est un point de produit.

#### LE RESTE DE LA SECTION 4, non commencé
Les 26 composants isolés — 8 cartes d'Index (§3.9 : 173 × 208 à deux par ligne, 110 × 138 à
trois ; trait à `per = 1`, `amp = 13 × échelle`, points `r = 3,2` tous les 11) et 5 bandeaux
du Fil (§3.10 : 358 × 128, trait VERTICAL à `x = 0,34 × largeur`, trois boîtes de hauteur
fixe à 16 / 50 / 98). Ils reprennent la hauteur de trait des fiches — la section 1 expose
déjà les primitives (`window._onde`), il n'y aura rien à dupliquer.


================================================================================
## SECTION 4 — INDEX ET FIL : **LIVRÉE.** Juge à 0/0/0/0/0, neuf batteries au vert.
================================================================================
`sauvegardes/avant-S4-index-fil.html` = l'état d'entrée · `sauvegardes/s4-index-fil.html`
= l'état livré. Juge : `releve-S4-index-fil.py` (6 écrans × 2 thèmes).

#### LE BLOCAGE EST LEVÉ — ET IL N'EN ÉTAIT PAS UN
La passation disait « je n'arrive pas à ouvrir la vue Index ». **L'Index n'est pas une vue.**
C'est une **feuille** : `window.ouvrirIndex()` → `buildIndex()` puis `openSheet(#indexSheet)`
(l. 3032), et le code de l'app le dit en toutes lettres — *« le sélecteur revient sur Toile :
l'Index est une feuille, pas une vue »* (l. 3039). Mesurer `#stage` et le `.on` de
`#viewSwitch` ne pouvait donc RIEN montrer : `#toile` reste sous la feuille, par construction.
`#indexSheet` passe bien de `opacity 0 / y 816` à `opacity 1 / 13,28 · 364 × 787`.
Le Fil, lui, est une vue : `setView('fil')` → `#feedView.in`, `#stage` en `display:none`.
Instrumenté par `scratchpad/probe_ix.py`, 0 erreur JS.

#### CE QUI A ÉTÉ PORTÉ
1. **L'écran plein** (décision Tom). `.topbar`, `.footer` (le dock), `.statusbar` et
   `#viewSwitch` sortent tant que `#device.s4-plein`. Le crible est posé **nœud par nœud**,
   jamais sur un conteneur — la leçon du §8 de CLAUDE.md.
2. **L'entête, la recherche, le tri** aux cotes du §5 : bloc 24 / 40 × 44, « Index »
   Bricolage 700/38 (-.035em) + compte 700/26 en `#3A54FF` (`#2BE88C` pour le Fil),
   ✕ FERMER Apfel 500/12.5 à droite ; recherche 270 × 56 à 24 / 108, rayon 28, contour 3
   (`#5D636D` sombre, `#9A9384` clair) ; tri 56 × 56 à 310 / 108 ; grille à 196.
3. **La carte d'Index** (§3.9) : 165 × 198 rayon 17 à deux par ligne (x = 24 · 201,
   pas 210), 106 × 133 rayon 11 à trois (x = 24 · 142 · 260, pas 145).
4. **Le bandeau du Fil** (§3.10) : 358 × 128 rayon 22 à x = 16, pas 140 ; trait **vertical**
   à 0,34 × largeur ; trois boîtes fixes 16 / 50 / 98.

#### LA LOI DE LA CARTE, RETROUVÉE DANS LE MOODBOARD — pas déduite, LUE
Le document donne les cotes carte par carte mais jamais la règle qui les produit. Elle est
dans les chemins SVG du moodboard (cadres 72, 74, et les cartes isolées) :

    échelle   = hauteur de la carte / 600
    base      = hauteur de trait figée à la plantation × échelle
    amplitude = 13 × largeur / 173          (§3.9, « amp = 13 × échelle » : 173 = la carte isolée)
    boîte     = ⌊ base + amplitude + 20 ⌋
    épaisseur = 5,5 × l/173 · points r = 3,2 × l/173 tous les 11 × l/173 (§3.9)
    dalle     : y = 0,0455 h · h = base − amp − 13,7 h/198 · l = 1,2 h · CENTRÉE (§2.7)

**Vérifiée sur les trois tailles du document** : pour une base de fiche de 312, la boîte
retombe sur **135** (165 × 198), **97** (106 × 133) et **141** (173 × 208) — les trois
valeurs des tableaux, au pixel près. L'onde, l'amorce, le chevron et les points ne sont pas
réécrits : `window._onde`, exposé par la section 1, est appelé tel quel.

#### Q41 · LE MOODBOARD NE CENTRE PAS TOUJOURS SA DALLE — le §2.7 si
Sur les six cartes du cadre 72, **trois dalles sont centrées** (36, 58, 39 — exactement
`(165−l)/2`) et **trois ne le sont pas** (97, 9, 77 : collées à droite, à gauche, à droite).
Le §2.7 dit « **toujours centrée horizontalement** ». **J'applique le document, je centre.**
Si la variation est voulue (donner de la vie à une grille), il lui faut une règle — elle n'est
écrite nulle part.

#### Q42 · LES BASES DE FICHE DU MOODBOARD SORTENT DE L'ÉCHELLE DU §2.5 — bornées
`hauteur_trait` vaut, par le §2.5, `max(196, 344 − 32(n−1))` : elle vit dans **[196, 344]**.
Or les fiches du moodboard portent **376** (« Promi · tenue ») et **372** (« Chiche · tenu à
deux ») — des cotes d'écran, posées à la main sur 844 px. Reportées telles quelles sur une
carte de 133 px, elles laissaient **10 px** au titre : vu au duo, « méditer le… » coupé en
plein mot, l'état par-dessus. **Je borne donc la base de la carte à [196, 344]**, la règle du
§2.5 elle-même. Les bases que le moodboard emploie pour ses PROPRES cartes tiennent toutes
dans [204, 348] — la borne est celle qu'il applique déjà. **À trancher :** si 376 doit rester
la hauteur d'une fiche tenue, le §2.5 doit dire que ses bornes ne valent que pour la fiche.

#### Q43 · « AVEC +4 » N'A PAS DE VERSION SANS MEMBRE
Le moodboard écrit **« avec +4 »** en tête d'une carte de Nuée. Une Nuée **sans membre** —
l'app en a une, « Moi-même » — n'a aucun mot au moodboard. Je n'en invente pas : je reprends
celui que `buildIndex` écrit déjà (l. 3399), **« perso »**. À confirmer.

#### Q44 · « À TENIR · 2 J » — l'app ne sait pas produire le « · 2 J »
Le moodboard écrit **« À TENIR · 2 J »** et **« TENUE · IL Y A 2 H »**. L'app ne connaît que
`p.due` en jours et `motDuTemps()`, qui rend « à tenir », « demain », « aujourd'hui » — jamais
un compte de jours en capitales. **Option conservatrice :** la carte d'Index écrit **« À
TENIR »** seul (le mot de la fiche, donc la cohérence du §4) ; le bandeau du Fil, lui, ajoute
le temps **que l'app affiche déjà** dans `.fd-t` (« RÉCEMMENT »), ce qui donne « À TENIR ·
RÉCEMMENT ». Rien n'est inventé, mais le « 2 J » du moodboard n'existe pas.

#### Q45 · L'INDEX À TROIS PAR LIGNE N'A AUCUN DÉCLENCHEUR
Le moodboard donne DEUX densités (cadres 72/73 à deux par ligne, 74/75 à trois) et le
document leurs deux jeux de cotes — **mais aucun des deux ne dit ce qui fait passer de l'une
à l'autre** : ni bouton, ni seuil de compte, ni réglage. **J'ai porté les deux** — les cotes
des cadres 74/75 sont tenues, le juge les mesure — et la bascule vit dans `window._s4Trois`,
**qu'aucun doigt n'atteint**. Je n'ajoute pas un contrôle de produit. À trancher : qui
choisit la densité ?

#### Q46 · CINQ CONTRÔLES DE `redteam_ecrans` NOMMAIENT L'ANCIEN MARQUAGE
`.ix-bloc`, `.ix-bd canvas`, `.ix-bj`, `.fd-item` : la section 4 les remplace par `.s4-carte`.
La batterie est tombée à **134/144**, puis remontée à **144/144** en désignant les nouveaux
nœuds — **l'intention de chaque contrôle est inchangée**, seul le nom du nœud change.
Un seul a dû être réécrit sur le fond : « seuls les urgents ont un aplat » supposait que
l'état vivait dans le FOND du bloc (classe `.vif`). Sur la carte du moodboard, l'état vit
**dans la ligne** (§2.1 bis) et le fond reste l'un des trois corps du §1.3 ; le contrôle
vérifie donc désormais qu'**aucune carte n'est peinte d'une couleur d'état**.
La version d'origine est gardée : `sauvegardes/redteam_ecrans-avant-S4.py`.
`releve-design.py` visait lui aussi `.ix-bloc.vif/.menthe/.nuee` pour ouvrir ses fiches : la
carte porte désormais `data-nat` et `data-etat`, la même information, et l'outil les emploie.

#### CE QUE `releve-design.py` DIT — et pourquoi ce n'est pas la section 4
556 écarts **avant** la section 4, 556 **après** : **la comparaison ligne à ligne des deux
listes ne donne AUCUN écart nouveau.** La référence `design-reference.json` date d'avant les
sections 1 à 3, qui ont réécrit les fiches ; elle n'a jamais été refigée. **Elle ne juge plus
rien tant que Tom n'a pas validé et lancé `--figer`.**

#### LES CINQ LIGNES DU CRITÈRE — SECTION 4
    écarts de position > 3 px      0
    écarts de style                0
    collisions                     0
    débordements                   0
    présence peinte                0
    batteries                      144/144 · 15/15 · 10/10 · 18/18 · 19/19 · 16/16 · 13/13 · 6/6 · 0 filet


================================================================================
## SECTION 5 — L'INSTANT : **LIVRÉE.** Juge à 0/0/0/0/0, neuf batteries au vert.
================================================================================
`sauvegardes/s4-index-fil.html` = l'état d'entrée · `sauvegardes/s5-instant.html` = l'état
livré. Juge : `releve-S5-instant.py` (3 écrans × 2 thèmes + la séquence).

#### CE QUI A ÉTÉ PORTÉ — trois écrans, une seule fiche
Le moment où la seconde moitié se referme. `base = 300 · amplitude = 44 · boîte = 384` sur
les trois cadres, sans exception. Le trait n'est pas réécrit : `window._onde`, exposé par la
section 1, est appelé tel quel.

| | champ | ligne | dalle |
|---|---|---|---|
| **l'autre moitié arrive** (96/97) | NATURE | terracotta plein 0 → 195 + chevron · **menthe 195 → 268** (l'autre trace) · points terracotta dès 213 | 180 × 150 à 105 / 91 |
| **le trait se referme** (98/99) | **MENTHE PLEIN** | encre `#16171B` plein 0 → 390 | **228 × 190 à 81 / 88** |
| **juste après** (100/101) | NATURE | menthe plein 0 → 390 | 180 × 150 à 105 / 91 |

Les segments et les couleurs sont **relevés dans les chemins SVG du moodboard**, pas déduits.
Le champ menthe dure **une seconde**, puis revient à la nature (CLAUDE.md §3, règle 9 du §9
du moodboard). Le juge mesure la séquence : à 300 ms « referme », à 1,5 s « apres ».
**La dalle se recompose bien plus grande** : sonde pixel, 604 → **1013** pixels peints, sur
18 relevés (3 écrans × 2 thèmes × 3 essais), aucun vide.

#### Q47 · « L'AUTRE MOITIÉ ARRIVE » N'A AUCUN DÉCLENCHEUR OBSERVABLE
Le cadre 96 montre **la moitié de l'autre en train d'arriver** — menthe de 195 à **268**.
C'est un événement **en direct** : quelqu'un d'autre trace, maintenant. **L'app ne modélise
rien de tel** : elle connaît « relevé », « à tenir », « tenu », jamais « l'autre est en train
de tracer ». J'ai donc porté l'écran et sa position d'arrivée (`window._instantX`, 268 = la
valeur du cadre), **sans lui inventer de déclencheur**. À trancher : d'où vient ce signal ?

#### Q48 · LA LIGNE DE « LE TRAIT SE REFERME » EST À L'ENCRE, DANS LES DEUX THÈMES
Le cadre 98 (sombre) **et** le cadre 99 (clair) peignent la ligne en `#16171B` sur le champ
menthe. C'est la seule fois du produit où la ligne n'est ni d'état ni de nature : elle
redevient la frontière pure. Je l'ai porté tel quel — mais le §2.1 bis ne prévoit pas ce cas,
il faudrait qu'il le dise.

#### Q49 · « RACHEL VIENT DE TRACER SA MOITIÉ » — sans autre personne, il manque un mot
Le cadre 98 écrit « **Rachel vient de tracer sa moitié. Le dessin existe.** » Le prénom vient
du Promi. Sur une parole **à soi seul**, il n'y a personne à nommer et le moodboard n'a pas
de version. **Option conservatrice :** j'écris alors la seconde phrase seule, « **Le dessin
existe.** » — un mot du moodboard, jamais un mot inventé. À confirmer.

#### Q50 · LA DALLE DE L'INSTANT NE SUIT PAS LA FORMULE DU §2.7
Le §2.7 donne, pour `base = 300 · amp = 44` : hauteur `(300−44) − 88 − 12 = 156`, largeur
`1,2 × 156 = 187`, centrée en x = 101, y = 88. **Les cadres écrivent 180 × 150 à 105 / 91**
(et 228 × 190 à 81 / 88 quand la parole se tient). L'écart passe la tolérance de 3 px : j'ai
**posé les valeurs des cadres**, qui font foi, et non la formule. La formule reste juste
partout ailleurs — c'est l'instant qui déroge.

#### Q51 · COMBIEN DE TEMPS DURE « JUSTE APRÈS » ?
« Le trait se referme » dure **une seconde** — CLAUDE.md le dit. Pour « juste après », aucun
document ne donne de durée. **Option conservatrice :** il reste tant que la fiche est
ouverte, et disparaît à la fermeture. « À L'INSTANT » cesse donc d'être vrai si la fiche
reste ouverte longtemps. À trancher.

#### DEUX PIÈGES DE PLUS, VÉRIFIÉS ET INSCRITS
1. **Un `display` posé EN LIGNE par la section 1 bat un `!important` de feuille.** Le geste
   restait à l'écran sur les trois cadres, qui n'en portent aucun : `_ficheCotes` lui pose
   `display:block!important` **en ligne**. Une règle de feuille, même en `!important`, ne
   peut rien contre ça. **On le sort en JavaScript, pas en CSS.**
2. **L'encre du CORPS n'est pas celle du CHAMP.** Sur le champ plein, le mot-marque reste
   crème ; dans le corps — **crème en thème clair** — le titre doit passer à l'encre. Vu au
   duo : le titre « faire les crêpes » avait purement disparu du cadre 101 clair, crème sur
   crème. Le juge de présence peinte le rattrape désormais (Δ luminosité < 42).
3. **§4.5 rappelé** : une seule passe de peinture laissait la dalle vide par intermittence.
   On rejoue à 0, 60, 200 et 600 ms, comme `peintMinis`.

#### DEUX SONDES DE JUGE CORRIGÉES — des faux rouges, pas des régressions
· **La boîte du trait** se mesure dans le repère du cadre. La lire dans `style.height`
  mélangeait deux échelles (#device est mis à l'échelle par une transformation) : le juge
  sortait **412** sur un canevas de **384**.
· **La sonde de la ligne lit LE CENTRE du trait**, pas son voisinage. Chercher « le premier
  pixel menthe à ±9 px » rendait la sonde aveugle sur « le trait se referme » : là, TOUT le
  champ au-dessus de l'onde est menthe, et la ligne d'encre passait pour menthe.
· (section 4) **Le trait du Fil est VERTICAL** : le compter en colonnes le rendait invisible
  dès qu'une dalle était petite.

#### LES CINQ LIGNES DU CRITÈRE — SECTION 5
    écarts de position > 3 px      0
    écarts de style                0
    collisions                     0
    débordements                   0
    présence peinte                0
    batteries                      144/144 · 15/15 · 10/10 · 18/18 · 19/19 · 16/16 · 13/13 · 6/6 · 0 filet

`redteam_toile` a donné 15/16 puis 14/16 puis **16/16 · 16/16** : c'est le flake documenté
(« Mes Promi : les intitulés restent », sonde à seuil sur un canevas animé). Reconfirmé vert.
`releve-design.py` : **556 lignes avant la section 4, 556 après la section 5, aucune ligne
nouvelle** (comparaison ligne à ligne des deux relevés). Sa référence date d'avant les
sections 1 à 3 et n'a jamais été refigée — elle ne juge plus rien tant que Tom n'a pas
validé et lancé `--figer`.


#### Q52 · LE CRÉNEAU « QUAND » DE LA PHRASE — RÉSOLU, il ne doit pas exister
J'ai cherché un mot de liaison pour poser une échéance dans la phrase de la page +, et j'ai
noté l'absence comme une casse (CASSE A3). **C'est faux, et c'était déjà tranché : Q28.**
**L'échéance a QUITTÉ la phrase.** Elle vit dans **Peaufiner, en tête**. La phrase est à
**deux lignes — le verbe et l'objet**, rien de plus. Je cherchais un mot pour un créneau qui
ne doit pas exister. Le contrôle `redteam_champs` qui l'exigeait est retiré au niveau de la
décision ; à sa place, un contrôle qui vérifie que **l'échéance est atteignable dans
Peaufiner** — puisque c'est désormais le SEUL endroit où on la pose.

#### Q53 · LA PHOTO DE FICHE — ce que j'ai dû décider seul
La demande était complète sur presque tout. Trois points manquaient ; j'ai pris à chaque
fois **l'option la plus sobre**, comme demandé.

1. **Le voile de lisibilité : retiré.** J'en avais posé un sur la photo pour protéger le
   mot-marque et ✕ FERMER. Il dessinait une bande sombre à bord franc, visible et laide —
   et la photo « ne se superpose à rien ». Il était surtout **inutile** : la boîte de la
   dalle commence à **y = 88** (§2.7), l'entête vit à **y = 38** (§3.1). **La photo ne
   l'atteint jamais** : les deux mots restent posés sur l'aplat de nature. Mesuré, pas
   supposé — `redteam_photo.py` le vérifie sur une photo **très claire** et une **très
   sombre**, seuil 42, sur les deux natures.
2. **L'écart au trait : 52 px**, du haut du bouton à l'onde prise **au droit du bouton**
   (`y(349)`), pas à la base. Le trait ondule ; l'écart ne bouge pas. Aucune valeur n'était
   donnée : 52 place le bouton juste au-dessus de l'onde sans jamais toucher la dalle.
   Contrôlé : l'écart est identique quand la hauteur de trait change.
3. **Le retour à la dalle : le même bouton, une flèche de retour.** Il n'y a pas de mot —
   « ce bouton doit être invisible tant qu'on ne le cherche pas ». Un libellé aurait été un
   mot inventé.

**Ce que je n'ai pas fait :** la photo n'est pas encore rangée dans la Toile ni dans les
listes — une carte d'Index et un bandeau du Fil montrent toujours la dalle. Le §4 dit que
la dalle porte le monde ; **une photo n'est pas une dalle**, et rien ne dit ce que l'Index
doit montrer d'une promesse en photo. **À trancher.**

#### Q54 · LE BROUILLON N'OUVRE PAS SA FICHE — et c'est une DÉCISION, pas un bug
J'ai écrit dans `CASSE.md` que la fiche « Gardé de côté » du §5 était inatteignable par
défaut de code. **C'est faux.** Sentinelle posée sur les dix fonctions qu'`openDetail`
appelle : `renderDetail` n'apparaît jamais dans la pile, `closeAll` voit déjà `cur = NULL`,
et `openSheet` suit. La cause est à la **ligne 9415**, écrite au lot 17 :

> *« un brouillon n'ouvre PAS une fiche — il ROUVRE la page + dans son état, prêt à planter
> (le Brouillon est un état, pas une fiche figée) »*

**Le document et l'app se contredisent donc frontalement.** Le §5 décrit **trois écrans
« Gardé de côté »** — Promi, Chiche, Nuée — avec leurs cotes complètes (base 262, amp 44,
dalle 141 × 118 à 124/88, quatre blocs texte en `#3A54FF`, « GARDÉ DE CÔTÉ · 2 AVRIL »).
L'app, elle, a décidé qu'un brouillon se REPREND au lieu de se REGARDER.
**C'est un point de produit : je ne tranche pas.** À décider : le brouillon a-t-il une fiche
(et alors le lot 17 est à défaire), ou le §5 décrit-il trois écrans que le produit a
abandonnés (et alors ils sortent du document) ?

#### Q53 · TRANCHÉ ET POSÉ — la photo remplace la matière partout
« Une carte d'Index et un bandeau du Fil montrent la photo, pas la dalle. Sinon la promesse
aurait deux visages. » (Décision Tom.) Fait : même cadrage centré, mêmes cotes que la dalle
— boîte de la carte pour l'Index, `5 / 19 · 110 × 89` pour le bandeau. `redteam_photo.py`
le mesure sur les deux, **27/27**.

#### Q55 · DEUX MOTS REMPLACÉS — à valider
`CLAUDE.md §2` interdit désormais « brouillon » et « score » (décision Tom, 18 août 2026).
Balayage de treize écrans dans les deux thèmes : **deux mots interdits étaient à l'écran.**

| où | avant | après | pourquoi ce mot |
|---|---|---|---|
| tri de l'Index et du Fil | **Brouillons** | **Gardés de côté** | le mot du produit, déjà employé sur la fiche (`Gardé de côté`) et sur la carte d'Index (`GARDÉ DE CÔTÉ`) — rien d'inventé |
| action d'une fiche | **Brouillon** | **Garder de côté** | l'action, à l'infinitif, comme « planter », « lancer », « tenir » |
| aide de l'Aura | **Le Noyau & le score** | **Le Noyau & l'Aura** | « Aura » est le nom du produit pour l'écran de progression (`CLAUDE.md §2`) |

**Les deux premiers ne sont pas des choix : ce sont les mots que le produit emploie déjà
ailleurs.** Le troisième est **à valider** : « Aura » est le mot juste pour la chose, mais
le titre parlait d'un *chiffre*, et l'Aura est un *écran*. Si un autre mot désigne le
pourcentage de parole tenue, il vaut mieux que le mien.
La clé de tri `data-s="brouillon"` n'est pas renommée : c'est une liaison interne, la
renommer casserait le tri sans rien changer à l'écran.

#### Q56 · LE MENU DE TRI NE COUVRE RIEN — c'était mon contrôle
J'avais écrit que le menu de tri de l'Index couvrait 844 px et se posait sur les cartes.
**Faux.** `#ixMenu` est le **voile** plein écran, transparent (`rgba(0,0,0,0)`) ; le
**panneau** est `.ix-menu-p` — **346 × 604, fond opaque**, bien placé. Mon contrôle mesurait
le voile. Corrigé : il mesure le panneau, et vérifie en plus qu'il est opaque.

#### Q54 · RÉSOLU (Tom, 19 août 2026) — un gardé de côté SE REPREND, il ne se regarde pas
Toucher un gardé de côté **rouvre la page + dans son état**, prêt à planter : c'est le
comportement voulu, celui du lot 17 (l. 9415). **Les trois écrans « Gardé de côté » du §5
décrivent la page +, pas une fiche.** Il n'y a donc rien à réparer, et `openDetail` a raison
de ne pas ouvrir de poster. Clos, ne pas y revenir.

#### Q55 · « Le Noyau & l'Aura » — VALIDÉ (Tom, 19 août 2026)
Le titre parlait d'un chiffre ; l'Aura est l'écran. Le mot est bon.

---

## 19 août 2026 — LA MATIÈRE REMPLIT LE CHAMP (décision Tom) : ce que ça a ouvert

#### Q57 · Une fiche À PHOTO garde la boîte de sa dalle — à confirmer
La décision du 19 août dit : *la matière — dalles ou Toile — remplit tout le champ, du haut
de l'écran jusqu'à la vague*. Elle nomme **les dalles et la Toile**. Elle ne nomme pas **la
photo**, qui est pourtant l'autre matière possible d'une fiche.

**Option prise, la plus sobre : la photo garde sa boîte.** Deux raisons, toutes deux écrites :
la photo « **remplace** la matière » (`redteam_photo`, 27/27, elle occupe la boîte de la
dalle) et elle **ne doit pas atteindre l'entête** — c'est le Q53, arbitré : *« la boîte de la
dalle commence à y = 88 et l'entête vit à y = 38 : la photo ne l'atteint jamais »*, ce qui
avait permis de **retirer le voile** posé sur l'entête. En couverture plein champ, la photo
remonterait à y = 0 et il faudrait ré-arbitrer l'entête sur une image quelconque.

**Conséquence assumée :** sur une fiche à photo, la matière s'arrête à mi-hauteur — ce que la
décision interdit ailleurs. **Si Tom veut la photo plein champ aussi, il faut trancher le
traitement de l'entête sur photo** (le §10.6 généralisé y répondrait peut-être : l'encre suit
ce qui est peint dessous). Non tranché seul.

Même choix, même raison, pour le **gardé de côté** : il n'a **pas de champ** (`e.aplat` est
faux — rien n'est promis, le cadre 27 montre la dalle et les points posés sur le corps nu).
Il n'y a donc rien à remplir ; sa dalle garde sa boîte.

#### Q58 · L'INSTANT ne remplit pas son champ — essayé, mesuré, écarté
La décision nomme **les fiches, la page + et la Nuée**. L'instant n'y est pas, et il ne
pouvait pas y être : c'est **la seule exception du produit**, celle où **la couleur du champ
EST le sujet** — « le champ entier passe au menthe une seconde, la dalle se recompose plus
grande, le mot tombe » (§6 du moodboard).

**Essayé quand même**, en gardant la recomposition (facteur 228/180 sur la couverture).
**Mesuré :** la matière recouvre jusqu'au pourtour du cadre et **le menthe disparaît** — le
juge de la section 5 relève `rgb(192,182,244)` au lieu du menthe, dans les deux thèmes. Le
cadre 98 n'existe plus. **Écarté.** L'instant garde ses trois boîtes d'inventaire.

#### Q59 · LE MOT-MARQUE A DEUX ENCRES — le §10.6 généralisé
Depuis que la matière remplit le champ, **n'importe quel monde clair peut passer sous
« Promi » / « Chiche » / « Nuée » et sous « ✕ FERMER »**. Mesuré avant correction :
`cs-mark « Chiche » : ton sur ton (Δ25)` sur la page +, et le mot-marque crème posé sur une
dalle lilas sur la fiche.

**Rien n'a été inventé : la règle existait.** §10.6 de `PROMI-SPECIFICATIONS.md`, écrit pour
la Toile vide d'une Nuée : *« la Toile vide étant crème dans les deux thèmes, le mot “Nuée”
et “✕ FERMER” passent à l'encre `#16171B` — sinon c'est blanc sur blanc. Dès qu'un Promi est
planté, le champ redevient mauve et ils repassent en crème. »* Le cas n'est plus propre à la
Nuée : **on l'a généralisé.** L'entête lit le pixel réellement peint sous lui et prend, des
**deux** encres du produit, celle qui s'en écarte le plus. **Jamais un troisième ton.**
Une seule construction : `window._enteteLisible`, appelée par la fiche et par la page +.

**À valider :** que le mot-marque change d'encre selon la dalle est un comportement visible.
Il est juste, il est écrit, mais il n'a jamais été vu sur une planche.

#### Q60 · Q30 s'applique à la bande haute d'une FICHE — elle ne l'appliquait pas
`CLAUDE.md §4 · Q30` dit : *« dans la bande haute d'une fiche **et** dans le champ de la
page +, et NULLE PART AILLEURS, la dalle prend la palette de sa nature »*. **La page + le
faisait ; la fiche, non** — son code portait encore « NON TEINTÉE : elle porte le monde,
jamais la nature », qui est la règle générale du §4, celle que Q30 excepte précisément là.

Tant que la dalle tenait dans une petite boîte au milieu du champ, l'écart ne se voyait
guère. **Depuis qu'elle remplit le champ, une dalle bleue occupe tout un champ framboise** —
« une dalle bleue sur un champ bleu est un bug, pas un parti pris ». La teinture est donc
appliquée, par **le même appel que la page +** (`window._ppTeinteDalle`) : un seul site de
teinture dans le produit. **La forme ne bouge pas** — c'est toujours la vraie dalle du
moteur ; seule la luminosité est remappée sur les trois teintes du §1.2.

Ce n'est pas une décision nouvelle : c'est **Q30 appliquée là où elle le dit**. Mesuré :
sans elle, `redteam_tonsurton` sortait un rouge par passage, sur un état de fiche qui
changeait à chaque tirage de dalle.

#### Q61 · « + Planter un Promi » n'est PAS dans l'inventaire de la fiche de Nuée
C'est le dernier rouge de `redteam_aveugle` (24/26), et **ce n'est pas une cote qui manque**.

Le bouton `#nfAdd` — « + Planter un Promi » — est peint **sur la fiche de Nuée au repos**,
à y = 776. La barre Peaufiner est à y = 760 : il passe donc **dessous**, et c'est ce que le
contrôle de superposition relève. C'est le même bouton que Tom signalait « à y = 0,
par-dessus ✕ FERMER » (il s'appelait `#nqAddPromi`) : il n'a jamais eu de place.

**La raison est qu'il n'en a pas.** Cherché dans les vingt écrans du §12 (`PROMI-SPECIFICATIONS.md`,
partie II) : **aucune ligne « Planter »**. Cherché dans `promi-nuee-toile.html` : **zéro
occurrence**. Il n'apparaît qu'au **cadre 86/87 du moodboard** — *« Planter un Promi dans la
Nuée · DISSOUDRE LA NUÉE → Peaufiner ▴ »* : **c'est un contrôle du Peaufiner ouvert**, pas un
élément de la fiche au repos.

**Ce qu'il faudrait faire :** le déplacer dans le panneau Peaufiner de la Nuée, avec
« DISSOUDRE LA NUÉE ». **Non fait, et pas de mon fait :** le retirer de la fiche sans l'avoir
posé ailleurs supprimerait la seule façon de planter dans une Nuée depuis sa fiche — c'est
une FONCTION, et `CLAUDE.md §9` interdit de la faire disparaître au passage. C'est un lot à
part, avec son avant/après : **le Peaufiner de la Nuée** (cadres 84 à 87).

En attendant, **le bouton reste**, et le contrôle reste rouge — avec sa raison écrite.

---

## 19 août 2026 (soir) — LE VIDE EST UN DÉFAUT DU PLANCHER (consigne corrigée par Tom)

#### Q57 et Q58 · CLOS (Tom, 19 août 2026)
Les trois exclusions sont validées : l'instant garde ses trois boîtes, un gardé de côté n'a
pas d'aplat, une fiche à photo garde la photo sous l'entête. Ne pas y revenir.

#### Q62 · LA TOILE D'UNE NUÉE SUIT LA RÈGLE DU MOTEUR, PLUS TROIS EMPLACEMENTS FIGÉS
**Ce que le code portait :** trois emplacements en dur —
`[[30,96,108,86],[150,88,118,94],[278,100,92,74]]` — relevés sur le cadre 58, à une base de
232/282. Ils ne dépendaient **ni du nombre d'éléments ni de la hauteur du champ**.

**Pourquoi ils ne pouvaient plus tenir.** Depuis que la base suit le §9, la boîte du champ va
de **540 à 256**. Les deux façons de garder ces trois valeurs ont été essayées **et
mesurées** :

| essai | résultat mesuré |
|---|---|
| les laisser en **absolu** | vide de **155 px** à n = 1, **69 px** à n = 2 |
| les mettre à l'échelle **d'un facteur unique** | à n = 1, le facteur est 3,7 : les cases extérieures partent **hors cadre** — **125 abscisses sur 125 sans la moindre matière** |

**Ce qui les remplace, et d'où ça vient.** Le §11 donne la formule du générateur —
*« la densité est constante, c'est LA VUE qui zoome »*, `sp = √(W·H / n)` — et le §10.6 dit
que **le semis ne compte pas les Promi** : *« douze graines : c'est une densité de semis, pas
un plafond […] il ne préjuge de rien, et surtout pas du nombre de Promi »*. Douze graines sur
le champ d'une Nuée vide (390 × 435) donnent un pas naturel de **119 px**. On sème à cette
densité, jamais moins d'une graine par Promi, et **les dalles de la Nuée tournent sur les
emplacements**. Les formes restent celles du moteur (`Toile.dalleTrame`, échelle 1) ; le
décalage de chaque dalle est tiré de **son id**, jamais d'un hasard — deux rendus de la même
Nuée sont identiques.

**Pourquoi pas `sp = √(W·H/n)` seul :** le `n` du §11 est le nombre de **graines**, pas le
nombre de **Promi**. Pris pour le second, il donne **une** graine à 1 Promi — une dalle
étirée sur 390 × 392, cinq fois sa taille native, dont la matière part en bouillie. Vu au duo
contre le **cadre 2** de la planche, qui montre au contraire un braille **net** sur tout le
champ. La densité du §10.6 ramène l'agrandissement à **2,2**.

**Mesuré après (`scratchpad/mesure_vide.py`, deux thèmes, n = 1, 2, 3, 4, 5, 7) :**
**zéro abscisse sans matière, médiane du vide 0, aucun bandeau de plus de 24 px.**

**Ce qui est mon choix et pas celui du document :** le **recouvrement de 1,35** entre cases
(pour que les dalles se touchent — §10.5, « les mondes se rencontrent en s'effilochant ») et
le **décalage de 34 %** tiré de l'id. Le document donne la densité, pas la dispersion.
**À valider.**

**Ce qui manque encore :** le semis de la **Nuée vide** (§10.6 — douze graines crème `GLIGHT`,
mot-marque à l'encre) n'est pas porté : à n = 0 le champ reste mauve nu.

#### Q63 · UNE DALLE SE REND UNE FOIS, PAS UNE FOIS PAR CASE
`Toile.dalleTrame` refait l'attribution pondérée **pixel par pixel**. L'appeler pour chacune
des neuf à douze cases, à chaque repeinte, `_ficheNuee` étant rejoué deux fois par pose, a
fait ramer l'app au point que **`redteam_toile` ne rendait plus la main — dix minutes, deux
fois de suite**. Un cache par id, le temps de la passe, l'a rendue instantanée. C'est
exactement le piège du §12 de `CLAUDE.md` ; il vaut pour tout rendu en grille.

---

## 19 août 2026 (nuit) — LA FICHE DE NUÉE PORTÉE

#### Q61 · CLOS — « + Planter un Promi » a maintenant sa place
Le Peaufiner d'une Nuée est porté (cadres 84 à 87). Le bouton y vit, comme le moodboard le
veut. **Rien n'a été retiré du produit** : on plante toujours dans une Nuée, par le
Peaufiner. Les deux boutons de l'app — `#nqAddPromi` (balisage d'origine, l. ~2622) et
`#nfAdd` (bâti par l'entête du fil) — sont ramenés à **un seul**, celui du panneau ; l'autre
est masqué. C'était le dernier rouge de `redteam_aveugle`, qui passe à **26/26**.

#### Q64 · Le §12 écrit « amplitude = 40 » sur l'écran défilé — c'est le §9 qui a raison
L'entête des deux écrans « Le fil, après défilement » annonce `base = 58, amplitude = 40`.
**Le tableau du même écran donne la Toile à 114 px.** Or `58 + 16 + 40 = 114`, quand
`58 + 40 + 40` ferait 138. Le §9 dit « **base 58, amplitude 16** » et « le champ s'y réduit
à une bande de 114 px » : il est cohérent avec le tableau, l'entête est un report du gabarit
des autres écrans. **Porté à 16.** Le juge exclut cet état du contrôle de la formule, comme
le §9 l'exige expressément.

#### Q65 · Les cadres 84 et 86 sont deux PAGES — l'app les montre d'un seul tenant
Le cadre 84 porte l'entête et quatre cartes (DESCRIPTION 110, MEMBRES 230, PIÈCES JOINTES
310, COMMENTAIRES 418). Le cadre 86 n'a **pas d'entête** et pose « Planter » à 46 et
« DISSOUDRE » à 124. **Le document ne dit pas comment on passe de l'un à l'autre**, ni quel
écart sépare COMMENTAIRES de « Planter ».

**Option prise, la plus sobre : un seul écran, six blocs.** L'écart vient du **rythme du
cadre 86 lui-même** — 62 de haut + 16 = 78 —, d'où Planter à **538** et DISSOUDRE à **616**.
Le juge contrôle donc les quatre blocs du cadre 84 à leur y **absolu**, et les deux du cadre
86 par leur x, leur taille et **leur écart** (124 − 46 = 78), qui est ce que la planche dit
d'eux sans dépendre de la page. **À valider :** si les deux cadres sont deux pages qu'un
geste sépare, il manque ce geste.

**Une valeur étrange, suivie telle quelle :** le bouton « Planter » du cadre 86 fait
**348 × 68 hors tout**, pas 342 × 62 — son bloc porte `width:342 + border:3` **sans**
`box-sizing:border-box`, que les cartes ont. Il est donc 6 px plus large que DISSOUDRE dans
la planche. Le §8 bis dit qu'une valeur étrange l'est pour une raison : je ne l'ai pas
arrondie.

#### Q66 · Le crible de la SECTION 2 mord sur la fiche de Nuée
À l'ouverture du panneau, le poster prend `s2-ouv` — le crible du Peaufiner d'une
**promesse**, qui passe en `visibility:hidden` tout ce que son inventaire ne liste pas. Les
cartes d'une Nuée n'y sont pas : mesurées à `display:block` **et** « masqué » sur les quatre
écrans. **On n'a pas touché au crible** (il protège la section 2) : les six nœuds de la Nuée
sont déclarés visibles, **nommément**. C'est le §8 de `CLAUDE.md` — un crible se pose nœud
par nœud, et se lève de même.

#### Q67 · La bande violette d'une fiche de Nuée était figée à 232,67 px
`.device #detailPoster.dp-nuee::before` la clouait à une valeur d'un lot **antérieur au
moteur géométrique**. Invisible tant que la boîte du champ valait 256 ou plus ; **à l'état
défilé la boîte tombe à 114** et la bande dépassait de 118 px, en un rectangle mauve à bord
franc sous la vague — absent de l'inventaire, dont le fond est `#1A1230` uni. **Elle n'a pas
été supprimée** (elle est le fond sur lequel le canevas se pose) : elle **suit la boîte**,
ce qu'elle aurait toujours dû faire. Variable `--nuee-bande`, bloc `lot-NUEE-BANDE`.

---

## 19 août 2026 (fin) — LES POLICES, ET LE DERNIER PASSAGE À L'ŒIL

#### Q64 · CLOS — le §12 est corrigé
Les deux entêtes « Le fil, après défilement » annonçaient `amplitude = 40` ; leur propre
tableau donne la Toile à **114 px**, et `58 + 16 + 40 = 114`. **Corrigées à 16** dans
`PROMI-SPECIFICATIONS.md`, avec la note de correction au §9. Validé par Tom.

#### Q65 · CLOS — les deux pages, et le geste qui manquait
Le défilement est porté, **comme sur les autres Peaufiner** : `.dpd-corps` devient un
défileur plein cadre **0 → 760**, la barre reste clouée à 760, et le contenu fait **deux
pages de 760**. Au repos c'est le cadre 84 (entête 36, cartes 110 · 230 · 310 · 418) ;
descendu de 760, c'est le cadre 86 (Planter 46, DISSOUDRE 124) — **aux cotes absolues de la
planche, mesuré**. Rien ne monte, rien ne recouvre : le défileur s'arrête où la barre commence.
L'entête vit **dans** le défileur, ce qui est exactement pourquoi le cadre 86 n'en a pas.

#### Q68 · « APFEL 500 » N'EXISTE PAS — les juges S4 et S5 l'exigeaient
L'inventaire écrit « Apfel 500 / 12.5 » pour ✕ FERMER et pour la ligne d'état. **Cette face
n'est pas embarquée.** Les six seules le sont : Fraunces 600 (normal et italique),
Bricolage 600, Bricolage 700, Apfel 400, ApfelMid 500. **La graisse 500 existe bel et bien —
dans ApfelMid**, la famille qui la porte. Le lot reporte donc `Apfel 500` sur
`ApfelMid 500`, et les deux juges attendent désormais ce couple. Ni le seuil ni la taille ne
bougent : seul le nom de la famille qui porte la graisse change.
**À noter pour le document :** le §5 et le §12 écrivent « Apfel 500 » à plusieurs endroits.
Ce n'est pas faux au sens du dessin — c'est la graisse voulue — mais **c'est faux au sens
du portage** : en Swift, `Apfel 500` n'existe pas. À trancher : faut-il réécrire ces cellules
en « ApfelMid 500 » dans la spécification, ou garder « Apfel 500 » comme intention de
dessin avec la table de report en regard ? **Non tranché seul.**

#### Q69 · « TENUE À DEUX » sur une promesse à soi — vu à l'œil, pas par un chiffre
Le passage d'usage l'a montré : un Promi « à moi », **un seul Noyau à l'écran**, et la ligne
d'état annonçait « TENUE À DEUX · À L'INSTANT ». Les mots viennent du **cadre 101**, qui
montre une parole tenue **avec quelqu'un** — c'est son cas, pas une formule.
**Corrigé sans rien inventer :** quand la promesse est à soi, on écrit le mot que l'app
emploie déjà pour cet état (`STLAB.tenu`), et rien de plus — on retire celui qui ne
s'applique pas. « TENUE · À L'INSTANT ». Aucun juge ne l'avait vu : les cinq lignes du
critère mesurent la cote, le style et la peinture, **pas le sens du mot**.

#### Q70 · Le report de polices est une couche d'exécution, pas une correction de source
`redteam_polices.py` passe à **0 couple absent** parce qu'une passe JavaScript ramène chaque
élément sur sa face. **Le CSS, lui, demande toujours des faces qui n'existent pas.** C'est
assumé et c'est écrit dans le bloc `lot-POLICES` : le couple dépend de DEUX déclarations —
famille et graisse — qui vivent rarement dans la même règle, et le §9 de `CLAUDE.md` interdit
de nettoyer le CSS (cinq tentatives, cinq échecs). **Pour le portage Swift, la table de report
du bloc fait foi** ; si un jour le CSS est repris, elle dit quoi écrire.

---

## 20 août 2026 — LA CONFORMITÉ DE FORME (chantier ouvert)

#### Q71 · ★ OÙ SONT LES TITRES DE NATURE ? — je ne les trouve pas dans les cadres
Tom : *« Les titres de nature manquent partout — Promi, Chiche, Nuée, gardé de côté. Ni dans
l'Index, ni dans le Fil. »*

**Cherché, texte par texte, avec cotes et couleurs** (`scratchpad/extrait_textes.py`, cadres
72 et 76). Voici TOUT ce que les deux cadres écrivent :

| cadre 72 · Index | cadre 76 · Fil |
|---|---|
| « Index » · « 12 » · « ✕ FERMER » · « ⌕ Rechercher » · « ⇅ » | « Fil » · « 4 » · « ✕ FERMER » · « ⌕ Rechercher » · « ⇅ » |
| « à moi » · « à Rachel » · « avec +4 » · « à Marion » | « Marion te lance un chiche » · « à moi » · « Adrien a planté » · « à Rachel » · « Marion a relevé » |
| « TENUE » · « À TENIR · 2 J » · « 6 PROMI · 1 TENU » · « LANCÉ » · « EN COURS » · « TENU À DEUX » | « À RELEVER » · « TENUE · IL Y A 2 H » · « LE POTAGER · 6 PROMI » · « À TENIR · 2 J » · « RELEVÉ · À TENIR À DEUX » |

**Aucun « Promi », aucun « Chiche », aucune « Nuée », aucun « gardé de côté ».** Dans ces
deux cadres, la nature se lit à **la couleur du champ** (bleu · framboise · mauve) et à
**celle de l'accent**, pas à un mot. C'est d'ailleurs la règle du §4 de `CLAUDE.md` —
« la dalle porte le monde, l'accent porte la nature ».

**Je n'invente pas un libellé** (§9 : inventer un mot est la faute la plus grave).
**Question :** dans quels cadres ces titres apparaissent-ils ? Si c'est ailleurs que 72/76,
je les porte tout de suite. Si c'est une décision de produit — ajouter le mot de la nature
là où le moodboard ne le met pas — il faut la poser, car elle contredit les cadres.

**Ce que j'ai corrigé en attendant, parce que c'est sourcé :** dans le fil d'une Nuée, un
Chiche sortait « en cours » — le mot d'un Promi. Il porte désormais **CHICHE LANCÉ** /
**CHICHE RELEVÉ**, les mots du cadre défilé de `promi-nuee-toile.html`.

#### Q72 · Le compte des Chiche — vérifié, ce n'était pas là le défaut
Mesuré : on met un vrai Chiche dans une Nuée, **le compte passe de 3 à 4**, sur la fiche
comme sur la carte d'Index. `promisDeNuee` filtre `!draft && nuee===k` — les Chiche y sont.
Ce qui manquait, c'était **le mot de la ligne**, pas le compte (Q71).
⚠ **Non mesurés :** l'Aura, le Noyau, les légendes. À faire.

#### Q73 · « Zéro écart au pixel » ne peut pas se mesurer sur des données différentes
`scratchpad/duo_pixel.py` superpose la planche et l'app. Le Fil sort à **48 %** de pixels
différents — et **corriger la forme ne fera pas baisser ce chiffre**, parce que la planche
montre **ses** données (4 entrées, « le grand plongeoir », ses mondes) et l'app **les
siennes** (12 entrées, d'autres titres, d'autres mondes, plus une rangée « TENIR ·
REPORTER » que la planche n'a pas).

**Ce qui converge et se mesure, c'est la géométrie** : chemins, cotes, épaisseurs, mots.
**Pour un vrai zéro il faut mettre l'app dans les données de la planche** — un jeu de
démonstration qui reprend les Promi du moodboard. **Non fait**, et c'est la première chose
à faire au tour suivant. À valider.

---

## 20 août 2026 (soir) — LE JEU DE LA PLANCHE, ET CE QUE « ZÉRO » PEUT VOULOIR DIRE

#### Q74 · ★ LA MATIÈRE D'UNE TOILE NE PEUT PAS COÏNCIDER AU PIXEL
Le jeu de démonstration de la planche est en place, et le comparateur descend là où les
données convergent : `fiche-tenue` de **30,4 % à 13,8 %**, `fil` de **48,4 % à 38,4 %**.

**Mais il ne descendra pas à zéro, et ce n'est pas une question de dessin.** Les dalles de
l'app **sortent du moteur** — graines, poids, monde tiré au Studio — et respirent avec
`performance.now()`. Celles de la planche sont **des courbes dessinées à la main**, cadre
par cadre. Sur une fiche de Nuée, le champ occupe les deux tiers de l'écran : la mesure y
donne **87 à 100 % de pixels différents**, et aucune correction de forme n'y changera rien.
Reproduire la matière de la planche voudrait dire **abandonner le moteur** — ce que le §9
interdit formellement (« ne jamais toucher au code de la Toile », « les formes viennent du
moteur »).

**Ce qui peut atteindre zéro, et se vérifier :** la **géométrie** (chemins, cotes,
épaisseurs), les **mots**, les **couleurs**. C'est ce que mesure `redteam_formes.py`, écrit
aujourd'hui : il compare la courbe peinte à la loi extraite du cadre, à 1,5 px près.

**Question :** « zéro écart sur tous les écrans » doit-il s'entendre comme **zéro sur la
géométrie, les mots et les couleurs — la matière exceptée** ? Si oui, je continue sur cette
cible, qui est atteignable et contrôlable. Sinon, il faut trancher ce qu'on abandonne :
le moteur de la Toile, ou la conformité au pixel du champ.

#### Q75 · Trois batteries encodent l'ANCIEN jeu de démonstration
Le nouveau jeu rougit trois contrats, et **aucun n'est une régression de dessin** :

| batterie | ce qui échoue | ce qu'il décrit |
|---|---|---|
| `redteam_ecrans` 143/144 | « Toile : hit() ignore les cellules grises » | 14 promesses au lieu de 23 : la Toile a des cellules grises là où le contrôle n'en attendait pas |
| `redteam_fonctions` 17/19 | « TENIR depuis le Fil » · « un bandeau ouvre sa fiche » | le Fil comptait 12 événements de l'app ; il en a 5, ceux du cadre 76 |
| `redteam_aveugle` 24/26 | « Nuée · rien ne se superpose » | la Nuée du jeu a 6 Promi au lieu de 3 |

C'est le §7 de `CLAUDE.md` — **un contrôle qui encode un état qu'une décision a remplacé se
met à jour au niveau de la décision**, jamais en revenant en arrière. **Non fait, faute de
marge.** À faire en premier au prochain tour, avant toute autre correction.

⚠ **Un conflit à trancher au passage :** `redteam_fonctions` exige que « TENIR » soit
atteignable depuis le Fil. **Le cadre 76 ne porte aucune rangée « TENIR · REPORTER »** —
ses cartes sont nues. Le moodboard et l'inventaire des fonctions se contredisent ici.

---

### ✔ Q74 · TRANCHÉ (Tom, 20 août 2026)

> « **Zéro écart** veut dire zéro sur la géométrie, les mots, les couleurs et les formes.
> **La matière est exceptée.** Une Toile est engendrée par le moteur, la planche l'a tracée
> à la main : elles ne peuvent pas coïncider, et on n'abandonne pas le moteur. **Le
> comparateur doit exclure la zone de matière et mesurer tout le reste.** »

Écrit comme règle dans **`CLAUDE.md` § 8 bis · « CE QUE ZÉRO ÉCART VEUT DIRE »**, avec ses
trois garde-fous : le masque se **déclare et se mesure**, l'exception ne vaut **que** pour le
comparateur pixel (la boîte, la place, la couleur de champ et l'échelle d'une dalle restent
mesurées), et un écran qui n'atteint pas zéro hors matière se **dit**, avec sa raison mesurée.
`scratchpad/duo_pixel.py` porte le masque et publie sa surface.

### ✔ Q75 · TRANCHÉ (Tom, 20 août 2026)

> « Le cadre 76 ne porte pas de rangée TENIR · REPORTER, **mais la fonction reste**. On ne
> perd pas la seule façon de tenir une parole sans ouvrir une fiche. Le moodboard montre un
> bandeau **au repos** ; **le geste apparaît au besoin**. Note-le comme **ajout validé, hors
> inventaire**. »

Écrit comme règle dans **`CLAUDE.md` § 5 · « UN AJOUT VALIDÉ, HORS INVENTAIRE »** — les
quatre points qu'un tel ajout doit tenir. Appliqué au Fil : bandeau au repos identique au
cadre (358 × 128, pas de 140), **appui maintenu** pour déplier la rangée, toucher bref pour
ouvrir la fiche.

⚠ **UNE DES TROIS ROUGES N'ÉTAIT PAS UN CONTRAT PÉRIMÉ — le diagnostic de Q75 était faux
sur ce point.** « `redteam_aveugle` · Nuée · rien ne se superpose » n'échouait **pas** parce
que la Nuée du jeu a 6 Promi au lieu de 3. Mesuré : après avoir ouvert une **fiche de Promi**,
puis une **Nuée**, le bloc **hérité `#dpNuee`** (390 × 1039) redevient visible au-dessus de
`#dpMain` et **jette la barre Peaufiner à y = 0**, par-dessus « ✕ FERMER ». Cause : la CSS
l. 10415 `#detailPoster:not(.dp-nuee) #dpNuee{display:none!important}` est **antérieure au
portage** ; `renderNueeDetail` pose `dp-nuee` **et** `dp-mode-nuee`, et `renderDetail` ne
retire `dp-nuee` que sur le chemin d'un Promi. Au premier passage l'écran est juste ; dès
qu'une fiche a été ouverte avant, il ne l'est plus. **C'était une régression, elle est
corrigée** — voir `ETAT-DES-LIEUX.md`.


---

## 20 août 2026 (nuit) — L'INDEX PORTÉ, ET DEUX EXCEPTIONS MESURÉES

#### ✔ Q76 · TRANCHÉ (Tom) · L'ORDRE DE L'INDEX EST CELUI DE LA PLANTATION
L'ordre des cadres 72 et 74 n'était reproductible par **aucun** tri de l'app, quelles que
soient les données : la planche range *planter un arbre (TENUE) · faire les crêpes (À TENIR)
· le potager (Nuée) · courir dimanche · nager le mardi · le grand plongeoir · l'atelier
(gardé) · appeler Mamie (gardé)* — un ordre chronologique, Nuées **intercalées**. L'app
triait « ce qui presse, puis les tenues, puis le reste », Nuées **en tête**, et ce choix
était écrit en commentaire dans `buildIndex`.

> **Décision Tom :** « L'ordre de plantation devient le tri au repos : Nuées intercalées à
> leur place, gardés de côté à la fin. *Ce qui presse d'abord* reste disponible, en entrée
> du menu ⇅ — rien n'est perdu. **La raison, au-delà du cadre : un tri par urgence est un
> classement par valeur, et le produit n'en fait nulle part.** L'ordre de plantation est
> chronologique et neutre. Les Nuées à leur place plutôt qu'en tête vont dans le même sens —
> une Nuée ne vaut pas plus qu'un Promi. »

Porté dans `buildIndex` (le commentaire d'origine est remplacé par cette décision).
« À tenir en premier » existait déjà au menu ⇅ : il devient le tri d'urgence.

#### Q77 · Trois faits que le cadre 74 impose, et qui n'étaient pas dans l'app
Tous relevés, aucun déduit — le cadre montre **huit** entrées pour un entête qui écrit **12**.

| | ce que le cadre montre | ce que l'app faisait |
|---|---|---|
| **une Nuée remplace ses Promi** | 8 entrées : 5 Promi hors Nuée + le potager + l'atelier + Mamie | 14 entrées : la Nuée **et** ses six Promi |
| **le compte inclut les gardés de côté** | « Index 12 » = 5 + 6 au potager + 1 gardé | 11 — le gardé n'était pas compté |
| **une Nuée sans Promi est un gardé de côté** | « gardé de côté · l'atelier du samedi · GARDÉ DE CÔTÉ » | « perso · 0 PROMI · 0 TENU » — et elle n'apparaissait pas du tout, la liste se tirant des promesses |

Les deux mots (« gardé de côté », « GARDÉ DE CÔTÉ ») sont ceux du cadre, et déjà ceux d'un
Promi gardé de côté dans l'app. **À valider :** « une Nuée sans aucun Promi est un gardé de
côté » est la règle la plus sobre qui rende le cadre ; le document ne la formule nulle part.

#### Q78 · ★ LA HAUTEUR DU TRAIT EST UNE COTE DU PROMI, PAS DE SON ÉTAT
Le §2.5 le dit — « base = **la hauteur de trait figée à la plantation** × échelle » — mais
l'app la **déduisait de la fiche** (`_ficheEcran`), donc de l'ÉTAT. Résultat mesuré sur le
cadre 72 : les six cartes sortaient à **145 · 118 · 108 · 118 · 118 · 145** là où la planche
donne **135 · 107 · 147 · 99 · 123 · 131** — et tout le contenu de la carte glissait de 10 à
20 px sous le trait.

**La preuve que c'est bien une cote du Promi :** les deux cadres de l'Index — 2 par ligne
(échelle 198/600) et 3 par ligne (133/600) — redonnent **la même hauteur figée, à 1,5 px
près**, sur les huit entrées :

```
             cadre 72 (h 198)   135  107  147   99  123  131    —    —
             cadre 74 (h 133)    97   78  105   73   89   94   86   81
             hauteur figée      311  226  347  202  275  299  262  239
```

Chaque nombre sort d'un chemin SVG, aucun n'est estimé. Porté : `p.ht` sur le Promi,
`NUEHT[k]` sur la Nuée, et **la borne [196, 344] du §2.5 ne mord plus sur une hauteur figée**
— elle ne visait que les bases empruntées à une fiche (376, 372). Sans cette levée, « le
potager » sortait à 145 au lieu de 147 : sa hauteur est 347, trois pixels au-dessus d'un
plafond qui ne le regardait pas.

#### Q79 · ★ LE BANDEAU DU FIL DIT L'ÉVÉNEMENT, PAS L'ÉTAT COURANT
La planche le prouve sur **le même Promi** : cadre 56, la fiche de « le grand plongeoir » →
**TENU À DEUX · 3 AOÛT**, trait menthe entier. Cadre 76, son bandeau dans le Fil → **À
RELEVER**, trait `#FFC0A8`, la moitié seulement.

**Aucun jeu de données ne peut satisfaire les deux à la fois.** Un journal enregistre ce qui
s'est passé, pas où en est la chose aujourd'hui. L'événement porte donc sa nature, sa couleur
et son mot (`ev` sur l'entrée de `FEED`, lus dans le cadre) et le bandeau les préfère à ceux
du Promi quand ils existent. Trois des cinq entrées en portent un ; les deux autres
(« planter un arbre », « faire les crêpes ») disaient déjà juste.

**À valider :** le nombre de l'entête du Fil. Le cadre écrit **4** au-dessus de **cinq**
bandeaux, et ni le document ni le moodboard ne disent ce qu'il compte. Le plus sobre qui
rende 4 : **les gestes qui viennent d'ailleurs que de moi** — quatre des cinq entrées portent
une autre personne, la cinquième est « à moi · planter un arbre ». C'est aussi ce que l'app
dit d'elle-même quand le Fil est vide : *« les gestes de tes proches apparaîtront ici. »*

#### Q80 · ★ LES GLYPHES NE PEUVENT PAS COÏNCIDER — c'est la seconde exception, après la matière
La planche est composée en **Hanken Grotesk** et **Bricolage Grotesque** (Google Fonts,
variables) ; l'app porte ses **six faces embarquées** — Apfel, ApfelMid, Bricolage, Fraunces
—, et `CLAUDE.md` §6 **interdit** toute graisse hors de ces six. `Hanken Grotesk` n'est pas
`Apfel` : c'est une autre fonte, que la planche a prise comme doublure (le document la
transcrit d'ailleurs partout en « Apfel 500 »).

**Les dessins de glyphes ne peuvent donc pas coïncider au pixel, quoi qu'on corrige.** Ce qui
doit coïncider, et qui est mesuré à zéro par les juges de section : **la boîte du texte** —
sa place, sa taille, sa couleur, son mot.

`scratchpad/duo_pixel.py` rend donc **deux chiffres** : « écart » (hors matière) et
« hors glyphe » (hors matière ET hors boîtes de texte, `window._zonesTexte()`).
**À valider**, comme Q74 l'a été pour la matière.


---

## 29 août 2026 — CE QUE LA SUPERPOSITION A SORTI

#### Q81 · Le JOUR d'une ligne d'état — l'app n'en garde aucun
Les six cadres de fiche écrivent `<ÉTAT> · <TEMPS>` : « TENUE · 12 MARS », « EN COURS ·
DEPUIS LE 4 AVRIL », « TENU À DEUX · 3 AOÛT », « LANCÉ · PAS ENCORE RELEVÉ », « GARDÉ DE
CÔTÉ · 2 AVRIL », « À TENIR · DIMANCHE ». L'app n'écrivait que le mot d'état.

Pour « à tenir », le temps existe déjà : il sort de `motDuTemps`, dans les mots du produit.
⚠ **`motDuTemps` court-circuite sur l'état** — pour `status:'rate'` il rend « à tenir » et ne
regarde jamais l'échéance ; on lui repose donc la question sur l'échéance seule.

Pour une parole TENUE ou EN COURS, **l'app ne garde aucune date** : elle n'a que des échéances
en jours. On lit `p.leJour` quand il existe, et on n'écrit rien sinon — **jamais une date
fabriquée**. Le jeu de démonstration porte les cinq dates des cadres. **À valider :** faut-il
que le produit date une plantation et une parole tenue ?

#### Q82 · L'anneau du Noyau portait la mauvaise couleur d'état — CORRIGÉ
Il peignait « tenu » en **mauve #D0B0FF** et « en cours » en **bleu #3A54FF**. Trois choses le
contredisaient, toutes dans le produit : `CLAUDE.md` §3, **sa propre légende** `.klegend`
(« #2BE88C tenues · #8FA0FF en cours · #F07A2E à tenir »), et le **cadre 48** (anneau
terracotta r 35 épaisseur 8, recouvert d'un arc **menthe** sur 72 % du tour). Le mauve est la
couleur d'une **Nuée** : sur un anneau qui dit un ÉTAT, il racontait autre chose.
Corrigé dans `drawKRing`. `redteam_geste` cherchait les anciennes couleurs — contrat réécrit
au niveau de la décision, et **il est passé de 12↔13 oscillant à 13/13 stable**, parce que le
menthe et le periwinkle sont moins présents que le mauve dans le fond de Toile animé.

#### Q83 · ★ UN GARDÉ DE CÔTÉ N'A PAS SA DALLE — et il faudrait toucher à la Toile
Le cadre 74 et le §5 donnent une DALLE aux cartes « gardé de côté » — 49 × 41 pour l'atelier,
43 × 36 pour Mamie. **L'app n'en peint aucune**, et ne le peut pas : `Toile.dalleTrame` ne
rend que les ids que la Toile connaît, et `Toile.sync` ne reçoit que les Promi **plantés**.

Mesuré : syncer le gardé fait bien apparaître sa dalle — **et lui donne une case sur la
Toile** (119 relevés au `hit`), c'est-à-dire le PLANTE. Ce n'est pas ce qu'on veut : un gardé
de côté n'est pas planté, c'est toute sa définition.

**Il faudrait que le moteur sache rendre une dalle sans occuper de case.** C'est une
modification de la Toile, que le §9 interdit sans demande explicite. **En attente.**

#### Q84 · ★ LES DEUX PLANCHES NE S'ACCORDENT PAS SUR LA NUÉE
Ni sur la **loi du champ**, ni sur les **données** du potager.

```
promi-nuee-toile   n = 0 · 1 · 2 · 3 · 4 · 7   base = 460 · 374 · 288 · 202 · 176 · 176
                   six points sur six pour base = max(176, 460 − 86 n) — la loi du §9,
                   celle que l'app porte et que redteam_nuee vérifie sur 24 écrans
                   « le potager · 3 PROMI · 2 TENUS » — monter la serre avant les gelées ·
                   reprendre l'arrosage automatique · récupérer les plants de tomates
moodboard-H c. 58  base 232 pour 6 Promi, qu'AUCUN n ne produit
                   « le potager · 6 PROMI · 1 TENU » — arroser tous les soirs · semer les radis
```

Le cadre 58 est donc **antérieur à la loi**. Le jeu de démonstration suit `moodboard-H` pour
les données, parce que l'Index (« 6 PROMI · 1 TENU ») et le Fil (« LE POTAGER · 6 PROMI ») en
dépendent ; et la géométrie suit `promi-nuee-toile`, parce que c'est elle qui porte la loi.

Comparée aux cadres 10/11 de `promi-nuee-toile` (base 176, comme notre n = 6), la Nuée tombe
à **5,1 % hors glyphe**. Comparée au cadre 58, il reste **17 %** — et ce n'est pas un défaut
de dessin.

**Question : laquelle des deux planches fait foi pour la Nuée ?** Tant qu'elle n'est pas
tranchée, l'écran ne peut pas être superposable aux deux.

#### Q85 · L'Index 3 par ligne : la planche RÉPÈTE ses entrées pour remplir la grille
Le cadre 74 porte **douze cartes** dont les quatre dernières répètent les quatre premières
(planter, crêpes, potager, courir une seconde fois). L'Index réel en a **huit** — le nombre
d'entrées, que l'entête confirme avec son « 12 » (5 Promi hors Nuée + 6 au potager + 1 gardé).
Les rangées 1 et 2 sont à **3 à 10 %**, comme l'Index 2 par ligne ; à partir de la rangée 3,
le cadre montre ce que l'app n'a pas. **Rien à corriger côté app.**

#### Q86 · La place de la dalle dans une carte d'Index — la planche se contredit
```
carte            planter  crêpes  potager  courir  nager  plongeoir
centre de la dalle  82,5   126,0    62,0    82,5   116,0    82,5     (centre carte : 82,5)
```
Trois sont centrées, trois ne le sont pas — et le cadre 74 place les mêmes dalles à des
fractions **différentes** de la largeur (0,750 contre 0,764 pour « faire les crêpes »).
Il n'y a pas de règle à en tirer. L'app centre. **~1 % de l'écran.** À valider.


---

## 29 août 2026 (soir) — LES DÉCISIONS DE TOM, ET CE QU'ELLES ONT RETIRÉ

### ✔ Q80 · TRANCHÉ — les glyphes sont la seconde exception
> « La planche est en Hanken Grotesk, l'app en Apfel embarqué, et le §6 l'impose. Les
> dessins ne peuvent pas coïncider, la boîte si — et tes juges la mesurent à zéro. Écris-le
> comme règle à côté de la matière : **zéro écart veut dire zéro hors matière et hors
> glyphe.** »

Écrit dans `CLAUDE.md` § 8 bis, à côté de celle de la matière.
**Et une correction qui en découle :** `_zonesTexte` ne déclarait pas les `<input>` — un
champ à `placeholder` n'a aucun nœud texte. « ⌕ Rechercher » comptait donc en entier comme
un écart de dessin, sur l'Index comme sur le Fil. La bande 120 est passée de 10 % à 5 %.

### ✔ Q84 · TRANCHÉ — `promi-nuee-toile.html` fait foi, le cadre 58 est une erreur
> « Six points sur six suivent `base = max(176, 460 − 86 n)`. Un cadre qui donne 232, qu'aucun
> n ne produit, est un dessin isolé, pas une loi. »

Noté dans `ECARTS-MOODBOARD § 0 bis.1`. **Et le cadre 60 est de la même famille** : il donne
base **282** pour une Nuée vide là où la loi donne **460** (cadre 0 de `promi-nuee-toile`).
Les deux comparaisons ont été repointées. `nuee` **17,3 % → 5,2 %** · `nuee-vide` **11,8 % → 5,2 %**.

### ✔ Q83 · TRANCHÉ — un gardé de côté n'a pas de dalle
> « Lui en donner une l'occuperait une case, donc le planterait. Un gardé de côté ne pose
> rien sur la Toile, parce que rien n'a été promis. Le cadre qui en montre une est une erreur
> de dessin. Sa carte d'Index garde le champ de nature en pointillé, sans matière. »

Noté dans `ECARTS-MOODBOARD § 0 bis.2`. **`peintCarte` n'annonce plus sa boîte de matière
qu'après avoir dessiné** : elle en déclarait une de 72 × 60 sur une carte qui ne peint rien —
un masque sans matière dessous, exactement ce que le § 8 bis interdit.
La **Nuée gardée de côté** suit la même règle : plus d'aplat, corps nu + pointillé de nature.

### ✔ Q79 · TRANCHÉ — « Fil 4 »
> « Ta règle la plus sobre est bonne. »

L'entête compte les gestes qui viennent d'ailleurs que de moi — quatre des cinq entrées.
Porté dans `_s4Fil` et dans `fdCount`, qui l'écrasait avec `FEED.length`.

### ✔ Q85 · TRANCHÉ — la répétition du cadre 74 est un artifice de planche
> « Mesure sur les rangées 1 et 2, et note la répétition comme artifice. »

`duo_pixel` prend une **fenêtre d'ordonnées déclarée** (`y 0 → 474`, le bas de la rangée 2),
**imprimée à chaque ligne** et peinte en gris sur l'image de diff : elle se voit.
`index-3` **21,3 % → 2,7 %**.

### Q87 · Le bouton ⇅ du cadre est en `content-box` — troisième erreur de dessin
Mesuré au rendu : la barre de recherche est en `border-box` (270 × 56), le ⇅ juste à côté en
`content-box` (**62 × 62**). Le tableau du §5 écrit 56 × 56 pour les deux, l'app pose 56 × 56,
`releve-S4` le valide. **Le document et l'app s'accordent contre un oubli de rendu.** On garde
56. Coût : un anneau de 3 px, ~0,2 %. Voir `ECARTS-MOODBOARD § 0 bis.3`. **À valider.**

### Q88 · Le modèle de l'anneau du Noyau — deux arcs contre trois
La géométrie est exacte (78/35/8 et 58/26/6, mesuré au pixel). Mais **la planche peint deux
arcs** — un cercle « reste » plein plus un arc « tenu » — et **l'app en peint trois** :
tenu, en cours, à tenir, avec leurs proportions réelles. Passer à deux **perdrait
« en cours »**. C'est une décision de produit, pas une correction. ~1,8 % sur une Nuée.
**À valider.**


---

## 29 août 2026 (nuit) — QUATRE DÉCISIONS, ET LA FIN DE LA MESURE AU PIXEL

> **Décision de méthode (Tom).** « On arrête la mesure au pixel. Tu as prouvé que le reste
> est le plancher de deux moteurs de rendu, pas un défaut : glisser la capture de −2 à +2 px
> donne le minimum à (0,0). Continuer ne fera plus rien baisser. **Tu regardes, tu corriges,
> tu termines.** »

### ✔ Q88 · TRANCHÉ — l'anneau garde ses TROIS arcs
> « Tenu, en cours, à tenir. La planche en peint deux, mais perdre « en cours » perdrait un
> état du produit. **Le dessin cède.** »

Rien à changer : la géométrie est déjà exacte (78/35/8 et 58/26/6, mesuré au pixel) et les
couleurs suivent le §3 depuis le 29 août. C'est le MODÈLE qui reste à trois arcs, et c'est
voulu.

### ✔ Q86 · TRANCHÉ — la dalle est centrée dans une carte d'Index
> « Les deux cadres donnent des fractions différentes pour la même dalle : elles ont été
> posées à la main. **Une règle vaut mieux que deux exceptions.** »

Rien à changer : `geo()` centre déjà.

### ✔ Q87 · TRANCHÉ — le bouton ⇅ fait 56
> « Le document et l'app s'accordent contre un oubli de rendu du cadre. Troisième erreur de
> dessin recensée, note-la et n'y reviens pas. »

`ECARTS-MOODBOARD § 0 bis.3`. Rien à changer.

### ✔ Les données du potager — alignées sur `promi-nuee-toile.html`
> « Aligne les deux planches sur `promi-nuee-toile.html`, qui porte la loi. Un titre qui
> passe à deux lignes d'un côté et une de l'autre n'est pas un écart de dessin. »

**Ce que j'ai fait, et pourquoi ce n'est pas un remplacement pur.** `promi-nuee-toile` nomme
**quatre** Promi au potager (cadres 8 et 10) : *monter la serre avant les gelées* (TENU),
*reprendre l'arrosage automatique* (À TENIR), *récupérer les plants de tomates* (TENU),
*vider le composteur à deux* (CHICHE RELEVÉ). Le moodboard H en nomme **deux** autres, et
**le Fil et l'Index en dépendent** — le cadre 76 écrit « Adrien a planté : *semer les
radis* », le cadre 72 « le potager · 6 PROMI ».

Le potager porte donc **les six**, les quatre de `promi-nuee-toile` **en tête** (ce sont
elles que la fiche de Nuée montre) puis les deux du moodboard H. Chaque titre vient d'un
cadre, **aucun n'est inventé**, et rien ne disparaît des autres écrans.

⚠ **Une conséquence à dire :** le compte de tenus devient **3** (monter la serre, récupérer
les plants, arroser tous les soirs) là où les cadres 58 et 72 écrivent « 1 TENU ». C'est
l'arithmétique du jeu réuni — et c'est exactement le désaccord que la décision tranche :
`promi-nuee-toile` marque deux TENU que le moodboard H ne connaît pas.


### Q89 · Ce que la passe à l'œil a trouvé, et qui n'était dans aucune liste
Douze points, tous corrigés le 29 août, détaillés dans `ETAT-DES-LIEUX.md`. Trois méritent
d'être retenus comme des FAMILLES, parce qu'ils reviendront :

1. **Un écran qui ne referme pas ce qu'il a ouvert.** Le Peaufiner d'une Nuée laissait ses
   cartes ET ses `display:none` en ligne sur l'entête de la fiche suivante. C'est la
   troisième fois de la même famille (la classe `dp-nuee`, la hauteur `min-height`, ce
   Peaufiner). **Un rendu qui pose quelque chose sur un écran doit savoir le retirer sur
   l'autre**, à l'endroit qui l'a posé.
2. **Un doublon que le garde ne voit pas.** Il y avait DEUX boutons « Planter un Promi dans
   la Nuée » (`#nfAdd`, `#nqAddPromi`) — on le savait. Il y en avait **trois** : la liste de
   Peaufiner de la section 2 en bâtit un troisième, sans id. **Un garde qui vise des ids ne
   voit pas ce qui n'en a pas ; on vise aussi LE MOT.**
3. **Une correction qui verrouille.** Ranger les jumeaux avec `display:none !important` les
   clouait fermés : le Peaufiner de la Nuée ne pouvait plus montrer celui qu'il garde.
   **On range, on ne verrouille pas** — le dernier qui passe doit pouvoir reprendre la main.

### Q90 · Deux contrats réécrits au niveau de la décision
- **`releve-S4`** échantillonnait son « aplat de nature » au milieu du haut de la carte,
  `(W×0,5 ; H×0,05)`. Depuis que la hauteur de trait est figée à la plantation (Q78), la
  dalle est plus grande et ce point tombe **dedans** : la sonde comparait la dalle à
  elle-même et criait « la DALLE n'est pas peinte » sur une carte parfaitement peinte.
  On échantillonne maintenant le coin haut-gauche, là où la dalle centrée ne va jamais.
- **`redteam_geste`** cherchait les ANCIENNES couleurs de l'anneau (mauve, bleu). Réécrit
  sur les couleurs d'état du §3 — et il est passé de 12↔13 oscillant à **13/13 stable**.

#### Q91 · Un écran vide — la cause était un mécanisme, en trois couches
Tom : *« Deux des captures que tu viens de livrer sont des écrans vides… La cause est
probablement celle que tu as déjà trouvée, et tu ne l'as réparée que sur un cas. »* C'était
exact, et il en restait **deux couches** sous celle que j'avais vue.

1. **Ce qu'un écran MASQUE.** `display:none` posé en ligne : il survit à l'écran suivant.
   Marqué `data-masque`, rendu par `closeAll`. (Couche déjà faite.)
2. **Ce qu'un écran POSE.** Le Peaufiner d'une Nuée clouait `#dpdCorps` en
   `display:block!important; position:absolute; z-index:30`. Les cartes qu'il avait bâties
   étaient bien retirées — mais le **contenu d'origine du tiroir** (« le potager »,
   DESCRIPTION, MEMBRES, PIÈCES, « Planter un Promi dans la Nuée ») se repeignait
   **par-dessus le titre de la fiche suivante, tiroir fermé**. `pose()` note désormais les
   propriétés qu'il écrit (`data-pose`) ; `closeAll` retire exactement celles-là.
3. **Ce qu'un écran BÂTIT.** `rangeNuee()` existait et savait ranger — personne ne
   l'appelait à la fermeture. Registre `window._rangeurs`, que `closeAll` passe.

**Le contrôle qui manquait : `redteam_vide.py`.** Il **enchaîne** quinze écrans sans
recharger, deux tours × deux thèmes, et exige de chacun son entête, son trait, son titre,
son état — et l'**absence** des nœuds d'un autre écran. Les autres batteries ne pouvaient
pas le voir : elles ouvrent chaque écran sur une page fraîche. **Prouvé, pas supposé :**
**28/61** sur la version fautive (il nomme `#dpTrameCv invisible inline:none` sur les
fiches et l'entête perdue sur la Nuée), **61/61** après.

**Deux exigences de mon propre contrôle étaient fausses**, corrigées au niveau de la
décision : « vide » ne veut pas dire « sans nœud texte » (une barre de recherche porte un
`<input>` à `placeholder`), et **le cadre 98 ne porte pas de titre** — exiger `#dptTitre`
sur « le trait se referme » aurait fait échouer un écran juste.

#### Q92 · La dalle d'une fiche changeait de couleur à chaque chargement — Q30 était bornée à tort
Trois passages du duo ont donné **trois couleurs** pour la même fiche : lavande, bleu, orange.
Mesuré : pour le **même id 125**, `Toile.dalleTrame` rend tantôt **[209,176,255]** (lavande),
tantôt **[57,84,255]** — c'est-à-dire **le bleu du champ**. La couleur d'une dalle est tirée
au hasard par le moteur (`cc()`, l. 7474, code de la Toile : intouchable, §9).

Une fois sur deux, la fiche sortait donc **bleue sur bleu**, écart de luminosité ≈ 0 là où
le seuil du §3 est 42 : **la fiche était vide à l'œil**. C'est exactement le rouge tournant
que **Q60** décrivait (« un état de fiche qui changeait à chaque tirage de dalle »).

**La cause : la teinture de Q30 était posée sous `if(e.aplat && e.auPlancher)`.** Or Q30 dit
« **dans la bande haute d'une fiche** », pas « quand la matière remplit le champ » — et le
commentaire du code disait lui-même qu'`auPlancher` est « faux partout » sur une fiche. La
borne a donc été levée : la teinture s'applique à la bande haute, boîtée ou pleine.
**Vérifié :** quatre chargements neufs donnent **[200,178,255] · [197,173,255] ·
[207,188,255] · [199,177,255]** — lavande stable, écart de luminosité **97** sur le champ
bleu. La forme ne bouge pas (seule la luminosité est remappée) ; les exclusions tiennent
(gardé de côté, fiche à photo).

#### Q93 · Ce que la revue des 32 captures a laissé ouvert
Aucun écran n'est vide, et aucun ne perd entête, trait, titre ou état. Restent ces écarts,
vus à l'œil, **non corrigés** — chacun est un lot à part (§9 : un lot = un écran) :

1. **Dalle invisible dans l'Index et le Fil.** Même cause que Q92, mais **la teinture y est
   INTERDITE** (§4 et Q30 bis : « le monde, et rien d'autre », vérifié 5/5 par
   `probe_hors_bande.py`). Deux règles se heurtent : le §3 interdit le ton sur ton en
   absolu, le §4 borne la teinture à la bande haute. **Fork réel, à trancher.**
2. **La bande d'une Nuée n'est plus teintée mauve** (§4) — dalle orange et dalle bleue au
   cadre 10.
3. **Gardé de côté :** l'app peint un aplat bleu là où les cadres 26/27 n'en ont pas (Q83),
   et la ligne « GARDÉ DE CÔTÉ · RIEN N'EST PROMIS » manque.
4. **Cartes d'Index :** le titre sur deux lignes touche la ligne d'état (CASSE.md).
5. **Anneau d'une personne :** orange dans l'app, menthe + lilas aux cadres 44/96.
6. **Page + :** le cadre 2 dit « **trace ta moitié** », l'app « trace pour planter ».
7. **Le potager :** 7 Promi au cadre de `promi-nuee-toile.html`, 6 dans l'app.
8. **Échéance :** « DANS 2 JOURS » au cadre 44, « LUNDI » dans l'app.

#### Q94 · La bande d'une Nuée n'est PAS teintée mauve — j'ai eu tort, et je le note
J'avais relevé « la bande du potager montre une dalle ORANGE et une BLEUE dans un champ
mauve » comme un défaut, en m'appuyant sur `CLAUDE.md §4` : *« ce sont de vraies dalles,
seulement teintées mauve »*. **C'était une mauvaise lecture de la planche.** Le cadre 10 de
`promi-nuee-toile.html` — celle qui FAIT FOI pour la Nuée — porte lui-même un carré orange
hachuré, une tache rose et des lignes bleues, et le chapô de sa page l'écrit : *« elle porte
maintenant SES DALLES, rendues par le vrai moteur de la Toile — LES NEUF MONDES du Studio »*.
Teintée, la bande sortait **délavée, presque blanche** (mesuré au duo, deux thèmes).
La teinture posée le matin a donc été **retirée le même jour**. La phrase du §4 vise la bande
haute d'une fiche de Nuée dans l'ancien dessin, pas ce champ-ci.

#### Q95 · Le potager : la planche annonce 7 Promi et n'en nomme que quatre — NON FAIT
`promi-nuee-toile.html` écrit **« 7 PROMI · 3 TENUS »**. L'app en a **6 · 3**. Aligner
demanderait d'ajouter un septième Promi — or la planche ne nomme que **quatre** titres
(monter la serre · reprendre l'arrosage · récupérer les plants · vider le composteur), et
`moodboard-H` compte de son côté **« Index 12 »**, qui vaut 5 hors Nuée + 6 au potager + 1
gardé de côté : à 7, l'Index en ferait 13 et contredirait le cadre 72.
**Je ne l'ai pas fait, et la raison est le §9 : inventer un mot est la faute la plus grave.**
Il faut le titre du septième Promi — un mot, et le lot se fait en deux minutes.

#### Q96 · L'anneau d'une personne — c'est une donnée, pas un dessin — NON FAIT
Aux cadres 44 et 96, l'anneau de Rachel est **menthe + lilas** ; dans l'app il est **orange
plein**. L'anneau dit les proportions tenu / en cours / à tenir de CETTE personne, et il est
juste : dans le jeu de démonstration, Rachel n'a qu'un seul Promi, « faire les crêpes », qui
est à tenir — donc 100 % orange. Le cadre suppose une Rachel qui a déjà tenu.
**Corriger le dessin serait mentir ; corriger la donnée demande d'inventer des Promi.**
Même blocage que Q95, même remède : dire lesquels.

#### Q97 · Le mot du geste sur la page + dépend de l'état — deux cadres, une règle
`promi-moodboard-H.html` ne contient **qu'une occurrence de chaque mot**, et le contexte les
situe : **« trace ta moitié » au cadre 2 · Promi · la phrase vide**, **« trace pour planter »
au cadre 10 · Écrire un mot**, qui est un CHOIX OUVERT. Les cadres 26/27 (reprise d'un gardé
de côté) portent aussi « trace pour planter ».
La règle, une seule, qui couvre les trois : **au repos on trace SA MOITIÉ** (l'autre tracera
la sienne, §2.6) ; **un choix ouvert, ou un gardé de côté, on trace POUR PLANTER** (rien
n'est encore posé). `releve-S3` attendait « trace pour planter » sur les huit écrans : c'était
une extrapolation du contrôle, pas une règle. Réécrit au niveau de la décision (§7), original
en `sauvegardes/releve-S3-page-plus-avant-29aout.py`.

#### Q98 · L'air mangé par le cran — la cote se réécrit dans la bonne unité
Tom, 29 août au soir : *« Tu as grossi les textes sans reprendre les écarts. »* Exact, et
c'était mécanique : monter une taille ne déplace **aucun** `top`, c'est la **hauteur** du
bloc qui grandit vers le bas. Un relevé de positions n'y voit rien.

**Mesuré**, en comparant la version d'aujourd'hui à la MÊME version dont on n'avait remis
que les quatre tailles à l'avant-cran (même jeu de démonstration, mêmes cotes) :
· `à qui → titre` : **6,9 → 4,7 px**, sur les CINQ états de fiche, deux thèmes ;
· `état → champ de message` : −1,1 px ;
· `état → première carte du fil` d'une Nuée : −1,1 px.

**La correction n'ajoute pas un décalage, elle réécrit la cote dans la bonne unité.** Le 30
du §5 n'est pas un espace : c'est « hauteur du bloc à-qui + air ». À 21 px, Bricolage 600
rend 23,1, donc l'air vaut **6,9**. `yTitre = yQui + quiFs × 1,10 + 6,9` redonne 30 au
dixième à 21 px — le moodboard ne bouge pas — et garde l'air à 23. Même chose pour le 42 du
§3.7 (= 13,75 + 28,25) et le 30 du §9 (= 13,75 + 16,25).

**Et un défaut qui n'était pas dû au cran :** le mot d'un gardé de côté n'avait que **9 px**
sous sa pastille là où le **cadre 26 en donne 23** (pastille de 47 de haut, mot à 624 pour un
bas de pastille à 601). Sa cote était figée à `top:558`, qui ne savait pas que la pastille de
l'app n'a pas la hauteur du dessin. Elle suit maintenant le bas réel de la pastille + 23 : à
hauteur égale elle retombe à 558 au pixel.

**`redteam_air.py`** mesure l'espace réel entre deux blocs de texte qui se recouvrent
horizontalement, sur 36 écrans (18 × 2 thèmes), et refuse tout resserrement contre
`air-reference.json`. Il se scope à **la feuille du dessus** (sinon il compare le titre d'une
fiche au bouton de l'Aura, que le DOM garde) et exclut la barre Peaufiner, qui est collante :
un fil défile dessous, c'est le dessin. **Prouvé : 18 paires rouges** sur la version « cran
sans les écarts », dont `à qui → titre` sur les cinq états et les deux thèmes ; vert après.

#### Q99 · Les Réglages · l'encart du profil retiré
Décision Tom : *« La photo et le nom se posent sur le fond, sans cadre, sans contour, sans
pastille. »* `.prof-card` portait `border:3px solid` et `border-radius:22px` — une boîte de
342 × 152 autour des deux seuls éléments qui n'ont rien à contenir. Retirée par le bloc
`lot-REGLAGES-PROFIL`, sans toucher aux deux règles d'origine (§9). **Le bouton d'appareil
reste** : c'est la seule façon de changer sa photo, et le §9 interdit de faire disparaître
une fonction au passage.

#### Q100 · Le jeu de démonstration complété — et l'arithmétique que ça change
Mots donnés par Tom : trois Promi au potager (**arroser les tomates · tailler la vigne ·
ramasser les courges**, à moi, en cours) et un second à Rachel (**rapporter le livre**, TENUE).
Q95 et Q96 sont donc closes : plus rien n'est inventé.

**⚠ Ce que ça change, et je le dis :** le potager en portait **six** — les quatre que
`promi-nuee-toile` nomme, plus « arroser tous les soirs » et « semer les radis », dont le Fil
et l'Index du moodboard H dépendent. Avec les trois nouveaux il en porte **neuf**, pas sept ;
l'entête de l'Index passe de 12 à **16**. L'encart et l'entête suivent le contenu réel — ils
ne récitent pas un nombre. Si la cible est 7, il faut dire lesquels des deux anciens sortent.
**L'anneau de Rachel**, lui, porte maintenant un tenu et un à tenir, comme les cadres 44 et 96
le montrent.

#### Q101 · Un champ blanc n'existe jamais — Q83 relue, et trois écrans corrigés
Tom : *« Sur la page + en thème clair, le champ est crème — la couleur du corps — au lieu de
l'aplat de nature. La dalle flotte sur du vide et “trace pour planter” est sur du crème.
C'est triste et c'est faux. »*

**J'avais lu Q83 de travers.** « Un gardé de côté n'a pas de **dalle** » ne dit rien du
**champ** — et la décision le précisait dans la même phrase : *« sa carte d'Index garde le
champ de nature en pointillé, **sans matière** »*. Ce qui manque à un gardé de côté, c'est la
matière, jamais la couleur. J'avais éteint l'aplat à **trois** endroits : la fiche
(`e.aplat=false`), la page + (`if(!e.garde)`), la carte d'une Nuée vide. Les trois sont
corrigés : `e.aplat` reste vrai, `e.sansMatiere` prend le relais.

**Les cadres 26/27 et 74 dessinent bien le gardé de côté sur le corps nu.** C'est une erreur
de dessin de la même famille que les cadres clairs au trait invisible (§3) : la décision
tranche contre eux, et `releve-S3` a été réécrit au niveau de la décision — il exigeait
« pas d'aplat », il exige maintenant l'inverse (original en
`sauvegardes/releve-S3-page-plus-avant-champ.py`).

**`redteam_champ.py`**, la 22ᵉ batterie, 16 écrans × 2 thèmes. Au-dessus du trait :
aucun pixel de couleur de corps, aucun champ transparent. **Prouvé : 2 rouges** sur la
version au champ éteint — *« le champ est TRANSPARENT (96 % des points) — le corps se voit
dessous »*, sur le gardé de côté, les deux thèmes.

**Deux pièges de l'instrument, corrigés :**
1. `#csTrameCv` reste `display:block` **dans une feuille fermée** : mesuré tel quel, il
   sortait « transparent » sur les cinq fiches. On demande la visibilité RÉELLE, ancêtres
   compris (`checkVisibility`).
2. **Une Nuée vide est semée de graines crème** (§10.6, « dans les deux thèmes ») : mesurées
   #F8F1E5, #F6EEE5 — à moins de 5 du crème. Un test au pixel ne peut pas y distinguer une
   graine d'un corps. **Chaque peintre déclare donc son champ** (`data-champ`) : on compare
   la composition, pas la peinture (§7). Cinq peintres l'écrivent — fiche, page +, carte,
   bandeau, Nuée.

---

# ⚑ CHANTIER STUDIO & PARTAGE — la conception, pas le portage (29 août 2026)

Le portage est clos. Le Studio et le partage **n'ont ni cadre ni inventaire** : la méthode
du duo ne s'y applique pas, il n'y a rien à superposer. Ce qui suit sont les points sur
lesquels les sources se contredisent ou se taisent. Dans chaque cas j'ai pris **l'option la
plus sobre** et j'ai continué, comme le §2 de `CLAUDE.md` l'autorise — **à valider**.

#### Q102 · COMBIEN DE MONDES — huit, et Éclats n'existe pas
Trois sources, deux comptes :
- `CLAUDE.md §4` en liste **neuf** : « Cercle — Terrazzo · Gravure · Sillons · **Éclats** ».
- `PROMI-SPECIFICATIONS §10.4` écrit noir sur blanc : *« `RD = {pixel, braille, sillons,
  gravure, mosaique, encre, terrazzo, touffe}`. **Éclats n'existe pas.** »* — huit moteurs.
- L'app : `order = ['encre','touffe','mosaique','braille','pixel','terrazzo','gravure','sillons']`,
  **huit**. `WL` et `_lockW` connaissent `eclats`, mais **aucun rail ne le montre**.
- Brief Tom, ce jour : cinq libres + trois du Cercle = **huit**.

**Pris : huit.** La spec, l'app et le brief concordent contre `CLAUDE.md`. **Le §4 de
`CLAUDE.md` est à corriger** — je ne l'ai pas touché, il fait autorité et sa correction est
une décision, pas un constat.

#### Q103 · L'ENTÊTE D'UN ÉCRAN DE DOCK — celle des Réglages, pas le mot-marque
`§3.1` donne le mot-marque **Fraunces 600 / 27** en haut à gauche. Mais c'est l'entête d'un
écran de **fiche**. Le seul écran de **dock** que le document inventorie — « Réglages
généraux » — porte autre chose : un **titre Bricolage 700 / 38** à `24/40`, interlettre
`-.035em`, et `✕ FERMER` en Apfel 500 / 12,5 interlettre `.20em`.

**Pris : l'entête des Réglages.** Le Studio et le Partage sont ses cousins de dock.
Conséquence assumée : **Fraunces n'apparaît pas sur ces écrans** — elle reste au seul
mot-marque, donc dans l'**image partagée**, où elle a toujours vécu (15 px).

#### Q104 · LE MOT « STUDIO » — l'app écrit « The Studio »
Le tableau du §2 de `CLAUDE.md` donne le terme du produit : **Studio**. L'app écrit
« The <i>Studio</i> » (l'article anglais), et la ligne des Réglages « The Studio · visuels
& humeurs ». **Pris : `Studio`**, seul, comme `Réglages`, `Index`, `Fil`. Ce n'est pas un
mot inventé — c'est le mot du lexique, débarrassé d'un article.

#### Q105 · LE PINCEAU — la fonction est validée, les mots ne le sont pas
Concept donné par Tom : *« on choisit aussi son pinceau au Studio — la matière avec laquelle
on trace ses moitiés de trait. Le monde est ce qu'on récolte, le pinceau est ce avec quoi on
signe. »* Le mot **pinceau** n'apparaît **nulle part** dans les documents (0 occurrence,
vérifié sur les 20 `.md`) : il vient de Tom, il est donc légitime.

Restaient les **matières**. Trois, aussi sobres que possible :
| matière | d'où vient le mot |
|---|---|
| **Plein** | `§2.6`, colonne « Plein » du tableau des états du trait |
| **Trame** | mot du produit — `dalleTrame`, `stTrameCv`, `csTrameCv`, `§10.4` |
| **Encre** | **TRANCHÉ Tom, 29 août** — remplace « Grain » que je proposais : *« C'est un mot du produit — Encre est déjà un monde, et le trait est une signature. »* |

**Écarté : « Points »** — un trait entièrement en points, c'est déjà l'état **gardé de côté**
(`§2.1 bis`). En faire un pinceau rendrait deux choses différentes identiques à l'œil.

> **⚠ LE DOUBLON « ENCRE » — signalé, comme Tom l'a demandé.** *Encre* nomme désormais deux
> choses au même écran : **un monde** (ce qu'on récolte) et **un pinceau** (ce avec quoi on
> signe). Sur la variante B au repos sur le monde Encre, l'écran écrit **« Encre » deux fois**,
> à 250 px l'un de l'autre — sous « LE MONDE » et sous « LE PINCEAU ». Ce n'est pas ambigu au
> sens du produit (les deux libellés le désambiguïsent), mais **ça se voit**. Tom : *« Si le
> doublon te gêne à l'usage, note-le et on verra à l'écran. »* — c'est noté, et c'est visible
> sur la planche.

#### Q105 bis · LE GESTE DU STUDIO — on glisse le champ, les mondes s'effilochent
Direction Tom, 29 août : *« Le passage d'un monde à l'autre doit être un geste, pas un menu.
[…] on doit sentir qu'on parcourt les mondes, pas qu'on ouvre une liste. »*

**Pris : on glisse le CHAMP.** Le champ *est* le monde ; c'est donc lui qu'on pousse, pas un
sélecteur à côté. Sous le trait, **un rail de huit points** — les points du trait eux-mêmes
(`§2.2` : cercles pleins, r 4,5, tous les 18 px), l'actif plus gros. Il dit **où l'on est**,
il ne se touche pas pour ouvrir une liste.

**La frontière entre deux mondes pendant le glissement n'est PAS une coupe.** `§10.5` le
tranche déjà, et c'est sa phrase : *« Chaque dalle est peinte seule, autour de sa graine […]
**Les mondes se rencontrent en s'effilochant, jamais en se coupant.** »* Pendant le geste, les
graines à droite de la frontière sont rendues par le monde entrant, celles à gauche par le
sortant — la trame s'arrête d'elle-même, tuile par tuile. **Aucun fondu** (le §6 interdit la
transparence molle), **aucun bord droit**.

**Les huit sont dans le rail, les trois du Cercle compris.** Y arriver ne les donne pas :
le champ passe au **flou 2,4** (`§3.8`), l'encart net s'y pose, et l'adoption à 1 € apparaît —
c'est le « au doigt » de Q106. **Le trait, lui, reste NET** : ce qui est fermé, c'est le monde,
jamais ta signature.

#### Q106 · L'ADOPTION D'UN MONDE À 1 € — gardée, mais hors repos
L'app porte `#stLockBuy` : *« Adopte ce design — 1 € »*, plus `#stLockCta` : *« Ou débloque-les
tous / avec Le Cercle »*. Le §9 interdit de faire disparaître une fonction au passage.
Le brief dit : *« on voit quoi, jamais combien, aucun compteur »* — un **prix** n'est pas un
compteur, mais il n'a rien à faire au repos.

**Pris : l'écran au repos ne porte que l'encart du `§3.8`** (« ✦ Le Cercle » + ce qu'il ouvre,
en toutes lettres : *sillons, gravure, terrazzo*). **L'adoption à 1 € est un ajout validé, hors
inventaire** (`CLAUDE.md § « UN AJOUT VALIDÉ, HORS INVENTAIRE »`) : elle apparaît **au doigt**,
quand on touche un monde du Cercle — exactement ce que fait `_lockedNow` aujourd'hui. À
inscrire dans `ETAT-DES-LIEUX.md` au moment de l'implémentation, sans quoi le passage suivant
la prendra pour un résidu.

#### Q107 · LE PARTAGE MONTE À 4K — l'app est bornée à 2160
`shCustomClamp()` borne à `Math.min(2160, …)` et `shareExport()` compose sur une base de
**1080**. Le brief demande **tous formats, 4K compris**. C'est un changement de borne
(3840 sur le grand côté), pas un point de design. Rien d'autre à trancher : *tout est gratuit,
aucun logo Cercle nulle part*.

#### Q108 · LA MAQUETTE N'EST PAS LE MOTEUR — ce que les planches dessinent vraiment
Les trois variantes peignent les huit trames avec **les constantes exactes du §10.4** (grille
de 5, points tous les 9 de rayon 2,9, tesselles de 11 à joint de 2, lignes tous les 6
d'épaisseur 2,6 et l'ondulation littérale, hachures tous les 7 d'épaisseur 3 à un angle par
dalle, neuf ellipses, sept éclats, 3 à 5 fleurs à cœur `#F07A2E`), semées par le générateur
du prototype. **Ce n'est pas `Toile.dalleTrame`.** À l'implémentation, la matière vient du
moteur et de lui seul (`CLAUDE.md §4`, règle 1) ; la maquette ne sert qu'à **choisir**.

---

## ⚑ LE PARTAGE — ce que les variantes supposent (à trancher avec le choix)

#### Q109 · LE « ⋯ » DEVIENT PEAUFINER — aucun tiroir à inventer
L'app ouvre ses quatorze réglages par un `⋯` (`shTrayBtn` → `shTrayWrap`). Le produit a déjà
son tiroir : **la barre Peaufiner du §3.2**, `top 760 · 390 × 84`, fond = couleur de la nature,
« Peaufiner » Bricolage 700/21, `▾` à droite. Tom l'a d'ailleurs mis dans la grammaire de ce
chantier : *« Barre Peaufiner clouée en bas, le contenu défile dessous. »*
**Pris : le `⋯` disparaît, la barre Peaufiner le remplace.** Ce n'est pas une fonction retirée,
c'est la même fonction rendue au composant commun du §5.
**Corollaire : pas d'icône Partager dans cette barre.** Le §3.2 l'interdit déjà sur la page + ;
sur l'écran de partage elle serait un renvoi sur soi-même.

#### Q110 · LE CHAMP D'UN ÉCRAN DE PARTAGE PORTE LA NATURE DE CE QU'ON PARTAGE
« Un champ blanc n'existe jamais » — mais le partage n'a pas de nature propre. **Pris : il
prend celle de son sujet.** Ma Toile et Mes Promi → **bleu `#3A54FF`** ; un Chiche →
**framboise `#FA2258`** ; une Nuée → **mauve `#8A5CF0`**. C'est le levier « Ce qu'on partage »
des planches. Rien n'est inventé : c'est le §4 appliqué à un écran qui montre autre chose que
lui-même.

#### Q111 · LE TRAIT D'UN ÉCRAN DE PARTAGE N'AFFIRME RIEN
L'onde borne le champ, donc il y a un trait. Mais **rien n'est promis sur cet écran**. Pris :
la **première ligne du §2.6 — « rien de tracé »** : amorce seule `0 → 42`, chevron, points
`64 → 390`, dans la **teinte claire de la nature**. C'est le seul état du trait qui ne dit rien
de faux. *À valider : on pourrait vouloir que le trait porte l'état du Promi qu'on partage —
menthe pour une parole tenue. Je ne l'ai pas fait : ce serait écrire un statut sur l'écran, et
la décision A9 dit « aucun statut écrit dans les images partagées ».*

#### Q112 · L'IMAGE EST LA DALLE — sa FORME dit le format
Sur les variantes 1 et 3, la prévisualisation se pose **dans la boîte du §2.7** (centrée, jamais
au-dessus de `y = 88`, jamais à moins de 12 px du trait) et **prend le ratio choisi**. Changer
de format change la silhouette de la carte : le format se lit **sans un mot**.
**La carte porte LE FOND DE L'IMAGE** (`#16171B` sombre / `#F4EEE1` clair), pas la couleur du
champ — mesuré : avec le fond du champ, sa silhouette disparaît et le format cesse d'être
lisible. Le mot-marque et le QR suivent ce fond (§10.6 généralisé, Q59).

#### Q113 · AUCUN SIGNE DU CERCLE SUR CET ÉCRAN — c'est une contrainte NÉGATIVE
Brief Tom : *« tout est gratuit. Aucun logo Cercle nulle part : personne ne doit pouvoir savoir
que quelqu'un ne paie pas. »* Conséquence de dessin, à tenir au moment d'implémenter :
**aucun `✦`, aucun `blur(2.4px)`, aucun encart du §3.8, aucun réglage grisé** sur l'écran de
partage ni dans son Peaufiner. C'est le seul écran du produit où le §3.8 est **interdit**.
`shInviteNote` (« 3 Nuées offertes, pour toi et la personne invitée ») reste — c'est une
invitation, pas une offre payante.

#### Q114 · LA BORNE MONTE À 4K — tranchée par Tom
`shCustomClamp()` borne aujourd'hui à `Math.min(2160, …)` et `shareExport()` compose sur une
base de **1080**. Tom : *« monte la borne à 4K. C'est gratuit, comme tout le partage. »*
Les planches écrivent **3840 × 2160**. Changement de borne uniquement — le pas de 120 et le
garde-fou de ratio (`shCW/shCH < 0.42`) ne bougent pas.

---

## ⚑ LE STUDIO ET LE PARTAGE SONT IMPLÉMENTÉS — 30 août 2026

#### Q115 · LA TRANSITION EFFILOCHÉE N'EST PAS IMPLÉMENTÉE — et je dis pourquoi
La planche du Studio montre, pendant le glissement, **deux mondes qui s'effilochent** l'un
dans l'autre — le §10.5 mot pour mot : *« Chaque dalle est peinte seule, autour de sa graine
[…] Les mondes se rencontrent en s'effilochant, jamais en se coupant. »* Mon peintre de
maquette le fait en portant **un monde par graine**.

**L'app ne le fait pas, et ne peut pas le faire sans toucher au moteur.** `Toile.preview`
sème avec `Math.random()` (relevé dans le code) : **deux appels ne partagent jamais le même
semis**, donc on ne peut pas composer un monde à gauche et l'autre à droite. Rendre deux
mondes en une passe demanderait d'ouvrir le moteur de la Toile — **interdit sans demande
explicite (§9)**. Le glissement **repeint net**, exactement comme avant ce chantier.

**Ce qu'il faudrait pour l'avoir :** une entrée du moteur qui accepte un monde PAR GRAINE
(ou deux mondes et une frontière). C'est une modification de la Toile : elle se décide, elle
ne se prend pas.

#### Q116 · LE TRAIT SUIT CE QUI EST PEINT SOUS LUI — extension de Q59
Le §2.1 bis pose la teinte claire *« parce que le trait est toujours posé sur le champ
plein »*. **Au Studio il ne l'est pas** : la Toile du monde recouvre le champ (§10.7, la
construction d'une Nuée), et en thème **clair** elle est crème. Mesuré : `#CBAAFF` sur crème
tombe très au-dessous du **seuil 42** du §3 — le trait disparaissait, et « Studio » sortait
**crème sur crème**.

**Pris :** le trait et l'entête prennent la **couleur pleine de la nature** sur fond clair,
la **teinte claire** sur fond sombre. C'est exactement la règle de Q59 (le mot-marque a deux
encres, il suit ce qui est peint sous lui), étendue au trait. Les deux tiennent le seuil.
⚠ **Les échantillons du pinceau, eux, SONT posés sur le champ plein** : ils gardent la teinte
claire dans les deux thèmes, comme le §2.1 bis l'écrit.

#### Q117 · TROIS LIBELLÉS DE L'APP REMPLACÉS PAR LA FORME DU DOCUMENT
Je le note parce que ce sont des **mots**, et que le §9 y est sévère.
1. **L'encart du Studio** disait « Ou débloque-les tous / avec Le Cercle ». Le §3.8 écrit la
   forme : titre **« ✦ Le Cercle »**, sous-titre = **ce qu'il ouvre**. D'où
   « ✦ Le Cercle / sillons, gravure, terrazzo ». Même sens, forme du document — et « on voit
   quoi, jamais combien » : les trois mondes sont nommés, aucun compteur.
2. **Le bouton d'adoption** portait l'une de **trois** formulations tirées **au hasard** par
   un rotateur (« Adopte ce design », « Nouvelle trame ? », « Débloque-le »). Sur la variante
   B on **nomme le monde** — « Adopte Terrazzo — 1 € ». Le rotateur n'est pas touché (§9) :
   on réécrit derrière lui, avec la garde du §8 (comparer l'état avant d'agir).
3. **Le bouton d'invitation du partage** portait « ✦  Inviter sur Promi ». **Q113 interdit le
   ✦ sur cet écran** ; et le libellé complet ne tient pas dans un §3.6 de 168 px. Il devient
   **« Inviter »**, et la phrase entière n'est pas perdue : elle vit dans la note de la
   feuille — « 3 Nuées offertes, pour toi et la personne invitée. »

#### Q118 · CE QUI RESTE À BRANCHER — le pinceau ne trace pas encore
Le Studio **enregistre** le pinceau (`localStorage.promi_pinceau`, lisible par
`window.promiPinceau()`) et le montre sur son propre trait. **Il ne change pas encore le
trait qu'on trace au doigt** sur une fiche ou sur la page + : ce trait est peint par le
moteur du geste (`#tenirCv`), et le brancher est un lot à part — celui-là touche au geste,
pas au Studio. **Rien n'est cassé** : sans branchement, le geste garde son trait plein
d'aujourd'hui, qui est exactement le pinceau « Plein ».

#### Q119 · LA BORNE 4K — ce qui a bougé, et ce qui n'a pas bougé
`shCustomClamp()` : **2160 → 3840** sur les deux côtés. `shareExport()` : le **grand côté**
passe de **1080 à 3840** — un format prédéfini sort donc en 2160 × 3840 (portrait) ou
3840 × 2160 (paysage). **N'ont pas bougé** : le pas de 120, le plancher de 540, le garde-fou
de ratio (`shCW/shCH < 0.42`), et la **valeur par défaut** du sur-mesure (1080 × 1920) — Tom
a demandé de monter la **borne**, pas le défaut.

---

#### Q120 · LES MOTS NEUFS DU STUDIO — à valider

Le §2 de `CLAUDE.md` autorise, quand un mot manque **partout** (moodboard,
`PROMI-SPECIFICATIONS.md`, app), à écrire **le plus sobre possible dans le lexique du
produit**, à le noter ici **« à valider »**, et à continuer. Cinq mots sont dans ce cas.

**Les quatre pinceaux.** `Plein` vient du §2.6 et `Sec` est acquis. Restent :

```
Coulé     l'encre qui s'épaissit et s'amincit          à valider
Peigné    le trait strié, plusieurs filets parallèles  à valider
```

⚠ **Aucun nom de pinceau ne reprend un nom de monde** (décision Tom, 31 août 2026).
La première série disait `Plein · Encre · Trame` : « Encre » est un des huit mondes,
« Trame » est le mot du moteur (`Toile.dalleTrame`). Deux vocabulaires sur le même écran,
le même mot pour deux choses — les quatre sont donc des participes, une seule série.

**Les trois invites** (l'ajout validé hors inventaire, voir la note du §5) :

```
« touche une dalle »        à valider
« touche une pastille »     à valider   — remplace « attrape », puis « bouge »
« écarte deux doigts »      à valider
```

`attrape` est tombé sur remarque de Tom (« attrape n'est pas clair comme mot »), et `bouge`
avec lui (« sonne mal »). Le mot retenu est **`touche`, le même qu'à la première invite** —
et c'est un choix, pas une facilité : **c'est LE MÊME geste**, doigt posé puis déplacé, à
deux endroits différents. Même verbe = même geste ; l'objet seul change et dit où. `touche`
et `pastille` sont tous deux des mots déjà au produit (§4 : « la nature se lit à l'ACCENT :
pastille, libellé, contour, badge »). Les trois invites sont **verbe + objet**, et nomment
chacune une action de doigt réelle — une seule série, comme les pinceaux.

**Le compteur, lui, est tranché et n'est pas une question de mot :** une invite ne dure pas
« cinq utilisations ». **Chaque invite meurt dès que SON geste a été fait une fois** — celui
qui comprend au premier coup n'en voit qu'une, celui qui bloque sur le pincement le garde
au trentième passage. Le dessin est la **flèche d'invite du §2.4**, celle que le produit
emploie déjà : elle montre où poser le doigt, elle ne raconte rien.

---

#### Q121 · LA FLÈCHE D'INVITE — sa géométrie se déduit de la corde

**Ce n'est pas une question, c'est un défaut corrigé, noté pour ne pas le refaire.**

Les poignées de la courbe étaient posées par **décalages fixes** (« −26 en x, +14 en y »).
Ça tient sur une flèche longue et se replie sur une flèche courte : sur `Invite2`, longue de
60 px et quasi verticale, **la queue se recroquevillait** et la tangente d'arrivée partait de
travers, si bien que **la pointe se posait sur son propre fût**. Relevé par Tom à l'œil, sur
les deux flèches.

**La loi, désormais :** les deux poignées sont **au tiers et aux deux tiers de la corde**,
poussées de la **même quantité** (0,19 × sa longueur) sur sa **perpendiculaire**. L'arc est
symétrique, il ne boucle à aucune longueur, et la tangente en B est exacte — les ailes s'en
déduisent. **Et la pointe s'arrête AVANT sa cible** (paramètre `recul`) : une flèche
**désigne**, elle ne touche pas ; si elle atteint sa cible, elle la recouvre.

**Deux règles de placement qui en découlent :**
1. **Une flèche ne traverse jamais le trait.** Sur `Invite2` elle partait de la matière et
   coupait la bande crème pour atteindre la pastille. Le trait est **la ligne du produit** :
   rien ne passe dessus. La flèche vit donc **entièrement dans le corps**, sous la vague ;
   le mot reste sur la matière. On lit de haut en bas : mot, vague, flèche, pastille.
2. **Le mot d'invite se pose dans une bande mesurée**, pas au jugé : entre le bas du nom du
   monde (452 → 498) et le point le plus **haut** de l'onde (535 à `base` 560, `amp` 36).

---

#### Q122 · « TENU À DEUX » EST UN SEUL RUBAN, COUPÉ AU MILIEU

L'effilement du trait se calcule sur **la longueur tracée** — c'est la règle du 31 août, et
elle donne raison à « ma moitié donnée », qui s'effile 22 → 6 sur sa propre moitié.

**Mais `duo` n'est pas deux moitiés : c'est un trait entier avec une coupure.** Effilé
« chacun pour soi », le second segment **reprenait à 22 après la coupure** — le trait
grossissait au milieu de l'écran, ce qu'aucune règle ne dit. `ruban()` prend donc un
paramètre `porte=(s0, s1)` : l'effilement se calcule sur **cette** longueur, pas sur le
segment. `duo` passe `porte=(0, 390)` — **un seul ruban 22 → 6 sur les 390, coupé au
milieu**, chaque moitié continuant à l'épaisseur où l'autre s'arrête.

⚠ **À reporter dans l'implémentation du trait effilé**, qui reste à faire : c'est un lot à
part, il déplace `releve-design` sur tous les écrans et finit par un `--figer`.


---

#### Q123 · RIEN DE FIN NE TIENT SUR LA MATIÈRE — mesuré, puis vu

**C'est la loi qui remplace deux règles que j'avais écrites de suite, et qui étaient
fausses toutes les deux.** Elle sort d'un comptage de pixels, pas d'une impression.

**Le problème.** Un mot d'invite ou une flèche d'invite ne se pose pas sur un aplat :
dessous il y a **la matière** — les quatre couleurs de la palette (L 34 à L 84) et, entre
les dalles, **le sol**, qui suit le thème. Compté pixel par pixel dans la boîte de chaque
élément, aux deux thèmes, avec le seuil du §3 (Δ luminosité ≥ 42) :

```
                                            sol nu   crème lisible   encre lisible
  invite 1, mot   (y 176, palette bleue)      14 %    76 % / 61 %     24 % / 39 %
  invite 1, flèche                            38 %    97 % / 59 %      3 % / 42 %
  invite 2, mot   (y 508, frange basse)       49 %    55 % /  6 %     45 % / 94 %
  invite 3, mot   (y 250, palette écartée)    36 %    47 % / 11 %     53 % / 89 %
  invite 3, flèches                           16 %    23 % /  7 %     77 % / 93 %
                                                     (sombre / clair)
```

**Les deux règles fausses, dans l'ordre où je les ai écrites.**
1. *« Sur la matière, l'invite est crème dans les deux thèmes. »* Faux : la bonne encre
   **s'inverse d'une palette à l'autre** — crème gagne sur la palette bleue (76/61), encre
   gagne sur la palette écartée (53/89). La matière est un champ que **l'utilisateur**
   colore ; aucune encre fixe ne peut y être juste.
2. *« Alors on CALCULE l'encre à partir de la palette. »* Faux aussi, et c'est le rendu qui
   l'a montré : sur l'invite 3 en sombre, la meilleure des deux encres ne couvre que **53 %**
   — à l'œil, « écarte deux doigts » y est **à moitié avalé** et les deux flèches
   disparaissent. **Aucune encre plate ne dépasse 61 % sur la matière.**

**La loi, sans exception :**
- **Le mot d'une invite vit DANS LE CORPS**, toujours, sur la même ligne (x 24, y 584,
  15 px, `{{c.ink}}`). Le corps est **le seul aplat de l'écran** : la lisibilité y est de
  **100 %**, dans les deux thèmes et sous n'importe quelle palette. Vérifié à l'œil sur les
  six cadres (trois invites × deux thèmes).
- **Ce qu'elle désigne se marque avec les FORMES du produit, jamais avec un trait fin :**
  la **flèche** quand la cible est dans le corps (invite 2, une pastille) ; le **doigt** et
  son **sillage** quand elle est sur la matière (invite 1 : un doigt posé sur une dalle ;
  invite 3 : deux doigts partis du même point, leur sillage derrière eux). Ce sont les
  mêmes formes qu'aux cadres « tu presses » et « tu traînes », et elles se lisent sur
  n'importe quel fond **parce que ce sont des surfaces**, pas des traits.

⚠ **Portée.** Cette loi vaut pour l'INVITE. Elle **ne touche pas** au mot-marque, au nom du
monde ni à « ✕ FERMER », qui sont du dessin existant — mais la mesure les concerne aussi
(« Studio » : crème 97 % en sombre, **65 % en clair**). **Le thème clair du Studio n'est pas
encore dessiné** : les cadres de la planche sont tous rendus en sombre, et la version claire
n'existe que dans l'outil de mesure. À traiter comme un lot à part.

---

#### Q124 · LA PLACE DU MOT D'INVITE DIT DE QUOI IL PARLE

**Défaut relevé par Tom, 31 août 2026 :** *« écarte deux doigts et touche une pastille,
c'est pas logique les placements ».* Il avait raison, et le défaut était structurel, pas
cosmétique — **le mot était cloué à une place fixe (x 24, y 584) quelle que soit sa cible.**
Deux invites qui parlent de deux choses situées à deux endroits se retrouvaient donc au même
endroit : la place du mot ne disait rien.

**Première réponse — la colonne — ABANDONNÉE.** J'ai d'abord centré chaque mot sur la
colonne de sa cible (110, 93, 195). Tom a tranché autrement le jour même : *« centre les
deux »*. Il a raison, et voici pourquoi : **le doigt désigne déjà.** Faire porter la
désignation par la place du mot, c'est deux organes pour une seule fonction — et ça casse
l'axe de l'écran, où tout le reste est centré.

**La règle, désormais — LE DOIGT MONTRE OÙ, LE MOT DIT QUOI :**

```
LE DOIGT   posé là où il faut poser le sien, sur la matière ou sur la pastille
           c'est lui, et lui seul, qui désigne
LE MOT     une ligne, CENTRÉE, toujours à la même place — y 603, 15 px, {{c.ink}}
           il ne bouge jamais : il nomme le geste, il ne le localise pas
```

**Ce qui en découle :** l'invite 2 n'a plus de flèche mais **un doigt posé sur la pastille
mère** — la même forme qu'aux invites 1 et 3, et qu'au cadre « tu presses ». Une seule
grammaire pour les trois. La flèche du §2.4 reste au produit ; elle n'a pas sa place ici.

**Et le rythme sous le trait a été recalculé** (Tom : *« il n'y a pas les mêmes interlignes,
c'est moche »*). Le bas de la bande, mesuré sur toute sa largeur, tombe à **583,3**. En
dessous : **gouttière 22** entre les rangées, **marge 30** en bas (plancher du §1.5), et les
**57 px** qui restent vont au-dessus des pastilles — c'est la respiration après le trait, et
c'est là que la ligne vient se loger, 19 px de part et d'autre.

```
583,3   bas de la bande
603     la ligne — nom du monde au repos, mot de l'invite pendant une invite
640     les quatre tons          (46)
708     les quatre pinceaux      (44)
774     l'écran et le texte      (40)   → bas 814, marge 30
```

---

#### Q125 · LA SENSIBILITÉ DU DOIGT — celle des réglages de Photos, sur iPhone

**Exigence Tom, 31 août 2026.** Elle vaut pour les trois gestes du Studio : presser une
dalle et traîner, toucher une pastille et bouger, écarter deux doigts.

**Ce qu'elle veut dire :** la couleur **suit le doigt au déplacement**, sans accélération,
**sur toute la course**. Un petit mouvement fait un petit changement ; un grand mouvement
continue de suivre au lieu de buter ; **on revient exactement d'où l'on vient** en refaisant
le chemin à l'envers. C'est un réglage qui **se joue au doigt**, pas un curseur qui saute.

**⚠ À vérifier contre la référence au moment de l'implémentation**, pas au jugé : la valeur
exacte (px de course par unité de teinte, seuil de départ, comportement au relâchement) se
relève sur l'app de référence. Rien n'en est décidé ici.


---

#### Q126 · RIEN N'EST ÉCRIT SUR LA MATIÈRE — la loi vaut aussi pour mon propre dessin

**Trouvé par le contrôle des 26 cadres que Tom a demandé avant intégration** (« mega check
si tout est cohérent, prends du recul »). C'est le défaut le plus grave de la série, et je
l'avais moi-même mis hors périmètre.

**Ce que j'avais écrit en Q123 :** *« cette loi vaut pour l'invite ; elle ne touche pas au
mot-marque, au nom du monde ni à ✕ FERMER, qui sont du dessin existant ».* **C'est faux.**
Le Studio n'a **pas de cadre au moodboard** — c'est un écran de conception, **je l'ai
dessiné**. Il n'y a pas de « dessin existant » à protéger : le défaut est le mien.

**Mesuré sur les 26 cadres (13 écrans × 2 thèmes), 298 textes :**

```
  ✕ FERMER        11 % à 30 % de lisibilité
  Studio          33 % à 34 %
  nom du monde    19 % au pire — « Pixel », cadre Écran, thème sombre
  ---------------------------------------------------------------
  70 textes sous 95 %, et TOUS sur la matière. Zéro ailleurs.
```

**Et à l'œil, « Pixel » n'est pas faible : il est ABSENT.** Crème sur un champ vert clair.
Ce n'était pas une marge à surveiller, c'était un texte qui n'existe pas à l'écran.

**Les deux corrections, et elles suivent la même règle — CE QUI DOIT SE LIRE EST SUR UN
APLAT :**
1. **La matière commence à 100, pas à 0.** Au-dessus, une bande de corps qui porte l'entête.
   L'onde ne bouge pas d'un pixel — c'est le haut du tracé de découpe qui remonte. La Toile
   y gagne un **cadre** : elle devient une image au lieu de border l'écran, et c'est mieux.
2. **Le nom du monde descend sous le trait**, sur la ligne 603, à 30 px au lieu de 46. C'est
   **la ligne où l'écran dit ce qu'on regarde** — ou, pendant une invite, ce qu'il faut
   faire. Au repos le nom, pendant l'invite le mot. **Une ligne, une voix.**

**Après correction : 292 textes mesurés, 0 sur la matière, 0 sous 95 %.** Et 232 contrôles
de géométrie (gouttières, marges, axes, chevauchements) passés sur les 26 cadres.

⚠ **La leçon, et elle dépasse le Studio :** *« c'est du dessin existant »* n'est une raison
de ne pas corriger que si le dessin **vient d'un cadre du moodboard**. Sur un écran de
conception, il n'y a pas d'existant — il n'y a que ce que j'ai posé, et qui se mesure comme
le reste.

---

#### Q127 · LE SENS — ce que le Studio dit, en vingt mots

Contrôle de vocabulaire sur ce qui est **visible** aux treize cadres. Tout l'écran tient en
**vingt mots**, et il n'y en a pas un de trop :

```
Studio · ✕ FERMER
Encre · Mosaïque · Pixel                    (le nom du monde, un par cadre)
Plein · Coulé · Peigné · Sec                (les quatre pinceaux)
sombre · clair · avec texte · sans texte    (l'écran et le texte)
touche une dalle · touche une pastille · écarte deux doigts   (les trois invites)
#3A54FF · #F4B23C · #E8E2D2 · #0E5B4A       (les codes, au Cercle seulement)
```

**Vérifié, sans exception :** aucun mot banni du §2 de `CLAUDE.md` (ni « valider », ni
« urgent », ni « score », ni « brouillon », ni « tâche », ni « objectif », ni « échéance ») ;
**aucun nom de pinceau ne reprend un nom de monde** ; **« Éclats » n'apparaît nulle part**
(Q102) ; et **aucun code couleur en gratuit** — les quatre hexadécimaux ne sortent que sur
le cadre du Cercle.

---

#### Q128 · TOUS LES TRAITS SONT EFFILÉS — et il y en a huit

**Exigence Tom, 31 août 2026 :** *« il faut que tous les designs de traits soient effilés »*,
et *« il en faut des designs en plus payables (50 cts ?) »*.

**1 · L'effilement n'est pas la marque d'un pinceau, c'est la loi du trait.** Les quatre
premiers ne l'appliquaient qu'à moitié : `Plein` et `Sec` s'effilaient, `Coulé` oscillait
sans décroître, `Peigné` ne perdait qu'un tiers. Tous passent par le même facteur —

```
EFFIL(t) = 1 − 0,72·t        11 → 3,08 en demi-épaisseur, soit 22 → 6,2 sur les 390
```

— appliqué **par-dessus la matière propre de chacun**. La goutte reste une goutte, la barre
une barre, la rupture une rupture : c'est l'enveloppe qui décroît, comme au trait d'une
parole tenue (§2.6).

**2 · Quatre pinceaux de plus, à l'unité.** Ils ne sont pas dans le Cercle : **0,50 € pièce**
(prix proposé par Tom — **à valider**). Ce sont des participes, comme les quatre premiers, et
**aucun ne reprend un nom de monde** :

```
libres           Plein · Coulé · Peigné · Sec
0,50 € pièce     Perlé    le trait se noue en perles, qui rapetissent avec lui
                 Tressé   deux brins qui se croisent — la tresse se serre en s'affinant
                 Frangé   le bas du trait s'effiloche, la frange raccourcit
                 Doublé   un second trait accompagne le premier, et s'efface avant lui
```

**« Tressé » a un sens de produit** et ce n'est pas un hasard : deux brins, comme une parole
tenue à deux (§2.6, mode `duo`).

**3 · La rangée glisse, elle ne s'empile pas.** Quatre pinceaux tiennent dans les 342 px ;
la rangée en fait **691**. Le cinquième **dépasse du bord**, et c'est lui qui dit qu'il y en a
d'autres — on glisse le doigt, **le geste déjà appris pour changer de monde**. Aucune seconde
rangée : le rythme sous le trait ne bouge pas.

**4 · Ce qui n'est pas encore à toi est EN POINTILLÉ, sans matière.** C'est le dessin que le
produit emploie déjà pour un gardé de côté (Q83) : le champ est là, la matière n'y est pas.
**Aucun cadenas, aucun badge, aucune couleur d'alerte** — le pointillé suffit et il ne bruite
pas (§ « la règle de la couleur qui gagne sa place »).

**5 · On essaie d'abord, on paie ensuite.** Toucher un pinceau du prix **refait le trait du
haut sous tes yeux, avec lui**. Le prix vient sur **la ligne du nom** — la ligne où l'écran
dit ce qu'on regarde. Une ligne, une voix : au repos le nom du monde, à l'essai
« Doublé — 0,50 € », pendant une invite le mot de l'invite.

---

#### Q129 · LA TOILE VA JUSQU'EN HAUT — et l'entête reste le point ouvert

**Tom, 31 août 2026 :** *« il y a une bande blanche en haut d'écran, corrige — il faut que la
Toile s'étende jusqu'en haut de l'écran ».* Fait : le tracé de découpe repart de 0. L'onde n'a
pas bougé d'un pixel.

**Ce qui reste acquis de la correction Q126 :** le **nom du monde ne remonte pas**. C'était
lui l'invisible — 19 % de lisibilité mesurée, et **absent à l'œil** sur Pixel en sombre. Il
garde sa place sous le trait, et le juge le confirme.

**Ce qui redevient ouvert :** « Studio » et « ✕ FERMER » sont de nouveau posés sur la Toile.

```
30 cadres · 208 contrôles de géométrie : 208 passés
456 textes · défauts HORS matière : 0
             défauts sur la matière : 50 — « Studio » (33–34 %) et « ✕ FERMER » (11–30 %)
             et rien d'autre.
```

**Trois façons de le régler, aucune choisie — c'est un arbitrage de dessin, pas de mesure :**
1. laisser tel quel et l'assumer (l'entête est court, connu, toujours au même endroit) ;
2. descendre « ✕ FERMER » et « Studio » sous le trait — mais le §5 cloue le ✕ en haut à
   droite, `top: 50px` : ce serait une exception à un composant commun ;
3. leur donner un aplat local — un champ derrière les deux mots seulement, pas un bandeau.

⚠ **Q126 reste donc ouverte sur ce seul point.** Le reste de ce qu'elle a corrigé tient.

---

#### Q128 · LE PINCEAU N'EST PAS UN RÉGLAGE DE STUDIO

**Décision Tom, 31 août 2026, et elle défait un lot entier — à raison.**

*« Ça n'a pas de sens de mettre le choix du pinceau dans le Studio. Il le faut dans la
page + lors de la création, puis adaptable et personnalisable depuis chaque fiche de Nuée,
gardé de côté ou Promi. Sinon, dans le système actuel, ça change pour toutes les fiches
d'un coup : ça restreint la personnalisation par fiche ou par Nuée. »*

**La règle qu'elle pose, et qui vaut au-delà du pinceau :** *le Studio ne porte que ce qui
est **vraiment global**.* Ce qui appartient à **une** parole se choisit là où cette parole
se fait.

```
AU STUDIO — global          le monde · la palette · l'écran (sombre/clair) · le texte
À LA PAGE +, à la création  LE TRAIT du Promi qu'on plante
DEPUIS CHAQUE FICHE         on le reprend — Promi, Nuée, gardé de côté
```

**Conséquence de dessin, et elle est grande :** au Studio, **le trait n'a plus rien à
montrer**. L'onde du §2.1 y était là pour porter le pinceau qu'on essayait. Elle disparaît,
le corps disparaît, et **la Toile prend tout l'écran**.

**Ce que ça oblige, et qui donne son concept à l'écran :** il n'y a plus d'aplat, or **rien
de fin ne tient sur la matière** (Q123/Q126 — 11 % à 46 % de lisibilité, mesuré). Donc :
- ce qu'on **touche** est une **forme**, et elle flotte sur un **plateau** — un aplat aux
  coins ronds découpé dans la Toile, sur lequel tout est lisible **par construction** ;
- ce qui reste sur la Toile nue est **gros** : le seul nom du monde, à 46 px.

**Deux plateaux, pas un tiroir** — « plein écran, et tout atteignable sans déplier » reste
la règle donnée par Tom. En haut : le mot-marque et FERMER. En bas : les quatre tons, et
sous eux les deux réglages de vue, **sans un libellé** :

```
L'ÉCRAN   un disque coupé en deux, encre à gauche, crème à droite ;
          l'anneau se porte sur la moitié active. Il ne dit pas « sombre / clair » :
          il les MONTRE.
LE TEXTE  un disque qui porte trois barres — les mots sur les dalles — ou le même
          disque nu. Ce qu'on voit est ce qu'on aura.
```

⚠ **À reprendre au lot de la page + :** le trait y devient un choix de création, et la
fiche doit pouvoir le reprendre. Les douze traits (quatre libres, huit à 0,50 €) sont
dessinés et tiennent ; c'est leur PLACE qui change, pas leur dessin.

⚠ **Ordre des traits :** `Perlé` passe **en dernier** des huit payants (décision Tom, même
jour) — il ouvrait la série, il la ferme.

---

#### Q129 · LE NOM DU MONDE RESTE SUR LA TOILE — arbitrage assumé

**Décision Tom, 31 août 2026 :** *« le nom du design doit aller sur la Toile et pas sous le
trait — mode clair police noire, mode sombre police blanche »*. C'est-à-dire `{{c.ink}}`,
sans exception locale.

Elle **annule la correction 2 de Q126**, qui l'avait fait descendre sous le trait pour la
lisibilité. **La mesure de Q126 reste vraie** : sur un monde clair et saturé, un texte posé
sur la matière descend à 19 % de lisibilité de boîte, et « Pixel » était invisible à l'œil.

**Ce qui rend l'arbitrage tenable, et il faut le dire :** le nom est à **46 px**. À cette
taille, la lettre porte là où un mot de 15 px se noie — le pourcentage de boîte n'est pas la
bonne mesure pour un glyphe épais. **Et c'est désormais le SEUL texte sur la Toile** :
l'entête est passée sur son plateau, tout le reste aussi. Le risque est concentré sur un mot
au lieu d'être dispersé sur cinq.

⚠ **À revérifier à l'œil sur les huit mondes, aux deux thèmes**, quand la palette du Studio
sera figée — en particulier Pixel et Mosaïque, les deux plus clairs.

---

#### Q130 · LA MAQUETTE DE MATIÈRE EST ABANDONNÉE — on prend le vrai moteur

**1er septembre 2026, et c'est la faute la plus grave de la série.** Tom, sur la planche des
huit mondes : *« tout est faux là-dedans, c'est pas du tout les vraies dalles dans leurs
vrais designs et leurs agencements de quand ils sont à la Toile. »*

**Il a raison, et le fichier fautif le disait lui-même.** L'en-tête de `painter.js` portait
noir sur blanc : *« Ceci est une MAQUETTE : à l'implémentation, la matière vient de
Toile.dalleTrame(canvas, id, 1), jamais d'ici. »* J'ai passé un lot entier à **corriger la
maquette** — les colonnes de couleur, le pas de la mosaïque, le remélange — au lieu de
constater qu'elle n'avait pas le droit d'exister. Le §4 est sans appel : *« toujours la
vraie dalle du moteur ; jamais un polygone, jamais une approximation »*, et le §9 range
l'invention de forme dans « la faute la plus grave ».

**Ce qui a été fait à la place.** Les planches **ne peignent plus rien**. Elles chargent
`app.html` dans un cadre caché et appellent **`Toile.preview()`** : formes, agencement,
semis et couleurs sont ceux de l'app, au pixel. Vérifié : **12 canevas sur 12** peints par
le moteur sur la planche du Studio, **8 sur 8** sur celle des mondes.

**Et ça corrige une erreur de conception, pas seulement de rendu.** Le moteur ne connaît pas
la loi « mère / écart / éclat » que la maquette inventait. Il porte :

```
Toile.palettes()   DIX palettes nommées — Signal, Terre, Océan, Aurore, Nuit,
                   Forêt, Braise, Lavande, Agrume, Ardoise
                   chacune : { name, cols: [[r,g,b] × 4] }
Toile.setPalette(k) · Toile.setHue(...) · Toile.getPalette()
Toile.setTheme(...) · Toile.getTheme() · Toile.isLight()
Toile.preview(cv, monde, w, h) · Toile.dalleTrame(cv, id, 1)
```

**Les quatre tons du plateau du Studio sont donc les quatre `cols` de la palette active**,
relus du moteur à chaque rendu — et le geste de couleur devra piloter `setPalette` et
`setHue`, pas une loi inventée. La planche porte les dix palettes en boutons : on voit
l'écran sous chacune.

**Le semis se remélange tout seul :** `Toile.preview` sème avec `Math.random()`. Aucun
mécanisme à ajouter — c'est le moteur qui le fait, comme dans l'app.

⚠ **La leçon, et elle vaut pour tout le reste du chantier.** Une maquette qui annonce
elle-même qu'elle est une maquette **n'est pas un point de départ, c'est une dette**. Quand
un moteur existe dans le produit, la planche l'appelle — même si c'est plus compliqué à
câbler. Sinon on juge un dessin qui n'existera jamais.

`painter.js` est conservé en archive (`scratchpad/c5/painter.js`, et son état d'avant les
corrections inutiles dans `painter-avant-melange.js`) mais **il n'est plus branché nulle
part**.

---

#### Q131 · CE QUE LA MAQUETTE AVAIT MASQUÉ — pour mémoire

Les trois bugs corrigés dans la maquette avant qu'elle ne soit abandonnée : la teinte
`P[(i*2 + x%3) % P.length]` qui rendait une colonne monochrome dès que `cols` était pair ;
un tremblement de ±0,33 cellule qui laissait lire la grille ; et un pas de mosaïque de 11
avec une tesselle de 9, là où le §10.4 dit **tesselle 11 + joint 2, donc un pas de 13**.

**Aucun de ces trois ne concernait le produit** — ils ne vivaient que dans la maquette. Ils
sont notés ici pour une seule raison : si quelqu'un rebranche un jour un peintre local, il
retrouvera les mêmes pièges. **La bonne réponse reste : ne pas en rebrancher.**

---


---

#### Q132 · DEUX LEVIERS DU MOTEUR QU'IL FAUT CONNAÎTRE POUR L'APERÇU

**Relevé par Tom sur les planches, 1er septembre 2026 :** *« il n'y a que quelques dalles,
le reste est vide dans les rectangles »* — et sur le Studio, *« quelques dalles dans un coin
de l'écran au lieu qu'il y en ait partout »*.

**Ce n'était pas un bug, et c'est important de le dire.** `Toile.preview` bâtit bien une
grille complète — `base = max(20, pw/5,5)`, soit **6 × 12 graines** en 390 × 844 — mais il
n'en teinte que **`nc = 11 + rand(2)`**, groupées autour d'un centre tiré au sort, plus une
à trois graines lointaines. C'est l'aperçu d'une Toile **qui n'a que quinze Promi** :
`Toile.count()` en renvoie 15. Le moteur dit la vérité de la Toile de ce compte-là.

**Le moteur porte ses deux leviers, et `shareRender()` les utilise déjà dans l'app :**

```
window._shAllColored = true     teinte TOUTES les graines — la Toile remplit l'écran
                                (et le moteur passe alors le sol clair à #DBD0BA :
                                 il sait qu'une Toile pleine demande un fond plus sourd)
window._shThemeOverride = bool  force le thème de la MATIÈRE, indépendamment de l'app
                                (lu par isLightM() ; null pour rendre la main)
```

On les pose, on rend, **on les retire**. Sans le second, la colonne « clair » d'une planche
montre une Toile **sombre** : `preview` lit le thème de l'app, pas celui de la vignette.

**Mesuré après correction, la part de matière par monde :**

```
pixel 82 %   encre 70 %   mosaïque 66 %   touffe 46 %
braille 34 % terrazzo 33 % sillons 32 %   gravure 29 %
```

Les basses ne sont pas des trous : **ce sont les matières ajourées** — des points, des
hachures, des lignes — où le sol se voit entre, conformément au §10.4. Les sols relevés par
thème : `#0b0c12` en sombre, `#dbd0ba` en clair.

⚠ **À reprendre à l'intégration :** le Studio de l'app appelle `Toile.preview` **sans** ces
deux drapeaux (`buildStudio`, ligne ≈ 6478). Sa Toile est donc, aujourd'hui aussi, une Toile
à douze dalles dans un coin. Le lot devra poser `_shAllColored` — c'est le même geste que
sur la planche, et il vient du moteur.

---

#### Q133 · LE STUDIO EST INTÉGRÉ — `lot-STUDIO-PLATEAUX`

**1er septembre 2026.** `lot-STUDIO-CHAMP` (« le champ ») est **supprimé** — 29 492 octets,
lignes 20909 → 21407 — et remplacé, pas ajusté par-dessus. Reste zéro `st-champ`, zéro
`stcCadre` dans le fichier.

**Les onze nœuds de l'app sont DÉPLACÉS, aucun refait :** `#stBg` (la Toile bord à bord),
`.closeb`, `.st3-wn` (le nom, 46 px sur la Toile), `.st3-dot` (les huit points),
`.st3-hint` (l'invite), `.st3-pals` et `.st3-spec` (les palettes du moteur et la jauge,
dépliées au besoin), `#thToggle` et `#txToggle` (portés par les quatre disques),
`#stLockBuy` et `#stLockCta`. **Les disques ne remplacent pas les bascules : ils les
CLIQUENT** — le comportement reste celui de l'app.

**Cinq défauts trouvés à la capture, tous corrigés :**

1. **Le cadre se calait à −823.** `cale()` mesurait **pendant la transition d'ouverture** :
   un `.screen` arrive de sous l'écran, donc `sc.top` valait ~880 quand `#device.top`
   valait 53. Le Studio sortait entièrement vide, tout posé 860 px trop haut. Garde de
   plausibilité (|décalage| > 120 → on refuse de caler) + recalage à l'ouverture par un
   observateur **qui compare avant d'agir** (§8).
2. **Le libellé disait « Nouvelle trame ? — 1 € ».** C'est le rotateur de `#stBuyTx`, le
   piège nommé au §8. Figé par un observateur qui compare avant d'écrire.
3. **Deux dégradés, interdits par le §6** — et ils ne venaient pas du fond :
   `getComputedStyle` donnait bien `background-image: none`. Ils étaient peints par des
   **enfants** : `.enc-live > .enc-fx` pose trois blobs floutés à 15 px et animés, plus un
   grain en `mix-blend-mode`. Invisibles à l'inspection de l'élément **et** à
   `elementsFromPoint` (ils sont en `pointer-events:none`). Éteints nommément, comme Q23
   l'a fait pour les Réglages.
4. **L'encart du Cercle cassait sur trois lignes.** `white-space:nowrap` sur ses deux
   lignes, et `flex:1 1 auto; min-width:0` sur son bloc de texte.
5. **La Toile montrait le monde PRÉCÉDENT sur un monde verrouillé.** `Toile.curWorld()`
   reste sur le dernier monde possédé : l'écran vendait « Gravure » en montrant la matière
   d'Encre. On lit désormais le monde du **point actif** (`.st3-dot.on[data-w]`), celui que
   le nom annonce. C'est tout l'enjeu de « on doit voir ce qu'on n'a pas ».

**Deux contrats de test réécrits au niveau de la décision** (CLAUDE.md §7) —
« les deux bascules sont dans le tiroir » et « groupe centré » visaient `#stcTiroir` et
`.stc-pile`, nœuds du lot supprimé. La règle protégée n'a pas bougé : **les deux bascules
sont atteignables et leur groupe est centré**. Le nouveau contrôle est **plus fort** : il
vérifie en plus que le disque **atteint vraiment la bascule** (il clique, puis relit l'état
de `#txToggle`). Original : `sauvegardes/redteam_ecrans-avant-studio-plateaux.py`.

**Les batteries, en série, après correctifs :**

```
redteam_ecrans   150/150     redteam_vide     61/61      redteam_champ    32/32
redteam_toile     17/17      redteam_geste    13/13      redteam_nuee     24 écrans, 0 écart
redteam3          18/18      redteam_demande  19/19      redteam_verbe      6/6
redteam_tonsurton 26/26      redteam_fonctions 22/22     redteam_polices   0 absent
redteam_air      391 paires, intact           redteam_filets  0 filet parasite
releve-design.py  ✅ AUCUN ÉCART
redteam / redteam2  11/15 et 9/10 — IDENTIQUES à la référence mesurée sur la sauvegarde
                    d'avant le lot : ces rouges préexistaient, ce ne sont pas les miens.
```

---

#### Q134 · LE FRÉMISSEMENT — l'app en a DEUX, et il ne fallait pas celui-là

**Relevé par Tom, 1er septembre 2026 :** *« quand on arrive dessus ou quand on change de
design en swipant, l'animation des dalles est ultra violente, c'est le même bug que dans
l'onboarding. »*

**La cause était la mienne, et ce n'était même pas une animation.** `poser()` appelait
`poseToile()` à **chaque `poser()`** — donc à chaque doigt levé, et cinq fois de suite à
l'ouverture. Or `Toile.preview` **sème avec `Math.random()`** : chaque appel compose une
**autre** Toile. Ce n'était pas un mouvement, c'était un **clignotement de compositions**.
Corrigé : on ne sème **qu'une fois par ouverture**, et au changement de monde l'app appelle
déjà `Toile.repaintWorld`, qui **garde les germes** — mêmes graines, mêmes places, matière
neuve. Doux par construction.

**L'app a deux animations de matière, et elles n'ont rien à voir :**

```
Toile_previewLive   découpe le rendu dans un BLOB qui ondule — AMP = rx × 0,05 + 2,5
                    c'est l'aperçu de l'ONBOARDING, et c'est l'effet « horrible »
_quiv (frame)       déplace CHAQUE GRAINE de quelques dixièmes de pixel, amorti
                    en exponentielle — c'est le frémissement de la Toile
```

**On reprend `_quiv` tel quel, aucune constante inventée :** durée **1100 ms** (850 sur les
mondes en grille), enveloppe `exp(−âge/380)` (300 en grille), amplitude **7 px** en x et
**5 px** en y, le tout multiplié par `window._liveAmp`, que l'app fixe à **0,07**. Le rendu
passe par `Toile.repaint(#stBg)`, qui relit `px/py` sur les graines mémorisées — **on ne
touche pas au moteur, on l'utilise**.

**Mesuré** (`window._studioFremiSonde()`, exposée comme l'app expose déjà `Toile_probe`) :

```
t =   21 ms   72/72 graines   moyen 0,384 px   max 0,539 px
t =   89 ms                   moyen 0,322     max 0,476
t =  141 ms                   moyen 0,280     max 0,433
t =  315 ms                   moyen 0,175     max 0,237
t =  524 ms                   moyen 0,102     max 0,164
t =  803 ms                   moyen 0,049     max 0,076
t = 1225 ms   0/72 — éteint
```

Un demi-pixel au départ, éteint en 1,1 s, sur **toutes** les graines. « À peine discernable
mais beau », et rapide — et ça se **mesure**, ça ne se juge pas sur une capture.

---

#### Q135 · TROIS AUTRES BUGS DU STUDIO, ET UNE FRAGILITÉ

**1 · Des mondes gratuits passaient PAYANTS.** `setW` fait
`if(_locked) window._lockedWorld = order[ni]` — il **écrit** le global quand c'est
verrouillé et **ne le remet jamais à null**. Le lire, c'était faire passer payant tout monde
visité **après** un monde payant. L'app maintient en revanche correctement la classe
`world-locked` (basculée dans les deux sens) : c'est **elle** qui dit l'état. Vérifié sur les
huit mondes après avoir sali le global : cinq gratuits, trois payants, accord parfait.

**2 · La Toile montrait le monde PRÉCÉDENT sur un monde verrouillé** — l'écran vendait
« Gravure » en affichant la matière d'Encre, parce que `Toile.curWorld()` reste sur le
dernier monde **possédé**. On lit le monde du **point actif** (`.st3-dot.on[data-w]`), celui
que le nom annonce.

**3 · Deux dégradés, interdits par le §6, et invisibles à l'inspection.**
`getComputedStyle` donnait `background-image: none` sur les deux nœuds : ils étaient peints
par des **enfants**, `.enc-live > .enc-fx`, trois blobs floutés à 15 px et animés, plus un
grain en `mix-blend-mode`. Invisibles aussi à `elementsFromPoint` — ils sont en
`pointer-events:none`. Éteints nommément.

**La fragilité — ON SUIT LE NOM, PAS LES GESTES.** `setW` est locale à `buildStudio` : on ne
peut pas l'envelopper. Mais elle met toujours `.st3-wn` à jour. Un observateur **qui compare
avant d'agir** suit donc **tous** les chemins — le glissement, le clic sur un point, et tout
appel extérieur. Vérifié sur un chemin non prévu : nom, point actif et matière d'accord.

⚠ **CE QUI N'EST PAS FAIT, et il faut le dire.** Le **geste de couleur au doigt** — presser
une dalle ou un ton et traîner, avec la sensibilité des réglages de Photos (Q125) — **n'est
pas implémenté**. La planche le dessine ; le code ne l'a pas. Aujourd'hui, toucher un ton
**déplie le rail des palettes du moteur** (`Toile.setPalette`) et la jauge de teinte
(`Toile.setHue`) : les dix palettes sont atteignables, mais **pas au doigt**. C'est le
prochain lot du Studio, et il devra se mesurer contre la référence, pas au jugé.

---

#### Q136 · L'ONDE PASSE À 36 PARTOUT

**Décision Tom, 1er septembre 2026 :** *« l'ondulation du trait doit devenir celle que tu
avais mise en moodboard — moins d'amplitude — et applique-la partout. »*

**Vérifié contre l'autorité avant de toucher.** `PROMI-SPECIFICATIONS §2.4 bis` dit que
`amp` est **une constante par écran**, qu'elle vaut **46 sur la page + et 36 à 52 sur les
fiches**, et donne la règle d'un écran neuf : **`amp ≈ 0,17 × base, borné à [36, 52]`**.
**36 est donc la borne BASSE que la spec autorise** — la valeur la plus calme possible, et
c'est celle des planches. L'onde garde sa loi entière (`per 1,5 · mont = amp·0,34 ·
a = amp·0,62`) : **seule l'amplitude change.**

**Ce qui a bougé — neuf points, tous les écrans :**

```
fiche · Chiche tenu à deux    base 372   amp 44 → 36
fiche · Promi tenu, à mot     base 262   amp 44 → 36
fiche · Promi tenu            base 376   amp 48 → 36
fiche · moitié                base 262   amp 44 → 36
Nuée  · les trois cadres      base 300   amp 44 → 36   (×3)
Nuée  · le champ posé                    amp 40 → 36
page + · au repos                        amp 46 → 36
```

**Deux exceptions écrites, intouchées :** `amp = 22` dès qu'un panneau de choix occupe le
corps (§2.4 bis — le champ y est réduit à `base = 196`, une amplitude normale ferait
toucher la dalle), et la **loi propre de la carte d'Index** (§3.9, `amp = 13 × largeur/173`,
période 1 sur SA largeur).

⚠ **Ce que ça contredit, et il faut le dire.** Les valeurs 44 / 46 / 48 étaient **relevées
cadre par cadre** du moodboard de référence — le commentaire de l'app le dit noir sur blanc
pour la Nuée : *« base = 300, amplitude = 44, boîte SVG = 384 — les trois cadres, sans
exception »*. Passer à 36, c'est donc **une décision de Tom qui remplace un relevé**, pas une
correction de bug. Elle reste dans la fourchette de la spec, et c'est ce qui la rend tenable.

**Les batteries, toutes, après le changement :**

```
redteam_ecrans 150/150   redteam_formes  38/38   redteam_vide     61/61
redteam_nuee   0 écart   redteam_champ   32/32   redteam_geste    13/13
redteam_toile   17/17    redteam_verbe     6/6   redteam_tonsurton 26/26
redteam3        18/18    redteam_demande 19/19   redteam_fonctions 22/22
redteam_phrase    6/6    redteam_pastilles 12/12 redteam_polices  0 absent
redteam_air    391 paires intact          redteam_filets  0 parasite
releve-design  ✅ AUCUN ÉCART
```

`redteam_formes` est le contrôle qui compte ici : il compare **la courbe peinte à la loi
extraite du cadre**. Il reste à 38/38 — la loi n'a pas bougé, seule son amplitude.

---

#### Q137 · LES DEUX PAIRES DU STUDIO — l'écart, les mots, et l'air

**Trois remarques de Tom, 1er septembre 2026, et les trois portaient.**

**1 · L'écart.** *« Ils sont trop rapprochés, on ne comprend pas que c'est deux et deux ; là
sont équidistants les 4. »* Mesuré : **18 px dedans, 22 px entre** — quasi égal, et l'anneau
de l'actif (6,5 + 3,2 px de part et d'autre) mangeait le peu qui restait. C'est désormais
**20 dedans, 56 entre**, mesuré à l'écran.

**2 · Les mots.** *« T'es sûr qu'on comprend ce que c'est, les deux ? »* — non, pas pour
celle du texte : trois barres dans un cercle peuvent dire n'importe quoi. J'ai d'abord posé
« l'écran » et « le texte » : **également faux**, comme Tom l'a vu tout de suite — ça nomme
**la question**, pas **la réponse**. Le mot dit maintenant **le choix courant**, et il change
au doigt :

```
sombre  ⇄  clair              (les mots de #thToggle)
avec texte  ⇄  sans texte     (les mots de #txToggle)
```

Ce sont **les mots de l'app**, repris tels quels — rien d'inventé. **Un mot par paire, pas
quatre** : « avec texte » mesure 75 px pour les 64 disponibles entre deux disques d'une
paire ; quatre mots se chevaucheraient. Le mot est centré sur 108 px — la largeur exacte de
deux disques et de leur écart.

**3 · L'air.** *« Là c'est tout écrasé. »* Le plateau ne se règle pas au jugé : il
s'additionne, marge basse 36 (§1.5).

```
marge interne 26 · les quatre tons 54 · gouttière 34 · le mot 13 · 8 ·
les disques 44 · gouttière 34 · les huit points 14 · marge interne 26   =   253
```

D'où le plateau **555 → 808** (au lieu de 600 → 808), et chaque rangée à sa place calculée :
tons 581, mot 669, disques 690, points 768. L'adoption suit — le bouton passe à 473, l'encart
du Cercle à 660, ce qui **laisse les quatre tons visibles au-dessus de lui** (§3.8).
Vérifié au pixel dans l'app : les cinq cotes tombent exactement sur le calcul.

---

#### Q137 bis · (ancienne rédaction, remplacée)

**Relevé par Tom :** *« ils sont trop rapprochés, on ne comprend pas que c'est deux et deux ;
là sont équidistants les 4, ça va pas. Et t'es sûr qu'on comprend ce que c'est, les deux ? »*

**L'écart : mesuré à 18 px dedans et 22 px entre** — quasi égal, et l'anneau de l'actif
(6,5 + 3,2 px de part et d'autre) mangeait le peu qui restait. C'est désormais **20 dedans,
56 entre** — presque le triple, mesuré à l'écran.

**La question : la réponse honnête est NON, pour l'une des deux.** La paire encre/crème se
lit — un disque noir et un disque crème disent « sombre / clair » sans un mot. La paire du
texte, **non** : trois barres dans un cercle ne disent pas « les mots sur les dalles », elles
peuvent dire n'importe quoi, à commencer par un bouton de menu. Le test **ÉVIDENT** du §10
tranche : *si on ne comprend pas en une seconde, ce n'est pas fini, même si c'est beau.*

Les deux paires portent donc leur libellé — **« l'écran »** et **« le texte »** —, dans la
grammaire déjà là (`.st3-lbl2`, `.sh-lab`) : ApfelMid 500, 10,5 px, capitales, interlettre
.16em, opacité .62. On perd un peu de pureté, on gagne l'évidence.

---

#### Q138 · L'ENCART DU HAUT — onze écrans, et quatre qui attendent leur lot

**Décision Tom, 1er septembre 2026 :** *« déploie à toutes les pages et toutes les fiches
l'encart en haut avec Studio et ✕ Fermer, mais ça va être Réglages et ✕ Fermer (avec s
couleur qui clignote), Partager ✕ Fermer, etc. partout »* — et *« fais moitié moitié »*.

**Onze écrans posés :** Réglages · Partager · Fil d'actu · Aura · Index · Arranger ·
Comprendre ton Aura · La langue · La confidentialité · Nuée (Essaim) · Le Cercle.

**⚠ QUATRE N'Y SONT PAS, ET C'EST DÉLIBÉRÉ.** Les forcer serait le « crible posé en bloc »
que le §8 interdit — chacun a une grammaire propre :

```
#personSheet     le titre vit DANS `.ps-head`, une rangée flex avec l'avatar :
                 y insérer un plateau brise la rangée
#previewScreen   n'a pas de titre en haut — le sien est sous l'aperçu
#createSheet     la page + porte le mot-marque du §5 dans `.cs-top`, et sa composition
                 est celle que `releve-S3-page-plus` mesure
#detailPoster    la fiche n'a AUCUN nœud de mot-marque dans son DOM : il est construit
                 par un lot, et `releve-S1-fiches` le mesure
```

Ces quatre-là demandent **chacun leur lot, avec son juge** — c'est le §9 : un lot, un écran,
un avant/après.

**Le titre est DÉPLACÉ, jamais refait.** Le `s` clignotant de « Réglages » est un
`<span class="ti-x blink">` : on déplace le titre **entier**, l'animation vient avec. La
liste des écrans est **nommée un par un** — jamais un balayage par famille (§8).

**Quatre pièges, tous rencontrés, tous mesurés :**

1. **Le titre n'est pas toujours un enfant direct.** Sur Réglages il vit dans `#stScroll`,
   sur Partager dans `.sh-top` — deux conteneurs posés par des lots antérieurs. On le
   cherche où qu'il soit et on pose le plateau **dans son parent**.
2. **`.closeb` est cloué en `position:absolute` par des règles à UN IDENTIFIANT**
   (`#settingsScreen .closeb`…) qui battent une règle à deux classes, `!important` ou pas.
   Vu à l'écran : « ✕ FERMER » tombait **sous** le plateau. Les cotes sont donc posées
   **en ligne et en `important`** — ce que le §8 recommande nommément — et notées
   (`data-pose`).
3. **La compensation doit viser le VOISIN, pas la hauteur du titre.** Le plateau centre le
   titre verticalement : rendre au flux la hauteur du titre laissait **1,5 px** de
   resserrement sur l'Index. On mémorise l'ordonnée du premier élément qui suit et on règle
   la marge pour qu'il y revienne — c'est ce que la batterie mesure, donc c'est ce qu'on
   vise. Et **la marge peut être négative** : un plateau de 60 px à la place d'un titre de
   40 pousse tout de 20 px sinon.
4. **⚠ ON NE MESURE JAMAIS UN ÉCRAN HORS CHAMP.** C'est celui qui a coûté le plus cher. Un
   `.screen` fermé est translaté sous l'appareil : ses rectangles sont ceux d'un ailleurs.
   Mesurée là, la compensation sortait à **+52 px** sur Réglages — tout le contenu poussé
   hors du cadre, et `redteam_air` qui **perdait 56 paires**. Pas un resserrement : une
   **disparition**. *Un contrôle qui mesure moins n'est pas vert, il est aveugle.*
   C'est exactement le piège de `cale()` sur le Studio (Q133), et la parade est la même :
   on ne pose et on n'ajuste que sur un écran **visible**, transition finie.

**Ce que ça a évité.** Avant ce quatrième correctif, j'étais à deux doigts de refiger
`redteam_air` : le refigeage sortait une référence de **335 paires au lieu de 391** — il
aurait **effacé 56 mesures** au lieu de corriger un défaut. La discipline qui l'a rattrapé
est celle qui a déjà payé trois fois ce jour-là : **mesurer la référence sur la sauvegarde
d'avant le lot**. 391 avant, 335 après → le lot était en cause, pas la batterie.

**Les batteries, après correction :**

```
redteam_air     388 paires, AUCUN ÉCART — et la référence d'origine est intacte,
                aucune paire refigée, aucune supprimée
redteam_ecrans  150/150     redteam_vide     61/61     redteam_champ  32/32
redteam_filets  0 parasite  redteam_polices  0 absent
releve-design   ✅ AUCUN ÉCART
redteam_tonsurton 24/26 — la RÉFÉRENCE d'avant le lot est à 23/26 : le lot en corrige un.
                Cette batterie oscille (elle échantillonne des canevas animés, §7).
```

⚠ **Trois paires sur 391 ne sont pas mesurées** dans la passe (388/391) — c'est le bruit
habituel des états d'écran, et c'était déjà le cas avant. Je le note plutôt que de
l'arrondir.

---

#### Q139 · PARTAGER, SANS TRAIT — et la restauration d'abord

**Décision Tom, 1er septembre 2026 :** *« page partager c'est moche, ça donne pas envie.
Faut un bandeau Peaufiner et Inviter Partager, mais PAS DE TRAIT c'est moche, et juste le
sélecteur Ma Toile / Mes Promi visible, sinon faut Peaufiner. »*

**Pourquoi le trait part, et ce n'est pas un caprice.** Le §2.1 fait de l'onde **la
frontière entre le champ et le corps**. Sur le partage, il n'y a pas de corps : l'écran est
un **champ plein** qui porte un aperçu. L'onde n'y bornait rien — elle coupait l'écran en
deux pour rien. Elle part, le champ prend tout, et le §2.1 reste entier **là où il a un
sens**. On ne supprime pas une règle, on cesse de l'appliquer là où elle ne dit rien.

**⚠ ET LE LOT RESTAURE AVANT DE DÉPLACER.** L'audit avait trouvé un mode entier sans porte
et six commandes vivantes mais inatteignables. On ne range pas un écran dont un tiers est
mort.

```
DÉFAUT 1  le mode Noyau n'avait AUCUN bouton — `#sealShare` cherchait
          `#shMode button[data-mode=noyau]`, qui n'existait nulle part.
          → le bouton « Le Noyau » est CRÉÉ dans `#shMode`, à côté des deux autres.
DÉFAUT 3  `#shNoyauParts` (six commandes) était masqué en dur et jamais démasqué.
          → il s'ouvre dès que le mode Noyau est pris (`.shc-noyau`).
DÉFAUT 2  le sur-mesure plafonnait à 2160 alors que le clamp autorise 3840.
          → `shCustomClamp` est ENVELOPPÉE et rétablit l'état des `+` sur la vraie borne.
DÉFAUT 5  deux libellés « Format » à la suite — le premier coiffe `#shNoyauParts`.
          → il dit maintenant « Ce qu'il montre ». On corrige le MOT, pas le nœud.
```

**Les cotes, calculées, marge basse 36 :**

```
 40 → 100   le plateau : Partager · ✕ FERMER
120 → 570   l'aperçu
600 → 644   LE SUJET — Ma Toile · Mes Promi · Le Noyau  (la seule commande dehors)
674 → 736   la barre Peaufiner (62 px, §5) — elle ouvre tout le reste
746 → 808   Inviter | Partager
```

**Trois pièges rencontrés :**
1. **Le champ est découpé par un `clip-path`, pas borné par une hauteur.** Lui donner 844 px
   ne servait à rien tant que le tracé le rognait : la vague restait et le bas de l'écran
   restait crème.
2. **Les boutons du sujet sont dans `#shMode`, pas en enfants directs** de `#shcSujet` — un
   sélecteur `>` ne les atteignait pas.
3. **§8 · une mise en page posée par un lot est défaite sans qu'on y touche.** Le lot
   « feuille » reprenait `#shMode` quelques centaines de millisecondes après : mesuré, le
   sélecteur revenait à **0 × 0** hors de son plateau. Envelopper `shareRender` ne suffit
   pas — ce n'est pas le seul chemin. Un observateur repose, **et il compare avant d'agir**,
   sans quoi il se réveille lui-même.

**Les batteries :**

```
redteam_ecrans 150/150   redteam_vide 61/61   redteam_champ 32/32
redteam_geste   13/13    redteam_demande 19/19   redteam_filets 0 parasite
redteam_air    388 paires, AUCUN ÉCART        releve-design ✅ AUCUN ÉCART
```

⚠ **Un détail non réglé, et je le note plutôt que de l'arrondir :** le bouton actif du
sujet sort **sombre** au lieu de crème — la règle d'origine `#shMode button.on` gagne encore.
C'est lisible et le bouton actif se distingue, mais ce n'est pas la couleur voulue.
À reprendre.

---

#### Q140 · LE SAUT DU STUDIO — une mesure différée, pas une animation

**Relevé par Tom, 1er septembre 2026 :** *« quand on ouvre le Studio, la page saute vers le
haut puis revient, c'est pas fluide, le rendu c'est hyper cheap visuellement. »*

**La cause était à moi, et c'était le garde que j'avais posé la veille.** `cale()` mesurait
avec `getBoundingClientRect()`, qui donne la position **après transformation** : un
`.screen` arrive de sous l'appareil, donc tant que la translation courait la mesure était
fausse et le garde refusait de caler. À la fin de la transition, le calage tombait d'un
coup — et **tout le contenu sautait de 16 px**. Le garde évitait le faux placement ; il ne
pouvait pas éviter le saut, il le **causait**.

**La parade supprime la mesure au lieu de la protéger.** `offsetWidth` et `offsetHeight`
sont des cotes de **mise en page** : elles ignorent les transformations. Le décalage se
déduit donc de `(offsetWidth − 390) / 2`, dès le premier rendu, et ne bouge plus.

**Mesuré à l'ouverture, huit relevés entre 0 et 950 ms :**

```
t =  42 ms   cadre left 16px  top 16px
t = 171 ms   cadre left 16px  top 16px
   …
t = 952 ms   cadre left 16px  top 16px
```

Une seule valeur, dès la première image. Plus de garde, plus de mesure différée, plus de
saut. **Une animation qu'on ne voit pas est meilleure qu'une animation qu'on lisse.**

---

#### Q141 · L'ENCART EST LA RÉFÉRENCE — les pages s'y alignent

**Reproche de Tom, et il était fondé :** *« là c'est juste posé, mais t'as pas regardé s'il
fallait décaler d'autres éléments logiquement, harmoniser visuellement les pages. »* J'avais
posé l'encart et déclaré le lot vert sans regarder ce qu'il laissait en désaccord autour.

**LA GRAMMAIRE, une fois pour toutes :**

```
x = 24 · largeur = 342 · bord = 2 px · rayon = hauteur / 2 · padding = 26 · titre 27 px
```

**Le relevé AVANT, écran par écran — sept désaccords :**

```
Index      .ix-bar 319 de large (au lieu de 342) · .ix-srch rayon 999 et bord 2,5
Le Cercle  #buyMonth et #buyYear à 378 — PLUS LARGES que l'encart, rayon 16
Nuée       l'encart à 291 et x 50 (le padding de la feuille) · champs à rayon 0 et 4
Aura       les bascules à rayon 16, conteneur à bord 1 px
auraHelp   « Comprendre ton Aura » : 287 px pour 290 disponibles — à 3 px près
tous       le titre gardait la taille de SON écran : 38 px sur l'Index, 27 ailleurs
```

**APRÈS, mesuré sur les dix :** encart **342 à x 24**, titre **27 px**, et **tous tiennent** —
« Comprendre ton Aura » descend à 21 px pour entrer, par pas de 1 px, plancher 19.
L'Index a sa recherche et son tri **au même contour, au même rayon, à la même largeur
totale**. Le Cercle et la Nuée aussi.

---

#### Q142 · LES COINS — un enfant transformé n'est pas rogné par son parent

*« Ya des pages avec des coins blancs bizarres cheap. »* Mesuré :

```
#device        border-radius 22px · overflow hidden · fond #EFEAE0 (crème)
les 10 écrans  border-radius 0
```

Un enfant carré devrait être rogné proprement par un parent arrondi en `overflow:hidden`.
**Sauf qu'un `.screen` arrive par une TRANSFORMATION, et un parent ne rogne pas un enfant
transformé.** Les écrans dépassaient donc l'arrondi, et le crème de l'appareil apparaissait
aux quatre angles — sur un écran sombre, quatre coins clairs.

Les écrans portent désormais **le rayon de l'appareil (22 px)** : ils l'épousent au lieu
d'être rognés. Un rayon ne masque aucune commande — il ne relève pas du crible du §8.

**Les batteries :**

```
redteam_ecrans 150/150   redteam_vide 61/61   redteam_champ 32/32
redteam_geste   13/13    redteam_filets 0 parasite
redteam_air    388 paires, AUCUN ÉCART      releve-design ✅ AUCUN ÉCART
redteam_toile   plante sur un NaN — la RÉFÉRENCE d'avant le lot plante à l'identique.
                Défaut préexistant de la batterie, pas une régression.
```

---

#### Q143 · LA PASSE À L'ŒIL — un juge de collisions, et cinq trouvées

**Tom, 1er septembre 2026 :** *« ne dis pas c'est bon quand tout est encore en bazar. Ne
livre pas sans avoir 100 % vérifié que tu as tout fait, que tout est bien calé. »*

J'avais mesuré les dix encarts et déclaré le lot vert **sans regarder ce qu'ils recouvraient
autour**. Regarder dix écrans à l'œil sur une image réduite ne le montre pas de façon fiable
— alors le geste juste est de **faire mesurer à un juge ce que l'œil cherche** : les
chevauchements, les débordements du cadre, les textes sous 12 px, les opacités sous 0,72
(§6).

**Ce qu'il a trouvé, et qui était de moi — CINQ collisions, 342 px de large à chaque fois,
donc des lignes entières recouvertes :**

```
#arrangeSheet   .enh × .sub        342 × 15
#langScreen     .enh × .sub        342 × 17
#privScreen     .enh × .sub        342 × 17
#auraHelp       .enh × .keyebrow   342 × 13
#plusScreen     .enh × .pl-h       342 × 34
```

**La faute était dans ma compensation, et elle était de conception.** Je ramenais le voisin
à **son ancienne ordonnée** — mais le plateau fait 60 px là où le titre en faisait 40 : il
descendait donc plus bas que le titre et recouvrait un voisin resté en place. Le garde
« la marge peut être négative » que j'avais ajouté la veille **aggravait** le problème : il
tirait le contenu vers le haut, sous le plateau.

**Ce qu'il faut préserver, c'est l'ÉCART, pas la position.** Le voisin se repose sous le
plateau à la même distance qu'il était sous le titre. Le contenu descend de la différence
de hauteur — et c'est normal : un plateau prend plus de place qu'un titre nu.

**Après : aucune collision avec l'encart sur les dix écrans**, et `redteam_air` remonte de
**388 à 391 paires** — la couverture complète est revenue, ce que la compensation par la
position ne permettait pas.

```
redteam_air    391 paires, AUCUN ÉCART     redteam_ecrans 150/150
redteam_vide    61/61    redteam_champ 32/32   redteam_geste 13/13
redteam_filets  0 parasite   redteam_polices 0 absent
releve-design  ✅ AUCUN ÉCART
redteam_tonsurton  24/26 — la référence d'avant est à 23/26 (batterie oscillante, §7)
```

⚠ **CE QUE LE JUGE A TROUVÉ EN PLUS, ET QUI N'EST PAS DE MOI.** Des violations du §6
(« rien en dessous de 12 px, aucune opacité sous 72 % sur du texte lisible ») **préexistantes**,
sur cinq écrans :

```
Réglages    « Toi » « C'EST IMPORTANT ? » « LA MÉMOIRE » « The Studio »   11,5 px
Aura        « ta parole dans le temps » « tenues » « en cours »           10 px
            le « i » de l'info                                     opacité 0,42
Index       « TENUE » « À TENIR · 2 J » « LANCÉ » « EN COURS »            10 px
Nuée        « Nom de la Nuée » « Promesses de la Nuée »                   10-11 px
Le Cercle   « ou un design à l'unité »                        11 px, opacité 0,70
            #plHeroCv déborde le cadre : x −16, largeur 430
```

**Je ne les corrige pas dans ce lot, et je dis pourquoi :** ce sont peut-être des valeurs
relevées des cadres du moodboard, comme les amplitudes 44/46/48 l'étaient. Les changer sans
vérifier l'inventaire de chaque écran, c'est refaire l'erreur que Q136 a documentée — écraser
un relevé en croyant corriger un bug. **Chacun demande sa vérification contre son cadre.**

---

#### Q144 · DÉPLACER UN NŒUD LE SORT DE TOUS LES SÉLECTEURS QUI LE VISAIENT PAR SA PLACE

**C'est la cause racine du désordre que Tom voyait**, et elle explique d'un coup tout ce
qu'il a listé : *« les textes et éléments sont mal placés dans l'encart ou mal
proportionnés »*, le « 16 » qui changeait d'aspect, le titre trop gros.

**Le lot de la section 4 pose tout l'Index et le Fil EN ABSOLU**, aux cotes du cadre, et il
vise le titre par des sélecteurs à **enfant direct** :

```
#device #indexSheet.s4 > .scr-ti                  l'entête
#device #indexSheet.s4 > .scr-ti .ix-count        le compte
#device #indexSheet.s4 > .ix-bar                  la barre        top 108
#device #indexSheet.s4 > #indexList               la liste        top 196
```

**En déplaçant le titre DANS le plateau, il cesse d'être un enfant direct de l'écran :
ces règles ne s'appliquent plus DU TOUT.** L'entête et le compte ont perdu d'un coup leur
famille, leur graisse, leur taille et leur couleur. Et comme rien n'est dans le flux, mon
encart ne décalait rien : il se posait à 54 et **la barre de recherche le chevauchait de
6 px**.

**La règle générale, et elle vaut pour les quatre écrans qui restent :**
*déplacer un nœud, c'est le sortir de tous les sélecteurs qui le visaient par sa place.*
Avant de déplacer, il faut relever ce que la place lui donnait — et le rendre explicitement.

**Ce qui a été rendu :** Bricolage 700 pour l'entête et le compte, crème `#F4EEE1`
(et non `var(--on-ground)`, qui vaut `#E7E5DF` — deux crèmes voisines que le juge
distingue à juste titre), et `#3A54FF` pour le compte.

**Ce qui a été décalé, et pourquoi :** toute la colonne descend de **+16 px** — la
différence entre le plateau (60) et le titre qu'il remplace (44). Barre 108 → 124, liste
196 → 212. Sans ce décalage, le plateau recouvre la barre.

**MON ERREUR DE MÉTHODE, et elle est plus grave que le bug.** Je vérifiais en appelant
`_encartHaut()` et `_harmonie()` **à la main** et en forçant `.show` — donc je mesurais un
état **que je fabriquais moi-même**, et je le déclarais vert. Dans le parcours réel, celui
que Tom fait, rien ne tournait au bon moment. Les lots sont désormais branchés sur un
observateur de la classe `show` de chaque écran, et **toute vérification se fait en ouvrant
l'écran par son bouton**, jamais en forçant.

**Le résultat, mesuré en ouvrant l'Index normalement :**

```
encart      40 → 100   342 × 60   rayon 30   bord 2   titre 27 px
barre      124 → 176   342 × 52              écart de 24 px, plus de chevauchement
  recherche            270 × 52   rayon 26   bord 2
  tri                   52 × 52   rayon 26   bord 2
liste      212
```

⚠ **`releve-S4-index-fil.py` sort 62 écarts — 20 de style, 42 de position — et ils sont
TOUS voulus.** Ce juge n'a pas de `--figer` : ses cotes sont écrites en dur contre
`PROMI-SPECIFICATIONS §5`. **La décision de Tom change donc la spec**, et elle y est notée
en tête du §5, datée, avec le tableau avant/après — pas écrasée en silence. La version
d'avant du juge est dans `sauvegardes/releve-S4-avant-encart.py`. **Le juge lui-même reste
à mettre à jour** : tant qu'il ne l'est pas, il est rouge, et je ne le dis pas vert.


---

#### Q145 · LE FIL, C'EST `#feedView` — pas `#feedScreen`

**Deux erreurs de ma part, et la seconde explique la première.**

**1 · Je m'étais trompé d'écran.** `#feedScreen` porte bien un `h1` « Fil d'actu », mais il
**ne s'affiche jamais** (`show` toujours faux). Le Fil qu'on voit est **`#feedView`**, avec
la classe `.s4`, son titre `h2.fd-h2.scr-ti` (« Fil » + son compteur) et son propre
`#fdClose`. Mes règles de grammaire, elles, visaient bien `#feedView.s4` — donc **la barre
y était déjà passée à 124 et la liste à 212, mais sans encart** : un trou de 16 px en haut.
Les cotes étaient bonnes, l'écran était le mauvais.

**2 · Je devinais la visibilité par une classe.** `visible()` testait `show` — or le Fil
s'ouvre avec **`in`**. Un écran dont je ne connais pas la classe d'ouverture est un écran
que le lot oublie, en silence.

**La parade : on MESURE la visibilité, on ne la devine pas.** L'écran est visible s'il
occupe vraiment la place de l'appareil — display, visibility, opacité, et un recouvrement
d'au moins la moitié de la hauteur du cadre. Aucune classe à connaître, aucun écran à
oublier.

**Mesuré en ouvrant le Fil par son bouton :**

```
encart      40 → 100   342 × 60   rayon 30   bord 2   « Fil 4 » 27 px, FERMER dedans
barre      124 → 176   342 × 52              écart de 24 px
liste      212
```

Identique à l'Index, au pixel.

```
redteam_ecrans 150/150   redteam_vide 61/61   redteam_champ 32/32
redteam_air 387 paires, AUCUN ÉCART          releve-design ✅ AUCUN ÉCART
```

---

#### Q146 · DEUX FAMILLES — la loi qui règle le décalage clair-obscur

**Tom, 2 septembre 2026 :** *« il faut repenser l'harmonie et la cohérence visuelle de toute
la page, sinon ça fait un décalage clair-obscur entre les éléments… pas juste poser
l'élément mais l'intégrer dans son univers, ou en l'occurrence adapter le reste à lui. »*

Il avait raison, et le relevé le chiffre. **Ce qui coexistait sur l'Index :**

```
la page          #E8E0D0
l'encart         #F4EEE1 PLEIN  + contour 2 encre     rayon 30
la recherche     TRANSPARENT    + contour 2 #9A9384   rayon 26
le tri           TRANSPARENT    + contour 2 encre     rayon 26
une carte        #F4EEE1 PLEIN  sans contour          rayon 17
```

**Trois matières** (plein+bordé · vide+bordé · plein nu), **trois rayons**, et un
**filet gris `#9A9384`** que le §3 interdit sans appel : *« Jamais de trait neutre ou
gris. »* L'œil voit ça en une fraction de seconde ; la mesure le nomme.

**LA LOI, deux familles, chacune homogène :**

```
LES COMMANDES SONT DES PILULES    contour d'encre 2 px, fond transparent,
                                  rayon = hauteur / 2 — donc la MÊME forme perçue
                                  quelle que soit la hauteur
                                    l'encart 60 → 30    la recherche 52 → 26
                                    le tri   52 → 26    Peaufiner   62 → 31
                                    le sujet 44 → 22    Inviter/Partager 62 → 31
LE CONTENU EST UNE SURFACE        aplat crème, sans contour, rayon 17
                                    les cartes, les bandeaux
```

**Ce qui sonnait faux, c'était l'encart :** il était **le seul objet de la page à porter un
aplat ET un contour**. Une commande est un contour, un contenu est une surface — on ne
mélange plus les deux. Il perd donc son fond plein, dans les deux thèmes.

**Vérifié sur neuf écrans, en les ouvrant normalement :** Index, Réglages, Aura, Le Cercle,
Nuée, la confidentialité, la langue, Arranger, Comprendre ton Aura — **toutes les commandes
principales sont des pilules**, contour 2 px d'encre, fond nu.

**Et ça corrige un contrôle, ce qui prouve que ce n'était pas qu'une affaire de goût :**

```
redteam_tonsurton   23/26  →  26/26
```

Les bords `#9A9384` (clair) et `#5D636D` (sombre) de la recherche étaient bien des gris
sous le seuil. Le juge du ton sur ton les voyait depuis le début ; je les avais pris pour
une oscillation de batterie. **Ce n'en était pas une.**

```
redteam_ecrans 150/150   redteam_vide 61/61   redteam_air 387 paires AUCUN ÉCART
redteam_filets 0 parasite   redteam_tonsurton 26/26   releve-design ✅ AUCUN ÉCART
```

⚠ **Trois éléments restent hors de la loi, et ce sont des lignes, pas des commandes :** une
ligne de menu de tri sur l'Index (h 48), un petit libellé de l'Aura (h 29), un champ de la
Nuée (h 34). Une ligne de liste n'a pas à être une pilule — mais je les nomme plutôt que de
les passer sous silence.


---

#### Q147 · LA RÉFÉRENCE, C'EST LE PLATEAU DU STUDIO — et il est PLEIN

**J'avais reculé, et Tom l'a vu immédiatement.** En Q146 j'avais conclu « les commandes sont
des contours vides, les contenus des surfaces », et j'avais **vidé l'encart**. C'était faux :
la référence n'était pas une théorie à construire, elle existait déjà — **le plateau du
Studio** — et il est **plein**.

**Relevé sur lui, au pixel, et c'est la seule chose à copier :**

```
boîte      x 24 · y 40 · 342 × 60
fond       le CORPS du thème — #F4EEE1 en clair, #12142A en sombre
contour    2 px d'encre · rayon 30 (la moitié de la hauteur)
padding    26 de chaque côté
titre      Bricolage 700 / 27 · interlettre −0,035em · encre · à 28 du bord
fermer     ApfelMid 500 / 12 · interlettre 0,20em · à 28 du bord droit
```

**LA LOI, en une phrase :** *tout ce qui se touche en haut d'une page porte ce traitement.*
Aplat du corps **+** contour d'encre de 2 px **+** rayon = hauteur / 2. Ni contour nu — ça
flotte —, ni aplat sans contour — ça se noie dans la page.

**Ce que ça a demandé de fine-tuning, et c'est là qu'était le vrai travail :**

```
la page       #E8E0D0
l'encart      #F4EEE1   ← la crème du plateau, pas var(--ground)
la recherche  #EFEAE0 → #F4EEE1
le tri        transparent → #F4EEE1
les cartes    #F4EEE1   (déjà)
```

**Trois crèmes voisines coexistaient** — #F4EEE1, #EFEAE0 et du transparent — sur des objets
qui se touchent. C'est exactement le « décalage » que Tom décrit : l'œil le voit en une
fraction de seconde, et aucune de mes mesures ne le cherchait, parce que je comparais des
formes et pas des matières.

⚠ **`var(--ground)` N'EST PAS UNE COULEUR, C'EST UNE VARIABLE D'ÉCRAN.** Elle vaut
`#EFEAE0` sur l'Index et `#F4EEE1` sur le Studio. Écrire `background: var(--ground)` pour
« reprendre la référence » donne donc **une autre couleur** selon l'écran. Quand deux objets
doivent avoir la même matière, on pose **la valeur**, pas la variable.

**Vérifié en ouvrant l'Index normalement : les quatre objets sont à `#F4EEE1`.**

```
redteam_ecrans 150/150   redteam_tonsurton 26/26   redteam_vide 61/61
redteam_champ 32/32      redteam_filets 0 parasite
redteam_air 387 paires AUCUN ÉCART   releve-design ✅ AUCUN ÉCART
```

---

### Q148 · « Comprendre ton Aura » ne peut pas porter le 27 px du plateau — **à trancher**

**Mesuré**, plateau ouvert par sa porte, deux thèmes :

```
largeur du plateau            342
− 2 bords de 2 px               4
− padding 26 + 26              52
− « ✕ Fermer »               74,5
− l'écart entre les deux       18
                            ─────
disponible pour le titre    197,5

« Comprendre ton Aura » à 27 px   268 px      ne tient pas
                        à 20 px   198 px      tient, c'est le maximum
```

L'ajustement automatique fait donc son travail : **20 px est la plus grande taille qui
tienne**. Mais un titre à 20 au milieu de neuf à 27, l'œil le voit.

Trois sorties, et **aucune ne m'appartient** :
1. **On garde 20** — l'écran le plus bavard est le seul à faire exception.
2. **Un titre plus court** — mais un mot ne s'invente pas (§9), il vient de toi ou du
   moodboard.
3. **Le plateau s'allonge sur deux lignes** pour ce seul écran — ce serait une exception
   de forme, pas de taille.

Je n'ai rien tranché : le titre reste à 20 px, l'ajustement fait foi.

### Q149 · « % d'harmonie » était un orphelin de l'ancien partage — **rangé, à confirmer**

`#shNyPctRow` flottait **sur le plateau du titre** (y 58 → 87), à opacité 0,34, sur la
page Partager. Il n'est ni dans le tiroir neuf (`#shcPile`) ni sous une règle qui le
masque : il vit dans `#shTray`, l'ancien tiroir, laissé en **`display:contents`** — un
conteneur qui ne cache rien, puisqu'il n'existe pas pour la mise en page.

**Sa fonction n'est pas perdue** : le tiroir neuf porte « CE QU'IL MONTRE → Noyau ·
Orbite · Promitteurs · Disques · **Harmonie chiffrée** · Jauge équilibre » (`#shNoyauParts`).
C'est le même réglage, en mieux. Je l'ai donc rangé, et pas supprimé.

**À confirmer** : que « Harmonie chiffrée » du tiroir remplace bien « % d'harmonie », et
qu'aucun geste ne dépendait du bouton orphelin.

### Q150 · `redteam_toile.py` ne tourne plus — **antérieur, à réparer**

La batterie s'arrête sur `ValueError: cannot convert float NaN to integer`, au contrôle
« planter des Promi change l'aperçu » : le hachage de l'aperçu revient `NaN`. Vérifié sur
deux sauvegardes d'avant-lot — **c'est antérieur**, ce n'est pas ce lot qui l'a cassée.

Ce n'est pas un rouge, c'est un **aveugle** : seize contrôles de la Toile ne mesurent plus
rien. C'est exactement le motif du §7 (« un contrôle qui compte des pixels sur un canevas
mesure la respiration du monde ») — le hachage porte sur un canevas animé.

### Q151 · Le plateau défile sur trois écrans, pas sur les six autres — **à trancher**

**Mesuré**, chaque écran ouvert par sa porte, défilement à 400 px :

```
le plateau RESTE     Réglages · Index · le Fil · Arranger · la langue · la confidentialité
le plateau PART      Aura (40 → −360) · Comprendre ton Aura (40 → −360) · Le Cercle (40 → −121)
```

**La cause est structurelle** : sur ces trois écrans, **l'écran lui-même est le conteneur
qui défile**, et un enfant en `position:absolute` d'un conteneur qui défile part avec son
contenu. `position:fixed` n'y change rien — mesuré, il tombe à −360 pareil (l'ancêtre
transformé devient le bloc englobant).

**Ce lot n'a rien changé pour ces trois-là** : l'encart y était dans le flux avant, il
défilait déjà. La seule chose que j'ai introduite, c'est aux **Réglages**, où le plateau
est devenu fixe — et le contenu passait alors dans la bande au-dessus de lui. **Corrigé**,
par la parade de l'Index : `#stScroll` commence à 100, sous le plateau, et rogne.

**Ce qui reste à trancher, et je ne l'ai pas fait :** ✕ FERMER qui part avec le doigt sur
trois écrans, c'est une friction. La corriger demande de donner à ces écrans un conteneur
de défilement interne — une modification de structure, pas de style, sur des écrans que ce
lot ne devait pas toucher. **Je ne l'ai pas faite sans ton accord.**

### Q152 · Le plateau sur une fiche déroge à une phrase du §3 — **acté, à confirmer**

Le §3 écrit : *« La zone haute et ses éléments — mot-marque, FERMER — gardent le traitement
du moodboard sur couleur pleine (blanc). »* C'était juste **tant qu'ils étaient posés à nu
sur la bande de nature**. Dans un plateau crème, du crème sur du crème ne se voit pas : c'est
le ton sur ton que le même §3 interdit, et le seuil 42 le refuse.

**Ta règle d'or tranche** — « la cohérence dans toute l'app sur les éléments communs est une
règle d'or absolue » : le plateau est le même partout, ou il n'est pas commun. Le mot de
nature et le FERMER passent donc **à l'encre** sur une fiche, comme sur les neuf autres
écrans.

**Ce qui NE change pas :** la bande haute garde la couleur de sa nature, la dalle reste
dessus, le §4 est intact. C'est le plateau qui est posé **sur** la bande, comme au Studio il
est posé sur la Toile.

### Q153 · La croix SVG d'une fiche est masquée, pas supprimée — **à confirmer**

La fermeture d'une fiche était **composite** : une croix SVG de 58 × 58 avec « FERMER »
dessous, soit **58 × 77 de haut pour un plateau qui en fait 60**. Elle débordait par le haut
ET par le bas, et le mot tombait sous la boîte.

Dans le plateau, elle prend la forme des neuf autres écrans : une ligne, « ✕ FERMER », en
ApfelMid 500 / 12. **La croix SVG reste dans le DOM**, seulement masquée (§9 : on ne détruit
pas ce qu'on n'a pas décidé). Si tu la veux, elle revient en une ligne.

### Q154 · « Grossis un peu le reste » s'est arrêté au plancher — **et voici pourquoi**

Un facteur uniforme de **1,08** a resserré **156 paires de textes**, dont, dans l'Index,
`« planter un arbre » → « TENUE »` qui passe de **2 px à 0** : le titre touche sa ligne
d'état, sur les six cartes, dans les deux thèmes.

La cause est ta propre loi, §8 : **les cartes et les écrans sont en cotes ABSOLUES**
(`top: 124 / 141 / 174` pour une carte d'Index), calculées pour les tailles d'alors. Un texte
qui grossit ne déplace aucun `top` — sa hauteur grandit vers le bas et mange l'air.

**J'ai donc posé un PLANCHER, `max(13, taille)`, et pas un facteur** : il ne touche que ce
qui était trop petit — et un tiers du petit texte était **sous le minimum de 12 du §6**.
Résultat : **43 paires au lieu de 156, pire cas −1,5 px sur 55 à 68**.

**Pour aller plus loin — et c'est ta décision :** il faut **recalculer les cotes absolues,
écran par écran**, avec son juge à chaque fois. Dis-moi si tu veux que j'ouvre ce chantier,
et sur quels écrans en premier.

---

#### Q155 · LE PLATEAU DE LA PAGE + EST VIDE — **CORRIGÉ, 2 septembre 2026**

> **Traité dans le lot de la page +, sur consigne de Tom** : *« ne le laisse pas traîner.
> C'est le même défaut, la même cause, la même correction que Q152. »*
> **La cause n'était pas celle que j'avais écrite ci-dessous.** Ce n'est pas un oubli de
> conversion : deux peintres se disputaient le plateau, et le mauvais parlait en dernier.
> `enteteLisible` (§10.6, Q59) lit **le pixel du CANEVAS** sous chaque élément d'entête et
> choisit, des deux encres, celle qui s'en écarte le plus. C'était juste tant que l'entête
> était posé **à nu sur le champ**. Depuis que le plateau est l'entête de toute l'app
> (loi 1), il y a un **aplat opaque entre les deux** : le canevas dit bleu, le mot est en
> fait sur du crème, et la passe le peignait en crème sur crème. `encreUn` écrivait bien
> l'encre — mesuré au piège, il passe en second — mais `enteteLisible` repassait derrière.
> **Le correctif tient en une ligne** : cette passe ne juge plus ce qui vit dans un `.enh`.
> L'encre d'un plateau est l'affaire de `encreUn`, qui suit **le corps** ; `enteteLisible`
> ne juge que ce qui est posé **sur la matière**.
> **Mesuré après :** page + `rgb(22,23,27)` sur `rgb(244,238,225)`, fiche et Réglages
> inchangés, et **`releve-S3` passe de 28 défauts de peinture à 0** (14 écrans × 2 thèmes).

#### Q155 · LE PLATEAU DE LA PAGE + EST VIDE — le relevé d'origine

Trouvé en relevant les cotes avant le chantier du pinceau, **au pixel et pas dans la règle** :

```
#createSheet .enh        fond   rgb(244, 238, 225)   crème
#createSheet .cs-mark    color  rgb(244, 238, 225)   « Promi »
#createSheet .closeb     color  rgb(244, 238, 225)   « ✕ FERMER »
-webkit-text-fill-color  identique à color, opacité 1
```

**Écart de luminosité : 0.** La capture le confirme — le plateau de la page + ne porte
**aucun texte visible**, dans les deux thèmes (le corps de cet écran est crème quel que
soit le thème).

**C'est exactement le défaut de Q152**, qui l'a corrigé **sur la fiche seulement** : le §3
écrit « la zone haute et ses éléments gardent le traitement du moodboard sur couleur pleine
(blanc) », ce qui était vrai tant qu'ils étaient posés **à nu sur la bande**. Dans un plateau
crème, c'est du crème sur du crème. La page + est passée au plateau dans le même lot et n'a
pas reçu la conversion.

**Le correctif est celui de Q152, mot pour mot :** le mot-marque et le FERMER passent à
**l'encre du corps**. Rien d'autre ne bouge. **Je ne l'ai pas appliqué** — le chantier en
cours est le pinceau, et un lot = un écran (§9).

#### Q155 bis · « LE TRAIT » ou « LE PINCEAU » comme libellé de rangée — **à valider**

Les deux mots existent au produit, aucun n'est inventé. J'ai écrit **« LE TRAIT »** sur les
cadres, pour deux raisons :
1. **Q128 l'écrit ainsi** — *« À LA PAGE +, à la création : LE TRAIT du Promi qu'on plante »* ;
2. les neuf autres libellés de Peaufiner nomment **la chose réglée**, jamais l'outil —
   À QUI, AVANT, DANS UNE NUÉE, NOTE. Le pinceau est l'outil, le trait est ce qu'on règle.

« Pinceau » reste le mot du concept (CLAUDE.md §5) et de la conversation. Si tu le veux à
l'écran, c'est un remplacement d'une ligne.


---

#### Q156 · LE PINCEAU EST POSÉ — page + (emplacement B) et Peaufiner (variante D)

**Décision Tom, 2 septembre 2026**, après cinq cadres montrés :
*« B à la page + : sur l'écran où l'on écrit sa promesse, la phrase ne descend pas de 64 px
pour un réglage. D dans Peaufiner : on y reprend un choix déjà fait, on ne le découvre pas —
le grand aperçu, c'est à la page +. »*

**Ce qui a rendu la chose possible, et qui n'était pas acquis :** les douze tracés de
`PLANCHE-DOUZE-TRAITS.html` sont posés sur **l'onde du §2.1**, base 560, amplitude 36,
effilement 21,2 → 5,9. Vérifié numériquement avant d'y toucher : l'ajustement tombe à
**0,05 px** sur les 111 points de la ligne moyenne de « Plein ». Ce ne sont donc pas des
dessins libres, et on peut les reporter sur n'importe quelle onde **sans rien inventer**.

**On remappe la ligne moyenne, jamais la boîte.** Une simple mise à l'échelle verticale
(`y' = base + (y−560)·amp/36`) grossirait aussi **l'épaisseur** du trait : 22 px
deviendraient 28 sur la page +. Or l'épaisseur est une constante du §2.3. On soustrait donc
l'onde de la planche et on rajoute celle de l'écran :
`Y(x) = y_planche(x) − onde(560,36)(x) + onde(base,amp)(x)`.
**Contrôlé** : les douze matières rendues tombent sur l'onde à **0,4 à 1,0 px** en moyenne
pour Plein, Coulé, Fendu, Vrillé, Tressé, Sec ; les écarts plus grands (Doublé 6,5, Frangé
3,4, Peigné 3,2) sont la matière elle-même qui déborde sous la ligne, par construction.

**Le trait appartient à UNE parole (Q128), et c'est vérifié :** `p.trait` sur un Promi ou un
Chiche, une table par clé sur une Nuée, `p.trait` du brouillon repris sur un gardé de côté,
et le repli global seulement tant qu'aucune promesse n'existe pour le porter.
⚠ **`cur` et `curNuee` ne sont pas sur `window`** — ce sont des liaisons `let` de portée
globale. `window.cur` rendait `null` et le choix partait dans le repli global, c'est-à-dire
dans le réglage unique que Q128 refuse. Mesuré, puis corrigé : identifiants nus.

**Ce qui n'a PAS le pinceau, et pourquoi :** une carte d'Index et un bandeau du Fil gardent
leur trait plein. Leur vague fait **une période sur leur propre largeur** (§3.9), pas 1,5 sur
390 : y reporter la matière la poserait sur la mauvaise onde. Je l'avais branché puis retiré,
mesure à l'appui.

**Ce qui reste ouvert :**
1. **Le libellé** — « LE TRAIT » ou « LE PINCEAU » (Q155 bis, toujours à valider).
2. **Les huit traits à 0,50 €** ne sont pas achetables : ils s'essaient (Q128 §5) et le prix
   s'affiche sur la ligne du nom. Aucun paiement n'est branché.
3. **Le geste de couleur au doigt dans le Studio (Q125)** n'est pas fait.

#### Q157 · LA GRAMMAIRE DES CONTOURS VA JUSQU'À PEAUFINER — **FAIT, 2 septembre 2026**

> **Décision Tom :** *« fais la conversion dans le lot suivant, pas plus tard. Tu as raison de
> ne pas laisser une rangée à 2/32 parmi six à 3/22. Mais laisser deux grammaires dans le
> produit est pire : passe toutes les rangées de Peaufiner à la loi, d'un coup. »*
>
> **Converties :** `#detailPoster .s2-reg`, `#createSheet.pp-peauf .s2-reg` et `.np-carte`,
> sur les quatre natures et les deux thèmes — 64 → 32, 92 → 46, 104 → 52, 118 → 59, le
> bouton 62 → 31. La hauteur vient de **la classe** (ou de `PLAN` pour une Nuée), **jamais
> d'une mesure**. `.s2-cercle` n'est pas une rangée : c'est le conteneur des quatre réglages
> floutés, sans contour (§3.8) — on n'y a pas touché.
>
> **Deux pièges, mesurés :**
> 1. **`.s2-reg.s2-vide` (le compagnon d'un Chiche) pèse deux ids ET CINQ classes** — les
>    `:not(.dp-nuee)` et `:not(.dp-mode-nuee)` comptent. Une règle à deux ids et deux classes
>    perd, même en `!important` : « AVEC » est resté seul à 3 px. On reprend ses six
>    sélecteurs à l'identique ; à poids égal, c'est l'ordre du fichier qui tranche.
> 2. **LE CADRE NE SE SOUSTRAIT PAS — il a fallu rendre le pixel, trois fois.** Un trait de 3
>    à 2 rend 1 px de boîte de contenu sur chaque bord. Une rangée en `flex` centre son
>    contenu : rien ne bouge. Un **bloc padé** (`.s2-zone`, `.s2-vis2`) voit son contenu
>    remonter : padding 16 → 17, 0 → 1. Un nœud **cloué en absolu** (`.np-bas`, `.s2-zone
>    .s2-vis`) a son ancre sur le bord de padding, que le padding n'atteint pas : `bottom`
>    14 → 15, `left` 22 → 23. **Vérifié nœud par nœud, avant/après : 0 déplacé sur 47.**

#### Q157 · le relevé d'origine — **à trancher**

Relevé en posant la rangée du pinceau : `#settingsScreen .s2-reg` est passé à **2 px /
rayon 32** au lot de la grammaire, mais **`#detailPoster .s2-reg` est resté à 3 px /
rayon 22**. Le même composant porte donc deux contours selon l'écran, alors que la loi 2 dit
*« le cadre ne se soustrait pas — c'est le reste qui monte jusqu'à lui »* et que la règle d'or
veut la cohérence sur les éléments communs.

**Ma rangée suit ses voisines, pas la loi** : une rangée à 2 / 32 au milieu de six à 3 / 22
jurerait. La convertir toutes est **un lot à part**, avec son avant/après — il touche sept
rangées × trois natures × deux thèmes, et `releve-S2` encode 3 / 22.

#### Q158 · `etatsDeCarte` DÉFAISAIT SON AJUSTEMENT À L'AVEUGLE — **corrigé**

`redteam_air` est passé au rouge sur une seule paire : dans l'Index en thème clair,
`« le potager » → « 9 PROMI · 3 TENUS »` tombait de **5,5 à 2**. Ce n'était pas l'air qui se
resserrait, **c'était le texte qui grossissait** — 12,5 px au passage sombre, **16 px** au
passage clair.

**La cause :** `etatsDeCarte()` retire son propre inline **avant** de vérifier que la carte
est disposée. Appelée pendant que l'Index est fermé (`clientWidth` 0), elle rendait le mot à
sa taille naturelle de 16 px et sortait aussitôt, sans jamais le réajuster. Le défaut est
**latent** : il ne dépend que du moment où la passe tombe. Il ne s'est vu qu'en rejouant la
séquence de `redteam_air`, qui enchaîne 15 écrans **sur une seule page** — les autres
batteries ouvrent chaque écran sur une page fraîche et ne peuvent pas le voir. Même famille
que `redteam_vide`.

**Le correctif :** on ne défait rien tant qu'on ne peut pas redécider. Deux passages verts
depuis, 428 paires.


---

#### Q158 bis · LA VRAIE CAUSE : DEUX PROPRIÉTAIRES POUR UNE MÊME PROPRIÉTÉ

**Q158 n'était pas réglée.** `redteam_air` a continué d'osciller — vert, rouge, vert — et
**trois correctifs successifs n'y ont rien fait**, parce qu'ils visaient tous la mauvaise
passe : rendre l'ajustement idempotent, envelopper le moteur de l'Index, poser un
`ResizeObserver` de largeur. Aucun ne pouvait rien.

**Ce que la sonde a fini par montrer**, en instrumentant la batterie elle-même :

```
{fs: '16px', inline: '-', data-fs0: '16', data-cw: '140', cw: 140, sw: 180}
```

Un ajustement **calculé, puis effacé par un tiers**. Le tiers, c'est `echelle()`, le plancher
du texte : il retire son propre inline avant de relire (`data-ech`), **et son marqueur se pose
sur ces mêmes nœuds** dès que l'ajustement descend sous 13. Au passage suivant il retirait un
inline **qu'il n'avait pas écrit** ; la relecture trouvait 16 px, au-dessus du plancher, et
sortait aussitôt. Le mot restait à 180 px dans une carte de 140.

**Le correctif est un ordre, pas une garde.** `etatsDeCarte()` était appelée **en tête** de
`echelle()` — donc avant la boucle qui l'effaçait. Elle est appelée **à la fin** : le plancher
pose sa taille, l'ajustement la ramène dans la carte, et ce dernier mot reste. Plus le retrait
de `echelle` qui s'arrête à la porte d'un `.s4-et`.

**⚠ Et une exemption trop large coûte cher.** Ma première tentative sortait d'emblée sur ces
nœuds — le plancher ne s'appliquait plus du tout, et **`releve-S4` est passé de 0 à 34
écarts** : des états à 6,4 · 10 · 11 px, sous le minimum du §6. On ne saute que le RETRAIT,
jamais le traitement.

**⚠ Et une « taille naturelle » ne se fabrique pas.** J'ai un temps lu la taille de référence
en retirant l'inline — **et cet inline était celui du BÂTISSEUR de la carte** (11 px à trois
par ligne, 12,5 à deux). Le retirer faisait remonter à la valeur de feuille, 16, gardée
ensuite comme référence. `releve-S4` l'a pris : trois états à 16 et 15 px, hors fourchette.

**Vérifié : `redteam_air` trois passages verts d'affilée, `releve-S4` vert deux fois.**


---

#### Q159 · LE PARTAGE · L'IMAGE EST L'ÉCRAN — et cinq restaurations

**Décision Tom, 2 septembre 2026 :** *« L'image est l'écran, entière. Une ligne posée dessus
dit où l'on en est. On la touche, un panneau plein se pose avec les formats et les réglages,
l'image reste entière derrière. Aucun ✦, aucun flou, aucun encart du Cercle — le partage est
entièrement gratuit et personne ne doit pouvoir savoir que quelqu'un ne paie pas. »*

**LES COTES, calculées, marge basse 36 :**

```
  0 → 844   l'image, entière — elle EST l'écran   (elle faisait 233 × 415 au milieu)
 40 → 100   le plateau : Partager · ✕ FERMER      (loi 1 — il ne part jamais)
674 → 736   LA LIGNE : « Ma Toile · Story »       (loi 2 — trait 2, rayon 31)
746 → 808   Inviter | Partager
ouvert :  la ligne monte à 120 · le panneau 198 → 736, il défile · l'image reste derrière
```

**CE QUE L'AUDIT AVAIT VU, ET CE QUE J'AI MESURÉ AVANT D'ÉCRIRE UNE LIGNE.** Le panneau
était cassé de bout en bout — bien au-delà de ce que Q139 déclarait corrigé :

```
#shcPile               390 × 148  pour un contenu qui descendait à y 1109
#shNoyauParts          les six commandes SOUS LE PLI, par quelque chemin qu'on prenne
la rangée « LE SUJET » son libellé seul — les boutons avaient disparu
le plateau             masqué à l'ouverture : plus de ✕ FERMER, donc plus de sortie
```

**LES CINQ DÉFAUTS, ET CE QUI EN EST.**

1. **Le mode Noyau · sa porte** — le bouton existe (posé par le lot du 1er septembre), il
   marche. **Rien à faire.**
2. **La borne du sur-mesure** — vérifiée en poussant les `+` jusqu'à la butée : la largeur
   atteint **3840**, alignée sur l'export. La hauteur s'arrête à 2640 parce que le
   **garde-fou de ratio** de Q119 (`< 0,42`) l'y arrête — c'est la règle, pas la borne.
3. **Les six commandes** — `#shNoyauParts` était `display:flex` dans un parent `display:none`.
   Le panneau **défile** désormais, et elles sont atteignables. Mesurées : six pastilles de
   38, sous le libellé « CE QU'IL MONTRE ».
4. **Les deux gestionnaires orphelins** — `#shOptVis` et `.sh-opts` n'ont plus de nœud
   (0 chacun), et leurs gestionnaires sont gardés par un `if(nœud)` : **du code mort, pas un
   bug actif**. Nommés dans le lot pour que le prochain ne les prenne pas pour une fonction.
   **⚠ MAIS DERRIÈRE L'ORPHELIN, UNE FONCTION QUI N'ARRIVAIT PAS JUSQU'À L'IMAGE.**
   `#shOptVis` pilotait `shareVis` — les noms sur l'image. Le nœud est parti ; la variable
   est restée à `true`, et **`shareExport` la lit encore**. La commande vivante — « Avec
   texte / Sans texte » — écrit `shLabels`. L'aperçu avait été rebranché (chantier 39),
   **l'export ne l'avait pas été** : choisir « Sans texte » puis partager sortait une image
   AVEC les noms. Relié, et vérifié : `shLabels false → shareVis false`.
5. **« Format » en double** — le premier coiffe les six commandes ; il dit maintenant
   **« Ce qu'il montre »**. Le mot est corrigé, le nœud intact.

**⚑ DEUX PROPRIÉTAIRES, DEUX FOIS — c'est le motif de tout ce lot.**
`#shMode` : l'ancien lot le reprenait dans `#shcSujet` à chaque passe, la rangée « LE SUJET »
du panneau sortait vide, et comme le clic n'était plus dans `#shcPile`, le garde « un tap
ailleurs referme » **refermait le panneau quand on choisissait Le Noyau**.
`#shcBarre`, `#shcPeaufiner`, `#shPreviewArea` : les deux lots posaient les mêmes cotes avec
des valeurs différentes. **Mesuré : la barre à 700 dans un relevé direct et à 746 dans la
passe de `redteam` au même instant du parcours.** C'est cette instabilité qui a avalé une
sonde de contrôle et m'a fait croire, pendant trois essais, qu'un contrat ne mordait plus.
L'ancien lot s'arrête maintenant dès que `sh-plein` est posé.

**DEUX CONTRATS RÉÉCRITS, ET PROUVÉS CONTRE DE VRAIS DÉFAUTS** (la règle que Tom vient de
faire inscrire au §7) :

```
« rien ne traîne hors du tiroir »   l'aperçu est exclu — shBadge et shWordmark SONT l'image,
                                     ils ne traînent pas. Sonde : un nœud de commande égaré
                                     hors du tiroir → PRIS.
« aucun recouvrement »              l'aperçu sort de la pile : il passe DESSOUS, par décision.
                                     Les commandes ne se recouvrent toujours pas entre elles,
                                     et on vérifie EN PLUS que l'image tient l'écran entier.
                                     Sondes : barre remontée à 700 → PRISE ;
                                              aperçu réduit à 300 de haut → PRIS.
```

Original : `sauvegardes/redteam-avant-partage-plein.py`.

**⚠ CE QUE LE PARTI COÛTE, ET JE LE DIS.** L'image occupe 0 → 844 ; la ligne et les deux
boutons sont **posés dessus**, comme demandé. **Le mot-marque de l'image, en bas à gauche,
passe donc sous la ligne.** C'est le sujet même de l'écran — la signature du produit sur ce
qu'on partage. Le rendre visible demanderait soit de rogner l'image (jamais : c'est la
composition de quelqu'un), soit de la borner au-dessus de la ligne — et elle ne serait plus
« l'écran, entière ». **Je n'ai pas tranché : le parti est le tien, le coût est celui-là.**


---

#### Q160 · LES QUATRE ROUGES ANTÉRIEURS SONT LEVÉS — au niveau de la décision, prouvés

**Consigne Tom, 3 septembre 2026 :** *« les rouges antérieurs que tu traînes : S1 132, nuee 56,
S3 position 64, S5 19. Ils encodent la géométrie d'avant le plateau. Mets-les au niveau de la
décision, prouvés contre un vrai défaut comme les cinq précédents. »*

```
                avant    après   ce qu'ils encodaient
releve-S1        132   →    0    l'entête à nu (24/38) ; l'onde du trait codée en dur
redteam_nuee      56   →    0    le mot-marque à 24/38, hauteur 34
releve-S3         64   →    0    l'entête à nu, + deux cadres du geste recopiés bruts
releve-S5         20   →    0    l'entête à nu ; l'onde codée en dur (amplitude 44)
```

**LA DÉCISION QUI LES REMPLACE, dans les quatre cas : LA LOI 1.** Le plateau est l'entête de
toute l'app — 24 / 40 / 342 × 60, contour 2 px, padding 26. Le mot-marque vit dedans, à
52 / 56,5 ; le FERMER à droite, hauteur 12. Le nœud d'avant (`#dpTete .dpt-nat`) n'existe plus :
les « aucun nœud » et « ABSENT » n'étaient pas des écrans cassés, c'étaient des juges qui
cherchaient un nœud que la décision avait remplacé.
**Et les quatre juges vérifient désormais LE PLATEAU lui-même, au pixel** — sa boîte, sa
largeur, sa hauteur, la place de ses deux textes. Aucun ne le regardait avant.

**⚑ TROIS AUTRES CAUSES, TROUVÉES EN CHEMIN — et deux étaient de VRAIS DÉFAUTS.**

1. **`releve-S1` et `releve-S5` codaient l'onde du trait EN DUR** pour aller lire sa couleur
   au pixel. La vraie amplitude est **36**, pas 44 : la sonde lisait 8 à 14 px à côté du trait
   et rendait la couleur du CHAMP, ou `null`. Dix-huit écarts qui n'étaient pas des défauts
   d'écran mais d'instrument. **Les deux peintres du canevas déclarent maintenant leur
   composition** (`data-trait` = base, amplitude, couleur, mode) et les juges la lisent —
   c'est la doctrine du §7 : on compare la composition, pas la peinture.
2. **Le corps d'une fiche descend pour dégager le plateau — mais pas du même pas partout :**
   +16 sur quatre écrans, +12 sur « tenue », +20 sur « Chiche à deux ». **Encoder trois
   constantes aurait été truquer.** Ce qui EST une règle : le corps descend **d'un seul
   tenant**. Le juge mesure donc le décalage sur le premier bloc du corps et l'applique aux
   suivants — toute dérive RELATIVE est prise au pixel comme avant, et le décalage mesuré est
   publié dans le relevé. Le plateau et la barre Peaufiner, eux, restent vérifiés en absolu :
   ils sont cloués.
3. **UN VRAI DÉFAUT D'ÉCRAN, que je prenais pour un rouge de juge.** `redteam_nuee` signalait
   « Nuée ⨯ ✕ Fermer » sur le fil défilé d'une Nuée. C'était exact : la branche « défilé » du
   §13 reposait le mot-marque en `position:absolute` et le FERMER à `top:20` — **les cotes de
   l'entête d'AVANT le plateau**. Rendre le mot-marque absolu le sortait du flux ; le plateau
   se retrouvait avec un seul enfant en flux et `space-between` collait le FERMER **à gauche,
   par-dessus le mot**. Mesuré : « Nuée » à 50/62, « ✕ FERMER » à 52/64, et
   `elementFromPoint` au centre du mot rendant `closeb`. Corrigé : le plateau garde ses deux
   textes, le §13 continue de faire remonter l'encart, les Noyaux et le titre.

**⚑ ET UN JUGE QUI SE CONTREDISAIT LUI-MÊME.** `releve-S3` pose comme règle générale
`trace = boîte − 60` et `phrase = boîte + 6` — soit 348 et 414 avec une boîte de 408, ce que
l'app rend au pixel sur douze cadres. Ses **deux lignes du geste** avaient été recopiées
BRUTES du document (372 et 454) sans le même report de 10 px : elles demandaient donc à l'app
dix pixels de plus que partout ailleurs. **Vérifié avant de conclure : l'onde est la MÊME dans
les trois états du geste** (base 312, amplitude 36, boîte 408, mesuré sur `_ppEcran()`), et
l'app applique bien le décalage du geste (+14 sur le mot, +30 sur la phrase). C'est le juge
qui comptait deux fois.

**CHACUN EST PROUVÉ CONTRE UN VRAI DÉFAUT**, sondes posées puis retirées :

```
releve-S1      mot-marque décalé de 40 dans le plateau      → PRIS (6 écrans)
releve-S1      titre désolidarisé de 12 px                  → PRIS (6 écrans)
releve-S3      phrase descendue de 14 px de trop            → PRIS (2 écrans × 2 thèmes)
releve-S5      mot-marque décalé de 40                      → PRIS (6 cadres)
releve-S5      trait peint en magenta                       → PRIS
redteam_nuee   plateau descendu de 20 dans sa constante     → PRIS (24 écrans)
```

⚠ **Et deux sondes ont d'abord été AVALÉES** — battues par une pose en ligne, non manquées par
le contrôle. C'est le corollaire 4 de la règle des deux propriétaires : une sonde qui « n'est
pas prise » se vérifie avant qu'on accuse le juge.

Sauvegardes : `sauvegardes/releve-S1-fiches-avant-plateau.py`,
`releve-S3-page-plus-avant-plateau.py`, `releve-S5-instant-avant-plateau.py`,
`redteam_nuee-avant-plateau.py`.

#### Q161 · LE MOT-MARQUE DE L'IMAGE — tranché, et implémenté

**Tom, 3 septembre 2026 :** *« L'image reste entière. Le mot-marque passe sous la ligne, et
c'est bien. L'image est la composition de quelqu'un — on ne la rogne pas, on ne la borne pas.
La ligne est un état, pas un cadre : elle dit ce qu'on donne, et elle ne part pas dans
l'export. Si le mot-marque est masqué au repos, il réapparaît dès que le panneau s'ouvre et
que l'image recule. »*

**Il ne reculait pas — je l'ai implémenté.** Mesuré au doigt : au repos le mot-marque est à
y 741 et `elementFromPoint` y rend `shcBarre` (les deux boutons le couvrent, pas la ligne).
À l'ouverture, l'image passe à **90 %** et se cale par le bas à **740**, juste au-dessus des
boutons ; le panneau raccourcit à 198 → 700 pour libérer la bande. Le mot-marque remonte à
**32 / 713** et `elementFromPoint` y rend **`shWordmark`** — il reparaît, vérifié au doigt.
Rien n'est rogné, rien n'est borné.

#### Q162 · « LARGEUR » ET « HAUTEUR » N'ÉTAIENT PAS CENTRÉS — corrigé

Relevé par Tom sur capture. Mesuré : la boîte fait 140, son contenu 104 centré à x 118 — mais
le libellé était en `text-align:start` et partait du bord gauche à 66, et la valeur flottait
dans son span de 35 px sans y être centrée. Tout le reste de la carte est centré ; ces deux-là
ne l'étaient pas. Corrigé : libellé centré sur toute la largeur, valeur en `flex:1` centrée
entre les deux boutons. Vérifié : span 98 → 138, centre 118 = centre de la boîte.


---

#### Q163 · LE RYTHME SOUS LE TRAIT — le mot du geste était à 65 px de sa vague

**Relevé par Tom sur capture, 3 septembre 2026 :** *« des problèmes de mise en page sous le
trait dans les fiches — "en cours" est trop proche de la ligne du dessus, "trace pour tenir"
trop loin du trait. Harmonise partout. Jamais de mauvaises mises en page, de superposition. »*

**LE RELEVÉ, EN AIR D'ENCRE** — bandes de pixels, pas boîtes (le PNG décodé à la main, PIL
n'est pas sur la machine) :

```
                        avant    après
trait  → mot du geste    65,0  →  26,3     ← le défaut
mot    → disques         27,0  →  27,0
disques→ à qui           22,5  →  26,5
à qui  → titre           15,0  →  20,0
titre  → état            30,0  →  30,0     ← inchangé, voir plus bas
état   → commentaires    31,5  →  31,5     ← inchangé
```

**LA CAUSE : tout était posé sur la BOÎTE, pas sur le TRAIT.** `e.boite` vaut
`base + amp + 40` — ces 40 px sont le padding du canevas SVG, pas un écart de dessin. Or le
trait ne descend jamais jusque-là : **son point le plus bas vaut exactement `base + 0,45·amp`**
(y(t) atteint son maximum en t = 1/2, où sin(3πt) = −1, une seule fois sur [0,1] ; vérifié :
base 286, amplitude 36 → 302,2, relevé à l'écran 302). Le mot se retrouvait donc à 65 px sous
la vague — le plus grand vide de l'écran, pour le lien le plus serré qui soit : **le mot NOMME
le geste juste au-dessus de lui.**

**ET CE N'EST PAS LE TRAIT QUI LE REPOUSSAIT, C'EST LA MARGE DE TOUCHE.** `#tenirZone` occupe
**244 → 362** — les 118 px du §5 — pour un tracé dont l'encre s'arrête à ~307 : **55 px de
marge vide sous le dessin**. Le §5 protège le GESTE, « toujours entier, jamais rogné ni
superposé » : c'est son TRACÉ qu'on ne recouvre pas. Sa marge de touche reste au-dessus en
z-index (4 contre 2) — le doigt continue de l'atteindre, rien ne lui est volé.

**⚠ ET JE N'AI PAS RESSERRÉ SOUS LE TITRE.** J'avais d'abord ramené `titre → état` de 30 à 26
et `état → commentaires` de 31,5 à 26 « pour harmoniser ». **C'était le contraire de ce qui
est demandé** — « en cours est TROP PROCHE » veut dire plus d'air, pas moins. `redteam_air`
l'a refusé sur-le-champ, quatorze paires. Les deux sont rendues. Le rythme du bas (30 · 31,5)
est plus large que celui du haut (26 · 27) : c'est une hiérarchie — serré autour du geste,
ample autour de la lecture — pas un défaut.

**Ce qui reste variable, et pourquoi ce n'est pas de la mise en page :** `titre → état` mesure
23 à 29,5 selon le titre. La cote est constante ; c'est l'ENCRE qui bouge, selon que le titre
porte une descendante ou non — « courir dimanche » n'en a pas, « ramasser les courges » si.
La chasser reviendrait à mesurer une cote sur elle-même, ce que le §8 interdit.

#### Q164 · `redteam_superpo` — la batterie du « jamais de superposition »

Neuve, née de la même exigence. Elle balaie **tous** les textes de **tous** les écrans, sans
liste de nœuds : le filet qui attrape ce qu'aucun inventaire ne prévoit. Résultat sur l'app :
**0 recouvrement, 13 écrans × 2 thèmes.**

**⚠ ELLE M'A EU DEUX FOIS AVANT D'ÊTRE JUSTE, et les deux pièges sont écrits dedans :**
1. **`elementFromPoint` ne rend que le dessus.** Exiger d'y trouver LES DEUX nœuds rend le
   contrôle **impossible à satisfaire, donc mort** : une sonde qui superposait l'état et le
   titre sur les six fiches n'était pas prise. C'est `elementsFromPoint`, au pluriel.
2. **La pile contient ce qui est DERRIÈRE.** Un écran fermé vit encore dans le DOM : sans
   coupe, le titre « Promi » de la Toile comptait comme recouvrant chaque fiche — **138 faux
   sur 13 écrans**. On coupe la pile au premier fond opaque.

C'est la règle du §7 appliquée à la lettre : *un contrat se prouve contre un vrai défaut,
sinon il ne mesure plus rien.* Prouvée dans les deux sens.

---

#### Q165 · L'AURA — LES MOTS, À TRANCHER D'UN COUP

> Mis à jour après la décision du parti A. **Les partis B et C sont abandonnés : leurs mots
> propres sortent de la liste.** Ce qui suit est l'intégralité du texte des trois écrans
> retenus — `PLANCHE-AURA-RETENU.html`. « existant » = déjà dans l'app ou dans le document.

**L'écran gratuit**

| | le mot | d'où il vient |
|---|---|---|
| 1 | `Aura` · `✕ FERMER` | existant (§3.1) |
| 2 | `ta parole dans le temps` | existant — `.keyebrow` de l'app |
| 3 | `solide` (et `rayonnante` · `installée` · `naissante` · `à tisser`) | existant — `harmonyWord()` |
| 4 | `harmonie` **67** | **NEUF dans sa FORME.** L'app écrit `HARMONIE 67 %` ; le `%` en fait une note sur cent, le nombre nu une mesure. Voir Q166. |
| 5 | `tenues` · `en cours` · `à tenir` | existant — `.klegend` |
| 6 | `il y a 8 semaines` · `aujourd’hui` | existant — `#kxaxis` |
| 7 | `avec qui` | **NEUF** — remplace « Par personne · à qui tu tiens parole » |
| 8 | `Partager mon Noyau` | repris **mot pour mot** de la fiche d'aide, qui l'annonce en gratuit |

**Ce que le Cercle ajoute**

| | le mot | d'où il vient |
|---|---|---|
| 9 | `ta moitié` · `la leur` | **NEUF** — la légende des deux moitiés du trait |
| 10 | `nuée par nuée` | **NEUF** — remplace « Par Nuée · touche pour déplier » |

**La page du Cercle**

| | le mot | d'où il vient |
|---|---|---|
| 11 | `Le Cercle` | existant |
| 12 | `Ta parole, vue des deux côtés.` | **NEUF** — le titre |
| 13 | `✦ Le Cercle` | existant — imposé par le §3.8 |
| 14 | `ce que tes proches tiennent envers toi` | **NEUF** — le sous-titre de l'encart |
| 15 | `ce qu’il ouvre` | **NEUF** |
| 16 | `réciproquement` · `le temps` · `Nuée par Nuée` | **NEUF** — les trois vignettes |
| 17 | `29 €` · `soit 2,42 €/mois · −39 %` | **la forme imposée par Tom**, mot pour mot |
| 18 | `Prendre l’année` | **NEUF** |
| 19 | `ou 3,99 €/mois · 14 jours d’essai · annulable à tout moment` | **NEUF** |

**Douze mots neufs sur dix-neuf lignes.**

**Ce qui est RETIRÉ, et qu'il faut savoir avant de trancher :** « % de parole tenue » ·
« Ta meilleure Nuée » · « Stats avancées » · « Les graphs » · « rayonne / se tisse / à
raviver » · « série » · « ↑ en hausse cette semaine » · « toi 80 % / eux 33 % » · « tu portes
un peu plus en ce moment » · « Aperçu gratuit / Aperçu membre » · « Rappels intelligents » ·
« Toiles signature » · « près de cinq mois offerts ». Tous relèvent du rendement, du classement
ou de la forme de prix interdite (§C et §E de `AUDIT-AURA-CERCLE.md`).

#### Q165 bis · Le mot du Noyau — VÉRIFIÉ, aucun n'est un reproche

Décision Tom : on le garde, si aucun ne blesse. Les cinq, relevés dans `harmonyWord()` :

```
rayonnante   ≥ 85   éloge franc, sans superlatif ni comparaison
solide       65-84  constat calme ; le seul épicène des cinq
installée    40-64  elle a pris racine — ni éloge ni reproche
naissante    < 40   LE CAS LE PLUS BAS, et il dit « ça commence », jamais « tu as échoué »
à tisser     rien de résolu — l'état vide
```

**L'échelle est monotone** (naissante → installée → solide → rayonnante) : aucun mot ne sonne
plus fort que celui qui le suit, ce qui est le piège habituel de ces échelles.
**Une réserve, mince :** « à tisser » est **une consigne, pas une description** — le seul des
cinq qui demande au lieu de constater. Sur un écran vide c'est le bon registre. Gardé, signalé.

#### Q166 · Le chiffre unique — pourquoi « harmonie 67 » et pas « 67 % »

La règle anti-notation dit : *un seul chiffre, le tien, global, visible de toi seul.* Le signe
**%** en fait une note sur cent ; le nombre nu, précédé du mot, en fait une mesure d'harmonie.
C'est la même valeur, ce n'est pas la même lecture. **Décision prise seul, à confirmer.**

#### Q167 · `#demoTg` et `#karmaCercle` — deux outils d'auteur restés dans le produit

`#demoTg` (« Aperçu gratuit / Aperçu membre ») et `#karmaCercle` (qui appelle `setPremium(true)`
**avant** d'ouvrir la page de vente) permettent de voir l'écran des deux côtés sans payer. Aucun
cadre ne les dessine, aucune décision ne les valide. **Aucune des trois planches ne les porte.**
Si ce sont des outils de démonstration, ils sortent au moment de l'intégration ; si Tom les veut,
ils reviennent — mais alors ce sont des fonctions, et elles se dessinent.

---

### LE PORTAGE DE L'ORBITE DANS L'APP · 10 septembre 2026 — `lot-AURA-ORBITE`

#### Q168 · `Toile.dalleGeneree` n'existe pas dans l'app — les îles prennent la VRAIE dalle du Promi — **à valider**

`batIles` (planche) appelle `Toile.dalleGeneree`, un ajout du 9 septembre **dans la copie du moteur**
(`scratchpad/toile-extrait.js`) — jamais dans `app.html`. L'y ajouter, c'était toucher le code de la
Toile (§9 et consigne du lot). **Option la plus sobre retenue :** dans l'app, une île EST un Promi réel,
qui a déjà sa dalle — `Toile.dalleTrame(cv, id, 1, p.monde)`, la règle 1 du §4, API publique, qui
respecte déjà les trois champs `{m,p,h}` du monde de plantation. Une seule retouche dans `batIles` :
la source de la dalle (`opt.dalle`) ; sans elle, le chemin de la planche est intact.

Ce que ça change à l'œil, et il faut le savoir : la **forme** de l'île est celle de la vraie cellule du
Promi sur la Toile, plus une cellule taillée pour l'île ; la **taille** reste celle de la planche (le plus
grand côté calé sur la cellule `g` de l'île) ; sur un monde à trame, `dalleTrame` coupe les marques au
bord (demi-pois) — c'est la dalle que montre toute l'app (fiche, Index). Si Tom veut la cellule taillée
de la planche, il faut porter `dalleGeneree` DANS le moteur : c'est une décision de moteur, pas de portage.

#### Q169 · « Le geste qui relisse tout » — deux touchers rapprochés sur la sphère — **VALIDÉ par Tom, 10 septembre 2026**

> *« C'est discret, ça ne s'active pas par accident, et ça n'ajoute aucun élément à l'écran. »*

Aucun document ne nomme le geste (ÉTAT : *« Un geste remet le velours à neuf »*). Retenu : **deux
touchers à moins de 350 ms**. Un toucher seul creuse, résiste et revient (acquis 4) ; deux touchers
rapprochés relissent.

#### Q170 · Les vraies données — sept réglages pris au plus sobre — **à valider**

1. **« Ce que tu as tenu »** = MES Promi (`from` moi), ni gardés de côté, ni demandés (`req`), statut
   `tenu`. La parole tenue d'un autre envers moi n'y est pas.
2. **L'ordre des îles est l'ordre d'APPARITION**, gardé (`localStorage` `promi_orbite_ordre`) et jamais
   recalculé : l'accrétion rend l'île k dépendante des k−1 précédentes, trier par id ferait bouger les
   anciennes. Au premier passage : par id.
3. **La nature** : un Promi dans une Nuée compte « Nuée » — y compris la Nuée « Moi-même » (`NUE.soi`),
   qui en est une dans les données. Égalité : l'ordre du §3 (Promi, Chiche, Nuée). Zéro : bleu (tranché).
4. **Le mot** : `MOTS[n % 5]` — il change en faisant plus, jamais au hasard d'une ouverture.
5. **Zéro parole tenue, des Promi en cours** : le mot est *« La première parole laissera sa trace
   ici. »* et « Ce que tu as tenu » disparaît (un titre posé sur rien serait un bloc vide). La légende
   perd alors sa déclaration de centrage — elle n'a plus deux voisins.
6. **L'état vide** = aucun Promi du tout (la planche : « Zéro Promi »).
7. **« Ce que tu as tenu »** montre les trois dernières, la plus récente d'abord, et **ne s'ouvre pas**
   (aucune fonction dessinée) ; **toucher « toi »** n'ouvre rien (il n'y a pas de fiche de soi).

#### Q171 · Les caresses se gardent — neuf au plus — **l'inscription AU REPOS est VALIDÉE par Tom, 10 septembre 2026**

> *« Une saccade au lâcher aurait cassé le seul moment où l'objet doit paraître vivant. »*
> (La garde — `localStorage`, neuf au plus — reste à confirmer avec le reste du lot.)

`localStorage` `promi_orbite_traces`, les neuf dernières (« neuf caresses », planche). Une caresse est
**le chemin du doigt SUR L'OBJET** — ce qui glisse sous la pulpe pendant qu'on tourne (la surface va
1,56 fois plus vite que le doigt, rapport de la planche du 5 septembre) — au diamètre du doigt
(0,27 rad). Même régime que `promi_state` : rien côté serveur.

**Et elle s'inscrit AU REPOS, pas au lâcher** : doigt levé, élan éteint, creux refermé. Inscrire une
caresse oblige le peintre à refaire tout son cache (une image de ~300 ms sur le Mac du banc) ; au
lâcher, cette image tombait pile quand l'élan est le plus fort — une saccade, que le juge a prise.
Au repos elle tombe pendant la rotation lente (1,3 pt au bord de la boule). La trace apparaît donc
quand la forme est revenue — ce que dit la planche : *« ce qui reste, c'est le poil couché »*.
⚠ Sur un appareil lent, ce recalcul reste un arrêt bref de la rotation lente : le supprimer demande
un recalcul PARTIEL (seulement les poils proches de la caresse) — lot à part.

#### Q172 · LE PEIGNE TOURNE AVEC L'OBJET — deux acquis qui se contredisaient — **à valider**

Sur la planche, le peigne `B` est la direction horizontale de L'ÉCRAN, prise à la vue du moment où le
peintre remplit son cache : ses deux zéros tombent aux limbes, invisibles. **Mais l'Orbite tourne
toujours**, et le cache ne se refait que quand les données ou les caresses changent :
- un quart de tour plus tard (~41 s), **un zéro — un épi, la « couronne » refusée — arrive au centre de
  la face** (capture `scratchpad/aura/peigne_comparaison.png`, rangée du haut) ;
- chaque caresse refaisait le cache à la vue du moment : **toute la fourrure changeait d'orientation au
  lâcher du doigt**. Mesuré à vue égale : une caresse changeait **77 %** des pixels, et un relissage
  laissait **7,8 %** de résidu.

**Retenu : un peigne azimutal autour de l'axe de rotation** (`u = y × p`). Vérifié par le calcul : au
centre de la face il vaut exactement le `B` de la planche, même sens ; il ne dépend plus de la vue ; ses
zéros sont aux pôles de l'axe, que la rotation lente ne ramène jamais de face (on ne peut les amener
qu'en inclinant au doigt, jusqu'à 66°). Après : une caresse change **9,2 %** (la caresse seule), un
relissage revient à **0,0000**. Deux lignes dans `_v_peint.js`, sous une option (`peigneAxial`) ; la
planche garde son chemin.

#### Q173 · La rotation de repos : **UN TOUR EN 2 MINUTES** — décision Tom, 10 septembre 2026 ; la valeur est mienne, **à valider à l'œil**

> Tom : *« La rotation est un peu trop lente. Accélère-la à peine — juste assez pour qu'on sente que ça
> tourne quand on regarde l'écran quelques secondes, sans que ça devienne agité. Elle doit rester
> contemplative. »* Retenu : **2 min** (0,0524 rad/s, ×1,4), entre les 2 min 45 d'avant et les 84 s déjà
> jugées trop vives. Au centre de la face, la surface passe de 4,4 à 6,1 pt/s. Le juge porte la valeur
> décidée EN DUR (il ne la lit pas dans l'app). L'élan s'additionne toujours à la rotation lente : le
> raccord reste continu par construction, et le contrôle de continuité le prouve à la nouvelle valeur.

*Rédaction d'origine, avant la décision :* la rotation de repos : 2 min 45, pas les 50 s du banc.

`banc_lent.py` tournait à 0,0021 rad par image (≈ 50 s le tour) : c'est un rythme de BANC — le coût
d'une image ne dépend pas de la vitesse. La décision écrite est **2 min 45** (ÉTAT, 5 septembre :
*« c'est le geste qui accélère, pas elle »*). Et le **tour d'arrivée** d'une parole de plus est un élan
de constante **1,1 s** : la planche n'en donne pas la durée, seulement le principe (« le levier est le
geste »).

#### Q174 · La pulpe, recalculée pour la boule de l'écran : a = 0,40 — **à confirmer**

*« La taille de l'empreinte se calcule, elle ne se choisit pas »* : 46,4 pt de demi-axe de pouce pour une
boule de 116 pt de rayon (296 × 0,392) — et non 170,8 pt comme sur la planche. Donc **a = 0,40** (index
0,26 : ce sont les bornes), et la cuvette `(2/π)·asin(a/r)` porte jusqu'à 1,2 rad : sous le pouce,
presque tout le disque visible cède un peu. C'est la loi, appliquée à une boule plus petite. Si Tom juge
l'enfoncement trop large, le levier est le diamètre de la boule, pas la pulpe.

#### Q175 · `#auraHelp` décrit encore l'ancienne Aura — **hors lot**

« Le grand chiffre — ton % de parole tenue », « La jauge d'équilibre », « Ta meilleure Nuée », « Les
graphs », « Les disques… selon la Nuée » : plus rien de tout ça n'est à l'écran. Réécrire l'aide, ce sont
des mots neufs — à Tom.

#### Q176 · `#demoTg` et `#karmaCercle` (Q167) sortent avec l'ancienne Aura — **à confirmer**

Masqués avec elle, nœud par nœud. Aucun cadre ne les porte. S'ils doivent revenir, ils se dessinent.

#### Q177 · « CE QUE TU AS TENU » : l'opacité .60 de la planche devient une teinte pleine — **tranché par le §6**

Le §6 interdit toute opacité sous 72 % sur un texte lisible. Même teinte que la légende (`#A8A396`
sombre, `#6B6658` clair) : c'est, au point de luminance près, ce que .60 produisait sur ce fond
(152 contre 163 en sombre, 109 contre 102 en clair).

#### Q208 · UNE COMPOSITION D'ÉCRAN N'EST PAS UN SEMIS — **TRANCHÉ par Tom, 12 septembre 2026**

> **Tom :** *« La règle du déterminisme régit la Toile d'un Promi et d'une Nuée, pas une composition d'écran. »*

Le §4 de CLAUDE.md pose qu'**un semis est déterministe** : *« Même Nuée, même semis. À chaque ouverture, dans les deux
thèmes, sur n'importe quel appareil : quelle dalle occupe quelle case, et où, ne change jamais. »* La raison y est
écrite : *« une Toile qui changerait de composition entre deux ouvertures ne serait plus la Toile de CETTE Nuée. »*

**L'écran qui vend fait exception, et l'exception est dans la raison même de la règle.** Sa Toile n'est celle de
personne : c'est une **Toile de démonstration**, engendrée, *« ce qu'une Toile peut devenir, pas ce qu'il a »*
(Tom, 12 sept.). Elle ne représente aucun Promi, aucune Nuée, aucun état — elle ne peut donc pas « ne plus être la
sienne ». Et le produit y gagne ce que la règle protège ailleurs : **on rouvre le Cercle, c'est une autre Toile.**

**Ce que l'exception couvre, nommément :** le semis (positions des germes), les couleurs tirées dans la palette du
Studio, la matière de chaque cellule parmi les huit mondes, et la densité. **Ce qu'elle ne couvre pas :** rien
d'autre. La Toile d'un Promi, celle d'une Nuée, l'Orbite de l'Aura et toute vue qui REPRÉSENTE des données restent
déterministes, et `scratchpad/semis_determin.py` continue de les contrôler.

**Corollaire pour les juges :** un contrôle qui compare deux ouvertures de l'écran qui vend doit vérifier qu'elles
**diffèrent**, jamais qu'elles coïncident. C'est l'inverse du contrat du §4, et c'est voulu.

#### Q207 · FRAUNCES AU TITRE ET AU PRIX DE L'ÉCRAN QUI VEND — **DÉCISION ASSUMÉE (Tom, 12 septembre 2026)**

Complète **Q194**, qui avait relevé que Fraunces n'apparaît qu'à trois endroits (le mot-marque, le mot de nature d'une
fiche, et `#ixCount`) et que les titres d'écran sont en Bricolage 700.

**L'écran qui vend y déroge, et c'est décidé, pas dérivé :** « Le Cercle » en **Fraunces 600 · 32 px** et « 39 € » en
**Fraunces 600 · 40 px**. Tom, 12 sept. : *« Fraunces au titre et au prix : assumé, c'est une décision. »* Le reste de
l'écran suit le produit — libellés **Bricolage 600**, bouton **Bricolage 700**, textes **Apfel 400**.

**Ce que ça n'ouvre pas :** aucun autre écran ne prend Fraunces pour son titre. Q194 reste vraie partout ailleurs, et
l'écart de TAILLE du mot-marque (§5 dit 20 px, l'app peint 27 et 29) reste à trancher avec le chantier des polices.

#### Q206 · LE « 1 € · 4 POUR 3 € » DU STUDIO — **NE PAS Y TOUCHER POUR L'INSTANT (Tom, 12 septembre 2026)**

En passant l'abonnement à **39 € l'année / 5,99 € le mois**, j'ai cherché toutes les mentions de prix : quatre
portaient l'abonnement (`.pl-sub`, `#buyMonth`, `#buyYear`, et le lot de l'écran qui vend). Une cinquième n'en est
pas : **« ou un design à l'unité — 1 €, ou 4 pour 3 € »**, et le rotateur du Studio (« Adopte ce design — 1 € »).

> **Tom :** *« C'est un autre produit, et il va changer — les trois mondes du Cercle deviendront exclusifs, l'unité
> portera sur les autres. Note-le. »*

**Donc :** ces mentions ne sont PAS alignées sur le nouveau prix, volontairement. Quand la décision tombera, l'unité
ne portera plus que sur les cinq mondes gratuits (Encre, Mosaïque, Touffe, Braille, Pixel) et Sillons, Gravure et
Terrazzo deviendront **réservés au Cercle** — ce qui changera aussi ce que l'écran qui vend peut promettre.

#### Q205 · L'ÉCRAN QUI VEND PREND LE BAS DE LA PLANCHE — **TRANCHÉ par Tom, 11 sept. (soir)**

> *« Oui, prends le bas de la planche. Trois mondes en vraies dalles, « 29 € » en grand, « Prendre l'année » en premier. C'est
> l'écran qui porte le revenu : il doit montrer ce qu'on achète, pas l'expliquer en cinq lignes. »* — *« Les vraies dalles,
> rendues par le moteur, dans les trois mondes payants — Sillons, Gravure, Terrazzo. Pas un visuel. C'est la matière qui vend,
> c'est ce qu'on a appris au Studio. »* — *« l'essai de 14 jours reste visible, sous « Prendre l'année ». »* — *« Ne fige pas
> releve-design tant que l'écran qui vend n'est pas refait. »*

**Ce qui est posé** (`lot-CERCLE-VEND-css` réécrit + script `lot-CERCLE-VEND`, `sauvegardes/audit-cercle/patch_vend_planche.py`) :
- **le bas de la planche, ses cotes au pixel** (`ecran_qui_vend` de la planche 2/AB) : dalles 98 × 98 à 24 / 146 / 268, noms à 238,
  « 29 € » (Bricolage 700 / 56) à 276, « soit 2,42 €/mois · −39 % » à 342, **« Prendre l'année » plein à 386, « Essayer 14 jours,
  puis 3,99 €/mois » en contour à 464**, les deux notes à 548 / 574. **Le bloc remonte sous le plateau à 132** — la cote où la
  planche posait son premier bloc (les réglages, que Q204/Q205 ne reprennent pas). Rien ne défile.
- **Les vraies dalles** : `Toile.dalleTrame(src, id, 1, monde)`, échelle 1, le monde courant avec seul `m` changé (sillons,
  gravure, terrazzo) — comme la planche. **Les Promi : les trois derniers plantés de l'utilisateur** (déterministe) — sa propre
  matière dans le monde qu'il achèterait, pas les n° 129 / 134 / 125 du jeu de démonstration. Une dalle se rend une fois par Promi
  et par monde ; posée sans être étirée. L'app publie ce qu'elle a composé (`window._vendDalles`).
- **Les boutons** : les mêmes nœuds (`#buyYear`, `#buyMonth`) — leurs achats et le chemin « par-dessus » du mur sont les leurs ;
  « Prendre l'année » perd son prix (écrit en grand juste au-dessus), le libellé de la planche.
- **Masqués, nommément** : le visuel (`#plHeroCv`), le titre, la phrase, les cinq lignes, et **l'ombre de dalle du fond**
  (`.tuto-fond::before`, vue derrière les dalles à la capture — §4, règle 6 : jamais de dalle en fond animé sur un écran qui
  montre des dalles de référence ; retirée sur cet écran seulement).
- **Lisibilité des dalles, mesurée** (`vend_dalles_de.py`, 8 chargements, les couleurs sont tirées au hasard) : ΔE au fond de
  **66 à 84 en sombre, 48 à 112 en clair** — plancher 15.

**Sans aucun Promi — TRANCHÉ par Tom (11 sept., nuit) :** *« cache la rangée et remonte le prix. Trois cases vides sur l'écran qui
vend, c'est pire que pas de dalles du tout — ça dit « il n'y a rien à montrer ». »* Posé (`patch_vend_vide.py`) : la classe
`plv-sans`, posée d'après les DONNÉES (aucun Promi planté), cache dalles et noms ; le bloc remonte de 144 (prix 132, « Prendre
l'année » 242, essai 320, notes 404 / 430), dans la foulée de l'ouverture (aucune image ne montre la rangée vide). Vérifié et
prouvé (`preuve_vide.py`). Tom ajoute : *« c'est le mauvais cas d'usage à protéger […] si tu trouves un chemin qui mène au Cercle
depuis un état vide, note-le »* → **chantier 74** : quatre portes y mènent sans passer par un Promi.

#### Q204 · L'ÉCRAN QUI VEND : `#plusScreen`, UNE SEULE VERSION — corrigé, pas redessiné — **ma lecture, à confirmer**

> *« Pas d'écran A ou B, j'ai confondu. L'écran qui vend est cercleScreen, celui qui porte le prix et le bouton — c'est
> celui-là que les murs doivent atteindre, et il n'y a qu'une version. »*

**Ce que j'en ai lu.** `cercleScreen` n'existe nulle part — ni dans `app.html`, ni dans un document, ni dans une planche (grep
sur tout le projet). L'écran qui porte le prix et les boutons est **la page du Cercle, `#plusScreen`** (AUDIT-CERCLE A1). Les murs
y mènent déjà : fiche, page +, gardé de côté (par-dessus), Réglages, Studio, accueil — vérifié à l'écran. **Je n'ai donc rien
redessiné** : A et B de `PLANCHE-CERCLE-AB.html` étaient deux versions d'un écran neuf, et « il n'y a qu'une version ».

**Ce que j'ai corrigé, parce que l'écran ne VENDAIT pas** (mesuré le 11 sept., `sauvegardes/audit-cercle/vend_avant.py`) :
- **en clair, le prix et les boutons ne se lisaient pas** — « Prendre l'année — 29 € » **1,09**, « Essayer 14 jours, puis
  3,99 €/mois » **1,16** (blanc sur crème), les deux montants de la phrase **1,09**, « ta » et « l'inverse » 1,09 → encre ;
- **en sombre, « soit 2,42 €/mois · −39 % » bleu sur encre, 3,36** (ton sur ton, §3) → crème, comme le reste du bouton ;
- **la forme du prix** : « soit près de cinq mois offerts » → **« 29 € · soit 2,42 €/mois · −39 % »** (ta forme, message 1) —
  la seule phrase du fichier qui écrivait « mois offerts » ;
- **la marge** : titre, phrase et liste à x 6 de l'appareil → **24**, comme les boutons (l'écran vit hors de `#device`, §8).
- **le contour des deux boutons, en clair** : crème sur crème (écart de luminosité 0) — le texte se lisait, le BOUTON ne se
  voyait plus (vu à la capture, pas par ma première vérification, qui ne mesurait que le texte : contrat ajouté, prouvé sur
  la version d'avant). → l'encre, trait 2, comme toute pilule en clair (§5).
- **« soit 2,42 €/mois · −39 % » dans le bouton, en clair** : il héritait l'encre du bouton en REMPLISSAGE et gardait sa
  couleur bleue (deux valeurs, interdit du §3) → l'encre. Un bouton, une encre, dans les deux thèmes.
Bloc `lot-CERCLE-VEND-css` + une phrase, en fin de fichier. Aucun mot neuf.

**La question qui reste** : veux-tu que cet écran prenne le bas commun de la planche (les trois mondes en vraies dalles, « 29 € »
en grand, « Prendre l'année » en premier) à la place du visuel et des cinq lignes d'aujourd'hui ? Tant que tu ne l'as pas dit,
il garde son contenu.

#### Q203 · LA BASCULE DU RAYON : 94,5 — la règle est de Tom, le seuil est MESURÉ — **TRANCHÉ, 11 sept.**

> *« Applique ta piste : rayon = moitié de la hauteur jusqu'à deux lignes, 30 au-delà. Un champ à une ligne garde sa pilule,
> un champ qui s'ouvre gagne l'air qu'il lui faut. La loi du §2 tient là où elle a du sens, et cède seulement là où elle
> produit un défaut. Mesure le seuil exact — à quelle hauteur la pilule commence à manger le texte — et pose la bascule là,
> pas à un nombre de lignes arbitraire. »*

**La règle posée : rayon = hauteur ÷ 2 jusqu'à 94,5 de haut, 30 au-delà.** Elle remplace Q202 §1 (une règle de CLASSE :
« trois lignes et plus → 30 »). Un seul propriétaire : `rayon()` dans `lot-CERCLE-MUR` ; la Nuée l'appelle.

**Comment le seuil a été mesuré** (`sauvegardes/audit-cercle/seuil_encre.py`, `_analyse`, `_bascule`) — sur l'ENCRE : chaque
champ de Peaufiner capturé (fiche, page +, Nuée, note ouverte à 4 et 5 rangées) ; pour tout rayon, la distance exacte de
l'encre la plus proche à la courbe intérieure du contour (l'encre ne dépend pas du rayon : le calcul est exact).
- **« Manger »** = serrer l'encre plus que ne le fait un champ OUVERT au rayon 30 (P, validé) : son air le plus serré vaut
  **C = 15,19** (NOTE de la page +, la ligne de visibilité ; 15,75 sur la fiche, 16,75 sur une Nuée).
- **Un champ à deux rangées qui s'ouvre** (rangée du haut à sa place, rangée du bas clouée au bas — la loi de `caleZone`)
  tient C en pilule jusqu'à **94,53** (PIÈCES JOINTES de la page +, le plus serré), 96,21 (Nuée), 105,95 (fiche). ⇒ **94,5**.
- **Les champs réels tombent nettement de part et d'autre** — air de l'encre en pilule : 64 → 19,3 à 22,7 (la ligne passe
  par l'axe : jamais mangée) · 92 → 15,7 à 18,0 · **104 → 10,7** · **118 → 6,3 / 7,2** (LE TRAIT d'une Nuée : **1,6**) ·
  140,5 → 1,7 · 163 → **−3,0** (la courbe coupe la ligne). Au rayon 30 : 15,2 à 16,8 sur tous les champs ouverts.
- **Pourquoi pas un nombre de lignes :** c'est la place de la PREMIÈRE rangée qui décide. Composée comme une NOTE (libellé à
  20,4 du haut), une pilule mangerait dès 85,75 ; comme PIÈCES JOINTES (29,9), à 94,5. La bascule vaut pour les compositions du
  produit ; tout champ neuf qui la contredirait est pris par les contrats (`releve-S2`, `verif_seuil.py`).
- **Ce qui a bougé à l'écran :** LE TRAIT d'une Nuée (118) passe de 59 à 30 — son libellé n'est plus contre la courbe
  (chantier 67 en partie). Tout le reste garde son rayon : 64 et 92 en pilule, 104 et plus à 30, comme sous Q202.
- **Mes instruments, dits :** le premier mesurait des BOÎTES de ligne et fusionnait le libellé de gauche avec la valeur de
  droite (« 0 fichier », à 23, donnait son haut à « PIÈCES JOINTES », à 26,4) : le coin mesuré n'était celui d'aucun texte.
  Remplacé par l'encre. LE TRAIT d'une Nuée est EXCLU de l'étalon C : même au rayon 30 sa rangée de pinceaux reste à 11,1 à l'écran
  (12,9 sur l'analyse ; elle est à 14,25 du bord droit) — un défaut de composition, chantier 67, pas un étalon.

#### Q202 · LES CHAMPS À TROIS LIGNES : P (RAYON 30), PAS T — et cinq autres décisions du même tour — **TRANCHÉ par Tom, 11 sept.**

> *« Prends P, pas T. Ta mesure tranche : T ne tient qu'à trois lignes et devient impossible à quatre. Un correctif qui ne
> marche qu'à un nombre de lignes précis n'est pas un correctif. Le rayon à 30 tient l'écart constant sans toucher à
> l'interligne — applique-le partout, y compris sur les écrans du mur où tu avais mis T. »*

1. **P** : tout champ de trois lignes et plus (libellé, texte, ligne de visibilité) prend le **rayon 30** du grand panneau de
   la grammaire — NOTE, COMMENTAIRES (fiche, page +), DESCRIPTION et COMMENTAIRES d'une Nuée. Les champs d'une et deux lignes
   gardent rayon = hauteur ÷ 2. Chantier 65 fermé par cette décision.
2. **Le chantier 68 dans le même lot** (*« c'est le même problème de géométrie »*) : le champ grandit d'une ligne (22,5) par
   ligne de texte, le haut du texte ne bouge pas, la ligne de visibilité descend avec la boîte.
3. **« ajoute un mot, un contexte… » centrée entre le haut et le bas du contour** — *« mesure les deux écarts, ils doivent
   être égaux »* : 46 / 46 (fiche, page +), 39 / 39 (Nuée).
4. **L'ordre des réglages payants : récurrence · rappels · importance · mémoire** — *« la mémoire […] est la plus abstraite
   des quatre, elle ne vend rien en tête de liste »*. (Remplace l'ordre de la planche 3, qui mettait l'importance en dernier.)
5. **Le bandeau du Peaufiner de la page + (chantier 64) n'est pas corrigé dans ce lot.**
6. **Le pinceau (chantier 69) est un lot à part, après le Cercle.**
Reste ouvert : **A ou B** pour l'écran qui vend (`PLANCHE-CERCLE-AB.html` les décrit en toutes lettres).

#### Q201 · LE LIBELLÉ DU MUR : « ✦ Le Cercle », SEUL — **TRANCHÉ par Tom, 11 sept.**

> *« Le libellé : « ✦ Le Cercle ». […] il nomme l'offre, pas son contenu, donc il ne périme pas quand le contenu bouge.
> C'est déjà le principe du Studio. »*

L'encart du mur porte **« ✦ Le Cercle »** et rien d'autre : le sous-titre de contenu (« importance, récurrence, rappels,
mémoire », §3.8) sort. ⚠ Écart assumé au §3.8 de la spec, qui dessine titre + sous-titre : la décision de Tom le remplace.
**Le sujet du lot, dans ses mots :** *« il ne s'agit pas de corriger un mur, il s'agit d'en poser un là où il n'y en a pas.
Les quatre réglages doivent exister, visibles et verrouillés, dans le Peaufiner d'une fiche et de la page +. C'est là
qu'on les découvre, c'est là qu'on veut les obtenir. »*
**Mesuré le même jour, pour que la décision repose sur le vrai :** sur une FICHE, le mur existe déjà — un Promi planté
à neuf (141) montre le bloc dans son Peaufiner, 342 × 304, quatre réglages floutés, encart net, deux thèmes, comme le
Promi 126 (`sauvegardes/audit-cercle/verif_mur.py`). Ce qui n'existe nulle part, c'est la FONCTION (réglages inertes,
même payés). **Sur la page +, le mur manque** : confirmé. Le gardé de côté rouvre la page + : voir `verif_garde.log`.

#### Q200 · LES LIBELLÉS DU STUDIO RESTENT TELS QUELS — **TRANCHÉ par Tom, 11 sept.** (annule le point 1 et 2 de Q117)

> *« Conserve-les tels quels. Ils sont ancrés dans l'offre — « Adopte ce design · 1 € » et « Ou débloque-les tous · avec
> Le Cercle ». Ils disent deux choses différentes de « ✦ Le Cercle », et ils vendent mieux que lui à cet endroit précis. »*

`#stLockBuy` et `#stLockCta` gardent leurs libellés et leur place (l'adoption au repos, Q106, reste donc telle quelle).
Noté pour ne pas le perdre : le rotateur de `#stBuyTx` tire aussi « Nouvelle trame ? — 1 € » et « Débloque-le — 1 € » ;
« tels quels » le garde. (Tom a cité « Q200 » : la question n'existait dans aucun document — inscrite ici avec sa décision.)

#### Q196 · LE CERCLE — CE QUE L'AUDIT NE TRANCHE PAS (11 sept.) — **ouvert** · détail dans `AUDIT-CERCLE.md` § G

1. **L'encart du §3.8 en sombre ne se lit presque pas** : la spec y pose le texte dans la teinte de la dalle sur crème —
   **#AE86F2 → contraste 2,42** (Promi, Réglages), **#F2977A → 1,92** (Chiche). CHANTIERS §10 : « terracotta et mauve ne
   passent pas en texte sur fond clair ». Deux règles se contredisent : **garder la spec, ou foncer la teinte de l'encart ?**
2. **Les blocs d'Aura que le Cercle ouvre — graphes, évolution, réciprocité — n'existent pas sur l'Orbite.** Ils sont à
   dessiner DANS l'Aura avant que la page du Cercle puisse les montrer voilés. (Le second anneau du §2.9 et la proposition
   « les anneaux des personnes ne se doublent pas », ETAT l. 6065, ne sont pas tranchés.)
3. **Le Peaufiner de la page + porte-t-il le bloc du Cercle ?** « Un réglage vit là où vit ce qu'il règle » range
   importance, récurrence, rappels à la création ; le moodboard ne dessine pas cet écran ; l'app ne le monte pas.
4. **« ou un design à l'unité — 1 €, ou 4 pour 3 € »** : aucun achat groupé n'existe, et il n'y a que trois mondes payants.
5. **Les pinceaux (0,50 €) et les codes couleur de palette** sont-ils dans le Cercle ? PLANCHE-STUDIO dit les pinceaux
   « hors du Cercle » ; le brief du 11 sept. ne cite ni l'un ni l'autre.
6. **Où mène `#cercleTopBtn` pour un abonné ?** Aujourd'hui : la page de vente. Aucun écran « membre » n'est dessiné.
7. **« Réinitialiser (test) » et « Membre du Cercle »** : outil d'auteur (donne le Cercle) et libellé que l'abonné ne voit
   jamais — à retirer ou à dessiner.

#### Q195 · UNE SEULE FICHE PAR PERSONNE — LES CHEMINS, TOUCHÉS AU DOIGT (11 sept.) — **cinq chemins manquants → CHANTIERS n° 63 · une question ouverte**

Tom : *« il n'y a qu'une seule fiche par personne, quel que soit le chemin […] Si un endroit affiche une personne sans y
mener, note-le — c'est un chemin manquant, pas une seconde fiche à créer. »*
**Relevé :** chaque nom et chaque visage visibles, touchés UN PAR UN au doigt, l'écran rouvert à neuf avant chaque toucher,
sur douze écrans — Aura, Index, Fil, fiche d'un Promi, de deux Chiche, d'un Promi planté par Rachel dans la Nuée, de la
Nuée, de la personne, Peaufiner d'un Promi / d'un Chiche / de la Nuée, partage. Thème sombre seulement (une porte est un
gestionnaire de toucher, pas une couleur — pas rejoué en clair). Outils et journaux entiers :
`sauvegardes/audit-fiche-personne/chemins/`. *(Une première passe dédoublonnait les visages par classe et n'en touchait
qu'un — celui de « toi » — sans le savoir ; la seconde les touche tous, identifiés.)*

**Aucun chemin n'ouvre autre chose que LA fiche.** Tout toucher qui mène à une personne ouvre `#psCadre[data-fiche=nom]`,
la fiche refaite — jamais l'ancienne. Portes vivantes : le visage et le nom sur l'Aura (Marion, Rachel) ; le disque d'une
personne sur la fiche d'un Promi (Rachel), d'un Chiche (Marion, et Rachel sa compagne), d'un Chiche de Nuée (Adrien). Dans
le code : le gestionnaire des disques (l. 4891) essaie `ouvrirPersonne` — qui n'existe pas — puis `openPerson` ; son dernier
recours (l'ancienne fiche via `renderPerson`) est mort, `renderPerson` n'existe pas. **Seul autre écran « d'une personne » :
`#profileScreen`** (`openProfile`, l. 3593), ton propre profil (tenu, raté) — **aucun appel, inatteignable**. Ce n'est pas
une seconde fiche d'une autre personne ; il rejoint le mode « moi » sans porte.

**Affichent une personne et n'y mènent pas — les chemins manquants (CHANTIERS n° 63) :**
1. **La Nuée — le vrai trou.** Sa fiche écrit « Avec Rachel, Adrien, +3 » (`.dpt-qui`) : touché, rien. Et **aucun disque
   de membre** : sa rangée ne porte que la Nuée. **Depuis une Nuée, aucun chemin ne mène à ses membres.**
2. Peaufiner d'une Nuée : « Rachel · Adrien · +3 » (`.np-val`) → rien.
3. La fiche d'un Promi ou d'un Chiche : la ligne « À Rachel », « À Marion · avec Rachel » (`.dpt-qui`) → rien. Les disques,
   juste en dessous, mènent.
4. Peaufiner d'un Promi ou d'un Chiche : la valeur « Rachel », « Marion » des rangées (`.s2-val`) → rien. (« visible par
   Rachel » est un réglage de visibilité — un toucher le bascule — pas un chemin.)
5. **« toi »** : visage et nom sur l'Aura, disque « toi » en tête de chaque fiche → rien. Le mode « moi » sans porte, déjà
   relevé (AUDIT-FICHE-PERSONNE § B bis).

**Affichent une personne, et le doigt ouvre la PAROLE — la question :** le Fil (visage `.s4-vis`, « Marion te lance un
chiche », « Adrien a planté », « Marion a relevé », « à Rachel »), la carte d'Index (« à Rachel », « à Marion ») et les
cartes de la fiche de la personne. Touchés, ils ouvrent **la fiche du Promi** : ce n'est pas une seconde fiche, c'est le
toucher de la carte (§5 : « un toucher bref ouvre sa fiche »). **Le nom et le visage d'une carte doivent-ils devenir une
porte à part, dans une carte qui est déjà une porte ?** Le plus sobre, appliqué : rien ne change ; noté.

> **Tom (11 sept., suite) : « enchaîne sur 63 ».** Il le décrit comme « le peintre de cartes chargé seulement dans
> l'Index, et les deux openPerson orphelins du Fil et de la fiche d'un Promi ». **Vérifié dans le code, dit sans
> polémique :** aucun `openPerson` orphelin dans le Fil ni dans la fiche d'un Promi — les appels vivants sont les disques
> d'une fiche (l. 3356, 4900) et les Noyaux de l'Aura (l. 28584) ; les seuls morts sont dans l'ancienne Aura masquée
> (l. 6320, 6322, 6510). Le moteur des cartes (`_s4Index`) ne bâtit bien que dans `#indexList`, mais la fiche d'une
> personne l'EMPRUNTE déjà et ses cartes sont peintes (juge, famille présence). **Le 63 reste les chemins ci-dessous.**
> **Appliqué au plus sobre** (la forme proposée à Tom, sans objection) : les noms écrits dans `#dptQui` et `.np-val`
> deviennent touchables et mènent à `openPerson` — aucune forme neuve ; **pas** la rangée « À QUI » du Peaufiner d'un
> Promi (elle accueille le champ qui change le destinataire : un toucher y règle), **pas** « toi », **pas** les cartes
> (la question ci-dessus reste ouverte).
> **✔ Tom (11 sept.) : « La rangée "À QUI" sans porte : validé. Elle sert à régler le destinataire, pas à naviguer. »**

**Ne montrent personne :** le partage d'un Promi à Rachel ; la fiche d'un Promi planté PAR Rachel dans la Nuée
(« reprendre l'arrosage automatique ») — son autrice n'y paraît nulle part, seul le disque « toi ».
**Pas joué au doigt, lu dans le code :** les pastilles de personnes de la page + (choisir le destinataire) et celles des
membres dans l'édition d'une Nuée (`#esMembers`, avec ✕ et `data-rm`) — des choix, pas des chemins.

#### Q194 · FRAUNCES HORS DU MOT-MARQUE — CE QUE L'APP EMPLOIE VRAIMENT (constat, 11 sept.) — **noté, non corrigé**

Tom : *« Le titre d'un écran n'est pas le mot-marque — si l'Index et le Fil l'emploient pour leur titre, c'est le §6 qui
est mal écrit ou l'app qui a dérivé. Ne le corrige pas ici, mais dis-le clairement. »* **Mesuré sur cinq écrans**
(accueil, Index, Fil, Aura, fiche d'un Promi — police calculée de chaque texte visible) :
- **Les titres de l'Index et du Fil ne sont PAS en Fraunces** : Bricolage 700 · 27 px, comme l'Aura (« Index », « Fil »,
  « Aura »). Sur ce point le §6 et l'app sont d'accord.
- **Fraunces n'apparaît qu'à trois endroits :** le mot-marque « Promi » (`.cs-mark`, 600 · **29 px**) ; sur une fiche, le
  mot de la nature en tête (`#dptNat` « Promi », 600 · **27 px**) — c'est le mot-marque qui dit la nature, voulu (§5, page +
  l. 17377) ; et **`#ixCount` « 16 » sur l'accueil (600 · 32,7 px) — un CHIFFRE en Fraunces : le seul emploi hors du
  mot-marque. Défaut préexistant probable** (chantier de polices, pas cette fiche).
- **Et un écart de taille** : le §5 donne au mot-marque **20 px** ; l'app le peint à 29 et à 27. À trancher avec le
  chantier des polices.

> **Tom (11 sept.) : « Le §6 est juste, l'app le respecte, et je m'étais trompé. »** Sur Fraunces, rien à corriger. Reste
> ouvert l'écart des LIBELLÉS de carte en Bricolage 600 → CHANTIERS n° 61 (chantier de polices, sur tout le produit) ; la
> fiche de la personne suit les cartes : **Bricolage 600 sur ses libellés** (titres de section compris).

#### Q193 · LA FICHE DE LA PERSONNE — CE QUI RESTE (réponses de Tom, 10 sept.) · deux mots À VALIDER, une donnée qui manque

> **✔ Tom, 11 sept. : « Q193 "Tenu ensemble" : validé. »** Les deux mots sont désormais validés (« + Lancer un Chiche »
> l'était déjà). Le juge `releve-fiche-personne.py` porte le titre en dur, marqué validé.

> **11 sept. — INTÉGRÉ (`lot-FICHE-PERSONNE`, Tom : « Go, intègre »).** La fiche de la planche 4 est dans l'app ; les deux
> gestes ouvrent la page + la personne déjà choisie (vérifié au doigt, jusqu'au Promi et au Chiche plantés) ; juge
> `releve-fiche-personne.py` (254 contrôles, prouvé contre l'app d'avant et deux sondes). Reste ouvert ici : **« Tenu
> ensemble » à valider.** Chapitre en tête d'ETAT-DES-LIEUX.
> **11 sept., fin — TITRE RETENU par Tom : « Ce que vous partagez »** (l'équivalent de « Ce que tu as tenu », il couvre les
> trois natures, et dit ce que la liste contient ; « vous » = toi et cette personne). **La typographie suit les cartes
> d'Index** (Tom : « elles font foi ; une fiche avec une autre typographie serait un troisième système ») : titres de
> section dans les petites capitales de l'Index et du Fil (ApfelMid 500 · 13 · 0,18 em). ⚠ Mises au point : il n'existe ni
> Q195 ni Q196, ni classes `.iq-when` / `.iq-eyebrow` / `.iq-sub` (0 occurrence dans app.html et dans tout le dossier) ;
> sur la carte d'Index le sens (« à Rachel ») est en **Bricolage 600 · 16**, le temps en **ApfelMid 500 · 13** capitales —
> aucune Apfel 400 sur une carte (mesuré). La carte est gardée telle quelle.

> **Tom (11 sept.) — VALIDÉ :** l'anneau qui compte toute la liste ; la date seulement quand la donnée existe ;
> **« + Lancer un Chiche »** (« c'est le bon mot, on lance un Chiche »). **Le bug `avec` : CORRIGÉ dans l'app**
> (`lot-PERSONNE-AVEC`, preuve dans les deux sens — chapitre en tête d'ETAT-DES-LIEUX).
> **La DA refusée sur la planche 2**, refaite en planche 3 (`PLANCHE-FICHE-PERSONNE-3.html`) : le Noyau de la rangée de
> l'Aura (58, le visage au centre), « Tenu ensemble » en dalles comme « ce que tu as tenu », les VRAIES cartes de l'Index
> (dalle, champ, trait d'état). ⚠ Deux constats de Tom ne tiennent pas à la mesure, dits sans polémique : le titre de la
> planche 2 était en **Bricolage 700** (face chargée, mesurée — Fraunces n'y était pas chargée) ; ses vignettes portaient
> les **vraies dalles** (0 image manquante) — les rectangles vides sont ceux de l'app d'aujourd'hui.
> **11 sept., suite — planche 4 (`PLANCHE-FICHE-PERSONNE-4.html`, AUTONOME) :** Tom ne voyait ni dalles ni polices — la
> planche 3 appelait images et polices par chemins absolus ; hors du serveur elle perdait tout. La planche 4 embarque les
> six faces et chaque image. **Le correctif `avec` : validé par Tom.** **« Promesses partagées » refusé** (on dit Promi,
> jamais promesse ; le titre doit couvrir Promi, Chiche et Promi de Nuée) — **trois formules proposées** : « Ce que tu
> partages avec Rachel » · « Entre toi et Rachel » · « Ce qui vous lie ». **« aucun Promi pour l'instant » retiré** (disait
> Promi, excluait les Chiche ; une absence ne se dessine pas). **L'état n'est plus écrit sur la carte** : le trait le dit ;
> la ligne du bas garde le temps quand l'app le sait, et la Nuée. « à le groupe » → CHANTIERS n° 60.
> **Nouveaux points ouverts :** le titre **« Tenu ensemble »** (aucun mot de l'app ; reprend « ce qu'on a fait ensemble »)
> — à valider ; **la Nuée d'une parole** n'a pas de place sur une carte d'Index (l'Index range ces paroles sous la carte de
> la Nuée) — la ligne d'état est la plus sobre ; **« à le groupe »** est déjà dans l'Index (grammaire : « au groupe »).

**Tranché par Tom :** ce qui reste = le nom, le visage, **l'anneau sans chiffre** (« il est la FORME de la liste » : il
compte toute la liste, tes paroles et les siennes, Promi et Chiche — le cadre 19 « ton côté seulement » ne vaut plus pour
cette fiche), **la liste des paroles partagées avec leur état, leur date, leur Nuée — Chiche compris**, et de quoi
planter un Promi ou lancer un Chiche avec cette personne. Tout le reste sort, sans remplacement. Planches :
`PLANCHE-FICHE-PERSONNE-2.html` (plein / vide × deux thèmes). **Rien d'intégré avant son accord.**

- **Les Chiche manquants — vérifié :** `openPerson` ne lit que `who` et `from`, jamais `avec` (le compagnon d'un Chiche),
  alors que la rangée de disques d'une fiche le compte (l. 3640). Au jeu de démonstration : **2 rangées absentes** —
  « courir dimanche » (Chiche, avec Rachel) sur la fiche de Rachel, « vider le composteur à deux » (Chiche, avec Adrien)
  sur celle d'Adrien. (« Vingt-et-une lignes » : je ne les retrouve pas.)
- **À valider — « + Lancer un Chiche » :** « + Planter un Promi » est le libellé de l'app (le fil d'une Nuée) ; aucun
  libellé ne lance un Chiche. Le plus sobre du lexique : on *lance* un Chiche (« CHICHE LANCÉ »).
- **À valider — « avec Rachel »** sur la rangée d'un Chiche dont elle est la compagne : « avec » est la liaison du Chiche
  dans la page + ; sans elle, « à Marion » sur la fiche de Rachel ne s'explique pas.
- **La date — une DONNÉE qui manque, pas un choix :** l'app ne garde aucune date d'une parole tenue ou en cours (règle
  l. 12695 : « on lit `leJour` quand il existe, on n'écrit rien sinon — jamais une date fabriquée »). Deux des quatre
  rangées de Rachel en ont une.
- **« comment ça évolue » au Cercle (Q183)** : absent de « ce qui reste » — mis de côté pour le lot du Cercle, pas dessiné ici.
- **Mises au point :** « il te doit une parole » n'existe nulle part dans l'app (vérifié) ; « rayonnante sur zéro
  promesse » ne se reproduit pas (`harmonyWord(null)` rend « à tisser », mesuré sur une personne sans Promi) — il
  disparaît de toute façon avec le mot. L'audit comptait **trois** interdits (Q184) et douze règles enfreintes (§ C), pas onze.

#### Q192 · LE PLANCHER DES DALLES : ΔE 15 — **réécriture validée par Tom · la correction TRANCHÉE : CHANTIER 59** · ET CE QUE LE FILTRE À 300 ÉCARTAIT

> **Tom (10 sept., suite) :** *« Note-le comme chantier, pas comme question : quand une dalle est trop proche du sol, sa
> couleur doit être écartée à la plantation. Ce n'est pas urgent — le contrôle rougira quand ça arrivera, c'est ce
> qu'on lui demande — mais ça ne doit pas se perdre. »* → **CHANTIERS.md n° 59.** Les trois voies du § 4 ci-dessous sont
> donc closes : c'est la couleur de la dalle qui s'écarte, à la plantation.
> **Remarque de Tom, notée telle quelle — NON MESURÉE :** *« à ΔE égal, une dalle texturée se lit mieux qu'une dalle
> unie. Le ΔE est un plancher, pas un prédicteur complet. »* Aucune mesure de ce projet ne compare une dalle texturée
> et une dalle unie à ΔE égal ; si le chantier 59 doit fixer un écart, c'est à mesurer.
> **Le taux, compté sur tout ce qui a été relevé :** 6 chargements sur 10 portent au moins une dalle sous 15 ; 12
> relevés de dalle sur 99 (≈ 1 sur 8) ; la pire, sur un tirage réel, à ΔE 8,0.
>
> **Repris (Tom, 10 sept.) :** « écarter à la plantation ne peut rien régler puisque c'est le sol qui bouge » — vérifié :
> le sol est la nature majoritaire des Promi tenus (`natureMaj`) ; il ne prend que trois valeurs. Piste préférée de Tom :
> **le peigné**. ⚠ Deux mises au point : ce n'était pas « ma piste 3 » (la mienne était « un tirage qui évite le sol »),
> et « à ΔE égal, une texture se lit mieux » n'était pas une mesure à moi. **Mesuré maintenant** (CHANTIERS n° 59) :
> le peigné existe déjà (l'épi de chaque île) et apporte +3,7 à +5,0 ; couché à 90°, rien de plus ; **0 dalle rouge
> sur 6 ne passe le plancher**, la pire 4,6 → 9,6 → 9,7. Le grain compte un peu au-delà de la couleur (ΔE pixel à
> pixel : +5,1 à +7,7 avec l'épi) mais même ainsi la pire reste à 11,1. **Le peigné seul n'y arrive pas.**

> **Tom (10 sept.) :** *« Ta réécriture est la bonne : mesurer chaque dalle réelle, sans masque, sans filtre, avec un
> plancher absolu en ΔE. »* Trois consignes, appliquées :
> 1. **Le plancher au-dessus de l'amas illisible, pas au milieu : 15.** L'amas illisible monte en fait jusqu'à **14,0**
>    (pas 11,1 : un « grand plongeoir » bleu sur bleu mesuré après coup), 15 le dépasse d'un point. Il reste bas devant
>    ce qui passe : l'amas lisible naturel commence à **21,2** (moucheté pâle en clair), et les dalles pâles des sphères
>    de sonde, lisibles, étaient à 16,3–18,3. 20 condamnait ces dernières ; le milieu (≈ 17,6) aurait laissé passer un
>    illisible un peu moins bleu que ceux vus.
> 2. **Le critère relatif de luminance est gardé**, en plus, sur les îles réelles.
> 3. **Prouvé sur le CAS RÉEL, sans rien poser** (`preuve_cas_reel.py`, l'ancien et le nouveau juge sur les MÊMES
>    pixels) : en trois chargements, le tirage a mis deux fois une dalle sur la couleur de la sphère — **« monter la
>    serre » ΔE 8,0, en 76 morceaux dont le plus gros fait 39 cellules** ; **« le grand plongeoir » ΔE 12,9, 138
>    morceaux, le plus gros 41.** Les deux JETÉES par l'ancien filtre, l'ancien juge ne dit rien ; le nouveau les
>    **nomme**. En clair, les mêmes dalles (8,3 et 14,0) étaient gardées par le filtre (313 et 481) — et l'ancien juge
>    ne disait **toujours rien** : la borne relative laissait passer, le sombre de référence étant aussi mauvais. C'est
>    exactement la faille que Tom avait nommée. Vu à l'œil : les trois dalles nommées ne se lisent pas (le plongeoir en
>    clair, à 14,0, est un moucheté pâle à la limite). Le chargement « à 212 cellules » cité ne se rejoue pas (tirage au
>    hasard) ; le mécanisme, lui, est pris deux fois, plus bas encore (39 et 41).
> 4. Leçon inscrite dans CLAUDE.md §7 (« une dalle se lit par sa teinte »). Les chiffres exacts de l'inversion en
>    luminance : **21,7 lisible** (dalle orange) contre **22,6 illisible** (moucheté pâle en clair, ΔE 11,1).

Tom (10 sept.) : *« "pas plus faibles qu'en sombre à 5 près" est une borne relative… Ajoute un plancher absolu »* et
*« ton filtre à 300 cellules : dis-moi ce qu'il écarte »*.

**1 · Le filtre écartait la dalle la plus illisible — mesuré.** Chaque île réelle retrouvée par son centre (le moteur
exporté, `batIles`, recoupé avec `_auraComp.derniere` : écart 0), dans la même page, deux thèmes, cinq chargements.
Le masque « avec − sans » (seuil 12) **fragmente une île pâle** : sous son centre, un morceau de 1 à 96 cellules ;
son plus gros morceau faisait 442 et 438 (gardé) dans un chargement, **212 et 176, puis 187 et 274, dans deux autres —
jetés par le filtre**. La dalle la plus illisible disparaissait alors de la mesure, et le juge rapportait comme « la plus
faible » la suivante. Le bruit du poil, lui, ne dépasse pas 60 cellules. **Aucune île bien lisible n'était sous 300** —
le filtre ne perdait QUE celles qu'il devait voir. **Retiré** : chaque île se mesure au cœur (disque de rayon ½ du
rayon projeté), là où le moteur la pose, et le juge vérifie qu'il la retrouve (sinon il le dit, il ne mesure pas du vide).

**2 · Le plancher ne peut pas être en luminance.** L'île orange se lit franchement avec un écart de luminosité de 18 à
21 ; l'île bleue sur bleu ne se lit pas, à 13–14. **La luminance les confond ; la couleur non** : ΔE (CIELAB, couleurs
moyennes au cœur de l'île, avec et sans elle) **84 à 94 contre 9 à 11**. Une dalle se lit par sa teinte autant que par
sa clarté. Le seuil 42 du §3 est un écart de LUMINOSITÉ entre deux aplats : il ne se transpose pas à une dalle texturée
sous le poil (la dalle blanche, bien lisible, n'y fait que 25 à 39).

**3 · La valeur — calibrée à l'œil, et c'est pour ça qu'elle est à valider.**
```
vu ILLISIBLE (bleu sur bleu, orange sur orange de la sonde)   9,4 · 10,4 · 10,8 · 11,1 · 14,0   (sonde : 7 à 13)
vu LISIBLE                                                    16,3 · 17,1 · 18,3 (pâles sur les sphères de sonde)
                                                              21,2 (moucheté pâle, en clair) · 24,1 (lilas) · le reste ≥ 25
```
**Plancher : 15.** Un premier plancher à 20 nommait des dalles que je lis sans peine (16 à 18) — baissé. **La marge est
mince des deux côtés (14,0 / 16,3)**, et elle a été lue sur l'écran du Mac : **à confirmer sur un vrai téléphone.**
Prouvé (`preuve_plancher.py`, le code du juge importé) : le sol pris à la couleur BRUTE de la dalle la plus lisible (le
mécanisme naturel du bleu sur bleu, rendu voulu) → la dalle est **nommée**, dans les deux thèmes (9,5 et 7,0), avec les
deux autres dalles tombées de la même couleur ; un sol loin de toutes → **rien** ; la sonde défaite → la page remesurée
au centième.

**4 · Ce que le plancher dit du jeu de démonstration — un défaut qui existait, et que le juge va maintenant voir.**
Sur les six chargements mesurés en ΔE, **trois** portent une dalle sous 15 en sombre (9,4 · 10,4 · 14,0), **deux** en
clair (10,8 et 11,1 · 10,3). C'est le **bleu sur bleu** : la couleur d'une dalle est tirée au hasard par le moteur à
chaque chargement (`cc()`, `Math.random` — code de la Toile, §9), et le sol de la sphère EST la couleur de nature. Ce
n'est pas le thème clair : le sombre est touché autant, ou plus. **`releve-aura` rougira donc environ un chargement sur
deux, en nommant la dalle — il dit vrai.** Je n'ai rien corrigé : toutes les voies sont des décisions de produit —
- la **teinture de Q30** étendue à la sphère (la dalle remappée sur la rampe de sa nature) — mais la sphère EST la Toile,
  et le §4 y interdit toute teinture ;
- **le champ qui cède**, comme dans l'Index et le Fil : la luminosité du sol (teinte de nature intacte) s'écarte de la
  dalle — mais le sol, ici, c'est la sphère entière ;
- **un tirage qui évite le sol**, dans la dalle — mais c'est le code de la Toile.

#### Q191 · LA PARTIE « DALLES » DE LA FAMILLE « LA MATIÈRE » N'A PAS ÉTÉ VUE MORDRE SEULE — **ouverte**

> **Mise à jour (10 sept., avec Q192) :** le critère relatif se mesure désormais sur les îles RÉELLES (plus de filtre) ;
> sur la « 2 » posée en clair il a cette fois mordu (médiane 16,9 contre 44,8) — **mais encore avec l'écart et le
> contour**, pas seul. Le **plancher absolu**, lui, a été vu mordre seul : il nomme une dalle précise, par son titre,
> et se tait quand aucune ne tombe.

La famille 10 du juge (`releve-aura.py`) a été prouvée contre de vrais défauts (`preuve_matiere.py`) : la « 2 »
posée en clair est prise, la boule sombre aussi. **Mais sur la « 2 », ce sont l'ÉCART et le CONTOUR qui ont
mordu — pas le critère des dalles.** Dans cette page, le sombre de référence était lui-même faible (médiane
31,6 : les couleurs des dalles sont tirées au hasard à chaque chargement), si bien que les dalles de la « 2 »
ne passaient pas sous la barre relative. **Le critère des dalles est donc encore NON PROUVÉ seul.** Pour le
prouver il faut une sonde qui noie les îles SANS toucher à l'écart ni au contour (aucune commande ne le fait
aujourd'hui), ou des dalles de couleurs FIXÉES pour la mesure. À faire avant de s'y fier seul.

#### Q190 · UN CONTRAT DE LA PREUVE A RATÉ UNE FOIS, SANS ÊTRE NOMMÉ — **vu une fois, non reproduit sur sept passes**

> ⚠ **Mise au point (10 sept.) :** Tom a lu que le contrat raté était « acquis 6 · le comblement du creux au lancer » et
> que je l'aurais écrit « lire toujours la même position, la boule ayant tourné ». **Ni l'un ni l'autre :** le contrat
> n'a jamais été nommé (c'est l'objet de Q190), et l'acquis 6 n'est pas un des 18 contrats de la preuve — il est dans
> `releve-aura.py`. **Vérifié dans le code : l'acquis 6 ne compare aucune position** ; il mesure deux DURÉES (la vie du
> creux après un lâcher sur place, puis après un lancer), en lisant l'état de l'empreinte, jamais des pixels. Il n'y a
> donc pas deux points à mettre au même angle. **Les contrôles qui comparent des PIXELS** (toucher, retour, trace,
> relissage) se prennent déjà à vue FIGÉE et remise (`fige(true)`, `vue(lac, tan)`) — même angle par construction.

Sur la version à la règle des cinq (`8e579374…`), la preuve des 18 contrats a donné une fois « ❌ 1 contrat
à reprendre » **sans que je puisse dire lequel** : mon rejeu ne gardait que les lignes de la légende et le
verdict, et le journal complet n'a pas été conservé. **C'était l'instrument, pas le contrat, qui était
aveugle.** Tom : *« un défaut non nommé qui ne se reproduit plus reste un défaut non nommé. »*
- **Non reproduit** : sept passes de suite à 18/18 (`preuve_rouge_1…7.log`, journaux entiers), puis la
  preuve de la réinsertion, verte.
- **Deux contaminations trouvées DANS la passe** en auditant les sondes (CLAUDE.md §8) : les retraits de la
  légende effaçaient la cote écrite par l'app ; la phrase remise ne recalculait la colonne qu'au passage
  suivant. Candidates plausibles, non prouvées comme cause.
- **Corrigé :** les sondes défont exactement (valeur et priorité d'avant), la phrase remise force le
  recalcul, et **le verdict nomme les contrats qui ratent** ; chaque passe garde son journal entier
  (original `preuve_contrats-avant-retraits-exacts.py`). S'il revient, il sera nommé.

#### Q189 · LA SECONDE RANGÉE : UN TROU À CINQ, À PEINE EFFLEURÉE AVEC UNE PHRASE D'UNE LIGNE — **TRANCHÉ par Tom : une RÈGLE**

> **Tom, 10 sept. :** *« la deuxième rangée à cinq est validée, note-la comme règle. »* **RÈGLE : la seconde rangée paraît
> à partir de CINQ dalles tenues ; en dessous, la première rangée seule** (une rangée au tiers, 3 + 1, dit « il en manque
> deux »). À cinq, le trou d'une case à droite est accepté — la mesure qui dit qu'il se voit lui avait été redonnée.
> Portée dans le code (`K.RANG2`, `nbMoisson()`) et dans le juge (`RANG2`, en dur). Reste ouvert dans Q188/Q189 : avec une
> phrase d'une ligne, la seconde rangée est posée contre le bord plutôt que coupée.

> Tom a répondu : *« Le trou invisible sous le pli : bien vérifié. Le garde-fou à cinq est le bon — sous cinq, une rangée
> pleine coupée vaut mieux qu'une rangée à un tiers. Note-le comme règle. »* **Mais la mesure dit l'inverse : à cinq le trou
> SE VOIT à l'ouverture** (une ligne : deux dalles entières + la case vide ; deux lignes : deux dalles coupées au quart + la
> case vide). Et je n'avais pas proposé de garde-fou à cinq. La règle « seconde rangée à partir de cinq » laisserait donc le
> trou visible dans le cas du jeu de démonstration (cinq). **Non appliquée : question reposée à Tom — cinq (le trou à cinq
> accepté) ou six (la seconde rangée seulement pleine) ?**

Tom, 10 sept. : *« une rangée à moitié vide dit « il en manque une », alors qu'une rangée pleine coupée par le
bord dit « il y en a d'autres ». Si le trou se voit, tranche par la composition : soit la seconde rangée est
décalée pour qu'aucun vide ne soit visible, soit elle ne s'affiche qu'à partir de quatre dalles. Dis-moi ce
que tu constates plutôt que de choisir seul. Et vérifie le cas à six et plus : la seconde rangée doit être
pleine et franchement coupée, pas juste effleurée par le bord. »*
**Mesuré** (`sauvegardes/aura-orbite-lot/mesure_rangees.py`, images `rangees/`, le DESSIN des dalles, à l'ouverture) :
```
paroles tenues   phrase d'une ligne (3 phrases sur 5)             phrase de deux lignes (2 sur 5)
3                une rangée · bouton sous le pli, fond nu           idem
5 (3 + 2)        2e rangée : TROU à droite · dessins ENTIERS,       TROU à droite · dessins cachés à 26 %
                 à 8 pt du bord · libellés sous le pli
6 et plus        2e rangée pleine · dessins ENTIERS, à 8 pt du      2e rangée pleine · cachée à 26 %
                 bord — POSÉE contre le bord, pas coupée
```
**Constats :** (1) **le trou se voit** — à cinq, le coin bas droit est vide sous une première rangée pleine ; il
se lit comme une dalle qui manque. (2) **à six et plus, la seconde rangée n'est franchement coupée que si la
phrase fait deux lignes** (le quart bas caché) ; avec une ligne — trois phrases sur cinq — elle est posée
contre le bord, entière, et seuls ses libellés passent dessous : effleurée. La différence est la hauteur
de la phrase (23,6 pt). (3) avec trois dalles ou moins, Q188.
**Rien n'est tranché.** La version à deux rangées (`scratchpad/app-aura-rang.html`, juge vert) n'est PAS
insérée ; `app.html` reste `31a0ed37…` (une rangée, bouton sous le pli).

#### Q188 · MOINS DE QUATRE PAROLES TENUES : UNE SEULE RANGÉE, RIEN À COUPER AU PLI — **une question de composition, pour Tom** (voir Q189)

> ⚠ Tom a écrit « Q188 est réglée — les teintes du plateau et du bouton sont au CSS, voulues » : les TEINTES sont bien
> réglées (voulues, au CSS — noté), mais elles n'étaient pas Q188. Q188 est la composition à trois dalles ou moins ; elle
> reste ouverte et rejoint Q189. **Mesuré : avec une seule rangée, le bouton ne peut PAS rester entier** — l'air de 28 sous
> les libellés porte son bas à 848 (phrase d'une ligne) ou 871 (deux lignes) : il passe sous le pli, et le fond nu revient.

Tom : *« si les dalles ne suffisent pas parce qu'il n'y en a pas assez, dis-le-moi : c'est alors une
question de composition de la colonne, pas d'affordance. »* **C'est le cas dès qu'on a tenu trois paroles
ou moins** (le jeu de démonstration en a cinq : deux rangées, 3 + 2). Avec une seule rangée, il n'y a rien à
couper au pli : sous ses libellés, le fond nu revient jusqu'au bas de l'écran (≈ 84 pt avec une phrase d'une
ligne, ≈ 61 avec deux), et le bouton est sous le pli (Q186). Avec ZÉRO parole tenue mais des Promi en cours,
« Ce que tu as tenu » ne paraît pas du tout. Le juge le note sans l'imputer (`composition` dans ses valeurs).
Rien n'est inventé en attendant.

#### Q187 · LE BOUTON EST SOUS LE PLI — MAIS RIEN NE L'ANNONCE — **TRANCHÉ par Tom**

> **Tom, 10 sept. :** *« c'est le fond nu qui trahit, pas le bouton. 84 pt de vide, ça dit « c'est fini », et personne
> ne défilera. La réponse est de supprimer le vide, pas d'ajouter un signe. Si les dalles s'arrêtent net, mets-en une
> rangée de plus, partiellement visible sous le pli — une dalle coupée par le bord de l'écran dit qu'il y a la suite,
> sans aucun élément ajouté. C'est le même principe que la rangée des six qui défile : le disque coupé est
> l'affordance. N'ajoute ni flèche, ni ombre, ni dégradé de fondu — ce sont trois choses interdites. »*
> **Appliqué :** « Ce que tu as tenu » porte jusqu'à SIX dalles, deux rangées (`K.MOISSON`). Contrôlé par `releve-aura.py`,
> famille 9 : dès qu'il y a plus d'une rangée, le bord de l'écran doit en couper une à l'ouverture. Les trois options
> ci-dessous sont écartées.

Tom, 10 sept. : *« le bouton doit rester atteignable sans effort. Il est sous le pli, donc on défile —
mais on doit sentir qu'il y a quelque chose en dessous. Si la colonne s'arrête pile après les dalles sans
laisser deviner la suite, personne n'ira. »* **Vérifié, mesuré : RIEN NE L'ANNONCE.** À l'ouverture, sous
les derniers libellés des dalles, il reste **84,4 pt de fond nu** jusqu'au bas de l'écran avec une phrase
d'une ligne, **61,4 pt** avec deux ; rien ne passe le pli ; la colonne a l'air finie. (L'état vide n'est pas
concerné : le bouton y est entier à l'ouverture, 22 du bord.)
Ce qui pourrait l'annoncer, sans couper le bouton (Q186) :
1. **le bouton reste à SA place de la planche (762), entier, dans tous les états** — la colonne défile
   entre le plateau et l'air au-dessus du bouton (28), et c'est le bord bas de cette fenêtre qui coupe les
   dalles quand elles ne tiennent pas : l'amorce du défilement, comme le disque coupé de la rangée
   (« la septième silhouette »). Le bouton est TOUJOURS visible et entier — atteignable sans effort, à la
   même place que dans l'état vide. Mais il ne suit plus la colonne : c'est ce que Q186 avait écarté.
2. **laisser la colonne telle quelle** (bouton franchement sous le pli) — rien ne l'annonce.
3. **une forme qui annonce la suite** (un signe au pli) — elle n'existe nulle part dans la planche ni le
   document : ce serait l'inventer (§9), elle ne se pose pas sans toi.
**En attendant, la version insérée garde la règle validée** (bouton sous le pli) : rien n'est changé.

#### Q186 · L'AIR RENDU NE TIENT PLUS DANS L'ÉCRAN — LE BOUTON EST COUPÉ À L'OUVERTURE — **TRANCHÉ par Tom : un vrai défaut**

> **Tom, 10 septembre :** *« La colonne qui défile sous le plateau est la bonne réponse. Le cadre fait 844 pt, l'écran
> n'a jamais eu de quoi tout tenir : mieux vaut assumer le défilement que serrer. Le bouton coupé : c'est un vrai
> défaut, pas un choix. Vérifie qu'il est entier à l'ouverture ou franchement sous le pli, jamais coupé en deux. »*
> **Appliqué :** entier avec sa marge (bas ≤ 822) ou franchement sous le pli (haut ≥ 844). Avec l'air de 28 il ne peut
> plus être entier dès qu'il y a des Noyaux : il tombe sous le pli. Contrôlé par `releve-aura.py`, famille 9.
> Les deux « autres voies » ci-dessous sont écartées.

Tom a demandé de baisser tout ce qui est sous la phrase (l'air sous elle tombait à 3,7 pt avec une phrase
de deux lignes). Fait, mesuré : l'air est de 27 à 29 pt partout dans la colonne. **Mais la colonne ne tient
plus dans 844** : elle défile (≈ 26 pt avec une phrase d'une ligne, ≈ 49 avec deux), sous le plateau qui
rogne. **À l'ouverture, le bouton « Partager mon Noyau » est donc coupé par le bas de l'écran** — de 3,4 pt
avec une phrase d'une ligne (il frôle le bord), à mi-hauteur de son libellé avec deux (34 pt sur 60).
**Fait (option la plus sobre, c'est la lettre de la demande) :** la colonne défile, le bouton coupé est
l'amorce du défilement — comme le disque coupé de la rangée glissante (« la septième silhouette »).
**Deux autres voies, sans en choisir une :**
1. **le bouton se détache et reste en bas de l'écran** (22 du bord), la colonne défile au-dessus de lui
   — toujours visible, jamais coupé ; mais c'est une forme que la planche n'a pas ;
2. **reprendre l'air au-dessus de la phrase** (50 pt entre la sphère et elle) : la phrase se rapproche de
   ce qu'elle commente, et tout tient — mais c'est l'inverse de « baisse tout ce qui est en dessous ».

#### Q184 · LA FICHE DE LA PERSONNE EST HORS DA ET PORTE TROIS INTERDITS — **le lot suivant, avec un audit** (Tom, 10 septembre 2026)

> **Audit écrit (10 sept.) : `AUDIT-FICHE-PERSONNE.md`** — nœud par nœud, rien de modifié. Les trois interdits y sont
> mesurés (§ A n° 3, 6, 9) avec ce que leur retrait emporte (§ E) ; il trouve en plus : les dalles de la liste jamais
> peintes, une courbe grise et inventée sous deux Promi résolus, les nœuds du Cercle inatteignables même abonné, la
> colonne à 8 au lieu de 24, trois opacités sous 72 %, « votre » et « ta » dans la même ligne. Partis de surface : § G.
> **Complété (10 sept., suite)** : § A bis — l'inventaire complet, nœud par nœud, gratuit/Cercle, vivant/mort, avec
> chaque valeur (dont le mode Cercle vu en le forçant : second anneau, « toi envers eux · eux envers toi », et pour
> Rachel « toi 50 % ⟷ eux 0 % · tu portes un peu plus ») ; § B bis — deux modes sans porte (« moi », Cercle), trois portes
> mortes ; la nature des rangées absente (trois Chiche montrés comme des Promi) ; « à le groupe ». **Planches :
> `PLANCHE-FICHE-PERSONNE.html`** (A velours · B Noyau · C Toile partagée) et le registre « rien ne se perd ». **Tom choisit
> avant toute intégration.**

`openPerson` — la fiche qu'ouvre un toucher sur un Noyau — **n'a jamais été refaite** : c'est un écran à
part entière, hors DA. **Rien n'est corrigé maintenant.** Tom : *« cette fiche demande son propre lot, avec
un audit comme pour le partage : on ne retire rien sans savoir ce qu'on perd. »* Les trois interdits, avec
leur règle (`AUDIT-AURA-CERCLE.md` § C, les huit règles anti-notation) :
**La référence : `AUDIT-AURA-CERCLE.md`, § C « Les huit règles anti-notation » — aucun chiffre ni agrégat
par personne** (règle 1 : *aucun chiffre attaché à une personne* ; règle 2 : *un seul chiffre, le tien,
global* ; règle 4 : *aucun agrégat par personne* — l'audit y range déjà « un mot par personne —
rayonnante, naissante »).
1. **« COMMENT ÇA ÉVOLUE » en gratuit** — la courbe d'évolution. **Elle va au Cercle** (Q183, tranché).
2. **« votre harmonie : rayonnante · ta parole : rayonnante »** — un MOT D'HARMONIE attaché à une personne.
   **Règle 1 : aucun chiffre ni mot de valeur pointé vers quelqu'un.** C'est pour cette raison qu'on l'a
   retiré de l'Aura ; il ne peut pas rester ici. (L'audit rangeait déjà « un mot par personne —
   rayonnante, naissante » parmi les agrégats de la règle 4.)
3. **« 3 Promi échangés · 1 reçu · 2 donnés »** — un AGRÉGAT par personne. **Règle 4 : aucun agrégat par
   personne. Un seul chiffre existe dans le produit : le tien, global** (règle 2).
**Méthode du lot :** l'audit d'abord, nœud par nœud — ce que chaque élément dit, d'où il vient, ce qui le
lit ailleurs, ce qu'on perd en le retirant — comme pour le partage ; puis la DA.

#### Q185 · L'AIDE « i » DE L'AURA DÉCRIT L'ANCIENNE AURA — **constat ; un LOT DE TEXTES à part (Tom)**

> **Tom, 10 sept. :** *« note-le, ne le corrige pas — c'est un lot de textes à part. Mais confirme-moi qu'elle n'explique
> pas la sphère. »* **VÉRIFIÉ : elle ne l'explique pas.** Le texte de `#auraHelp` est du HTML statique (1 882 caractères) ;
> les deux scripts qui la touchent (l. 8934–8935) n'y écrivent rien, ils accrochent des clics. Ni « sphère », ni
> « enroulée », ni « boule », ni « velours ». « Toile » n'y paraît qu'une fois — *« ouvre les designs signature de la
> Toile »*, un item du Cercle ; « orbite » y désigne l'ANCIEN double Noyau du Cercle (*« ton Noyau s'entoure d'une orbite
> où chaque proche prend sa place »*), pas la sphère. Rien à retirer au titre de la sphère.

Le « i » du plateau ouvre `#auraHelp`. Il décrit TOUT l'ancien écran : *« L'anneau central, c'est ton
harmonie envers les autres. Le grand chiffre — ton % de parole tenue… La jauge d'équilibre… Ta meilleure
Nuée… Les graphs… »* — des éléments qui n'existent plus, dont plusieurs enfreignent les règles 1, 2, 4 et 5.
Et Tom a posé le principe : **la sphère ne s'explique pas** (ci-dessous). Rien n'est changé : l'aide est à
réécrire ou à retirer, et c'est une décision.

#### ⚑ LA SPHÈRE NE S'EXPLIQUE PAS — **décision Tom, 10 septembre 2026**

*« On n'explique pas. Pas de légende, pas de phrase qui dit « c'est ta Toile enroulée ». L'abstraction est
ce qui rend l'écran partageable — un inconnu ne doit rien pouvoir y lire. On le découvre en touchant, et
c'est très bien ainsi. »* Vaut pour tout ce qui entoure la sphère : l'écran, l'aide (Q185), le partage.
La légende de l'écran nomme les ARCS DES NOYAUX, pas la sphère — elle reste.

#### Q182 · L'ORBITE EN THÈME CLAIR N'A JAMAIS ÉTÉ VALIDÉE — le pavage s'y lit en plages à bords polygonaux — **TRANCHÉ par Tom : A (le poil garde sa nature, la peau s'éclaircit)**

> **Tom, 10 sept. (arbitrage final) :** *« Fixe A. Ma règle était mal posée : je t'ai donné l'écart objet/fond comme
> critère principal, alors que les dalles sont le point dur. A garde le contour, garde les dalles, et fait disparaître les
> plages polygonales. Il ne rate qu'un critère, et sur un écart qui va dans le sens de la présence — un objet trop présent
> se corrige ; un objet qui se dissout, non. La 2 rate les trois choses qui comptent. »* **À faire :** trois essais, pas plus,
> pour rattraper le 93 sans toucher aux dalles ; sinon 93 est ASSUMÉ. La cible du juge = la valeur retenue. (Note : le juge
> n'avait AUCUN contrôle d'écart boule ↔ page — il est créé, pas mis à jour.)
> **LES TROIS ESSAIS, MESURÉS** (`mesure_a3.py`, même page, îles ≥ 300 cellules — la médiane du sombre avait varié de
> 57 à 41 d'une page à l'autre : les couleurs des dalles sont tirées au hasard, seule la comparaison dans la même page vaut) :
> ```
>                                   boule↔page   contour   îles : plus faible · médiane
> sombre (même page)                   71,7        59,5          23,0 · 40,7
> A                                    95,9        95,9          36,7 · 49,3
> A1 · peau à 30 % vers le crème       90,6        95,3          27,5 · 49,9
> A2 · peau à 60 % vers le crème       85,1        94,7          30,7 · 50,1     ← RETENU
> A3 · poil 15 % plus clair            88,3        86,3          29,9 · 41,6
> ```
> **RETENU : A2** — la peau part entièrement vers la teinte claire de la nature, tirée à 60 % vers le crème du corps (§1.3).
> 11 points rattrapés sans rien coûter aux dalles ; **les 9 restants au-dessus de 76 sont ASSUMÉS.** (« Le poil légèrement
> moins clair » de Tom allait dans le mauvais sens — il assombrit la boule ; dit à Tom, essayé dans l'autre sens : A3.)
> **Le juge porte la décision** (`releve-aura.py`, famille 10 « la matière ») : boule ↔ page 76 en sombre, 85 en clair, ±8 ;
> contour ≥ 42 ; les dalles du clair pas moins lisibles qu'en sombre, dans la même page, à 5 près.

> ⬇ Historique des arbitrages :

> **Tom, 10 sept. (second arbitrage) :** *« sol clair, poil sombre. Le vrai négatif du thème sombre, pas sa version
> éclaircie. Le champ garde sa couleur de nature, c'est la matière qui s'adapte au corps. Trois choses à mesurer : l'écart
> objet/fond comme en sombre ; le contour net ; les dalles lisibles — elles ne doivent ni se noyer dans un sol clair ni
> devenir des taches sur un poil sombre. Si l'inversion ne tient pas, dis-le : on gardera la 2 comme repli assumé. »*
> ⚠ Dit à Tom : je n'avais ni essayé le sol clair, ni mesuré « un écart de 4 », ni proposé « poil sombre » — la piste est
> la sienne, prise. Et la référence « comme en sombre » est **77** (écart boule ↔ page, métrique du §3), pas 33.
> **Le point de départ, relevé :** sombre — boule↔page 77, limbe↔page 59, poil↔sol 94 ; clair aujourd'hui — 129, 99, 84.
> **SA VERSION, ESSAYÉE ET MESURÉE (copie, rien d'inséré) :** la peau part vers la teinte claire de la nature (§1.2), le
> poil garde sa couleur de nature. Métrique du §3, vue figée, contre le sombre :
> ```
>                        boule↔page   limbe↔page   dentelle   îles↔sol
> sombre (référence)        74,5         59,5         93,2       47,9
> clair, peau inchangée    130,1         98,9         90,5       46,9
> clair, peau 70 %         101,2         96,2         78,6       51,1
> clair, peau 100 %         94,4         95,9         75,0       50,4
> ```
> **Tient :** le contour (96, seuil 42), les îles en moyenne (50 contre 48 en sombre), les plages polygonales disparaissent
> (l'aire qui change sans les îles revient de 7 196 à 4 855 px, contre 4 319 en sombre), la dentelle s'inverse (poil sombre
> sur peau claire). **Ne tient pas :** l'écart boule ↔ page reste à 94 contre 74 en sombre — le poil, qui garde sa couleur
> de nature, couvre l'essentiel de la boule ; la peau ne se voit qu'entre les poils. **À l'œil :** les îles pâlissent
> (l'orange tire au saumon), et une île bleu sombre, au centre, devient presque invisible — la moyenne ne le dit pas.
> ⚠ La première passe de mesure était FAUSSE sans le dire (le masque `trame:null` arrêtait le peintre) : l'instrument
> vérifie maintenant chaque image et s'arrête s'il mesure du vide. **Question posée à Tom.**
> **LES TROIS VOIES, MESURÉES CÔTE À CÔTE** (Tom : « ta version ; si ça ne tient pas, inverse le poil ; sinon la 2 ») —
> `mesure_q182.py`, même vue figée, îles une à une (composantes du masque) :
> ```
>                                   boule↔page   contour   dentelle   îles : plus faible · médiane
> sombre (référence)                   75,6        59,5       94,5          27,3 · 56,6
> A · sa version (poil nature,         93,4        95,9       79,4          35,4 · 53,9
>     peau claire §1.2)
> B · poil inversé (poil = corps      137,7       150,8      117,8          88,3 · 105,1
>     sombre §1.3, peau claire)
> C · la « 2 » (poil = teinte claire,  65,7        39,2       82,1          23,5 · 24,9
>     peau assombrie)
> ```
> **A** : contour net, îles aussi lisibles qu'en sombre, plages polygonales disparues — l'écart boule ↔ page reste trop
> fort (93 contre 76). **B** : une boule gris-bleu lourde sur le crème, des îles en taches — l'écart s'éloigne encore
> (138). **C** : la seule qui approche l'écart (66) — mais le contour tombe SOUS le seuil (39 < 42, il se dissout à gauche),
> les îles se NOIENT (médiane 25 contre 57 en sombre ; seule l'orange reste lisible), et les plages polygonales
> REVIENNENT. **Aucune ne tient les trois.** Le repli annoncé (C) casse le point dur. Question reposée à Tom : A ou C.

> **Tom, 10 sept. :** *« un sol clair. Le champ porte la couleur de nature, et une couleur de nature n'est pas plus sombre
> en thème clair — c'est le corps qui change, pas le champ. Un sol clair avec des poils qui s'y détachent, c'est
> exactement le rapport du thème sombre inversé. »* Écartées : la boule sombre (`#16171B`) sur le crème — l'objet
> crèverait l'écran ; et garder le sol sombre en éclaircissant les poils — un pansement.
> **À vérifier en le faisant (Tom) :** le CONTOUR reste net (un objet clair sur crème peut se dissoudre au bord — mesurer le
> limbe) ; les DALLES restent lisibles sur le sol clair (elles portent les mondes) ; l'ÉCART DE LUMINOSITÉ tombe dans la
> même fourchette qu'en sombre.
> ⚠ **Deux mises au point, dites à Tom :** (1) sa numérotation n'était pas la mienne — ma « 3 » était la boule sombre sur
> crème, qu'il écarte ; sa « 3 » (le sol clair) est une option nouvelle ; (2) les écarts « 61 » et « 33 » qu'il m'attribue,
> je ne les ai pas mesurés : le critère se mesure avec la métrique du §3 (0,2126 R + 0,7152 G + 0,0722 B), et la valeur
> de référence est celle du thème SOMBRE, relevée — voir le point de départ dans le chapitre du lot.
> **Candidat de la loi pour le sol clair :** la teinte claire de la nature (PROMI-SPECIFICATIONS §1.2 : Promi `#CBAAFF`,
> Chiche `#FFC0A8`, Nuée `#D0B0FF`) — rien d'inventé.

Vu en regardant les captures finales (`sauvegardes/aura-orbite-lot/finales/aura_light*.png`). **La planche
de l'Orbite est peinte sur le fond sombre, et seulement lui** (`_v_planche.js` l. 427 : `fond:'#16171B'`).
Dans l'app, le canevas est transparent (le fond de l'écran passe derrière) : en clair, le CRÈME passe
entre les poils. Les cellules du sol, au poil le plus court (`if(ci>=NCOL && tai>0) tai--`), s'en
éclaircissent ; la grappe, plus fournie, reste bleu soutenu. **Le pavage se lit alors en grandes plages
bleu nuit à bords polygonaux** (bas-droite de la boule), et sur la sphère VIDE ça peut se lire comme une
tache carrée. En sombre, la même structure existe mais le fond sombre la fond.
**Ce n'est pas un défaut prouvé** — c'est la Toile en clair (cellules vides claires), transposée sur la
sphère — **mais personne ne l'a regardée en clair avant ce lot.** Trois options, sans en choisir une :
1. **la garder** — la sphère en clair dit la Toile en clair ;
2. **une peau opaque sous le poil, en clair** (la couleur du sol, pas le crème) — la sphère a le même
   corps dans les deux thèmes ; seule la lumière autour change ;
3. **peindre sur le fond de la planche** (`#16171B`) dans les deux thèmes — une boule sombre posée sur
   le crème.
Rien n'est changé en attendant.

#### Q183 · LA FICHE DE LA PERSONNE PORTE « COMMENT ÇA ÉVOLUE » EN GRATUIT — **tranché par Tom : le graphe va au Cercle** — à faire dans le lot de la fiche (Q184)

Toucher un Noyau ouvre la fiche de la personne — l'écran EXISTANT de l'app (`openPerson`), pas refait
dans ce lot. Elle porte une courbe « COMMENT ÇA ÉVOLUE » (captures `aura_{dark,light}_personne.png`).
Or le chapitre du lot range « les graphes d'évolution » dans ce que le Cercle ajoute à l'Aura. Je ne
tranche pas : à régler avec le Cercle (garder la courbe en gratuit sur la fiche de la personne, ou la
réserver).

#### Q181 · LE RÉGULATEUR DE DENSITÉ CHANGEAIT LA MATIÈRE SOUS LES YEUX — **VALIDÉ par Tom** (10 septembre 2026)

> **Tom :** *« ta correction est validée. Le palier ne s'applique qu'à l'ouverture suivante, plus rien ne change sous
> les yeux. Le prix — une séance sur appareil lent reste au palier de départ — est acceptable. L'alternative en fondu
> attendra. »* L'alternative (paliers emboîtés + fondu) n'est PAS abandonnée : elle attend.

Tom, 10 septembre : *« si le régulateur est nécessaire, il l'est — mais il doit être imperceptible »*.
**Mesuré** (`sauvegardes/aura-orbite-lot/mesure_regulateur.py`, planches `regulateur/paliers_{dark,light}.png`) :
- **Ça se voyait.** Un palier n'est pas un sous-ensemble du précédent : c'est un AUTRE semis (la spirale
  dépend du nombre de poils, chaque poil change de place). Même vue : **71 à 78 % des pixels changent**,
  10 à 15 niveaux en moyenne. **La matière s'éclaircit en clair** (+4,8 niveaux de luminance à 90 000,
  +11,2 à 75 000 : le fond crème passe entre les poils, les îles sombres deviennent un semis pâle) et se
  troue de noir en sombre (−2,8 / −6,6).
- **Le premier passage à un palier fige une image de 783 ms** (le semis et le cache refaits d'un coup).
- **Ça remontait** : charge levée, 75 000 → 90 000 en ≈ 3 s, puis → 110 000 en ≈ 13 s. Un épisode de
  charge = **quatre changements de toute la texture**.
- **Quand** : jugé sur les 45 dernières images, suspendu seulement tant qu'un creux existe. **Rien ne
  l'empêchait en plein élan** (l'élan dure jusqu'à 5,2 s, le creux se referme en 0,4 s) — possible par le
  code ; dans ma mesure l'élan s'était éteint avant le premier palier, je ne l'ai donc pas observé.

**Tranché (option la plus sobre) : le régulateur mesure et VISE pendant qu'on regarde, et la vise ne
s'applique qu'à l'OUVERTURE suivante**, pendant que l'écran se bâtit — aucun changement de matière ni
image figée sous les yeux, jamais. La vise est gardée d'une ouverture à l'autre. Coût, dit franchement :
une session sur un appareil lent reste entière au palier où elle a commencé. Il pèse peu : sur un
processeur ×4, 110 000 poils tournent à 17 images/s et 75 000 à 22 (Q178) — le régulateur n'achète que
peu de fluidité ; le vrai levier est la résolution du tampon.
**L'alternative, si Tom veut que la densité s'adapte PENDANT la vue :** rendre les paliers EMBOÎTÉS (un
seul semis de 110 000, les paliers plus bas n'en gardent qu'une partie, tirée au hasard) et ÉCLAIRCIR
PROGRESSIVEMENT sur une ou deux secondes — seuls les poils retirés disparaissent, en fondu. C'est une
retouche du moteur (semis + boucle du peintre), un lot à part.
Contrat du juge réécrit au niveau de cette décision (`releve-aura.py`, famille 8 ; original
`sauvegardes/releve-aura-avant-regulateur.py`).

#### Q180 · L'OMBRE DE DALLE ÉCRIT SUR LES DOUZE ÉCRANS, FERMÉS COMPRIS, À CHAQUE IMAGE — **hors lot, à traiter**

Trouvé au profileur en cherchant l'image de 267 ms de l'élan. La boucle `frame` des écrans
`.tuto-fond` (≈ l. 8917) tient pour « visible » tout élément dont `offsetParent` n'est pas nul — or un
écran fermé n'est pas en `display:none`, il est glissé hors champ. Elle écrit donc `--gx`, `--gy`,
`--grot` sur **les douze** écrans (`.tuto-fond`, `#createSheet`, `#settingsScreen`) à chaque image : ces
variables s'héritent, et la lecture d'`offsetParent` à l'image suivante force le recalcul de style de
milliers de nœuds cachés. **Mesuré pendant l'Aura : 27 % du temps du fil principal ; 1,6 % une fois ces
écritures ignorées sur les écrans cachés** (24 480 écritures en 20 s).
Le lot de l'Aura ne corrige que ce qui le touche : tant qu'elle est ouverte, les écrans cachés dessous et
l'Aura elle-même ne reçoivent plus ces écritures. **Le coût existe partout ailleurs** (la Toile, le Fil,
l'Index…) : la correction propre est dans cette boucle elle-même — ne peindre que les écrans `.show`.
C'est une règle existante d'un autre lot : **pas touchée, à décider.**

#### Q179 · Le Studio n'intervient nulle part sur l'Aura — **CONSTAT** (Tom, 10 septembre 2026), pas une décision en attente

Le **sol** prend la nature majoritaire de ce qui est tenu ; les **dalles** gardent le monde de LEUR
plantation ; les **arcs** portent l'état. Aucun élément de l'écran ne suit la palette ni le monde choisis
au Studio. C'est ce que le contrat réécrit de `redteam_ecrans.py` protège (« le Studio ne repeint pas
les dalles déjà plantées », qui remplace « les teintes suivent le Studio » de l'ancienne Aura).

#### Q178 · LA DENSITÉ SUR UN VRAI TÉLÉPHONE — PAS MESURÉE, faute d'appareil — **à faire par Tom**

> **⚑ LE PLANCHER EST L'IPHONE 12 — décision Tom, 11 septembre 2026.** *« L'iPhone 12 est le plancher. Puce A14,
> encore massivement en circulation. »* Tout ce qui doit tourner sur tous les téléphones visés — la sphère de
> l'Aura d'abord — se juge contre ce palier, pas contre le Mac du banc ni contre un processeur ralenti ×4 ou ×6
> (ce ne sont que des substituts). **La sphère se mesure contre ce palier dès qu'un iPhone 12 (ou un appareil A14)
> est joignable** : palier tenu à la SECONDE ouverture (`_aura.etat()` : `palier`, `ms`, `cede`, `vise`), et la
> taille de contact lue au capteur (`emp.a`). Si 110 000 poils ne tiennent pas sur A14, c'est la sphère qui change
> (CHANTIERS §9, « le téléphone »), pas un réglage.

Aucun téléphone n'est joignable depuis la machine du banc. Mesure de SUBSTITUTION, dite comme telle :
Chromium sur le Mac Intel i5-8279U, puis le même processeur ralenti ×4 (le « mobile moyen » de
Lighthouse) et ×6 — temps de `peint` par image, sphère en rotation lente, dans l'app :
```
processeur  110 000    90 000    75 000     le gouverneur, parti de 110 000
   ×1      13,7 ms   12,2 ms   10,6 ms     reste à 110 000
   ×4      58,4 ms   51,9 ms   45,7 ms     descend à 75 000 (2 paliers) — 22 images/s
   ×6      88,6 ms   78,9 ms   69,7 ms     descend à 75 000 (2 paliers) — 14 images/s
```
**Ce que ça dit, franchement :** la densité cède, le comportement tient (prouvé sous ×6 par
`releve-aura.py` : la rotation continue, le doigt tourne toujours) — **mais sur un processeur ×4, même
le plancher ne tient pas 60 images par seconde.** Le coût n'est PAS proportionnel au nombre de poils :
75 000 coûtent encore 78 % de 110 000. Il y a une part FIXE (~19 ms à ×4) — vider et verser le tampon
de 592 × 592, la peau, le comblement — qui dépasse à elle seule le budget. **Le levier sur un appareil
lent est la RÉSOLUTION du tampon, pas le nombre de poils** ; il demande de rendre `D` (fixé à 2 dans
`_v_moteur.js`) et l'atlas des poils dépendants de l'appareil — un lot à part, et une décision (moins
de pixels, c'est une matière plus douce à l'œil).
**⚠ UNE RÉSERVE À NE PAS PERDRE (Tom, 10 septembre) : le juge pilote une souris, pas un doigt.** Le
chemin qui lit la TAILLE DU CONTACT au capteur (`PointerEvent.width/height`, borné entre la pulpe de
l'index et celle du pouce) n'est JAMAIS testé : c'est la valeur par défaut du pouce qui joue partout.
**À vérifier sur appareil, en même temps que la densité** — `_aura.etat().emp.a` pendant un appui rend
le demi-axe réellement lu (0,40 = le pouce par défaut ; entre 0,26 et 0,40 = le capteur a parlé).

**Pour mesurer sur l'iPhone :** servir le dossier sur le réseau local (un SECOND serveur, pour ne pas
toucher au 8752 des outils), ouvrir l'Aura dans Safari sur le téléphone, puis sur le Mac Safari →
Développement → l'iPhone → console : `_aura.etat()` rend le palier tenu (`palier`), la médiane par image
(`ms`), le nombre de cessions (`cede`) et le palier VISÉ (`vise`). ⚠ **Depuis Q181, la vise ne s'applique
qu'à l'ouverture suivante** : ouvrir l'Aura, la laisser tourner ~10 s, la fermer, la rouvrir — c'est
le palier de la SECONDE ouverture qui dit ce que l'appareil tient.
