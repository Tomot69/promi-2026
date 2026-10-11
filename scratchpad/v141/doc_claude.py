import io
S=io.open('CLAUDE.md',encoding='utf-8').read()
anc="### ⚑ v139 (9 oct. 2026) — RETOURS DE TOM SUR IPHONE : LA PELOTE (CONTOUR FRANC, OMBRE, TOUCHER)"
assert S.count(anc)==1
B="""### ⚑ v141 (10 oct. 2026) — RETOURS DE TOM SUR IPHONE : TROIS RÉCIDIVES (LA PELOTE, RITOURNELLE, LE MUR DU STUDIO), L'ONBOARDING D'AVANT v140, LE GUIDE DE FIN DE PARCOURS. (Décisions Tom.) Ce bloc CORRIGE v139, v140 (qui n'a pas de bloc ici), E2 / E2bis et v136 (C-084) là où ils disent autre chose.
> **Q439, Q441, Q442, Q445 validées. Q444 sans objet (E2bis est remplacé). Q449 : on ne plante plus de dalle sous la barre du bas.**
> **⚑ LA PELOTE (C-083, RÉCIDIVE). ① LE BORD EST CELUI DU PEINTRE D'AVANT v114** (`sauvegardes/app-avant-v114.html`) : les pointes telles que le
> peintre les pose, avec L'OPACITÉ DE LEUR TAMPON. *Pourquoi c'est revenu* : les deux peintres (canevas, carte graphique) posent les poils de
> la même façon (un tampon par poil, le plus opaque gagne) — ce n'est pas eux qui différaient, c'est ce que la COMPOSITION ajoutait après :
> la limite franche (v139), puis l'opacité des pointes resserrée et recolorée (v140). Tout cela est retiré. Restent : le corps opaque (v120),
> qui s'efface de **0,955 à 1,035 R** (à R → 1,012 R il faisait une marche : la frange se lisait comme un anneau pâle derrière un bord net),
> et la correction de COULEUR de v137–v138 (au-delà de 0,92 R, la couleur du vis-à-vis intérieur) — le corps est d'une autre teinte que le
> poil depuis v123, la peau d'avant v114 était de la couleur du poil. ⚠ Deux essais faits et vus, à ne pas refaire : le corps qui prend la
> teinte du poil au bord (anneau SOMBRE), les pointes à la couleur « poil sur corps » avec leur opacité (anneau PÂLE).
> **② LES POILS DU BORD SE COUCHENT DANS LE SENS OÙ LA PELOTE TOURNE** (`tour()`, `o.tour`, `uTour` ; du milieu du rayon — rien — au bord — tout ;
> 0,18 à la rotation de repos, jusqu'à 0,9 sur un lancer ; rien, vue figée). **③ L'ÉTOILE ET TOUT DESSIN GÉOMÉTRIQUE SONT RETIRÉS** : un appui ne
> pose plus AUCUNE trace, et au fond du creux les poils gardent leur sens (le peigne rayonnant convergeait sur un point). **④ LA TRACE EST LA
> SURFACE RÉELLEMENT TOUCHÉE, FORMÉE SOUS LE DOIGT** : tous les 10 pt de geste, la zone de contact du moment reçoit un arc de sa longueur, couché
> dans le sens où le doigt va, inscrit AUSSITÔT ; une zone de contact = UN arc (le dernier). Plus rien n'est posé au lâcher.
> *La règle* : **sur la Pelote, on ne corrige jamais un bord par l'opacité ; et une trace ne se dessine pas après coup, elle s'inscrit pendant le geste.**
> Juges : `redteam_trace` (réécrit : en direct, sans étoile), `redteam_bord`, `redteam_fourrure`.
> **⚑ RITOURNELLE (C-088, RÉCIDIVE — « trop dézoomé »).** Cibles sur 390 pt : **une parole → sa dalle ≥ 60 % de la largeur ; deux, trois, quatre →
> toutes entières ; au plus deux cellules vides entièrement visibles jusqu'à quatre paroles.** *Pourquoi c'est revenu* : v140 cadrait les
> GRAINES avec une marge ; une marge autour de points ne dit rien de la taille des dalles (50 % de la largeur à une parole ; 5 et 7 cellules
> vides entières à trois et quatre). Le moteur cadre maintenant la boîte des CELLULES des paroles à leur poids final (`_boiteSerre`), à 118 %
> de la largeur pour une parole, 100 % au-delà, entre le plateau et la barre ; l'amas des paroles monte plutôt qu'il ne s'étale.
> *La règle* : **un cadrage se calcule sur ce qu'on voit (la cellule), jamais sur des graines.** Juge : **`redteam_ritournelle.py`**.
> **⚑ Q449 — PLUS DE DALLE SOUS LA BARRE.** `plantOne` : borne basse = la barre (710) moins une dalle (0,87 cellule). *La cause du rouge* : une
> cellule REPLIÉE (une dalle partie) était reprise d'abord, sans passer par la zone dégagée (plantations mesurées à 716, 730, 815).
> **⚑ LE MUR DU STUDIO (C-100, RÉCIDIVE — « une fois sur quatre »).** *La cause* : le mur était fait de QUATRE BANDES (54, 19, 44 et 4 pt) ; entre
> elles et autour, le panneau n'était pas un mur. Le mur est LE PANNEAU (`#stpBas`). *Pourquoi les juges ne le voyaient pas* : ils touchaient
> le centre de chaque bande, sans glisser. *La règle* : **un mur est la surface qu'on voit floutée, pas la liste de ses éléments ; un juge de
> toucher répartit ses points sur toute la zone et fait glisser le doigt de quelques points.** Juge : **`redteam_murs_toucher.py`** (huit murs,
> vingt touchers chacun, 20 sur 20). Le bouton « Adopte ce design » n'est pas un mur. **Q447** : pendant la lecture d'une phrase sur le
> panneau des palettes, ses pastilles se retirent (`.mur-lu`).
> **⚑ L'ONBOARDING DE v140 EST RETIRÉ (C-075) : celui d'avant v140 revient EN ENTIER, mot pour mot** (prénom → parole → trait → message de fin →
> compte). `lot-E2` (le script) n'existe plus ; l'étape « principe » et ses textes non plus. Gardé de v140 : la main fantôme sur le trait
> (`onb-trait`), le mot de trace à 19 px, **« Plus tard » à chaque étape — en haut à droite, 12 px (le plancher du §6), sans soulignement**.
> « Toi, c'est ? » : la zone dégagée de la phrase prend toute la largeur. Juge : **`redteam_onb_sorties.py`** (textes EN DUR ; `--r6`).
> **⚑ LE GUIDE DE FIN DE PARCOURS REMPLACE E2bis (C-094 ; C-076 est abandonné par lui).** La barre est complète dès le départ. Une seule fois
> (`promi_guide`), 0,8 s après l'arrivée sur l'accueil d'un parcours COMPLET : un flou (`backdrop-filter:blur(4.8px)`, la valeur des murs) dont
> le MASQUE grandit par zones (1,5 s), net sur l'icône du Studio (× 1,2) — « Chacun sa matière. La tienne est au Studio. » ; la toucher ouvre
> le Studio ; au retour, net sur le + (× 1,1) — « Tout le reste part d'ici. » ; le toucher ouvre les trois natures. Toucher ailleurs ou
> « Plus tard » le dissout ; « Revoir la présentation » le rejoue ; mouvement réduit : posé d'un coup. `lot-V141-GUIDE`,
> `TEXTES_ENGAGEMENT.guide`. **C'est, avec les murs, le seul flou de l'app.** Juge : **`redteam_guide.py`**.
> **⚑ LE CRÈME DES FICHES (C-084) : `#EAD9B9` est RETIRÉ** (« trop beige ») — corps et encarts reprennent `#F7F0DE`, les cartes du fil d'un Cercle
> `#E9D8B7`. **Deux tons clairs dans l'app, pas trois.**
> **⚑ LA PAGE + ET LE TRAIT (C-095)** : « TRACE TA MOITIÉ » à quelqu'un, « TRACE POUR PLANTER » à soi. La main : × 1,3, contour doublé vers
> l'intérieur ; **sur une fiche elle part du MILIEU et suit les points, posés SUR l'onde — et le geste de tenir part aussi du milieu** (il
> faut alors aller presque au bout). Après « tenir » : **« C'est tenu. »** (avant : « Le dessin existe. »).
> **⚑ LA FICHE D'UN CERCLE (C-096)** : « + Planter dans le Cercle » reste la dernière ligne du fil mais se tient à 12 pt au-dessus du bandeau
> (`position:sticky`), le fil défile dessous ; dans Peaufiner il est sous COMMENTAIRES (672, 342 × 62, son + dans son rond), le reste
> remonte de 140 ; « Dissoudre le Cercle » n'a plus d'encart.
> **Aussi** : le partage d'une parole seule — une colonne, la case à 56 % de la largeur, centrée à 44 % de la hauteur (C-097) ; une photo se
> TOURNE à deux doigts, bande d'une fiche (`photoCadre.a`) et photo d'un dessin (`a`) — `redteam_tourne.py` (C-098) ; le bouton recadrer
> porte quatre coins, à 12 pt au-dessus de la barre (C-099). **Au registre, sans rien construire : déplacer une dalle sur sa Toile (C-101, v142).**
> ⚠ **PromiLate n'a pas de capitale accentuée : le É de « TRACE TA MOITIÉ » tombe sur la police suivante.**

"""
S=S.replace(anc,B+anc)
a="python3 redteam_enfonce.py     # 14 — v139 (C-083)"
assert S.count(a)==1
S=S.replace(a,"""python3 redteam_guide.py       # v141 (C-094) : le guide de fin de parcours — stockage vierge, parcours complet au doigt, clair et sombre : flou 0,8 s après l'arrivée, seul le Studio net, puis le + ; toucher ailleurs, « Plus tard », rechargement, mouvement réduit, rejeu. --vite.
python3 redteam_onb_sorties.py # 27 — v141 (C-075) : l'onboarding d'avant v140, mot pour mot (textes en dur), « Plus tard » à chaque étape (12 px, sans soulignement), plus d'étape « principe », la main sur le trait. --r6 pour redteam_engagement.
python3 redteam_murs_toucher.py # 8 — v141 (C-100) : huit murs, vingt touchers répartis sur toute la zone floutée, doigt qui glisse : 20 sur 20. --seul=.
python3 redteam_ritournelle.py # 12 — v141 (C-088) : une parole ≥ 60 % de la largeur ; 2, 3, 4 entières ; au plus deux cellules vides entières. WebKit.
python3 redteam_tourne.py      # 8 — v141 (C-098) : une photo se tourne à deux doigts (bande d'une fiche, dessin), l'angle est mémorisé.
"""+a)
io.open('CLAUDE.md','w',encoding='utf-8').write(S)
