### ⚑ v148 (16 oct. 2026) — CLÔTURE DE LA SÉRIE : LES RONDS ORANGE RETIRÉS, LA PHRASE DE VALIDATION AU « ! », LE RIDEAU À VITESSE CONSTANTE, LE RUBAN AMANDE, LES CARTES EN CONSTRUCTION DE FICHE, « GARDER DE CÔTÉ », « PROMI PLANTÉ ! » PAS À PAS, LES TRANSITIONS EN FLAQUES, LES PHRASES DU GUIDE, L'ORDRE DU GUIDE. (Décisions Tom.) Ce bloc CORRIGE v147 (l'échelle, C-141 « cellule par cellule », le guide « toucher ailleurs fait avancer », C-118 l'épaississement), v146 (« Promi planté ! » et le reste au toucher, la marée) et v144 (le guide).
> **Validés par Tom : C-088 (Ritournelle), C-094 (le guide en flaques, « flou ok »), C-116 (les commentaires), C-129 (pas d'emoji), C-135 (la Pelote tout de
> suite), C-142 (le menu du +, « parfait » : on fige) ; et, dans l'onboarding, le flou et l'arrivée douce des encarts à leur place (« top de top, on garde ») :
> ON N'Y TOUCHE PLUS.**
> **⚑ EXCEPTIONS NOMMÉES AU « ! » — LA LISTE COMPLÈTE : « Ma Parole ! » (v106), « Promi planté ! » (v146), « Parole tenue ! » et « Défi relevé ! » (v148,
> C-144 : les phrases de validation de « tenir »).** Espace insécable avant « ! ». Partout ailleurs, pas de « ! ».
> **⚑ C-143 — LES DEUX RONDS ORANGE DE SIGNATURE SONT RETIRÉS PARTOUT** (fiche, page +, trois natures, deux thèmes). *La cause* : le canevas du geste
> (`#tenirCv`, `#planterCv`) peignait encore les deux points de guidage du geste d'origine ; sur la fiche une règle le posait à `opacity:0 !important` — mais
> **dans WebKit l'animation `tenirPouls` l'emporte sur ce `!important`** : sur l'iPhone les ronds pulsaient, Chromium ne les montrait pas. Les peintres ne les
> peignent plus, l'animation est coupée. Le chevron orange du départ (C-133) reste. Juge : **`redteam_ronds.py`** (WebKit ; rouge sur v147).
> *La règle* : **un `!important` ne bat pas une animation CSS dans WebKit — on retire la cause (le dessin), jamais on ne la cache.**
> **⚑ C-139 — AUCUNE INVITATION ANIMÉE DANS L'APP tant que Tom n'a pas choisi** (le chevron suffit). `promi-invite-variantes.html` ne montre plus que
> l'invitation (la fiche du cadre ne reçoit plus le doigt : Tom voyait la validation) : **A, les POINTS du chemin s'allument ; B, la FLÈCHE avance et trace
> devant elle** (44 pt). `redteam_ronds` E : la bande du trait ne bouge pas au repos (7 s).
> **⚑ C-144 — LA PHRASE DE VALIDATION** : centrée sur sa ligne ; « Parole tenue ! », « Défi relevé ! » (`TEXTES_ENGAGEMENT.tenir`) ; la nappe la porte au milieu.
> **⚑ C-118 — LE RIDEAU DESCEND À VITESSE CONSTANTE.** *La cause* : deux mouvements bout à bout — le trait s'épaississait (12 → 46 pt en 160 ms), puis le
> rideau partait en ease-in-out et restait caché sous le trait épaissi jusqu'à ≈ 300 ms (« il s'arrête puis repart ») ; et l'horloge partait à la pose
> d'un canevas de 1170 × 2532 alloué dans la même image (le premier pas sautait). *Aujourd'hui* : un seul mouvement, le front part du bas du trait dès la
> première image, vitesse constante jusqu'à la barre (700 ms), canevas alloué à l'avance, horloge à la première image peinte ; la remontée ne change pas.
> Juge : `redteam_tenir` G, H (régularité image par image ; jugée au calme seulement, C-137).
> **⚑ C-148 — LE RUBAN AMANDE** (`lot-V148-RUBAN`) : plus de rectangle (le fond de la zone du geste est transparent, A2) ; un ruban PLEIN `#8FE08F` qui suit
> l'onde du trait, 94 pt d'épaisseur (80 % des 118 d'avant), bords légèrement irréguliers (0,4 à 3,5 pt) ; il naît en 200 ms et se retire en 240 ms ; le mot
> du trait n'est jamais coupé en deux. Juge : **`redteam_ruban.py`** (WebKit ; rouge sur v147).
> **⚑ C-147 — LES CARTES DE L'INDEX, DU FIL ET DU FIL D'UN CERCLE SONT CONSTRUITES COMME LA FICHE, DANS LES DEUX THÈMES** : corps `#0E78F2` · `#7C3F58` ·
> `#5D4978`, la terre `#2B1020` d'une tenue, l'état crème (« TENUE » en amande). Dans `lot-S4` : `light()` rend toujours faux pour une carte ; le résolveur
> d'état de la fiche répond « sombre » pour une fausse fiche (`__carte`). ⚠ **Le trait d'une carte tient donc les mêmes contrastes que la fiche : Chiche et
> Cercle IMPOSSIBLES à 3:1 face aux deux fonds (Q513), l'orange « à tenir » à 1,03 sur le cobalt (Q514), la crête d'une tenue sur la terre à 1,68 (Q528)** —
> `redteam_contraste_trait` est rouge PAR DÉCISION À PRENDRE.
> **⚑ C-149 — LA PAGE +** : les phrases « se retourne » sont retirées partout (« Un Chiche se lance, il ne se retourne pas » et l'aide du sens) ; « Garder de
> côté » est visible, ACTIF seulement quand la page a changé depuis son ouverture (une personne ajoutée, une modification — `window._garderEtat`, la page se
> signe à l'ouverture) ; inactif : non souligné, sa teinte rapprochée du corps (30 %, sans transparence), il ne fait rien. Juge : `redteam_garder` E–I.
> **⚑ C-124 — LA PAGE DU PREMIER PROMI ET « PROMI PLANTÉ ! »** : l'Atkinson de l'onboarding −7 % (texte 27 → 25 pt, liste 24 → 22,3) ; « Promi planté ! »
> PAS À PAS (`finPas`, `window._onbFinPas`) — au départ le titre SEUL, la parole et ses voisines plus haut (centre 647 pt, comme v146) ; chaque toucher : le
> texte remonte et les dalles descendent du même mouvement (la loi de la vue, 133 ms), puis le paragraphe suivant se trace dans la place faite —
> « Ton premier Promi… plus qu'à le tenir. » (à la taille des suivants), Primo · Deuxio · Tertio, puis « Le reste se découvre en traçant. » et « La suite
> t'appartient. » (9 pt plus bas) ; 22 pt d'air entre le texte et les dalles à chaque pas ; les dalles finissent à 722 pt (738 en v147, −16) ; un quatrième
> toucher mène au compte. ⚠ **Un juge qui traverse l'onboarding touche quatre fois** (`data-onb-reste` = 1, 2, 3 puis « fini »).
> **⚑ C-141 — LES TRANSITIONS DE L'ONBOARDING SONT EN FLAQUES** (`window._passageFlaques` : le moteur du guide, `Flaques.Scene` — 12 à 20 germes, naissances
> étalées, ponts ; mode « ouvre » : une couverture se troue en flaques ; « couvre » : la page suivante naît en flaques par-dessus). **Plus de balayage, plus
> de fondu, plus de glissement, rien d'un coup** : ① l'arrivée sur le prénom : le voile s'ouvre en flaques (1,1 s ; v147 : cellule par cellule) ; ② le trait
> du premier Promi naît en flaques à la première lettre (700 ms) ; ③ la page du trait est recouverte en flaques par la Toile d'avant (620 ms ; v147 : un
> fondu) ; ④ « Promi planté ! » est recouvert en flaques (650 ms ; v147 : un BALAYAGE de droite à gauche) pendant que le panneau du compte naît en flaques
> à sa place (800 ms ; v147 : il glissait du bas) ; ⑤ le panneau du compte est recouvert en flaques (500 ms), puis l'écran entier s'ouvre en flaques sur
> l'accueil (900 ms), les voisines parties et la vue recadrée SOUS la couverture ; ⑥ l'arrivée douce des encarts : inchangée (validée). Juge :
> **`redteam_transitions_onb.py` réécrit** (image par image, le passage rejoué : ≥ 3 trous séparés à 8–45 % ouverts ; rouge sur v147).
> **⚑ C-145 — LES PHRASES DU GUIDE** : en GRAS (Atkinson 700), 29 pt (27 × 1,07), interligne 1,45 (42 pt), mots-clés PromiLate 29 ; « monde » `#8363AA` en
> clair, `#C9A8F5` en sombre (le rose de v147 ne se lisait pas — Q518) ; aucun contour ; tracées (les chemins médians de l'Atkinson 500 couvrent le gras :
> vu à l'image, deux thèmes).
> **⚑ C-146 — L'ORDRE DU GUIDE** : au lancement, le flou du Studio ; **tant que le Studio n'a jamais été ouvert, toucher ailleurs montre le RAPPEL — la phrase
> du Studio, écrite de nouveau, mot pour mot — et seulement lui, autant de fois qu'on touche** ; jamais l'étape ni la phrase du + avant le Studio (v144 : toucher
> ailleurs y menait) ; le Studio ouvert puis refermé, avec ou sans changement → le flou et l'invitation vers le +. **L'app quittée à l'étape du Studio : le
> guide reprend au lancement suivant** (`promi_guide` = « studio » ; « 1 » dès que le Studio est ouvert). Juge : **`redteam_ordre_guide.py`** (rouge sur v147).
> **⚑ L'ÉCHELLE (C-138) — CE BLOC REMPLACE CELLE DE v147** (`lot-V147-ECHELLE-css`, variables `--ech-*`) — un RÔLE = une taille, sur toutes les pages :
> ```
> titre        PromiLate 52 pt — « PROMI » de « Promi planté ! » ; sa suite « planté ! » 42 pt
> phrase       Gilbert 35 pt / 66 — la phrase de promesse (« Toi, c'est … ? », « Je me promets de … »)
> texte        Atkinson 500, 25 pt / 30 — « [Prénom], donc. Enchanté. », « Quid… », « Petite ou grande promesse, elle compte. »
> liste        Atkinson 500, 22,3 pt / 26 — « Ton premier Promi… », Primo, Deuxio, Tertio, « Le reste se découvre en traçant. »
> mot-clé      PromiLate 25 pt — Primo, Deuxio, Tertio ; 32 pt pour « La suite t'appartient. »
> consigne     PromiLate 19 pt — « trace pour planter »
> guide        Atkinson 700, 29 pt / 42 — les deux phrases du guide ; leurs mots-clés (« monde », « Studio », « commence ») en PromiLate 29 pt
> ```
> Juge : `redteam_echelle_onboarding` (neuf rôles).
> **LA RÈGLE DE L'ORANGE (v146, rappelée)** : `#FB4C0D` marque les points de départ d'une action et rien d'autre (le + de l'accueil, le + qui valide un nom, le
> départ de la flèche) ; la même valeur reste celle de « Ma Parole ! » dans les murs (deux jetons, deux rôles). Les ronds orange de signature, qui n'étaient
> pas un départ, sont retirés (C-143).
> **Contrats de test remis au niveau des décisions de ce lot** (originaux : `sauvegardes/*-avant-v148.py`) : `redteam_tenir` (G, H), `redteam_garder` (E à I),
> `redteam_transitions_onb` (réécrit), `redteam_guide` (le rappel au lieu d'avancer ; la phrase en gras, 29 pt, « monde » lilas), `redteam_echelle_onboarding`,
> `redteam_onb_sorties` (« fin » = le titre seul), `redteam_onboarding` (quatre touchers), `redteam_decisions` (les cartes, deux thèmes), `redteam_couleurs_ref`
> (E19 : les cartes).
