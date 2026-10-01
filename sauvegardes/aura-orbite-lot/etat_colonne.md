## ⚑ L'AIR DE LA COLONNE DE L'AURA — la cote se dérive, la colonne défile · 10 septembre 2026

> **`app.html` modifié** — md5 avant `e10da6dc1bfb81aef2081b34e0c39b6b`, **après `8e579374b07507b90015e0f6d18bb437`**.
> Même bloc `lot-AURA-ORBITE`, refabriqué (`sauvegardes/aura-orbite-lot/fabrique.py`) : aucune règle
> existante touchée, aucune ligne du moteur de la Toile. Tom : *« sous le commentaire de la sphère, les
> disques sont trop près : ça ne respire pas. Baisse tout ce qui est en dessous. Mesure, ne rapproche
> pas à l'œil, et vérifie sur l'image rendue. C'est la quatrième fois qu'un espacement revient, ça ne
> doit plus arriver. »*

### 1 · MESURÉ AVANT DE TOUCHER — aux boîtes ET à l'encre, les cinq phrases, deux thèmes
`sauvegardes/aura-orbite-lot/mesure_air_aura.py`, relevé `air_avant.log` :
```
                                   phrase d'une ligne   phrase de deux lignes
sphère → phrase                         50,3                  50,3
PHRASE → DISQUES                        27,3                   3,7   (5,5 à l'encre)
prénoms → légende                       28,0                  28,0
légende → « ce que tu as tenu »         28,0                  28,0
LIBELLÉS DES DALLES → BOUTON             2,7                   2,7
```
**La cause — le piège du §8, « une cote dérivée n'est pas un espace » :** la planche posait les Noyaux à
**454** (396 dans son gabarit), calcul fait pour une phrase d'UNE ligne. Deux des cinq phrases de Tom en
font DEUX (« Rien de ce qui est ici n'a été dit à la légère. », « On ne dirait pas comme ça, mais c'est
du solide. ») : la seconde ligne mangeait l'air. **Mon port avait recopié le défaut de la planche à
l'identique** — et aucun relevé fait sur une seule phrase ne pouvait le voir. Et les libellés des
dalles touchaient le bouton (2,7 pt ; 1 px dans la planche), dans tous les états.

### 2 · LA CORRECTION — la colonne se dérive, et elle défile
- **`place()`** (aura.js) : les Noyaux = bas RÉEL de la phrase + **26,675** (l'air que la planche laissait
  sous UNE ligne : 454 − 403,7 − 18,9 × 1,25) ; la légende et « Ce que tu as tenu » suivent du même écart
  (28 de chaque côté, inchangé) ; le bouton = bas des libellés + **28** (le rythme de la colonne). La
  fonction compare avant d'écrire, et se relance quand la phrase change de hauteur (polices arrivées).
- **La colonne DÉFILE sous le plateau** : le cadre garde ses cotes 390 × 844, défile, et ROGNE au bas du
  plateau (`clip-path: inset(100px 0 0 0)`) — la parade de l'Index (§8). Il se DÉCLARE (`data-defile`).
  La sphère garde `touch-action:none` : un doigt posé sur elle la tourne, il ne fait pas défiler.
- **Le bouton n'est JAMAIS coupé par le pli** (Tom — Q186 : *« un vrai défaut, pas un choix »*) : à
  l'ouverture il est ENTIER avec sa marge (bas ≤ 822) ou FRANCHEMENT sous le pli (haut ≥ 844). Avec l'air
  de 28, il ne peut plus être entier dès qu'il y a des Noyaux : il tombe sous le pli, on le découvre en
  défilant. (Une première version le laissait coupé : de 3,4 pt avec une phrase d'une ligne, à mi-hauteur
  de son libellé avec deux — 34 pt visibles sur 60.)
- **Rien au-dessus de la phrase ne bouge.** L'état vide ne bouge pas (le bouton y reste à 762, entier).

**Après** (relevé `air_apres.log`, deux thèmes identiques) :
```
                                   phrase d'une ligne   phrase de deux lignes
PHRASE → DISQUES                        27,7                  27,1   (28,0 / 29,0 à l'encre)
prénoms → légende → titre              28 · 28               28 · 28
LIBELLÉS DES DALLES → BOUTON            27,8                  27,8
la colonne défile de                    ≈ 26 pt               ≈ 49 pt
```
**Le pli, mesuré sur la version insérée** (`air_pli.log`, deux thèmes identiques) : dans les états
non vides, le bouton est FRANCHEMENT sous le pli — son haut à 844 exactement, rien de lui ne se voit à
l'ouverture ; libellés → bouton 84,4 pt (phrase d'une ligne) et 61,4 pt (deux lignes), la colonne défile de
≈ 82 pt. **Dans l'état vide, le bouton est ENTIER à l'ouverture, 22 pt du bord** (bas 822) — c'est le seul
écran qu'un nouveau verra (Tom). **⚠ Mais rien n'annonce le bouton sous le pli** : sous les derniers
libellés, 84,4 / 61,4 pt de fond nu jusqu'au bas de l'écran, rien ne passe le pli.
**Q187, tranché par Tom — c'est le fond nu qui trahit, pas le bouton ; on supprime le vide, on n'ajoute pas
de signe** (ni flèche, ni ombre, ni fondu : trois choses interdites). « Ce que tu as tenu » porte jusqu'à
**SIX** dalles, deux rangées : une rangée de plus, que le bord de l'écran coupe, dit qu'il y a la suite —
le principe de la rangée des six qui défile. **Mesuré** (`mesure_rangees.py`, le DESSIN des dalles, simulé à 3 · 4 · 5 · 6 · 9 tenues) :
```
paroles tenues   phrase d'une ligne (3 phrases sur 5)             phrase de deux lignes (2 sur 5)
3 ou 4           une rangée · bouton sous le pli, fond nu           idem
5 (3 + 2)        2e rangée : trou à droite · dessins entiers,       trou à droite · dessins cachés à 26 %
                 à 8 pt du bord · libellés sous le pli
6 et plus        2e rangée pleine · dessins entiers, POSÉE contre   2e rangée pleine · cachée à 26 %
                 le bord · libellés sous le pli
```
**RÈGLE (Tom — Q189) : la seconde rangée paraît à partir de CINQ dalles tenues ; en dessous, la
première seule** — une rangée au tiers (3 + 1) dirait « il en manque deux ». À cinq, le trou d'une case est
accepté. Portée dans le code (`K.RANG2`, `nbMoisson()`) et EN DUR dans le juge (`RANG2`). **Prouvée** : sur l'app d'avant (`31a0ed37…`) le juge
prend « 3 dalles tenues au lieu de 5 » ; sur la version corrigée il passe ; mesurée à 3 · 4 · 5 · 6 · 9 tenues —
à quatre, une rangée (3 dalles) ; à cinq, 3 + 2 ; à six et au-delà, deux rangées pleines.
**Restent ouverts :** avec une phrase d'une ligne, la seconde rangée est posée contre le bord plutôt que
franchement coupée ; et à quatre tenues ou moins, le fond nu revient (Q188) — le bouton ne peut pas y rester
entier avec l'air de 28 (son bas tomberait à 848 ou 871).
**Q188 — quand il n'y en a pas assez :** dès qu'on a tenu trois paroles ou moins, il n'y a qu'une rangée et
rien à couper ; le fond nu revient. C'est une question de COMPOSITION de la colonne, posée à Tom.

### 3 · LE CONTRÔLE — pour que ça n'arrive plus (CLAUDE.md §8, « un espacement qui revient pour la cinquième fois »)
**J'ai réécrit un contrat de test et j'en ai ajouté un** (`releve-aura.py` ; original
`sauvegardes/releve-aura-avant-colonne.py`) :
- **positions** : la rangée, la légende, le titre et le bouton ne sont plus attendus à des cotes figées
  (454 · 589 · 633 · 762) — ils se DÉRIVENT du bas réel de la phrase et des deux airs décidés, **écrits en
  dur dans le juge** (26,675 et 28).
- **9ᵉ famille, « air de la colonne »** : pour CHACUNE des cinq phrases, deux thèmes, CHAQUE paire de
  blocs, texte ou non — phrase → disques ≥ 26 et indépendant du nombre de lignes, légende centrée,
  libellés → bouton ≥ 26, **le bouton jamais coupé par le pli à l'ouverture** (Q186), bouton atteignable
  en défilant, rien du cadre au-dessus du plateau une fois
  défilé ; **et à l'encre, sur l'image rendue**, phrase → disques ≥ 26. `redteam_air.py` ne mesure que des
  paires de TEXTES : il ne pouvait pas voir une phrase contre une rangée de disques.
- **débordements** : un bloc qui dépasse VERS LE BAS dans une colonne DÉCLARÉE, qui tient dans l'appareil
  et qui rogne, n'est pas un débordement (la règle de la rangée glissante, tournée d'un quart).
**Prouvés dans les deux sens :** sur l'app d'avant (`e10da6dc…`) le juge est PRIS — 8 écarts de position,
20 d'air (3,7 pt sous la phrase, 2,8 sous les libellés, 6,0 à l'encre) ; sur la version corrigée il
passe. La preuve des 18 contrats de l'Aura, sur l'app insérée finale (`8e579374…`), avec l'instrument corrigé : **deux passes, les 18 passent tels quels et PRENNENT le défaut posé exprès** (`preuve_finale_1.log`, `preuve_finale_2.log`, journaux entiers). La règle du pli, prouvée elle aussi : sur la version d'avant (`3ec7bd34…`) le juge prend le bouton COUPÉ à l'ouverture (33,6 pt visibles sur 60 avec deux lignes, 56,6 avec une), sur la version corrigée il passe. Les contrôles réécrits contre des sondes (`preuve_defile.py`) : la version telle quelle passe ; les quatre défauts
sont PRIS — le cadre qui ne se déclare plus, le cadre qui ne rogne plus, un bloc qui sort par le côté
(pris par `DEBORD`), le cadre qui défile sans rogner sous le plateau (pris par `PROTEGE`). Le code testé
est celui du juge, importé. **⚠ Une sonde a d'abord été AVALÉE** (§7) : posée dans `<head>` avec la même
spécificité que le bloc, qui vient après elle, elle ne s'appliquait pas — la colonne défilait encore de
48 pt. Renforcée, et chaque sonde affiche désormais l'état réellement obtenu avant d'être jugée.

### ⚠ LA PREUVE A ROUGI UNE FOIS APRÈS INSERTION — ARRÊT, RESTAURATION, ET CE QUE C'ÉTAIT
Règle de Tom : *batterie verte qui rougit → arrêt immédiat et restauration*. Insérée, la version à la règle
des cinq (`8e579374…`) a donné **2 contrats « légende centrée » NON PRIS** (redteam_ecrans et redteam_air).
La série a été arrêtée, **`app.html` remis à `e10da6dc…`** (la dernière série complète verte), la version
rouge gardée à côté, tout le diagnostic fait sur une COPIE.
- **Le contrat n'était pas éteint** : isolée, la sonde (+9 px sur la légende) s'applique et se voit
  (28/28 → 37/19), sur la version rouge comme sur la verte ; rejouée, la preuve la PREND.
- **C'était l'instrument** : la sonde et la mesure étaient posées en DEUX appels ; une image pouvait passer
  entre eux, la colonne se recalculer (`place()`) et réécrire la cote de la légende — la sonde était
  avalée (§7, « une sonde qui n'est pas prise peut être avalée »). **Sonde et mesure sont désormais dans la
  MÊME tâche** — le contrat ne change pas ; original `preuve_contrats-avant-meme-tache.py`.
- **L'audit des sondes (demandé par Tom) a trouvé deux contaminations DANS une passe** (pas d'une passe à
  l'autre : chaque passe ouvre une page neuve) : les sondes de la légende se « défaisaient » par
  `removeProperty('top')`, ce qui effaçait AUSSI la cote écrite par `place()` — la légende retombait sur
  l'ancienne cote figée du CSS jusqu'à la réouverture ; et la sonde de la phrase remettait le texte sans que
  la colonne se recalcule tout de suite. **Corrigé** : chaque sonde remet la valeur d'avant et sa priorité,
  la phrase remise force le recalcul, et **le verdict nomme les contrats qui ratent** (original
  `preuve_contrats-avant-retraits-exacts.py`). Piège inscrit au §8 de CLAUDE.md.
- Sur six passes, une autre a donné « 1 contrat à reprendre » **sans que je sache lequel** — mon filtre
  n'imprimait que la légende et le verdict, le journal entier n'était pas gardé : l'instrument était
  aveugle (Q190, « vu une fois, non reproduit ») ; **non reproduit** : sept passes de suite à 18/18 sur la version rouge,
avec l'instrument corrigé (`preuve_rouge_1…7.log`). Je le dis tel quel : non reproduit, non identifié. Puis
réinsertion (`8e579374…`, identique à la copie jugée) et série complète.

### 4 · CONTRÔLES
**Série complète, EN SÉRIE, sur l'app insérée finale `8e579374…`** — journal
`sauvegardes/aura-orbite-lot/bat_apres10.log`, 17 batteries, aucune sortie en erreur :
```
redteam_ecrans      150/150        redteam_vide        61/61
redteam             15/15          redteam_air         ✅ 442 paires, 38 écrans, deux thèmes
redteam2            10/10          redteam_champ       32/32
redteam3            18/18          releve-design       ✅ aucun écart
redteam_demande     19/19          redteam_fonctions   22/22
redteam_toile       17/17          redteam_polices     0 couple absent
redteam_geste       13/13          redteam_superpo     0 recouvrement de texte
redteam_verbe       6/6            releve-aura         ✅ au vert — 9 familles (air de la colonne compris)
redteam_filets      0 filet parasite
```
(`redteam_air` compte 442 paires au lieu de 448 : les libellés de la seconde rangée sont sous le pli,
il y a moins de textes visibles à apparier ; aucun air ne s'est resserré.) Syntaxe : `node --check` — OK.

### 5 · DÉCISIONS ET CONSTATS DE CE TOUR (QUESTIONS.md)
- **Q181 VALIDÉ** — le régulateur n'applique son palier qu'à l'ouverture suivante ; l'alternative en fondu attend.
- **La sphère ne s'explique pas** (décision Tom) — pas de légende, pas de phrase qui dit ce qu'elle est.
- **Q184** — la fiche de la personne : hors DA, trois interdits (la courbe « COMMENT ÇA ÉVOLUE » → Cercle,
  Q183 ; un mot d'harmonie pointé vers quelqu'un → règle 1 ; « 3 Promi échangés · 1 reçu · 2 donnés » →
  règle 4). **Rien de corrigé** : c'est le lot suivant, avec un audit.
- **Q185** — l'aide « i » décrit l'ancienne Aura (grand chiffre, harmonie, jauge, meilleure Nuée).
- **Q187 TRANCHÉ (Tom)** — supprimer le vide, pas ajouter un signe : une seconde rangée de dalles, coupée par le bord.
- **Q188** — trois paroles tenues ou moins : une seule rangée, rien à couper — question de composition, pour Tom.
- **Le bouton en thème clair n'est pas bleu nuit** : il est à l'encre `#16171B` (trait et texte), la même que le trait
  du plateau — la grammaire des contours. Le seul bleu nuit de l'écran est le fond du plateau en SOMBRE, `#12142A`, la
  teinte de corps du §1.3, posée sur le sol `#16171B` de la planche ; et en clair, la plage de la sphère (Q182).
- **Q186 TRANCHÉ (Tom)** — la colonne qui défile est la bonne réponse (*« mieux vaut assumer le défilement
  que serrer »*) ; le bouton coupé est un vrai défaut : entier ou franchement sous le pli, jamais coupé.
- **Q185 — VÉRIFIÉ : l'aide « i » n'explique pas la sphère** (HTML statique, aucun script n'y écrit ; ni
  « sphère », ni « enroulée » ; « orbite » y désigne l'ancien double Noyau du Cercle). Elle décrit l'ancienne
  Aura : un lot de textes à part, non corrigé.
- Captures sur disque, non envoyées (`sauvegardes/aura-orbite-lot/colonne/`).

### 6 · LA SUITE — l'ordre fixé par Tom
1. **l'Orbite en thème clair** — Q182 : la planche n'a été peinte que sur fond sombre ; trois options.
2. **la fiche de la personne** — Q184, **l'audit d'abord** (comme pour le partage), puis la DA.
3. **la densité et le capteur sur un vrai téléphone** — Q178.
4. **le Cercle.**
**Le chantier 58 reste hors de tout ça** — prioritaire quand on reviendra à la performance.
